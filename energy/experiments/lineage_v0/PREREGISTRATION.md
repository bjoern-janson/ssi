# Lineage Corrective Economy V0 — Preregistration

## Status

**FROZEN BEFORE EXECUTION.**

This is the first executable synthetic mechanism test under `energy/`. It does not alter SSI core theory, Axis I, or the definition of corrective topology.

The experiment tests only whether preserved validated lineage can reduce a frozen compute-cost proxy for correction on related-but-nonidentical held-out failures, after charging lineage infrastructure.

A positive result has authority only inside this synthetic search/retrieval cost model. It is not evidence about physical joules or general AI energy use.

## 1. Treatment contrast

Two otherwise identical correction agents receive the same paired held-out challenges.

- **A — lineage preserved:** retains validated correction signatures and their mechanism labels across episodes.
- **B — lineage unavailable:** receives no persistent correction lineage between episodes.

Both agents use the same candidate mechanisms, exact diagnostic probe, revision rule, validation rule, recovery rule, correction horizon, and phase-cost schedule.

The intended mechanism remains

$$
\Lambda_{\rm preserved}
\overset{?}{\longrightarrow}
E_{\rm rediscover}\downarrow
\overset{?}{\longrightarrow}
J_{\rm corr}\downarrow
\overset{?}{\longrightarrow}
N_\Lambda>0.
$$

Every arrow is adjudicated separately.

## 2. Frozen world generator

- Master seed: `20260815`.
- Independent replicate worlds: `64`.
- Mechanism families per world: `12`.
- Binary signature dimension: `32`.
- Warm-up lineage examples per mechanism: `2`.
- Warm-up bit-flip probability: `0.10`.
- Held-out correction episodes per world: `96`.
- Each mechanism occurs exactly `8` times in held-out evaluation; order is shuffled within world.
- Held-out noise tiers per world are a shuffled multiset of:
  - `48` episodes at bit-flip probability `0.15`;
  - `32` episodes at bit-flip probability `0.25`;
  - `16` episodes at bit-flip probability `0.35`.
- A held-out signature is regenerated if it is exactly equal to any lineage signature already available to A. Thus held-out failures are related to prior failures but cannot be exact replay.

Each world receives independently generated mechanism prototypes and episode noise from the frozen seed sequence.

## 3. Frozen lineage contents and update rule

Before held-out evaluation, A receives the `24` validated warm-up signatures (`12` mechanisms × `2` examples). B receives no persistent lineage.

After each warranted held-out correction:

- A appends the validated held-out signature and mechanism label to lineage;
- B discards the episode-specific correction record before the next episode.

No unvalidated or failed mechanism assignment may enter A's lineage.

## 4. Frozen correction policy

### A — lineage-preserved ordering

For the current held-out signature, A computes for each mechanism family the minimum normalized Hamming distance to any stored validated lineage signature carrying that mechanism label.

Mechanisms are tested in ascending distance. Distance ties are broken by a deterministic episode-specific pseudorandom permutation independent of the true mechanism label.

### B — lineage-unavailable ordering

B tests mechanism families in a deterministic episode-specific pseudorandom permutation independent of the true mechanism label and held-out signature.

### Shared warranted probe

Both agents test mechanisms sequentially. The diagnostic probe is exact: a tested candidate either matches the true latent mechanism or does not. The agent may revise/commit only after the exact probe identifies the true mechanism.

Maximum candidate tests per episode: `12`.

This deliberately fixes correction quality so that V0 isolates corrective traversal cost rather than mixing efficiency with accuracy differences.

## 5. Frozen correction-quality contract

For every episode and both agents:

- `H_recover = 1` iff the true mechanism is identified within 12 tests;
- `R_collateral = 0` iff no incorrect mechanism is committed;
- `R_reopen = 1` because untested/failed alternatives remain available until warranted identification;
- `Auth = 1` iff commitment occurs only after the exact probe identifies the true mechanism.

The admissibility contract is

$$
H_{\rm recover}=1,
\qquad
R_{\rm collateral}=0,
\qquad
R_{\rm reopen}=1,
\qquad
\mathrm{Auth}=1.
$$

Any implementation violation of this contract fails the V0 run; energy savings cannot rescue it.

## 6. Frozen correction-cost proxy

The units below are **synthetic compute-cost units**, not joules.

For each correction episode:

- detection: `1.0`;
- diagnosis: `1.0` per mechanism candidate tested;
- probe: `2.0` per mechanism candidate tested;
- revision: `2.0` once, after warranted identification;
- validation: `3.0` once;
- recovery: `1.0` once.

Therefore, for `n_tested` candidates,

$$
J_{\rm corr}=7+3n_{\rm tested}.
$$

Rediscovery is an attribution variable, not an additional charge:

$$
E_{\rm rediscover}
=3\max(n_{\rm tested}-1,0).
$$

It measures correction search spent before the finally warranted candidate.

## 7. Frozen lineage-infrastructure cost

Only A pays lineage-specific infrastructure.

- record formation/storage on insertion: `0.10` per validated record;
- maintenance: `0.005 × current lineage record count` per held-out episode;
- retrieval/indexing: `0.20 + 0.01 × current lineage record count` per held-out episode.

The `24` warm-up records are charged their formation/storage cost before held-out episode 1. Each newly appended held-out record is charged on insertion.

B has zero lineage-infrastructure cost because the experiment isolates the incremental cost of persistent lineage. All shared solver costs are already inside `J_corr`.

## 8. Frozen estimands

For episode `k`,

$$
\Delta J_{\rm corr,k}=J_{\rm corr,k}^{A}-J_{\rm corr,k}^{B}.
$$

For a world after `K` episodes,

$$
G_\Lambda(K)
=\sum_{k=1}^{K}
\left(J_{\rm corr,k}^{B}-J_{\rm corr,k}^{A}\right).
$$

Let `E_Lambda,infrastructure(K)` contain all A-only storage, maintenance, and retrieval charges through episode `K`. Then

$$
N_\Lambda(K)=G_\Lambda(K)-E_{\Lambda,\rm infrastructure}(K).
$$

The amortization crossover in each world is

$$
K^\star=\min\{K:N_\Lambda(K)>0\}.
$$

If no crossover occurs by 96 episodes, report `NOT_CROSSED`; do not impute a value.

## 9. Frozen uncertainty procedure

Inference unit: replicate world.

For each of the 64 worlds, retain paired A/B totals and means over the same 96 challenges.

- Paired-bootstrap resamples: `20,000`.
- Bootstrap seed: `20260816`.
- Resample the 64 world-level paired results with replacement.
- Report percentile 95% confidence intervals.

No episode-level iid bootstrap will be used because A's lineage evolves across episodes within a world.

## 10. Frozen evidence ladder

### I. Reuse

Supported iff the upper endpoint of the 95% bootstrap CI for

$$
\mathbb E[E_{\rm rediscover}^{A}-E_{\rm rediscover}^{B}]
$$

is below zero.

### II. Gross economy

Supported iff the upper endpoint of the 95% bootstrap CI for

$$
\mathbb E[\Delta J_{\rm corr}]
$$

is below zero.

### III. Net economy

Supported iff the lower endpoint of the 95% bootstrap CI for world-level

$$
N_\Lambda(96)
$$

is above zero.

### IV. Admissible net economy

Supported iff I–III are supported and the frozen correction-quality contract passes for both A and B in every included world.

Only IV supports the V0 SSI corrective-economy mechanism.

## 11. Missingness and execution failure

No imputation is permitted.

- Any missing phase cost, missing mechanism label, or malformed episode causes that world to be `NOT_IDENTIFIED` and excluded from numerical aggregation while being reported explicitly.
- If fewer than 60 of 64 worlds remain identified, the entire V0 result is `NOT_IDENTIFIED`.
- `NOT_IDENTIFIED` is neither zero effect nor negative effect.

## 12. Frozen scope of authority

A positive result supports only this statement:

> In the frozen synthetic family-classification correction environment, persistent validated lineage reduced a predefined correction-search cost proxy enough to exceed its predefined storage, maintenance, and retrieval costs while preserving the exact same warranted correction criterion.

It does **not** establish:

- physical energy savings in joules;
- general AI inference savings;
- that all lineage is economically beneficial;
- that corrective topology generally lowers energy;
- Axis I;
- SSI core theory.

Any expansion requires a new freeze and independent experiment.
