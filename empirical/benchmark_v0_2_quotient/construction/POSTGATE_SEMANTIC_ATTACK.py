#!/usr/bin/env python3
"""Adversarial construction attack for the post-gate semantic contract.

No real future obligation is accessed. The attack tests semantic representation
invariance and sensitivity to genuine q-induced revision merges. It also refuses
to promote the contract while future-distinction grounding remains unidentified.
"""
from __future__ import annotations

import ast
import copy
import json
from itertools import combinations
from pathlib import Path

import POSTGATE_SEMANTIC_KERNEL as sk

HERE = Path(__file__).resolve().parent
CONTRACT = json.loads((HERE / "POSTGATE_SEMANTIC_CONTRACT.json").read_text())
GA = json.loads((HERE / "GAMMA_A.json").read_text())
GB = json.loads((HERE / "GAMMA_B.json").read_text())
OUT = HERE / "postgate_semantic_audit.json"


def partition_signature(p: sk.RevisionPartition):
    return tuple(p.block_by_ref)


def ref_index(gamma):
    return {
        (r["relation_kind"], r["source_fact_id"]): sk.SemanticRef(r["relation_kind"], r["source_fact_id"])
        for r in gamma["path_records"]
    }


def pair_key(x: sk.SemanticRef, y: sk.SemanticRef):
    return tuple(sorted((x.key, y.key)))


def kernel_and_controls():
    pa, pb = sk.canonical_partition(GA), sk.canonical_partition(GB)
    refs = tuple(sorted(pa.refs))
    kernel, controls = [], []
    for x, y in combinations(refs, 2):
        if x.relation_kind != y.relation_kind:
            continue
        merged = pa.block(x) != pa.block(y) and pb.block(x) == pb.block(y)
        (kernel if merged else controls).append((x, y))
    return pa, pb, tuple(kernel), tuple(controls)


def representation_variant(gamma, shift: int, reverse: bool, rename_paths: bool):
    x = copy.deepcopy(gamma)
    labels = sorted(set(x["equivalence_class"].values()))
    rotated = labels[shift % len(labels):] + labels[:shift % len(labels)]
    label_map = {old: f"opaque-class-{i:03d}" for i, old in enumerate(rotated)}
    x["equivalence_class"] = {p: label_map[v] for p, v in x["equivalence_class"].items()}

    if rename_paths:
        path_map = {r["path_id"]: f"opaque-path-{i:03d}" for i, r in enumerate(x["path_records"])}
        for r in x["path_records"]:
            r["path_id"] = path_map[r["path_id"]]
        x["equivalence_class"] = {path_map[p]: v for p, v in x["equivalence_class"].items()}
    if reverse:
        x["path_records"] = list(reversed(x["path_records"]))
    return x


def mixed_rows(kernel):
    statuses = ("DISTINGUISHED", "EQUIVALENT", "NOT_IDENTIFIED")
    return tuple(sk.DistinctionRow(x, y, statuses[i % 3]) for i, (x, y) in enumerate(kernel))


def representation_invariance_attack():
    pa, pb, kernel, _ = kernel_and_controls()
    rows = mixed_rows(kernel)
    base = {
        "A": sk.evaluate_pair_reachability(pa, rows),
        "B": sk.evaluate_pair_reachability(pb, rows),
    }
    mismatches = []
    comparisons = 0
    for arm, gamma in (("A", GA), ("B", GB)):
        for shift in range(8):
            for reverse in (False, True):
                for rename_paths in (False, True):
                    variant = representation_variant(gamma, shift, reverse, rename_paths)
                    pv = sk.canonical_partition(variant)
                    got = sk.evaluate_pair_reachability(pv, rows)
                    comparisons += 1
                    if partition_signature(pv) != partition_signature(pa if arm == "A" else pb) or got != base[arm]:
                        mismatches.append({"arm": arm, "shift": shift, "reverse": reverse, "rename_paths": rename_paths})

    rows_reordered = tuple(reversed(tuple(sk.DistinctionRow(r.right, r.left, r.status) for r in rows)))
    orientation_pass = (
        sk.evaluate_pair_reachability(pa, rows_reordered) == base["A"]
        and sk.evaluate_pair_reachability(pb, rows_reordered) == base["B"]
    )
    return {
        "pass": not mismatches and orientation_pass,
        "metamorphic_partition_evaluator_comparisons": comparisons,
        "mismatch_count": len(mismatches),
        "pair_order_orientation_invariance": orientation_pass,
        "mismatches": mismatches[:10],
    }


def revision_sensitivity_attack():
    pa, pb, kernel, controls = kernel_and_controls()
    kernel_failures = []
    control_failures = []
    for x, y in kernel:
        row = (sk.DistinctionRow(x, y, "DISTINGUISHED"),)
        a = sk.evaluate_pair_reachability(pa, row)[0]
        b = sk.evaluate_pair_reachability(pb, row)[0]
        if not (a["reachable"] is True and b["reachable"] is False):
            kernel_failures.append(pair_key(x, y))
    for x, y in controls:
        row = (sk.DistinctionRow(x, y, "DISTINGUISHED"),)
        a = sk.evaluate_pair_reachability(pa, row)[0]
        b = sk.evaluate_pair_reachability(pb, row)[0]
        if not (a["reachable"] is True and b["reachable"] is True):
            control_failures.append(pair_key(x, y))

    status_failures = []
    for x, y in kernel:
        equivalent = sk.DistinctionRow(x, y, "EQUIVALENT")
        missing = sk.DistinctionRow(x, y, "NOT_IDENTIFIED")
        ea = sk.evaluate_pair_reachability(pa, (equivalent,))[0]
        eb = sk.evaluate_pair_reachability(pb, (equivalent,))[0]
        ma = sk.evaluate_pair_reachability(pa, (missing,))[0]
        mb = sk.evaluate_pair_reachability(pb, (missing,))[0]
        if ea["reachable"] is not False or eb["reachable"] is not False or ma["reachable"] is not None or mb["reachable"] is not None:
            status_failures.append(pair_key(x, y))
    return {
        "pass": not kernel_failures and not control_failures and not status_failures and len(kernel) == 12,
        "q_kernel_pairs": len(kernel),
        "same_kind_nonkernel_control_pairs": len(controls),
        "kernel_pairs_with_A_reachable_B_unreachable": len(kernel) - len(kernel_failures),
        "nonkernel_pairs_reachable_both": len(controls) - len(control_failures),
        "missingness_and_equivalent_semantics_pass": not status_failures,
        "kernel_failures": kernel_failures,
        "control_failures": control_failures,
        "status_failures": status_failures,
    }


def operation_grammar_attack():
    pa, _, _, _ = kernel_and_controls()
    refs = {r.relation_kind: r for r in pa.refs}
    probes = [
        sk.trace(pa, refs["PROVENANCE"]),
        sk.follow(pa, refs["ALTERNATIVE"]),
        sk.challenge(pa, refs["CHALLENGE"]),
        sk.reopen(pa, refs["REOPEN"]),
    ]
    split_rejected = False
    try:
        sk.split(pa, refs["REOPEN"])
    except PermissionError:
        split_rejected = True
    wrong_relation_rejected = False
    try:
        sk.reopen(pa, refs["PROVENANCE"])
    except ValueError:
        wrong_relation_rejected = True
    return {
        "pass": len(probes) == 4 and split_rejected and wrong_relation_rejected,
        "licensed_unary_operations_exercised": [p.operation for p in probes],
        "split_rejected": split_rejected,
        "wrong_relation_operation_rejected": wrong_relation_rejected,
    }


def decoder_prohibition_attack():
    source = (HERE / "POSTGATE_SEMANTIC_KERNEL.py").read_text()
    tree = ast.parse(source)
    compare_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "compare")
    calls = []
    names = set()
    attrs = set()
    for n in ast.walk(compare_node):
        if isinstance(n, ast.Name):
            names.add(n.id)
        if isinstance(n, ast.Attribute):
            attrs.add(n.attr)
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name):
                calls.append(n.func.id)
            elif isinstance(n.func, ast.Attribute):
                calls.append(n.func.attr)
    forbidden_tokens = {
        "hash", "sha", "sha256", "Counter", "ones", "row_sum", "density",
        "singleton", "score", "arm", "treatment", "performance"
    }
    hits = sorted(forbidden_tokens & (names | attrs | set(calls)))
    return {
        "pass": not hits and "len" not in calls and "sum" not in calls and "count" not in calls,
        "forbidden_decoder_hits": hits,
        "compare_calls": sorted(set(calls)),
        "decision_semantics": "partition.block(left) != partition.block(right); no topology summary statistic",
    }


def grounding_gate():
    status = CONTRACT["future_distinction_table"]["grounding_operator_status"]
    return {
        "pass": status != "NOT_IDENTIFIED",
        "status": status,
        "required_domain": CONTRACT["future_distinction_table"]["required_domain"],
        "reason": "A future pair-status table without a frozen treatment-blind grounding operator could itself select the A-favoring kernel distinctions and therefore retains causal authority over the estimand."
    }


def main():
    results = {
        "representation_invariance": representation_invariance_attack(),
        "revision_sensitivity": revision_sensitivity_attack(),
        "operation_grammar": operation_grammar_attack(),
        "decoder_prohibition": decoder_prohibition_attack(),
        "future_grounding": grounding_gate(),
    }
    semantic_algebra_pass = all(results[k]["pass"] for k in (
        "representation_invariance", "revision_sensitivity", "operation_grammar", "decoder_prohibition"
    ))
    overall = semantic_algebra_pass and results["future_grounding"]["pass"]
    out = {
        "benchmark_id": CONTRACT["benchmark_id"],
        "audit_identity": "VFA-0.2-POSTGATE-SEMANTIC-ATTACK-1",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "semantic_algebra_adjudication": "PASS" if semantic_algebra_pass else "FAIL",
        "future_grounding_adjudication": "PASS" if results["future_grounding"]["pass"] else "FAIL",
        "postgate_contract_adjudication": "PASS" if overall else "FAIL",
        "failure_code": None if overall else "FUTURE_DISTINCTION_GROUNDING_NOT_IDENTIFIED",
        "attack_results": results,
        "interpretation": "The reference-based Gamma -> pair-reachability algebra is representation-invariant and sensitive exactly to q-induced revision merges, but H cannot be repaired until the realized future obligation is mapped to the complete q-kernel distinction table by a frozen treatment-blind grounding operator.",
        "authorization_effect": {
            "H": "REMAINS_FAIL",
            "I": "NOT_EVALUATED",
            "E_reaudit": "REQUIRED_AFTER_FINAL_POSTGATE_OPERATOR_IS_IDENTIFIED",
            "F_reaudit": "REQUIRED_AFTER_FINAL_POSTGATE_OPERATOR_IS_IDENTIFIED",
            "G_reaudit": "REQUIRED_IF_FUTURE_EVIDENCE_PACKAGING_OR_GROUNDING_INTERFACE_CHANGES"
        },
        "authority_boundary": {
            "Delta_Pi": "NOT_EVALUATED",
            "kernel_q_subset_kernel_T_future": "NOT_EVALUATED",
            "freeze_packet": "NOT_FROZEN",
            "authorization_certificate": "NOT_ISSUED",
            "future_run": "NOT_AUTHORIZED"
        }
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "semantic_algebra": out["semantic_algebra_adjudication"],
        "future_grounding": out["future_grounding_adjudication"],
        "postgate_contract": out["postgate_contract_adjudication"],
        "representation_comparisons": results["representation_invariance"]["metamorphic_partition_evaluator_comparisons"],
        "kernel_pairs": results["revision_sensitivity"]["q_kernel_pairs"],
        "future_obligation_accessed": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
