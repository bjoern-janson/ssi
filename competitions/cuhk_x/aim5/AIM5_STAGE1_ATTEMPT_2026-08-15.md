# CUHK-X AIM5 — Stage 1 input-staging attempt (2026-08-15)

**Purpose:** execute Stage 1 mechanical precheck only.  
**Outcome:** `NOT_RUN_FROZEN_INPUT_BOUNDARY_UNAVAILABLE`  
**AIM5 status remains:** `MECHANICAL_PRECHECK_PENDING`.

This is **not** a failed AIM5 precheck and carries no negative authority about the AIM5 implementation or hypothesis. The mechanical precheck could not begin because the exact frozen input bundle could not be constituted in the available execution environment.

## Frozen Stage 1 requirement

Stage 1 requires byte-identical copies of:

```text
cuhkx_submission1.py
Training-20260813T154030Z-1-002.zip
cuhkx_v7_ir_dinov2_cache/features.npz
cuhkx_b2_hau_pose_cache/features.npz
cuhkx_b4_imu_v2_cache/features.npz
cuhkx_v7_strong_ir_dinov2_results.zip
cuhkx_aim4_structured_set.py
cuhkx_aim5_conditional_setmap.py
cuhkx_aim5_precheck.py
```

The first six data/provenance inputs are hash-gated by the frozen AIM4/AIM5 loaders.

## Inputs recovered and verified

From the ChatGPT Library:

```text
cuhkx_submission1.py
SHA-256 = 38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f
STATUS  = exact frozen S1 byte match

cuhkx_v7_strong_ir_dinov2_results.zip
SHA-256 = af7687fad3c7a4d140707c09dd84edea79288abdd81f91e9755d21cb63aad088
STATUS  = exact frozen V7 results byte match
```

The Library contains one unrelated file named `features.npz`:

```text
SHA-256 = b28cecfede3690a67ecd75bbe34d18a2f3f463157f7a2289c5ec47bb25b6e217
keys    = X, y, folds, subjects, units
X shape = (2927, 3782)
```

It is **not** any frozen AIM5 cache. In particular it does not match:

```text
V7 cache expected  = e9699696af7d886896df7fa1e52d2b28ecfbb8abeef71a6b3b2ee04a68abb5db
pose cache expected = d7e609a5e8a9ebc4bbdda92f8fe601d8b0c6ccfd4a2757f9a632a1ac9211b89a
IMU cache expected  = 8c4656e2c76029783c18d0b76f92f58fa8165a786a7049c3be7bf90a28aa0234
```

Existing B2/B4/B5 result ZIPs in the Library were inspected as possible recovery sources. They contain result tables/specifications but do not contain the frozen feature-cache bytes.

## Inputs unavailable in the current execution environment

```text
Training-20260813T154030Z-1-002.zip
  expected SHA-256 = 667a00cb03ec67e1eeb49a744cb4fc764878fadae0b35ea873e25c2f7b3868bc

cuhkx_v7_ir_dinov2_cache/features.npz
  expected SHA-256 = e9699696af7d886896df7fa1e52d2b28ecfbb8abeef71a6b3b2ee04a68abb5db

cuhkx_b2_hau_pose_cache/features.npz
  expected SHA-256 = d7e609a5e8a9ebc4bbdda92f8fe601d8b0c6ccfd4a2757f9a632a1ac9211b89a

cuhkx_b4_imu_v2_cache/features.npz
  expected SHA-256 = 8c4656e2c76029783c18d0b76f92f58fa8165a786a7049c3be7bf90a28aa0234
```

Searches of the ChatGPT Library and connected Google Drive did not recover the missing byte-identical inputs. No Kaggle connector/execution plugin is available in this session, and the current runtime has no authenticated Kaggle credentials.

## Adjudication

Because the frozen byte boundary cannot be staged:

```text
MECHANICAL_PRECHECK = NOT_RUN
PRECHECK            = NOT_IDENTIFIED
RUN_AUTHORIZATION   = NOT_AUTHORIZED
AIM5_RUN            = PROHIBITED
```

Do **not** reinterpret this as:

```text
PRECHECK = FAIL
AIM5 = NOT_SUPPORTED
```

No AIM5 invariant has yet been tested against the complete frozen substrate.

## Next admissible transition

Obtain the byte-identical historical private AIM2/AIM5 cache inputs (or the already-created private Kaggle dataset containing them) in an execution environment that also has the official Training ZIP, verify all frozen hashes, then run:

```text
cuhkx_aim5_precheck.py
```

and stop.

Only a completed precheck may produce:

```text
cuhkx_aim5_precheck_report.json
PRIVATE_BUNDLE_SHA256
AIM5_PRECHECK_SHA256
```

and advance the state to `BYTE_FREEZE_PENDING`.
