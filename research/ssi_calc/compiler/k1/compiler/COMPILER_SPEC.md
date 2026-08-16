# K1 Maude Compiler / SSI-IR Freeze Contract

Object: `K1-CROSS-REGIME-COMPILER-TRANSFER/COMPILER`

This is a new source-specific compiler instance for the R2 Maude rewriting-logic fragment. It does **not** modify or reuse the K0 STLC compiler implementation as a universal translator.

What transfers from K0 is the frozen compilation discipline:

- source constitution precedes compiler construction;
- source and IR are distinct representations;
- the compiler cannot read source gold or task outcomes;
- an independent IR executor is frozen before audit;
- judgment, distinction, justification, and lineage fidelity remain separate obligations;
- hostile compiler mutations and their expected detection classes are frozen before audit;
- overreach and lineage fabrication are hard failures.

## IR

`SSI-IR/K1-MAUDE-RW-v0.1` represents:

- a finite term universe;
- forward-only rewrite direction;
- congruence policy;
- replacement-variable evolution policy;
- translated source rule templates;
- four executable proof opcodes carrying explicit source-rule ancestry.

The executor may produce derivation traces but cannot acquire new authority from them.

## Firewall

Before compiler-audit exposure:

```text
SOURCE_GOLD_READ = FALSE
TASKS_EXECUTED = FALSE
AUDIT_EXECUTED = FALSE
DELTA_K0 = 0
DELTA_R2_SOURCE = 0
```

A compiler-freeze pass establishes only deterministic construction of this source-specific IR. It does not establish cross-regime transfer until the separately frozen audit is executed.
