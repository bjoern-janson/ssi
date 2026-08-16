# Phase-V Provenance Scope

Status snapshot: 2026-08-16.

This note constrains how the Phase-V semantic-equivalence milestone may be interpreted.

## 1. Historical identity-side provenance

The V1→V8 handoff is preserved exactly as reconstructed research provenance in `../V1_V8_RECONSTRUCTED_HANDOFF.md`.

The later identity-side development summarized in `../BOTTLENECK_HISTORY.md` — including V8.4 extension-set analysis, E0/E1 controls, and the earlier E2-A identity result — is likewise **reconstructed research provenance unless and until exact pre-Phase-V contract/checker/witness artifacts are separately materialized**.

Therefore those historical entries must not be read as byte-complete executable evidence merely because the current Phase-V audit is executable.

## 2. Phase-V materialization boundary

The following artifacts are materialized in this lineage:

- `E2A_WORLD.json`
- `verify_moore_behavior.py`
- `E2A_MOORE_BEHAVIOR_RESULT.json`
- `E2A_MOORE_BEHAVIOR_AUDIT.md`
- `PHASE_V_SEMANTIC_EQUIVALENCE.md`
- `STATUS.json`

The E2-A world and the Moore semantic contract were fixed in the originating research process before the behavioral audit was interpreted, but their **first Git-materialized form appears in the same PR/commit lineage as the verifier and result**.

Accordingly, this repository supports:

```text
REPRODUCIBLE_FORMAL_AUDIT = YES
GIT_PREREGISTERED_BEFORE_RESULT = NO
```

Do not describe this object as a Git-preregistered experiment or as chain-of-custody evidence equivalent to VFA Packet 7.

The strongest authorized status remains:

```text
PHASE_V_BOUNDARY = DEMONSTRATED_IN_FROZEN_SYNTHETIC_FORMAL_SCOPE
```

not `EXTERNALLY_VALIDATED`, `PREREGISTERED`, or `GENERAL_VALIDATION`.

## 3. What the executable audit does establish

Given the committed E2-A world and committed Moore-behavior contract, the verifier deterministically computes the behavioral equivalence relation and checks its declared congruence scope.

That establishes a reproducible formal fact about this frozen object.

It does not establish:

- presentation-state identity;
- future sufficiency;
- cross-regime comparison;
- empirical external validity;
- historical byte-complete provenance for the identity-side V8.4/E0/E1/E2-A lineage.

## 4. Authority rule

> **Executable current evidence does not retroactively upgrade reconstructed historical provenance.**

And:

> **Reproducibility of a formal audit is not the same claim as preregistration of its inputs.**

These distinctions are permanent authority ceilings for the Phase-V milestone.
