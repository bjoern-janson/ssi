#!/usr/bin/env python3
"""Capability-minimal authorized runner for VFA-0.2's first endpoint.

Trust bootstrap is stdlib-only. Project code is loaded only from absolute packet-
authorized paths after identity checks; ordinary ambient project imports are not
used. The runner does not discover, select, fetch, or ground a future obligation.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from types import ModuleType
from typing import Any

REQUIRED_IMPLEMENTATION = "cpython"
REQUIRED_PYTHON_VERSION = "3.13.5"
REQUIRED_SYSTEM = "Linux"
REQUIRED_MACHINE = "x86_64"
EXPECTED_CUSTODY_BLOB = "db3e1d4bcdb9cce691cf86c66ad7705f5a42fc5e"
CUSTODY_RELATIVE_PATH = "empirical/benchmark_v0_2_quotient/construction/I_CHAIN_OF_CUSTODY_KERNEL.py"
ALLOWED_KERNEL = frozenset({"NONINCLUSION_WITNESS", "INCLUSION_ON_FROZEN_KERNEL_DOMAIN", "NOT_IDENTIFIED"})

ENVELOPE_KEYS = frozenset({
    "obligation", "artifact", "witness_consequences", "grounding_rows",
    "path_surfaces", "kernel_adjudication", "contract_digests", "envelope_sha256",
})
G_CERT_KEYS = frozenset({
    "certificate_type", "status", "authorization_packet_digest",
    "selected_candidate_id", "selected_version", "selection_trace_sha256",
    "selected_at", "artifact_resolved_at", "wrapper_tar_sha256",
    "platform_tar_sha256", "executable_sha256", "artifact_contract_conformance",
    "six_witness_execution_conformance", "repeat_determinism_conformance",
    "grounding_unit_count", "path_surface_count", "grounding_envelope_sha256",
    "grounding_committed_at", "bundle_committed_at", "disclosed_at_A",
    "disclosed_at_B", "deadline_A", "deadline_B", "common_obligation_sha256_A",
    "common_obligation_sha256_B", "common_grounding_envelope_sha256_A",
    "common_grounding_envelope_sha256_B", "first_qualifying_rule_conformance",
    "implementation_independence_conformance", "no_arm_access_before_grounding_commit",
    "no_substitution_conformance", "realized_kernel_domain_adjudication",
    "post_disclosure_validity", "rule",
})


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    try:
        obj = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON: {path}") from exc
    if type(obj) is not dict:
        raise TypeError(f"JSON object required: {path}")
    return obj


def _parse_utc(value: Any) -> datetime:
    if type(value) is not str or not value.endswith("Z"):
        raise ValueError("UTC timestamp required")
    try:
        dt = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError("invalid UTC timestamp") from exc
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("UTC timestamp required")
    return dt


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


def _load_exact_module(name: str, path: Path, expected_blob: str) -> ModuleType:
    data = path.read_bytes()
    if _git_blob_sha1(data) != expected_blob:
        raise RuntimeError(f"authorized module blob mismatch before import: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot create module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _role_member(packet: dict[str, Any], role: str) -> dict[str, Any]:
    rows = [m for m in packet["members"] if m["role"] == role and m["execution_required"] is True]
    if len(rows) != 1:
        raise ValueError(f"execution role must resolve uniquely: {role}")
    return rows[0]


def _load_execution_members(repo_root: Path, packet: dict[str, Any]) -> dict[str, bytes]:
    return {
        m["path"]: (repo_root / m["path"]).read_bytes()
        for m in packet["members"] if m["execution_required"] is True
    }


def _load_role_module(repo_root: Path, packet: dict[str, Any], role: str, module_name: str) -> ModuleType:
    member = _role_member(packet, role)
    return _load_exact_module(module_name, repo_root / member["path"], member["git_blob_sha"])


def _validated_grounding_envelope(envelope_bytes: bytes, domain: dict[str, Any], grounding: ModuleType):
    try:
        obj = json.loads(envelope_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid GroundingEnvelope JSON") from exc
    if type(obj) is not dict or set(obj) != ENVELOPE_KEYS:
        raise ValueError("GroundingEnvelope schema drift")
    if type(obj["obligation"]) is not dict or type(obj["artifact"]) is not dict:
        raise TypeError("typed GroundingEnvelope identity required")
    obligation = grounding.ObligationDescriptor(**obj["obligation"])
    artifact = grounding.ArtifactRecord(**obj["artifact"])

    wc = []
    for row in obj["witness_consequences"]:
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError("invalid envelope witness row")
        wc.append({"fact_id": row[0], "status": row[1], "signature_sha256": row[2]})
    gr = []
    for row in obj["grounding_rows"]:
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError("invalid envelope grounding row")
        gr.append({"unit_id": row[0], "left_fact_id": row[1], "right_fact_id": row[2], "status": row[3]})
    ps = []
    for row in obj["path_surfaces"]:
        if not isinstance(row, list) or len(row) != 5:
            raise ValueError("invalid envelope path-surface row")
        ps.append({"unit_id": row[0], "relation_kind": row[1], "left_ref": row[2], "right_ref": row[3], "status": row[4]})
    cd = {}
    if type(obj["contract_digests"]) is not list:
        raise TypeError("contract digest list required")
    for row in obj["contract_digests"]:
        if not isinstance(row, list) or len(row) != 2 or row[0] in cd:
            raise ValueError("invalid/duplicate contract digest row")
        cd[row[0]] = row[1]

    rebuilt = grounding.make_grounding_envelope(
        obligation=obligation, artifact=artifact, domain=domain,
        witness_consequences=wc, grounding_rows=gr, path_surfaces=ps,
        kernel_adjudication=obj["kernel_adjudication"], contract_digests=cd,
    )
    if grounding.envelope_bytes(rebuilt) != envelope_bytes or rebuilt.envelope_sha256 != obj["envelope_sha256"]:
        raise ValueError("GroundingEnvelope canonical identity mismatch")
    return rebuilt


def _validate_realized_g_certificate(cert_bytes: bytes, packet: dict[str, Any], auth: dict[str, Any], envelope) -> dict[str, Any]:
    try:
        cert = json.loads(cert_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid realized-G certificate JSON") from exc
    if type(cert) is not dict or set(cert) != G_CERT_KEYS:
        raise ValueError("realized-G certificate schema drift")
    if cert["certificate_type"] != "VFA-0.2-REALIZED-GROUNDED-COMMON-CAUSE-CONFORMANCE" or cert["status"] != "PASS":
        raise PermissionError("realized-G conformance must PASS")
    if cert["authorization_packet_digest"] != packet["packet_sha256"]:
        raise ValueError("realized-G packet mismatch")
    expected = {
        "selected_candidate_id": envelope.obligation.selected_candidate_id,
        "selected_version": envelope.obligation.selected_version,
        "selection_trace_sha256": envelope.obligation.selection_trace_sha256,
        "wrapper_tar_sha256": envelope.artifact.wrapper_tar_sha256,
        "platform_tar_sha256": envelope.artifact.platform_tar_sha256,
        "executable_sha256": envelope.artifact.executable_sha256,
        "grounding_envelope_sha256": envelope.envelope_sha256,
        "realized_kernel_domain_adjudication": envelope.kernel_adjudication,
    }
    for field, value in expected.items():
        if cert[field] != value:
            raise ValueError(f"realized-G/envelope mismatch: {field}")
    if cert["grounding_unit_count"] != 3 or cert["path_surface_count"] != 12:
        raise ValueError("realized-G domain count mismatch")
    required_pass = (
        "artifact_contract_conformance", "six_witness_execution_conformance",
        "repeat_determinism_conformance", "first_qualifying_rule_conformance",
        "implementation_independence_conformance", "no_arm_access_before_grounding_commit",
        "no_substitution_conformance", "post_disclosure_validity",
    )
    if any(cert[field] != "PASS" for field in required_pass):
        raise PermissionError("realized-G predicate not PASS")
    if cert["common_obligation_sha256_A"] != cert["common_obligation_sha256_B"]:
        raise ValueError("A/B common obligation mismatch")
    if cert["common_grounding_envelope_sha256_A"] != envelope.envelope_sha256 or cert["common_grounding_envelope_sha256_B"] != envelope.envelope_sha256:
        raise ValueError("A/B grounding envelope mismatch")
    if cert["disclosed_at_A"] != cert["disclosed_at_B"] or cert["deadline_A"] != cert["deadline_B"]:
        raise ValueError("A/B disclosure/deadline mismatch")
    times = [
        _parse_utc(auth["freeze_timestamp_utc"]), _parse_utc(cert["selected_at"]),
        _parse_utc(cert["artifact_resolved_at"]), _parse_utc(cert["grounding_committed_at"]),
        _parse_utc(cert["bundle_committed_at"]), _parse_utc(cert["disclosed_at_A"]),
        _parse_utc(cert["deadline_A"]),
    ]
    if not (times[0] < times[1] <= times[2] <= times[3] <= times[4] < times[5] < times[6]):
        raise ValueError("realized-G temporal contract violation")
    return cert


def _expected_mirror(envelope) -> dict[str, Any]:
    return {
        "selected_candidate_id": envelope.obligation.selected_candidate_id,
        "selected_version": envelope.obligation.selected_version,
        "selection_trace_sha256": envelope.obligation.selection_trace_sha256,
        "published_at": envelope.obligation.published_at,
        "release_id": envelope.obligation.release_id,
        "wrapper_tar_sha256": envelope.artifact.wrapper_tar_sha256,
        "platform_tar_sha256": envelope.artifact.platform_tar_sha256,
        "executable_sha256": envelope.artifact.executable_sha256,
        "artifact_integrity_status": envelope.artifact.status,
        "T_future_consequences": [
            {"fact_id": r[0], "status": r[1], "signature_sha256": r[2]}
            for r in envelope.witness_consequences
        ],
        "J_future_grounding_rows": [
            {"unit_id": r[0], "left_fact_id": r[1], "right_fact_id": r[2], "status": r[3]}
            for r in envelope.grounding_rows
        ],
        "path_surfaces": [
            {"unit_id": r[0], "relation_kind": r[1], "left_ref": list(r[2]), "right_ref": list(r[3]), "status": r[4]}
            for r in envelope.path_surfaces
        ],
        "kernel_adjudication": envelope.kernel_adjudication,
        "grounding_envelope_sha256": envelope.envelope_sha256,
    }


def run_authorized_first_endpoint(
    repo_root: str | Path, packet_path: str | Path, freeze_anchor_path: str | Path,
    authorization_certificate_path: str | Path, realized_record_path: str | Path,
    grounding_envelope_path: str | Path, realized_g_certificate_path: str | Path,
) -> dict[str, Any]:
    runtime_facts = validate_runtime_platform()
    root = Path(repo_root).resolve()

    # Bootstrap authority from a pinned custody implementation before any project import.
    custody_path = root / CUSTODY_RELATIVE_PATH
    custody = _load_exact_module("vfa_i_custody", custody_path, EXPECTED_CUSTODY_BLOB)
    packet_bytes = Path(packet_path).read_bytes()
    anchor_bytes = Path(freeze_anchor_path).read_bytes()
    certificate_bytes = Path(authorization_certificate_path).read_bytes()
    realized = _read_json(Path(realized_record_path))
    envelope_bytes = Path(grounding_envelope_path).read_bytes()
    realized_g_bytes = Path(realized_g_certificate_path).read_bytes()

    packet = custody.validate_packet_bytes(packet_bytes)
    runner_member = _role_member(packet, "authorized_first_endpoint_runner")
    if _git_blob_sha1(Path(__file__).read_bytes()) != runner_member["git_blob_sha"]:
        raise RuntimeError("executing runner bytes do not match authorized runner blob")
    if packet["authorized_runner_blob"] != runner_member["git_blob_sha"]:
        raise RuntimeError("packet runner binding mismatch")
    loaded = _load_execution_members(root, packet)
    custody.authorize_execution(packet_bytes, anchor_bytes, certificate_bytes, loaded, realized)
    _packet, _anchor, auth = custody.validate_certificate_bytes(packet_bytes, anchor_bytes, certificate_bytes)

    # Only now load scientific project modules from exact authorized files.
    grounding = _load_role_module(root, packet, "grounded_common_cause_integration_kernel", "vfa_i_grounding")
    materialize = _load_role_module(root, packet, "semantic_treatment_materializer", "vfa_i_materialize")
    endpoint = _load_role_module(root, packet, "first_endpoint_runtime", "vfa_i_endpoint")

    domain = _read_json(root / _role_member(packet, "complete_q_kernel_grounding_domain")["path"])
    envelope = _validated_grounding_envelope(envelope_bytes, domain, grounding)
    realized_g = _validate_realized_g_certificate(realized_g_bytes, packet, auth, envelope)

    mirror = _expected_mirror(envelope)
    for field, expected in mirror.items():
        if realized["realized"][field] != expected:
            raise ValueError(f"realized record does not mirror GroundingEnvelope: {field}")
    conformance = realized["realized"]["realized_common_cause_conformance"]
    if type(conformance) is not dict or set(conformance) != {"status", "certificate_sha256"}:
        raise ValueError("realized common-cause conformance schema drift")
    if conformance["status"] != "PASS" or conformance["certificate_sha256"] != _sha256(realized_g_bytes):
        raise PermissionError("realized record not bound to realized-G certificate")
    if realized["realized"]["bundle_commit_timestamp_utc"] != realized_g["bundle_committed_at"]:
        raise ValueError("bundle timestamp mismatch")
    if realized["realized"]["disclosure_timestamp_utc"] != realized_g["disclosed_at_A"]:
        raise ValueError("disclosure timestamp mismatch")
    if realized["realized"]["deadline_timestamp_utc"] != realized_g["deadline_A"]:
        raise ValueError("deadline timestamp mismatch")

    gamma_a = _read_json(root / _role_member(packet, "treatment_Gamma_A")["path"])
    gamma_b = _read_json(root / _role_member(packet, "treatment_Gamma_B")["path"])
    coordinate_obj = _read_json(root / _role_member(packet, "semantic_coordinate_map")["path"])
    coordinates = coordinate_obj.get("coordinates")
    if type(coordinates) is not dict:
        raise TypeError("semantic coordinate map missing coordinates")
    surfaces = mirror["path_surfaces"]

    matrix_a, mat_trace_a = materialize.compile_semantic_matrix(gamma_a, coordinates)
    matrix_b, mat_trace_b = materialize.compile_semantic_matrix(gamma_b, coordinates)
    if mat_trace_a != mat_trace_b:
        raise RuntimeError("A/B treatment materialization schedule mismatch")
    result_a, run_trace_a = endpoint.evaluate_first_endpoint(matrix_a, coordinates, domain, surfaces)
    result_b, run_trace_b = endpoint.evaluate_first_endpoint(matrix_b, coordinates, domain, surfaces)
    if run_trace_a != run_trace_b:
        raise RuntimeError("A/B first-endpoint schedule mismatch")

    core = {
        "benchmark_id": packet["benchmark_id"],
        "packet_sha256": packet["packet_sha256"],
        "execution_root_sha256": packet["execution_root_sha256"],
        "authorization_certificate_sha256": auth["certificate_sha256"],
        "freeze_commit_sha": auth["freeze_commit_sha"],
        "freeze_timestamp_utc": auth["freeze_timestamp_utc"],
        "grounding_envelope_sha256": envelope.envelope_sha256,
        "realized_g_certificate_sha256": _sha256(realized_g_bytes),
        "kernel_adjudication": envelope.kernel_adjudication,
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
    return {**core, "result_sha256": _sha256(_canonical(core))}


def main() -> None:
    if len(sys.argv) != 8:
        raise SystemExit("usage: I_AUTHORIZED_FIRST_ENDPOINT_RUNNER.py REPO_ROOT PACKET ANCHOR AUTH_CERT REALIZED_RECORD GROUNDING_ENVELOPE REALIZED_G_CERT")
    result = run_authorized_first_endpoint(*sys.argv[1:])
    sys.stdout.buffer.write(_canonical(result) + b"\n")


if __name__ == "__main__":
    main()
