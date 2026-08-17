#!/usr/bin/env python3
"""Blind operational jurisdiction assay for SSI-JURISDICTION-FALSIFICATION/S0."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

FORBIDDEN_KEY_FRAGMENTS = ("break", "oracle", "expected", "required_classification", "ground_truth")


def _reject_label_leakage(obj: Any, path: str = "$") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            lk = k.lower()
            if any(fragment in lk for fragment in FORBIDDEN_KEY_FRAGMENTS):
                raise ValueError(f"construction-label leakage forbidden at {path}.{k}")
            _reject_label_leakage(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _reject_label_leakage(v, f"{path}[{i}]")


def classify_case(case: dict) -> dict:
    _reject_label_leakage(case)
    p = case["operational_probes"]

    d = p["detectability"]["reality_0_signal"] != p["detectability"]["reality_1_signal"]
    r = p["reachability"]["authority_boundary_receipt_nonce"] is not None

    lev = p["leverage"]
    if lev["validated_direction"] != "DECREASE":
        raise ValueError("S0 supports only preregistered DECREASE challenge direction")
    l = r and (lev["authority_after"] < lev["authority_before"])

    indep = p["independence"]
    i = indep["authority_clamp_low_signal"] == indep["authority_clamp_high_signal"]

    components = {"D": d, "R": r, "L": l, "I": i}
    failed = [k for k, ok in components.items() if not ok]
    if not failed:
        cls = "J=1"
    elif len(failed) > 1:
        cls = "MULTIPLE_BREAKS"
    else:
        cls = {
            "D": "CHALLENGE_BLIND",
            "R": "CHALLENGE_BLOCKED",
            "L": "AUTHORITY_INERT",
            "I": "CHALLENGE_CIRCULAR",
        }[failed[0]]
    return {
        "case_id": case["case_id"],
        "intact_components": components,
        "classification": cls,
        "jurisdiction": all(components.values()),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cases", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    payload = json.loads(args.cases.read_text())
    results = [classify_case(case) for case in payload["cases"]]
    args.out.write_text(json.dumps({"assay_results": results}, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
