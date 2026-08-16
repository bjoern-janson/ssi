# K0 Source Contract — Simply Typed Lambda Calculus

Object: `K0-SOURCE-TYPE-SYSTEM-COMPILER/SOURCE`

## External source

The source regime is the Bool + Arrow fragment of the Simply Typed Lambda Calculus
from **Software Foundations, Programming Language Foundations, version 5.6,
chapter `Stlc`**.

Versioned source URL:

`https://softwarefoundations.cis.upenn.edu/plf-5.6/Stlc.html`

The external chapter defines:

- types: `Bool` and `Arrow(T1,T2)`;
- terms: variables, abstractions, applications, `tru`, `fls`, and `test`;
- contexts as partial maps from variables to types;
- typing rules `T_Var`, `T_Abs`, `T_App`, `T_Tru`, `T_Fls`, `T_Test`.

This repository does **not** claim authorship of the source calculus. The files in
this directory are a frozen machine-readable constitution of the selected
external fragment for the K0 compiler experiment.

## Scope

Only typing judgments of the form

`Gamma |- t : T`

are in scope. Operational semantics, substitution, progress, preservation,
subtyping, products, sums, records, recursion, polymorphism, identity,
behavioral equivalence, and SSI-specific authority notions are out of scope.

## Source truth

`source_reference.py` is a syntax-directed executable restatement of the frozen
typing rules. It does not import SSI-CALC or any compiler code.

For each frozen task `q`, `gold/GOLD.json` records:

- the requested source judgment;
- whether the judgment is licensed by the source typing relation;
- a source derivation tree when available;
- or a frozen rejection witness identifying the first source typing obligation
  that cannot be met.

Negative rejection witnesses are **K0 source-constitution artifacts**, not a
claim that Software Foundations itself defines these exact diagnostic codes.

## Firewall

The following are frozen before K0 compiler construction:

- external source/version;
- syntax;
- typing rules;
- task distribution;
- source-derived judgments;
- source derivation/rejection witnesses;
- task-relevant distinction inventory.

The K0 compiler may not modify these objects.

## Authority ceiling

Passing this source freeze establishes only that the K0 source contract is
constituted and reproducible. It says nothing about compiler fidelity,
compiler adequacy, SSI-CALC execution, compiler generalization, or external
niche advantage.
