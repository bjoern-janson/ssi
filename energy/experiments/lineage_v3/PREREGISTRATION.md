# Lineage Corrective Economy V3 — Physical-Energy Preregistration

## Status

**FROZEN BEFORE ANY V3 TREATMENT RUN.**

V3 is authorized only if the execution environment exposes an independently readable physical-energy boundary. V3 must not substitute process CPU time, wall time, synthetic costs, estimated TDP, or provider-reported utilization for joules.

The scientific question is deliberately narrow:

> Does the V2 lineage intervention reduce measured physical energy for the same heterogeneous corrective workload and the same warranted correction-quality contract?

## 1. Frozen treatment and workload

V3 inherits the V2 experimental skeleton without changing the treatment mechanism:

- `A = Lambda_preserved`;
- `B = Lambda_unavailable`;
- same 12 heterogeneous reversible repair candidates;
- same lineage-only ordering intervention;
- same held-out related-but-nonidentical challenge construction;
- same transfer-relevance tiers;
- same exact validator and acceptance contract;
- same rule that lineage may influence ordering only, never candidate implementation, intrinsic cost, or correctness.

No SSI core theory, Axis I definition, or corrective-topology definition is modified by V3.

## 2. Measurement-gate requirement

Before any A/B V3 treatment run, the environment must expose at least one physically grounded energy interface that can produce cumulative energy measurements in joules or directly convertible energy units over the experimental boundary.

Admissible examples include:

- a readable Linux powercap/RAPL-style cumulative `energy_uj` counter;
- a readable hardware-monitor cumulative energy counter with documented units;
- an externally instrumented power/energy meter whose readings can be synchronized to frozen experiment batches.

A mere instantaneous power reading is insufficient unless the sampling/integration procedure is independently frozen and validated at the experiment timescale.

If no admissible physical-energy interface is exposed, V3 treatment execution is prohibited and status is:

`NOT_RUN_MEASUREMENT_BOUNDARY_NOT_IDENTIFIED`.

`NOT_IDENTIFIED` is not zero effect and not a negative effect.

## 3. Primary estimand if the gate passes

For matched correction batches under identical workload exposure, define

$$
\Delta E_{\rm physical}
=
E_{\rm physical}^{A}
-
E_{\rm physical}^{B}.
$$

The primary directional hypothesis is

$$
\mathbb E[\Delta E_{\rm physical}]<0,
$$

subject to the unchanged correction-quality admissibility contract.

CPU time remains a secondary diagnostic only. V3 authority comes from measured physical energy.

## 4. Accounting boundary

The physical-energy measurement must include all treatment-specific executed work inside the measured system boundary, including:

- lineage retrieval/order construction;
- candidate repair execution;
- lineage update;
- validation work;
- any treatment-specific indexing or memory-maintenance work occurring during the measured batch.

Energy must not disappear by moving work outside the measured interval or measured device boundary.

## 5. Correction-quality contract

Both arms must continue to satisfy the frozen V2 correction-quality requirements:

- `H_recover = 1`;
- `R_collateral = 0`;
- `R_reopen = 1`;
- `Auth = 1`.

Physical-energy reduction cannot rescue a correction-quality failure.

## 6. Execution-order control

If the measurement gate passes, A/B batch order must be balanced or randomized within replicate blocks to reduce thermal, DVFS, cache, and background-load confounding.

The physical counter must be read immediately before and after each frozen batch, with counter wrap handling specified before treatment results are observed.

## 7. Transfer-relevance moderator

The V0–V2 transfer tiers remain frozen as a moderator. V3 may report energy contrasts by tier, but no universal monotone relationship is assumed.

## 8. Missingness and measurement failure

No imputation is permitted.

A batch is `NOT_IDENTIFIED` if:

- the energy counter cannot be read before or after the batch;
- units cannot be established;
- counter wrap cannot be resolved;
- another process/device contribution makes the physical-energy boundary uninterpretable under the frozen isolation rule.

If the preregistered minimum identified replicate count is not met, V3 as a whole is `NOT_IDENTIFIED`.

## 9. Scope of authority

A positive V3 result would support only:

> In the frozen heterogeneous executable correction environment and on the measured hardware/energy boundary, persistent validated lineage reduced measured physical energy while preserving the same warranted correction criterion.

It would not establish general AI energy efficiency, GPU/LLM savings, provider-scale savings, or SSI core theory.
