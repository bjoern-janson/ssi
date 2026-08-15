#!/usr/bin/env python3
"""Temporal-hardening wrapper for the generalized predicate-I custody kernel.

Loads the frozen generalized base guard by exact sibling path/blob, preserves its
closed schemas and identity checks, and adds the causal temporal invariant:
authorization must occur strictly after freeze.
"""
from __future__ import annotations

from datetime import datetime
import importlib.util
from pathlib import Path
import sys
from typing import Any, Mapping

BASE_FILENAME = "I_CHAIN_OF_CUSTODY_KERNEL.py"
BASE_GIT_BLOB = "db3e1d4bcdb9cce691cf86c66ad7705f5a42fc5e"


def _git_blob_sha1(data: bytes) -> str:
    import hashlib
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _load_base():
    path = Path(__file__).resolve().with_name(BASE_FILENAME)
    data = path.read_bytes()
    if _git_blob_sha1(data) != BASE_GIT_BLOB:
        raise RuntimeError("base custody-kernel blob mismatch")
    name = "vfa_i_custody_base"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load base custody kernel")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()

# Re-export non-overridden frozen primitives used by the runner/audits.
canonical_bytes = _base.canonical_bytes
sha256_obj = _base.sha256_obj
git_blob_sha1 = _base.git_blob_sha1
packet_core = _base.packet_core
packet_sha256 = _base.packet_sha256
execution_root_sha256 = _base.execution_root_sha256
validate_packet = _base.validate_packet
validate_packet_bytes = _base.validate_packet_bytes
anchor_core = _base.anchor_core
anchor_sha256 = _base.anchor_sha256
validate_freeze_anchor = _base.validate_freeze_anchor
validate_freeze_anchor_bytes = _base.validate_freeze_anchor_bytes
validate_loaded_execution = _base.validate_loaded_execution
certificate_core = _base.certificate_core
certificate_sha256 = _base.certificate_sha256
validate_realized_record = _base.validate_realized_record


def _parse_utc(value: Any) -> datetime:
    if type(value) is not str or not value.endswith("Z"):
        raise ValueError("UTC timestamp required")
    try:
        dt = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError("invalid UTC timestamp") from exc
    if dt.utcoffset() is None or dt.utcoffset().total_seconds() != 0:
        raise ValueError("UTC timestamp required")
    return dt


def validate_certificate(
    packet: Mapping[str, Any],
    packet_bytes: bytes,
    anchor: Mapping[str, Any],
    anchor_bytes: bytes,
    certificate: Mapping[str, Any],
) -> None:
    _base.validate_certificate(packet, packet_bytes, anchor, anchor_bytes, certificate)
    freeze_time = _parse_utc(certificate["freeze_timestamp_utc"])
    authorization_time = _parse_utc(certificate["authorization_timestamp_utc"])
    if not freeze_time < authorization_time:
        raise ValueError("authorization must occur strictly after freeze")


def validate_certificate_bytes(packet_bytes: bytes, anchor_bytes: bytes, certificate_bytes: bytes):
    packet, anchor = validate_freeze_anchor_bytes(packet_bytes, anchor_bytes)
    certificate = _base._json_object(certificate_bytes, "certificate")
    validate_certificate(packet, packet_bytes, anchor, anchor_bytes, certificate)
    return packet, anchor, certificate


def authorize_execution(
    packet_bytes: bytes,
    anchor_bytes: bytes,
    certificate_bytes: bytes,
    loaded: Mapping[str, bytes],
    realized,
) -> str:
    packet, _anchor, certificate = validate_certificate_bytes(packet_bytes, anchor_bytes, certificate_bytes)
    validate_loaded_execution(packet, loaded)
    validate_realized_record(certificate, realized)
    return "RUN_IDENTITY_ACCEPTED"
