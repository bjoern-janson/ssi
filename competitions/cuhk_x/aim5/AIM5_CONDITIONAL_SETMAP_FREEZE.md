# CUHK-X AIM5 — nested action-aware conditional SET-MAP freeze

**Status:** FROZEN BEFORE AIM5 EXECUTION  
**Role:** internal aiming experiment only; no S2 package or leaderboard shot is authorized by this file.

AIM4 remains frozen and untouched as a historical/intermediate baseline. AIM5 is a successor, not a rewrite of AIM4.

---

## 1. Why AIM5 exists

The recovered S1 HAU `multi` locus is a decision-layer bottleneck:

```text
informative candidate evidence
    -> independent threshold decisions
    -> conjunctive exact-set amplification
```

AIM4 asked whether a learned answer cardinality followed by top-k margin selection can repair that bottleneck.

AIM5 asks a stronger but still local question:

> Holding all upstream S1 evidence generation fixed, can we preserve action-relative candidate evidence and cardinality uncertainty through the final exact-set decision instead of collapsing them prematurely?

The intervention remains entirely downstream of the frozen S1 normalized candidate margins.

---

## 2. Corrections to the naive SET-MAP proposal

### 2.1 AIM4 does not discard margin magnitude

AIM4 uses

\[
(s_1,s_2,s_3,s_4,n_+),
\]

not rank alone. Therefore cases such as

\[
(0.90,0.89,0.88,0.87)
\]

and

\[
(0.90,0.89,0.20,0.19)
\]

are already distinguishable by AIM4.

What AIM4 does discard is the mapping from each margin to the **semantic action identity**, and it converts the cardinality distribution to a single hard \(\hat k\) before set construction.

### 2.2 Adjacent gap features add no new linear information

For

\[
g_1=s_1-s_2,\quad g_2=s_2-s_3,\quad g_3=s_3-s_4,
\]

each \(g_j\) is a linear combination of \((s_1,s_2,s_3,s_4)\).

Because AIM4/AIM5 cardinality models are linear logistic models after scaling, explicitly appending those gaps does not expand the linear information space. AIM5 therefore does **not** add them.

### 2.3 Do not multiply two unnormalized uses of the same evidence

The naive score

\[
P(K=|S|\mid m)
\prod_{i\in S}p_i
\prod_{i\notin S}(1-p_i)
\]

uses the same margin evidence in both the cardinality term and marginal inclusion terms and is not automatically a coherent posterior.

AIM5 instead freezes the exact conditional factorization

\[
\boxed{
P(S\mid m,a)
=
q_{|S|}(m)\,
P(S\mid K=|S|,m,a)
}
\]

where the cardinality model owns the probability mass **between cardinalities**, and candidate utilities allocate that mass **within a fixed cardinality**.

---

## 3. Upstream invariants

AIM5 changes none of the following:

- V7 strong-IR representation;
- V7F pose + IMU + strong-IR representation;
- S1 HAU-multi route: V7F on common support, V7 IR fallback otherwise;
- per-action `StandardScaler + hinge-SGD` candidate model family;
- S1 candidate model hyperparameters;
- S1 median-absolute-training-margin normalization;
- 40-action semantic vocabulary;
- candidate labels;
- five canonical subject folds;
- any non-multi S1 branch;
- query text or query factorization;
- test data.

AIM2 Q1 and AIM3 Z remain closed.

---

## 4. Nested evaluation firewall

AIM5 fixes a meta-evaluation weakness in the frozen AIM4 implementation.

For outer subject fold \(f\):

### 4.1 Outer test evidence

Train the exact frozen S1 candidate models on the other four folds only and score fold \(f\).

These outer-test candidate signs MUST reproduce the corresponding frozen V7/V7F OOF candidate signs exactly. Otherwise:

```text
AIM5 = NOT_IDENTIFIED_BASE_REPRODUCTION_FAILURE
S2   = NOT_AUTHORIZED
```

### 4.2 Inner meta-training evidence

The decision layer may not train on in-sample candidate margins and may not use candidate-margin features produced by a model trained on outer fold \(f\).

Therefore, for every inner fold \(g\neq f\):

1. train S1 candidate models on the three folds excluding both \(f\) and \(g\);
2. score fold \(g\);
3. normalize margins using only that inner model's training-margin scales.

Concatenate the four inner-held-out folds to form the decision-layer training table for outer fold \(f\).

Thus:

\[
\boxed{
\text{outer-test subjects never enter either base-model or meta-model training.}
}
\]

No result receives S2 authority without this nested firewall.

---

## 5. Frozen candidate utility model

For each offered option \(i\), AIM5 observes:

- S1-normalized candidate margin \(m_i\);
- semantic action identity \(a_i\in\{1,\ldots,40\}\).

AIM5 does **not** fit 40 independent Platt curves. Existing HAU-multi support is too sparse for stable independent action slopes in some actions.

Instead it freezes one shared-slope, action-intercept logistic utility:

\[
\boxed{
\ell_i
=
\alpha\,\widetilde m_i
+
\beta_{a_i}
}
\]

where \(\widetilde m_i\) is the standardized normalized margin using decision-layer training rows only.

Implementation:

```text
X = [standardized_margin, one_hot(action_1..action_40)]
LogisticRegression(
    C=1.0,
    solver="lbfgs",
    max_iter=1000,
    class_weight=None,
    fit_intercept=False
)
```

The model is fit on **inner OOF candidate rows only** for the current outer fold.

The returned `decision_function` value is the candidate utility \(\ell_i\).

No per-action slope, threshold, class weight, C search, or alternate calibrator is allowed.

---

## 6. Frozen cardinality model

For one row, sort the four S1-normalized margins:

\[
s_1\ge s_2\ge s_3\ge s_4
\]

and define

\[
n_+=\sum_{i=1}^4\mathbf 1[m_i\ge0].
\]

Cardinality features remain exactly the AIM4 information set:

\[
\boxed{
z=(s_1,s_2,s_3,s_4,n_+).}
\]

No explicit gap features are added because they are linear combinations of the sorted margins.

Target:

\[
K=|Y|\in\{1,2,3,4\}.
\]

Frozen model:

```text
StandardScaler
-> LogisticRegression(
       C=1.0,
       solver="lbfgs",
       max_iter=1000,
       class_weight=None
   )
```

Fit on inner OOF episode rows only.

For outer-test row \(x\), retain the full probability vector

\[
\boxed{
q_k(x)=P(K=k\mid z_x),\qquad k=1,2,3,4.
}
\]

AIM5 does not collapse this to a hard \(\hat k\) before set construction.

---

## 7. Conditional SET-MAP decoder

For each nonempty subset

\[
S\subseteq\{A,B,C,D\},
\qquad S\neq\varnothing,
\]

let \(k=|S|\).

Within a fixed cardinality, define

\[
\boxed{
P(S\mid K=k,m,a)
=
\frac{
\exp\left(\sum_{i\in S}\ell_i\right)
}{
\sum_{T:\,|T|=k}
\exp\left(\sum_{j\in T}\ell_j\right)
}.
}
\]

Then

\[
\boxed{
P(S\mid m,a)
=
q_k(m)
\frac{
\exp\left(\sum_{i\in S}\ell_i\right)
}{
\sum_{T:\,|T|=k}
\exp\left(\sum_{j\in T}\ell_j\right)
}.
}
\]

This is normalized because

\[
\sum_{S\neq\varnothing}P(S\mid m,a)
=
\sum_{k=1}^4 q_k(m)=1.
\]

The AIM5 prediction is

\[
\boxed{
\widehat S_{\rm AIM5}
=
\arg\max_{S\neq\varnothing} P(S\mid m,a).
}
\]

There are exactly \(15\) candidate sets, so all are enumerated exactly.

---

## 8. Why this is strictly richer than hard cardinality top-k

For fixed \(k\), AIM4-style top-k trusts the raw normalized-margin ranking.

AIM5 can alter the within-k ordering when two semantic actions have different learned residual reliability after the S1 normalization, because

\[
\ell_i=\alpha\widetilde m_i+\beta_{a_i}.
\]

Across cardinalities, AIM4 retains only

\[
\hat k=\arg\max_k q_k,
\]

whereas AIM5 retains all \(q_k\) until final set MAP.

Thus AIM5 preserves two distinctions AIM4 merges:

1. **semantic action-relative evidence**;
2. **cardinality uncertainty**.

---

## 9. Comparators

### Primary comparator

Actual reproduced S1 multi decision operator:

```text
select every normalized margin >= 0
if none: select the maximum-margin singleton
```

### Secondary diagnostic comparator

Within the same nested AIM5 run, report a hard-cardinality comparator:

```text
k_hat = argmax_k q_k
answer = top-k_hat by raw S1-normalized margin
```

This is an AIM4-equivalent mechanism diagnostic under AIM5's nested firewall. It is **not** substituted for the separately frozen AIM4 artifact and cannot rescue AIM5.

---

## 10. Primary estimand

\[
\boxed{
\Delta_{\rm exact}^{AIM5}
=
Acc_{\rm exact}(D_{AIM5})
-
Acc_{\rm exact}(D_{S1}).
}
\]

Secondary diagnostics only:

- nested hard-cardinality exact accuracy;
- fold-level paired deltas;
- subject-level paired deltas;
- candidate-level accuracy/balanced accuracy;
- true vs predicted cardinality distribution;
- mean entropy of \(q_K\);
- frequency with which action-aware utility ranking differs from raw-margin ranking;
- S1 -> AIM5 answer transitions.

No secondary metric can rescue primary failure.

---

## 11. Frozen support gate

Keep the AIM4 bar unchanged.

AIM5 is supported only if ALL hold:

\[
\Delta_{\rm exact}^{AIM5}\ge +0.05,
\]

exact-set delta is nonnegative in at least 4 of 5 outer subject folds, and a 20,000-resample subject-cluster paired bootstrap has

\[
CI_{95\%,lower}(\Delta_{\rm exact}^{AIM5})>0.
\]

Bootstrap seed:

```text
260817
```

No weakening or retuning after execution.

---

## 12. Adjudication

If outer S1 sign reproduction fails:

```text
AIM5 = NOT_IDENTIFIED_BASE_REPRODUCTION_FAILURE
S2   = NOT_AUTHORIZED
```

If the experiment is identified but any support gate fails:

```text
AIM5 = NOT_SUPPORTED_CONDITIONAL_SETMAP
S2   = NOT_AUTHORIZED_BY_AIM5
```

If all support gates pass:

```text
AIM5 = SUPPORTED_CONDITIONAL_SETMAP_IN_FROZEN_MULTI_SCOPE
S2   = PACKAGING_CANDIDATE_AUTHORIZED
```

Success authorizes construction of a package candidate only. Before an external shot, the package must independently prove:

- the exact outer-training analogue of the frozen candidate utility and cardinality models is used;
- all non-multi S1 routes/predictions are unchanged;
- the multi test decision receives only information available under S1 plus semantic action identity already present in each option;
- no OOF truth enters test-time fitting;
- package/smoke tests pass;
- package bytes and provenance are frozen.

---

## 13. Closed search space

AIM5 performs no search over:

- candidate model family;
- representation;
- sensors;
- per-action calibration slopes;
- calibration C;
- cardinality model C;
- threshold;
- action subsets;
- gap features;
- feature zoo;
- ensemble weights;
- alternate set scorers;
- alternate folds;
- Q1;
- Z substrate variants.

Failure closes only this frozen `NESTED_ACTION_AWARE_CONDITIONAL_SETMAP_V1` candidate.
