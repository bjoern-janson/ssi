# SSI-CALC v0.1 — HF16 First Exposure

Status: `HF16_FAILED`

HF16 was constituted after the Compass-orchestration successor was frozen and merged before first exposure. This report records the first remote execution without modifying either object.

## Frozen inputs

```text
SUCCESSOR_FREEZE_MERGE = 87322c273ca9db1e9ae8d90a2ceb7faf272f75c1
HF16_FREEZE_MERGE      = 61ef09fa28959a6c7a5124c4e0c42a4f59d5bfc6
HF16_SHA256            = 0744abe38f6d32b32eace1862b571246d5bb256f47b76b4bf179b5c9404372a7
KERNEL_RULE_COUNT      = 11
RULES_ADDED_BEYOND_R11 = 0
```

GitHub Actions first exposure:

```text
RUN      = 31949675994
JOB      = 95171110165
ARTIFACT = 9264282865
```

## Result

```text
TP = 6
FP / OVERREACH = 3
FN / FALSE REFUSAL = 2
TN = 5
```

| Metric | HF16 |
|---|---:|
| Decision accuracy | 68.75% |
| Overreach rate | 37.5% |
| False refusal rate | 25.0% |
| Exact status | 68.75% |
| Shallowest locus | 68.75% |
| Preservation-aware refusal | 100% |
| Missing-authority certificate | 68.75% |
| Reopened-set accuracy | 100% |
| Exact certificate | 68.75% |

The prospectively frozen threshold therefore returns:

```text
HF16_FAILED
```

because decision accuracy is below 75% and overreach exceeds 25%.

## Five fresh failures

### CASE-208 — identity authority liveness

Expected:

`NOT_IDENTIFIED@EQUIV`

Observed:

`AUTHORIZED_SCOPED@NONE`

The identity-by-denotation authority had been withdrawn, but the local identity matcher still consumed the fact as if live.

### CASE-209 — bridge discharge on a new operation

Expected:

`AUTHORIZED_SCOPED@NONE`

Observed:

`PROVENANCE_LEAK@PROVENANCE`

An independently constituted metadata→validity semantic bridge was present, but the successor's positive bridge handling was operation-specific rather than a general scoped discharge mechanism.

### CASE-213 — withdrawn negative transport fact

Expected:

`AUTHORIZED@NONE`

Observed:

`UNLICENSED_TRANSPORT@TRANSPORT`

A withdrawn `non_injective` claim still triggered a local negative guard even though the active transport premises licensed the operation.

### CASE-214 — withdrawn positive transport fact

Expected:

`NOT_IDENTIFIED@TRANSPORT`

Observed:

`AUTHORIZED@NONE`

A withdrawn target-independence fact still discharged a positive local premise.

### CASE-216 — unresolved preservation proof

Expected:

`NOT_IDENTIFIED@PRESERVE`

Observed:

`AUTHORIZED_SCOPED@NONE`

An unresolved kernel-containment fact still discharged preservation.

## What generalized

The result is not a return to the original H24 failure surface. Several repaired mechanisms generalized successfully to fresh structure:

- multi-hop information-flow ancestry;
- three-hop transfer-route composition;
- refusal of a partial transfer-route certificate;
- whole-chain composition;
- refusal of an unresolved component-jurisdiction transfer;
- admitted-regime comparison on an active shared carrier;
- preservation-aware refusal;
- reopened-set discipline.

In particular, the successor did learn useful route-composition behavior. HF16 instead exposed a more general implementation problem:

> **Authority liveness is still implemented as selected orchestration patches around a frozen matcher whose local predicates often treat fact presence as sufficient.**

The dual failure is also fresh:

> **Positive bridge discharge remains operation-specific rather than typed and uniform.**

## Scientific interpretation

The H24 repair result remains valid as known-failure regression:

```text
B64 = 64/64 exact
H24 = 24/24 exact regression
```

HF16 shows that this does not generalize strongly enough to a new placement of the same authority-liveness principle.

Therefore:

```text
KNOWN_FAILURES_REPAIRED                          = YES
POST_REPAIR_WHITEBOX_GENERALIZATION_IN_HF16     = NOT_SUPPORTED
GENERALIZATION_ESTABLISHED                       = NO
NICHE_ADVANTAGE_ESTABLISHED                      = NO
```

This is not evidence for R12. No failure classification or repair is authorized by this execution lineage.

The next earned object is a five-witness failure analysis asking whether the shallowest defect is still implementation/orchestration, a representation problem, or an actually missing calculus capability. The successor and HF16 remain frozen until that analysis exists.
