# SSI Adequacy Governor — H9 Neighborhood Candidate Search V0.1

Status: **prospective local representation search; frozen before first candidate evaluation**.

Base lineage:

```text
PR63 governor = frozen
PR64 hostile result/diagnosis = frozen
PR64 head = ab72cb4e7b352896aa7c0cedbfe217e87c24ac47
H9 = POSITIVE_ADEQUACY_CONSTITUTION_NONIDENTIFIABILITY
```

This artifact does **not** repair PR63. It operationalizes the local search license earned by H9:

```text
coverage-constitution interface
-> candidate distinguishing structures
-> pairwise discrimination audit
```

No candidate receives authority merely by separating the original H9 pair.

## Frozen local question

> What is the smallest additional independently constitutable distinction that separates coverage claims entitled to support positive adequacy from claims that are merely asserted, while avoiding unnecessary distinctions where adequacy consequence does not change?

H9 supplies the local collision:

```text
W_independent != W_self_asserted

Phi_calc(W_independent)
    =
Phi_calc(W_self_asserted)

Y_adequacy(W_independent)
    !=
Y_adequacy(W_self_asserted)
```

The search region is only:

```text
POSITIVE_ADEQUACY / COVERAGE_CONSTITUTION
```

It does not reopen the whole governor, SSI, Level 3, or SSI-CALC.

## Frozen candidate family

Exactly five one-bit candidate factorizations are admitted in V0.1:

```text
C1_INDEPENDENT_PROVENANCE
    = world.independent_provenance

C2_TRUSTED_INPUT_BOUNDARY
    = world.trusted_input_boundary

C3_CHECKABLE_COVERAGE_WITNESS
    = world.checkable_coverage_witness

C4_INDEPENDENT_SELECTOR_DOMAIN
    = world.independently_constituted_selector_domain

C5_CLAIM_SOURCE_STANDING
    = world.claim_source_has_standing
```

These names are candidate descriptions, not claims of sufficiency.

No conjunction, disjunction, weighting, inferred latent variable, learned classifier, or post-hoc feature may be added after seeing V0.1 results.

## Frozen external consequence

Each world in `WORLDS.json` carries an externally frozen:

```text
Y_adequacy
    = SUPPORTABLE
    | NOT_ESTABLISHED
```

`Y_adequacy` is the discriminator. Candidate signatures do not generate or modify it.

The world family intentionally contains nearby cases where one attractive candidate feature is present but adequacy standing is still not established, plus more than one positively constituted pattern. This prevents H9-only overfitting.

## Pairwise criterion

For every unordered world pair `(a,b)`:

```text
if Y_adequacy(a) != Y_adequacy(b):
    candidate must distinguish a and b

if Y_adequacy(a) == Y_adequacy(b):
    candidate distinction is counted as gratuitous
```

For candidate `C_i`:

```text
missed_consequential
    = count(
        Delta Y_adequacy != 0
        and
        Delta phi_Ci == 0
      )

gratuitous_distinctions
    = count(
        Delta Y_adequacy == 0
        and
        Delta phi_Ci != 0
      )
```

The ideal local factorization is:

```text
missed_consequential = 0
gratuitous_distinctions = 0
```

If no candidate satisfies both, V0.1 returns:

```text
NO_EXACT_CANDIDATE
```

and does **not** synthesize a replacement.

If multiple candidates satisfy both, V0.1 returns:

```text
AMBIGUOUS_EXACT_CANDIDATES
```

and does **not** choose among them.

If exactly one satisfies both, V0.1 may report:

```text
UNIQUE_EXACT_CANDIDATE
```

but this still means only:

```text
candidate survives frozen local discrimination suite
```

not:

```text
validated repair
```

## H9 anchor

The search also records whether each candidate separates:

```text
W0_SELF_ASSERTED
vs
W1_INDEPENDENTLY_CONSTITUTED
```

A candidate that does not separate this anchor cannot repair H9.

But:

```text
separates H9
!=
survives neighborhood
```

## Firewalls

```text
H9_COLLISION
    -> LOCAL_CANDIDATE_SEARCH

LOCAL_CANDIDATE_SEARCH
    != REPAIR

CANDIDATE_SURVIVES
    != VALIDATED_REPAIR

VALIDATED_REPAIR
    != AUTHORITY

NO_EXACT_CANDIDATE
    != PERMISSION_TO_ADD_COMPOSITES_AUTOMATICALLY

PR63
    = UNCHANGED

PR64
    = UNCHANGED

NEW_SSI_COORDINATE
    = NO

LEVEL_3_INTERFACE_INVENTION
    = NOT_OPENED

SSI_CALC_KERNEL_DELTA
    = 0
```

## First-result firewall

Before execution:

```text
SPEC = FROZEN
WORLDS = FROZEN
CANDIDATES = FROZEN
FIRST_RESULT = NOT_EXECUTED
REPAIR = PROHIBITED
```

After execution, preserve the complete ledger before changing the candidate family or world set.
