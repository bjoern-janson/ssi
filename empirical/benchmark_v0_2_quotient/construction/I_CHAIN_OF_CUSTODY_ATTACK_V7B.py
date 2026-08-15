#!/usr/bin/env python3
"""Fixture-only repair wrapper for I_CHAIN_OF_CUSTODY_ATTACK_V7.py.

The first CI attempt failed before runner invocation because the audit fixture
looked for a nonexistent top-level `source_fact_ids`. The frozen domain instead
encodes the six facts in its three grounding-unit rows. This wrapper verifies the
original attack blob, applies exactly that one source-level fixture correction in
memory, and executes the otherwise unchanged attack. Packet 7 is untouched.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "I_CHAIN_OF_CUSTODY_ATTACK_V7.py"
EXPECTED_SOURCE_BLOB = "14b1ff16e65f2f1cc0038679d664c63b0a67bc18"
OLD = 'facts = list(domain["source_fact_ids"])'
NEW = 'facts = sorted({f for u in domain["grounding_units"] for f in (u["left_fact_id"], u["right_fact_id"])})'


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def main() -> None:
    data = SOURCE.read_bytes()
    if git_blob(data) != EXPECTED_SOURCE_BLOB:
        raise RuntimeError("original I attack blob drift")
    text = data.decode("utf-8")
    if text.count(OLD) != 1:
        raise RuntimeError("fixture correction target drift")
    corrected = text.replace(OLD, NEW)
    code = compile(corrected, str(SOURCE) + "[fixture-corrected]", "exec")
    ns = {"__name__": "__main__", "__file__": str(SOURCE)}
    exec(code, ns, ns)


if __name__ == "__main__":
    main()
