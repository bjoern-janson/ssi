#!/usr/bin/env python3
"""VFA-0.2 pre-activation noninterference attack.

Construction-audit machinery only. No prospective future obligation is read.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import inspect
import itertools
import json
from collections import Counter
from pathlib import Path

import reserve_interface as ri

HERE = Path(__file__).resolve().parent
SHARED = json.loads((HERE / "SHARED_FORWARD.json").read_text())
RESERVE_A = json.loads((HERE / "reserve_A.json").read_text())
RESERVE_B = json.loads((HERE / "reserve_B.json").read_text())
OUT = HERE / "preactivation_leakage_audit.json"

TRACE_FIELDS = ["I", "A", "C", "pi", "E", "S", "M", "L", "tau", "R", "O"]
FORBIDDEN = {"reserve", "reserve_a", "reserve_b", "reserve_handle", "reserve_path", "d", "d_t"}


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def sha256_obj(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def surrogate_universe():
    universe = sorted(SHARED["transformation_classes"])
    historical = [set(v) for v in SHARED["cases"].values()]
    out = []
    for r in range(1, len(universe) + 1):
        for comb in itertools.combinations(universe, r):
            s = set(comb)
            if not any(s == h for h in historical):
                out.append(list(comb))
    return out


def static_boundary():
    tree = ast.parse(Path(ri.__file__).read_text())
    wanted = {"forward_trace", "evaluate_gate"}
    detail = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in wanted:
            args = [a.arg for a in node.args.args]
            names = {n.id.lower() for n in ast.walk(node) if isinstance(n, ast.Name)}
            attrs = {n.attr.lower() for n in ast.walk(node) if isinstance(n, ast.Attribute)}
            bad = sorted(
                x for x in (names | attrs | {a.lower() for a in args})
                if x in FORBIDDEN or x.startswith("reserve")
            )
            detail[node.name] = {
                "args": args,
                "forbidden_reserve_symbols": bad,
                "pass": not bad,
            }
    signature_pass = (
        list(inspect.signature(ri.forward_trace).parameters) == ["query", "shared_forward"]
        and list(inspect.signature(ri.evaluate_gate).parameters) == ["evidence"]
    )
    return {
        "signature_pass": signature_pass,
        "functions": detail,
        "pass": signature_pass and all(v["pass"] for v in detail.values()),
    }


def reserve_payload_symmetry():
    kinds_a = sorted(RESERVE_A["bindings"])
    kinds_b = sorted(RESERVE_B["bindings"])
    same_sources = all(
        sorted(RESERVE_A["bindings"][k]) == sorted(RESERVE_B["bindings"][k])
        for k in kinds_a
    )
    same_target_multisets = all(
        Counter(RESERVE_A["bindings"][k].values())
        == Counter(RESERVE_B["bindings"][k].values())
        for k in kinds_a
    )
    result = {
        "same_cases": RESERVE_A["cases"] == RESERVE_B["cases"],
        "same_binding_kinds": kinds_a == kinds_b,
        "same_edge_count": sum(len(v) for v in RESERVE_A["bindings"].values())
        == sum(len(v) for v in RESERVE_B["bindings"].values()),
        "same_source_multisets": same_sources,
        "same_target_multisets": same_target_multisets,
        "same_canonical_byte_length": len(canonical(RESERVE_A)) == len(canonical(RESERVE_B)),
        "canonical_bytes_A": len(canonical(RESERVE_A)),
        "canonical_bytes_B": len(canonical(RESERVE_B)),
    }
    result["pass"] = all(
        result[k]
        for k in [
            "same_cases",
            "same_binding_kinds",
            "same_edge_count",
            "same_source_multisets",
            "same_target_multisets",
            "same_canonical_byte_length",
        ]
    )
    return result


def reserve_phi(reserve):
    cases = reserve["cases"]
    b = reserve["bindings"]

    def aligned(kind):
        return sum(src == tgt for src, tgt in b[kind].items()) / len(cases)

    return {
        "C_challenge": aligned("CHALLENGE"),
        "L_prov": aligned("PROVENANCE"),
        # Presence/quantity, not binding quality: both arms preserve one
        # alternative binding per route.
        "A_preserve": len(b["ALTERNATIVE"]) / len(cases),
        "R_reopen": aligned("REOPEN"),
    }


def reserve_variants(reserve):
    variants = {"canonical": copy.deepcopy(reserve)}

    x = copy.deepcopy(reserve)
    x["cases"] = list(reversed(x["cases"]))
    variants["case_order_reversed"] = x

    x = copy.deepcopy(reserve)
    x["bindings"] = dict(reversed(list(x["bindings"].items())))
    variants["binding_kind_order_reversed"] = x

    x = copy.deepcopy(reserve)
    x["audit_padding"] = "X" * 8192
    variants["large_serialization_padding"] = x

    x = copy.deepcopy(reserve)
    x["metadata"] = {
        "logging_label": "RESERVE_PRESENT",
        "candidate_identity_noise": ["unused", "dormant", "objects"],
        "stopping_hint": "MUST_NOT_BE_READ",
    }
    variants["adversarial_metadata"] = x
    return variants


def trace_noninterference(tasks):
    variants = {
        **{f"A/{k}": v for k, v in reserve_variants(RESERVE_A).items()},
        **{f"B/{k}": v for k, v in reserve_variants(RESERVE_B).items()},
    }
    mismatches = []
    for task in tasks:
        reference = ri.forward_trace(task, SHARED)
        if list(reference) != TRACE_FIELDS:
            raise AssertionError("trace schema drift")
        for label, dormant_reference in variants.items():
            # Keep the reserve live in the calling frame, but do not pass any
            # reserve-capable reference into the forward subsystem.
            trace = ri.forward_trace(task, SHARED)
            if trace != reference:
                mismatches.append(
                    {
                        "task": task,
                        "variant": label,
                        "reference_sha256": sha256_obj(reference),
                        "trace_sha256": sha256_obj(trace),
                        "dormant_sha256": sha256_obj(dormant_reference),
                    }
                )
                break
    return {
        "tasks": len(tasks),
        "reserve_variants_per_arm": 5,
        "comparisons": len(tasks) * len(variants),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:10],
        "pass": not mismatches,
    }


def gate_noninterference():
    cases = [
        (
            {
                "validator_status": "PASS",
                "failure_scope": "CURRENT_ROUTE",
                "independent_validator": True,
                "validator_id": "v1",
            },
            False,
        ),
        (
            {
                "validator_status": "FAIL",
                "failure_scope": "OTHER",
                "independent_validator": True,
                "validator_id": "v1",
            },
            False,
        ),
        (
            {
                "validator_status": "FAIL",
                "failure_scope": "CURRENT_ROUTE",
                "independent_validator": False,
                "validator_id": "v1",
            },
            False,
        ),
        (
            {
                "validator_status": "FAIL",
                "failure_scope": "CURRENT_ROUTE",
                "independent_validator": True,
                "validator_id": "",
            },
            False,
        ),
        (
            {
                "validator_status": "FAIL",
                "failure_scope": "CURRENT_ROUTE",
                "independent_validator": True,
                "validator_id": "v1",
            },
            True,
        ),
    ]
    mismatches = []
    for idx, (evidence, expected) in enumerate(cases):
        for arm, dormant_reference in [("A", RESERVE_A), ("B", RESERVE_B)]:
            got = ri.evaluate_gate(evidence)
            if got != expected:
                mismatches.append(
                    {
                        "case": idx,
                        "arm": arm,
                        "expected": expected,
                        "got": got,
                        "dormant_sha256": sha256_obj(dormant_reference),
                    }
                )
    dereference_violations = []
    closed_evidence = cases[0][0]
    for arm, reserve in [("A", RESERVE_A), ("B", RESERVE_B)]:
        try:
            ri.activate_reserve(closed_evidence, reserve)
            dereference_violations.append(arm)
        except ri.ReserveClosed:
            pass
    return {
        "gate_cases": len(cases),
        "arm_comparisons": len(cases) * 2,
        "mismatch_count": len(mismatches),
        "closed_gate_dereference_violations": dereference_violations,
        "pass": not mismatches and not dereference_violations,
    }


def q_adapt(tasks):
    rows = [ri.forward_trace(task, SHARED)["O"] for task in tasks]
    return {
        "task_count": len(rows),
        "mean_recovery_recall": sum(r["recall"] for r in rows) / len(rows),
        "full_recovery_count": sum(r["full_recovery"] for r in rows),
        "full_recovery_rate": sum(r["full_recovery"] for r in rows) / len(rows),
    }


def main():
    tasks = surrogate_universe()
    static = static_boundary()
    trace = trace_noninterference(tasks)
    gate = gate_noninterference()
    payload = reserve_payload_symmetry()

    qa = q_adapt(tasks)
    qb = q_adapt(tasks)
    q_equal = qa == qb

    phi_a = reserve_phi(RESERVE_A)
    phi_b = reserve_phi(RESERVE_B)
    delta = {k: phi_a[k] - phi_b[k] for k in phi_a}
    sep = any(v != 0 for v in delta.values())

    n_pass = static["pass"] and trace["pass"] and gate["pass"]
    d_pass = n_pass and q_equal and payload["pass"] and sep

    out = {
        "benchmark_id": "VFA-0.2-DORMANT-CORRECTIVE-RESERVE",
        "future_obligation_accessed": False,
        "governing_invariant": (
            "VFA-0.2 is not allowed to demonstrate treatment advantage before reserve activation."
        ),
        "certificates": {
            "N_noninterference": {
                "pass": n_pass,
                "static_architecture": static,
                "trace": trace,
                "gate": gate,
            },
            "Q_adapt_equivalence": {
                "pass": q_equal,
                "equivalence_rule": (
                    "EXACT_EQUALITY on exhaustive deterministic pre-freeze surrogate universe"
                ),
                "A": qa,
                "B": qb,
            },
            "reserve_payload_symmetry": payload,
            "Sep_Phi_reserve": {
                "pass": sep,
                "A": phi_a,
                "B": phi_b,
                "delta_A_minus_B": delta,
                "aggregation": "PROHIBITED",
            },
        },
        "D_pre_activation": {
            "rule": (
                "N AND Q_adapt_equivalence AND reserve_payload_symmetry AND Sep_Phi_reserve"
            ),
            "adjudication": "PASS" if d_pass else "FAIL",
        },
        "authorization": {
            "freeze_packet": "NOT_FROZEN",
            "authorization_certificate": "NOT_ISSUED",
            "future_run": "NOT_AUTHORIZED",
        },
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "N": n_pass,
                "Q_adapt_equal": q_equal,
                "reserve_payload_symmetry": payload["pass"],
                "Sep_Phi_reserve": sep,
                "D_pre_activation": out["D_pre_activation"]["adjudication"],
                "trace_comparisons": trace["comparisons"],
                "trace_mismatches": trace["mismatch_count"],
                "gate_mismatches": gate["mismatch_count"],
                "Phi_A": phi_a,
                "Phi_B": phi_b,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
