#!/usr/bin/env python3
"""Run the frozen 64-case benchmark against SSI-CALC v0.1 R1..R11."""
from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import json

from checker import derive, load_json, RULES

HERE = Path(__file__).resolve().parent
SCHEMA = load_json(HERE / "schema.json")
BENCHMARK = HERE / "benchmark"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Run frozen SSI-CALC v0.1 benchmark")
    parser.add_argument("--output", default="CURRENT_RUN_RESULT.json")
    args = parser.parse_args()
    files = sorted(BENCHMARK.glob("CASE-*.json"))
    records = []
    family = defaultdict(lambda: Counter(total=0, status=0, locus=0, preserved=0, missing=0, reopened=0, exact=0))
    status_confusion = Counter()
    for path in files:
        raw = load_json(path)
        got = derive(raw, SCHEMA).to_dict()
        exp = raw["expected"]
        checks = {
            "status": got["status"] == exp["status"],
            "locus": got["failure_locus"] == exp["failure_locus"],
            "preserved": got["preserved_facts"] == exp["preserved_facts"],
            "missing": got["missing_authority"] == exp["missing_authority"],
            "reopened": got["reopened"] == exp["reopened"],
        }
        exact = all(checks.values())
        fam = raw["family"]
        family[fam]["total"] += 1
        for key, ok in checks.items():
            family[fam][key] += int(ok)
        family[fam]["exact"] += int(exact)
        status_confusion[(exp["status"], got["status"])] += 1
        records.append({
            "id": raw["id"],
            "family": fam,
            "title": raw["title"],
            "expected": {k: exp[k] for k in ["status", "failure_locus", "preserved_facts", "missing_authority", "reopened"]},
            "observed": got,
            "checks": checks,
            "exact": exact,
            "case_sha256": digest(path),
        })

    n = len(records)
    metrics = {}
    for key in ["status", "locus", "preserved", "missing", "reopened"]:
        metrics[f"{key}_accuracy"] = sum(r["checks"][key] for r in records) / n if n else 0.0
    metrics["exact_certificate_accuracy"] = sum(r["exact"] for r in records) / n if n else 0.0

    manifest_text = "\n".join(f"{r['id']} {r['case_sha256']}" for r in records) + "\n"
    result = {
        "object": "SSI_CALC_REFERENCE_CHECKER_V0.1/FROZEN_B64_RUN",
        "kernel": RULES,
        "kernel_rule_count": len(RULES),
        "benchmark_case_count": n,
        "benchmark_manifest_sha256": sha256(manifest_text.encode()).hexdigest(),
        "schema_sha256": digest(HERE / "schema.json"),
        "metrics": metrics,
        "family_metrics": {fam: dict(counts) for fam, counts in sorted(family.items())},
        "status_confusion": [
            {"expected": e, "observed": o, "count": count}
            for (e, o), count in sorted(status_confusion.items())
        ],
        "rule_growth": {
            "rules_added_beyond_R11": 0,
            "trigger_cases": [],
        },
        "records": records,
    }
    out = HERE / args.output
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["object", "kernel_rule_count", "benchmark_case_count", "metrics", "family_metrics", "rule_growth"]}, indent=2))


if __name__ == "__main__":
    main()
