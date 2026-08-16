# K1/R2 Source-Lineage Contradiction Analysis

## Scope

This is an **analysis-only** classification after the first execution-valid K1/R2 audit. No selection, R2 source, source gold, compiler, IR, hostile mutation, expected detection, K0 artifact, or prospective threshold is modified.

The raw execution-valid audit is preserved historically with its prospective label:

```text
K1_R2_CROSS_REGIME_STRONG_PASS
```

but that label does not automatically determine the final scientific claim after contradictory evidence appeared.

## Raw first-valid audit

```text
RUN      = 31955849285
JOB      = 95186264682
ARTIFACT = 9265912712
```

Baseline execution reported:

```text
A_comp = 1.0
JUDGMENT_ACCURACY = 24/24
COMPILATION_OVERREACH = 0
COMPILATION_LOSS = 0
DISTINCTION_LOSS = empty
LINEAGE_MISMATCH = 0
LINEAGE_FABRICATION = 0
LINEAGE_RECOVERY = 1.0
MUTATIONS_CAUGHT = 6/6
```

`MUT-105` and `MUT-106` each retained 24/24 judgment accuracy while producing `LINEAGE_MISMATCH` and `LINEAGE_FABRICATION`, respectively. Thus the audit again operationally separates judgment correctness from justification lineage.

## Contradiction signal

A later automatic run of the already-superseded original audit harness failed **before any IR comparison**:

```text
RUN = 31955831729
JOB = 95186223748
FAILURE = source derivation digest assertion
FIRST WITNESS = CASE-009
```

This cannot be classified as a compiler error because the mismatch occurred while revalidating the frozen source proof witness itself.

## Competing hypotheses

### H1 — compiler lineage failure

Prediction: the source proof witness is stable independently, and mismatch appears only after compilation.

**Rejected.** The mismatch can be reproduced by the unchanged source-only verifier.

### H2 — source judgment relation is non-reproducible

Prediction: changing Python hash seed changes one or more of the 24 source judgment bits.

**Rejected.** Across 16 independent processes with `PYTHONHASHSEED=0..15`, every process reproduced the same 24-bit judgment vector.

### H3 — exact source proof witness is non-canonical

Prediction: the source judgment vector remains fixed while at least one valid derivation tree changes across independent runs.

**Supported.**

## Independent discrimination

### Frozen source verifier across 16 hash seeds

```text
RUN = 31956059458
JOB = 95186763363
ARTIFACT = 9265965033
PASS = 6/16
FAIL = 10/16
```

All ten failures first occurred at `CASE-009` on the frozen derivation SHA.

### Judgment versus proof vectors

```text
RUN = 31956143844
JOB = 95186968282
ARTIFACT = 9265989408
ALL_SEEDS_MATCH_FROZEN_JUDGMENTS = TRUE
UNIQUE_JUDGMENT_VECTORS = 1
UNIQUE_PROOF_VECTORS = 2
```

Only `CASE-009` varies. Its judgment is always licensed and its root rule is always:

```text
TRANSITIVITY
```

but two valid exact proof trees occur:

```text
03ddde13bb07bcbacf38dd191c1e4f4fd07f5c418191a9d12d768990aa4f6ba9
56d686236bb647ccaf20461c31b32ce74681f336831dd35ff37d904c8e8b3bb7
```

The mechanism is unordered proof search in the frozen source reference implementation: multiple valid transitivity derivations exist and set iteration can select different witnesses.

## Shallowest failure locus

```text
SOURCE_CONSTITUTION / PROOF_WITNESS_CANONICALIZATION
```

Classification:

```text
SOURCE_PROOF_CANONICALIZATION_INADEQUATE
```

The source **entailment relation** is constituted and reproducible. The source's selected **exact proof-tree witness** is not canonically constituted.

## Authority update

The contradiction narrows the result rather than erasing it:

```text
J judgment transfer              = SUPPORTED_IN_R2
D-001 .. D-007                   = SUPPORTED_IN_R2
D-008 nested lineage topology    = NOT_IDENTIFIED
A exact justification transfer   = NOT_IDENTIFIED
L exact lineage transfer         = NOT_IDENTIFIED
FULL (J,D,A,L) TRANSFER          = NOT_ESTABLISHED
```

The first seven distinction claims concern stable source judgment/semantic structure. `DIST-008` explicitly concerns nested lineage topology and therefore cannot acquire authority from a source proof representation that admits multiple ungoverned exact witnesses.

## Important surviving result

The hostile controls still reproduce the K0 separation in a different semantic regime:

```text
MUT-105: judgment = 24/24; LINEAGE_MISMATCH
MUT-106: judgment = 24/24; LINEAGE_FABRICATION
```

So:

```text
correct judgment does not imply correct lineage
```

is operationally distinguishable in both STLC typing and Maude rewriting terrain. This does **not** rescue the baseline exact-lineage claim; it only shows the audit dimensions remain non-redundant.

## Strongest warranted claim

```text
K1_R2_CROSS_REGIME_JUDGMENT_TRANSFER_SUPPORTED_SOURCE_LINEAGE_NOT_CANONICALLY_CONSTITUTED
```

This is a partial cross-regime result. It is evidence that the K0-derived discipline transferred at the judgment and non-lineage distinction levels from a typing relation to a rewriting entailment relation. It is not evidence that exact justification/lineage preservation transferred successfully.

## Freshness consequence

R2 is now exposed. It must not be repaired and then reused as fresh evidence for full `(J,D,A,L)` transfer.

A future proof-canonicalization methodology may be developed and regression-tested on R2, but a fresh claim of full lineage transfer requires a new unseen formal regime.

No R3 is started in this lineage.
