# Lineage Corrective Economy V0 — Results

## Adjudication

**SUPPORTED_IN_FROZEN_SYNTHETIC_SCOPE**

This result has authority only in the frozen synthetic compute-cost model. It is not a physical-energy result.

## Frozen sample

- Replicate worlds: 64
- Paired held-out episodes per world: 96
- Total paired correction episodes: 6144
- Missing / unidentified worlds: 0

## Primary results

Treatment A tested **1.522** candidate mechanisms per episode on average versus **6.525** for control B.

Mean correction cost:

- A: **11.566** synthetic compute units / episode
- B: **26.575** synthetic compute units / episode
- A − B: **-15.009**
- 95% world-bootstrap CI: **[-15.282, -14.737]**

Mean rediscovery attribution:

- A: **1.566**
- B: **16.575**
- A − B: **-15.009**
- 95% world-bootstrap CI: **[-15.282, -14.737]**

Across 96 held-out episodes, mean per-world gross lineage savings were **1440.891** units, lineage infrastructure cost was **134.160**, and net lineage economy was **1306.731**.

95% world-bootstrap CI for net savings:

**[1280.574, 1332.887]**

The amortization threshold was crossed in **64/64** worlds. Median $K^\star$ was **1** episode (IQR 1–1).

A was cheaper on **87.2%** of individual episodes, equal on **8.2%**, and more expensive on **4.6%**.

## Evidence ladder

- I. Reuse: **SUPPORTED**
- II. Gross economy: **SUPPORTED**
- III. Net economy: **SUPPORTED**
- IV. Admissible net economy: **SUPPORTED**

Correction-quality contract passed in every world: **True**.

Because correctness was deliberately fixed by an exact probe, V0 identifies only the lineage-to-search-cost mechanism. It does not test whether lineage improves correction quality.

## Stress gradient

The lineage advantage weakened as held-out signatures moved farther from prior lineage, which is the expected direction if savings are actually mediated by reusable similarity rather than a treatment-independent constant.

| Held-out bit-flip p | Mean candidates A | Mean candidates B | Mean J A−B | A cheaper | A more expensive |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 1.061 | 6.543 | -16.447 | 91.9% | 0.5% |
| 0.25 | 1.554 | 6.496 | -14.824 | 86.3% | 5.0% |
| 0.35 | 2.841 | 6.529 | -11.065 | 75.1% | 15.7% |

## Local interpretation

Within the frozen synthetic scope, validated persistent lineage reduced rediscovery/search traversal enough to exceed its own predefined formation, maintenance, and retrieval charges while preserving the exact same warranted correction endpoint.

The observed mechanism is therefore consistent with:

$$
\Lambda_{\rm preserved}
\rightarrow
E_{\rm rediscover}\downarrow
\rightarrow
J_{\rm corr}\downarrow
\rightarrow
N_\Lambda>0.
$$

## Authority boundary

This experiment does **not** establish that SSI reduces physical AI energy use. The costs are synthetic compute proxies and the exact probe deliberately fixes correction quality.

The earned update is local:

> In this frozen related-but-nonidentical mechanism-search environment, persistent validated correction lineage behaved as reusable infrastructure and reduced net correction-search cost.

The next experiment, if authorized, must replace at least one synthetic convenience—e.g. exact probes, hand-set phase costs, or symbolic lineage retrieval—with measured compute from an executable correcting agent. No SSI core update is licensed by V0 alone.
