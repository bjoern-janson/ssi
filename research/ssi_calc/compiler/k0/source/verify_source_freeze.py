#!/usr/bin/env python3
"""Verify the frozen K0 source contract without importing compiler or SSI code."""

from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = json.loads((ROOT / "MANIFEST.json").read_text())
for rel, meta in manifest["files"].items():
    path = ROOT / rel
    assert path.exists(), rel
    assert sha256(path) == meta["sha256"], (rel, sha256(path), meta["sha256"])
    assert path.stat().st_size == meta["bytes"], rel

assert manifest["compiler_executed"] is False
assert manifest["ssi_calc_imported"] is False

spec = importlib.util.spec_from_file_location("k0_source_reference", ROOT / "source_reference.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

tasks_doc = json.loads((ROOT / "TASKS.json").read_text())
gold_doc = json.loads((ROOT / "gold" / "GOLD.json").read_text())
dist_doc = json.loads((ROOT / "distinctions.json").read_text())

recomputed = module.evaluate_all(tasks_doc["cases"])

assert tasks_doc["case_count"] == 24
assert gold_doc["case_count"] == 24
assert len(recomputed) == 24
assert recomputed == gold_doc["cases"]
assert sum(1 for x in recomputed if x["judgment"]) == 12
assert sum(1 for x in recomputed if not x["judgment"]) == 12
assert len(dist_doc["distinctions"]) == 8

case_ids = {case["id"] for case in tasks_doc["cases"]}
assert case_ids == {f"CASE-{i:03d}" for i in range(1, 25)}
for d in dist_doc["distinctions"]:
    assert d["witness_cases"], d["id"]
    assert set(d["witness_cases"]) <= case_ids, d["id"]

print(json.dumps({
    "object": "K0-SOURCE-TYPE-SYSTEM-COMPILER/SOURCE_FREEZE_VERIFY",
    "manifest_sha256": sha256(ROOT / "MANIFEST.json"),
    "case_count": 24,
    "positive": 12,
    "negative": 12,
    "distinction_count": 8,
    "gold_recomputed_exact": True,
    "compiler_executed": False,
    "ssi_calc_imported": False,
}, indent=2, sort_keys=True))
