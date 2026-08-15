# Independent Future Adaptation Benchmark V0.1

## Scientific status

```text
BENCHMARK = CONSTRUCTION_AUDIT
A = PASS
B = PASS
C = PASS
D = FAIL
E = NOT_EVALUATED
F = NOT_EVALUATED
G = NOT_EVALUATED
H = NOT_EVALUATED
I = NOT_EVALUATED
FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
RUN = NOT_AUTHORIZED
V0.X_SYNTHETIC_LADDER = CLOSED
```

Machine-readable current adjudication:

```text
empirical/benchmark_v0_1/AUDIT_STATUS.json
```

The first A/B construction is blocked at predicate D: it separates corrective topology and matches the frozen present-state dimensions, but it already produces an ordinary-adaptation difference on an exhaustive pre-freeze surrogate universe. It is therefore **not eligible for the confirmatory future shot**.

## Question

Among systems matched on present capability and ordinary adaptability, does a preregistered difference in corrective topology predict adaptation to a genuinely new correction obligation?

The benchmark uses a prospective versioned-configuration migration domain. The external source, cutoff, admissible change class, first-qualifying-obligation rule, and observation horizon are fixed before any future obligation is disclosed.

## Scientific identity

The unit of confirmatory scientific identity is the eventual frozen packet:

```text
(Phi_A, Phi_B,
 Q_state_A, Q_state_B,
 Q_adapt_A, Q_adapt_B,
 H, R, H_residual,
 O_future_rule,
 evaluation_rule)
```

Construction, authorization, and execution are distinct objects.

```text
construction <= freeze < disclosure <= outcome
```

No future outcome may modify the confirmatory packet.

## Current evidence lineage

### A — prospective source and selector

`PASS`.

Biome (`biomejs/biome`) is the frozen external upstream source. The construction cutoff, stable baseline release, 180-day observation horizon, qualifying migration-change class, exclusions, and deterministic first-qualifying-release selector are recorded in:

```text
empirical/benchmark_v0_1/evidence/A_SCOPE_SOURCE.md
```

### B — treatment and Phi identity

`PASS`.

The construction retains the same six direct historical migration pairs and the same migration-class payload in A and B. A/B differ only in second-order cross-case analogy/provenance bindings. B uses one fixed deterministic weight-multiset scramble; the first specified seed was accepted without search.

Artifacts:

```text
empirical/benchmark_v0_1/evidence/B_SOURCE_MANIFEST.md
empirical/benchmark_v0_1/evidence/B_CONSTRUCTION.md
empirical/benchmark_v0_1/construction/MIGRATION_SIGNATURES.json
empirical/benchmark_v0_1/construction/BUILD_STATES.py
empirical/benchmark_v0_1/construction/state_A.json
empirical/benchmark_v0_1/construction/state_B.json
empirical/benchmark_v0_1/construction/phi_measurement.json
```

The frozen vector remains non-aggregated:

```text
(C_cover_pre, R_reconf, C_challenge, A_preserve, L_prov, R_reopen)
```

### C — present capability

`PASS` on the frozen current-state dimensions.

A/B exactly match case count, direct pair count, edge count, transformation-class count, known-pair availability, and topology-weight multiset.

### D — ordinary adaptation

`FAIL`.

The adversarial pre-freeze audit enumerates all 249 nonempty subsets of the eight frozen migration classes that are not exact historical case signatures. Both arms use the same resolver and the same two-neighbor budget.

```text
                         A                    B                 A-B
mean recovery recall     0.8646921017402945   0.8494979919678715   +0.015194109772423081
full recovery rate       0.4738955823293173   0.4497991967871486   +0.024096385542168697
full recovery count      118                  112                  +6
```

29 of 249 surrogate obligations differ.

Evidence:

```text
empirical/benchmark_v0_1/construction/PRE_FREEZE_AUDIT.py
empirical/benchmark_v0_1/construction/pre_freeze_audit.json
empirical/benchmark_v0_1/evidence/C_D_PRE_FREEZE_AUDIT.md
```

This means the current construction cannot rule out the rival explanation:

> A succeeds later because A was already a better ordinary analogical adapter before the future perturbation.

The shot is therefore stopped before freeze.

## Audit rule

A failed material predicate blocks the confirmatory shot. Passing earlier predicates does not compensate for D failure, and no later performance can repair the authorization defect.

E–I remain `NOT_EVALUATED` on this construction because D already blocks freeze and authorization.

## Files

- `DESIGN.md` — benchmark specification and frozen causal structure.
- `CONSTRUCTION_AUDIT.md` — A–I predicate definitions and authorization semantics.
- `AUDIT_STATUS.json` — current machine-readable adjudication.
- `evidence/` — predicate evidence and preserved failure lineage.
- `construction/` — pre-freeze construction and audit executables/artifacts only.

There is no future `RUNNER.py` and no future-result artifact.
