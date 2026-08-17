# SSI Relicense Interaction Interface V0.1

Status: `PROSPECTIVE_FORMAL_INTERFACE_CANDIDATE__IDENTIFIABILITY_ONLY`

This object is stacked on the diagnostic result in PR #53 and does **not** repair or modify that result.

Frozen parent head:

```text
PR53_HEAD = 8753a936ff39efb35d2f37f2ef81efb1ee39e957
```

The scientific target is deliberately earlier than witness sufficiency or composition:

> **What is the smallest interface candidate that can preserve distinctions required by a higher-order interaction-entitlement judgment when the local transport interface collapses those distinctions?**

No composition rule is introduced.
No `W_comp` sufficiency claim is introduced.
No SSI-CALC, behavior, or JEPA object is opened.

---

# 1. Working research hypothesis

The synthesis of F4 and F5 motivates the following **working hypothesis**, not a theorem about all SSI interfaces:

```text
HIGHER_ORDER_NONIDENTIFIABILITY
```

For a lower-level interface `Phi_k` and a higher-level entitlement question `E_(k+1)`, if there exist two admissible states `x_a`, `x_b` such that:

```text
Phi_k(x_a) = Phi_k(x_b)
AND
E_(k+1)(x_a) != E_(k+1)(x_b)
```

then `Phi_k` is non-identifying for that higher-order entitlement question on that pair.

This is a diagnostic criterion for a particular interface/question relation. It does not imply that every lower-level interface is globally inadequate, nor that a unique higher-order interface exists.

F5 supplies one bounded instance:

```text
role-level certificate-visible facts equal
while
whole-execution effect legitimacy differs
```

F4 supplies another bounded instance:

```text
local transport-visible facts equal
while
composed-boundary interaction legitimacy differs
```

The synthesis status is therefore:

```text
HIGHER_ORDER_NONIDENTIFIABILITY = WORKING_RESEARCH_HYPOTHESIS_SUPPORTED_BY_F4_F5_SYNTHESIS
UNIVERSAL_THEOREM = NO
```

---

# 2. Ladder and firewalls

The research ladder is frozen as:

```text
representation
-> identifiability
-> detection
-> witness sufficiency
-> entitlement
-> composition
```

The following non-collapses are first-class:

```text
representation != identifiability
identifiability != detection
identifiability != sufficiency
detection != sufficiency
interface resolution != witness sufficiency
witness sufficiency != derivation rule
derivation rule != empirical result
```

In particular:

```text
IDENTIFIABLE !=> SUFFICIENT
```

A candidate interface may separate two higher-order-relevant cases while still being inadequate to justify `PRESERVED`, `REVOKED`, or any positive composition conclusion.

---

# 3. Frozen lower interface

For the present object, the lower interface is the pair of local transport records inherited unchanged from the parent branch:

```text
Phi_local(x) = (
    W_tr^12 visible record,
    W_tr^23 visible record
)
```

The local records are immutable inputs for the paired experiment.

No candidate interaction interface may change, enrich, rewrite, or reinterpret either local certificate in order to separate a pair.

The target failure pattern is:

```text
Phi_local(x_a) = Phi_local(x_b)
```

while an independently frozen higher-order oracle assigns:

```text
E_123(x_a) != E_123(x_b)
```

where `E_123` concerns only the requested composed-boundary interaction status.

---

# 4. Candidate interaction representation

The candidate interface is **not a witness rule**. It is a representation of cross-boundary facts:

```text
Phi_int^123(x) = (
    boundary_path,
    local_certificate_refs,
    interaction_scope,
    interaction_facts,
    observation_coverage,
    provenance,
    challenge_record
)
```

Its purpose is only to make potentially relevant interaction distinctions representable.

## 4.1 boundary_path

```text
(J1, J2, J3)
```

identifies the composed path being examined.

It does not imply a valid `J1 -> J3` transition.

## 4.2 local_certificate_refs

Immutable references to the two local transport records:

```text
W_tr^12
W_tr^23
```

These references provide lineage only. Their joint presence does not imply composition.

## 4.3 interaction_scope

The exact higher-order scope in which an interaction fact is asserted, for example:

```text
composed_boundary(J1 -> J3)
```

An interaction fact scoped only to another path or another purpose cannot silently transfer.

## 4.4 interaction_facts

A finite set of factual records with the following candidate vocabulary:

```text
interaction_fact = {
    relation_type,
    participants,
    activation_condition,
    observed_relation,
    affected_scope,
    provenance_basis
}
```

Allowed `relation_type` values in V0.1 are intentionally small:

```text
SHARED_STATE_ALIAS
ORDER_DEPENDENCE
CROSS_BOUNDARY_EFFECT
EMERGENT_CONSTRAINT
```

These are **descriptive relation types**, not entitlement labels.

The interface must not contain fields such as:

```text
defeater = true
preserved = true
revoked = true
oracle_label = ...
```

because embedding the target answer would make the identifiability test circular.

## 4.5 observation_coverage

The interface must distinguish positive observation from absence of observation:

```text
OBSERVED
NOT_OBSERVED
UNKNOWN
```

This field is epistemic metadata about coverage, not a transition status.

In particular:

```text
UNKNOWN != NOT_OBSERVED
NOT_OBSERVED != NO_INTERACTION_EXISTS
```

## 4.6 provenance

Each interaction fact must identify the source by which the factual relation was constituted.

Provenance does not grant semantic authority by itself.

## 4.7 challenge_record

The interface may record whether the asserted interaction fact has an independently addressable challenge route.

This is a reopenability property only.

```text
challengeable != true
challengeable != sufficient
```

---

# 5. Semantic projection and anti-cheating rule

Raw serialized objects can differ for irrelevant reasons. Therefore identifiability is evaluated only on a frozen semantic projection:

```text
Psi_int(Phi_int^123(x)) = (
    interaction_scope,
    normalized interaction_facts,
    observation_coverage
)
```

The following fields are excluded from the semantic comparison:

```text
case_id
world_id
record_id
certificate_id
file path
commit SHA
content hash
timestamp
serialization order
provenance object identifier
challenge object identifier
oracle label
expected result
```

Provenance **basis/type** may remain semantically relevant where prospectively declared, but unique identifiers may not.

A candidate interface does not earn identifiability merely because two records have different names or hashes.

---

# 6. Higher-order identifiability criterion

For a frozen discriminating pair `(x_a, x_b)` satisfying:

```text
Phi_local(x_a) = Phi_local(x_b)
AND
E_123(x_a) != E_123(x_b)
```

V0.1 calls the candidate interaction interface **pair-identifying** iff:

```text
Psi_int(Phi_int^123(x_a)) != Psi_int(Phi_int^123(x_b))
```

and all of the following hold:

```text
1. local certificate bytes/references are unchanged across the pair
2. the distinguishing field belongs to the prospectively frozen interaction vocabulary
3. the target oracle label is not present in the interface
4. unique identifiers/hashes/timestamps do not cause the separation
5. the distinction is scoped to the composed boundary being queried
```

This establishes only:

```text
THE RELEVANT DISTINCTION IS REPRESENTABLE ON THIS PAIR
```

It does **not** establish:

```text
that the distinction is detected in all cases
that the represented fact is true in the world beyond its frozen constitution
that it is sufficient for PRESERVED
that it is sufficient for REVOKED
that W_int is sufficient
that W_comp exists
that composition is derivable
```

---

# 7. Non-identifiability and resolution statuses

The interface-level result vocabulary is separate from transition statuses.

Allowed interface statuses:

```text
NON_IDENTIFYING
PAIR_IDENTIFYING
SPURIOUSLY_IDENTIFYING
IDENTIFIABILITY_UNPROVEN
```

Definitions:

### NON_IDENTIFYING

A discriminating pair has different higher-order oracle labels but identical semantic interaction projection:

```text
E_123(x_a) != E_123(x_b)
AND
Psi_int(Phi_int(x_a)) = Psi_int(Phi_int(x_b))
```

### PAIR_IDENTIFYING

The candidate semantic projection distinguishes the frozen pair under the criterion in Section 6.

### SPURIOUSLY_IDENTIFYING

The records differ only through excluded identifiers, serialization artifacts, or target-label leakage.

### IDENTIFIABILITY_UNPROVEN

The pair or interface lacks enough constituted information to decide whether the candidate semantic projection preserves the required distinction.

No interface status is a transition-entitlement status.

---

# 8. Transition statuses remain separate

The parent transport vocabulary remains:

```text
PRESERVED
EXTENDED
REVOKED
UNPROVEN
```

with the strengthened firewall:

```text
UNPROVEN != NOT_PRESERVED
UNPROVEN != REVOKED
```

and:

```text
REVOKED requires positive applicable defeater evidence
```

while:

```text
UNPROVEN does not imply that a defeater exists
```

The interaction interface V0.1 does not itself decide these statuses.

---

# 9. Prospective experiment target

The first experiment will freeze paired formal states such that:

```text
Phi_local(x_a) = Phi_local(x_b)
```

while the higher-order oracle differs because of an interaction that emerges only across the composed path.

The candidate interface will be tested for whether its semantic projection separates the pair **without changing the local certificates**.

The primary metric is:

```text
PAIR_IDENTIFICATION_ACCURACY
```

with hard anti-cheating metrics:

```text
LOCAL_CERTIFICATE_MUTATIONS = 0 required
ORACLE_LABEL_LEAKAGE = 0 required
IDENTIFIER_ONLY_SEPARATIONS = 0 required
```

A positive result is evidence only for interface resolution on the frozen paired suite.

---

# 10. First attack families

The initial suite must include at least:

```text
I1 SHARED_STATE_ALIAS
I2 ORDER_DEPENDENCE
I3 CROSS_BOUNDARY_EFFECT
I4 NEGATIVE_CONTROL_NO_SEMANTIC_DIFFERENCE
```

The first three require local-interface equality with higher-order oracle inequality.

The negative control requires semantically identical interaction conditions and the same higher-order oracle label despite different irrelevant record identifiers, so the candidate must **not** separate the pair semantically.

This prevents a representation from winning through identity leakage.

---

# 11. Authority ceiling

```text
OBJECT = SSI_RELICENSE_INTERACTION_INTERFACE_V0.1
STATUS = PROSPECTIVE_FORMAL_INTERFACE_CANDIDATE__IDENTIFIABILITY_ONLY
HIGHER_ORDER_NONIDENTIFIABILITY = WORKING_RESEARCH_HYPOTHESIS
F4_PARENT_RESULT = PRESERVED_UNREPAIRED
F5_PARENT_RESULT = PRESERVED_UNREPAIRED
IDENTIFIABILITY = OPEN_UNTIL_FROZEN_PAIR_EXECUTION
DETECTABILITY = NOT_TESTED
WITNESS_SUFFICIENCY = NOT_TESTED
W_int = NOT_ADMITTED_AS_SUFFICIENT_WITNESS
W_comp = NOT_DEFINED
COMPOSITION_RULE = NOT_ADMITTED
FORMAL_SOUNDNESS = UNESTABLISHED
EMPIRICAL_VALIDITY = NOT_CLAIMED
SSI_CALC_KERNEL_DELTA = 0
JEPA = PARKED
BEHAVIORAL_EXPERIMENT_AUTHORITY = NONE
```

The governing constraint is:

> **First preserve the distinction. Only then ask whether anything is entitled to consume it.**
