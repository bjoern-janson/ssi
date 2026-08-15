# CUHK-X Large Model Track

This directory is the competition workspace for the CUHK-X Large Model Track inside the SSI repository.

## Boundary

The competition module is operationally separate from SSI core theory.

- Competition results may provide external rebounds and diagnostics.
- A leaderboard result does not automatically update SSI theory.
- Closed competition branches remain closed unless new evidence explicitly reopens them.
- Competition data, organizer-owned media, and non-redistributable derived data are not committed here.
- Frozen hashes and provenance may be committed so local artifacts can be verified without redistribution.

## Current shot state

Submission 1 (`S1`) has been taken and externally observed.

Submission 2 (`S2`) is **not yet authorized**. The completed internal aiming sequence after S1 closed both tested broad candidates:

1. AIM2 query-relative `Q1` (`QUERY_RELEVANCE_GATED_OVR`) — closed.
2. AIM3 reusable `Z0 -> Z1` substrate scope — closed.

The largest already-localized unresolved competition locus is HAU `multi`, whose failure geometry is candidate-decision error amplified by conjunctive exact-set scoring.

AIM4 remains frozen lineage/baseline:

```text
CARDINALITY_TOPK_V1
```

The active frontier is AIM5:

```text
NESTED_ACTION_AWARE_CONDITIONAL_SETMAP_V1
```

AIM5 holds S1 representation, sensors, per-action models, folds, vocabulary, routing, and margin normalization fixed. It changes only the row-level exact-set decision operator and uses a fully nested outer/inner subject split for decision-layer learning.

## Current authorization boundary

AIM5 is **not yet authorized to run**.

Current state:

```text
AIM5 = MECHANICAL_PRECHECK_PENDING
S2   = NOT_AUTHORIZED
```

Required order:

```text
MECHANICAL_PRECHECK
-> STOP
-> POST_PRECHECK_BYTE_FREEZE
-> RUN_AUTHORIZED
-> AIM5_RUN
```

The mechanical precheck verifies outer subject isolation, inner base-model isolation, training-only margin normalization/meta fitting, the frozen meta-feature contract, frozen AIM4 helper bytes, exact S1/V7/V7F candidate-sign reproduction, and the exact S1 multi decision operator.

A passing precheck yields only:

```text
RUN_AUTHORIZATION = BYTE_FREEZE_PENDING
```

It must not automatically execute AIM5.

AIM5 itself can later produce only:

```text
NOT_IDENTIFIED_BASE_REPRODUCTION_FAILURE
NOT_SUPPORTED_CONDITIONAL_SETMAP
SUPPORTED_CONDITIONAL_SETMAP_IN_FROZEN_MULTI_SCOPE
```

Only the final state authorizes construction of an S2 packaging candidate. It does not itself authorize an external leaderboard shot.

See:

- `STATE_RECOVERY_2026-08-15.md` — recovered S1→AIM3 ledger;
- `aim4/*` — frozen AIM4 lineage;
- `aim5/AIM5_CONDITIONAL_SETMAP_FREEZE.md` — AIM5 scientific freeze;
- `aim5/AIM5_MANIFEST.json` — current authorization state and hashes;
- `aim5/cuhkx_aim5_precheck.py` — mechanical precheck;
- `aim5/AIM5_KAGGLE_RUN.md` — two-stage precheck/freeze/run contract.
