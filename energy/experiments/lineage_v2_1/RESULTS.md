# Lineage Corrective Economy V2.1 — Results

## Adjudication

**NOT_SUPPORTED_IN_FROZEN_COST_AWARE_ROUTING_SCOPE**

V2.1 compared the V2 similarity-only lineage router against a cost-aware router using

\[
\operatorname{priority}_i = \frac{q_\Lambda(i\mid x)}{\hat c_i},
\]

where `q_Lambda` is calibrated only from pre-holdout lineage examples and `hat c_i` is the frozen V2 candidate-cost field.

The result is a localized negative mechanism result: the cost-aware router reduced heterogeneous candidate-execution CPU, but its additional routing computation more than erased that gain on average.

## Frozen sample

- Replicate worlds: **64**
- Paired held-out episodes per world: **96**
- Total paired corrections: **6,144**
- Fresh V2.1 master seed: `20260821`
- Missing / unidentified worlds: **0**
- Correction-quality contract passed in every world: **True**

## I. Lineage proposal quality — supported

The lineage-derived proposal distribution was strongly informative.

Uniform-reference log loss:

\[
\log 12 = 2.4849.
\]

Observed held-out proposal log loss:

- mean: **0.6676**
- 95% world-bootstrap CI: **[0.6443, 0.6901]**

The entire CI is far below the uniform reference, so

\[
\Lambda \rightarrow q_\Lambda
\]

is supported in the frozen V2.1 proposal model.

The pre-holdout temperature calibration selected median `beta = 24`; 55/64 worlds selected `24` and 9/64 selected `32`.

## II. Frozen cost-field transfer — supported

The V2 B-only median candidate costs were frozen before V2.1 and reused unchanged.

On V2.1 S-arm timings:

- Spearman rank correlation with frozen V2 costs: **1.000**
- current candidate-cost heterogeneity ratio: **11.514×**

The preregistered gate required `rho >= 0.80` and heterogeneity `>= 2×`; both passed.

So failure cannot be localized to loss of the heterogeneous cost field on the current execution platform.

## III. Heterogeneous candidate-work routing — supported

Cost-aware routing tested slightly **more** candidates on average:

- C: **1.6255** candidates / episode
- S: **1.5197** candidates / episode
- C − S: **+0.1058**
- 95% CI: **[+0.0843, +0.1271]**

Nevertheless it reduced candidate-evaluation CPU:

- C: **36.563 µs** / episode
- S: **39.255 µs** / episode
- C − S: **−2.692 µs**
- 95% CI: **[−3.563, −1.835] µs**

This is exactly the V2 principle generalized: candidate count is not the economic object. The cost-aware router sometimes accepts a longer sequence in exchange for cheaper expected candidate work.

## IV. Net executable router economy — failed

Routing itself cost more:

- C routing CPU: **78.110 µs** / episode
- S routing CPU: **70.347 µs** / episode
- additional C routing computation: approximately **+7.762 µs** / episode

Total process CPU including routing, candidate evaluation, and lineage update:

- C: **115.392 µs** / episode
- S: **110.312 µs** / episode
- C − S: **+5.079 µs**
- 95% world-bootstrap CI: **[+3.928, +6.290] µs**

Thus the preregistered net-economy criterion fails decisively:

\[
\boxed{C_{\rm total}^{C} > C_{\rm total}^{S}}
\]

on average in the frozen V2.1 scope.

C was total-CPU cheaper on only **20.6%** of paired episodes.

## V. Correction quality — supported

The exact same warranted correction criterion was preserved in all worlds. No economy claim is being rescued by a quality tradeoff.

## Evidence ladder

- I. Lineage proposal quality: **SUPPORTED**
- II. Cost-field transfer: **SUPPORTED**
- III. Heterogeneous work routing: **SUPPORTED**
- IV. Net executable router economy: **NOT SUPPORTED**
- V. Correction-quality admissibility: **SUPPORTED**
- V2.1: **NOT_SUPPORTED_IN_FROZEN_COST_AWARE_ROUTING_SCOPE**

## Transfer-relevance localization

| flip p | mean Δ candidates C−S | mean Δ candidate CPU | mean Δ total CPU | C total-CPU cheaper |
|---:|---:|---:|---:|---:|
| 0.15 | +0.049 | +0.339 µs | **+8.342 µs** | 15.1% |
| 0.25 | +0.142 | −3.113 µs | **+4.404 µs** | 21.3% |
| 0.35 | +0.203 | −10.943 µs | **−3.357 µs** | 35.5% |

This boundary is informative. Cost-aware routing is harmful at high-relevance/easy tiers because similarity-only routing is already strong and the extra routing computation is not repaid. At the hardest tier, where the proposal is less decisive and search costs are larger, the candidate-work saving becomes large enough to overcome the routing overhead on average.

That pattern is descriptive within the frozen moderator tiers; V2.1 does not license a universal monotone rule.

## Adversarial / diagnostic patterns

Across all episodes:

- C tested **more candidates but was cheaper overall** on **1.35%** of episodes;
- C tested **fewer candidates but was more expensive overall** on **0.31%** of episodes.

The first pattern directly confirms that cost-aware economy cannot be reduced to candidate-count minimization.

## Local diagnosis

The V2.1 failure is not:

- `no lineage proposal` — the proposal strongly beat uniform;
- `cost field failed to transfer` — rank correlation was 1.0 and heterogeneity remained >11×;
- `candidate-work objective had no effect` — candidate-evaluation CPU fell significantly;
- `quality degraded` — the correction contract passed everywhere.

The shallowest supported failure locus is:

\[
\boxed{
\text{routing computation / policy overhead}
}
\]

More specifically:

\[
\underbrace{\Delta C_{\rm candidate}<0}_{\text{saved work}}
\quad\text{but}\quad
\underbrace{\Delta C_{\rm route}>|\Delta C_{\rm candidate}|}_{\text{routing overhead}}
\quad\Rightarrow\quad
\Delta C_{\rm total}>0.
\]

## Earned update

V2.1 does **not** support replacing similarity-only routing with unconditional `q/c` routing.

It does support the narrower decomposition:

\[
\boxed{
\Lambda
\rightarrow
q_\Lambda
}
\]

and

\[
\boxed{
(q_\Lambda,\hat c)
\rightarrow
\text{lower heterogeneous candidate-execution work}
}
\]

while falsifying, in this implementation and scope, the stronger unconditional step

\[
\boxed{
(q_\Lambda,\hat c)
\not\Rightarrow
C_{\rm total}\downarrow.
}
\]

## Next localized hypothesis

The tier pattern points naturally to the previously deferred STOP/bypass gate:

\[
\text{use cost-aware routing only when expected candidate-work savings exceed incremental routing cost}.
\]

That is a new experiment, not a post-hoc rescue of V2.1.

## Authority boundary

This result does not modify V0–V2, V3, Axis I, SSI core theory, or any physical-energy claim. Physical energy remains `NOT_MEASURED`.
