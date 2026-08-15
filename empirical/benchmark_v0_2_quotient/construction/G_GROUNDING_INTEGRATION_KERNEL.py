#!/usr/bin/env python3
"""Canonical treatment-free grounding envelope for predicate G integration.

This module does not select or fetch a future release. It canonicalizes already
externally grounded common-cause data against the frozen q-kernel grounding
domain before disclosure. No arm, Gamma, Phi, reachability, or downstream
outcome input is accepted.
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
    selected_version: str
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


def _domain_units(domain: dict[str, Any]) -> dict[str, tuple[str, str]]:
    if type(domain) is not dict:
        raise TypeError("frozen grounding domain required")
    units = {}
    for row in domain.get("grounding_units", []):
        unit_id, left, right = row.get("unit_id"), row.get("left_fact_id"), row.get("right_fact_id")
        if type(unit_id) is not str or not unit_id or unit_id in units:
            raise ValueError("invalid frozen grounding unit")
        if not all(type(x) is str and x for x in (left, right)) or left == right:
            raise ValueError("invalid frozen grounding pair")
        units[unit_id] = tuple(sorted((left, right)))
    if len(units) != 3:
        raise ValueError("frozen domain must contain exactly three grounding units")
    return units


def _domain_surfaces(domain: dict[str, Any]) -> set[tuple[str, str, tuple[str, str], tuple[str, str]]]:
    out = set()
    for row in domain.get("path_surfaces", []):
        unit_id, relation_kind = row.get("unit_id"), row.get("relation_kind")
        left, right = _ref(row.get("left_ref")), _ref(row.get("right_ref"))
        if left[0] != relation_kind or right[0] != relation_kind or left == right:
            raise ValueError("invalid frozen path surface")
        a, b = sorted((left, right))
        ident = (unit_id, relation_kind, a, b)
        if ident in out:
            raise ValueError("duplicate frozen path surface")
        out.add(ident)
    if len(out) != 12:
        raise ValueError("frozen domain must contain exactly twelve path surfaces")
    return out


def _kernel_from_statuses(statuses: list[str]) -> str:
    if any(x == "DISTINGUISHED" for x in statuses):
        return "NONINCLUSION_WITNESS"
    if any(x == "NOT_IDENTIFIED" for x in statuses):
        return "NOT_IDENTIFIED"
    if statuses and all(x == "EQUIVALENT" for x in statuses):
        return "INCLUSION_ON_FROZEN_KERNEL_DOMAIN"
    raise ValueError("invalid grounding status set")


def make_grounding_envelope(
    obligation: ObligationDescriptor,
    artifact: ArtifactRecord,
    domain: dict[str, Any],
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
    if artifact.selected_version != obligation.selected_version:
        raise ValueError("artifact version must equal selected obligation version")
    if kernel_adjudication not in ALLOWED_KERNEL:
        raise ValueError("invalid kernel adjudication")
    if type(contract_digests) is not dict or not contract_digests:
        raise TypeError("contract digests required")

    units = _domain_units(domain)
    expected_surfaces = _domain_surfaces(domain)
    expected_facts = {fact for pair in units.values() for fact in pair}
    if len(expected_facts) != 6:
        raise ValueError("frozen grounding units must span exactly six witness facts")

    if artifact.status == "IDENTIFIED":
        if not all(type(x) is str and len(x) == 64 for x in (artifact.wrapper_tar_sha256, artifact.platform_tar_sha256, artifact.executable_sha256)):
            raise ValueError("identified artifact requires three SHA-256 hashes")
    else:
        if artifact.executable_sha256 is not None:
            raise ValueError("unidentified artifact cannot expose executable hash")

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
        if status == "IDENTIFIED" and (type(sig) is not str or len(sig) != 64):
            raise ValueError("identified consequence requires SHA-256 signature hash")
        if status == "NOT_IDENTIFIED" and sig is not None:
            raise ValueError("missing consequence cannot carry signature hash")
        seen_facts.add(fact_id)
        wc.append((fact_id, status, sig))
    if seen_facts != expected_facts or len(wc) != 6:
        raise ValueError("witness consequences must exactly cover frozen six-fact domain")

    gr = []
    status_by_unit = {}
    for row in grounding_rows:
        if type(row) is not dict:
            raise TypeError("grounding row must be dict")
        unit_id, left, right, status = row.get("unit_id"), row.get("left_fact_id"), row.get("right_fact_id"), row.get("status")
        if unit_id not in units or unit_id in status_by_unit:
            raise ValueError("grounding rows must exactly use frozen unit IDs once")
        if not all(type(x) is str and x for x in (left, right)) or left == right:
            raise ValueError("two grounding facts required")
        if tuple(sorted((left, right))) != units[unit_id]:
            raise ValueError("grounding pair differs from frozen unit")
        if status not in ALLOWED_GROUNDING_STATUS:
            raise ValueError("invalid grounding status")
        a, b = units[unit_id]
        status_by_unit[unit_id] = status
        gr.append((unit_id, a, b, status))
    if set(status_by_unit) != set(units):
        raise ValueError("all three frozen grounding units required")

    ps = [_canonical_surface(row) for row in path_surfaces]
    identities = {(u, k, a, b) for u, k, a, b, _ in ps}
    if identities != expected_surfaces or len(ps) != 12 or len(identities) != 12:
        raise ValueError("path surfaces must exactly cover frozen domain")
    for unit_id, _, _, _, status in ps:
        if status != status_by_unit[unit_id]:
            raise ValueError("path-surface status must inherit grounding-unit status")

    expected_kernel = _kernel_from_statuses(list(status_by_unit.values()))
    if kernel_adjudication != expected_kernel:
        raise ValueError("kernel adjudication inconsistent with grounding rows")

    if artifact.status == "NOT_IDENTIFIED":
        if any(status != "NOT_IDENTIFIED" for _, status, _ in wc):
            raise ValueError("unidentified artifact requires all witness consequences NOT_IDENTIFIED")
        if any(status != "NOT_IDENTIFIED" for status in status_by_unit.values()):
            raise ValueError("unidentified artifact requires all grounding units NOT_IDENTIFIED")
        if kernel_adjudication != "NOT_IDENTIFIED":
            raise ValueError("unidentified artifact requires unidentified kernel adjudication")

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
