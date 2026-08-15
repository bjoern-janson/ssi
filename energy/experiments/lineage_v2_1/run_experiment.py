#!/usr/bin/env python3
"""SSI Energy Suite — Lineage Corrective Economy V2.1.

Frozen protocol: PREREGISTRATION.md in this directory.
Compares similarity-only lineage routing with q/c cost-aware lineage routing.
"""
from __future__ import annotations

import csv
import json
import math
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

MASTER_SEED = 20260821
BOOTSTRAP_SEED = 20260822
N_BOOT = 20_000
N_WORLDS = 64
N_MECH = 12
BITS = 32
WARMUP_PER_MECH = 2
WARMUP_NOISE = 0.10
K = 96
PAYLOAD_LEN = 16_384
NOISE_LEVELS = np.array([0.15] * 48 + [0.25] * 32 + [0.35] * 16, dtype=float)
BETA_GRID = np.array([0, 1, 2, 4, 8, 12, 16, 24, 32, 48, 64], dtype=float)
CAL_NOISE = (0.15, 0.15, 0.25, 0.25, 0.35, 0.35)

FROZEN_COST_NS = np.array(
    [8452.0, 12609.0, 5128.0, 9023.0, 12499.0, 12449.0,
     34941.0, 15943.5, 22007.5, 45988.0, 57225.0, 43765.0],
    dtype=float,
)

PIPELINES: dict[int, tuple[str, ...]] = {
    0: ("reverse",),
    1: ("roll_113",),
    2: ("xor_a5",),
    3: ("add_17_mod256",),
    4: ("rotl3",),
    5: ("nibble_swap",),
    6: ("pair_swap", "xor_a5"),
    7: ("block_reverse_64", "add_17_mod256"),
    8: ("matrix_transpose_128", "roll_113", "xor_a5"),
    9: ("affine_5x_plus_7_mod256", "pair_swap", "reverse"),
    10: ("prefix_xor", "nibble_swap", "roll_113"),
    11: ("delta_mod256", "matrix_transpose_128", "block_reverse_64", "xor_a5"),
}


def signature_from(prototype: np.ndarray, p: float, rng: np.random.Generator) -> np.ndarray:
    flips = (rng.random(prototype.shape[0]) < p).astype(np.int8)
    return np.bitwise_xor(prototype, flips)


def nonidentical_signature(prototype, p, rng, existing):
    for _ in range(1000):
        s = signature_from(prototype, p, rng)
        if not any(np.array_equal(s, prior) for prior in existing):
            return s
    raise RuntimeError("Failed to generate non-identical held-out signature")


def normalized_hamming(a, b) -> float:
    return float(np.count_nonzero(a != b)) / float(a.size)


def distances_to_lineage(signature, lineage) -> np.ndarray:
    return np.array([
        min(normalized_hamming(signature, prior) for prior in lineage[m])
        for m in range(N_MECH)
    ], dtype=float)


def q_from_distances(distances: np.ndarray, beta: float) -> np.ndarray:
    logits = -beta * distances
    logits -= np.max(logits)
    ex = np.exp(logits)
    return ex / np.sum(ex)


def fit_beta(prototypes, lineage, rng) -> tuple[float, float]:
    examples: list[tuple[np.ndarray, int]] = []
    for mechanism in range(N_MECH):
        for p in CAL_NOISE:
            s = signature_from(prototypes[mechanism], p, rng)
            examples.append((distances_to_lineage(s, lineage), mechanism))

    losses = []
    for beta in BETA_GRID:
        loss = 0.0
        for d, true_m in examples:
            q = q_from_distances(d, float(beta))
            loss += -math.log(max(float(q[true_m]), 1e-300))
        losses.append(loss / len(examples))
    best_idx = int(np.argmin(np.array(losses)))
    return float(BETA_GRID[best_idx]), float(losses[best_idx])


def u8_mod(values):
    return np.bitwise_and(values, 255).astype(np.uint8, copy=False)


def forward_primitive(x, name):
    if name == "reverse": return x[::-1].copy()
    if name == "roll_113": return np.roll(x, 113)
    if name == "xor_a5": return np.bitwise_xor(x, np.uint8(0xA5))
    if name == "add_17_mod256": return u8_mod(x.astype(np.uint16) + 17)
    if name == "rotl3":
        u = x.astype(np.uint16); return u8_mod((u << 3) | (u >> 5))
    if name == "nibble_swap":
        u = x.astype(np.uint16); return u8_mod((u << 4) | (u >> 4))
    if name == "pair_swap": return x.reshape(-1, 2)[:, ::-1].reshape(-1).copy()
    if name == "block_reverse_64": return x.reshape(-1, 64)[:, ::-1].reshape(-1).copy()
    if name == "matrix_transpose_128": return x.reshape(128, 128).T.reshape(-1).copy()
    if name == "affine_5x_plus_7_mod256": return u8_mod(5 * x.astype(np.uint16) + 7)
    if name == "prefix_xor":
        out = np.empty_like(x); out[0] = x[0]; out[1:] = np.bitwise_xor(x[1:], x[:-1]); return out
    if name == "delta_mod256":
        out = np.empty_like(x); out[0] = x[0]; out[1:] = u8_mod(x[1:].astype(np.int16) - x[:-1].astype(np.int16)); return out
    raise ValueError(name)


def inverse_primitive(x, name):
    if name == "reverse": return x[::-1].copy()
    if name == "roll_113": return np.roll(x, -113)
    if name == "xor_a5": return np.bitwise_xor(x, np.uint8(0xA5))
    if name == "add_17_mod256": return u8_mod(x.astype(np.int16) - 17)
    if name == "rotl3":
        u = x.astype(np.uint16); return u8_mod((u >> 3) | (u << 5))
    if name == "nibble_swap":
        u = x.astype(np.uint16); return u8_mod((u << 4) | (u >> 4))
    if name == "pair_swap": return x.reshape(-1, 2)[:, ::-1].reshape(-1).copy()
    if name == "block_reverse_64": return x.reshape(-1, 64)[:, ::-1].reshape(-1).copy()
    if name == "matrix_transpose_128": return x.reshape(128, 128).T.reshape(-1).copy()
    if name == "affine_5x_plus_7_mod256": return u8_mod((x.astype(np.int16) - 7) * 205)
    if name == "prefix_xor": return np.bitwise_xor.accumulate(x).astype(np.uint8, copy=False)
    if name == "delta_mod256": return u8_mod(np.cumsum(x, dtype=np.uint64))
    raise ValueError(name)


def corrupt(clean, mechanism):
    out = clean
    for primitive in PIPELINES[mechanism]: out = forward_primitive(out, primitive)
    return out


def repair(corrupted, mechanism):
    out = corrupted
    for primitive in reversed(PIPELINES[mechanism]): out = inverse_primitive(out, primitive)
    return out


def build_similarity_order(signature, lineage, tie_rank):
    cpu0 = time.process_time_ns(); wall0 = time.perf_counter_ns()
    d = distances_to_lineage(signature, lineage)
    order = sorted(range(N_MECH), key=lambda i: (d[i], tie_rank[i]))
    return order, d, time.process_time_ns()-cpu0, time.perf_counter_ns()-wall0


def build_costaware_order(signature, lineage, tie_rank, beta):
    cpu0 = time.process_time_ns(); wall0 = time.perf_counter_ns()
    d = distances_to_lineage(signature, lineage)
    q = q_from_distances(d, beta)
    priority = q / FROZEN_COST_NS
    order = sorted(range(N_MECH), key=lambda i: (-priority[i], tie_rank[i]))
    return order, d, q, time.process_time_ns()-cpu0, time.perf_counter_ns()-wall0


def evaluate_candidate(corrupted, clean, candidate):
    cpu0 = time.process_time_ns(); wall0 = time.perf_counter_ns()
    candidate_output = repair(corrupted, candidate)
    valid = bool(np.array_equal(candidate_output, clean))
    return valid, time.process_time_ns()-cpu0, time.perf_counter_ns()-wall0


def run_arm(arm, corrupted, clean, true_mechanism, order, lineage, signature):
    eval_cpu = eval_wall = 0
    n = 0
    candidate_rows = []
    found = None
    for candidate in order:
        valid, cpu, wall = evaluate_candidate(corrupted, clean, candidate)
        n += 1; eval_cpu += cpu; eval_wall += wall
        candidate_rows.append({
            "arm": arm, "candidate": int(candidate), "position": n,
            "candidate_cpu_ns": int(cpu), "candidate_wall_ns": int(wall),
            "valid": int(valid), "candidate_depth": len(PIPELINES[candidate]),
        })
        if valid:
            found = int(candidate); break
    if found != true_mechanism:
        raise RuntimeError(f"validator mismatch arm={arm} expected={true_mechanism} got={found}")
    cpu0 = time.process_time_ns(); wall0 = time.perf_counter_ns()
    lineage[true_mechanism].append(signature.copy())
    update_cpu = time.process_time_ns()-cpu0; update_wall = time.perf_counter_ns()-wall0
    return {
        "n_tested": n, "eval_cpu_ns": eval_cpu, "eval_wall_ns": eval_wall,
        "update_cpu_ns": update_cpu, "update_wall_ns": update_wall,
    }, candidate_rows


def run_world(world_index, seed):
    rng = np.random.default_rng(seed)
    prototypes = rng.integers(0, 2, size=(N_MECH, BITS), dtype=np.int8)
    lineage_s = {m: [] for m in range(N_MECH)}
    lineage_c = {m: [] for m in range(N_MECH)}
    all_lineage = []
    for m in range(N_MECH):
        for _ in range(WARMUP_PER_MECH):
            sig = signature_from(prototypes[m], WARMUP_NOISE, rng)
            lineage_s[m].append(sig.copy()); lineage_c[m].append(sig.copy()); all_lineage.append(sig.copy())

    beta, calibration_ll = fit_beta(prototypes, lineage_c, rng)

    mechanism_order = np.repeat(np.arange(N_MECH), K // N_MECH); rng.shuffle(mechanism_order)
    noise_order = NOISE_LEVELS.copy(); rng.shuffle(noise_order)

    episodes = []; candidates = []
    for ez in range(K):
        episode = ez + 1
        true_m = int(mechanism_order[ez]); noise_p = float(noise_order[ez])
        signature = nonidentical_signature(prototypes[true_m], noise_p, rng, all_lineage)
        clean = rng.integers(0, 256, size=PAYLOAD_LEN, dtype=np.uint8)
        corrupted = corrupt(clean, true_m)
        if not np.array_equal(repair(corrupted, true_m), clean):
            raise RuntimeError(f"true repair not exact mechanism={true_m}")

        base_seed = MASTER_SEED * 10_000_000 + world_index * 10_000 + ez
        tie_rng = np.random.default_rng(base_seed + 101)
        tie_perm = list(map(int, tie_rng.permutation(N_MECH)))
        tie_rank = {m: r for r, m in enumerate(tie_perm)}

        order_s, d_s, route_cpu_s, route_wall_s = build_similarity_order(signature, lineage_s, tie_rank)
        order_c, d_c, q_c, route_cpu_c, route_wall_c = build_costaware_order(signature, lineage_c, tie_rank, beta)
        if not np.allclose(d_s, d_c): raise RuntimeError("lineage distances diverged")

        if episode % 2 == 1:
            c, crows = run_arm("C", corrupted, clean, true_m, order_c, lineage_c, signature)
            s, srows = run_arm("S", corrupted, clean, true_m, order_s, lineage_s, signature)
            execution_order = "C_then_S"
        else:
            s, srows = run_arm("S", corrupted, clean, true_m, order_s, lineage_s, signature)
            c, crows = run_arm("C", corrupted, clean, true_m, order_c, lineage_c, signature)
            execution_order = "S_then_C"

        all_lineage.append(signature.copy())
        total_cpu_s = route_cpu_s + s["eval_cpu_ns"] + s["update_cpu_ns"]
        total_cpu_c = route_cpu_c + c["eval_cpu_ns"] + c["update_cpu_ns"]
        total_wall_s = route_wall_s + s["eval_wall_ns"] + s["update_wall_ns"]
        total_wall_c = route_wall_c + c["eval_wall_ns"] + c["update_wall_ns"]

        q_true = float(q_c[true_m])
        row = {
            "world": world_index, "episode": episode, "noise_p": noise_p, "mechanism": true_m,
            "beta": beta, "execution_order": execution_order, "q_true": q_true,
            "proposal_logloss": -math.log(max(q_true, 1e-300)),
            "n_tested_C": c["n_tested"], "n_tested_S": s["n_tested"], "delta_n_C_minus_S": c["n_tested"]-s["n_tested"],
            "route_cpu_C_ns": route_cpu_c, "route_cpu_S_ns": route_cpu_s,
            "eval_cpu_C_ns": c["eval_cpu_ns"], "eval_cpu_S_ns": s["eval_cpu_ns"], "delta_eval_cpu_C_minus_S_ns": c["eval_cpu_ns"]-s["eval_cpu_ns"],
            "update_cpu_C_ns": c["update_cpu_ns"], "update_cpu_S_ns": s["update_cpu_ns"],
            "total_cpu_C_ns": total_cpu_c, "total_cpu_S_ns": total_cpu_s, "delta_total_cpu_C_minus_S_ns": total_cpu_c-total_cpu_s,
            "total_wall_C_ns": total_wall_c, "total_wall_S_ns": total_wall_s, "delta_total_wall_C_minus_S_ns": total_wall_c-total_wall_s,
            "quality_pass": True,
            "more_candidates_but_cheaper": int(c["n_tested"] > s["n_tested"] and total_cpu_c < total_cpu_s),
            "fewer_candidates_but_costlier": int(c["n_tested"] < s["n_tested"] and total_cpu_c > total_cpu_s),
        }
        episodes.append(row)
        for rr in crows:
            rr.update({"world": world_index, "episode": episode, "noise_p": noise_p, "true_mechanism": true_m})
            candidates.append(rr)
        for rr in srows:
            rr.update({"world": world_index, "episode": episode, "noise_p": noise_p, "true_mechanism": true_m})
            candidates.append(rr)

    def mean(key): return float(np.mean([r[key] for r in episodes]))
    world = {
        "world": world_index, "beta": beta, "calibration_logloss": calibration_ll,
        "heldout_proposal_logloss": mean("proposal_logloss"),
        "mean_delta_n": mean("delta_n_C_minus_S"),
        "mean_delta_eval_cpu_ns": mean("delta_eval_cpu_C_minus_S_ns"),
        "mean_delta_total_cpu_ns": mean("delta_total_cpu_C_minus_S_ns"),
        "mean_delta_total_wall_ns": mean("delta_total_wall_C_minus_S_ns"),
        "quality_pass": True,
    }
    return episodes, candidates, world


def ci(values, indices):
    boot = values[indices].mean(axis=1)
    return [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]


def rankdata(values):
    order = np.argsort(values)
    ranks = np.empty(len(values), dtype=float)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and values[order[j]] == values[order[i]]: j += 1
        avg = (i + j - 1) / 2.0 + 1.0
        for k in range(i, j): ranks[order[k]] = avg
        i = j
    return ranks


def spearman(a, b):
    ra = rankdata(np.asarray(a, dtype=float)); rb = rankdata(np.asarray(b, dtype=float))
    return float(np.corrcoef(ra, rb)[0, 1])


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)


def main():
    out = Path(__file__).resolve().parent / "outputs"; out.mkdir(parents=True, exist_ok=True)
    seeds = np.random.SeedSequence(MASTER_SEED).spawn(N_WORLDS)
    episodes = []; candidates = []; worlds = []
    run_cpu0 = time.process_time_ns(); run_wall0 = time.perf_counter_ns()
    for wi, seed in enumerate(seeds):
        er, cr, wr = run_world(wi, seed); episodes.extend(er); candidates.extend(cr); worlds.append(wr)
    run_cpu = time.process_time_ns()-run_cpu0; run_wall = time.perf_counter_ns()-run_wall0

    if len(worlds) < 60: raise RuntimeError("V2.1 NOT_IDENTIFIED: fewer than 60 worlds")

    write_csv(out / "episode_results.csv", episodes); write_csv(out / "candidate_results.csv", candidates); write_csv(out / "world_results.csv", worlds)

    current_costs = []
    for c in range(N_MECH):
        vals = [r["candidate_cpu_ns"] for r in candidates if r["arm"] == "S" and r["candidate"] == c]
        if not vals: raise RuntimeError(f"No S-arm timings for candidate {c}")
        current_costs.append(float(np.median(vals)))
    current_costs_arr = np.array(current_costs, dtype=float)
    rho = spearman(FROZEN_COST_NS, current_costs_arr)
    h_current = float(np.max(current_costs_arr) / np.min(current_costs_arr))

    boot_rng = np.random.default_rng(BOOTSTRAP_SEED)
    idx = boot_rng.integers(0, N_WORLDS, size=(N_BOOT, N_WORLDS))
    w_ll = np.array([w["heldout_proposal_logloss"] for w in worlds])
    w_dn = np.array([w["mean_delta_n"] for w in worlds])
    w_de = np.array([w["mean_delta_eval_cpu_ns"] for w in worlds])
    w_dt = np.array([w["mean_delta_total_cpu_ns"] for w in worlds])
    w_dw = np.array([w["mean_delta_total_wall_ns"] for w in worlds])

    ll_ci = ci(w_ll, idx); dn_ci = ci(w_dn, idx); de_ci = ci(w_de, idx); dt_ci = ci(w_dt, idx); dw_ci = ci(w_dw, idx)
    uniform_ll = math.log(N_MECH)
    evidence = {
        "proposal_quality": ll_ci[1] < uniform_ll,
        "cost_field_transfer": rho >= 0.80 and h_current >= 2.0,
        "heterogeneous_work_routing": de_ci[1] < 0,
        "net_executable_router_economy": dt_ci[1] < 0,
        "quality_admissible": all(bool(w["quality_pass"]) for w in worlds),
    }
    evidence["v2_1_supported"] = evidence["proposal_quality"] and evidence["cost_field_transfer"] and evidence["net_executable_router_economy"] and evidence["quality_admissible"]

    tiers = []
    for p in (0.15, 0.25, 0.35):
        rr = [r for r in episodes if r["noise_p"] == p]
        tiers.append({
            "noise_p": p, "episodes": len(rr),
            "mean_delta_n_C_minus_S": float(np.mean([r["delta_n_C_minus_S"] for r in rr])),
            "mean_delta_eval_cpu_C_minus_S_ns": float(np.mean([r["delta_eval_cpu_C_minus_S_ns"] for r in rr])),
            "mean_delta_total_cpu_C_minus_S_ns": float(np.mean([r["delta_total_cpu_C_minus_S_ns"] for r in rr])),
            "fraction_C_total_cpu_cheaper": float(np.mean([r["delta_total_cpu_C_minus_S_ns"] < 0 for r in rr])),
            "fraction_more_candidates_but_cheaper": float(np.mean([r["more_candidates_but_cheaper"] for r in rr])),
            "fraction_fewer_candidates_but_costlier": float(np.mean([r["fewer_candidates_but_costlier"] for r in rr])),
            "mean_proposal_logloss": float(np.mean([r["proposal_logloss"] for r in rr])),
        })

    summary = {
        "status": "SUPPORTED_IN_FROZEN_COST_AWARE_ROUTING_SCOPE" if evidence["v2_1_supported"] else (
            "NOT_IDENTIFIED_FOR_COST_FIELD_TRANSFER" if not evidence["cost_field_transfer"] else "NOT_SUPPORTED_IN_FROZEN_COST_AWARE_ROUTING_SCOPE"
        ),
        "scope": "Synthetic heterogeneous executable repair programs; similarity-only vs q/c cost-aware lineage routing; process CPU primary; not physical energy.",
        "worlds": N_WORLDS, "episodes_per_world": K, "total_paired_episodes": N_WORLDS*K,
        "uniform_logloss": uniform_ll,
        "mean_beta": float(np.mean([w["beta"] for w in worlds])),
        "median_beta": float(np.median([w["beta"] for w in worlds])),
        "beta_counts": {str(float(b)): int(sum(w["beta"] == float(b) for w in worlds)) for b in BETA_GRID},
        "mean_heldout_proposal_logloss": float(np.mean(w_ll)), "proposal_logloss_95pct_CI": ll_ci,
        "mean_n_tested_C": float(np.mean([r["n_tested_C"] for r in episodes])),
        "mean_n_tested_S": float(np.mean([r["n_tested_S"] for r in episodes])),
        "mean_delta_n_C_minus_S": float(np.mean(w_dn)), "mean_delta_n_95pct_CI": dn_ci,
        "mean_route_cpu_C_ns": float(np.mean([r["route_cpu_C_ns"] for r in episodes])),
        "mean_route_cpu_S_ns": float(np.mean([r["route_cpu_S_ns"] for r in episodes])),
        "mean_eval_cpu_C_ns": float(np.mean([r["eval_cpu_C_ns"] for r in episodes])),
        "mean_eval_cpu_S_ns": float(np.mean([r["eval_cpu_S_ns"] for r in episodes])),
        "mean_delta_eval_cpu_C_minus_S_ns": float(np.mean(w_de)), "mean_delta_eval_cpu_95pct_CI_ns": de_ci,
        "mean_total_cpu_C_ns": float(np.mean([r["total_cpu_C_ns"] for r in episodes])),
        "mean_total_cpu_S_ns": float(np.mean([r["total_cpu_S_ns"] for r in episodes])),
        "mean_delta_total_cpu_C_minus_S_ns": float(np.mean(w_dt)), "mean_delta_total_cpu_95pct_CI_ns": dt_ci,
        "mean_delta_total_wall_C_minus_S_ns": float(np.mean(w_dw)), "mean_delta_total_wall_95pct_CI_ns": dw_ci,
        "fraction_C_total_cpu_cheaper": float(np.mean([r["delta_total_cpu_C_minus_S_ns"] < 0 for r in episodes])),
        "fraction_more_candidates_but_cheaper": float(np.mean([r["more_candidates_but_cheaper"] for r in episodes])),
        "fraction_fewer_candidates_but_costlier": float(np.mean([r["fewer_candidates_but_costlier"] for r in episodes])),
        "frozen_v2_cost_ns": FROZEN_COST_NS.tolist(),
        "current_S_median_candidate_cost_ns": current_costs,
        "cost_field_spearman_rho": rho, "current_cost_heterogeneity_ratio": h_current,
        "quality_contract_all_worlds": evidence["quality_admissible"],
        "evidence_ladder": evidence,
        "transfer_tier_diagnostics": tiers,
        "run_total_process_cpu_ns": run_cpu, "run_total_wall_ns": run_wall,
        "environment": {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version, "numpy": np.__version__, "platform": platform.platform(), "machine": platform.machine()},
        "not_measured": {"physical_energy_joules": "NOT_MEASURED", "gpu_time": "NOT_MEASURED", "llm_tokens": "NOT_APPLICABLE"},
    }
    with (out / "summary.json").open("w", encoding="utf-8") as f: json.dump(summary, f, indent=2); f.write("\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
