# I freeze packet candidate 4 — rejected before authorization

```text
PACKET_ID = VFA-0.2-FROZEN-PACKET-4
PACKET_SHA256 = e2d602b51755b63949de654c192a67ee70ed3927de3f20f4cf3ae541a69db547
EXECUTION_ROOT_SHA256 = 602bee7b945fce614a34352949d884fdb197e25bb0b92592d796f22cf7838682
PACKET_MANIFEST_GIT_BLOB_SHA1 = 8f5bc1047a8fcb9da05e965b432376faa31c3ed3
FREEZE_CANDIDATE_COMMIT = 8a53be09a2544d8f3f7ab0700d1c2bf7d49254e9
FREEZE_CANDIDATE_TREE = ea8e963be0cd1015c7c5c168dd53f65c9660eba8
FREEZE_CANDIDATE_TIMESTAMP_UTC = 2026-08-15T18:39:25Z
FREEZE_ANCHOR_SHA256 = 9468e661cf0895b8cde830ed54f262fb894c02b433055c87afb2ee66d728b320
FREEZE_ANCHOR_GIT_BLOB_SHA1 = e7e651e696936b2a66ad70705fdab5757cff1921
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
STATUS = REJECTED_BEFORE_I_ADJUDICATION
```

Candidate 4 was the first packet to include a capability-minimal authorized first-endpoint runner and to bind that runner as a unique critical packet role.

The next coherence review found an internal execution-closure contradiction before certificate issuance:

- `I_AUTHORIZED_FIRST_ENDPOINT_RUNNER.py` correctly requires the realized canonical `GroundingEnvelope` bytes and a realized-G common-cause conformance certificate so future scientific statuses cannot be manufactured by editing duplicated fields in the realized record;
- `I_EXECUTION_CLOSURE.json` still allowed only the authorization certificate and realized record as post-freeze runner inputs.

Therefore the combined frozen object did not authorize its own complete input surface:

```text
RUNNER_REQUIRED_REALIZED_INPUTS
  = {authorization certificate, realized record, GroundingEnvelope, realized-G certificate}

FROZEN_CLOSURE_ALLOWED_REALIZED_INPUTS
  = {authorization certificate, realized record}
```

This is a predicate-I Frankenstein/coherence failure even though each component is locally defensible. Candidate 4 must never receive an authorization certificate.

Minimal repair: update only the execution-closure contract to admit the two additional content-addressed common-cause artifacts under their already-frozen G semantics, then create a new packet identity and rerun I.

No future obligation, package, `T_future`, `J_future`, `DeltaPi`, or outcome was accessed during this rejection.
