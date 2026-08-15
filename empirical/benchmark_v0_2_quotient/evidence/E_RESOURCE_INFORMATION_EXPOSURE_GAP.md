# Predicate E gap — Resource, information, and exposure symmetry

## Adjudication

```text
E = NOT_EVALUATED
```

This artifact records why predicate E cannot yet be adjudicated for `VFA-0.2-QUOTIENT-REVISION-TOPOLOGY`.

It is a gap record, not evidence that E passes or fails.

## What is already established

The quotient construction and hardened preactivation audit establish:

- one identical validated substrate for A/B;
- identical 24 path records;
- identical canonical Gamma byte length;
- identical ordinary forward implementation and state;
- exact ordinary full-trace equality over 249 pre-freeze surrogate tasks;
- preactivation metamorphic invariance under 101,592 comparisons;
- closed caller-capability surface under `PREACTIVATION_CALLER_V1`.

These facts constrain preactivation asymmetry but do not constitute the full resource/information/exposure contract required by predicate E.

## Missing frozen manifest

Before E can be adjudicated, one content-addressed manifest must specify A and B side by side for every non-treatment resource and exposure field.

Required fields:

```text
runtime/interpreter version
dependency/environment versions
compute budget
memory/context/storage budget
Gamma storage/materialization representation
post-gate probe-generation budget
adaptation/update budget
wall-clock and/or deterministic operation-count limit
tool/API permissions
pre-freeze data-access manifest
future-disclosure documentation/evidence contract
evaluator implementation/version/access
randomness policy and seeds, if any
cache policy
concurrency/process policy
stopping rule
failure/timeout/abstention handling
```

## Why 3189 / 3189 bytes is insufficient

Equal canonical serialization length does not prove equal:

- allocation cost;
- traversal cost;
- materialization cost;
- in-memory representation;
- cache behavior;
- operation count after activation;
- evaluator exposure;
- total correction budget.

Those quantities can be consequences of representation or runtime choices even when serialized payload lengths are equal.

## Treatment boundary

The intended treatment is the quotient over revision-path equivalence classes:

```text
W_A = W_B
path_records_A = path_records_B
Gamma_B = q(Gamma_A)
```

Predicate E must freeze all remaining capacity and exposure variables around that treatment. It must not erase genuine mechanistic consequences of the quotient by normalizing treatment effects away, but it must prevent extra compute, memory, tools, evidence, or evaluator access from becoming alternative explanations.

## Stop condition

Until the complete manifest exists and is mechanically compared:

```text
E = NOT_EVALUATED
F = NOT_EVALUATED
G = NOT_EVALUATED
H = NOT_EVALUATED
I = NOT_EVALUATED
FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
G_ACTIVATION = PROHIBITED
FUTURE_RUN = NOT_AUTHORIZED
```
