#!/usr/bin/env python3
"""SSI Energy Suite — Lineage Corrective Economy V2.2.

Final V2.x routing experiment. Uses the frozen V2.1 executable substrate and
compares similarity-only routing with a preregistered gated q/c router.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

MASTER_SEED = 20260823
BOOTSTRAP_SEED = 20260824
N_BOOT = 20_000
N_WORLDS = 64
K = 96
GATE_THRESHOLD = 11.0 / 32.0
BASE_BLOB_SHA = "e3e609dae6dc604b460623462f7c1bca666f22d5"


def git_blob_sha(data: bytes) -> str:
    payload = f"blob {len(data)}\0".encode() + data
    return hashlib.sha1(payload).hexdigest()


def load_base():
    base_path = Path(__file__).resolve().parent.parent / "lineage_v2_1" / "run_experiment.py"
    data = base_path.read_bytes()
    observed = git_blob_sha(data)
    if observed != BASE_BLOB_SHA:
        raise RuntimeError(
            f"V2.2 substrate mismatch: expected {BASE_BLOB_SHA}, observed {observed}"
        )
    spec = importlib.util.spec_from_file_location("ssi_lineage_v21_frozen", base_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load frozen V2.1 substrate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, base_path, observed


base, BASE_PATH, OBSERVED_BASE_SHA = load_base()


def build_gated_order(signature, lineage, tie_rank, beta):
    cpu0 = time.process_time_ns()
    wall0 = time.perf_counter_ns()
    d = base.distances_to_lineage(signature, lineage)
    similarity_order = sorted(range(base.N_MECH), key=lambda i: (d[i], tie_rank[i]))
    dmin = float(np.min(d))
    invoked = dmin >= GATE_THRESHOLD
    if invoked:
        q = base.q_from_distances(d, beta)
        priority = q / base.FROZEN_COST_NS
        order = sorted(range(base.N_MECH), key=lambda i: (-priority[i], tie_rank[i]))
    else:
        order = similarity_order
    return (
        order,
        d,
        dmin,
        invoked,
        time.process_time_ns() - cpu0,
        time.perf_counter_ns() - wall0,
    )


def run_world(world_index, seed):
    rng = np.random.default_rng(seed)
    prototypes = rng.integers(0, 2, size=(base.N_MECH, base.BITS), dtype=np.int8)
    lineage_s = {m: [] for m in range(base.N_MECH)}
    lineage_g = {m: [] for m in range(base.N_MECH)}
    all_lineage = []
    for m in range(base.N_MECH):
        for _ in range(base.WARMUP_PER_MECH):
            sig = base.signature_from(prototypes[m], base.WARMUP_NOISE, rng)
            lineage_s[m].append(sig.copy())
            lineage_g[m].append(sig.copy())
            all_lineage.append(sig.copy())

    cal_cpu0 = time.process_time_ns()
    beta, calibration_ll = base.fit_beta(prototypes, lineage_g, rng)
    calibration_cpu_ns = time.process_time_ns() - cal_cpu0

    mechanism_order = np.repeat(np.arange(base.N_MECH), K // base.N_MECH)
    rng.shuffle(mechanism_order)
    noise_order = base.NOISE_LEVELS.copy()
    rng.shuffle(noise_order)

    episodes = []
    candidates = []
    for ez in range(K):
        episode = ez + 1
        true_m = int(mechanism_order[ez])
        noise_p = float(noise_order[ez])
        signature = base.nonidentical_signature(
            prototypes[true_m], noise_p, rng, all_lineage
        )
        clean = rng.integers(0, 256, size=base.PAYLOAD_LEN, dtype=np.uint8)
        corrupted = base.corrupt(clean, true_m)
        if not np.array_equal(base.repair(corrupted, true_m), clean):
            raise RuntimeError(f"true repair not exact mechanism={true_m}")

        tie_seed = MASTER_SEED * 10_000_000 + world_index * 10_000 + ez
        tie_rng = np.random.default_rng(tie_seed + 101)
        tie_perm = list(map(int, tie_rng.permutation(base.N_MECH)))
        tie_rank = {m: r for r, m in enumerate(tie_perm)}

        order_s, d_s, route_cpu_s, route_wall_s = base.build_similarity_order(
            signature, lineage_s, tie_rank
        )
        (
            order_g,
            d_g,
            dmin,
            gate_invoked,
            route_cpu_g,
            route_wall_g,
        ) = build_gated_order(signature, lineage_g, tie_rank, beta)

        if not np.allclose(d_s, d_g):
            raise RuntimeError("lineage distances diverged")

        if episode % 2 == 1:
            g, grows = base.run_arm(
                "G", corrupted, clean, true_m, order_g, lineage_g, signature
            )
            s, srows = base.run_arm(
                "S", corrupted, clean, true_m, order_s, lineage_s, signature
            )
            execution_order = "G_then_S"
        else:
            s, srows = base.run_arm(
                "S", corrupted, clean, true_m, order_s, lineage_s, signature
            )
            g, grows = base.run_arm(
                "G", corrupted, clean, true_m, order_g, lineage_g, signature
            )
            execution_order = "S_then_G"

        all_lineage.append(signature.copy())

        total_cpu_g = route_cpu_g + g["eval_cpu_ns"] + g["update_cpu_ns"]
        total_cpu_s = route_cpu_s + s["eval_cpu_ns"] + s["update_cpu_ns"]
        total_wall_g = route_wall_g + g["eval_wall_ns"] + g["update_wall_ns"]
        total_wall_s = route_wall_s + s["eval_wall_ns"] + s["update_wall_ns"]

        row = {
            "world": world_index,
            "episode": episode,
            "noise_p": noise_p,
            "mechanism": true_m,
            "beta": beta,
            "execution_order": execution_order,
            "dmin": dmin,
            "gate_invoked": int(gate_invoked),
            "n_tested_G": g["n_tested"],
            "n_tested_S": s["n_tested"],
            "delta_n_G_minus_S": g["n_tested"] - s["n_tested"],
            "route_cpu_G_ns": route_cpu_g,
            "route_cpu_S_ns": route_cpu_s,
            "delta_route_cpu_G_minus_S_ns": route_cpu_g - route_cpu_s,
            "eval_cpu_G_ns": g["eval_cpu_ns"],
            "eval_cpu_S_ns": s["eval_cpu_ns"],
            "delta_eval_cpu_G_minus_S_ns": g["eval_cpu_ns"] - s["eval_cpu_ns"],
            "update_cpu_G_ns": g["update_cpu_ns"],
            "update_cpu_S_ns": s["update_cpu_ns"],
            "total_cpu_G_ns": total_cpu_g,
            "total_cpu_S_ns": total_cpu_s,
            "delta_total_cpu_G_minus_S_ns": total_cpu_g - total_cpu_s,
            "total_wall_G_ns": total_wall_g,
            "total_wall_S_ns": total_wall_s,
            "delta_total_wall_G_minus_S_ns": total_wall_g - total_wall_s,
            "gate_open_but_costlier": int(gate_invoked and total_cpu_g > total_cpu_s),
            "quality_pass": True,
        }
        episodes.append(row)

        for rr in grows:
            rr.update(
                {
                    "world": world_index,
                    "episode": episode,
                    "noise_p": noise_p,
                    "true_mechanism": true_m,
                    "gate_invoked": int(gate_invoked),
                }
            )
            candidates.append(rr)
        for rr in srows:
            rr.update(
                {
                    "world": world_index,
                    "episode": episode,
                    "noise_p": noise_p,
                    "true_mechanism": true_m,
                    "gate_invoked": int(gate_invoked),
                }
            )
            candidates.append(rr)

    def mean(key):
        return float(np.mean([r[key] for r in episodes]))

    world = {
        "world": world_index,
        "beta": beta,
        "calibration_logloss": calibration_ll,
        "calibration_cpu_ns": calibration_cpu_ns,
        "gate_invocation_fraction": mean("gate_invoked"),
        "mean_delta_n": mean("delta_n_G_minus_S"),
        "mean_delta_route_cpu_ns": mean("delta_route_cpu_G_minus_S_ns"),
        "mean_delta_eval_cpu_ns": mean("delta_eval_cpu_G_minus_S_ns"),
        "mean_delta_total_cpu_ns": mean("delta_total_cpu_G_minus_S_ns"),
        "mean_delta_total_wall_ns": mean("delta_total_wall_G_minus_S_ns"),
        "quality_pass": True,
    }
    return episodes, candidates, world


def ci(values, indices):
    boot = values[indices].mean(axis=1)
    return [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    out = Path(__file__).resolve().parent / "outputs"
    out.mkdir(parents=True, exist_ok=True)

    seeds = np.random.SeedSequence(MASTER_SEED).spawn(N_WORLDS)
    episodes = []
    candidates = []
    worlds = []
    run_cpu0 = time.process_time_ns()
    run_wall0 = time.perf_counter_ns()
    for wi, seed in enumerate(seeds):
        er, cr, wr = run_world(wi, seed)
        episodes.extend(er)
        candidates.extend(cr)
        worlds.append(wr)
    run_cpu = time.process_time_ns() - run_cpu0
    run_wall = time.perf_counter_ns() - run_wall0

    if len(worlds) < 60:
        raise RuntimeError("V2.2 NOT_IDENTIFIED: fewer than 60 worlds")

    write_csv(out / "episode_results.csv", episodes)
    write_csv(out / "candidate_results.csv", candidates)
    write_csv(out / "world_results.csv", worlds)

    boot_rng = np.random.default_rng(BOOTSTRAP_SEED)
    idx = boot_rng.integers(0, N_WORLDS, size=(N_BOOT, N_WORLDS))
    w_dn = np.array([w["mean_delta_n"] for w in worlds], dtype=float)
    w_dr = np.array([w["mean_delta_route_cpu_ns"] for w in worlds], dtype=float)
    w_de = np.array([w["mean_delta_eval_cpu_ns"] for w in worlds], dtype=float)
    w_dt = np.array([w["mean_delta_total_cpu_ns"] for w in worlds], dtype=float)
    w_dw = np.array([w["mean_delta_total_wall_ns"] for w in worlds], dtype=float)

    dn_ci = ci(w_dn, idx)
    dr_ci = ci(w_dr, idx)
    de_ci = ci(w_de, idx)
    dt_ci = ci(w_dt, idx)
    dw_ci = ci(w_dw, idx)

    quality = all(bool(w["quality_pass"]) for w in worlds)
    evidence = {
        "net_gated_executable_economy": dt_ci[1] < 0,
        "quality_admissible": quality,
    }
    evidence["v2_2_supported"] = all(evidence.values())

    tiers = []
    for p in (0.15, 0.25, 0.35):
        rr = [r for r in episodes if r["noise_p"] == p]
        tiers.append(
            {
                "noise_p": p,
                "episodes": len(rr),
                "gate_invocation_fraction": float(np.mean([r["gate_invoked"] for r in rr])),
                "mean_dmin": float(np.mean([r["dmin"] for r in rr])),
                "mean_delta_n_G_minus_S": float(np.mean([r["delta_n_G_minus_S"] for r in rr])),
                "mean_delta_route_cpu_G_minus_S_ns": float(np.mean([r["delta_route_cpu_G_minus_S_ns"] for r in rr])),
                "mean_delta_eval_cpu_G_minus_S_ns": float(np.mean([r["delta_eval_cpu_G_minus_S_ns"] for r in rr])),
                "mean_delta_total_cpu_G_minus_S_ns": float(np.mean([r["delta_total_cpu_G_minus_S_ns"] for r in rr])),
                "fraction_G_total_cpu_cheaper": float(np.mean([r["delta_total_cpu_G_minus_S_ns"] < 0 for r in rr])),
                "fraction_gate_open_but_costlier": float(np.mean([r["gate_open_but_costlier"] for r in rr])),
            }
        )

    invoked = [r for r in episodes if r["gate_invoked"]]
    closed = [r for r in episodes if not r["gate_invoked"]]

    summary = {
        "status": (
            "SUPPORTED_IN_FROZEN_GATED_ROUTING_SCOPE"
            if evidence["v2_2_supported"]
            else "NOT_SUPPORTED_IN_FROZEN_GATED_ROUTING_SCOPE"
        ),
        "scope": "Fresh synthetic heterogeneous executable repair worlds; similarity-only vs preregistered nearest-lineage-distance gated q/c routing; process CPU primary; final V2.x routing experiment; not physical energy.",
        "base_v2_1_blob_sha": OBSERVED_BASE_SHA,
        "gate_threshold_dmin": GATE_THRESHOLD,
        "worlds": N_WORLDS,
        "episodes_per_world": K,
        "total_paired_episodes": N_WORLDS * K,
        "gate_invocations": len(invoked),
        "gate_invocation_fraction": float(np.mean([r["gate_invoked"] for r in episodes])),
        "mean_n_tested_G": float(np.mean([r["n_tested_G"] for r in episodes])),
        "mean_n_tested_S": float(np.mean([r["n_tested_S"] for r in episodes])),
        "mean_delta_n_G_minus_S": float(np.mean(w_dn)),
        "mean_delta_n_95pct_CI": dn_ci,
        "mean_route_cpu_G_ns": float(np.mean([r["route_cpu_G_ns"] for r in episodes])),
        "mean_route_cpu_S_ns": float(np.mean([r["route_cpu_S_ns"] for r in episodes])),
        "mean_delta_route_cpu_G_minus_S_ns": float(np.mean(w_dr)),
        "mean_delta_route_cpu_95pct_CI_ns": dr_ci,
        "mean_eval_cpu_G_ns": float(np.mean([r["eval_cpu_G_ns"] for r in episodes])),
        "mean_eval_cpu_S_ns": float(np.mean([r["eval_cpu_S_ns"] for r in episodes])),
        "mean_delta_eval_cpu_G_minus_S_ns": float(np.mean(w_de)),
        "mean_delta_eval_cpu_95pct_CI_ns": de_ci,
        "mean_total_cpu_G_ns": float(np.mean([r["total_cpu_G_ns"] for r in episodes])),
        "mean_total_cpu_S_ns": float(np.mean([r["total_cpu_S_ns"] for r in episodes])),
        "mean_delta_total_cpu_G_minus_S_ns": float(np.mean(w_dt)),
        "mean_delta_total_cpu_95pct_CI_ns": dt_ci,
        "mean_delta_total_wall_G_minus_S_ns": float(np.mean(w_dw)),
        "mean_delta_total_wall_95pct_CI_ns": dw_ci,
        "fraction_G_total_cpu_cheaper": float(np.mean([r["delta_total_cpu_G_minus_S_ns"] < 0 for r in episodes])),
        "fraction_gate_open_but_costlier_overall": float(np.mean([r["gate_open_but_costlier"] for r in episodes])),
        "invoked_only_mean_delta_total_cpu_ns": float(np.mean([r["delta_total_cpu_G_minus_S_ns"] for r in invoked])) if invoked else None,
        "invoked_only_fraction_G_cheaper": float(np.mean([r["delta_total_cpu_G_minus_S_ns"] < 0 for r in invoked])) if invoked else None,
        "closed_only_mean_delta_total_cpu_ns": float(np.mean([r["delta_total_cpu_G_minus_S_ns"] for r in closed])) if closed else None,
        "mean_beta_calibration_cpu_ns_per_world": float(np.mean([w["calibration_cpu_ns"] for w in worlds])),
        "mean_beta_calibration_cpu_amortized_ns_per_episode": float(np.mean([w["calibration_cpu_ns"] / K for w in worlds])),
        "quality_contract_all_worlds": quality,
        "evidence_ladder": evidence,
        "transfer_tier_diagnostics": tiers,
        "routing_branch_status": "CLOSED_AFTER_V2_2_BY_PREREGISTRATION",
        "run_total_process_cpu_ns": run_cpu,
        "run_total_wall_ns": run_wall,
        "environment": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "not_measured": {
            "physical_energy_joules": "NOT_MEASURED",
            "gpu_time": "NOT_MEASURED",
            "llm_tokens": "NOT_APPLICABLE",
        },
    }
    with (out / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
