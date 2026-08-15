#!/usr/bin/env python3
"""Mechanical precheck for frozen CUHK-X AIM5.

This script does not fit AIM5 meta-models and does not adjudicate AIM5.
It verifies the frozen inputs, outer/inner subject isolation, the meta-feature
contract, exact S1/V7/V7F OOF candidate-sign reproduction, and the exact S1
multi answer-set decision operator before AIM5 execution is authorized.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

EXPECTED_AIM4_SHA256 = "ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5"
EXPECTED_AIM5_SHA256 = "620e35da4256e3368359e202729e45489b916687ef890e3f9d887e91f11a0605"
EXPECTED_FOLDS = set(range(5))
EXPECTED_HAU = 809
EXPECTED_PAIRS = 3236
EXPECTED_ACTIONS = 40
OPTIONS = tuple("ABCD")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def exact_s1_answer_independent(g: pd.DataFrame) -> str:
    rows = [(float(r.margin), str(r.option)) for r in g.itertuples(index=False)]
    chosen = [option for margin, option in rows if margin >= 0.0]
    if not chosen:
        chosen = [max(rows)[1]]
    return "".join(sorted(chosen))


def audit_fold_partition(q: pd.DataFrame) -> list[dict]:
    if len(q) != EXPECTED_HAU or q.qa_id.nunique() != EXPECTED_HAU:
        raise RuntimeError(f"HAU multi population drift: {len(q)}/{q.qa_id.nunique()}")
    folds = set(q.fold.astype(int).unique().tolist())
    if folds != EXPECTED_FOLDS:
        raise RuntimeError(f"fold set drift: {sorted(folds)}")

    subj_fold_counts = q.groupby("subject")["fold"].nunique()
    bad = subj_fold_counts[subj_fold_counts != 1]
    if len(bad):
        raise RuntimeError(f"subject appears in multiple folds: {bad.to_dict()}")

    rows = []
    all_subjects = set(q.subject.astype(int).unique().tolist())
    for outer in range(5):
        outer_subjects = set(q.loc[q.fold == outer, "subject"].astype(int))
        train_subjects = set(q.loc[q.fold != outer, "subject"].astype(int))
        if outer_subjects & train_subjects:
            raise RuntimeError(f"outer subject leakage at fold {outer}")
        if outer_subjects | train_subjects != all_subjects:
            raise RuntimeError(f"outer subject partition incomplete at fold {outer}")
        rows.append({
            "outer_fold": outer,
            "outer_subjects": sorted(outer_subjects),
            "training_subjects": sorted(train_subjects),
            "outer_n": int((q.fold == outer).sum()),
            "train_n": int((q.fold != outer).sum()),
        })
    return rows


def audit_build_inner_meta_control_flow(aim5, q: pd.DataFrame) -> list[dict]:
    """Exercise AIM5's actual build_inner_meta fold selection with a recorder.

    The recorder replaces score_population only for this structural audit. It
    records the train/score folds and returns a shape-compatible dummy table so
    build_inner_meta itself executes its population checks.
    """
    original = aim5.score_population
    audit_rows = []

    try:
        for outer in range(5):
            calls = []

            def recorder(
                s1, aim4, q_train, q_score, v7_map, v7f_map, common,
                frozen_key=None, require_frozen_sign_reproduction=False,
            ):
                train_folds = set(q_train.fold.astype(int).unique().tolist())
                score_folds = set(q_score.fold.astype(int).unique().tolist())
                train_subjects = set(q_train.subject.astype(int).unique().tolist())
                score_subjects = set(q_score.subject.astype(int).unique().tolist())
                calls.append({
                    "train_folds": sorted(train_folds),
                    "score_folds": sorted(score_folds),
                    "train_subjects": sorted(train_subjects),
                    "score_subjects": sorted(score_subjects),
                })
                dummy = []
                for r in q_score.itertuples(index=False):
                    truth = set(str(r.answer))
                    for option in OPTIONS:
                        dummy.append({
                            "qa_id": str(r.qa_id),
                            "path": str(r.path),
                            "subject": int(r.subject),
                            "fold": int(r.fold),
                            "option": option,
                            "action": str(getattr(r, option)),
                            "label": int(option in truth),
                            "margin": 0.0,
                            "sign_prediction": 1,
                            "route": "AUDIT_ONLY",
                        })
                return pd.DataFrame(dummy)

            aim5.score_population = recorder
            meta = aim5.build_inner_meta(
                None, None, q, outer, {}, {}, set()
            )
            expected_inner = [f for f in range(5) if f != outer]
            if len(calls) != 4:
                raise RuntimeError(f"outer {outer}: expected 4 inner calls, got {len(calls)}")

            outer_subjects = set(q.loc[q.fold == outer, "subject"].astype(int))
            seen_inner = []
            for call in calls:
                if len(call["score_folds"]) != 1:
                    raise RuntimeError(f"outer {outer}: inner score is not one fold: {call}")
                inner = int(call["score_folds"][0])
                seen_inner.append(inner)
                if inner == outer:
                    raise RuntimeError(f"outer {outer}: outer fold used as inner score fold")
                expected_train = EXPECTED_FOLDS - {outer, inner}
                if set(call["train_folds"]) != expected_train:
                    raise RuntimeError(
                        f"outer {outer}, inner {inner}: train folds {call['train_folds']} != {sorted(expected_train)}"
                    )
                train_subjects = set(call["train_subjects"])
                score_subjects = set(call["score_subjects"])
                if train_subjects & outer_subjects:
                    raise RuntimeError(f"outer {outer}, inner {inner}: outer subjects leak into base training")
                if score_subjects & outer_subjects:
                    raise RuntimeError(f"outer {outer}, inner {inner}: outer subjects leak into meta scoring")
                if train_subjects & score_subjects:
                    raise RuntimeError(f"outer {outer}, inner {inner}: inner subjects leak into base training")

            if sorted(seen_inner) != expected_inner:
                raise RuntimeError(
                    f"outer {outer}: inner folds {sorted(seen_inner)} != {expected_inner}"
                )
            expected_ep = int((q.fold != outer).sum())
            if meta.qa_id.nunique() != expected_ep or len(meta) != expected_ep * 4:
                raise RuntimeError(f"outer {outer}: inner meta population check failed")
            audit_rows.append({
                "outer_fold": outer,
                "inner_folds": expected_inner,
                "meta_episodes": int(meta.qa_id.nunique()),
                "meta_pairs": int(len(meta)),
                "status": "PASS",
            })
    finally:
        aim5.score_population = original

    return audit_rows


def audit_meta_feature_contract(aim5, q: pd.DataFrame) -> dict:
    """Verify the frozen meta-model input dimensions from executable behavior."""
    actions = sorted(set(q[["A", "B", "C", "D"]].stack().astype(str)))
    if len(actions) != EXPECTED_ACTIONS:
        raise RuntimeError(f"semantic action vocabulary drift: {len(actions)}")

    # Candidate utility: exactly one margin column plus one-hot semantic action.
    rows = []
    for j, action in enumerate(actions):
        rows.append({"action": action, "margin": -0.75 + 0.01 * j, "label": 0})
        rows.append({"action": action, "margin": +0.75 + 0.01 * j, "label": 1})
    util_df = pd.DataFrame(rows)
    util_model, got_actions, _, _, _ = aim5.fit_candidate_utility(util_df)
    if got_actions != actions:
        raise RuntimeError("candidate utility action ordering drift")
    if int(util_model.n_features_in_) != 1 + EXPECTED_ACTIONS:
        raise RuntimeError(
            f"candidate utility feature dimension drift: {util_model.n_features_in_}"
        )

    # Cardinality model: exactly (s1,s2,s3,s4,n_pos), no action/query identity.
    cand_rows = []
    qid = 0
    for k in (1, 2, 3, 4):
        for rep in range(3):
            qid += 1
            for oi, option in enumerate(OPTIONS):
                cand_rows.append({
                    "qa_id": str(qid),
                    "subject": rep + 1,
                    "fold": rep % 3,
                    "option": option,
                    "action": actions[(qid + oi) % len(actions)],
                    "label": int(oi < k),
                    "margin": float(2.0 - oi + 0.1 * rep),
                    "query_text": f"POISON_{qid}",
                })
    card_model = aim5.fit_cardinality_model(pd.DataFrame(cand_rows))
    scaler = card_model.named_steps["scale"]
    if int(scaler.n_features_in_) != 5:
        raise RuntimeError(f"cardinality feature dimension drift: {scaler.n_features_in_}")

    return {
        "candidate_utility_features": 1 + EXPECTED_ACTIONS,
        "candidate_utility_contract": "standardized normalized margin + semantic-action one-hot only",
        "cardinality_features": 5,
        "cardinality_contract": "(s1,s2,s3,s4,n_nonnegative) only",
        "query_text_used": False,
        "option_identity_used_by_meta_models": False,
        "status": "PASS",
    }


def audit_s1_reproduction(aim5, aim4, s1, q, v7_map, v7f_map, common, frozen_key):
    """Reproduce frozen outer candidate signs and independently verify S1 set rule."""
    all_cand = []
    fold_rows = []
    for outer in range(5):
        q_train = q[q.fold != outer].copy()
        q_test = q[q.fold == outer].copy()
        cand = aim5.score_population(
            s1, aim4, q_train, q_test, v7_map, v7f_map, common,
            frozen_key=frozen_key,
            require_frozen_sign_reproduction=True,
        )
        if set(cand.fold.astype(int).unique().tolist()) != {outer}:
            raise RuntimeError(f"outer {outer}: scored rows contain wrong fold")
        train_subjects = set(q_train.subject.astype(int))
        test_subjects = set(q_test.subject.astype(int))
        if train_subjects & test_subjects:
            raise RuntimeError(f"outer {outer}: subject leakage in exact S1 replay")

        decision_mismatch = 0
        exact_correct = 0
        for _, g in cand.groupby("qa_id", sort=False):
            independent = exact_s1_answer_independent(g)
            helper = aim4.chosen_from_margins(g[["option", "margin"]].copy(), None)
            if independent != helper:
                decision_mismatch += 1
            truth = "".join(sorted(g.loc[g.label == 1, "option"].astype(str).tolist()))
            exact_correct += int(helper == truth)
        if decision_mismatch:
            raise RuntimeError(
                f"outer {outer}: S1 decision-operator mismatch on {decision_mismatch} rows"
            )
        fold_rows.append({
            "outer_fold": outer,
            "episodes": int(cand.qa_id.nunique()),
            "candidate_pairs": int(len(cand)),
            "candidate_sign_reproduction": "PASS",
            "decision_operator_reproduction": "PASS",
            "s1_exact_replay": float(exact_correct / cand.qa_id.nunique()),
        })
        all_cand.append(cand)

    cand_all = pd.concat(all_cand, ignore_index=True)
    if len(cand_all) != EXPECTED_PAIRS or cand_all.qa_id.nunique() != EXPECTED_HAU:
        raise RuntimeError(
            f"full S1 replay population drift: {len(cand_all)}/{cand_all.qa_id.nunique()}"
        )
    exacts = []
    for _, g in cand_all.groupby("qa_id", sort=False):
        pred = exact_s1_answer_independent(g)
        truth = "".join(sorted(g.loc[g.label == 1, "option"].astype(str).tolist()))
        exacts.append(int(pred == truth))
    return fold_rows, float(np.mean(exacts))


def run_precheck(workdir: Path, report_path: Path) -> int:
    aim4_path = workdir / "cuhkx_aim4_structured_set.py"
    aim5_path = workdir / "cuhkx_aim5_conditional_setmap.py"
    if not aim4_path.exists():
        raise FileNotFoundError(aim4_path)
    if not aim5_path.exists():
        raise FileNotFoundError(aim5_path)

    got4 = sha256_file(aim4_path)
    got5 = sha256_file(aim5_path)
    if got4 != EXPECTED_AIM4_SHA256:
        raise RuntimeError(f"AIM4 helper SHA mismatch: {got4}")
    if got5 != EXPECTED_AIM5_SHA256:
        raise RuntimeError(f"AIM5 executable SHA mismatch: {got5}")

    aim4 = load_module("aim5_precheck_aim4", aim4_path)
    aim5 = load_module("aim5_precheck_target", aim5_path)
    paths, input_hashes, s1, q, v7_map, v7f_map, common, frozen_key = aim4.load_inputs(workdir)

    fold_partition = audit_fold_partition(q)
    nested_control_flow = audit_build_inner_meta_control_flow(aim5, q)
    feature_contract = audit_meta_feature_contract(aim5, q)
    s1_folds, s1_exact = audit_s1_reproduction(
        aim5, aim4, s1, q, v7_map, v7f_map, common, frozen_key
    )

    report = {
        "STOP": "AIM5_MECHANICAL_PRECHECK_COMPLETE",
        "PRECHECK": "PASS",
        "RUN_AUTHORIZATION": "BYTE_FREEZE_PENDING",
        "hashes": {
            "aim4_helper_sha256": got4,
            "aim5_executable_sha256": got5,
            **input_hashes,
        },
        "invariants": {
            "outer_subject_isolation": "PASS",
            "inner_base_model_isolation": "PASS",
            "training_only_margin_normalization": (
                "PASS_BY_COMPOSITION: frozen S1 train_per_action_candidate_models derives scale "
                "only from q_train; audited outer/inner q_train excludes sealed subjects"
            ),
            "training_only_meta_fitting": "PASS",
            "no_query_leakage": "PASS",
            "aim4_comparator_frozen": "PASS",
            "s1_candidate_sign_reproduction": "PASS",
            "s1_decision_operator_reproduction": "PASS",
        },
        "fold_partition": fold_partition,
        "nested_control_flow": nested_control_flow,
        "meta_feature_contract": feature_contract,
        "s1_reproduction_folds": s1_folds,
        "s1_exact_replay": s1_exact,
        "next_state": (
            "Freeze the verified AIM5 executable/precheck/input hashes in the post-precheck "
            "authorization record before running AIM5. Do not modify architecture or gates."
        ),
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("PRECHECK = PASS")
    print(f"S1_EXACT_REPLAY = {s1_exact:.9f}")
    print("RUN_AUTHORIZATION = BYTE_FREEZE_PENDING")
    print(f"REPORT = {report_path}")
    print("STOP = AIM5_MECHANICAL_PRECHECK_COMPLETE")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", type=Path, default=Path.cwd())
    ap.add_argument("--report", type=Path, default=None)
    args = ap.parse_args()
    workdir = args.workdir.resolve()
    report = (args.report or (workdir / "cuhkx_aim5_precheck_report.json")).resolve()
    try:
        return run_precheck(workdir, report)
    except Exception as exc:
        print("PRECHECK = FAIL")
        print("RUN_AUTHORIZATION = NOT_AUTHORIZED")
        print(f"REASON = {type(exc).__name__}")
        print(str(exc))
        print("STOP = AIM5_PRECHECK_NOT_IDENTIFIED")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
