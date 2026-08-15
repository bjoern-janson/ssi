# Lineage Corrective Economy

## Status

First concrete SSI Axis-II experiment. This document isolates the energy/economy hypothesis from the core SSI architecture.

## 1. Question

Does preserved validated correction lineage reduce the lifecycle computational cost of reaching the same warranted correction on related-but-nonidentical held-out failures?

The treatment contrast is

$$
A=\Lambda_{\rm preserved},
\qquad
B=\Lambda_{\rm unavailable}.
$$

The intended causal mechanism is

$$
\Lambda_{\rm preserved}
\overset{?}{\longrightarrow}
E_{\rm rediscover}\downarrow
\overset{?}{\longrightarrow}
J_{\rm corr}\downarrow
\overset{?}{\longrightarrow}
N_\Lambda>0.
$$

Every arrow is independently falsifiable.

## 2. Matching and isolation

Before held-out correction episodes, treatment and control should be matched as closely as possible on

$$
Q_{\rm state},
\qquad
Q_{\rm adapt},
\qquad
E_{\rm baseline},
$$

and on any other present-state variable that could explain correction cost independently of lineage.

Both systems receive the same held-out challenge exposure. Challenges must be related enough for valid lineage transfer to be possible, but non-identical so that the treatment cannot succeed by simple replay.

The lineage treatment must not alter the acceptance criterion for a warranted correction.

## 3. Frozen correction-quality contract

Energy comparisons are not sufficient by themselves. A cheap failure is not an SSI efficiency gain.

Define the correction-quality vector

$$
\mathcal V_{\rm corr}
=
(
H_{\rm recover},
R_{\rm collateral},
R_{\rm reopen},
\mathrm{Auth}
).
$$

A preregistered acceptance contract should specify thresholds such as

$$
H_{\rm recover}\ge H_{\min},
$$

$$
R_{\rm collateral}\le R_{\max},
$$

$$
R_{\rm reopen}\ge R_{\min},
$$

and

$$
\mathrm{Auth}=1.
$$

Axis-II support requires corrective economy without compensating degradation in the frozen correction-quality outcomes.

## 4. Correction energy accounting

For correction episode $k$,

$$
E_k^{\rm corr}
=
E_{k,\rm detect}
+
E_{k,\rm diagnose}
+
E_{k,\rm probe}
+
E_{k,\rm revise}
+
E_{k,\rm validate}
+
E_{k,\rm recover}.
$$

Rediscovery is recorded separately as an attribution variable:

$$
E_{k,\rm rediscover}.
$$

It is not automatically added to $E_k^{\rm corr}$ if the same compute is already charged to diagnosis, probing, revision, validation, or recovery.

The full experimental accounting boundary must include any material treatment-specific infrastructure, including

- lineage storage and maintenance;
- lineage retrieval and indexing;
- inference compute;
- retrieval or tool compute;
- adaptation/update compute;
- validation compute;
- recovery/rollback compute.

Energy must not be made to disappear by outsourcing work outside the accounting boundary.

## 5. Primary corrective-economy contrast

Define

$$
\Delta J_{\rm corr}
=
J_{\rm corr}^{A}
-
J_{\rm corr}^{B}.
$$

The directional economy hypothesis is

$$
\mathbb E[\Delta J_{\rm corr}]<0,
$$

subject to the independently frozen correction-quality admissibility test.

The primary analysis must use a frozen rule for unsuccessful or non-recovered episodes rather than silently conditioning them away. One admissible construction is cost accumulated until warranted recovery or the frozen horizon $h$:

$$
J_{\rm corr}(k)
=
\sum_{\tau=0}^{\min(\tau_{\rm corr},h)}E_{k,\tau},
$$

with recovery reported separately:

$$
H_{\rm recover}(k)
=
\mathbf 1\{\tau_{\rm corr}\le h\}.
$$

For episodes in which both systems reach the same warranted endpoint, also report the paired mechanism contrast

$$
\Delta J_{\rm matched}
=
J_{\rm corr}^{A}
-
J_{\rm corr}^{B}.
$$

This paired contrast is interpretable as cost of reaching the same earned outcome, but it does not replace the full adjudication because conditioning on post-treatment success can introduce selection bias.

## 6. Lineage gross and net economy

Across $K$ correction episodes, define gross lineage savings

$$
G_\Lambda(K)
=
\sum_{k=1}^{K}
\left(
E_{k,\rm corr\mid\neg\Lambda}
-
E_{k,\rm corr\mid\Lambda}
\right).
$$

Define lineage infrastructure cost

$$
E_{\Lambda,\rm infrastructure}(K)
=
E_{\Lambda,\rm maintain}(K)
+
E_{\Lambda,\rm retrieve}(K)
$$

plus any other treatment-specific cost not already charged inside episode correction costs.

Net lineage economy is

$$
N_\Lambda(K)
=
G_\Lambda(K)
-
E_{\Lambda,\rm infrastructure}(K).
$$

The amortization crossover is

$$
K^\star
=
\min\{K:N_\Lambda(K)>0\}.
$$

A treatment may therefore be locally more expensive while becoming globally cheaper over the preregistered horizon.

## 7. Evidence ladder

The experiment distinguishes four increasingly strong claims.

### Reuse

$$
E_{\rm rediscover}^{A}
<
E_{\rm rediscover}^{B}.
$$

Evidence supports reuse of preserved lineage.

### Gross economy

$$
G_\Lambda(K)>0.
$$

Lineage reduces correction-episode cost before infrastructure charges.

### Net economy

$$
N_\Lambda(K)>0.
$$

Gross savings exceed lineage preservation/retrieval cost.

### Admissible net economy

$$
N_\Lambda(K)>0
\quad\land\quad
\mathcal V_{\rm corr}^{A}\not\prec\mathcal V_{\rm corr}^{B}.
$$

Only this level supports the full SSI corrective-economy mechanism.

## 8. Falsification and localization

The experiment should localize failures rather than collapse them.

- If $E_{\rm rediscover}^{A}\not<E_{\rm rediscover}^{B}$, the lineage-reuse mechanism is unsupported in scope.
- If reuse occurs but $G_\Lambda(K)\le0$, reuse did not create gross corrective economy.
- If $G_\Lambda(K)>0$ but $N_\Lambda(K)\le0$, infrastructure cost erased the gross benefit.
- If $N_\Lambda(K)>0$ but correction-quality constraints degrade, the energy gain is inadmissible as SSI efficiency.
- If the mechanism is `NOT_IDENTIFIED`, it must not be imputed as zero or negative.
- Failure of this Axis-II mechanism does not automatically falsify Axis I or SSI as a whole.

## 9. Required freeze before execution

Before measurement, freeze at minimum:

- treatment and control construction;
- lineage contents available to the treatment;
- challenge-generation and holdout procedure;
- related-but-nonidentical transfer criterion;
- matching variables and tolerances;
- correction-quality thresholds;
- energy accounting boundary;
- phase-level energy measurement instruments;
- rule for unsuccessful/non-recovered episodes;
- rediscovery attribution rule;
- infrastructure accounting rule;
- horizon $K$ and/or $h$;
- uncertainty and repeated-measures procedure;
- interpretation of `NOT_IDENTIFIED` and missingness;
- scope within which a positive result may update Axis II.

No post-hoc adjustment of the accounting boundary, correction criterion, or challenge set is permitted after observing treatment results.

## 10. Engineering principle

> **Make expensive thinking accumulate.**

Scientific qualification:

> Accumulation counts as corrective capital only when the reusable structure is warranted, accessible at acceptable cost, transfers to genuinely new correction demands, and remains itself future-correctable.
