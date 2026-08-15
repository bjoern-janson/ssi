#!/usr/bin/env python3
"""Deterministic extraction of cutoff migration-result files from frozen Biome snapshots.

The extractor consumes only immutable pre-freeze snapshot text. It supports the
two forms present in the six frozen V2 migration snapshots:

- WRITTEN_FILE_BLOCKS: snapshot file sections already contain post-migration JSON.
- DRY_RUN_PROPOSED_OUTPUTS: emitted migration diffs contain the proposed JSON
  output; this is required for the nested-config snapshot.

No future release, arm, Gamma, Phi, or outcome input is accepted.
"""
from __future__ import annotations

import json
import re
from typing import Mapping

WRITTEN_FILE_BLOCKS = "WRITTEN_FILE_BLOCKS"
DRY_RUN_PROPOSED_OUTPUTS = "DRY_RUN_PROPOSED_OUTPUTS"

_FILE_BLOCK = re.compile(
    r"^## `(?P<path>[^`]+)`\s*\n\s*```json\s*\n(?P<body>.*?)\n```",
    re.MULTILINE | re.DOTALL,
)
_DRY_RUN_BLOCK = re.compile(
    r"^<TEMP_DIR>/[^/]+/(?P<path>[^\n]+?) migrate[^\n]*\n(?P<body>.*?)(?=^```|\Z)",
    re.MULTILINE | re.DOTALL,
)
_PLUS_LINE = re.compile(r"^\s*\+\s+(?P<json>\{.*\})\s*$", re.MULTILINE)


def _canonical_json_bytes(text: str) -> bytes:
    obj = json.loads(text)
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _normalize_path(path: str) -> str:
    x = path.replace("\\", "/").strip("/")
    if not x or x.startswith("../") or "/../" in x or x == "..":
        raise ValueError("invalid relative witness path")
    return x


def extract_written_file_blocks(snapshot_text: str) -> dict[str, bytes]:
    rows: dict[str, bytes] = {}
    for match in _FILE_BLOCK.finditer(snapshot_text):
        path = _normalize_path(match.group("path"))
        if path in rows:
            raise ValueError("duplicate snapshot file block")
        rows[path] = _canonical_json_bytes(match.group("body"))
    if not rows:
        raise ValueError("no JSON file blocks found")
    return dict(sorted(rows.items()))


def extract_dry_run_proposed_outputs(snapshot_text: str) -> dict[str, bytes]:
    rows: dict[str, bytes] = {}
    for match in _DRY_RUN_BLOCK.finditer(snapshot_text):
        path = _normalize_path(match.group("path"))
        plus = _PLUS_LINE.findall(match.group("body"))
        if not plus:
            continue
        if len(plus) != 1:
            raise ValueError("dry-run block must contain exactly one proposed JSON line")
        if path in rows:
            raise ValueError("duplicate dry-run output path")
        # Biome snapshot redaction renders spaces in one-line diffs as middle dots.
        rendered = plus[0].replace("·", " ")
        rows[path] = _canonical_json_bytes(rendered)
    if not rows:
        raise ValueError("no dry-run proposed outputs found")
    return dict(sorted(rows.items()))


def extract_cutoff_files(snapshot_text: str, mode: str) -> dict[str, bytes]:
    if type(snapshot_text) is not str or type(mode) is not str:
        raise TypeError("snapshot_text and mode must be strings")
    if mode == WRITTEN_FILE_BLOCKS:
        return extract_written_file_blocks(snapshot_text)
    if mode == DRY_RUN_PROPOSED_OUTPUTS:
        return extract_dry_run_proposed_outputs(snapshot_text)
    raise ValueError("unknown witness extraction mode")


def canonical_filesystem_digest(files: Mapping[str, bytes]) -> str:
    import hashlib
    payload = []
    for path in sorted(files):
        if type(path) is not str or type(files[path]) is not bytes:
            raise TypeError("filesystem must map str paths to bytes")
        payload.append([path, files[path].decode("utf-8")])
    data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()
