#!/usr/bin/env python3
"""CUHK-X AIM4 — frozen structured cardinality decoder for HAU multi."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import platform
import sys
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

AIM_ID = "CUHKX_AIM4_STRUCTURED_CARDINALITY_TOPK_V1"
SEED = 260813
BOOT_SEED = 260816
N_BOOT = 20000
MATERIAL_DELTA_EXACT = 0.05
MIN_NONNEG_FOLDS = 4
EXPECTED_HAU = 809
EXPECTED_PAIRS = 3236
EXPECTED_COMMON = 786
EXPECTED_V7_DIM = 53762
POSE_DIM = 3782
IMU_DIM = 2817
V7F_DIM = 60361
EXPECTED_V7_RESULTS_SHA256 = "af7687fad3c7a4d140707c09dd84edea79288abdd81f91e9755d21cb63aad088"
EXPECTED_S1_SHA256 = "38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f"
EXPECTED_TRAIN_SHA256 = "667a00cb03ec67e1eeb49a744cb4fc764878fadae0b35ea873e25c2f7b3868bc"
EXPECTED_V7_CACHE_SHA256 = "e9699696af7d886896df7fa1e52d2b28ecfbb8abeef71a6b3b2ee04a68abb5db"
EXPECTED_POSE_CACHE_SHA256 = "d7e609a5e8a9ebc4bbdda92f8fe601d8b0c6ccfd4a2757f9a632a1ac9211b89a"
EXPECTED_IMU_CACHE_SHA256 = "8c4656e2c76029783c18d0b76f92f58fa8165a786a7049c3be7bf90a28aa0234"
TRAIN_QA_MEMBER = "Training/training_qa.csv"
FOLD_TO_SUBJECTS = {
    0: [2, 16, 20],
    1: [3, 9, 18, 24],
    2: [1, 19, 22],
    3: [5, 7, 8, 21],
    4: [4, 6, 17, 23],
}
SUBJECT_TO_FOLD = {s: f for f, ss in FOLD_TO_SUBJECTS.items() for s in ss}


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


def make_base_model():
    return Pipeline([
        ("scale", StandardScaler()),
        ("clf", SGDClassifier(
            loss="hinge", penalty="l2", alpha=1e-4,
            class_weight="balanced", max_iter=100, tol=1e-3,
            shuffle=True, random_state=SEED, average=True, n_jobs=-1,
        )),
    ])


class ModelFactory:
    @staticmethod
    def make_model():
        return make_base_model()


def subject_from_path(path: str) -> int:
    text = str(path).replace("\\", "/")
    for part in text.split("/"):
        if part.startswith("user") and part[4:].isdigit():
            return int(part[4:])
    raise ValueError(f"cannot parse HAU subject from {path!r}")


def exact_answer_from_labels(g: pd.DataFrame) -> str:
    return "".join(sorted(g.loc[g.label == 1, "option"].astype(str).tolist()))


def chosen_from_margins(g: pd.DataFrame, k: int | None = None) -> str:
    rows = [(float(r.margin), str(r.option)) for r in g.itertuples(index=False)]
    if k is None:
        chosen = [letter for margin, letter in rows if margin >= 0.0]
        if not chosen:
            # Exact S1 tuple-max behavior: margin first, option letter breaks an exact tie.
            chosen = [max(rows)[1]]
    else:
        if k < 1 or k > 4:
            raise RuntimeError(f"invalid predicted cardinality {k}")
        chosen = [letter for _, letter in sorted(rows, reverse=True)[:k]]
    return "".join(sorted(chosen))


def decoder_features(g: pd.DataFrame) -> np.ndarray:
    m = np.asarray(sorted(g.margin.astype(float).tolist(), reverse=True), dtype=float)
    if m.shape != (4,):
        raise RuntimeError(f"expected four margins, got {m.shape}")
    n_pos = float(np.sum(m >= 0.0))
    return np.asarray([m[0], m[1], m[2], m[3], n_pos], dtype=float)


def make_decoder():
    return Pipeline([
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(
            C=1.0, solver="lbfgs", max_iter=1000, class_weight=None,
        )),
    ])


def load_inputs(workdir: Path):
    paths = {
        "s1": workdir / "cuhkx_submission1.py",
        "train": workdir / "Training-20260813T154030Z-1-002.zip",
        "v7": workdir / "cuhkx_v7_ir_dinov2_cache" / "features.npz",
        "pose": workdir / "cuhkx_b2_hau_pose_cache" / "features.npz",
        "imu": workdir / "cuhkx_b4_imu_v2_cache" / "features.npz",
        "v7_results": workdir / "cuhkx_v7_strong_ir_dinov2_results.zip",
    }
    expected = {
        "s1": EXPECTED_S1_SHA256,
        "train": EXPECTED_TRAIN_SHA256,
        "v7": EXPECTED_V7_CACHE_SHA256,
        "pose": EXPECTED_POSE_CACHE_SHA256,
        "imu": EXPECTED_IMU_CACHE_SHA256,
        "v7_results": EXPECTED_V7_RESULTS_SHA256,
    }
    hashes = {}
    for key, p in paths.items():
        if not p.exists():
            raise FileNotFoundError(p)
        got = sha256_file(p)
        if got != expected[key]:
            raise RuntimeError(f"{key} SHA mismatch: {got} != {expected[key]}")
        hashes[key] = got

    s1 = load_module("aim4_s1", paths["s1"])

    with zipfile.ZipFile(paths["train"]) as z:
        with z.open(TRAIN_QA_MEMBER) as f:
            qa = pd.read_csv(f)
    q = qa[(qa.source == "HAU") & (qa.category == "multi")].copy()
    if len(q) != EXPECTED_HAU or q.qa_id.nunique() != EXPECTED_HAU:
        raise RuntimeError(f"HAU multi population drift: {len(q)}/{q.qa_id.nunique()}")
    q["subject"] = q.path.map(subject_from_path)
    q["fold"] = q.subject.map(SUBJECT_TO_FOLD)
    if q.fold.isna().any():
        raise RuntimeError("unmapped HAU subject")
    q["fold"] = q.fold.astype(int)

    dv = np.load(paths["v7"], allow_pickle=False)
    Xv = dv["X"].astype(np.float32, copy=False)
    uv = dv["units"].astype(str)
    if Xv.shape != (EXPECTED_HAU, EXPECTED_V7_DIM) or len(set(uv)) != EXPECTED_HAU:
        raise RuntimeError(f"V7 cache drift: {Xv.shape}/{len(set(uv))}")
    v7_map = {u: Xv[i] for i, u in enumerate(uv)}

    dp = np.load(paths["pose"], allow_pickle=False)
    Xp = dp["X"].astype(np.float32, copy=False)
    up = dp["units"].astype(str)
    if Xp.shape[1] != POSE_DIM:
        raise RuntimeError(f"pose dim drift: {Xp.shape}")
    pose_map = {u: Xp[i] for i, u in enumerate(up)}

    di = np.load(paths["imu"], allow_pickle=False)
    Xi = di["X"].astype(np.float32, copy=False)
    ui = di["units"].astype(str)
    if Xi.shape != (EXPECTED_COMMON, IMU_DIM) or len(set(ui)) != EXPECTED_COMMON:
        raise RuntimeError(f"IMU cache drift: {Xi.shape}/{len(set(ui))}")
    if any(u not in pose_map or u not in v7_map for u in ui):
        raise RuntimeError("V7F common support missing pose/V7 features")
    common = set(ui)
    v7f_map = {
        u: np.concatenate([pose_map[u], Xi[i], v7_map[u]]).astype(np.float32)
        for i, u in enumerate(ui)
    }
    if any(x.shape != (V7F_DIM,) for x in v7f_map.values()):
        raise RuntimeError("V7F feature dimension drift")

    with zipfile.ZipFile(paths["v7_results"]) as z:
        v7c = pd.read_csv(z.open("V7_all809_candidate_predictions.csv"))
        v7fc = pd.read_csv(z.open("V7F_candidate_predictions.csv"))
    if len(v7c) != EXPECTED_PAIRS or len(v7fc) != EXPECTED_COMMON * 4:
        raise RuntimeError("V7 result candidate population drift")
    frozen = pd.concat([
        v7fc.assign(route="V7F"),
        v7c[~v7c.qa_id.astype(str).isin(set(v7fc.qa_id.astype(str)))].assign(route="V7_IR_FALLBACK"),
    ], ignore_index=True)
    if len(frozen) != EXPECTED_PAIRS:
        raise RuntimeError(f"frozen route pair drift: {len(frozen)}")
    frozen["qa_id"] = frozen.qa_id.astype(str)
    frozen["option"] = frozen.option.astype(str)
    frozen_key = frozen.set_index(["qa_id", "option"])

    return paths, hashes, s1, q, v7_map, v7f_map, common, frozen_key


def reconstruct_oof(s1, q, v7_map, v7f_map, common, frozen_key):
    rows = []
    sign_mismatches = []
    for fold in range(5):
        qtr = q[q.fold != fold].copy()
        qva = q[q.fold == fold].copy()
        ir_models = s1.train_per_action_candidate_models(v7_map, qtr, ModelFactory)
        qtr_f = qtr[qtr.path.astype(str).isin(common)].copy()
        v7f_models = s1.train_per_action_candidate_models(v7f_map, qtr_f, ModelFactory)

        for r in qva.itertuples(index=False):
            qid = str(r.qa_id)
            unit = str(r.path)
            if unit in common:
                models, x, route = v7f_models, v7f_map[unit], "V7F"
            else:
                models, x, route = ir_models, v7_map[unit], "V7_IR_FALLBACK"
            _, action_margin = s1.score_action_models(models, x)
            true_letters = set(str(r.answer))
            for option in "ABCD":
                action = str(getattr(r, option))
                margin = float(action_margin[action])
                pred_sign = int(margin >= 0.0)
                key = (qid, option)
                if key not in frozen_key.index:
                    raise RuntimeError(f"missing frozen candidate key {key}")
                old = frozen_key.loc[key]
                old_pred = int(old.prediction)
                if pred_sign != old_pred:
                    sign_mismatches.append((qid, option, pred_sign, old_pred, fold, route))
                rows.append({
                    "qa_id": qid,
                    "path": unit,
                    "subject": int(r.subject),
                    "fold": fold,
                    "option": option,
                    "action": action,
                    "label": int(option in true_letters),
                    "margin": margin,
                    "sign_prediction": pred_sign,
                    "route": route,
                })
    df = pd.DataFrame(rows)
    if len(df) != EXPECTED_PAIRS or df.qa_id.nunique() != EXPECTED_HAU:
        raise RuntimeError(f"OOF reconstruction drift: {len(df)}/{df.qa_id.nunique()}")
    if sign_mismatches:
        sample = sign_mismatches[:10]
        raise RuntimeError(f"BASE_SIGN_REPRODUCTION_FAILURE n={len(sign_mismatches)} sample={sample}")
    return df


def episode_table(cand: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for qid, g in cand.groupby("qa_id", sort=False):
        g = g.sort_values("option")
        truth = exact_answer_from_labels(g)
        baseline = chosen_from_margins(g, None)
        x = decoder_features(g)
        rows.append({
            "qa_id": str(qid),
            "path": str(g.path.iloc[0]),
            "subject": int(g.subject.iloc[0]),
            "fold": int(g.fold.iloc[0]),
            "truth": truth,
            "true_k": len(truth),
            "baseline_answer": baseline,
            "baseline_exact": int(baseline == truth),
            "mA": float(g.loc[g.option == "A", "margin"].iloc[0]),
            "mB": float(g.loc[g.option == "B", "margin"].iloc[0]),
            "mC": float(g.loc[g.option == "C", "margin"].iloc[0]),
            "mD": float(g.loc[g.option == "D", "margin"].iloc[0]),
            "s1": float(x[0]), "s2": float(x[1]), "s3": float(x[2]), "s4": float(x[3]),
            "n_pos": int(x[4]),
            "route": str(g.route.iloc[0]),
        })
    ep = pd.DataFrame(rows)
    if len(ep) != EXPECTED_HAU:
        raise RuntimeError(f"episode table drift: {len(ep)}")
    return ep


def crossfit_decoder(ep: pd.DataFrame) -> pd.DataFrame:
    out = ep.copy()
    out["decoder_k"] = -1
    out["decoder_answer"] = ""
    feats = ["s1", "s2", "s3", "s4", "n_pos"]
    for fold in range(5):
        tr = out[out.fold != fold]
        va = out[out.fold == fold]
        model = make_decoder()
        model.fit(tr[feats].to_numpy(float), tr.true_k.to_numpy(int))
        khat = model.predict(va[feats].to_numpy(float)).astype(int)
        out.loc[va.index, "decoder_k"] = khat
        for idx, k in zip(va.index, khat):
            row = out.loc[idx]
            g = pd.DataFrame({
                "option": list("ABCD"),
                "margin": [row.mA, row.mB, row.mC, row.mD],
            })
            out.at[idx, "decoder_answer"] = chosen_from_margins(g, int(k))
    if (out.decoder_k < 1).any() or (out.decoder_answer == "").any():
        raise RuntimeError("decoder crossfit incomplete")
    out["decoder_exact"] = (out.decoder_answer == out.truth).astype(int)
    out["paired_delta"] = out.decoder_exact - out.baseline_exact
    return out


def candidate_metrics(ep: pd.DataFrame, answer_col: str) -> dict:
    y, p = [], []
    for r in ep.itertuples(index=False):
        truth = set(str(r.truth))
        pred = set(str(getattr(r, answer_col)))
        for option in "ABCD":
            y.append(int(option in truth))
            p.append(int(option in pred))
    return {
        "accuracy": float(accuracy_score(y, p)),
        "balanced_accuracy": float(balanced_accuracy_score(y, p)),
    }


def subject_bootstrap(ep: pd.DataFrame) -> tuple[float, float]:
    subjects = np.asarray(sorted(ep.subject.unique()), dtype=int)
    by_subject = {s: ep[ep.subject == s].paired_delta.to_numpy(float) for s in subjects}
    rng = np.random.default_rng(BOOT_SEED)
    vals = np.empty(N_BOOT, dtype=float)
    for b in range(N_BOOT):
        draw = rng.choice(subjects, size=len(subjects), replace=True)
        arr = np.concatenate([by_subject[int(s)] for s in draw])
        vals[b] = float(arr.mean())
    return float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))


def run(workdir: Path, outdir: Path) -> int:
    paths, hashes, s1, q, v7_map, v7f_map, common, frozen_key = load_inputs(workdir)
    print("PRECHECK = PASS")
    print("[1/4] Reconstructing exact S1 OOF normalized-margin route...", flush=True)
    cand = reconstruct_oof(s1, q, v7_map, v7f_map, common, frozen_key)
    print("BASE_SIGN_REPRODUCTION = PASS")

    print("[2/4] Constituting S1 baseline and frozen decoder features...", flush=True)
    ep = episode_table(cand)
    baseline_exact = float(ep.baseline_exact.mean())

    print("[3/4] Cross-fitting frozen CARDINALITY_TOPK_V1...", flush=True)
    ep = crossfit_decoder(ep)
    decoder_exact = float(ep.decoder_exact.mean())
    delta = decoder_exact - baseline_exact
    ci_lo, ci_hi = subject_bootstrap(ep)

    fold_rows = []
    nonneg = 0
    for fold in range(5):
        g = ep[ep.fold == fold]
        b = float(g.baseline_exact.mean())
        d = float(g.decoder_exact.mean())
        dd = d - b
        nonneg += int(dd >= 0.0)
        fold_rows.append({"fold": fold, "n": len(g), "baseline_exact": b, "decoder_exact": d, "delta": dd})

    support = bool(delta >= MATERIAL_DELTA_EXACT and nonneg >= MIN_NONNEG_FOLDS and ci_lo > 0.0)
    status = (
        "SUPPORTED_STRUCTURED_CARDINALITY_DECODER_IN_FROZEN_MULTI_SCOPE"
        if support else "NOT_SUPPORTED_STRUCTURED_CARDINALITY_DECODER"
    )
    s2 = "PACKAGING_CANDIDATE_AUTHORIZED" if support else "NOT_AUTHORIZED"

    outdir.mkdir(parents=True, exist_ok=True)
    cand.to_csv(outdir / "aim4_oof_candidate_margins.csv", index=False)
    ep.to_csv(outdir / "aim4_oof_episode_predictions.csv", index=False)
    pd.DataFrame(fold_rows).to_csv(outdir / "aim4_fold_metrics.csv", index=False)

    summary = {
        "STOP": "AIM4_EXECUTION_COMPLETE",
        "AIM4": status,
        "S2": s2,
        "baseline": {
            "name": "S1_EXACT_NORMALIZED_MARGIN_WITH_SINGLETON_FALLBACK",
            "exact_accuracy": baseline_exact,
            "candidate_metrics": candidate_metrics(ep, "baseline_answer"),
        },
        "decoder": {
            "name": "CARDINALITY_TOPK_V1",
            "exact_accuracy": decoder_exact,
            "candidate_metrics": candidate_metrics(ep, "decoder_answer"),
            "delta_exact": delta,
            "folds_nonnegative": nonneg,
            "subject_bootstrap_ci95": [ci_lo, ci_hi],
            "true_cardinality_counts": {str(k): int(v) for k, v in ep.true_k.value_counts().sort_index().items()},
            "predicted_cardinality_counts": {str(k): int(v) for k, v in ep.decoder_k.value_counts().sort_index().items()},
        },
        "gates": {
            "required_delta_exact": MATERIAL_DELTA_EXACT,
            "required_nonnegative_folds": MIN_NONNEG_FOLDS,
            "require_bootstrap_ci_lower_gt_zero": True,
            "bootstrap_resamples": N_BOOT,
            "bootstrap_seed": BOOT_SEED,
        },
        "population": {"episodes": EXPECTED_HAU, "candidate_pairs": EXPECTED_PAIRS, "v7f_common": EXPECTED_COMMON},
        "hashes": hashes,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "sklearn": sklearn.__version__,
        },
        "authority_ceiling": (
            "Internal subject-held-out evidence for the single frozen HAU-multi CARDINALITY_TOPK_V1 "
            "decoder over exact S1-normalized candidate margins. No authority for other branches, "
            "other structured decoders, or leaderboard transfer."
        ),
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    result_zip = outdir.parent / "cuhkx_aim4_structured_set_results.zip"
    if result_zip.exists():
        result_zip.unlink()
    with zipfile.ZipFile(result_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(outdir.iterdir()):
            if p.is_file():
                z.write(p, arcname=p.name)
        z.write(Path(__file__).resolve(), arcname=Path(__file__).name)

    print("[4/4] COMPLETE")
    print(f"B0_exact = {baseline_exact:.9f}")
    print(f"D1_exact = {decoder_exact:.9f}")
    print(f"delta_exact = {delta:+.9f}")
    print(f"CI95 = [{ci_lo:+.9f}, {ci_hi:+.9f}]")
    print(f"folds_nonnegative = {nonneg}/5")
    print(f"AIM4 = {status}")
    print(f"S2 = {s2}")
    print(f"RESULT_ZIP = {result_zip}")
    print("STOP = AIM4_EXECUTION_COMPLETE")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", type=Path, default=Path.cwd())
    ap.add_argument("--outdir", type=Path, default=None)
    ap.add_argument("--precheck-only", action="store_true")
    args = ap.parse_args()
    workdir = args.workdir.resolve()
    outdir = (args.outdir or (workdir / "cuhkx_aim4_structured_set")).resolve()
    try:
        if args.precheck_only:
            load_inputs(workdir)
            print("PRECHECK = PASS")
            print("STOP = AIM4_PRECHECK_ONLY")
            return 0
        return run(workdir, outdir)
    except Exception as exc:
        print("STOP = AIM4_NOT_IDENTIFIED")
        print(f"REASON = {type(exc).__name__}")
        print(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
