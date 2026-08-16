# SSI-CALC v0.1 — H24 Failure Analysis

Status: `FAILURE_LOCALIZATION_COMPLETE / NO_REPAIR_AUTHORIZED`

This artifact analyzes the 17 exact-certificate mismatches from the first immutable H24 exposure recorded at merge commit `22055cb887006efb4c283d4223ab9f06ae54c66c`.

It does **not** modify the checker, H24, the original 64-case benchmark, the schema, or the R1..R11 kernel.

## 1. Question

For each frozen H24 mismatch, discriminate among:

```text
H1 = IMPLEMENTATION / ORCHESTRATION DEFECT
H2 = REPRESENTATION / SPECIFICATION DEFECT
H3 = MISSING CALCULUS CAPABILITY
```

The classification is made at the shallowest sufficient layer.

A mismatch is `H1` only when:

1. the frozen case already contains the semantic distinction required to decide it;
2. an existing R1..R11 jurisdiction already owns the requested operation; and
3. the smallest sufficient correction changes only matcher/dispatcher/guard/status/orchestration behavior.

A mismatch is `H2` only when the frozen representation or contract cannot express or unambiguously consume the distinction without schema/specification refinement.

A mismatch is `H3` only when the representation is adequate but **no existing rule jurisdiction can express the required derivation/refusal**, thereby earning an R12+ candidate.

## 2. Result

```text
H1 IMPLEMENTATION / ORCHESTRATION = 17
H2 REPRESENTATION / SPECIFICATION = 0
H3 MISSING CALCULUS CAPABILITY     = 0
```

Decision errors decompose as:

```text
OVERREACH       = 6
FALSE_REFUSAL   = 6
DECISION-CORRECT / CERTIFICATE-LOCALIZATION MISS = 5
```

The important interpretation is **not** “the calculus is therefore correct.”

It is narrower:

> **H24 has not yet earned R12.**

Every frozen failure can be repaired counterfactually by changing the reference implementation inside an already-declared R1..R11 jurisdiction, using distinctions already present in the case representation.

## 3. Why this does not vindicate the calculus

`SPEC.md` names rules and intended jurisdictions; it is not yet a theorem-prover-style formal inference system.

Therefore:

```text
H1 = 17
```

means:

> no H24 witness currently forces a new rule **under the existing v0.1 rule partition**.

It does **not** mean:

> R1..R11 are formally complete, uniquely specified, or generally adequate.

There is a real global formalization debt: several implementation errors occurred because rule premises, active-authority semantics, certificate scope, and cross-rule dispatch were encoded procedurally rather than as explicit derivation clauses.

That debt should not be misreported as 17 separate capability gaps, but neither should it be hidden.

## 4. Witness ledger

| Case | Error kind | Observed | Expected | Class | Shallowest implementation locus | Rule impact |
|---|---|---|---|---|---|---|
| `CASE-101` | NONE | `NOT_IDENTIFIED@LICENSE` | `UNLICENSED_JURISDICTION_TRANSFER@TRANSFER` | **IMPLEMENTATION** | R3:LICENSE information-flow lineage lookup | R3 implementation only |
| `CASE-104` | OVERREACH | `AUTHORIZED_SCOPED` | `UNLICENSED_JURISDICTION_TRANSFER@SUBSTITUTE` | **IMPLEMENTATION** | R5:SUBSTITUTE transfer matching | R5 implementation only |
| `CASE-105` | OVERREACH | `AUTHORIZED_SCOPED` | `COMPOSITION_FAILURE@COMPOSE` | **IMPLEMENTATION** | R5→R9 transfer-chain composition gate | R5/R9 orchestration; no kernel growth |
| `CASE-107` | OVERREACH | `AUTHORIZED` | `COMPOSITION_FAILURE@COMPOSE` | **IMPLEMENTATION** | R9:COMPOSE certificate arity/scope matching | R9 implementation only |
| `CASE-109` | OVERREACH | `AUTHORIZED` | `COMPOSITION_FAILURE@COMPOSE` | **IMPLEMENTATION** | R9:COMPOSE component authority validation | R9 implementation only |
| `CASE-110` | FALSE_REFUSAL | `UNLICENSED_JURISDICTION_TRANSFER` | `AUTHORIZED_SCOPED` | **IMPLEMENTATION** | R4:EQUIV identity-transfer consumption | R4 implementation only |
| `CASE-111` | NONE | `NOT_IDENTIFIED@LICENSE` | `NOT_IDENTIFIED@EQUIV` | **IMPLEMENTATION** | R4:EQUIV foreign identity-regime localization | R4 localization implementation |
| `CASE-113` | FALSE_REFUSAL | `PROVENANCE_LEAK` | `AUTHORIZED_SCOPED` | **IMPLEMENTATION** | R3:LICENSE provenance guard / semantic-bridge recognition | R3 implementation only |
| `CASE-114` | FALSE_REFUSAL | `PROVENANCE_LEAK` | `AUTHORIZED_SCOPED` | **IMPLEMENTATION** | R3:LICENSE independence-bridge recognition | R3 implementation only |
| `CASE-115` | NONE | `NOT_IDENTIFIED@LICENSE with generic missing derivation` | `NOT_IDENTIFIED@LICENSE consumer_scoped_support_authority` | **IMPLEMENTATION** | R3:LICENSE support-edge localization | R3 diagnostic implementation |
| `CASE-116` | NONE | `NOT_IDENTIFIED@LICENSE` | `JURISDICTIONAL_DIVERGENCE@TRANSPORT` | **IMPLEMENTATION** | R2:ADMIT→R7:TRANSPORT comparison gate | R2/R7 orchestration; no kernel growth |
| `CASE-117` | FALSE_REFUSAL | `NOT_IDENTIFIED@LICENSE` | `AUTHORIZED_SCOPED` | **IMPLEMENTATION** | R2:ADMIT→R7:TRANSPORT positive comparison path | R2/R7 orchestration; no kernel growth |
| `CASE-118` | FALSE_REFUSAL | `UNLICENSED_JURISDICTION_TRANSFER` | `AUTHORIZED_SCOPED` | **IMPLEMENTATION** | R2:ADMIT universalization transfer matching | R2 implementation only |
| `CASE-119` | FALSE_REFUSAL | `UNLICENSED_TRANSPORT` | `AUTHORIZED_SCOPED` | **IMPLEMENTATION** | R7:TRANSPORT non-injective semantics gate | R7 implementation only |
| `CASE-120` | OVERREACH | `AUTHORIZED` | `NOT_IDENTIFIED@TRANSPORT` | **IMPLEMENTATION** | shared fact lookup used by R7 | shared active-fact predicate + R7 |
| `CASE-122` | OVERREACH | `AUTHORIZED` | `NOT_IDENTIFIED@PRESERVE` | **IMPLEMENTATION** | shared fact lookup used by R10 | shared active-fact predicate + R10 |
| `CASE-123` | NONE | `FUTURE_UNSAFE` | `NOT_IDENTIFIED@PRESERVE` | **IMPLEMENTATION** | shared fact lookup used by R10 | shared active-fact predicate + R10 |

## 5. Failure mechanisms

The 17 mismatches collapse into a small number of implementation mechanisms.

### A. Authority-status gating

Cases:

```text
CASE-120, CASE-122, CASE-123
```

The shared fact lookup treats fact presence as sufficient even when:

```text
authority = WITHDRAWN
authority = UNRESOLVED
```

This directly recreates the recurring SSI pathology:

> **fact availability does not imply current authority.**

Minimal counterfactual: positive premises require an **active-authority** predicate; unresolved/withdrawn facts remain inspectable for diagnostics but cannot discharge a proof obligation.

### B. Transfer target and transfer composition

Cases include:

```text
CASE-104
CASE-105
CASE-110
CASE-118
```

The checker alternates between two symmetric errors:

```text
some transfer exists -> authorize too much
explicit transfer exists -> refuse anyway
```

The missing implementation object is not a new rule but a typed transfer matcher:

```text
TransferOK(source_jurisdiction, target_jurisdiction, purpose)
```

with composition delegated to R9 rather than inferred from mere fact existence.

### C. Composition-certificate scope

Cases:

```text
CASE-105
CASE-107
CASE-109
```

The checker currently permits:

```text
pairwise certificate -> whole requested composition
composition certificate -> component jurisdiction repair
```

Both violate the frozen authority-edge discipline.

A certificate must cover the **requested transformation and its scoped components**, not merely overlap them.

### D. Positive bridge recognition

Cases:

```text
CASE-113
CASE-114
CASE-119
```

Anti-leak guards correctly recognize dangerous unlicensed moves in the original benchmark, but the implementation often fires the guard **before checking whether the missing bridge is now explicitly constituted**.

This is the symmetric failure:

> **anti-leak discipline does not imply ignoring earned transfer authority.**

### E. Cross-rule orchestration and localization

Cases include:

```text
CASE-101
CASE-111
CASE-115
CASE-116
CASE-117
```

The checker is organized as a linear first-match pipeline. H24 exposes requests whose correct adjudication crosses rule jurisdictions:

```text
lineage -> LICENSE
foreign identity regime -> EQUIV / TRANSFER
attribution + semantic bridge -> LICENSE
regime admission -> TRANSPORT
```

The rules exist, but the dispatcher often falls through to the generic evaluator instead of advancing to the next required gate.

The strongest architectural implementation finding is:

> **local rule recognition is stronger than cross-rule authority orchestration.**

## 6. Minimal counterfactuals

The machine-readable companion file records one minimal counterfactual per mismatch.

The aggregate repair surface is smaller than 17 patches. A successor implementation would likely need a small set of shared mechanisms:

```text
1. ACTIVE_AUTHORITY(fact)
2. typed TRANSFER_MATCH(source, target, purpose)
3. explicit transfer-chain composition through R9
4. certificate-covers-requested-composition checks
5. positive constituted-bridge recognition before anti-leak refusal
6. rule-gate orchestration instead of generic evaluator fallthrough
7. indirect lineage reachability for R3 oracle/information-flow checks
```

These are **candidate implementation repairs**, not authorized changes in this lineage.

No R12 candidate is admitted by this analysis.

## 7. The compass diagnosis

H24 did not primarily show that preservation-aware refusal is broken.

It showed the following sequence:

```text
authority representation
-> authority composition
-> boundary adjudication
-> preservation-aware refusal
```

with the downstream preservation stage remaining strong while upstream composition/adjudication fails.

The compact diagnosis is:

> **the compass is locally informed but compositionally unreliable.**

More precisely:

> the reference checker often recognizes individual authority facts correctly, but it does not yet compose, scope, withdraw, or transport them reliably in novel multi-fact derivations.

## 8. Scientific state

```text
INTERNAL_FROZEN_CONTRACT_PASS = PRESERVED
WHITEBOX_HELDOUT_H24 = FAILED
H24_FAILURE_ANALYSIS = COMPLETE
H1_IMPLEMENTATION = 17
H2_REPRESENTATION_SPECIFICATION = 0
H3_MISSING_CAPABILITY = 0
R12_AUTHORIZED = NO
NICHE_ADVANTAGE_ESTABLISHED = NO
```

The next earned transition is **not kernel growth**.

It is a successor implementation proposal that groups the 17 failures by shared mechanism, makes the minimal R1..R11 implementation revisions, reruns the untouched 64 + H24, and then faces a **fresh held-out object**. H24 must remain a regression set after repair; it can never become fresh validation again.
