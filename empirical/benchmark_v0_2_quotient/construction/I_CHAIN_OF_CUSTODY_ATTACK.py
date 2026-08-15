#!/usr/bin/env python3
"""Hostile predicate-I attack for packet/certificate/execution identity.

This script reads only frozen/pre-freeze repository artifacts. It never selects,
fetches, grounds, or executes a future obligation.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import I_CHAIN_OF_CUSTODY_KERNEL as ck

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKET_PATH = HERE / "I_FREEZE_PACKET.json"
TEMPLATE_PATH = HERE / "I_REALIZED_RECORD_TEMPLATE.json"
OUT = HERE / "i_chain_of_custody_audit.json"
FREEZE_COMMIT = "962e41235852768505d7a0e626c748e766a51734"
FREEZE_TIME = "2026-08-15T18:17:44Z"


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
        "packet_sha256": packet["packet_sha256"],
        "execution_root_sha256": packet["execution_root_sha256"],
        "freeze_commit_sha": FREEZE_COMMIT,
        "freeze_timestamp_utc": FREEZE_TIME,
        "predicates": {k: "PASS" for k in "ABCDEFGHI"},
        "H_residual_set": packet["H_residual_set"],
        "future_obligation_rule_blob": packet["future_obligation_rule_blob"],
        "evaluation_rule_blob": packet["evaluation_rule_blob"],
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
    packet = json.loads(PACKET_PATH.read_text())
    template = json.loads(TEMPLATE_PATH.read_text())
    ck.validate_packet(packet)

    execution_members = [m for m in packet["members"] if m["execution_required"]]
    loaded = {m["path"]: (ROOT / m["path"]).read_bytes() for m in execution_members}
    ck.validate_loaded_execution(packet, loaded)

    cert = synthetic_certificate(packet)
    realized = synthetic_realized(template, cert)
    positive = ck.authorize_execution(packet, cert, loaded, realized) == "RUN_IDENTITY_ACCEPTED"

    packet_wrong_blob = copy.deepcopy(packet)
    packet_wrong_blob["members"][0]["git_blob_sha"] = "0" * 40

    packet_wrong_role = copy.deepcopy(packet)
    packet_wrong_role["members"][0]["role"] = "DRIFTED_ROLE"

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

    failed_pred = copy.deepcopy(cert)
    failed_pred["predicates"]["H"] = "FAIL"
    failed_pred["certificate_sha256"] = ck.certificate_sha256(failed_pred)

    tampered_cert = copy.deepcopy(cert)
    tampered_cert["freeze_timestamp_utc"] = "2099-01-01T00:00:00Z"

    wrong_realized_parent = copy.deepcopy(realized)
    wrong_realized_parent["frozen_identity"]["packet_sha256"] = "2" * 64

    realized_override = copy.deepcopy(realized)
    realized_override["realized"]["packet_sha256"] = packet["packet_sha256"]

    realized_schema_drift = copy.deepcopy(realized)
    realized_schema_drift["replacement_rules"] = {}

    attacks = {
        "packet_member_blob_change": expect_reject(lambda: ck.validate_packet(packet_wrong_blob)),
        "packet_member_role_change": expect_reject(lambda: ck.validate_packet(packet_wrong_role)),
        "missing_execution_member": expect_reject(lambda: ck.validate_loaded_execution(packet, missing_loaded)),
        "extra_or_superseded_execution_member": expect_reject(lambda: ck.validate_loaded_execution(packet, extra_loaded)),
        "same_path_wrong_bytes": expect_reject(lambda: ck.validate_loaded_execution(packet, wrong_loaded)),
        "old_certificate_new_packet": expect_reject(lambda: ck.validate_certificate(packet, old_cert)),
        "nonpass_predicate_certificate": expect_reject(lambda: ck.validate_certificate(packet, failed_pred)),
        "certificate_content_without_rehash": expect_reject(lambda: ck.validate_certificate(packet, tampered_cert)),
        "realized_wrong_frozen_parent": expect_reject(lambda: ck.validate_realized_record(cert, wrong_realized_parent)),
        "realized_override_of_packet_identity": expect_reject(lambda: ck.validate_realized_record(cert, realized_override)),
        "realized_top_level_schema_drift": expect_reject(lambda: ck.validate_realized_record(cert, realized_schema_drift))
    }

    paths = [m["path"] for m in packet["members"]]
    exec_paths = {m["path"] for m in execution_members}
    superseded = set(packet["superseded_or_non_authorized_runtime_artifacts"])
    completeness = {
        "unique_member_paths": len(paths) == len(set(paths)),
        "member_count": len(paths),
        "execution_member_count": len(exec_paths),
        "superseded_runtime_overlap": sorted(exec_paths & superseded),
        "future_unknowns_absent_from_member_paths": all(x not in exec_paths for x in packet["future_unknowns_not_packet_members"]),
        "evaluation_rule_bound": packet["evaluation_rule_blob"] == next(m["git_blob_sha"] for m in packet["members"] if m["role"] == "final_evaluation_rule"),
        "future_rule_bound": packet["future_obligation_rule_blob"] == next(m["git_blob_sha"] for m in packet["members"] if m["role"] == "prospective_scope_and_selector")
    }
    completeness["pass"] = (
        completeness["unique_member_paths"]
        and not completeness["superseded_runtime_overlap"]
        and completeness["evaluation_rule_bound"]
        and completeness["future_rule_bound"]
    )

    overall = positive and all(attacks.values()) and completeness["pass"]
    out = {
        "benchmark_id": packet["benchmark_id"],
        "audit_identity": "VFA-0.2-I-CHAIN-OF-CUSTODY-ATTACK-1",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "freeze_anchor": {"commit": FREEZE_COMMIT, "timestamp_utc": FREEZE_TIME},
        "packet_sha256": packet["packet_sha256"],
        "execution_root_sha256": packet["execution_root_sha256"],
        "positive_control": positive,
        "completeness": completeness,
        "hostile_identity_attacks": attacks,
        "rejected_attack_count": sum(attacks.values()),
        "attack_count": len(attacks),
        "I_adjudication": "PASS" if overall else "FAIL",
        "scope": "packet/certificate/realization/execution identity; no prospective future object accessed",
        "validation_note": "Executable deterministic repository attack; result must not be represented as GitHub Actions or external CI unless such a run is separately recorded."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
