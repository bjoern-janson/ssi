#!/usr/bin/env python3
"""Audit current CUHK-X Kaggle competition bytes before any modeling.

This program is intentionally model-agnostic. It recursively inventories a
user-authorized competition download, hashes every file, inspects tabular
schemas, and emits candidate grouping/task metadata when those columns exist.
It does not import or depend on any prior CUHK-X experimental artifact.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

VERSION = "CUHKX_RAW_AUDIT_V1"
HASH_CHUNK = 8 * 1024 * 1024
TABULAR_SUFFIXES = {".csv", ".tsv"}
CANDIDATE_COLUMNS = (
    "source",
    "task",
    "category",
    "type",
    "subject",
    "user",
    "qa_id",
    "question_id",
    "path",
    "answer",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(HASH_CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def scalar_for_json(x: Any) -> Any:
    if pd.isna(x):
        return None
    if hasattr(x, "item"):
        try:
            return x.item()
        except Exception:
            pass
    return x


def value_profile(series: pd.Series, max_values: int = 100) -> dict[str, Any]:
    vc = series.value_counts(dropna=False)
    values = []
    for key, count in vc.iloc[:max_values].items():
        values.append({"value": scalar_for_json(key), "count": int(count)})
    return {
        "n_unique_dropna": int(series.nunique(dropna=True)),
        "n_missing": int(series.isna().sum()),
        "top_values": values,
        "truncated": bool(len(vc) > max_values),
    }


def inspect_table(path: Path) -> dict[str, Any]:
    sep = "\t" if path.suffix.lower() == ".tsv" else ","
    df = pd.read_csv(path, sep=sep, low_memory=False)
    report: dict[str, Any] = {
        "rows": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "dtypes": {str(c): str(df[c].dtype) for c in df.columns},
        "candidate_profiles": {},
    }
    for c in CANDIDATE_COLUMNS:
        if c in df.columns:
            report["candidate_profiles"][c] = value_profile(df[c])

    # Generic duplicate signals relevant to leakage-safe validation.
    for c in ("qa_id", "question_id", "path"):
        if c in df.columns:
            report[f"duplicate_rows_by_{c}"] = int(df.duplicated(c, keep=False).sum())

    # If a path and question identifier coexist, quantify questions/episode.
    qcol = next((c for c in ("qa_id", "question_id") if c in df.columns), None)
    if "path" in df.columns and qcol:
        per_path = df.groupby("path", dropna=False)[qcol].nunique(dropna=False)
        report["questions_per_path"] = {
            "n_paths": int(len(per_path)),
            "min": int(per_path.min()) if len(per_path) else None,
            "median": float(per_path.median()) if len(per_path) else None,
            "max": int(per_path.max()) if len(per_path) else None,
            "paths_with_multiple_questions": int((per_path > 1).sum()),
        }

    # Option-column detection without assuming names are A/B/C/D.
    option_cols = [c for c in df.columns if str(c).upper() in {"A", "B", "C", "D", "E", "F"}]
    if option_cols:
        report["option_columns"] = [str(c) for c in option_cols]

    return report


def inspect_zip(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as z:
        infos = [i for i in z.infolist() if not i.is_dir()]
        return {
            "members": len(infos),
            "uncompressed_bytes": int(sum(i.file_size for i in infos)),
            "sample_members": [i.filename for i in infos[:100]],
            "sample_truncated": bool(len(infos) > 100),
        }


def inventory(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        stat = path.stat()
        row: dict[str, Any] = {
            "path": safe_rel(path, root),
            "bytes": int(stat.st_size),
            "sha256": sha256_file(path),
            "suffix": path.suffix.lower(),
        }
        if path.suffix.lower() in TABULAR_SUFFIXES:
            try:
                row["table"] = inspect_table(path)
            except Exception as exc:
                row["table_error"] = f"{type(exc).__name__}: {exc}"
        elif path.suffix.lower() == ".zip":
            try:
                row["zip"] = inspect_zip(path)
            except Exception as exc:
                row["zip_error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return rows


def write_manifest_csv(rows: list[dict[str, Any]], path: Path) -> None:
    fields = ["path", "bytes", "sha256", "suffix"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in fields})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path, help="Directory containing current Kaggle competition files")
    ap.add_argument("--out", type=Path, default=None, help="Output directory (default: <root>/raw_audit)")
    args = ap.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 2

    out = (args.out or (root / "raw_audit")).resolve()
    out.mkdir(parents=True, exist_ok=True)

    # Avoid recursively auditing our own output if rerun.
    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and out not in p.parents):
        stat = path.stat()
        row: dict[str, Any] = {
            "path": safe_rel(path, root),
            "bytes": int(stat.st_size),
            "sha256": sha256_file(path),
            "suffix": path.suffix.lower(),
        }
        if path.suffix.lower() in TABULAR_SUFFIXES:
            try:
                row["table"] = inspect_table(path)
            except Exception as exc:
                row["table_error"] = f"{type(exc).__name__}: {exc}"
        elif path.suffix.lower() == ".zip":
            try:
                row["zip"] = inspect_zip(path)
            except Exception as exc:
                row["zip_error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)

    total_bytes = sum(r["bytes"] for r in rows)
    suffix_counts = Counter(r["suffix"] or "<none>" for r in rows)
    report = {
        "audit_version": VERSION,
        "root": str(root),
        "file_count": len(rows),
        "total_bytes": int(total_bytes),
        "suffix_counts": dict(sorted(suffix_counts.items())),
        "files": rows,
        "modeling_authority": "NONE — raw contract audit only",
        "next_gate": (
            "Human/research review must identify authoritative train/test/submission files, "
            "evaluation metric, grouping unit, and leakage-safe validation contract before modeling."
        ),
    }

    report_path = out / "RAW_AUDIT.json"
    manifest_path = out / "RAW_MANIFEST.csv"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_manifest_csv(rows, manifest_path)

    print(f"AUDIT_VERSION = {VERSION}")
    print(f"FILES = {len(rows)}")
    print(f"TOTAL_BYTES = {total_bytes}")
    print(f"REPORT = {report_path}")
    print(f"MANIFEST = {manifest_path}")
    print("STATUS = RAW_AUDIT_COMPLETE")
    print("MODELING_AUTHORITY = NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
