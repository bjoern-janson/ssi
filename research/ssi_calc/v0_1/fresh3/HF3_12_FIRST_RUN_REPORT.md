# HF3-12 First Exposure

## Frozen result

```text
HF3_12_STRONG_PASS
```

The prospective strong-pass criterion was decision-level:

```text
12/12 decisions
0% overreach
0% false refusal
```

All three targeted structural classes were adjudicated correctly at the authorize/refuse level:

```text
ALTERNATIVE_SUFFICIENT
CONJUNCTIVE_REQUIRED
ACTIVE_DEFEATER
```

## Metrics

```text
DECISION_ACCURACY = 12/12 = 100%
OVERREACH = 0/6 = 0%
FALSE_REFUSAL = 0/6 = 0%
LOCUS_ACCURACY = 100%
PRESERVATION_ACCURACY = 100%
MISSING_AUTHORITY_ACCURACY = 100%
REOPENED_ACCURACY = 100%
EXACT_STATUS_ACCURACY = 11/12 = 91.67%
EXACT_CERTIFICATE_ACCURACY = 11/12 = 91.67%
```

Remote identifiers:

```text
RUN = 31951747818
JOB = 95176155518
ARTIFACT = 9264823939
DIGEST = sha256:132bb2afa6edbeece10676d2fc2c6b31417045b403ca425715b1b938c277a7de
TESTED_HEAD = 4e325ab61745b770d37dda4322fee9155d6a3e4a
```

## Single certificate mismatch

`CASE-402` was correctly authorized, with correct locus, preserved facts, missing-authority set, and reopen set, but emitted `AUTHORIZED` rather than the frozen expected `AUTHORIZED_SCOPED`.

This mismatch is preserved exactly. No case, expectation, successor, or threshold is changed in this execution lineage.

The mismatch must be classified separately before any repair. In particular, the existence of a decision-level strong pass does not authorize post-hoc normalization of certificate granularity.

## Authority ceiling

```text
POST_OBLIGATION_RESOLUTION_WHITEBOX_GENERALIZATION = SUPPORTED_AT_DECISION_LEVEL_IN_HF3_12
EXACT_CERTIFICATE_GENERALIZATION = NOT_CLEAN
R12_AUTHORIZED = NO
NICHE_ADVANTAGE_ESTABLISHED = NO
```
