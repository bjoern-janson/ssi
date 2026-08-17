#!/usr/bin/env python3
"""Generate post-freeze blinded Stage-0 controlled-break exemplars.

The fresh seed is derived from the already-existing specification freeze commit,
so exact fresh cases do not exist until after assay constitution. Oracle labels
are emitted to a separate file and are never supplied to jurisdiction_assay.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from controlled_breaks import build_case, write_suite


def seed_from_freeze_sha(sha: str) -> int:
    if len(sha) < 12 or any(ch not in "0123456789abcdefABCDEF" for ch in sha):
        raise ValueError("freeze SHA must be hexadecimal")
    return int(hashlib.sha256(("SSI-JF-S0-FRESH:" + sha.lower()).encode()).hexdigest()[:16], 16)


def fresh_suite(freeze_sha: str) -> tuple[list[dict], list[dict]]:
    rng = random.Random(seed_from_freeze_sha(freeze_sha))
    # Balanced single-component cases plus intact controls and selected
    # interactions. Order is shuffled and IDs are opaque.
    break_sets = (
        [()] * 8
        + [("D",)] * 8
        + [("R",)] * 8
        + [("L",)] * 8
        + [("I",)] * 8
        + [("D", "R"), ("D", "L"), ("D", "I"), ("R", "L"),
           ("R", "I"), ("L", "I"), ("D", "R", "L"), ("R", "L", "I")]
    )
    break_sets = list(break_sets)
    rng.shuffle(break_sets)
    cases, key = [], []
    for idx, breaks in enumerate(break_sets):
        local_seed = rng.getrandbits(63)
        opaque = hashlib.sha256(f"{freeze_sha}:{idx}:{local_seed}".encode()).hexdigest()[:12]
        case, oracle = build_case(f"fresh_{opaque}", breaks, local_seed, "fresh")
        cases.append(case)
        key.append(oracle)
    return cases, key


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--freeze-sha", required=True)
    p.add_argument("--cases", required=True, type=Path)
    p.add_argument("--key", required=True, type=Path)
    args = p.parse_args()
    cases, key = fresh_suite(args.freeze_sha)
    write_suite(cases, key, args.cases, args.key)


if __name__ == "__main__":
    main()
