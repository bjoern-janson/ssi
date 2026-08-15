# Evidence Ledger — Current Authority and Preserved Failures

This directory contains **interpretive evidence documents and preserved failure records** for the VFA-0.2 quotient lineage.

This README is navigation only. It is not a Packet-7 member and has no authority to change any adjudication. Current benchmark state lives in [`../AUTHORIZATION_STATUS.json`](../AUTHORIZATION_STATUS.json); exact frozen identity lives in [`../construction/I_FREEZE_PACKET_V7.json`](../construction/I_FREEZE_PACKET_V7.json) and [`../construction/I_AUTHORIZATION_CERTIFICATE.json`](../construction/I_AUTHORIZATION_CERTIFICATE.json).

The directory deliberately contains both `PASS` and `FAIL`/gap records. A later pass does not erase the earlier failure; it identifies a repaired lineage.

## Current evidence spine

For the authorized Packet-7 lineage, the most relevant reader path is:

1. [`HARDENED_N_LADDER_ATTACK_1.md`](HARDENED_N_LADDER_ATTACK_1.md) — hardened preactivation noninterference scope and result.
2. [`E_RESOURCE_INFORMATION_EXECUTION_PASS.md`](E_RESOURCE_INFORMATION_EXECUTION_PASS.md) — final logical resource/information/execution symmetry interpretation.
3. [`F_TREATMENT_ISOLATION_PASS.md`](F_TREATMENT_ISOLATION_PASS.md) — treatment-isolation interpretation.
4. [`FUTURE_CONSEQUENCE_GROUNDING_PASS.md`](FUTURE_CONSEQUENCE_GROUNDING_PASS.md) — treatment-blind future-consequence grounding.
5. [`G_COMMON_CAUSE_PASS.md`](G_COMMON_CAUSE_PASS.md) — common-cause future selection/disclosure evidence.
6. [`H_GROUNDED_RESIDUAL_VETO_PASS.md`](H_GROUNDED_RESIDUAL_VETO_PASS.md) — final grounded H rival/confound adjudication.
7. [`I_CHAIN_OF_CUSTODY_PASS.md`](I_CHAIN_OF_CUSTODY_PASS.md) — Packet-7 chain of custody, hostile execution evidence, and authorization interpretation.

These prose artifacts explain evidence; machine-readable predicate state is still controlled by `../AUTHORIZATION_STATUS.json` and the content-addressed construction/audit JSON.

## Historical blockers and repaired failures

The following are intentionally preserved because they identify why an earlier construction or authorization state was insufficient:

- [`E_RESOURCE_INFORMATION_EXPOSURE_GAP.md`](E_RESOURCE_INFORMATION_EXPOSURE_GAP.md) — earlier E blocker before a complete resource/information/execution contract existed.
- [`H_RESIDUAL_CONFOUND_VETO_FAIL.md`](H_RESIDUAL_CONFOUND_VETO_FAIL.md) — earlier H veto before consequence-grounded semantic/evaluator rivals were bounded.
- [`POSTGATE_SEMANTIC_CONTRACT_ATTACK_1.md`](POSTGATE_SEMANTIC_CONTRACT_ATTACK_1.md) — preserved post-gate semantic underdetermination failure that motivated consequence grounding.

These files are not stale mistakes. They are causal provenance for the repairs that followed.

## Rejected predicate-I packet candidates

Six candidate freeze packets were rejected before Packet 7 earned authorization:

- `I_FREEZE_PACKET_CANDIDATE_1_REJECTED.md`
- `I_FREEZE_PACKET_CANDIDATE_2_REJECTED.md`
- `I_FREEZE_PACKET_CANDIDATE_3_REJECTED.md`
- `I_FREEZE_PACKET_CANDIDATE_4_REJECTED.md`
- `I_FREEZE_PACKET_CANDIDATE_5_REJECTED.md`
- `I_FREEZE_PACKET_CANDIDATE_6_REJECTED.md`

They remain reviewable because the sequence localized open authority fields, packet/certificate schema weaknesses, execution-enforcement gaps, runner/closure incoherence, version-specific anchoring, and ambient-import shadowing before Packet 7 closed those surfaces.

Packet 7 explicitly retains these rejection records as provenance members. Do not collapse them into a generic “old versions” note or delete them after authorization.

## Reproduction and source-review notes

Supporting notes qualify where and how evidence was reproduced or independently inspected:

- [`F_REPRODUCTION_NOTE.md`](F_REPRODUCTION_NOTE.md)
- [`G_REPRODUCTION_NOTE.md`](G_REPRODUCTION_NOTE.md)
- [`H_REPRODUCTION_NOTE.md`](H_REPRODUCTION_NOTE.md)
- [`GROUNDING_REPAIR_REPRODUCTION_NOTE.md`](GROUNDING_REPAIR_REPRODUCTION_NOTE.md)
- [`FUTURE_WITNESS_SOURCE_REVIEW.md`](FUTURE_WITNESS_SOURCE_REVIEW.md)

A reproduction note does not independently upgrade the adjudication it documents; authority remains predicate- and artifact-specific.

## Reading rule

Do not infer current truth from suffixes such as `PASS`, `FAIL`, `GAP`, or from file modification order alone. Read evidence in lineage context:

```text
failure / gap
    -> localized repair
    -> independent or hostile re-attack
    -> machine-readable adjudication
    -> freeze / authorization, if all gates pass
```

The current endpoint is:

```text
A-I = PASS
PACKET_7 = FROZEN
AUTHORIZATION = ISSUED
FUTURE_OBLIGATION_ACCESSED = FALSE
FUTURE_RUN = NOT_EXECUTED
```

## Preservation rule

> **A failed gate is evidence about the generating process, not disposable clutter.**

Accordingly, cleanup in this directory should improve routing and labeling, not rewrite or remove the historical evidence that explains how the authorized object was earned.
