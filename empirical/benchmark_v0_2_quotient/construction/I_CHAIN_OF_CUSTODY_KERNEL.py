#!/usr/bin/env python3
"""Fail-closed identity guard for VFA-0.2 freeze, authorization, and execution.

Predicate-I v2: packet and certificate are validated from loaded bytes; critical
rule identities are role-bound; realized/execution records are closed schemas.
The future may instantiate declared fields only. It may not extend the control
surface or alter frozen authority.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

PASS = "PASS"
AUTHORIZED = "AUTHORIZED"
BENCHMARK_ID = "VFA-0.2-QUOTIENT-REVISION-TOPOLOGY"

REALIZED_KEYS = frozenset({
    "selected_candidate_id",
    "selected_version",
    "selection_trace_sha256",
    "published_at",
    "release_id",
    "wrapper_tar_sha256",
    "platform_tar_sha256",
    "executable_sha256",
    "artifact_integrity_status",
    "witness_execution_records",
    "T_future_consequences",
    "J_future_grounding_rows",
    "path_surfaces",
    "kernel_adjudication",
    "grounding_envelope_sha256",
    "bundle_commit_timestamp_utc",
    "disclosure_timestamp_utc",
    "deadline_timestamp_utc",
    "realized_common_cause_conformance",
})

EXECUTION_KEYS = frozenset({
    "loaded_execution_root_sha256",
    "packet_identity_check",
    "certificate_identity_check",
    "member_set_check",
    "runtime_conformance",
    "first_endpoint_results",
    "result_sha256",
    "execution_status",
})

CRITICAL_ROLE_FIELDS = {
    "final_evaluation_rule": "evaluation_rule_blob",
    "prospective_scope_and_selector": "future_obligation_rule_blob",
    "grounded_common_cause_integration_contract": "common_cause_rule_blob",
}


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    if type(data) is not bytes:
        raise TypeError("member bytes required")
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _hex(value: Any, n: int) -> bool:
    if type(value) is not str or len(value) != n:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _json_object(data: bytes, label: str) -> dict[str, Any]:
    if type(data) is not bytes:
        raise TypeError(f"{label} bytes required")
    try:
        obj = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid {label} JSON") from exc
    if type(obj) is not dict:
        raise TypeError(f"{label} must decode to object")
    return obj


def packet_core(packet: Mapping[str, Any]) -> dict[str, Any]:
    if type(packet) is not dict:
        raise TypeError("packet must be dict")
    return {k: v for k, v in packet.items() if k != "packet_sha256"}


def packet_sha256(packet: Mapping[str, Any]) -> str:
    return sha256_obj(packet_core(packet))


def execution_root_sha256(packet: Mapping[str, Any]) -> str:
    members = packet.get("members")
    if type(members) is not list:
        raise TypeError("members list required")
    root = []
    for member in members:
        if type(member) is not dict:
            raise TypeError("member dict required")
        if member.get("execution_required") is True:
            root.append({
                "path": member.get("path"),
                "git_blob_sha": member.get("git_blob_sha"),
                "role": member.get("role"),
            })
    return sha256_obj(sorted(root, key=lambda x: x["path"]))


def validate_packet(packet: Mapping[str, Any]) -> None:
    if type(packet) is not dict:
        raise TypeError("packet must be dict")
    if packet.get("benchmark_id") != BENCHMARK_ID:
        raise ValueError("wrong benchmark identity")
    if packet.get("schema_version") != "2":
        raise ValueError("wrong packet schema")
    if not _hex(packet.get("source_snapshot_commit"), 40):
        raise ValueError("source snapshot commit required")

    residuals = packet.get("H_residual_set")
    if type(residuals) is not list or not residuals or len(residuals) != len(set(residuals)):
        raise ValueError("unique nonempty H residual set required")
    if not all(type(x) is str and x for x in residuals):
        raise TypeError("H residual IDs must be strings")

    members = packet.get("members")
    if type(members) is not list or not members:
        raise ValueError("nonempty member list required")
    seen_paths = set()
    role_members: dict[str, list[dict[str, Any]]] = {}
    for member in members:
        if type(member) is not dict:
            raise TypeError("member dict required")
        path = member.get("path")
        blob = member.get("git_blob_sha")
        role = member.get("role")
        flag = member.get("execution_required")
        if type(path) is not str or not path or path in seen_paths:
            raise ValueError("unique member paths required")
        if not _hex(blob, 40):
            raise ValueError("member Git blob SHA-1 required")
        if type(role) is not str or not role:
            raise ValueError("member role required")
        if type(flag) is not bool:
            raise TypeError("execution_required must be bool")
        seen_paths.add(path)
        role_members.setdefault(role, []).append(member)

    for role, field in CRITICAL_ROLE_FIELDS.items():
        bound = role_members.get(role, [])
        if len(bound) != 1:
            raise ValueError(f"critical role {role} must appear exactly once")
        if packet.get(field) != bound[0]["git_blob_sha"]:
            raise ValueError(f"critical role binding mismatch: {role}")

    superseded = packet.get("superseded_or_non_authorized_runtime_artifacts")
    if type(superseded) is not list or not all(type(x) is str and x for x in superseded):
        raise TypeError("superseded runtime list required")
    execution_paths = {m["path"] for m in members if m["execution_required"] is True}
    if execution_paths & set(superseded):
        raise ValueError("superseded artifact present in execution root")

    expected_exec = execution_root_sha256(packet)
    if packet.get("execution_root_sha256") != expected_exec:
        raise ValueError("execution-root SHA-256 mismatch")
    expected_packet = packet_sha256(packet)
    if packet.get("packet_sha256") != expected_packet:
        raise ValueError("packet SHA-256 mismatch")


def validate_packet_bytes(packet_bytes: bytes) -> dict[str, Any]:
    packet = _json_object(packet_bytes, "packet")
    validate_packet(packet)
    return packet


def validate_loaded_execution(packet: Mapping[str, Any], loaded: Mapping[str, bytes]) -> None:
    validate_packet(packet)
    if type(loaded) is not dict:
        raise TypeError("loaded member map must be dict")
    expected = {
        m["path"]: m["git_blob_sha"]
        for m in packet["members"]
        if m["execution_required"] is True
    }
    if set(loaded) != set(expected):
        missing = sorted(set(expected) - set(loaded))
        extra = sorted(set(loaded) - set(expected))
        raise ValueError(f"execution member-set mismatch missing={missing} extra={extra}")
    for path, expected_blob in expected.items():
        data = loaded[path]
        if type(data) is not bytes:
            raise TypeError(f"loaded member {path} is not bytes")
        if git_blob_sha1(data) != expected_blob:
            raise ValueError(f"loaded member blob mismatch: {path}")


def certificate_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    if type(certificate) is not dict:
        raise TypeError("certificate must be dict")
    return {k: v for k, v in certificate.items() if k != "certificate_sha256"}


def certificate_sha256(certificate: Mapping[str, Any]) -> str:
    return sha256_obj(certificate_core(certificate))


def validate_certificate(packet: Mapping[str, Any], packet_bytes: bytes, certificate: Mapping[str, Any]) -> None:
    validate_packet(packet)
    if type(certificate) is not dict:
        raise TypeError("certificate must be dict")
    if certificate.get("schema_version") != "1":
        raise ValueError("wrong certificate schema")
    if certificate.get("benchmark_id") != packet.get("benchmark_id"):
        raise ValueError("certificate benchmark mismatch")
    if certificate.get("packet_manifest_git_blob_sha") != git_blob_sha1(packet_bytes):
        raise ValueError("certificate packet-file blob mismatch")
    if certificate.get("packet_sha256") != packet.get("packet_sha256"):
        raise ValueError("certificate packet mismatch")
    if certificate.get("execution_root_sha256") != packet.get("execution_root_sha256"):
        raise ValueError("certificate execution-root mismatch")
    if certificate.get("H_residual_set") != packet.get("H_residual_set"):
        raise ValueError("certificate residual-set mismatch")

    predicates = certificate.get("predicates")
    if type(predicates) is not dict or set(predicates) != set("ABCDEFGHI"):
        raise ValueError("certificate must bind predicates A-I")
    if any(predicates[k] != PASS for k in "ABCDEFGHI"):
        raise PermissionError("authorization predicate not PASS")
    if certificate.get("authorization") != AUTHORIZED:
        raise PermissionError("certificate not authorized")
    if certificate.get("state") != "AUTHORIZED_FUTURE_NOT_YET_REALIZED":
        raise ValueError("unexpected authorization state")
    if not _hex(certificate.get("freeze_commit_sha"), 40):
        raise ValueError("freeze commit required")
    if type(certificate.get("freeze_timestamp_utc")) is not str or not certificate["freeze_timestamp_utc"].endswith("Z"):
        raise ValueError("UTC freeze timestamp required")
    if not _hex(certificate.get("I_evidence_blob"), 40):
        raise ValueError("I evidence blob required")
    if certificate.get("evaluation_rule_blob") != packet.get("evaluation_rule_blob"):
        raise ValueError("evaluation rule identity mismatch")
    if certificate.get("future_obligation_rule_blob") != packet.get("future_obligation_rule_blob"):
        raise ValueError("future rule identity mismatch")
    if certificate.get("common_cause_rule_blob") != packet.get("common_cause_rule_blob"):
        raise ValueError("common-cause rule identity mismatch")
    if certificate.get("certificate_sha256") != certificate_sha256(certificate):
        raise ValueError("certificate SHA-256 mismatch")


def validate_certificate_bytes(packet_bytes: bytes, certificate_bytes: bytes) -> tuple[dict[str, Any], dict[str, Any]]:
    packet = validate_packet_bytes(packet_bytes)
    certificate = _json_object(certificate_bytes, "certificate")
    validate_certificate(packet, packet_bytes, certificate)
    return packet, certificate


def validate_realized_record(certificate: Mapping[str, Any], realized: Mapping[str, Any]) -> None:
    if type(realized) is not dict:
        raise TypeError("realized record must be dict")
    allowed_top = {"schema_version", "benchmark_id", "frozen_identity", "realized", "execution"}
    if set(realized) != allowed_top:
        raise ValueError("realized record top-level schema drift")
    frozen = realized.get("frozen_identity")
    if type(frozen) is not dict:
        raise TypeError("frozen_identity required")
    expected_frozen = {
        "packet_sha256": certificate.get("packet_sha256"),
        "execution_root_sha256": certificate.get("execution_root_sha256"),
        "authorization_certificate_sha256": certificate.get("certificate_sha256"),
        "freeze_commit_sha": certificate.get("freeze_commit_sha"),
        "freeze_timestamp_utc": certificate.get("freeze_timestamp_utc"),
    }
    if frozen != expected_frozen:
        raise ValueError("realized record does not descend from authorized frozen identity")
    if realized.get("benchmark_id") != certificate.get("benchmark_id") or realized.get("schema_version") != "1":
        raise ValueError("realized identity mismatch")

    realized_fields = realized.get("realized")
    execution_fields = realized.get("execution")
    if type(realized_fields) is not dict or set(realized_fields) != REALIZED_KEYS:
        raise ValueError("realized block must match exact frozen schema")
    if type(execution_fields) is not dict or set(execution_fields) != EXECUTION_KEYS:
        raise ValueError("execution block must match exact frozen schema")


def authorize_execution(
    packet_bytes: bytes,
    certificate_bytes: bytes,
    loaded: Mapping[str, bytes],
    realized: Mapping[str, Any],
) -> str:
    packet, certificate = validate_certificate_bytes(packet_bytes, certificate_bytes)
    validate_loaded_execution(packet, loaded)
    validate_realized_record(certificate, realized)
    return "RUN_IDENTITY_ACCEPTED"
