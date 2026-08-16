# SSI-CALC v0.1 — Live-Authority Substrate Repair

## Result

The HF16-earned successor-v2 implementation repairs the known authority-state failure surface **without changing R1..R11**.

```text
KERNEL_RULE_COUNT      = 11
RULES_ADDED_BEYOND_R11 = 0
DELTA_B64              = 0
DELTA_H24              = 0
DELTA_HF16             = 0
```

Final remote regression:

```text
B64   exact certificate = 64/64 = 100%
H24   exact certificate = 24/24 = 100%
HF16  exact certificate = 16/16 = 100%

B64/H24/HF16 overreach      = 0%
B64/H24/HF16 false refusal  = 0%
```

GitHub Actions provenance:

```text
RUN      = 31950311940
JOB      = 95172662508
ARTIFACT = 9264451077
DIGEST   = sha256:f4d61b69e00fcb77028ed118dbf52b2d6ff199ffdc29edf9736aec8922168cfe
HEAD     = 162e5697c10d71f37f637ca4b6f7acbde4dc75ee
```

## Earned implementation distinction

HF16 exposed that selected `ActiveAuthority(...)` checks were insufficient because some local matchers still consumed the raw epistemic substrate.

Successor-v2 makes three states explicit:

```text
EXISTS      fact is retained in historical lineage
LIVE        fact is admitted to the current authority projection
DISCHARGES  live fact/route satisfies the current typed obligation
```

with the hard separation:

```text
EXISTS != LIVE != DISCHARGES
```

The evaluator now maintains historical facts for lineage, explanation, provenance, reopening, and obligation construction, while rule execution is performed over a live-authority projection.

A historical fact may therefore create an obligation without being allowed to satisfy it.

Examples:

- `WITHDRAWN` identity authority remains in lineage but cannot license identity.
- `UNRESOLVED` kernel-containment evidence remains explainable but cannot prove future preservation.
- `PROVENANCE_ONLY` source ancestry may reveal information-flow risk without acquiring detector-safe authority.
- reference-only distinctness may create a transfer obligation without constituting semantic difference.

## Typed bridge discharge

The same distinction applies to bridges.

The evaluator no longer treats mere presence of a `semantic_bridge` token as sufficient. A generic bridge discharge path requires:

1. the source semantic/provenance type to exist in lineage;
2. the bridge itself to be live in the requested jurisdiction;
3. the bridge source type to match the historical source object;
4. the bridge target to match the current obligation jurisdiction.

This is implementation semantics under existing R3 licensing authority, not a new calculus rule.

## Three-run lineage

### Run 1 — execution interface failure

```text
RUN = 31950188837
JOB = 95172364006
```

No cases were adjudicated. The first live projection removed schema-required envelope fields before the already-frozen validator. The correction restored the validation envelope while keeping semantic execution blind to benchmark labels.

This run carries no scientific performance result.

### Run 2 — decisions repaired, legacy certificates exposed

```text
RUN      = 31950237124
JOB      = 95172480845
ARTIFACT = 9264430760
```

```text
B64:  decision 64/64, exact certificate 60/64
H24:  decision 24/24, exact certificate 22/24
HF16: decision 16/16, exact certificate 16/16

ALL THREE:
  overreach     = 0%
  false refusal = 0%
```

The remaining six mismatches were not authorization failures. They showed that some **historical facts legitimately create typed obligations** even though they cannot discharge those obligations.

The minimal correction therefore did not weaken the live-authority membrane. It added historical obligation construction for:

- unresolved feature-information provenance;
- reference-only distinctness;
- incomplete source attribution;
- unresolved transport well-formedness;
- foreign-but-live identity authority;
- support lineage with a live bridge but missing consumer-scoped authority.

### Run 3 — full exact regression

All 104 frozen cases are exact:

```text
64 + 24 + 16 = 104 / 104
```

No rule growth occurred.

## Scientific interpretation

This result supports the narrow implementation hypothesis that the H24/HF16 failures could be repaired by separating historical lineage from current obligation-relative authority.

It does **not** establish fresh generalization because both H24 and HF16 participated in the repair process.

Their permanent roles are now:

```text
B64   contract conformance
H24   known-failure regression
HF16  known-failure regression
```

The strongest status is therefore:

```text
KNOWN_AUTHORITY_STATE_FAILURES_REPAIRED = YES
THREE_SUITE_EXACT_REGRESSION_PASS       = YES
R12_AUTHORIZED                           = NO
GENERALIZATION_ESTABLISHED               = NO
NICHE_ADVANTAGE_ESTABLISHED              = NO
```

## Next transition

Freeze this successor-v2 implementation on `main` before constituting any new test object.

Only after that freeze may a fresh post-substrate test set be created. That object must not be used to repair this implementation before its first exposure.
