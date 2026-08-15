# SSI Energy Suite

This directory isolates the **Corrective Economy** work from the core SSI theory, benchmark lineage, and independent future-adaptation protocol.

## Scope boundary

The suite is intentionally additive-only.

- It does not redefine corrective topology $\Phi$.
- It does not make energy part of the definition of SSI.
- It does not modify the frozen V0.x lineage.
- It does not alter `ARCHITECTURE.md`, the main empirical protocol, or existing results.
- Energy claims are downstream consequence hypotheses and must earn authority independently.

The stable two-axis framing is

$$
\Phi
\longrightarrow
\begin{cases}
H_{\rm future} & \text{Axis I: Corrective Effectiveness},\\
E_{\rm horizon} & \text{Axis II: Corrective Economy}.
\end{cases}
$$

with

$$
\Phi\not\equiv H_{\rm future},
\qquad
\Phi\not\equiv E_{\rm horizon},
\qquad
H_{\rm future}\not\equiv E_{\rm horizon}.
$$

An energy reduction counts as an SSI efficiency gain only when correction quality remains admissible. Cheap failure is not corrective economy.

## Engineering principle

> **Make expensive thinking accumulate.**

Validated correction experience should become reusable structure when doing so lowers future correction cost after charging preservation and retrieval costs, without destroying the pathways required to detect and correct later mistakes.

The practical target is not minimum immediate compute. It is lower cost for the **same warranted correction**:

$$
J_{\rm corr}^{SSI}<J_{\rm corr}^{control}.
$$

## Energy accounting

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

Rediscovery is tracked as an attribution variable rather than automatically added as a disjoint term, to avoid double counting energy already charged to diagnosis, probing, revision, or recovery.

The accounting boundary must include any material infrastructure used by the treatment, including memory maintenance, retrieval, tool calls, adaptation, validation, and recovery.

## Experiment ladder

The lineage program currently has four rungs:

- **V0 — synthetic traversal economy:** supported in its frozen synthetic scope.
- **V1 — executed-work economy:** supported in its frozen executable CPU scope.
- **V2 — heterogeneous executed corrective-work economy:** supported in its frozen heterogeneous executable CPU scope.
- **V3 — measured physical energy:** **not run** because the current runtime does not expose a preregistration-admissible physical-energy boundary.

V3 explicitly forbids substituting CPU time or wall time for joules. `NOT_RUN_MEASUREMENT_BOUNDARY_NOT_IDENTIFIED` is neither support nor contradiction.

## First mechanism

The narrow causal test is the lineage intervention:

$$
A=\text{persistent validated correction lineage},
\qquad
B=\text{same system with lineage unavailable between episodes}.
$$

The hypothesized mechanism is

$$
\Lambda_{\rm preserved}
\overset{?}{\longrightarrow}
\text{less corrective traversal/work}
\overset{?}{\longrightarrow}
\text{lower lifecycle correction cost}.
$$

See [`LINEAGE_CORRECTIVE_ECONOMY.md`](LINEAGE_CORRECTIVE_ECONOMY.md) and `experiments/lineage_v*/` for the frozen protocols and adjudications.

## Failure discipline

Distinct outcomes remain distinct:

- lineage may be reused without producing gross savings;
- gross savings may fail to exceed lineage infrastructure cost;
- fewer candidates may still cost more when candidate work is heterogeneous;
- executable compute savings may fail to translate into physical energy savings;
- net savings may be purchased through worse correction quality and therefore be inadmissible;
- a null, failed, or nonidentified energy mechanism does not by itself falsify Axis I or SSI as a whole.

`NOT_IDENTIFIED` must remain distinct from zero and from a negative effect. Missing or nonidentified energy components are not to be silently imputed.

## Integration rule

Work in this directory should remain separable until an energy result earns broader authority. Changes to core SSI theory or architecture should be proposed independently rather than smuggled in through the energy suite.
