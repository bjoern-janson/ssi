#!/usr/bin/env python3
"""Canonical treatment-free grounding envelope for predicate G integration.

This module does not select or fetch a future release. It canonicalizes already
externally grounded common-cause data before disclosure. No arm, Gamma, Phi,
reachability, or downstream outcome input is accepted.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from typing import Any

ALLOWED_CONSEQUENCE_STATUS = frozenset({"IDENTIFIED", "NOT_IDENTIFIED"})
ALLOWED_GROUNDING_STATUS = frozenset({"DISTINGUISHED", "EQUIVALENT", "NOT_IDENTIFIED"})
ALLOWED_KERNEL = frozenset({"NONINCLUSION_WITNESS", "INCLUSION_ON_FROZEN_KERNEL_DOMAIN", "NOT_IDENTIFIED"})


@dataclass(frozen=True, slots=True)
class ObligationDescriptor:
    selected_candidate_id: str
    selected_version: str
    published_at: str
    release_id: int
    selection_trace_sha256: str


@dataclass(frozen=True, slots=True)
class ArtifactRecord:
    status: str
    wrapper_tar_sha256: str | None
    platform_tar_sha256: str | None
    executable_sha256: str | None


@dataclass(frozen=True, slots=True)
class GroundingEnvelope:
    obligation: ObligationDescriptor
    artifact: ArtifactRecord
    witness_consequences: tuple[tuple[str, str, str | None], ...]
    grounding_rows: tuple[tuple[str, str, str, str], ...]
    path_surfaces: tuple[tuple[str, str, tuple[str, str], tuple[str, str], str], ...]
    kernel_adjudication: str
    contract_digests: tuple[tuple[str, str], ...]
    envelope_sha256: str


def _sha(obj: Any) -> str:
    data = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()


def _ref(value) -> tuple[str, str]:
    if not isinstance(value, (list, tuple)) or len(value) != 2 or not all(type(x) is str and x for x in value):
        raise TypeError("semantic reference must contain relation kind and source fact id")
    return (value[0], value[1])


def _canonical_surface(row: dict[str, Any]) -> tuple[str, str, tuple[str, str], tuple[str, str], str]:
    if type(row) is not dict:
        raise TypeError("surface row must be dict")
    unit_id = row.get("unit_id")
    relation_kind = row.get("relation_kind")
    status = row.get("status")
    if type(unit_id) is not str or not unit_id or type(relation_kind) is not str or not relation_kind:
        raise TypeError("surface identifiers required")
    if status not in ALLOWED_GROUNDING_STATUS:
        raise ValueError("invalid surface status")
    left, right = _ref(row.get("left_ref")), _ref(row.get("right_ref"))
    if left[0] != relation_kind or right[0] != relation_kind or left == right:
        raise ValueError("invalid relation-kind surface")
    a, b = sorted((left, right))
    return unit_id, relation_kind, a, b, status


def make_grounding_envelope(
    obligation: ObligationDescriptor,
    artifact: ArtifactRecord,
    witness_consequences: list[dict[str, Any]],
    grounding_rows: list[dict[str, Any]],
    path_surfaces: list[dict[str, Any]],
    kernel_adjudication: str,
    contract_digests: dict[str, str],
) -> GroundingEnvelope:
    if type(obligation) is not ObligationDescriptor or type(artifact) is not ArtifactRecord:
        raise TypeError("typed common records required")
    if not obligation.selected_candidate_id or not obligation.selected_version or not obligation.published_at or not obligation.selection_trace_sha256:
        raise ValueError("complete obligation identity required")
    if type(obligation.release_id) is not int or obligation.release_id < 0:
        raise ValueError("release_id must be nonnegative int")
    if artifact.status not in ALLOWED_CONSEQUENCE_STATUS:
        raise ValueError("invalid artifact status")
    if kernel_adjudication not in ALLOWED_KERNEL:
        raise ValueError("invalid kernel adjudication")
    if type(contract_digests) is not dict or not contract_digests:
        raise TypeError("contract digests required")

    wc = []
    seen_facts = set()
    for row in witness_consequences:
        if type(row) is not dict:
            raise TypeError("witness consequence row must be dict")
        fact_id, status, sig = row.get("fact_id"), row.get("status"), row.get("signature_sha256")
        if type(fact_id) is not str or not fact_id or fact_id in seen_facts:
            raise ValueError("unique fact_id required")
        if status not in ALLOWED_CONSEQUENCE_STATUS:
            raise ValueError("invalid witness consequence status")
        if status == "IDENTIFIED" and (type(sig) is not str or not sig):
            raise ValueError("identified consequence requires signature hash")
        if status == "NOT_IDENTIFIED" and sig is not None:
            raise ValueError("missing consequence cannot carry signature hash")
        seen_facts.add(fact_id)
        wc.append((fact_id, status, sig))
    if len(wc) != 6:
        raise ValueError("exactly six witness consequence rows required")

    gr = []
    seen_units = set()
    for row in grounding_rows:
        if type(row) is not dict:
            raise TypeError("grounding row must be dict")
        unit_id, left, right, status = row.get("unit_id"), row.get("left_fact_id"), row.get("right_fact_id"), row.get("status")
        if type(unit_id) is not str or not unit_id or unit_id in seen_units:
            raise ValueError("unique grounding unit required")
        if not all(type(x) is str and x for x in (left, right)) or left == right:
            raise ValueError("two grounding facts required")
        if status not in ALLOWED_GROUNDING_STATUS:
            raise ValueError("invalid grounding status")
        a, b = sorted((left, right))
        seen_units.add(unit_id)
        gr.append((unit_id, a, b, status))
    if len(gr) != 3:
        raise ValueError("exactly three grounding units required")

    ps = [_canonical_surface(row) for row in path_surfaces]
    if len(ps) != 12 or len(set(ps)) != 12:
        raise ValueError("exactly twelve unique path surfaces required")

    cd = []
    for name, digest in contract_digests.items():
        if type(name) is not str or not name or type(digest) is not str or len(digest) != 64:
            raise ValueError("contract digests must be named SHA-256 hex strings")
        int(digest, 16)
        cd.append((name, digest.lower()))

    core = {
        "obligation": asdict(obligation),
        "artifact": asdict(artifact),
        "witness_consequences": sorted(wc),
        "grounding_rows": sorted(gr),
        "path_surfaces": sorted(ps),
        "kernel_adjudication": kernel_adjudication,
        "contract_digests": sorted(cd),
    }
    digest = _sha(core)
    return GroundingEnvelope(
        obligation=obligation,
        artifact=artifact,
        witness_consequences=tuple(core["witness_consequences"]),
        grounding_rows=tuple(core["grounding_rows"]),
        path_surfaces=tuple(core["path_surfaces"]),
        kernel_adjudication=kernel_adjudication,
        contract_digests=tuple(core["contract_digests"]),
        envelope_sha256=digest,
    )


def envelope_bytes(envelope: GroundingEnvelope) -> bytes:
    if type(envelope) is not GroundingEnvelope:
        raise TypeError("GroundingEnvelope required")
    obj = asdict(envelope)
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
