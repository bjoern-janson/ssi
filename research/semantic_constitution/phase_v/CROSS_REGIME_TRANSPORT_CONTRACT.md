# Cross-Regime Transport Contract

Status snapshot: 2026-08-16.

This note is the canonical typing rule for transporting purpose-indexed equivalence relations into a common cross-regime comparison domain.

It sharpens the shorthand notation used elsewhere in the Phase-V documentation.

## 1. Why transport itself needs a contract

For a regime \(r\), let:

\[
\equiv_r\;\subseteq\;S_r\times S_r
\]

be an equivalence relation on source carrier \(S_r\).

An arbitrary map

\[
\tau_r:S_r\to S_*
\]

does **not** guarantee that the direct image

\[
(\tau_r\times\tau_r)(\equiv_r)
\]

is an equivalence relation on \(S_*\). In particular, non-injective transport can merge images of distinct equivalence classes and destroy transitivity.

Therefore the expression

\[
\widetilde{\equiv}_r=(\tau_r\times\tau_r)(\equiv_r)
\]

is authorized only when the transport contract separately proves that the resulting relation is well-formed on the declared comparison domain.

Permanent rule:

\[
\boxed{
\textbf{carrier alignment does not imply equivalence-preserving transport.}
}
\]

## 2. A comparison domain must be constituted first

Cross-regime comparison is indexed to an explicit common comparison carrier:

\[
S_*^{\rm cmp}.
\]

This carrier is not inferred from the desired agreement/disagreement result.

Its constitution must specify:

- what its elements denote;
- how each source regime is related to it;
- which source elements are actually comparable;
- which operation family is common enough to compare.

If no such carrier can be constituted, stop with:

```text
JURISDICTIONAL_DIVERGENCE
```

## 3. Safe transport pattern A — pullback to a common carrier

When a constituted interpretation map exists:

\[
\pi_r:S_*^{\rm cmp}\to S_r,
\]

define:

\[
\boxed{
x\;\widetilde{\equiv}_r\;y
\iff
\pi_r(x)\equiv_r\pi_r(y).
}
\]

This is the pullback of \(\equiv_r\) along \(\pi_r\).

Because \(\equiv_r\) is an equivalence relation, its pullback is automatically an equivalence relation on \(S_*^{\rm cmp}\).

This is the preferred pattern when all regimes can interpret a genuinely common comparison presentation.

## 4. Safe transport pattern B — embedding into a common carrier

When a constituted injective embedding exists:

\[
\iota_r:S_r\hookrightarrow S_*,
\]

define the transported relation on the image \(\iota_r(S_r)\) by:

\[
\boxed{
\iota_r(x)\;\widetilde{\equiv}_r\;\iota_r(y)
\iff
x\equiv_r y.
}
\]

For cross-regime comparison, first constitute a common comparison subset:

\[
S_*^{\rm cmp}
\subseteq
\bigcap_r\iota_r(S_r),
\]

and restrict every transported relation to \(S_*^{\rm cmp}\).

Restriction of an equivalence relation to a subset remains an equivalence relation on that subset.

An arbitrary non-injective pushforward is **not** licensed by this pattern.

## 5. More general transports require an explicit proof obligation

A regime may use another alignment construction only if it separately establishes:

```text
TRANSPORTED_RELATION_WELL_FORMED = true
```

meaning that the transported relation is reflexive, symmetric, and transitive on the exact declared comparison carrier.

No notation is allowed to hide this burden.

## 6. Operation alignment must commute

Relation comparison is not enough to create a shared operational jurisdiction.

Let \(f_*\) be a proposed common operation and \(f_r\) the corresponding operation in regime \(r\).

For pullback-style alignment, require the relevant commuting condition:

\[
\boxed{
\pi_r\circ f_*
=
f_r\circ\pi_r
}
\]

on the declared comparison domain.

For embedding-style alignment, require:

\[
\boxed{
f_*\circ\iota_r
=
\iota_r\circ f_r
}
\]

where defined.

Only operations satisfying the constituted alignment contract belong to the cross-regime common operation family \(\Omega_*^{\rm cmp}\).

Therefore:

\[
\boxed{
\textbf{same operation name}
\not\Rightarrow
\textbf{same cross-regime operation}.
}
\]

## 7. Cross-regime invariant

Only after each regime supplies a well-formed transported equivalence relation on the **same** comparison carrier may one form:

\[
\boxed{
\equiv_\Box^{\rm cross}
=
\bigcap_{r\in\mathfrak R_{\rm compared}^{\rm eq}}
\widetilde{\equiv}_r.
}
\]

Because each \(\widetilde{\equiv}_r\) is then an equivalence relation on the same carrier, the intersection is also an equivalence relation on that carrier.

Its authority remains exactly:

> equivalent under every included, aligned regime for the frozen comparison proposition and common operational jurisdiction.

It does not acquire presentation-identity authority.

## 8. Revised comparability gate

Cross-regime comparison requires all of:

```text
PURPOSE_OR_PROPOSITION_COMPATIBILITY
COMMON_COMPARISON_DOMAIN_CONSTITUTED
CARRIER_ALIGNMENT_CONSTITUTED
TRANSPORTED_RELATION_WELL_FORMED
RELATION_TYPING_COMPATIBLE
COMMON_OPERATION_FAMILY_CONSTITUTED
OPERATION_ALIGNMENT_COMMUTES
TARGET_INDEPENDENT_TRANSPORT
```

Failure at any row yields:

```text
JURISDICTIONAL_DIVERGENCE
```

not `REGIME_DISAGREEMENT`.

## 9. Permanent anti-leak

\[
\boxed{
\textbf{unlicensed alignment}
\not\Rightarrow
\textbf{cross-regime comparison}.
}
\]

More precisely:

\[
\boxed{
\textbf{a map between carriers is not yet a transported semantic relation.}
}
\]

The relation, comparison domain, and common operation family must each survive their own typing and authority checks before cross-regime invariants are in scope.
