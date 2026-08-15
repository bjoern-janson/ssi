# Lineage Corrective Economy V2.2 — Results

## Adjudication

**NOT_SUPPORTED_IN_FROZEN_GATED_ROUTING_SCOPE**

V2.2 is the final preregistered V2.x routing experiment. It tested whether a cheap nearest-lineage-distance gate could selectively invoke the already-frozen V2.1 `q/c` router and recover net executable economy relative to similarity-only routing.

The primary criterion did not pass. The routing branch is therefore closed by preregistration; no V2.3 threshold tuning or router rescue is licensed from this result.

## Frozen provenance

Authoritative execution occurred only after byte identity matched the committed Git blobs:

- V2.2 preregistration: `fdfeb8ec94b2f1f76fd6f97a00a5bae5c6a17239`;
- V2.2 gate calibration: `97f4591cda94e0bb4068b93e1093b93f6107ea3b`;
- V2.2 runner: `1cc32eeacf801c4ca57a50988fffdfd12a84c340`;
- imported frozen V2.1 runner substrate: `e3e609dae6dc604b460623462f7c1bca666f22d5`.

## Frozen sample

- fresh independent worlds: **64**;
- paired held-out episodes/world: **96**;
- total paired corrections: **6,144**;
- gate threshold: **11/32 = 0.34375**;
- correction-quality contract passed in every world: **True**.

## Gate transfer

The V2.1 calibration predicted a gate-open rate of `4.3457%` at the frozen threshold.

Fresh V2.2 observed:

- gate invocations: **276 / 6,144**;
- gate-open fraction: **4.4922%**.

Thus the activation frequency transferred closely. Economic selectivity did not.

## Primary result — total executable CPU

Mean total process CPU per correction:

- G, gated cost-aware: **108.008 µs**;
- S, similarity-only: **107.662 µs**;
- G − S: **+0.346 µs**;
- 95% paired world-bootstrap CI: **[-0.225, +0.927] µs**.

The preregistered support criterion required the full 95% CI to lie below zero. It does not.

Therefore:

\[
\boxed{\texttt{NOT\_SUPPORTED\_IN\_FROZEN\_GATED\_ROUTING\_SCOPE}}
\]

This result does not identify a reliable net benefit and also does not establish a reliable net harm, because the primary CI crosses zero.

## Decomposition

### Candidate count

- G: **1.573** candidates/episode;
- S: **1.550**;
- G − S: **+0.0226**;
- 95% CI: **[+0.0114,+0.0339]**.

As in V2.1, candidate count is not the economic objective.

### Candidate-evaluation work

- G: **37.810 µs**;
- S: **38.283 µs**;
- G − S: **-0.473 µs**;
- 95% CI: **[-1.011,+0.154] µs**.

The point estimate favors G at the candidate-work layer, but the interval includes zero. V2.2 therefore does not independently replicate a reliable candidate-work saving.

### Routing work

- G: **69.504 µs**;
- S: **68.671 µs**;
- G − S: **+0.833 µs**;
- 95% CI: **[+0.445,+1.229] µs**.

The gate plus occasional `q/c` invocation imposes a reliably positive routing overhead.

The observed decomposition is therefore:

\[
\Delta C_{\rm eval}\approx-0.473\ \mu s,
\qquad
\Delta C_{\rm route}\approx+0.833\ \mu s,
\]

which yields the small positive total point estimate.

## The gate failed at selection, not merely frequency

Among gate-open episodes only:

- mean G − S total CPU: **+2.614 µs**;
- G was cheaper on only **34.8%** of gate-open episodes.

The threshold therefore reproduced approximately the expected activation rate but did not identify episodes in which the expensive router repaid its cost.

Among gate-closed episodes, mean G − S total CPU was **+0.240 µs**, reflecting the small cost/noise of carrying the gate path even when no expensive routing was invoked.

## Transfer-tier diagnostics

| held-out flip p | gate-open | Δ candidates G−S | Δ route CPU | Δ eval CPU | Δ total CPU |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 0.39% | +0.0016 | +0.321 µs | +0.160 µs | **+0.481 µs** |
| 0.25 | 4.64% | +0.0186 | +0.577 µs | -0.467 µs | **+0.104 µs** |
| 0.35 | 16.50% | +0.0938 | +2.881 µs | -2.382 µs | **+0.426 µs** |

The gate correctly became more active as transfer difficulty increased, but the V2.1 hardest-tier net benefit did **not** replicate. Even at `p=0.35`, the mean total contrast was positive.

This is evidence against treating nearest-lineage distance alone as a sufficient estimate of the expected value of invoking cost-aware routing in this environment.

## Quality

The exact correction-quality contract passed for both arms in every included world:

\[
H_{\rm recover}=1,
\quad
R_{\rm collateral}=0,
\quad
R_{\rm reopen}=1,
\quad
\mathrm{Auth}=1.
\]

The failure is therefore localized to executable economy, not correction quality.

## Infrastructure diagnostic

The inherited pre-holdout beta calibration cost averaged:

- **6.497 ms/world**;
- **67.673 µs/episode** if naively amortized across 96 episodes.

By preregistration this infrastructure timing is excluded from the primary per-episode adjudication to preserve V2.1 accounting continuity. It is reported because a fully charged deployment would need to decide whether such proposal calibration is reusable across sufficiently many future corrections to amortize its cost.

Including it would not rescue V2.2; it would make G less economical.

## Earned localization

V2.1 established that lineage can support an informative proposal and that `q/c` routing can reduce heterogeneous candidate work while still losing net economy to routing overhead.

V2.2 tested one cheap invocation policy and found:

\[
\boxed{
\text{difficulty-triggered activation frequency transfers}
\not\Rightarrow
\text{economic value selection transfers}.
}
\]

The narrow gate

\[
d_{\min}\ge11/32
\]

is not supported as a net-economical invocation policy on fresh held-out worlds.

This does **not** erase:

- V2.1 proposal quality;
- V2.1 cost-field transfer;
- V2.1 candidate-work reduction;
- V0–V2 lineage-economy results.

It rejects only this frozen V2.2 gate as a reliable way to turn those ingredients into additional net savings.

## Routing branch closure

Per preregistration:

\[
\boxed{\text{V2.x routing branch closed after V2.2}.}
\]

No threshold retuning, additional gate features, V2.3, or post-hoc subgroup rescue is licensed from this experiment.

The physical-energy bridge remains separately open at V3 and remains `NOT_IDENTIFIED` until admissible physical-energy instrumentation is available.
