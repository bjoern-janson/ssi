# Construction Ledger — Role and Authority Index

This directory is an **append-only scientific construction ledger**, not a conventional source package.

This README is navigation only. It is **not** a member of `VFA-0.2-FROZEN-PACKET-7`, carries no execution authority, and cannot override the content-addressed packet, freeze anchor, authorization certificate, or current authorization status.

If any summary here conflicts with a frozen object, the frozen object governs.

## Start here

Current authority is determined in this order:

1. [`../AUTHORIZATION_STATUS.json`](../AUTHORIZATION_STATUS.json) — current A–I state and future-realization boundary.
2. [`I_AUTHORIZATION_CERTIFICATE.json`](I_AUTHORIZATION_CERTIFICATE.json) — issued Packet-7 authorization certificate.
3. [`I_FREEZE_PACKET_V7.json`](I_FREEZE_PACKET_V7.json) — exact frozen member/path/blob/role manifest.
4. [`I_FREEZE_ANCHOR_V7.json`](I_FREEZE_ANCHOR_V7.json) — packet-to-Git freeze anchor.
5. [`../evidence/I_CHAIN_OF_CUSTODY_PASS.md`](../evidence/I_CHAIN_OF_CUSTODY_PASS.md) — predicate-I interpretation and external validation record.

Current state:

```text
PACKET = VFA-0.2-FROZEN-PACKET-7
PACKET_SHA256 = 2d8b64e28f8207b51d1acae2459d0cf89774e7be0c10cb5a2a04808029ade3b7
AUTHORIZED_RUNNER_BLOB = c28245196b75f25892355baebf5ff5bc7a3758bb
STATE = AUTHORIZED_FUTURE_NOT_YET_REALIZED
FUTURE_OBLIGATION_ACCESSED = FALSE
FUTURE_RUN = NOT_EXECUTED
```

The authorized first-endpoint entrypoint is **`I_AUTHORIZED_FIRST_ENDPOINT_RUNNER_V2.py`**. `I_AUTHORIZED_FIRST_ENDPOINT_RUNNER.py` is retained as the Packet-7 `authorized_runner_base`; it is not a substitute entrypoint.

## 1. Treatment and known-domain construction

These files define the same-truth quotient treatment and its ordinary-domain noninterference evidence:

- `VALIDATED_SUBSTRATE.json` — shared truth-bearing substrate \(\mathcal W\).
- `GAMMA_A.json` / `GAMMA_B.json` — same 24 path records, different revision-equivalence partitions.
- `QUOTIENT_MAP.json` — deterministic quotient \(q\).
- `SEMANTIC_COORDINATE_MAP.json` — common semantic coordinate system.
- `QUOTIENT_CONSTRUCTION_AUDIT.py` / `quotient_construction_audit.json` — construction and \(F\circ q=F\) audit.
- `CAPABILITY_THREAT_MODEL.json` — frozen preactivation caller-capability scope.
- `CLOSED_PREACTIVATION_INTERFACE.py` — closed ordinary/gate interfaces.
- `HARDENED_N_LADDER_ATTACK.py` / `hardened_n_ladder_audit.json` — hardened N0–N4 noninterference attack and record.

## 2. Resource symmetry and treatment isolation

Predicate-E/F construction and evidence surfaces:

- `E_ENVIRONMENT_MANIFEST.json` — logical resource/information/execution contract.
- `E_ENVIRONMENT_KERNEL.py` / `E_ENVIRONMENT_ATTACK.py` / `e_environment_audit.json` — fixed-opportunity exposure and hostile E audit.
- `F_TREATMENT_ISOLATION_MANIFEST.json` — declared treatment/observable boundary.
- `F_TREATMENT_ISOLATION_ATTACK.py` / `f_treatment_isolation_audit.json` — residual treatment-recovery attack.
- `FINAL_POSTGATE_RUNTIME.py` — final first-endpoint runtime included in Packet 7.
- `FINAL_POSTGATE_SEMANTIC_CONTRACT.json` — final post-gate semantic contract included in Packet 7.
- `FINAL_TREATMENT_MATERIALIZATION.py` — common semantic treatment materializer included in Packet 7.
- `FINAL_POSTGATE_REAUDIT.py` / `final_postgate_reaudit.json` — final E/F post-gate re-audit.

`POSTGATE_SEMANTIC_CONTRACT.json`, `POSTGATE_SEMANTIC_KERNEL.py`, `POSTGATE_SEMANTIC_ATTACK.py`, and `postgate_semantic_audit.json` are preserved predecessor surfaces. They do not supersede the final consequence-grounded contract.

## 3. Future-consequence grounding

These files define how a future obligation may establish a treatment-blind consequence distinction without assuming one in advance:

- `FUTURE_GROUNDING_DOMAIN.json` — complete frozen q-kernel grounding domain.
- `FUTURE_CONSEQUENCE_WITNESSES.json` — frozen pre-future witness descriptions.
- `FUTURE_WITNESS_EXTRACTOR.py` — witness reconstruction kernel.
- `FUTURE_CONSEQUENCE_GROUNDING_CONTRACT.json` — \(J_{\rm future}\) grounding contract.
- `FUTURE_CONSEQUENCE_GROUNDING_KERNEL.py` — consequence-grounding implementation.
- `FUTURE_CONSEQUENCE_GROUNDING_ATTACK.py` / `future_consequence_grounding_audit.json` — grounding attack and evidence.
- `FUTURE_EXECUTION_ARTIFACT_CONTRACT.json` — exact future executable-resolution contract.
- `FUTURE_EXECUTION_ARTIFACT_KERNEL.py` — executable-resolution implementation.
- `FUTURE_EXECUTION_ARTIFACT_ATTACK.py` / `future_execution_artifact_audit.json` — artifact-resolution attack and evidence.

No realized future artifact, \(T_{\rm future}\), \(J_{\rm future}\), kernel adjudication, or result is a Packet-7 member; those are intentionally future-instantiated objects admitted only through the frozen rules.

## 4. Common-cause exposure and realized-event schemas

- `G_COMMON_CAUSE_MANIFEST.json` / `G_COMMON_CAUSE_KERNEL.py` — common obligation-selection/disclosure contract and kernel.
- `G_COMMON_CAUSE_ATTACK.py` / `g_common_cause_audit.json` — common-cause attack and record.
- `G_GROUNDING_INTEGRATION_MANIFEST.json` / `G_GROUNDING_INTEGRATION_KERNEL.py` — grounded common-cause integration contract and kernel.
- `G_GROUNDING_INTEGRATION_ATTACK.py` / `g_grounding_integration_audit.json` — integration attack and record.
- `G_GROUNDING_REALIZED_CERTIFICATE_TEMPLATE.json` — grounded realization certificate schema.
- `G_REALIZED_COMMON_CAUSE_CERTIFICATE_TEMPLATE.json` — realized common-cause certificate schema.
- `I_REALIZED_RECORD_TEMPLATE.json` — final future-realization record schema.

Templates are schemas for future-instantiated records. Their presence is not evidence that a future event has occurred.

## 5. Predicate-H rival ledger

- `H_MATERIAL_RIVAL_MANIFEST.json` — earlier rival ledger.
- `H_RESIDUAL_CONFOUND_AUDIT.py` / `h_residual_confound_audit.json` — earlier residual-veto adjudication, preserved with its failure.
- `H_MATERIAL_RIVAL_MANIFEST_GROUNDED.json` — consequence-grounded final rival ledger included in Packet 7.
- `H_GROUNDED_RESIDUAL_AUDIT.py` / `h_grounded_residual_audit.json` — final H adjudication evidence.

The current residual set is frozen as:

```text
H_future_distribution
H_CCA_CARS_downstream
H_physical_runtime
```

## 6. Predicate-I frozen identity and execution closure

Current Packet-7 identity/execution surfaces:

- `I_EVALUATION_RULE.json` — final evaluation rule.
- `I_EXECUTION_CLOSURE.json` — exact execution dependency closure.
- `I_CHAIN_OF_CUSTODY_KERNEL.py` — identity guard base.
- `I_CHAIN_OF_CUSTODY_KERNEL_V2.py` — identity and execution guard.
- `I_AUTHORIZED_FIRST_ENDPOINT_RUNNER.py` — authorized runner base retained as a Packet member.
- `I_AUTHORIZED_FIRST_ENDPOINT_RUNNER_V2.py` — **authorized first-endpoint entrypoint**, blob `c28245196b75f25892355baebf5ff5bc7a3758bb`.
- `I_CHAIN_OF_CUSTODY_ATTACK_V7.py` / `I_CHAIN_OF_CUSTODY_ATTACK_V7B.py` — final hostile chain-of-custody attack lineage.
- `i_chain_of_custody_audit_v7.json` — final machine-readable I evidence.
- `I_FREEZE_PACKET_V7.json` — authorized frozen packet.
- `I_FREEZE_ANCHOR_V7.json` — authorized packet's freeze anchor.
- `I_AUTHORIZATION_CERTIFICATE.json` — issued certificate.

The certificate, not filename recency, determines the authorized runner and packet identity.

## 7. Rejected packet candidates and predecessor machinery

`I_FREEZE_PACKET.json` through `I_FREEZE_PACKET_V6.json`, earlier available freeze anchors, earlier chain-of-custody attack/kernel variants, and their rejection evidence are preserved because each failure localized a real authorization weakness.

They are **not alternate authorized packets**. Packet 7 is the only issued object.

Do not delete, rename, move, or normalize these files merely because later candidates superseded them. Packet 7 itself includes the candidate-1 through candidate-6 rejection records as provenance members.

## 8. Generated audit records

Lower-case `*_audit.json` files are machine-readable records emitted by the corresponding attacks/audits. They are evidence records, not libraries or entrypoints. Several are Packet members by exact blob identity.

Do not regenerate them in place as a cleanup operation. A new execution that is scientifically licensed must write through the applicable frozen protocol and preserve the prior record when required by that protocol.

## Preservation rule

The flat namespace is costly for human navigation but valuable for content-addressed lineage. Therefore:

> **Index the ledger; do not refactor the ledger.**

No file in this directory should be moved, renamed, deduplicated, reformatted, or replaced solely for software-style cleanliness when a packet, certificate, audit, or preserved failure may depend on its exact path or blob identity.
