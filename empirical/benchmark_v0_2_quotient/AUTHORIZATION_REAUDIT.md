# VFA-0.2 Quotient Revision Topology — Fresh Authorization Re-audit

## Status

```text
BENCHMARK_ID = VFA-0.2-QUOTIENT-REVISION-TOPOLOGY
AUTHORIZATION_REAUDIT = OPEN
A = PASS
B = PASS
C = PASS
D = PASS
E = PASS
F = PASS
G = NOT_EVALUATED
H = NOT_EVALUATED
I = NOT_EVALUATED

FUTURE_OBLIGATION_ACCESSED = FALSE
G_ACTIVATION = PROHIBITED
DELTA_PI = NOT_EVALUATED
FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
FUTURE_RUN = NOT_AUTHORIZED
```

This is a fresh authorization audit for the redesigned quotient treatment. It does not inherit treatment-sensitive adjudications mechanically from `benchmark_v0_1`. The old C/D artifact remains preserved as evidence for `VFA-0.1-REJECTED_RETRIEVAL_LEAKAGE`.

The governing review question is:

> Can an adversarial reviewer explain a future A/B difference using anything other than the declared quotient over revision-path equivalence classes, conditional on one identical validated substrate?

The audit stops at the first predicate that lacks complete content-addressed evidence. A missing prerequisite is `NOT_EVALUATED`, not an inferred PASS.

---

# A — Prospective scope and source freeze

## Re-audit question

Did the treatment redesign change the external source, construction cutoff, admissible future-change class, exclusion rule, observation horizon, first-qualifying selector, or prospective independence rule?

Evidence:

```text
empirical/benchmark_v0_1/evidence/A_SCOPE_SOURCE.md
Git blob SHA = bec386d1d3e1f172e5bbf48cb942b13ed2c5072e
```

The artifact freezes upstream `biomejs/biome`, construction cutoff `b51d8b1598effd064c3490c3866d5b2d60ebd5f8`, baseline `@biomejs/biome@2.5.8`, admissible migration-relevant future changes, exclusions, a 180-day horizon, the deterministic first-qualifying-obligation rule, and prospective implementation independence.

```text
A = PASS
```

---

# B — Quotient treatment and Phi_path identity

## Treatment identity

```text
W_A = W_B = W
D_A = (W, Gamma_A)
D_B = (W, Gamma_B)
Gamma_B = q(Gamma_A)
```

`q` acts only on revision-path equivalence labels. It does not rewrite facts, validation state, transformation classes, or source-fact references.

Evidence:

```text
construction/quotient_construction_audit.json
Git blob SHA = 6da2488fecb9dd407d2d6139ce17165bf145a127
```

The construction audit establishes one shared validated substrate, 24 identical path records, no truth-bearing Gamma fields, equal canonical representation size, a total/surjective/nontrivial quotient, and 12 merged path pairs. `Phi_path` is a component-wise structural descriptor; aggregation is prohibited.

```text
B = PASS
```

---

# C — Present-state equivalence

Outside the declared path-equivalence partition, A and B share the same validated substrate, path records, ordinary forward state and implementation, preactivation gate, representation size, and closed caller-capability surface.

Evidence:

```text
construction/quotient_construction_audit.json
construction/hardened_n_ladder_audit.json
```

```text
C = PASS
```

---

# D — Ordinary causal/adaptation equivalence

Required condition:

\[
F\circ q=F.
\]

Evidence establishes exact full-trace identity over all 249 exhaustive deterministic pre-freeze surrogate tasks and zero mismatches across 101592 hardened metamorphic comparisons.

```text
Q_adapt mean recovery recall A/B = 0.8646921017402945 / 0.8646921017402945
full recovery count A/B          = 118 / 118
ordinary full-trace mismatches   = 0
```

```text
D = PASS
```

This is the gate the rejected VFA-0.1 treatment failed.

---

# E — Resource, information, and execution symmetry

E is decomposed as:

\[
E=(E_{\rm capacity},E_{\rm information},E_{\rm execution}).
\]

Evidence:

```text
construction/E_ENVIRONMENT_MANIFEST.json
construction/E_ENVIRONMENT_KERNEL.py
construction/E_ENVIRONMENT_ATTACK.py
construction/e_environment_audit.json
evidence/E_RESOURCE_INFORMATION_EXECUTION_PASS.md
```

The environment freezes one common deterministic logical-resource contract around the quotient treatment. The only arm-facing treatment view is the fixed-size equivalence relation:

\[
M_\Gamma\in\{0,1\}^{24\times24}.
\]

Both arms receive:

```text
path slots                   = 24 / 24
treatment buffer bytes       = 576 / 576
matrix comparisons           = 576 / 576
matrix writes                = 576 / 576
unordered pair slots         = 276 / 276
probe-generation slots       = 276 / 276
fresh-validation slots       = 276 / 276
authorized persistence tries = 1 / 1
```

There is no arm-specific randomness, concurrency, cache, wall-clock stop rule, tool/API permission, network access, retry, or topology-dependent early stopping. Raw Gamma labels do not cross the trusted materialization boundary.

The hostile E attack records 192 metamorphic cost comparisons with zero mismatches.

Scope: equal deterministic execution opportunity, **not** equal CPU cycles, joules, cache misses, or nanoseconds. If physical cost later controls success or stopping, E must be reopened.

```text
E_capacity    = PASS
E_information = PASS
E_execution   = PASS
E             = PASS
```

---

# F — Treatment isolation and hidden-asymmetry audit

## Re-audit question

Can treatment identity be recovered from any material observable other than the declared revision-equivalence relation or a deterministic consequence of it?

The full declared treatment object is the equivalence relation `M_Gamma`. `Phi_path` is only a structural descriptor. This distinction matters because a matrix fingerprint or class-size statistic is information already contained in the treatment itself, not an independent treatment channel.

Evidence:

```text
construction/F_TREATMENT_ISOLATION_MANIFEST.json
construction/F_TREATMENT_ISOLATION_ATTACK.py
construction/f_treatment_isolation_audit.json
evidence/F_TREATMENT_ISOLATION_PASS.md
```

The motivating information-theoretic statement is:

\[
I(T;Z_{\rm undeclared}\mid\Phi_{\rm path})=0.
\]

But with only two treatment states, `Phi_path` itself identifies the arm, so ordinary finite-sample conditional-MI estimation is not informative. F therefore uses a stronger operational criterion: mask the full declared equivalence relation `M_Gamma` and preregistered deterministic consequences, then require exact paired identity of the residual observable vector.

Result:

```text
metamorphic A/B pairs      = 64
residual mismatches        = 0
paired residual identity   = PASS

holdout classifier accuracy:
  exact memorizer          = 0.500
  categorical stump        = 0.500
  1-NN Hamming             = 0.500
  chance                   = 0.500
```

Exact paired identity is primary. Classifier failure is secondary.

## Positive sensitivity control

Raw repository metadata remains treatment-revealing:

```text
GAMMA_A.json vs GAMMA_B.json
A... vs B... raw equivalence-label namespace
raw Gamma file hash
```

A trivial repository-level rule recovers the arm at 100%. F does not hide this. Those signals receive the disposition:

```text
BLOCKED_NONCAUSAL_REPOSITORY_OR_TRUSTED_MATERIALIZATION_METADATA
```

They are non-material only because predicate E proves that raw Gamma metadata terminates at the trusted materialization boundary and never becomes arm/evaluator-visible. The shared materialization kernel has no A/B literal and uses raw label values only in pairwise equality comparisons that compile `M_Gamma`.

Classification result:

```text
unclassified observables            = 0
material undeclared distinguishers  = 0
```

```text
F = PASS
```

Any later exposure of raw repository/label metadata to the arm, evaluator, stopping logic, evidence channel, or resource scheduler automatically reopens F.

---

# G — Future-obligation independence and common-cause exposure

```text
G = NOT_EVALUATED
```

G is now the next authorization predicate. It must re-audit and freeze the prospective obligation-selection/disclosure mechanism for this quotient lineage. Passing A–F does not authorize disclosure or activation.

The required future obligation remains a common cause:

\[
O_{\rm future}^{A}=O_{\rm future}^{B}
\]

with one canonical evidence bundle, identical timing, permissions, and evaluation start conditions. The realized future event remains unknown and must not be accessed while G is being specified.

---

# H/I — Stop rule

Because G is not yet adjudicated:

```text
H = NOT_EVALUATED
I = NOT_EVALUATED
```

H must later re-open the confound ledger with quotient-specific rivals. I cannot be attempted until A–H all pass and the complete endpoint/evaluation packet is content-addressed and frozen.

## Current authority boundary

```text
CONSTRUCTION_VALID = YES
A_THROUGH_F = PASS
AUTHORIZATION_VALID = NO
FUTURE_HYPOTHESIS_TESTED = NO

FUTURE_OBLIGATION_ACCESSED = FALSE
G_ACTIVATION = PROHIBITED
DELTA_PI = NOT_EVALUATED
KERNEL_FUTURE_INCLUSION = NOT_EVALUATED
FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
FUTURE_RUN = NOT_AUTHORIZED
```

No `G=1`. No prospective obligation. No future runner.
