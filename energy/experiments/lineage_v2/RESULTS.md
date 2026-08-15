# Lineage Corrective Economy V2 — Results

## Adjudication

**SUPPORTED_IN_FROZEN_HETEROGENEOUS_EXECUTABLE_SCOPE**

V2 removes the V1 fixed-cost candidate-evaluation convenience. Candidate evaluations are now heterogeneous reversible repair programs with a common exact validator. Lineage affects candidate ordering only.

This result has authority only inside the frozen executable synthetic repair-program environment. It is not a physical-energy result.

## Frozen sample

- Replicate worlds: **64**
- Paired held-out episodes per world: **96**
- Total paired correction episodes: **6,144**
- Payload: **16,384 uint8 elements / episode**
- Candidate repair programs: **12**
- Missing / unidentified worlds: **0**
- Correction-quality contract passed in every world: **True**

## I. Search reuse

Persistent lineage again reduced candidate traversal:

- A mean candidates tested: **1.528**
- B mean candidates tested: **6.525**
- Mean A − B: **-4.997 candidates / episode**
- 95% paired world-bootstrap CI: **[-5.088, -4.907]**

Search reuse therefore replicated.

## II. Heterogeneous-work gate

The preregistered heterogeneity gate was:

$$
H_C=
\frac{\max_j\operatorname{median}(C_j)}
{\min_j\operatorname{median}(C_j)}
\ge 2.
$$

Observed:

$$
\boxed{H_C=11.159}
$$

so the gate passed.

The cheapest B-only median candidate evaluation was about **5.128 µs** and the most expensive was about **57.225 µs**.

Candidate count therefore no longer determines correction cost.

## III. Heterogeneous candidate-work avoidance

Mean measured candidate-evaluation CPU per correction:

- A: **38.603 µs**
- B: **169.183 µs**
- A − B: **-130.579 µs**
- 95% world-bootstrap CI: **[-145.793, -121.894] µs**

Thus lineage ordering reduced the CPU spent executing heterogeneous repair candidates.

## IV. Net executable corrective economy

A also paid executed lineage overhead:

- lineage retrieval/order construction: **67.165 µs / episode**
- lineage update: **0.779 µs / episode**

Total process CPU per correction:

- A: **106.548 µs**
- B: **169.183 µs**
- A − B: **-62.635 µs**
- 95% world-bootstrap CI: **[-77.752, -54.016] µs**

This is an average total process-CPU reduction of approximately **37.0%** relative to B after retrieval and update overhead.

A had lower total CPU on **68.0%** of individual paired episodes.

## The adversarial V2 failure mode actually occurred

V2 explicitly allowed:

$$
n_A<n_B
\quad\land\quad
C_A>C_B.
$$

This occurred.

- Fewer candidates but **higher candidate-evaluation CPU**: **0.90%** of episodes.
- Fewer candidates but **higher total CPU after lineage overhead**: **19.55%** of episodes.

So V2 is not reducible to “fewer candidates implies cheaper correction.”

The average treatment effect remained favorable despite a substantial episode-level region where lineage reduced traversal but did not reduce total compute.

## Evidence ladder

- I. Search reuse: **SUPPORTED**
- II. Heterogeneity gate: **SUPPORTED**
- III. Heterogeneous work avoidance: **SUPPORTED**
- IV. Net executable corrective economy: **SUPPORTED**
- V. Correction-quality admissibility: **SUPPORTED**
- V2: **SUPPORTED_IN_FROZEN_HETEROGENEOUS_EXECUTABLE_SCOPE**

## Transfer-relevance moderator

| held-out flip p | mean Δ candidates A−B | mean Δ candidate CPU | mean Δ total CPU | A total-CPU cheaper | fewer candidates but higher total CPU |
|---:|---:|---:|---:|---:|---:|
| 0.15 | -5.473 | -136.901 µs | -68.590 µs | 72.1% | 19.9% |
| 0.25 | -4.954 | -142.689 µs | -75.244 µs | 67.6% | 18.9% |
| 0.35 | -3.654 | -87.395 µs | -19.554 µs | 56.7% | 19.9% |

Routing quality retained the preregistered directional pattern: as signature transfer relevance weakened, A's candidate-count advantage shrank.

Total CPU did **not** decrease monotonically across the first two relevance tiers. The `p=0.25` tier showed a slightly larger mean CPU saving than `p=0.15` despite weaker traversal reduction. That is consistent with the purpose of V2: heterogeneous candidate costs break the identity between candidate count and correction cost.

The hardest tier (`p=0.35`) showed the clearest boundary pressure: the traversal advantage was smaller and A was total-CPU cheaper on only about 57% of episodes, although the mean total-CPU contrast remained favorable.

## Local interpretation

The dangerous V2 possibility was:

$$
n_A<n_B
\quad\text{but}\quad
C_A\ge C_B
$$

because lineage could route through fewer but more expensive repair programs, or retrieval overhead could erase candidate-work savings.

That failure occurred on a nontrivial subset of episodes, but it did not dominate the preregistered world-level estimand.

The earned update is:

> In the frozen heterogeneous executable repair-program environment, persistent validated lineage reduced measured heterogeneous candidate-repair work and total process CPU after lineage retrieval/update overhead, while preserving the same exact warranted correction criterion.

This extends V1 because candidate evaluations no longer have approximately fixed intrinsic cost.

## Authority boundary

V2 still does **not** establish:

- physical energy reduction in joules;
- lower wall-plug energy;
- GPU or LLM inference savings;
- general AI corrective economy;
- that every lineage/retrieval implementation is beneficial;
- a universal monotone law relating transfer relevance to economy;
- Axis I;
- SSI core theory.

Physical energy remains `NOT_MEASURED`.

## Run integrity

The preregistration and executable runner were committed before the authoritative execution.

- preregistration Git blob: `52fa680cedaf4d8bbb6d9ee4bf0f0888b79cccec`
- runner Git blob: `7428151d1d64a827053cd3768105192f3c830a21`

A preliminary local execution copy was rejected before result packaging after a byte-level mismatch with the committed runner was detected. No inference is taken from that copy. The reported V2 result comes from a rerun whose local Git blob hashes exactly matched both committed files before execution.
