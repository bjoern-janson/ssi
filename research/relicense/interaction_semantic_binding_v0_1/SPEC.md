# SSI Relicense Interaction Semantic Binding V0.1 — Specification

Status: `PROSPECTIVE_SEMANTIC_BINDING_SPEC_FROZEN__SPEC_ONLY`

Object:

```text
SSI_RELICENSE_INTERACTION_SEMANTIC_BINDING_V0.1
```

This object studies a boundary exposed by the first held-out interaction-detection stress result: an observation can be informative while remaining semantically ill-typed for an already-frozen detector predicate.

The sole research question is:

> **When does a novel observation constitute the same evidence relation required by an existing detector predicate?**

This object does **not** test witness sufficiency, transition entitlement, `W_int`, `W_comp`, composition, or behavioral utility.

---

## 1. Parent provenance

This specification is stacked directly on the completed first-run stress result:

```text
PARENT_OBJECT = SSI_RELICENSE_INTERACTION_DETECTION_STRESS_V0.1
PARENT_PR = 56
PARENT_HEAD = ba650e48976323df4f4361ad3965be1eeaf6e65e
```

The parent result established, boundedly:

```text
G1 world-novelty detection = SUPPORTED
G4 failure-novelty detection = SUPPORTED
G3 degraded-coverage handling = SUPPORTED
G5 contradiction handling = SUPPORTED_AS_CONFLICT_PRESERVATION
G2 state-commitment channel = SEMANTIC_BINDING_BOUNDARY_PRESERVED
G3 complete state-commitment channel = SEMANTIC_BINDING_BOUNDARY_PRESERVED
```

The parent result did **not** establish channel-novelty detection under G2, because the frozen detector predicate could not consume the new state-commitment observation without changing evidence semantics.

This specification preserves that negative boundary exactly.

---

## 2. Live semantic stack

The active stack is:

```text
observation
-> semantic binding
-> evidence
-> detector judgment
```

No arrow is automatic.

Hard non-collapse rules:

```text
information preservation != semantic preservation
lossless transformation != semantic preservation
predictive usefulness != semantic preservation
causal correlation != evidence-type identity
correct downstream answer != legitimate evidence path
```

Governing law:

> **Do not translate observations into answers. Translate them only into evidence they actually constitute.**

---

## 3. Frozen target predicate for V0.1

V0.1 is deliberately narrow. It does not attempt a universal semantic-binding calculus.

The frozen target detector predicate is the parent D2 predicate:

```text
P_WRITE = EXACT_J3_ADMISSIBILITY_WRITE_PRESENCE
```

Predicate-relevant evidence language:

```text
E_P_WRITE
```

Predicate-relevant distinction:

```text
WRITE_EVENT_TO_DECLARED_J3_ADMISSIBILITY_TARGET_OBSERVED
vs
NO_SUCH_WRITE_EVENT_OBSERVED_WITHIN_DECLARED_OBSERVATION_SCOPE
```

The target semantic object is an **observed write-event relation**, including the event/provenance semantics required by the frozen predicate.

It is not merely:

```text
J3 admissibility value changed
```

or:

```text
J3 admissibility value differs between two snapshots
```

Therefore:

```text
state-value change != write-event observation
```

remains a hard firewall.

No V0.1 result may generalize automatically from `P_WRITE` to other detector predicates.

---

## 4. Candidate bridge object

For a novel observation channel `C`, let:

```text
O_C = observation language exposed by C
E_P = evidence language consumed by predicate P
```

A candidate semantic bridge is:

```text
beta : O_C -> E_P
```

`beta` is **not** licensed merely because it is computable, lossless, highly predictive, or operationally convenient.

The candidate bridge must be adjudicated before its output may count as predicate evidence.

---

## 5. Frozen predicate-relative semantic criterion

For V0.1, semantic preservation is predicate-relative and scope-indexed.

Let:

```text
Sem_C(o)
```

be the relation directly constituted by source observation `o`, and let:

```text
Sem_E_P(beta(o))
```

be the relation asserted by the target evidence object produced by the bridge.

A bridge may be classified `SEMANTICS_PRESERVING` only when the frozen case evidence establishes:

```text
Sem_C(o) ≡_(P,sigma) Sem_E_P(beta(o))
```

where:

```text
P     = frozen target predicate
sigma = declared semantic/observation scope of the case
```

For V0.1, `≡_(P,sigma)` means:

1. source and target evidence establish the same truth conditions for the predicate-relevant relation within `sigma`;
2. the bridge does not invent an event, actor, target, time, provenance property, observation status, or causal history absent from the source semantics;
3. the bridge does not erase a predicate-relevant distinction present in the source;
4. the bridge does not add predicate-relevant certainty beyond what the source observation constitutes;
5. equivalence is justified independently of downstream detector correctness.

This is a **formal experimental criterion for V0.1**, not a universal theorem of semantic equivalence.

---

## 6. Semantic compatibility is not byte identity

A source observation may use a novel representation while still constituting the same predicate-relevant relation.

Therefore:

```text
different serialization != different semantics
new encoding != new evidence type
```

A semantics-preserving bridge may normalize syntax, field names, ordering, units, or serialization when those changes do not alter the frozen predicate-relevant relation.

The experiment must include a positive control for this possibility.

---

## 7. Frozen semantic-binding statuses

The evaluator may use exactly these four scientific semantic-binding statuses:

### `SEMANTICS_PRESERVING`

The source observation and bridged evidence are established to constitute the same predicate-relevant relation within the declared scope.

This status derives **only semantic admissibility of the bridge for the frozen predicate and scope**.

It does not derive detector correctness, witness sufficiency, entitlement, or composition.

### `SEMANTICS_EXTENSION_REQUIRED`

The source observation constitutes a useful/relevant relation, but that relation is genuinely different from the evidence relation consumed by the frozen predicate.

The correct response is to preserve the new semantic object rather than coerce it into `E_P`.

Canonical motivating form:

```text
state-value change != write-event observation
```

### `UNPROVEN`

The frozen evidence is insufficient to establish predicate-relative semantic equivalence or semantic inequivalence strongly enough for either of the classifications above.

Hard rule:

```text
UNPROVEN != SEMANTICS_EXTENSION_REQUIRED
```

and:

```text
UNPROVEN != INVALID_SEMANTIC_LAUNDERING
```

### `INVALID_SEMANTIC_LAUNDERING`

The proposed bridge manufactures, upgrades, or substitutes predicate-relevant semantics not constituted by the source observation.

Examples include:

```text
state delta -> fabricated observed write event
proxy score -> fabricated event provenance
high-confidence prediction -> fabricated direct observation
answer-target inference -> synthetic evidence chosen to force detector output
```

This status is about the bridge/evidence path, not the downstream detector answer.

---

## 8. Planned minimal adversarial ladder

The following are **case classes only**. No concrete cases are instantiated in this specification.

The next stage must construct frozen cases after this SPEC commit.

### B1 — different encoding, same semantic relation

Target property:

```text
novel representation
same predicate-relevant observed write-event relation
```

Intended scientific role: positive control against trivial refusal.

Prospective expected status class:

```text
SEMANTICS_PRESERVING
```

The concrete case must be constituted later without modifying this specification.

### B2 — different but useful relation

Target property:

```text
source observation is relevant/informative
source relation differs from observed write-event relation
```

Canonical family:

```text
pre/post state-value relation
```

Prospective expected status class:

```text
SEMANTICS_EXTENSION_REQUIRED
```

This case class protects against semantic coercion.

### B3 — highly predictive proxy without relational identity

Target property:

```text
proxy is statistically excellent
proxy does not constitute the target write-event relation
```

The future case construction should make the proxy intentionally strong, including a large frozen calibration family and rare counterexamples where the proxy relation holds without the target evidence relation.

The specification does not freeze a concrete probability, sample size, or counterexample count; those belong to the CASES stage.

Hard rule:

```text
prediction != semantic equivalence
```

A bridge that converts the proxy into direct write-event evidence must not receive `SEMANTICS_PRESERVING` merely because downstream predictions are accurate.

`INVALID_SEMANTIC_LAUNDERING` is available when the concrete bridge explicitly manufactures target evidence semantics.

### B4 — independently established cross-interface equivalence

Target property:

```text
novel representation
independent provenance establishes the same predicate-relevant relation
```

Intended scientific role: positive cross-interface equivalence control.

Prospective expected status class:

```text
SEMANTICS_PRESERVING
```

B4 prevents the trivial policy:

```text
beta = undefined for every novel channel
```

from masquerading as semantic safety.

---

## 9. Anti-shortcut firewall

The experiment must reject all of the following inference shortcuts:

```text
lossless(beta) -> SEMANTICS_PRESERVING
high mutual information -> SEMANTICS_PRESERVING
high predictive accuracy -> SEMANTICS_PRESERVING
causal correlation -> evidence-type identity
source contains more information -> source constitutes target evidence
same downstream answer -> same evidence relation
D2(beta(o)) correct -> beta legitimate
```

The bridge may not be selected, tuned, or repaired using downstream detector correctness.

---

## 10. Detector-execution firewall

Semantic adjudication is upstream of detector execution.

The V0.1 scientific target is:

```text
Is beta semantically admissible for P_WRITE within the frozen scope?
```

not:

```text
Does D2 give the right answer after beta?
```

Therefore detector correctness carries zero authority for semantic-binding classification.

If a later protocol includes downstream D2 replay as a descriptive regression check, that replay must occur only after semantic-binding classification has been frozen and may not alter it.

The preferred V0.1 design is to keep D2 execution outside the semantic adjudication path entirely.

---

## 11. Prospective case-construction constraints

The CASES stage must freeze source observations, scopes, and any calibration/counterexample families before candidate bridge evaluation.

Concrete cases must not contain or expose to a bridge:

```text
semantic_binding_status
expected classification
oracle classification
D2 expected output
transition status
witness status
entitlement status
composition status
```

Case identity, labels (`B1`–`B4`), unique hashes, timestamps, or provenance identifiers may not serve as semantic evidence unless the case itself prospectively declares them predicate-relevant.

`instance identity != semantic equivalence evidence`.

---

## 12. Binding-stage role

After CASES are frozen, the BINDINGS stage may propose candidate `beta` mappings.

A binding proposal must state at minimum:

```text
source observation fields consumed
normalization/transformation performed
target evidence fields emitted
predicate-relevant semantic claim made by emitted evidence
declared scope
provenance basis used by the bridge
```

A bridge may normalize syntax but may not silently expand the semantic claim.

If the bridge requires a genuinely new predicate/evidence type, the binding must preserve that boundary rather than patch `P_WRITE`.

---

## 13. Descriptive semantic oracle

The DESCRIPTIVE_ORACLE stage is descriptive, not adjudicative.

It may record:

```text
what relation the source observation actually constitutes
what relation the proposed target evidence object asserts
what provenance is directly present
what scope is observed
what counterexample relation actually holds in the frozen case
```

It must not contain:

```text
SEMANTICS_PRESERVING
SEMANTICS_EXTENSION_REQUIRED
UNPROVEN
INVALID_SEMANTIC_LAUNDERING
bridge pass/fail
D2 pass/fail
REVOKED
PRESERVED as transition status
UNPROVEN as entitlement status
ENTITLED
W_int
W_comp
composition authorization
```

The evaluator, not the descriptive oracle, compares source semantics to target predicate semantics.

Hard separation:

```text
source semantic fact != bridge classification
```

---

## 14. Protocol and evaluator boundaries

The future protocol must freeze:

```text
run order
visibility constraints
bridge invocation
descriptive-oracle isolation
provenance checks
reproducibility
abstention / UNPROVEN preservation
```

The future evaluator must preserve typed outcomes and may not use a compensatory scalar.

No correct B1/B4 result may cancel an invalid B2/B3 laundering result.

Suggested non-compensatory principle:

```text
INVALID_SEMANTIC_LAUNDERING on any adversarial case blocks a clean compatibility claim.
```

Exact severity annotations, if any, are deferred to CASES/EVALUATOR and are not frozen here.

---

## 15. Success criterion

The strongest positive result available to this V0.1 object is:

```text
SEMANTIC_BINDING_COMPATIBILITY_SUPPORTED_ON_FROZEN_SUITE
```

This claim requires the frozen experiment to distinguish the planned semantic regimes without collapsing:

```text
new encoding
new evidence type
predictive proxy
true semantic equivalence
```

At minimum, the final result must preserve per-case/per-class typed outcomes and show that positive controls are accepted while semantic laundering is rejected.

No generic claim of universal semantic transportability is available.

A bounded secondary formulation, if earned, is:

```text
PREDICATE_RELATIVE_SEMANTIC_TRANSPORT_CAN_BE_CERTIFIED_ON_FROZEN_V0_1_SUITE
```

This is suite-relative and predicate-relative only.

---

## 16. Negative-result value

Clean negative results are admissible and must be preserved.

Examples:

```text
representational compatibility does not generalize across tested channels
predicate-relative equivalence cannot be established from frozen evidence
provenance is insufficient for tested equivalence claims
positive and negative controls cannot be separated by the frozen criterion
```

A failure may motivate later study of additional arguments such as provenance structure, causal linkage, scope-indexed equivalence, or challenge independence.

No such additional argument is predeclared as necessary or sufficient by V0.1 merely because it might become relevant.

---

## 17. Frozen lineage order

The required prospective lineage is:

```text
SPEC
-> CASES
-> BINDINGS
-> DESCRIPTIVE_ORACLE
-> PROTOCOL
-> EVALUATOR
-> RESULT
```

At this commit:

```text
SPEC = FROZEN
CASES = NOT_CONSTITUTED
BINDINGS = NOT_CONSTITUTED
DESCRIPTIVE_ORACLE = NOT_CONSTITUTED
PROTOCOL = NOT_CONSTITUTED
EVALUATOR = NOT_CONSTITUTED
RESULT = NOT_CONSTITUTED
```

The next admissible scientific stage is exactly:

```text
CASES
```

No bridge may help design its own cases.

---

## 18. Hard upstream/downstream authority ceiling

This object may earn semantic-binding compatibility only.

It may not derive:

```text
detector correctness in general
detection completeness
witness sufficiency
interaction-defeater status
PRESERVED transition status
REVOKED transition status
W_int sufficiency
W_comp
composition rule
formal soundness
real-world empirical validity
```

Hard firewall:

```text
SEMANTICS_PRESERVING !=> WITNESS_SUFFICIENT
SEMANTICS_PRESERVING !=> DETECTION_SUPPORTED
correct downstream answer !=> legitimate evidence path
```

The unresolved ladder remains:

```text
semantic binding compatibility
-> ?
-> witness sufficiency
```

The `?` is intentionally not filled by this specification.

---

## 19. Current authority status

```text
OBJECT = SSI_RELICENSE_INTERACTION_SEMANTIC_BINDING_V0.1
STATUS = PROSPECTIVE_SEMANTIC_BINDING_SPEC_FROZEN__SPEC_ONLY

PARENT_HELDOUT_DETECTION_RESULT
    = PARTIAL_TYPED_SUPPORT__FULL_SUITE_NOT_ESTABLISHED

SEMANTIC_BINDING_COMPATIBILITY
    = NEXT_RESEARCH_TARGET__SPEC_FROZEN

SEMANTIC_BINDING_GENERALIZATION
    = OPEN

WITNESS_SUFFICIENCY
    = NOT_OPENED

W_int
    = NOT_ADMITTED_AS_SUFFICIENT_WITNESS

W_comp
    = NOT_DEFINED

COMPOSITION_RULE
    = NOT_ADMITTED

FORMAL_SOUNDNESS
    = UNESTABLISHED

EMPIRICAL_REAL_WORLD_VALIDITY
    = NOT_CLAIMED

SSI_CALC_KERNEL_DELTA
    = 0

JEPA
    = PARKED

BEHAVIORAL_EXPERIMENT_AUTHORITY
    = NONE
```

Governing sentence:

> **Do not translate observations into answers. Translate them only into evidence they actually constitute.**
