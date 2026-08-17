# SSI Adequacy Governor Hostile V0.1 — First Diagnosis

Status: **FIRST_DIAGNOSIS_FROZEN__NO_REPAIR_AUTHORITY**

This diagnosis is downstream of the frozen first result in `FIRST_RESULT.json` and does not modify PR #63, the hostile specification, the hostile cases, or SSI-CALC.

## Frozen first result

```text
TOTAL = 10
PASS = 8
FAIL = 2

H2
expected = UNKNOWN
observed = NOT_EVALUABLE
search_license = NONE

H9
expected = UNKNOWN
observed = SUPPORTED_ADEQUATE_ON_TESTED_SCOPE
search_license = NONE
```

All search-license and authority-ceiling firewalls held.

## H2 diagnosis

```text
H2 = CONSERVATIVE_PROTOCOL_BOUNDARY_MISMATCH
```

The frozen governor treats an inadmissible consequence as a constitution failure and returns `NOT_EVALUABLE`. The hostile oracle asked whether the same situation should remain a scientifically meaningful `UNKNOWN`.

The mismatch does not grant search permission or positive adequacy standing.

Therefore the first supported diagnosis is only:

```text
UNKNOWN vs NOT_EVALUABLE boundary remains contestable.
NO AUTHORITY LEAK OBSERVED.
```

No repair is earned.

## H9 diagnosis

H9 is the higher-signal mismatch.

The frozen PR63 prose requires:

```text
positive constituted tested coverage
+ preservation of every required tested consequence distinction
-> SUPPORTED_ADEQUATE_ON_TESTED_SCOPE
```

and says positive adequacy requires an explicitly constituted positive coverage claim.

However, the executable coverage interface contains only:

```text
CoverageClaim(
    constituted: bool,
    required_consequences: tuple
)
```

The calculator checks that required consequence classes are present when `constituted = true`, but it has no representable distinction between:

```text
W_independent:
    coverage.constituted = true
    coverage basis independently constituted

W_self_asserted:
    coverage.constituted = true
    coverage basis merely asserted by the caller
```

At the frozen input interface:

```text
Phi_calc(W_independent) = Phi_calc(W_self_asserted)
```

while the hostile external oracle assigns different epistemic consequences:

```text
Y_adequacy(W_independent) = positive adequacy may be supportable
Y_adequacy(W_self_asserted) = positive adequacy not established
```

H9 instantiated the second world. The frozen governor returned:

```text
SUPPORTED_ADEQUATE_ON_TESTED_SCOPE
```

## Failure locus

The shallowest supported locus is:

```text
INTERFACE / EXPERIMENT-CONSTITUTION REPRESENTATION
```

not yet:

```text
INFERENCE BUG
MECHANISM BUG
NEW SSI ONTOLOGY DEFECT
```

The implementation faithfully consumes the representation it was given. The problem exposed by H9 is that the representation of positive coverage constitution does not encode enough information to discriminate independent constitution from self-assertion.

## Strongest supported claim

```text
POSITIVE_ADEQUACY_CONSTITUTION_NONIDENTIFIABILITY
    = SUPPORTED_IN_H9
```

Bounded statement:

> Under the frozen PR63 interface, independently constituted positive coverage and caller-self-asserted positive coverage can map to the same executable coverage representation. H9 shows that the latter can therefore reach `SUPPORTED_ADEQUATE_ON_TESTED_SCOPE`.

This is a positive-adequacy integrity issue. It is not a search-license leak.

## What H9 does not establish

H9 does **not** establish:

```text
- that `pi_coverage` is the uniquely correct repair;
- that coverage provenance must have the same type as consequence provenance;
- that PR63 should return UNKNOWN rather than NOT_EVALUABLE after a future repair;
- that SSI itself is inadequate;
- that Level 3 should be opened;
- that SSI-CALC should change.
```

`coverage assertion != coverage warrant` is a supported diagnostic compression, not a new SSI coordinate.

## Current authority ceiling

```text
PR63
    = UNCHANGED

PR64_FIRST_RESULT
    = FROZEN__8_OF_10

H2
    = CONSERVATIVE_PROTOCOL_BOUNDARY_MISMATCH
      __NO_AUTHORITY_LEAK

H9
    = POSITIVE_ADEQUACY_CONSTITUTION_NONIDENTIFIABILITY
      __INTERFACE_LEVEL

SEARCH_LICENSE_LEAK
    = 0_IN_10

MISSED_GENUINE_COLLISION
    = 0_IN_TESTED_CASES

SCOPE_LEAK
    = 0_IN_TESTED_CASES

REPAIR
    = NOT_PERMITTED_BY_THIS_DIAGNOSIS

NEW_FORMAL_OBJECT
    = NO

SSI_CALC_KERNEL_DELTA
    = 0
```
