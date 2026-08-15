# CUHK-X Large Model Track — clean restart

**Reset date:** 2026-08-15  
**Branch:** `agent/cuhkx-restart-clean`  
**Base:** SSI `main` at `e03127f839bbbf960ee45244e75c637df858ecf9`

This workspace starts the CUHK-X Large Model Track from the current public competition contract. It intentionally does **not** inherit AIM2–AIM5 architectures, feature choices, folds, thresholds, caches, or adjudications from earlier CUHK-X work.

Those artifacts remain historical lineage on separate branches only.

## Official source of truth

- Kaggle competition: https://www.kaggle.com/competitions/cuhk-x-competition-large-model-track
- Official challenge site: https://openaiotlab.github.io/CUHK-X-Challenge/
- CUHK-X project page: https://openaiotlab.github.io/CUHK-X/
- CUHK-X paper: https://arxiv.org/abs/2512.07136

When these disagree, the current Kaggle competition page/rules govern competition participation and submission requirements.

## Verified public competition contract

### Track

CUHK-X Multimodal Human Activity Challenge — **Large Model Track**.

The task is privacy-preserving multimodal **VQA** over Human Action Understanding (HAU) and Human Action Reasoning (HARn).

The official challenge site currently describes:

- 6,160 VQA questions across five reasoning types;
- 40 action classes in the underlying CUHK-X activity ontology;
- cross-subject evaluation;
- challenge modalities excluding RGB;
- no parameter limit for the Large Model Track;
- large/pretrained vision-language models permitted.

### Subject split

Public challenge description:

```text
train subjects: user 1–9, 16–24
public-test subjects: user 10, 11, 25, 26
private-test subjects: additional held-out subjects
```

The raw Kaggle files will be treated as authoritative for the exact current split and row schema once reacquired.

### Modalities

The challenge site lists the permitted non-RGB modalities as:

```text
Depth
Thermal
Infrared
Skeleton
IMU
mmWave radar
```

The Large Model Track page emphasizes depth/non-RGB VQA. The challenge news states that non-visual modalities for the Large Model Track (IMU, skeleton, radar) were uploaded on 2026-07-14.

No modality will be assumed present for a particular row until verified against the current Kaggle files.

### External models/tools

Current competition rules permit external data/models and closed-source APIs in the Large Model Track subject to the competition's accessibility/reasonableness, licensing, reproducibility, and winner-delivery requirements.

This permission is **not** itself a modeling choice.

### Integrity constraints

Forbidden by the competition rules:

- use of test-set ground-truth labels in training;
- manual labeling/prediction of test questions;
- multiple Kaggle accounts for submissions;
- collusion/private sharing outside an official team.

### Submission / final-selection consequences

- maximum 5 Kaggle submissions per day;
- up to 2 final submissions may be selected;
- private leaderboard determines Kaggle ranking;
- current deadline / leaderboard freeze: 2026-09-15;
- top-ranked teams enter a verification stage involving fresh seen/unseen-subject data and organizer reproduction;
- winner/finalist deliverables include reproducible training/inference code, checkpoint(s), `inference.sh`, README/environment documentation, and required declarations.

Therefore the optimization target is not merely public-leaderboard score. A viable solution must survive subject shift and independent reproduction.

## Clean-reset firewall

The new workflow is:

```text
CURRENT KAGGLE BYTES
        ↓
RAW DATA / SCHEMA AUDIT
        ↓
METRIC + SUBMISSION CONTRACT
        ↓
LEAKAGE-SAFE VALIDATION DESIGN
        ↓
BASELINES
        ↓
ERROR TOPOLOGY
        ↓
MODEL / INTERFACE HYPOTHESES
        ↓
HELD-OUT EVALUATION
        ↓
SUBMISSION SHOT
```

Explicitly forbidden during reset:

```text
old model choice -> new baseline
old feature result -> presumed useful feature
old fold design -> current validation design
old leaderboard rebound -> current parameter choice
old derived cache -> authoritative raw input
```

Historical work may later be reintroduced only as a named candidate after the new data/metric/validation contract has been independently established.

## Current unknowns — must be resolved from current Kaggle files

Before modeling, establish and freeze:

1. exact competition file inventory and SHA-256 values;
2. training-question schema;
3. test-question schema;
4. exact submission columns / answer encoding;
5. exact Kaggle evaluation formula;
6. row counts and task/category frequencies;
7. path-to-modality availability by source/task;
8. subject identifiers and leakage-safe grouping unit;
9. whether multiple questions share the same sensor episode;
10. exact relationship among HAU/HARn task families and answer grammars.

None of these will be inferred from earlier AIM artifacts when the raw competition files can answer them directly.

## Immediate gate

```text
STATUS = RAW_KAGGLE_ACQUISITION_PENDING
```

This runtime currently has no authenticated Kaggle CLI/API credentials, so the current competition bytes cannot be downloaded directly here.

The next valid step is to obtain the **current Kaggle competition data archive/files** under the user's authorized Kaggle access, then hash and audit those bytes before choosing a model.
