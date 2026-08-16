# K1/R2 Cross-Regime Compiler-Transfer Audit

Object: `K1-CROSS-REGIME-COMPILER-TRANSFER/FIRST_AUDIT`

## Frozen upstream lineage

```text
K0_CONFORMANCE_MERGE = be08eb4f9f42373b5bf4c2e18e82cd95036d38bc
R2_SELECTION_MERGE  = 87ae0612d1f6457c7e97fdf54bc35255c495df84
R2_SOURCE_MERGE     = 4f3f488737b8dabc107d66c5f6260bc09087b450
K1_COMPILER_MERGE   = f3337dbd5601d19aac313cb9fe286ed026023703
```

The audit is the first component permitted to read both R2 source gold and the frozen K1 executable IR.

## Prospective strong-pass contract

`K1_R2_CROSS_REGIME_STRONG_PASS` requires:

```text
A_comp = 1
judgment accuracy = 24/24
COMPILATION_OVERREACH = 0
COMPILATION_LOSS = 0
DISTINCTION_LOSS = empty
LINEAGE_MISMATCH = 0
LINEAGE_FABRICATION = 0
LINEAGE_RECOVERY = 1
all six pre-frozen hostile mutations satisfy their expected detections
```

For `MUT-105` and `MUT-106`, the frozen expectation additionally requires judgment accuracy to remain 24/24 while lineage fails. This prospectively retests the K0 result that correct judgments do not imply correct justification lineage.

## Audit dimensions

- `J`: source judgment fidelity.
- `D`: preservation of all eight frozen R2 distinctions.
- `A`: preservation of source justification basis without fabricated compiled justification.
- `L`: recursive source-rule ancestry, premise topology, rule labels, substitutions, congruence operators, and transitivity intermediates.

## Firewall

After first exposure:

```text
DELTA_SELECTION = 0
DELTA_R2_SOURCE = 0
DELTA_K1_COMPILER = 0
DELTA_IR = 0
DELTA_MUTATIONS = 0
DELTA_EXPECTED_MUTATION_DETECTIONS = 0
DELTA_K0 = 0
```

No failure may be repaired on the first-run branch before its exact result is durably preserved.

## Authority ceiling

A strong pass can support only that the K0-derived compilation discipline transferred across this one semantic-axis change, from STLC typing judgments to the frozen Maude rewriting-logic entailment regime.

It does not establish a universal compiler, universal SSI-IR adequacy, AMP validation, pocket-calculator economics, or external niche advantage.
