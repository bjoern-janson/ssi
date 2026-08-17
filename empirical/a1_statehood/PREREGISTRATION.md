# A1 Corrective Statehood — Preregistration

## Status

**FROZEN SCIENTIFIC PREREGISTRATION BEFORE ANY A1 TREATMENT EXECUTION.**

This artifact freezes the A1 statehood claim before a downstream corrective-topology measurement is introduced.

The sole object under test is

\[
\boxed{\mathcal K_t=(R_t,\mathfrak C_t,\Lambda_t)}
\]

relative to a frozen future-corrective behavioral contract \(\mathcal B_{P,h}\).

This preregistration does **not** define, estimate, train, score, or test \(\Phi\). No corrective-topology scalar or measurement operator may enter A1 adjudication.

The scientific question is:

> **Does \(\mathcal K_t=(R_t,\mathfrak C_t,\Lambda_t)\) preserve future-corrective distinctions that \(R_t\) erases, while rendering additional remote history substantially less relevant?**

The authority hierarchy is frozen as

\[
\boxed{\mathrm{A1a/A1b}\succ\mathrm{A1c}.}
\]

Collision evidence dominates average predictive/information gain.

---

## 1. Frozen state objects

### Present authoritative state

\[
R_t
\]

is the current authoritative representation/commitment state at the freeze boundary.

Equality is exact under the canonical serialization defined by the executable A1 substrate. A pair is accepted as an \(R_t\)-match only if the canonical serialized objects are byte-identical and all frozen present-state validation outputs are identical.

### Corrective continuation space

\[
\mathfrak C_t=\operatorname{CorrCont}(R_t,P,h)
\]

is the frozen representation of admissible corrective continuations available from the present state under contract \(P\) and horizon \(h\).

For A1:

\[
\boxed{h=6\text{ corrective rounds}.}
\]

The executable substrate must define a canonical serialization of \(\mathfrak C_t\). Equality or inequality of \(\mathfrak C_t\) is decided **before** any held-out future challenge is sampled.

### Preserved lineage

\[
\Lambda_t
\]

is the preserved lineage available at the freeze boundary: collision witnesses, failed transitions, provenance, and reopenable evidence retained by the system.

The executable substrate must define a canonical serialization of \(\Lambda_t\). Equality or inequality is decided before future challenge sampling.

### Augmented candidate state

\[
\boxed{\mathcal K_t=(R_t,\mathfrak C_t,\Lambda_t).}
\]

Two systems are A1-\(\mathcal K\)-equivalent iff all three canonical components are exactly equal.

No downstream behavior is consulted when deciding \(R\)- or \(\mathcal K\)-equivalence.

---

## 2. Frozen behavioral semantics

For frozen policy/contract \(P\), horizon \(h=6\), and a held-out admissible challenge \(d\), define

\[
Y(d)=
\bigl(
H_{\rm recover},
T_{\rm recover},
R_{\rm reopen},
R_{\rm collateral},
C_{\rm revise}
\bigr).
\]

The components remain separate.

### \(H_{\rm recover}\)

Binary. \(1\) iff the system reaches a warranted acceptable corrective state within \(h\) rounds; otherwise \(0\).

### \(T_{\rm recover}\)

Integer number of corrective rounds to the first warranted acceptable recovery. Failure is encoded as \(h+1=7\).

### \(R_{\rm reopen}\)

For challenges in which reopening is applicable, binary. \(1\) iff the required previously inactive/discarded alternative can be reopened when warranted; otherwise \(0\). For challenge classes in which reopening is not applicable, the value is the explicit categorical token `NOT_APPLICABLE`.

### \(R_{\rm collateral}\)

Nonnegative integer count of previously valid commitments/structures made invalid unnecessarily by the corrective response under the frozen challenge contract.

### \(C_{\rm revise}\)

Nonnegative integer count of state-changing revision operations executed before recovery or horizon exhaustion. Diagnostic observations/probes that do not change the committed state are not counted as revision operations.

### Behavioral map

For the complete held-out challenge set \(\mathcal D_{\rm holdout}\),

\[
\mathcal B_{P,h}(s)
=
\{d\mapsto Y_s(d):d\in\mathcal D_{\rm holdout}\}.
\]

---

## 3. Preregistered behavioral equivalence

Because A1 uses exact discrete synthetic/executable endpoints, all component tolerances are frozen to zero:

\[
\epsilon_j=0\qquad\forall j.
\]

For one challenge,

\[
Y_1(d)\sim_Y Y_2(d)
\iff
\bigwedge_j Y_{1j}(d)=Y_{2j}(d).
\]

For complete behavioral maps,

\[
\boxed{
\mathcal B_1\sim_Y\mathcal B_2
\iff
Y_1(d)\sim_Y Y_2(d)
\quad\forall d\in\mathcal D_{\rm holdout}.
}
\]

A **behavioral collision witness** occurs when two states that are equal under the representation being tested are non-equivalent under \(\mathcal B_{P,h}\).

No post-hoc tolerance widening is permitted.

---

## 4. Experimental unit: matched four-history world

A1 uses independent replicate worlds. Each identified world contains a four-system matched quartet indexed only for generator bookkeeping by

\[
u\in\{0,1\},\qquad v\in\{0,1\}.
\]

These labels are not new theoretical variables.

The quartet is constructed so that

\[
R_{0,0}=R_{0,1}=R_{1,0}=R_{1,1},
\]

while

\[
\mathcal K_{0,0}=\mathcal K_{0,1}=\mathcal K^{(0)},
\]

\[
\mathcal K_{1,0}=\mathcal K_{1,1}=\mathcal K^{(1)},
\]

and

\[
\boxed{\mathcal K^{(0)}\neq\mathcal K^{(1)}.}
\]

Within each \(u\)-level, the two remote histories must be genuinely different:

\[
H_{u,0;<t}\neq H_{u,1;<t},
\]

while ending in exactly the same candidate state:

\[
\boxed{\mathcal K_{u,0}=\mathcal K_{u,1}.}
\]

Thus each world simultaneously contains:

1. an \(R_t\)-collision opportunity with different \(\mathcal K_t\) values; and
2. a \(\mathcal K_t\)-collision opportunity with different remote histories.

All equality/difference gates are checked before any held-out challenge instance is generated.

---

## 5. A1a — present-state insufficiency collision test

### Structural contrast

For matched remote-history index \(v\), compare

\[
(R_{0,v},\mathcal K_{0,v})
\quad\text{vs}\quad
(R_{1,v},\mathcal K_{1,v}),
\]

with

\[
R_{0,v}=R_{1,v},
\qquad
\mathcal K_{0,v}\neq\mathcal K_{1,v}.
\]

A challenge-level A1a collision occurs iff

\[
\boxed{
R_{0,v}=R_{1,v}
\land
Y_{0,v}(d)\not\sim_Y Y_{1,v}(d).
}
\]

A world-level A1a collision occurs iff at least one of its two matched-\(v\) contrasts produces at least one held-out challenge collision.

### Kernel interpretation

A validated A1a collision is a direct witness that

\[
\boxed{
\ker R_t\not\subseteq\ker\mathcal B_{P,h}.
}
\]

and therefore that present authoritative state alone is insufficient for the frozen future-corrective behavior contract.

### Frozen \(\mathcal K\)-contrast strata

The 192 worlds are balanced across three preregistered construction strata:

- **64 \(\mathfrak C\)-only worlds:** \(\Lambda^{(0)}=\Lambda^{(1)}\) and \(\mathfrak C^{(0)}\neq\mathfrak C^{(1)}\);
- **64 \(\Lambda\)-only worlds:** \(\mathfrak C^{(0)}=\mathfrak C^{(1)}\) and \(\Lambda^{(0)}\neq\Lambda^{(1)}\);
- **64 joint worlds:** both \(\mathfrak C\) and \(\Lambda\) differ.

The aggregate A1a adjudication is primary. Stratum-specific results are localization diagnostics and may not override the aggregate adjudication.

### A1a support rule

`A1A_R_STATE_INSUFFICIENCY_SUPPORTED` iff:

1. A1a collisions occur in at least **two independent worlds**;
2. those witnesses involve at least **two independently generated held-out challenge instances**; and
3. the lower endpoint of the 95% confidence interval for the world-level A1a collision probability is strictly above zero.

One isolated world-level collision is `A1A_SINGLE_COLLISION_INCONCLUSIVE` until independently reproduced.

Zero validated collisions is `A1A_R_STATE_INSUFFICIENCY_NOT_SUPPORTED_IN_FROZEN_SCOPE`.

---

## 6. A1b — augmented-state collision test

### Structural contrast

Within each \(u\)-level, compare histories

\[
H_{u,0;<t}\neq H_{u,1;<t}
\]

that have been verified before holdout sampling to satisfy

\[
\boxed{
\mathcal K_{u,0}=\mathcal K_{u,1}.
}
\]

A challenge-level A1b collision occurs iff

\[
\boxed{
\mathcal K_{u,0}=\mathcal K_{u,1}
\land
Y_{u,0}(d)\not\sim_Y Y_{u,1}(d).
}
\]

A world-level A1b collision occurs iff either \(u\)-level produces at least one held-out challenge collision.

### How \(\mathcal K\)-equivalent histories are generated

The executable substrate may construct distinct histories by:

- permuting the order of pre-freeze historical events;
- using different surface realizations of structurally equivalent events;
- inserting additional pre-freeze events that are **\(\mathcal K\)-null at the freeze boundary**; or
- using distinct pre-freeze paths that converge to the same canonical \((R_t,\mathfrak C_t,\Lambda_t)\).

A `K-null` event is defined operationally only by the fact that the final canonical \(\mathcal K_t\) is unchanged. It is **not** assumed to be behaviorally irrelevant.

This is intentional: A1b tests whether the candidate state projection has erased future-relevant path dependence.

History pairs are accepted using only pre-freeze history and state information. Future outcomes may never be used to search for, reject, or regenerate a pair.

### Kernel interpretation

A validated A1b collision is a direct witness that

\[
\boxed{
\ker\mathcal K_t\not\subseteq\ker\mathcal B_{P,h}.
}
\]

within the frozen scope.

### A1b finite-scope criterion

Finite testing cannot establish universal kernel inclusion. A1b therefore tests an explicitly approximate candidate-state claim in the frozen challenge family.

Let \(\rho_K\) be the world-level A1b collision probability. Freeze

\[
\boxed{\delta_K=0.05.}
\]

A1b outcomes are adjudicated as follows:

- **0 world-level A1b collisions** and a one-sided 95% upper confidence bound \(\le0.05\): `A1B_CANDIDATE_STATE_SUFFICIENCY_SUPPORTED_IN_FROZEN_SCOPE`.
- **1 world-level A1b collision:** `A1B_SINGLE_K_COLLISION_INCONCLUSIVE`; no statehood support is licensed.
- **2 or more independent world-level A1b collisions:** `A1B_K_STATE_INSUFFICIENT_IN_FROZEN_SCOPE`.

No average predictive improvement can rescue the last two outcomes.

---

## 7. A1c — graded residual-history reduction

The preregistered quantity is

\[
\boxed{
\Delta I_H
=
I(H_{<t};Y\mid R_t)
-
I(H_{<t};Y\mid\mathcal K_t).
}
\]

Because \(\mathcal K_t\) is a deterministic function of the frozen history and contains \(R_t\) as a component,

\[
\boxed{
\Delta I_H
=
I(\mathcal K_t;Y\mid R_t).
}
\]

This identity is used only to estimate the already-preregistered augmentation gain; it does not convert A1c into a structural sufficiency test.

### Outcome code for A1c

For information estimation only, the exact endpoint tuple

\[
Y^\star
=
(H_{\rm recover},T_{\rm recover},R_{\rm reopen},R_{\rm collateral},C_{\rm revise})
\]

is treated as one finite categorical outcome. The individual endpoint results remain separately reported and retain independent interpretive authority.

### Estimator

Within each world, the held-out challenge distribution is exactly balanced across all four systems. A1c uses the plug-in conditional mutual information between canonical \(\mathcal K\)-class and \(Y^\star\) given the matched \(R_t\), with Miller–Madow entropy correction.

The primary A1c estimand is the mean world-level corrected \(\Delta I_H\), in bits.

A1c is supported iff:

1. the mean corrected \(\Delta I_H>0\);
2. the lower endpoint of the 95% paired world-bootstrap interval is strictly above zero; and
3. a preregistered within-world label-randomization test gives \(p<0.01\).

The randomization null preserves the two-versus-two \(\mathcal K\)-class count inside each world/challenge while breaking its association with behavioral outcome.

A1c is a graded companion only:

\[
\boxed{
\Delta I_H>0
\not\Rightarrow
\text{state sufficiency}.
}
\]

---

## 8. Held-out future challenge family

No concrete future challenge instance is generated until the complete four-history world has passed all pre-freeze matching/equality gates.

The frozen family contains **32 held-out challenges per world**, eight from each of four previously specified SSI future-adaptation classes:

1. **requirement change** — a previously unannounced requirement changes what counts as an acceptable correction;
2. **reopening demand** — later evidence makes a previously inactive/discarded alternative relevant again;
3. **independent contradiction** — a challenge channel not used to establish the present commitment contradicts a currently relied-on distinction or shortcut;
4. **interface/constraint shift** — a previously unannounced constraint invalidates a current route while preserving the underlying task semantics.

The structural family is known before freeze; the concrete targets, surface realizations, and challenge parameters are sampled only afterward from independent held-out randomness.

No concrete held-out challenge may be:

- replayed from a pre-freeze historical event;
- selected based on which \(\mathcal K\)-variant appears stronger;
- replaced after observing treatment behavior; or
- used to construct, match, reject, or refine a history quartet.

The exact same 32 challenges, in the same canonical order, are applied to all four systems in an identified world.

Syntactically invalid challenge draws may be rejected only by a frozen validity predicate that does not execute any member of the quartet and does not inspect its future behavior.

---

## 9. Sample size, seeds, and inference unit

Frozen design:

- independent worlds: **192**;
- systems/history realizations per world: **4**;
- held-out challenges per world: **32**;
- challenge classes: **4**, with **8** instances/class/world;
- maximum corrective horizon: **6** rounds;
- primary inference unit: **world**;
- bootstrap resamples: **20,000** worlds with replacement.

Frozen seeds:

```text
WORLD_MASTER_SEED      = 20260827
HOLDOUT_CHALLENGE_SEED = 20260828
BOOTSTRAP_SEED         = 20260829
RANDOMIZATION_SEED     = 20260830
```

Worlds, not individual challenge episodes, are the inferential units because four histories and 32 challenges are dependent within world.

Primary confidence intervals are percentile 95% world-bootstrap intervals unless A1b explicitly calls for a one-sided binomial upper bound.

For \(\rho_K\), use the exact one-sided 95% Clopper–Pearson upper confidence bound.

---

## 10. Construction gates and missingness

A world is identified only if, before holdout generation:

1. all four present authoritative states are exactly equal;
2. all four frozen present-state validation outputs are exactly equal;
3. \(\mathcal K^{(0)}\neq\mathcal K^{(1)}\);
4. each within-\(u\) history pair is genuinely different;
5. each within-\(u\) pair has exactly equal canonical \(\mathcal K_t\);
6. the world satisfies its preregistered \(\mathfrak C\)-only, \(\Lambda\)-only, or joint stratum definition.

Construction rejection/regeneration is allowed only before held-out challenge generation and only on these frozen gates.

No post-outcome regeneration is permitted.

No imputation.

`NOT_IDENTIFIED` is distinct from zero and from a negative result.

If fewer than **180 of 192 worlds** are identified and fully executed, A1 as a whole is

```text
NOT_IDENTIFIED_IN_FROZEN_A1_SCOPE
```

and no structural or information conclusion is promoted.

All construction failure rates and reasons must be reported.

---

## 11. Frozen adjudication hierarchy

A1 is component-adjudicated first.

### A1a

Tests whether \(R_t\) erases future-corrective distinctions:

\[
\ker R_t\overset{?}{\subseteq}\ker\mathcal B_{P,h}.
\]

### A1b

Tests whether the proposed augmentation still erases future-corrective distinctions:

\[
\ker\mathcal K_t\overset{?}{\subseteq}\ker\mathcal B_{P,h}.
\]

### A1c

Tests whether the augmentation removes graded residual history dependence:

\[
\Delta I_H>0\;?
\]

### Final supported candidate-state claim

The final status

```text
SUPPORTED_CANDIDATE_CORRECTIVE_STATE_IN_FROZEN_A1_SCOPE
```

requires all of:

1. `A1A_R_STATE_INSUFFICIENCY_SUPPORTED`;
2. `A1B_CANDIDATE_STATE_SUFFICIENCY_SUPPORTED_IN_FROZEN_SCOPE`;
3. `A1C_RESIDUAL_HISTORY_REDUCTION_SUPPORTED`.

If A1a and A1c pass but A1b yields two or more independent \(\mathcal K\)-collisions, the required adjudication is

```text
PREDICTIVELY_IMPROVED_BUT_STRUCTURALLY_INSUFFICIENT
```

and no statehood claim is licensed.

If A1b yields one collision, the final A1 statehood status remains inconclusive regardless of A1c.

A1a/A1b collision evidence always dominates A1c.

---

## 12. Licensed interpretation of a positive A1 result

If all frozen gates pass, the strongest licensed statement is:

> **Within the frozen A1 executable environment, contract, horizon, and held-out challenge family, \(\mathcal K_t=(R_t,\mathfrak C_t,\Lambda_t)\) is an empirically supported candidate corrective-state representation: it preserves future-corrective distinctions that present authoritative state alone erases, no \(\mathcal K\)-equivalent remote-history collision was detected above the preregistered finite-scope tolerance, and the augmentation reduces residual history dependence.**

This does **not** establish:

- universal or exact Markov sufficiency;
- that \(\mathcal K_t\) is the unique or minimal state representation;
- causal effects of corrective topology itself;
- that a particular \(\Phi\) is valid;
- that any scalar compression of \(\mathcal K_t\) is licensed;
- independent cross-domain future-adaptation prediction;
- Axis II / physical energy claims; or
- SSI core theory as a whole.

---

## 13. Failure interpretation

A1 failures localize rather than globally falsify SSI.

### A1a fails

If no replicated \(R_t\)-collision is established, then this experiment has not shown that \(R_t\) is insufficient under the frozen challenge family.

### A1b fails

If replicated \(\mathcal K_t\)-collisions occur, then the current candidate state representation is structurally insufficient in the frozen scope. The collision lineage must be preserved before any revision to the state object is proposed.

### A1c fails

If \(\Delta I_H\) is not reliably positive while A1a/A1b do not otherwise fail, then graded incremental information gain has not been established. Structural collision results retain their own authority.

No failure may be attributed to a deeper SSI claim until its locus is independently established.

---

## 14. Freeze firewall

The causal ordering is immutable:

\[
\boxed{
H_{<t}
\rightarrow
(R_t,\mathfrak C_t,\Lambda_t)
\rightarrow
\texttt{FREEZE}
\rightarrow
\mathcal D_{\rm holdout}
\rightarrow
\mathcal B_{P,h}
\rightarrow
\mathrm{A1a/A1b/A1c}.
}
\]

Prohibited before A1 adjudication:

- defining or fitting \(\mathcal M_\Phi\);
- scoring systems with \(\Phi\);
- choosing future challenges from observed state differences;
- changing \(\mathcal K_t\) after seeing held-out behavior;
- changing endpoint tolerances after seeing collisions;
- collapsing the outcome vector into a favorable scalar;
- treating A1c predictive gain as a substitute for A1b;
- post-hoc subgroup rescue of a failed aggregate gate.

Only after A1 earns the status

```text
SUPPORTED_CANDIDATE_CORRECTIVE_STATE_IN_FROZEN_A1_SCOPE
```

may the next branch ask whether a frozen measurement operator

\[
\mathcal M_\Phi:\mathcal K_t\rightarrow\phi_t
\]

preserves the downstream behavioral distinctions established here.

---

## 15. Execution authorization

This file freezes the **scientific design**.

A1 treatment execution is not authorized until the executable substrate and runner are committed on this branch and demonstrate, without using held-out outcomes, that they implement:

- the exact canonical equality gates above;
- the 192-world four-history construction;
- the three 64-world \(\mathcal K\)-contrast strata;
- the frozen 32-challenge holdout generator;
- the exact endpoint semantics and zero-tolerance equivalence relation;
- the frozen seeds and inference procedures; and
- the prohibition on any \(\Phi\)-based quantity.

Implementation details may instantiate this preregistration but may not change its scientific objects, contrasts, endpoints, thresholds, sample sizes, challenge classes, or adjudication rules.
