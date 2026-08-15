# CUHK-X P1 constitution evidence 🧊

## Terminal state

```text
IMPLEMENTATION_CONSTITUTED_NOT_YET_AUTHORIZED
```

This artifact records implementation constitution only. It does **not** authorize P1 scoring, a Kaggle submission, or any update to SSI Packet 7.

## Exact parent

The constitution branch was created from frozen P1 specification head:

```text
78d81a8727dc59b99a00f7706ad8cdcb01616fcc
```

The P1 scientific specification was not modified.

## Baseline reproduction

The harness binds the exact S1 script and archived V7 result lineage, reconstructs the frozen S1 HAU-multi V7F-or-V7 routing stream, and checks exact stream identity before any constitution result is admitted.

```text
S1 script SHA-256       = 38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f
V7 result ZIP SHA-256   = af7687fad3c7a4d140707c09dd84edea79288abdd81f91e9755d21cb63aad088
V7 script SHA-256       = 473d83342c680836badc0aa5232f32df5aecb7ae7d5755ec7986798eac13b544
subject-fold SHA-256    = 0ae2bd6a594152dd1af444566416410043ac11f153d20c8a517bb2a6d5052b73
HAU multi rows          = 809
candidate rows          = 3236
exact stream SHA-256    = 60bb4240da39e55f064a7eed7805f11d61e76f5539b0f9fe90251e2dbc3b7a9a
candidate stream SHA-256= 15a0b6501aa2f3ff34bafa69dc8144922ec57c97337282ffdad2af22925e5f18
BASELINE_REPRODUCTION   = PASS
```

The reported baseline metrics are frozen reproduction anchors only; no preserved-arm metric is computed.

## Constituted boundary

One shared blind candidate-evidence object is materialized from the already-frozen upstream evidence channels. It contains candidate identity, subject/fold, route/availability, and the pre-existing B5 pose+IMU, V7 IR, and V7F fused evidence margins. It contains no truth, label, correctness, or evaluator result.

```text
shared encoded SHA-256 = 146cd131634889be7a856be8c280276a4564d1b5e0b696fd57f85962ad9bda38
```

The arm transformation changes only the fixed three-slot `Z` active mask:

```text
EARLY_COMPRESSION   -> only frozen S1 routed evidence slot active
PRESERVED_EVIDENCE  -> all already-available evidence slots remain active
```

The evidence-sign matrix, candidate order, upstream evidence bytes, and non-Z runtime context remain fixed. The same arm-blind composer function consumes both representations. On the early arm it exactly reproduces the frozen S1 candidate stream.

## I1-I4

```text
I1 same shared encoded object     = PASS
I2 only declared Z boundary differs= PASS
I3 identical reasoner             = PASS
I4 no undeclared arm channel       = PASS
```

Key identities:

```text
early Z SHA-256        = b5307a8f337cec7a5722e3a86b8a07e9daee3f1dc06c2b57c621fc78a7511994
preserved Z SHA-256    = 066588dadea0b683647f50d111de010aac237a28e78032f2bdada26d01ae13b1
transform SHA-256      = 8012758ab213f586c0654ad9085c30b31ddfa3db82d308da4c4a4e9952801516
reasoner SHA-256       = 3d70eefebbe85e8988e75812e8911719023527c51e085d08feb01c22c16e58be
non-Z context SHA-256  = 26df2d7eeec8a6bfb67cab3a8902c13cd14fde322cde43d3b88df1f4efbe2f4a
```

I4 attacks the declared non-Z surfaces: files, tensor shape, memory-visible non-Z context, operation counts, RNG calls, prompt, external calls, logs, evaluator inputs, and timing. The committed harness uses one reasoner call in both arms, fixed tensor shape, zero RNG/external calls, no prompt, and no evaluator.

The authoritative timing attack passed its frozen gate. Five additional unchanged executions also ended in `IMPLEMENTATION_CONSTITUTED_NOT_YET_AUTHORIZED` with baseline, I1-I4, and G all PASS. The recheck artifact SHA-256 is:

```text
2be0b8a53e22f04463b85916e83cb116edbb20080783b5afa9844a45e0a429d0
```

## Frozen representation invariances G

All preregistered semantic-preserving attacks passed in both arms:

```text
record permutation            PASS
bijective field renaming      PASS
opaque identifier renaming    PASS
equivalent serialization      PASS
confidence serialization      PASS
```

Maximum confidence decode delta was `0.0`, within the frozen `1e-12` tolerance.

## Implementation identity

```text
harness Git blob SHA-1 = fb0f707b03fa468f0a16ae26d18acc951520a89d
harness SHA-256        = aaadc5f232dff14ea52caa179cfdba31f720e085097d5e02ceb81967247c55b1
authoritative status SHA-256 = 3fcc7b7704d1c694aeb3272ca69d9e1c99cba9016e42f5b1f4ee426f02ae9af6
```

An opaque digest of the preserved-arm prediction vector was recorded only to bind the constituted output without revealing or evaluating it:

```text
3d6376d15c855c8b8b2b3fdd088f50e5b31b99d4ab407ed54bf573bfc56db80e
```

No preserved prediction values are emitted by the evidence artifact, and no truth-conditioned preserved score was computed.

## Authority boundary

```text
SPECIFICATION         = FROZEN
IMPLEMENTATION        = CONSTITUTED
EXECUTION_AUTHORITY   = NONE
LEADERBOARD_AUTHORITY = NONE
PACKET7_AUTHORITY     = NONE
P1_A                  = NOT_EVALUATED
P1_B                  = NOT_EVALUATED
P1_C                  = NOT_EVALUATED
```

The only next admissible state transition is a separate execution-authorization decision over these frozen implementation bytes.
