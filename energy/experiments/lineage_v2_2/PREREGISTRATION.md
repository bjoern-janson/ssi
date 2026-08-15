# Lineage Corrective Economy V2.2 — Gated Cost-Aware Router Preregistration

## Status

**FROZEN BEFORE ANY V2.2 TREATMENT RUN.**

V2.2 is the final experiment in the V2.x routing branch. It tests one intervention only: whether a cheap invocation gate can avoid the net-overhead failure observed in V2.1 by invoking the already-frozen `q/c` router only when expected candidate-work savings justify its incremental routing cost.

After V2.2 adjudication, the routing branch closes. No V2.3 threshold tuning, feature search, router redesign, or rescue experiment is licensed from the V2.2 outcome.

V2.2 does not modify SSI core theory, Axis I, V0–V2 results, or the V3 physical-energy measurement boundary.

## 1. Frozen contrast

Both arms preserve the same validated lineage and receive the same paired held-out challenges.

- **S — similarity-only:** the frozen V2/V2.1 similarity router.
- **G — gated cost-aware:** first computes the same similarity distances and similarity ordering. It then applies one frozen gate. If the gate is closed, it uses the similarity order. If the gate opens, it invokes the unchanged V2.1 `q/c` cost-aware ordering.

The only treatment difference is whether the frozen gate condition triggers the already-defined cost-aware ordering.

Candidate implementations, intrinsic cost field, lineage contents, validator, correction-quality contract, payload, and challenge generator are treatment-invariant.

## 2. Frozen executable substrate

V2.2 imports the committed V2.1 runner as its executable substrate and aborts unless its Git blob SHA is exactly:

`e3e609dae6dc604b460623462f7c1bca666f22d5`

Thus the 12 heterogeneous reversible candidate repair programs, exact validator, proposal mapping, beta calibration procedure, and frozen V2 candidate-cost field are inherited byte-for-byte rather than reimplemented.

Frozen V2 cost field in nanoseconds:

`[8452.0, 12609.0, 5128.0, 9023.0, 12499.0, 12449.0, 34941.0, 15943.5, 22007.5, 45988.0, 57225.0, 43765.0]`

## 3. Gate feature

The gate may use exactly one feature:

\[
d_{\min}(x,\Lambda)=\min_i d_i(x,\Lambda),
\]

where `d_i` is the same per-mechanism minimum normalized Hamming distance already computed by the similarity router.

No hidden transfer tier, true mechanism, candidate outcome, measured runtime from the current episode, proposal log loss, or post-treatment variable may enter the gate.

The gate therefore adds no new representation beyond information already produced by the cheap similarity router.

## 4. Frozen threshold calibration from V2.1 only

V2.1 is calibration data; V2.2 uses fresh worlds.

Admissible threshold grid:

\[
\tau\in\{0/32,1/32,\ldots,32/32\}.
\]

For each V2.1 episode, reconstruct the similarity and `q/c` candidate orders from the frozen V2.1 seeds and lineage state. Using the frozen V2 candidate-cost field, define the predicted candidate-work contrast for invoking `q/c` rather than similarity:

\[
\widehat{\Delta C}_{\rm eval,k}
=
\sum_{j\in J_{q/c,k}}\hat c_j
-
\sum_{j\in J_{S,k}}\hat c_j.
\]

Charge the V2.1 mean incremental routing cost:

\[
\widehat C_{\rm route,inc}
=78109.79361979167-70347.36344401042
=7762.43017578125\ \mathrm{ns}.
\]

For threshold \(\tau\), the calibration objective is

\[
\widehat\Delta(\tau)
=
\frac1K\sum_k
\mathbf 1[d_{\min,k}\ge\tau]
\left(
\widehat{\Delta C}_{\rm eval,k}
+
\widehat C_{\rm route,inc}
\right).
\]

Choose the threshold minimizing this **predicted** net contrast. Realized V2.1 total-CPU outcomes are not used in the objective.

Frozen calibration result:

\[
\boxed{\tau=11/32=0.34375.}
\]

At this threshold, the gate would have opened on 267 of 6144 V2.1 episodes (4.3457%), with predicted mean net contrast `-261.842 ns/episode` over all episodes.

No V2.2 outcome may change this threshold.

## 5. Frozen gate

\[
\boxed{
\mathrm{USE}_{q/c}(x)
\iff
d_{\min}(x,\Lambda)\ge0.34375.
}
\]

If false, G uses the already-computed similarity order.

If true, G computes the same V2.1 proposal

\[
q_\Lambda(i\mid x)\propto e^{-\beta d_i}
\]

and ranks candidates by

\[
\frac{q_\Lambda(i\mid x)}{\hat c_i}.
\]

The gate itself and any additional `q/c` computation are inside G's measured routing cost.

## 6. Fresh held-out worlds

- Master seed: `20260823`.
- Bootstrap seed: `20260824`.
- Independent worlds: `64`.
- Held-out episodes per world: `96`.
- Candidate mechanisms: `12`, each appearing exactly `8` times/world.
- Signature dimension: `32` bits.
- Warm-up lineage examples/mechanism: `2`.
- Warm-up bit-flip probability: `0.10`.
- Transfer tiers: exactly `48 × 0.15`, `32 × 0.25`, `16 × 0.35` per world.
- Payload length: `16384 uint8` elements.
- Held-out signatures cannot exactly duplicate an already available lineage signature.

These worlds are distinct from V2.1 and are not used in threshold calibration.

## 7. Correction-quality contract

Unchanged from V2/V2.1:

\[
H_{\rm recover}=1,
\quad
R_{\rm collateral}=0,
\quad
R_{\rm reopen}=1,
\quad
\mathrm{Auth}=1.
\]

Both arms use the same exact validator and commit only after exact restoration of the clean payload.

Compute economy cannot rescue a quality failure.

## 8. Accounting boundary

Primary metric: `time.process_time_ns()`.

Secondary: `time.perf_counter_ns()`.

For each arm:

\[
C_{\rm total}
=
C_{\rm route}
+C_{\rm candidate\ eval}
+C_{\rm lineage\ update}.
\]

For G, `C_route` includes:

1. the same distance computation and similarity sort as S;
2. evaluation of the threshold gate;
3. when invoked, proposal construction, division by the frozen cost field, and the additional cost-aware sort.

Thus the optimization layer is priced inside the surface it optimizes.

Pre-holdout beta calibration remains outside the per-episode primary accounting exactly as in V2.1 and is reported separately as infrastructure timing; it cannot determine the primary adjudication.

Execution order alternates G-first / S-first by episode.

## 9. Primary estimand

For episode \(k\):

\[
\Delta C_{{\rm total},k}^{G-S}
=C_{{\rm total},G,k}-C_{{\rm total},S,k}.
\]

World-level means over 96 paired episodes are the inferential units.

Primary hypothesis:

\[
\mathbb E[\Delta C_{\rm total}^{G-S}]<0.
\]

## 10. Secondary diagnostics

Report, without changing adjudication:

- gate invocation fraction overall and by transfer tier;
- candidate-evaluation CPU contrast;
- routing CPU contrast;
- candidate-count contrast;
- fraction G total-CPU cheaper;
- fraction where gate opens but G is more expensive;
- fraction where gate remains closed;
- beta calibration CPU as separate infrastructure cost;
- transfer-tier contrasts.

The transfer tiers remain moderators, not gate inputs.

## 11. Uncertainty

- Inference unit: world.
- Worlds: `64`.
- Paired world bootstrap: `20,000` resamples.
- Bootstrap seed: `20260824`.
- Percentile 95% confidence intervals.
- No iid episode bootstrap because lineage evolves within world.
- If fewer than 60 worlds are identified, V2.2 is `NOT_IDENTIFIED`.

## 12. Evidence ladder

### I. Gate nondegeneracy

Diagnostic only: report invocation rate. No minimum invocation rate is required for identification.

### II. Net gated executable economy

Supported iff the upper endpoint of the 95% world-bootstrap CI for

\[
\mathbb E[\Delta C_{\rm total}^{G-S}]
\]

is below zero.

### III. Correction-quality admissibility

Supported iff the frozen quality contract passes in every included world for both arms.

### V2.2 adjudication

`SUPPORTED_IN_FROZEN_GATED_ROUTING_SCOPE` iff II and III pass.

Otherwise, if measurement is identified, status is `NOT_SUPPORTED_IN_FROZEN_GATED_ROUTING_SCOPE`.

No threshold change or post-hoc subgroup restriction can rescue the result.

## 13. Scope and stopping rule

A positive result would support only:

> In the frozen heterogeneous executable repair environment, a preregistered nearest-lineage-distance gate calibrated on V2.1 improved net executable correction economy by selectively invoking the already-frozen cost-aware router while preserving the same correction-quality contract.

A negative result would localize failure to this specific invocation policy/threshold under this workload; it would not erase V2.1 proposal-quality or candidate-work findings.

**Regardless of outcome, V2.2 closes the routing branch.** Further router optimization requires a new program justification rather than V2.3/V2.4 escalation.
