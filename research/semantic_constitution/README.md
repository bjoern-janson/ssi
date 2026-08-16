# SSI Semantic Constitution — Lineage 2 Handoff

Status snapshot: 2026-08-16.

This directory is a **research handoff and authority map** for the semantic lineage that follows the failed `SSI-JURISDICTION-FALSIFICATION/S0` assay in PR #18. It is not an assay, observation operator, implementation, or scientific result. It does not modify the failed S0 lineage, Packet 7, CUHK-X, or any frozen object.

## Why this lineage exists

PR #18 froze and executed the first jurisdiction-falsification Stage-0 assay. It terminated:

```text
S0_VALID = false
OPERATIONALIZATION_INADEQUATE
NO_STAGE1_AUTHORITY
```

The localized defect was that the frozen leverage test was conditional on reachability:

```text
L := R AND (authority_after < authority_before)
```

so an `R↓` break forced the assay to report `L=0` even when leverage itself was intact. The assay therefore could not independently identify reachability and leverage.

That failed lineage remains failed. It is not repaired in place.

The only inherited scientific requirement was:

> `D`, `R`, `L_cap`, and `I_cap` must be independently semantically identifiable under controlled breaks before a new assay can claim to measure them.

This Lineage 2 therefore moved **upstream of measurement** and asked whether the semantic target itself could be constituted before any observation operator was designed.

## Permanent layer distinction

Do not collapse these states:

```text
SEMANTIC_TYPE_ERROR
    declared semantic graph is not formally closed / well-typed

SEMANTIC_NOT_IDENTIFIED
    graph is closed, but hostile semantic worlds expose ambiguity,
    circularity, drift, arbitrary truth conditions, or unstable identity

OBSERVATIONAL_NONIDENTIFIABILITY
    semantic target is well-defined, but an observation operator O merges
    target-distinct states

OPERATIONALIZATION_INADEQUATE
    an executed assay cannot localize the intended operational components
```

The ordering is intentional:

```text
semantic schema
    -> static closure
    -> hostile semantic adequacy
    -> only then observation / assay constitution
```

A failure at an earlier layer grants no authority to infer anything about later layers.

## Semantic target

The semantic lineage works with the target

\[
T_{\rm semantic}(s)=(D(s),R(s),L_{\rm cap}(s),I_{\rm cap}(s)).
\]

The important refinement from the failed S0 assay is:

- `L_cap` is leverage **capacity** at the authority boundary, not realized update and not `R AND update`;
- `I_cap` is an authority-independence / transportability property under licensed authority counterfactuals;
- `⊥` means the semantic property is not identified. It is not the same as `0`.

No current observation operator `O` is authorized for Lineage 2.

## V1 → V8 lineage

The versions below are semantic-contract lineages, not software releases.

| Version | Static status | Semantic status | Decisive result |
| --- | --- | --- | --- |
| **V1** | `FAILED_STATIC_CLOSURE` | not reached | `S_control` depended on target evaluability, creating `T -> D -> e_H -> Q_H -> S_control -> T`; additional referents remained unbound |
| **V2** | `CLOSED` | `REJECTED` | evidence equivalence lacked consumer congruence; detector `H(..., delta)` received the external answer oracle |
| **V3** | `FAILED_STATIC_CLOSURE` | not reached | `Info` was ill-typed/underspecified; `Inputs_licensed` missing; substitution schemas uninstantiated; inherited `delta -> H` contradicted the no-answer-oracle rule |
| **V4** | `CLOSED` | `REJECTED` | individually safe inputs could jointly reveal the answer (secret-sharing witness); declared substitution could disagree with consumer semantics |
| **V5** | `CLOSED` | `REJECTED` | `JNO_H` was well-typed but its extension was arbitrary: a named composition-safety predicate without independently grounded truth conditions |
| **V6** | `FAILED_STATIC_CLOSURE` | not reached | compatibility grounding introduced an undeclared licensed-input tuple type, undefined `equiv_I`, and raw answer equality instead of proposition identity |
| **V7** | `CLOSED` | `REJECTED` | `equiv_I = equiv_Info × equiv_Info` treated tuple identity as the product of component identities and erased constitutive joint relations |
| **V8** | `NOT_YET_CONSTITUTED` | not reached | current frontier: relational identity constitution |

### V1 — closure failure

The static checker rejected V1 before hostile semantic attack. The decisive cycle was:

\[
T\rightarrow D\rightarrow e_H\rightarrow Q_H\rightarrow\mathcal S_{\rm control}\rightarrow T.
\]

`S_control` had been defined partly by whether the target was semantically meaningful. That made the target participate in defining its own domain.

This established a durable rule:

> A target domain must be constituted independently of whether the target later evaluates successfully.

### V2 — closed but semantically inadequate

V2 repaired formal closure, but hostile attack found two independent semantic witnesses.

1. `e1 equiv_E e2` did not imply consumer interchangeability. The same evidence class could produce different authority semantics.
2. The challenge mechanism received `delta`, while `delta` contained the externally imposed correct answer. A trivial copier could obtain `D=1` without detecting anything.

Durable distinctions:

```text
semantic equivalence != licensed substitution
referent closure      != information-flow admissibility
```

### V3 — repair machinery failed closure

V3 introduced consumer-specific substitution licenses and semantic information licenses, but the repair layer itself was unclosed.

The checker localized:

- `Info` domain/type ambiguity;
- undeclared `Inputs_licensed`;
- generic `Sub_{F,r}` without the concrete route/authority instances required by the targets;
- a direct contradiction between inherited `H(..., delta)` and the no-answer-oracle constraint.

This preserved another rule:

> A repair mechanism earns no authority merely because it was introduced to enforce authority discipline.

### V4 — composition defeats local safety

V4 closed the V3 type defects. Hostile attack then found that pointwise safety did not compose.

Secret-sharing witness:

```text
x1 = r
x2 = r XOR b
```

Neither input individually contained the answer `b`, but the tuple did.

A second witness showed that a declared `Sub_A(e1,e2)=1` could coexist with different authority-semantic consequences if the consumer did not actually respect the license.

Durable rule:

> Local semantic safety is not automatically preserved under licensed composition.

### V5 — naming a guarantee does not ground it

V5 introduced a joint-non-oracularity predicate `JNO_H` and composition-preservation nodes. Static closure passed.

Hostile attack constructed two semantic models with the same grounded world facts but opposite `JNO_H` truth values. The contract fixed the predicate's extension before outcomes but supplied no independent truth condition for that extension.

Durable distinction:

```text
well-typed predicate != independently grounded predicate
fixed extension       != grounded extension
```

### V6 — compatibility grounding idea, missing identity machinery

V6 proposed the first non-arbitrary grounding candidate:

\[
\mathcal C(I)=\{s'\in\mathcal S_{\rm control}:I_H(s')\equiv_I I\},
\]

\[
G(I)=1
\iff
\forall s_a,s_b\in\mathcal C(I),\;
\kappa(\delta_a)\equiv_{\mathcal P}\kappa(\delta_b).
\]

Interpretation:

> A licensed input determines the answer iff no semantically compatible world permits a different answer.

The grounding idea itself was not semantically rejected. The static checker stopped earlier because `I`, `equiv_I`, and the cross-world proposition identity were not fully declared.

No dependency cycle was found in the intended direction:

```text
S_control -> I_H -> C(I) -> G -> JNO_H
```

### V7 — component identity is not composition identity

V7 declared the tuple type and defined componentwise identity:

\[
I_1\equiv_I I_2
\iff
x_1\equiv_{\rm Info}x_2
\land
y_1\equiv_{\rm Info}y_2.
\]

Static closure passed.

Hostile attack then changed only the licensed **joint interpretation relation** between otherwise component-identical inputs. The same component values could determine opposite answers under different joint semantic relations.

Therefore:

```text
part identity != composition identity
```

and, more generally:

> Semantic identity is relationally closed, not merely componentwise closed.

## Current frontier: V8 identity constitution

Authoritative state:

```text
V7_STATIC   = CLOSED
V7_SEMANTIC = REJECTED
V8          = NOT_YET_CONSTITUTED
O           = UNDEFINED
V0.2        = UNTESTED
```

V8 owns exactly one question:

> **What independently makes a relation among licensed inputs part of the identity of the composed semantic object?**

Do not broaden V8 into a theory of prediction, measurement, information, or all possible composition.

The allowed relation-level status is deliberately three-valued:

```text
CONSTITUTIVE
NONCONSTITUTIVE
NOT_IDENTIFIED
```

`NOT_IDENTIFIED` is a valid terminal state. V8 must not force every relation into the identity relation.

### Symmetric risks

V8 must avoid both:

```text
under-identification -> premature merging

over-identification  -> accidental/gratuitous structure becomes permanent identity
```

This is why SSI must not become preservation-maximalist. A distinction does not belong in identity merely because it might someday matter.

## V8 authority boundary

A relation does **not** earn identity membership merely because:

- it improves prediction;
- a model uses it;
- a downstream task depends on it;
- it is stable across environments;
- it varies with an environment;
- preserving it makes `G` produce a preferred result;
- it is convenient to serialize as a field.

The V8 candidate must independently ground constitutiveness **before** compatibility grounding `G` is allowed to use the resulting identity relation.

Forbidden direction:

```text
G / desired determinacy
    -> choose constitutive relations
    -> equiv_I
```

Required direction:

```text
licensed input semantics
    -> independently constituted joint relations
    -> composition identity
    -> equiv_I
    -> C(I)
    -> G
```

## Literature-derived attack material, not construction authority

The literature review conducted for this frontier supports only the weak claim that joint/contextual structure can carry information not recoverable from isolated component descriptions. It does **not** identify which relations belong in semantic identity.

Reserve these as hostile-attack families for an eventual V8 candidate:

```text
W_comp : same ingredients, different valid composition procedure
W_ctx  : same nominal task object, different generative/context regime
W_rel  : same components, different relations among them
```

They are attacks, not rules for constructing identity.

## Program-level chain

The current upstream-to-downstream order is:

```text
identity constitution
    -> licensed compression
    -> future sufficiency
    -> authority
    -> correction
```

V8 owns only the first object.

The strongest current compression is:

> **You cannot safely compress an object until you know what makes it the same object.**

## Exact next move for a successor

Do **not** build an assay and do **not** define an observation operator.

The next legitimate artifact is a minimal V8 relational-identity constitution candidate whose only burden is:

> What independent fact makes relation `r` constitutive, nonconstitutive, or not identified for the composed licensed input object?

After writing that candidate:

```text
V8 candidate
    -> STATIC_CLOSURE_CHECKER
        -> SEMANTIC_TYPE_ERROR : STOP, preserve failure
        -> CLOSED              : authorize hostile semantic attack
```

Only a statically closed candidate may be attacked with `W_comp`, `W_ctx`, and `W_rel` or other semantic counterexamples.

Even a V8 semantic success would **not** authorize an assay automatically. Observation/assay constitution remains downstream.

## Handoff discipline

A successor should preserve these rules:

1. **Do not modify PR #18 to repair S0.** It is a failed lineage and its failure is evidence.
2. **Do not collapse failure classes.** Static type failure, semantic inadequacy, observational nonidentifiability, and executed assay failure have different authority.
3. **Run the static checker before hostile semantic attack.** If closure fails, semantic adequacy is not adjudicated.
4. **Stop after a decisive witness.** Inherited constraints should be minimal; do not accumulate speculative repairs.
5. **No earned transition, no transition.** A negative or unconstituted state is a valid endpoint.
6. **Do not let downstream success define upstream semantics.** Prediction, `G`, measurement, or desired outcomes cannot constitute identity retroactively.
7. **Preserve failed versions.** Do not rewrite V1–V7 as if the final formulation had always been known.
8. **Keep `O` undefined until semantic constitution survives.** The current bottleneck is semantic identity, not instrumentation.

## What is already earned vs not earned

Earned:

- a recursive semantic type/closure discipline;
- a distinct hostile semantic adequacy layer;
- failure witnesses showing that equivalence, information safety, substitution, and identity can fail compositionally;
- compatibility-grounding candidate `G` as an idea worth retaining once identity is constituted;
- the V8 frontier above.

Not earned:

- a V8 identity rule;
- a general composition algebra;
- a general information measure;
- an observation operator for Lineage 2;
- a valid second S0 assay;
- Stage 1 jurisdiction authority;
- SSI validation.

## Scientific authority ceiling

This handoff document records the current research state. It does not itself establish V8, S0-2, Stage 1, or SSI.

```text
SEMANTIC_FRONTIER = IDENTIFIED
V8_CONSTRUCTION   = NOT_YET_CONSTITUTED
ASSAY              = UNDEFINED
OBSERVATION_O      = UNDEFINED
SSI_VALIDATION     = NOT_ESTABLISHED
```
