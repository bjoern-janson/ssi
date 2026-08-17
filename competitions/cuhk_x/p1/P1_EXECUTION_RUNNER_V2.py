#!/usr/bin/env python3
"""CUHK-X P1 one-shot execution runner.

This runner deliberately contains no P1 support thresholds. It validates the
execution certificate and exact constituted implementation, executes the two
already-constituted Z arms once, freezes raw candidate/QA outcomes, and reports
metrics/decompositions. Scientific classification is delegated to the separate
prebound adjudicator.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np

RUN_ID = "CUHKX-P1-SHOT-1"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def canonical_json_bytes(obj) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("p1_constitution_harness_authorized", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load authorized constitution harness")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def csv_rows(z: zipfile.ZipFile, name: str):
    with z.open(name) as f:
        return list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", newline="")))


def binary_metrics(labels: list[int], preds: list[int]) -> dict:
    if len(labels) != len(preds) or not labels:
        raise RuntimeError("binary metric population invalid")
    tp = sum(y == 1 and p == 1 for y, p in zip(labels, preds))
    fn = sum(y == 1 and p == 0 for y, p in zip(labels, preds))
    tn = sum(y == 0 and p == 0 for y, p in zip(labels, preds))
    fp = sum(y == 0 and p == 1 for y, p in zip(labels, preds))
    acc = (tp + tn) / len(labels)
    tpr = tp / (tp + fn) if tp + fn else float("nan")
    tnr = tn / (tn + fp) if tn + fp else float("nan")
    bal = 0.5 * (tpr + tnr)

    def f1(pos: int) -> float:
        if pos == 1:
            a, b, c = tp, fp, fn
        else:
            a, b, c = tn, fn, fp
        den = 2 * a + b + c
        return 2 * a / den if den else 0.0

    return {
        "n": len(labels),
        "tp": tp,
        "fn": fn,
        "tn": tn,
        "fp": fp,
        "accuracy": acc,
        "balanced_accuracy": bal,
        "macro_f1": 0.5 * (f1(1) + f1(0)),
        "required_option_recall": tpr,
        "false_positive_option_rate": fp / (fp + tn) if fp + tn else float("nan"),
    }


def answer_from_option_predictions(rows: list[dict], pred_field: str) -> str:
    ordered = sorted(rows, key=lambda r: r["option"])
    return "".join(str(r["option"]) for r in ordered if int(r[pred_field]) == 1)


def aggregate_qa(candidate_rows: list[dict], truths: dict[str, str]) -> list[dict]:
    by_q: dict[str, list[dict]] = defaultdict(list)
    for r in candidate_rows:
        by_q[str(r["qa_id"])].append(r)
    out = []
    for qid in sorted(by_q):
        rs = by_q[qid]
        first = rs[0]
        truth = str(truths[qid])
        early = answer_from_option_predictions(rs, "early_prediction")
        preserved = answer_from_option_predictions(rs, "preserved_prediction")
        true_set = set(truth)
        p_set = set(preserved)
        out.append({
            "qa_id": qid,
            "path": first["path"],
            "subject": int(first["subject"]),
            "fold": int(first["fold"]),
            "truth": truth,
            "early_answer": early,
            "preserved_answer": preserved,
            "early_exact": int(early == truth),
            "preserved_exact": int(preserved == truth),
            "preserved_full_set_recovery": int(true_set.issubset(p_set)),
            "early_full_set_recovery": int(true_set.issubset(set(early))),
            "early_set_size_error": len(early) - len(truth),
            "preserved_set_size_error": len(preserved) - len(truth),
        })
    return out


def qa_summary(rows: list[dict], prefix: str) -> dict:
    n = len(rows)
    return {
        "n": n,
        "exact_set_accuracy": sum(int(r[f"{prefix}_exact"]) for r in rows) / n,
        "full_set_recovery": sum(int(r[f"{prefix}_full_set_recovery"]) for r in rows) / n,
        "mean_set_size_error": sum(int(r[f"{prefix}_set_size_error"]) for r in rows) / n,
        "set_size_error_counts": {
            str(k): sum(int(r[f"{prefix}_set_size_error"]) == k for r in rows)
            for k in sorted({int(r[f"{prefix}_set_size_error"]) for r in rows})
        },
    }


def group_summaries(candidate_rows: list[dict], qa_rows: list[dict], group: str) -> list[dict]:
    c_by = defaultdict(list)
    q_by = defaultdict(list)
    for r in candidate_rows:
        c_by[int(r[group])].append(r)
    for r in qa_rows:
        q_by[int(r[group])].append(r)
    out = []
    for g in sorted(q_by):
        c = c_by[g]
        q = q_by[g]
        y = [int(r["label"]) for r in c]
        e = [int(r["early_prediction"]) for r in c]
        p = [int(r["preserved_prediction"]) for r in c]
        em = binary_metrics(y, e)
        pm = binary_metrics(y, p)
        eq = qa_summary(q, "early")
        pq = qa_summary(q, "preserved")
        out.append({
            group: g,
            "n_qa": len(q),
            "n_candidates": len(c),
            "early_exact_set_accuracy": eq["exact_set_accuracy"],
            "preserved_exact_set_accuracy": pq["exact_set_accuracy"],
            "delta_exact_set_accuracy": pq["exact_set_accuracy"] - eq["exact_set_accuracy"],
            "early_candidate_balanced_accuracy": em["balanced_accuracy"],
            "preserved_candidate_balanced_accuracy": pm["balanced_accuracy"],
            "delta_candidate_balanced_accuracy": pm["balanced_accuracy"] - em["balanced_accuracy"],
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, required=True)
    ap.add_argument("--harness", type=Path, required=True)
    ap.add_argument("--constitution-status", type=Path, required=True)
    ap.add_argument("--s1-script", type=Path, required=True)
    ap.add_argument("--v7-results", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    cert = load_json(args.certificate)
    loaded = {
        "runner_sha256": sha256_file(Path(__file__)),
        "certificate_sha256": sha256_file(args.certificate),
        "harness_sha256": sha256_file(args.harness),
        "constitution_status_sha256": sha256_file(args.constitution_status),
        "s1_script_sha256": sha256_file(args.s1_script),
        "v7_results_sha256": sha256_file(args.v7_results),
    }

    required = {
        "runner_sha256": cert["authorized_execution"]["runner_sha256"],
        "harness_sha256": cert["authorized_object"]["harness_sha256"],
        "constitution_status_sha256": cert["authorized_object"]["constitution_status_sha256"],
        "s1_script_sha256": cert["authorized_inputs"]["s1_script_sha256"],
        "v7_results_sha256": cert["authorized_inputs"]["v7_results_sha256"],
    }
    mismatch = {k: {"loaded": loaded[k], "authorized": v} for k, v in required.items() if loaded[k] != v}
    if mismatch:
        raise RuntimeError("EXECUTION_REJECTED_IDENTITY_MISMATCH: " + json.dumps(mismatch, sort_keys=True))
    if cert["authorization_state"] != "EXECUTION_AUTHORIZED_ONE_SHOT":
        raise RuntimeError("execution certificate does not authorize one shot")
    if cert["authorized_execution"]["max_scoring_runs"] != 1:
        raise RuntimeError("certificate run-count drift")

    constitution = load_json(args.constitution_status)
    if constitution.get("final_state") != "IMPLEMENTATION_CONSTITUTED_NOT_YET_AUTHORIZED":
        raise RuntimeError("constitution state is not the authorized pre-run state")

    H = load_module(args.harness)
    identity = H.identity(args.s1_script, args.v7_results)
    shared, baseline, frozen = H.reproduce(args.v7_results)
    if baseline["candidate_stream_sha256"] != cert["authorized_baseline"]["candidate_stream_sha256"]:
        raise RuntimeError("baseline candidate stream drift at execution")
    if baseline["exact_stream_sha256"] != cert["authorized_baseline"]["exact_stream_sha256"]:
        raise RuntimeError("baseline exact stream drift at execution")
    if H.shared_hash(shared) != cert["authorized_object"]["shared_encoded_sha256"]:
        raise RuntimeError("shared encoded object drift at execution")

    z_early = H.zmake(shared, "EARLY_COMPRESSION")
    z_preserved = H.zmake(shared, "PRESERVED_EVIDENCE")
    early_pred = H.compose(*z_early).astype(int)
    preserved_pred = H.compose(*z_preserved).astype(int)
    if sha256_bytes(preserved_pred.astype(np.int8).tobytes()) != cert["authorized_object"]["preserved_prediction_digest_unscored"]:
        raise RuntimeError("preserved prediction digest differs from constituted opaque digest")

    # Truth/labels are attached only after the authorized prediction vectors exist.
    with zipfile.ZipFile(args.v7_results) as z:
        v7c = csv_rows(z, "V7_all809_candidate_predictions.csv")
        v7e = csv_rows(z, "V7_all809_exact_set_predictions.csv")
    truths = {str(r["qa_id"]): str(r["true_answer"]) for r in v7e}
    if len(v7c) != len(shared) or len(v7c) != len(early_pred):
        raise RuntimeError("candidate population alignment drift")

    candidate_rows = []
    archive_by_key = {}
    for r in v7c:
        k = (str(r["qa_id"]), str(r["option"]), str(r["action"]))
        if k in archive_by_key:
            raise RuntimeError("duplicate candidate key in archive")
        archive_by_key[k] = r
    if len(archive_by_key) != len(shared):
        raise RuntimeError("candidate key cardinality drift")
    for i, s in enumerate(shared):
        k = (s.q, s.opt, s.act)
        r = archive_by_key.get(k)
        if r is None:
            raise RuntimeError("candidate key alignment drift")
        candidate_rows.append({
            "qa_id": s.q,
            "path": s.path,
            "subject": int(s.subj),
            "fold": int(s.fold),
            "option": s.opt,
            "action": s.act,
            "label": int(r["label"]),
            "early_prediction": int(early_pred[i]),
            "preserved_prediction": int(preserved_pred[i]),
        })

    qa_rows = aggregate_qa(candidate_rows, truths)
    y = [int(r["label"]) for r in candidate_rows]
    ep = [int(r["early_prediction"]) for r in candidate_rows]
    pp = [int(r["preserved_prediction"]) for r in candidate_rows]
    early_candidate = binary_metrics(y, ep)
    preserved_candidate = binary_metrics(y, pp)
    early_qa = qa_summary(qa_rows, "early")
    preserved_qa = qa_summary(qa_rows, "preserved")

    metrics = {
        "run_id": RUN_ID,
        "scope": "HAU/multi",
        "loaded_identity": loaded,
        "input_identity": identity,
        "baseline_reproduction": baseline,
        "early": {"candidate": early_candidate, "qa": early_qa},
        "preserved": {"candidate": preserved_candidate, "qa": preserved_qa},
        "deltas": {
            "candidate_accuracy": preserved_candidate["accuracy"] - early_candidate["accuracy"],
            "candidate_balanced_accuracy": preserved_candidate["balanced_accuracy"] - early_candidate["balanced_accuracy"],
            "candidate_macro_f1": preserved_candidate["macro_f1"] - early_candidate["macro_f1"],
            "required_option_recall": preserved_candidate["required_option_recall"] - early_candidate["required_option_recall"],
            "false_positive_option_rate": preserved_candidate["false_positive_option_rate"] - early_candidate["false_positive_option_rate"],
            "full_set_recovery": preserved_qa["full_set_recovery"] - early_qa["full_set_recovery"],
            "exact_set_accuracy": preserved_qa["exact_set_accuracy"] - early_qa["exact_set_accuracy"],
            "mean_set_size_error": preserved_qa["mean_set_size_error"] - early_qa["mean_set_size_error"],
        },
        "folds": group_summaries(candidate_rows, qa_rows, "fold"),
        "subjects": group_summaries(candidate_rows, qa_rows, "subject"),
        "secondary_branch_constitution": {
            "HAU_sequence": False,
            "HAU_combination": False,
            "HAU_emotion": False,
        },
        "transfer_comparator": {
            "nested_inner_subject_oof_available": False,
            "reason": "authorized retained artifacts contain outer OOF evidence only; frozen P1-C requires nested inner subject-fold OOF on each outer-training population",
        },
        "scientific_adjudication_performed": False,
    }

    raw = {
        "run_id": RUN_ID,
        "authorization_certificate_sha256": loaded["certificate_sha256"],
        "candidate_rows": candidate_rows,
        "qa_rows": qa_rows,
    }
    raw_bytes = canonical_json_bytes(raw)
    metrics["raw_result_sha256"] = sha256_bytes(raw_bytes)
    metrics_bytes = canonical_json_bytes(metrics)

    (args.out / "P1_SHOT1_RAW_RESULT.json").write_bytes(raw_bytes)
    (args.out / "P1_SHOT1_METRICS.json").write_bytes(metrics_bytes)
    record = {
        "run_id": RUN_ID,
        "state": "SHOT_EXECUTED_RESULT_FROZEN_PENDING_ADJUDICATION",
        "raw_result_sha256": sha256_bytes(raw_bytes),
        "metrics_sha256": sha256_bytes(metrics_bytes),
        "preserved_prediction_digest": sha256_bytes(preserved_pred.astype(np.int8).tobytes()),
        "scientific_adjudication_performed": False,
    }
    (args.out / "P1_SHOT1_EXECUTION_RECORD.json").write_bytes(canonical_json_bytes(record))
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
