# SSI-CALC v0.1 — HF16 Post-Repair Fresh Terrain

Status: `PROSPECTIVE_FRESH_FREEZE_CANDIDATE`

HF16 is constituted **after** the Compass-orchestration successor was frozen on `main` at merge commit:

`87322c273ca9db1e9ae8d90a2ceb7faf272f75c1`

The successor must not be executed on HF16 until this freeze object is merged.

## Epistemic role

```text
B64  = contract conformance
H24  = known-failure regression only
HF16 = fresh post-repair generalization test
```

HF16 cannot establish external niche advantage because its author has white-box knowledge of the research program and successor architecture. It can, however, falsify the claim that the orchestration repair generalizes beyond the exact 17 H24 repair witnesses.

## Corpus

HF16 contains 16 balanced cases: two per existing authority-transfer family, with 8 expected authorize decisions and 8 expected non-authorize decisions.

The cases are not literal extensions of the 17 H24 repairs. They move the same governing invariants into structurally different compositions:

- multi-hop information-flow ancestry rather than the H24 one-hop lineage;
- three-hop jurisdiction transfer chains and partial route certificates;
- whole-chain composition and unresolved component-transfer authority;
- active-authority gating inside identity premises;
- a semantic bridge applied to metadata→validity rather than hash→equivalence;
- admitted regimes using a shared carrier, including a withdrawn alignment;
- withdrawn negative/positive transport premises in new positions;
- unresolved kernel-containment evidence as the preservation proof.

The scientific question is not whether HF16 resembles a product workload. It is:

> Did the implementation learn a reusable authority-orchestration discipline, or only the specific placements exposed by H24?

## Frozen execution rule

After merge:

```text
DELTA_HF16_AFTER_EXPOSURE = 0
DELTA_EXPECTED_AFTER_EXPOSURE = 0
DELTA_SUCCESSOR_DURING_FIRST_RUN = 0
DELTA_METRICS_AFTER_EXPOSURE = 0
```

The successor first-run result must be preserved before any later correction.

Family labels, titles, and expected certificates remain scoring metadata and may not enter derivation.

## Metrics

Report separately:

```text
DECISION_ACCURACY
OVERREACH_RATE
FALSE_REFUSAL_RATE
EXACT_STATUS_ACCURACY
SHALLOWEST_LOCUS_ACCURACY
PRESERVATION_AWARE_REFUSAL_ACCURACY
MISSING_AUTHORITY_ACCURACY
REOPENED_SET_ACCURACY
EXACT_CERTIFICATE_ACCURACY
```

`AUTHORIZED` and `AUTHORIZED_SCOPED` count as authorize decisions. All other statuses count as non-authorize.

## Frozen result labels

Because HF16 is balanced but small, thresholds are fixed prospectively:

- `HF16_STRONG_PASS`: 16/16 decisions, zero overreach, zero false refusal.
- `HF16_PASS`: decision accuracy >= 0.875, overreach <= 0.125, false refusal <= 0.125.
- `HF16_PARTIAL`: decision accuracy >= 0.75 but pass thresholds fail.
- `HF16_FAILED`: decision accuracy < 0.75 or overreach > 0.25.

Exact-certificate dimensions are reported independently and cannot be hidden by the decision label.

## Authority ceiling

Even `HF16_STRONG_PASS` would mean only:

`POST_REPAIR_WHITEBOX_GENERALIZATION_SUPPORTED_IN_HF16`

It would not establish formal completeness, external generalization, or `NICHE_ADVANTAGE_ESTABLISHED`.
