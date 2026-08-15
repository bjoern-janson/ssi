# CUHK-X AIM4 — structured-set / cardinality decoder freeze

**Status:** FROZEN BEFORE AIM4 EXECUTION  
**Role:** internal aiming experiment only; does not create or submit S2.

## 1. Recovered locus

The frozen S1 exact diagnostic localized HAU `multi` to candidate-decision errors amplified by conjunctive exact-set scoring. On the recovered route, candidate accuracy was about `0.75803` while exact-set accuracy was about `0.36959`; 304 of 510 failed sets were one candidate decision away from exact correctness.

A provenance correction is required before testing a repair: the historical S1 diagnostic reconstructed HAU-multi exact sets from the V7/V7F research result tables. Those tables apply independent `margin >= 0` decisions but do not implement the S1 runtime's forced-singleton fallback when no candidate margin is positive. S1 also normalizes each action margin by the median absolute training margin before cross-action confidence use.

Therefore AIM4 MUST first reconstruct the actual S1 multi OOF decision semantics. No repair result is admissible if that base replay does not reproduce the frozen V7/V7F candidate signs.

## 2. Scientific / competition question

Holding the S1 representation, sensors, candidate classifiers, folds, and candidate vocabulary fixed, can a structured row-level decision map improve HAU-multi exact-answer accuracy materially?

The intervention changes only:

```text
four normalized candidate margins
        -> answer-set decision map
```

It does NOT change:

- V7 strong-IR features;
- pose or IMU features;
- V7F concatenation;
- per-action StandardScaler + hinge-SGD candidate models;
- subject folds;
- action vocabulary;
- candidate labels;
- query text or query factorization;
- decision-margin training threshold;
- any other S1 branch;
- test data.

This is not reopening AIM2 Q1 or AIM3 Z. Those branches remain closed.

## 3. Frozen population and route

Population: all 809 HAU `multi` training QA rows under the five canonical subject-held-out folds.

For each held-out fold:

1. fit the frozen S1 IR per-action models on all non-held-out HAU-multi rows;
2. fit the frozen S1 V7F per-action models on the non-held-out rows inside the exact 786-unit pose+IMU+V7 common support;
3. score each held-out episode through the same S1 route:
   - common-support episode -> V7F;
   - otherwise -> V7 strong-IR fallback;
4. normalize each action margin by the median absolute training margin exactly as S1 does.

Before any decoder adjudication, the sign of every reconstructed OOF candidate margin must exactly reproduce the corresponding frozen V7/V7F candidate prediction in `cuhkx_v7_strong_ir_dinov2_results.zip`.

If this sign-reproduction gate fails:

```text
AIM4 = NOT_IDENTIFIED_BASE_REPRODUCTION_FAILURE
```

and no decoder result receives authority.

## 4. Frozen baseline B0

For each HAU-multi row, using the four S1-normalized offered-option margins:

```text
choose every option with margin >= 0
if none are chosen: choose the single option with maximum normalized margin
return selected option letters in sorted order
```

This is the actual S1 runtime set-decision rule.

AIM4 reports the exact-row OOF accuracy of this replay as `B0_exact`. The historical `0.36959` diagnostic value is retained as provenance; it is not forced as the replay value because the historical diagnostic omitted the S1 zero-positive singleton fallback.

## 5. Frozen intervention D1 — CARDINALITY_TOPK_V1

For each OOF episode, let the four S1-normalized margins be

\[
m_A,m_B,m_C,m_D.
\]

Sort them descending:

\[
s_1\ge s_2\ge s_3\ge s_4.
\]

The decoder feature vector is exactly

\[
x=(s_1,s_2,s_3,s_4,n_+),
\qquad
n_+=\sum_{j=1}^4 \mathbf 1[m_j\ge0].
\]

No action identity, option identity, question text, subject identity, sensor feature, or representation feature enters the decoder.

Target:

\[
k=|Y|\in\{1,2,3,4\},
\]

the number of correct offered options.

Decoder family is frozen as:

```text
StandardScaler
-> LogisticRegression(
       C=1.0,
       solver="lbfgs",
       max_iter=1000,
       class_weight=None
   )
```

No hyperparameter search, threshold tuning, class-weight search, feature search, or alternative decoder is allowed after AIM4 execution.

### Cross-fitting

For decoder fold `f`:

- train the decoder only on OOF margin rows belonging to the other four subject folds;
- predict cardinality `k_hat` for fold `f`;
- select the `k_hat` offered options with the largest S1-normalized margins;
- return letters sorted alphabetically.

Thus the held-out fold contributes neither candidate-model fitting labels nor decoder fitting labels to its own prediction.

## 6. Outcomes

Primary:

\[
\Delta_{exact}
=
Acc_{exact}(D1)-Acc_{exact}(B0).
\]

Secondary diagnostics only:

- fold-level exact-set deltas;
- candidate-level accuracy and balanced accuracy after top-k decoding;
- predicted vs true cardinality distribution;
- transition counts `B0 answer -> D1 answer`;
- subject-level paired exact differences.

Candidate-level metrics cannot rescue failure on exact-row accuracy.

## 7. Frozen materiality / uncertainty gate

AIM4 supports the structured decoder only if ALL hold:

1. pooled exact-set improvement

\[
\Delta_{exact}\ge +0.05;
\]

2. exact-set delta is nonnegative in at least 4 of 5 held-out-subject folds;

3. a 20,000-resample subject-cluster paired bootstrap has

\[
CI_{95\%,lower}(\Delta_{exact})>0.
\]

Bootstrap seed:

```text
260816
```

The `+0.05` branch gate corresponds to approximately

```text
0.05 * 144 / 682 = 0.01055718
```

of full-test exact-row score if the 144-row HAU-multi test branch transfers proportionally. This is a magnitude translation only, not a claimed leaderboard effect.

## 8. Frozen adjudication

If the base sign reproduction fails:

```text
AIM4 = NOT_IDENTIFIED_BASE_REPRODUCTION_FAILURE
S2   = NOT_AUTHORIZED
```

If the base replay succeeds but any support gate fails:

```text
AIM4 = NOT_SUPPORTED_STRUCTURED_CARDINALITY_DECODER
S2   = NOT_AUTHORIZED
```

If all support gates pass:

```text
AIM4 = SUPPORTED_STRUCTURED_CARDINALITY_DECODER_IN_FROZEN_MULTI_SCOPE
S2   = PACKAGING_CANDIDATE_AUTHORIZED
```

`PACKAGING_CANDIDATE_AUTHORIZED` is not permission to submit. The eventual S2 package must separately prove:

- all non-multi S1 predictions/routes are unchanged by construction;
- the exact supported decoder is fit from the frozen OOF margin table and applied to S1 test normalized margins;
- packaging/smoke-test checks pass;
- byte/provenance manifest is frozen before the external shot.

Only then may S2 become `READY_FOR_EXTERNAL_SHOT`.

## 9. Closed alternatives

AIM4 does not search among:

- alternative cardinality models;
- score-fusion schemes;
- per-action thresholds;
- global threshold shifts;
- hand-written cardinality caps;
- query-relative Q1;
- new Z substrate additions;
- branch-specific representation changes.

Failure closes only `CARDINALITY_TOPK_V1` in this frozen scope. It does not establish that structured set decoding in general is impossible.
