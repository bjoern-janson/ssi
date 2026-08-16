# K0 SSI-IR Contract — STLC v0.1

Object: `SSI-IR/K0-STLC-v0.1`

## Purpose

This is the first source-specific compiler target for the external K0 STLC
source contract. It is an experimental SSI-IR fragment. It does **not** modify
SSI-CALC R1..R11 and it does not claim to be a universal SSI intermediate
representation.

The compiler boundary is:

```text
K0 frozen source contract
        |
        v
compiler.py
        |
        v
SSI-IR/K0-STLC-v0.1
```

`IR.json` is the frozen executable semantic contract produced by `compiler.py`.

## Encoded source objects

Source types are translated:

```text
Bool            -> {"kind":"BOOL"}
Arrow(T1,T2)    -> {"kind":"ARROW","domain":...,"codomain":...}
```

Source terms are translated:

```text
Var   -> VAR
Abs   -> ABS
App   -> APP
tru   -> TRUE
fls   -> FALSE
test  -> IF
```

Source contexts become ordered binding lists. Input snapshots sort source
bindings by variable name; abstraction execution appends a new binding and
lookup searches from newest to oldest, preserving shadowing.

## Executable rules

The six source rules have one compiled rule each:

```text
T_Var  -> IR-T-VAR   / LOOKUP
T_Abs  -> IR-T-ABS   / ABS_EXTEND
T_App  -> IR-T-APP   / APP_ARROW
T_Tru  -> IR-T-TRU   / CONST_BOOL
T_Fls  -> IR-T-FLS   / CONST_BOOL
T_Test -> IR-T-TEST  / IF_BOOL_BRANCH_EQ
```

The compiled rule carries its declared source-rule ancestor. That declaration
is not self-authenticating: the independent compiler audit must compare it
against the frozen source derivation lineage.

## Query contract

A compiled query contains:

```text
context
term
expected_type
source_case_id
```

The executor returns either:

```text
JUDGMENT_LICENSED
JUDGMENT_REJECTED
```

plus a machine-readable derivation/rejection certificate.

The executor does not read source gold.

## Justification boundary

A source proof rule is a source-level justification object, not automatically
SSI authority. The K0 experiment freezes an explicit source-rule-to-IR-rule
correspondence and asks whether source justification lineage remains
recoverable after compilation.

A compiled trace node records:

```text
ir_rule
source_rule_ancestor
judgment
premises
evidence
```

The audit, not the compiler, decides whether this lineage is faithful.

## Hard compiler invariants

```text
NO_UNAUTHORIZED_DISTINCTION_PRUNING
NO_COMPENSATORY_AUTHORITY_SCORE
REPRESENTATION_REVISION != EXECUTION_OPTIMIZATION
```

The IR retains explicit targets for all eight distinctions frozen in the
source contract. Merely naming a target does not prove preservation; the
later audit must test the distinctions operationally.

## Hostile mutations

`mutations.json` freezes six deliberately invalid compiler/IR variants before
the independent audit:

1. erase context information;
2. merge distinct types;
3. drop an application premise;
4. replace source-rule ancestry;
5. fabricate a justification edge;
6. collapse branch-type agreement.

These mutations are validation attacks. Their expected failure classes are
frozen before audit execution so the audit cannot define success after seeing
the outcomes.

## Authority ceiling

A deterministic `IR.json` build establishes only a frozen compiler artifact.
It does not establish source/IR judgment fidelity, distinction preservation,
lineage fidelity, compiler generalization, external SSI-CALC validation, or
niche advantage.
