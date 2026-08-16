#!/usr/bin/env python3
import hashlib, importlib.util, json, py_compile
from pathlib import Path

BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/"source"

spec=importlib.util.spec_from_file_location("k1_compiler",BASE/"compiler.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
signature=json.loads((SOURCE/"signature.json").read_text())
rules=json.loads((SOURCE/"rewrite_rules.json").read_text())
stored=json.loads((BASE/"IR.json").read_text())
rebuilt=mod.compile_contract(signature,rules)
assert rebuilt==stored
canon=hashlib.sha256(json.dumps(stored,sort_keys=True,separators=(",",":")).encode()).hexdigest()
assert canon=="3dedd77353adc2d0daf80f5aeaf64a20663c6a44479ff9f5771573dd129cb707"
compiler_text=(BASE/"compiler.py").read_text()
assert "gold/GOLD" not in compiler_text and "TASKS.json" not in compiler_text
py_compile.compile(str(BASE/"ir_evaluator.py"),doraise=True)
mut=json.loads((BASE/"mutations.json").read_text())
assert len(mut["mutations"])==6
print(json.dumps({
  "object":"K1-CROSS-REGIME-COMPILER-TRANSFER/COMPILER_FREEZE_VERIFY",
  "ir_canonical_sha256":canon,
  "hostile_mutation_count":6,
  "source_gold_read":False,
  "tasks_executed":False,
  "audit_executed":False,
  "K0_STLC_modified":False,
  "R2_source_modified":False
},indent=2,sort_keys=True))
