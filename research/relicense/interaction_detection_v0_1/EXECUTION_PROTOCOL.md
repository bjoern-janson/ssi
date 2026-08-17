# SSI Relicense Interaction Detection V0.1 — Execution Protocol

Status: `FROZEN_BEFORE_EXECUTION`

Bound objects:

```text
SPEC_COMMIT      = cec1368839b0711cca35dce0e7572774cc1a135b
WORLDS_COMMIT    = 4b051bc96400eb99c3205082afd924726709200a
DETECTORS_COMMIT = f0a048b8802e85001012121a384495751aa378e9
ORACLE_COMMIT    = dd5e4d077b8faf703c31c3ed02e7c47a52c550a7
PARENT_PR54_HEAD = d80c6c4d60a15fda892c7b34c775358041c1daaa
```

No bound object may be edited during adjudication.

---

## 1. Execution order

For each of the four primary pairs:

1. Verify both worlds reference the canonical local interface.
2. Verify both worlds reference the canonical deterministic local-derived closure.
3. Run D0 on the canonical local interface.
4. Run D1 on the canonical local interface plus local-derived closure.
5. Run D2 on each world's own raw probe.
6. Compare D2 outputs with the frozen descriptive interaction oracle.
7. Run D3 by replacing each world's own raw probe with the prospectively frozen `recipient_to_source_world` probe while keeping the D2 algorithm unchanged.
8. Measure pair separation for D0-D3.

Then run the two controls:

```text
C1 identifier leakage control
C2 UNKNOWN coverage control
```

No transition-status adjudication is executed.

---

## 2. Metrics

Primary metrics:

```text
PRIMARY_PAIRS
D0_PAIR_SEPARATION
D1_PAIR_SEPARATION
D2_PAIR_SEPARATION
D2_STATE_EXACT
D2_FACT_EXACT
D3_PAIR_SEPARATION
```

Control metrics:

```text
D3_PROBE_COUNT_PRESERVED
D3_PROBE_TYPE_HISTOGRAM_PRESERVED
D3_STATE_MARGINAL_PRESERVED
IDENTIFIER_ONLY_SEPARATIONS
UNKNOWN_AS_NEGATIVE_COLLAPSES
LOCAL_CERTIFICATE_MUTATIONS
ORACLE_ENTITLEMENT_LABEL_LEAKAGE
```

A pair is separated iff detector `state` differs between its two members. Descriptive `fact` is scored separately.

---

## 3. Expected control logic

D0 and D1 are intentionally quotient-dependent controls. Their failure to separate is required evidence that the benchmark really holds the local quotient fixed.

```text
D0_PAIR_SEPARATION expected = 0/4
D1_PAIR_SEPARATION expected = 0/4
```

If D0 or D1 separates any primary pair:

```text
PAIR_LEAKAGE = true
scientific adjudication stops at benchmark/procedure defect
```

D2 is the only candidate independent channel.

D3 is a correspondence-destroyed control. Its probe multiset is identical to D2's primary probe multiset, but probe/world assignment is changed. The frozen permutation was selected prospectively to preserve global probe/state marginals while eliminating pair-level discrimination.

```text
D3_PAIR_SEPARATION expected = 0/4
```

---

## 4. Scientific adjudication

Apply the shallowest applicable status.

### REPRESENTATION_FAILURE

Use only if the inherited `Phi_int` cannot encode the oracle distinction. Because PR #54 already passed the frozen constructed identifiability suite, this status requires a new representation mismatch in the present worlds; it may not be inferred merely from detector failure.

### PAIR_LEAKAGE

Diagnostic preemption if D0/D1 separate a claimed quotient-identical pair, or if identifiers/oracle labels enter the discriminating path.

### CHALLENGE_DEPENDENCE

Applies to D0/D1 by construction and to any other detector whose discriminating information is reducible to the frozen local quotient/closure.

### DETECTION_BLINDNESS

Use if representation remains adequate, D0/D1 controls are clean, but D2 fails to recover a frozen interaction distinction from its independently constituted raw observation channel.

### DETECTION_SUPPORTED

May be assigned only if all are true:

```text
D0_PAIR_SEPARATION = 0/4
D1_PAIR_SEPARATION = 0/4
D2_PAIR_SEPARATION = 4/4
D2_STATE_EXACT = 8/8 on primary worlds
D2_FACT_EXACT = 8/8 on primary worlds
D3_PAIR_SEPARATION = 0/4
D3 probe count/type/state marginals preserved
C1 identifier leakage control passes
C2 UNKNOWN remains UNKNOWN
LOCAL_CERTIFICATE_MUTATIONS = 0
ORACLE_ENTITLEMENT_LABEL_LEAKAGE = 0
```

If assigned, the exact claim is:

```text
INDEPENDENT_HIGHER_ORDER_DETECTION_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
```

---

## 5. Authority ceiling

Even `DETECTION_SUPPORTED` cannot be consumed as:

```text
WITNESS_SUFFICIENT
PRESERVED
REVOKED
EXTENDED
W_int
W_comp
COMPOSITION_VALID
```

No execution step asks whether an observed interaction is defeating, preserving, or sufficient.

The experiment ends at detection.
