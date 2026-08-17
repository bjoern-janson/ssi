# SSI Relicense Interaction Detection Stress V0.1

Status: `PROSPECTIVE_HELDOUT_DETECTION_ATTACK__SPEC_ONLY`

This object is stacked on draft PR #55 and attacks the detector result without modifying it.

Frozen parent head:

```text
PR55_HEAD = c379294a56ba82336e7d335fa343ed40467b4c70
```

The scientific target is entirely inside the detection layer.

```text
representation
-> identifiability
-> independent detection
-> held-out robustness
-> localization
-> ?
```

The `?` remains witness sufficiency and is explicitly NOT OPENED by this object.

No transition status is adjudicated.
No `W_int` sufficiency claim is introduced.
No `W_comp` object is defined.
No composition rule is introduced.
No SSI-CALC, JEPA, or behavioral object is opened.

---

## 1. Frozen parent result

PR #55 established only the bounded result:

```text
INDEPENDENT_HIGHER_ORDER_DETECTION_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
```

with:

```text
D0 = CHALLENGE_DEPENDENCE
D1 = CHALLENGE_DEPENDENCE
D2 = DETECTION_SUPPORTED
D3 = TARGET_WORLD_CORRESPONDENCE_DESTROYED_CONTROL
```

and the hard firewall:

```text
DETECTION_SUPPORTED !=> WITNESS_SUFFICIENT
INTERACTION_PRESENT !=> REVOKED
INTERACTION_ABSENT  !=> PRESERVED
```

This stress object does not strengthen those claims prospectively.

D2 is no longer the object being validated. D2 is the object being attacked.

---

## 2. Research question

> **Does D2's independently constituted discriminating access survive held-out changes to worlds, channels, coverage, failure structure, and channel agreement?**

The benchmark is designed to attack assumptions used to constitute the first positive detector suite.

The target is not binary answer production. Correct preservation of `UNKNOWN`, coverage limitations, and unresolved cross-channel conflict is a valid scientific outcome.

Governing asymmetry:

```text
PRESERVE_UNCERTAINTY > FABRICATE_RESOLUTION
```

---

## 3. Five frozen stress axes

The first held-out suite must attack five distinct assumptions:

```text
G1 = WORLD_NOVELTY
G2 = CHANNEL_NOVELTY
G3 = COVERAGE_DEGRADATION
G4 = FAILURE_STRUCTURE_NOVELTY
G5 = INDEPENDENT_CHANNEL_CONTRADICTION
```

These axes are diagnostic partitions, not entitlement rules.

### G1 — WORLD_NOVELTY

Fresh higher-order configurations must be constructed without reusing the exact interaction worlds that constituted the first D2 suite.

The local quotient remains frozen where the case is intended to test higher-order access:

```text
Phi_local(a) = Phi_local(b)
C_local(a)   = C_local(b)
```

while the held-out interaction state differs.

Target question:

```text
constructed-pair detection success
!=
world generalization
```

### G2 — CHANNEL_NOVELTY

Hold a higher-order interaction relation fixed while changing the independently constituted observation mechanism by which the relation becomes visible.

Target distinction:

```text
interaction detection
!=
probe-format recognition
```

A detector that succeeds only when observations share the constituting channel encoding must be localized as channel-fragile rather than promoted to general detection.

### G3 — COVERAGE_DEGRADATION

Attack detection under incomplete, missing, or one-sided observations.

Hard epistemic firewalls:

```text
UNKNOWN != OBSERVED_ABSENT
UNOBSERVED != OBSERVED_ABSENT
PARTIAL_COVERAGE != NEGATIVE_EVIDENCE
```

A detector must not convert missing coverage into interaction absence.

### G4 — FAILURE_STRUCTURE_NOVELTY

Introduce interaction structures absent from the original detector-construction suite.

Before assigning detector failure, apply the shallowest-failure gate:

```text
Can Phi_int represent the held-out distinction?
```

If NO:

```text
REPRESENTATION_FAILURE
```

If YES but the tested independent channel cannot recover it:

```text
DETECTION_BLINDNESS
```

Do not blame the detector for a distinction that the frozen target interface cannot encode.

### G5 — INDEPENDENT_CHANNEL_CONTRADICTION

Construct at least one held-out state where independently constituted channels provide incompatible descriptive observations.

Example abstract form:

```text
D_A(x) = INTERACTION_PRESENT
D_B(x) = INTERACTION_ABSENT
```

provided both channels satisfy the frozen independence requirements relative to `Phi_local`.

No channel receives automatic authority merely because it is independent or historically accurate.

Hard non-collapse:

```text
detected != reconciled != authoritative
```

Allowed detection-layer outcome:

```text
DETECTION_CONFLICT
```

or an equivalent prospectively frozen unresolved state.

`DETECTION_CONFLICT` is not a transition status and implies neither `REVOKED`, `PRESERVED`, nor any composition judgment.

---

## 4. Quotient-relative independence remains binding

The parent definition of independence remains unchanged.

For the frozen local quotient:

```text
x_a ~_local x_b
iff
Phi_local(x_a) = Phi_local(x_b)
```

any candidate challenge channel reducible to:

```text
D = g o Phi_local
```

or to deterministic permitted local derivatives remains:

```text
CHALLENGE_DEPENDENCE
```

regardless of implementation complexity, architecture, file separation, model class, or feature count.

Architectural separation is not evidence of epistemic independence.

---

## 5. Diagnostic vocabulary

The held-out stress suite may use the following diagnostic labels prospectively:

```text
REPRESENTATION_FAILURE
CHALLENGE_DEPENDENCE
DETECTION_BLINDNESS
CHANNEL_FRAGILITY
COVERAGE_LIMIT
DETECTION_CONFLICT
DETECTION_SUPPORTED
PAIR_LEAKAGE
```

These are experiment-local diagnostic labels in V0.1, not permanent calculus primitives.

Definitions:

### REPRESENTATION_FAILURE

The held-out higher-order distinction cannot be encoded by the frozen `Phi_int` target interface.

### CHALLENGE_DEPENDENCE

Apparent discrimination is functionally reducible to the frozen local quotient or its permitted deterministic closure.

### DETECTION_BLINDNESS

The distinction is representable by `Phi_int`, but the tested independent observation process fails to recover it under adequate coverage.

### CHANNEL_FRAGILITY

Detection succeeds for the constituting probe mechanism but fails under a prospectively legitimate alternative independent observation mechanism for the same higher-order relation.

### COVERAGE_LIMIT

Available observations are insufficient to determine the descriptive interaction state without fabricating resolution.

### DETECTION_CONFLICT

Two or more independently constituted channels yield incompatible descriptive observations and no reconciliation rule has been earned.

### DETECTION_SUPPORTED

The tested detector/channel preserves appropriate held-out discrimination under the prospectively frozen case and controls.

### PAIR_LEAKAGE

A supposedly local-nonidentifiable case becomes separable using forbidden identifiers, oracle-derived fields, or local-derived information that should have been held equal. This is a benchmark/specification defect, not detector success.

---

## 6. Failure localization order

When a held-out case fails, classify the shallowest supported locus:

```text
1. BENCHMARK / PAIR LEAKAGE
2. REPRESENTATION FAILURE
3. CHALLENGE DEPENDENCE
4. DETECTION BLINDNESS / CHANNEL FRAGILITY / COVERAGE LIMIT / DETECTION CONFLICT
5. ONLY LATER: witness-sufficiency questions
```

Do not escalate to witness or entitlement layers from a detection-layer failure.

A contradiction is a signal, not a cause.

---

## 7. Asymmetric error discipline

The experiment must not optimize for forced binary resolution.

False confident resolution is more serious than correctly localized abstention.

At minimum, distinguish:

```text
FALSE_POSITIVE_CONFIDENT_DETECTION
FALSE_NEGATIVE_CONFIDENT_DETECTION
CORRECT_UNKNOWN
CORRECT_COVERAGE_LIMIT
CORRECT_DETECTION_CONFLICT
```

The exact scoring weights must be frozen with the cases before execution.

No scalar score may erase the typed error classes.

---

## 8. Freshness requirements

The held-out suite must not simply replay the four constituting D2 mechanisms in isomorphic worlds under renamed identifiers.

At minimum:

```text
G1 requires fresh world structure
G2 requires a genuinely alternate independent observation mechanism
G3 requires partial or missing coverage not present in the positive construction
G4 requires a held-out interaction/failure form
G5 requires independently constituted conflicting channels
```

Any relaxation of these requirements must be recorded as reduced freshness rather than silently treated as held-out generalization.

---

## 9. Freeze order

The execution lineage must preserve:

```text
SPEC
-> HELDOUT_CASES
-> DETECTOR/CHANNEL_BINDINGS
-> DESCRIPTIVE_ORACLE
-> EXECUTION_PROTOCOL
-> EVALUATOR
-> FIRST_RESULT
```

Rules:

```text
DELTA_SPEC_AFTER_CASE_EXPOSURE = 0
DELTA_CASES_AFTER_EXECUTION_START = 0
DELTA_DETECTOR_AFTER_ORACLE_EXPOSURE = 0
DELTA_ORACLE_AFTER_EXECUTION_START = 0
```

First-run failures must remain durable even if a later repair is attempted.

---

## 10. Success ceiling

Even a perfect held-out result may establish at most a bounded claim such as:

```text
INDEPENDENT_HIGHER_ORDER_DETECTION_ROBUSTNESS_SUPPORTED_ON_FROZEN_HELDOUT_SUITE
```

It must not establish:

```text
universal detector soundness
detection completeness
interaction ontology completeness
causal independence in general
real-world empirical observability
witness sufficiency
PRESERVED sufficiency
REVOKED sufficiency
W_int sufficiency
W_comp
certificate composition
formal soundness
```

The central firewall remains:

```text
DETECTION_SUPPORTED !=> WITNESS_SUFFICIENT
```

---

## 11. Negative-result value

The following are first-class scientific outcomes:

```text
representable but not detectably accessible under held-out channel
constructed detection does not generalize to fresh worlds
detection is channel-fragile
partial coverage forces legitimate UNKNOWN
independent channels conflict without earned reconciliation
```

None is permission to patch the witness or composition layers.

---

## 12. Authority ceiling

```text
OBJECT = SSI_RELICENSE_INTERACTION_DETECTION_STRESS_V0.1
STATUS = PROSPECTIVE_HELDOUT_DETECTION_ATTACK__SPEC_ONLY
PARENT_PR55_RESULT = PRESERVED_UNMODIFIED

REPRESENTATION
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE

IDENTIFIABILITY
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE

INDEPENDENT_DETECTION
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE

DETECTION_GENERALIZATION
    = OPEN

DETECTION_LOCALIZATION
    = OPEN

CONTRADICTORY_CHANNEL_HANDLING
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

EMPIRICAL_REAL_WORLD_DETECTION
    = NOT_CLAIMED

SSI_CALC_KERNEL_DELTA
    = 0

JEPA
    = PARKED

BEHAVIORAL_EXPERIMENT_AUTHORITY
    = NONE
```

Governing sentence:

> **First prove that reality has another route in. Then attack whether that route survives when reality stops cooperating with the assumptions used to build it.**
