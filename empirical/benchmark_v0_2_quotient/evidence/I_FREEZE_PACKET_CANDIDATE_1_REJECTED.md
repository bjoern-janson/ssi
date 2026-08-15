# I freeze packet candidate 1 — rejected before authorization

```text
PACKET_ID = VFA-0.2-FROZEN-PACKET-1
PACKET_SHA256 = f7f5ec1353e8fa5c5aeaa92abff3a7676aa4900478be3350134e067a7776e210
FREEZE_CANDIDATE_COMMIT = 962e41235852768505d7a0e626c748e766a51734
FREEZE_CANDIDATE_TIMESTAMP_UTC = 2026-08-15T18:17:44Z
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
STATUS = REJECTED_BEFORE_I_ADJUDICATION
```

The first hostile I review found two chain-of-custody weaknesses before any authorization certificate was issued.

1. The certificate validator required A-I PASS and packet/execution roots, but did not require the certificate's frozen `H_residual_set` to equal the packet's residual set.
2. The realized-record validator fixed the top-level schema but did not require exact nested key sets inside `realized` and `execution`. An undeclared future-populated control such as an alternative evaluator mode could therefore be introduced without literally overwriting a named frozen identity field.

These are predicate-I failures, not changes to A-H or to the scientific treatment. They localize to authorization/execution chain of custody.

Minimal repair:

- certificate must bind the exact packet residual set and critical rule identities;
- packet validation must bind critical top-level rule digests to unique packet-member roles;
- realized and execution blocks must have exact frozen schemas, not open maps;
- packet and certificate validation must operate from their loaded bytes so the guard can bind the manifest Git blob and certificate bytes rather than trusting pre-parsed caller objects.

Candidate 1 remains preserved and must never receive an authorization certificate. A repaired packet receives a new packet digest and a later freeze anchor.

No future obligation, future package, `T_future`, `J_future`, `DeltaPi`, or outcome was accessed during this rejection.
