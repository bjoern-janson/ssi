# SSI_RELICENSE_TRANSITION_INTERFACE_SEPARABILITY_V0.1

```text
STATUS = PROSPECTIVE_TRANSITION_INTERFACE_SEPARABILITY_SPEC_FROZEN__NO_CASES_NO_BINDINGS_NO_RESULT
OBJECT = SSI_RELICENSE_TRANSITION_INTERFACE_SEPARABILITY_V0.1
PARENT_OBJECT = SSI_RELICENSE_INTERACTION_FACTORED_EVIDENCE_INTERFACE_V0.1
PARENT_COMMIT = 506bfedd757c03b8cc5d9258701505ff5424380a
PARENT_STAGE = CASES_FROZEN
SSI_CALC_KERNEL_DELTA = 0
FORMAL_TRANSITION_CALCULUS = NOT_CONSTITUTED
BOUNDARY_SEMANTICS = NOT_CONSTITUTED
BOUNDARY_RESPONSE = NOT_OPENED
BOUNDARY_REPAIR = NOT_OPENED
AUTHORITY_MAPPING = NOT_OPENED
```

## 1. Scientific question

This object asks exactly one question:

> **Can a task-relative transition interface separately represent state, response law, validity, and authority without under-resolution, coordinate contamination, or forced certainty on a frozen constructed suite?**

The candidate dynamic object under test is:

\[
K_t^{\sigma,P}=(S_t,\mathcal L_t,\mathcal V_t,\Lambda_t)
\]

with:

- \(S_t\): current configuration;
- \(\mathcal L_t\): response / transformation law;
- \(\mathcal V_t\): constituted applicability / validity envelope;
- \(\Lambda_t\): authority envelope.

The experiment tests interface separability only.

It does **not** constitute boundary semantics, transition rules, repair rules, authority transport, composition, or SSI-CALC instrumentation.

## 2. Scope and operational typing

Within the frozen constructed scope:

\[
S_t\in\mathsf S_{\sigma,P}
\]

\[
E_t\in\mathsf E_{\sigma,P}
\]

\[
\mathcal L_t:\mathsf S\times\mathsf E\to 2^{\mathsf{Effect}}
\]

\[
\mathcal V_t\subseteq\mathsf S\times\mathsf E
\]

\[
\Lambda_t:\mathsf S\times\mathsf E\to 2^{\mathsf{Effect}}.
\]

The familiar execution distinction is preserved conceptually:

\[
R_t=\operatorname{Realizable}(\mathcal L_t,S_t,E_t)
\]

and, when the current situation is within the validity envelope,

\[
W_t=R_t\cap\Lambda_t(S_t,E_t).
\]

Any eventual actual effects would have to satisfy:

\[
A_t^{\rm actual}\subseteq W_t.
\]

These equations motivate the coordinate distinction only. This experiment does not test execution or authorize effects.

```text
CAN != MAY != DID
APPLICABLE != AUTHORIZED
```

## 3. Four-coordinate non-collapse claim under test

The proposed interface separation is:

\[
S\neq\mathcal L\neq\mathcal V\neq\Lambda.
\]

No coordinate change licenses inference of change in another coordinate.

Within the frozen constructed geometry, for coordinate \(i\in\{S,\mathcal L,\mathcal V,\Lambda\}\), the eventual candidate projection must satisfy, modulo independently constituted coordinate equivalence:

\[
\Delta K_i\neq0
\Rightarrow
\Delta q_i\neq0.
\]

For every orthogonal coordinate \(j\neq i\):

\[
\Delta K_j\neq0
\land
\Delta K_i=0
\Rightarrow
\Delta q_i=0.
\]

The cases are frozen before any \(\Phi_K\) or \(q_i\) is constituted.

## 4. Frozen case geometry requirement

CASES must instantiate one complete Cartesian hypercube:

\[
\mathcal W=
\{w_{slv\lambda}:s,l,v,\lambda\in\{0,1\}\}
\]

with:

\[
|\mathcal W|=16.
\]

Each bit corresponds to one independently constituted semantic variation.

Every pure edge changes exactly one coordinate while holding the other three semantic coordinates fixed.

Each of the four axes therefore has:

\[
2^{4-1}=8
\]

pure edges, for a total of:

\[
4\times8=32
\]

pure edges.

The hypercube is the adversary. The candidate representation may not participate in case construction.

```text
CASE_CONSTRUCTION = FUNCTION_OF_FROZEN_SPEC_ONLY
CASE_CONSTRUCTION != FUNCTION_OF_Phi_K
CASE_CONSTRUCTION != FUNCTION_OF_q_i
```

## 5. Adequacy obligations

### A1 — Relevant Separation

If a constituted coordinate changes, the corresponding projection must preserve the distinction:

\[
K_i(a)\not\equiv_i K_i(b)
\Rightarrow
q_i\Phi_K(a)\not\equiv_i^q q_i\Phi_K(b).
\]

Primary failure form:

```text
UNDER_RESOLUTION
```

### A2 — Orthogonal Invariance

If coordinate \(i\) is held fixed while an orthogonal coordinate \(j\) changes:

\[
K_i(a)\equiv_iK_i(b)
\land
K_j(a)\not\equiv_jK_j(b),
\]

then:

\[
q_i\Phi_K(a)\equiv_i^q q_i\Phi_K(b).
\]

Primary failure form:

```text
COORDINATE_CONTAMINATION
```

A change assigned to one downstream role may not masquerade as change in another role.

### A3 — Coordinate Recoverability

The candidate must support consistent reconstruction of all four constituted coordinates across the whole frozen cube:

\[
q_K(\Phi_K(w))
=
(\hat S,\hat{\mathcal L},\hat{\mathcal V},\hat\Lambda)
\]

with each recovered coordinate equivalent to the corresponding frozen world coordinate under the later frozen comparison semantics.

Pairwise discrimination alone is insufficient.

### A4 — Uncertainty Preservation

Controls outside the cube must test whether insufficient evidence remains insufficient.

```text
UNRESOLVED != NO_CHANGE
UNRESOLVED != SINGLE_COORDINATE_DIAGNOSIS
MULTI_COORDINATE_CANDIDATE_SET != SINGLE_COORDINATE_DIAGNOSIS
```

The representation must not manufacture a unique localization merely because a later output schema prefers one.

## 6. Counterfactual response-law requirement

A single realized output does not constitute law identity.

Frozen CASES must provide a prospectively specified perturbation family \(\Delta_{\rm probe}\) such that the two \(\mathcal L\) variants agree at the current input but differ under at least one frozen counterfactual probe:

\[
\mathcal L_0(S,E_{\rm current})
\equiv
\mathcal L_1(S,E_{\rm current})
\]

and:

\[
\exists\delta\in\Delta_{\rm probe}:
\mathcal L_0(S,\delta)
\not\equiv
\mathcal L_1(S,\delta).
\]

Frozen non-rule:

\[
\text{same current output}
\not\Rightarrow
\text{same response law}.
\]

The CASES representation must encode the response surface itself, not a convenient `LAW_0` / `LAW_1` label as bridge-visible evidence.

## 7. Validity / authority non-collapse requirement

The constructed worlds must independently constitute:

\[
(S,E)\notin\mathcal V
\]

separately from:

\[
(S,E)\in\mathcal V
\quad\land\quad
R(S,E)\nsubseteq\Lambda(S,E).
\]

These states may later share a superficial non-execution outcome, but the interface must not be given a pre-collapsed `DENIED` label.

Frozen non-rule:

```text
INAPPLICABLE != UNAUTHORIZED
```

A later collapse of these roles is a valid negative result.

It must not be repaired inside V0.1 after first-result evidence.

## 8. Case-stage semantic firewall

The CASES stage may establish only world semantics, frozen probe surfaces, coverage, and construction geometry.

The 16 cube worlds may include:

- current state facts;
- current evidence / context facts;
- frozen response observations under the prospectively specified probe family;
- constituted validity-envelope facts;
- constituted authority-envelope facts;
- explicit coverage metadata;
- non-bridge construction metadata needed to freeze the Cartesian geometry.

The uncertainty controls live outside the cube in the methodological sense:

\[
\mathcal U\perp\mathcal W.
\]

They test insufficient localization rather than add another cube coordinate.

The CASES stage must omit:

```text
Phi_K
q_S
q_L
q_V
q_LAMBDA
expected projections
expected diagnosis
oracle classification
boundary response
repair action
replacement law
```

## 9. Anti-cheating firewall for later BINDINGS

A later candidate mapping may consume only the frozen `bridge_visible` semantic surface of each world or control snapshot.

It may not consume:

- world IDs;
- binary construction bits;
- pair / edge IDs;
- Hamming distance;
- coordinate names used only by construction metadata;
- expected geometry;
- expected projection values;
- expected diagnoses;
- oracle classifications;
- intended runtime actions;
- hidden truth;
- timestamps, hashes, packet IDs, serialization order, or opaque identifiers whose inequality is not itself semantically constituted.

```text
case geometry != projection result
construction metadata != candidate evidence
```

## 10. Boundary between representation and runtime semantics

The experiment freezes this ordering:

\[
\text{representation of transition structure}
\prec
\text{boundary semantics}
\prec
\text{boundary response}
\prec
\text{repair authority}.
\]

Therefore:

```text
coordinate detectable != coordinate actionable
separability != boundary semantics
boundary semantics != boundary response
boundary response != repair authority
```

No later result in this experiment may cross that boundary without a separately constituted object.

## 11. Maximum positive claim

Even a perfect frozen-suite result may establish only:

```text
FOUR_COORDINATE_TRANSITION_INTERFACE_SEPARABILITY
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE

RELEVANT_SEPARATION
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE

ORTHOGONAL_INVARIANCE
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE

COORDINATE_RECOVERABILITY
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE

UNCERTAINTY_PRESERVATION
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_CONTROLS

MULTI_COORDINATE_IDENTIFIABILITY
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
```

It does not establish:

```text
FOUR_COORDINATE_COMPLETENESS
    = NOT_ESTABLISHED

REAL_WORLD_BOUNDARY_GENERALIZATION
    = NOT_ESTABLISHED

BOUNDARY_DETECTION_GENERALIZATION
    = NOT_ESTABLISHED

BOUNDARY_LOCALIZATION_GENERALIZATION
    = NOT_ESTABLISHED

BOUNDARY_REPAIR_SUFFICIENCY
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

## 12. Stage firewall

The only admissible lineage is:

```text
SPEC
  -> CASES
  -> BINDINGS
  -> DESCRIPTIVE_ORACLE
  -> PROTOCOL
  -> EVALUATOR
  -> FIRST_RESULT
```

Each stage freezes before the next is constituted.

At SPEC freeze:

```text
SPEC = FROZEN
CASES = NOT_CONSTITUTED
BINDINGS = NOT_CONSTITUTED
DESCRIPTIVE_ORACLE = NOT_CONSTITUTED
PROTOCOL = NOT_CONSTITUTED
EVALUATOR = NOT_CONSTITUTED
RESULT = NOT_CONSTITUTED
```

The governing falsification rule is:

> **Hold three constituted roles fixed. Change the fourth. The corresponding projection must change and orthogonal projections must remain invariant. If the evidence cannot localize the difference, that uncertainty must survive.**

No fifth coordinate is admitted in V0.1.
