# Lineage Corrective Economy V2.1 — Cost-Aware Router Preregistration

## Status

**FROZEN BEFORE EXECUTION.**

V2.1 is a router-level follow-up to V2. It does not modify SSI core theory, Axis I, the V2 candidate set, or the physical-energy claim.

V2 showed that persistent lineage can reduce total executed correction CPU even when candidate costs are heterogeneous. V2.1 asks a narrower algorithmic question:

> Given the same validated lineage and the same heterogeneous candidate procedures, does routing by a lineage-derived proposal probability divided by a frozen expected candidate cost reduce actual executable correction cost relative to similarity-only routing?

The intervention changes **ordering policy only**.

## 1. Treatment contrast

Both arms preserve the same validated lineage and see the same paired held-out failures.

- **S — similarity-only router:** order candidate mechanisms by ascending nearest-lineage Hamming distance, as in V2.
- **C — cost-aware router:** derive a proposal distribution from those same lineage distances, then order by descending proposal-probability-per-frozen-expected-cost.

Both arms use identical:

- lineage contents and update rule;
- candidate repair implementations;
- held-out payloads and signatures;
- exact validator;
- correction-quality contract;
- transfer-relevance tiers;
- candidate-cost metadata;
- stopping rule after exact warranted validation.

Lineage may affect routing only. Candidate implementation, intrinsic cost, correctness, validator, and acceptance criteria are treatment-invariant.

## 2. Fresh held-out world generator

V2.1 uses a fresh seed so no V2.1 treatment challenge is reused from V2.

- Master seed: `20260821`.
- Bootstrap seed: `20260822`.
- Independent replicate worlds: `64`.
- Candidate mechanisms per world: `12`.
- Binary signature dimension: `32`.
- Warm-up lineage examples per mechanism: `2`.
- Warm-up bit-flip probability: `0.10`.
- Held-out episodes per world: `96`.
- Each mechanism occurs exactly `8` times per world.
- Transfer tiers per world:
  - `48` episodes at bit-flip probability `0.15`;
  - `32` episodes at `0.25`;
  - `16` episodes at `0.35`.
- Held-out signatures are regenerated if exactly equal to any lineage signature already available to either arm.
- Payload length: `16,384` uint8 elements.

The 12 heterogeneous reversible repair pipelines are exactly the V2 pipelines.

## 3. Frozen lineage-derived proposal model

For a current signature `x`, let `d_i(x, Lambda)` be the minimum normalized Hamming distance between `x` and stored validated lineage signatures labelled mechanism `i`.

Define

\[
q_\Lambda(i\mid x;\beta)
=
\frac{\exp(-\beta d_i)}{\sum_j\exp(-\beta d_j)}.
\]

For any fixed positive `beta`, sorting by descending `q` is identical to V2 similarity sorting by ascending distance. Therefore the proposal transformation alone does not change the similarity-only router.

### Pre-holdout temperature calibration

Within each world, before held-out evaluation:

- generate `6` independent calibration signatures per mechanism;
- calibration noise sequence per mechanism is `[0.15, 0.15, 0.25, 0.25, 0.35, 0.35]`;
- calibration examples are never added to lineage;
- fit `beta` only on these pre-holdout labelled calibration examples;
- beta grid is `[0, 1, 2, 4, 8, 12, 16, 24, 32, 48, 64]`;
- select the beta minimizing mean multiclass log loss of `q_Lambda`; ties choose the smaller beta.

No V2.1 held-out outcome may alter beta.

## 4. Frozen candidate cost field

V2.1 does **not** re-estimate candidate costs from its own treatment outcomes.

The cost-aware router consumes the already-frozen V2 B-only median candidate-evaluation CPU times, in nanoseconds:

| candidate | frozen expected cost ns |
|---:|---:|
| 0 | 8452.0 |
| 1 | 12609.0 |
| 2 | 5128.0 |
| 3 | 9023.0 |
| 4 | 12499.0 |
| 5 | 12449.0 |
| 6 | 34941.0 |
| 7 | 15943.5 |
| 8 | 22007.5 |
| 9 | 45988.0 |
| 10 | 57225.0 |
| 11 | 43765.0 |

These values were frozen by V2 before V2.1 execution and are not updated after observing V2.1 timings.

V2.1 therefore tests routing **conditional on an already available cost field**. Acquisition cost for learning the cost field is outside the primary V2.1 estimand and is not claimed to be free in general.

## 5. Frozen router policies

### S — similarity-only

Compute `d_i` and sort by ascending distance. Distance ties use a deterministic episode-specific pseudorandom tie rank independent of the true mechanism and candidate runtime.

### C — cost-aware proposal router

Using the same `d_i` and calibrated beta, compute `q_i = q_Lambda(i|x)`.

Define

\[
\operatorname{priority}_i
=
\frac{q_i}{\hat c_i},
\]

where `hat c_i` is the frozen V2 expected candidate cost.

Sort by descending priority. Exact priority ties use the same deterministic episode-specific tie rank.

Under exact mutually exclusive validation and perfectly calibrated probabilities/costs, the pairwise exchange criterion motivates `p_i/c_i`. V2.1 does **not** assume `q_i` or `hat c_i` are perfect; it tests whether this approximation improves actual executable correction economy.

## 6. Identical correction-quality contract

Both routers execute candidate repair programs until the common exact validator reproduces the clean held-out payload.

For every episode and both arms:

- `H_recover = 1` iff a warranted repair is found within 12 candidate evaluations;
- `R_collateral = 0` iff no invalid repair is committed;
- `R_reopen = 1` while untested/failed alternatives remain available;
- `Auth = 1` iff commitment occurs only after exact validation.

Any quality violation fails admissibility. CPU savings cannot rescue it.

## 7. Executed-work accounting boundary

Primary metric: `time.process_time_ns()`.
Secondary: `time.perf_counter_ns()`.

For both arms:

\[
C_{\rm total}
=
C_{\rm route}
+
C_{\rm candidate\ evals}
+
C_{\rm lineage\ update}.
\]

Routing cost includes all computation required to construct that arm's ordering. Candidate evaluation includes execution of the candidate repair and exact validator. Both arms separately maintain identical lineage copies and pay their own lineage-update CPU.

Challenge generation/corruption is outside both treatment intervals.

Execution order alternates C-first / S-first by episode.

## 8. Proposal-quality diagnostic

For each held-out episode, record the cost-aware arm's pre-evaluation proposal probability assigned to the true mechanism.

World-level held-out proposal log loss is

\[
LL_q=-\frac{1}{K}\sum_k \log q_\Lambda(i_k^\star\mid x_k).
\]

Uniform-reference log loss is

\[
LL_{\rm uniform}=\log 12.
\]

Proposal quality is supported iff the upper endpoint of the world-bootstrap 95% CI for mean `LL_q` is below `log(12)`.

This tests the first mechanism link `Lambda -> q_Lambda`; it is not by itself an economy result.

## 9. Cost-field transfer gate

V2.1 must verify that the frozen V2 cost field still tracks the current execution platform.

Using **S-arm candidate timings only**, compute the median observed CPU time for each candidate label across all times it is tested.

Define:

- `rho_cost`: Spearman rank correlation between frozen V2 cost medians and V2.1 S-arm observed candidate medians;
- `H_current = max_j median(C_j) / min_j median(C_j)` from V2.1 S-arm timings.

The cost-field transfer gate passes iff:

\[
rho_{\rm cost}\ge0.80
\quad\land\quad
H_{\rm current}\ge2.0.
\]

If this gate fails, the cost-aware routing test is `NOT_IDENTIFIED_FOR_COST_FIELD_TRANSFER`; do not reinterpret a failure as evidence that `p/c` routing is intrinsically ineffective.

## 10. Primary estimands

For held-out episode `k`:

\[
\Delta n_k=n_{C,k}-n_{S,k},
\]

\[
\Delta C_{{\rm eval},k}
=C_{{\rm eval},C,k}-C_{{\rm eval},S,k},
\]

\[
\Delta C_{{\rm total},k}
=C_{{\rm total},C,k}-C_{{\rm total},S,k}.
\]

World-level means over 96 paired episodes are the inferential units.

The primary economy hypothesis is

\[
\mathbb E[\Delta C_{\rm total}]<0.
\]

Candidate count is diagnostic, not constitutive of success.

## 11. Frozen uncertainty procedure

- Inference unit: replicate world.
- Worlds: `64`.
- Paired-bootstrap resamples: `20,000`.
- Bootstrap seed: `20260822`.
- Resample world-level paired summaries with replacement.
- Percentile 95% confidence intervals.
- No iid episode bootstrap because lineage evolves within world.
- If fewer than 60 worlds are identified, V2.1 is `NOT_IDENTIFIED`.

## 12. Evidence ladder

### I. Lineage proposal quality

Supported iff mean held-out proposal log loss beats uniform with the frozen CI rule in section 8.

### II. Cost-field transfer

Supported iff `rho_cost >= 0.80` and `H_current >= 2.0`.

### III. Heterogeneous work routing

Supported iff the upper endpoint of the 95% CI for

\[
\mathbb E[\Delta C_{\rm eval}]
\]

is below zero.

### IV. Net executable router economy

Supported iff the upper endpoint of the 95% CI for

\[
\mathbb E[\Delta C_{\rm total}]
\]

is below zero.

This includes each router's own ordering computation and lineage update.

### V. Admissibility

Supported iff the correction-quality contract passes for both routers in every included world.

### V2.1 adjudication

`SUPPORTED_IN_FROZEN_COST_AWARE_ROUTING_SCOPE` iff I, II, IV, and V are supported.

Stage III is mechanistic support but is not independently required if total executable economy passes; a router may spend more candidate-evaluation CPU yet still reduce total cost only in unusual routing-overhead configurations. Both are reported.

## 13. Adversarial and diagnostic patterns to retain

Report overall and by transfer tier:

- `n_C > n_S` but `C_total_C < C_total_S` — cost-aware routing tests more candidates yet is cheaper;
- `n_C < n_S` but `C_total_C > C_total_S` — fewer candidates yet more expensive;
- fraction C total-CPU cheaper;
- mean delta candidates;
- mean delta candidate-evaluation CPU;
- mean delta total CPU.

Do not smooth these away.

## 14. Transfer relevance

The frozen `0.15`, `0.25`, `0.35` tiers remain moderators only. No universal monotonic economy law is assumed.

## 15. STOP / bypass is not part of V2.1

V2.1 forces both routers to use lineage on every held-out episode. It does **not** introduce a bypass/STOP gate. Selective use of lineage is reserved for a later experiment so that V2.1 changes only the ordering objective.

## 16. Authority boundary

A positive V2.1 result supports only:

> In the frozen heterogeneous executable repair environment, a lineage-derived proposal distribution combined with a previously measured candidate-cost field produced lower total correction CPU than similarity-only lineage routing while preserving the exact same warranted correction criterion.

It does not establish:

- physical energy reduction;
- that candidate-cost estimation is free;
- universal optimality of `q/c` routing;
- general AI energy efficiency;
- Axis I;
- SSI core theory.

No post-hoc change to beta calibration, cost field, router formula, challenge generator, candidate pipelines, accounting boundary, or evidence rules is permitted after treatment results are observed.
