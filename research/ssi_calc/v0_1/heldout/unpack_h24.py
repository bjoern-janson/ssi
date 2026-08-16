#!/usr/bin/env python3
"""Unpack and verify the frozen H24 held-out corpus without executing SSI-CALC."""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKED = HERE / "H24.json.gz.b64"
OUTPUT = HERE / "H24.json"
EXPECTED_SHA256 = "0910569fe786b29f5f1d64c295f8be7f2857ec6447bd2cf3286a336fc121b941"
EXPECTED_CASES = 24
EXPECTED_IDS = [f"CASE-{i:03d}" for i in range(101, 125)]


def main() -> None:
    packed_text = PACKED.read_text().strip()
    raw = gzip.decompress(base64.b64decode(packed_text))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"H24 SHA-256 mismatch: {digest}")

    obj = json.loads(raw)
    cases = obj.get("cases", [])
    ids = [case.get("id") for case in cases]
    if len(cases) != EXPECTED_CASES:
        raise SystemExit(f"H24 case-count mismatch: {len(cases)}")
    if ids != EXPECTED_IDS:
        raise SystemExit(f"H24 case-id sequence mismatch: {ids}")

    OUTPUT.write_bytes(raw)
    print(json.dumps({
        "status": "H24_UNPACK_VERIFIED",
        "sha256": digest,
        "case_count": len(cases),
        "output": str(OUTPUT),
        "checker_executed": False
    }, indent=2))


if __name__ == "__main__":
    main()
