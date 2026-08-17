# SSI Relicense Interaction Detection V0.1 — Result

Status:

```text
DETECTION_SUPPORTED
```

Bounded claim:

```text
INDEPENDENT_HIGHER_ORDER_DETECTION_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
```

This is a **formal constructed-suite result**, not a real-world empirical detector claim and not a witness-sufficiency result.

---

## 1. Freeze lineage

```text
parent PR54 head
  d80c6c4d60a15fda892c7b34c775358041c1daaa

SPEC
  cec1368839b0711cca35dce0e7572774cc1a135b

WORLDS
  4b051bc96400eb99c3205082afd924726709200a

DETECTORS
  f0a048b8802e85001012121a384495751aa378e9

ORACLE
  dd5e4d077b8faf703c31c3ed02e7c47a52c550a7

EXECUTION_PROTOCOL
  e5aad39084705ebf4b7bf006f9fadede964c70b0

EVALUATOR
  e3c445df412422256a34cd1a1fbe18749d94cfe1

RESULT.json
  5f6f5bb4610dea7a2cefc702a237d54863fdd38c
```

The detector specification was frozen before the explicit descriptive oracle file. The oracle contains interaction state/fact only; it contains no transition-entitlement labels.

No bound object was rewritten during adjudication.

---

## 2. Core construction

All eight primary worlds share exactly the same frozen local quotient and permitted deterministic local-derived closure:

```text
Phi_local(x_a) = Phi_local(x_b)
C_local(x_a)   = C_local(x_b)
```

The raw higher-order probes vary across four interaction families:

```text
SHARED_STATE_ALIAS
ORDER_DEPENDENCE
CROSS_BOUNDARY_EFFECT
EMERGENT_CONSTRAINT
```

D0 sees only `Phi_local`.
D1 sees `Phi_local` plus deterministic local-derived features.
D2 sees only the prospectively constituted raw interaction probe.
D3 applies the unchanged D2 algorithm to a frozen correspondence-destroyed permutation of the exact primary probe multiset.

---

## 3. Primary result

```text
PRIMARY_PAIRS                  = 4
PRIMARY_WORLDS                 = 8

D0_PAIR_SEPARATION             = 0/4
D1_PAIR_SEPARATION             = 0/4
D2_PAIR_SEPARATION             = 4/4
D2_STATE_EXACT                 = 8/8
D2_FACT_EXACT                  = 8/8
D3_PAIR_SEPARATION             = 0/4
```

Thus the two quotient-dependent controls fail exactly where they should:

```text
D0 = CHALLENGE_DEPENDENCE
D1 = CHALLENGE_DEPENDENCE
```

while the independently constituted raw probe recovers all four frozen higher-order distinctions:

```text
D2 = DETECTION_SUPPORTED
```

---

## 4. D3 correspondence-destruction control

D3 preserves the full primary raw-probe multiset.

Before and after permutation:

```text
ALIAS_TOKEN_PROBE               = 2
ORDER_REVERSAL_PROBE            = 2
EFFECT_TRACE_PROBE              = 2
COMPOSED_PRECONDITION_PROBE     = 2

INTERACTION_ABSENT              = 4
INTERACTION_PRESENT             = 4
```

Therefore:

```text
D3_PROBE_COUNT_PRESERVED            = true
D3_PROBE_TYPE_HISTOGRAM_PRESERVED   = true
D3_STATE_MARGINAL_PRESERVED         = true
```

Yet pair-level target-state discrimination collapses:

```text
D3_PAIR_SEPARATION = 0/4
```

Important qualification: D3 does **not** make all detector output text identical. Because the wrong donor probes still carry descriptive content, D3 may emit different descriptive `fact` strings within a pair. What collapses is the prospectively scored higher-order **interaction-state contrast** (`INTERACTION_PRESENT` vs `INTERACTION_ABSENT`) for the paired worlds.

So the supported control claim is:

> Preserving probe format, probe-type counts, and interaction-state marginals is not sufficient for correct pair-level detection when probe-to-world correspondence is destroyed.

It is not:

> every descriptive output becomes identical after shuffling.

---

## 5. Anti-leakage and epistemic controls

```text
IDENTIFIER_ONLY_SEPARATIONS          = 0
UNKNOWN_AS_NEGATIVE_COLLAPSES        = 0
LOCAL_CERTIFICATE_MUTATIONS          = 0
ORACLE_ENTITLEMENT_LABEL_LEAKAGE     = 0
```

The identifier-control pair has different world identifiers but identical raw semantic observations and remains unseparated.

The epistemic control preserves:

```text
UNKNOWN != INTERACTION_ABSENT
```

D2 emits `UNKNOWN` when observation coverage is unknown rather than manufacturing negative evidence.

---

## 6. What was earned

On this prospectively frozen constructed suite, there exists a detector input path whose discriminating information is not functionally determined by the frozen local quotient on the critical pairs:

```text
Phi_local(x_a) = Phi_local(x_b)
while
D2(x_a) != D2(x_b)
```

D0 and D1 demonstrate that elaborating the local quotient does not recover the distinction.

D3 demonstrates that the D2 result depends on world-correspondent higher-order observations rather than only the marginal structure of the probe collection.

This supports, on this suite only:

```text
NEW_DISCRIMINATING_CHANNEL_RELATIVE_TO_FROZEN_LOCAL_QUOTIENT = YES
```

and therefore:

```text
INDEPENDENT_HIGHER_ORDER_DETECTION_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
```

The word `independent` here is quotient-relative and suite-relative. It means the D2 discriminating information is not reducible to the frozen `Phi_local`/permitted local-derived closure on the tested pairs. It does **not** establish universal causal or statistical independence.

---

## 7. What was not earned

Nothing in this run establishes:

```text
detection completeness
interaction ontology completeness
general detector soundness
real-world empirical observability
causal independence
witness sufficiency
PRESERVED sufficiency
REVOKED sufficiency
W_int sufficiency
W_comp
certificate composition
formal soundness
```

In particular:

```text
DETECTION_SUPPORTED !=> WITNESS_SUFFICIENT
INTERACTION_PRESENT !=> REVOKED
INTERACTION_ABSENT  !=> PRESERVED
```

No transition status was adjudicated.

---

## 8. Updated frontier

The ladder now reads:

```text
representation       = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
identifiability      = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
independent detection= SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
witness sufficiency  = NOT_TESTED
entitlement           = NOT OPENED
composition           = NOT OPENED
```

This result closes only the first constructed detector attack. It does not yet justify opening witness sufficiency automatically.

Before doing so, the clean next challenge is to attack **detection robustness** itself: fresh held-out interaction worlds, alternative independently constituted probe mechanisms, incomplete/contradictory channel evidence, and detector failure localization.

That is a new experiment, not a repair to this one.

---

## 9. Authority ceiling

```text
OBJECT = SSI_RELICENSE_INTERACTION_DETECTION_V0.1
SCIENTIFIC_STATUS = DETECTION_SUPPORTED
BOUNDED_CLAIM = INDEPENDENT_HIGHER_ORDER_DETECTION_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE

DETECTION_COMPLETENESS = UNESTABLISHED
WITNESS_SUFFICIENCY = NOT_TESTED
W_int = NOT_ADMITTED_AS_SUFFICIENT_WITNESS
W_comp = NOT_DEFINED
COMPOSITION_RULE = NOT_ADMITTED
FORMAL_SOUNDNESS = UNESTABLISHED
EMPIRICAL_REAL_WORLD_DETECTION = NOT_CLAIMED
SSI_CALC_KERNEL_DELTA = 0
JEPA = PARKED
BEHAVIORAL_EXPERIMENT_AUTHORITY = NONE
```
