# SSI Adequacy Governor

Status: **isolated executable governor artifact; not SSI-CALC and not a post-PR61 formal object**.

This tool operationalizes exactly one transition:

```text
frozen representation
-> adequacy status
-> possible local reopening
```

It does not generate repairs, infer new coordinates, establish novelty, modify the frozen representation, or grant execution authority.

## Scientific state space

The scientific adequacy states are:

```text
SUPPORTED_ADEQUATE_ON_TESTED_SCOPE
UNKNOWN
INADEQUATE
```

`NOT_EVALUABLE` is a protocol/constitution failure and is not part of the adequacy ordering.

The asymmetry is deliberate:

```text
one admissible consequential collision
-> INADEQUATE

positive constituted tested coverage
+ preservation of every required tested consequence distinction
-> SUPPORTED_ADEQUATE_ON_TESTED_SCOPE

otherwise
-> UNKNOWN
```

Therefore:

```text
NO_COLLISION_FOUND != SUPPORTED_ADEQUATE
UNKNOWN != SEARCH_LICENSE
NOT_EVALUABLE != UNKNOWN
```

Only `INADEQUATE` yields:

```text
search_license = LOCAL
```

All other states yield:

```text
search_license = NONE
```

The authority ceiling is always:

```text
ADEQUACY_ONLY
```

## Internal case model

Each external case supplies the scientific tuple:

```text
(phi_F, Y_P, q_Y, sigma, P, pi_Y)
```

where:

- `phi_F` is the case signature under the already frozen representation;
- `Y_P` is an externally constituted consequence for property `P`;
- `q_Y` says whether that consequence is admissible as a discriminator;
- `sigma` is the tested scope;
- `P` is the tested property;
- `pi_Y` records consequence provenance and whether it is independent of the frozen representation.

The calculator never derives `Y_P`.

```text
SSI maps the case.
SSI does not manufacture the discriminator.
```

## Inadequacy witness

`INADEQUATE` is existential. The calculator returns an explicit pair:

```text
case_a
case_b

frozen_signature_a == frozen_signature_b

external_consequence_a != external_consequence_b

consequence_provenance_a
consequence_provenance_b

scope
property

status = INADEQUATE
search_license = LOCAL
ceiling = ADEQUACY_ONLY
```

A reviewer should be able to inspect the exact worlds collapsed by the frozen representation.

## Positive adequacy

Positive adequacy is intentionally not symmetric with inadequacy.

`SUPPORTED_ADEQUATE_ON_TESTED_SCOPE` requires:

1. an explicitly constituted positive coverage claim;
2. the required external consequence classes to be present in the supplied test domain; and
3. every tested pair with different consequences to have different frozen signatures.

This is a bounded tested-scope result only. It is not global adequacy.

## Constitution failures

The conservative v0.1 artifact returns `NOT_EVALUABLE` if, among other things:

- the representation changed after case selection;
- a case was not mapped under the frozen representation;
- an external consequence is missing;
- the consequence is not admissible;
- consequence provenance is missing;
- the consequence is derived from the frozen SSI representation rather than independently constituted;
- a claimed positive coverage set is not actually present.

These failures never produce `INADEQUATE`, `SUPPORTED_ADEQUATE_ON_TESTED_SCOPE`, or search permission.

## Run

From this directory:

```bash
python calculator.py request.json
```

or:

```bash
cat request.json | python calculator.py
```

The output is JSON:

```text
status
witness
scope
property
search_license
ceiling
```

`reason` is included only for `NOT_EVALUABLE`.

## Tests

```bash
python -m unittest -v test_calculator.py
```

The frozen test set includes:

- `SUPPORTED_ADEQUATE_ON_TESTED_SCOPE`;
- `UNKNOWN`;
- `INADEQUATE` with an explicit deterministic witness;
- `NOT_EVALUABLE`;
- missing consequence;
- representation mutation after case selection;
- SSI-derived consequence provenance;
- inadmissible consequence;
- false positive coverage constitution;
- mapping under a non-frozen representation.

## Firewalls

```text
ADEQUACY_GOVERNOR != SSI_CALC
ADEQUACY_GOVERNOR != REPAIR_CALCULUS
COLLISION != REPAIR
SEARCH_LICENSE != REPAIR_AUTHORITY
REPAIR != VALIDATION
VALIDATION != AUTHORITY
UNKNOWN != EXPANSION
NO_FAILURE_OBSERVED != ADEQUACY
```

The artifact must not change the SSI-CALC kernel:

```text
SSI_CALC_KERNEL_DELTA = 0
```
