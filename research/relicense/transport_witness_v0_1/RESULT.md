# SSI Relicense Transport Witness V0.1 — First Adversarial Result

Status: `COMPOSED_BOUNDARY_DEFEATER_EXPRESSIVE_GAP_IDENTIFIED`

The frozen transport suite was adjudicated against the pre-existing `SSI_RELICENSE_CERTIFICATE_CALCULUS_V0.1` using the separately frozen execution protocol.

No target calculus, schema, case, expectation, SSI-CALC rule, behavioral object, or JEPA state changed during adjudication.

## Frozen lineage

```text
main provenance baseline
    = 268ea1f84b92f6e2dfda08cc19563fdbb8e26a97

transport SPEC freeze
    = 568f5e7db3b18e0f5fadd5d07079987c9c47de9e

transport CASES freeze
    = f1746a657872f105e6c5249f66afa8b829ae6813

execution protocol freeze
    = 46167168c8b1a51f3cc6099e30811f16445882e4

frozen target calculus SHA-256
    = af394081b10be84d7fd4d0b1f03e4ab13f4839d0ed661e812d3b8d81fd54aa40

frozen target certificate schema SHA-256
    = cff76ed9a30a45a99612e15b0846e34351405e8241594f2b7769d1ba3800b642
```

## Aggregate result

```text
cases                                  = 4
exact transport-oracle matches         = 3 / 4
invalid transitions authorized         = 0 / 4
local valid transitions destroyed      = 0 / 4
UNPROVEN/REVOKED collapses exposed      = 1
composition rule inferred              = NO
formal-soundness defect identified      = NO
formal-interface expressive gap         = YES
```

The mismatch is `TW-F4-001` only.

---

## TW-F3-001 — candidate-domain laundering

Frozen attack:

```text
Domain(H) != C
S(H,J,C) in C
```

The target calculus already requires:

```text
candidate_domain(H) = C2
```

and explicitly states that output membership is necessary but not sufficient. Failure of an authority obligation yields:

```text
C_auth = FAIL
L_target = NOT_ESTABLISHED
C_util = NOT_EVALUATED
```

Under the frozen transport mapping, failed establishment without a separately constituted active revocation is:

```text
UNPROVEN
```

Result:

```text
expected = UNPROVEN
observed = UNPROVEN
MATCH
```

Preserved facts:

```text
source judgment remains valid
selected endpoint remains a member of C
endpoint legality does not legalize the selection process
```

F3 therefore supports, on this formal object:

> **Legal output does not imply a legally constituted selection process.**

No new rule is required for this case.

---

## TW-F1-001 — nested refinement

Frozen attack:

```text
J1 --W12--> J2 = PRESERVED
J2 --W23--> J3 = PRESERVED
```

with no direct `W13` and no composition/interaction witness.

The target calculus explicitly freezes:

```text
C_auth^12 AND C_auth^23 !=> C_auth^13
```

and:

```text
CERTIFICATE_COMPOSITION = NONRULE_UNTIL_EARNED
```

Therefore the two local certificates remain valid but no direct target certificate is derivable.

Result:

```text
expected direct 1->3 = UNPROVEN
observed direct 1->3 = UNPROVEN
MATCH
```

The nested scope notation does not manufacture transitivity.

---

## TW-F2-001 — incomparable jurisdictions

Frozen attack:

```text
J_A not<= J_B
J_B not<= J_A
```

with no independently constituted transfer basis.

`CA-R1-REFINEMENT-SCOPE` requires a witnessed target-class containment relation for the certified refinement, and the formal audit explicitly preserves the absence of an unconditional cross-jurisdiction transfer rule.

The requested crossing cannot satisfy the frozen refinement rule and no generic transfer rule exists.

Result:

```text
expected = UNPROVEN
observed = UNPROVEN
MATCH
```

No refinement map is invented.

---

## TW-F4-001 — attempted certificate composition

Frozen attack:

```text
J1 --W12--> J2 = PRESERVED
J2 --W23--> J3 = PRESERVED
```

plus:

```text
I_123 = active composed-boundary interaction defeater
```

where `I_123` is active only for the requested `J1 -> J3` crossing and is invisible in both local transitions.

Frozen transport-oracle expectation:

```text
J1 -> J3 = REVOKED
```

because the longer crossing is affirmatively defeated, not merely unsupported.

### Existing-calculus observation

The target calculus correctly refuses to derive `C_auth^13` from the two local certificates because composition is an explicit non-rule.

Therefore it does **not** authorize the invalid composition.

However, the frozen V0.1 authority-certificate schema contains the authority witness fields:

```text
target_constitution_independent_of_H
class_map
class_containment
candidate_domain_exactly_target_class
authority_relation_immutable_under_H
selector_output_membership
```

and authority statuses:

```text
STRUCTURALLY_VERIFIED_UNDER_V0_1_CALCULUS
UNPROVEN
FAIL
```

It has no authority-level field/premise representing an interaction that exists only across the composed boundary, and no native `REVOKED` transport state.

Consequently the existing calculus can only leave the direct crossing unestablished.

Under the frozen comparison protocol:

```text
observed direct 1->3 = UNPROVEN
```

Result:

```text
expected = REVOKED
observed = UNPROVEN
MISMATCH
```

### Shallowest diagnosis

```text
H2 = TARGET_FORMAL_INTERFACE_EXPRESSIVE_INSUFFICIENCY
```

More specifically:

```text
COMPOSED_BOUNDARY_INTERACTION_DEFEATER_NOT_REPRESENTABLE
```

This is **not** an invalid-authorization witness.

The target did the safe thing:

```text
do not compose
```

but it cannot yet express the stronger fact:

```text
this longer crossing is actively defeated by an interaction that appears only under composition
```

Therefore:

```text
UNPROVEN != REVOKED
```

is not merely terminological. The first adversarial suite identifies a concrete formal situation in which the distinction matters.

---

## Scientific interpretation

The result supports three bounded claims.

### 1. The current refinement calculus survives F3/F1/F2 without overreach

It rejects candidate-domain laundering, refuses silent transitivity, and does not coerce incomparable jurisdictions.

### 2. No formal-soundness defect was identified in F4

The calculus does **not** authorize:

```text
C_auth^12 AND C_auth^23 => C_auth^13
```

so the attack does not show unsafe certificate composition.

### 3. F4 exposes a composition-level expressive gap

The existing interface cannot represent a defeater that becomes visible only for the longer crossing strongly enough to distinguish:

```text
not proven
```

from:

```text
actively invalidated by composed-boundary interaction
```

This earns a narrower next research object:

```text
composition / interaction witness or defeater interface
```

It does **not** earn a composition rule.

The current evidence therefore supports keeping separate research obligations for:

```text
W_tr  = witness that a judgment survives one boundary
W_comp = future witness/interaction object for a longer composition
```

but does not yet define `W_comp`, prove its sufficiency, prove its necessity, or establish a universal inequality theorem between witness classes.

---

## Current non-collapse

The strongest bounded formal conclusion from this first suite is:

```text
local validity
!=
transport establishment
!=
composition establishment
```

with an additional demonstrated distinction:

```text
composition UNPROVEN
!=
composition REVOKED by active interaction
```

This is adversarial support for the transition-boundary discipline on the frozen formal objects. It is not a universal theorem.

---

## Authority ceiling

```text
SSI_RELICENSE_TRANSPORT_WITNESS_V0.1
    = FIRST_ADVERSARIAL_EXECUTION_COMPLETE

F3_CANDIDATE_DOMAIN_LAUNDERING
    = REJECTED_BY_EXISTING_CA_R1

F1_NESTED_REFINEMENT
    = NO_SILENT_TRANSITIVITY

F2_INCOMPARABLE_JURISDICTIONS
    = NO_GENERIC_TRANSFER

F4_CERTIFICATE_COMPOSITION
    = NO_INVALID_COMPOSITION_AUTHORIZED

F4_COMPOSED_BOUNDARY_DEFEATER
    = EXPRESSIVE_GAP_IDENTIFIED

W_tr
    = FORMAL_RESEARCH_OBJECT_UNDER_TEST

W_comp
    = SEPARATE_RESEARCH_TARGET_NOW_MOTIVATED_NOT_DEFINED

COMPOSITION_RULE
    = NOT_ADMITTED

FORMAL_SOUNDNESS
    = UNESTABLISHED

EMPIRICAL_VALIDITY
    = NOT_CLAIMED

SSI_CALC_KERNEL_DELTA
    = 0

JEPA
    = PARKED

BEHAVIORAL_EXPERIMENT_AUTHORITY
    = NONE
```

The next admissible formal move is to constitute the **smallest composition/interaction witness interface** needed to discriminate active composed-boundary defeat from mere absence of proof, before attempting any positive composition rule.