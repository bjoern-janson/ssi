# Architecture

## 1. Scientific object

Safe self-improvement is not defined as monotonic improvement in present score. The object is the evolution of a system's **corrective dynamics**: which future revisions remain reachable, what evidence can still distinguish them, what authority those distinctions may acquire, and which commitments preserve or destroy later correction.

The state object is

$$
\mathcal K_t=(R_t,\mathfrak C_t,\Lambda_t).
$$

- $R_t$: authoritative present representation/state.
- $\mathfrak C_t$: candidate corrective continuation space.
- $\Lambda_t$: lineage of collisions, failed transitions, provenance, and reopenable evidence.

For contract $P$ and horizon $h$,

$$
\mathfrak C_t=\operatorname{CorrCont}(R_t,P,h).
$$

Two systems can therefore satisfy

$$
R_t^A\approx R_t^B
$$

while differing materially in

$$
\mathcal K_t^A\neq\mathcal K_t^B
$$

because their reachable correction topology or preserved lineage differs.

## 2. Corrective-topology functional

Define

$$
\Phi_t=\Phi(\mathfrak C_t,\Lambda_t;P,h).
$$

$\Phi_t$ is deliberately not candidate count. It may include:

- **coverage** — which future obligations remain satisfiable;
- **reachability** — which successor states can still be reached;
- **reconfigurability** — whether current commitments can be released or transformed;
- **challengeability** — whether independent reality-contact can still alter confidence;
- **reopenability** — whether discarded alternatives can be recovered;
- **lineage** — whether the evidence required to diagnose earlier failure survives.

The synthetic ladder repeatedly falsified the shortcut

$$
|\mathfrak C_t|\approx \Phi_t.
$$

Future Sufficiency is about reachable corrective structure, not raw multiplicity.

## 3. Corrective pipeline

The current causal architecture is

$$
W
\rightarrow
O
\rightarrow
\widehat\Phi
\rightarrow
\mathcal E
\rightarrow
\mathrm{Auth}
\rightarrow
\mathrm{Select}
\rightarrow
\Gamma
\rightarrow
H_{\rm future}.
$$

Interpretation:

1. **$W$ — contact / collision witness.** Reality produces discrepancy, consequence, or constraint.
2. **$O$ — interface.** The system preserves or collapses distinctions exposed by contact.
3. **$\widehat\Phi$ — learned semantic map.** Relational structure is assigned predictive meaning for future transformability.
4. **$\mathcal E$ — evidential state.** Point estimates, uncertainty, grounding lineage, stability, and candidate margins remain available for warrant.
5. **$\mathrm{Auth}$ — authority allocation.** Evidence is translated into permission to commit, abstain, retain, revise, or reopen.
6. **$\mathrm{Select}$ — commitment operation.** A candidate is chosen, or selection is withheld.
7. **$\Gamma$ — reachable transition topology.** The selected commitment constrains which future states remain accessible.
8. **$H_{\rm future}$ — future adaptation / correction consequence.** The system later encounters demands not exhausted by its present state.

Upstream success never automatically licenses downstream success.

## 4. Three jurisdictions

### Future Sufficiency (FS)

Question:

> Does the current pipeline preserve the distinctions and reachable transformations still required for future correction?

FS is contract- and horizon-relative:

$$
FS_{P,h}(R_t).
$$

A currently adequate state can still be Future-Insufficient if it has consumed the transition topology needed for later authorized correction.

### Contradiction-Correction Architecture (CCA)

Question:

> What does the evidence actually warrant changing, preserving, distinguishing, or reopening?

CCA prevents failure signals from acquiring causal meaning automatically:

$$
\text{failure}\not\Rightarrow\text{cause identified}\not\Rightarrow\text{repair authorized}.
$$

### Controlled Adaptive Reasoning System (CARS)

Question:

> What authority may an evidence-supported distinction acquire and retain in commitment?

CARS prevents outcome success from laundering unjustified commitment into warrant:

$$
\text{correct outcome}\not\Rightarrow\text{correct authority}.
$$

## 5. Dual failure laws

### Premature merging

Let $O$ be an interface and $T_{\rm future}$ the downstream property on which correction depends.

A sufficient interface must satisfy

$$
\ker O\subseteq\ker T_{\rm future}.
$$

Violation:

$$
\ker O\not\subseteq\ker T_{\rm future}.
$$

Then there exist $x,y$ such that

$$
O(x)=O(y),
\qquad
T_{\rm future}(x)\neq T_{\rm future}(y).
$$

The interface has merged alternatives whose future corrective consequences remain distinct.

> **Do not merge what future correction still distinguishes.**

### Unauthorized splitting

Let $\mathcal E$ be the evidential state and $A$ the authority/commitment map.

A warranted authority map must not discriminate more finely than the evidence licenses:

$$
\ker\mathcal E\subseteq\ker A.
$$

Violation:

$$
\ker\mathcal E\not\subseteq\ker A.
$$

Then the commitment layer distinguishes alternatives that the evidence still treats as non-unique.

> **Do not distinguish in commitment what present evidence still merges.**

These are dual errors:

- **premature merge:** erase a distinction reality still requires;
- **unauthorized split:** manufacture a distinction the evidence has not earned.

## 6. Authority and STOP

The V0.8 authority rule is intentionally minimal:

$$
\operatorname{COMMIT}
\iff
|\operatorname{Top}(\mathcal E)|=1.
$$

Otherwise:

$$
\operatorname{STOP}.
$$

`STOP` is not defined as downstream success. It means only that unresolved candidate multiplicity is preserved rather than contracted without warrant.

This yields a testable distinction between:

- immediate decisiveness;
- epistemically correct authority allocation;
- future correction topology.

A system can guess correctly while violating authority. Conversely, a system can decline to commit now while preserving more future correction capacity.

## 7. Transition semantics

Selection changes not only the present state but the topology of reachable successors.

Write

$$
S_1\xRightarrow[P,E]{}S_2
$$

for a licensed transition under contract $P$ and evidence $E$, and

$$
\Gamma_P(S_1,E)=\{S_2:S_1\xRightarrow[P,E]{}S_2\}
$$

for the reachable successor set.

The key empirical separation is

$$
\text{present sufficiency}
\not\Rightarrow
\text{future transformability}.
$$

The selection operation and the interface supplied to it are therefore themselves Future-Sufficiency loci.

## 8. Governing invariant

> **No committed transformation may consume the evidential, representational, or authority pathway required to correct that transformation later.**

Operationally:

> **Preserve distinctions until their future consequences are exhausted; grant commitment authority only to the level the evidence identifies.**
