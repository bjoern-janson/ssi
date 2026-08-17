# SSI Relicense Interaction Detection Stress V0.1 — Execution Protocol

Status: `PROSPECTIVE_EXECUTION_PROTOCOL_FROZEN__NO_EVALUATOR_NO_EXECUTION`

This protocol determines **how the already-frozen stress objects are executed**. It does not reinterpret, repair, extend, or adjudicate them.

Frozen lineage:

```text
SPEC                       a35b68779994026427dcc759ddc1188b8e604406
HELDOUT_CASES              714cd34fbbf260b25fa2bdf8c25009443b531899
DETECTOR_CHANNEL_BINDINGS  44a92a88d61b87f43a719662ac463862357fccdf
DESCRIPTIVE_ORACLE         c7c1cc88992a3a2dc1f095a250cf163318c9087f
```

Parent detector freeze:

```text
D0-D3 detector commit = f0a048b8802e85001012121a384495751aa378e9
```

The next permitted stage after this protocol is:

```text
EVALUATOR
```

Execution does **not** begin when this protocol is frozen.

---

## 1. Hard immutability firewall

Before any future evaluator or execution may run, verify exact upstream lineage.

```text
DELTA_SPEC      = 0
DELTA_CASES     = 0
DELTA_BINDINGS  = 0
DELTA_ORACLE    = 0
DELTA_D0_D1_D2_D3_ALGORITHMS = 0
```

If any required artifact hash/commit differs from the frozen lineage above:

```text
ABORT_EXECUTION = TRUE
```

No runtime reconciliation, migration, normalization repair, or compatibility patch is permitted.

A preflight mismatch is a provenance failure, not a detector result.

---

## 2. Separation of stages

The protocol preserves:

```text
descriptive ground truth != detector-visible evidence != detector judgment
binding compatibility      != detector correctness
detected                   != reconciled             != authoritative
```

The descriptive oracle is **never detector-visible**.

The execution harness may use case identifiers internally for deterministic orchestration and logging, but must strip all prohibited fields before detector invocation.

No detector invocation may receive:

```text
case_id
axis
purpose
freshness_delta
required_equalities
latent_world
independence_basis prose
descriptive_oracle
expected_detector_output
transition_status
witness status
entitlement status
```

---

## 3. Determinism and state reset

All execution is deterministic.

Forbidden runtime dependencies:

```text
random seeds not frozen by this protocol
wall-clock time
network state
external services
adaptive learning
cross-case memory
cross-case cache reuse
post-result parameter updates
```

Each held-out world begins from a fresh detector/harness state.

Each G5 observer invocation also begins from an independent fresh detector state so one observer's output cannot influence the other observer's computation.

Normalization arithmetic is exact over the integer values present in the frozen cases.

Serialization for execution records must use stable key ordering and preserve all typed states exactly.

---

## 4. Fixed run order

The orchestration order is frozen as:

```text
1. HD-G1-A-WINDOW-SEPARATED
2. HD-G1-B-WINDOW-OVERLAP
3. HD-G2-A-COMMITMENT-STABLE
4. HD-G2-B-COMMITMENT-CHANGED
5. HD-G3-A-COMPLETE
6. HD-G3-B-PRE-ONLY
7. HD-G3-C-UNOBSERVED
8. HD-G4-A-ROLLBACK-CAPACITY-TWO
9. HD-G4-B-ROLLBACK-CAPACITY-ONE
10. HD-G5-A-ALPHA-DISJOINT-BETA-ALIASED
11. HD-G5-B-ALPHA-ALIASED-BETA-DISJOINT
```

Run order is an orchestration property only. `case_id` and axis identity are not exposed to D0, D1, or D2.

No output from an earlier world may alter invocation semantics for a later world.

---

## 5. Per-world execution sequence

For each world, execute the following sequence without consulting the descriptive oracle.

### Step 5.1 — construct detector visibility envelope

Read only the raw fields authorized by `DETECTOR_CHANNEL_BINDINGS.json` for that world.

Reject any attempted field outside the binding visibility contract.

### Step 5.2 — run D0 local-quotient control

Expose only the canonical local interface referenced by the case.

Record the D0 output verbatim.

### Step 5.3 — run D1 local-derived control

Expose only the canonical local interface plus canonical deterministic local-derived closure.

Record the D1 output verbatim.

### Step 5.4 — apply coverage gate before semantic detector invocation

Coverage handling is frozen:

```text
COMPLETE:
    continue only if a semantics-preserving binding exists

PARTIAL_PRE_ONLY:
    do not invoke D2 semantic predicate
    emit harness_state = COVERAGE_LIMIT

UNOBSERVED:
    do not invoke D2 semantic predicate
    emit harness_state = COVERAGE_LIMIT

UNKNOWN:
    do not infer absence or presence
    preserve harness_state = UNKNOWN
```

Hard firewall:

```text
PARTIAL_COVERAGE != NEGATIVE_EVIDENCE
UNOBSERVED       != OBSERVED_ABSENT
UNKNOWN          != OBSERVED_ABSENT
```

### Step 5.5 — check binding compatibility

If the frozen binding status is:

```text
UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
```

then:

```text
D2_INVOKED = FALSE
execution_state = UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
```

Do not synthesize a compatible probe.
Do not reinterpret one observation type as another.
Do not patch D2.

In particular:

```text
state-value relation != write-event observation
```

### Step 5.6 — invoke D2 only through frozen semantics-preserving adapter

Where the binding is semantics-preserving, construct only the normalized D2 fields prospectively frozen in `DETECTOR_CHANNEL_BINDINGS.json` and invoke the unchanged D2 algorithm.

Record:

```text
adapter_name
normalized_probe_fields
D2_state
D2_fact
```

Do not compare the D2 output with the descriptive oracle at execution time.

---

## 6. Axis-specific invocation rules

### G1 — world novelty

Use only:

```text
A_COMPOSED_RESOURCE_THRESHOLD
```

with the prospectively frozen temporal-window normalization.

Invoke unchanged D2 `COMPOSED_PRECONDITION_PROBE` semantics.

### G2 — channel novelty

Binding status remains:

```text
UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
```

For both G2 worlds:

```text
D2_INVOKED = FALSE
```

The complete signed state-commitment observation is logged only as an available bound surface that lacks a semantics-preserving D2 adapter.

No state-delta-to-write-trace translation is permitted.

### G3 — coverage degradation

For `HD-G3-A-COMPLETE`:

```text
coverage = COMPLETE
semantic binding = UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
D2_INVOKED = FALSE
execution_state = UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
```

For `HD-G3-B-PRE-ONLY`:

```text
D2_INVOKED = FALSE
harness_state = COVERAGE_LIMIT
```

For `HD-G3-C-UNOBSERVED`:

```text
D2_INVOKED = FALSE
harness_state = COVERAGE_LIMIT
```

The harness may preserve observed pre-state material where available, but it may not convert missing post-state material into interaction absence.

### G4 — failure-structure novelty

Use only:

```text
A_COMPOSED_RESOURCE_THRESHOLD
```

with the prospectively frozen recovery-resource normalization.

Invoke unchanged D2 `COMPOSED_PRECONDITION_PROBE` semantics.

### G5 — independent-channel contradiction

For each G5 world:

1. invoke `observer_alpha` independently through `A_ALIAS_PHYSICAL_PAGE_EQUALITY`;
2. reset detector state;
3. invoke `observer_beta` independently through `A_ALIAS_PHYSICAL_PAGE_EQUALITY`;
4. preserve both detector outputs verbatim;
5. compare only their **descriptive interaction states on the same declared epoch/scope**.

If the channel states are incompatible:

```text
harness_state = DETECTION_CONFLICT
```

The conflict handler must preserve:

```text
alpha_output
beta_output
observer_priority = NONE
reconciliation = NOT_PERFORMED
```

`DETECTION_CONFLICT` is a detection-layer observation-handling state only.

It must not emit or imply:

```text
REVOKED
PRESERVED
UNPROVEN
ENTITLED
W_int
W_comp
composition authorization
```

---

## 7. D3 handling

The original D3 correspondence-destroyed control is not invoked in this stress run.

Reason:

```text
its frozen permutation is specific to the original eight construction worlds
```

No new held-out permutation may be created now.

```text
post-freeze convenience != scientific permission
```

---

## 8. Execution record schema

Each world produces one immutable execution record containing only:

```text
case_id                         # orchestration/logging only; never detector-visible
preflight_status
D0_output
D1_output
coverage_state
binding_status
adapter_used_or_null
normalized_probe_fields_or_null
D2_invoked
D2_state_or_null
D2_fact_or_null
harness_state_or_null
channel_outputs_or_null         # G5 only
execution_errors
```

For G5, `channel_outputs_or_null` preserves separate alpha and beta outputs.

The execution record must not contain an entitlement or transition judgment.

---

## 9. Abstention and unresolved-state preservation

The following are legitimate terminal execution states for a world:

```text
UNBOUND_REQUIRES_NEW_DETECTOR_SEMANTICS
COVERAGE_LIMIT
UNKNOWN
DETECTION_CONFLICT
```

None is automatically an error.

None may be coerced into a binary `INTERACTION_PRESENT` or `INTERACTION_ABSENT` state merely to simplify later scoring.

Governing asymmetry:

```text
PRESERVE_UNCERTAINTY > FABRICATE_RESOLUTION
```

---

## 10. Scoring-input firewall

Execution itself performs **no correctness scoring**.

The later evaluator may receive only these frozen inputs:

```text
1. immutable execution records produced under this protocol
2. DESCRIPTIVE_ORACLE.json
3. typed severity weights already frozen in HELDOUT_CASES.json
4. binding statuses already frozen in DETECTOR_CHANNEL_BINDINGS.json
5. diagnostic vocabulary already frozen in SPEC.md
```

The evaluator may not modify any of those inputs.

The typed severity classes remain non-compensatory:

```text
NO_COMPENSATORY_SCALAR
```

The protocol does not define per-case expected detector outputs; that remains an evaluator-stage operation constrained by the descriptive oracle and frozen diagnostics.

---

## 11. Reproducibility requirements

A conforming re-execution must reproduce the same execution records byte-for-byte after canonical serialization, except for explicitly excluded repository transport metadata.

Required reproducibility checks:

```text
same frozen upstream commits
same fixed run order
same visibility filtering
same adapters
same D0-D2 algorithms
same coverage gate
same G5 conflict handler
no random or external state
```

If two executions differ under the same frozen inputs, classify the discrepancy as:

```text
EXECUTION_PROTOCOL_OR_IMPLEMENTATION_DEFECT
```

not as detector epistemic evidence.

---

## 12. No backward semantic leakage

Execution may reveal that a frozen binding is awkward, incomplete, or unexecutable.

That does not authorize rewriting:

```text
SPEC
HELDOUT_CASES
DETECTOR_CHANNEL_BINDINGS
DESCRIPTIVE_ORACLE
D0-D3
```

First-run defects remain durable.

Any later repair must be a separate versioned object with explicit regression against this first run.

---

## 13. Authority ceiling

```text
OBJECT = SSI_RELICENSE_INTERACTION_DETECTION_STRESS_V0.1/EXECUTION_PROTOCOL
STATUS = PROSPECTIVE_EXECUTION_PROTOCOL_FROZEN__NO_EVALUATOR_NO_EXECUTION

SPEC = FROZEN
HELDOUT_CASES = FROZEN
DETECTOR_CHANNEL_BINDINGS = FROZEN
DESCRIPTIVE_ORACLE = FROZEN
EXECUTION_PROTOCOL = FROZEN

EVALUATOR = NOT_CONSTITUTED
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

Hard firewall:

```text
DETECTION_SUPPORTED !=> WITNESS_SUFFICIENT
DETECTION_CONFLICT  !=> any transition status
```

Governing sentence:

> **Execution may expose what the frozen detector does under the frozen evidence path; it may not rewrite the path to improve the answer.**
