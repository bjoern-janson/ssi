#!/usr/bin/env python3
"""Frozen CUHK-X P1 adjudicator.

Applies only the preregistered P1-A threshold logic to a frozen Shot-1 metrics
artifact. P1-B and P1-C fail closed when their preregistered constitution/input
requirements were not instantiated in the authorized shot.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def canonical_json_bytes(obj) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, required=True)
    ap.add_argument("--metrics", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    cert = json.loads(args.certificate.read_text(encoding="utf-8"))
    metrics = json.loads(args.metrics.read_text(encoding="utf-8"))

    loaded_self = sha256_file(Path(__file__))
    if loaded_self != cert["authorized_execution"]["adjudicator_sha256"]:
        raise RuntimeError("ADJUDICATION_REJECTED_IDENTITY_MISMATCH")
    if metrics.get("scientific_adjudication_performed") is not False:
        raise RuntimeError("metrics artifact was already adjudicated")

    d_exact = float(metrics["deltas"]["exact_set_accuracy"])
    d_bal = float(metrics["deltas"]["candidate_balanced_accuracy"])
    folds = metrics["folds"]
    nonnegative_folds = sum(float(r["delta_exact_set_accuracy"]) >= 0.0 for r in folds)

    p1a_supported = (
        d_exact >= 0.03
        and abs(d_bal) <= 0.01
        and nonnegative_folds >= 4
    )
    p1a = "SUPPORTED_PRESERVED_COMPOSITION" if p1a_supported else "NOT_SUPPORTED_PRESERVED_COMPOSITION"

    sec = metrics["secondary_branch_constitution"]
    p1b = {
        "HAU_sequence": "NOT_IDENTIFIED_UNCONSTITUTED_BRANCH" if not sec.get("HAU_sequence") else "CONSTITUTED_REQUIRES_BRANCH_RESULT",
        "HAU_combination": "NOT_IDENTIFIED_UNCONSTITUTED_BRANCH" if not sec.get("HAU_combination") else "CONSTITUTED_REQUIRES_BRANCH_RESULT",
        "HAU_emotion": "NOT_IDENTIFIED_UNCONSTITUTED_BRANCH" if not sec.get("HAU_emotion") else "CONSTITUTED_REQUIRES_BRANCH_RESULT",
    }

    tc = metrics["transfer_comparator"]
    if tc.get("nested_inner_subject_oof_available"):
        p1c = "CONSTITUTED_REQUIRES_TRANSFER_STATISTIC"
    else:
        p1c = "NOT_IDENTIFIED_UNCONSTITUTED_TRANSFER_COMPARATOR"

    result = {
        "run_id": metrics["run_id"],
        "metrics_sha256": sha256_file(args.metrics),
        "P1_A": p1a,
        "P1_A_gate": {
            "delta_exact_set_accuracy": d_exact,
            "required_min_delta_exact_set_accuracy": 0.03,
            "delta_candidate_balanced_accuracy": d_bal,
            "required_abs_max_delta_candidate_balanced_accuracy": 0.01,
            "nonnegative_exact_set_folds": nonnegative_folds,
            "required_nonnegative_exact_set_folds": 4,
        },
        "P1_B": p1b,
        "P1_C": p1c,
        "P1_C_reason": tc.get("reason"),
        "leaderboard_authority": "NONE",
        "ssi_packet7_authority": "NONE",
        "post_result_rule": (
            "If P1-A is NOT_SUPPORTED, the frozen P1 preservation branch is closed in this composition scope; "
            "no larger preserved-evidence architecture is justified as a P1 rescue."
        ),
    }
    out = canonical_json_bytes(result)
    (args.out / "P1_SHOT1_ADJUDICATION.json").write_bytes(out)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
