#!/usr/bin/env python3
"""Hostile predicate-I attack for frozen packet v3 and its freeze anchor.

Reads only pre-realization repository artifacts. It never selects, fetches,
grounds, or executes a future obligation. The attack harness is audit
instrumentation and is outside the execution root.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import I_CHAIN_OF_CUSTODY_KERNEL as ck

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKET_PATH = HERE / "I_FREEZE_PACKET_V3.json"
ANCHOR_PATH = HERE / "I_FREEZE_ANCHOR_V3.json"
TEMPLATE_PATH = HERE / "I_REALIZED_RECORD_TEMPLATE.json"
OUT = HERE / "i_chain_of_custody_audit_v3.json"
PACKET_BLOB = "64f5af7182b64b963f334e9c3dddafac4353d5a4"
ANCHOR_BLOB = "5d39f16fd38f5fbfbc8beed5845a37b97c0cb466"
FREEZE_COMMIT = "43535c2badaff7f892141afe9ed8058793950a2f"
FREEZE_TREE = "0cb767b8ab4b9c86466984afc20d11fb400df846"
FREEZE_TIME = "2026-08-15T18:27:57Z"
SYNTHETIC_I_EVIDENCE_BLOB = "a" * 40
SYNTHETIC_AUTH_TIME = "2026-08-15T18:30:00Z"


def expect_reject(fn) -> bool:
    try:
        fn()
    except (TypeError, ValueError, PermissionError, KeyError):
        return True
    return False


def synthetic_certificate(packet: dict, anchor: dict) -> dict:
    cert = {
        "schema_version": "1",
        "benchmark_id": packet["benchmark_id"],
        "packet_manifest_git_blob_sha": PACKET_BLOB,
        "packet_sha256": packet["packet_sha256"],
        "execution_root_sha256": packet["execution_root_sha256"],
        "freeze_anchor_git_blob_sha": ANCHOR_BLOB,
        "freeze_anchor_sha256": anchor["anchor_sha256"],
        "freeze_commit_sha": anchor["freeze_commit_sha"],
        "freeze_tree_sha": anchor["freeze_tree_sha"],
        "freeze_timestamp_utc": anchor["freeze_timestamp_utc"],
        "authorization_timestamp_utc": SYNTHETIC_AUTH_TIME,
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
    anchor_bytes = ANCHOR_PATH.read_bytes()
    packet, anchor = ck.validate_freeze_anchor_bytes(packet_bytes, anchor_bytes)
    template = json.loads(TEMPLATE_PATH.read_text())

    if ck.git_blob_sha1(packet_bytes) != PACKET_BLOB:
        raise AssertionError("frozen packet file blob drift")
    if ck.git_blob_sha1(anchor_bytes) != ANCHOR_BLOB:
        raise AssertionError("freeze anchor file blob drift")
    if anchor["freeze_commit_sha"] != FREEZE_COMMIT or anchor["freeze_tree_sha"] != FREEZE_TREE or anchor["freeze_timestamp_utc"] != FREEZE_TIME:
        raise AssertionError("freeze anchor coordinate drift")

    execution_members = [m for m in packet["members"] if m["execution_required"]]
    loaded = {m["path"]: (ROOT / m["path"]).read_bytes() for m in execution_members}
    ck.validate_loaded_execution(packet, loaded)

    cert = synthetic_certificate(packet, anchor)
    cert_bytes = ck.canonical_bytes(cert)
    realized = synthetic_realized(template, cert)
    positive = ck.authorize_execution(packet_bytes, anchor_bytes, cert_bytes, loaded, realized) == "RUN_IDENTITY_ACCEPTED"

    # A changed-and-rehashed packet is a new packet, so test it against the old anchor/certificate.
    mutant_packet = copy.deepcopy(packet)
    target = next(m for m in mutant_packet["members"] if m["role"] == "validated_substrate_W")
    target["git_blob_sha"] = "0" * 40
    mutant_packet["execution_root_sha256"] = ck.execution_root_sha256(mutant_packet)
    mutant_packet["packet_sha256"] = ck.packet_sha256(mutant_packet)
    mutant_packet_bytes = ck.canonical_bytes(mutant_packet)

    packet_extra_key = copy.deepcopy(packet)
    packet_extra_key["alternative_evaluator_mode"] = "convenient"
    packet_extra_key["packet_sha256"] = ck.packet_sha256(packet_extra_key)

    member_extra_key = copy.deepcopy(packet)
    member_extra_key["members"][0]["loader_hint"] = "alternate"
    member_extra_key["packet_sha256"] = ck.packet_sha256(member_extra_key)

    missing_loaded = dict(loaded)
    missing_loaded.pop(next(iter(missing_loaded)))
    extra_loaded = dict(loaded)
    extra_loaded["empirical/benchmark_v0_2_quotient/construction/POSTGATE_SEMANTIC_KERNEL.py"] = b"superseded"
    wrong_loaded = dict(loaded)
    first_path = next(iter(wrong_loaded))
    wrong_loaded[first_path] = wrong_loaded[first_path] + b"\nDRIFT"

    anchor_extra_key = copy.deepcopy(anchor)
    anchor_extra_key["fallback_commit"] = "0" * 40
    anchor_extra_key["anchor_sha256"] = ck.anchor_sha256(anchor_extra_key)

    anchor_wrong_packet = copy.deepcopy(anchor)
    anchor_wrong_packet["packet_sha256"] = mutant_packet["packet_sha256"]
    anchor_wrong_packet["anchor_sha256"] = ck.anchor_sha256(anchor_wrong_packet)

    old_cert_new_packet = copy.deepcopy(cert)
    old_cert_new_packet_bytes = ck.canonical_bytes(old_cert_new_packet)

    certificate_extra_key = copy.deepcopy(cert)
    certificate_extra_key["alternative_stop_rule"] = "early"
    certificate_extra_key["certificate_sha256"] = ck.certificate_sha256(certificate_extra_key)

    residual_drift_cert = copy.deepcopy(cert)
    residual_drift_cert["H_residual_set"] = ["H_future_distribution"]
    residual_drift_cert["certificate_sha256"] = ck.certificate_sha256(residual_drift_cert)

    failed_pred = copy.deepcopy(cert)
    failed_pred["predicates"]["H"] = "FAIL"
    failed_pred["certificate_sha256"] = ck.certificate_sha256(failed_pred)

    wrong_anchor_cert = copy.deepcopy(cert)
    wrong_anchor_cert["freeze_anchor_git_blob_sha"] = "3" * 40
    wrong_anchor_cert["certificate_sha256"] = ck.certificate_sha256(wrong_anchor_cert)

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
        "rehashed_mutant_packet_under_original_anchor": expect_reject(lambda: ck.validate_freeze_anchor(mutant_packet, mutant_packet_bytes, anchor)),
        "rehashed_mutant_packet_under_original_certificate": expect_reject(lambda: ck.validate_certificate_bytes(mutant_packet_bytes, anchor_bytes, old_cert_new_packet_bytes)),
        "packet_top_level_control_smuggling": expect_reject(lambda: ck.validate_packet(packet_extra_key)),
        "packet_member_control_smuggling": expect_reject(lambda: ck.validate_packet(member_extra_key)),
        "missing_execution_member": expect_reject(lambda: ck.validate_loaded_execution(packet, missing_loaded)),
        "extra_or_superseded_execution_member": expect_reject(lambda: ck.validate_loaded_execution(packet, extra_loaded)),
        "same_path_wrong_bytes": expect_reject(lambda: ck.validate_loaded_execution(packet, wrong_loaded)),
        "freeze_anchor_schema_smuggling": expect_reject(lambda: ck.validate_freeze_anchor(packet, packet_bytes, anchor_extra_key)),
        "freeze_anchor_wrong_packet": expect_reject(lambda: ck.validate_freeze_anchor(packet, packet_bytes, anchor_wrong_packet)),
        "certificate_schema_smuggling": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, anchor, anchor_bytes, certificate_extra_key)),
        "certificate_residual_set_drift": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, anchor, anchor_bytes, residual_drift_cert)),
        "nonpass_predicate_certificate": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, anchor, anchor_bytes, failed_pred)),
        "certificate_wrong_freeze_anchor_blob": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, anchor, anchor_bytes, wrong_anchor_cert)),
        "certificate_content_without_rehash": expect_reject(lambda: ck.validate_certificate(packet, packet_bytes, anchor, anchor_bytes, tampered_cert)),
        "realized_wrong_frozen_parent": expect_reject(lambda: ck.validate_realized_record(cert, wrong_realized_parent)),
        "realized_nested_control_smuggling": expect_reject(lambda: ck.validate_realized_record(cert, realized_nested_extra)),
        "execution_nested_control_smuggling": expect_reject(lambda: ck.validate_realized_record(cert, execution_nested_extra)),
        "realized_top_level_schema_drift": expect_reject(lambda: ck.validate_realized_record(cert, realized_top_level_drift))
    }

    paths = [m["path"] for m in packet["members"]]
    roles = [m["role"] for m in packet["members"]]
    exec_paths = {m["path"] for m in execution_members}
    superseded = set(packet["superseded_or_non_authorized_runtime_artifacts"])
    role_map = {m["role"]: m for m in packet["members"]}
    completeness = {
        "unique_member_paths": len(paths) == len(set(paths)),
        "member_count": len(paths),
        "execution_member_count": len(exec_paths),
        "critical_roles_unique": all(roles.count(r) == 1 for r in ("final_evaluation_rule", "prospective_scope_and_selector", "grounded_common_cause_integration_contract")),
        "superseded_runtime_overlap": sorted(exec_paths & superseded),
        "evaluation_rule_bound": packet["evaluation_rule_blob"] == role_map["final_evaluation_rule"]["git_blob_sha"],
        "future_rule_bound": packet["future_obligation_rule_blob"] == role_map["prospective_scope_and_selector"]["git_blob_sha"],
        "common_cause_rule_bound": packet["common_cause_rule_blob"] == role_map["grounded_common_cause_integration_contract"]["git_blob_sha"],
        "packet_file_blob_bound": ck.git_blob_sha1(packet_bytes) == PACKET_BLOB,
        "anchor_file_blob_bound": ck.git_blob_sha1(anchor_bytes) == ANCHOR_BLOB,
        "rejected_predecessors_preserved": all(r in role_map for r in ("I_candidate_1_rejection_provenance", "I_candidate_2_rejection_provenance")),
        "future_unknown_count": len(packet["future_unknowns_not_packet_members"])
    }
    completeness["pass"] = (
        completeness["unique_member_paths"] and completeness["critical_roles_unique"]
        and not completeness["superseded_runtime_overlap"]
        and completeness["evaluation_rule_bound"] and completeness["future_rule_bound"]
        and completeness["common_cause_rule_bound"] and completeness["packet_file_blob_bound"]
        and completeness["anchor_file_blob_bound"] and completeness["rejected_predecessors_preserved"]
    )

    overall = positive and all(attacks.values()) and completeness["pass"]
    out = {
        "benchmark_id": packet["benchmark_id"],
        "audit_identity": "VFA-0.2-I-CHAIN-OF-CUSTODY-ATTACK-3",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "freeze_anchor": {"commit": FREEZE_COMMIT, "tree": FREEZE_TREE, "timestamp_utc": FREEZE_TIME},
        "packet_manifest_git_blob_sha": PACKET_BLOB,
        "packet_sha256": packet["packet_sha256"],
        "execution_root_sha256": packet["execution_root_sha256"],
        "freeze_anchor_git_blob_sha": ANCHOR_BLOB,
        "freeze_anchor_sha256": anchor["anchor_sha256"],
        "positive_control": positive,
        "completeness": completeness,
        "hostile_identity_attacks": attacks,
        "rejected_attack_count": sum(attacks.values()),
        "attack_count": len(attacks),
        "I_adjudication": "PASS" if overall else "FAIL",
        "scope": "packet/freeze-anchor/certificate/realization/execution identity; no prospective future object accessed",
        "validation_note": "Executable deterministic repository attack. External GitHub commit/tree membership for the frozen packet is separately recorded by the I evidence; this result does not claim GitHub Actions or signer attestation."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
