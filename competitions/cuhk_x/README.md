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

AIM4 is now frozen before execution:

```text
CARDINALITY_TOPK_V1
```

It holds S1 representation, sensors, per-action models, folds, and vocabulary fixed, reconstructs the actual S1 normalized-margin multi decision semantics, and changes only the row-level answer-set map by cross-fitting a frozen cardinality predictor over four normalized candidate margins.

AIM4 can produce only:

```text
NOT_IDENTIFIED_BASE_REPRODUCTION_FAILURE
NOT_SUPPORTED_STRUCTURED_CARDINALITY_DECODER
SUPPORTED_STRUCTURED_CARDINALITY_DECODER_IN_FROZEN_MULTI_SCOPE
```

Only the final state authorizes construction of an S2 packaging candidate. It does not itself authorize an external leaderboard shot.

See:

- `STATE_RECOVERY_2026-08-15.md` — recovered S1→AIM3 ledger;
- `aim4/AIM4_STRUCTURED_SET_FREEZE.md` — scientific/competition freeze;
- `aim4/AIM4_MANIFEST.json` — executable and input hashes;
- `aim4/AIM4_KAGGLE_RUN.md` — precheck-first execution contract.
