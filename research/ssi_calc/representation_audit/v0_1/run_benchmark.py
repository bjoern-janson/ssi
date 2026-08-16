#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from checker import evaluate

HERE = Path(__file__).resolve().parent


def main() -> None:
    bench = json.loads((HERE / "benchmark.json").read_text())
    rows = []
    passed = 0
    for case in bench["cases"]:
        result = evaluate(case)
        ok = result["status"] == case["expected_status"]
        passed += int(ok)
        rows.append({
            "id": case["id"],
            "family": case["family"],
            "expected": case["expected_status"],
            "actual": result["status"],
            "passed": ok,
            "collision_count": len(result.get("collisions", [])),
            "reason": result.get("reason"),
        })
    summary = {
        "object": "SSI_CALC_REPRESENTATION_AUDIT_V0.1/BENCHMARK_RESULT_01",
        "status": "PASS" if passed == len(rows) else "FAIL",
        "passed": passed,
        "total": len(rows),
        "rows": rows,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    if passed != len(rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
