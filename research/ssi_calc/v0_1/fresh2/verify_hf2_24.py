#!/usr/bin/env python3
"""Verify HF2-24 packing, hashes, balance, and pre-exposure firewall only.

This script is stdlib-only and does not import or execute SSI-CALC.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAIN_SHA = "96498b2f195cdf6ca99e0c5f4efbf99305f2bc7168ff008eda3f6cca14c78218"
GZIP_SHA = "fa0e12c1e01d2465e2e1a1a1de48f2be95662ad3256f1868af2c2346838e8d64"
AUTHORIZED = {"AUTHORIZED", "AUTHORIZED_SCOPED"}

packed = base64.b64decode((HERE / "HF2_24.json.gz.b64").read_text().strip())
assert hashlib.sha256(packed).hexdigest() == GZIP_SHA
plain = gzip.decompress(packed)
assert hashlib.sha256(plain).hexdigest() == PLAIN_SHA
obj = json.loads(plain)
cases = obj["cases"]

assert len(cases) == 24
assert [c["id"] for c in cases] == [f"CASE-{i:03d}" for i in range(301, 325)]
counts = Counter(c["family"] for c in cases)
assert set(counts.values()) == {3}
assert len(counts) == 8
licensed = sum(c["expected"]["status"] in AUTHORIZED for c in cases)
assert licensed == 12
assert len(cases) - licensed == 12
assert all("expected" in c and "request" in c and "facts" in c for c in cases)

firewall = json.loads((HERE / "FIREWALL.json").read_text())
assert firewall["successor_executed_before_freeze"] is False

print(json.dumps({
    "object": obj["object"],
    "case_count": len(cases),
    "licensed": licensed,
    "non_authorized": len(cases) - licensed,
    "families": dict(sorted(counts.items())),
    "plain_sha256": PLAIN_SHA,
    "gzip_sha256": GZIP_SHA,
    "successor_executed": False
}, indent=2))
