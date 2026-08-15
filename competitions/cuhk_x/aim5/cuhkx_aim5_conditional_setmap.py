#!/usr/bin/env python3
"""CUHK-X AIM5 — nested action-aware conditional SET-MAP for HAU multi."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import platform
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

AIM_ID = "CUHKX_AIM5_NESTED_ACTION_AWARE_CONDITIONAL_SETMAP_V1"
HELPER_SHA256 = "ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5"
BOOT_SEED = 260817
N_BOOT = 20000
MATERIAL_DELTA_EXACT = 0.05
MIN_NONNEG_FOLDS = 4
EXPECTED_HAU = 809
EXPECTED_PAIRS = 3236
EXPECTED_ACTIONS = 40
OPTIONS = tuple("ABCD")
SUBSETS = [
    tuple(i for i in range(4) if mask & (1 << i))
    for mask in range(1, 16)
]


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


def fit_candidate_utility(meta_cand: pd.DataFrame):
    actions = sorted(meta_cand.action.astype(str).unique().tolist())
    if len(actions) != EXPECTED_ACTIONS:
        raise RuntimeError(f"action vocabulary drift: {len(actions)}")
    action_to_col = {a: j + 1 for j, a in enumerate(actions)}
    mu = float(meta_cand.margin.mean())
    sd = float(meta_cand.margin.std(ddof=0))
    if not np.isfinite(sd) or sd <= 1e-12:
        raise RuntimeError(f"degenerate meta margin scale: {sd}")
    X = np.zeros((len(meta_cand), 1 + len(actions)), dtype=float)
    X[:, 0] = (meta_cand.margin.to_numpy(float) - mu) / sd
    for rix, action in enumerate(meta_cand.action.astype(str)):
        X[rix, action_to_col[action]] = 1.0
    y = meta_cand.label.to_numpy(int)
    if set(np.unique(y).tolist()) != {0, 1}:
        raise RuntimeError("candidate utility meta labels lack both classes")
    model = LogisticRegression(
        C=1.0,
        solver="lbfgs",
        max_iter=1000,
        class_weight=None,
        fit_intercept=False,
    )
    model.fit(X, y)
    return model, actions, action_to_col, mu, sd


def candidate_utilities(
    model: LogisticRegression,
    action_to_col: dict[str, int],
    mu: float,
    sd: float,
    margins: list[float],
    actions: list[str],
) -> np.ndarray:
    X = np.zeros((4, 1 + len(action_to_col)), dtype=float)
    X[:, 0] = (np.asarray(margins, dtype=float) - mu) / sd
    for i, action in enumerate(actions):
        if action not in action_to_col:
            raise RuntimeError(f"unseen semantic action at meta test: {action!r}")
        X[i, action_to_col[action]] = 1.0
    return np.asarray(model.decision_function(X), dtype=float)


def card_features(g: pd.DataFrame) -> np.ndarray:
    m = np.asarray(sorted(g.margin.astype(float).tolist(), reverse=True), dtype=float)
    if m.shape != (4,):
        raise RuntimeError(f"expected four margins, got {m.shape}")
    return np.asarray([m[0], m[1], m[2], m[3], float(np.sum(m >= 0.0))], dtype=float)


def episode_meta_table(cand: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for qid, g in cand.groupby("qa_id", sort=False):
        g = g.sort_values("option")
        x = card_features(g)
        truth = "".join(sorted(g.loc[g.label == 1, "option"].astype(str).tolist()))
        rows.append({
            "qa_id": str(qid),
            "subject": int(g.subject.iloc[0]),
            "fold": int(g.fold.iloc[0]),
            "true_k": len(truth),
            "s1": x[0], "s2": x[1], "s3": x[2], "s4": x[3], "n_pos": x[4],
        })
    return pd.DataFrame(rows)


def fit_cardinality_model(meta_cand: pd.DataFrame):
    ep = episode_meta_table(meta_cand)
    feats = ["s1", "s2", "s3", "s4", "n_pos"]
    classes = set(ep.true_k.astype(int).unique().tolist())
    if classes != {1, 2, 3, 4}:
        raise RuntimeError(f"cardinality class support drift: {sorted(classes)}")
    model = Pipeline([
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(
            C=1.0,
            solver="lbfgs",
            max_iter=1000,
            class_weight=None,
        )),
    ])
    model.fit(ep[feats].to_numpy(float), ep.true_k.to_numpy(int))
    return model


def logsumexp(vals: list[float]) -> float:
    a = np.asarray(vals, dtype=float)
    m = float(np.max(a))
    return m + math.log(float(np.exp(a - m).sum()))


def conditional_setmap(q_probs: dict[int, float], utilities: np.ndarray) -> str:
    log_scores = {}
    for k in range(1, 5):
        sets_k = [S for S in SUBSETS if len(S) == k]
        within = [float(sum(utilities[i] for i in S)) for S in sets_k]
        logz = logsumexp(within)
        qk = float(q_probs[k])
        if not (qk > 0.0 and np.isfinite(qk)):
            raise RuntimeError(f"invalid q_k for k={k}: {qk}")
        for S, u in zip(sets_k, within):
            log_scores[S] = math.log(qk) + u - logz
    best = max(log_scores.items(), key=lambda kv: (kv[1], tuple(OPTIONS[i] for i in kv[0])))[0]
    return "".join(sorted(OPTIONS[i] for i in best))


def score_population(
    s1,
    aim4,
    q_train: pd.DataFrame,
    q_score: pd.DataFrame,
    v7_map: dict[str, np.ndarray],
    v7f_map: dict[str, np.ndarray],
    common: set[str],
    frozen_key=None,
    require_frozen_sign_reproduction: bool = False,
) -> pd.DataFrame:
    ir_models = s1.train_per_action_candidate_models(v7_map, q_train, aim4.ModelFactory)
    q_train_f = q_train[q_train.path.astype(str).isin(common)].copy()
    v7f_models = s1.train_per_action_candidate_models(v7f_map, q_train_f, aim4.ModelFactory)

    rows = []
    mismatches = []
    for r in q_score.itertuples(index=False):
        qid = str(r.qa_id)
        unit = str(r.path)
        if unit in common:
            models, x, route = v7f_models, v7f_map[unit], "V7F"
        else:
            models, x, route = ir_models, v7_map[unit], "V7_IR_FALLBACK"
        _, margin_by_action = s1.score_action_models(models, x)
        truth = set(str(r.answer))
        for option in OPTIONS:
            action = str(getattr(r, option))
            margin = float(margin_by_action[action])
            sign = int(margin >= 0.0)
            if require_frozen_sign_reproduction:
                key = (qid, option)
                if frozen_key is None or key not in frozen_key.index:
                    raise RuntimeError(f"missing frozen candidate key {key}")
                old = int(frozen_key.loc[key].prediction)
                if sign != old:
                    mismatches.append((qid, option, sign, old, int(r.fold), route))
            rows.append({
                "qa_id": qid,
                "path": unit,
                "subject": int(r.subject),
                "fold": int(r.fold),
                "option": option,
                "action": action,
                "label": int(option in truth),
                "margin": margin,
                "sign_prediction": sign,
                "route": route,
            })
    out = pd.DataFrame(rows)
    if require_frozen_sign_reproduction and mismatches:
        raise RuntimeError(
            f"BASE_SIGN_REPRODUCTION_FAILURE n={len(mismatches)} sample={mismatches[:10]}"
        )
    return out


def build_inner_meta(
    s1, aim4, q, outer_fold, v7_map, v7f_map, common
) -> pd.DataFrame:
    parts = []
    inner_folds = [f for f in range(5) if f != outer_fold]
    for inner_fold in inner_folds:
        train_mask = (~q.fold.isin([outer_fold, inner_fold]))
        q_train = q[train_mask].copy()
        q_score = q[q.fold == inner_fold].copy()
        part = score_population(
            s1, aim4, q_train, q_score, v7_map, v7f_map, common,
            require_frozen_sign_reproduction=False,
        )
        parts.append(part)
    meta = pd.concat(parts, ignore_index=True)
    expected_ep = int((q.fold != outer_fold).sum())
    if meta.qa_id.nunique() != expected_ep or len(meta) != expected_ep * 4:
        raise RuntimeError(
            f"inner meta population drift outer={outer_fold}: "
            f"{meta.qa_id.nunique()}/{len(meta)} expected {expected_ep}/{expected_ep*4}"
        )
    return meta


def baseline_answer(aim4, g: pd.DataFrame) -> str:
    return aim4.chosen_from_margins(g[["option", "margin"]].copy(), None)


def hard_cardinality_answer(aim4, g: pd.DataFrame, k: int) -> str:
    return aim4.chosen_from_margins(g[["option", "margin"]].copy(), int(k))


def outer_predictions(
    aim4,
    outer_cand: pd.DataFrame,
    util_model,
    action_to_col,
    mu,
    sd,
    card_model,
) -> pd.DataFrame:
    rows = []
    card_classes = [int(x) for x in card_model.named_steps["clf"].classes_]
    if set(card_classes) != {1, 2, 3, 4}:
        raise RuntimeError(f"cardinality model classes drift: {card_classes}")

    for qid, g in outer_cand.groupby("qa_id", sort=False):
        g = g.sort_values("option")
        truth = "".join(sorted(g.loc[g.label == 1, "option"].astype(str).tolist()))
        b0 = baseline_answer(aim4, g)
        z = card_features(g)
        qv = card_model.predict_proba(z.reshape(1, -1))[0]
        q_probs = {k: float(qv[card_classes.index(k)]) for k in range(1, 5)}
        khat = max(q_probs.items(), key=lambda kv: (kv[1], -kv[0]))[0]
        khard = hard_cardinality_answer(aim4, g, khat)

        margins = [float(g.loc[g.option == o, "margin"].iloc[0]) for o in OPTIONS]
        actions = [str(g.loc[g.option == o, "action"].iloc[0]) for o in OPTIONS]
        util = candidate_utilities(
            util_model, action_to_col, mu, sd, margins, actions
        )
        setmap = conditional_setmap(q_probs, util)

        raw_order = tuple(
            x[1] for x in sorted(zip(margins, OPTIONS), reverse=True)
        )
        util_order = tuple(
            x[1] for x in sorted(zip(util.tolist(), OPTIONS), reverse=True)
        )
        entropy = -sum(p * math.log(max(p, 1e-300)) for p in q_probs.values())

        rows.append({
            "qa_id": str(qid),
            "path": str(g.path.iloc[0]),
            "subject": int(g.subject.iloc[0]),
            "fold": int(g.fold.iloc[0]),
            "route": str(g.route.iloc[0]),
            "truth": truth,
            "true_k": len(truth),
            "s1_answer": b0,
            "s1_exact": int(b0 == truth),
            "khard_k": int(khat),
            "khard_answer": khard,
            "khard_exact": int(khard == truth),
            "aim5_answer": setmap,
            "aim5_exact": int(setmap == truth),
            "paired_delta": int(setmap == truth) - int(b0 == truth),
            "q1": q_probs[1], "q2": q_probs[2], "q3": q_probs[3], "q4": q_probs[4],
            "q_entropy": entropy,
            "raw_order": "".join(raw_order),
            "utility_order": "".join(util_order),
            "utility_reordered": int(raw_order != util_order),
            "mA": margins[0], "mB": margins[1], "mC": margins[2], "mD": margins[3],
            "uA": float(util[0]), "uB": float(util[1]),
            "uC": float(util[2]), "uD": float(util[3]),
        })
    return pd.DataFrame(rows)


def candidate_metrics(ep: pd.DataFrame, answer_col: str) -> dict:
    y, p = [], []
    for r in ep.itertuples(index=False):
        truth = set(str(r.truth))
        pred = set(str(getattr(r, answer_col)))
        for option in OPTIONS:
            y.append(int(option in truth))
            p.append(int(option in pred))
    return {
        "accuracy": float(accuracy_score(y, p)),
        "balanced_accuracy": float(balanced_accuracy_score(y, p)),
    }


def subject_bootstrap(ep: pd.DataFrame) -> tuple[float, float]:
    subjects = np.asarray(sorted(ep.subject.unique()), dtype=int)
    by_subject = {
        int(s): ep[ep.subject == s].paired_delta.to_numpy(float)
        for s in subjects
    }
    rng = np.random.default_rng(BOOT_SEED)
    vals = np.empty(N_BOOT, dtype=float)
    for b in range(N_BOOT):
        draw = rng.choice(subjects, size=len(subjects), replace=True)
        arr = np.concatenate([by_subject[int(s)] for s in draw])
        vals[b] = float(arr.mean())
    return float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))


def run(workdir: Path, outdir: Path) -> int:
    helper = workdir / "cuhkx_aim4_structured_set.py"
    if not helper.exists():
        raise FileNotFoundError(helper)
    got_helper_sha = sha256_file(helper)
    if got_helper_sha != HELPER_SHA256:
        raise RuntimeError(
            f"AIM4 helper SHA mismatch: {got_helper_sha} != {HELPER_SHA256}"
        )
    aim4 = load_module("aim5_frozen_aim4_helper", helper)
    paths, hashes, s1, q, v7_map, v7f_map, common, frozen_key = aim4.load_inputs(workdir)

    all_outer = []
    fold_rows = []
    print("PRECHECK = PASS")
    for outer_fold in range(5):
        print(f"[outer {outer_fold}] nested meta margins...", flush=True)
        meta_cand = build_inner_meta(
            s1, aim4, q, outer_fold, v7_map, v7f_map, common
        )
        util_model, actions, action_to_col, mu, sd = fit_candidate_utility(meta_cand)
        card_model = fit_cardinality_model(meta_cand)

        print(f"[outer {outer_fold}] exact S1 outer evidence + sign reproduction...", flush=True)
        q_train = q[q.fold != outer_fold].copy()
        q_test = q[q.fold == outer_fold].copy()
        outer_cand = score_population(
            s1, aim4, q_train, q_test, v7_map, v7f_map, common,
            frozen_key=frozen_key,
            require_frozen_sign_reproduction=True,
        )
        pred = outer_predictions(
            aim4, outer_cand, util_model, action_to_col, mu, sd, card_model
        )
        all_outer.append(pred)
        b0 = float(pred.s1_exact.mean())
        kh = float(pred.khard_exact.mean())
        a5 = float(pred.aim5_exact.mean())
        fold_rows.append({
            "fold": outer_fold,
            "n": len(pred),
            "s1_exact": b0,
            "khard_exact": kh,
            "aim5_exact": a5,
            "delta_aim5_minus_s1": a5 - b0,
            "delta_khard_minus_s1": kh - b0,
            "utility_reorder_rate": float(pred.utility_reordered.mean()),
            "mean_q_entropy": float(pred.q_entropy.mean()),
        })

    ep = pd.concat(all_outer, ignore_index=True)
    if len(ep) != EXPECTED_HAU or ep.qa_id.nunique() != EXPECTED_HAU:
        raise RuntimeError(f"outer prediction population drift: {len(ep)}/{ep.qa_id.nunique()}")

    s1_exact = float(ep.s1_exact.mean())
    kh_exact = float(ep.khard_exact.mean())
    aim5_exact = float(ep.aim5_exact.mean())
    delta = aim5_exact - s1_exact
    ci_lo, ci_hi = subject_bootstrap(ep)
    nonneg = int(sum(r["delta_aim5_minus_s1"] >= 0.0 for r in fold_rows))
    support = bool(
        delta >= MATERIAL_DELTA_EXACT
        and nonneg >= MIN_NONNEG_FOLDS
        and ci_lo > 0.0
    )
    status = (
        "SUPPORTED_CONDITIONAL_SETMAP_IN_FROZEN_MULTI_SCOPE"
        if support else "NOT_SUPPORTED_CONDITIONAL_SETMAP"
    )
    s2 = "PACKAGING_CANDIDATE_AUTHORIZED" if support else "NOT_AUTHORIZED_BY_AIM5"

    outdir.mkdir(parents=True, exist_ok=True)
    ep.to_csv(outdir / "aim5_outer_predictions.csv", index=False)
    pd.DataFrame(fold_rows).to_csv(outdir / "aim5_fold_metrics.csv", index=False)

    summary = {
        "STOP": "AIM5_EXECUTION_COMPLETE",
        "AIM5": status,
        "S2": s2,
        "primary": {
            "s1_exact": s1_exact,
            "aim5_exact": aim5_exact,
            "delta_exact": delta,
            "subject_bootstrap_ci95": [ci_lo, ci_hi],
            "folds_nonnegative": nonneg,
        },
        "secondary": {
            "nested_hard_cardinality_exact": kh_exact,
            "delta_khard_minus_s1": kh_exact - s1_exact,
            "utility_reorder_rate": float(ep.utility_reordered.mean()),
            "mean_q_entropy": float(ep.q_entropy.mean()),
            "s1_candidate_metrics": candidate_metrics(ep, "s1_answer"),
            "khard_candidate_metrics": candidate_metrics(ep, "khard_answer"),
            "aim5_candidate_metrics": candidate_metrics(ep, "aim5_answer"),
            "true_cardinality_counts": {
                str(k): int(v) for k, v in ep.true_k.value_counts().sort_index().items()
            },
            "khard_cardinality_counts": {
                str(k): int(v) for k, v in ep.khard_k.value_counts().sort_index().items()
            },
        },
        "gates": {
            "minimum_delta_exact": MATERIAL_DELTA_EXACT,
            "minimum_nonnegative_folds": MIN_NONNEG_FOLDS,
            "bootstrap_resamples": N_BOOT,
            "bootstrap_seed": BOOT_SEED,
            "require_ci95_lower_gt_zero": True,
        },
        "nested_firewall": {
            "outer_folds": 5,
            "inner_meta_rule": "for outer f and inner g, base train excludes both f and g; score g",
            "outer_test_rule": "base train excludes outer f; score f; exact frozen sign reproduction required",
        },
        "hashes": {
            **hashes,
            "aim4_helper_sha256": got_helper_sha,
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "sklearn": sklearn.__version__,
        },
        "authority_ceiling": (
            "Internal nested subject-held-out evidence for the single frozen "
            "NESTED_ACTION_AWARE_CONDITIONAL_SETMAP_V1 HAU-multi decision operator only."
        ),
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    result_zip = outdir.parent / "cuhkx_aim5_conditional_setmap_results.zip"
    if result_zip.exists():
        result_zip.unlink()
    with zipfile.ZipFile(
        result_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as z:
        for p in sorted(outdir.iterdir()):
            if p.is_file():
                z.write(p, arcname=p.name)
        z.write(Path(__file__).resolve(), arcname=Path(__file__).name)
        z.write(helper, arcname=helper.name)

    print("[COMPLETE]")
    print(f"S1_exact = {s1_exact:.9f}")
    print(f"KHARD_exact = {kh_exact:.9f}")
    print(f"AIM5_exact = {aim5_exact:.9f}")
    print(f"delta_exact = {delta:+.9f}")
    print(f"CI95 = [{ci_lo:+.9f}, {ci_hi:+.9f}]")
    print(f"folds_nonnegative = {nonneg}/5")
    print(f"AIM5 = {status}")
    print(f"S2 = {s2}")
    print(f"RESULT_ZIP = {result_zip}")
    print("STOP = AIM5_EXECUTION_COMPLETE")
    return 0


def precheck(workdir: Path) -> int:
    helper = workdir / "cuhkx_aim4_structured_set.py"
    if not helper.exists():
        raise FileNotFoundError(helper)
    got = sha256_file(helper)
    if got != HELPER_SHA256:
        raise RuntimeError(f"AIM4 helper SHA mismatch: {got} != {HELPER_SHA256}")
    aim4 = load_module("aim5_precheck_aim4_helper", helper)
    aim4.load_inputs(workdir)
    print("PRECHECK = PASS")
    print("STOP = AIM5_PRECHECK_ONLY")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", type=Path, default=Path.cwd())
    ap.add_argument("--outdir", type=Path, default=None)
    ap.add_argument("--precheck-only", action="store_true")
    args = ap.parse_args()
    workdir = args.workdir.resolve()
    outdir = (args.outdir or (workdir / "cuhkx_aim5_conditional_setmap")).resolve()
    try:
        if args.precheck_only:
            return precheck(workdir)
        return run(workdir, outdir)
    except Exception as exc:
        print("STOP = AIM5_NOT_IDENTIFIED")
        print(f"REASON = {type(exc).__name__}")
        print(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
