# SSI Relicense Interaction Detection Stress V0.1 — Evaluator

Status: `PROSPECTIVE_EVALUATOR_FROZEN__NO_EXECUTION_NO_RESULT`

This evaluator defines **how immutable execution records are graded** against the already-frozen stress constitution. It does not execute detectors, repair upstream objects, add detector semantics, adjudicate entitlement, or collapse typed outcomes into one scalar.

Frozen lineage:

```text
SPEC                       a35b68779994026427dcc759ddc1188b8e604406
HELDOUT_CASES              714cd34fbbf260b25fa2bdf8c25009443b531899
DETECTOR_CHANNEL_BINDINGS  44a92a88d61b87f43a719662ac463862357fccdf
DESCRIPTIVE_ORACLE         c7c1cc88992a3a2dc1f095a250cf163318c9087f
EXECUTION_PROTOCOL         4aaad63e07244bce613371e81e0337794bd3c1a0
PARENT_D0_D1_D2_D3         f0a048b8802e85001012121a384495751aa378e9
```

After this evaluator is frozen, the next permitted stage is:

```text
FIRST_EXECUTION_AND_RESULT
```

No execution has occurred when this evaluator is frozen.

---

## 1. Hard immutability and admissibility gate

Before grading any execution record, verify the execution protocol preflight succeeded against the exact frozen lineage above.

Required:

```text
DELTA_SPEC      = 0
DELTA_CASES     = 0
DELTA_BINDINGS  = 0
DELTA_ORACLE    = 0
DELTA_D0_D1_D2_D3_ALGORITHMS = 0
```

If any required preflight condition failed, or any execution record has `preflight_status != PASS`:

```text
SCIENTIFIC_ADJUDICATION = ABORTED
DIAGNOSIS = EXECUTION_PROVENANCE_DEFECT
```

This is not detector evidence.

The evaluator may not repair, reinterpret, migrate, or normalize an upstream object to make grading possible.

---

## 2. Allowed evaluator inputs

The evaluator may consume only:

```text
1. immutable execution records produced under EXECUTION_PROTOCOL.md
2. DESCRIPTIVE_ORACLE.json
3. typed severity weights frozen in HELDOUT_CASES.json
4. binding statuses frozen in DETECTOR_CHANNEL_BINDINGS.json
5. diagnostic vocabulary frozen in SPEC.md
```

The evaluator may use case identifiers only to join execution records to the frozen oracle and binding records.

The evaluator may not expose oracle fields back to the detector or rerun a detector after inspecting oracle facts.

Hard separation:

```text
descriptive ground truth != detector-visible evidence != detector judgment
binding compatibility      != detector correctness
detected                   != reconciled             != authoritative
```

---

## 3. No compensatory scalar

The evaluator produces a typed outcome vector.

Forbidden:

```text
single accuracy score that erases error type
weighted-sum rescue
averaging an unbound axis into successful axes
letting correct easy cases cancel fabricated resolution
letting correct conflict handling cancel false confident detection elsewhere
```

Binding rule:

```text
NO_COMPENSATORY_SCALAR
```

The frozen severity weights may be attached to their matching typed errors for prioritization and reporting, but may not be summed into a suite score.

Frozen typed severities:

```text
FALSE_POSITIVE_CONFIDENT_DETECTION                   = 5
FALSE_NEGATIVE_CONFIDENT_DETECTION                   = 4
FABRICATED_ABSENCE_FROM_PARTIAL_OR_MISSING_COVERAGE = 6
FABRICATED_RESOLUTION_UNDER_CHANNEL_CONFLICT         = 6
CORRECT_UNKNOWN                                      = 0
CORRECT_COVERAGE_LIMIT                               = 0
CORRECT_DETECTION_CONFLICT                           = 0
```

---

## 4. Evaluation order

Grade in this fixed order:

```text
E0 provenance and execution determinism
E1 local-control integrity (D0/D1)
E2 representation gate
E3 coverage handling
E4 binding compatibility
E5 bound D2 descriptive correctness
E6 independent-channel conflict preservation
E7 per-axis diagnostic classification
E8 bounded suite-level claim ceiling
```

Later stages may not overwrite a shallower failure.

---

## 5. E0 — provenance and execution determinism

If the execution protocol reports non-reproducible records under identical frozen inputs:

```text
SCIENTIFIC_ADJUDICATION = ABORTED
DIAGNOSIS = EXECUTION_PROTOCOL_OR_IMPLEMENTATION_DEFECT
```

Do not classify the discrepancy as detector blindness, channel fragility, or detection evidence.

---

## 6. E1 — D0/D1 local-control integrity

The held-out suite freezes one canonical local quotient and one canonical deterministic local closure for all 11 worlds.

Therefore, under deterministic execution:

```text
D0_output must be byte-identical across all 11 worlds
D1_output must be byte-identical across all 11 worlds
```

If a D0/D1 difference is traceable to forbidden case/oracle/axis information entering detector visibility:

```text
DIAGNOSIS = PAIR_LEAKAGE
```

If the visibility envelope is correct but identical frozen inputs produce divergent D0/D1 outputs:

```text
SCIENTIFIC_ADJUDICATION = ABORTED
DIAGNOSIS = EXECUTION_PROTOCOL_OR_IMPLEMENTATION_DEFECT
```

A local-control separation is never counted as higher-order detector success.

---

## 7. E2 — representation gate

Before assigning a detection failure, determine whether the frozen `Phi_int` vocabulary can encode the held-out distinction.

Frozen representation mappings for this suite:

```text
G1 TEMPORAL_AGGREGATE_WINDOW      -> EMERGENT_CONSTRAINT
G2 CROSS_BOUNDARY_EFFECT          -> CROSS_BOUNDARY_EFFECT
G3 CROSS_BOUNDARY_EFFECT          -> CROSS_BOUNDARY_EFFECT
G4 ROLLBACK_PATH_INTERFERENCE     -> EMERGENT_CONSTRAINT
G5 physical alias relation/report -> SHARED_STATE_ALIAS
```

These mappings are grading projections into the already-frozen interaction relation types. They do not add a new relation type or detector predicate.

If a future execution record or oracle fact requires a distinction outside these frozen mappings:

```text
DIAGNOSIS = REPRESENTATION_FAILURE
```

and do not escalate that case to detector blindness.

For the currently frozen 11 worlds, the intended descriptive distinctions are representable under the mappings above.

Representability still does not imply bindability, detectability, correctness, or sufficiency.

---

## 8. E3 — coverage handling

Coverage is graded before semantic detector correctness.

### COMPLETE

`COMPLETE` permits semantic grading only when the frozen binding is semantics-preserving.

### PARTIAL_PRE_ONLY

Required terminal execution behavior:

```text
D2_invoked = false
harness_state = COVERAGE_LIMIT
```

If satisfied:

```text
typed_outcome = CORRECT_COVERAGE_LIMIT
severity = 0
```

If the execution coerces partial coverage into `INTERACTION_ABSENT`:

```text
typed_error = FABRICATED_ABSENCE_FROM_PARTIAL_OR_MISSING_COVERAGE
severity = 6
```

If D2 is otherwise invoked or a binary interaction state is fabricated under inadequate coverage, classify first as:

```text
DIAGNOSIS = COVERAGE_LIMIT
PROTOCOL_CONFORMANCE = FAIL
```

Do not grant scientific credit merely because a fabricated binary answer happens to match latent oracle truth.

### UNOBSERVED

Required terminal execution behavior:

```text
D2_invoked = false
harness_state = COVERAGE_LIMIT
```

If satisfied:

```text
typed_outcome = CORRECT_COVERAGE_LIMIT
severity = 0
```

`UNOBSERVED` must never be graded as evidence for `INTERACTION_ABSENT`.

### UNKNOWN

If a frozen case carries `UNKNOWN`, preservation of `UNKNOWN` is correct and receives:

```text
typed_outcome = CORRECT_UNKNOWN
severity = 0
```

`UNKNOWN != OBSERVED_ABSENT` remains binding.

---

## 9. E4 — binding compatibility

Binding compatibility is evaluated independently of detector correctness.

### G1

Frozen binding:

```text
BOUND_SEMANTICS_PRESERVING
```

Proceed to bound D2 grading.

### G2

Frozen binding:

```text
UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
```

Required execution behavior for both G2 worlds:

```text
D2_invoked = false
execution_state = UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
```

If preserved, record:

```text
BINDING_COMPATIBILITY = UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
DETECTION_CORRECTNESS = NOT_SCORED
```

This is not `DETECTION_BLINDNESS`, not a false negative, and not `CHANNEL_FRAGILITY` by itself.

It establishes only that the frozen D2 semantics do not accept the new state-commitment observation without semantic extension.

The evaluator must not convert:

```text
state_value_relation = CHANGED
```

into a synthetic D2 write event.

### G3

For `HD-G3-A-COMPLETE`:

```text
BINDING_COMPATIBILITY = UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
DETECTION_CORRECTNESS = NOT_SCORED
```

For partial and unobserved members, grade the coverage gate under E3; do not score semantic D2 correctness.

### G4

Frozen binding:

```text
BOUND_SEMANTICS_PRESERVING
```

Proceed to bound D2 grading.

### G5

Both observer channels are individually bound through alias-equality semantics.

Proceed to per-channel descriptive preservation and conflict grading. Do not score either observer against an unconstituted physical truth.

---

## 10. E5 — bound D2 descriptive correctness for G1/G4

For the semantics-preserving composed-resource adapter, the frozen D2 predicate is:

```text
available_resource < required_resource
    -> INTERACTION_PRESENT / COMPOSED_PRECONDITION_VIOLATION

available_resource >= required_resource
    -> INTERACTION_ABSENT / COMPOSED_PRECONDITION_SATISFIED
```

### Oracle-to-D2 grading projection

For G1:

```text
capacity_relation = AVAILABLE_LT_REQUIRED
    -> expected D2_state = INTERACTION_PRESENT
    -> expected D2_fact  = COMPOSED_PRECONDITION_VIOLATION

capacity_relation = AVAILABLE_GE_REQUIRED
    -> expected D2_state = INTERACTION_ABSENT
    -> expected D2_fact  = COMPOSED_PRECONDITION_SATISFIED
```

For G4:

```text
recovery_capacity_relation = AVAILABLE_LT_REQUIRED
    -> expected D2_state = INTERACTION_PRESENT
    -> expected D2_fact  = COMPOSED_PRECONDITION_VIOLATION

recovery_capacity_relation = AVAILABLE_GE_REQUIRED
    -> expected D2_state = INTERACTION_ABSENT
    -> expected D2_fact  = COMPOSED_PRECONDITION_SATISFIED
```

This projection grades whether the unchanged D2 predicate correctly processes the frozen semantics-preserving adapter. It does not claim that the interaction is a defeater or that any transition status follows.

### Correct binary detection

If state and fact both match:

```text
DIAGNOSIS = DETECTION_SUPPORTED
```

### False confident positive

If oracle relation is `AVAILABLE_GE_REQUIRED` but D2 emits `INTERACTION_PRESENT`:

```text
typed_error = FALSE_POSITIVE_CONFIDENT_DETECTION
severity = 5
DIAGNOSIS = DETECTION_BLINDNESS
```

### False confident negative

If oracle relation is `AVAILABLE_LT_REQUIRED` but D2 emits `INTERACTION_ABSENT`:

```text
typed_error = FALSE_NEGATIVE_CONFIDENT_DETECTION
severity = 4
DIAGNOSIS = DETECTION_BLINDNESS
```

### Unexpected abstention or malformed output under complete bound evidence

If the case is complete, representable, semantics-preservingly bound, and D2 fails to produce a valid state/fact pair:

```text
DIAGNOSIS = DETECTION_BLINDNESS
```

Do not coerce the malformed/abstaining output into a binary result for scoring convenience.

---

## 11. E6 — G5 independent-channel conflict grading

The G5 oracle constitutes **observer reports**, not underlying physical alias truth.

For each observer separately, grade only whether unchanged alias-equality D2 semantics preserve that observer's frozen report:

```text
reported_relation = ALIASED
    -> expected channel D2_state = INTERACTION_PRESENT
    -> expected channel D2_fact  = ALIASED_WITH_AUTHORITY_SENSITIVE_COLLISION

reported_relation = DISJOINT
    -> expected channel D2_state = INTERACTION_ABSENT
    -> expected channel D2_fact  = DISJOINT
```

This is observation-translation grading, not physical-truth adjudication.

The G5 scientific target is the harness response to incompatible same-scope channel states.

If both channel outputs preserve their respective reports and the states are incompatible, required harness behavior is:

```text
harness_state = DETECTION_CONFLICT
observer_priority = NONE
reconciliation = NOT_PERFORMED
```

If preserved:

```text
typed_outcome = CORRECT_DETECTION_CONFLICT
severity = 0
DIAGNOSIS = DETECTION_CONFLICT
```

If the harness selects one observer, synthesizes a reconciled relation, or converts disagreement into a binary resolved state:

```text
typed_error = FABRICATED_RESOLUTION_UNDER_CHANNEL_CONFLICT
severity = 6
DIAGNOSIS = DETECTION_CONFLICT
PROTOCOL_CONFORMANCE = FAIL
```

Never grade:

```text
which observer was physically correct
whether alias truth was present or absent
whether the conflict should revoke or preserve anything
```

because the frozen oracle intentionally does not constitute that truth.

Hard firewall:

```text
DETECTION_CONFLICT != REVOKED
DETECTION_CONFLICT != PRESERVED
DETECTION_CONFLICT != UNPROVEN
DETECTION_CONFLICT != ENTITLED
```

---

## 12. E7 — per-axis outcome vector

The evaluator must emit independent axis outcomes.

Required output shape:

```text
G1_WORLD_NOVELTY = <typed per-case results + axis diagnosis>
G2_CHANNEL_NOVELTY = <binding compatibility result; detection correctness NOT_SCORED if unbound>
G3_COVERAGE_DEGRADATION = <complete-case binding result + partial/missing coverage results>
G4_FAILURE_STRUCTURE_NOVELTY = <typed per-case results + axis diagnosis>
G5_INDEPENDENT_CHANNEL_CONTRADICTION = <per-channel preservation + conflict-handling result>
```

Axis aggregation rules:

### G1

`DETECTION_SUPPORTED` at axis level only if both G1 worlds are correctly detected and all shallower gates pass.

### G2

If both worlds preserve the frozen unbound status:

```text
AXIS_RESULT = SEMANTIC_BINDING_BOUNDARY_PRESERVED
DETECTION_GENERALIZATION_ON_G2 = NOT_EVALUABLE_UNDER_FROZEN_D2
```

Do not relabel this as detector failure.

### G3

Report the COMPLETE semantic binding boundary separately from partial/unobserved coverage handling.

No scalar G3 pass may hide the distinction:

```text
coverage semantics may generalize
while
interaction semantics remain unbound
```

### G4

`DETECTION_SUPPORTED` at axis level only if both G4 worlds are correctly detected and all shallower gates pass.

### G5

The axis succeeds only at the conflict-handling target if both channel reports are faithfully preserved and the harness retains `DETECTION_CONFLICT` without reconciliation.

The axis does not and cannot succeed at physical truth adjudication in V0.1.

---

## 13. E8 — suite-level claim ceiling

The evaluator must not issue a generic `PASS`.

It must report the typed vector first.

The maximal predeclared positive robustness claim is:

```text
INDEPENDENT_HIGHER_ORDER_DETECTION_ROBUSTNESS_SUPPORTED_ON_FROZEN_HELDOUT_SUITE
```

That claim is available only if:

```text
all required axes are representable
all required axes are semantics-preservingly bound for their detection target
all complete bound detection cases are correct
coverage-limit cases preserve uncertainty
conflicting channels preserve DETECTION_CONFLICT
no PAIR_LEAKAGE
no execution/provenance defect
no typed scientific error
```

A required axis with:

```text
UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
```

blocks the full robustness claim. Successes on other axes may not compensate.

Therefore, under the already-frozen V0.1 bindings, the full five-axis robustness claim is **not prospectively earnable without changing the experiment**, because G2 and the COMPLETE G3 semantic channel are unbound. The evaluator must preserve that boundary rather than reinterpret it after execution.

Possible bounded suite interpretation if execution conforms is instead a vector such as:

```text
G1 world-novelty detection       = SUPPORTED or NOT_SUPPORTED
G2 channel-novelty detection     = NOT_EVALUABLE_UNDER_FROZEN_D2__SEMANTIC_BINDING_BOUNDARY
G3 coverage handling             = SUPPORTED or NOT_SUPPORTED
G3 complete semantic detection   = NOT_EVALUABLE_UNDER_FROZEN_D2__SEMANTIC_BINDING_BOUNDARY
G4 failure-novelty detection     = SUPPORTED or NOT_SUPPORTED
G5 contradiction handling        = SUPPORTED_AS_CONFLICT_PRESERVATION or NOT_SUPPORTED
```

The exact populated vector is a RESULT-stage output and is not filled in now.

---

## 14. Diagnostic localization precedence

When multiple symptoms appear, preserve the shallowest supported diagnosis:

```text
1. EXECUTION_PROVENANCE_DEFECT / EXECUTION_PROTOCOL_OR_IMPLEMENTATION_DEFECT
2. PAIR_LEAKAGE
3. REPRESENTATION_FAILURE
4. UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS  # binding status, not detector failure
5. COVERAGE_LIMIT
6. DETECTION_BLINDNESS
7. DETECTION_CONFLICT
8. DETECTION_SUPPORTED
```

`CHANNEL_FRAGILITY` may be used only if a semantics-preserving alternative channel binding exists and detection then fails relative to the same represented relation. Mere inability to bind G2 under frozen D2 is not sufficient to assign `CHANNEL_FRAGILITY`.

`CHALLENGE_DEPENDENCE` may be used only if apparent discrimination is shown reducible to the frozen local quotient or deterministic local closure.

---

## 15. Required evaluator output schema

The first result must contain at least:

```text
provenance_status
execution_reproducibility_status
D0_control_status
D1_control_status
per_world_results[11]
per_axis_results[G1..G5]
typed_error_counts_by_class
typed_outcome_counts_by_class
severity_annotations_by_error_class
binding_boundaries
coverage_preservation_status
conflict_preservation_status
full_robustness_claim_available   # boolean
authority_ceiling
```

`typed_error_counts_by_class` and `severity_annotations_by_error_class` are reported separately.

No severity-weighted total is permitted.

---

## 16. Forbidden evaluator outputs

The evaluator must not emit or infer:

```text
REVOKED
PRESERVED as a higher-order transition judgment
UNPROVEN as an entitlement-layer status
ENTITLED
W_int sufficiency
W_comp
composition authorization
formal soundness
real-world empirical validity
causal independence in general
```

It must not convert:

```text
INTERACTION_PRESENT -> defeater
INTERACTION_ABSENT  -> preservation
DETECTION_CONFLICT  -> transition status
```

---

## 17. Authority ceiling

```text
OBJECT = SSI_RELICENSE_INTERACTION_DETECTION_STRESS_V0.1/EVALUATOR
STATUS = PROSPECTIVE_EVALUATOR_FROZEN__NO_EXECUTION_NO_RESULT

SPEC = FROZEN
HELDOUT_CASES = FROZEN
DETECTOR_CHANNEL_BINDINGS = FROZEN
DESCRIPTIVE_ORACLE = FROZEN
EXECUTION_PROTOCOL = FROZEN
EVALUATOR = FROZEN

EXECUTION = NOT_STARTED
RESULT = NOT_CONSTITUTED

DETECTION_GENERALIZATION = OPEN
DETECTION_LOCALIZATION = OPEN
CONTRADICTORY_CHANNEL_HANDLING = OPEN

WITNESS_SUFFICIENCY = NOT_OPENED
W_int = NOT_ADMITTED_AS_SUFFICIENT_WITNESS
W_comp = NOT_DEFINED
COMPOSITION_RULE = NOT_ADMITTED
FORMAL_SOUNDNESS = UNESTABLISHED
EMPIRICAL_REAL_WORLD_DETECTION = NOT_CLAIMED
SSI_CALC_KERNEL_DELTA = 0
JEPA = PARKED
BEHAVIORAL_EXPERIMENT_AUTHORITY = NONE
```

Hard firewalls:

```text
UNBOUND != FAILED_DETECTION
CORRECT_UNCERTAINTY != FAILURE
DETECTION_SUPPORTED != WITNESS_SUFFICIENT
DETECTION_CONFLICT != ANY_TRANSITION_STATUS
```

Governing sentence:

> **Grade only what the frozen experiment made adjudicable; preserve everything else as an explicit boundary.**
