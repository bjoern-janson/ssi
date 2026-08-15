# Benchmark V0.1 — Design

## 1. Scientific question

The first independent benchmark tests one claim:

> Among systems matched on present capability and ordinary adaptability, does a preregistered difference in corrective topology predict a difference in adaptation to a future correction obligation that was unavailable during construction and matching?

Formally, construct $A$ and $B$ such that

$$
Q_{\rm state}^{A}\approx Q_{\rm state}^{B},
\qquad
Q_{\rm adapt}^{A}\approx Q_{\rm adapt}^{B},
$$

while obtaining a frozen structural contrast

$$
\Phi_A\neq\Phi_B.
$$

Then expose both systems to the same prospectively selected future obligation and evaluate

$$
\Delta Q_{\rm future}=Q_{\rm future}^{A}-Q_{\rm future}^{B}.
$$

The benchmark does **not** test CCA, Auth, or CARS as simultaneous treatment factors.

## 2. Independent test domain

V0.1 uses a **prospective versioned-configuration migration** task.

At construction time, both systems operate on the same current configuration/schema version and must satisfy the same present-task contract. After freeze, the first qualifying upstream configuration/schema change is disclosed. Both systems must adapt the frozen implementation to the new obligation under the same evidence, resources, and evaluation clock.

The future obligation must not be available during system construction, matching, topology measurement, or audit.

### First-qualifying-obligation rule

Before freeze, specify:

1. the upstream project or project cohort;
2. the construction cutoff commit/version;
3. the admissible change class;
4. exclusion criteria;
5. the prospective observation horizon;
6. the deterministic rule selecting the **first** qualifying post-freeze change.

No later change may replace the first qualifying change because it produces a cleaner or larger A/B difference.

## 3. A/B treatment construction

$A$ and $B$ must share the same present-task payload and ordinary adaptation machinery. The treatment difference is the structure of preserved corrective continuation topology.

The preferred treatment construction is:

- **A:** preserve the genuine typed dependency/alternative/provenance structure available at freeze;
- **B:** apply a preregistered topology-scrambling operation that preserves non-topological marginals required by the audit.

The scrambling operation must preserve, to the preregistered tolerances:

- total retained payload size;
- number of retained objects/candidates where candidate count is not itself the treatment;
- object type counts;
- storage/memory budget;
- compute budget;
- ordinary adaptation operator;
- access permissions;
- current-task information content;
- present-task score distribution.

The treatment may alter only the declared relational structure needed to create the frozen $\Phi$ contrast.

## 4. Frozen corrective-topology vector

$\Phi$ is a preregistered vector, not candidate count and not a post-hoc weighted utility:

$$
\boxed{
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
}
$$

### $C_{\rm cover}^{\rm pre}$ — prospective future coverage

Fraction or set-valued coverage of preregistered admissible correction classes reachable from the frozen state under the declared resource contract. This is measured **without using the realized future obligation**.

### $R_{\rm reconf}$ — reconfigurability

Ability to release, replace, or recombine current commitments under admissible pre-freeze surrogate changes without rebuilding the system from scratch.

### $C_{\rm challenge}$ — challengeability

Number/quality of independently grounded paths by which contradictory evidence can reduce confidence in or challenge the current representation/commitment.

### $A_{\rm preserve}$ — alternative preservation

Extent to which non-authoritative but still admissible alternatives remain recoverable rather than irreversibly collapsed.

### $L_{\rm prov}$ — lineage/provenance accessibility

Extent to which prior failed attempts, dependency lineage, evidence origin, and transformation history remain available for later diagnosis.

### $R_{\rm reopen}$ — authority reversibility / reopenability

Ability to reopen a previously non-selected route or reverse a current commitment when new evidence warrants revision.

Each component requires an executable measurement definition, admissible transformation class, missingness rule, and pre-freeze threshold/tolerance before authorization.

No component may be replaced, reweighted, or newly promoted because of the observed future result.

## 5. Present-state matching

$Q_{\rm state}$ must be frozen as a vector of current-capability measurements rather than a single convenient score. At minimum include:

- current contract success;
- calibration/error profile where applicable;
- latency/resource use;
- robustness to preregistered current-version perturbations;
- any task-specific capability measure that an adversarial reviewer could plausibly use to explain later adaptation.

The matching rule and tolerances are fixed before future disclosure.

## 6. Ordinary-adaptation matching

$Q_{\rm adapt}$ measures generic adaptation competence **without exposure to the future obligation**.

Use preregistered surrogate adaptation probes drawn from pre-freeze information only. Candidate dimensions include:

- adaptation success rate;
- update latency;
- update cost;
- collateral regression;
- sample/evidence efficiency.

The A/B comparison must satisfy preregistered equivalence margins, not merely fail to reach statistical significance.

## 7. Resource and information symmetry

At future disclosure, both systems receive:

- the same obligation;
- the same disclosure time;
- the same raw evidence and documentation;
- the same tool/API permissions;
- the same compute budget;
- the same memory/context/storage budget;
- the same adaptation/update budget;
- the same wall-clock or operation-count limit;
- the same evaluation mechanism.

Any unavoidable difference is entered in the confound ledger before authorization.

## 8. Confound ledger

Let $\mathcal H$ be the preregistered set of material rival explanations. Each rival receives exactly one disposition:

$$
\mathcal R:H_j\mapsto
\{
\texttt{BLOCKED},
\texttt{MEASURED},
\texttt{RANDOMIZED},
\texttt{RESIDUAL}
\}.
$$

The minimum ledger must include rival explanations based on:

- baseline capacity;
- information access;
- ordinary adaptability;
- current-task distribution;
- future-obligation distribution;
- resource allocation;
- implementation/path asymmetry;
- treatment-label leakage;
- selection/cherry-picking of the future event;
- differential stopping/time exposure;
- evaluator asymmetry;
- missingness/failure handling.

`RESIDUAL` is not automatically disqualifying. It becomes a run veto when a residual is simultaneously:

$$
\text{material}
\land
\text{unbounded}
\land
\text{capable of explaining the predicted effect}.
$$

The residual set $\mathcal H_{\rm residual}$ is frozen with the benchmark packet.

## 9. Hidden-treatment test

Before authorization, perform an adversarial label-inference audit:

> If A/B labels are hidden, can a reviewer or preregistered classifier infer treatment assignment from any construction artifact **other than the declared topology-treatment fields**?

Any successful inference route identifies a candidate hidden treatment. It must be removed, balanced, randomized, measured, or entered as a bounded residual before authorization.

This test does not require literal perfect indistinguishability. It requires that any material non-$\Phi$ distinguisher have a declared disposition.

## 10. Frozen evaluation rule

Before disclosure, freeze:

- primary endpoint(s);
- secondary endpoint(s);
- unit of analysis;
- equivalence margins for $Q_{\rm state}$ and $Q_{\rm adapt}$;
- confirmatory effect direction;
- uncertainty interval/test procedure;
- missingness and timeout rules;
- failure/abstention semantics;
- collateral-damage accounting;
- multiplicity handling, if needed;
- exclusion criteria;
- theory-update scope.

The first benchmark should keep endpoints separate rather than collapsing them into a convenience score.

Candidate future endpoints remain:

$$
H_{\rm recover},
\quad
T_{\rm recover},
\quad
C_{\rm revise},
\quad
R_{\rm collateral},
\quad
R_{\rm reopen},
\quad
\Delta V_{\rm future}.
$$

## 11. Freeze packet

The unit of scientific identity is

$$
\mathcal B_{\rm frozen}
=
\left(
\Phi_A,\Phi_B,
Q_{\rm state}^A,Q_{\rm state}^B,
Q_{\rm adapt}^A,Q_{\rm adapt}^B,
\mathcal H,\mathcal R,\mathcal H_{\rm residual},
O_{\rm future},
\mathcal E
\right).
$$

The packet must be content-addressed and timestamped before the qualifying future obligation is disclosed.

Required ordering:

$$
t_{\rm construct}
\le t_{\rm freeze}
< t_{\rm disclose}
\le t_{\rm outcome}.
$$

Within the confirmatory workflow:

$$
\frac{\partial\mathcal B_{\rm frozen}}
{\partial Y_{\rm future}}=0.
$$

## 12. Interpretation boundary

The preregistered confirmatory direction is

$$
\Phi_A-\Phi_B
\longrightarrow
Y_A-Y_B.
$$

The following move is prohibited:

$$
Y_A-Y_B
\longrightarrow
\text{retroactive redefinition, reweighting, or replacement of }\Phi.
$$

Outcome magnitude does not increase identification authority.

A large effect from an unauthorized or confounded shot is exploratory. A null result from an authorized, faithfully executed shot is a valid negative rebound.

## 13. Execution boundary

No `RUNNER.py` should be committed as the confirmatory runner until the construction audit issues an authorization certificate.

Authorization validates the design. After execution, result validity additionally requires faithful execution against the frozen packet:

$$
\boxed{
\text{valid confirmatory shot}
=
\text{authorized design}
+
\text{faithful execution}.
}
$$
