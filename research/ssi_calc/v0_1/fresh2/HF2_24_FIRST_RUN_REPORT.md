# SSI-CALC v0.1 — HF2-24 First Exposure

## Result

The frozen typed live-authority successor-v2 was executed for the first time against the separately frozen HF2-24 corpus.

```text
THRESHOLD_STATUS = HF2_24_PARTIAL
```

Frozen inputs:

```text
SUCCESSOR_V2_FREEZE_MERGE = ed9ae7ab94f74bbc39aaadad312c40647aed62d9
HF2_24_FREEZE_MERGE       = 4c7c2c0d4c91fa420053a552759a16934ab42b50
HF2_24_PLAIN_SHA256       = 96498b2f195cdf6ca99e0c5f4efbf99305f2bc7168ff008eda3f6cca14c78218
KERNEL_RULE_COUNT         = 11
RULES_ADDED_BEYOND_R11    = 0
DELTA_SUCCESSOR           = 0
DELTA_HF2_24              = 0
```

GitHub Actions provenance:

```text
RUN      = 31950896524
JOB      = 95174071387
ARTIFACT = 9264604486
DIGEST   = sha256:ebe087917cf21e269bf77ed6cffd91bdb4a4f1756fbb82e3d5178dba7124b623
HEAD     = d895f585a9eccf4e0a531a2e5f178c94a08a3474
```

## Metrics

```text
TP = 10
FP / OVERREACH = 0
FN / FALSE REFUSAL = 2
TN = 12

DECISION_ACCURACY                   = 22 / 24 = 91.67%
OVERREACH_RATE                      =  0 / 12 = 0%
FALSE_REFUSAL_RATE                  =  2 / 12 = 16.67%
EXACT_STATUS_ACCURACY               = 91.67%
SHALLOWEST_LOCUS_ACCURACY           = 91.67%
PRESERVATION_AWARE_REFUSAL_ACCURACY = 100%
MISSING_AUTHORITY_ACCURACY          = 91.67%
REOPENED_SET_ACCURACY               = 100%
EXACT_CERTIFICATE_ACCURACY          = 91.67%
```

The prospective `HF2_24_PASS` threshold required false refusal <= 12.5%, so the correct frozen label is `HF2_24_PARTIAL`.

## What generalized

Relative to HF16, the typed live-authority substrate substantially improved fresh behavior:

- fresh overreach fell from 37.5% on HF16 to **0%** on HF2-24;
- decision accuracy rose from 68.75% to **91.67%**;
- preservation-aware refusal remained **100%**;
- reopening remained **100%**.

The successor correctly handled 22 of 24 fresh combinations, including deeper historical obligation triggers, longer transfer routes, mixed-jurisdiction compositions, live authority coexisting with irrelevant historical facts, generic typed bridge target matching, active adverse evidence, and consumer-scoped support.

This is evidence that the `EXISTS != LIVE != DISCHARGES` substrate generalized materially beyond the HF16 repair witnesses.

It is not a full pass.

## Two fresh witnesses

### CASE-312 — identity

Expected:

```text
AUTHORIZED_SCOPED
```

Observed:

```text
NOT_IDENTIFIED
missing = active_identity_by_denotation_authority
```

The case contains an explicit live identity transfer from the source semantic regime into presentation identity while a separate historical `identity_by_denotation` fact is inactive.

The current evaluator lets the inactive alternative path create a blocking obligation before considering the independently sufficient live transfer path.

### CASE-322 — future preservation

Expected:

```text
AUTHORIZED_SCOPED
```

Observed:

```text
NOT_IDENTIFIED
missing = constituted_future_invariance_proof
```

The case contains a live kernel-containment proof sufficient for the requested future consumer, while a separate alternative `future_invariant_under` proof channel is unresolved.

Again, the unresolved alternative path blocks an independently sufficient live proof.

## Diagnostic hypothesis — not yet a repair

The two failures suggest a shared issue:

> **An inactive or unresolved alternative proof path must not block a distinct live path that already discharges the same obligation.**

Equivalently, obligation discharge is currently too conjunctive over represented evidence channels.

The likely next object is not another calculus rule but explicit representation of **alternative sufficient discharge paths** / proof search ordering under the same typed obligation.

That classification is not yet frozen and must be adjudicated separately before any implementation change.

## Scientific state

```text
B64 CONTRACT CONFORMANCE                  = PRESERVED
H24 KNOWN-FAILURE REGRESSION              = PASSED
HF16 KNOWN-FAILURE REGRESSION             = PASSED
HF2_24 FIRST EXPOSURE                     = PARTIAL
POST_SUBSTRATE FRESH OVERREACH            = 0%
POST_SUBSTRATE WHITEBOX GENERALIZATION    = PARTIALLY SUPPORTED, NOT PASSED
R12_AUTHORIZED                            = NO
NICHE_ADVANTAGE_ESTABLISHED               = NO
```

The next earned transition is classification of CASE-312 and CASE-322 before any successor-v3 repair.
