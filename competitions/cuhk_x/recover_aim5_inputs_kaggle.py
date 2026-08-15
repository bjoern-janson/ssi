#!/usr/bin/env python3
"""CUHK-X: hash-only recovery probe for historical AIM5 frozen inputs on Kaggle.

This program does NOT run AIM5, fit a model, extract features, or execute the
mechanical precheck. It only searches mounted Kaggle inputs for byte-identical
historical files required by the frozen AIM5 Stage-1 boundary.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from typing import BinaryIO

HASH_CHUNK = 8 * 1024 * 1024

EXPECTED = {
    "training_zip": {
        "name": "Training-20260813T154030Z-1-002.zip",
        "sha256": "667a00cb03ec67e1eeb49a744cb4fc764878fadae0b35ea873e25c2f7b3868bc",
    },
    "v7_cache": {
        "name": "features.npz",
        "sha256": "e9699696af7d886896df7fa1e52d2b28ecfbb8abeef71a6b3b2ee04a68abb5db",
    },
    "pose_cache": {
        "name": "features.npz",
        "sha256": "d7e609a5e8a9ebc4bbdda92f8fe601d8b0c6ccfd4a2757f9a632a1ac9211b89a",
    },
    "imu_cache": {
        "name": "features.npz",
        "sha256": "8c4656e2c76029783c18d0b76f92f58fa8165a786a7049c3be7bf90a28aa0234",
    },
    "s1_script": {
        "name": "cuhkx_submission1.py",
        "sha256": "38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f",
    },
    "v7_results": {
        "name": "cuhkx_v7_strong_ir_dinov2_results.zip",
        "sha256": "af7687fad3c7a4d140707c09dd84edea79288abdd81f91e9755d21cb63aad088",
    },
    "aim4_helper": {
        "name": "cuhkx_aim4_structured_set.py",
        "sha256": "ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5",
    },
    "aim5_executable": {
        "name": "cuhkx_aim5_conditional_setmap.py",
        "sha256": "620e35da4256e3368359e202729e45489b916687ef890e3f9d887e91f11a0605",
    },
}


def hash_stream(f: BinaryIO) -> str:
    h = hashlib.sha256()
    while True:
        b = f.read(HASH_CHUNK)
        if not b:
            break
        h.update(b)
    return h.hexdigest()


def hash_file(path: Path) -> str:
    with path.open("rb") as f:
        return hash_stream(f)


def candidate_direct_files(root: Path) -> list[Path]:
    wanted = {v["name"] for v in EXPECTED.values()}
    # Also report the historical private bundle/precheck if present.
    wanted |= {"cuhkx_aim5_private_inputs.zip", "cuhkx_aim5_precheck.py"}
    return sorted(p for p in root.rglob("*") if p.is_file() and p.name in wanted)


def candidate_zip_members(root: Path) -> list[tuple[Path, str, int]]:
    wanted = {v["name"] for v in EXPECTED.values()}
    wanted |= {"cuhkx_aim5_precheck.py"}
    rows: list[tuple[Path, str, int]] = []
    # Limit archive inspection to mounted ZIP files; reading central directories
    # does not extract media or execute code.
    for zp in sorted(p for p in root.rglob("*.zip") if p.is_file()):
        try:
            with zipfile.ZipFile(zp) as z:
                for info in z.infolist():
                    if info.is_dir():
                        continue
                    if Path(info.filename).name in wanted:
                        rows.append((zp, info.filename, int(info.file_size)))
        except zipfile.BadZipFile:
            continue
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("/kaggle/input"))
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("/kaggle/working/cuhkx_aim5_input_reconstitution.json"),
    )
    args = ap.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    print("FREEZE = AIM5_INPUT_RECONSTITUTION_HASH_ONLY")
    print("ROOT =", root)

    observed: list[dict] = []

    direct = candidate_direct_files(root)
    print(f"DIRECT_CANDIDATES = {len(direct)}")
    for p in direct:
        print("HASH_DIRECT =", p)
        observed.append({
            "kind": "direct",
            "location": str(p),
            "basename": p.name,
            "bytes": int(p.stat().st_size),
            "sha256": hash_file(p),
        })

    members = candidate_zip_members(root)
    print(f"ZIP_MEMBER_CANDIDATES = {len(members)}")
    for zp, member, size in members:
        # Do not duplicate a nested member that is the outer archive itself.
        print("HASH_ZIP_MEMBER =", f"{zp}::{member}")
        with zipfile.ZipFile(zp) as z, z.open(member) as f:
            sha = hash_stream(f)
        observed.append({
            "kind": "zip_member",
            "location": f"{zp}::{member}",
            "basename": Path(member).name,
            "bytes": size,
            "sha256": sha,
        })

    status = {}
    for key, spec in EXPECTED.items():
        matches = [
            r for r in observed
            if r["basename"] == spec["name"] and r["sha256"] == spec["sha256"]
        ]
        status[key] = {
            "expected_name": spec["name"],
            "expected_sha256": spec["sha256"],
            "match_count": len(matches),
            "matches": matches,
            "status": "PASS" if matches else "MISSING_OR_HASH_MISMATCH",
        }

    # Historical Stage-1 core requires these six provenance/data inputs.
    stage1_core = [
        "training_zip", "v7_cache", "pose_cache", "imu_cache",
        "s1_script", "v7_results",
    ]
    helpers = ["aim4_helper", "aim5_executable"]
    core_pass = all(status[k]["status"] == "PASS" for k in stage1_core)
    helper_pass = all(status[k]["status"] == "PASS" for k in helpers)

    bundle_rows = [r for r in observed if r["basename"] == "cuhkx_aim5_private_inputs.zip"]
    precheck_rows = [r for r in observed if r["basename"] == "cuhkx_aim5_precheck.py"]

    report = {
        "probe": "AIM5_INPUT_RECONSTITUTION_HASH_ONLY",
        "root": str(root),
        "expected": EXPECTED,
        "observed_candidates": observed,
        "status": status,
        "stage1_core_inputs_pass": core_pass,
        "aim4_aim5_helpers_pass": helper_pass,
        "private_bundle_candidates": bundle_rows,
        "precheck_candidates": precheck_rows,
        "modeling_authority": "NONE",
        "precheck_authority": (
            "ELIGIBLE_FOR_REVIEW" if core_pass and helper_pass and precheck_rows
            else "NOT_YET_ELIGIBLE"
        ),
        "next_gate": (
            "If all frozen inputs/helpers and a precheck executable are present, "
            "review this report and separately authorize Stage-1 mechanical precheck."
        ),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n=== FROZEN MATCH STATUS ===")
    for key in EXPECTED:
        x = status[key]
        print(f"{key:16s} {x['status']:24s} matches={x['match_count']}")

    print("\nSTAGE1_CORE_INPUTS_PASS =", core_pass)
    print("AIM4_AIM5_HELPERS_PASS =", helper_pass)
    print("PRECHECK_CANDIDATES =", len(precheck_rows))
    print("REPORT =", args.out)
    print("MODELING_AUTHORITY = NONE")
    print("STOP = RETURN_AIM5_INPUT_RECONSTITUTION_REPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
