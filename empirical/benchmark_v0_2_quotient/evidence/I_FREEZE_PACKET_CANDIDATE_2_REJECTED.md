# I freeze packet candidate 2 — rejected before authorization

```text
PACKET_ID = VFA-0.2-FROZEN-PACKET-2
PACKET_SHA256 = 514d0f87921ec574a803f8da537f9b693d2793b39578ba4e7bb9acff53e50fb9
EXECUTION_ROOT_SHA256 = 910024193a57e71706e8ed0e15b3338034c4c8b69ac3f78d30d10b68f55160f3
PACKET_MANIFEST_GIT_BLOB_SHA1 = c8eedbea4466dae2ee4e6cfea18c40623eccddfb
FREEZE_CANDIDATE_COMMIT = 4dc3b466af2f420e4a375d28eb37df5512edee70
FREEZE_CANDIDATE_TIMESTAMP_UTC = 2026-08-15T18:21:37Z
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
STATUS = REJECTED_BEFORE_I_ADJUDICATION
```

Candidate 2 repaired the candidate-1 authority gaps by binding the exact H residual set, critical rule roles, loaded packet bytes, and exact nested realized/execution schemas.

The second hostile review found one remaining completeness weakness before certificate issuance: the packet and authorization-certificate validators did not require exact top-level key sets (and packet member records did not require exact member key sets). A rehashed object could therefore remain structurally valid while carrying an undeclared top-level control field. The current execution code did not consume such a field, but predicate I's completeness requirement is stronger: no unrecorded configuration surface capable of later acquiring execution semantics may survive authorization.

The review also corrected an attack expectation: changing a packet member and recomputing the packet digest creates a new packet identity; that object need not be intrinsically malformed. It must instead fail under the existing authorization/freeze identity. Candidate 3 attacks the correct chain relation.

Minimal repair:

- exact packet top-level schema;
- exact packet-member schema;
- exact authorization-certificate schema;
- exact realized/execution schemas retained;
- certificate binds a content-addressed freeze-anchor record establishing packet-blob membership in the declared freeze commit/tree;
- mutated-and-rehashed packet is tested against the prior certificate/anchor rather than expected to fail parsing.

Candidate 2 must never receive an authorization certificate. No future obligation, package, `T_future`, `J_future`, `DeltaPi`, or outcome was accessed during this rejection.
