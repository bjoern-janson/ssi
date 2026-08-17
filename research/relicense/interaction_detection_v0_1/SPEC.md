# SSI Relicense Interaction Detection V0.1

Status: `PROSPECTIVE_FORMAL_DETECTION_EXPERIMENT__WITNESS_LAYER_CLOSED`

Parent object:

```text
SSI_RELICENSE_INTERACTION_INTERFACE_V0.1
PR54_HEAD = d80c6c4d60a15fda892c7b34c775358041c1daaa
```

This experiment opens **detection only**. It does not test witness sufficiency, transition entitlement, or composition.

Scientific question:

> **Can a prospectively independent observation channel recover a higher-order interaction distinction that is provably absent from the frozen local transport quotient?**

---

## 1. Frozen research ladder

```text
representation
-> identifiability
-> detection
-> witness sufficiency
-> entitlement
-> composition
```

Hard firewalls:

```text
representation != identifiability
identifiability != detection
detection != witness sufficiency
DETECTION_SUPPORTED !=> WITNESS_SUFFICIENT
WITNESS_SUFFICIENT !=> DERIVATION_RULE
validity != transportability != composability
```

`W_int`, `W_comp`, and every composition rule remain closed.

---

## 2. Quotient-relative definition of independence

Let the frozen local interface induce:

```text
x_a ~_local x_b
iff
Phi_local(x_a) = Phi_local(x_b)
```

where:

```text
Phi_local(x) = (W_tr^12 visible record, W_tr^23 visible record)
```

Architectural separation is not sufficient for independence.

Any detector of the form:

```text
D = g o Phi_local
```

or any detector using only features in the permitted deterministic local closure:

```text
C_local = { f(Phi_local) | f permitted by the frozen procedure }
```

is classified as `CHALLENGE_DEPENDENCE`, regardless of code complexity, feature count, model class, or separate input fields.

For this frozen suite, evidence of genuinely new discriminating access requires at least one pair with:

```text
Phi_local(x_a) = Phi_local(x_b)
AND
I_123(x_a) != I_123(x_b)
AND
D_int(x_a) != D_int(x_b)
```

and the separation must be attributable to a channel not functionally determined by the frozen local quotient on that pair.

This is a **suite-relative discrimination claim**, not a proof of global statistical or causal independence.

---

## 3. Detection target

The detection target is descriptive interaction state, not entitlement.

Allowed target states:

```text
INTERACTION_PRESENT
INTERACTION_ABSENT
UNKNOWN
```

A detector may also emit a descriptive fact in the already-frozen PR #54 vocabulary:

```text
SHARED_STATE_ALIAS
ORDER_DEPENDENCE
CROSS_BOUNDARY_EFFECT
EMERGENT_CONSTRAINT
```

No detector output may contain or derive:

```text
PRESERVED
EXTENDED
REVOKED
UNPROVEN
WITNESS_SUFFICIENT
COMPOSITION_VALID
oracle entitlement labels
```

In particular:

```text
INTERACTION_PRESENT !=> REVOKED
INTERACTION_ABSENT !=> PRESERVED
UNKNOWN != INTERACTION_ABSENT
```

---

## 4. Prospectively frozen raw observation channels

D2 receives raw observations rather than pre-labeled interaction facts.

### 4.1 Alias-token probe

Raw fields:

```text
phase12_token
phase23_token
coverage
```

Mechanical semantic rule:

```text
coverage = UNKNOWN -> state = UNKNOWN
phase12_token = phase23_token -> INTERACTION_PRESENT
otherwise -> INTERACTION_ABSENT
```

Descriptive facts:

```text
present -> ALIASED_WITH_AUTHORITY_SENSITIVE_COLLISION
absent  -> DISJOINT
```

### 4.2 Order-reversal probe

Raw fields:

```text
forward_authority_state
reverse_authority_state
coverage
```

Mechanical semantic rule:

```text
coverage = UNKNOWN -> state = UNKNOWN
forward_authority_state != reverse_authority_state -> INTERACTION_PRESENT
otherwise -> INTERACTION_ABSENT
```

Descriptive facts:

```text
present -> NONCOMMUTATIVE_AUTHORITY_GUARD_FLIP
absent  -> COMMUTES_ON_AUTHORITY_RELEVANT_STATE
```

### 4.3 Cross-boundary effect trace

Raw fields:

```text
writes[]
coverage
```

Mechanical semantic rule:

```text
coverage = UNKNOWN -> state = UNKNOWN
any write target == J3.admissibility_state -> INTERACTION_PRESENT
otherwise -> INTERACTION_ABSENT
```

Descriptive facts:

```text
present -> WRITE_ALTERS_J3_ADMISSIBILITY_STATE
absent  -> NO_WRITE_TO_J3_ADMISSIBILITY_STATE
```

### 4.4 Composed-precondition probe

Raw fields:

```text
j2_post_quota
j3_required_quota_min
coverage
```

Mechanical semantic rule:

```text
coverage = UNKNOWN -> state = UNKNOWN
j2_post_quota < j3_required_quota_min -> INTERACTION_PRESENT
otherwise -> INTERACTION_ABSENT
```

Descriptive facts:

```text
present -> COMPOSED_PRECONDITION_VIOLATION
absent  -> COMPOSED_PRECONDITION_SATISFIED
```

These rules are frozen before the world suite and before the detector implementation.

---

## 5. D0-D3 adversarial/control ladder

The detector ladder is fixed as follows.

### D0 — local quotient control

Inputs:

```text
Phi_local only
```

Classification:

```text
CHALLENGE_DEPENDENCE
```

It must not separate any critical pair whose local quotient is equal.

### D1 — elaborated local derivative control

Inputs:

```text
Phi_local + frozen deterministic local-derived closure
```

All added features are functions of `Phi_local`.

Classification:

```text
CHALLENGE_DEPENDENCE
```

A critical-pair separation by D1 is `PAIR_LEAKAGE`, not evidence of independence.

### D2 — independently constituted raw interaction probe

Inputs:

```text
raw probe observations from Section 4
```

D2 applies only the prospectively frozen mechanical semantic rules.

Possible positive classification:

```text
DETECTION_SUPPORTED
```

but only if D0/D1 fail to separate the quotient-identical critical pairs, D2 recovers the frozen descriptive interaction state, anti-leakage controls pass, and D3 behaves as expected.

### D3 — correspondence-destroyed probe control

D3 uses the same D2 algorithm and the same multiset of primary raw probe records, but a prospectively frozen permutation destroys probe-to-world correspondence.

Required preservation:

```text
same number of probe records
same probe-type counts
same INTERACTION_PRESENT/INTERACTION_ABSENT marginal counts under the frozen mechanical rules
same serialization schema
```

Required destruction:

```text
probe record no longer belongs to the world receiving it
```

A successful control should remove pair-level discrimination while retaining these global marginals.

---

## 6. Failure taxonomy

Frozen scientific statuses:

```text
REPRESENTATION_FAILURE
DETECTION_BLINDNESS
CHALLENGE_DEPENDENCE
DETECTION_SUPPORTED
```

Definitions:

```text
REPRESENTATION_FAILURE:
Phi_int cannot encode the higher-order distinction.

DETECTION_BLINDNESS:
Phi_int can encode the distinction, but the prospectively independent D2 channel fails to recover it.

CHALLENGE_DEPENDENCE:
Apparent discrimination is reducible to Phi_local or its permitted deterministic closure.

DETECTION_SUPPORTED:
The independently constituted D2 channel recovers the frozen higher-order interaction distinction and survives the specified controls.
```

Diagnostic, not scientific status:

```text
PAIR_LEAKAGE
```

`PAIR_LEAKAGE` fires if D0 or D1 separates a pair claimed to be quotient-identical, or if identifiers/oracle labels enter the discriminating path. It diagnoses a benchmark/procedure defect before any theoretical revision.

---

## 7. Primary success criteria

For every critical pair:

```text
Phi_local(a) == Phi_local(b)
C_local(a) == C_local(b)
I_123(a) != I_123(b)
```

Required pattern:

```text
D0 pair separation = 0
D1 pair separation = 0
D2 pair separation = 1
D2 semantic state recovery = correct
```

Aggregate D3 requirement:

```text
primary pair separation collapses under the frozen correspondence-destroying permutation
```

Hard anti-cheating constraints:

```text
LOCAL_CERTIFICATE_MUTATIONS = 0
ORACLE_ENTITLEMENT_LABEL_LEAKAGE = 0
IDENTIFIER_ONLY_SEPARATIONS = 0
UNKNOWN_AS_NEGATIVE_COLLAPSES = 0
```

---

## 8. Epistemic ceiling

Even a perfect positive run licenses only:

```text
INDEPENDENT_HIGHER_ORDER_DETECTION_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
```

It does not establish:

```text
general detector soundness
detection completeness
interaction ontology completeness
real-world empirical detection
causal independence
witness sufficiency
PRESERVED sufficiency
REVOKED sufficiency
W_int sufficiency
W_comp
certificate composition
formal soundness
```

A negative D2 result after representation success is preserved as:

```text
REPRESENTABLE_DOES_NOT_IMPLY_DETECTABLY_ACCESSIBLE_ON_TESTED_CHANNELS
```

The governing line is:

> **Hold the local quotient fixed. Vary the higher-order interaction. Then ask whether reality has another route into the detector.**
