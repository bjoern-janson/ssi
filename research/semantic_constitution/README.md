# SSI Semantic Constitution — Current Authority Index

Status snapshot: 2026-08-16.

This directory now contains **two distinct provenance layers**:

1. the reconstructed V1→V8 handoff that localized the original identity-construction problem;
2. the materialized Phase-V semantic-equivalence architecture and first executable E2-A audit.

The current authority state is **Phase V**, not the old “V8 identity constitution is the current frontier” snapshot.

The former `README.md` has been preserved byte-for-byte as:

- [`V1_V8_RECONSTRUCTED_HANDOFF.md`](V1_V8_RECONSTRUCTED_HANDOFF.md)

That file remains historical research provenance. Its statements about the “current frontier” describe the state at the time of that handoff and do not override the current Phase-V records.

---

## Current milestone

```text
PHASE_V_BOUNDARY = DEMONSTRATED_IN_FROZEN_SYNTHETIC_FORMAL_SCOPE

R_behavior^eq in R_constituted^eq = true
R_behavior^eq in R_audited^eq = true
R_behavior^eq in R_constituted^id = false

E2A_MOORE_BEHAVIOR_AUDIT = PASS
IDENTITY_AUTHORIZATION = NOT_IN_SCOPE
FUTURE_SUFFICIENCY = NOT_IN_SCOPE
CROSS_REGIME_COMPARISON = NOT_IN_SCOPE
```

The demonstrated path is:

```text
external semantic contract
    -> scoped constitution
    -> purpose-indexed equivalence
    -> congruence audit
    -> use inside jurisdiction
    -> STOP
```

The strongest current principle is:

> **An equivalence relation carries authority only together with the jurisdiction that constituted it.**

Or, more compactly:

\[
\boxed{
\text{the semantic object is }(\equiv,\kappa)\text{, not }\equiv\text{ alone.}
}
\]

---

## Current canonical files

### Phase-V architecture

- [`phase_v/PHASE_V_SEMANTIC_EQUIVALENCE.md`](phase_v/PHASE_V_SEMANTIC_EQUIVALENCE.md) — current scoped semantic-equivalence architecture, registry split, congruence jurisdiction, and cross-regime comparability gate.
- [`phase_v/STATUS.json`](phase_v/STATUS.json) — machine-readable Phase-V authority ledger.

### First executed audit

- [`phase_v/E2A_WORLD.json`](phase_v/E2A_WORLD.json) — frozen finite E2-A transition/interface world used by the audit.
- [`phase_v/verify_moore_behavior.py`](phase_v/verify_moore_behavior.py) — deterministic finite partition-refinement verifier.
- [`phase_v/E2A_MOORE_BEHAVIOR_RESULT.json`](phase_v/E2A_MOORE_BEHAVIOR_RESULT.json) — deterministic verifier output.
- [`phase_v/E2A_MOORE_BEHAVIOR_AUDIT.md`](phase_v/E2A_MOORE_BEHAVIOR_AUDIT.md) — human-readable audit and jurisdictional interpretation.

### Historical compression

- [`BOTTLENECK_HISTORY.md`](BOTTLENECK_HISTORY.md) — twenty-stage history compressed into five bottleneck phase transitions.
- [`V1_V8_RECONSTRUCTED_HANDOFF.md`](V1_V8_RECONSTRUCTED_HANDOFF.md) — preserved pre-Phase-V handoff; reconstructed provenance, not byte-complete V1→V7 execution evidence.

---

## Registry split

Semantic equivalence and identity are separate regime classes:

\[
\boxed{
\mathfrak R_{\rm constituted}^{\rm eq}
\neq
\mathfrak R_{\rm constituted}^{\rm id}.
}
\]

Therefore:

\[
\boxed{
r\in\mathfrak R_{\rm constituted}^{\rm eq}
\not\Rightarrow
r\in\mathfrak R_{\rm constituted}^{\rm id}.
}
\]

The behavioral regime is currently:

```text
OBJECT_CLASS = SEMANTIC_EQUIVALENCE_REGIME
REGIME = DETERMINISTIC_MOORE_COALGEBRAIC_BEHAVIOR
PURPOSE = FINITE_INPUT_OBSERVATIONAL_BEHAVIOR

SEMANTIC_EQUIVALENCE = CONSTITUTED
CONGRUENCE_SCOPE = VERIFIED

IDENTITY_ROLE = NOT_IN_SCOPE
IDENTITY_REGIME_MEMBERSHIP = NOT_AUTHORIZED
```

---

## Current E2-A result

The externally constituted Moore-style behavioral regime produces:

\[
\boxed{
\equiv_{\rm beh}
=
\{q_1,q_2\}^2
\cup
\{q_3,q_4\}^2.
}
\]

The immediate output partition is already behaviorally stable:

\[
\boxed{
\equiv_{\rm beh}
=
\equiv_\omega.
}
\]

The transition structure therefore contributes **certification without refinement**: it verifies that the output equivalence is preserved by each licensed action and hence by all finite action words.

This does not alter the earlier presentation-identity underdetermination.

---

## Cross-regime comparison gate

Two audited semantic-equivalence regimes are not automatically comparable merely because both define equivalence relations.

Comparison requires:

1. purpose/proposition compatibility;
2. constituted carrier alignment;
3. relation and operation typing compatibility;
4. target-independent transport.

For different carriers, a transport

\[
\tau_r:S_r\to S_\ast
\]

is itself a semantic object requiring authority.

Only after transport is licensed may one compare:

\[
\widetilde{\equiv}_r
=
(\tau_r\times\tau_r)(\equiv_r).
\]

If comparability fails, the correct status is:

```text
JURISDICTIONAL_DIVERGENCE
```

not `REGIME_DISAGREEMENT`.

Permanent anti-leak:

> **Unlicensed alignment does not authorize cross-regime comparison.**

---

## Current stop condition

No next semantic regime, identity regime, comparison panel, or future-sufficiency test is owed merely to continue the sequence.

A legitimate successor must bring a genuinely new independently constituted object or challenge.

Do not manufacture a second regime to force disagreement.

Do not promote behavioral equivalence into identity.

Do not consume the behavioral quotient for future-sufficiency claims until that downstream jurisdiction is separately constituted.

> **Receive. Scope. Audit. Use. Stop.**
