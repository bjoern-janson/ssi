# SSI Relicense Interaction Interface V0.1 — Execution Protocol

Status: `FROZEN_PROTOCOL__IDENTIFIABILITY_ONLY`

This protocol executes only the representational question frozen in `SPEC.md` and `PAIRS.json`.

It does not evaluate witness sufficiency, transition entitlement, or certificate composition.

## 1. Frozen lineage

```text
PARENT_PR53_HEAD = 8753a936ff39efb35d2f37f2ef81efb1ee39e957
SPEC_COMMIT = d52ff9d5885d360cbe86f61eb01bdd951b305b83
PAIRS_COMMIT = 57300a384b4dddee89e3f9fa880954720f93f4a3
```

During execution:

```text
DELTA_SPEC = 0
DELTA_PAIRS = 0
DELTA_PARENT_F4 = 0
DELTA_RELICENSE_CALCULUS = 0
DELTA_SSI_CALC = 0
```

## 2. Baseline interface test

For every pair, compare the canonical local interface:

```text
Phi_local(x) = (W_tr^12, W_tr^23)
```

The three primary adversarial pairs I1-I3 are required by construction to satisfy:

```text
Phi_local(a) = Phi_local(b)
```

while their independently frozen higher-order oracle values differ.

If so, the lower interface is `NON_IDENTIFYING` for that pair by the working diagnostic criterion.

No general theorem is inferred.

## 3. Candidate semantic projection

For each candidate interaction-interface record, compute conceptually:

```text
Psi_int = (
    interaction_scope,
    normalize(interaction_facts),
    observation_coverage
)
```

`normalize(interaction_facts)` retains only the following fields for each fact:

```text
relation_type
participants
activation_condition
observed_relation
affected_scope
provenance_basis
```

Facts are compared as an order-insensitive set.

The following fields are excluded from comparison:

```text
boundary_path identifiers that are identical by construction
local certificate record identifiers that are identical by construction
case_id
pair_id
world_id
record_id
provenance.object_id
challenge_record.object_id
commit SHA
content hash
timestamp
serialization order
higher_order_oracle
expected_interface_status
```

No oracle-derived field may be copied into `Psi_int`.

## 4. Pair result rules

### Primary discriminating pairs I1-I3

Given:

```text
Phi_local(a) = Phi_local(b)
E_123(a) != E_123(b)
```

classify:

```text
Psi_int(a) != Psi_int(b)
    -> PAIR_IDENTIFYING

Psi_int(a) = Psi_int(b)
    -> NON_IDENTIFYING
```

unless the only difference arose from an excluded field, in which case:

```text
SPURIOUSLY_IDENTIFYING
```

### Negative control I4

Given equal higher-order oracle values and semantically identical interaction conditions with deliberately different irrelevant identifiers:

```text
Psi_int(a) = Psi_int(b)
    -> NEGATIVE_CONTROL_PASS

Psi_int(a) != Psi_int(b)
    -> IDENTIFIER_LEAKAGE_FAILURE
```

### Epistemic control I5

The purpose is only to preserve:

```text
UNKNOWN != OBSERVED_POSITIVE_INTERACTION
```

A pass requires:

```text
Psi_int(a) != Psi_int(b)
```

without interpreting `UNKNOWN` as evidence that no interaction exists.

The I5 result does not establish the entitlement status of the unknown case.

## 5. Metrics

Record:

```text
PRIMARY_DISCRIMINATING_PAIRS = 3
PRIMARY_PAIR_IDENTIFICATION_ACCURACY
NEGATIVE_CONTROL_PASS
EPISTEMIC_UNKNOWN_CONTROL_PASS
LOCAL_CERTIFICATE_MUTATIONS
ORACLE_LABEL_LEAKAGE_EVENTS
IDENTIFIER_ONLY_SEPARATIONS
```

Hard validity gates:

```text
LOCAL_CERTIFICATE_MUTATIONS = 0
ORACLE_LABEL_LEAKAGE_EVENTS = 0
IDENTIFIER_ONLY_SEPARATIONS = 0
NEGATIVE_CONTROL_PASS = true
```

If a hard gate fails, no positive identifiability claim is allowed even if the primary pairs are separated.

## 6. Allowed conclusions

If all hard gates pass and all three primary adversarial pairs are separated:

```text
INTERACTION_INTERFACE_V0_1 = PAIR_IDENTIFYING_ON_FROZEN_SUITE
```

and the strongest bounded claim is:

> The candidate interaction representation preserves the prospectively frozen distinctions needed to separate these higher-order interaction cases while the unchanged local transport interface does not.

This does **not** establish:

```text
general higher-order identifiability
detection completeness
truth of interaction facts outside the frozen constitution
witness sufficiency
PRESERVED sufficiency
REVOKED sufficiency
W_int sufficiency
W_comp
composition closure
formal soundness
empirical validity
```

## 7. Failure localization

If a primary pair fails, classify the shallowest applicable reason:

```text
R1 REPRESENTATION_VOCABULARY_COLLAPSE
R2 SEMANTIC_PROJECTION_COLLAPSE
R3 CASE_SPECIFICATION_DEFECT
R4 ORACLE_LEAKAGE_OR_IDENTIFIER_CHEAT
```

Do not repair the interface in the same execution lineage.

## 8. Authority ceiling

```text
OBJECT = SSI_RELICENSE_INTERACTION_INTERFACE_V0.1
EXECUTION_LEVEL = IDENTIFIABILITY_ONLY
DETECTION = NOT_TESTED
WITNESS_SUFFICIENCY = NOT_TESTED
ENTITLEMENT_RULE = NOT_ADMITTED
W_int = NOT_ADMITTED_AS_SUFFICIENT_WITNESS
W_comp = NOT_DEFINED
COMPOSITION_RULE = NOT_ADMITTED
SSI_CALC_KERNEL_DELTA = 0
JEPA = PARKED
BEHAVIORAL_EXPERIMENT_AUTHORITY = NONE
```
