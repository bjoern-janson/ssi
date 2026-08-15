# CUHK-X — recovered state before Submission 2

**Recovery date:** 2026-08-15  
**Status:** recovered from the recent-chat/Library lineage and checked against `bjoern-janson/future-sufficiency`; continuation now lives in `bjoern-janson/ssi`.

This file is a handoff ledger. It does not retroactively authorize a second leaderboard submission and does not reinterpret closed experiments.

---

## 1. External shot S1

The first external competition shot was:

```text
S1 public score = 0.49122
observed rank    = 50 / 132
```

The later frozen exact-row OOF replay was:

```text
S1 OOF proxy     = 0.5049003832
public - OOF     = -0.0136803832
```

The rebound was therefore treated as broadly consistent with the frozen internal capability rather than as evidence of a large hidden-test collapse.

### Exact-row branch diagnostic

| Branch | OOF exact | Test rows | Oracle error mass |
|---|---:|---:|---:|
| HAU emotion | 0.3004 | 144 | 0.14772 |
| HAU multi | 0.3696 | 144 | 0.13311 |
| HAU single | 0.5711 | 144 | 0.09056 |
| HAU combination | 0.7038 | 139 | 0.06037 |
| HAU sequence | 0.3961 | 39 | 0.03453 |
| HARn single | 0.6737 | 51 | 0.02440 |
| HARn object | 0.8571 | 21 | 0.00440 |

This established that the dominant unresolved competition mass was concentrated in HAU, especially emotion and multi.

Important metric firewall:

```text
candidate-level balanced accuracy != Kaggle exact-answer-row accuracy
```

For example, the V7 HAU-multi matched-support exact-set result was about `0.37405`, while S1 HAU-multi exact OOF was about `0.36959`; V7's roughly `0.75` figure was candidate-level balanced accuracy and must not be compared directly to the leaderboard metric.

---

## 2. Closed representation ladder through V7

The prior CUHK-X aiming ladder was closed at V7:

```text
B0 -> B5 -> B6/V1/V5 -> B7/B8/V2/V3/V6 -> V4 -> V7
```

Earned interpretation:

- B5: material measurement complementarity.
- B6/V1/V5: additional channels preserved nonredundant distinctions.
- B7/B8/V2/V3/V6: complementarity did not imply successful exploitation/fusion.
- V4: a diagnosed representation problem did not prescribe its repair.
- V7: a stronger representation/interface materially changed what was accessible from fixed IR measurement.

V7 fixed-measurement result:

```text
X_IR fixed
O_cheap != O_DINOv2
candidate balanced accuracy ~0.66557 -> ~0.75092
all five held-out-subject folds positive
```

Licensed compression:

> Complementarity identifies potentially recoverable missing distinctions; it does not identify the mechanism required to make those distinctions usable.

and:

```text
X_fixed does not imply Z_accessible fixed.
```

V7 did not add new world measurement; it changed what could be recovered from already measured IR.

---

## 3. AIM2 — query-relative lever

AIM2 tested the exact 2x2 on HAU emotion over the frozen 786-unit common support:

```text
                 Q0 global-first       Q1 query-relative
Z0 V7 IR              Y00                   Y01
Z1 V7 IR+B5            Y10                   Y11
```

`Q1` was the frozen `QUERY_RELEVANCE_GATED_OVR` intervention. It changed training support/factorization only; it did not add a sensor, external model, semantic embedding, threshold, or larger output vocabulary.

`Z1` added the frozen B5 pose+IMU representation to V7 IR.

### AIM2 result

```text
Y00 = 0.2888
Y01 = 0.2392
Y10 = 0.3104
Y11 = 0.2430

Delta_Q  = -0.04962
Delta_Z  = +0.02163
Delta_ZQ = -0.01781
```

For the primary Q contrast:

```text
95% CI(Delta_Q) = [-0.0806, -0.0210]
all five emotion folds negative
```

Cross-branch Q response signature over emotion/single/combination:

```text
r_Q = (-0.07169, -0.06304, +0.00506)
test-weighted delta mass = -0.02742
```

Frozen adjudication:

```text
QUERY_RELEVANCE_GATED_OVR = CLOSED
AIM2_Q  = CLOSED
AIM2_Z  = POSITIVE_BUT_SUBMATERIAL
AIM2_ZQ = NO_INTERACTION_GAIN
shared Q candidate = FALSE
S2 = NOT_AUTHORIZED
```

Do **not** rewrite this as “query-relative sufficiency is false.” Only the constituted Q1 implementation was closed.

### Frozen AIM2 lineage hashes

```text
S1 script:
38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f

training ZIP:
667a00cb03ec67e1eeb49a744cb4fc764878fadae0b35ea873e25c2f7b3868bc

V7 cache:
e9699696af7d886896df7fa1e52d2b28ecfbb8abeef71a6b3b2ee04a68abb5db

pose cache:
d7e609a5e8a9ebc4bbdda92f8fe601d8b0c6ccfd4a2757f9a632a1ac9211b89a

IMU cache:
8c4656e2c76029783c18d0b76f92f58fa8165a786a7049c3be7bf90a28aa0234

AIM2-v2 executable:
6090c230339280573fb997c1c6bc89bf2050cd9a2cf7a683e73be55ca600c2a4
```

---

## 4. AIM3 — Z scope

Because AIM2 left a small positive `Z0 -> Z1` emotion contrast, AIM3 held `Q=Q0` fixed and tested whether the same substrate perturbation recurred materially across emotion, single, and combination.

Frozen scope gates:

```text
branch positive threshold       = +0.030
nonnegative folds required      = 4 / 5
material adverse threshold      = -0.030
pooled test-weighted mass gate  = +0.020
```

Historical emotion anchor required exact reproduction:

```text
Z0 = 0.28880407124681934
Z1 = 0.3104325699745547
Delta = +0.021628498727735368
```

### AIM3 result

```text
r_Z = (+0.02163, +0.01781, +0.02461)
       emotion     single      combination

pooled test-weighted delta mass = +0.01334 < +0.020
branches reaching +0.030        = 0 / 3
```

Frozen adjudication:

```text
classification = Z_CLOSED
S2 = NOT_AUTHORIZED
```

The recurring positive sign remains diagnostic/generative evidence, but it did not earn a reusable competition intervention:

```text
consistent sign != material shared substrate scope
```

Recovered interpretation:

```text
G_opt  = 0
G_diag > 0
G_gen  > 0
```

The AIM3 result artifact was recorded with SHA-256:

```text
bb8b7d1ad8e85213f299f3a934e9e528b4b7f005af6842a11dad962fcd59c20f
```

---

## 5. What was deliberately outside AIM2/AIM3

HAU `multi` was excluded from AIM2 because its already-characterized failure geometry was different:

```text
candidate-decision error
        -> conjunctive exact-set amplification
        -> exact-answer-row failure
```

The AIM2 freeze explicitly anticipated that any broad #1 architecture would need to be recomposed with a **separately earned multi intervention** plus residual branch improvements.

No recovered artifact freezes an AIM4 or a specific post-AIM3 multi repair. Therefore the scientific/competition state is:

```text
Q1 family tested here       = CLOSED
shared Z scope tested here  = CLOSED
S2                           = NOT_AUTHORIZED
HAU multi locus              = OPEN
post-AIM3 repair mechanism   = NOT_YET_FROZEN
```

That distinction matters: the next competition step may target the open multi locus, but this recovery ledger does not manufacture a preregistered intervention that did not previously exist.

---

## 6. Competition-shot discipline

The prior operating rule is retained:

> A submission is a shot taken.

Offline work is aiming/construction; the leaderboard is an external rebound.

Every external submission should either move the game or improve the map, ideally both. Diagnostic, competitive, and hybrid shots are distinct; when the map is mature, a hybrid shot is preferred.

The next external S2 shot must therefore be earned by a frozen internal candidate. Closed AIM2/AIM3 candidates cannot be silently recycled into S2.

---

## 7. Recovered source locations

Competition-specific artifacts recovered from the Library include, among others:

```text
/CUHK-X/Submission1/cuhkx_submission1.py
/CUHK-X/Submission1/S1_FREEZE.md
/CUHK-X/Submission1/S1_MANIFEST.json
/CUHK-X/Submission1/Diagnostic1/cuhkx_s1_exact_diagnostic.py
/CUHK-X/Submission1/Diagnostic1/S1_EXACT_DIAGNOSTIC_FREEZE.md

cuhkx_aim2_query_relative_v2.py
AIM2_QUERY_RELATIVE_FREEZE.md
CUHKX_AIM2_v2_Kaggle_Runner.ipynb
CUHKX_AIM2_KAGGLE_README.md
CUHKX_AIM3_Z_SCOPE_EXECUTION_CELL.py
```

The historical `future-sufficiency` repository was checked as a context source; the competition continuation is now intentionally moved to this SSI module.

No organizer dataset, media, or derived feature cache is copied into this repository by this recovery step.
