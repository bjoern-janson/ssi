#!/usr/bin/env python3
"""Hostile predicate-I attack for repaired packet/certificate/execution identity.

Reads only frozen/pre-freeze repository artifacts. It never selects, fetches,
grounds, or executes a future obligation. The attack harness itself is audit
instrumentation and is not an execution-root member.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import I_CHAIN_OF_CUSTODY_KERNEL as ck

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKET_PATH = HERE / "I_FREEZE_PACKET_V2.json"
TEMPLATE_PATH = HERE / "I_REALIZED_RECORD_TEMPLATE.json"
OUT = HERE / "i_chain_of_custody_audit_v2.json"
FREEZE_COMMIT = "4dc3b466af2f420e4a375d28eb37df5512edee70"
FREEZE_TIME = "2026-08-15T18:21:37Z"
PACKET_MANIFEST_GIT_BLOB = "c8eedbea4466dae2ee4e6cfea18c40623eccddfb"
SYNTHETIC_I_EVIDENCE_BLOB = "a" * 40


def expect_reject(fn) -> bool:
    try:
        fn()
    except (TypeError, ValueError, PermissionError, KeyError):
        return True
    return False


def synthetic_certificate(packet: dict) -> dict:
    cert = {
        "schema_version": "1",
        "benchmark_id": packet["benchmark_id"],
        "packet_manifest_git_blob_sha": PACKET_MANIFEST_GIT_BLOB,
        "packet_sha256": packet["packet_sha256"],
        "execution_root_sha256": packet["execution_root_sha256"],
        "freeze_commit_sha": FREEZE_COMMIT,
        "freeze_timestamp_utc": FREEZE_TIME,
        "predicates": {k: "PASS" for k in "ABCDEFGHI"},
        "H_residual_set": list(packet["H_residual_set"]),
        "future_obligation_rule_blob": packet["future_obligation_rule_blob"],
        "evaluation_rule_blob": packet["evaluation_rule_blob"],
        "common_cause_rule_blob": packet["common_cause_rule_blob"],
        "I_evidence_blob": SYNTHETIC_I_EVIDENCE_BLOB,
        "authorization": "AUTHORIZED",
        "state": "AUTHORIZED_FUTURE_NOT_YET_REALIZED"
    }
    cert["certificate_sha256"] = ck.certificate_sha256(cert)
    return cert


def synthetic_realized(template: dict, cert: dict) -> dict:
    obj = copy.deepcopy(template)
    obj["frozen_identity"] = {
        "packet_sha256": cert["packet_sha256"],
        "execution_root_sha256": cert["execution_root_sha256"],
        "authorization_certificate_sha256": cert["certificate_sha256"],
        "freeze_commit_sha": cert["freeze_commit_sha"],
        "freeze_timestamp_utc": cert["freeze_timestamp_utc"]
    }
    return obj


def main() -> None:
    packet_bytes = PACKET_PATH.read_bytes()
    packet = ck.validate_packet_bytes(packet_bytes)
    template = json.loads(TEMPLATE_PATH.read_text())

    if ck.git_blob_sha1(packet_bytes) != PACKET_MANIFEST_GIT_BLOB:
        raise AssertionError("frozen packet file blob drift")

    execution_members = [m for m in packet["members"] if m["execution_required"]]
    loaded = {m["path"]: (ROOT / m["path"]).read_bytes() for m in execution_members}
    ck.validate_loaded_execution(packet, loaded)

    cert = synthetic_certificate(packet)
    cert_bytes = ck.canonical_bytes(cert)
    realized = synthetic_realized(template, cert)
    positive = ck.authorize_execution(packet_bytes, cert_bytes, loaded, realized) == "RUN_IDENTITY_ACCEPTED"

    packet_wrong_blob = copy.deepcopy(packet)
    packet_wrong_blob["members"][0]["git_blob_sha"] = "0" * 40
    packet_wrong_blob["packet_sha256"] = ck.packet_sha256(packet_wrong_blob)

    packet_wrong_role = copy.deepcopy(packet)
    target = next(m for m in packet_wrong_role["members"] if m["role"] == "final_evaluation_rule")
    target["role"] = "DRIFTED_ROLE"
    packet_wrong_role["packet_sha256"] = ck.packet_sha256(packet_wrong_role)

    packet_wrong_critical_binding = copy.deepcopy(packet)
    packet_wrong_critical_binding["evaluation_rule_blob"] = "0" * 40
    packet_wrong_critical_binding["packet_sha256"] = ck.packet_sha256(packet_wrong_critical_binding)

    missing_loaded = dict(loaded)
    missing_loaded.pop(next(iter(missing_loaded)))

    extra_loaded = dict(loaded)
    extra_loaded["empirical/benchmark_v0_2_quotient/construction/POSTGATE_SEMANTIC_KERNEL.py"] = b"superseded"

    wrong_loaded = dict(loaded)
    first_path = next(iter(wrong_loaded))
    wrong_loaded[first_path] = wrong_loaded[first_path] + b"\nDRIFT"

    old_cert = copy.deepcopy(cert)
    old_cert["packet_sha256"] = "1" * 64
    old_cert["certificate_sha256"] = ck.certificate_sha256(old_cert)

    residual_drift_cert = copy.deepcopy(cert)
    residual_drift_cert["H_residual_set"] = ["H_future_distribution"]
    residual_drift_cert["certificate_sha256"] = ck.certificate_sha256(residual_drift_cert)

    failed_pred = copy.deepcopy(cert)
    failed_pred["predicates"]["H"] = "FAIL"
    failed_pred["certificate_sha256"] = ck.certificate_sha256(failed_pred)

    wrong_packet_blob_cert = copy.deepcopy(cert)
    wrong_packet_blob_cert["packet_manifest_git_blob_sha"] = "3" * 40
    wrong_packet_blob_cert["certificate_sha256"] = ck.certificate_sha256(wrong_packet_blob_cert)

    tampered_cert = copy.deepcopy(cert)
    tampered_cert["freeze_timestamp_utc"] = "2099-01-01T00:00:00Z"

    wrong_realized_parent = copy.deepcopy(realized)
    wrong_realized_parent["frozen_identity"]["packet_sha256"] = "2" * 64

    realized_nested_extra = copy.deepcopy(realized)
    realized_nested_extra["realized"]["alternative_evaluator_mode"] = "convenient"

    execution_nested_extra = copy.deepcopy(realized)
    execution_nested_extra["execution"]["alternate_stop_rule"] = "early"

    realized_top_level_drift = copy.deepcopy(realized)
    realized_top_level_drift["replacement_rules"] = {}

    attacks = {
        "packet_member_blob_change_even_after_rehash": expect_reject(lambda: ck.validate_packet(packet_wrong_blob)),
        "critical_member_role_change_even_after_rehash": expect_reject(lambda: ck.validate_packet(packet_wrong_role)),
        "critical_top_level_binding_change_even_after_rehash": expect_reject(lambda: ck.validate_packet(packet_wrong_critical_binding)),
        "missing_execution_member": expect_reject(lambda: ck.validate_loaded_execution(packet, missing_loaded)),
        "extra_or_superseded_execution_member": expect_reject(lambda: ck.validate_loaded_execution(packet, extra_loaded)),
        "same_path_wrong_bytes": expect_reject(lambda: ck.validate_loaded_execution(packet, wrong_loaded)),
        "old_certificate_new_packet": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, old_cert)),
        "certificate_residual_set_drift": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, residual_drift_cert)),
        "nonpass_predicate_certificate": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, failed_pred)),
        "certificate_wrong_packet_file_blob": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, wrong_packet_blob_cert)),
        "certificate_content_without_rehash": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, tampered_cert)),
        "realized_wrong_frozen_parent": expect_reject(lambda: ck.validate_realized_record(cert, wrong_realized_parent)),
        "realized_nested_control_smuggling": expect_reject(lambda: ck.validate_realized_record(cert, realized_nested_extra)),
        "execution_nested_control_smuggling": expect_reject(lambda: ck.validate_realized_record(cert, execution_nested_extra)),
        "realized_top_level_schema_drift": expect_reject(lambda: ck.validate_realized_record(cert, realized_top_level_drift))
    }

    paths = [m["path"] for m in packet["members"]]
    exec_paths = {m["path"] for m in execution_members}
    superseded = set(packet["superseded_or_non_authorized_runtime_artifacts"])
    role_map = {m["role"]: m for m in packet["members"]}
    completeness = {
        "unique_member_paths": len(paths) == len(set(paths)),
        "member_count": len(paths),
        "execution_member_count": len(exec_paths),
        "superseded_runtime_overlap": sorted(exec_paths & superseded),
        "evaluation_rule_bound": packet["evaluation_rule_blob"] == role_map["final_evaluation_rule"]["git_blob_sha"],
        "future_rule_bound": packet["future_obligation_rule_blob"] == role_map["prospective_scope_and_selector"]["git_blob_sha"],
        "common_cause_rule_bound": packet["common_cause_rule_blob"] == role_map["grounded_common_cause_integration_contract"]["git_blob_sha"],
        "packet_file_blob_bound": ck.git_blob_sha1(packet_bytes) == PACKET_MANIFEST_GIT_BLOB,
        "candidate_1_rejection_preserved": "I_candidate_1_rejection_provenance" in role_map,
        "future_unknowns_only_by_rule": len(packet["future_unknowns_not_packet_members"]) == 10
    }
    completeness["pass"] = (
        completeness["unique_member_paths"]
        and not completeness["superseded_runtime_overlap"]
        and completeness["evaluation_rule_bound"]
        and completeness["future_rule_bound"]
        and completeness["common_cause_rule_bound"]
        and completeness["packet_file_blob_bound"]
        and completeness["candidate_1_rejection_preserved"]
        and completeness["future_unknowns_only_by_rule"]
    )

    overall = positive and all(attacks.values()) and completeness["pass"]
    out = {
        "benchmark_id": packet["benchmark_id"],
        "audit_identity": "VFA-0.2-I-CHAIN-OF-CUSTODY-ATTACK-2",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "freeze_anchor": {"commit": FREEZE_COMMIT, "timestamp_utc": FREEZE_TIME},
        "packet_manifest_git_blob_sha": PACKET_MANIFEST_GIT_BLOB,
        "packet_sha256": packet["packet_sha256"],
        "execution_root_sha256": packet["execution_root_sha256"],
        "positive_control": positive,
        "completeness": completeness,
        "hostile_identity_attacks": attacks,
        "rejected_attack_count": sum(attacks.values()),
        "attack_count": len(attacks),
        "I_adjudication": "PASS" if overall else "FAIL",
        "scope": "packet/certificate/realization/execution identity; no prospective future object accessed",
        "validation_note": "Executable deterministic repository attack; this artifact does not claim GitHub Actions or external-CI execution unless separately recorded."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
