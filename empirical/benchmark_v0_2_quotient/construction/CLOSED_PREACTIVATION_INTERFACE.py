#!/usr/bin/env python3
"""Closed preactivation interface for VFA-0.2 quotient revision topology.

This module intentionally imports no Gamma/revision-topology artifact. Ordinary
forward operation has no arm or revision-topology input.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
W = json.loads((HERE / "VALIDATED_SUBSTRATE.json").read_text())
FROZEN = json.loads(
    (HERE.parent.parent / "benchmark_v0_2" / "construction" / "SHARED_FORWARD.json").read_text()
)
_ALLOWED_CLASSES = frozenset(FROZEN["transformation_classes"])


@dataclass(frozen=True, slots=True)
class ForwardState:
    cases: tuple[tuple[str, tuple[str, ...]], ...]
    topology_weights: tuple[tuple[str, float], ...]
    top_k: int

    def __post_init__(self):
        if type(self.top_k) is not int or self.top_k <= 0:
            raise TypeError("invalid top_k")
        if not all(
            type(case) is str
            and type(vals) is tuple
            and all(type(v) is str and v in _ALLOWED_CLASSES for v in vals)
            for case, vals in self.cases
        ):
            raise TypeError("invalid cases")
        if not all(type(k) is str and type(v) in (int, float) for k, v in self.topology_weights):
            raise TypeError("invalid topology weights")


@dataclass(frozen=True, slots=True)
class InsufficiencyEvidence:
    validator_status: str
    failure_scope: str
    independent_validator: bool
    validator_id: str

    def __post_init__(self):
        if type(self.validator_status) is not str:
            raise TypeError("validator_status must be str")
        if type(self.failure_scope) is not str:
            raise TypeError("failure_scope must be str")
        if type(self.independent_validator) is not bool:
            raise TypeError("independent_validator must be bool")
        if type(self.validator_id) is not str:
            raise TypeError("validator_id must be str")


def _edge_key(a: str, b: str) -> str:
    return "|".join(sorted((a, b)))


def _jaccard(a: set[str], b: set[str]) -> float:
    u = a | b
    return 1.0 if not u else len(a & b) / len(u)


def _build_forward_state() -> ForwardState:
    cases = tuple(
        sorted(
            (fact["case"], tuple(sorted(fact["transformation_classes"])))
            for fact in W["facts"]
        )
    )
    weights = tuple(sorted((k, float(v)) for k, v in FROZEN["topology_weights"].items()))
    return ForwardState(cases=cases, topology_weights=weights, top_k=int(FROZEN["top_k"]))


FORWARD_STATE = _build_forward_state()


def forward_trace(query: tuple[str, ...]) -> dict[str, Any]:
    """Ordinary forward operation over a closed immutable state."""
    if type(query) is not tuple or not query:
        raise TypeError("query must be a nonempty tuple")
    if not all(type(v) is str and v in _ALLOWED_CLASSES for v in query):
        raise TypeError("query contains non-class payload")
    if len(query) != len(set(query)):
        raise ValueError("query must not contain duplicates")

    q = set(query)
    features = {case: set(vals) for case, vals in FORWARD_STATE.cases}
    weights = dict(FORWARD_STATE.topology_weights)
    ids = sorted(features)
    exact = [c for c in ids if features[c] == q]
    actions: list[str] = []

    if len(exact) == 1:
        anchor = exact[0]
        ranking = []
        selected = []
        actions.extend(["EXACT_SIGNATURE_MATCH", f"RETRIEVE:{anchor}"])
    else:
        anchors = [(_jaccard(q, features[c]), c) for c in ids]
        anchors.sort(key=lambda row: (-row[0], row[1]))
        anchor = anchors[0][1]
        ranked = []
        for c in ids:
            if c != anchor:
                ranked.append((weights[_edge_key(anchor, c)], c))
        ranked.sort(key=lambda row: (-row[0], row[1]))
        ranking = [{"case": c, "weight": w} for w, c in ranked]
        selected = [c for _, c in ranked[:FORWARD_STATE.top_k]]
        actions.extend(
            ["COMPUTE_SHARED_ANCHOR", f"ANCHOR:{anchor}", "RANK_SHARED_NEIGHBORS"]
            + [f"RETRIEVE:{c}" for c in selected]
            + ["UNION_SHARED_PRECEDENTS"]
        )

    recovered = set(features[anchor])
    for c in selected:
        recovered |= features[c]
    recall = len(q & recovered) / len(q)

    return {
        "I": sorted(q),
        "A": anchor,
        "C": [c for c in ids if c != anchor] if not exact else [],
        "pi": {"ranking": ranking, "selected": selected},
        "E": {
            "anchor_features": sorted(features[anchor]),
            "selected_features": {c: sorted(features[c]) for c in selected},
        },
        "S": actions,
        "M": {"revision_topology_accesses": 0},
        "L": ["mode=DIRECT" if exact else "mode=TOPOLOGY_ASSISTED"],
        "tau": {
            "normalization": "DETERMINISTIC_OPERATION_COUNT",
            "candidate_tests": len(selected),
        },
        "R": {
            "top_k": FORWARD_STATE.top_k,
            "revision_topology_capability": False,
        },
        "O": {
            "recovered": sorted(recovered),
            "recall": recall,
            "full_recovery": recall == 1.0,
        },
    }


def evaluate_gate(evidence: InsufficiencyEvidence) -> bool:
    """Arm-independent closed insufficiency gate."""
    if type(evidence) is not InsufficiencyEvidence:
        raise TypeError("closed evidence schema required")
    return (
        evidence.validator_status == "FAIL"
        and evidence.failure_scope == "CURRENT_ROUTE"
        and evidence.independent_validator is True
        and bool(evidence.validator_id)
    )
