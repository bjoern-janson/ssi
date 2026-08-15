#!/usr/bin/env python3
"""Executable hostile predicate-I attack for frozen packet 7.

Uses only frozen/pre-realization artifacts plus synthetic contract-valid future
objects. It never selects/fetches a real future obligation or produces scientific
future evidence. The authorized runner itself is executed as a subprocess.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKET = HERE / "I_FREEZE_PACKET_V7.json"
ANCHOR = HERE / "I_FREEZE_ANCHOR_V7.json"
REALIZED_TEMPLATE = HERE / "I_REALIZED_RECORD_TEMPLATE.json"
RUNNER = HERE / "I_AUTHORIZED_FIRST_ENDPOINT_RUNNER_V2.py"
CUSTODY = HERE / "I_CHAIN_OF_CUSTODY_KERNEL_V2.py"
GROUNDING = HERE / "G_GROUNDING_INTEGRATION_KERNEL.py"
DOMAIN = HERE / "FUTURE_GROUNDING_DOMAIN.json"
OUT = HERE / "i_chain_of_custody_audit_v7.json"

PACKET_BLOB = "9781f8c918263fba11ea6ad3a2e735f75755668f"
ANCHOR_BLOB = "94be872e1cc281ddb4dfefec0a851f0079e1c12f"
CUSTODY_BLOB = "184c31de33a8ba617f1ec51b66dbdfe5ad0d9413"
GROUNDING_BLOB = "17852fd8922b9284415aa64abbeabf09811dd816"
FREEZE_TIME = "2026-08-15T18:50:48Z"
AUTH_TIME = "2026-08-15T18:51:48Z"


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_exact(name: str, path: Path, blob: str):
    data = path.read_bytes()
    if git_blob(data) != blob:
        raise AssertionError(f"audit dependency blob drift: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def write_json(path: Path, obj) -> None:
    path.write_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def run_runner(files: dict[str, Path], *, pythonpath: str | None = None, runner: Path = RUNNER):
    env = os.environ.copy()
    if pythonpath is not None:
        env["PYTHONPATH"] = pythonpath
    cmd = [
        sys.executable, str(runner), str(ROOT), str(files["packet"]), str(files["anchor"]),
        str(files["auth"]), str(files["realized"]), str(files["envelope"]), str(files["gcert"]),
    ]
    return subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=30)


def rejected(proc) -> bool:
    return proc.returncode != 0


def main() -> None:
    custody = load_exact("audit_custody_v2", CUSTODY, CUSTODY_BLOB)
    grounding = load_exact("audit_grounding", GROUNDING, GROUNDING_BLOB)
    packet_bytes = PACKET.read_bytes()
    anchor_bytes = ANCHOR.read_bytes()
    packet, anchor = custody.validate_freeze_anchor_bytes(packet_bytes, anchor_bytes)
    if git_blob(packet_bytes) != PACKET_BLOB or git_blob(anchor_bytes) != ANCHOR_BLOB:
        raise AssertionError("packet/anchor blob drift")

    domain = json.loads(DOMAIN.read_text())
    facts = list(domain["source_fact_ids"])
    unit_status = {u["unit_id"]: ("DISTINGUISHED" if i == 0 else "EQUIVALENT") for i, u in enumerate(domain["grounding_units"])}
    witness = [
        {"fact_id": fact, "status": "IDENTIFIED", "signature_sha256": hashlib.sha256(("effect:" + fact).encode()).hexdigest()}
        for fact in facts
    ]
    ground_rows = [
        {"unit_id": u["unit_id"], "left_fact_id": u["left_fact_id"], "right_fact_id": u["right_fact_id"], "status": unit_status[u["unit_id"]]}
        for u in domain["grounding_units"]
    ]
    surfaces = [
        {"unit_id": s["unit_id"], "relation_kind": s["relation_kind"], "left_ref": s["left_ref"], "right_ref": s["right_ref"], "status": unit_status[s["unit_id"]]}
        for s in domain["path_surfaces"]
    ]
    obligation = grounding.ObligationDescriptor(
        selected_candidate_id="synthetic-release-9.9.9", selected_version="9.9.9",
        published_at="2030-01-02T00:00:00Z", release_id=999999,
        selection_trace_sha256="1" * 64,
    )
    artifact = grounding.ArtifactRecord(
        status="IDENTIFIED", selected_version="9.9.9",
        wrapper_tar_sha256="2" * 64, platform_tar_sha256="3" * 64,
        executable_sha256="4" * 64,
    )
    envelope = grounding.make_grounding_envelope(
        obligation=obligation, artifact=artifact, domain=domain,
        witness_consequences=witness, grounding_rows=ground_rows,
        path_surfaces=surfaces, kernel_adjudication="NONINCLUSION_WITNESS",
        contract_digests={"synthetic_attack_contract":"5" * 64},
    )
    envelope_bytes = grounding.envelope_bytes(envelope)

    cert = {
        "schema_version":"1", "benchmark_id":packet["benchmark_id"],
        "packet_manifest_git_blob_sha":PACKET_BLOB, "packet_sha256":packet["packet_sha256"],
        "execution_root_sha256":packet["execution_root_sha256"],
        "freeze_anchor_git_blob_sha":ANCHOR_BLOB, "freeze_anchor_sha256":anchor["anchor_sha256"],
        "freeze_commit_sha":anchor["freeze_commit_sha"], "freeze_tree_sha":anchor["freeze_tree_sha"],
        "freeze_timestamp_utc":FREEZE_TIME, "authorization_timestamp_utc":AUTH_TIME,
        "predicates":{k:"PASS" for k in "ABCDEFGHI"}, "H_residual_set":packet["H_residual_set"],
        "future_obligation_rule_blob":packet["future_obligation_rule_blob"],
        "evaluation_rule_blob":packet["evaluation_rule_blob"],
        "common_cause_rule_blob":packet["common_cause_rule_blob"],
        "authorized_runner_blob":packet["authorized_runner_blob"], "I_evidence_blob":"6" * 40,
        "authorization":"AUTHORIZED", "state":"AUTHORIZED_FUTURE_NOT_YET_REALIZED",
    }
    cert["certificate_sha256"] = custody.certificate_sha256(cert)

    gcert = {
        "certificate_type":"VFA-0.2-REALIZED-GROUNDED-COMMON-CAUSE-CONFORMANCE", "status":"PASS",
        "authorization_packet_digest":packet["packet_sha256"],
        "selected_candidate_id":obligation.selected_candidate_id, "selected_version":obligation.selected_version,
        "selection_trace_sha256":obligation.selection_trace_sha256,
        "selected_at":"2030-01-02T00:00:01Z", "artifact_resolved_at":"2030-01-02T00:00:02Z",
        "wrapper_tar_sha256":artifact.wrapper_tar_sha256, "platform_tar_sha256":artifact.platform_tar_sha256,
        "executable_sha256":artifact.executable_sha256, "artifact_contract_conformance":"PASS",
        "six_witness_execution_conformance":"PASS", "repeat_determinism_conformance":"PASS",
        "grounding_unit_count":3, "path_surface_count":12,
        "grounding_envelope_sha256":envelope.envelope_sha256,
        "grounding_committed_at":"2030-01-02T00:00:03Z", "bundle_committed_at":"2030-01-02T00:00:04Z",
        "disclosed_at_A":"2030-01-02T00:00:05Z", "disclosed_at_B":"2030-01-02T00:00:05Z",
        "deadline_A":"2030-01-03T00:00:00Z", "deadline_B":"2030-01-03T00:00:00Z",
        "common_obligation_sha256_A":"7" * 64, "common_obligation_sha256_B":"7" * 64,
        "common_grounding_envelope_sha256_A":envelope.envelope_sha256,
        "common_grounding_envelope_sha256_B":envelope.envelope_sha256,
        "first_qualifying_rule_conformance":"PASS", "implementation_independence_conformance":"PASS",
        "no_arm_access_before_grounding_commit":"PASS", "no_substitution_conformance":"PASS",
        "realized_kernel_domain_adjudication":"NONINCLUSION_WITNESS", "post_disclosure_validity":"PASS",
        "rule":"synthetic construction-side attack fixture; no real future event",
    }
    gcert_bytes = json.dumps(gcert, sort_keys=True, separators=(",", ":")).encode()

    template = json.loads(REALIZED_TEMPLATE.read_text())
    realized = copy.deepcopy(template)
    realized["frozen_identity"] = {
        "packet_sha256":packet["packet_sha256"], "execution_root_sha256":packet["execution_root_sha256"],
        "authorization_certificate_sha256":cert["certificate_sha256"],
        "freeze_commit_sha":anchor["freeze_commit_sha"], "freeze_timestamp_utc":anchor["freeze_timestamp_utc"],
    }
    realized["realized"].update({
        "selected_candidate_id":obligation.selected_candidate_id, "selected_version":obligation.selected_version,
        "selection_trace_sha256":obligation.selection_trace_sha256, "published_at":obligation.published_at,
        "release_id":obligation.release_id, "wrapper_tar_sha256":artifact.wrapper_tar_sha256,
        "platform_tar_sha256":artifact.platform_tar_sha256, "executable_sha256":artifact.executable_sha256,
        "artifact_integrity_status":artifact.status, "witness_execution_records":[],
        "T_future_consequences":[{"fact_id":r[0],"status":r[1],"signature_sha256":r[2]} for r in envelope.witness_consequences],
        "J_future_grounding_rows":[{"unit_id":r[0],"left_fact_id":r[1],"right_fact_id":r[2],"status":r[3]} for r in envelope.grounding_rows],
        "path_surfaces":[{"unit_id":r[0],"relation_kind":r[1],"left_ref":list(r[2]),"right_ref":list(r[3]),"status":r[4]} for r in envelope.path_surfaces],
        "kernel_adjudication":envelope.kernel_adjudication, "grounding_envelope_sha256":envelope.envelope_sha256,
        "bundle_commit_timestamp_utc":gcert["bundle_committed_at"], "disclosure_timestamp_utc":gcert["disclosed_at_A"],
        "deadline_timestamp_utc":gcert["deadline_A"],
        "realized_common_cause_conformance":{"status":"PASS","certificate_sha256":sha256(gcert_bytes)},
    })

    with tempfile.TemporaryDirectory(prefix="vfa_i_attack_") as td:
        td = Path(td)
        files = {k: td / name for k, name in {
            "packet":"packet.json", "anchor":"anchor.json", "auth":"auth.json", "realized":"realized.json",
            "envelope":"envelope.json", "gcert":"gcert.json"}.items()}
        files["packet"].write_bytes(packet_bytes); files["anchor"].write_bytes(anchor_bytes)
        write_json(files["auth"], cert); write_json(files["realized"], realized)
        files["envelope"].write_bytes(envelope_bytes); files["gcert"].write_bytes(gcert_bytes)

        positive = run_runner(files)
        if positive.returncode != 0:
            raise AssertionError(f"positive authorized synthetic execution failed: {positive.stderr}")
        result = json.loads(positive.stdout)

        # Ambient project-name shadowing must not affect the exact-path/blob loader.
        shadow = td / "shadow"; shadow.mkdir()
        for name in ("I_CHAIN_OF_CUSTODY_KERNEL_V2.py", "FINAL_POSTGATE_RUNTIME.py", "FINAL_TREATMENT_MATERIALIZATION.py", "G_GROUNDING_INTEGRATION_KERNEL.py"):
            (shadow / name).write_text("raise RuntimeError('AMBIENT_SHADOW_EXECUTED')\n")
        shadow_run = run_runner(files, pythonpath=str(shadow))

        attacks = {}
        def attempt(name, mutate=None, runner=RUNNER):
            local = {k: td / (name + "_" + v.name) for k, v in files.items()}
            for k in files: local[k].write_bytes(files[k].read_bytes())
            if mutate: mutate(local)
            attacks[name] = rejected(run_runner(local, runner=runner))

        def early_auth(local):
            x=json.loads(local["auth"].read_text()); x["authorization_timestamp_utc"]=FREEZE_TIME; x["certificate_sha256"]=custody.certificate_sha256(x); write_json(local["auth"],x)
        attempt("authorization_not_after_freeze", early_auth)

        def cert_extra(local):
            x=json.loads(local["auth"].read_text()); x["alternate_stop_rule"]="early"; x["certificate_sha256"]=custody.certificate_sha256(x); write_json(local["auth"],x)
        attempt("certificate_schema_smuggling", cert_extra)

        def realized_extra(local):
            x=json.loads(local["realized"].read_text()); x["realized"]["alternative_evaluator_mode"]="convenient"; write_json(local["realized"],x)
        attempt("realized_schema_smuggling", realized_extra)

        def mirror_forge(local):
            x=json.loads(local["realized"].read_text()); x["realized"]["J_future_grounding_rows"][0]["status"]="EQUIVALENT"; write_json(local["realized"],x)
        attempt("realized_future_status_forge", mirror_forge)

        def envelope_forge(local):
            x=json.loads(local["envelope"].read_text()); x["grounding_rows"][0][3]="EQUIVALENT"; write_json(local["envelope"],x)
        attempt("grounding_envelope_forge", envelope_forge)

        def gcert_env_mismatch(local):
            x=json.loads(local["gcert"].read_text()); x["grounding_envelope_sha256"]="8"*64; write_json(local["gcert"],x)
            r=json.loads(local["realized"].read_text()); r["realized"]["realized_common_cause_conformance"]["certificate_sha256"]=sha256(local["gcert"].read_bytes()); write_json(local["realized"],r)
        attempt("realized_G_envelope_mismatch", gcert_env_mismatch)

        def gcert_time(local):
            x=json.loads(local["gcert"].read_text()); x["disclosed_at_A"]="2030-01-02T00:00:03Z"; x["disclosed_at_B"]="2030-01-02T00:00:03Z"; write_json(local["gcert"],x)
            r=json.loads(local["realized"].read_text()); r["realized"]["disclosure_timestamp_utc"]=x["disclosed_at_A"]; r["realized"]["realized_common_cause_conformance"]["certificate_sha256"]=sha256(local["gcert"].read_bytes()); write_json(local["realized"],r)
        attempt("realized_G_temporal_violation", gcert_time)

        def gcert_arm(local):
            x=json.loads(local["gcert"].read_text()); x["common_obligation_sha256_B"]="9"*64; write_json(local["gcert"],x)
            r=json.loads(local["realized"].read_text()); r["realized"]["realized_common_cause_conformance"]["certificate_sha256"]=sha256(local["gcert"].read_bytes()); write_json(local["realized"],r)
        attempt("realized_G_arm_identity_divergence", gcert_arm)

        def packet_mut(local):
            x=json.loads(local["packet"].read_text()); x["H_residual_set"]=["H_future_distribution"]; x["packet_sha256"]=custody.packet_sha256(x); write_json(local["packet"],x)
        attempt("rehashed_packet_under_old_anchor_certificate", packet_mut)

        # Modified runner bytes must fail their own packet-bound self identity.
        modified_runner = td / "modified_runner.py"
        modified_runner.write_bytes(RUNNER.read_bytes() + b"\n# drift\n")
        attacks["modified_authorized_runner_bytes"] = rejected(run_runner(files, runner=modified_runner))

        loaded = {m["path"]:(ROOT/m["path"]).read_bytes() for m in packet["members"] if m["execution_required"]}
        custody.validate_loaded_execution(packet, loaded)
        missing = dict(loaded); missing.pop(next(iter(missing)))
        extra = dict(loaded); extra["undeclared.py"] = b"x"
        wrong = dict(loaded); p=next(iter(wrong)); wrong[p]=wrong[p]+b"drift"
        direct_rejections = {
            "missing_execution_member": False,
            "extra_execution_member": False,
            "wrong_execution_member_bytes": False,
        }
        for key,obj in (("missing_execution_member",missing),("extra_execution_member",extra),("wrong_execution_member_bytes",wrong)):
            try: custody.validate_loaded_execution(packet,obj)
            except Exception: direct_rejections[key]=True

        overall = (
            shadow_run.returncode == 0 and result.get("result_sha256") and
            all(attacks.values()) and all(direct_rejections.values())
        )
        audit = {
            "benchmark_id":packet["benchmark_id"], "audit_identity":"VFA-0.2-I-CHAIN-OF-CUSTODY-ATTACK-7",
            "future_obligation_accessed":False, "real_future_execution":False,
            "packet_sha256":packet["packet_sha256"], "execution_root_sha256":packet["execution_root_sha256"],
            "packet_manifest_git_blob_sha":PACKET_BLOB, "freeze_anchor_sha256":anchor["anchor_sha256"],
            "freeze_anchor_git_blob_sha":ANCHOR_BLOB, "freeze_commit_sha":anchor["freeze_commit_sha"],
            "freeze_tree_sha":anchor["freeze_tree_sha"], "freeze_timestamp_utc":anchor["freeze_timestamp_utc"],
            "runtime":{"implementation":sys.implementation.name,"python_version":__import__('platform').python_version(),"system":__import__('platform').system(),"machine":__import__('platform').machine()},
            "positive_synthetic_authorized_execution":True,
            "positive_result_sha256":result["result_sha256"],
            "ambient_shadowing_positive_control":shadow_run.returncode == 0,
            "hostile_runner_attacks":attacks,
            "direct_member_set_attacks":direct_rejections,
            "hostile_attack_count":len(attacks)+len(direct_rejections),
            "hostile_rejected_count":sum(attacks.values())+sum(direct_rejections.values()),
            "I_identity":"PASS" if overall else "FAIL", "I_completeness":"PASS" if overall else "FAIL",
            "I_immutability":"PASS" if overall else "FAIL", "I_execution":"PASS" if overall else "FAIL",
            "I_provenance":"PASS" if overall else "FAIL", "I_adjudication":"PASS" if overall else "FAIL",
            "validation_scope":"synthetic future objects only; real future obligation remains untouched",
        }
        OUT.write_text(json.dumps(audit, indent=2, sort_keys=True)+"\n")
        print(json.dumps(audit, sort_keys=True))
        if not overall:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
