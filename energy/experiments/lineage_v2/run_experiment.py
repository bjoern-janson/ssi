#!/usr/bin/env python3
"""SSI Energy Suite — Lineage Corrective Economy V2.

Frozen protocol: PREREGISTRATION.md in this directory.

V2 executes heterogeneous reversible repair programs and measures process CPU
time. Candidate implementations and validators are identical across treatment
arms; lineage affects ordering only.
"""
from __future__ import annotations

import csv
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

MASTER_SEED = 20260815
BOOTSTRAP_SEED = 20260818
N_BOOT = 20_000
N_WORLDS = 64
N_MECH = 12
BITS = 32
WARMUP_PER_MECH = 2
WARMUP_NOISE = 0.10
K = 96
PAYLOAD_LEN = 16_384
NOISE_LEVELS = np.array([0.15] * 48 + [0.25] * 32 + [0.35] * 16, dtype=float)

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


def normalized_hamming(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.count_nonzero(a != b)) / float(a.size)


def u8_mod(values: np.ndarray) -> np.ndarray:
    return np.bitwise_and(values, 255).astype(np.uint8, copy=False)


def forward_primitive(x: np.ndarray, name: str) -> np.ndarray:
    if name == "reverse":
        return x[::-1].copy()
    if name == "roll_113":
        return np.roll(x, 113)
    if name == "xor_a5":
        return np.bitwise_xor(x, np.uint8(0xA5))
    if name == "add_17_mod256":
        return u8_mod(x.astype(np.uint16) + 17)
    if name == "rotl3":
        u = x.astype(np.uint16)
        return u8_mod((u << 3) | (u >> 5))
    if name == "nibble_swap":
        u = x.astype(np.uint16)
        return u8_mod((u << 4) | (u >> 4))
    if name == "pair_swap":
        return x.reshape(-1, 2)[:, ::-1].reshape(-1).copy()
    if name == "block_reverse_64":
        return x.reshape(-1, 64)[:, ::-1].reshape(-1).copy()
    if name == "matrix_transpose_128":
        return x.reshape(128, 128).T.reshape(-1).copy()
    if name == "affine_5x_plus_7_mod256":
        return u8_mod(5 * x.astype(np.uint16) + 7)
    if name == "prefix_xor":
        out = np.empty_like(x)
        out[0] = x[0]
        out[1:] = np.bitwise_xor(x[1:], x[:-1])
        return out
    if name == "delta_mod256":
        out = np.empty_like(x)
        out[0] = x[0]
        out[1:] = u8_mod(x[1:].astype(np.int16) - x[:-1].astype(np.int16))
        return out
    raise ValueError(name)


def inverse_primitive(x: np.ndarray, name: str) -> np.ndarray:
    if name == "reverse":
        return x[::-1].copy()
    if name == "roll_113":
        return np.roll(x, -113)
    if name == "xor_a5":
        return np.bitwise_xor(x, np.uint8(0xA5))
    if name == "add_17_mod256":
        return u8_mod(x.astype(np.int16) - 17)
    if name == "rotl3":
        u = x.astype(np.uint16)
        return u8_mod((u >> 3) | (u << 5))
    if name == "nibble_swap":
        u = x.astype(np.uint16)
        return u8_mod((u << 4) | (u >> 4))
    if name == "pair_swap":
        return x.reshape(-1, 2)[:, ::-1].reshape(-1).copy()
    if name == "block_reverse_64":
        return x.reshape(-1, 64)[:, ::-1].reshape(-1).copy()
    if name == "matrix_transpose_128":
        return x.reshape(128, 128).T.reshape(-1).copy()
    if name == "affine_5x_plus_7_mod256":
        return u8_mod((x.astype(np.int16) - 7) * 205)
    if name == "prefix_xor":
        return np.bitwise_xor.accumulate(x).astype(np.uint8, copy=False)
    if name == "delta_mod256":
        return u8_mod(np.cumsum(x, dtype=np.uint64))
    raise ValueError(name)


def corrupt(clean: np.ndarray, mechanism: int) -> np.ndarray:
    out = clean
    for primitive in PIPELINES[mechanism]:
        out = forward_primitive(out, primitive)
    return out


def repair(corrupted: np.ndarray, mechanism: int) -> np.ndarray:
    out = corrupted
    for primitive in reversed(PIPELINES[mechanism]):
        out = inverse_primitive(out, primitive)
    return out


def retrieve_order(
    signature: np.ndarray,
    lineage: dict[int, list[np.ndarray]],
    tie_rank: dict[int, int],
) -> list[int]:
    distances = {}
    for mechanism in range(N_MECH):
        distances[mechanism] = min(
            normalized_hamming(signature, prior)
            for prior in lineage[mechanism]
        )
    return sorted(
        range(N_MECH),
        key=lambda mechanism: (distances[mechanism], tie_rank[mechanism]),
    )


def evaluate_candidate(
    corrupted: np.ndarray,
    clean: np.ndarray,
    candidate: int,
) -> tuple[bool, int, int]:
    cpu0 = time.process_time_ns()
    wall0 = time.perf_counter_ns()
    candidate_output = repair(corrupted, candidate)
    valid = bool(np.array_equal(candidate_output, clean))
    cpu = time.process_time_ns() - cpu0
    wall = time.perf_counter_ns() - wall0
    return valid, cpu, wall


def run_agent(
    *,
    arm: str,
    signature: np.ndarray,
    corrupted: np.ndarray,
    clean: np.ndarray,
    true_mechanism: int,
    order: list[int],
    lineage: dict[int, list[np.ndarray]] | None,
) -> tuple[dict, list[dict]]:
    candidate_rows: list[dict] = []
    eval_cpu_total = 0
    eval_wall_total = 0
    n_tested = 0
    correct_candidate = None

    for candidate in order:
        valid, cpu, wall = evaluate_candidate(corrupted, clean, candidate)
        n_tested += 1
        eval_cpu_total += cpu
        eval_wall_total += wall
        candidate_rows.append(
            {
                "arm": arm,
                "candidate": int(candidate),
                "candidate_depth": len(PIPELINES[candidate]),
                "candidate_cpu_ns": int(cpu),
                "candidate_wall_ns": int(wall),
                "valid": int(valid),
                "position": n_tested,
            }
        )
        if valid:
            correct_candidate = int(candidate)
            break

    if correct_candidate != true_mechanism:
        raise RuntimeError(
            f"Validator failed to identify true mechanism: arm={arm} "
            f"expected={true_mechanism} got={correct_candidate}"
        )

    update_cpu = update_wall = 0
    if arm == "A":
        assert lineage is not None
        cpu0 = time.process_time_ns()
        wall0 = time.perf_counter_ns()
        lineage[true_mechanism].append(signature.copy())
        update_cpu = time.process_time_ns() - cpu0
        update_wall = time.perf_counter_ns() - wall0

    return (
        {
            "n_tested": n_tested,
            "eval_cpu_ns": eval_cpu_total,
            "eval_wall_ns": eval_wall_total,
            "update_cpu_ns": update_cpu,
            "update_wall_ns": update_wall,
        },
        candidate_rows,
    )


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

    episode_rows: list[dict] = []
    candidate_rows: list[dict] = []

    for episode_zero in range(K):
        episode = episode_zero + 1
        true_mechanism = int(mechanism_order[episode_zero])
        noise_p = float(noise_order[episode_zero])
        signature = nonidentical_signature(
            prototypes[true_mechanism], noise_p, rng, all_lineage
        )

        clean = rng.integers(0, 256, size=PAYLOAD_LEN, dtype=np.uint8)
        corrupted = corrupt(clean, true_mechanism)

        if not np.array_equal(repair(corrupted, true_mechanism), clean):
            raise RuntimeError(f"True repair is not exact for mechanism {true_mechanism}")

        base_seed = MASTER_SEED * 10_000_000 + world_index * 10_000 + episode_zero

        tie_rng = np.random.default_rng(base_seed + 101)
        tie_permutation = list(map(int, tie_rng.permutation(N_MECH)))
        tie_rank = {mechanism: rank for rank, mechanism in enumerate(tie_permutation)}

        retrieval_cpu0 = time.process_time_ns()
        retrieval_wall0 = time.perf_counter_ns()
        order_a = retrieve_order(signature, lineage, tie_rank)
        retrieve_cpu_a = time.process_time_ns() - retrieval_cpu0
        retrieve_wall_a = time.perf_counter_ns() - retrieval_wall0

        b_rng = np.random.default_rng(base_seed + 202)
        order_b = list(map(int, b_rng.permutation(N_MECH)))

        records_before = sum(len(v) for v in lineage.values())

        if episode % 2 == 1:
            a, a_candidates = run_agent(
                arm="A",
                signature=signature,
                corrupted=corrupted,
                clean=clean,
                true_mechanism=true_mechanism,
                order=order_a,
                lineage=lineage,
            )
            b, b_candidates = run_agent(
                arm="B",
                signature=signature,
                corrupted=corrupted,
                clean=clean,
                true_mechanism=true_mechanism,
                order=order_b,
                lineage=None,
            )
            execution_order = "A_then_B"
        else:
            b, b_candidates = run_agent(
                arm="B",
                signature=signature,
                corrupted=corrupted,
                clean=clean,
                true_mechanism=true_mechanism,
                order=order_b,
                lineage=None,
            )
            a, a_candidates = run_agent(
                arm="A",
                signature=signature,
                corrupted=corrupted,
                clean=clean,
                true_mechanism=true_mechanism,
                order=order_a,
                lineage=lineage,
            )
            execution_order = "B_then_A"

        all_lineage.append(signature.copy())

        total_cpu_a = retrieve_cpu_a + a["eval_cpu_ns"] + a["update_cpu_ns"]
        total_wall_a = retrieve_wall_a + a["eval_wall_ns"] + a["update_wall_ns"]
        total_cpu_b = b["eval_cpu_ns"]
        total_wall_b = b["eval_wall_ns"]

        quality_pass = a["n_tested"] <= N_MECH and b["n_tested"] <= N_MECH

        row = {
            "world": world_index,
            "episode": episode,
            "noise_p": noise_p,
            "mechanism": true_mechanism,
            "execution_order": execution_order,
            "lineage_records_before": records_before,
            "n_tested_A": a["n_tested"],
            "n_tested_B": b["n_tested"],
            "delta_n_A_minus_B": a["n_tested"] - b["n_tested"],
            "eval_cpu_A_ns": a["eval_cpu_ns"],
            "eval_cpu_B_ns": b["eval_cpu_ns"],
            "delta_eval_cpu_A_minus_B_ns": a["eval_cpu_ns"] - b["eval_cpu_ns"],
            "retrieve_cpu_A_ns": retrieve_cpu_a,
            "update_cpu_A_ns": a["update_cpu_ns"],
            "total_cpu_A_ns": total_cpu_a,
            "total_cpu_B_ns": total_cpu_b,
            "delta_total_cpu_A_minus_B_ns": total_cpu_a - total_cpu_b,
            "eval_wall_A_ns": a["eval_wall_ns"],
            "eval_wall_B_ns": b["eval_wall_ns"],
            "retrieve_wall_A_ns": retrieve_wall_a,
            "update_wall_A_ns": a["update_wall_ns"],
            "total_wall_A_ns": total_wall_a,
            "total_wall_B_ns": total_wall_b,
            "delta_total_wall_A_minus_B_ns": total_wall_a - total_wall_b,
            "H_recover_A": 1,
            "H_recover_B": 1,
            "R_collateral_A": 0,
            "R_collateral_B": 0,
            "R_reopen_A": 1,
            "R_reopen_B": 1,
            "Auth_A": 1,
            "Auth_B": 1,
            "quality_pass": quality_pass,
            "adversarial_eval": int(
                a["n_tested"] < b["n_tested"]
                and a["eval_cpu_ns"] > b["eval_cpu_ns"]
            ),
            "adversarial_total": int(
                a["n_tested"] < b["n_tested"]
                and total_cpu_a > total_cpu_b
            ),
        }
        episode_rows.append(row)

        for cr in a_candidates + b_candidates:
            cr.update(
                {
                    "world": world_index,
                    "episode": episode,
                    "noise_p": noise_p,
                    "true_mechanism": true_mechanism,
                }
            )
            candidate_rows.append(cr)

    def mean(key: str) -> float:
        return float(np.mean([r[key] for r in episode_rows]))

    world_row = {
        "world": world_index,
        "mean_delta_n": mean("delta_n_A_minus_B"),
        "mean_delta_eval_cpu_ns": mean("delta_eval_cpu_A_minus_B_ns"),
        "mean_delta_total_cpu_ns": mean("delta_total_cpu_A_minus_B_ns"),
        "mean_delta_total_wall_ns": mean("delta_total_wall_A_minus_B_ns"),
        "mean_n_A": mean("n_tested_A"),
        "mean_n_B": mean("n_tested_B"),
        "mean_eval_cpu_A_ns": mean("eval_cpu_A_ns"),
        "mean_eval_cpu_B_ns": mean("eval_cpu_B_ns"),
        "mean_total_cpu_A_ns": mean("total_cpu_A_ns"),
        "mean_total_cpu_B_ns": mean("total_cpu_B_ns"),
        "mean_retrieve_cpu_A_ns": mean("retrieve_cpu_A_ns"),
        "mean_update_cpu_A_ns": mean("update_cpu_A_ns"),
        "fraction_adversarial_eval": mean("adversarial_eval"),
        "fraction_adversarial_total": mean("adversarial_total"),
        "quality_pass": all(bool(r["quality_pass"]) for r in episode_rows),
    }
    return episode_rows, candidate_rows, world_row


def percentile_ci(values: np.ndarray, bootstrap_indices: np.ndarray) -> list[float]:
    boot_means = values[bootstrap_indices].mean(axis=1)
    return [
        float(np.percentile(boot_means, 2.5)),
        float(np.percentile(boot_means, 97.5)),
    ]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    out = Path(__file__).resolve().parent / "outputs"
    out.mkdir(parents=True, exist_ok=True)

    seed_sequence = np.random.SeedSequence(MASTER_SEED)
    world_seeds = seed_sequence.spawn(N_WORLDS)

    episode_rows: list[dict] = []
    candidate_rows: list[dict] = []
    world_rows: list[dict] = []

    run_wall0 = time.perf_counter_ns()
    run_cpu0 = time.process_time_ns()
    for world_index, world_seed in enumerate(world_seeds):
        erows, crows, wrow = run_world(world_index, world_seed)
        episode_rows.extend(erows)
        candidate_rows.extend(crows)
        world_rows.append(wrow)
    run_cpu_ns = time.process_time_ns() - run_cpu0
    run_wall_ns = time.perf_counter_ns() - run_wall0

    if len(world_rows) < 60:
        raise RuntimeError("V2 NOT_IDENTIFIED: fewer than 60 worlds")

    write_csv(out / "episode_results.csv", episode_rows)
    write_csv(out / "candidate_evaluations.csv", candidate_rows)
    write_csv(out / "world_results.csv", world_rows)

    delta_n = np.array([w["mean_delta_n"] for w in world_rows], dtype=float)
    delta_eval = np.array(
        [w["mean_delta_eval_cpu_ns"] for w in world_rows], dtype=float
    )
    delta_total = np.array(
        [w["mean_delta_total_cpu_ns"] for w in world_rows], dtype=float
    )
    delta_wall = np.array(
        [w["mean_delta_total_wall_ns"] for w in world_rows], dtype=float
    )

    boot_rng = np.random.default_rng(BOOTSTRAP_SEED)
    bootstrap_indices = boot_rng.integers(
        0, N_WORLDS, size=(N_BOOT, N_WORLDS)
    )

    ci_n = percentile_ci(delta_n, bootstrap_indices)
    ci_eval = percentile_ci(delta_eval, bootstrap_indices)
    ci_total = percentile_ci(delta_total, bootstrap_indices)
    ci_wall = percentile_ci(delta_wall, bootstrap_indices)

    b_candidate_costs: dict[int, list[int]] = {j: [] for j in range(N_MECH)}
    for row in candidate_rows:
        if row["arm"] == "B":
            b_candidate_costs[int(row["candidate"])].append(
                int(row["candidate_cpu_ns"])
            )

    candidate_cost_table = []
    medians = []
    for candidate in range(N_MECH):
        values = np.array(b_candidate_costs[candidate], dtype=float)
        if values.size == 0:
            raise RuntimeError(f"No B timings for candidate {candidate}")
        median = float(np.median(values))
        medians.append(median)
        candidate_cost_table.append(
            {
                "candidate": candidate,
                "pipeline": " -> ".join(PIPELINES[candidate]),
                "depth": len(PIPELINES[candidate]),
                "B_evaluations": int(values.size),
                "median_cpu_ns": median,
                "mean_cpu_ns": float(values.mean()),
            }
        )

    heterogeneity_ratio = float(max(medians) / min(medians))
    heterogeneity_gate = heterogeneity_ratio >= 2.0
    quality = all(bool(w["quality_pass"]) for w in world_rows)

    evidence = {
        "search_reuse": ci_n[1] < 0,
        "heterogeneity_gate": heterogeneity_gate,
        "heterogeneous_work_avoidance": heterogeneity_gate and ci_eval[1] < 0,
        "net_executable_economy": ci_total[1] < 0,
        "quality_admissible": quality,
    }
    evidence["v2_supported"] = (
        evidence["heterogeneous_work_avoidance"]
        and evidence["net_executable_economy"]
        and evidence["quality_admissible"]
    )

    transfer_tiers = []
    for p in (0.15, 0.25, 0.35):
        rows = [r for r in episode_rows if r["noise_p"] == p]
        transfer_tiers.append(
            {
                "noise_p": p,
                "episodes": len(rows),
                "mean_delta_n": float(np.mean([r["delta_n_A_minus_B"] for r in rows])),
                "mean_delta_eval_cpu_ns": float(
                    np.mean([r["delta_eval_cpu_A_minus_B_ns"] for r in rows])
                ),
                "mean_delta_total_cpu_ns": float(
                    np.mean([r["delta_total_cpu_A_minus_B_ns"] for r in rows])
                ),
                "fraction_A_total_cpu_cheaper": float(
                    np.mean([r["delta_total_cpu_A_minus_B_ns"] < 0 for r in rows])
                ),
                "fraction_adversarial_eval": float(
                    np.mean([r["adversarial_eval"] for r in rows])
                ),
                "fraction_adversarial_total": float(
                    np.mean([r["adversarial_total"] for r in rows])
                ),
            }
        )

    status = (
        "SUPPORTED_IN_FROZEN_HETEROGENEOUS_EXECUTABLE_SCOPE"
        if evidence["v2_supported"]
        else (
            "NOT_IDENTIFIED_FOR_HETEROGENEOUS_COST"
            if not heterogeneity_gate
            else "NOT_SUPPORTED_IN_FROZEN_HETEROGENEOUS_EXECUTABLE_SCOPE"
        )
    )

    summary = {
        "status": status,
        "scope": (
            "Executable synthetic heterogeneous repair programs; process CPU "
            "time primary; not physical energy."
        ),
        "worlds": N_WORLDS,
        "episodes_per_world": K,
        "total_paired_episodes": N_WORLDS * K,
        "payload_len_uint8": PAYLOAD_LEN,
        "candidate_pipelines": {
            str(k): list(v) for k, v in PIPELINES.items()
        },
        "mean_n_tested_A": float(
            np.mean([r["n_tested_A"] for r in episode_rows])
        ),
        "mean_n_tested_B": float(
            np.mean([r["n_tested_B"] for r in episode_rows])
        ),
        "mean_delta_n_A_minus_B": float(delta_n.mean()),
        "mean_delta_n_95pct_CI": ci_n,
        "mean_eval_cpu_A_ns": float(
            np.mean([r["eval_cpu_A_ns"] for r in episode_rows])
        ),
        "mean_eval_cpu_B_ns": float(
            np.mean([r["eval_cpu_B_ns"] for r in episode_rows])
        ),
        "mean_delta_eval_cpu_A_minus_B_ns": float(delta_eval.mean()),
        "mean_delta_eval_cpu_95pct_CI_ns": ci_eval,
        "mean_retrieve_cpu_A_ns": float(
            np.mean([r["retrieve_cpu_A_ns"] for r in episode_rows])
        ),
        "mean_update_cpu_A_ns": float(
            np.mean([r["update_cpu_A_ns"] for r in episode_rows])
        ),
        "mean_total_cpu_A_ns": float(
            np.mean([r["total_cpu_A_ns"] for r in episode_rows])
        ),
        "mean_total_cpu_B_ns": float(
            np.mean([r["total_cpu_B_ns"] for r in episode_rows])
        ),
        "mean_delta_total_cpu_A_minus_B_ns": float(delta_total.mean()),
        "mean_delta_total_cpu_95pct_CI_ns": ci_total,
        "mean_delta_total_wall_A_minus_B_ns": float(delta_wall.mean()),
        "mean_delta_total_wall_95pct_CI_ns": ci_wall,
        "candidate_cost_heterogeneity_ratio_B_medians": heterogeneity_ratio,
        "candidate_cost_table_B": candidate_cost_table,
        "fraction_episodes_adversarial_eval": float(
            np.mean([r["adversarial_eval"] for r in episode_rows])
        ),
        "fraction_episodes_adversarial_total": float(
            np.mean([r["adversarial_total"] for r in episode_rows])
        ),
        "fraction_episodes_A_total_cpu_cheaper": float(
            np.mean([r["delta_total_cpu_A_minus_B_ns"] < 0 for r in episode_rows])
        ),
        "quality_contract_all_worlds": quality,
        "evidence_ladder": evidence,
        "transfer_tier_diagnostics": transfer_tiers,
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
        "not_measured": {
            "gpu_time": "NOT_MEASURED",
            "physical_energy_joules": "NOT_MEASURED",
            "llm_tokens": "NOT_APPLICABLE",
        },
    }

    with (out / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
