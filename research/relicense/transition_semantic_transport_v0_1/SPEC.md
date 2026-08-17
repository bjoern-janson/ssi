# SSI Relicense Transition Semantic Transport V0.1

```text
OBJECT = SSI_RELICENSE_TRANSITION_SEMANTIC_TRANSPORT_V0.1
STAGE  = SPEC
STATUS = SPEC_FROZEN__NO_CASES_NO_BINDINGS_NO_SEMANTIC_ORACLE_NO_PROTOCOL_NO_EVALUATOR_NO_RESULT
```

## 0. Parent boundary

This object opens from the exact frozen first RESULT of PR #60:

```text
PARENT_RESULT = 21753d9e3e2264c5954ba035ed5db0455cae4f5c
```

The parent result remains unchanged:

```text
G1 WORLD_NOVELTY                                  = SUPPORTED_ON_FROZEN_HELDOUT_STRESS_AXIS
G2 OBSERVATION_CHANNEL_NOVELTY                    = NOT_EVALUABLE_UNDER_FROZEN_BINDING
G3 COVERAGE_DEGRADATION                           = SUPPORTED_ON_FROZEN_HELDOUT_STRESS_AXIS
G4 FAILURE_STRUCTURE_NOVELTY                      = SUPPORTED_ON_FROZEN_HELDOUT_STRESS_AXIS
G5 COORDINATE_CONTRADICTION_OR_CONFLICTING_CHANNELS = SUPPORTED_ON_FROZEN_HELDOUT_STRESS_AXIS

FULL_FOUR_COORDINATE_SEPARABILITY_GENERALIZATION = NOT_ESTABLISHED
```

PR #59's constructed-suite result also remains unchanged:

```text
FOUR_COORDINATE_TRANSITION_INTERFACE_SEPARABILITY
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
```

This object does not reopen either result.

## 1. Sole scientific question

> **When may a novel observation carrier legitimately transport an already constituted predicate-/coordinate-relevant semantic object into the existing factorized transition interface without silently changing what that semantic object means?**

The target transition object remains:

\[
K=(S,\mathcal L,\mathcal V,\Lambda).
\]

No fifth transition coordinate is introduced.

The frontier is not whether these four roles can be represented. PR #59 and the evaluable axes of PR #60 already provide bounded evidence for that proposition.

The frontier is whether the meaning assigned to one of those roles can travel across a changed observation carrier while preserving semantic identity, evidence typing, provenance, and uncertainty.

## 2. Core decomposition

For a target coordinate \(i\in\{S,\mathcal L,\mathcal V,\Lambda\}\), keep four objects distinct:

\[
\boxed{
\text{carrier }c
\neq
\text{semantic object }m_i
\neq
\text{evidence type }\tau_i
\neq
\text{provenance }\pi
}
\]

### 2.1 Carrier \(c\)

The observation technology, encoding, message family, or source-side representation that carries information.

Examples inherited only as motivating parent witnesses, not as already validated transports:

```text
SIGNED_STATE_SNAPSHOT_V2
SIGNED_COUNTERFACTUAL_EVENT_BUNDLE_V2
APPLICABILITY_ATTESTATION_V2
AUTHORITY_RECEIPT_BUNDLE_V2
```

Carrier identity alone has no semantic or evidential authority.

### 2.2 Semantic object \(m_i\)

The coordinate-relevant meaning independently constituted from source semantics.

For this V0.1 target:

```text
S       -> current configuration semantics
L       -> complete response relation over the frozen probe domain
V       -> applicability context/envelope semantics
Lambda  -> authority context/allowed-effect-envelope semantics
```

### 2.3 Evidence type \(\tau_i\)

The target-side contract specifying what kind of evidence is admissible for the existing coordinate interface.

Evidence type is not defined by carrier name, payload shape, successful parsing, or candidate convenience.

### 2.4 Provenance \(\pi\)

Source lineage, authenticity, coverage, constitution, and other evidence-bearing facts that may matter to admissibility or challengeability.

Provenance must remain separately recoverable from semantic identity.

## 3. Central non-collapse

The experiment freezes these distinctions:

\[
\boxed{
\text{information transport}
\neq
\text{semantic transport}
\neq
\text{evidence-type admission}
\neq
\text{authority transport}
}
\]

and:

\[
\boxed{
\text{carrier novelty}
\neq
\text{semantic novelty}.
}
\]

A new carrier may express an old semantic object. An old carrier may express a new semantic object. Neither implication is automatic.

## 4. Prospective transport relation

Later BINDINGS may propose one deterministic transport candidate for each permitted source family. This SPEC does not constitute that candidate.

The prospective shape is:

\[
T_i:(c,o,\pi)\rightsquigarrow e_i
\]

where \(o\) is source-visible observation content and \(e_i\) is a target evidence object intended for coordinate \(i\).

A transport candidate may not define the source semantic object, the target evidence type, or the equivalence relation used to certify itself.

The scientific dependency must remain:

\[
\boxed{
\text{source cases}
\rightarrow
\text{transport candidate}
\rightarrow
\text{independent semantic/type oracle}
\rightarrow
\text{comparison}
\rightarrow
\text{judgment}
}
\]

not:

\[
\boxed{
T_i
\rightarrow
\text{semantic/type criterion}^{T_i}
\rightarrow
\text{self-certification}.
}
\]

## 5. Transport obligations

A positive semantic-transport result must satisfy all obligations below. No scalar compensation is permitted.

### ST-A1 — Semantic identity preservation

Where two independently constituted source observations carry the same coordinate-relevant semantic object under scope/predicate \((\sigma,P)\), a legitimate transport must preserve that semantic identity at the target interface.

\[
O_i(x_a)\equiv_i O_i(x_b)
\land
Transportable_i(x_a)
\land
Transportable_i(x_b)
\Rightarrow
D_i(T_i(x_a))\equiv_i D_i(T_i(x_b)).
\]

This is a carrier-invariance obligation, not a claim that the carriers are identical.

### ST-A2 — Semantic separation

Where independently constituted source semantics differ on the target coordinate, transport must not collapse them merely because the carrier family is the same or the payloads are structurally similar.

\[
O_i(x_a)\not\equiv_i O_i(x_b)
\Rightarrow
D_i(T_i(x_a))\not\equiv_i D_i(T_i(x_b))
\]

for cases legitimately admitted to the same target evidence type.

### ST-A3 — Evidence-type legitimacy

A source observation may enter target evidence type \(\tau_i\) only if independently frozen obligations for \(\tau_i\) are satisfied.

The transport candidate may not manufacture evidence-type membership from:

```text
carrier name
payload isomorphism
successful parsing
confidence score
prediction accuracy
opaque identifier match
shared field names
candidate output usefulness
```

Semantic sameness alone is insufficient:

\[
\boxed{
m_a\equiv_i m_b\not\Rightarrow \tau(m_a)=\tau(m_b).}
\]

A carrier change may preserve semantic identity while still failing evidence-type admission.

### ST-A4 — Provenance factor separation and recoverability

If provenance changes while coordinate-relevant semantics remain equivalent, semantic identity must remain invariant unless the frozen coordinate semantics explicitly make that provenance fact semantic.

At the same time, provenance relevant to admissibility or challengeability must remain recoverable rather than being erased into the semantic payload.

The experiment therefore requires both:

\[
\boxed{
\Delta \pi\not\Rightarrow\Delta m_i
}
\]

and:

\[
\boxed{
\text{semantic equivalence}\not\Rightarrow\text{provenance equivalence}.
}
\]

This is the transition-level continuation of the earlier relation/provenance factorization boundary.

### ST-A5 — Uncertainty preservation

Incomplete, ambiguous, conflicting, or only partially constituted source semantics must not be promoted to a complete target semantic identity merely to make the transport succeed.

\[
\boxed{
\text{insufficient source constitution}
\neq
\text{complete target evidence}.
}
\]

The transport must preserve the source-side epistemic limit in a form the target interface can represent or else remain not established/not evaluable under the frozen transport contract.

## 6. Role-preservation firewall

Transport is coordinate-indexed.

Evidence constituted for one transition role does not automatically transport into another:

\[
\boxed{
Transport_S\not\Rightarrow Transport_{\mathcal L}
\not\Rightarrow Transport_{\mathcal V}
\not\Rightarrow Transport_{\Lambda}.
}
\]

In particular:

```text
state semantics      != law semantics
law semantics        != validity semantics
validity semantics   != authority semantics
```

A source carrier may contain several kinds of information; that does not license cross-coordinate remapping.

## 7. Candidate failure modes authorized for later evaluation

This SPEC authorizes only the following broad transport-layer failures; later evaluator vocabulary must remain subordinate to these definitions and to any more specific frozen case geometry.

### 7.1 SEMANTIC_UNDER_RESOLUTION

Different independently constituted coordinate semantics collapse after legitimate transport.

### 7.2 SEMANTIC_CONTAMINATION

A variation assigned to carrier/provenance or another orthogonal factor changes the decoded target semantic identity when the target coordinate semantics are independently invariant.

### 7.3 EVIDENCE_TYPE_LAUNDERING

A source carrier is admitted as target evidence without satisfying the independently frozen target evidence-type obligations.

### 7.4 PROVENANCE_CONFLATION

Provenance variation changes coordinate semantic identity merely because provenance is encoded in the same representation, or semantic identity erases provenance that the target evidence contract requires to remain recoverable.

### 7.5 UNCERTAINTY_LAUNDERING

Incomplete, conflicting, proxy, or otherwise insufficient source evidence is transformed into a complete target semantic identity without an independently constituted basis.

These are interface/representation diagnostics. They do not establish causal mechanism.

## 8. Case-design requirements for the next stage

CASES must be constituted from this SPEC before any transport candidate is proposed.

The suite must include, for each relevant coordinate family where construction is feasible, adversarial examples spanning at least these relations:

### C1 — same semantics, different carriers

Hold the independently constituted coordinate semantic object fixed while changing carrier and provenance route.

Purpose: test carrier invariance without erasing provenance.

### C2 — different semantics, same carrier family

Hold carrier family fixed while changing coordinate-relevant semantic content.

Purpose: test semantic separation.

### C3 — same apparent payload shape, wrong evidence type

Construct source observations whose syntax or fields resemble admissible target evidence but whose source constitution does not satisfy the target evidence-type obligations.

Purpose: expose evidence-type laundering.

### C4 — proxy/prediction controls

Include high-confidence predictive or derived signals that may correlate with the target semantic object but do not independently constitute it.

Purpose: preserve:

\[
\boxed{
\text{prediction}\neq\text{observation}\neq\text{attestation}.
}
\]

### C5 — provenance variation

Hold semantic content fixed while varying source/provenance properties relevant to admissibility or challengeability.

Purpose: distinguish semantic identity from provenance/evidence legitimacy.

### C6 — incomplete/conflicting source semantics

Provide novel carriers with partial, missing, or conflicting source facts.

Purpose: test uncertainty preservation and prevent forced completion.

### C7 — role-crossing negatives

Provide a carrier with genuine semantics for one coordinate while making it superficially tempting to populate another coordinate.

Purpose: test coordinate-indexed transport rather than generic information transfer.

The CASES stage must not include:

```text
transport candidate outputs
expected transport verdicts
evaluator labels
semantic oracle labels
pass/fail fields
repair actions
boundary responses
```

Construction metadata may exist only outside candidate-visible surfaces.

## 9. Independent oracle requirement

A later SEMANTIC_ORACLE must independently describe, from SPEC + CASES only:

1. what semantic object each source carrier actually constitutes;
2. which target coordinate that object belongs to;
3. what source coverage/conflict/provenance is constituted;
4. what the frozen target evidence type requires;
5. whether a complete target semantic identity is independently available for comparison.

The oracle must not inspect transport candidate outputs or decide whether the candidate passed.

Critically:

\[
\boxed{
\text{source semantic identity}
\neq
\text{target evidence-type admissibility}.
}
\]

The oracle may establish each independently.

## 10. Future protocol boundary

A later PROTOCOL may compare the frozen transport candidate to the frozen semantic/type oracle, but may not redefine either side.

The comparison layer must preserve at least three descriptive possibilities:

```text
SEMANTICALLY_COMPARABLE_AND_TYPE_ADMISSIBLE
SEMANTICALLY_DESCRIBABLE_BUT_TYPE_ADMISSION_UNESTABLISHED
SOURCE_SEMANTICS_INSUFFICIENT_FOR_COMPLETE_COMPARISON
```

These are descriptive relations, not evaluator verdicts.

## 11. Future result space

The exact evaluator is not constituted here. Prospectively, the scientific result must distinguish at minimum:

```text
SEMANTIC_TRANSPORT_SUPPORTED_ON_FROZEN_SUITE
SEMANTIC_TRANSPORT_NOT_SUPPORTED_ON_FROZEN_SUITE
NOT_EVALUABLE_UNDER_FROZEN_TRANSPORT_CONTRACT
```

A not-evaluable or type-unestablished case is not to be relabeled as semantic transport failure unless a legitimate in-contract counterexample exists.

No scalar score may compensate across ST-A1..ST-A5.

## 12. Central falsification

The core falsification is:

> **Change the carrier while independently holding coordinate semantics fixed. If the transported semantic identity changes merely because the carrier/provenance route changed, semantic transport failed. Change the coordinate semantics while holding the carrier family fixed. If the transported semantic identity does not change, semantic transport failed. If a source is admitted to the target evidence type without satisfying its independently frozen type obligations, evidence-type laundering occurred.**

## 13. Parent G2 witnesses are boundary inputs, not positive examples

The four PR #60 G2 cases motivate this object:

```text
g2_state_signed_snapshot
g2_law_event_stream
g2_validity_attestation
g2_authority_receipt
```

PR #60 established only:

```text
complete target-role semantics exist on novel carriers
AND
the inherited PR #59 binding has no admissible input path to those carriers
```

It did not establish that any adapter from those carriers into the existing evidence types would be semantically preserving or evidentially legitimate.

Therefore:

\[
\boxed{
\text{PR60 G2 not evaluable}
\neq
\text{semantic transport witness}.
}
\]

## 14. Non-rules

```text
SAME_INFORMATION_CONTENT != SAME_EVIDENCE_TYPE
SAME_SEMANTIC_OBJECT != SAME_PROVENANCE
SAME_PROVENANCE != SAME_SEMANTIC_OBJECT
SAME_CARRIER != SAME_SEMANTICS
DIFFERENT_CARRIER != DIFFERENT_SEMANTICS
VERIFIED_PROVENANCE != SEMANTIC_EQUIVALENCE
SEMANTIC_EQUIVALENCE != EVIDENCE_TYPE_ADMISSION
EVIDENCE_TYPE_ADMISSION != AUTHORITY_TRANSPORT
SUCCESSFUL_PARSING != SEMANTIC_TRANSPORT
PREDICTIVE_ACCURACY != OBSERVATIONAL_CONSTITUTION
HIGH_CONFIDENCE_PROXY != ADMISSIBLE_TARGET_EVIDENCE
TRANSPORT_SUCCESS != BOUNDARY_SEMANTICS
TRANSPORT_SUCCESS != REPAIR_AUTHORITY
TRANSPORT_SUCCESS != FORMAL_TRANSITION_CALCULUS
PR61_FAILURE != RETROACTIVE_INVALIDATION_OF_PR59_OR_PR60
```

## 15. Maximum positive claim

Even if every later obligation passes, the maximum V0.1 promotion is bounded to:

```text
TRANSITION_SEMANTIC_TRANSPORT
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_CROSS_CARRIER_SUITE
```

Expanded only where separately earned:

```text
SEMANTIC_IDENTITY_PRESERVATION
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
SEMANTIC_SEPARATION
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
EVIDENCE_TYPE_LEGITIMACY
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
PROVENANCE_FACTOR_SEPARATION_AND_RECOVERABILITY
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
UNCERTAINTY_PRESERVATION
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_CONTROLS
```

Nothing in this object can establish universal carrier equivalence or arbitrary real-world semantic transport.

## 16. Authority ceiling

```text
PR59_CONSTRUCTED_SEPARABILITY
    = REMAINS_EARNED

PR60_TESTED_AXIS_TRANSPORT
    = REMAINS_EARNED

PR60_G2_OBSERVATION_CHANNEL_TRANSPORT
    = NOT_EVALUABLE_UNDER_FROZEN_BINDING

TRANSITION_SEMANTIC_TRANSPORT
    = NOT_YET_EVALUATED

UNIVERSAL_EVIDENCE_TYPE_EQUIVALENCE
    = NOT_ESTABLISHED

ARBITRARY_CHANNEL_TRANSPORT
    = NOT_ESTABLISHED

FOUR_COORDINATE_COMPLETENESS
    = NOT_ESTABLISHED

BOUNDARY_SEMANTICS
    = NOT_OPENED

BOUNDARY_RESPONSE
    = NOT_OPENED

BOUNDARY_REPAIR
    = NOT_OPENED

REPAIR_COMPOSABILITY
    = NOT_OPENED

FORMAL_TRANSITION_CALCULUS
    = NOT_CONSTITUTED

SSI_CALC_INSTRUMENTATION
    = NOT_CHANGED

SSI_CALC_KERNEL_DELTA
    = 0
```

## 17. Stage firewall

```text
SPEC            = FROZEN
CASES           = NOT_CONSTITUTED
BINDINGS        = NOT_CONSTITUTED
SEMANTIC_ORACLE = NOT_CONSTITUTED
PROTOCOL        = NOT_CONSTITUTED
EVALUATOR       = NOT_CONSTITUTED
RESULT          = NOT_CONSTITUTED
```

Next permitted stage:

```text
CASES
```

No CASES may be constructed from a later transport candidate. No BINDINGS may be constituted before CASES freeze. No oracle/protocol/evaluator/result may be back-propagated to repair an upstream frozen object.

---

> **First preserve the coordinate. Then prove the new carrier is entitled to carry it. Meaning may travel only through an evidence path that independently earns the right to transport it.**
