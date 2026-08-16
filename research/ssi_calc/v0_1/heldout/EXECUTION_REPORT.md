# SSI-CALC v0.1 — H24 White-Box Held-Out Execution

Status: `WHITEBOX_HELDOUT_FAILED`

This report records the **first exposure** of the frozen SSI-CALC v0.1 checker to the H24 corpus frozen by PR #26. Neither checker nor held-out object was modified during this run.

## Frozen objects

```text
CHECKER_MERGE_COMMIT = 8eac548f338f0f8463302f2f1746a2c75f8227ca
H24_FREEZE_MERGE_COMMIT = c10eba651c1ae66b32da179c30a1a2a9a0690d90
CHECKER_SHA256 = 12f3256abf2755fe6f1b9fdb104b9f7b3038713f8bab6260b4f09ad956d42baa
H24_SHA256 = 0910569fe786b29f5f1d64c295f8be7f2857ec6447bd2cf3286a336fc121b941
SCHEMA_SHA256 = 9b14274e1bb232daf7dc4eed11f869fb9ed44400b8d682070c23afd41aee12fd
KERNEL_RULE_COUNT = 11
DELTA_CHECKER = 0
DELTA_H24 = 0
DELTA_KERNEL = 0
```

## Primary result

| Metric | SSI-CALC |
|---|---:|
| Decision accuracy | 50.0% |
| Overreach rate | 50.0% |
| False refusal rate | 50.0% |
| Exact status | 37.5% |
| Shallowest failure locus | 37.5% |
| Preservation-aware refusal | 100.0% |
| Missing-authority certificate | 29.2% |
| Reopened-set accuracy | 100.0% |
| Exact certificate | 29.2% |

Confusion matrix:

```text
TP = 6
FP / OVERREACH = 6
FN / FALSE REFUSAL = 6
TN = 6
```

Under the prospectively frozen threshold:

```text
WHITEBOX_HELDOUT_FAILED
```

The failure is decisive because decision accuracy is below 75% **and** overreach exceeds 15%.

## Family localization

| Family | Decision | Exact cert. | Overreach | False refusal |
|---|---:|---:|---:|---:|
| `F1_ORACLE` | 3/3 | 2/3 | 0 | 0 |
| `F2_SUBSTITUTION` | 1/3 | 1/3 | 2 | 0 |
| `F3_COMPOSITION` | 1/3 | 1/3 | 2 | 0 |
| `F4_IDENTITY` | 2/3 | 1/3 | 0 | 1 |
| `F5_PROVENANCE` | 1/3 | 0/3 | 0 | 2 |
| `F6_REGIME` | 1/3 | 0/3 | 0 | 2 |
| `F7_TRANSPORT` | 1/3 | 1/3 | 1 | 1 |
| `F8_FUTURE` | 2/3 | 1/3 | 1 | 0 |

The largest overreach concentrations are substitution and composition. The largest false-refusal concentrations are provenance and regime handling.

## Internal generic baselines

| System | Decision | Overreach | False refusal |
|---|---:|---:|---:|
| SSI-CALC | 50.0% | 50.0% | 50.0% |
| B0 `MATCHING_EDGE_POLICY` | 50.0% | 16.7% | 83.3% |
| B1 `EDGE_PLUS_COMPOSITION_GUARD` | 50.0% | 16.7% | 83.3% |

SSI-CALC therefore does **not** establish an internal decision advantage on H24. It matches both generic baselines in decision accuracy while overreaching more often. It is less conservative than the baselines, reflected in a lower false-refusal rate, but that trade is unacceptable under the frozen overreach-first objective.

The baselines do not provide SSI-style failure localization or preservation certificates, so no fabricated localization comparison is reported.

## What survived

One property survived perfectly:

```text
PRESERVATION_AWARE_REFUSAL_ACCURACY = 100%
REOPENED_SET_ACCURACY = 100%
```

This does not rescue the decision result. It means that when the implementation produces a certificate, it remains disciplined about preserving upstream facts and reopening the expected alternatives on this corpus.

## First-run witnesses

Overreach cases:

```text
CASE-104 F2_SUBSTITUTION: expected UNLICENSED_JURISDICTION_TRANSFER -> observed AUTHORIZED_SCOPED
CASE-105 F2_SUBSTITUTION: expected COMPOSITION_FAILURE -> observed AUTHORIZED_SCOPED
CASE-107 F3_COMPOSITION: expected COMPOSITION_FAILURE -> observed AUTHORIZED
CASE-109 F3_COMPOSITION: expected COMPOSITION_FAILURE -> observed AUTHORIZED
CASE-120 F7_TRANSPORT: expected NOT_IDENTIFIED -> observed AUTHORIZED
CASE-122 F8_FUTURE: expected NOT_IDENTIFIED -> observed AUTHORIZED
```

False-refusal cases:

```text
CASE-110 F4_IDENTITY: expected AUTHORIZED_SCOPED -> observed UNLICENSED_JURISDICTION_TRANSFER
CASE-113 F5_PROVENANCE: expected AUTHORIZED_SCOPED -> observed PROVENANCE_LEAK
CASE-114 F5_PROVENANCE: expected AUTHORIZED_SCOPED -> observed PROVENANCE_LEAK
CASE-117 F6_REGIME: expected AUTHORIZED_SCOPED -> observed NOT_IDENTIFIED
CASE-118 F6_REGIME: expected AUTHORIZED_SCOPED -> observed UNLICENSED_JURISDICTION_TRANSFER
CASE-119 F7_TRANSPORT: expected AUTHORIZED_SCOPED -> observed UNLICENSED_TRANSPORT
```

There are 17 exact-certificate mismatches in total. `FIRST_RUN.json` is preserved in compressed form and contains every expected/observed certificate pair.

## Diagnostic hypotheses — not repairs

The first run points to several likely implementation boundaries that must be analyzed **after** preserving this result:

- transfer facts may be treated as destination-agnostic;
- pairwise composition evidence may be promoted to whole-chain composition;
- component jurisdictions may not be checked strongly enough during composition;
- explicitly authorized identity transfers are not consumed positively;
- provenance-leak guards may fire even when an independent semantic bridge exists;
- regime admission and carrier-alignment evidence may not compose;
- explicit scoped-to-universal transfer authority is not consumed;
- non-injective transport is rejected before independently constituted quotient semantics can matter;
- `WITHDRAWN` / `UNRESOLVED` facts can be consumed as if active in transport/future checks.

These are hypotheses about the failure-generating implementation. **No checker change is authorized in this execution lineage.** Each proposed correction must be tested against the existing R1..R11 contract before deciding whether the failure is implementation, representation, or genuinely missing calculus capability.

## Measurement defect

`specification_atoms_consumed` was named in the frozen metric set but no prospectively frozen operational definition made SSI-CALC and the baselines commensurable on that dimension.

Status:

```text
SPECIFICATION_ATOMS_CONSUMED = NOT_OPERATIONALIZED
```

The baseline runner records simple atoms-inspected counts only as diagnostics; they are not used for a comparative claim.

## Scientific status

```text
INTERNAL_FROZEN_CONTRACT_PASS = PRESERVED
WHITEBOX_HELDOUT_H24 = FAILED
NICHE_ADVANTAGE_ESTABLISHED = NO
```

This is not a contradiction. The 64-case result established implementation fidelity to its internal authored contract. H24 demonstrates that the same frozen implementation generalizes poorly to hostile novel compositions.

The correct next transition is **failure localization**, not benchmark repair and not immediate rule growth.
