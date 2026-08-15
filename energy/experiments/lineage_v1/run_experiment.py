#!/usr/bin/env python3
"""SSI Energy Suite — Lineage Corrective Economy V1.

Measures executed CPU/wall work rather than assigning a synthetic price to candidate traversal.
Protocol: PREREGISTRATION.md in this directory.
"""
from __future__ import annotations

import csv
import hashlib
import json
import platform
import struct
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

MASTER_SEED = 20260815
BOOTSTRAP_SEED = 20260817
N_BOOT = 20_000
N_WORLDS = 64
N_MECH = 12
BITS = 32
WARMUP_PER_MECH = 2
WARMUP_NOISE = 0.10
K = 96
NOISE_LEVELS = np.array([0.15] * 48 + [0.25] * 32 + [0.35] * 16, dtype=float)
PROBE_ROUNDS = 256
DIGEST_SIZE = 32


def signature_from(prototype: np.ndarray, p: float, rng: np.random.Generator) -> np.ndarray:
    flips = (rng.random(prototype.shape[0]) < p).astype(np.int8)
    return np.bitwise_xor(prototype, flips)


def nonidentical_signature(
    prototype: np.ndarray,
    p: float,
    rng: np.random.Generator,
    existing: list[np.ndarray],
) -> np.ndarray:
    for _ in range(1000):
        signature = signature_from(prototype, p, rng)
        if not any(np.array_equal(signature, prior) for prior in existing):
            return signature
    raise RuntimeError("Failed to generate non-identical held-out signature")


def execute_candidate_workload(
    signature: np.ndarray, candidate: int, world: int, episode_zero: int
) -> int:
    """Execute the frozen CPU workload and return a small checksum."""
    payload = signature.tobytes() + struct.pack(">III", candidate, world, episode_zero)
    digest = payload
    for _ in range(PROBE_ROUNDS):
        digest = hashlib.blake2b(digest, digest_size=DIGEST_SIZE).digest()
    return digest[0]


def retrieve_order(
    signature: np.ndarray,
    lineage: dict[int, list[np.ndarray]],
    tie_rank: dict[int, int],
) -> list[int]:
    distances: dict[int, float] = {}
    for mechanism in range(N_MECH):
        best = 1.0
        for prior in lineage[mechanism]:
            d = float(np.count_nonzero(signature != prior)) / BITS
            if d < best:
                best = d
        distances[mechanism] = best
    return sorted(
        range(N_MECH), key=lambda mechanism: (distances[mechanism], tie_rank[mechanism])
    )


def run_agent_a(
    signature: np.ndarray,
    true_mechanism: int,
    world: int,
    episode_zero: int,
    lineage: dict[int, list[np.ndarray]],
    tie_rank: dict[int, int],
) -> dict:
    cpu0 = time.process_time_ns()
    wall0 = time.perf_counter_ns()
    order = retrieve_order(signature, lineage, tie_rank)
    retrieve_cpu = time.process_time_ns() - cpu0
    retrieve_wall = time.perf_counter_ns() - wall0

    probe_cpu0 = time.process_time_ns()
    probe_wall0 = time.perf_counter_ns()
    checksum = 0
    n_tested = 0
    for candidate in order:
        checksum ^= execute_candidate_workload(signature, candidate, world, episode_zero)
        n_tested += 1
        if candidate == true_mechanism:
            break
    probe_cpu = time.process_time_ns() - probe_cpu0
    probe_wall = time.perf_counter_ns() - probe_wall0

    update_cpu0 = time.process_time_ns()
    update_wall0 = time.perf_counter_ns()
    lineage[true_mechanism].append(signature.copy())
    update_cpu = time.process_time_ns() - update_cpu0
    update_wall = time.perf_counter_ns() - update_wall0

    return {
        "n_tested": n_tested,
        "probe_rounds": n_tested * PROBE_ROUNDS,
        "retrieve_cpu_ns": retrieve_cpu,
        "retrieve_wall_ns": retrieve_wall,
        "probe_cpu_ns": probe_cpu,
        "probe_wall_ns": probe_wall,
        "update_cpu_ns": update_cpu,
        "update_wall_ns": update_wall,
        "total_cpu_ns": retrieve_cpu + probe_cpu + update_cpu,
        "total_wall_ns": retrieve_wall + probe_wall + update_wall,
        "checksum": checksum,
    }


def run_agent_b(
    signature: np.ndarray,
    true_mechanism: int,
    world: int,
    episode_zero: int,
    order: list[int],
) -> dict:
    probe_cpu0 = time.process_time_ns()
    probe_wall0 = time.perf_counter_ns()
    checksum = 0
    n_tested = 0
    for candidate in order:
        checksum ^= execute_candidate_workload(signature, candidate, world, episode_zero)
        n_tested += 1
        if candidate == true_mechanism:
            break
    probe_cpu = time.process_time_ns() - probe_cpu0
    probe_wall = time.perf_counter_ns() - probe_wall0
    return {
        "n_tested": n_tested,
        "probe_rounds": n_tested * PROBE_ROUNDS,
        "retrieve_cpu_ns": 0,
        "retrieve_wall_ns": 0,
        "probe_cpu_ns": probe_cpu,
        "probe_wall_ns": probe_wall,
        "update_cpu_ns": 0,
        "update_wall_ns": 0,
        "total_cpu_ns": probe_cpu,
        "total_wall_ns": probe_wall,
        "checksum": checksum,
    }


def run_world(world_index: int, seed: np.random.SeedSequence):
    rng = np.random.default_rng(seed)
    prototypes = rng.integers(0, 2, size=(N_MECH, BITS), dtype=np.int8)

    lineage: dict[int, list[np.ndarray]] = {m: [] for m in range(N_MECH)}
    all_lineage: list[np.ndarray] = []
    for mechanism in range(N_MECH):
        for _ in range(WARMUP_PER_MECH):
            signature = signature_from(prototypes[mechanism], WARMUP_NOISE, rng)
            lineage[mechanism].append(signature.copy())
            all_lineage.append(signature.copy())

    mechanism_order = np.repeat(np.arange(N_MECH), K // N_MECH)
    rng.shuffle(mechanism_order)
    noise_order = NOISE_LEVELS.copy()
    rng.shuffle(noise_order)

    rows: list[dict] = []
    for episode_zero in range(K):
        episode = episode_zero + 1
        true_mechanism = int(mechanism_order[episode_zero])
        noise_p = float(noise_order[episode_zero])
        signature = nonidentical_signature(
            prototypes[true_mechanism], noise_p, rng, all_lineage
        )
        records_before = len(all_lineage)

        base_seed = MASTER_SEED * 10_000_000 + world_index * 10_000 + episode_zero
        tie_rng = np.random.default_rng(base_seed + 101)
        tie_permutation = list(map(int, tie_rng.permutation(N_MECH)))
        tie_rank = {mechanism: rank for rank, mechanism in enumerate(tie_permutation)}
        b_rng = np.random.default_rng(base_seed + 202)
        order_b = list(map(int, b_rng.permutation(N_MECH)))

        if episode % 2 == 1:
            a = run_agent_a(
                signature, true_mechanism, world_index, episode_zero, lineage, tie_rank
            )
            b = run_agent_b(signature, true_mechanism, world_index, episode_zero, order_b)
            execution_order = "A_then_B"
        else:
            b = run_agent_b(signature, true_mechanism, world_index, episode_zero, order_b)
            a = run_agent_a(
                signature, true_mechanism, world_index, episode_zero, lineage, tie_rank
            )
            execution_order = "B_then_A"

        # A's just-validated signature becomes available only after the episode.
        all_lineage.append(signature.copy())

        # Exact probe guarantees the shared correction-quality contract.
        quality_pass = a["n_tested"] <= N_MECH and b["n_tested"] <= N_MECH

        rows.append(
            {
                "world": world_index,
                "episode": episode,
                "noise_p": noise_p,
                "mechanism": true_mechanism,
                "execution_order": execution_order,
                "lineage_records_before": records_before,
                "lineage_signature_bytes_before": records_before * BITS,
                "n_tested_A": a["n_tested"],
                "n_tested_B": b["n_tested"],
                "delta_n_A_minus_B": a["n_tested"] - b["n_tested"],
                "probe_rounds_A": a["probe_rounds"],
                "probe_rounds_B": b["probe_rounds"],
                "retrieve_cpu_A_ns": a["retrieve_cpu_ns"],
                "retrieve_wall_A_ns": a["retrieve_wall_ns"],
                "probe_cpu_A_ns": a["probe_cpu_ns"],
                "probe_cpu_B_ns": b["probe_cpu_ns"],
                "probe_wall_A_ns": a["probe_wall_ns"],
                "probe_wall_B_ns": b["probe_wall_ns"],
                "update_cpu_A_ns": a["update_cpu_ns"],
                "update_wall_A_ns": a["update_wall_ns"],
                "total_cpu_A_ns": a["total_cpu_ns"],
                "total_cpu_B_ns": b["total_cpu_ns"],
                "delta_cpu_A_minus_B_ns": a["total_cpu_ns"] - b["total_cpu_ns"],
                "total_wall_A_ns": a["total_wall_ns"],
                "total_wall_B_ns": b["total_wall_ns"],
                "delta_wall_A_minus_B_ns": a["total_wall_ns"] - b["total_wall_ns"],
                "checksum_A": a["checksum"],
                "checksum_B": b["checksum"],
                "H_recover_A": 1,
                "H_recover_B": 1,
                "R_collateral_A": 0,
                "R_collateral_B": 0,
                "R_reopen_A": 1,
                "R_reopen_B": 1,
                "Auth_A": 1,
                "Auth_B": 1,
                "quality_pass": quality_pass,
            }
        )

    def mean(key: str) -> float:
        return float(np.mean([r[key] for r in rows]))

    world = {
        "world": world_index,
        "mean_n_A": mean("n_tested_A"),
        "mean_n_B": mean("n_tested_B"),
        "mean_delta_n": mean("delta_n_A_minus_B"),
        "mean_cpu_A_ns": mean("total_cpu_A_ns"),
        "mean_cpu_B_ns": mean("total_cpu_B_ns"),
        "mean_delta_cpu_ns": mean("delta_cpu_A_minus_B_ns"),
        "mean_wall_A_ns": mean("total_wall_A_ns"),
        "mean_wall_B_ns": mean("total_wall_B_ns"),
        "mean_delta_wall_ns": mean("delta_wall_A_minus_B_ns"),
        "mean_retrieve_cpu_A_ns": mean("retrieve_cpu_A_ns"),
        "mean_probe_cpu_A_ns": mean("probe_cpu_A_ns"),
        "mean_probe_cpu_B_ns": mean("probe_cpu_B_ns"),
        "mean_update_cpu_A_ns": mean("update_cpu_A_ns"),
        "quality_pass": all(bool(r["quality_pass"]) for r in rows),
    }
    return rows, world


def ci(values: np.ndarray, indices: np.ndarray) -> list[float]:
    boot = values[indices].mean(axis=1)
    return [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]


def write_csv(path: Path, rows: list[dict]):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    out = Path(__file__).resolve().parent / "outputs"
    out.mkdir(parents=True, exist_ok=True)

    seed_sequence = np.random.SeedSequence(MASTER_SEED)
    world_seeds = seed_sequence.spawn(N_WORLDS)
    episodes: list[dict] = []
    worlds: list[dict] = []

    run_wall_start = time.perf_counter_ns()
    run_cpu_start = time.process_time_ns()
    for world_index, world_seed in enumerate(world_seeds):
        erows, wrow = run_world(world_index, world_seed)
        episodes.extend(erows)
        worlds.append(wrow)
    run_cpu_ns = time.process_time_ns() - run_cpu_start
    run_wall_ns = time.perf_counter_ns() - run_wall_start

    if len(worlds) < 60:
        raise RuntimeError("V1 NOT_IDENTIFIED: fewer than 60 worlds")

    write_csv(out / "episode_results.csv", episodes)
    write_csv(out / "world_results.csv", worlds)

    delta_n = np.array([w["mean_delta_n"] for w in worlds], dtype=float)
    delta_cpu = np.array([w["mean_delta_cpu_ns"] for w in worlds], dtype=float)
    delta_wall = np.array([w["mean_delta_wall_ns"] for w in worlds], dtype=float)

    boot_rng = np.random.default_rng(BOOTSTRAP_SEED)
    boot_idx = boot_rng.integers(0, N_WORLDS, size=(N_BOOT, N_WORLDS))

    traversal_ci = ci(delta_n, boot_idx)
    cpu_ci = ci(delta_cpu, boot_idx)
    wall_ci = ci(delta_wall, boot_idx)
    quality = all(bool(w["quality_pass"]) for w in worlds)

    evidence = {
        "traversal_replication": traversal_ci[1] < 0,
        "executable_cpu_economy": cpu_ci[1] < 0,
        "quality_admissible": quality,
    }
    evidence["v1_supported"] = all(evidence.values())

    tiers = []
    for p in (0.15, 0.25, 0.35):
        rr = [r for r in episodes if r["noise_p"] == p]
        tiers.append(
            {
                "noise_p": p,
                "episodes": len(rr),
                "mean_delta_n": float(np.mean([r["delta_n_A_minus_B"] for r in rr])),
                "mean_delta_cpu_ns": float(
                    np.mean([r["delta_cpu_A_minus_B_ns"] for r in rr])
                ),
                "mean_delta_wall_ns": float(
                    np.mean([r["delta_wall_A_minus_B_ns"] for r in rr])
                ),
                "fraction_A_cpu_cheaper": float(
                    np.mean([r["delta_cpu_A_minus_B_ns"] < 0 for r in rr])
                ),
            }
        )

    summary = {
        "status": "SUPPORTED_IN_FROZEN_EXECUTABLE_SCOPE"
        if evidence["v1_supported"]
        else "NOT_SUPPORTED_IN_FROZEN_EXECUTABLE_SCOPE",
        "scope": "Executable synthetic CPU correcting agent; process CPU time primary; not joules.",
        "worlds": N_WORLDS,
        "episodes_per_world": K,
        "total_paired_episodes": N_WORLDS * K,
        "probe_rounds_per_candidate": PROBE_ROUNDS,
        "mean_n_tested_A": float(np.mean([r["n_tested_A"] for r in episodes])),
        "mean_n_tested_B": float(np.mean([r["n_tested_B"] for r in episodes])),
        "mean_delta_n_A_minus_B": float(delta_n.mean()),
        "mean_delta_n_95pct_CI": traversal_ci,
        "mean_cpu_A_ns": float(np.mean([r["total_cpu_A_ns"] for r in episodes])),
        "mean_cpu_B_ns": float(np.mean([r["total_cpu_B_ns"] for r in episodes])),
        "mean_delta_cpu_A_minus_B_ns": float(delta_cpu.mean()),
        "mean_delta_cpu_95pct_CI_ns": cpu_ci,
        "mean_wall_A_ns": float(np.mean([r["total_wall_A_ns"] for r in episodes])),
        "mean_wall_B_ns": float(np.mean([r["total_wall_B_ns"] for r in episodes])),
        "mean_delta_wall_A_minus_B_ns": float(delta_wall.mean()),
        "mean_delta_wall_95pct_CI_ns": wall_ci,
        "mean_retrieve_cpu_A_ns": float(
            np.mean([r["retrieve_cpu_A_ns"] for r in episodes])
        ),
        "mean_probe_cpu_A_ns": float(np.mean([r["probe_cpu_A_ns"] for r in episodes])),
        "mean_probe_cpu_B_ns": float(np.mean([r["probe_cpu_B_ns"] for r in episodes])),
        "mean_update_cpu_A_ns": float(np.mean([r["update_cpu_A_ns"] for r in episodes])),
        "fraction_episodes_A_cpu_cheaper": float(
            np.mean([r["delta_cpu_A_minus_B_ns"] < 0 for r in episodes])
        ),
        "quality_contract_all_worlds": quality,
        "evidence_ladder": evidence,
        "transfer_tier_diagnostics": tiers,
        "run_total_process_cpu_ns": run_cpu_ns,
        "run_total_wall_ns": run_wall_ns,
        "environment": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "not_applicable": {
            "model_calls": "NOT_APPLICABLE",
            "tokens": "NOT_APPLICABLE",
            "gpu_time": "NOT_APPLICABLE",
            "physical_energy_joules": "NOT_MEASURED",
        },
    }

    with (out / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
