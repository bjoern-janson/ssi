# K0 Compiler Fidelity Audit — Prospective Contract

Object: `K0-SOURCE-TYPE-SYSTEM-COMPILER/FIDELITY_AUDIT`

This audit is constituted only after:

```text
SOURCE_FREEZE_MERGE   = 722f2a1be4d2a3d2200d4cbc2b3ec7dc94728d79
COMPILER_FREEZE_MERGE = 7c419d970eb8235e4352c3f38ac23c8c0c1e6d0f
```

The audit is the first component permitted to read both frozen source gold and
the frozen compiled IR.

## Frozen inputs

```text
SOURCE_MANIFEST_SHA256   = 27e5d9675453f36289bee9af8fc020655c9874799905bdac3a2ea700d6207345
COMPILER_MANIFEST_SHA256 = de904002f50199349af1d678eb161237ac61149e03c79c7fe24146a0f0fe03c1
IR_SHA256                = f551d61884dd26e110e6d2af71a8a911fc5abc812282b974dab0b4b4fe7717d9
CASE_COUNT               = 24
HOSTILE_MUTATIONS        = 6
```

The audit may not modify source, compiler, IR, evaluator, mutation definitions,
or frozen expected mutation detections.

## Baseline measurements

### Representability

```text
A_comp = representable source tasks / 24
```

A source task that cannot be translated is classified at the compiler adequacy
boundary (`F_K_a`), not as an evaluator error.

### Judgment fidelity

For each task:

```text
source licensed + IR licensed   -> preserved positive
source rejected + IR rejected   -> preserved negative
source rejected + IR licensed   -> COMPILATION_OVERREACH
source licensed + IR rejected   -> COMPILATION_LOSS
```

`COMPILATION_OVERREACH` is a hard failure because it manufactures a judgment
not licensed by the frozen source.

### Distinction preservation

All eight source distinctions frozen before compiler construction are checked
both against the executable IR structure and against their frozen witness-case
decisions.

```text
L_comp^Q = {d : d is not recoverable in the executable IR}
```

### Justification / lineage fidelity

For positive source judgments the audit compares:

- source rule ancestry;
- premise topology;
- source context-lookup evidence;
- source context-extension evidence.

Source syntax and IR syntax need not be identical. The criterion is recoverable
justification correspondence.

Any compiled justification with no source ancestor is:

```text
LINEAGE_FABRICATION
```

and is a hard failure.

A wrong declared source ancestor is:

```text
LINEAGE_MISMATCH
```

even when the final judgment is correct.

## Hostile mutation sensitivity

The six hostile mutation definitions and their expected detection classes were
frozen with the compiler before this audit existed.

The audit applies each mutation to a copy of the frozen IR and must observe
**all** expected detections for that mutation.

Mutation outcomes do not alter the source/compiler artifacts.

## Prospective result labels

`K0_COMPILER_AUDIT_STRONG_PASS` requires all of:

```text
A_comp = 1
judgment accuracy = 24/24
COMPILATION_OVERREACH = 0
COMPILATION_LOSS = 0
L_comp^Q = empty
LINEAGE_FABRICATION = 0
LINEAGE_MISMATCH = 0
lineage topology mismatch = 0
lineage recovery = 1
all 6 hostile mutations satisfy their frozen expected detections
```

If baseline conformance is perfect but one or more hostile mutations are not
detected as prospectively required:

```text
K0_COMPILER_CONFORMANCE_PASS_AUDIT_SENSITIVITY_PARTIAL
```

Otherwise:

```text
K0_COMPILER_CONFORMANCE_FAILED
```

## Authority ceiling

Even `K0_COMPILER_AUDIT_STRONG_PASS` can support only source-specific compiler
conformance in this frozen K0 STLC regime.

It cannot establish:

- compiler generalization to an unseen regime;
- universal SSI-IR adequacy;
- SSI-CALC external niche advantage;
- correctness of AMP;
- any new SSI-CALC rule.
