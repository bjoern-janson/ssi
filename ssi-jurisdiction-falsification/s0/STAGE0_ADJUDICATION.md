# SSI Jurisdiction Falsification — Stage 0 Adjudication

## Frozen object

- Object: `SSI-JURISDICTION-FALSIFICATION/S0`
- Specification freeze: `8275d4abca783a70adda0226c0401ddbb0755c19`
- Base: `main@7bec11badfbd51117ec942819e4c7dc15647c360`
- Scope: operational assay validity only

## Result

- Constitution fixtures: `8/11` exact localization passes
- Fresh post-freeze fixtures: `38/48` exact localization passes
- Terminal state: `OPERATIONALIZATION_INADEQUATE`
- Stage-1 authority: `NONE_STOP`

## Failure localization

All observed misses share one operationalization defect: when `R=0`, the frozen assay computes leverage as false because its leverage test is conditional on authority-boundary receipt (`L := R AND authority_after < authority_before`). The construction oracle, correctly for the requested independent-component assay, treats `L` as intact whenever no `L↓` break was injected.

Consequences:

- Constitution `R↓`-containing cases mislocalized `L` in `3/3` relevant fixtures.
- Fresh `R↓`-only cases: `0/8` exact localization passes; each was classified as `MULTIPLE_BREAKS` with observed `{R=0,L=0}` instead of required `CHALLENGE_BLOCKED` with `{R=0,L=1}`.
- Fresh intact, `D↓`-only, `L↓`-only, and `I↓`-only cases each passed `8/8`.
- The two fresh interaction cases containing `R↓` while `L` remained intact also mislocalized `L`; all other fresh cases passed.

This is a Stage-0 assay failure, not a kernel result. It demonstrates that the current `R/L` operational tests do not support independent localization under reachability failure.

## Frozen gate consequence

`S0_VALID = false`.

Therefore:

- `OPERATIONALIZATION_INADEQUATE`
- `NO_STAGE1_AUTHORITY`
- no semantic repair in this lineage
- no kernel support or falsification claim
- no Packet 7 or CUHK-X authority transfer

The next scientific action, if any, must be a newly constituted Stage-0 assay lineage rather than modification of this observed shot.
