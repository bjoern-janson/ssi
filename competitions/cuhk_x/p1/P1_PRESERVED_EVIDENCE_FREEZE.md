# CUHK-X P1 — preserved-evidence freeze 🧊

## Status

```text
EXPERIMENT_ID              = CUHKX-P1-PRESERVED-EVIDENCE-1
STATE                      = FROZEN_SPECIFICATION_ONLY
IMPLEMENTATION             = NOT_YET_CONSTITUTED
EXECUTION_AUTHORITY        = NONE
LEADERBOARD_AUTHORITY      = NONE
SSI_PACKET7_AUTHORITY      = NONE
PARENT_MAIN                = 7bec11badfbd51117ec942819e4c7dc15647c360
```

P1 is a **competitive engineering stress test** extracted from the SSI/MAGIKARP preservation principle. It is not an SSI confirmation experiment and it has no authority over VFA-0.2 Packet 7.

The frozen wager is:

\[
\boxed{Z_{\rm early}\rightarrow Z_{\rm preserved}}
\]

with the upstream encoded evidence and downstream reasoning system held fixed.

P1 separates two claims that must never be collapsed:

\[
\boxed{\text{P1-A/B: does preservation improve relational composition?}}
\]

and

\[
\boxed{\text{P1-C: is that gain larger under held-out-subject shift?}}
\]

---

## 1. Frozen lineage

### Current competition contract

```text
current QA ZIP SHA-256
6a9dc7dd59c1bec120f4d408b911695e1592b81c10845dce3c1306a3cb876433

training_qa.csv rows = 4087
test_qa.csv rows     = 682

current nonvisual supplement SHA-256
72f34e9f0005d2ee0fefe9a7687bd54fa6dbdf171b6112132523085fa7475afb
```

### Frozen S1 control identity

```text
submission_id = CUHKX_SUBMISSION_1_V7_ROUTER
main script    = cuhkx_submission1.py
SHA-256        = 38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f
```

Reference implementation identities:

```text
cuhkx_v7_strong_ir_dinov2.py
473d83342c680836badc0aa5232f32df5aecb7ae7d5755ec7986798eac13b544

cuhkx_b2_hau_pose_v2.py
6bb2a411864d0a9c48cce0d122ca17ccb980912d71d17f75aa99b4593ee49fb1

cuhkx_b4_imu_v2.py
1bf3b37923f59e433fd95bcebbac511a2e51b34b24efe8fd89d0b75ccc7a814a
```

Historical diagnostic identity:

```text
DIAGNOSTIC_ID = CUHKX_S1_EXACT_OOF_DIAGNOSTIC_V1
S1 public     = 0.49122
S1 OOF exact  = 0.5049003832
S1 HAU multi exact OOF          = 0.36959
V7 matched-support exact-set    = 0.37405
```

These numerical values are lineage/reproduction anchors. They are not substitutes for exact prediction-stream reproduction.

### Canonical subject folds

```text
fold 0 = [2, 16, 20]
fold 1 = [3, 9, 18, 24]
fold 2 = [1, 19, 22]
fold 3 = [5, 7, 8, 21]
fold 4 = [4, 6, 17, 23]

canonical fold SHA-256
0ae2bd6a594152dd1af444566416410043ac11f153d20c8a517bb2a6d5052b73
```

Historical AIM2/AIM3/AIM4/AIM5 material remains provenance only. None of those objects is silently promoted into P1 authority.

---

## 2. Scientific questions

### P1-A — composition

> Under identical upstream encoded evidence and an identical downstream reasoner, does delaying irreversible compression materially improve exact relational composition?

### P1-B — localization

> If P1-A is positive, does the gain localize to composition-sensitive structure rather than generic perception?

P1-B is secondary. It cannot rescue P1-A.

### P1-C — transfer interaction

> Independently of P1-A/B, is the preserved-evidence gain larger under held-out-subject shift than under the corresponding familiar-subject estimate?

P1-C is a separate claim. A positive P1-A does not imply P1-C.

---

## 3. Treatment identity

The causal boundary is frozen as:

\[
X
\rightarrow
\boxed{\operatorname{Encode}(X)}
\rightarrow
\begin{cases}
Z_{\rm early}\\
Z_{\rm preserved}
\end{cases}
\rightarrow
\boxed{\text{same reasoner}}
\rightarrow
\hat S.
\]

### Same-upstream-evidence gate

`Encode(X)` must be computed once per unit, or otherwise mechanically proven identical, and both arms must consume the same content-addressed encoded object.

Any arm-specific difference before this boundary yields:

```text
NOT_IDENTIFIED_UPSTREAM_EVIDENCE_MISMATCH
```

and P1 stops before scientific scoring.

The preserved arm may **not** add:

- a modality;
- an encoder or feature extractor;
- encoder fine-tuning;
- extra augmentation;
- extra retrieval;
- an external-model call;
- extra training examples;
- arm-specific preprocessing;
- arm-specific prompt content before the treatment boundary.

### Control — `EARLY_COMPRESSION`

The identical encoded evidence is collapsed at the incumbent S1-compatible interface before final composition.

### Treatment — `PRESERVED_EVIDENCE`

The same encoded evidence remains explicit through a minimal typed evidence object until question-conditioned composition.

Minimal record:

\[
e_i=(\text{entity/action},\text{modality},t,\text{relation},\text{confidence})
\]

with alternatives retained **only** when the identical upstream evidence already supports multiple hypotheses.

The treatment is not licensed to invent alternatives.

---

## 4. Held-fixed contract

The following are identical between arms:

```text
raw competition inputs
measurement availability
encoder weights / bytes
encoder preprocessing
training rows and labels
subject folds
reasoner implementation / bytes
question text and answer options
prompt / template
output vocabulary
training budget
inference budget
random seeds
decision policy except where the same reasoner deterministically consumes the arm representation
hardware class where materially relevant
```

Forbidden treatment leakage:

```text
new modality
new pretrained backbone
larger reasoner
extra perception stage
extra training examples
extra inference calls
arm-specific hyperparameter search
arm-specific threshold tuning
post-result manual rules
```

If these equalities cannot be mechanically established, the outcome is:

```text
NOT_IDENTIFIED_TREATMENT_IDENTITY_FAILURE
```

not a negative P1 result.

---

## 5. Representation semantic contract

### Licensed invariances \(\mathcal G\)

The following transformations must not change question-conditioned evidence selection or the final prediction, except for deterministic tie representation:

1. **Record permutation** — only when explicit time/relation fields preserve semantics and canonicalization reconstructs the same relation graph.
2. **Field renaming** — bijective schema renaming with an exact map.
3. **Opaque identifier renaming** — bijective relabeling preserving equality and relations.
4. **Equivalent serialization** — canonical decode yields identical typed records and numerical values.
5. **Confidence serialization** — representation changes only when canonical decode reproduces the same confidence values within absolute tolerance `1e-12`.

Formally:

\[
\boxed{f(g(\mathcal E),q)=f(\mathcal E,q)\quad\forall g\in\mathcal G.}
\]

### Predeclared destructive ablations \(d\)

These are explicitly **not** invariances:

```text
d_time        delete/merge a represented temporal-order distinction
d_modality    erase modality provenance
d_alternative collapse supported alternatives to top-1 early
d_relation    merge distinct relation labels into one class
```

They are secondary mechanism probes only. No destructive ablation may define, tune, rescue, or replace the primary P1 treatment after outcomes are visible.

---

## 6. Evaluation hierarchy

```text
subject
  > episode/path
      > QA row
          > candidate option
```

The primary inferential unit is the **subject**.

Questions, episodes, frames, and candidate options nested inside a subject are repeated measures and must not be counted as independent inferential units.

No question-level bootstrap is permitted for the primary claims.

---

## 7. Baseline reproduction gate

Before the preserved arm may receive scientific scoring, the control must reproduce the frozen S1/V7 diagnostic prediction stream on the applicable P1 population, including:

- exact S1 multi decision semantics;
- canonical subject-fold assignment;
- the frozen S1/V7 control lineage;
- exact row/unit alignment.

The historical values `0.36959` and `0.37405` are useful alarms but do not replace exact lineage reproduction.

Failure yields:

```text
NOT_IDENTIFIED_BASELINE_REPRODUCTION_FAILURE
```

and stops P1.

---

## 8. P1-A — primary composition endpoint

Primary scope:

```text
HAU / multi
```

Primary metric:

```text
exact-set accuracy
```

Required decomposition:

```text
candidate balanced accuracy
candidate accuracy
candidate macro-F1
required-option recall
false-positive option rate
full-set recovery
exact-set accuracy
predicted-set-size error = |S_pred| - |S_true|
```

The clean mechanistic signature is:

\[
Q_{\rm candidate}^{P}\approx Q_{\rm candidate}^{E}
\quad\land\quad
Q_{\rm exact}^{P}>Q_{\rm exact}^{E}.
\]

`approximately equal` is frozen as:

```text
abs(delta candidate balanced accuracy) <= 0.01
```

Material exact-set improvement is frozen as:

```text
delta exact-set accuracy >= +0.03
```

Fold stability requires:

```text
preserved exact-set >= early exact-set in at least 4 / 5 canonical outer folds
```

Therefore:

```text
SUPPORTED_PRESERVED_COMPOSITION
iff
    delta exact-set >= +0.03
AND abs(delta candidate balanced accuracy) <= 0.01
AND preserved exact-set >= early exact-set in >= 4/5 folds
```

Otherwise:

```text
NOT_SUPPORTED_PRESERVED_COMPOSITION
```

The supported claim is narrow:

> In the frozen HAU-multi scope, delaying compression improved exact composition without a material gain in candidate-level recognition.

It does not establish general representation superiority.

---

## 9. P1-B — predeclared localization diagnostics

These branches are secondary and cannot alter P1-A adjudication.

### HAU sequence

Primary diagnostic:

```text
order-confusion rate
```

Expected preservation signature if the exact same treatment is constituted:

```text
order-confusion rate decreases
```

### HAU combination

Primary diagnostic:

```text
exact-option accuracy
```

with latent relation/composition diagnostics reported underneath it.

Expected direction if constituted:

```text
accuracy increases
```

### HAU emotion — negative control

Primary diagnostic:

```text
exact-option accuracy
```

Expected preservation signature:

```text
approximately unchanged
```

### Constitution gate

A secondary branch is scored **only** if the exact same post-encoder intervention can be applied without changing:

- upstream evidence;
- encoder bytes;
- reasoner bytes;
- prompt;
- training budget;
- inference budget.

Otherwise that branch is:

```text
NOT_IDENTIFIED_UNCONSTITUTED_BRANCH
```

We do not build a different architecture merely to obtain the desired multi/sequence/combination/emotion pattern.

---

## 10. P1-C — subject-shift interaction

The existing five canonical S1 subject folds remain the outer held-out-subject structure.

For held-out subject \(k\) in outer fold \(f\):

\[
\Delta_{{\rm unseen},k}
=
Q^P_k-Q^E_k
\]

where both models are trained only on folds \(\neq f\).

For the familiar-subject comparator, the outer training population is evaluated through **fully nested inner subject-fold OOF predictions** using only the other four canonical folds. No in-sample prediction may enter the seen estimate.

Let:

\[
\Delta_{{\rm seen},f}
=
\text{mean subject-level preserved-minus-early effect over the inner-OOF outer-training subjects}.
\]

Then:

\[
\boxed{
\Delta_{{\rm transfer},k}
=
\Delta_{{\rm unseen},k}
-
\Delta_{{\rm seen},f(k)}.
}
\]

and:

\[
\boxed{
\overline{\Delta_{\rm transfer}}
=
\frac{1}{18}\sum_{k=1}^{18}\Delta_{{\rm transfer},k}.
}
\]

### Uncertainty

Use a hierarchical paired bootstrap with `20,000` resamples:

1. resample the five outer folds with replacement;
2. within each selected fold, resample its held-out subjects with replacement;
3. recompute the mean transfer interaction.

No QA-row or candidate-level bootstrap may substitute for this procedure.

### P1-C support gate

```text
SUPPORTED_TRANSFER_INTERACTION
iff
    mean(delta_transfer) > 0
AND 95% hierarchical-bootstrap CI lower bound > 0
AND delta_transfer_k > 0 for at least 12 / 18 subjects
```

Otherwise:

```text
NOT_SUPPORTED_TRANSFER_INTERACTION
```

The licensed claim is only:

> The frozen preservation intervention had a larger effect under held-out-subject shift than under its corresponding familiar-subject OOF estimate.

P1-C does not inherit authority from P1-A/B.

---

## 11. Implementation freeze required before scoring

This specification does **not** authorize immediate outcome measurement.

Required order:

```text
P1 SPECIFICATION FREEZE
-> materialize exact S1 control lineage
-> implement both arms from one shared encoded-evidence object
-> mechanical baseline-reproduction check
-> mechanical treatment-isolation check
-> mechanical G-invariance check
-> freeze implementation bytes + environment
-> P1 RUN
-> result freeze
```

Implementation changes are allowed only to instantiate the already-frozen scientific object. If implementation exposes a contradiction in the specification, the contradiction must be preserved and P1 remains unscored until a new explicitly superseding preregistration is created **before any P1 outcome is observed**.

---

## 12. Stopping rule

The branch-level rule is:

\[
\boxed{\text{No P1 support}\Rightarrow\text{no larger architecture justified by P1}.}
\]

More precisely:

```text
if P1-A is NOT_SUPPORTED:
    close this preservation branch in the frozen composition scope
    do not create a larger preserved-evidence architecture as a rescue

if P1-A is SUPPORTED:
    composition-oriented scaling may be considered only in a new frozen experiment

if P1-C is NOT_SUPPORTED:
    do not claim portability from P1-A/B

if P1-C is SUPPORTED:
    transfer-oriented scaling may be considered only in a new frozen experiment
```

Forbidden post-result moves:

```text
P2 as rescue for failed P1
architecture expansion to recover a failed endpoint
threshold retuning
subject/category subset selection
new treatment definition after seeing P1
new materiality threshold after seeing P1
relabeling NOT_IDENTIFIED as negative or zero
using a leaderboard result to retroactively validate P1
```

No internal P1 result authorizes an external Kaggle submission. A competition shot requires a separate packaging/submission authorization decision.

---

## 13. Explicit non-claims

P1 does **not** establish:

- SSI validity;
- MAGIKARP validity in general;
- VFA-0.2 Packet 7 support or contradiction;
- formal future-safe representation;
- general superiority of richer representations;
- that emotion is measurement-limited unless separately identified;
- a right to change the current CUHK-X competition system;
- authority to submit to Kaggle.

The sole frozen engineering question is:

> **When upstream evidence is identical, does delaying irreversible compression preserve enough relational structure to improve exact composition, and independently, does that advantage grow under held-out-subject shift?**
