#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
from source_reference import adjudicate_keys

BASE=Path(__file__).resolve().parent

def h(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()

tasks=json.loads((BASE/"TASKS.json").read_text())["cases"]
gold={x["id"]:x for x in json.loads((BASE/"gold/GOLD.json").read_text())["cases"]}
dists=json.loads((BASE/"distinctions.json").read_text())
assert len(tasks)==24 and len(gold)==24 and dists["count"]==8
positive=negative=0
for q in tasks:
    got=adjudicate_keys(q["source"],q["target"])
    exp=gold[q["id"]]
    assert got["licensed"]==exp["licensed"], q["id"]
    if got["licensed"]:
        positive += 1
        assert got["derivation"]["rule"]==exp["derivation_root"], q["id"]
        assert h(got["derivation"])==exp["derivation_sha256"], q["id"]
    else:
        negative += 1
        assert h(got["rejection"])==exp["rejection_sha256"], q["id"]
assert (positive,negative)==(12,12)
print(json.dumps({
  "object":"K1-CROSS-REGIME-COMPILER-TRANSFER/R2_SOURCE_FREEZE_VERIFY",
  "case_count":24,"positive":12,"negative":12,"distinction_count":8,
  "gold_recomputed_exact":True,"compiler_executed":False,
  "K0_STLC_modified":False
},indent=2,sort_keys=True))
