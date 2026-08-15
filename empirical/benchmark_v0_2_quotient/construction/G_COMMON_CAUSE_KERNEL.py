#!/usr/bin/env python3
"""Treatment-free prospective selector and common-bundle kernel for predicate G.

Authorization-side only. No real future Biome release is fetched or inspected here.
The kernel has no arm, Gamma, Phi, M_Gamma, score, or outcome input.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json
from typing import Iterable

MAX_PAYLOAD_BYTES = 67_108_864
ELIGIBLE_CHANGE_KINDS = frozenset({
    "PROPERTY_REMOVED",
    "PROPERTY_RENAMED",
    "PROPERTY_PATH_MOVED",
    "ACCEPTED_TYPE_CHANGED",
    "ENUM_OR_DOMAIN_NARROWED",
    "REQUIREDNESS_CHANGED",
    "VERSIONED_CONFIGURATION_SEMANTICS_CHANGED",
})


def _dt(value: str) -> datetime:
    x = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if x.tzinfo is None:
        raise ValueError("timezone-aware timestamp required")
    return x.astimezone(timezone.utc)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


@dataclass(frozen=True, slots=True)
class Candidate:
    candidate_id: str
    published_at: str
    release_id: int
    stable: bool
    implementation_after_freeze: bool
    migration_relevant: bool
    change_kinds: tuple[str, ...]
    excluded: bool
    common_packaging_possible: bool

    def __post_init__(self):
        if type(self.candidate_id) is not str or not self.candidate_id:
            raise TypeError("candidate_id required")
        _dt(self.published_at)
        if type(self.release_id) is not int or self.release_id < 0:
            raise TypeError("release_id must be nonnegative int")
        if any(type(x) is not str for x in self.change_kinds):
            raise TypeError("change kinds must be strings")


@dataclass(frozen=True, slots=True)
class SelectionTrace:
    freeze_timestamp: str
    ordered_candidate_ids: tuple[str, ...]
    eligibility_rows: tuple[tuple[str, bool, tuple[str, ...]], ...]
    selected_candidate_id: str

    @property
    def sha256(self) -> str:
        return _sha(_canonical(asdict(self)))


@dataclass(frozen=True, slots=True)
class CommonBundleCommitment:
    selected_candidate_id: str
    selection_trace_sha256: str
    selected_at: str
    bundle_committed_at: str
    disclose_at: str
    deadline_at: str
    payload_sha256: str
    evidence_sha256: str
    payload_bytes: int
    evidence_bytes: int
    commitment_sha256: str


def _eligibility(candidate: Candidate, freeze_timestamp: str) -> tuple[bool, tuple[str, ...]]:
    reasons = []
    if _dt(candidate.published_at) <= _dt(freeze_timestamp):
        reasons.append("NOT_POST_FREEZE_RELEASE")
    if not candidate.stable:
        reasons.append("NOT_STABLE")
    if not candidate.implementation_after_freeze:
        reasons.append("IMPLEMENTATION_NOT_INDEPENDENT")
    if not candidate.migration_relevant:
        reasons.append("NOT_MIGRATION_RELEVANT")
    if candidate.excluded:
        reasons.append("EXCLUDED")
    if not candidate.common_packaging_possible:
        reasons.append("NO_COMMON_PACKAGING")
    if not candidate.change_kinds or not set(candidate.change_kinds) <= ELIGIBLE_CHANGE_KINDS:
        reasons.append("CHANGE_KIND_NOT_ADMISSIBLE")
    return (not reasons, tuple(reasons))


def select_first_qualifying(candidates: Iterable[Candidate], freeze_timestamp: str) -> SelectionTrace:
    """Select globally by frozen external order. No treatment/arm input exists."""
    _dt(freeze_timestamp)
    rows = list(candidates)
    if len({x.candidate_id for x in rows}) != len(rows):
        raise ValueError("candidate IDs must be unique")
    ordered = sorted(rows, key=lambda x: (_dt(x.published_at), x.release_id))
    eligibility_rows = []
    selected = "NO_QUALIFYING_OBLIGATION"
    for candidate in ordered:
        ok, reasons = _eligibility(candidate, freeze_timestamp)
        eligibility_rows.append((candidate.candidate_id, ok, reasons))
        if selected == "NO_QUALIFYING_OBLIGATION" and ok:
            selected = candidate.candidate_id
    return SelectionTrace(
        freeze_timestamp=freeze_timestamp,
        ordered_candidate_ids=tuple(x.candidate_id for x in ordered),
        eligibility_rows=tuple(eligibility_rows),
        selected_candidate_id=selected,
    )


def commit_common_bundle(
    trace: SelectionTrace,
    payload: bytes,
    evidence: bytes,
    selected_at: str,
    bundle_committed_at: str,
    disclose_at: str,
    deadline_at: str,
) -> CommonBundleCommitment:
    """Create one global bundle commitment before any arm receives it."""
    if trace.selected_candidate_id == "NO_QUALIFYING_OBLIGATION":
        raise ValueError("no obligation to package")
    if type(payload) is not bytes or type(evidence) is not bytes:
        raise TypeError("payload and evidence must be bytes")
    if len(payload) > MAX_PAYLOAD_BYTES or len(evidence) > MAX_PAYLOAD_BYTES:
        raise ValueError("common bundle exceeds frozen cap")
    t_freeze = _dt(trace.freeze_timestamp)
    t_select = _dt(selected_at)
    t_commit = _dt(bundle_committed_at)
    t_disclose = _dt(disclose_at)
    t_deadline = _dt(deadline_at)
    if not (t_freeze < t_select <= t_commit < t_disclose < t_deadline):
        raise ValueError("invalid common-cause temporal order")
    core = {
        "selected_candidate_id": trace.selected_candidate_id,
        "selection_trace_sha256": trace.sha256,
        "selected_at": selected_at,
        "bundle_committed_at": bundle_committed_at,
        "disclose_at": disclose_at,
        "deadline_at": deadline_at,
        "payload_sha256": _sha(payload),
        "evidence_sha256": _sha(evidence),
        "payload_bytes": len(payload),
        "evidence_bytes": len(evidence),
    }
    return CommonBundleCommitment(**core, commitment_sha256=_sha(_canonical(core)))


def arm_view(commitment: CommonBundleCommitment) -> tuple[str, str, str, str]:
    """Common view has no arm argument; both recipients must use this exact object."""
    if type(commitment) is not CommonBundleCommitment:
        raise TypeError("CommonBundleCommitment required")
    return (
        commitment.commitment_sha256,
        commitment.payload_sha256,
        commitment.evidence_sha256,
        commitment.disclose_at,
    )
