#!/usr/bin/env python3
"""Reproduce the frozen SSI-CALC v0.1 H24 execution without mutating frozen inputs."""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE
DEFAULT_CHECKER = HERE.parent / "checker.py"
DEFAULT_SCHEMA = HERE.parent / "schema.json"
FROZEN_CHECKER_SHA256 = "12f3256abf2755fe6f1b9fdb104b9f7b3038713f8bab6260b4f09ad956d42baa"
FROZEN_H24_SHA256 = "0910569fe786b29f5f1d64c295f8be7f2857ec6447bd2cf3286a336fc121b941"
AUTHORIZED = {"AUTHORIZED", "AUTHORIZED_SCOPED"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_checker(path: Path):
    raw = path.read_bytes()
    if sha256(raw) != FROZEN_CHECKER_SHA256:
        raise SystemExit("checker SHA-256 does not match frozen PR #25 checker")
    spec = importlib.util.spec_from_file_location("ssi_calc_v01_frozen", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_h24(root: Path) -> tuple[dict, bytes]:
    direct = root / "H24.json"
    if direct.exists():
        raw = direct.read_bytes()
    else:
        packed = (root / "H24.json.gz.b64").read_text().strip()
        raw = gzip.decompress(base64.b64decode(packed))
    if sha256(raw) != FROZEN_H24_SHA256:
        raise SystemExit("H24 SHA-256 does not match frozen PR #26 corpus")
    return json.loads(raw), raw


def score_ssi(bundle: dict, schema: dict, checker, checker_path: Path, h24_raw: bytes, schema_raw: bytes) -> dict:
    records = []
    for case in bundle["cases"]:
        cert = checker.derive(case, schema).dict()
        exp = case["expected"]
        pred_auth = cert["status"] in AUTHORIZED
        exp_auth = exp["status"] in AUTHORIZED
        checks = {
            "decision": pred_auth == exp_auth,
            "status": cert["status"] == exp["status"],
            "locus": cert["failure_locus"] == exp["failure_locus"],
            "preserved": set(cert["preserved_facts"]) == set(exp["preserved_facts"]),
            "missing": set(cert["missing_authority"]) == set(exp["missing_authority"]),
            "reopened": set(cert["reopened"]) == set(exp["reopened"]),
        }
        checks["exact"] = all(checks[k] for k in ("status", "locus", "preserved", "missing", "reopened"))
        records.append({
            "id": case["id"], "family": case["family"], "title": case["title"],
            "expected": exp, "observed": cert,
            "expected_authorize": exp_auth, "predicted_authorize": pred_auth, "checks": checks,
        })

    n = len(records)
    licensed = sum(r["expected_authorize"] for r in records)
    unlicensed = n - licensed
    tp = sum(r["expected_authorize"] and r["predicted_authorize"] for r in records)
    fp = sum((not r["expected_authorize"]) and r["predicted_authorize"] for r in records)
    fn = sum(r["expected_authorize"] and (not r["predicted_authorize"]) for r in records)
    tn = sum((not r["expected_authorize"]) and (not r["predicted_authorize"]) for r in records)
    metrics = {
        "decision_accuracy": (tp + tn) / n,
        "overreach_rate": fp / unlicensed,
        "false_refusal_rate": fn / licensed,
        "exact_status_accuracy": sum(r["checks"]["status"] for r in records) / n,
        "shallowest_locus_accuracy": sum(r["checks"]["locus"] for r in records) / n,
        "preservation_aware_refusal_accuracy": sum(r["checks"]["preserved"] for r in records) / n,
        "missing_authority_accuracy": sum(r["checks"]["missing"] for r in records) / n,
        "reopened_set_accuracy": sum(r["checks"]["reopened"] for r in records) / n,
        "exact_certificate_accuracy": sum(r["checks"]["exact"] for r in records) / n,
        "specification_atoms_consumed": "NOT_OPERATIONALIZED_IN_FROZEN_METRIC_CONTRACT",
    }
    if metrics["decision_accuracy"] >= .90 and metrics["overreach_rate"] <= .05 and metrics["false_refusal_rate"] <= .10:
        threshold = "WHITEBOX_HELDOUT_PASS"
    elif metrics["decision_accuracy"] < .75 or metrics["overreach_rate"] > .15:
        threshold = "WHITEBOX_HELDOUT_FAILED"
    else:
        threshold = "WHITEBOX_HELDOUT_PARTIAL"
    return {
        "object": "SSI_CALC_V0.1_H24_FIRST_RUN",
        "checker_sha256": sha256(checker_path.read_bytes()),
        "h24_sha256": sha256(h24_raw),
        "schema_sha256": sha256(schema_raw),
        "checker_mutated": False, "heldout_mutated": False,
        "kernel_rule_count": len(checker.RULES),
        "confusion_matrix": {"TP": tp, "FP_overreach": fp, "FN_false_refusal": fn, "TN": tn, "licensed": licensed, "unlicensed": unlicensed},
        "metrics": metrics, "threshold_status": threshold,
        "mismatch_count": sum(not r["checks"]["exact"] for r in records),
        "decision_error_count": fp + fn,
        "records": records,
    }


def declared_input_atoms(case: dict) -> int:
    return len(case.get("objects", [])) + len(case.get("facts", [])) + len(case.get("authority_edges", [])) + 1


def baseline_b0(case: dict) -> dict:
    req = case["request"]
    j = req["jurisdiction"]
    consumer = req.get("consumer")
    inspected = 1
    for edge in case["authority_edges"]:
        inspected += 1
        if edge.get("jurisdiction") == j and (consumer is None or edge.get("target") == consumer):
            return {"decision": "AUTHORIZE", "reason": "matching_authority_edge", "atoms_inspected": inspected}
    return {"decision": "NON_AUTHORIZE", "reason": "no_matching_authority_edge", "atoms_inspected": inspected}


def baseline_b1(case: dict) -> dict:
    req = case["request"]
    if req["operation"] != "compose":
        return baseline_b0(case)
    j = req["jurisdiction"]
    ids = list(map(str, req.get("args", [])))
    edges = {str(e["id"]): e for e in case["authority_edges"]}
    inspected = 1 + len(case["authority_edges"])
    if any(i not in edges for i in ids):
        return {"decision": "NON_AUTHORIZE", "reason": "missing_component_edge", "atoms_inspected": inspected}
    if any(edges[i].get("jurisdiction") != j for i in ids):
        return {"decision": "NON_AUTHORIZE", "reason": "component_jurisdiction_mismatch", "atoms_inspected": inspected}
    outs = {f["args"][0]: f["args"][1] for f in case["facts"] if f["kind"] == "output_contract"}
    ins = {f["args"][0]: f["args"][1] for f in case["facts"] if f["kind"] == "input_contract"}
    inspected += len(case["facts"])
    for a, b in zip(ids, ids[1:]):
        if a in outs and b in ins and outs[a] != ins[b]:
            return {"decision": "NON_AUTHORIZE", "reason": "type_mismatch", "atoms_inspected": inspected}
    return {"decision": "AUTHORIZE", "reason": "generic_composition_guard_pass", "atoms_inspected": inspected}


def score_baseline(name: str, fn, bundle: dict) -> dict:
    records = []
    for case in bundle["cases"]:
        observed = fn(case)
        exp_auth = case["expected"]["status"] in AUTHORIZED
        pred_auth = observed["decision"] == "AUTHORIZE"
        records.append({
            "id": case["id"], "family": case["family"],
            "expected_authorize": exp_auth, "predicted_authorize": pred_auth,
            **observed, "declared_input_atoms": declared_input_atoms(case),
        })
    n = len(records); licensed = sum(r["expected_authorize"] for r in records); unlicensed = n - licensed
    tp = sum(r["expected_authorize"] and r["predicted_authorize"] for r in records)
    fp = sum((not r["expected_authorize"]) and r["predicted_authorize"] for r in records)
    fnc = sum(r["expected_authorize"] and (not r["predicted_authorize"]) for r in records)
    tn = sum((not r["expected_authorize"]) and (not r["predicted_authorize"]) for r in records)
    return {
        "baseline": name,
        "confusion_matrix": {"TP": tp, "FP_overreach": fp, "FN_false_refusal": fnc, "TN": tn, "licensed": licensed, "unlicensed": unlicensed},
        "metrics": {
            "decision_accuracy": (tp + tn) / n,
            "overreach_rate": fp / unlicensed,
            "false_refusal_rate": fnc / licensed,
            "mean_atoms_inspected": sum(r["atoms_inspected"] for r in records) / n,
            "mean_declared_input_atoms": sum(r["declared_input_atoms"] for r in records) / n,
            "localization_metrics": "NOT_SUPPORTED_BY_FROZEN_BASELINE_CONTRACT",
        },
        "records": records,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    p.add_argument("--checker", type=Path, default=DEFAULT_CHECKER)
    p.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    p.add_argument("--out", type=Path, default=HERE / "local_h24_run")
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    bundle, h24_raw = load_h24(args.root)
    schema_raw = args.schema.read_bytes()
    schema = json.loads(schema_raw)
    checker = load_checker(args.checker)
    first = score_ssi(bundle, schema, checker, args.checker, h24_raw, schema_raw)
    baselines = {
        "object": "SSI_CALC_V0.1_H24_INTERNAL_BASELINE_RESULTS",
        "h24_sha256": sha256(h24_raw),
        "B0": score_baseline("MATCHING_EDGE_POLICY", baseline_b0, bundle),
        "B1": score_baseline("EDGE_PLUS_COMPOSITION_GUARD", baseline_b1, bundle),
    }
    (args.out / "FIRST_RUN.json").write_text(json.dumps(first, indent=2) + "\n")
    (args.out / "BASELINE_RESULTS.json").write_text(json.dumps(baselines, indent=2) + "\n")
    print(json.dumps({"ssi": first["metrics"], "status": first["threshold_status"], "B0": baselines["B0"]["metrics"], "B1": baselines["B1"]["metrics"]}, indent=2))


if __name__ == "__main__":
    main()
