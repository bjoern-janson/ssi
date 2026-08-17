# SSI Relicense Interaction Interface V0.1 — First Identifiability Result

Status: `PAIR_IDENTIFIABILITY_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE`

This result evaluates only whether the prospectively frozen candidate interaction representation preserves distinctions required by the frozen higher-order oracle on the paired suite.

It does **not** evaluate detection, witness sufficiency, entitlement, or composition.

---

# 1. Frozen lineage

```text
PARENT_PR53_HEAD
    = 8753a936ff39efb35d2f37f2ef81efb1ee39e957

SPEC_COMMIT
    = d52ff9d5885d360cbe86f61eb01bdd951b305b83

PAIRS_COMMIT
    = 57300a384b4dddee89e3f9fa880954720f93f4a3

EXECUTION_PROTOCOL_COMMIT
    = f04a78092b6afe51dfcc4c321f1a0647b7c74d6c
```

No parent F4 artifact, Relicense Calculus artifact, SSI-CALC object, behavior object, or JEPA state was modified.

---

# 2. Baseline lower-interface diagnosis

For each of the three primary adversarial pairs I1-I3, the local interface is frozen identically:

```text
Phi_local(x) = (W_tr^12, W_tr^23)
```

with the same canonical local records:

```text
LOCAL12_CANONICAL = PRESERVED
LOCAL23_CANONICAL = PRESERVED
```

The independently frozen higher-order oracle differs within each primary pair.

Therefore, pairwise:

```text
Phi_local(a) = Phi_local(b)
AND
E_123(a) != E_123(b)
```

for:

```text
I1 SHARED_STATE_ALIAS
I2 ORDER_DEPENDENCE
I3 CROSS_BOUNDARY_EFFECT
```

Under the frozen working criterion, the unchanged local interface is:

```text
NON_IDENTIFYING
```

for all three primary pairs.

This is a bounded pairwise diagnosis, not a universal theorem about local transport interfaces.

---

# 3. Candidate interaction semantic projection

The frozen evaluator compares only:

```text
Psi_int = (
    interaction_scope,
    normalized interaction_facts,
    observation_coverage
)
```

with normalized interaction facts retaining:

```text
relation_type
participants
activation_condition
observed_relation
affected_scope
provenance_basis
```

and excluding unique identifiers, hashes, timestamps, serialization order, oracle labels, and expected results.

---

# 4. Pair results

## I1 — shared-state alias

Local interface:

```text
identical
```

Candidate semantic distinction:

```text
A: SHARED_STATE_ALIAS observed_relation = DISJOINT
B: SHARED_STATE_ALIAS observed_relation = ALIASED_WITH_AUTHORITY_SENSITIVE_COLLISION
```

Frozen higher-order oracle:

```text
A: NO_ACTIVE_DEFEATER_IN_FROZEN_INTERACTION_MODEL
B: ACTIVE_DEFEATER_IN_FROZEN_INTERACTION_MODEL
```

Result:

```text
PAIR_IDENTIFYING
```

The separating field belongs to the prospectively frozen interaction vocabulary and is scoped to `composed_boundary:J1->J3`.

## I2 — order dependence

Local interface:

```text
identical
```

Candidate semantic distinction:

```text
A: ORDER_DEPENDENCE observed_relation = COMMUTES_ON_AUTHORITY_RELEVANT_STATE
B: ORDER_DEPENDENCE observed_relation = NONCOMMUTATIVE_AUTHORITY_GUARD_FLIP
```

Frozen higher-order oracle differs.

Result:

```text
PAIR_IDENTIFYING
```

## I3 — cross-boundary effect

Local interface:

```text
identical
```

Candidate semantic distinction:

```text
A: CROSS_BOUNDARY_EFFECT = NO_WRITE_TO_J3_ADMISSIBILITY_STATE
B: CROSS_BOUNDARY_EFFECT = WRITE_ALTERS_J3_ADMISSIBILITY_STATE
```

Frozen higher-order oracle differs.

Result:

```text
PAIR_IDENTIFYING
```

## I4 — identifier-leakage negative control

The two records deliberately differ in:

```text
case_id
provenance object_id
challenge object_id
```

while their semantic interaction projection is identical and their higher-order oracle label is identical.

After applying the frozen semantic projection:

```text
Psi_int(A) = Psi_int(B)
```

Result:

```text
NEGATIVE_CONTROL_PASS
```

The interface does not win through unique-identifier leakage.

## I5 — unknown versus positive interaction

A has:

```text
interaction_facts = []
observation_coverage = UNKNOWN
```

B has an observed `EMERGENT_CONSTRAINT`:

```text
COMPOSED_PRECONDITION_VIOLATION
```

The semantic projections differ.

Result:

```text
EPISTEMIC_UNKNOWN_CONTROL_PASS
```

Crucially, no claim is made that the unknown case has no interaction or that it is preserved.

The only supported distinction is:

```text
UNKNOWN != OBSERVED_POSITIVE_INTERACTION
```

---

# 5. Aggregate metrics

```text
PRIMARY_DISCRIMINATING_PAIRS          = 3
PRIMARY_PAIR_IDENTIFICATION_ACCURACY  = 3 / 3
NEGATIVE_CONTROL_PASS                 = true
EPISTEMIC_UNKNOWN_CONTROL_PASS        = true
LOCAL_CERTIFICATE_MUTATIONS           = 0
ORACLE_LABEL_LEAKAGE_EVENTS           = 0
IDENTIFIER_ONLY_SEPARATIONS            = 0
```

All frozen validity gates pass.

---

# 6. Supported bounded result

The candidate interaction representation is:

```text
PAIR_IDENTIFYING_ON_FROZEN_CONSTRUCTED_SUITE
```

The strongest supported claim is:

> **On the prospectively frozen paired suite, the candidate interaction representation preserves higher-order-relevant distinctions that the unchanged pair of local transport records does not preserve.**

Equivalently, on these pairs:

```text
Phi_local(a) = Phi_local(b)
```

while:

```text
Psi_int(Phi_int(a)) != Psi_int(Phi_int(b))
```

for the three frozen higher-order discriminations.

---

# 7. What this does not establish

This result is intentionally below sufficiency.

It does not establish:

```text
that the interface detects all real interactions
that the descriptive interaction vocabulary is complete
that a represented interaction fact is sufficient for REVOKED
that absence of a represented interaction is sufficient for PRESERVED
that W_int is a sufficient witness
that W_comp exists
that certificates compose
that the interaction interface generalizes beyond the frozen suite
formal soundness
empirical validity
```

It also does not establish blind interface invention.

The candidate vocabulary was constituted **after F4 exposed the missing interaction dimension**. Therefore this is best classified as:

```text
INTERFACE_CORRECTION_AFTER_DIAGNOSIS
```

not:

```text
LEVEL_3_BLIND_INTERFACE_INVENTION
```

This preserves the older program result:

> **Interface correction is easier than interface discovery.**

---

# 8. Higher-order non-identifiability hypothesis status

The F4/F5 synthesis remains a working research hypothesis:

```text
HIGHER_ORDER_NONIDENTIFIABILITY
    = WORKING_RESEARCH_HYPOTHESIS
```

This execution adds a different kind of support:

```text
candidate higher-order interface can resolve the prospectively constructed F4-style pair distinctions
```

It does not convert the synthesis into a theorem.

The recursive research pattern remains a candidate:

```text
certificate sound at level k
+ higher-order question at level k+1
+ Phi_k collapses states with different E_(k+1)
-> higher-order non-identifiability for that question
```

and the key non-collapse remains:

```text
expressive insufficiency at k+1
!=
unsoundness at k
```

---

# 9. Next scientific boundary

The representation question has now been answered positively on the frozen constructed suite.

The next layer is **not composition**.

It is:

```text
DETECTION
```

Specifically:

> **Given an interaction interface capable of representing the relevant distinction, what independent observation process can populate that interface without inheriting the blindness of the local certificates?**

Only after detection should the program ask whether any detected interaction structure is a sufficient witness for `PRESERVED`, `REVOKED`, or another entitlement status.

This ordering preserves:

```text
representation
-> identifiability
-> detection
-> witness sufficiency
-> entitlement
-> composition
```

---

# 10. Authority ceiling

```text
OBJECT = SSI_RELICENSE_INTERACTION_INTERFACE_V0.1
STATUS = PAIR_IDENTIFIABILITY_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
HIGHER_ORDER_NONIDENTIFIABILITY = WORKING_RESEARCH_HYPOTHESIS
INTERFACE_CORRECTION = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
BLIND_INTERFACE_INVENTION = NOT_CLAIMED
DETECTABILITY = OPEN
DETECTION_COMPLETENESS = OPEN
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

The governing result is:

> **The distinction can now be represented on the frozen cases. Nothing has yet earned the right to consume it.**
