# Lineage Corrective Economy V1 — Preregistration

## Status

**FROZEN BEFORE EXECUTION.**

V1 removes one synthetic convenience from V0: correction cost is no longer assigned by the identity

$$
J_{\rm corr}=7+3n_{\rm tested}.
$$

Instead, both agents execute the candidate tests and lineage retrieval operations, and V1 measures the resulting process CPU time and wall-clock time directly.

This remains a synthetic correcting-agent experiment. It is **not** a physical-energy experiment and does not measure joules.

## 1. Earned V0 premise and V1 question

V0 earned only the local claim that persistent validated lineage reduced candidate traversal in the frozen related-but-nonidentical mechanism-search environment. V1 asks the next independent question:

$$
\Lambda_{\rm preserved}
\overset{?}{\longrightarrow}
n_{\rm tested}\downarrow
\overset{?}{\longrightarrow}
C_{\rm actual}\downarrow,
$$

where $C_{\rm actual}$ is measured execution work rather than a deterministic price assigned to $n_{\rm tested}$.

A valid negative result is

$$
n_A<n_B
\quad\land\quad
C_A\ge C_B.
$$

That would mean lineage prunes search but does not produce executable corrective economy under the V1 implementation.

## 2. Treatment contrast

The treatment remains:

- **A — lineage preserved:** persistent validated correction signatures are available across episodes;
- **B — lineage unavailable:** no persistent correction lineage is available between episodes.

Both agents receive the same paired held-out challenges and use the same candidate mechanisms, exact warranted probe, correction rule, validation rule, horizon, and candidate-execution workload.

Only A performs lineage retrieval and lineage update.

## 3. Frozen world and challenge generator

V1 preserves the V0 challenge structure.

- Master seed: `20260815`.
- Independent replicate worlds: `64`.
- Mechanism families per world: `12`.
- Binary signature dimension: `32`.
- Warm-up lineage examples per mechanism: `2`.
- Warm-up bit-flip probability: `0.10`.
- Held-out correction episodes per world: `96`.
- Each mechanism occurs exactly `8` times per world.
- Held-out transfer tiers are a shuffled multiset:
  - `48` episodes at bit-flip probability `0.15`;
  - `32` episodes at `0.25`;
  - `16` episodes at `0.35`.
- Held-out signatures are regenerated if exactly equal to any lineage signature available to A before the episode.

The noise tier is a preregistered transfer-relevance moderator, not itself an outcome.

## 4. Frozen correction policy

### A — lineage-preserved ordering

A computes the minimum normalized Hamming distance from the current signature to the stored validated lineage for each mechanism family, then tests mechanism candidates in ascending distance. Ties are resolved by the same deterministic episode-specific pseudorandom procedure used in V0.

### B — lineage-unavailable ordering

B tests mechanism families in a deterministic episode-specific pseudorandom permutation independent of the true mechanism and held-out signature.

### Execution-order balance

To reduce systematic cache/order bias in timing, the order in which A and B are executed alternates by episode:

- odd-numbered episodes: A then B;
- even-numbered episodes: B then A.

The two agents do not share lineage state.

## 5. Frozen executable candidate workload

Each candidate test performs an actual deterministic CPU workload before the exact warranted probe returns whether the candidate is the true mechanism.

- Work function: chained `hashlib.blake2b` digest computation.
- Digest size: `32` bytes.
- Rounds per candidate test: `256`.
- Initial payload contains the 32-bit signature bytes, candidate mechanism id, world id, and episode id.
- Every round consumes the previous digest; therefore every candidate test executes all 256 rounds.

The exact oracle check `candidate == true_mechanism` occurs **after** the workload. This keeps correction quality fixed while making candidate traversal execute real CPU work.

No result-dependent early exit is permitted inside the 256-round workload.

## 6. Frozen lineage retrieval and update implementation

For each episode, A executes lineage retrieval before candidate probes:

1. for each of 12 mechanism families;
2. scan all stored signatures for that family;
3. compute normalized Hamming distance with NumPy;
4. retain the minimum distance;
5. sort candidate mechanisms by `(distance, frozen tie rank)`.

After warranted correction, A appends the held-out signature to the validated lineage for the identified mechanism.

No artificial price is assigned to retrieval, storage, or update. Their executed CPU/wall time is included in measured A time.

The following lineage quantities are recorded separately:

- records before episode;
- retrieval CPU time;
- retrieval wall time;
- update CPU time;
- update wall time;
- approximate stored signature bytes (`record_count × 32 bytes`), reported as a memory-footprint descriptor rather than converted into energy.

There is no synthetic background-maintenance charge in V1.

## 7. Frozen execution-work measurements

For each paired episode and agent, record:

- `n_tested`;
- candidate probe rounds executed (`256 × n_tested`);
- process CPU time using `time.process_time_ns()`;
- wall time using `time.perf_counter_ns()`;
- retrieval CPU/wall time for A;
- lineage-update CPU/wall time for A;
- probe CPU/wall time;
- total correction CPU/wall time.

For A:

$$
C_{\rm CPU}^{A}
=
C_{\rm retrieve}^{A}
+
C_{\rm probe}^{A}
+
C_{\rm update}^{A}.
$$

For B:

$$
C_{\rm CPU}^{B}=C_{\rm probe}^{B}.
$$

Measured wall time is secondary because scheduler noise can affect it. Process CPU time is the primary V1 executable-work endpoint.

`model_calls`, `tokens`, and `GPU_time` are `NOT_APPLICABLE` in V1 because the correcting agent is an executable CPU program, not a language-model inference system. They must not be imputed as zero-cost evidence for later stages.

## 8. Frozen correction-quality contract

As in V0, the exact probe fixes correction quality:

$$
H_{\rm recover}=1,
\qquad
R_{\rm collateral}=0,
\qquad
R_{\rm reopen}=1,
\qquad
\mathrm{Auth}=1.
$$

for every included episode and both agents.

Any violation fails V1 admissibility. Timing savings cannot rescue a quality failure.

## 9. Frozen estimands

### Traversal

For each world, compute mean paired difference

$$
\Delta n
=
\overline n_A-\overline n_B.
$$

### Primary executable economy

For each world:

$$
\Delta C_{\rm CPU}
=
\overline C_{\rm CPU}^{A}
-
\overline C_{\rm CPU}^{B}.
$$

V1 executable economy is supported only if the upper endpoint of the preregistered 95% bootstrap CI for the cross-world mean of $\Delta C_{\rm CPU}$ is below zero.

### Secondary wall-time economy

Analogously compute

$$
\Delta C_{\rm wall}
=
\overline C_{\rm wall}^{A}
-
\overline C_{\rm wall}^{B}.
$$

Wall time is descriptive/secondary and cannot override the primary CPU-time result.

### Transfer-relevance moderation

For each frozen noise tier $r\in\{0.15,0.25,0.35\}$, report mean paired differences in traversal and CPU time:

$$
\Delta n(r),
\qquad
\Delta C_{\rm CPU}(r).
$$

No continuous crossover $r^\star$ will be estimated from only three tiers. A tier-level sign reversal, if observed, will be reported without interpolation.

## 10. Frozen uncertainty procedure

- Inference unit: replicate world.
- Paired world-level bootstrap resamples: `20,000`.
- Bootstrap seed: `20260817`.
- Resample 64 world-level paired summaries with replacement.
- Report percentile 95% confidence intervals.
- No episode-level iid bootstrap is permitted because A's lineage evolves within world.

## 11. Evidence ladder

### I. Traversal replication

Supported iff the 95% bootstrap CI upper endpoint for mean $\Delta n$ is below zero.

### II. Executable CPU economy

Supported iff the 95% bootstrap CI upper endpoint for mean $\Delta C_{\rm CPU}$ is below zero.

### III. Admissibility

Supported iff the frozen correction-quality contract passes for both agents in every included world.

### IV. V1 supported

V1 is `SUPPORTED_IN_FROZEN_EXECUTABLE_SCOPE` iff I–III all pass.

A wall-time reduction is not required for IV because CPU time is primary, but it is reported.

## 12. Missingness and execution integrity

- Missing or malformed world data yields `NOT_IDENTIFIED` for that world.
- If fewer than 60 of 64 worlds remain identified, V1 overall is `NOT_IDENTIFIED`.
- `NOT_IDENTIFIED` is neither zero nor a negative result.
- The runner records Python, NumPy, platform, processor string, and run timestamp.
- No timing threshold, workload size, retrieval implementation, bootstrap rule, or transfer tier may be changed after execution begins.

## 13. Scope of authority

A positive V1 result supports only:

> In the frozen executable CPU correction environment, persistent validated lineage reduced candidate traversal and reduced measured process CPU time after including executed lineage retrieval and update overhead, while preserving the same exact warranted correction criterion.

It does **not** establish:

- physical energy savings;
- GPU or LLM inference savings;
- lower wall-plug power;
- general AI corrective economy;
- that all lineage retrieval policies are beneficial;
- Axis I;
- SSI core theory.

A V1 result licenses only the next measurement rung; it does not retroactively expand V0.
