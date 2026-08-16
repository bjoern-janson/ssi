# K1 R2 Source Contract — Finite Rewriting-Logic Fragment

Object: `K1-CROSS-REGIME-COMPILER-TRANSFER/R2_SOURCE`

## External regime

The source semantics is selected from **Maude Manual 4.2.1 — Theories and Deduction**.
The external deduction system defines rewriting-logic entailment using reflexivity,
congruence, replacement, and transitivity.

K1 constitutes a deliberately finite fragment so source truth is mechanically
exhaustible before compiler construction.

## Frozen fragment

- equational theory `E = ∅`;
- constants `a,b,c`;
- unary operators `f,g`;
- ground terms of depth at most 3;
- rules `r_ab: a -> b`, `r_bc: b -> c`, `r_fg: f(x) -> g(x)`;
- judgments are directed entailments `R |- t -> t'`;
- all generated premises and conclusions must remain in the frozen term universe.

For this finite fragment, `source_reference.py` computes the least fixed point
of the four source deduction rules. Negative judgments are therefore exhaustive
relative to the constituted finite domain, not heuristic failures to find a proof.

## Firewall

Frozen before K1 compiler construction:

- external selected source;
- finite source signature;
- rewrite rules;
- 24 query distribution;
- 12/12 source judgments;
- positive derivation trees;
- exhaustive negative reachable-target witnesses;
- eight task-relevant distinctions.

No K0 STLC file may change.

## Authority ceiling

A passing source freeze establishes only reproducible R2 source constitution.
It establishes neither cross-regime compiler transfer nor general compiler validity.
