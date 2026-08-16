# K0 External STLC Source Freeze Report

## Object

`K0-SOURCE-TYPE-SYSTEM-COMPILER/SOURCE`

The frozen source regime is the Bool + Arrow typing fragment of Software Foundations PLF 5.6 `Stlc`.

## Frozen source surface

```text
CASE_COUNT = 24
POSITIVE = 12
NEGATIVE = 12
DISTINCTIONS = 8
MANIFEST_SHA256 = 27e5d9675453f36289bee9af8fc020655c9874799905bdac3a2ea700d6207345
COMPILER_EXECUTED = FALSE
SSI_CALC_IMPORTED = FALSE
```

The source-only checker exactly recomputes every frozen gold judgment and derivation/rejection witness.

## Pre-exposure verification lineage

The first remote freeze check failed before any compiler existed:

```text
RUN = 31953148603
JOB = 95179629687
MECHANISM = SOURCE_REF_JSON_ESCAPE_REPRESENTATION_MISMATCH
```

The local manifest had been generated from JSON bytes containing the literal escape sequence `\u2014`, while the initial GitHub write had stored the equivalent Unicode em dash character. This changed file bytes but not the parsed source reference object.

The correction changed only the serialized representation of `SOURCE_REF.json` to the already-frozen manifest representation:

```text
CORRECTION_COMMIT = e159aefe9b189a2dc077921b9f1d289da7d74540
DELTA_SOURCE_SEMANTICS = 0
DELTA_TASKS = 0
DELTA_GOLD = 0
DELTA_DISTINCTIONS = 0
```

The second remote verification then passed:

```text
RUN = 31953202429
JOB = 95179760883
GOLD_RECOMPUTED_EXACT = TRUE
CASE_COUNT = 24
POSITIVE = 12
NEGATIVE = 12
DISTINCTIONS = 8
COMPILER_EXECUTED = FALSE
SSI_CALC_IMPORTED = FALSE
```

The failed packaging preflight is retained as lineage rather than erased.

## Scientific interpretation

This freeze establishes only that the source contract is reproducible before compiler construction. It does **not** establish compiler fidelity, compiler adequacy, compiler generalization, SSI-CALC external validation, or niche advantage.

The next permitted step is a separate compiler implementation branch based on the merge commit of this source freeze. The frozen `source/` scientific objects may not be modified by that branch.
