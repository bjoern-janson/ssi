#!/usr/bin/env python3
"""Verify the frozen HF16 corpus without importing or executing SSI-CALC."""
from __future__ import annotations
import base64, gzip, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAIN_SHA256 = "0744abe38f6d32b32eace1862b571246d5bb256f47b76b4bf179b5c9404372a7"
GZIP_SHA256 = "683ee08e1f9d43f9dca7513157c17bdc170e2e77f1acc6cc93a255bda8974edd"
IDS = [f"CASE-{i:03d}" for i in range(201, 217)]
AUTHORIZED = {"AUTHORIZED", "AUTHORIZED_SCOPED"}

def main() -> None:
    packed = base64.b64decode((HERE / "HF16.json.gz.b64").read_text().strip())
    assert hashlib.sha256(packed).hexdigest() == GZIP_SHA256
    raw = gzip.decompress(packed)
    assert hashlib.sha256(raw).hexdigest() == PLAIN_SHA256
    bundle = json.loads(raw)
    cases = bundle["cases"]
    assert bundle["case_count"] == 16 == len(cases)
    assert [c["id"] for c in cases] == IDS
    assert len({c["id"] for c in cases}) == 16
    assert sum(c["expected"]["status"] in AUTHORIZED for c in cases) == 8
    assert sum(c["expected"]["status"] not in AUTHORIZED for c in cases) == 8
    for c in cases:
        assert c["spec_version"] == "SSI-CALC-V0.1"
        assert set(c) >= {"id", "family", "objects", "facts", "authority_edges", "request", "expected"}
        assert set(c["expected"]) >= {"status", "failure_locus", "preserved_facts", "missing_authority", "reopened", "explanation"}
        assert c["expected"]["preserved_facts"] == [f["id"] for f in c["facts"]]
    print(json.dumps({
        "object": bundle["object"],
        "case_count": len(cases),
        "licensed": 8,
        "non_authorized": 8,
        "plain_sha256": PLAIN_SHA256,
        "gzip_sha256": GZIP_SHA256,
        "successor_executed": False
    }, indent=2))

if __name__ == "__main__":
    main()
