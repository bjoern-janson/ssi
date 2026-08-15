#!/usr/bin/env python3
"""Construction-side adversarial attack for consequence-grounded J_future.

No future Biome release is fetched or run. Synthetic repeated migration outcomes
exercise the grounding algebra. Immutable pre-freeze manifests are checked for
complete q-kernel coverage and witness provenance.
"""
from __future__ import annotations

import ast
import inspect
import json
from pathlib import Path

import FUTURE_CONSEQUENCE_GROUNDING_KERNEL as gk
import FUTURE_WITNESS_EXTRACTOR as wx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DOMAIN = json.loads((HERE / "FUTURE_GROUNDING_DOMAIN.json").read_text())
WITNESSES = json.loads((HERE / "FUTURE_CONSEQUENCE_WITNESSES.json").read_text())
W = json.loads((HERE / "VALIDATED_SUBSTRATE.json").read_text())
GA = json.loads((HERE / "GAMMA_A.json").read_text())
GB = json.loads((HERE / "GAMMA_B.json").read_text())
SOURCE_MANIFEST = (ROOT / "benchmark_v0_1" / "evidence" / "B_SOURCE_MANIFEST.md").read_text()
OUT = HERE / "future_consequence_grounding_audit.json"

FORBIDDEN = {
    "arm", "treatment", "gamma", "gamma_a", "gamma_b", "m_gamma", "phi", "phi_path",
    "reach", "deltapi", "delta_pi", "outcome", "score", "performance",
}


def _run(files, *, completed=True, exit_code=0):
    payload = None if files is None else tuple(sorted(files.items()))
    return gk.MigrationRun(completed=completed, exit_code=exit_code, files=payload)


def _json(obj, *, pretty=False, reverse=False):
    if reverse and isinstance(obj, dict):
        obj = {k: obj[k] for k in reversed(list(obj))}
    if pretty:
        return json.dumps(obj, ensure_ascii=False, indent=2).encode()
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode()


def static_independence_attack():
    expected = {
        "consequence_signature": ("baseline_files", "run_1", "run_2"),
        "ground_status": ("left", "right"),
        "ground_table": ("domain", "consequence_by_fact"),
        "lift_path_surfaces": ("domain", "grounding_rows"),
        "future_kernel_adjudication": ("grounding_rows",),
    }
    signatures = {}
    signature_ok = True
    smuggling = {}
    for name, params in expected.items():
        fn = getattr(gk, name)
        got = tuple(inspect.signature(fn).parameters)
        signatures[name] = list(got)
        signature_ok &= got == params

    tree = ast.parse(Path(gk.__file__).read_text())
    hits = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in expected:
            names = {n.id.lower() for n in ast.walk(node) if isinstance(n, ast.Name)}
            args = {a.arg.lower() for a in node.args.args}
            hits[node.name] = sorted((names | args) & FORBIDDEN)

    base = {"biome.json": b'{"x":1}'}
    good = _run({"biome.json": b'{"x":2}'})
    for bad in ("arm", "Gamma", "M_Gamma", "Phi_path", "DeltaPi", "outcome", "performance"):
        try:
            gk.consequence_signature(base, good, good, **{bad: "A"})
            smuggling[bad] = "ACCEPTED"
        except TypeError:
            smuggling[bad] = "REJECTED"

    return {
        "pass": signature_ok and all(not v for v in hits.values()) and all(v == "REJECTED" for v in smuggling.values()),
        "signatures": signatures,
        "forbidden_name_hits": hits,
        "smuggling": smuggling,
    }


def domain_completeness_attack():
    record = {r["path_id"]: (r["relation_kind"], r["source_fact_id"]) for r in GA["path_records"]}
    ids = sorted(record)
    kernel = []
    for i, x in enumerate(ids):
        for y in ids[i + 1:]:
            if GA["equivalence_class"][x] != GA["equivalence_class"][y] and GB["equivalence_class"][x] == GB["equivalence_class"][y]:
                left, right = record[x], record[y]
                if left[0] != right[0]:
                    raise AssertionError("q kernel unexpectedly merges relation kinds")
                kernel.append((left[0], tuple(sorted((left[1], right[1])))))

    manifest_surfaces = {
        (s["relation_kind"], tuple(sorted((s["left_ref"][1], s["right_ref"][1]))))
        for s in DOMAIN["path_surfaces"]
    }
    kernel_set = set(kernel)
    derived_units = {pair for _, pair in kernel_set}
    manifest_units = {
        tuple(sorted((u["left_fact_id"], u["right_fact_id"])))
        for u in DOMAIN["grounding_units"]
    }
    counts = {"kernel_path_pairs": len(kernel), "unique_grounding_units": len(derived_units), "manifest_path_surfaces": len(DOMAIN["path_surfaces"])}
    return {
        "pass": len(kernel) == 12 and kernel_set == manifest_surfaces and derived_units == manifest_units and len(derived_units) == 3,
        **counts,
        "relation_kind_surface_multiplier": len(kernel) // len(derived_units),
        "surface_independence_claim": False,
    }


def witness_manifest_attack():
    facts = {f["fact_id"] for f in W["facts"]}
    rows = WITNESSES["witnesses"]
    witness_facts = [r["fact_id"] for r in rows]
    source_refs_present = all(r["snapshot"] in SOURCE_MANIFEST and r["git_blob_sha1"] in SOURCE_MANIFEST for r in rows)
    expected_mode = {
        "case:ariakit": wx.WRITTEN_FILE_BLOCKS,
        "case:aws": wx.WRITTEN_FILE_BLOCKS,
        "case:issue_5465": wx.WRITTEN_FILE_BLOCKS,
        "case:knip": wx.WRITTEN_FILE_BLOCKS,
        "case:nested": wx.DRY_RUN_PROPOSED_OUTPUTS,
        "case:sentry": wx.WRITTEN_FILE_BLOCKS,
    }
    mode_ok = all(r["extraction_mode"] == expected_mode[r["fact_id"]] for r in rows)
    path_ok = all(r["expected_paths"] for r in rows) and next(r for r in rows if r["fact_id"] == "case:nested")["expected_paths"] == ["bar/biome.json", "biome.json", "foo/biome.json"]
    return {
        "pass": set(witness_facts) == facts and len(witness_facts) == len(set(witness_facts)) == 6 and source_refs_present and mode_ok and path_ok,
        "fact_count": len(witness_facts),
        "all_W_facts_covered": set(witness_facts) == facts,
        "source_manifest_blob_refs_present": source_refs_present,
        "nested_full_filesystem_paths_frozen": path_ok,
    }


def extractor_attack():
    written = '''---\n## `biome.json`\n\n```json\n{ "b": 2, "a": 1 }\n```\n\n## `pkg/biome.json`\n\n```json\n{\n  "x": [1, 2]\n}\n```\n'''
    got_written = wx.extract_cutoff_files(written, wx.WRITTEN_FILE_BLOCKS)
    written_ok = set(got_written) == {"biome.json", "pkg/biome.json"} and got_written["biome.json"] == b'{"a":1,"b":2}'

    nested = '''---\n# Emitted Messages\n\n```block\n<TEMP_DIR>/should_migrate_nested_config/bar/biome.json migrate ---\n\n  - {\u00b7"old":\u00b7true}\n  + {\u00b7"root":\u00b7false,"linter":\u00b7{\u00b7"rules":\u00b7{\u00b7"preset":\u00b7"none"\u00b7}\u00b7}\u00b7}\n\n```\n\n```block\n<TEMP_DIR>/should_migrate_nested_config/biome.json migrate ---\n\n  - {\u00b7"old":\u00b7true}\n  + {\u00b7"linter":\u00b7{\u00b7"rules":\u00b7{\u00b7"preset":\u00b7"none"\u00b7}\u00b7}\u00b7}\n\n```\n\n```block\n<TEMP_DIR>/should_migrate_nested_config/foo/biome.json migrate ---\n\n  - {\u00b7"old":\u00b7true}\n  + {\u00b7"root":\u00b7false,"linter":\u00b7{\u00b7"rules":\u00b7{\u00b7"preset":\u00b7"none"\u00b7}\u00b7}\u00b7}\n\n```\n'''
    got_nested = wx.extract_cutoff_files(nested, wx.DRY_RUN_PROPOSED_OUTPUTS)
    nested_ok = set(got_nested) == {"bar/biome.json", "biome.json", "foo/biome.json"}
    middle_dot_ok = json.loads(got_nested["bar/biome.json"])["root"] is False

    invalid_mode_rejected = False
    try:
        wx.extract_cutoff_files(written, "UNKNOWN")
    except ValueError:
        invalid_mode_rejected = True
    return {
        "pass": written_ok and nested_ok and middle_dot_ok and invalid_mode_rejected,
        "written_multifile_extraction": written_ok,
        "dry_run_multifile_extraction": nested_ok,
        "snapshot_middle_dot_reversal": middle_dot_ok,
        "unknown_mode_rejected": invalid_mode_rejected,
    }


def effect_semantics_attack():
    equal_effect = 0
    distinguished_effect = 0
    representation_mismatches = 0
    for i in range(128):
        base_l = {"biome.json": _json({"pre": i, "target": i, "stable": {"k": i % 7}})}
        base_r = {"biome.json": _json({"pre": i + 10000, "target": i + 5000, "stable": {"k": (i + 3) % 7}})}
        future_l_obj = {"pre": i, "target": 777, "stable": {"k": i % 7}}
        future_r_same_obj = {"pre": i + 10000, "target": 777, "stable": {"k": (i + 3) % 7}}
        future_r_diff_obj = {"pre": i + 10000, "target": 778, "stable": {"k": (i + 3) % 7}}

        l1 = _run({"biome.json": _json(future_l_obj, pretty=True)})
        l2 = _run({"biome.json": _json(future_l_obj, reverse=True)})
        rs1 = _run({"biome.json": _json(future_r_same_obj, pretty=True)})
        rs2 = _run({"biome.json": _json(future_r_same_obj, reverse=True)})
        rd = _run({"biome.json": _json(future_r_diff_obj)})

        cl = gk.consequence_signature(base_l, l1, l2)
        cr_same = gk.consequence_signature(base_r, rs1, rs2)
        cr_diff = gk.consequence_signature(base_r, rd, rd)
        if cl.status != gk.IDENTIFIED or cr_same.status != gk.IDENTIFIED:
            representation_mismatches += 1
            continue
        if gk.ground_status(cl, cr_same) == gk.EQUIVALENT:
            equal_effect += 1
        if gk.ground_status(cl, cr_diff) == gk.DISTINGUISHED:
            distinguished_effect += 1

    # Array order is intentionally semantic.
    base = {"biome.json": b'{"a":[1,2]}'}
    ca = gk.consequence_signature(base, _run({"biome.json": b'{"a":[2,1]}'}), _run({"biome.json": b'{"a":[2,1]}'}))
    cb = gk.consequence_signature(base, _run({"biome.json": b'{"a":[1,2]}'}), _run({"biome.json": b'{"a":[1,2]}'}))
    array_semantic = gk.ground_status(ca, cb) == gk.DISTINGUISHED

    return {
        "pass": equal_effect == 128 and distinguished_effect == 128 and representation_mismatches == 0 and array_semantic,
        "equal_effect_despite_different_prehistory": equal_effect,
        "different_future_effect_detected": distinguished_effect,
        "representation_mismatches": representation_mismatches,
        "array_order_preserved_as_semantic": array_semantic,
    }


def fail_closed_attack():
    base = {"biome.json": b'{"x":1}'}
    good = _run({"biome.json": b'{"x":2}'})
    cases = {
        "not_completed": _run({"biome.json": b'{"x":2}'}, completed=False),
        "nonzero_exit": _run({"biome.json": b'{"x":2}'}, exit_code=1),
        "missing_files": _run(None),
        "path_set_drift": _run({"other.json": b'{"x":2}'}),
        "parse_failure": _run({"biome.json": b'{not-json'}),
        "nondeterministic": _run({"biome.json": b'{"x":3}'})
    }
    results = {}
    results["not_completed"] = gk.consequence_signature(base, cases["not_completed"], good).status
    results["nonzero_exit"] = gk.consequence_signature(base, cases["nonzero_exit"], good).status
    results["missing_files"] = gk.consequence_signature(base, cases["missing_files"], good).status
    results["path_set_drift"] = gk.consequence_signature(base, cases["path_set_drift"], cases["path_set_drift"]).status
    results["parse_failure"] = gk.consequence_signature(base, cases["parse_failure"], cases["parse_failure"]).status
    results["nondeterministic"] = gk.consequence_signature(base, good, cases["nondeterministic"]).status
    return {"pass": all(v == gk.NOT_IDENTIFIED for v in results.values()), "results": results}


def table_and_kernel_attack():
    eq = gk.Consequence(gk.IDENTIFIED, "[]", "0", None)
    d1 = gk.Consequence(gk.IDENTIFIED, '[{"op":"ADD","path":"/x","after":1}]', "1", None)
    d2 = gk.Consequence(gk.IDENTIFIED, '[{"op":"ADD","path":"/x","after":2}]', "2", None)

    all_eq = {f["fact_id"]: eq for f in W["facts"]}
    rows_eq = gk.ground_table(DOMAIN, all_eq)
    surfaces_eq = gk.lift_path_surfaces(DOMAIN, rows_eq)

    one_dist = dict(all_eq)
    one_dist["case:ariakit"] = d1
    one_dist["case:aws"] = d2
    rows_dist = gk.ground_table(DOMAIN, one_dist)

    one_missing = dict(all_eq)
    del one_missing["case:nested"]
    rows_missing = gk.ground_table(DOMAIN, one_missing)

    lift_counts = {u["unit_id"]: 0 for u in DOMAIN["grounding_units"]}
    for row in surfaces_eq:
        lift_counts[row["unit_id"]] += 1

    return {
        "pass": (
            len(rows_eq) == 3 and len(surfaces_eq) == 12 and all(v == 4 for v in lift_counts.values())
            and gk.future_kernel_adjudication(rows_eq) == "INCLUSION_ON_FROZEN_KERNEL_DOMAIN"
            and gk.future_kernel_adjudication(rows_dist) == "NONINCLUSION_WITNESS"
            and gk.future_kernel_adjudication(rows_missing) == gk.NOT_IDENTIFIED
            and any(r["status"] == gk.NOT_IDENTIFIED for r in rows_missing)
        ),
        "grounding_rows": len(rows_eq),
        "lifted_path_surfaces": len(surfaces_eq),
        "surfaces_per_grounding_unit": lift_counts,
        "all_equivalent_adjudication": gk.future_kernel_adjudication(rows_eq),
        "one_distinguished_adjudication": gk.future_kernel_adjudication(rows_dist),
        "missing_adjudication": gk.future_kernel_adjudication(rows_missing),
        "missing_row_preserved": any(r["status"] == gk.NOT_IDENTIFIED for r in rows_missing),
    }


def main():
    results = {
        "static_independence": static_independence_attack(),
        "domain_completeness": domain_completeness_attack(),
        "witness_manifest": witness_manifest_attack(),
        "extractor_semantics": extractor_attack(),
        "effect_semantics": effect_semantics_attack(),
        "fail_closed": fail_closed_attack(),
        "table_and_kernel": table_and_kernel_attack(),
    }
    overall = all(x["pass"] for x in results.values())
    out = {
        "benchmark_id": "VFA-0.2-QUOTIENT-REVISION-TOPOLOGY",
        "audit_identity": "VFA-0.2-FUTURE-CONSEQUENCE-GROUNDING-ATTACK-1",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "attack_results": results,
        "grounding_contract_adjudication": "PASS" if overall else "FAIL",
        "scope": {
            "realized_future_execution": "NOT_PERFORMED",
            "attack_data": "pre-freeze manifests plus synthetic migration outcomes only",
            "claim": "construction identifies a treatment-blind consequence-to-distinction rule; realized future conformance remains prospective"
        },
        "authority_boundary": {
            "realized_T_future": "NOT_EVALUATED",
            "realized_J_future": "NOT_EVALUATED",
            "H": "REMAINS_FAIL_UNTIL_AFFECTED_E_F_G_READJUDICATION_AND_H_REAUDIT",
            "I": "NOT_EVALUATED",
            "freeze_packet": "NOT_FROZEN",
            "authorization_certificate": "NOT_ISSUED",
            "future_run": "NOT_AUTHORIZED"
        }
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "grounding_contract": out["grounding_contract_adjudication"],
        "q_kernel_path_pairs": results["domain_completeness"]["kernel_path_pairs"],
        "grounding_units": results["domain_completeness"]["unique_grounding_units"],
        "equal_effect_tests": results["effect_semantics"]["equal_effect_despite_different_prehistory"],
        "distinct_effect_tests": results["effect_semantics"]["different_future_effect_detected"],
        "future_obligation_accessed": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
