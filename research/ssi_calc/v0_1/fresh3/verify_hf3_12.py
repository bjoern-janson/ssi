#!/usr/bin/env python3
"""Verify HF3-12 freeze integrity without importing SSI-CALC."""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAIN_SHA = "0747244689af2caca39c4f692e4c0eccf7ce39cda386c5855620bb8ce286ae33"
GZIP_SHA = "3be543c9b303f9220687e0d933ff0d9eb887ff2ddae7d8d089d9ae36a822ef76"
AUTHORIZED = {"AUTHORIZED", "AUTHORIZED_SCOPED"}

packed = base64.b64decode((HERE / "HF3_12.json.gz.b64").read_text().strip())
assert hashlib.sha256(packed).hexdigest() == GZIP_SHA
plain = gzip.decompress(packed)
assert hashlib.sha256(plain).hexdigest() == PLAIN_SHA
obj = json.loads(plain)
cases = obj["cases"]
assert len(cases) == 12
assert [c["id"] for c in cases] == [f"CASE-{n:03d}" for n in range(401, 413)]
licensed = sum(c["expected"]["status"] in AUTHORIZED for c in cases)
assert licensed == 6
assert len(cases) - licensed == 6
for c in cases:
    assert c["spec_version"] == "SSI-CALC-V0.1"
    assert set(c) >= {"id", "family", "objects", "facts", "authority_edges", "request", "expected"}

print(json.dumps({
    "object": obj["object"],
    "case_count": len(cases),
    "licensed": licensed,
    "non_authorized": len(cases) - licensed,
    "families": dict(Counter(c["family"] for c in cases)),
    "plain_sha256": hashlib.sha256(plain).hexdigest(),
    "gzip_sha256": hashlib.sha256(packed).hexdigest(),
    "successor_executed": False,
}, indent=2, sort_keys=True))
