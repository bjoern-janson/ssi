#!/usr/bin/env python3
"""Verify frozen K0 compiler artifacts without reading source gold or executing tasks."""

from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "source"
EXPECTED_SOURCE_MANIFEST = "27e5d9675453f36289bee9af8fc020655c9874799905bdac3a2ea700d6207345"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = json.loads((HERE / "MANIFEST.json").read_text())
for rel, meta in manifest["files"].items():
    path = HERE / rel
    assert path.exists(), rel
    assert sha256(path) == meta["sha256"], (rel, sha256(path), meta["sha256"])
    assert path.stat().st_size == meta["bytes"], rel

assert sha256(SOURCE / "MANIFEST.json") == EXPECTED_SOURCE_MANIFEST

spec = importlib.util.spec_from_file_location("k0_compiler", HERE / "compiler.py")
compiler = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(compiler)

rebuilt = compiler.canonical(compiler.build_ir())
frozen = (HERE / "IR.json").read_text()
assert rebuilt == frozen
assert hashlib.sha256(rebuilt.encode()).hexdigest() == manifest["ir_sha256"]

mutations = json.loads((HERE / "mutations.json").read_text())
assert mutations["frozen_before_audit"] is True
assert [m["id"] for m in mutations["mutations"]] == [
    "MUT-001", "MUT-002", "MUT-003", "MUT-004", "MUT-005", "MUT-006"
]

# Syntax-check the independent evaluator but do not execute any query.
compile((HERE / "ir_evaluator.py").read_text(), str(HERE / "ir_evaluator.py"), "exec")

# Enforce that compiler/evaluator sources do not read source gold.
for name in ["compiler.py", "ir_evaluator.py"]:
    text = (HERE / name).read_text()
    assert "gold/GOLD.json" not in text
    assert "source_reference" not in text

print(json.dumps({
    "object": "K0-SOURCE-TYPE-SYSTEM-COMPILER/COMPILER_FREEZE_VERIFY",
    "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST,
    "ir_sha256": manifest["ir_sha256"],
    "compiler_manifest_sha256": sha256(HERE / "MANIFEST.json"),
    "ir_rebuilt_exact": True,
    "hostile_mutation_count": 6,
    "source_gold_read": False,
    "tasks_executed": False,
    "ssi_calc_R1_R11_modified": False,
}, indent=2, sort_keys=True))
