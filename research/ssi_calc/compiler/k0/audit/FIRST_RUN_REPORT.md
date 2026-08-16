# K0 Compiler First Fidelity Audit Report

## Frozen lineage

```text
SOURCE_FREEZE_MERGE   = 722f2a1be4d2a3d2200d4cbc2b3ec7dc94728d79
COMPILER_FREEZE_MERGE = 7c419d970eb8235e4352c3f38ac23c8c0c1e6d0f
SOURCE_MANIFEST       = 27e5d9675453f36289bee9af8fc020655c9874799905bdac3a2ea700d6207345
COMPILER_MANIFEST     = de904002f50199349af1d678eb161237ac61149e03c79c7fe24146a0f0fe03c1
IR_SHA256             = f551d61884dd26e110e6d2af71a8a911fc5abc812282b974dab0b4b4fe7717d9
```

The first fidelity audit executed at:

```text
RUN      = 31954003742
JOB      = 95181711422
ARTIFACT = 9265432313
```

The exact JSON result is preserved in deterministic gzip+base64 form. Its raw JSON SHA256 is:

```text
7c942655936a7c0b336051e0d27a005d07e17114b94546e5bbc46abf7220db01
```

## Prospective result

```text
K0_COMPILER_AUDIT_STRONG_PASS
```

### Baseline source-to-IR conformance

```text
A_comp                  = 1.0  (24/24 representable)
source licensed / IR licensed = 12
source rejected / IR rejected = 12
COMPILATION_OVERREACH   = 0
COMPILATION_LOSS        = 0
JUDGMENT_ACCURACY       = 24/24
DISTINCTION_LOSS        = empty
```

All eight predeclared source distinctions were structurally recoverable in the executable IR and preserved the decisions of their frozen witness cases.

### Justification / lineage fidelity

Across the 12 positive source derivations:

```text
SOURCE RULE UNITS            = 37
RULE UNITS RECOVERED         = 37
RULE ANCESTRY ACCURACY       = 1.0
SOURCE EVIDENCE UNITS        = 21
EVIDENCE UNITS RECOVERED     = 21
LINEAGE RECOVERY             = 1.0
TOPOLOGY MISMATCH            = 0
RULE ANCESTRY MISMATCH       = 0
LINEAGE FABRICATION          = 0
```

So the result is stronger than final-judgment agreement in this frozen K0 domain: the source justification topology and the context lookup/extension evidence used by positive judgments were recoverable through the compiled traces.

## Hostile compiler mutations

All six mutations satisfied the detection classes frozen before audit exposure:

```text
MUT-001 ERASE_CONTEXT_INFORMATION
  -> COMPILATION_LOSS
  -> DISTINCTION_LOSS:DIST-001 (plus downstream affected distinctions)

MUT-002 MERGE_DISTINCT_TYPES
  -> COMPILATION_OVERREACH
  -> DISTINCTION_LOSS:DIST-002 (plus downstream affected distinctions)

MUT-003 DROP_APPLICATION_PREMISE
  -> COMPILATION_OVERREACH
  -> DISTINCTION_LOSS:DIST-004

MUT-004 REPLACE_SOURCE_RULE_ANCESTRY
  -> LINEAGE_MISMATCH
  -> final judgment accuracy remained 24/24

MUT-005 FABRICATE_JUSTIFICATION_EDGE
  -> LINEAGE_FABRICATION
  -> final judgment accuracy remained 24/24

MUT-006 COLLAPSE_BRANCH_AGREEMENT_DISTINCTION
  -> COMPILATION_OVERREACH
  -> DISTINCTION_LOSS:DIST-006
```

The two lineage-only attacks are particularly important: the audit rejected compiler variants that retained perfect final judgment accuracy but changed or fabricated the source justification path.

## Scientific interpretation

This result supports:

```text
K0_SOURCE_SPECIFIC_COMPILER_CONFORMANCE = SUPPORTED
```

for the frozen Bool+Arrow STLC source contract and the frozen 24-case task domain.

It does **not** establish:

```text
COMPILER_GENERALIZATION = NO
UNIVERSAL_SSI_IR_ADEQUACY = NO
SSI_CALC_EXTERNAL_NICHE_ADVANTAGE = NO
AMP_VALIDATED = NO
NEW_SSI_CALC_RULE = NO
```

K0 is compiler conformance, not compiler generalization. Because this source regime and task domain participated in compiler/audit construction, they may never later be reused as evidence that the compiler generalizes to an unseen semantic regime.

## Next scientific boundary

The next compiler claim, if pursued, requires a separately chosen external formal regime that was not used to construct K0. K0 becomes a permanent compiler regression/conformance suite.
