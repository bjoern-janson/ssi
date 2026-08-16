#!/usr/bin/env python3
"""Regression harness for the HF2-24-earned obligation-resolution successor.

B64, H24, HF16, and HF2-24 are immutable regression objects. Expected labels are
read only by this scorer after checker_resolved derives a certificate.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRESH = ROOT / "fresh"
HELDOUT = ROOT / "heldout"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import checker_resolved as checker

SCHEMA = json.loads((ROOT / "schema.json").read_text())
AUTHORIZED = {"AUTHORIZED", "AUTHORIZED_SCOPED"}
H24_SHA = "0910569fe786b29f5f1d64c295f8be7f2857ec6447bd2cf3286a336fc121b941"
HF16_SHA = "0744abe38f6d32b32eace1862b571246d5bb256f47b76b4bf179b5c9404372a7"
HF2_SHA = "96498b2f195cdf6ca99e0c5f4efbf99305f2bc7168ff008eda3f6cca14c78218"


def load_packed(path: Path, expected_sha: str) -> list[dict]:
    raw = gzip.decompress(base64.b64decode(path.read_text().strip()))
    assert hashlib.sha256(raw).hexdigest() == expected_sha
    return json.loads(raw)["cases"]


def score(cases: list[dict], name: str) -> dict:
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
            "id": case["id"], "family": case.get("family"), "expected": exp,
            "observed": got, "checks": checks,
            "expected_authorize": ea, "predicted_authorize": pa,
        })

    n = len(rows)
    licensed = sum(r["expected_authorize"] for r in rows)
    unlicensed = n - licensed
    fp = sum((not r["expected_authorize"]) and r["predicted_authorize"] for r in rows)
    fn = sum(r["expected_authorize"] and (not r["predicted_authorize"]) for r in rows)
    return {
        "object": name,
        "metrics": {
            "cases": n,
            "decision_accuracy": sum(r["checks"]["decision"] for r in rows) / n,
            "overreach_rate": fp / unlicensed if unlicensed else 0.0,
            "false_refusal_rate": fn / licensed if licensed else 0.0,
            "status_accuracy": sum(r["checks"]["status"] for r in rows) / n,
            "locus_accuracy": sum(r["checks"]["locus"] for r in rows) / n,
            "preserved_accuracy": sum(r["checks"]["preserved"] for r in rows) / n,
            "missing_accuracy": sum(r["checks"]["missing"] for r in rows) / n,
            "reopened_accuracy": sum(r["checks"]["reopened"] for r in rows) / n,
            "exact_certificate_accuracy": sum(r["checks"]["exact"] for r in rows) / n,
            "mismatch_count": sum(not r["checks"]["exact"] for r in rows),
            "decision_error_count": sum(not r["checks"]["decision"] for r in rows),
        },
        "records": rows,
    }


def main() -> None:
    b64 = [json.loads(p.read_text()) for p in sorted((ROOT / "benchmark").glob("CASE-*.json"))]
    h24 = load_packed(HELDOUT / "H24.json.gz.b64", H24_SHA)
    hf16 = load_packed(FRESH / "HF16.json.gz.b64", HF16_SHA)
    hf2 = load_packed(HERE / "HF2_24.json.gz.b64", HF2_SHA)

    result = {
        "object": "SSI_CALC_V0.1/OBLIGATION_RESOLUTION_REGRESSION",
        "kernel_rule_count": len(checker.RULES),
        "rules_added_beyond_R11": 0,
        "frozen_objects": {"B64": 64, "H24": 24, "HF16": 16, "HF2_24": 24},
        "B64": score(b64, "B64_CONTRACT"),
        "H24": score(h24, "H24_REGRESSION"),
        "HF16": score(hf16, "HF16_REGRESSION"),
        "HF2_24": score(hf2, "HF2_24_REGRESSION"),
    }
    out = HERE / "OBLIGATION_RESOLUTION_REGRESSION_RESULT.json"
    out.write_text(json.dumps(result, indent=2) + "\n")

    summary = {"kernel_rule_count": result["kernel_rule_count"], "rules_added_beyond_R11": 0}
    for bucket in ("B64", "H24", "HF16", "HF2_24"):
        summary[bucket] = result[bucket]["metrics"]
    print(json.dumps(summary, indent=2))

    for bucket in ("B64", "H24", "HF16", "HF2_24"):
        bad = [r for r in result[bucket]["records"] if not r["checks"]["exact"]]
        if bad:
            print(f"--- {bucket} MISMATCHES ({len(bad)}) ---")
            for r in bad:
                print(json.dumps({
                    "id": r["id"], "family": r.get("family"),
                    "expected": {k: r["expected"][k] for k in ("status", "failure_locus", "preserved_facts", "missing_authority", "reopened")},
                    "observed": r["observed"], "checks": r["checks"],
                }, sort_keys=True))


if __name__ == "__main__":
    main()
