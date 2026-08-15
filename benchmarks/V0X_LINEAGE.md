# V0.x Benchmark Lineage

This file preserves the scientific lineage of the synthetic benchmark program. Negative results are part of the lineage and must not be rewritten as successful intermediate steps.

## V0.1 — Generative probe mechanism unit test

**Question:** can preserved failure/contact generate a missing discriminating probe?

Result: treatment generated the target functional novelty while matched controls did not.

Adjudication:

```text
V0.1 = MECHANISM_UNIT_TEST_PASS
```

Boundary: mechanism unit test only; not general interface invention.

---

## V0.2 — Ambiguous witnesses

**Question:** does probe generation survive noisy/ambiguous witnesses?

Treatment exceeded controls, but shortcuts remained and the result was only partial.

Adjudication:

```text
V0.2 = G1_PARTIAL_PASS
```

Boundary: interface correction remained easier than genuine interface discovery.

---

## V0.3 — Novelty / generalization separation

Separated novelty $N$ from held-out collision generalization $H$ and fresh usefulness $V$.

The construction succeeded at separating $N$ from $H$, but $H$ and $V$ still collapsed in the observed evaluations.

Adjudication: strong G1 partial pass; $H/V$ separation not established.

---

## V0.4 — Fresh usefulness veto

Constructed same-world stable-useful and stable-only probes with

$$
N_s=N_u=1,
\qquad
H_s=H_u=1,
\qquad
V_s<\tau<V_u.
$$

Hence

$$
N\land H\not\Rightarrow V.
$$

Adjudications:

```text
V0.4_H/V_FACTORIZATION = PASS
V0.4_FRESH_VETO        = PASS
```

Boundary: preserving both alternatives was built into the treatment construction; cardinality inference was not tested.

---

## V0.5 — Candidate-set sufficiency

Defined candidate-set future coverage and an oracle minimum sufficient size $m^\star$.

Important asymmetry: $m^\star$ is an after-future oracle lower bound, not a normative pre-future retention target.

Main result: structured collision evidence strongly improved preservation of future corrective routes relative to matched scrambling and aggressive fixed contraction.

But conservative retention remained competitive/perfect.

Adjudications:

```text
V0.5_STRUCTURED_FUTURE_ROUTE_PRESERVATION = PASS
V0.5_ADAPTIVE_CONTRACTION_SUPERIORITY     = NOT_ESTABLISHED
```

This negative result blocked the shortcut "Future Sufficiency = retain fewer candidates cleverly."

---

## V0.6a — Resource-bounded Future Sufficiency

Introduced a hard capacity budget.

Treatment strongly beat scrambling, random feasible retention, and an undersized fixed policy. But a simple max-budget policy achieved perfect Future Sufficiency.

Key result:

$$
FS_B(K_3)=1>FS_B(T).
$$

Therefore:

$$
\text{capacity feasibility}
\neq
\text{capacity opportunity cost}
\neq
\text{future sufficiency}.
$$

Adjudications:

```text
V0.6a_RESOURCE_BOUNDED_FS             = PASS
V0.6a_ADAPTIVE_RETENTION_SUPERIORITY  = NOT_ESTABLISHED
```

The preferred adaptive policy was falsified by a simpler max-budget policy.

---

## V0.6b — Transition-level Future Sufficiency

Moved the object from present state to reachable successor topology.

Constructed states that were equally present-sufficient and equal-cost while differing in whether current commitments left a releasable route for later independently constituted obligations.

Established:

$$
\text{present sufficiency}
+
\text{resource feasibility}
\not\Rightarrow
\text{future transformability}.
$$

Adjudication:

```text
V0.6b_TRANSITION_FS = STRONG_PARTIAL_PASS
```

Boundary: adaptive treatment success still partly collapsed with latent-pair identification; independent transition selection was not yet established.

---

## V0.6c — Selection-level Future Sufficiency

Held present sufficiency, cost, and current valid count fixed across candidate commitments while varying future transition breadth.

Treatment used structured collision evidence to select more transformable commitments.

Primary result:

$$
\Delta TFS^{T-C}=+0.680.
$$

Adjudication:

```text
V0.6c_FS_SELECT = PASS
```

Licensed statement:

> When present sufficiency and current resource cost are held fixed, structured reality-contact can causally improve selection of commitments that preserve more of the reachable topology of later authorized correction.

Boundary: evidence strength remained monotonically tied to transition breadth.

---

## V0.6d — Topological selection under scalar equivalence

All candidates were exactly equivalent under the frozen scalar evidence interface while differing in future transition topology.

Scientific run:

$$
TFS_T=0.930,
\qquad
TFS_S=0.239\approx\frac14.
$$

Primary contrasts:

$$
\Delta TFS^{T-C}=+0.673,
\qquad
\Delta TFS^{T-S}=+0.691.
$$

Established operationally:

$$
\ker O_{\rm scalar}\not\subseteq\ker T_{\rm transition}.
$$

Adjudications:

```text
V0.6d_SCALAR_INTERFACE_INSUFFICIENCY = PASS
V0.6d_RELATIONAL_INTERFACE_SUFFICIENCY = PASS
```

Boundary:

```text
RELATIONAL_SEMANTICS_DISCOVERY = NOT_ESTABLISHED
```

---

## V0.7 — Relational semantics acquisition

Removed the hard-coded relational-motif-to-transition mapping.

The learner received independently grounded training cases, learned

$$
\widehat\Phi:\mathcal G_W\rightarrow T_{\rm transition},
$$

froze that mapping, and transferred it to held-out raw-novel surface realizations.

Scientific run:

$$
TFS_T=0.947,
\qquad
TFS_C=0.230,
\qquad
TFS_M=0.250,
\qquad
TFS_S=0.250,
\qquad
TFS_R=0.257.
$$

Primary:

$$
\Delta TFS^{T-C}=+0.717,
\qquad
\Delta R_{\rm trans}^{T-C}=+0.487.
$$

The anti-memorization dissociation was especially important:

$$
RMSE_{\rm train,M}=0,
\qquad
TFS_M=0.250,
$$

while the invariant semantic learner had worse training fit but

$$
TFS_T=0.947.
$$

Licensed claim:

> Within the frozen relational construction, independently grounded consequences can teach an adaptive system a relational semantics that transfers to unseen surface realizations and substantially improves selection of future-transformable commitments.

Boundaries:

```text
V0.7 != general semantic learning
V0.7 != general Future Sufficiency
V0.7 != mechanistic identification
```

---

## V0.7 Junction Diagnostic — semantics to selection

The 53 treatment failures were reconstructed with the full semantic evidence state.

Decomposition:

$$
53
=
20_{\rm semantic\ estimation}
+
21_{\rm current\ evidence\ ambiguity}
+
12_{\rm point\ reduction/authority}.
$$

A full-evidence commit-or-STOP policy converted 33 of the 53 original failures into either safe commitment or preserved ambiguity without changing the learned semantics.

This was a post-hoc diagnostic, not a confirmatory CCA/CARS result.

---

## V0.8 — Evidence to authority

Prospectively promoted the junction diagnostic into a fresh-world preregistered causal test.

Factorial dimensions:

$$
U\in\{\text{unique},\text{ambiguous}\},
\qquad
I\in\{\text{point-preserving},\text{point-collapsing}\}.
$$

Primary endpoint:

$$
A_{\rm auth}
=
\mathbf 1[
\text{commit iff full evidence uniquely warrants commitment}
].
$$

Secondary endpoint:

$$
H_{\rm future}
=
\text{future transformation coverage after the decision}.
$$

### D3 — evidence compression

When full evidence uniquely identified the safe choice but point compression reduced it to a tie:

$$
A_{\rm auth}^{P_1}=0.476,
\qquad
A_{\rm auth}^{P_2}=A_{\rm auth}^{P_3}=1.
$$

### D2 — authority overreach

When full evidence remained non-unique:

$$
A_{\rm auth}^{P_1}=A_{\rm auth}^{P_2}=0,
\qquad
A_{\rm auth}^{P_3}=1,
$$

with $P_3$ using STOP rather than manufactured uniqueness.

Forced policies happened to choose the future-safe candidate in 476/1000 ambiguous worlds while still having

$$
A_{\rm auth}=0.
$$

Thus:

$$
\text{correct outcome}\not\Rightarrow\text{correct authority}.
$$

All preregistered directional gates passed.

Adjudications:

```text
V0.8_D3_EVIDENCE_COMPRESSION      = PASS
V0.8_D2_AUTHORITY_OVERREACH       = PASS
V0.8_AUTHORITY_OUTCOME_SEPARATION = PASS
V0.8_EVIDENCE_TO_AUTHORITY        = PASS
```

This is the first preregistered fresh-world causal CCA/CARS result in the synthetic ladder.

---

# Closure

The V0.x ladder is closed.

Its final scientific product is not a benchmark score but a localization calculus:

> **Adaptive correction becomes Future-Insufficient at the first interface that collapses a distinction whose downstream corrective consequences remain non-equivalent.**

and its authority dual:

> **Commitment becomes unwarranted at the first decision map that distinguishes alternatives the evidence itself still treats as non-unique.**

The next research object is independent future adaptation outside the synthetic benchmark family.
