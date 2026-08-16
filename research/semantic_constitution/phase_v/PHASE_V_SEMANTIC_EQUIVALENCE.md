# Phase V — Scoped Semantic Equivalence

Status snapshot: 2026-08-16.

> **Phase-V boundary:** `DEMONSTRATED_IN_FROZEN_SYNTHETIC_FORMAL_SCOPE`

This artifact records the current semantic-authority architecture after the V8 identity-construction recursion was stopped. It is a **research-layer architecture**, not a replacement for the promoted SSI core pipeline in [`ARCHITECTURE.md`](../../../ARCHITECTURE.md), and it does not modify Packet 7 or any frozen prospective VFA object.

The decisive architectural shift is:

\[
\boxed{
\text{SSI need not originate semantic identity in order to consume legitimate semantic equivalence.}
}
\]

The operational signature is:

\[
\boxed{
\textbf{receive}
\rightarrow
\textbf{scope}
\rightarrow
\textbf{audit}
\rightarrow
\textbf{use}
\rightarrow
\textbf{stop}.
}
\]

The final `stop` is part of the architecture. A scoped semantic relation does not acquire authority merely because a stronger downstream use would be convenient.

---

## 1. From identity-first to purpose-indexed equivalence

The V8 lineage exposed repeated failures of the form:

\[
X\text{ is available}
\not\Rightarrow
X\text{ has authority for operation }Y.
\]

The strongest surviving generalization is:

\[
\boxed{
\textbf{An equivalence relation carries authority only together with the jurisdiction that constituted it.}
}
\]

The semantic object is therefore not an unindexed relation \(\equiv\), but:

\[
\boxed{
(\equiv_{r,\kappa},\kappa),
}
\]

where:

- \(r\) is an independently admitted semantic regime;
- \(\kappa\) is the declared semantic purpose, observation context, or operation family for which the equivalence is licensed.

The statement

\[
x\equiv_{r,\kappa}y
\]

means only:

> \(x\) and \(y\) are interchangeable under regime \(r\) for purpose \(\kappa\).

It does **not** automatically mean:

\[
x =_{\rm ref} y,
\qquad
x\equiv_{I,S}y,
\qquad
x\equiv_{r,\kappa'}y,
\]

or that the quotient induced by \(\equiv_{r,\kappa}\) is safe for future correction.

---

## 2. Three distinct relations

Phase V keeps three relations structurally separate.

### Referential identity

\[
x =_{\rm ref} y
\]

answers which tracked artifact, token, or presentation occurrence is being referenced.

### Purpose-indexed semantic equivalence

\[
x\equiv_{r,\kappa}y
\]

answers whether two presentations are interchangeable for a declared semantic purpose under an admitted regime.

### Semantic identity under a sort

\[
x\equiv_{I,S}y
\]

answers whether two presentations count as the same semantic object under a separately licensed identity regime for sort \(S\).

No automatic transfer is authorized:

\[
\boxed{
=_{\rm ref}
\not\Rightarrow
\equiv_{r,\kappa}
\not\Rightarrow
\equiv_{I,S}.
}
\]

Likewise:

\[
\boxed{
\equiv_{r,\kappa}
\not\Rightarrow
\equiv_{r,\kappa'}
}
\]

for \(\kappa\neq\kappa'\) without an independently constituted transfer.

This is the semantic analogue of the repository-wide provenance firewall:

> **Traceability grants reference authority, not semantic authority.**

---

## 3. Separate registries

The current architecture maintains separate regime registries:

\[
\boxed{
\mathfrak R_{\rm constituted}^{\rm eq}
\neq
\mathfrak R_{\rm constituted}^{\rm id}.
}
\]

A regime may be fully constituted and audited as a semantic-equivalence regime without entering any identity registry:

\[
\boxed{
r\in\mathfrak R_{\rm constituted}^{\rm eq}
\not\Rightarrow
r\in\mathfrak R_{\rm constituted}^{\rm id}.
}
\]

The same distinction applies after audit:

\[
\mathfrak R_{\rm audited}^{\rm eq}
\neq
\mathfrak R_{\rm audited}^{\rm id}.
\]

A successful equivalence audit therefore establishes only the relation and jurisdiction actually tested.

---

## 4. Regime constitution is scoped admission, not metaphysical endorsement

An external semantic regime does not need to be declared `ULTIMATELY_TRUE`.

Its admission is a versioned, scoped relation. Conceptually:

\[
Q_p(r,e,J,d)
\]

binds:

- regime/version \(r\);
- admission protocol \(p\);
- frozen envelope \(e\);
- semantic jurisdiction \(J\);
- evidence/provenance snapshot \(d\).

The constitution gate asks whether the regime is sufficiently external, scoped, explicit, coherent, and target-independent for the proposed use.

It does **not** ask SSI to re-found the ultimate philosophical legitimacy of the external discipline.

Permanent stopping rule:

\[
\boxed{
\textbf{Scoped external authority may enter without SSI re-grounding its ultimate philosophical basis.}
}
\]

A constituted regime therefore means:

> eligible for this scoped semantic use under this frozen contract.

It does not mean:

> universally true semantics.

---

## 5. Minimal equivalence-regime contract

For a semantic-equivalence regime, the useful object is:

\[
\boxed{
\mathcal R^{\rm eq}
=
(r,\kappa,S_{\rm pres},D_r,\nu_r,\Omega_r).
}
\]

Where:

- \(S_{\rm pres}\) is the presentation/source sort;
- \(D_r\) is the external semantic denotation domain;
- \(\nu_r:S_{\rm pres}\to D_r\) is the external semantic map;
- \(\Omega_r\) is the licensed operation/context family;
- \(\kappa\) names the purpose under which denotational equality is being consumed.

Define:

\[
\boxed{
x\equiv_{r,\kappa}y
\iff
\nu_r(x)=_{D_r}\nu_r(y).
}
\]

The equality on the right lives first in \(D_r\).

That yields a permanent typing rule:

\[
\boxed{
\textbf{Equality of denotations belongs to the denotation domain first; identity of presentations is a separate jurisdiction.}
}
\]

---

## 6. Congruence is a separate audit

A constituted equivalence relation does not automatically survive every operation.

For a licensed operation family \(\Omega_r\), the audit asks whether:

\[
x\equiv_{r,\kappa}y
\Rightarrow
f(x)\equiv_{r,\kappa'}f(y)
\]

for each declared \(f\in\Omega_r\), with the codomain purpose/type made explicit.

For state-transition semantics, this often becomes:

\[
x\equiv_{r,\kappa}y
\Rightarrow
\delta_u(x)\equiv_{r,\kappa}\delta_u(y)
\qquad
\forall u\in U.
\]

Only after that audit may the equivalence be consumed compositionally inside the declared operation family.

Permanent anti-leak:

\[
\boxed{
\text{equivalence}
\not\Rightarrow
\text{congruence}.
}
\]

---

## 7. Identity remains optional and orthogonal

Phase V does not insert an SSI-authored “identity bridge.”

There are only two legitimate outcomes.

### Equivalence-only regime

The external contract licenses interchangeability for \(\kappa\), but says nothing about identity of the presentation objects.

Then:

```text
SEMANTIC_EQUIVALENCE = CONSTITUTED
IDENTITY_AUTHORIZATION = NOT_IN_SCOPE
```

The regime remains useful.

### Identity of an externally declared semantic sort

The external theory itself says that the semantic objects are denotations in some sort \(S\), with identity fixed by equality in that denotation domain.

Only then may an identity regime be separately constituted.

The direction is external semantics \(\to\) identity authority, not SSI convenience \(\to\) identity.

---

## 8. Licensed quotient and future sufficiency remain downstream

A purpose-indexed equivalence may induce a local quotient:

\[
S_{\rm pres}/{\equiv_{r,\kappa}}.
\]

That quotient is licensed only for the semantic jurisdiction already established.

Two different questions remain downstream:

\[
\boxed{
\text{May these presentations be merged for }\kappa?
}
\]

and:

\[
\boxed{
\text{Will consuming that merge preserve distinctions required by }T_{\rm future}?
}
\]

Therefore:

\[
\boxed{
\text{congruence}
\not\Rightarrow
\text{future sufficiency}.
}
\]

The broader SSI sequence is:

\[
\boxed{
\text{semantic regime}
\rightarrow
\text{purpose-indexed equivalence}
\rightarrow
\text{congruence scope}
\rightarrow
\text{licensed quotient}
\rightarrow
\text{future sufficiency}
\rightarrow
\text{corrective reachability}.
}
\]

Identity may appear as a separately authorized semantic jurisdiction, but is no longer forced to sit in front of every useful quotient.

---

## 9. Cross-regime comparison requires constituted alignment

Different equivalence relations are not automatically regime disagreement.

For regimes \(r_1,r_2\):

\[
\equiv_{r_1,\kappa_1}\neq\equiv_{r_2,\kappa_2}
\]

may simply mean the regimes answer different semantic questions.

Cross-regime comparison is authorized only after a jurisdiction-comparability gate establishes:

1. **purpose/proposition compatibility**;
2. **carrier alignment**;
3. **relation and operation typing compatibility**;
4. **target-independent transport**.

If the source carriers differ, each transport

\[
\tau_r:S_r\to S_\ast
\]

is itself a semantic object requiring authority.

Only after those transports are constituted may the relations be compared on a common carrier:

\[
\widetilde{\equiv}_r
=
(\tau_r\times\tau_r)(\equiv_r).
\]

Then and only then may one form:

\[
\boxed{
\equiv_{\Box}^{\rm cross}
=
\bigcap_{r\in\mathfrak R_{\rm compared}^{\rm eq}}
\widetilde{\equiv}_r.
}
\]

If the comparability gate fails, the correct status is:

```text
JURISDICTIONAL_DIVERGENCE
```

not `REGIME_DISAGREEMENT`.

Permanent anti-leak:

\[
\boxed{
\textbf{unlicensed alignment}
\not\Rightarrow
\textbf{cross-regime comparison}.
}
\]

---

## 10. Demonstrated Phase-V instance

The first executed instance is the frozen E2-A Moore-behavior audit.

Current state:

```text
OBJECT_CLASS = SEMANTIC_EQUIVALENCE_REGIME
REGIME = DETERMINISTIC_MOORE_COALGEBRAIC_BEHAVIOR
PURPOSE = FINITE_INPUT_OBSERVATIONAL_BEHAVIOR

R_behavior^eq in R_constituted^eq = true
R_behavior^eq in R_audited^eq = true

IDENTITY_AUTHORIZATION = NOT_IN_SCOPE
IDENTITY_REGIME_MEMBERSHIP = NOT_AUTHORIZED
FUTURE_SUFFICIENCY = NOT_IN_SCOPE
CROSS_REGIME_COMPARISON = NOT_IN_SCOPE

PHASE_V_BOUNDARY = DEMONSTRATED_IN_FROZEN_SYNTHETIC_FORMAL_SCOPE
```

See:

- [`E2A_MOORE_BEHAVIOR_AUDIT.md`](E2A_MOORE_BEHAVIOR_AUDIT.md)
- [`E2A_MOORE_BEHAVIOR_RESULT.json`](E2A_MOORE_BEHAVIOR_RESULT.json)
- [`verify_moore_behavior.py`](verify_moore_behavior.py)
- [`E2A_WORLD.json`](E2A_WORLD.json)

The strongest demonstrated result is:

\[
\boxed{
\textbf{SSI successfully admitted and consumed an external semantic equivalence without allowing that equivalence to acquire identity authority.}
}
\]

This is an architectural demonstration in a frozen synthetic formal scope. It is **not** general validation across arbitrary semantic disciplines or empirical systems.

---

## 11. Permanent anti-selection laws

The Phase-V layer freezes the following prohibitions:

\[
\boxed{
\begin{aligned}
\text{desired identity}
&\not\rightarrow
\text{equivalence authority},\\
\text{desired comparison}
&\not\rightarrow
\text{regime constitution},\\
\text{desired disagreement}
&\not\rightarrow
\text{carrier alignment},\\
\text{desired result}
&\not\rightarrow
\text{transport semantics},\\
\text{audit result}
&\not\rightarrow
\text{retroactive external authority}.
\end{aligned}}
\]

Compactly:

\[
\boxed{
\textbf{No downstream convenience may create upstream semantic authority.}
}
\]

---

## 12. External semantic sources and authority ceiling

The behavioral regime used in the E2-A audit is grounded in standard deterministic coalgebraic/Moore-machine semantics, not invented from the desired E2-A partition.

Relevant external sources:

- J.J.M.M. Rutten, **Universal coalgebra: a theory of systems**, *Theoretical Computer Science* 249(1), 2000. CWI record: <https://ir.cwi.nl/pub/48>
- A. Silva, F. Bonchi, M.M. Bonsangue, J.J.M.M. Rutten, **Generalizing determinization from automata to coalgebras**, 2013. <https://arxiv.org/abs/1302.1046>
- `interface-theory` protocol boundary, which explicitly uses extensional collapse where sufficient while leaving protocol identity outside that layer: <https://github.com/bjoern-janson/interface-theory/blob/main/docs/protocol_foundations.md>
- `interface-theory` candidate qualification protocol, which separates qualification from comparison and forbids revising the admission envelope to admit a preferred candidate: <https://github.com/bjoern-janson/interface-theory/blob/main/ADAPTIVE_CAPACITY_CANDIDATE_QUALIFICATION_PROTOCOL.md>

These sources constitute the **scoped semantic role** used here. They are not imported as universal identity authority.

---

## 13. Stop condition

Nothing downstream is owed merely to create forward motion.

The current lineage may stop here until a genuinely new object arrives, for example:

- a second independently constituted semantic-equivalence regime;
- an independently constituted identity regime;
- an external challenge to the current admission contract;
- a future-sufficiency question that explicitly consumes the licensed quotient.

Do not manufacture any of these objects merely to populate the architecture.

> **Receive. Scope. Audit. Use. Stop.**
