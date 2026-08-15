#!/usr/bin/env python3
"""Fail-closed predicate-I identity guard for VFA-0.2.

Identity chain:
  frozen packet -> freeze anchor -> authorization certificate -> realized record.
All control schemas are closed. Rehashed changes create new packet identities and
cannot inherit an older anchor/certificate.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

PASS = "PASS"
AUTHORIZED = "AUTHORIZED"
BENCHMARK_ID = "VFA-0.2-QUOTIENT-REVISION-TOPOLOGY"
PACKET_PREFIX = "VFA-0.2-FROZEN-PACKET-"
PACKET_PATH_PREFIX = "empirical/benchmark_v0_2_quotient/construction/I_FREEZE_PACKET_V"

PACKET_KEYS = frozenset({
    "schema_version", "benchmark_id", "packet_id", "lineage", "source_snapshot_commit",
    "construction_rule", "evaluation_rule_blob", "future_obligation_rule_blob",
    "common_cause_rule_blob", "authorized_runner_blob", "H_residual_set",
    "future_unknowns_not_packet_members", "superseded_or_non_authorized_runtime_artifacts",
    "execution_root_sha256", "members", "previous_candidates", "packet_sha256",
})
MEMBER_KEYS = frozenset({"path", "git_blob_sha", "role", "execution_required"})
PREVIOUS_KEYS = frozenset({"packet_id", "packet_sha256", "status", "authorization_certificate"})
ANCHOR_KEYS = frozenset({
    "schema_version", "benchmark_id", "anchor_id", "packet_id", "packet_path",
    "packet_sha256", "execution_root_sha256", "packet_manifest_git_blob_sha",
    "freeze_commit_sha", "freeze_tree_sha", "freeze_timestamp_utc",
    "verification_basis", "anchor_sha256",
})
CERTIFICATE_KEYS = frozenset({
    "schema_version", "benchmark_id", "packet_manifest_git_blob_sha", "packet_sha256",
    "execution_root_sha256", "freeze_anchor_git_blob_sha", "freeze_anchor_sha256",
    "freeze_commit_sha", "freeze_tree_sha", "freeze_timestamp_utc",
    "authorization_timestamp_utc", "predicates", "H_residual_set",
    "future_obligation_rule_blob", "evaluation_rule_blob", "common_cause_rule_blob",
    "authorized_runner_blob", "I_evidence_blob", "authorization", "state",
    "certificate_sha256",
})
REALIZED_TOP_KEYS = frozenset({"schema_version", "benchmark_id", "frozen_identity", "realized", "execution"})
FROZEN_IDENTITY_KEYS = frozenset({
    "packet_sha256", "execution_root_sha256", "authorization_certificate_sha256",
    "freeze_commit_sha", "freeze_timestamp_utc",
})
REALIZED_KEYS = frozenset({
    "selected_candidate_id", "selected_version", "selection_trace_sha256", "published_at",
    "release_id", "wrapper_tar_sha256", "platform_tar_sha256", "executable_sha256",
    "artifact_integrity_status", "witness_execution_records", "T_future_consequences",
    "J_future_grounding_rows", "path_surfaces", "kernel_adjudication",
    "grounding_envelope_sha256", "bundle_commit_timestamp_utc", "disclosure_timestamp_utc",
    "deadline_timestamp_utc", "realized_common_cause_conformance",
})
EXECUTION_KEYS = frozenset({
    "loaded_execution_root_sha256", "packet_identity_check", "certificate_identity_check",
    "member_set_check", "runtime_conformance", "first_endpoint_results", "result_sha256",
    "execution_status",
})
CRITICAL_ROLE_FIELDS = {
    "final_evaluation_rule": "evaluation_rule_blob",
    "prospective_scope_and_selector": "future_obligation_rule_blob",
    "grounded_common_cause_integration_contract": "common_cause_rule_blob",
    "authorized_first_endpoint_runner": "authorized_runner_blob",
}


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    if type(data) is not bytes:
        raise TypeError("bytes required")
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _hex(value: Any, n: int) -> bool:
    if type(value) is not str or len(value) != n:
        return False
    try:
        int(value, 16)
        return True
    except ValueError:
        return False


def _utc(value: Any) -> bool:
    return type(value) is str and value.endswith("Z") and len(value) >= 20


def _json_object(data: bytes, label: str) -> dict[str, Any]:
    if type(data) is not bytes:
        raise TypeError(f"{label} bytes required")
    try:
        obj = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid {label} JSON") from exc
    if type(obj) is not dict:
        raise TypeError(f"{label} object required")
    return obj


def _packet_number(packet_id: Any) -> int:
    if type(packet_id) is not str or not packet_id.startswith(PACKET_PREFIX):
        raise ValueError("invalid packet id")
    suffix = packet_id[len(PACKET_PREFIX):]
    if not suffix.isdigit() or int(suffix) < 1:
        raise ValueError("invalid packet version")
    return int(suffix)


def packet_core(packet: Mapping[str, Any]) -> dict[str, Any]:
    if type(packet) is not dict:
        raise TypeError("packet object required")
    return {k: v for k, v in packet.items() if k != "packet_sha256"}


def packet_sha256(packet: Mapping[str, Any]) -> str:
    return sha256_obj(packet_core(packet))


def execution_root_sha256(packet: Mapping[str, Any]) -> str:
    members = packet.get("members")
    if type(members) is not list:
        raise TypeError("member list required")
    root = [
        {"path": m.get("path"), "git_blob_sha": m.get("git_blob_sha"), "role": m.get("role")}
        for m in members if m.get("execution_required") is True
    ]
    return sha256_obj(sorted(root, key=lambda x: x["path"]))


def validate_packet(packet: Mapping[str, Any]) -> None:
    if type(packet) is not dict or set(packet) != PACKET_KEYS:
        raise ValueError("packet schema drift")
    if packet["schema_version"] != "4" or packet["benchmark_id"] != BENCHMARK_ID:
        raise ValueError("packet identity/schema mismatch")
    current_n = _packet_number(packet["packet_id"])
    if not _hex(packet["source_snapshot_commit"], 40):
        raise ValueError("source snapshot commit required")

    residuals = packet["H_residual_set"]
    if type(residuals) is not list or not residuals or len(residuals) != len(set(residuals)) or not all(type(x) is str and x for x in residuals):
        raise ValueError("unique nonempty H residual set required")

    previous = packet["previous_candidates"]
    if type(previous) is not list or len(previous) != current_n - 1:
        raise ValueError("complete sequential predecessor lineage required")
    seen_ids, seen_hashes = set(), set()
    for expected_n, row in enumerate(previous, 1):
        if type(row) is not dict or set(row) != PREVIOUS_KEYS:
            raise ValueError("predecessor schema drift")
        if row["packet_id"] != f"{PACKET_PREFIX}{expected_n}":
            raise ValueError("predecessor sequence drift")
        if row["packet_id"] in seen_ids or row["packet_sha256"] in seen_hashes:
            raise ValueError("duplicate predecessor identity")
        if not _hex(row["packet_sha256"], 64) or row["status"] != "REJECTED_BEFORE_AUTHORIZATION" or row["authorization_certificate"] != "NOT_ISSUED":
            raise ValueError("invalid rejected predecessor")
        seen_ids.add(row["packet_id"]); seen_hashes.add(row["packet_sha256"])

    members = packet["members"]
    if type(members) is not list or not members:
        raise ValueError("nonempty member list required")
    seen_paths, role_members = set(), {}
    for member in members:
        if type(member) is not dict or set(member) != MEMBER_KEYS:
            raise ValueError("member schema drift")
        path, blob, role, required = member["path"], member["git_blob_sha"], member["role"], member["execution_required"]
        if type(path) is not str or not path or path in seen_paths or not _hex(blob, 40) or type(role) is not str or not role or type(required) is not bool:
            raise ValueError("invalid packet member")
        seen_paths.add(path)
        role_members.setdefault(role, []).append(member)

    for role, field in CRITICAL_ROLE_FIELDS.items():
        rows = role_members.get(role, [])
        if len(rows) != 1 or rows[0]["execution_required"] is not True or rows[0]["git_blob_sha"] != packet[field]:
            raise ValueError(f"critical role binding mismatch: {role}")

    superseded = packet["superseded_or_non_authorized_runtime_artifacts"]
    if type(superseded) is not list or not all(type(x) is str and x for x in superseded):
        raise ValueError("superseded list required")
    execution_paths = {m["path"] for m in members if m["execution_required"] is True}
    if execution_paths & set(superseded):
        raise ValueError("superseded runtime artifact in execution root")
    unknowns = packet["future_unknowns_not_packet_members"]
    if type(unknowns) is not list or not unknowns or not all(type(x) is str and x for x in unknowns):
        raise ValueError("future unknown declaration required")
    if packet["execution_root_sha256"] != execution_root_sha256(packet):
        raise ValueError("execution root mismatch")
    if packet["packet_sha256"] != packet_sha256(packet):
        raise ValueError("packet digest mismatch")


def validate_packet_bytes(packet_bytes: bytes) -> dict[str, Any]:
    packet = _json_object(packet_bytes, "packet")
    validate_packet(packet)
    return packet


def anchor_core(anchor: Mapping[str, Any]) -> dict[str, Any]:
    if type(anchor) is not dict:
        raise TypeError("anchor object required")
    return {k: v for k, v in anchor.items() if k != "anchor_sha256"}


def anchor_sha256(anchor: Mapping[str, Any]) -> str:
    return sha256_obj(anchor_core(anchor))


def validate_freeze_anchor(packet: Mapping[str, Any], packet_bytes: bytes, anchor: Mapping[str, Any]) -> None:
    validate_packet(packet)
    if type(anchor) is not dict or set(anchor) != ANCHOR_KEYS:
        raise ValueError("freeze anchor schema drift")
    if anchor["schema_version"] != "1" or anchor["benchmark_id"] != packet["benchmark_id"] or anchor["packet_id"] != packet["packet_id"]:
        raise ValueError("freeze anchor identity mismatch")
    if anchor["packet_sha256"] != packet["packet_sha256"] or anchor["execution_root_sha256"] != packet["execution_root_sha256"]:
        raise ValueError("freeze anchor packet/root mismatch")
    if anchor["packet_manifest_git_blob_sha"] != git_blob_sha1(packet_bytes):
        raise ValueError("freeze anchor packet blob mismatch")
    if not _hex(anchor["freeze_commit_sha"], 40) or not _hex(anchor["freeze_tree_sha"], 40) or not _utc(anchor["freeze_timestamp_utc"]):
        raise ValueError("freeze Git/time identity required")
    expected_path = f"{PACKET_PATH_PREFIX}{_packet_number(packet['packet_id'])}.json"
    if anchor["packet_path"] != expected_path:
        raise ValueError("freeze anchor packet path mismatch")
    if anchor["verification_basis"] != "GITHUB_COMMIT_TREE_MEMBERSHIP_VERIFIED_AT_I_ADJUDICATION":
        raise ValueError("unrecognized freeze verification basis")
    if anchor["anchor_sha256"] != anchor_sha256(anchor):
        raise ValueError("freeze anchor digest mismatch")


def validate_freeze_anchor_bytes(packet_bytes: bytes, anchor_bytes: bytes):
    packet = validate_packet_bytes(packet_bytes)
    anchor = _json_object(anchor_bytes, "freeze anchor")
    validate_freeze_anchor(packet, packet_bytes, anchor)
    return packet, anchor


def validate_loaded_execution(packet: Mapping[str, Any], loaded: Mapping[str, bytes]) -> None:
    validate_packet(packet)
    if type(loaded) is not dict:
        raise TypeError("loaded member map required")
    expected = {m["path"]: m["git_blob_sha"] for m in packet["members"] if m["execution_required"] is True}
    if set(loaded) != set(expected):
        raise ValueError("execution member set mismatch")
    for path, blob in expected.items():
        data = loaded[path]
        if type(data) is not bytes or git_blob_sha1(data) != blob:
            raise ValueError(f"execution member blob mismatch: {path}")


def certificate_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    if type(certificate) is not dict:
        raise TypeError("certificate object required")
    return {k: v for k, v in certificate.items() if k != "certificate_sha256"}


def certificate_sha256(certificate: Mapping[str, Any]) -> str:
    return sha256_obj(certificate_core(certificate))


def validate_certificate(packet, packet_bytes: bytes, anchor, anchor_bytes: bytes, certificate) -> None:
    validate_freeze_anchor(packet, packet_bytes, anchor)
    if type(certificate) is not dict or set(certificate) != CERTIFICATE_KEYS:
        raise ValueError("authorization certificate schema drift")
    if certificate["schema_version"] != "1" or certificate["benchmark_id"] != packet["benchmark_id"]:
        raise ValueError("certificate identity mismatch")
    if certificate["packet_manifest_git_blob_sha"] != git_blob_sha1(packet_bytes) or certificate["packet_sha256"] != packet["packet_sha256"] or certificate["execution_root_sha256"] != packet["execution_root_sha256"]:
        raise ValueError("certificate packet binding mismatch")
    if certificate["freeze_anchor_git_blob_sha"] != git_blob_sha1(anchor_bytes) or certificate["freeze_anchor_sha256"] != anchor["anchor_sha256"]:
        raise ValueError("certificate anchor binding mismatch")
    for field in ("freeze_commit_sha", "freeze_tree_sha", "freeze_timestamp_utc"):
        if certificate[field] != anchor[field]:
            raise ValueError(f"certificate freeze mismatch: {field}")
    if not _utc(certificate["authorization_timestamp_utc"]) or certificate["H_residual_set"] != packet["H_residual_set"]:
        raise ValueError("certificate time/residual mismatch")
    predicates = certificate["predicates"]
    if type(predicates) is not dict or set(predicates) != set("ABCDEFGHI") or any(predicates[k] != PASS for k in "ABCDEFGHI"):
        raise PermissionError("certificate requires A-I PASS")
    if certificate["authorization"] != AUTHORIZED or certificate["state"] != "AUTHORIZED_FUTURE_NOT_YET_REALIZED":
        raise PermissionError("certificate state not authorized")
    if not _hex(certificate["I_evidence_blob"], 40):
        raise ValueError("I evidence blob required")
    for field in ("evaluation_rule_blob", "future_obligation_rule_blob", "common_cause_rule_blob", "authorized_runner_blob"):
        if certificate[field] != packet[field]:
            raise ValueError(f"certificate critical binding mismatch: {field}")
    if certificate["certificate_sha256"] != certificate_sha256(certificate):
        raise ValueError("certificate digest mismatch")


def validate_certificate_bytes(packet_bytes: bytes, anchor_bytes: bytes, certificate_bytes: bytes):
    packet, anchor = validate_freeze_anchor_bytes(packet_bytes, anchor_bytes)
    certificate = _json_object(certificate_bytes, "certificate")
    validate_certificate(packet, packet_bytes, anchor, anchor_bytes, certificate)
    return packet, anchor, certificate


def validate_realized_record(certificate, realized) -> None:
    if type(realized) is not dict or set(realized) != REALIZED_TOP_KEYS:
        raise ValueError("realized top-level schema drift")
    frozen = realized["frozen_identity"]
    if type(frozen) is not dict or set(frozen) != FROZEN_IDENTITY_KEYS:
        raise ValueError("realized frozen-identity schema drift")
    expected = {
        "packet_sha256": certificate["packet_sha256"],
        "execution_root_sha256": certificate["execution_root_sha256"],
        "authorization_certificate_sha256": certificate["certificate_sha256"],
        "freeze_commit_sha": certificate["freeze_commit_sha"],
        "freeze_timestamp_utc": certificate["freeze_timestamp_utc"],
    }
    if frozen != expected or realized["benchmark_id"] != certificate["benchmark_id"] or realized["schema_version"] != "1":
        raise ValueError("realized parent identity mismatch")
    if type(realized["realized"]) is not dict or set(realized["realized"]) != REALIZED_KEYS:
        raise ValueError("realized evidence schema drift")
    if type(realized["execution"]) is not dict or set(realized["execution"]) != EXECUTION_KEYS:
        raise ValueError("realized execution schema drift")


def authorize_execution(packet_bytes: bytes, anchor_bytes: bytes, certificate_bytes: bytes, loaded: Mapping[str, bytes], realized) -> str:
    packet, _anchor, certificate = validate_certificate_bytes(packet_bytes, anchor_bytes, certificate_bytes)
    validate_loaded_execution(packet, loaded)
    validate_realized_record(certificate, realized)
    return "RUN_IDENTITY_ACCEPTED"
