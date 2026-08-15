# Lineage Corrective Economy V2 — Preregistration

## Status

**FROZEN BEFORE EXECUTION.**

V2 is the next executable mechanism test under `energy/`. It preserves the V1 A/B lineage intervention but removes the remaining fixed-cost candidate-evaluation convenience.

V2 asks whether persistent validated lineage can reduce the cost of **meaningful heterogeneous corrective computation**, where:

\[
n_{\rm tested}\downarrow
\not\Rightarrow
C_{\rm correction}\downarrow
\]

by construction.

A positive result has authority only inside this executable synthetic repair-program environment. It is not evidence about physical energy in joules, GPU/LLM workloads, or SSI core theory.

## 1. Treatment contrast

Two otherwise identical correcting agents receive the same paired held-out failures.

- **A — lineage preserved:** retains validated failure signatures and mechanism labels across episodes and uses them only to order candidate repair programs.
- **B — lineage unavailable:** receives no persistent correction lineage and tests the same candidate repair programs in a deterministic episode-specific pseudorandom order.

Lineage may affect **ordering only**. It may not alter candidate implementation, intrinsic cost, validator, correctness, payload, correction threshold, or acceptance rule.

## 2. Frozen world and challenge generator

- Master seed: `20260815`.
- Bootstrap seed: `20260818`.
- Independent replicate worlds: `64`.
- Candidate mechanisms per world: `12`.
- Signature dimension: `32` binary features.
- Warm-up lineage examples per mechanism: `2`.
- Warm-up signature bit-flip probability: `0.10`.
- Held-out episodes per world: `96`.
- Each mechanism occurs exactly `8` times per world.
- Transfer-relevance tiers are the same frozen multiset as V0/V1:
  - `48` episodes at signature bit-flip probability `0.15`;
  - `32` episodes at `0.25`;
  - `16` episodes at `0.35`.
- Held-out signatures are regenerated if they exactly match any lineage signature already available to A.
- Payload length: `16384` unsigned 8-bit elements.
- Each episode receives a fresh clean payload generated independently of treatment ordering.

The signature predicts the latent repair family. The actual payload is corrupted by that repair family's frozen reversible transformation pipeline.

## 3. Frozen heterogeneous candidate repair programs

All 12 candidate programs are fixed before execution and are identical for A and B.

Primitive reversible transformations:

1. `reverse`
2. `roll_113`
3. `xor_a5`
4. `add_17_mod256`
5. `rotl3`
6. `nibble_swap`
7. `pair_swap`
8. `block_reverse_64`
9. `matrix_transpose_128`
10. `affine_5x_plus_7_mod256`
11. `prefix_xor`
12. `delta_mod256`

The 12 mechanism pipelines are:

| mechanism | corruption pipeline | repair pipeline depth |
|---:|---|---:|
| 0 | `reverse` | 1 |
| 1 | `roll_113` | 1 |
| 2 | `xor_a5` | 1 |
| 3 | `add_17_mod256` | 1 |
| 4 | `rotl3` | 1 |
| 5 | `nibble_swap` | 1 |
| 6 | `pair_swap -> xor_a5` | 2 |
| 7 | `block_reverse_64 -> add_17_mod256` | 2 |
| 8 | `matrix_transpose_128 -> roll_113 -> xor_a5` | 3 |
| 9 | `affine_5x_plus_7_mod256 -> pair_swap -> reverse` | 3 |
| 10 | `prefix_xor -> nibble_swap -> roll_113` | 3 |
| 11 | `delta_mod256 -> matrix_transpose_128 -> block_reverse_64 -> xor_a5` | 4 |

The repair program applies the exact mathematical inverse primitives in reverse order.

Candidate evaluation therefore consists of:

\[
\text{corrupted payload}
\rightarrow
\text{candidate repair program}
\rightarrow
\text{common exact validator}.
\]

The common validator is `numpy.array_equal(candidate_output, clean_payload)`.

A candidate is warranted iff the validator returns true. No candidate label is accepted by construction alone.

## 4. Heterogeneity gate

V2 is intended to break the V1 near-monotonic relation between candidate count and CPU work.

Using **B-only candidate-evaluation timings**, compute the median measured candidate-evaluation CPU time for each of the 12 candidate labels over all times that label is actually tested.

Define:

\[
H_C=
\frac{\max_j \operatorname{median}(C_j)}
{\min_j \operatorname{median}(C_j)}.
\]

The heterogeneous-work gate passes iff:

\[
H_C \ge 2.0.
\]

If the gate fails, V2 is `NOT_IDENTIFIED_FOR_HETEROGENEOUS_COST` even if A uses less CPU overall. This prevents a positive result from being interpreted as evidence under heterogeneous correction costs when effective costs were nearly homogeneous on the execution platform.

## 5. Frozen ordering policies

### A — lineage-preserved

For each mechanism label, A computes the minimum normalized Hamming distance between the current failure signature and all validated lineage signatures carrying that label.

Candidate labels are sorted by ascending minimum distance.

Distance ties are broken by a deterministic episode-specific pseudorandom permutation independent of the true mechanism and independent of candidate runtime.

### B — lineage-unavailable

B uses a deterministic episode-specific pseudorandom permutation independent of the true mechanism, failure signature, candidate runtime, and A's ordering.

Candidate intrinsic cost is never used by either ordering policy.

## 6. Frozen correction-quality contract

Both agents use the same exact validator and stop only when a candidate repair exactly reproduces the clean held-out payload.

For every episode:

- `H_recover = 1` iff the correct repair is identified within 12 candidate evaluations;
- `R_collateral = 0` iff no incorrect repair is committed;
- `R_reopen = 1` because failed alternatives remain available until warranted identification;
- `Auth = 1` iff commitment occurs only after exact validation.

The frozen admissibility contract is:

\[
H_{\rm recover}=1,\qquad
R_{\rm collateral}=0,\qquad
R_{\rm reopen}=1,\qquad
\mathrm{Auth}=1.
\]

Energy/compute success cannot rescue any quality-contract violation.

## 7. Executed-work accounting boundary

Primary work metric: `time.process_time_ns()`.

Secondary metric: `time.perf_counter_ns()`.

For A, total measured correction CPU includes:

\[
C_A=
C_{\rm retrieve}
+
C_{\rm candidate\ evals}
+
C_{\rm lineage\ update}.
\]

For B:

\[
C_B=
C_{\rm candidate\ evals}.
\]

Each candidate-evaluation timing includes both:

- execution of that candidate's repair program on the corrupted payload;
- the common exact validation call.

Payload generation and corruption are challenge-generation costs and are outside both treatment arms.

The same candidate program on the same episode payload is treatment-invariant; only its position in the tested sequence may differ.

Execution order alternates A-first / B-first by episode to reduce systematic timing-order bias.

## 8. Frozen estimands

For episode \(k\):

\[
\Delta n_k=n_{A,k}-n_{B,k},
\]

\[
\Delta C_{{\rm eval},k}
=
C_{{\rm candidate\ evals},A,k}
-
C_{{\rm candidate\ evals},B,k},
\]

\[
\Delta C_{{\rm total},k}
=
C_{{\rm total},A,k}
-
C_{{\rm total},B,k}.
\]

World-level means over the same 96 paired episodes are the inferential units.

## 9. Frozen uncertainty procedure

- Inference unit: replicate world.
- World count: `64`.
- Paired bootstrap resamples: `20,000`.
- Bootstrap seed: `20260818`.
- Resample worlds with replacement.
- Report percentile 95% confidence intervals.
- No iid episode bootstrap because A's lineage evolves within world.

If fewer than 60 worlds are identified, V2 is `NOT_IDENTIFIED`.

## 10. Frozen evidence ladder

### I. Search reuse

Supported iff the upper endpoint of the 95% CI for

\[
\mathbb E[\Delta n]
\]

is below zero.

### II. Heterogeneous work avoidance

Supported iff the heterogeneity gate \(H_C\ge2.0\) passes **and** the upper endpoint of the 95% CI for

\[
\mathbb E[\Delta C_{\rm eval}]
\]

is below zero.

### III. Net executable corrective economy

Supported iff the upper endpoint of the 95% CI for

\[
\mathbb E[\Delta C_{\rm total}]
\]

is below zero.

This includes A's lineage retrieval and update overhead.

### IV. Admissibility

Supported iff the frozen correction-quality contract passes for both A and B in every included world.

### V2 adjudication

`SUPPORTED_IN_FROZEN_HETEROGENEOUS_EXECUTABLE_SCOPE` iff II, III, and IV are all supported.

Stage I is diagnostic: V2 may in principle show net economy even without fewer candidates if ordering shifts toward cheaper candidates, although A is not allowed to use cost information directly.

## 11. Adversarial failure patterns to retain

V2 explicitly allows and records:

\[
n_A<n_B
\quad\land\quad
C_{{\rm eval},A}>C_{{\rm eval},B},
\]

and

\[
n_A<n_B
\quad\land\quad
C_{{\rm total},A}>C_{{\rm total},B}.
\]

These are the key heterogeneous-cost failure modes.

Report their episode fractions overall and by transfer-relevance tier. Do not smooth them away.

## 12. Transfer-relevance moderator

The same tiers `0.15`, `0.25`, `0.35` remain preregistered moderators.

For each tier report:

- mean \(\Delta n\);
- mean \(\Delta C_{\rm eval}\);
- mean \(\Delta C_{\rm total}\);
- fraction A total-CPU cheaper;
- fraction with `n_A < n_B` but `C_eval_A > C_eval_B`.

The directional hypothesis is:

\[
r\downarrow
\Rightarrow
\text{lineage routing quality}\downarrow,
\]

but V2 does not assume or fit a universal monotone function or continuous crossover \(r^\star\).

## 13. Missingness and interpretation

No imputation.

`NOT_IDENTIFIED` is distinct from zero and from a negative result.

A positive V2 result licenses only:

> In the frozen heterogeneous executable repair-program environment, persistent validated lineage changed candidate ordering in a way that reduced measured candidate-repair CPU work and total correction CPU after lineage retrieval/update overhead, while preserving the same exact correction criterion.

It does **not** establish:

- physical energy reduction in joules;
- GPU/LLM energy savings;
- general AI corrective economy;
- that all lineage systems are beneficial;
- that transfer relevance has a universal monotone relationship with value;
- Axis I;
- SSI core theory.

No post-hoc change to candidate pipelines, cost heterogeneity, transfer tiers, accounting boundary, or acceptance contract is permitted after treatment results are observed.
