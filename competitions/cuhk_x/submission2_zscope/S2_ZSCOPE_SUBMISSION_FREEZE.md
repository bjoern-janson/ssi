# CUHK-X Submission 2 — Z-scope external-transfer diagnostic

```text
submission_id        CUHKX_SUBMISSION_2_Z_SCOPE_EXTERNAL_DIAGNOSTIC
role                 ONE_SHOT_EXTERNAL_TRANSFER_DIAGNOSTIC
parent                CUHKX_SUBMISSION_1_V7_ROUTER
parent_S1_SHA256      38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f
main_script_SHA256    16533abbd43781c898e0a9488844ae1fb16c32eb29fa70416c4f481aa73fe781
package_SHA256        ffb9e912f632d3406cba07d2727d6f457d58416493ff777edc0fa44435eff318
local_generation      AUTHORIZED_IF_PRECHECK_PASSES
leaderboard           UNOBSERVED
AIM3_status            Z_CLOSED
P1_authority           NONE
Packet7_authority      NONE
```

## Frozen shot

Exactly one deployment axis differs from S1.

For HAU `emotion`, `single`, and `combination` only:

```text
if test pose + IMU are available:
    Z1 = [frozen pose, frozen IMU, frozen strong-IR]
    use the same S1 model family / decision rule on frozen common training support
else:
    exact S1 strong-IR fallback
```

Unchanged from S1:

```text
HAU multi
HAU sequence
HARn single
HARn object_interaction
random seed
thresholds
reference implementations
output grammar
```

No Q1/query-relative operator, architecture sweep, threshold tuning, P1 treatment, or Packet-7 dependency is included.

## Motivation without authority leakage

Historical AIM3 measured the same `Z0 -> Z1` substrate axis across emotion/single/combination and observed the descriptive response signature approximately

```text
(+0.02163, +0.01781, +0.02461)
```

with test-weighted OOF mass approximately `+0.01334`, below the frozen `+0.020` materiality gate; no branch reached `+0.03`. AIM3 therefore remained `Z_CLOSED`.

This shot does not reverse that gate. It uses the public leaderboard only as an external transfer observation of this exact fixed axis.

## Output contract

```text
cuhkx_submission2_zscope.csv
qa_id,prediction
682 rows
exact official test order
```

## Current execution state

The executable/package was statically audited and syntax-checked. Generation in the ChatGPT runtime stops at precheck because the official large CUHK-X archives and frozen local feature caches are not present there. The full generation package is preserved separately in `/CUHK-X/Submission2/` in the user Library.

No outcome-contingent repair is authorized inside this shot.
