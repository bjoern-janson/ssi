#!/usr/bin/env python3
"""Independent K0 source -> SSI-IR compiler fidelity audit.

This is the first component permitted to read both the frozen source gold and
the frozen compiled IR. It does not modify source/compiler artifacts.
"""

from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
K0 = HERE.parent
SOURCE = K0 / "source"
COMPILER_DIR = K0 / "compiler"

SOURCE_MANIFEST_SHA256 = "27e5d9675453f36289bee9af8fc020655c9874799905bdac3a2ea700d6207345"
COMPILER_MANIFEST_SHA256 = "de904002f50199349af1d678eb161237ac61149e03c79c7fe24146a0f0fe03c1"
IR_SHA256 = "f551d61884dd26e110e6d2af71a8a911fc5abc812282b974dab0b4b4fe7717d9"
COMPILER_FREEZE_MERGE = "7c419d970eb8235e4352c3f38ac23c8c0c1e6d0f"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def rule(ir, rule_id):
    for r in ir["rules"]:
        if r["id"] == rule_id:
            return r
    raise KeyError(rule_id)


def set_path(obj, path, value):
    cursor = obj
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def apply_mutation(base_ir, mutation):
    ir = copy.deepcopy(base_ir)
    for op in mutation["operations"]:
        if op["op"] == "set_path":
            set_path(ir, op["path"], copy.deepcopy(op["value"]))
        elif op["op"] == "set_rule_field":
            rule(ir, op["rule_id"])[op["field"]] = copy.deepcopy(op["value"])
        elif op["op"] == "remove_rule_requirement":
            r = rule(ir, op["rule_id"])
            r["requirements"] = [
                x for x in r.get("requirements", []) if x != op["requirement"]
            ]
        else:
            raise ValueError(f"unknown mutation op: {op['op']}")
    return ir


def compare_lineage(source_node, ir_node, compiler):
    """Compare source justification tree with compiled trace."""
    stats = {
        "rule_units": 0,
        "rule_units_recovered": 0,
        "evidence_units": 0,
        "evidence_units_recovered": 0,
        "topology_mismatch": 0,
        "rule_ancestry_mismatch": 0,
    }

    def rec(src, dst):
        if src is None:
            if dst is not None:
                stats["topology_mismatch"] += 1
            return
        stats["rule_units"] += 1
        if dst is None:
            stats["topology_mismatch"] += 1
            return

        if src["rule"] == dst.get("source_rule_ancestor"):
            stats["rule_units_recovered"] += 1
        else:
            stats["rule_ancestry_mismatch"] += 1

        expected_evidence = []
        if "lookup" in src:
            expected_evidence.append({
                "kind": "CONTEXT_BINDING",
                "variable": src["lookup"]["variable"],
                "type": compiler.compile_type(src["lookup"]["type"]),
            })
        if "context_extension" in src:
            expected_evidence.append({
                "kind": "CONTEXT_EXTENSION",
                "variable": src["context_extension"]["variable"],
                "type": compiler.compile_type(src["context_extension"]["type"]),
            })

        observed_evidence = dst.get("evidence", [])
        for ev in expected_evidence:
            stats["evidence_units"] += 1
            if ev in observed_evidence:
                stats["evidence_units_recovered"] += 1

        src_children = src.get("premises", [])
        dst_children = dst.get("premises", [])
        if len(src_children) != len(dst_children):
            stats["topology_mismatch"] += 1
        for i, src_child in enumerate(src_children):
            rec(src_child, dst_children[i] if i < len(dst_children) else None)

    rec(source_node, ir_node)
    return stats


def distinction_checks(ir, results_by_id, source_by_id):
    checks = {}
    app = rule(ir, "IR-T-APP")
    test = rule(ir, "IR-T-TEST")
    abs_rule = rule(ir, "IR-T-ABS")
    var_rule = rule(ir, "IR-T-VAR")

    structural = {
        "DIST-001": (
            ir["context"]["lookup"] == "LATEST_EXACT_VARIABLE_NAME"
            and "EXACT_CONTEXT_BINDING" in var_rule["requirements"]
        ),
        "DIST-002": (
            ir["type_system"]["equality"] == "STRUCTURAL_EXACT"
            and set(ir["type_system"]["constructors"]) == {"BOOL", "ARROW"}
        ),
        "DIST-003": "FUNCTION_HAS_ARROW_TYPE" in app["requirements"],
        "DIST-004": "ARGUMENT_MATCHES_ARROW_DOMAIN" in app["requirements"],
        "DIST-005": "GUARD_HAS_BOOL_TYPE" in test["requirements"],
        "DIST-006": "BRANCH_TYPES_EQUAL" in test["requirements"],
        "DIST-007": (
            ir["context"]["extension"] == "APPEND_BINDING_SHADOWS_EARLIER"
            and "EXTEND_CONTEXT_WITH_BINDER" in abs_rule["requirements"]
        ),
        "DIST-008": (
            ir["type_system"]["constructors"]["ARROW"]["ordered_fields"]
            == ["domain", "codomain"]
            and "FUNCTION_HAS_ARROW_TYPE" in app["requirements"]
            and "ARGUMENT_MATCHES_ARROW_DOMAIN" in app["requirements"]
        ),
    }

    witness_map = {
        d["id"]: d["witness_cases"]
        for d in json.loads((SOURCE / "distinctions.json").read_text())["distinctions"]
    }

    for dist_id in sorted(witness_map):
        witness_decisions_preserved = all(
            results_by_id[cid]["judgment"] == source_by_id[cid]["judgment"]
            for cid in witness_map[dist_id]
        )
        checks[dist_id] = {
            "structural_recoverable": structural[dist_id],
            "witness_decisions_preserved": witness_decisions_preserved,
            "recoverable": structural[dist_id] and witness_decisions_preserved,
            "witness_cases": witness_map[dist_id],
        }
    return checks


def audit_variant(name, ir, tasks, gold, compiler, evaluator):
    compiled = {}
    unrepresentable = []
    for case in tasks:
        try:
            compiled[case["id"]] = compiler.compile_query(case)
        except Exception as exc:
            unrepresentable.append({"id": case["id"], "error": type(exc).__name__})

    observed = {}
    for cid, query in compiled.items():
        observed[cid] = evaluator.evaluate_query(query, ir)

    source_by_id = {x["id"]: x for x in gold}
    tp = fp = fn = tn = 0
    judgment_mismatches = []
    for cid, result in observed.items():
        src = source_by_id[cid]["judgment"]
        obs = result["judgment"]
        if src and obs:
            tp += 1
        elif (not src) and obs:
            fp += 1
            judgment_mismatches.append({"id": cid, "class": "COMPILATION_OVERREACH"})
        elif src and (not obs):
            fn += 1
            judgment_mismatches.append({"id": cid, "class": "COMPILATION_LOSS"})
        else:
            tn += 1

    lineage = {
        "rule_units": 0,
        "rule_units_recovered": 0,
        "evidence_units": 0,
        "evidence_units_recovered": 0,
        "topology_mismatch": 0,
        "rule_ancestry_mismatch": 0,
        "fabrication_count": 0,
        "cases_checked": 0,
    }
    lineage_case_mismatches = []

    for src in gold:
        if not src["judgment"]:
            continue
        cid = src["id"]
        if cid not in observed or not observed[cid]["judgment"]:
            continue
        lineage["cases_checked"] += 1
        stats = compare_lineage(src["derivation"], observed[cid]["derivation"], compiler)
        for key in [
            "rule_units", "rule_units_recovered", "evidence_units",
            "evidence_units_recovered", "topology_mismatch",
            "rule_ancestry_mismatch",
        ]:
            lineage[key] += stats[key]
        if stats["topology_mismatch"] or stats["rule_ancestry_mismatch"]:
            lineage_case_mismatches.append({"id": cid, **stats})
        lineage["fabrication_count"] += len(
            observed[cid].get("fabricated_justification", [])
        )

    basis_total = lineage["rule_units"] + lineage["evidence_units"]
    basis_recovered = (
        lineage["rule_units_recovered"] + lineage["evidence_units_recovered"]
    )
    lineage["recovery_rate"] = 1.0 if basis_total == 0 else basis_recovered / basis_total
    lineage["rule_ancestry_accuracy"] = (
        1.0 if lineage["rule_units"] == 0
        else lineage["rule_units_recovered"] / lineage["rule_units"]
    )

    dist = distinction_checks(ir, observed, source_by_id)
    dist_loss = [d for d, c in dist.items() if not c["recoverable"]]

    detections = []
    if unrepresentable:
        detections.append("COMPILATION_INADEQUATE")
    if fp:
        detections.append("COMPILATION_OVERREACH")
    if fn:
        detections.append("COMPILATION_LOSS")
    for d in dist_loss:
        detections.append(f"DISTINCTION_LOSS:{d}")
    if lineage["rule_ancestry_mismatch"] or lineage["topology_mismatch"]:
        detections.append("LINEAGE_MISMATCH")
    if lineage["fabrication_count"]:
        detections.append("LINEAGE_FABRICATION")

    return {
        "variant": name,
        "representability": {
            "representable": len(compiled),
            "total": len(tasks),
            "A_comp": len(compiled) / len(tasks),
            "unrepresentable": unrepresentable,
        },
        "judgment": {
            "TP": tp,
            "FP_compilation_overreach": fp,
            "FN_compilation_loss": fn,
            "TN": tn,
            "accuracy": (tp + tn) / len(tasks),
            "mismatches": judgment_mismatches,
        },
        "distinctions": {
            "checks": dist,
            "loss": dist_loss,
        },
        "lineage": {
            **lineage,
            "case_mismatches": lineage_case_mismatches,
        },
        "detections": sorted(set(detections)),
    }


def main():
    assert sha256(SOURCE / "MANIFEST.json") == SOURCE_MANIFEST_SHA256
    assert sha256(COMPILER_DIR / "MANIFEST.json") == COMPILER_MANIFEST_SHA256
    assert sha256(COMPILER_DIR / "IR.json") == IR_SHA256

    compiler = load_module("k0_compiler_frozen", COMPILER_DIR / "compiler.py")
    evaluator = load_module("k0_ir_evaluator_frozen", COMPILER_DIR / "ir_evaluator.py")

    tasks = json.loads((SOURCE / "TASKS.json").read_text())["cases"]
    gold = json.loads((SOURCE / "gold" / "GOLD.json").read_text())["cases"]
    base_ir = json.loads((COMPILER_DIR / "IR.json").read_text())
    mutations = json.loads((COMPILER_DIR / "mutations.json").read_text())["mutations"]

    baseline = audit_variant("BASELINE", base_ir, tasks, gold, compiler, evaluator)

    baseline_strong = (
        baseline["representability"]["A_comp"] == 1.0
        and baseline["judgment"]["FP_compilation_overreach"] == 0
        and baseline["judgment"]["FN_compilation_loss"] == 0
        and baseline["distinctions"]["loss"] == []
        and baseline["lineage"]["fabrication_count"] == 0
        and baseline["lineage"]["topology_mismatch"] == 0
        and baseline["lineage"]["rule_ancestry_mismatch"] == 0
        and baseline["lineage"]["recovery_rate"] == 1.0
    )

    mutation_results = []
    for mutation in mutations:
        mutated_ir = apply_mutation(base_ir, mutation)
        result = audit_variant(
            mutation["id"], mutated_ir, tasks, gold, compiler, evaluator
        )
        observed = set(result["detections"])
        expected = set(mutation["expected_detection"])
        result["mutation_name"] = mutation["name"]
        result["expected_detection"] = mutation["expected_detection"]
        result["expected_locus"] = mutation["expected_locus"]
        result["expected_detection_satisfied"] = expected <= observed
        mutation_results.append(result)

    caught = sum(1 for x in mutation_results if x["expected_detection_satisfied"])

    if baseline_strong and caught == len(mutation_results):
        status = "K0_COMPILER_AUDIT_STRONG_PASS"
    elif baseline_strong:
        status = "K0_COMPILER_CONFORMANCE_PASS_AUDIT_SENSITIVITY_PARTIAL"
    else:
        status = "K0_COMPILER_CONFORMANCE_FAILED"

    output = {
        "object": "K0-SOURCE-TYPE-SYSTEM-COMPILER/FIRST_FIDELITY_AUDIT",
        "compiler_freeze_merge": COMPILER_FREEZE_MERGE,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "compiler_manifest_sha256": COMPILER_MANIFEST_SHA256,
        "ir_sha256": IR_SHA256,
        "prospective_status": status,
        "baseline_strong_pass": baseline_strong,
        "baseline": baseline,
        "mutation_sensitivity": {
            "caught": caught,
            "total": len(mutation_results),
            "all_expected_detections_satisfied": caught == len(mutation_results),
            "results": mutation_results,
        },
        "authority_ceiling": {
            "compiler_conformance_in_K0_can_be_supported": status == "K0_COMPILER_AUDIT_STRONG_PASS",
            "compiler_generalization_established": False,
            "ssi_calc_external_niche_advantage_established": False,
            "R1_R11_modified": False,
        },
    }

    out_path = HERE / "K0_AUDIT_FIRST_RUN.json"
    out_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")

    summary = {
        "object": output["object"],
        "prospective_status": status,
        "baseline": {
            "A_comp": baseline["representability"]["A_comp"],
            "accuracy": baseline["judgment"]["accuracy"],
            "compilation_overreach": baseline["judgment"]["FP_compilation_overreach"],
            "compilation_loss": baseline["judgment"]["FN_compilation_loss"],
            "distinction_loss": baseline["distinctions"]["loss"],
            "rule_ancestry_accuracy": baseline["lineage"]["rule_ancestry_accuracy"],
            "lineage_recovery_rate": baseline["lineage"]["recovery_rate"],
            "lineage_fabrication": baseline["lineage"]["fabrication_count"],
            "lineage_topology_mismatch": baseline["lineage"]["topology_mismatch"],
        },
        "mutations_caught": f"{caught}/{len(mutation_results)}",
        "mutation_detections": [
            {
                "id": x["variant"],
                "name": x["mutation_name"],
                "expected_satisfied": x["expected_detection_satisfied"],
                "detections": x["detections"],
            }
            for x in mutation_results
        ],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
