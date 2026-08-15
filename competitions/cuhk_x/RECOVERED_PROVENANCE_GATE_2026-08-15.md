# CUHK-X — recovered provenance gate

**Date:** 2026-08-15  
**Branch:** `agent/cuhkx-restart-clean`  
**Role:** bridge between the clean restart and the preserved historical laboratory record.

This file corrects one ambiguity in the clean restart:

```text
revoking inherited authority != erasing verified provenance
```

Historical CUHK-X experiments remain available as evidence/provenance. They may regain current operational authority only through explicit continuity checks against the current competition object.

---

## 1. Current competition object reverified in the clean restart

Current official Kaggle competition bytes supplied on 2026-08-15:

```text
competition ZIP SHA-256
6a9dc7dd59c1bec120f4d408b911695e1592b81c10845dce3c1306a3cb876433

training_qa.csv
2509ed00f9305d552378618d8987559bdff7a4b56241c630ba99dc4051f535bc
4087 rows

test_qa.csv
d694c7abc5a003d5c9048098880f0f77716fae0eb18d1c9fe9330e4e987320a5
682 rows

sample_submission.csv
456905af98ce5257042f3779982e5b48e0ea248fcdf38eb79c9dd3e4f88a0a38
682 rows
```

The current competition object has:

```text
train episodes = 1333
  HAU = 809
  HARn = 524

test episodes = 208
  HAU = 144
  HARn = 64
```

Observed hierarchy:

```text
subject > physical episode/path > QA row
```

QA rows sharing one path are repeated questions over one physical episode and are not independent observations.

Current evaluation contract was read directly from the Kaggle Evaluation page:

```text
overall accuracy
all QA rows weighted equally
single/combination/emotion/object_interaction: exact match
multi: exact set equality, order ignored, no partial credit
sequence: exact chronological order
```

The current mounted sample-submission byte schema is:

```text
qa_id,prediction
```

---

## 2. Current nonvisual byte continuity

The currently supplied official nonvisual supplement is byte-identical to the historical laboratory input:

```text
LMT_(IMU,Radar,Skeleton).zip
SHA-256 = 72f34e9f0005d2ee0fefe9a7687bd54fa6dbdf171b6112132523085fa7475afb
```

Its manifest maps IMU/Radar/Skeleton observations to the same QA episode/path units.

Therefore current continuity is established for:

```text
QA object                PASS
QA episode grammar       PASS
nonvisual supplement     PASS
scoring semantics        PASS
cross-subject structure  PASS
```

---

## 3. Recovered historical visual provenance

The preserved historical laboratory record contains the official visual release inputs:

```text
HAU-001.zip
Training-20260813T154030Z-1-002.zip
Testing-20260813T154026Z-1-001.zip
```

The completed V0 visual census reported:

```text
train QA episodes visually found = 1333 / 1333
test QA episodes visually found  = 208 / 208
MP4 streams                       = 13128
observed modalities               = Depth, Depth_Color, IR, Thermal
MP4 parse errors                  = 0
```

It also established the systematic train/test interface shift:

```text
Depth/IR: train 320x240 -> test 640x480
Thermal: 320x240 where present
```

These are recovered historical measurement facts, not newly rerun measurements in the clean branch.

---

## 4. Recovered historical empirical boundary

The prior representation ladder was closed through V7. The recovered evidence record includes:

```text
S1 public score       = 0.49122
S1 exact-row OOF      = 0.5049003832
public - OOF          = -0.0136803832
```

The V7 fixed-IR representation intervention changed candidate balanced accuracy approximately:

```text
0.66557 -> 0.75092
```

with all five held-out-subject folds positive.

The recovered exact-row diagnostic localized the largest remaining competition error mass to HAU emotion and HAU multi.

AIM2 and AIM3 were executed and closed their specific constituted candidates:

```text
AIM2 QUERY_RELEVANCE_GATED_OVR = CLOSED
AIM2 Z                          = POSITIVE_BUT_SUBMATERIAL
AIM3 shared Z scope             = CLOSED
S2                              = NOT_AUTHORIZED
```

These are preserved historical adjudications. They are not silently promoted into the clean branch as fresh conclusions.

---

## 5. AIM5 was never empirically adjudicated

Historical AIM5 froze:

```text
NESTED_ACTION_AWARE_CONDITIONAL_SETMAP_V1
```

for the HAU-multi decision layer, with a fully nested subject-held-out firewall and unchanged upstream S1 evidence generation.

Its Stage-1 mechanical precheck did **not** fail. It was never run because four byte-identical historical inputs could not be staged in the prior execution environment.

Historical terminal state:

```text
AIM5                  = MECHANICAL_PRECHECK_PENDING
MECHANICAL_PRECHECK   = NOT_RUN
PRECHECK              = NOT_IDENTIFIED
AIM5 empirical status = NOT_ADJUDICATED
```

Required frozen hashes include:

```text
Training ZIP
667a00cb03ec67e1eeb49a744cb4fc764878fadae0b35ea873e25c2f7b3868bc

V7 cache
e9699696af7d886896df7fa1e52d2b28ecfbb8abeef71a6b3b2ee04a68abb5db

pose cache
d7e609a5e8a9ebc4bbdda92f8fe601d8b0c6ccfd4a2757f9a632a1ac9211b89a

IMU cache
8c4656e2c76029783c18d0b76f92f58fa8165a786a7049c3be7bf90a28aa0234

S1 script
38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f

V7 result ZIP
af7687fad3c7a4d140707c09dd84edea79288abdd81f91e9755d21cb63aad088

AIM4 helper
ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5

AIM5 executable
620e35da4256e3368359e202729e45489b916687ef890e3f9d887e91f11a0605
```

---

## 6. Current continuity/re-admission rule

Historical work may regain operational authority only when all inputs relevant to the claim are reconstituted at their frozen byte identities and the current competition contract does not contradict the historical estimand.

For AIM5 the next admissible transition is therefore only:

```text
current Kaggle private datasets
    -> locate frozen AIM5 inputs
    -> verify exact SHA-256 values
    -> run AIM5 Stage-1 mechanical precheck only
    -> STOP
```

A passing mechanical precheck would establish implementation/lineage continuity. It would **not** itself establish AIM5 support and would not authorize a leaderboard submission.

No AIM5 Stage-2 empirical execution occurs until the post-precheck byte-freeze/authorization boundary is explicitly recorded.

---

## 7. Current state

```text
CURRENT_QA_CONTRACT                 = IDENTIFIED
CURRENT_EVALUATION_CONTRACT         = IDENTIFIED
CURRENT_INDEPENDENCE_STRUCTURE      = IDENTIFIED
CURRENT_NONVISUAL_BYTE_CONTINUITY   = PASS
HISTORICAL_VISUAL_PROVENANCE        = RECOVERED
HISTORICAL_S1_V7_PROVENANCE         = RECOVERED
HISTORICAL_AIM2_AIM3                = RECOVERED_CLOSED
AIM5                                = NOT_ADJUDICATED
AIM5_INPUT_RECONSTITUTION           = PENDING
MODELING_AUTHORITY_FROM_RECOVERY    = NONE
```

The immediate operation is a hash-only AIM5 input-reconstitution check in Kaggle. No model fitting is authorized by this ledger.
