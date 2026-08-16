#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFY = HERE.parent / "source" / "verify_source_freeze.py"

rows = []
for seed in range(16):
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = str(seed)
    p = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=str(VERIFY.parent),
        env=env,
        text=True,
        capture_output=True,
    )
    tail = (p.stderr.strip().splitlines() or p.stdout.strip().splitlines() or [""])[-1]
    rows.append({"seed": seed, "pass": p.returncode == 0, "returncode": p.returncode, "tail": tail})

out = {
    "object": "K1-CROSS-REGIME-COMPILER-TRANSFER/SOURCE_PROOF_REPRODUCIBILITY_DIAGNOSTIC",
    "method": "run unchanged frozen source verifier in independent Python processes with PYTHONHASHSEED=0..15",
    "seeds": rows,
    "pass_count": sum(r["pass"] for r in rows),
    "fail_count": sum(not r["pass"] for r in rows),
    "source_modified": False,
    "compiler_modified": False,
    "ir_modified": False,
}
(HERE / "SOURCE_PROOF_REPRO_DIAGNOSTIC.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps(out, indent=2, sort_keys=True))
