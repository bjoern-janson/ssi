# K1 R2 Maude Source Freeze Report

## Frozen source

R2 was selected by the deterministic pool freeze merged at `87ae0612d1f6457c7e97fdf54bc35255c495df84`.

The source is a finite ground fragment of Maude rewriting logic (`E = empty`) using the external deduction rules reflexivity, congruence, replacement, and transitivity.

```text
TERM_UNIVERSE = 45
ENTAILMENT_CLOSURE = 240
CASES = 24
POSITIVE = 12
NEGATIVE = 12
DISTINCTIONS = 8
```

## Remote pre-compiler verification

```text
RUN = 31954850348
JOB = 95183806385
CONCLUSION = PASS
GOLD_RECOMPUTED_EXACT = TRUE
COMPILER_EXECUTED = FALSE
K0_STLC_MODIFIED = FALSE
```

For positive cases, the frozen source checker reproduced the exact root rule and full derivation SHA256. For negative cases it reproduced the exact exhaustive rejection-witness SHA256 over the constituted finite term universe.

## Authority ceiling

This establishes only a reproducible R2 source constitution. It does not establish K1 compiler fidelity, cross-regime architecture transfer, compiler generalization, or external niche advantage.
