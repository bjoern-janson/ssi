# Lineage Corrective Economy V1 — Results

## Adjudication

**SUPPORTED_IN_FROZEN_EXECUTABLE_SCOPE**

V1 removes the V0 hand-priced correction-cost identity and measures executed process CPU time directly. The result has authority only in this executable synthetic CPU correction environment. It is not a physical-energy result.

## Frozen sample

- Replicate worlds: **64**
- Paired held-out episodes per world: **96**
- Total paired correction episodes: **6,144**
- Candidate workload: **256 chained BLAKE2b rounds per candidate test**
- Missing / unidentified worlds: **0**
- Correction-quality contract passed in every world: **True**

## I. Traversal replication

Persistent lineage again reduced corrective traversal:

- A mean candidates tested: **1.522**
- B mean candidates tested: **6.525**
- Mean A − B: **-5.003 candidates / episode**
- 95% paired world-bootstrap CI: **[-5.096, -4.912]**

Therefore the V0 traversal result replicated under the V1 executable implementation.

## II. Primary executable-work result

Process CPU time includes A's executed lineage retrieval, candidate probing, and lineage update overhead. B's total includes its executed candidate probing.

Mean process CPU time per correction:

- A: **204.111 µs**
- B: **610.005 µs**
- A − B: **-405.894 µs**
- 95% paired world-bootstrap CI: **[-418.330, -394.782] µs**

This is a mean CPU-time reduction of approximately **66.5%** relative to B.

A was CPU-cheaper on **86.4%** of individual paired episodes.

The primary preregistered executable-economy criterion passed because the full 95% CI for the world-level mean CPU difference is below zero.

## Where A spent its executed work

Mean A process CPU components per episode:

- lineage retrieval/order construction: **59.798 µs**
- candidate probe workload: **142.964 µs**
- lineage update: **1.350 µs**

Mean B candidate probe workload:

- **610.005 µs**

Thus lineage retrieval was not free: it represented about **29.3%** of A's measured CPU cost. In the frozen V1 environment, however, this overhead was smaller than the executed candidate-work reduction produced by the improved ordering.

## Secondary wall-time result

Mean wall time per correction:

- A: **205.467 µs**
- B: **611.300 µs**
- A − B: **-405.833 µs**
- 95% world-bootstrap CI: **[-418.336, -394.614] µs**

Wall time is secondary by preregistration and does not determine V1 adjudication.

## Evidence ladder

- I. Traversal replication: **SUPPORTED**
- II. Executable CPU economy: **SUPPORTED**
- III. Correction-quality admissibility: **SUPPORTED**
- IV. V1: **SUPPORTED_IN_FROZEN_EXECUTABLE_SCOPE**

The result therefore supports the narrow executable mechanism:

$$
\Lambda_{\rm preserved}
\rightarrow
n_{\rm tested}\downarrow
\rightarrow
C_{\rm CPU,actual}\downarrow
$$

within this frozen implementation.

The second arrow is now empirical rather than an accounting identity: V1 measures executed CPU time after including lineage retrieval and update work.

## Transfer-relevance gradient

The preregistered relevance tiers retained the V0 directional pattern.

| held-out flip p | mean Δ candidates A−B | mean Δ CPU A−B | A CPU-cheaper |
|---:|---:|---:|---:|
| 0.15 | -5.482 | **-453.647 µs** | 91.1% |
| 0.25 | -4.941 | **-399.535 µs** | 85.4% |
| 0.35 | -3.688 | **-275.352 µs** | 74.4% |

As transfer relevance weakened, lineage reduced fewer candidate tests and produced a smaller executable CPU advantage. No continuous $r^\star$ is estimated from these three tiers, as frozen in the protocol.

This pattern supports further testing of transfer relevance as a moderator; it does not establish a universal monotone law.

## Local interpretation

The dangerous V1 possibility was:

$$
n_A<n_B
\quad\text{but}\quad
C_A\ge C_B
$$

because lineage retrieval/indexing might cost more CPU than search pruning saved.

That failure did **not** occur in V1. Instead:

$$
n_A<n_B
\quad\land\quad
C_{\rm CPU}^{A}<C_{\rm CPU}^{B}
$$

with the same exact warranted correction criterion for both agents.

The earned update is therefore:

> In the frozen executable CPU mechanism-search environment, persistent validated lineage reduced candidate traversal enough to reduce measured process CPU time even after executed lineage retrieval and update overhead were included.

## Authority boundary

V1 still does **not** establish:

- physical energy reduction in joules;
- lower wall-plug power;
- GPU or LLM inference savings;
- that runtime is a calibrated energy proxy;
- general AI corrective economy;
- that all lineage/retrieval implementations are beneficial;
- Axis I;
- SSI core theory.

`model_calls`, `tokens`, and `GPU_time` are `NOT_APPLICABLE` in V1. Physical energy is `NOT_MEASURED`.

The next rung should independently measure a richer runtime/compute workload or a calibrated energy proxy without changing the earned V1 statement.

## Execution environment

Primary run environment:

- Python: **3.13.5**
- NumPy: **2.3.5**
- Platform: **Linux 6.18.35 x86_64**
- Total experiment process CPU time: **6.170 s**
- Total experiment wall time: **6.180 s**

A Python-startup spreadsheet-runtime warmup warning occurred before the runner's measurement window; the experiment itself completed with return code 0. Per-episode CPU timing starts inside the correction functions after startup/import initialization.
