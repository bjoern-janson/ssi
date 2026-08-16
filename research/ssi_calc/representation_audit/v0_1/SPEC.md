# SSI-CALC Representation Audit v0.1 — Extension Contract

Status: `REPRESENTATION_AUDIT_V0.1_FREEZE_CANDIDATE`

This is an **optional audit namespace**, not a new SSI-CALC authority rule and not an extension of the frozen `SSI_CALC_V0.1` kernel. It evaluates whether a supplied representation preserves the distinctions of an independently constituted observable for a named purpose.

## 1. Object

\[
\boxed{
\texttt{REPRESENTATION\_AUDIT}_{v0.1}=(\Sigma_{RA},D_{RA},B_{RA})
}
\]

It does not train representations, infer semantic authority from predictive performance, or authorize actions.

## 2. Purpose-indexed recoverability

For a representation

\[
f:\mathcal X\to Z
\]

and constituted observable

\[
O_{\Delta_\kappa}:\mathcal X\to Y_\kappa,
\]

recoverability for purpose \(\kappa\) is

\[
\boxed{
\operatorname{Recoverable}_\kappa(f,O)=1
\iff
\exists R_\kappa:\ O_{\Delta_\kappa}=R_\kappa\circ f.
}
\]

On a complete finite audit domain this is equivalent to

\[
\boxed{
\ker f\subseteq\ker O_{\Delta_\kappa}.
}
\]

The same representation may be sufficient for one purpose and insufficient for another. No global representation-sufficiency bit is licensed.

## 3. Outcomes

```text
REPRESENTATION_SUFFICIENT
AUTHORIZED_DISTINCTION_LOST
REPRESENTATION_NOT_IDENTIFIED
```

`AUTHORIZED_DISTINCTION_LOST` requires a witnessed collision:

\[
f(x_1)=f(x_2)\land O_{\Delta_\kappa}(x_1)\ne O_{\Delta_\kappa}(x_2).
\]

A witnessed collision is decisive even when the audit domain is incomplete. By contrast, absence of a collision on an incomplete domain yields `REPRESENTATION_NOT_IDENTIFIED`, not sufficiency.

## 4. Implemented operations

### `CHECK_SUFFICIENCY`

Checks finite kernel containment for a named `purpose` and `observable_id` using supplied `representation_value` and `observable_value` pairs.

### `CHECK_MASK_SUFFICIENCY`

Runs the same calculation over a supplied `masked_representation_value` for a named `mask_id`. This is an audit of which constituted distinctions survive the masking/transformation; it is not JEPA training and does not infer that a mask is permanently safe.

## 5. Reserved, not implemented

```text
CHECK_ALTERNATIVE_FRONTIER
PREDICT_CONSEQUENCE
```

These names are reserved only to prevent accidental conflation with current functionality. The first requires a separately constituted frontier contract. The second is a proposal/prediction interface and may never imply `AUTHORIZE_ACTION` without an independent authority derivation.

Future corrective sufficiency, JEPA training, EMA target networks, Gaussian/LeJEPA regularization, world-model learning, robot planning, and probabilistic uncertainty are explicitly out of scope.

## 6. Typing firewall

Inputs must bind:

```text
purpose
observable_id
finite audit samples
completeness flag
```

A missing purpose, missing observable constitution, missing representation value, or incomplete non-colliding domain yields `REPRESENTATION_NOT_IDENTIFIED`.

The audit answer is a representation-conformance fact only:

\[
\boxed{
\text{representation sufficiency}\ne\text{prediction accuracy}\ne\text{authority}\ne\text{future sufficiency}.
}
\]

## 7. Certificate payload

Each result returns the scoped purpose, observable identifier, finite-domain completeness, collision witnesses, and status. Collision witnesses preserve the state IDs and conflicting authorized-observable values needed to reopen or repair the representation.

## 8. Benchmark-first discipline

The bundled benchmark contains positive recoverability cases, authorized-distinction collisions, incomplete-domain `NOT_IDENTIFIED` cases, a purpose-indexing discriminator in which one representation is sufficient under `kappa_prediction` but insufficient under `kappa_correction`, masking cases, typing failures, and a reserved-operation refusal.

No change is made to the frozen SSI-CALC v0.1 rule kernel, compiler, SSI-IR, K1 evaluator, R2/R3 constitutions, or runtime semantic-ABI patch.

## 9. Parked hypothesis

\[
\boxed{
H_{\rm PQC}:\text{predictive sufficiency does not guarantee future corrective sufficiency.}
}
\]

This hypothesis is recorded but **not implemented or scored** by this extension.
