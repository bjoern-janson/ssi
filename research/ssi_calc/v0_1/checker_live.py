#!/usr/bin/env python3
"""SSI-CALC v0.1 successor-v2: typed live-authority substrate.

R1..R11 are unchanged. Historical facts remain available for lineage, explanation,
and obligation construction, but rule execution receives only a live-authority
projection. A historical fact can therefore EXIST without being LIVE, and a live
fact can still fail to DISCHARGE the current typed obligation.

Derivation never reads benchmark family metadata or case['expected'].
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from typing import Iterable

import jsonschema
import checker_orchestrated as prior

RULES = prior.RULES
Certificate = prior.Certificate
ACTIVE = {None, "CONSTITUTED", "SCOPED"}


@dataclass(frozen=True)
class Obligation:
    kind: str
    jurisdiction: str
    operation: str
    locus: str
    rule: str
    missing: str


class AuthorityView:
    def __init__(self, raw: dict):
        self.raw = raw
        self.history = list(raw["facts"])
        self.req = raw["request"]
        self.jurisdiction = self.req["jurisdiction"]

    @staticmethod
    def is_live(fact: dict) -> bool:
        return fact.get("authority") in ACTIVE

    def historical(self, kind: str) -> list[dict]:
        return [f for f in self.history if f["kind"] == kind]

    def live(self, kind: str, jurisdiction: str | None = None) -> list[dict]:
        return [
            f for f in self.historical(kind)
            if self.is_live(f) and (jurisdiction is None or f.get("jurisdiction") == jurisdiction)
        ]

    def any_history(self, kinds: Iterable[str]) -> bool:
        ks = set(kinds)
        return any(f["kind"] in ks for f in self.history)

    def projected_raw(self) -> dict:
        """Execution projection: no inactive/provenance-only fact reaches R1..R11.

        Historical facts are still accessible through this AuthorityView to create
        obligations, trace ancestry, and explain refusals.
        """
        out = dict(self.raw)
        out["facts"] = [f for f in self.history if self.is_live(f)]
        return out

    def indirect_lineage_reaches(self, source: str, root_kind: str) -> bool:
        """Historical reachability is lineage, not authority discharge."""
        source = str(source)
        roots = {
            str(f["args"][0])
            for f in self.historical(root_kind)
            if f.get("args")
        }
        parents: dict[str, list[str]] = {}
        for f in self.historical("derived_from"):
            a = list(map(str, f.get("args", [])))
            if len(a) >= 2:
                parents.setdefault(a[0], []).append(a[1])
        q = deque([source]); seen = {source}
        while q:
            node = q.popleft()
            if node in roots:
                return True
            for parent in parents.get(node, []):
                if parent not in seen:
                    seen.add(parent)
                    q.append(parent)
        return False

    def bridge_discharges(self, source_kind: str, goal_jurisdiction: str) -> bool:
        """Generic typed bridge discharge.

        A bridge must itself be live in the goal jurisdiction, identify the
        historical source type, and target the exact current jurisdiction.
        Historical source material is not promoted directly; only the bridge is
        authority-bearing.
        """
        if not self.historical(source_kind):
            return False
        for bridge in self.live("semantic_bridge", goal_jurisdiction):
            args = list(map(str, bridge.get("args", [])))
            if len(args) >= 2 and args[0] == source_kind and args[1] == str(goal_jurisdiction):
                return True
        return False


def _cert(view: AuthorityView, status: str, locus: str, rule: str,
          missing: list[str] | None = None, why: str = "") -> Certificate:
    return Certificate(
        status,
        locus,
        rule,
        [f["id"] for f in view.history],
        missing or [],
        [],
        why,
    )


def _rebase_preservation(view: AuthorityView, cert: Certificate) -> Certificate:
    # Ordinary adjudication preserves the complete historical input record. Reopen
    # certificates intentionally preserve their narrower trigger lineage as emitted.
    if cert.status == "REOPEN":
        return cert
    return replace(cert, preserved_facts=[f["id"] for f in view.history])


def _provenance_goal(view: AuthorityView) -> Certificate | None:
    op = view.req["operation"]
    j = view.jurisdiction
    source_types = {
        "assert_semantic_equivalence": ("same_hash", "hash_to_semantic_role_bridge"),
        "assert_valid": ("filename", "metadata_to_validity_bridge"),
        "assert_independent_evidence": ("same_training_source", "independence_bridge"),
        "count_independent_observations": ("derived_from", "augmentation_to_independence_bridge"),
    }
    if op not in source_types:
        return None
    source_kind, missing = source_types[op]
    if not view.historical(source_kind) and not any(
        f.get("authority") == "PROVENANCE_ONLY" for f in view.history
    ):
        return None

    # First try the generic typed bridge. Existing specialized bridge kinds remain
    # executable through the prior evaluator after projection.
    if view.bridge_discharges(source_kind, j):
        return _cert(
            view, "AUTHORIZED_SCOPED", "NONE", "R3:LICENSE",
            why="A live typed bridge discharges the provenance-to-semantic obligation.",
        )

    # If a specialized active bridge is already present, leave it to prior R3 logic.
    specialized = {
        "assert_semantic_equivalence": "semantic_bridge",
        "assert_independent_evidence": "independence_bridge",
    }.get(op)
    if specialized and view.live(specialized, j):
        return None

    return _cert(
        view, "PROVENANCE_LEAK", "PROVENANCE", "R3:LICENSE", [missing],
        "Historical provenance exists, but no live typed bridge discharges the current semantic obligation.",
    )


def _inactive_obligation(view: AuthorityView) -> Certificate | None:
    """Turn represented-but-inactive premises into typed unresolved obligations.

    These are not new rules. They prevent historical/unresolved facts from either
    authorizing or prohibiting a live derivation while retaining an exact failure
    locus for the existing R1..R11 jurisdiction.
    """
    op = view.req["operation"]
    j = view.jurisdiction

    if op == "assert_identity":
        hist = view.historical("identity_by_denotation")
        if hist and not view.live("identity_by_denotation", j):
            return _cert(
                view, "NOT_IDENTIFIED", "EQUIV", "R4:EQUIV",
                ["active_identity_by_denotation_authority"],
                "Identity-by-denotation exists in lineage but is not live for the current identity obligation.",
            )

    if op == "transport_relation":
        requirements = [
            ("operations_commute", "active_operations_commutation_certificate"),
            ("target_independent", "active_target_independence_certificate"),
        ]
        for kind, missing in requirements:
            if view.historical(kind) and not view.live(kind, j):
                return _cert(
                    view, "NOT_IDENTIFIED", "TRANSPORT", "R7:TRANSPORT", [missing],
                    f"Historical {kind} evidence is not live for the current transport obligation.",
                )

    if op == "consume_quotient":
        if view.live("local_quotient_licensed"):
            if view.historical("kernel_containment_verified") and not view.live("kernel_containment_verified", j):
                return _cert(
                    view, "NOT_IDENTIFIED", "PRESERVE", "R10:PRESERVE",
                    ["constituted_kernel_containment_proof"],
                    "Kernel-containment evidence exists but is not live for the future-consumer obligation.",
                )
            if view.historical("future_invariant_under") and not view.live("future_invariant_under", j):
                return _cert(
                    view, "NOT_IDENTIFIED", "PRESERVE", "R10:PRESERVE",
                    ["constituted_future_invariance_proof"],
                    "Future-invariance evidence exists but is not live for the preservation obligation.",
                )

    if op == "assert_future_safe":
        if view.historical("future_distinguishes") and not view.live("future_distinguishes", j):
            return _cert(
                view, "NOT_IDENTIFIED", "PRESERVE", "R10:PRESERVE",
                ["active_future_distinction_or_preservation_proof"],
                "Historical future-distinction evidence is not live for the current preservation judgment.",
            )

    if op == "compare_regimes":
        hist = view.historical("purpose_compatibility")
        if hist and not view.live("purpose_compatibility") and not view.live("purpose_compatible"):
            return _cert(
                view, "NOT_IDENTIFIED", "ADMIT", "R2:ADMIT",
                ["purpose_compatibility(kappa1,kappa2)"],
                "Purpose comparability is represented but not live.",
            )

    if op == "apply_equivalent":
        hist = view.historical("congruence_status")
        if hist and not view.live("congruence_status"):
            arg = str(view.req.get("args", ["consumer"])[0])
            return _cert(
                view, "NOT_IDENTIFIED", "CONGRUENCE", "R6:CONGRUENCE",
                [f"congruence({arg},{j})"],
                "Consumer congruence is represented but not live.",
            )

    if op == "compose":
        hist = view.historical("compose_compatibility")
        if hist and not view.live("compose_compatibility"):
            ids = list(map(str, view.req.get("args", [])))
            label = f"composition_certificate({ids[0]},{ids[1]})" if len(ids) >= 2 else "composition_certificate"
            return _cert(
                view, "NOT_IDENTIFIED", "COMPOSE", "R9:COMPOSE", [label],
                "Composition compatibility is represented but not live.",
            )

    return None


def _historical_lineage_gate(view: AuthorityView) -> Certificate | None:
    if view.req["operation"] == "inform" and view.req.get("args"):
        source = str(view.req["args"][0])
        if view.indirect_lineage_reaches(source, "encodes"):
            return _cert(
                view, "UNLICENSED_JURISDICTION_TRANSFER", "TRANSFER", "R3:LICENSE",
                ["oracle_safe_feature_license"],
                "Historical answer-bearing ancestry creates an information-flow obligation but does not grant detector-safe authority.",
            )
    return None


def derive(raw: dict, schema: dict) -> Certificate:
    jsonschema.Draft202012Validator(schema).validate(raw)
    view = AuthorityView({k: raw[k] for k in ["id", "objects", "facts", "authority_edges", "request"]})

    # Historical information may create obligations but never discharge them.
    for gate in (_historical_lineage_gate, _provenance_goal, _inactive_obligation):
        result = gate(view)
        if result is not None:
            return result

    # Every R1..R11 execution path receives the same live-authority membrane.
    result = prior.derive(view.projected_raw(), schema)
    return _rebase_preservation(view, result)


def load_json(path):
    return prior.load_json(path)
