# K0 STLC Compiler Freeze Report

## Object

`K0-SOURCE-TYPE-SYSTEM-COMPILER/COMPILER`

The compiler is based only on the external source contract frozen and merged at:

```text
SOURCE_FREEZE_MERGE = 722f2a1be4d2a3d2200d4cbc2b3ec7dc94728d79
SOURCE_MANIFEST_SHA256 = 27e5d9675453f36289bee9af8fc020655c9874799905bdac3a2ea700d6207345
```

It produces:

```text
SSI-IR/K0-STLC-v0.1
IR_SHA256 = f551d61884dd26e110e6d2af71a8a911fc5abc812282b974dab0b4b4fe7717d9
COMPILER_MANIFEST_SHA256 = de904002f50199349af1d678eb161237ac61149e03c79c7fe24146a0f0fe03c1
```

## Firewall

Before fidelity-audit exposure:

```text
SOURCE_GOLD_READ = FALSE
TASKS_EXECUTED = FALSE
AUDIT_EXECUTED = FALSE
HOSTILE_MUTATIONS = 6
DELTA_SOURCE = 0
DELTA_R1_R11 = 0
```

The frozen hostile variants target context erasure, type collapse, premise loss, false rule ancestry, fabricated justification, and branch-agreement collapse.

## Pre-audit verification lineage

The first remote compiler-freeze verification failed:

```text
RUN = 31953710779
JOB = 95180996000
MECHANISM = EVALUATOR_COMMENT_BYTE_MISMATCH
```

The repository copy of `ir_evaluator.py` omitted one explanatory comment that was present in the already-frozen compiler manifest. Its executable semantics were unchanged.

The correction restored only the manifested comment:

```text
CORRECTION_COMMIT = 8a579545f956c61ca86efe7d2453b4a25e24a387
DELTA_EXECUTABLE_SEMANTICS = 0
DELTA_IR = 0
DELTA_MUTATIONS = 0
DELTA_SOURCE = 0
```

The second remote check passed:

```text
RUN = 31953766289
JOB = 95181129566
IR_REBUILT_EXACT = TRUE
IR_SHA256 = f551d61884dd26e110e6d2af71a8a911fc5abc812282b974dab0b4b4fe7717d9
SOURCE_GOLD_READ = FALSE
TASKS_EXECUTED = FALSE
DELTA_R1_R11 = 0
```

The failed pre-audit packaging check remains part of compiler lineage.

## Scientific interpretation

This PR freezes a deterministic source-specific compiler and executable IR. It has not yet been compared with source gold. Therefore it does **not** establish judgment fidelity, adequacy, distinction preservation, justification/lineage fidelity, compiler generalization, external SSI-CALC validation, or niche advantage.

The next permitted step is an independent audit branch based on this compiler freeze merge. That branch may read the frozen source gold and execute the frozen IR, but it may not modify the source, compiler, IR, mutation definitions, or expected mutation detection classes.
