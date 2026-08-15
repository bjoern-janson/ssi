#!/usr/bin/env python3
"""VFA-0.2 pre-activation interface.

The forward subsystem and insufficiency gate intentionally have no reserve
argument, reserve handle, reserve path, or arm identity. Reserve access is
possible only through activate_reserve(), after evaluate_gate() returns True.
"""

from __future__ import annotations

from typing import Any


class ReserveClosed(RuntimeError):
    pass


def _edge_key(a: str, b: str) -> str:
    return "|".join(sorted((a, b)))


def _jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return 1.0 if not union else len(a & b) / len(union)


def evaluate_gate(evidence: dict[str, Any]) -> bool:
    """Arm-independent external insufficiency gate.

    The gate fires only when the shared current route has failed an independently
    named validator and that failure has been adjudicated as current-route
    insufficiency. No reserve object is accepted or reachable from this function.
    """
    return (
        evidence.get("validator_status") == "FAIL"
        and evidence.get("failure_scope") == "CURRENT_ROUTE"
        and evidence.get("independent_validator") is True
        and isinstance(evidence.get("validator_id"), str)
        and bool(evidence.get("validator_id"))
    )


def forward_trace(query: list[str], shared_forward: dict[str, Any]) -> dict[str, Any]:
    """Execute the ordinary forward path with no reserve-capable interface."""
    q = set(query)
    features = {case: set(vals) for case, vals in shared_forward["cases"].items()}
    case_ids = sorted(features)
    top_k = int(shared_forward["top_k"])

    exact = sorted(case for case in case_ids if features[case] == q)
    memory_reads = [
        "shared_forward.cases",
        "shared_forward.topology_weights",
        "shared_forward.top_k",
    ]
    memory_writes: list[str] = []
    logs: list[str] = []
    action_sequence: list[str] = []
    jaccard_evals = 0
    edge_lookups = 0

    if len(exact) == 1:
        anchor = exact[0]
        candidate_set: list[str] = []
        ranking: list[dict[str, Any]] = []
        selected: list[str] = []
        recovered = set(features[anchor])
        action_sequence.extend(["EXACT_SIGNATURE_MATCH", f"RETRIEVE:{anchor}"])
        logs.append("mode=DIRECT")
    else:
        anchors = []
        for case in case_ids:
            score = _jaccard(q, features[case])
            jaccard_evals += 1
            anchors.append((score, case))
        anchors.sort(key=lambda row: (-row[0], row[1]))
        anchor = anchors[0][1]

        candidate_set = sorted(case for case in case_ids if case != anchor)
        ranked = []
        for case in candidate_set:
            weight = shared_forward["topology_weights"][_edge_key(anchor, case)]
            edge_lookups += 1
            ranked.append((weight, case))
        ranked.sort(key=lambda row: (-row[0], row[1]))
        ranking = [{"case": case, "weight": weight} for weight, case in ranked]
        selected = [case for _, case in ranked[:top_k]]

        recovered = set(features[anchor])
        for case in selected:
            recovered |= features[case]

        action_sequence.extend(
            [
                "COMPUTE_SHARED_ANCHOR",
                f"ANCHOR:{anchor}",
                "RANK_SHARED_NEIGHBORS",
                *[f"RETRIEVE:{case}" for case in selected],
                "UNION_SHARED_PRECEDENTS",
            ]
        )
        logs.append("mode=TOPOLOGY_ASSISTED")

    recall = len(q & recovered) / len(q) if q else 1.0
    op_count = jaccard_evals + edge_lookups + len(selected) + 1

    return {
        "I": sorted(q),
        "A": anchor,
        "C": candidate_set,
        "pi": {"ranking": ranking, "selected": selected},
        "E": {
            "anchor_features": sorted(features[anchor]),
            "selected_features": {case: sorted(features[case]) for case in selected},
        },
        "S": action_sequence,
        "M": {
            "reads": memory_reads,
            "writes": memory_writes,
            "reserve_reads": 0,
            "reserve_writes": 0,
        },
        "L": logs,
        "tau": {
            "normalization": "DETERMINISTIC_OPERATION_COUNT",
            "operations": op_count,
            "jaccard_evaluations": jaccard_evals,
            "edge_lookups": edge_lookups,
        },
        "R": {
            "top_k": top_k,
            "candidate_tests": len(selected),
            "shared_forward_reads": len(memory_reads),
            "reserve_accesses": 0,
        },
        "O": {
            "recovered": sorted(recovered),
            "recall": recall,
            "full_recovery": recall == 1.0,
        },
    }


def activate_reserve(evidence: dict[str, Any], reserve_handle: dict[str, Any]) -> dict[str, Any]:
    """The sole reserve-dereference boundary."""
    if not evaluate_gate(evidence):
        raise ReserveClosed("corrective reserve is inaccessible while G=0")
    return reserve_handle
