# I freeze packet candidate 5 — rejected before authorization

```text
PACKET_ID = VFA-0.2-FROZEN-PACKET-5
PACKET_SHA256 = b5caceac0d1d5471f2796948dbb31faf69804dc2071a208d4268d6465240b178
EXECUTION_ROOT_SHA256 = 9f2a48d1169af616394f7044ed7a1dcd7bb5b3676429049d9bd34cde70931542
PACKET_MANIFEST_GIT_BLOB_SHA1 = b5d875d2579cf044c107fb940db7ff46e0421df3
FREEZE_CANDIDATE_COMMIT = cf7bf73f36d83d7b60c0a7dbfc084ec99e88abc0
FREEZE_CANDIDATE_TREE = dc95c846e9f8aabd4d81e324831231e8d41739ca
FREEZE_CANDIDATE_TIMESTAMP_UTC = 2026-08-15T18:42:05Z
FREEZE_ANCHOR = NOT_ISSUED
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
STATUS = REJECTED_BEFORE_I_ADJUDICATION
```

Candidate 5 repaired the candidate-4 execution-closure contradiction: the frozen closure and authorized runner agree that the only post-freeze runner inputs are the authorization certificate, exact realized record, canonical GroundingEnvelope, and content-addressed realized-G conformance certificate.

Before a freeze anchor was issued, the identity review found a smaller but real implementation defect in the custody guard: `validate_freeze_anchor` still required an anchor path ending in `I_FREEZE_PACKET_V4.json`. Thus a valid successor packet could not be anchored by the supposedly generic chain-of-custody implementation.

This is a predicate-I identity failure. It does not affect A-H, treatment semantics, future grounding, or the authorized execution surface.

Minimal repair:

- derive the expected frozen packet filename from the packet ID rather than a hard-coded predecessor version;
- require rejected predecessor packet IDs and digests to be unique and sequentially preserved;
- create a new packet identity after the guard repair.

Candidate 5 must never receive a freeze anchor or authorization certificate. No future obligation, package, `T_future`, `J_future`, `DeltaPi`, or outcome was accessed during this rejection.
