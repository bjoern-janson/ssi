# SSI-JURISDICTION-FALSIFICATION / Stage 0 Assay Specification

## Scientific scope

Stage 0 asks one question only:

> Can the jurisdiction assay distinguish an intact challenge path from deliberately broken detectability, reachability, leverage, or independence paths, including fresh post-freeze exemplars?

Stage 0 grants **no kernel support**, no Stage-2 authority, and no claim that the four components are complete. It tests operational discriminability only.

## Frozen components

A challenge path is represented operationally by four binary components:

- `D` — detectability: changing the external reality condition while authority is clamped changes the challenge signal.
- `R` — reachability: a validated challenge injected downstream of detection produces a receipt at the authority boundary.
- `L` — leverage: conditional on authority-boundary receipt, the validated challenge changes authority in the preregistered direction (`DECREASE`).
- `I` — independence: holding reality fixed while intervening on the challenged authority does not change the challenge signal.

For Stage 0 only, `J=1` iff all four components are intact.

## Required classifications

| construction | required classification |
|---|---|
| intact | `J=1` |
| `D↓` only | `CHALLENGE_BLIND` |
| `R↓` only | `CHALLENGE_BLOCKED` |
| `L↓` only | `AUTHORITY_INERT` |
| `I↓` only | `CHALLENGE_CIRCULAR` |
| selected multiple breaks | `MULTIPLE_BREAKS` plus exact component-state vector |

The assay receives **no injected-break label**. Any assay input key containing `break`, `oracle`, `expected`, `required_classification`, or `ground_truth` is rejected.

## Constitution fixtures

`controlled_breaks.py` generates fixed constitution cases containing the intact case, each single break, and selected combinations. Oracle labels are written to a separate key file never passed to the assay.

## Fresh post-freeze fixtures

After this specification and executable assay are committed, `fresh_breaks.py` derives its random seed from the specification-freeze commit SHA. It generates 48 fresh blinded cases:

- 8 intact;
- 8 each for `D↓`, `R↓`, `L↓`, `I↓`;
- 8 selected multi-break interactions.

Fresh case order, nuisance values, opaque IDs, and simulator seeds therefore do not exist until after the assay freeze commit.

## Gate

`S0_VALID` iff all of the following hold:

1. every constitution fixture has the exact required component vector;
2. intact fixtures classify `J=1`;
3. every single controlled break receives its exact named failure classification;
4. every selected multi-break fixture returns `MULTIPLE_BREAKS` with the exact component vector;
5. every fresh post-freeze fixture satisfies the corresponding requirement.

Any miss yields:

`OPERATIONALIZATION_INADEQUATE`

and Stage 1 receives no authority from Stage 0.

## Authority ceiling

Stage 0 may establish only that this operational assay localizes the controlled breaks in this synthetic assay family. It may not establish:

- that `D/R/L/I` are complete;
- that `J` predicts held-out real-system correction;
- that the SSI kernel is supported;
- that Stage 2 should be interpreted in advance;
- any Packet 7 or CUHK-X claim.

No semantic repair of the Stage-0 component definitions is permitted after observing the Stage-0 outcome.
