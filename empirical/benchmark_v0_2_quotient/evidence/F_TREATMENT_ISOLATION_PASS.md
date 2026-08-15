# F Evidence — Treatment Isolation and Hidden-Asymmetry Audit

## Adjudication

```text
F = PASS
```

This is authorization-side evidence for `VFA-0.2-QUOTIENT-REVISION-TOPOLOGY`. It accesses no prospective future obligation, does not activate `G`, and does not evaluate `DeltaPi`.

The governing criterion is:

> Every material A/B-discriminating observable must be either the declared revision-equivalence treatment, a preregistered deterministic consequence of that treatment, or explicitly blocked/non-causal under the frozen environment boundary.

## Statistical clarification

The motivating expression is:

\[
I(T;Z_{\rm undeclared}\mid\Phi_{\rm path})=0.
\]

But with only two treatment states, `Phi_path` itself identifies the arm, so an ordinary finite-sample conditional-mutual-information estimate would be uninformative.

The audit therefore uses a stronger operational criterion. The full declared treatment is the equivalence relation encoded by:

\[
M_\Gamma\in\{0,1\}^{24\times24}.
\]

The attack masks `M_Gamma` and every preregistered deterministic function of it, then requires exact paired identity of the residual observable vector `Z_undeclared` across treatment-equivalent metamorphic encodings.

## Primary result — exact residual identity

The attack generates 64 metamorphic A/B pairs using neutral equivalence-label renaming and path-record reorderings while preserving each arm's declared equivalence relation.

```text
metamorphic A/B pairs      = 64
residual mismatches        = 0
paired residual identity   = PASS
```

The residual vector includes non-treatment artifact structure, path-record identity, substrate identity, representation lengths, materialization trace, pair-slot count, common-evidence identity, exposure type/arity, exception profile, and arm/raw-Gamma visibility flags. Matrix content itself is masked because it is the treatment.

## Blind treatment-recovery attack

Pairs 0–47 form the training set and pairs 48–63 form a holdout set. Each residual signature appears once with label A and once with label B.

Three standard-library classifiers are attacked:

```text
exact residual-signature memorizer   = 0.500
single-feature categorical stump      = 0.500
1-nearest-neighbor, Hamming distance  = 0.500
chance                                = 0.500
```

This classifier result is secondary. Exact paired residual identity is stronger: any deterministic classifier that receives only `Z_undeclared` must make the same prediction for both members of each identical pair, so it cannot exceed 50% paired accuracy.

## Positive sensitivity control

Raw repository artifacts are deliberately **not** observationally identical.

A reviewer with access to repository-only metadata can recover the arm at 100% from, for example:

```text
GAMMA_A.json vs GAMMA_B.json
A... vs B... raw equivalence-label namespace
raw Gamma file hash
```

This is not hidden or normalized away.

Disposition:

```text
BLOCKED_NONCAUSAL_REPOSITORY_OR_TRUSTED_MATERIALIZATION_METADATA
```

Those signals are non-material only because predicate E established a closed causal boundary:

- raw Gamma never crosses the arm/evaluator interface;
- evaluator-visible treatment is only the fixed 576-byte `M_Gamma`;
- raw arm labels are not evaluator-visible;
- the shared materialization kernel contains no A/B literal;
- raw equivalence labels are used only in pairwise equality comparisons that compile `M_Gamma`.

If any raw repository or label metadata later becomes arm/evaluator-visible or influences stopping, allocation opportunity, evidence exposure, or output interpretation, F must be reopened.

## Observable classification ledger

| Observable | Distinguishes? | Material? | Disposition |
|---|---:|---:|---|
| `M_Gamma` content | yes | yes | `DECLARED_TREATMENT` |
| matrix-derived topology statistics | yes | yes | `DETERMINISTIC_TREATMENT_CONSEQUENCE` |
| raw Gamma repository filename | yes | no | `BLOCKED_NONCAUSAL_REPOSITORY_METADATA` |
| raw equivalence-label namespace | yes | no | `BLOCKED_NONCAUSAL_TRUSTED_MATERIALIZATION_METADATA` |
| raw Gamma file SHA | yes | no | `BLOCKED_NONCAUSAL_REPOSITORY_METADATA` |
| masked artifact residual | no | yes | `MUST_MATCH` |
| materialization logical trace | no | yes | `MUST_MATCH` |
| arm/evaluator residual exposure | no | yes | `MUST_MATCH` |

```text
unclassified observables                 = 0
material undeclared distinguishers       = 0
```

## Implementation confinement

The shared E environment kernel is reused by both arms. Static inspection of `compile_equivalence_matrix` shows exactly two loads of the local raw-label tuple and exactly one comparison involving it:

```text
labels[i] == labels[j]
```

There are no calls that consume the raw labels, no A/B arm literals, and no arm-specific implementation branch. Materialization traces, matrix sizes, pair schedules, and exception profiles match.

## F scope

F does **not** require A and B to be observationally identical after erasing the treatment. That would destroy the intervention.

It requires:

\[
\boxed{
\text{all exploitable A/B differences}
\in
\{\text{declared treatment},\text{deterministic treatment consequence},\text{blocked non-causal metadata}\}.
}
\]

Within the frozen E environment and treatment boundary, that criterion passes.

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

Passing F licenses only predicate G. It does not authorize future disclosure, activation, or execution.
