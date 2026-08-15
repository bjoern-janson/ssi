# Post-gate semantic contract — construction attack 1

## Lineage state

```text
VFA-0.2-H-FAIL-POSTGATE-SEMANTIC-UNDERDETERMINATION
    ->
VFA-0.2-POSTGATE-SEMANTIC-CONTRACT-1
```

This is a construction-side repair attempt for the H failure. It does not overwrite `H_RESIDUAL_CONFOUND_VETO_FAIL.md` and does not change the current authorization state.

```text
SEMANTIC_ALGEBRA = PASS
FUTURE_GROUNDING = FAIL
POSTGATE_CONTRACT = FAIL
FAILURE_CODE = FUTURE_DISTINCTION_GROUNDING_NOT_IDENTIFIED
```

No real future obligation was accessed. `G` remains prohibited. `DeltaPi` was not realized.

## Governing rule

> **No post-gate implementation may assign semantic meaning to Gamma that is not already present in the frozen contract.**

The repair therefore replaces an arbitrary Gamma decoder with a reference-based semantic algebra.

A semantic revision reference is exactly:

```text
(relation_kind, source_fact_id)
```

Raw `path_id` strings and raw Gamma equivalence labels are representation metadata, not semantic inputs.

## Licensed operation algebra

The frozen first-stage grammar contains only:

```text
TRACE
FOLLOW
CHALLENGE
REOPEN
COMPARE
```

`SPLIT` is prohibited at the first endpoint. A split requires later independently validating fresh evidence.

The primary discriminating operation is `COMPARE(x,y)`. It is legal only when:

1. `x` and `y` belong to the same declared relation kind; and
2. the current revision partition keeps them in distinct blocks.

Thus the reachability decision is exactly:

\[
\operatorname{Reach}_{\Gamma}(x,y)
=
\mathbf 1\!\left([x]_{\Gamma}\neq[y]_{\Gamma}\right).
\]

No class count, singleton fraction, matrix density, row sum, raw label, hash, arm label, score, or performance statistic enters that decision.

## Representation equivalence

The contract freezes `~repr` over harmless representation changes. The attack exercised:

- raw equivalence-label renaming;
- raw `path_id` renaming with references preserved;
- path-record reversal;
- future-distinction row reversal;
- pair-orientation swap.

Result:

```text
metamorphic partition/evaluator comparisons = 64
mismatches                                  = 0
pair order/orientation invariance           = PASS
```

Therefore:

\[
x\sim_{\rm repr}y
\Rightarrow
\operatorname{Reach}(x)=\operatorname{Reach}(y)
\]

for the attacked representation class.

## Revision sensitivity

The quotient has exactly 12 nontrivial q-kernel pairs. Each was synthetically exercised as `DISTINGUISHED` without using a real future obligation.

```text
q-kernel pairs                                = 12
A reachable / B unreachable                   = 12 / 12
same-kind non-kernel control pairs             = 48
reachable in both arms                         = 48 / 48
EQUIVALENT semantics                           = PASS
NOT_IDENTIFIED preserved without imputation    = PASS
```

So the algebra is sensitive to actual loss of a revision distinction rather than to arbitrary representation changes.

## Why the contract still fails

The future-distinction table is required to cover **all 12 q-kernel pairs**, with exactly one status per pair:

```text
DISTINGUISHED
EQUIVALENT
NOT_IDENTIFIED
```

No favorable subset may be selected.

But the benchmark does not yet contain a frozen external operator that maps the realized future obligation to those statuses without access to:

```text
Gamma_A / Gamma_B
Phi_path
arm outcomes
DeltaPi
```

That missing operator still has causal authority over the primary estimand. A discretionary witness constructor could simply mark an A-favoring kernel pair `DISTINGUISHED` and thereby manufacture the predicted reachability contrast.

Therefore:

\[
\boxed{
\text{semantic invariance}
\neq
\text{future semantic grounding}.
}
\]

The first has now been operationalized. The second has not.

## H implications

This construction is strong evidence that two original H vetoes are repairable:

```text
H_quotient_interpretation -> candidate BLOCKED
H_evaluator               -> candidate BLOCKED
```

because Gamma meaning is reference-based and the reachability evaluator is canonical under `~repr`.

However:

```text
H_challenge_recognizability -> REMAINS RESIDUAL VETO
```

in the sharper form:

```text
FUTURE_DISTINCTION_GROUNDING_NOT_IDENTIFIED
```

H is therefore **not** re-adjudicated as PASS.

## Re-audit consequences

If a final grounding operator is later identified and this post-gate contract is adopted into the benchmark, the newly introduced post-gate implementation must not inherit prior environment/isolation evidence mechanically:

```text
E re-audit = REQUIRED
F re-audit = REQUIRED
G re-audit = REQUIRED if grounding changes future evidence packaging/disclosure
```

The existing A–G evidence remains preserved as evidence about the prior authorized construction surface; the candidate repair has not yet been promoted into that surface.

## Authority boundary

```text
FUTURE_OBLIGATION_ACCESSED = FALSE
G_ACTIVATION               = PROHIBITED
DELTA_PI                    = NOT_EVALUATED
KERNEL_FUTURE_INCLUSION     = NOT_EVALUATED
H                           = FAIL
I                           = NOT_EVALUATED
FREEZE_PACKET               = NOT_FROZEN
AUTHORIZATION_CERTIFICATE   = NOT_ISSUED
FUTURE_RUN                  = NOT_AUTHORIZED
```

The next construction problem is no longer “define Gamma semantics.” It is:

> **Freeze a treatment-blind, non-discretionary rule by which the realized future obligation determines, for every q-kernel pair, whether that pair is future-distinguished, future-equivalent, or not identified.**
