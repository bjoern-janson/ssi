# Benchmark V0.1 — Construction Audit

## Status

```text
CONSTRUCTION_AUDIT = OPEN
A = PASS
B = NOT_EVALUATED
C = NOT_EVALUATED
D = NOT_EVALUATED
E = NOT_EVALUATED
F = NOT_EVALUATED
G = NOT_EVALUATED
H = NOT_EVALUATED
I = NOT_EVALUATED
FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
RUN = NOT_AUTHORIZED
```

> **Status note:** the block above is the specification-time initialization and is intentionally not rewritten by evidence collection. Current machine-readable adjudication is `AUDIT_STATUS.json`. The current A/B construction is blocked at predicate D; see `evidence/C_D_PRE_FREEZE_AUDIT.md`.

This document is part of the benchmark's scientific identity. It is not a narrative checklist. It defines the predicates that must be mechanically adjudicated before the confirmatory shot is authorized.

The governing adversarial question is:

> **Can an adversarial reviewer explain the predicted A/B future difference using anything other than the preregistered $\Phi$ contrast?**

Every material rival explanation must receive a declared disposition before authorization.

## 0. Allowed predicate states

Each predicate $P\in\{A,\ldots,I\}$ has exactly one state:

```text
NOT_EVALUATED
PASS
FAIL
```

A predicate may move from `NOT_EVALUATED` to `PASS` or `FAIL` only when its required evidence artifact is present and content-addressed.

A later change to any evidence artifact used by a passed predicate invalidates that predicate and returns it to `NOT_EVALUATED` until re-adjudicated.

No predicate may be waived because the expected or observed effect is large.

## Authorization-time information boundary

Predicates A–I are **authorization predicates**. Therefore their PASS conditions may depend only on information available no later than `t_freeze`.

A predicate must not require the realized post-freeze obligation, disclosure timestamp, or future outcome in order to authorize the shot. Realized-event conformance is evaluated later under **post-execution validity**.

Operationally:

```text
authorization evidence <= t_freeze
realized obligation / disclosure conformance > t_freeze
outcome evidence >= t_outcome
```

If an authorization predicate is written so that it can pass only after disclosure, the audit specification is internally invalid and must be minimally corrected before any shot can be authorized.

---

# A — Prospective scope and source freeze

## Purpose

Prevent future-event selection, construction-window leakage, and post-hoc choice of a favorable upstream change.

## Required frozen fields

- upstream project or project cohort;
- construction cutoff commit/version/date;
- admissible future-change class;
- exclusion criteria;
- prospective observation horizon;
- deterministic first-qualifying-obligation rule;
- prospective independence rule requiring the realized qualifying implementation to become public only after $t_{\rm freeze}$.

## Predicate

$$
A=1
\iff
\text{all scope fields and the prospective selector are fixed before }t_{\rm freeze}
$$

and the selector has no discretionary branch that can inspect A/B future outcomes or realized topology advantage.

## Mechanical PASS rule

`PASS` only if all required fields are non-null, their source artifacts are content-addressed, and the frozen rule mechanically determines which *future* event would qualify without requiring that event to have occurred yet.

Whether the realized event actually satisfies the frozen rule is a **post-disclosure execution-conformance check**. It cannot be used to create or repair authorization after the fact.

## Automatic FAIL conditions

- future obligation chosen after seeing A/B future performance;
- future obligation replaced because the first qualifying event was inconvenient;
- construction cutoff moved after inspecting post-cutoff information;
- exclusion applied only after seeing the realized A/B effect.

## Evidence record

```text
A_EVIDENCE = empirical/benchmark_v0_1/evidence/A_SCOPE_SOURCE.md
A_SHA256 = 3234728a690d8e5f2b6e3b806d1d4d174836c0e94232b479dd729029055add3a
A_ADJUDICATION = PASS
```

---

# B — Treatment and $\Phi$ identity freeze

## Purpose

Prevent outcome-driven treatment redefinition or post-hoc promotion/reweighting of topology dimensions.

## Required frozen fields

- exact A construction;
- exact B construction;
- topology-scrambling operator, if used;
- executable measurement definition for each $\Phi$ component;
- admissible transformation class for each component;
- missingness rule for each component;
- expected direction of the A/B topology contrast;
- rule specifying whether the confirmatory claim is component-wise, multivariate, or both.

Frozen vector:

$$
\Phi
=
\left(
C_{\rm cover}^{\rm pre},
R_{\rm reconf},
C_{\rm challenge},
A_{\rm preserve},
L_{\rm prov},
R_{\rm reopen}
\right).
$$

## Predicate

$$
B=1
\iff
\Phi_A,\Phi_B\text{ and all measurement operators are determined without }Y_{\rm future}.
$$

## Mechanical PASS rule

`PASS` only if every $\Phi$ component can be recomputed from frozen pre-disclosure artifacts and reproduces the recorded value within its preregistered numerical tolerance.

## Automatic FAIL conditions

- adding/removing a $\Phi$ dimension after future outcomes are known;
- changing weights because one component correlated with the result;
- replacing a failed topology measure with a more favorable post-hoc proxy;
- allowing realized future-obligation information into $C_{\rm cover}^{\rm pre}$.

## Evidence record

```text
B_EVIDENCE = empirical/benchmark_v0_1/evidence/B_CONSTRUCTION.md
B_STATE_A_SHA256 = 353113d6e93717d037f7de4d46e686423ec7cfb165fead77397561de0bedaa3f
B_STATE_B_SHA256 = 2952ada6d4a27acf05200097cc4b3b55161afae3afeecb6cd926ceef4555cb8a
B_PHI_SHA256 = 18d01e9262abb8f4e13caab0260f399a198a50b36c83d4896e5be66455d12b8e
B_ADJUDICATION = PASS
```

---

# C — Present-capability equivalence

## Purpose

Block the explanation that A was simply better before the treatment was tested prospectively.

## Required frozen fields

- $Q_{\rm state}$ vector;
- metric definitions;
- evaluation sample/support;
- equivalence margins or exact-match tolerances;
- uncertainty procedure;
- required subgroup/stratum checks;
- rule for handling any unmatched dimension.

## Predicate

$$
C=1
\iff
Q_{\rm state}^{A}\approx Q_{\rm state}^{B}
$$

under the preregistered equivalence rule.

## Mechanical PASS rule

Use equivalence or exact matching, not `p > 0.05` as evidence of equality. Every material preregistered current-capability dimension must fall within its frozen equivalence margin.

## Automatic FAIL conditions

- any material $Q_{\rm state}$ dimension exceeds its margin;
- matching is redefined after future disclosure;
- a current-capability measure is dropped because it disfavors equivalence.

## Evidence record

```text
C_EVIDENCE = empirical/benchmark_v0_1/evidence/C_D_PRE_FREEZE_AUDIT.md
C_AUDIT_SHA256 = 523fbe8211253b8d8c859322f4dda48272f6a6c5c74650746c037a0053e3f94d
C_ADJUDICATION = PASS
```

---

# D — Ordinary-adaptation equivalence

## Purpose

Block the explanation that A was already a better generic adapter independently of corrective topology.

## Required frozen fields

- $Q_{\rm adapt}$ vector;
- pre-freeze surrogate adaptation tasks;
- proof that surrogate tasks contain no information from the realized future obligation;
- adaptation success, latency, cost, collateral, and evidence-efficiency metrics as applicable;
- equivalence margins;
- uncertainty procedure.

## Predicate

$$
D=1
\iff
Q_{\rm adapt}^{A}\approx Q_{\rm adapt}^{B}
$$

under the preregistered equivalence rule and using pre-disclosure probes only.

## Mechanical PASS rule

All material ordinary-adaptation dimensions must satisfy their frozen equivalence margins.

## Automatic FAIL conditions

- surrogate adaptation probe contains the future obligation or a derivative of it;
- equivalence judged only by non-significance;
- A receives a stronger ordinary adaptation operator than B;
- margins are widened after seeing results.

## Evidence record

```text
D_EVIDENCE = empirical/benchmark_v0_1/evidence/C_D_PRE_FREEZE_AUDIT.md
D_AUDIT_SHA256 = 523fbe8211253b8d8c859322f4dda48272f6a6c5c74650746c037a0053e3f94d
D_ADJUDICATION = FAIL
D_REASON = A already outperforms B on exhaustive pre-freeze ordinary-adaptation surrogates
```

Because D fails, the current construction is blocked. E–I remain `NOT_EVALUATED`; they are not promoted merely to complete the checklist.

---

# E — Resource, information, and exposure symmetry

## Purpose
Block capacity, information-access, and differential-exposure explanations.

## Required frozen fields

For both A and B, record:

- model/runtime version;
- compute budget;
- memory/context/storage budget;
- tool/API permissions;
- pre-freeze training/construction data;
- future-disclosure evidence/documentation;
- adaptation/update budget;
- wall-clock or operation-count limit;
- evaluator access;
- stopping rule.

## Predicate

$$
E=1
\iff
\text{all non-treatment resources, information, and exposure are equal or within frozen tolerances.}
$$

## Mechanical PASS rule

A/B resource and information manifests must compare equal on all exact-match fields and fall inside tolerance on all quantitative fields not declared part of the treatment.

## Automatic FAIL conditions

- different future documentation or evidence;
- different compute/update budget;
- different evaluator or stopping rule;
- differential access created by implementation accident and left undisposed.

## Evidence record

```text
E_EVIDENCE = NOT_RECORDED
E_SHA256 = NOT_RECORDED
E_ADJUDICATION = NOT_EVALUATED
```

---

# F — Treatment isolation and hidden-asymmetry audit

## Purpose

Test whether A/B assignment can be inferred from undeclared implementation differences rather than the intended topology contrast.

## Required audit

Hide treatment labels and inspect all construction artifacts outside the declared topology-treatment fields.

At minimum perform:

1. deterministic manifest diff of code/config/resources;
2. normalized artifact comparison;
3. preregistered label-inference attempt using non-treatment fields only;
4. manual adversarial review of any remaining asymmetry.

## Predicate

$$
F=1
\iff
\text{every material non-}\Phi\text{ A/B distinguisher is eliminated or assigned a declared confound disposition.}
$$

## Mechanical PASS rule

`PASS` requires either:

- no material non-treatment distinguisher survives; or
- every surviving material distinguisher appears in $\mathcal H$ with a valid disposition under predicate H.

## Automatic FAIL conditions

- hidden treatment label can be recovered from a material undeclared implementation asymmetry;
- A/B code paths differ outside the declared treatment without a ledger entry;
- reviewer identifies an unrecorded asymmetry capable of explaining the predicted effect.

## Evidence record

```text
F_EVIDENCE = NOT_RECORDED
F_SHA256 = NOT_RECORDED
F_ADJUDICATION = NOT_EVALUATED
```

---

# G — Future-obligation independence and common-cause exposure

## Purpose

Ensure the future event is genuinely prospective and that A/B receive the same correction obligation.

## Required frozen fields

- first-qualifying-obligation rule from A;
- deterministic disclosure timestamp trigger;
- rule for constructing one common obligation identifier from the selected event;
- rule for constructing one common evidence bundle;
- common evaluation start condition;
- pre-disclosure access-control proof showing that neither A nor B can access post-cutoff obligation-specific information before the disclosure trigger.

## Predicate

$$
G=1
\iff
\text{the frozen disclosure mechanism guarantees}
\quad
O_{\rm future}^{A}=O_{\rm future}^{B}
$$

with identical evidence, timing, permissions, and evaluation start conditions once the prospective selector fires.

## Mechanical PASS rule

Before disclosure, the audit must be able to reproduce the disclosure mechanism from frozen artifacts and show that:

1. it consumes only the event selected by predicate A's frozen rule;
2. it emits one canonical obligation/evidence bundle to both arms;
3. all non-identifier bytes delivered to A and B are specified to hash identically;
4. the mechanism cannot inspect A/B future outcomes before selecting or packaging the event.

After disclosure, the realized event identifier, timestamps, and A/B bundle hashes are checked under **post-execution validity**. A mismatch invalidates the confirmatory result; it does not retroactively alter the pre-disclosure authorization certificate.

## Automatic FAIL conditions

- A and B receive different obligations;
- one arm receives earlier or richer disclosure;
- event is selected after outcome inspection;
- obligation was available during matching or $\Phi$ measurement.

## Evidence record

```text
G_EVIDENCE = NOT_RECORDED
G_SHA256 = NOT_RECORDED
G_ADJUDICATION = NOT_EVALUATED
```

---

# H — Confound-ledger completeness and residual-confound veto

## Purpose

Make the rival-explanation state part of the benchmark rather than an after-the-fact discussion.

## Mandatory rival set

$\mathcal H$ must include, at minimum:

```text
H_capacity
H_information
H_ordinary_adapt
H_current_distribution
H_future_distribution
H_resources
H_implementation
H_label_leakage
H_future_selection
H_differential_exposure
H_evaluator
H_missingness
```

Additional rivals identified during construction must be added **before freeze**.

Each $H_j$ receives exactly one disposition:

```text
BLOCKED
MEASURED
RANDOMIZED
RESIDUAL
```

For each rival, record:

- why it is or is not material;
- disposition;
- evidence artifact;
- quantitative bound if `MEASURED` or `RESIDUAL`;
- how large an A/B effect it could plausibly explain;
- whether it aligns with the preregistered effect direction.

## Residual veto

A residual rival vetoes authorization iff

$$
\boxed{
\text{Material}(H_j)
\land
\text{Unbounded}(H_j)
\land
\text{EffectExplaining}(H_j).
}
$$

`RESIDUAL` alone is not failure.

## Predicate

$$
H=1
\iff
\forall H_j\in\mathcal H,
\mathcal R(H_j)\text{ is declared}
$$

and no residual satisfies the veto condition.

## Mechanical PASS rule

`PASS` only if there are zero `UNCLASSIFIED` rivals and zero residual-veto rows.

## Confound-ledger template

| Rival | Material? | Disposition | Bound/evidence | Can explain predicted effect? | Veto? |
|---|---:|---|---|---:|---:|
| `H_capacity` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_information` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_ordinary_adapt` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_current_distribution` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_future_distribution` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_resources` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_implementation` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_label_leakage` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_future_selection` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_differential_exposure` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_evaluator` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |
| `H_missingness` | TBD | `UNCLASSIFIED` | TBD | TBD | TBD |

Frozen residual set:

```text
H_RESIDUAL = NOT_FROZEN
```

## Evidence record

```text
H_EVIDENCE = NOT_RECORDED
H_SHA256 = NOT_RECORDED
H_ADJUDICATION = NOT_EVALUATED
```

---

# I — Freeze-packet integrity and authorization certificate

## Purpose

Create the causal chain of custody and prohibit contamination between construction, authorization, and execution.

## Required packet

$$
\mathcal B_{\rm frozen}
=
\left(
\Phi_A,\Phi_B,
Q_{\rm state}^A,Q_{\rm state}^B,
Q_{\rm adapt}^A,Q_{\rm adapt}^B,
\mathcal H,\mathcal R,\mathcal H_{\rm residual},
O_{\rm future}^{\rm rule},
\mathcal E
\right).
$$

Here $O_{\rm future}^{\rm rule}$ is the frozen prospective obligation-selection and disclosure contract, not the unknown realized future event. The realized $O_{\rm future}$ is appended to the execution record only after disclosure.

$\mathcal E$ must include:

- primary and secondary endpoints;
- confirmatory effect direction;
- unit of analysis;
- uncertainty/test procedure;
- equivalence margins;
- multiplicity rule if needed;
- timeout/stopping rule;
- missingness rule;
- failure/abstention semantics;
- collateral accounting;
- exclusion rule;
- theory-update scope.

## Temporal invariant

$$
\boxed{
 t_{\rm construct}
 \le t_{\rm freeze}
 < t_{\rm disclose}
 \le t_{\rm outcome}
}
$$

Confirmatory immutability:

$$
\boxed{
\frac{\partial\mathcal B_{\rm frozen}}
{\partial Y_{\rm future}}=0.
}
$$

## Predicate

$$
I=1
\iff
A=B=C=D=E=F=G=H=1
$$

and the complete packet is content-addressed and timestamped before future disclosure.

## Mechanical PASS rule

`PASS` requires:

1. predicates A–H all equal `PASS`;
2. all packet members present;
3. packet digest recorded;
4. freeze timestamp recorded;
5. no qualifying future obligation disclosed before the freeze timestamp;
6. evaluation rule fully specified;
7. authorization certificate generated from the frozen packet digest.

## Automatic FAIL conditions

- any A–H predicate is not `PASS`;
- packet member changes after freeze without creating a new benchmark identity;
- evaluation rule remains discretionary at disclosure time;
- outcome-dependent modification occurs in the confirmatory workflow.

## Evidence record

```text
I_EVIDENCE = NOT_RECORDED
I_PACKET_SHA256 = NOT_RECORDED
I_FREEZE_TIMESTAMP = NOT_RECORDED
I_ADJUDICATION = NOT_EVALUATED
```

---

# Authorization rule

Authorization is not a judgment call at launch time.

$$
\boxed{
\texttt{AUTHORIZED}
\iff
A\land B\land C\land D\land E\land F\land G\land H\land I.
}
$$

Operationally:

```text
if any(A..I) != PASS:
    AUTHORIZATION_CERTIFICATE = NOT_ISSUED
    RUN = NOT_AUTHORIZED
else:
    AUTHORIZATION_CERTIFICATE = ISSUED
    RUN = AUTHORIZED
```

No effect size, anticipated effect size, or scientific excitement may override this gate.

## Authorization certificate template

```text
BENCHMARK_ID = independent-future-adaptation-v0.1
PACKET_SHA256 = <frozen digest>
FREEZE_TIMESTAMP_UTC = <timestamp>
A = PASS
B = PASS
C = PASS
D = PASS
E = PASS
F = PASS
G = PASS
H = PASS
I = PASS
H_RESIDUAL = <frozen residual set>
FUTURE_OBLIGATION_RULE_SHA256 = <digest>
EVALUATION_RULE_SHA256 = <digest>
AUTHORIZATION = AUTHORIZED
```

Until that certificate exists, the repository status remains:

```text
RUN = NOT_AUTHORIZED
```

---

# Post-execution validity

Authorization validity and result validity remain distinct.

After execution, a confirmatory result is valid only if execution faithfully realizes the frozen packet.

Faithful execution includes a post-disclosure conformance record showing that:

- the realized event is exactly the first qualifying event under predicate A's frozen selector;
- the event's relevant implementation first became public after `t_freeze` under A's independence rule;
- A and B received the same canonical obligation/evidence bundle;
- disclosure timestamps and evaluation start conditions satisfy predicate G's frozen mechanism;
- no frozen packet member was altered after observing the realized event or outcome.

$$
\boxed{
\text{valid confirmatory shot}
=
\text{authorized design}
+
\text{faithful execution}.
}
$$

A spectacular result from an unauthorized or non-faithful shot is exploratory evidence only.

A null result from an authorized and faithfully executed shot is a valid negative rebound.

> **Outcome magnitude does not increase identification authority.**