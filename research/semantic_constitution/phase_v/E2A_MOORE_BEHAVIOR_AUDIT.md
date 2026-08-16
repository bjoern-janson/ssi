# E2-A Moore Behavioral-Equivalence Audit

Status snapshot: 2026-08-16.

```text
OBJECT = SEMANTIC_EQUIVALENCE_REGIME_AUDIT/E2-A/MOORE_BEHAVIOR
AUDIT_METHOD = EXECUTABLE_DETERMINISTIC_FINITE_PARTITION_REFINEMENT
TERMINAL_STATUS = PASS

IDENTITY_AUTHORIZATION = NOT_IN_SCOPE
IDENTITY_REGIME_MEMBERSHIP = NOT_AUTHORIZED
FUTURE_SUFFICIENCY = NOT_IN_SCOPE
CROSS_REGIME_COMPARISON = NOT_IN_SCOPE
```

This is the first executed Phase-V semantic-equivalence audit. It intentionally computes only the behavioral equivalence licensed by the externally constituted Moore-style semantic regime and verifies its declared congruence scope.

It does **not** convert behavioral equivalence into presentation-state identity.

---

## 1. Frozen inputs

The presentation-state carrier is:

\[
Q=\{q_1,q_2,q_3,q_4\}.
\]

Actions:

\[
U=\{a,b\}.
\]

Observations:

\[
\operatorname{Obs}(q_1)=\operatorname{Obs}(q_2)=y_0,
\qquad
\operatorname{Obs}(q_3)=\operatorname{Obs}(q_4)=y_1.
\]

All states have the same declared type:

\[
\operatorname{Type}(q_i)=\theta.
\]

Transition table:

| state | \(a\) | \(b\) |
|---|---|---|
| \(q_1\) | \(q_3\) | \(q_1\) |
| \(q_2\) | \(q_4\) | \(q_2\) |
| \(q_3\) | \(q_3\) | \(q_1\) |
| \(q_4\) | \(q_4\) | \(q_2\) |

The machine-readable frozen input is [`E2A_WORLD.json`](E2A_WORLD.json).

Input SHA-256:

```text
40631f87972439dbff9a442375b10c767ea9b04191692c401ffb990b3e668021
```

---

## 2. External semantic regime

The regime is:

```text
REGIME = DETERMINISTIC_MOORE_COALGEBRAIC_BEHAVIOR
PURPOSE = FINITE_INPUT_OBSERVATIONAL_BEHAVIOR
```

Define the state-local readout:

\[
\omega(q)
=
\bigl(
\operatorname{Type}(q),
\operatorname{Obs}(q)
\bigr).
\]

The E2-A world therefore has the Moore-coalgebra shape:

\[
\gamma:
Q
\to
(\Theta\times Y)\times Q^U.
\]

The behavioral denotation domain is:

\[
D_{\rm beh}
=
(\Theta\times Y)^{U^*}.
\]

For finite action word \(w\in U^*\), define:

\[
\nu_{\rm beh}(q)(w)
=
\omega(\delta^*(q,w)).
\]

Behavioral equivalence is:

\[
\boxed{
q\equiv_{\rm beh}q'
\iff
\nu_{\rm beh}(q)=\nu_{\rm beh}(q').
}
\]

This equality lives in the behavioral denotation domain. It does not establish presentation identity.

---

## 3. Executable audit

The verifier is [`verify_moore_behavior.py`](verify_moore_behavior.py).

Verifier SHA-256:

```text
641f72ded761448d11318eb99f7f00788b9c0458b2ac4d28f8d8232771560029
```

Run from this directory:

```bash
python3 verify_moore_behavior.py
```

The verifier:

1. constructs the immediate output partition;
2. repeatedly refines states by current output and successor-block signature;
3. stops at the stable behavioral partition;
4. verifies immediate-readout preservation;
5. verifies transition congruence for every action;
6. verifies the generator property implying the nonempty-word last-action result;
7. writes the deterministic result record.

No identity relation is read, created, optimized, or constrained by the verifier.

---

## 4. Behavioral result

The immediate output partition is:

\[
\Pi_\omega
=
\bigl\{
\{q_1,q_2\},
\{q_3,q_4\}
\bigr\}.
\]

Partition refinement performs **zero additional refinement rounds**.

Therefore:

\[
\boxed{
\Pi_{\rm beh}
=
\Pi_\omega.
}
\]

Equivalently:

\[
\boxed{
\ker\nu_{\rm beh}
=
\{q_1,q_2\}^2
\cup
\{q_3,q_4\}^2.
}
\]

The behavioral quotient has exactly two classes:

\[
\boxed{
Q/{\equiv_{\rm beh}}
=
\left\{
[q_1]=[q_2],
[q_3]=[q_4]
\right\}.
}
\]

The committed result is [`E2A_MOORE_BEHAVIOR_RESULT.json`](E2A_MOORE_BEHAVIOR_RESULT.json).

Result SHA-256:

```text
55624bce2ad25c2800a42f40b29f0aa6b7b8fbcd50a32770a32b0637b0837cc5
```

---

## 5. Congruence audit

For the first block:

\[
q_1\equiv_{\rm beh}q_2.
\]

Immediate output agrees:

\[
\omega(q_1)=\omega(q_2)=(\theta,y_0).
\]

Under action \(a\):

\[
\delta_a(q_1)=q_3
\equiv_{\rm beh}
q_4=\delta_a(q_2).
\]

Under action \(b\):

\[
\delta_b(q_1)=q_1
\equiv_{\rm beh}
q_2=\delta_b(q_2).
\]

For the second block:

\[
q_3\equiv_{\rm beh}q_4.
\]

Immediate output agrees:

\[
\omega(q_3)=\omega(q_4)=(\theta,y_1).
\]

Under action \(a\):

\[
\delta_a(q_3)=q_3
\equiv_{\rm beh}
q_4=\delta_a(q_4).
\]

Under action \(b\):

\[
\delta_b(q_3)=q_1
\equiv_{\rm beh}
q_2=\delta_b(q_4).
\]

Therefore:

\[
\boxed{
q\equiv_{\rm beh}q'
\Rightarrow
\delta_u(q)\equiv_{\rm beh}\delta_u(q')
\quad
\forall u\in U.
}
\]

By induction on action words:

\[
\boxed{
q\equiv_{\rm beh}q'
\Rightarrow
\delta_w(q)\equiv_{\rm beh}\delta_w(q')
\quad
\forall w\in U^*.
}
\]

Result:

```text
CONGRUENCE_SCOPE = VERIFIED
U_STAR_CLOSURE = VERIFIED_BY_ONE_STEP_CONGRUENCE_INDUCTION
```

---

## 6. Why the transition structure matters even though it does not refine the partition

A potentially misleading summary would be:

> the transition structure added nothing because \(\equiv_{\rm beh}=\equiv_\omega\).

That is false.

The transition structure contributes **certification without refinement**.

For action \(a\), every state transitions to a \(y_1\)-state. For action \(b\), every state transitions to a \(y_0\)-state:

\[
\boxed{
\omega(\delta_a(q))=(\theta,y_1),
\qquad
\omega(\delta_b(q))=(\theta,y_0)
\quad
\forall q\in Q.
}
\]

Hence for any nonempty word \(w\):

\[
\boxed{
\omega(\delta_w(q))
=
\begin{cases}
(\theta,y_1), & \operatorname{last}(w)=a,\\
(\theta,y_0), & \operatorname{last}(w)=b,
\end{cases}
}
\]

independently of the starting presentation state.

The only starting-state behavioral distinction therefore appears at the empty word/current readout.

So:

\[
\boxed{
\text{more semantic structure}
\not\Rightarrow
\text{more authorized distinctions}.
}
\]

Here the richer transition structure proves that the already visible output partition is stable through every licensed finite input context.

---

## 7. Jurisdictional interpretation

The audit establishes:

\[
q_1\equiv_{\rm beh}q_2,
\qquad
q_3\equiv_{\rm beh}q_4.
\]

It does not establish:

\[
q_1\equiv_{I,S_{\rm pres}}q_2
\]

or any other presentation-state identity claim.

The three layers remain distinct:

\[
\boxed{
\begin{aligned}
\text{reference} &: q_i\neq_{\rm ref}q_j \text{ for distinct tracked tokens},\\
\text{behavior} &: q_1\equiv_{\rm beh}q_2,\;q_3\equiv_{\rm beh}q_4,\\
\text{presentation identity} &: \texttt{NOT\_AUTHORIZED}.
\end{aligned}}
\]

Thus the audit gives a concrete positive case of:

\[
\boxed{
\textbf{semantic equivalence can be fully operationally useful without becoming identity.}
}
\]

---

## 8. Relationship to the earlier E2-A identity result

The earlier E2-A identity audit admitted every equivalence relation on the four presentation states because its theory contained no cross-constraint linking the prior transition/interface semantics to \(E_S\).

That result remains untouched.

Phase V introduces an **additional externally licensed behavioral relation**. It does not retroactively constrain \(E_S\).

Formally:

\[
\boxed{
\Delta\operatorname{Ext}_{E_S}=0.
}
\]

This coexistence is informative:

> one semantic jurisdiction may be fully determined while another remains underdetermined on the same presentation carrier.

Knowing behavior perfectly does not, by itself, settle presentation identity.

---

## 9. Terminal ledger

```text
OBJECT = SEMANTIC_EQUIVALENCE_REGIME_AUDIT/E2-A/MOORE_BEHAVIOR
AUDIT_METHOD = EXECUTABLE_DETERMINISTIC_FINITE_PARTITION_REFINEMENT

BEHAVIORAL_EQUIVALENCE = {{q1,q2},{q3,q4}}
NUMBER_OF_CLASSES = 2
BEHAVIORAL_EQUIVALENCE_EQUALS_IMMEDIATE_OUTPUT_EQUIVALENCE = true
PARTITION_REFINEMENT_ROUNDS_BEYOND_OUTPUT_PARTITION = 0

CONGRUENCE_SCOPE = VERIFIED
U_STAR_CLOSURE = VERIFIED_BY_ONE_STEP_CONGRUENCE_INDUCTION

IDENTITY_AUTHORIZATION = NOT_IN_SCOPE
IDENTITY_REGIME_MEMBERSHIP = NOT_AUTHORIZED
FUTURE_SUFFICIENCY = NOT_IN_SCOPE
CROSS_REGIME_COMPARISON = NOT_IN_SCOPE

TERMINAL_STATUS = PASS
```

The correct stopping statement is:

\[
\boxed{
\textbf{The external behavioral equivalence was consumed exactly within its constituted jurisdiction, and the audit stopped before identity.}
}
\]
