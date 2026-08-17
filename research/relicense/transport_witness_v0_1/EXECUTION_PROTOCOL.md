# SSI Relicense Transport Witness V0.1 — Execution Protocol

Status: `FROZEN_PROTOCOL__RESULT_NOT_YET_RECORDED`

This protocol binds the already-frozen `SPEC.md` and `CASES.json` to the pre-existing authoritative Relicense Calculus without modifying either object.

## 1. Frozen target

Target formal object:

```text
SSI_RELICENSE_CERTIFICATE_CALCULUS_V0.1
```

Bound identities:

```text
CALCULUS_SHA256 = af394081b10be84d7fd4d0b1f03e4ab13f4839d0ed661e812d3b8d81fd54aa40
CERTIFICATE_SCHEMA_SHA256 = cff76ed9a30a45a99612e15b0846e34351405e8241594f2b7769d1ba3800b642
```

Relevant frozen target semantics:

```text
CA-R1-REFINEMENT-SCOPE

1. J2 prospectively constituted independently of H and inherited utility evidence
2. C2 subseteq C1 witnessed for every certified target class
3. candidate_domain(H) = C2
4. H does not modify J2 admissibility/equivalence/class membership
5. S(H,J2,C2) in C2
6. certificate provenance and unvalidated remainder explicit
```

If any authority obligation fails:

```text
C_auth = FAIL
L_target = NOT_ESTABLISHED
C_util = NOT_EVALUATED
```

Target non-rules include:

```text
L(H,J1) !=> L(H,J2)
C_auth^12 AND C_auth^23 !=> C_auth^13
C_util^12 AND C_util^23 !=> C_util^13
```

Certificate composition remains:

```text
NONRULE_UNTIL_EARNED
```

## 2. Independence rule

The transport suite is not allowed to repair the target calculus during execution.

```text
DELTA_TARGET_CALCULUS = 0
DELTA_TARGET_SCHEMA = 0
DELTA_SPEC = 0
DELTA_CASES = 0
```

No transport status may be inferred merely because it is the frozen expected answer.

## 3. Existing-calculus observation mapping

The target calculus does not natively use the transport status vocabulary. The comparison therefore freezes this mapping before results are recorded.

### Existing authority certificate succeeds on the exact requested boundary

If the pre-existing calculus derives the target role-scoped license for the exact boundary and no separately constituted extension or active boundary defeater is present:

```text
OBSERVED_TRANSPORT_STATUS = PRESERVED
```

### Existing authority derivation fails or no rule licenses the crossing

If:

```text
C_auth = FAIL
```

or the requested crossing has no applicable derivation because an explicit target non-rule blocks inference, then:

```text
OBSERVED_TRANSPORT_STATUS = UNPROVEN
```

unless the target calculus itself contains a representable and applicable active revocation/defeater object sufficient to establish `REVOKED`.

This preserves:

```text
failed proof != revocation
UNPROVEN != REVOKED
```

### Extension

`EXTENDED` requires independently constituted target-side entitlement beyond the transported source entitlement. No frozen case in the first suite requires this status.

### Revocation

`REVOKED` requires an active target/boundary defeater to be representable and consumed as such. Merely lacking a certificate is insufficient.

## 4. Independent transport oracle

The frozen `CASES.json` expected statuses act as the prospective transport oracle.

The oracle is **not** a new rule in the target calculus. It exists only to discriminate:

```text
current calculus agrees with the frozen boundary semantics
```

from:

```text
current calculus cannot express or consume a distinction required by the frozen boundary semantics
```

This is directly analogous to the earlier F5 use of an independent prospective effect-trace oracle.

## 5. Case adjudication order

Execute exactly:

```text
1. TW-F3-001
2. TW-F1-001
3. TW-F2-001
4. TW-F4-001
```

For each case record:

```text
existing_calculus_observation
transport_oracle_expected
match_or_mismatch
shallowest_failure_locus_if_mismatch
preserved_valid_facts
```

## 6. Mismatch classification

A mismatch must be classified at the shallowest sufficient layer:

```text
H1 = execution / derivation application defect
H2 = target formal interface expressive insufficiency
H3 = transport-suite specification defect
H4 = genuine invalid authorization / formal-soundness witness
```

Do not call a missing composition rule a soundness defect merely because the target refuses to compose.

Do not call an inability to distinguish `UNPROVEN` from an independently constituted active composed-boundary defeater a successful revocation.

## 7. Outcome policy

Possible first-run conclusions:

```text
ALL_ATTACKS_MATCH
EXPRESSIVE_GAP_IDENTIFIED
TRANSPORT_SUITE_DEFECT_IDENTIFIED
INVALID_TRANSITION_AUTHORIZED
NOT_IDENTIFIED
```

No first-run outcome authorizes:

```text
W_comp as a derivation rule
certificate composition
SSI-CALC modification
behavioral experiments
JEPA
```

Any repair or new formal object requires a separate post-result lineage.