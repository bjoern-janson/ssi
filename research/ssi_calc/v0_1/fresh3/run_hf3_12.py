#!/usr/bin/env python3
"""First exposure of frozen successor-v3 to frozen HF3-12.

Expected labels are read only for scoring after checker_resolved derives a certificate.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import checker_resolved as checker

SCHEMA = json.loads((ROOT / "schema.json").read_text())
AUTHORIZED = {"AUTHORIZED", "AUTHORIZED_SCOPED"}
PLAIN_SHA = "0747244689af2caca39c4f692e4c0eccf7ce39cda386c5855620bb8ce286ae33"
GZIP_SHA = "3be543c9b303f9220687e0d933ff0d9eb887ff2ddae7d8d089d9ae36a822ef76"


def load_cases() -> list[dict]:
    packed = base64.b64decode((HERE / "HF3_12.json.gz.b64").read_text().strip())
    assert hashlib.sha256(packed).hexdigest() == GZIP_SHA
    plain = gzip.decompress(packed)
    assert hashlib.sha256(plain).hexdigest() == PLAIN_SHA
    obj = json.loads(plain)
    assert len(obj["cases"]) == 12
    return obj["cases"]


def label(decision: float, overreach: float, false_refusal: float) -> str:
    if decision == 1.0 and overreach == 0.0 and false_refusal == 0.0:
        return "HF3_12_STRONG_PASS"
    if decision >= 11/12 and overreach <= 1/6 and false_refusal <= 1/6:
        return "HF3_12_PASS"
    if decision >= 9/12:
        return "HF3_12_PARTIAL"
    if decision < 9/12 or overreach > 2/6:
        return "HF3_12_FAILED"
    return "HF3_12_PARTIAL"


def main() -> None:
    rows = []
    for case in load_cases():
        got = checker.derive(case, SCHEMA).dict()
        exp = case["expected"]
        pa = got["status"] in AUTHORIZED
        ea = exp["status"] in AUTHORIZED
        checks = {
            "decision": pa == ea,
            "status": got["status"] == exp["status"],
            "locus": got["failure_locus"] == exp["failure_locus"],
            "preserved": set(got["preserved_facts"]) == set(exp["preserved_facts"]),
            "missing": set(got["missing_authority"]) == set(exp["missing_authority"]),
            "reopened": set(got["reopened"]) == set(exp["reopened"]),
        }
        checks["exact"] = all(checks[k] for k in ("status", "locus", "preserved", "missing", "reopened"))
        rows.append({
            "id": case["id"], "family": case["family"], "expected": exp,
            "observed": got, "checks": checks,
            "expected_authorize": ea, "predicted_authorize": pa,
        })

    n = len(rows)
    licensed = sum(r["expected_authorize"] for r in rows)
    unlicensed = n - licensed
    tp = sum(r["expected_authorize"] and r["predicted_authorize"] for r in rows)
    fp = sum((not r["expected_authorize"]) and r["predicted_authorize"] for r in rows)
    fn = sum(r["expected_authorize"] and (not r["predicted_authorize"]) for r in rows)
    tn = sum((not r["expected_authorize"]) and (not r["predicted_authorize"]) for r in rows)
    decision = sum(r["checks"]["decision"] for r in rows) / n
    overreach = fp / unlicensed if unlicensed else 0.0
    false_refusal = fn / licensed if licensed else 0.0

    metrics = {
        "decision_accuracy": decision,
        "overreach_rate": overreach,
        "false_refusal_rate": false_refusal,
        "status_accuracy": sum(r["checks"]["status"] for r in rows) / n,
        "locus_accuracy": sum(r["checks"]["locus"] for r in rows) / n,
        "preserved_accuracy": sum(r["checks"]["preserved"] for r in rows) / n,
        "missing_accuracy": sum(r["checks"]["missing"] for r in rows) / n,
        "reopened_accuracy": sum(r["checks"]["reopened"] for r in rows) / n,
        "exact_certificate_accuracy": sum(r["checks"]["exact"] for r in rows) / n,
    }
    result = {
        "object": "SSI_CALC_V0.1/HF3_12_FIRST_EXPOSURE",
        "successor_v3_freeze_merge": "559ce29d0ace8f518009067639a39ba6ac3994dc",
        "hf3_12_freeze_merge": "b52e99ac4b06b29d5c7318c6fa9186bb76ae34e2",
        "hf3_12_plain_sha256": PLAIN_SHA,
        "kernel_rule_count": len(checker.RULES),
        "rules_added_beyond_R11": 0,
        "confusion_matrix": {"TP": tp, "FP_overreach": fp, "FN_false_refusal": fn, "TN": tn, "licensed": licensed, "unlicensed": unlicensed},
        "metrics": metrics,
        "threshold_status": label(decision, overreach, false_refusal),
        "mismatch_count": sum(not r["checks"]["exact"] for r in rows),
        "decision_error_count": sum(not r["checks"]["decision"] for r in rows),
        "records": rows,
    }
    (HERE / "HF3_12_FIRST_RUN.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("object", "kernel_rule_count", "rules_added_beyond_R11", "confusion_matrix", "metrics", "threshold_status", "mismatch_count", "decision_error_count")}, indent=2))
    bad = [r for r in rows if not r["checks"]["exact"]]
    if bad:
        print(f"--- HF3-12 MISMATCHES ({len(bad)}) ---")
        for r in bad:
            print(json.dumps({
                "id": r["id"], "family": r["family"],
                "expected": {k: r["expected"][k] for k in ("status", "failure_locus", "preserved_facts", "missing_authority", "reopened")},
                "observed": r["observed"], "checks": r["checks"],
            }, sort_keys=True))


if __name__ == "__main__":
    main()
