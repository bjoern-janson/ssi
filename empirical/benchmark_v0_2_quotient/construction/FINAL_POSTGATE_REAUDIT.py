#!/usr/bin/env python3
"""Fresh E/F re-audit for the consequence-grounded post-gate surface.

Construction-side only. No future obligation is accessed and G is never
activated. Synthetic complete grounding tables exercise the final semantic
coordinate materialization and matrix-only evaluator.
"""
from __future__ import annotations

import ast
import copy
import inspect
import json
from pathlib import Path

import FINAL_TREATMENT_MATERIALIZATION as tm
import FINAL_POSTGATE_RUNTIME as rt

HERE = Path(__file__).resolve().parent
GA = json.loads((HERE / "GAMMA_A.json").read_text())
GB = json.loads((HERE / "GAMMA_B.json").read_text())
COORD = json.loads((HERE / "SEMANTIC_COORDINATE_MAP.json").read_text())["coordinates"]
DOMAIN = json.loads((HERE / "FUTURE_GROUNDING_DOMAIN.json").read_text())
OUT = HERE / "final_postgate_reaudit.json"

FORBIDDEN_RUNTIME_NAMES = {
    "arm", "gamma", "gamma_a", "gamma_b", "path_id", "equivalence_class",
    "class_label", "phi", "phi_path", "outcome", "performance",
}


def rename_representation(gamma: dict, prefix: str, reverse_records: bool) -> dict:
    g = copy.deepcopy(gamma)
    records = list(g["path_records"])
    old_ids = [r["path_id"] for r in records]
    id_map = {old: f"{prefix}-path-{i:02d}" for i, old in enumerate(reversed(old_ids))}
    labels = sorted(set(g["equivalence_class"].values()))
    label_map = {old: f"{prefix}-class-{i:02d}" for i, old in enumerate(reversed(labels))}
    new_eq = {}
    for record in records:
        old = record["path_id"]
        new = id_map[old]
        record["path_id"] = new
        new_eq[new] = label_map[g["equivalence_class"][old]]
    if reverse_records:
        records.reverse()
    g["path_records"] = records
    g["equivalence_class"] = dict(reversed(list(new_eq.items())))
    return g


def grounded(status: str, *, reverse_rows=False, reverse_pairs=False):
    rows = []
    for surface in DOMAIN["path_surfaces"]:
        left = list(surface["left_ref"])
        right = list(surface["right_ref"])
        if reverse_pairs:
            left, right = right, left
        rows.append({
            "unit_id": surface["unit_id"],
            "relation_kind": surface["relation_kind"],
            "left_ref": left,
            "right_ref": right,
            "status": status,
        })
    if reverse_rows:
        rows.reverse()
    return rows


def coordinate_and_materialization_attack():
    ma, ta = tm.compile_semantic_matrix(GA, COORD)
    mb, tb = tm.compile_semantic_matrix(GB, COORD)
    variants = []
    mismatch = []
    for i in range(64):
        va = rename_representation(GA, f"ra{i}", reverse_records=bool(i % 2))
        vb = rename_representation(GB, f"rb{i}", reverse_records=bool((i + 1) % 2))
        xa, txa = tm.compile_semantic_matrix(va, COORD)
        xb, txb = tm.compile_semantic_matrix(vb, COORD)
        variants.append((txa, txb))
        if xa != ma:
            mismatch.append({"i": i, "arm": "A"})
        if xb != mb:
            mismatch.append({"i": i, "arm": "B"})
        if txa != ta or txb != tb:
            mismatch.append({"i": i, "arm": "TRACE"})
    # A must remain the identity relation; B must contain exactly 24 off-diagonal
    # directed equality bytes corresponding to 12 unordered q-kernel pairs.
    off_a = sum(ma[i * 24 + j] for i in range(24) for j in range(24) if i != j)
    off_b = sum(mb[i * 24 + j] for i in range(24) for j in range(24) if i != j)
    expected_trace = (24, 24, 24, 576, 576, 576)
    got_trace_a = (ta.path_record_reads, ta.semantic_coordinate_lookups, ta.class_label_lookups, ta.matrix_comparisons, ta.matrix_writes, ta.output_bytes)
    got_trace_b = (tb.path_record_reads, tb.semantic_coordinate_lookups, tb.class_label_lookups, tb.matrix_comparisons, tb.matrix_writes, tb.output_bytes)
    return {
        "pass": not mismatch and len(ma) == len(mb) == 576 and off_a == 0 and off_b == 24 and got_trace_a == got_trace_b == expected_trace,
        "metamorphic_pairs": 64,
        "mismatch_count": len(mismatch),
        "matrix_bytes_A": len(ma),
        "matrix_bytes_B": len(mb),
        "A_off_diagonal_equality_bytes": off_a,
        "B_off_diagonal_equality_bytes": off_b,
        "materialization_trace_A": got_trace_a,
        "materialization_trace_B": got_trace_b,
    }


def runtime_surface_attack():
    ma, _ = tm.compile_semantic_matrix(GA, COORD)
    mb, _ = tm.compile_semantic_matrix(GB, COORD)
    all_d = grounded("DISTINGUISHED")
    all_e = grounded("EQUIVALENT")
    all_n = grounded("NOT_IDENTIFIED")

    a_d, ta = rt.evaluate_first_endpoint(ma, COORD, DOMAIN, all_d)
    b_d, tb = rt.evaluate_first_endpoint(mb, COORD, DOMAIN, all_d)
    a_e, tea = rt.evaluate_first_endpoint(ma, COORD, DOMAIN, all_e)
    b_e, teb = rt.evaluate_first_endpoint(mb, COORD, DOMAIN, all_e)
    a_n, tna = rt.evaluate_first_endpoint(ma, COORD, DOMAIN, all_n)
    b_n, tnb = rt.evaluate_first_endpoint(mb, COORD, DOMAIN, all_n)

    orientation_mismatch = 0
    order_mismatch = 0
    for status, base_a, base_b in (("DISTINGUISHED", a_d, b_d), ("EQUIVALENT", a_e, b_e), ("NOT_IDENTIFIED", a_n, b_n)):
        oa, ota = rt.evaluate_first_endpoint(ma, COORD, DOMAIN, grounded(status, reverse_pairs=True))
        ob, otb = rt.evaluate_first_endpoint(mb, COORD, DOMAIN, grounded(status, reverse_pairs=True))
        ra, rta = rt.evaluate_first_endpoint(ma, COORD, DOMAIN, grounded(status, reverse_rows=True))
        rb, rtb = rt.evaluate_first_endpoint(mb, COORD, DOMAIN, grounded(status, reverse_rows=True))
        orientation_mismatch += int(oa != base_a or ob != base_b or ota != ta or otb != tb)
        order_mismatch += int(ra != base_a or rb != base_b or rta != ta or rtb != tb)

    reach_a = sum(row["reachable"] is True for row in a_d)
    reach_b = sum(row["reachable"] is True for row in b_d)
    equivalent_false = all(row["reachable"] is False and row["probe_id"] is None for row in a_e + b_e)
    missing_none = all(row["reachable"] is None and row["probe_id"] is None for row in a_n + b_n)
    fixed_trace = (576, 276, 276, 12, 12)
    traces = [ta, tb, tea, teb, tna, tnb]
    traces_tuple = [(x.matrix_bytes_read, x.pair_slots_scanned, x.probe_generation_slots, x.target_surfaces_read, x.target_result_slots_written) for x in traces]
    return {
        "pass": reach_a == 12 and reach_b == 0 and equivalent_false and missing_none and not orientation_mismatch and not order_mismatch and all(x == fixed_trace for x in traces_tuple),
        "DISTINGUISHED_reachable_A": reach_a,
        "DISTINGUISHED_reachable_B": reach_b,
        "EQUIVALENT_no_advantage": equivalent_false,
        "NOT_IDENTIFIED_preserved": missing_none,
        "pair_orientation_mismatches": orientation_mismatch,
        "row_order_mismatches": order_mismatch,
        "runtime_traces": traces_tuple,
    }


def static_exposure_attack():
    fn = rt.evaluate_first_endpoint
    signature = tuple(inspect.signature(fn).parameters)
    expected = ("matrix", "coordinates", "domain", "grounded_surfaces")
    tree = ast.parse(Path(rt.__file__).read_text())
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id.lower() in FORBIDDEN_RUNTIME_NAMES:
            hits.append(node.id)
    # Strings/comments are not executable identifiers; runtime module imports no Gamma module.
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    forbidden_import = any("gamma" in x.lower() for x in imports)
    smuggle = {}
    ma, _ = tm.compile_semantic_matrix(GA, COORD)
    rows = grounded("EQUIVALENT")
    for bad in ("arm", "Gamma", "path_id", "equivalence_class", "Phi_path", "outcome"):
        try:
            rt.evaluate_first_endpoint(ma, COORD, DOMAIN, rows, **{bad: "A"})
            smuggle[bad] = "ACCEPTED"
        except TypeError:
            smuggle[bad] = "REJECTED"
    return {
        "pass": signature == expected and not hits and not forbidden_import and all(x == "REJECTED" for x in smuggle.values()),
        "signature": list(signature),
        "forbidden_identifier_hits": hits,
        "forbidden_import": forbidden_import,
        "smuggling": smuggle,
    }


def common_surface_symmetry_attack():
    # Coordinates and domain are single common objects, not A/B copies.
    coord_keys = set(COORD)
    refs = {
        f"{record['relation_kind']}|{record['source_fact_id']}"
        for record in GA["path_records"]
    }
    refs_b = {
        f"{record['relation_kind']}|{record['source_fact_id']}"
        for record in GB["path_records"]
    }
    domain_refs = {
        _ref
        for s in DOMAIN["path_surfaces"]
        for _ref in (f"{s['left_ref'][0]}|{s['left_ref'][1]}", f"{s['right_ref'][0]}|{s['right_ref'][1]}")
    }
    return {
        "pass": len(COORD) == 24 and set(COORD.values()) == set(range(24)) and refs == refs_b == coord_keys and domain_refs <= coord_keys and len(DOMAIN["path_surfaces"]) == 12,
        "coordinate_count": len(COORD),
        "same_semantic_reference_domain": refs == refs_b == coord_keys,
        "grounding_surface_refs_in_coordinate_domain": domain_refs <= coord_keys,
        "target_surface_count": len(DOMAIN["path_surfaces"]),
    }


def main():
    results = {
        "semantic_coordinate_materialization": coordinate_and_materialization_attack(),
        "fixed_runtime_and_treatment_sensitivity": runtime_surface_attack(),
        "static_exposure_boundary": static_exposure_attack(),
        "common_surface_symmetry": common_surface_symmetry_attack(),
    }
    overall = all(x["pass"] for x in results.values())
    out = {
        "benchmark_id": "VFA-0.2-QUOTIENT-REVISION-TOPOLOGY",
        "audit_identity": "VFA-0.2-FINAL-POSTGATE-EF-REAUDIT-1",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "attack_results": results,
        "E_postgate_reaudit": "PASS" if overall else "FAIL",
        "F_postgate_reaudit": "PASS" if overall else "FAIL",
        "scope": {
            "E": "same fixed logical opportunity around final matrix/evaluator surface; no physical-time equality claim",
            "F": "all remaining A/B output differences are functions of the declared semantic-coordinate equivalence matrix and common grounded statuses; raw representation metadata is blocked",
        },
        "authority_boundary": {
            "G_reaudit": "REQUIRED",
            "H": "REMAINS_FAIL_UNTIL_G_AND_H_READJUDICATED",
            "I": "NOT_EVALUATED",
            "freeze_packet": "NOT_FROZEN",
            "future_run": "NOT_AUTHORIZED",
        },
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"E": out["E_postgate_reaudit"], "F": out["F_postgate_reaudit"], "future_obligation_accessed": False}, indent=2))


if __name__ == "__main__":
    main()
