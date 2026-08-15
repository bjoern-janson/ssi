#!/usr/bin/env python3
"""Kaggle-native RAW_AUDIT runner for the clean CUHK-X restart.

This script performs no modeling. It locates the mounted CUHK-X competition
payload under /kaggle/input, inventories and hashes the mounted files, inspects
CSV/TSV tables both directly and inside ZIP archives, summarizes candidate
question/episode/subject/trial relationships, writes a frozen audit bundle,
and stops.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

import pandas as pd

VERSION = "CUHKX_KAGGLE_RAW_AUDIT_V1"
HASH_CHUNK = 8 * 1024 * 1024
MAX_ZIP_TABLE_BYTES = 64 * 1024 * 1024
TABULAR_SUFFIXES = {".csv", ".tsv"}

ID_CANDIDATES = (
    "qa_id", "question_id", "qid", "id",
)
EPISODE_CANDIDATES = (
    "episode_id", "episode", "trial_id", "trial", "recording_id", "recording",
    "clip_id", "clip", "sample_id", "sample", "path", "filepath", "file_path",
)
SUBJECT_CANDIDATES = (
    "subject_id", "subject", "user_id", "user", "participant_id", "participant",
)
TASK_CANDIDATES = (
    "source", "task", "category", "type", "reasoning_type", "question_type",
)
MODALITY_CANDIDATES = (
    "modality", "sensor", "sensor_type", "data_type",
)
ANSWER_CANDIDATES = (
    "answer", "label", "target", "prediction",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(HASH_CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_scalar(x: Any) -> Any:
    if pd.isna(x):
        return None
    if hasattr(x, "item"):
        try:
            return x.item()
        except Exception:
            pass
    return x


def normalize_columns(df: pd.DataFrame) -> dict[str, str]:
    return {str(c).strip().lower(): str(c) for c in df.columns}


def first_column(df: pd.DataFrame, names: tuple[str, ...]) -> str | None:
    lower = normalize_columns(df)
    for name in names:
        if name in lower:
            return lower[name]
    return None


def profile(series: pd.Series, topn: int = 30) -> dict[str, Any]:
    vc = series.value_counts(dropna=False)
    return {
        "n_unique_dropna": int(series.nunique(dropna=True)),
        "n_missing": int(series.isna().sum()),
        "top_values": [
            {"value": json_scalar(k), "count": int(v)}
            for k, v in vc.iloc[:topn].items()
        ],
        "truncated": bool(len(vc) > topn),
    }


def maybe_subject_from_path(value: Any) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).replace("\\", "/")
    patterns = (
        r"(?:^|/)(user[_-]?\d+)(?:/|$)",
        r"(?:^|/)(subject[_-]?\d+)(?:/|$)",
        r"(?:^|/)(sub[_-]?\d+)(?:/|$)",
    )
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            return m.group(1).lower()
    return None


def table_report(df: pd.DataFrame, origin: str) -> dict[str, Any]:
    report: dict[str, Any] = {
        "origin": origin,
        "rows": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "dtypes": {str(c): str(df[c].dtype) for c in df.columns},
    }

    qcol = first_column(df, ID_CANDIDATES)
    ecol = first_column(df, EPISODE_CANDIDATES)
    scol = first_column(df, SUBJECT_CANDIDATES)
    tcol = first_column(df, TASK_CANDIDATES)
    mcol = first_column(df, MODALITY_CANDIDATES)
    acol = first_column(df, ANSWER_CANDIDATES)

    report["detected_roles"] = {
        "question_id": qcol,
        "episode_or_path": ecol,
        "subject": scol,
        "task_or_category": tcol,
        "modality": mcol,
        "answer": acol,
    }

    prof_cols = [c for c in (qcol, ecol, scol, tcol, mcol, acol) if c is not None]
    report["profiles"] = {c: profile(df[c]) for c in dict.fromkeys(prof_cols)}

    option_cols = [str(c) for c in df.columns if str(c).strip().upper() in {"A", "B", "C", "D", "E", "F"}]
    if option_cols:
        report["option_columns"] = option_cols

    if qcol:
        report["duplicate_question_rows"] = int(df.duplicated(qcol, keep=False).sum())

    if ecol:
        report["duplicate_episode_rows"] = int(df.duplicated(ecol, keep=False).sum())

    if qcol and ecol:
        q_per_ep = df.groupby(ecol, dropna=False)[qcol].nunique(dropna=False)
        ep_per_q = df.groupby(qcol, dropna=False)[ecol].nunique(dropna=False)
        report["question_episode_structure"] = {
            "n_episodes": int(len(q_per_ep)),
            "questions_per_episode_min": int(q_per_ep.min()) if len(q_per_ep) else None,
            "questions_per_episode_median": float(q_per_ep.median()) if len(q_per_ep) else None,
            "questions_per_episode_max": int(q_per_ep.max()) if len(q_per_ep) else None,
            "episodes_with_multiple_questions": int((q_per_ep > 1).sum()),
            "questions_linked_to_multiple_episodes": int((ep_per_q > 1).sum()),
        }

    if ecol and scol:
        subj_per_ep = df.groupby(ecol, dropna=False)[scol].nunique(dropna=False)
        eps_per_subj = df.groupby(scol, dropna=False)[ecol].nunique(dropna=False)
        report["episode_subject_structure"] = {
            "episodes_linked_to_multiple_subjects": int((subj_per_ep > 1).sum()),
            "episodes_per_subject": {
                str(json_scalar(k)): int(v) for k, v in eps_per_subj.items()
            },
        }

    # If no explicit subject column exists but a path-like episode column does,
    # report path-derived subject tokens as a candidate structural signal only.
    if ecol and not scol:
        derived = df[ecol].map(maybe_subject_from_path)
        if derived.notna().any():
            report["path_derived_subject_candidate"] = profile(derived)

    return report


def read_table_bytes(data: bytes, suffix: str) -> pd.DataFrame:
    sep = "\t" if suffix == ".tsv" else ","
    return pd.read_csv(io.BytesIO(data), sep=sep, low_memory=False)


def inspect_zip(path: Path) -> dict[str, Any]:
    out: dict[str, Any] = {}
    with zipfile.ZipFile(path) as z:
        infos = [i for i in z.infolist() if not i.is_dir()]
        out.update({
            "members": len(infos),
            "uncompressed_bytes": int(sum(i.file_size for i in infos)),
            "member_suffix_counts": dict(sorted(Counter(PurePosixPath(i.filename).suffix.lower() or "<none>" for i in infos).items())),
            "sample_members": [i.filename for i in infos[:100]],
            "sample_truncated": bool(len(infos) > 100),
        })
        tables = []
        for info in infos:
            suffix = PurePosixPath(info.filename).suffix.lower()
            if suffix not in TABULAR_SUFFIXES:
                continue
            entry = {
                "member": info.filename,
                "bytes": int(info.file_size),
                "crc32": f"{info.CRC:08x}",
            }
            if info.file_size > MAX_ZIP_TABLE_BYTES:
                entry["table_skipped"] = f"member exceeds {MAX_ZIP_TABLE_BYTES} bytes"
            else:
                try:
                    data = z.read(info)
                    entry["sha256_uncompressed"] = sha256_bytes(data)
                    entry["table"] = table_report(read_table_bytes(data, suffix), f"{path.name}::{info.filename}")
                except Exception as exc:
                    entry["table_error"] = f"{type(exc).__name__}: {exc}"
            tables.append(entry)
        out["tabular_members"] = tables
    return out


def discover_root(input_root: Path) -> Path:
    exact = input_root / "cuhk-x-competition-large-model-track"
    if exact.is_dir():
        return exact
    dirs = [p for p in input_root.iterdir() if p.is_dir()]
    scored = []
    for p in dirs:
        name = p.name.lower()
        score = sum(token in name for token in ("cuhk", "competition", "large", "model"))
        if score:
            scored.append((score, p.name, p))
    if not scored:
        raise RuntimeError(f"cannot locate CUHK-X competition mount under {input_root}; dirs={[p.name for p in dirs]}")
    scored.sort(reverse=True)
    top_score = scored[0][0]
    top = [p for s, _, p in scored if s == top_score]
    if len(top) != 1:
        raise RuntimeError(f"ambiguous CUHK-X mounts under {input_root}: {[p.name for p in top]}")
    return top[0]


def write_manifest(rows: list[dict[str, Any]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "bytes", "sha256", "suffix"])
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in ("path", "bytes", "sha256", "suffix")})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", type=Path, default=Path("/kaggle/input"))
    ap.add_argument("--competition-root", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=Path("/kaggle/working/cuhkx_raw_audit"))
    args = ap.parse_args()

    root = args.competition_root.resolve() if args.competition_root else discover_root(args.input_root.resolve())
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        row: dict[str, Any] = {
            "path": rel,
            "bytes": int(path.stat().st_size),
            "sha256": sha256_file(path),
            "suffix": path.suffix.lower(),
        }
        if path.suffix.lower() in TABULAR_SUFFIXES:
            try:
                sep = "\t" if path.suffix.lower() == ".tsv" else ","
                df = pd.read_csv(path, sep=sep, low_memory=False)
                row["table"] = table_report(df, rel)
            except Exception as exc:
                row["table_error"] = f"{type(exc).__name__}: {exc}"
        elif path.suffix.lower() == ".zip":
            try:
                row["zip"] = inspect_zip(path)
            except Exception as exc:
                row["zip_error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)

    report = {
        "audit_version": VERSION,
        "competition_root": str(root),
        "file_count": len(rows),
        "total_bytes": int(sum(r["bytes"] for r in rows)),
        "suffix_counts": dict(sorted(Counter(r["suffix"] or "<none>" for r in rows).items())),
        "files": rows,
        "modeling_authority": "NONE — raw competition contract only",
        "status": "RAW_AUDIT_COMPLETE",
        "next_gate": (
            "Review authoritative train/test/submission tables and current Kaggle metric; "
            "freeze the true independence/grouping unit before any validation or model design."
        ),
    }

    report_path = out / "RAW_AUDIT.json"
    manifest_path = out / "RAW_MANIFEST.csv"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_manifest(rows, manifest_path)

    bundle = out.parent / "cuhkx_raw_audit_bundle.zip"
    if bundle.exists():
        bundle.unlink()
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(report_path, arcname=report_path.name)
        z.write(manifest_path, arcname=manifest_path.name)

    print(f"AUDIT_VERSION = {VERSION}")
    print(f"COMPETITION_ROOT = {root}")
    print(f"FILES = {len(rows)}")
    print(f"TOTAL_BYTES = {report['total_bytes']}")
    print(f"REPORT = {report_path}")
    print(f"MANIFEST = {manifest_path}")
    print(f"REPORT_SHA256 = {sha256_file(report_path)}")
    print(f"MANIFEST_SHA256 = {sha256_file(manifest_path)}")
    print(f"BUNDLE = {bundle}")
    print(f"BUNDLE_SHA256 = {sha256_file(bundle)}")
    print("STATUS = RAW_AUDIT_COMPLETE")
    print("MODELING_AUTHORITY = NONE")
    print("STOP = RAW_AUDIT_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
