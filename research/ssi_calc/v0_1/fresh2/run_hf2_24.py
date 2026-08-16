#!/usr/bin/env python3
"""First exposure of frozen SSI-CALC successor-v2 to frozen HF2-24.

This runner reads expected labels only for scoring after derivation. checker_live.py
never receives family metadata or expected labels as semantic evidence.
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
import checker_live as checker

SCHEMA = json.loads((ROOT / "schema.json").read_text())
AUTHORIZED = {"AUTHORIZED", "AUTHORIZED_SCOPED"}
PLAIN_SHA = "96498b2f195cdf6ca99e0c5f4efbf99305f2bc7168ff008eda3f6cca14c78218"
GZIP_SHA = "fa0e12c1e01d2465e2e1a1a1de48f2be95662ad3256f1868af2c2346838e8d64"


def load_cases() -> list[dict]:
    packed = base64.b64decode((HERE / "HF2_24.json.gz.b64").read_text().strip())
    assert hashlib.sha256(packed).hexdigest() == GZIP_SHA
    plain = gzip.decompress(packed)
    assert hashlib.sha256(plain).hexdigest() == PLAIN_SHA
    obj = json.loads(plain)
    assert len(obj["cases"]) == 24
    return obj["cases"]


def threshold(decision: float, overreach: float, false_refusal: float) -> str:
    if decision == 1.0 and overreach == 0.0 and false_refusal == 0.0:
        return "HF2_24_STRONG_PASS"
    if decision >= 0.875 and overreach <= 0.125 and false_refusal <= 0.125:
        return "HF2_24_PASS"
    if decision >= 0.75:
        return "HF2_24_PARTIAL"
    if decision < 0.75 or overreach > 0.25:
        return "HF2_24_FAILED"
    return "HF2_24_PARTIAL"


def main() -> None:
    cases = load_cases()
    rows = []
    for case in cases:
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
            "id": case["id"],
            "family": case["family"],
            "expected": exp,
            "observed": got,
            "checks": checks,
            "expected_authorize": ea,
            "predicted_authorize": pa,
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
        "exact_status_accuracy": sum(r["checks"]["status"] for r in rows) / n,
        "shallowest_locus_accuracy": sum(r["checks"]["locus"] for r in rows) / n,
        "preservation_aware_refusal_accuracy": sum(r["checks"]["preserved"] for r in rows) / n,
        "missing_authority_accuracy": sum(r["checks"]["missing"] for r in rows) / n,
        "reopened_set_accuracy": sum(r["checks"]["reopened"] for r in rows) / n,
        "exact_certificate_accuracy": sum(r["checks"]["exact"] for r in rows) / n,
    }

    result = {
        "object": "SSI_CALC_V0.1/HF2_24_FIRST_EXPOSURE",
        "successor_v2_freeze_merge": "ed9ae7ab94f74bbc39aaadad312c40647aed62d9",
        "hf2_24_freeze_merge": "4c7c2c0d4c91fa420053a552759a16934ab42b50",
        "hf2_24_plain_sha256": PLAIN_SHA,
        "kernel_rule_count": len(checker.RULES),
        "rules_added_beyond_R11": 0,
        "confusion_matrix": {
            "TP": tp,
            "FP_overreach": fp,
            "FN_false_refusal": fn,
            "TN": tn,
            "licensed": licensed,
            "unlicensed": unlicensed,
        },
        "metrics": metrics,
        "threshold_status": threshold(decision, overreach, false_refusal),
        "mismatch_count": sum(not r["checks"]["exact"] for r in rows),
        "decision_error_count": sum(not r["checks"]["decision"] for r in rows),
        "records": rows,
    }
    out = HERE / "HF2_24_FIRST_RUN.json"
    out.write_text(json.dumps(result, indent=2) + "\n")

    print(json.dumps({k: result[k] for k in (
        "object", "kernel_rule_count", "rules_added_beyond_R11", "confusion_matrix",
        "metrics", "threshold_status", "mismatch_count", "decision_error_count"
    )}, indent=2))

    bad = [r for r in rows if not r["checks"]["exact"]]
    if bad:
        print(f"--- HF2-24 MISMATCHES ({len(bad)}) ---")
        for r in bad:
            print(json.dumps({
                "id": r["id"],
                "family": r["family"],
                "expected": {k: r["expected"][k] for k in ("status", "failure_locus", "preserved_facts", "missing_authority", "reopened")},
                "observed": r["observed"],
                "checks": r["checks"],
            }, sort_keys=True))


if __name__ == "__main__":
    main()
