# CUHK-X Router Matrix V1 — frozen constitution

ID: `CUHKX_ROUTER_MATRIX_V1`

## Sole question

Do any already-existing predictor families beat the currently deployed S1 route on a branch under the frozen five subject-held-out folds?

This is an aiming/selection object, **not S2** and not a submission.

## Invariants

- same official training corpus / QA rows;
- same five subject folds (`0ae2bd6a594152dd1af444566416410043ac11f153d20c8a517bb2a6d5052b73`);
- exact QA-row accuracy is the primary currency;
- no public-leaderboard information enters selection;
- no new representation, sensor, trained model family, hyperparameter search, threshold search, P1 treatment, AIM2 Q1, AIM3 Z1 deployment, or SSI experiment;
- S1 is the incumbent for every branch;
- an alternative is admitted only if exact OOF predictions can be reconstructed on the full target branch from its pre-existing predictor family without using test labels;
- partial-coverage alternatives are `NOT_CONSTITUTED` for branch replacement;
- no subset routing, fold-specific deployment, or outcome-contingent repair.

## Frozen candidate matrix

| Branch | Incumbent | Alternative |
|---|---|---|
| HAU/multi | S1 V7F/V7 hybrid | pure V7 strong-IR action-presence |
| HAU/single | S1 V7 IR 40-way | archived V7 per-action margins, offered-option argmax |
| HAU/combination | S1 V7 IR combination heads | archived V7 per-action margins through the exact S1 combination conversion |
| HARn/single | S1 V7 IR class head | B0 Skeleton class predictor only if full exact-row option scoring is constituted |
| HARn/object_interaction | S1 V7 IR class head | B0 Skeleton class predictor only if full exact-row option scoring is constituted |
| HAU/emotion | S1 only | none |
| HAU/sequence | S1 only | none |

The V7 per-action alternatives reuse already-generated subject-held-out action margins. They do not refit a model. Their branch conversion is fixed here before matrix scoring.

### HAU/single V7 per-action conversion

For each offered option, look up the archived V7 OOF margin for `(path, action)`. Full offered-option coverage is required. Predict the option with maximum margin; ties resolve A before B before C before D. Missing or duplicate `(path, action)` margins make the alternative `NOT_CONSTITUTED`.

### HAU/combination V7 per-action conversion

For the branch's full 40-action vocabulary, a margin for every action must be available for every row. Presence is `margin >= 0`. For each offered set, use the exact S1 conversion: minimize Hamming mismatch across the full action vocabulary; tie-break with the S1 signed `tanh(margin)` confidence sum; final tie-break A before B before C before D. Missing margins make the alternative `NOT_CONSTITUTED`; no imputation is allowed.

### HARn B0 Skeleton conversion

The historical B0 artifact stores top-1/top-3 class predictions, not full class-score vectors. Branch replacement requires the same offered-option exact-row currency as S1. B0 is admitted only if an unchanged B0 predictor execution supplies the class-score vector needed for deterministic S1-style option mapping on every target row. Otherwise it is `NOT_CONSTITUTED`. No top-1-only surrogate is permitted.

## Frozen selection gate

For a constituted alternative `m` against S1 on branch `b`:

```text
SELECT(m,b)
iff
    delta exact OOF >= +0.0100000000
AND alternative-minus-S1 exact delta >= 0 in at least 4/5 folds.
```

A zero fold delta counts as nonnegative. If several alternatives were ever constituted for one branch, select the largest pooled exact OOF accuracy among gate-passers; ties retain S1.

## Terminal states

Per alternative: `CONSTITUTED_SELECTED`, `CONSTITUTED_REJECTED`, or `NOT_CONSTITUTED`.

Whole matrix: `ROUTE_CHANGES_EARNED` iff at least one alternative is `CONSTITUTED_SELECTED`; otherwise `NO_ROUTE_CHANGES`.

`NO_ROUTE_CHANGES` is a valid result. It does not authorize a synthetic S2 identical to S1.

## Authority ceiling

This matrix can authorize only branch substitutions satisfying the frozen exact-OOF/stability gate. It cannot authorize a new representation, new model family, subset router, public-LB selection, P1/AIM3 revival, or claim about why a branch performs differently.
