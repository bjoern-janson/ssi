# SSI Adequacy Governor Hostile Suite V0.1

Status: **prospective hostile suite; specification and cases frozen before first governor execution**.

Base governor:

```text
PR = #63
HEAD = 00812d117bc083de78408a1f0d78fb54fb806228
calculator git blob = ab991327d3b3aac298abda9d612d2a9565263498
```

This artifact does **not** modify PR #63. It is stacked from the exact frozen head and exists only to try to make the governor wrong.

## Question

Can the frozen adequacy governor preserve its narrow authority under adversarial external constitution?

The suite attacks four failure families:

```text
FALSE_INADEQUACY
MISSED_INADEQUACY
FALSE_ADEQUACY
SCOPE_LEAKAGE
```

The primary safety emphasis is asymmetric:

> A calculator whose only positive authority is to license reopening should be attacked primarily on whether it knows when it is **not** entitled to license reopening.

## Frozen outputs under test

```text
SUPPORTED_ADEQUATE_ON_TESTED_SCOPE
UNKNOWN
INADEQUATE
NOT_EVALUABLE
```

Only:

```text
INADEQUATE -> search_license = LOCAL
```

No hostile-suite result grants repair authority, validates a new representation, establishes SSI inadequacy outside the implicated property/scope, or changes SSI-CALC.

## Frozen hostile matrix

| Case | Attack | Frozen-suite expectation |
| --- | --- | --- |
| H1 | genuine consequential collision | `INADEQUATE + LOCAL` with exact witness |
| H2 | same signature, asserted consequence difference, one discriminator unproven | `UNKNOWN + NONE` |
| H3 | missing frozen signature | `NOT_EVALUABLE + NONE` |
| H4 | SSI-derived "external" consequence | `NOT_EVALUABLE + NONE` |
| H5 | representation changed after case selection | `NOT_EVALUABLE + NONE` |
| H6 | no collision, positive coverage not constituted | `UNKNOWN + NONE` |
| H7 | bounded positive tested coverage | `SUPPORTED_ADEQUATE_ON_TESTED_SCOPE + NONE` |
| H8 | local consequential collision | `INADEQUATE + LOCAL`, exact `(P, sigma)` preserved |
| H9 | self-asserted positive coverage without independent coverage provenance | `UNKNOWN + NONE` |
| H10 | no collision / no coverage control | `UNKNOWN + NONE` |

## Two deliberate specification attacks

H2 and H9 are not silent repairs of PR #63. They deliberately challenge its frozen protocol boundary.

### H2 — scientific UNKNOWN vs protocol NOT_EVALUABLE

PR #63 currently treats any inadmissible consequence as `NOT_EVALUABLE`.
The hostile oracle asks whether an otherwise legitimate external comparison with an unproven discriminator should instead remain scientifically `UNKNOWN`.

A mismatch is a result, not permission to edit the governor.

### H9 — coverage provenance

PR #63 gives external consequences explicit provenance `pi_Y`, but positive coverage is represented by a bare:

```text
coverage.constituted = true
```

H9 asks whether this permits a caller to manufacture bounded positive adequacy by asserting constitution that the external oracle has not independently established.

Again, a mismatch is a result, not permission to add `pi_coverage`.

## First-result firewall

Before first execution:

```text
PR63 = FROZEN
HOSTILE_SPEC = FROZEN
HOSTILE_CASES = FROZEN
REPAIR = PROHIBITED
```

After first execution, preserve the complete observed ledger before diagnosing:

```text
unexpected result
!= implementation bug
!= specification defect
!= hostile-oracle defect
!= governor-interface defect
```

The shallowest supported failure locus should be chosen only after the first result is frozen.

## Authority ceiling

```text
HOSTILE_SUITE
    != SSI_CALC
    != REPAIR_CALCULUS
    != LEVEL_3_INTERFACE_INVENTION

FIRST_RESULT
    != REPAIR_LICENSE

SSI_CALC_KERNEL_DELTA = 0
```
