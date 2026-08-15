# VFA-0.2 — Dormant Corrective Reserve

## Lineage identity

```text
VFA-0.1-REJECTED_RETRIEVAL_LEAKAGE
    ->
VFA-0.2-DORMANT-CORRECTIVE-RESERVE
```

VFA-0.2 is a **new construction lineage**, not a repaired scramble seed.

The VFA-0.1 construction showed that genuine similarity/provenance topology changed precedent retrieval and therefore ordinary adaptability before any future obligation. That construction remains preserved and rejected at D.

VFA-0.2 factorizes the causal object:

\[
\mathcal K_t=(R_t,F_t,D_t)
\]

with the intended construction

\[
R_t^A=R_t^B,\qquad
F_t^A=F_t^B,\qquad
D_t^A\ne D_t^B.
\]

`D_t` is dormant corrective reserve structure: provenance, challenge, alternative-preservation and reopenability relations. It is **not** extra compute, extra candidate count, a larger search budget, or a better ordinary retrieval policy.

## Defining invariant

> **VFA-0.2 is not allowed to demonstrate treatment advantage before reserve activation.**

Formally,

\[
G_{\rm reserve}=0
\Rightarrow
\frac{\partial T_{\rm forward}}{\partial D}=0
\]

and

\[
G=g(E_{\rm insuff}),
\qquad
\frac{\partial G}{\partial D}=0.
\]

Thus two upstream leak paths are independently prohibited:

\[
D\nrightarrow T_{\rm forward},
\qquad
D\nrightarrow G.
\]

The reserve may enter the causal graph only after shared, independently grounded evidence establishes insufficiency of the shared current route.

## Current construction status

```text
LINEAGE = VFA-0.2-DORMANT-CORRECTIVE-RESERVE
FUTURE_OBLIGATION_ACCESSED = FALSE
N_TRACE = PASS
N_GATE = PASS
Q_ADAPT_EQUIVALENCE = PASS
RESERVE_PAYLOAD_SYMMETRY = PASS
SEP_PHI_RESERVE = PASS
D_PRE_ACTIVATION = PASS

FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
FUTURE_RUN = NOT_AUTHORIZED
```

This is **not** an A-I authorization certificate. It is the first construction-level noninterference result for the VFA-0.2 lineage.

## Pre-activation result

The leakage suite uses the inherited frozen Biome migration-class corpus and the same genuine forward retrieval topology for both arms.

Across the exhaustive 249-task pre-freeze surrogate universe:

- A/B use the same forward state and same solver;
- 10 reserve presentations/mutations are attacked per task (5 based on each arm);
- total forward-trace comparisons: **2,490**;
- material trace mismatches: **0**;
- gate mismatches: **0**;
- `Q_adapt` is exactly equal;
- reserve A/B retain the same nodes, edge count, edge-kind multiset, and canonical serialized byte length;
- reserve topology separates on `C_challenge`, `L_prov`, and `R_reopen`;
- `A_preserve` remains equal at `1.0` because both arms retain the same alternative quantity.

The reserve therefore separates structurally while remaining causally inaccessible to ordinary forward operation in this construction.

## Architectural boundary

`forward_trace(query, shared_forward)` has **no reserve argument**.

`evaluate_gate(evidence)` has **no reserve argument**.

The sole reserve-dereference function is `activate_reserve(evidence, reserve_handle)`, and it raises `ReserveClosed` while `G=0`.

The leakage suite additionally parses the implementation AST and checks the forward/gate function signatures for reserve-capable symbols.

## Frozen trace equivalence

Ordinary-operation equivalence is trace-level, not endpoint-only:

\[
T_A(x)\equiv_{\mathcal T_{\rm prereg}}T_B(x).
\]

The trace fields and admissible equivalence relation are frozen in `construction/TRACE_EQUIVALENCE.json`. The current relation is `IDENTITY_ONLY`; no result-dependent normalization is permitted.

## Files

- `CONSTRUCTION_INVARIANTS.md` — causal and adjudication invariants.
- `construction/SHARED_FORWARD.json` — common ordinary forward state.
- `construction/reserve_A.json` / `reserve_B.json` — equal-quantity, different-binding dormant reserves.
- `construction/reserve_interface.py` — architectural gate boundary.
- `construction/TRACE_EQUIVALENCE.json` — frozen trace identity.
- `construction/GATE_SPEC.json` — arm-independent insufficiency gate.
- `construction/PREACTIVATION_LEAKAGE_SUITE.py` — adversarial construction audit.
- `construction/preactivation_leakage_audit.json` — machine-readable result.

## Stop condition

No prospective future obligation is to be inspected, selected, simulated, or executed from this lineage yet.

The current result licenses only the next construction-audit question: whether this reserve factorization survives broader adversarial implementation review and the remaining authorization predicates.
