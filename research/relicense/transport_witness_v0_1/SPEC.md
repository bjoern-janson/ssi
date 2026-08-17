# SSI Relicense Transport Witness V0.1

Status: `FROZEN_FORMAL_CANDIDATE__ADVERSARIAL_EXECUTION_NOT_RUN`

Repository base:

```text
main merge commit = 268ea1f84b92f6e2dfda08cc19563fdbb8e26a97
parent provenance object = ssi-research-ledger/v0.5
```

This object opens the F4 transition-boundary program at the smallest boundary. It does **not** add a composition rule, modify SSI-CALC, reopen behavioral experiments, or instantiate JEPA.

The research question is:

> **What is the minimum witness that turns a valid scoped judgment into a valid transition to another scoped judgment?**

The governing non-collapse is:

```text
validity != transportability != composability
```

and the methodological constraint is:

> **Do not coerce across a boundary. Certify the boundary.**

---

## 1. Primitive transition object

A candidate boundary is represented as:

```text
T_12 = (Gamma, J_1 @ sigma_1, b_12 : sigma_1 -> sigma_2, J_2 @ sigma_2, E_12)
```

where:

- `J_1 @ sigma_1` is a valid source scoped judgment;
- `J_2 @ sigma_2` is the target judgment under evaluation;
- `b_12` identifies the particular scope/jurisdiction boundary;
- `E_12` is the constituted evidence available for deciding whether the source entitlement survives that boundary.

A transport witness is **relational**, not intrinsic:

```text
W_tr^12 subseteq E_12
```

and is meaningful only for the exact tuple `(J_1, b_12, J_2)`.

V0.1 does not claim that a particular evidence decomposition is minimal. The adversarial suite exists to attack necessity and sufficiency before any stronger schema is promoted.

No global predicate of the form

```text
Transportable(J)
```

is admitted.

---

## 2. Transport outcome type

Every attempted boundary crossing returns exactly one transition status:

```text
PRESERVED
EXTENDED
REVOKED
UNPROVEN
```

Candidate V0.1 meanings:

### `PRESERVED`

The source entitlement is supported across this exact boundary with no additional target-side entitlement silently inherited or invented.

### `EXTENDED`

The target judgment is supported only because independently constituted target-side entitlement supplements the preserved source entitlement. The extension must be named as target-side authority; it is not attributed to transport alone.

### `REVOKED`

Active target/boundary evidence defeats the transported entitlement claim for this crossing.

### `UNPROVEN`

The available evidence does not establish transport, and no active defeating judgment is sufficient to classify the crossing as revoked.

Hard firewall:

```text
UNPROVEN != REVOKED
```

A missing, malformed, inapplicable, or insufficient witness cannot by itself revoke the source judgment.

A transition status is local to the crossing. `REVOKED` for `T_12` does not retroactively invalidate `J_1 @ sigma_1` unless a separate source-side revocation is constituted.

---

## 3. Required preservation discipline

A failed transport derivation must preserve every unaffected valid fact.

In particular:

```text
valid source judgment + failed transport
!=
invalid source judgment
```

and:

```text
legal endpoint + illegal/unsupported transition
!=
legal transition
```

The transport object must therefore distinguish at least:

```text
source validity
boundary warrant
target validity
transition status
```

without collapsing them into one scalar certificate.

---

## 4. Candidate-domain invariant carried into transport attacks

For representative-selection judgments inherited from `SSI_RELICENSE_CERTIFICATE_CALCULUS_V0.1`, endpoint membership is insufficient.

The frozen candidate-domain invariant remains:

```text
Domain(H_C) = C
before
S(H,J,C) in C
```

Therefore:

```text
S(H,J,C) in C
AND
Domain(H_C) != C
```

must not establish transport of the selection entitlement.

Compact law:

> **Legal output does not imply a legally constituted selection process.**

This is a transport attack on an existing formal invariant, not a new SSI-CALC rule.

---

## 5. Explicit non-rules

V0.1 freezes the following as non-rules:

```text
valid source !=> valid target
valid endpoints !=> valid transition
witness exists !=> witness sufficient
source entitlement !=> target entitlement
refinement-looking notation !=> refinement authority
adjacent valid transports !=> direct transport
adjacent valid transports !=> valid composition
```

In particular:

```text
J_1 --W_12--> J_2
AND
J_2 --W_23--> J_3
!=>
J_1 --W_13--> J_3
```

and:

```text
W_tr^12 AND W_tr^23 !=> W_comp^123
```

`W_comp` is named only as a future research target. It is not defined, derived, or admitted as a rule in this object.

---

## 6. First adversarial suite

The frozen attack order is deliberately asymmetric:

```text
F3 candidate-domain laundering
-> F1 nested refinement
-> F2 incomparable jurisdictions
-> F4 attempted certificate composition
```

The order is chosen so that the first attack tests whether process constitution survives boundary reasoning before any composition machinery is considered.

### F3 — candidate-domain laundering

Construct:

```text
Domain(H) != C
S(H,J,C) in C
```

while preserving endpoint legality and every unrelated source fact.

Expected transition result:

```text
UNPROVEN
```

with the shallow reason:

```text
CANDIDATE_DOMAIN_MISMATCH
```

The derivation must not be rescued by the legal selected representative.

### F1 — nested refinement

Constitute nested scopes:

```text
sigma_3 <= sigma_2 <= sigma_1
```

with individually sufficient local transport witnesses for:

```text
J_1 --W_12--> J_2
J_2 --W_23--> J_3
```

The local crossings may each return `PRESERVED`.

Then request a direct `J_1 -> J_3` crossing without a direct witness or separately constituted composition/interaction witness.

Expected direct result:

```text
UNPROVEN
```

The implementation/formal derivation must not manufacture transitivity from nested notation.

### F2 — incomparable jurisdictions

Constitute:

```text
J_A not<= J_B
J_B not<= J_A
```

with a valid source judgment in `J_A` and no independently constituted transport basis into `J_B`.

Expected result:

```text
UNPROVEN
```

The calculus must not invent a refinement relation or treat relicensing as a generic transfer operator.

### F4 — attempted certificate composition

Constitute two individually valid crossings:

```text
J_1 --W_12--> J_2
J_2 --W_23--> J_3
```

with each local crossing returning:

```text
PRESERVED
```

Then add a composed-boundary interaction/defeater `I_123` that is not visible in either local crossing but is active for the requested `J_1 -> J_3` transition.

Expected direct/composed result:

```text
REVOKED
```

The local transport judgments remain valid and must not be destroyed.

This case attacks the forbidden inference:

```text
local transport validity
+
local transport validity
!=
global composition validity
```

It is the first explicit target for the later question:

> **What additional witness is required before two individually valid boundary crossings support a longer crossing?**

No answer to that question is frozen here.

---

## 7. Adjudication invariants

Any future formal executor for this object must satisfy:

```text
I1  source validity is evaluated separately from transport status
I2  boundary identity is explicit
I3  witness applicability is typed to the exact boundary
I4  UNPROVEN never aliases REVOKED
I5  failed transport preserves unaffected source facts
I6  endpoint legality cannot repair candidate-domain mismatch
I7  incomparable jurisdictions cannot be coerced into refinement
I8  local transport witnesses cannot be silently composed
I9  active composed-boundary defeaters can defeat the longer crossing without invalidating local crossings
I10 no SSI-CALC, behavior, or JEPA authority is acquired
```

---

## 8. Scientific decision surface

The first adversarial execution may support only one of these bounded conclusions:

```text
A  candidate transport interface survives the frozen attacks
B  candidate interface is expressively insufficient
C  candidate interface permits an invalid transition/composition
D  result is not identified because the attack itself is underconstituted
```

No outcome establishes a universal transport theorem.

No outcome may retroactively change the frozen Relicense Calculus, F5, or SSI-CALC.

A formal failure must be localized before any repair:

```text
representation/specification
inference/derivation semantics
boundary typing
witness sufficiency
composition/interaction gap
```

---

## 9. Authority ceiling

```text
SSI_RELICENSE_TRANSPORT_WITNESS_V0.1 = FROZEN_FORMAL_CANDIDATE
TRANSPORTABILITY = UNDER_ADVERSARIAL_TEST
COMPOSITION_RULE = NOT_ADMITTED
W_comp = FUTURE_TARGET_ONLY
F4_CERTIFICATE_COMPOSITION = NOT_YET_EXECUTED
FORMAL_SOUNDNESS = UNESTABLISHED
EMPIRICAL_VALIDITY = NOT_CLAIMED
SSI_CALC_KERNEL_DELTA = 0
JEPA = PARKED
BEHAVIORAL_EXPERIMENT_AUTHORITY = NONE
```

The next admissible transition is to execute the frozen four-case adversarial suite without modifying this specification or its expected outcomes.