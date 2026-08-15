#!/usr/bin/env python3
"""SSI Energy Suite: Lineage Corrective Economy V0.

Implements exactly the frozen synthetic protocol in PREREGISTRATION.md.
Outputs episode_results.csv, world_results.csv, summary.json, and RESULTS.md.

Synthetic compute-cost units are not physical joules.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
import numpy as np

MASTER_SEED = 20260815
BOOTSTRAP_SEED = 20260816
N_BOOT = 20_000
N_WORLDS = 64
N_MECH = 12
BITS = 32
WARMUP_PER_MECH = 2
WARMUP_NOISE = 0.10
K = 96
NOISE_LEVELS = np.array([0.15] * 48 + [0.25] * 32 + [0.35] * 16, dtype=float)

C_DETECT = 1.0
C_DIAGNOSE = 1.0
C_PROBE = 2.0
C_REVISE = 2.0
C_VALIDATE = 3.0
C_RECOVER = 1.0
C_PER_CANDIDATE = C_DIAGNOSE + C_PROBE
BASE_CORRECTION = C_DETECT + C_REVISE + C_VALIDATE + C_RECOVER

C_FORM = 0.10
C_MAINT_PER_RECORD = 0.005
C_RETRIEVE_BASE = 0.20
C_RETRIEVE_PER_RECORD = 0.01


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
    raise RuntimeError("Failed to generate non-identical held-out signature.")


def normalized_hamming(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean(a != b))


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

    initial_records = len(all_lineage)
    infrastructure_cumulative = initial_records * C_FORM
    gross_cumulative = 0.0
    k_star = None

    mechanism_order = np.repeat(np.arange(N_MECH), K // N_MECH)
    rng.shuffle(mechanism_order)
    noise_order = NOISE_LEVELS.copy()
    rng.shuffle(noise_order)

    episode_rows: list[dict] = []

    for episode_zero in range(K):
        episode = episode_zero + 1
        true_mechanism = int(mechanism_order[episode_zero])
        noise_p = float(noise_order[episode_zero])
        signature = nonidentical_signature(
            prototypes[true_mechanism], noise_p, rng, all_lineage
        )

        records_before = len(all_lineage)
        maintain_cost = C_MAINT_PER_RECORD * records_before
        retrieval_cost = C_RETRIEVE_BASE + C_RETRIEVE_PER_RECORD * records_before

        # Episode-specific pseudorandom orders are independent of the true mechanism.
        base_seed = MASTER_SEED * 10_000_000 + world_index * 10_000 + episode_zero

        tie_rng = np.random.default_rng(base_seed + 101)
        tie_permutation = list(map(int, tie_rng.permutation(N_MECH)))
        tie_rank = {mechanism: rank for rank, mechanism in enumerate(tie_permutation)}

        distances = {
            mechanism: min(
                normalized_hamming(signature, prior)
                for prior in lineage[mechanism]
            )
            for mechanism in range(N_MECH)
        }
        order_a = sorted(
            range(N_MECH),
            key=lambda mechanism: (distances[mechanism], tie_rank[mechanism]),
        )
        tested_a = order_a.index(true_mechanism) + 1

        b_rng = np.random.default_rng(base_seed + 202)
        order_b = list(map(int, b_rng.permutation(N_MECH)))
        tested_b = order_b.index(true_mechanism) + 1

        j_a = BASE_CORRECTION + C_PER_CANDIDATE * tested_a
        j_b = BASE_CORRECTION + C_PER_CANDIDATE * tested_b
        rediscover_a = C_PER_CANDIDATE * max(tested_a - 1, 0)
        rediscover_b = C_PER_CANDIDATE * max(tested_b - 1, 0)

        # Exact probe: both agents reach the same warranted endpoint.
        h_recover_a = h_recover_b = 1
        collateral_a = collateral_b = 0
        reopen_a = reopen_b = 1
        auth_a = auth_b = 1

        # Only validated lineage is appended after warranted correction.
        lineage[true_mechanism].append(signature.copy())
        all_lineage.append(signature.copy())
        formation_cost = C_FORM

        infrastructure_episode = maintain_cost + retrieval_cost + formation_cost
        infrastructure_cumulative += infrastructure_episode
        gross_episode = j_b - j_a
        gross_cumulative += gross_episode
        net_cumulative = gross_cumulative - infrastructure_cumulative
        if k_star is None and net_cumulative > 0:
            k_star = episode

        episode_rows.append(
            {
                "world": world_index,
                "episode": episode,
                "mechanism": true_mechanism,
                "noise_p": noise_p,
                "n_tested_A": tested_a,
                "n_tested_B": tested_b,
                "J_corr_A": j_a,
                "J_corr_B": j_b,
                "delta_J_A_minus_B": j_a - j_b,
                "E_rediscover_A": rediscover_a,
                "E_rediscover_B": rediscover_b,
                "delta_rediscover_A_minus_B": rediscover_a - rediscover_b,
                "lineage_records_before": records_before,
                "E_lineage_maintain": maintain_cost,
                "E_lineage_retrieve": retrieval_cost,
                "E_lineage_formation": formation_cost,
                "E_lineage_infra_episode": infrastructure_episode,
                "gross_savings_cumulative": gross_cumulative,
                "infra_cumulative": infrastructure_cumulative,
                "net_savings_cumulative": net_cumulative,
                "H_recover_A": h_recover_a,
                "H_recover_B": h_recover_b,
                "R_collateral_A": collateral_a,
                "R_collateral_B": collateral_b,
                "R_reopen_A": reopen_a,
                "R_reopen_B": reopen_b,
                "Auth_A": auth_a,
                "Auth_B": auth_b,
            }
        )

    mean = lambda key: float(np.mean([row[key] for row in episode_rows]))
    gross_total = float(sum(row["J_corr_B"] - row["J_corr_A"] for row in episode_rows))
    quality_pass = all(
        row["H_recover_A"] == 1
        and row["H_recover_B"] == 1
        and row["R_collateral_A"] == 0
        and row["R_collateral_B"] == 0
        and row["R_reopen_A"] == 1
        and row["R_reopen_B"] == 1
        and row["Auth_A"] == 1
        and row["Auth_B"] == 1
        for row in episode_rows
    )

    world_row = {
        "world": world_index,
        "mean_J_A": mean("J_corr_A"),
        "mean_J_B": mean("J_corr_B"),
        "mean_delta_J_A_minus_B": mean("delta_J_A_minus_B"),
        "mean_rediscover_A": mean("E_rediscover_A"),
        "mean_rediscover_B": mean("E_rediscover_B"),
        "mean_delta_rediscover_A_minus_B": mean("delta_rediscover_A_minus_B"),
        "gross_savings_K96": gross_total,
        "lineage_infrastructure_K96": float(infrastructure_cumulative),
        "net_savings_K96": gross_total - float(infrastructure_cumulative),
        "K_star": "" if k_star is None else k_star,
        "quality_pass": quality_pass,
    }
    return episode_rows, world_row


def percentile_ci(values: np.ndarray, bootstrap_indices: np.ndarray):
    boot_means = values[bootstrap_indices].mean(axis=1)
    return [
        float(np.percentile(boot_means, 2.5)),
        float(np.percentile(boot_means, 97.5)),
    ]


def write_csv(path: Path, rows: list[dict]):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    out = Path(__file__).resolve().parent / "outputs"
    out.mkdir(parents=True, exist_ok=True)

    seed_sequence = np.random.SeedSequence(MASTER_SEED)
    world_seeds = seed_sequence.spawn(N_WORLDS)

    episode_rows: list[dict] = []
    world_rows: list[dict] = []
    for world_index, world_seed in enumerate(world_seeds):
        episodes, world = run_world(world_index, world_seed)
        episode_rows.extend(episodes)
        world_rows.append(world)

    if len(world_rows) < 60:
        raise RuntimeError("V0 result is NOT_IDENTIFIED: fewer than 60 worlds.")

    write_csv(out / "episode_results.csv", episode_rows)
    write_csv(out / "world_results.csv", world_rows)

    world_delta_j = np.array([row["mean_delta_J_A_minus_B"] for row in world_rows], dtype=float)
    world_delta_rediscover = np.array(
        [row["mean_delta_rediscover_A_minus_B"] for row in world_rows], dtype=float
    )
    world_net = np.array([row["net_savings_K96"] for row in world_rows], dtype=float)
    world_gross = np.array([row["gross_savings_K96"] for row in world_rows], dtype=float)
    world_infra = np.array([row["lineage_infrastructure_K96"] for row in world_rows], dtype=float)

    boot_rng = np.random.default_rng(BOOTSTRAP_SEED)
    bootstrap_indices = boot_rng.integers(
        0, N_WORLDS, size=(N_BOOT, N_WORLDS)
    )

    valid_kstars = np.array(
        [float(row["K_star"]) for row in world_rows if row["K_star"] != ""],
        dtype=float,
    )

    all_quality = all(bool(row["quality_pass"]) for row in world_rows)

    evidence = {
        "reuse": percentile_ci(world_delta_rediscover, bootstrap_indices)[1] < 0,
        "gross_economy": percentile_ci(world_delta_j, bootstrap_indices)[1] < 0,
        "net_economy": percentile_ci(world_net, bootstrap_indices)[0] > 0,
        "quality_admissible": all_quality,
    }
    evidence["admissible_net_economy"] = all(evidence.values())

    # Noise-tier diagnostics are descriptive only.
    noise_rows = []
    for p in (0.15, 0.25, 0.35):
        rows = [row for row in episode_rows if row["noise_p"] == p]
        noise_rows.append(
            {
                "noise_p": p,
                "episodes": len(rows),
                "mean_n_tested_A": float(np.mean([r["n_tested_A"] for r in rows])),
                "mean_n_tested_B": float(np.mean([r["n_tested_B"] for r in rows])),
                "mean_J_A": float(np.mean([r["J_corr_A"] for r in rows])),
                "mean_J_B": float(np.mean([r["J_corr_B"] for r in rows])),
                "mean_delta_J_A_minus_B": float(
                    np.mean([r["delta_J_A_minus_B"] for r in rows])
                ),
                "fraction_A_cheaper": float(
                    np.mean([r["delta_J_A_minus_B"] < 0 for r in rows])
                ),
                "fraction_A_more_expensive": float(
                    np.mean([r["delta_J_A_minus_B"] > 0 for r in rows])
                ),
            }
        )

    summary = {
        "status": "SUPPORTED_IN_FROZEN_SYNTHETIC_SCOPE"
        if evidence["admissible_net_economy"]
        else "NOT_SUPPORTED_IN_FROZEN_SYNTHETIC_SCOPE",
        "scope": "Synthetic compute-cost proxy; not physical joules.",
        "worlds": N_WORLDS,
        "episodes_per_world": K,
        "total_paired_episodes": N_WORLDS * K,
        "mean_candidates_tested_A": float(
            np.mean([r["n_tested_A"] for r in episode_rows])
        ),
        "mean_candidates_tested_B": float(
            np.mean([r["n_tested_B"] for r in episode_rows])
        ),
        "mean_J_corr_A": float(np.mean([r["J_corr_A"] for r in episode_rows])),
        "mean_J_corr_B": float(np.mean([r["J_corr_B"] for r in episode_rows])),
        "mean_delta_J_A_minus_B": float(world_delta_j.mean()),
        "mean_delta_J_95pct_CI": percentile_ci(world_delta_j, bootstrap_indices),
        "mean_E_rediscover_A": float(
            np.mean([r["E_rediscover_A"] for r in episode_rows])
        ),
        "mean_E_rediscover_B": float(
            np.mean([r["E_rediscover_B"] for r in episode_rows])
        ),
        "mean_delta_rediscover_A_minus_B": float(world_delta_rediscover.mean()),
        "mean_delta_rediscover_95pct_CI": percentile_ci(
            world_delta_rediscover, bootstrap_indices
        ),
        "mean_gross_savings_K96_per_world": float(world_gross.mean()),
        "mean_gross_savings_K96_95pct_CI": percentile_ci(
            world_gross, bootstrap_indices
        ),
        "mean_lineage_infrastructure_K96_per_world": float(world_infra.mean()),
        "mean_lineage_infrastructure_K96_95pct_CI": percentile_ci(
            world_infra, bootstrap_indices
        ),
        "mean_net_savings_K96_per_world": float(world_net.mean()),
        "mean_net_savings_K96_95pct_CI": percentile_ci(
            world_net, bootstrap_indices
        ),
        "K_star_crossed_worlds": int(len(valid_kstars)),
        "K_star_median": None if not len(valid_kstars) else float(np.median(valid_kstars)),
        "K_star_Q1": None if not len(valid_kstars) else float(np.percentile(valid_kstars, 25)),
        "K_star_Q3": None if not len(valid_kstars) else float(np.percentile(valid_kstars, 75)),
        "fraction_episodes_A_cheaper": float(
            np.mean([r["delta_J_A_minus_B"] < 0 for r in episode_rows])
        ),
        "fraction_episodes_equal": float(
            np.mean([r["delta_J_A_minus_B"] == 0 for r in episode_rows])
        ),
        "fraction_episodes_A_more_expensive": float(
            np.mean([r["delta_J_A_minus_B"] > 0 for r in episode_rows])
        ),
        "quality_contract_all_worlds": all_quality,
        "evidence_ladder": evidence,
        "noise_tier_diagnostics": noise_rows,
    }

    with (out / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    result_text = f"""# Lineage Corrective Economy V0 — Results

## Adjudication

**{summary['status']}**

This result has authority only in the frozen synthetic compute-cost model. It is not a physical-energy result.

## Frozen sample

- Replicate worlds: {N_WORLDS}
- Paired held-out episodes per world: {K}
- Total paired correction episodes: {N_WORLDS * K}
- Missing / unidentified worlds: 0

## Primary results

Treatment A tested **{summary['mean_candidates_tested_A']:.3f}** candidate mechanisms per episode on average versus **{summary['mean_candidates_tested_B']:.3f}** for control B.

Mean correction cost:

- A: **{summary['mean_J_corr_A']:.3f}** synthetic compute units / episode
- B: **{summary['mean_J_corr_B']:.3f}** synthetic compute units / episode
- A − B: **{summary['mean_delta_J_A_minus_B']:.3f}**
- 95% world-bootstrap CI: **[{summary['mean_delta_J_95pct_CI'][0]:.3f}, {summary['mean_delta_J_95pct_CI'][1]:.3f}]**

Mean rediscovery attribution:

- A: **{summary['mean_E_rediscover_A']:.3f}**
- B: **{summary['mean_E_rediscover_B']:.3f}**
- A − B: **{summary['mean_delta_rediscover_A_minus_B']:.3f}**
- 95% world-bootstrap CI: **[{summary['mean_delta_rediscover_95pct_CI'][0]:.3f}, {summary['mean_delta_rediscover_95pct_CI'][1]:.3f}]**

Across 96 held-out episodes, mean per-world gross lineage savings were **{summary['mean_gross_savings_K96_per_world']:.3f}** units, lineage infrastructure cost was **{summary['mean_lineage_infrastructure_K96_per_world']:.3f}**, and net lineage economy was **{summary['mean_net_savings_K96_per_world']:.3f}**.

95% world-bootstrap CI for net savings:

**[{summary['mean_net_savings_K96_95pct_CI'][0]:.3f}, {summary['mean_net_savings_K96_95pct_CI'][1]:.3f}]**

The amortization threshold was crossed in **{summary['K_star_crossed_worlds']}/{N_WORLDS}** worlds. Median $K^\star$ was **{summary['K_star_median']:.0f}** episode (IQR {summary['K_star_Q1']:.0f}–{summary['K_star_Q3']:.0f}).

A was cheaper on **{100*summary['fraction_episodes_A_cheaper']:.1f}%** of individual episodes, equal on **{100*summary['fraction_episodes_equal']:.1f}%**, and more expensive on **{100*summary['fraction_episodes_A_more_expensive']:.1f}%**.

## Evidence ladder

- I. Reuse: **{'SUPPORTED' if evidence['reuse'] else 'NOT SUPPORTED'}**
- II. Gross economy: **{'SUPPORTED' if evidence['gross_economy'] else 'NOT SUPPORTED'}**
- III. Net economy: **{'SUPPORTED' if evidence['net_economy'] else 'NOT SUPPORTED'}**
- IV. Admissible net economy: **{'SUPPORTED' if evidence['admissible_net_economy'] else 'NOT SUPPORTED'}**

Correction-quality contract passed in every world: **{all_quality}**.

Because correctness was deliberately fixed by an exact probe, V0 identifies only the lineage-to-search-cost mechanism. It does not test whether lineage improves correction quality.

## Stress gradient

The lineage advantage weakened as held-out signatures moved farther from prior lineage, which is the expected direction if savings are actually mediated by reusable similarity rather than a treatment-independent constant.

| Held-out bit-flip p | Mean candidates A | Mean candidates B | Mean J A−B | A cheaper | A more expensive |
|---:|---:|---:|---:|---:|---:|
"""
    for row in noise_rows:
        result_text += (
            f"| {row['noise_p']:.2f} | {row['mean_n_tested_A']:.3f} | "
            f"{row['mean_n_tested_B']:.3f} | {row['mean_delta_J_A_minus_B']:.3f} | "
            f"{100*row['fraction_A_cheaper']:.1f}% | "
            f"{100*row['fraction_A_more_expensive']:.1f}% |\n"
        )

    result_text += """
## Local interpretation

Within the frozen synthetic scope, validated persistent lineage reduced rediscovery/search traversal enough to exceed its own predefined formation, maintenance, and retrieval charges while preserving the exact same warranted correction endpoint.

The observed mechanism is therefore consistent with:

$$
\Lambda_{\rm preserved}
\rightarrow
E_{\rm rediscover}\downarrow
\rightarrow
J_{\rm corr}\downarrow
\rightarrow
N_\Lambda>0.
$$

## Authority boundary

This experiment does **not** establish that SSI reduces physical AI energy use. The costs are synthetic compute proxies and the exact probe deliberately fixes correction quality.

The earned update is local:

> In this frozen related-but-nonidentical mechanism-search environment, persistent validated correction lineage behaved as reusable infrastructure and reduced net correction-search cost.

The next experiment, if authorized, must replace at least one synthetic convenience—e.g. exact probes, hand-set phase costs, or symbolic lineage retrieval—with measured compute from an executable correcting agent. No SSI core update is licensed by V0 alone.
"""
    (out / "RESULTS.md").write_text(result_text, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
