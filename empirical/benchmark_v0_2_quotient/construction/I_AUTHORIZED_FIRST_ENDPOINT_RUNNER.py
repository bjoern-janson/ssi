#!/usr/bin/env python3
"""Capability-minimal authorized runner for VFA-0.2's first prospective endpoint.

The runner does not discover, select, fetch, or ground a future obligation. It
accepts an already-realized common record only after predicate-I identity
preflight. Treatment matrices and first-endpoint outputs are derived solely from
frozen packet members plus the common grounded path-surface table.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import sys
from typing import Any

import I_CHAIN_OF_CUSTODY_KERNEL as custody
import FINAL_TREATMENT_MATERIALIZATION as materialize
import FINAL_POSTGATE_RUNTIME as endpoint

REQUIRED_IMPLEMENTATION = "cpython"
REQUIRED_PYTHON_VERSION = "3.13.5"
REQUIRED_SYSTEM = "Linux"
REQUIRED_MACHINE = "x86_64"
ALLOWED_KERNEL = frozenset({"NONINCLUSION_WITNESS", "INCLUSION_ON_FROZEN_KERNEL_DOMAIN", "NOT_IDENTIFIED"})


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    obj = json.loads(data.decode("utf-8"))
    if type(obj) is not dict:
        raise TypeError(f"JSON object required: {path}")
    return obj


def validate_runtime_platform() -> dict[str, str]:
    facts = {
        "implementation": sys.implementation.name,
        "python_version": platform.python_version(),
        "system": platform.system(),
        "machine": platform.machine(),
    }
    expected = {
        "implementation": REQUIRED_IMPLEMENTATION,
        "python_version": REQUIRED_PYTHON_VERSION,
        "system": REQUIRED_SYSTEM,
        "machine": REQUIRED_MACHINE,
    }
    if facts != expected:
        raise RuntimeError(f"runtime platform mismatch: actual={facts} expected={expected}")
    return facts


def _role_path(packet: dict[str, Any], role: str) -> str:
    matches = [m["path"] for m in packet["members"] if m["role"] == role and m["execution_required"] is True]
    if len(matches) != 1:
        raise ValueError(f"execution role must resolve uniquely: {role}")
    return matches[0]


def _load_execution_members(repo_root: Path, packet: dict[str, Any]) -> dict[str, bytes]:
    out = {}
    for member in packet["members"]:
        if member["execution_required"] is True:
            path = member["path"]
            out[path] = (repo_root / path).read_bytes()
    return out


def _surface_rows(realized: dict[str, Any]) -> list[dict[str, Any]]:
    rows = realized["realized"]["path_surfaces"]
    if type(rows) is not list or len(rows) != 12:
        raise ValueError("realized common record must contain exactly 12 grounded path surfaces")
    for row in rows:
        if type(row) is not dict:
            raise TypeError("grounded path surface must be dict")
    return rows


def run_authorized_first_endpoint(
    repo_root: str | Path,
    packet_path: str | Path,
    freeze_anchor_path: str | Path,
    authorization_certificate_path: str | Path,
    realized_record_path: str | Path,
) -> dict[str, Any]:
    """Run the paired first endpoint after fail-closed authorization preflight."""
    runtime_facts = validate_runtime_platform()
    root = Path(repo_root).resolve()
    packet_bytes = Path(packet_path).read_bytes()
    anchor_bytes = Path(freeze_anchor_path).read_bytes()
    certificate_bytes = Path(authorization_certificate_path).read_bytes()
    realized = _read_json(Path(realized_record_path))

    packet = custody.validate_packet_bytes(packet_bytes)
    loaded = _load_execution_members(root, packet)
    custody.authorize_execution(packet_bytes, anchor_bytes, certificate_bytes, loaded, realized)
    _packet, _anchor, certificate = custody.validate_certificate_bytes(packet_bytes, anchor_bytes, certificate_bytes)

    if realized["realized"]["realized_common_cause_conformance"] != "PASS":
        raise PermissionError("realized common-cause conformance must PASS before endpoint execution")
    kernel_adjudication = realized["realized"]["kernel_adjudication"]
    if kernel_adjudication not in ALLOWED_KERNEL:
        raise ValueError("invalid realized kernel adjudication")
    envelope_sha = realized["realized"]["grounding_envelope_sha256"]
    if type(envelope_sha) is not str or len(envelope_sha) != 64:
        raise ValueError("grounding envelope identity required")
    int(envelope_sha, 16)

    gamma_a = _read_json(root / _role_path(packet, "treatment_Gamma_A"))
    gamma_b = _read_json(root / _role_path(packet, "treatment_Gamma_B"))
    coordinate_obj = _read_json(root / _role_path(packet, "semantic_coordinate_map"))
    domain = _read_json(root / _role_path(packet, "complete_q_kernel_grounding_domain"))
    coordinates = coordinate_obj.get("coordinates")
    if type(coordinates) is not dict:
        raise TypeError("semantic coordinate map missing coordinates")
    surfaces = _surface_rows(realized)

    matrix_a, mat_trace_a = materialize.compile_semantic_matrix(gamma_a, coordinates)
    matrix_b, mat_trace_b = materialize.compile_semantic_matrix(gamma_b, coordinates)
    if mat_trace_a != mat_trace_b:
        raise RuntimeError("A/B treatment materialization logical schedule mismatch")

    result_a, run_trace_a = endpoint.evaluate_first_endpoint(matrix_a, coordinates, domain, surfaces)
    result_b, run_trace_b = endpoint.evaluate_first_endpoint(matrix_b, coordinates, domain, surfaces)
    if run_trace_a != run_trace_b:
        raise RuntimeError("A/B first-endpoint logical schedule mismatch")

    result_core = {
        "benchmark_id": packet["benchmark_id"],
        "packet_sha256": packet["packet_sha256"],
        "execution_root_sha256": packet["execution_root_sha256"],
        "authorization_certificate_sha256": certificate["certificate_sha256"],
        "freeze_commit_sha": certificate["freeze_commit_sha"],
        "freeze_timestamp_utc": certificate["freeze_timestamp_utc"],
        "grounding_envelope_sha256": envelope_sha,
        "kernel_adjudication": kernel_adjudication,
        "runtime_platform": runtime_facts,
        "materialization_trace": {
            "path_record_reads": mat_trace_a.path_record_reads,
            "semantic_coordinate_lookups": mat_trace_a.semantic_coordinate_lookups,
            "class_label_lookups": mat_trace_a.class_label_lookups,
            "matrix_comparisons": mat_trace_a.matrix_comparisons,
            "matrix_writes": mat_trace_a.matrix_writes,
            "output_bytes": mat_trace_a.output_bytes,
        },
        "runtime_trace": {
            "matrix_bytes_read": run_trace_a.matrix_bytes_read,
            "pair_slots_scanned": run_trace_a.pair_slots_scanned,
            "probe_generation_slots": run_trace_a.probe_generation_slots,
            "target_surfaces_read": run_trace_a.target_surfaces_read,
            "target_result_slots_written": run_trace_a.target_result_slots_written,
        },
        "arm_A": list(result_a),
        "arm_B": list(result_b),
        "claim_scope": "first-endpoint q-kernel consequence/reachability only; no CCA/CARS/final adaptation claim",
    }
    result_sha256 = hashlib.sha256(_canonical(result_core)).hexdigest()
    return {**result_core, "result_sha256": result_sha256}


def main() -> None:
    if len(sys.argv) != 6:
        raise SystemExit("usage: I_AUTHORIZED_FIRST_ENDPOINT_RUNNER.py REPO_ROOT PACKET ANCHOR CERTIFICATE REALIZED_RECORD")
    result = run_authorized_first_endpoint(*sys.argv[1:])
    sys.stdout.buffer.write(_canonical(result) + b"\n")


if __name__ == "__main__":
    main()
