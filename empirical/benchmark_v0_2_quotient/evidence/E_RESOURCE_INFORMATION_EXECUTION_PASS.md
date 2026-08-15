# E Evidence — Resource, Information, and Execution Symmetry

## Adjudication

```text
E_capacity    = PASS
E_information = PASS
E_execution   = PASS
E             = PASS
```

This is authorization-side environment evidence for `VFA-0.2-QUOTIENT-REVISION-TOPOLOGY`. It accesses no prospective future obligation, does not activate `G`, and does not evaluate `DeltaPi`.

The governing rule is:

> Any material unexplained A/B resource, information, or execution asymmetry is disqualifying. No statistical compensation is permitted.

## E decomposition

\[
E=(E_{\rm capacity},E_{\rm information},E_{\rm execution}).
\]

### Capacity

Both arms are constrained to one common logical execution contract:

- CPython 3.13.5;
- standard library only;
- same interpreter instance and evaluator code;
- 24 path slots;
- a fixed 576-byte `24 x 24` equivalence-matrix treatment view;
- all 276 unordered path pairs scanned;
- 276 probe-generation slots;
- 276 fresh-evidence validation slots;
- one authorized-persistence attempt;
- no arm-private storage beyond the fixed 576-byte treatment buffer.

The common future-evidence interface has one shared 64 MiB cap. If the first qualifying event cannot be packaged within that cap, execution is invalid; a later event may not be substituted.

### Information

Both arms use the same validated substrate. The trusted environment may read the arm-specific Gamma only to compile its equivalence relation. Raw Gamma class labels are not evaluator-visible.

The only treatment view crossing the arm-facing boundary is:

\[
M_\Gamma\in\{0,1\}^{24\times24},
\]

where `M[i,j]=1` iff the two frozen revision paths are in the same equivalence class.

Thus arbitrary renaming of equivalence-class labels is observationally irrelevant. In particular, the raw `A...` / `B...` class-label namespaces do not become an information side channel.

Tools, APIs, and network access are empty/disabled. Predicate G remains responsible for proving that the realized future obligation is packaged once and disclosed identically to both arms.

### Execution

The environment uses deterministic logical operation budgets, not wall-clock or physical-energy equality:

- no randomness;
- no concurrency;
- no persistent cache;
- no arm-specific timeout;
- no topology-dependent early stop;
- no unique-class or deduplication budget;
- paired invalidation on any arm exception;
- no one-arm retry.

Post-gate materialization is fixed-cost in the benchmark's adjudication metric:

```text
path-record reads          = 24 / 24
class-label lookups        = 24 / 24
matrix comparisons         = 576 / 576
matrix byte writes         = 576 / 576
matrix output bytes        = 576 / 576
unordered pair slots       = 276 / 276
```

This certificate does **not** claim equal CPU cycles, joules, cache misses, or nanoseconds. Those quantities are deliberately prevented from controlling availability, stopping, or the confirmatory estimand.

## Adversarial attack

`E_ENVIRONMENT_ATTACK.py` attacks the contract rather than merely comparing manifest strings.

It checks:

1. exact runtime/stdlib contract;
2. shared validated-substrate identity;
3. equal raw and canonical Gamma representation sizes;
4. fixed-size matrix exposure and exact logical materialization-cost equality;
5. 192 metamorphic cost comparisons under class-label renaming, record-order reversal, allocation pressure, and both A/B execution orders;
6. rejection of dirty common-evidence schemas and raw-Gamma exposure;
7. absence of raw arm-label literals from the environment kernel;
8. absence of randomness, timing, concurrency, subprocess, or network dependencies in the kernel.

Result:

```text
metamorphic cost comparisons = 192
metamorphic cost mismatches   = 0
AB/BA order invariance        = PASS
raw Gamma exposure rejected   = PASS
common evidence schema closed = PASS
```

## Scope

The cost claim is:

\[
\boxed{\text{equal deterministic execution opportunity}}
\]

not equal physical runtime or energy.

If a later benchmark version makes wall-clock, joules, or low-level runtime cost causally relevant to stopping or success, E must be re-opened and those resources independently matched.

## Authority boundary

```text
FUTURE_OBLIGATION_ACCESSED = FALSE
G_ACTIVATION               = PROHIBITED
DELTA_PI                    = NOT_EVALUATED
KERNEL_FUTURE_INCLUSION     = NOT_EVALUATED
FREEZE_PACKET               = NOT_FROZEN
AUTHORIZATION_CERTIFICATE  = NOT_ISSUED
FUTURE_RUN                  = NOT_AUTHORIZED
```

Passing E licenses only the next authorization predicate. It does not authorize activation or prospective execution.
