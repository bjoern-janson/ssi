#!/usr/bin/env python3
import hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "source"


def h(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def probe():
    spec = importlib.util.spec_from_file_location("r2_source_probe", SOURCE / "source_reference.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    tasks = json.loads((SOURCE / "TASKS.json").read_text())["cases"]
    gold = {x["id"]: x for x in json.loads((SOURCE / "gold/GOLD.json").read_text())["cases"]}
    rows = []
    for q in tasks:
        got = mod.adjudicate_keys(q["source"], q["target"])
        row = {
            "id": q["id"],
            "licensed": got["licensed"],
            "matches_frozen_judgment": got["licensed"] == gold[q["id"]]["licensed"],
        }
        if got["licensed"]:
            row["root"] = got["derivation"]["rule"]
            row["proof_sha256"] = h(got["derivation"])
        rows.append(row)
    print(json.dumps(rows, sort_keys=True))


def main():
    if "--probe" in sys.argv:
        probe(); return
    seeds = []
    for seed in range(16):
        env = dict(os.environ); env["PYTHONHASHSEED"] = str(seed)
        p = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--probe"], env=env, text=True, capture_output=True, check=True)
        rows = json.loads(p.stdout)
        judgment_vector = [(r["id"], r["licensed"]) for r in rows]
        proof_vector = [(r["id"], r.get("root"), r.get("proof_sha256")) for r in rows if r["licensed"]]
        seeds.append({
            "seed": seed,
            "all_judgments_match_frozen": all(r["matches_frozen_judgment"] for r in rows),
            "judgment_vector_sha256": h(judgment_vector),
            "proof_vector_sha256": h(proof_vector),
            "cases": rows,
        })
    case_variation = {}
    ids = [r["id"] for r in seeds[0]["cases"]]
    for cid in ids:
        entries = [next(r for r in s["cases"] if r["id"] == cid) for s in seeds]
        judgments = sorted({str(e["licensed"]) for e in entries})
        proofs = sorted({e.get("proof_sha256") for e in entries if e.get("proof_sha256")})
        roots = sorted({e.get("root") for e in entries if e.get("root")})
        if len(judgments) > 1 or len(proofs) > 1 or len(roots) > 1:
            case_variation[cid] = {"judgments": judgments, "roots": roots, "proof_sha256_count": len(proofs), "proof_sha256_values": proofs}
    out = {
        "object": "K1-CROSS-REGIME-COMPILER-TRANSFER/SOURCE_JUDGMENT_VS_PROOF_REPRODUCIBILITY",
        "method": "independent Python processes with PYTHONHASHSEED=0..15",
        "all_seeds_match_frozen_judgments": all(s["all_judgments_match_frozen"] for s in seeds),
        "unique_judgment_vectors": len({s["judgment_vector_sha256"] for s in seeds}),
        "unique_proof_vectors": len({s["proof_vector_sha256"] for s in seeds}),
        "case_variation": case_variation,
        "source_modified": False,
        "compiler_modified": False,
        "ir_modified": False,
    }
    (HERE / "SOURCE_JUDGMENT_VS_PROOF_DIAGNOSTIC.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__": main()
