#!/usr/bin/env python3
"""Execute and adjudicate the frozen Stage-0 jurisdiction assay."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def adjudicate(results_path: Path, key_path: Path) -> dict:
    results = {x["case_id"]: x for x in json.loads(results_path.read_text())["assay_results"]}
    key = {x["case_id"]: x for x in json.loads(key_path.read_text())["oracle"]}
    if set(results) != set(key):
        return {"pass": False, "reason": "CASE_ID_SET_MISMATCH", "cases": []}
    rows = []
    for cid in sorted(key):
        got, exp = results[cid], key[cid]
        component_ok = got["intact_components"] == exp["intact_components"]
        class_ok = got["classification"] == exp["required_classification"]
        jurisdiction_ok = got["jurisdiction"] == exp["jurisdiction_required"]
        rows.append({
            "case_id": cid,
            "component_ok": component_ok,
            "classification_ok": class_ok,
            "jurisdiction_ok": jurisdiction_ok,
            "pass": component_ok and class_ok and jurisdiction_ok,
            "observed": got,
            "required": exp,
        })
    return {"pass": all(x["pass"] for x in rows), "cases": rows}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--freeze-sha", required=True)
    p.add_argument("--out-dir", required=True, type=Path)
    args = p.parse_args()
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    constit_cases = out / "constitution_cases.json"
    constit_key = out / "constitution_key.json"
    constit_res = out / "constitution_assay.json"
    fresh_cases = out / "fresh_cases.json"
    fresh_key = out / "fresh_key.json"
    fresh_res = out / "fresh_assay.json"

    run("controlled_breaks.py", "--cases", str(constit_cases), "--key", str(constit_key))
    run("jurisdiction_assay.py", "--cases", str(constit_cases), "--out", str(constit_res))
    run("fresh_breaks.py", "--freeze-sha", args.freeze_sha, "--cases", str(fresh_cases), "--key", str(fresh_key))
    run("jurisdiction_assay.py", "--cases", str(fresh_cases), "--out", str(fresh_res))

    constit = adjudicate(constit_res, constit_key)
    fresh = adjudicate(fresh_res, fresh_key)
    s0_valid = constit["pass"] and fresh["pass"]
    terminal = "S0_VALID" if s0_valid else "OPERATIONALIZATION_INADEQUATE"

    result = {
        "object_id": "SSI-JURISDICTION-FALSIFICATION/S0",
        "freeze_sha": args.freeze_sha,
        "constitution": constit,
        "fresh": fresh,
        "gate": {
            "S0_VALID": s0_valid,
            "terminal_state": terminal,
            "stage1_authority": "PERMITTED_TO_CONSTITUTE" if s0_valid else "NONE_STOP",
        },
        "artifact_sha256": {
            p.name: sha256(p)
            for p in (constit_cases, constit_key, constit_res, fresh_cases, fresh_key, fresh_res)
        },
    }
    result_path = out / "STAGE0_RESULT.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    total_constit = len(constit["cases"])
    total_fresh = len(fresh["cases"])
    pass_constit = sum(x["pass"] for x in constit["cases"])
    pass_fresh = sum(x["pass"] for x in fresh["cases"])
    md = f"""# SSI Jurisdiction Falsification — Stage 0 Adjudication\n\n- Object: `SSI-JURISDICTION-FALSIFICATION/S0`\n- Specification freeze: `{args.freeze_sha}`\n- Constitution fixtures: `{pass_constit}/{total_constit}` exact localization passes\n- Fresh post-freeze fixtures: `{pass_fresh}/{total_fresh}` exact localization passes\n- Terminal state: `{terminal}`\n- Stage-1 authority: `{result['gate']['stage1_authority']}`\n\nThe assay was never given the oracle construction labels. Single-component breaks require the exact named failure classification; multi-break cases require the exact component-state vector and `MULTIPLE_BREAKS`.\n"""
    (out / "STAGE0_ADJUDICATION.md").write_text(md)

    print(json.dumps({
        "terminal_state": terminal,
        "constitution": f"{pass_constit}/{total_constit}",
        "fresh": f"{pass_fresh}/{total_fresh}",
        "result_sha256": sha256(result_path),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
