# SSI ADEQ Governor Hostile V0.1

Status: **SPEC + CASES FROZEN; FIRST RESULT FROZEN**.

This suite is stacked directly on the exact frozen PR #63 head:

```text
00812d117bc083de78408a1f0d78fb54fb806228
```

Frozen calculator Git blob:

```text
ab991327d3b3aac298abda9d612d2a9565263498
```

It does **not** modify the adequacy governor. Its purpose is to try to make the frozen governor wrong before any repair is permitted.

## Attack surface

The suite attacks four failure families:

```text
FALSE_INADEQUACY
MISSED_INADEQUACY
FALSE_ADEQUACY
SCOPE_LEAKAGE
```

The frozen hostile vectors are:

1. `H1_GENUINE_CONSEQUENTIAL_COLLISION`
   - genuine admissible collision
   - expected: `INADEQUATE + LOCAL`

2. `H2_UNPROVEN_CONSEQUENCE_COLLISION_SHAPE`
   - same-signature / different-label shape, but one consequence is inadmissible
   - hostile expected: `UNKNOWN + NONE`
   - deliberate tension: frozen PR63 currently maps any inadmissible consequence to `NOT_EVALUABLE`

3. `H3_MISSING_FROZEN_SIGNATURE`
   - expected: `NOT_EVALUABLE + NONE`

4. `H4_SSI_DERIVED_EXTERNAL_CONSEQUENCE`
   - consequence is not independently constituted
   - expected: `NOT_EVALUABLE + NONE`

5. `H5_REPRESENTATION_CHANGED_AFTER_CASE_SELECTION`
   - freeze violation
   - expected: `NOT_EVALUABLE + NONE`

6. `H6_INSUFFICIENT_POSITIVE_COVERAGE`
   - no collision, no positive coverage constitution
   - expected: `UNKNOWN + NONE`

7. `H7_BOUNDED_POSITIVE_TESTED_COVERAGE`
   - positive tested-scope coverage explicitly asserted and consequence classes present
   - expected: `SUPPORTED_ADEQUATE_ON_TESTED_SCOPE + NONE`

8. `H8_LOCAL_COLLISION_SCOPE_BINDING`
   - genuine collision in a local `(P, sigma)`
   - expected: `INADEQUATE + LOCAL` with unchanged local scope/property

9. `H9_SELF_ASSERTED_COVERAGE_PROVENANCE`
   - consequence provenance is independent, but coverage itself is only self-asserted through `coverage.constituted=true`
   - external oracle marks coverage as *not independently constituted*
   - hostile expected: `UNKNOWN + NONE`
   - deliberate tension: PR63 currently has no coverage-provenance input

10. `H10_NO_COLLISION_NO_COVERAGE_CONTROL`
    - same signature, same consequence, no positive coverage constitution
    - expected: `UNKNOWN + NONE`

## Oracle discipline

The hostile oracle is frozen before the first governor execution.

A mismatch is not automatically a governor defect. It is a first-result diagnostic candidate whose failure locus must be discriminated before repair:

```text
HOSTILE_ORACLE_DEFECT
vs
GOVERNOR_SPECIFICATION_DEFECT
vs
GOVERNOR_IMPLEMENTATION_DEFECT
vs
INTERFACE_EXPRESSIVE_GAP
```

No result permits silent repair.

## First-result firewall

The first result is frozen in:

```text
FIRST_RESULT.json
```

Observed first execution:

```text
TOTAL = 10
PASS = 8
FAIL = 2

H2: expected UNKNOWN; observed NOT_EVALUABLE
H9: expected UNKNOWN; observed SUPPORTED_ADEQUATE_ON_TESTED_SCOPE
```

No repair is permitted by this result.

## Freeze firewall

```text
PR63 = FROZEN
HOSTILE_SPEC = FROZEN
HOSTILE_CASES = FROZEN
FIRST_RESULT = FROZEN
REPAIR = PROHIBITED
SSI_CALC_KERNEL_DELTA = 0
```
