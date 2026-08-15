# VFA-0.2 — Quotient Revision Topology

This directory is the construction and evidence lineage for the first authorized prospective VFA benchmark.

It is intentionally **append-heavy**. Failed constructions, hostile attacks, repaired semantic contracts, rejected freeze packets, and execution evidence remain present because they are part of the scientific provenance chain.

For the current state, do not infer authority from filename recency. Start with:

1. [`AUTHORIZATION_STATUS.json`](AUTHORIZATION_STATUS.json)
2. [`construction/I_AUTHORIZATION_CERTIFICATE.json`](construction/I_AUTHORIZATION_CERTIFICATE.json)
3. [`construction/I_FREEZE_PACKET_V7.json`](construction/I_FREEZE_PACKET_V7.json)
4. [`construction/I_FREEZE_ANCHOR_V7.json`](construction/I_FREEZE_ANCHOR_V7.json)
5. [`evidence/I_CHAIN_OF_CUSTODY_PASS.md`](evidence/I_CHAIN_OF_CUSTODY_PASS.md)

For local navigation inside the two append-heavy ledgers:

- [`construction/README.md`](construction/README.md) — role/authority index for treatment objects, executable surfaces, audit records, packet candidates, and frozen execution identity.
- [`evidence/README.md`](evidence/README.md) — current evidence spine, historical blockers, rejected packet candidates, and reproduction notes.

## Current authority state

```text
BENCHMARK = VFA-0.2-QUOTIENT-REVISION-TOPOLOGY
A = PASS
B = PASS
C = PASS
D = PASS
E = PASS
F = PASS
G = PASS
H = PASS
I = PASS

PACKET = VFA-0.2-FROZEN-PACKET-7
PACKET_SHA256 = 2d8b64e28f8207b51d1acae2459d0cf89774e7be0c10cb5a2a04808029ade3b7
EXECUTION_ROOT_SHA256 = 56d2f3a996f6dc71183fa7325af06d738e8ba994f9b62a2ba454f85c5fe8fe1d
AUTHORIZATION_CERTIFICATE_SHA256 = 17335f0a5893406763fb7660e4f23c06b9343cc0818a1bc63db3abad9e0e4e1e

STATE = AUTHORIZED_FUTURE_NOT_YET_REALIZED
FUTURE_OBLIGATION_ACCESSED = FALSE
G_ACTIVATION = NOT_ACTIVATED
REALIZED_T_FUTURE = NOT_EVALUATED
REALIZED_J_FUTURE = NOT_EVALUATED
DELTA_PI = NOT_EVALUATED
KERNEL_FUTURE_INCLUSION = NOT_EVALUATED
FUTURE_RUN = NOT_EXECUTED
```

Packet 7 is frozen. The next scientific state transition must be produced by the preregistered external source. This README has no authority to modify the packet or reinterpret its execution rules.

## Treatment identity

The final construction removes the earlier truth/provenance confound by holding the validated factual substrate literally equal:

\[
\mathcal W_A=\mathcal W_B=\mathcal W.
\]

Both arms contain the same 24 semantic revision-path records. They differ only in revision-equivalence structure:

\[
D_A=(\mathcal W,\Gamma_A),
\qquad
D_B=(\mathcal W,\Gamma_B),
\qquad
\Gamma_B=q(\Gamma_A).
\]

The quotient is frozen independently of future outcomes and satisfies the known-domain condition:

\[
F\circ q=F.
\]

Thus the contrast is:

```text
same validated facts
+ same ordinary behavior
+ same resource/information/execution opportunity
+ different revision equivalence structure
```

not "A knows more" and not "A has a better ordinary retrieval graph."

Core treatment files:

- [`construction/VALIDATED_SUBSTRATE.json`](construction/VALIDATED_SUBSTRATE.json)
- [`construction/GAMMA_A.json`](construction/GAMMA_A.json)
- [`construction/GAMMA_B.json`](construction/GAMMA_B.json)
- [`construction/QUOTIENT_MAP.json`](construction/QUOTIENT_MAP.json)
- [`construction/SEMANTIC_COORDINATE_MAP.json`](construction/SEMANTIC_COORDINATE_MAP.json)

## Prospective scientific question

The logically prior future test is:

\[
\boxed{
\ker q\stackrel{?}{\subseteq}\ker T_{\rm future}.
}
\]

The future consequence grounder is treatment-blind. The twelve nontrivial q-kernel path surfaces reduce to **three independent source-fact grounding units**:

```text
ariakit    <-> aws
issue_5465 <-> knip
nested     <-> sentry
```

Each grounding unit is lifted across four relation kinds, yielding twelve reporting surfaces. The twelve surfaces are deterministic mechanism surfaces, **not twelve independent future observations**.

Primary interpretation order:

```text
realized common-cause conformance
    -> J_future over 3 grounding units
    -> kernel inclusion / non-inclusion
    -> conditional DeltaPi mechanism localization
    -> fresh evidence
    -> CCA
    -> CARS
    -> downstream viability
```

A/B reachability is not allowed to decide whether the future distinction exists. Future non-inclusion must be established first from treatment-blind consequences.

## Lineage

The current object was earned through preserved failures:

```text
VFA-0.1-REJECTED_RETRIEVAL_LEAKAGE
    |
    v
VFA-0.2-DORMANT-CORRECTIVE-RESERVE
    |
    +-- semantic truth/provenance confound
    +-- OPEN_CAPABILITY_SURFACE under hostile attack
    |
    v
VFA-0.2-QUOTIENT-REVISION-TOPOLOGY
    |
    +-- H failure: POSTGATE_SEMANTIC_UNDERDETERMINATION
    |
    v
VFA-0.2-FUTURE-CONSEQUENCE-GROUNDING
    |
    v
VFA-0.2-FREEZE-CHAIN-OF-CUSTODY
    |
    v
VFA-0.2-FROZEN-PACKET-7 / AUTHORIZED
```

Those failures are not dead code in the scientific sense. They establish why the final treatment and authority boundary have their present form.

## Evidence routing

### Construction and preactivation isolation

- `construction/quotient_construction_audit.json` — same truth, quotient separation, and `F o q = F`.
- `construction/hardened_n_ladder_audit.json` — N0–N4 caller-capability noninterference.

### Environment and hidden-channel isolation

- `construction/E_ENVIRONMENT_MANIFEST.json`
- `construction/e_environment_audit.json`
- `construction/F_TREATMENT_ISOLATION_MANIFEST.json`
- `construction/f_treatment_isolation_audit.json`
- `construction/final_postgate_reaudit.json` — final consequence-grounded E/F surface.

### Future consequence grounding

- `construction/FUTURE_CONSEQUENCE_GROUNDING_CONTRACT.json`
- `construction/FUTURE_CONSEQUENCE_GROUNDING_KERNEL.py`
- `construction/FUTURE_CONSEQUENCE_WITNESSES.json`
- `construction/FUTURE_GROUNDING_DOMAIN.json`
- `construction/future_consequence_grounding_audit.json`

### Exact future executable and common cause

- `construction/FUTURE_EXECUTION_ARTIFACT_CONTRACT.json`
- `construction/FUTURE_EXECUTION_ARTIFACT_KERNEL.py`
- `construction/future_execution_artifact_audit.json`
- `construction/G_GROUNDING_INTEGRATION_MANIFEST.json`
- `construction/G_GROUNDING_INTEGRATION_KERNEL.py`
- `construction/g_grounding_integration_audit.json`

### Residual-confound adjudication

- `construction/H_MATERIAL_RIVAL_MANIFEST_GROUNDED.json`
- `construction/h_grounded_residual_audit.json`

### Freeze, authorization, and execution identity

- `construction/I_EVALUATION_RULE.json`
- `construction/I_EXECUTION_CLOSURE.json`
- `construction/I_REALIZED_RECORD_TEMPLATE.json`
- `construction/I_AUTHORIZED_FIRST_ENDPOINT_RUNNER_V2.py`
- `construction/I_FREEZE_PACKET_V7.json`
- `construction/I_FREEZE_ANCHOR_V7.json`
- `construction/I_AUTHORIZATION_CERTIFICATE.json`
- `construction/i_chain_of_custody_audit_v7.json`
- `evidence/I_CHAIN_OF_CUSTODY_PASS.md`

## Historical files in this directory

Several root-level and construction files intentionally describe earlier states:

- `AUTHORIZATION_REAUDIT.md`
- `AUTHORIZATION_REAUDIT_G_ADDENDUM.md`
- `AUTHORIZATION_REAUDIT_H_ADDENDUM.md`
- `H_REPAIR_CANDIDATE_STATUS.json`
- old post-gate semantic contracts/attacks;
- Packet 1–6 candidates and their rejection evidence;
- earlier I kernels/runners and failed fixture attack.

These are **preserved predecessors**, not alternate current configurations. They should not be deleted, renamed, or combined unless a later provenance audit establishes that they are outside every scientific identity and reproducibility requirement.

## Post-authorization interpretation is outside Packet 7

The blind outcome map and FSO theory live outside this directory's authorized execution object:

- [`../../research/post_authorization/VFA_0_2_BLIND_OUTCOME_ADJUDICATION.json`](../../research/post_authorization/VFA_0_2_BLIND_OUTCOME_ADJUDICATION.json)
- [`../../theory/FUTURE_SAFE_OPTION_STRUCTURE.md`](../../theory/FUTURE_SAFE_OPTION_STRUCTURE.md)

They may narrow later narrative interpretation. They cannot alter selection, grounding, execution, evaluation, or authorization.

## Stop condition

```text
PACKET_7_MUTATION = PROHIBITED
FUTURE_SELECTOR_PEEKING = PROHIBITED
POSTFREEZE_GUARD_ADDITION = PROHIBITED
OUTCOME_CONTINGENT_REPAIR = PROHIBITED
```

The next meaningful scientific information must come from the world.
