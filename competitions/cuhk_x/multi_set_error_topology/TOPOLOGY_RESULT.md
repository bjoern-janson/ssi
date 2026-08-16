# CUHK-X Multi Set-Error Topology — frozen result

```text
DIAGNOSTIC_ID = CUHKX-MULTI-SET-ERROR-TOPOLOGY-1
MODEL_AUTHORITY = NONE
TREATMENT_AUTHORITY = NONE
P2_AUTHORITY = NONE
CAUSAL_MECHANISM = NOT_IDENTIFIED
```

## Input identity

- P1 raw result SHA-256: `b3429ee3d9737a98cd4ded5865ffd1d519c812c03b77563c172c98cb2c64e248`
- P1 metrics SHA-256: `f432d854c0973647071db771638191259623ad8a8a9ddff31fb25b3c29680488`
- 809 HAU/multi QA rows, 3,236 candidate rows.

The first local diagnostic execution stopped before permutation/result generation because the frozen P1 exact metric was addressed at `metrics[arm][exact_set_accuracy]` rather than its actual retained path `metrics[arm][qa][exact_set_accuracy]`. Only that JSON lookup path was repaired. The frozen diagnostic specification, null, input hashes, topology definitions, permutation count, seed, and authority ceiling were unchanged.

## D0 — observed topology

| class | Early | Preserved | Delta |
|---|---:|---:|---:|
| E: exact | 299 / 36.9592% | 311 / 38.4425% | +12 / +1.4833 pp |
| U: under-inclusive only | 178 / 22.0025% | 168 / 20.7664% | -10 / -1.2361 pp |
| O: over-inclusive only | 207 / 25.5871% | 218 / 26.9468% | +11 / +1.3597 pp |
| M: mixed FN+FP | 125 / 15.4512% | 112 / 13.8443% | -13 / -1.6069 pp |

Additional movement:

```text
mean FN                  0.459827 -> 0.425216   delta -0.034611
mean FP                  0.508035 -> 0.505562   delta -0.002472
mean Hamming set error   0.967862 -> 0.930779   delta -0.037083
signed set-size error    0.048208 -> 0.080346   delta +0.032138
full-set recovery        0.625464 -> 0.653894   delta +0.028430
exact-set accuracy       0.369592 -> 0.384425   delta +0.014833
P(O)=full-exact          0.255871 -> 0.269468   delta +0.013597
```

The +23 QA increase in full-set recovery decomposes exactly into +12 exact rows and +11 over-inclusive-only rows.

## D1 — class transitions

Counts, early row -> preserved column:

| early \\ preserved | E | U | O | M |
|---|---:|---:|---:|---:|
| E | 279 | 3 | 17 | 0 |
| U | 18 | 155 | 0 | 5 |
| O | 14 | 2 | 190 | 1 |
| M | 0 | 8 | 11 | 106 |

These are descriptive transitions only.

## D2 — frozen candidate-error null

Primary null: independently permute candidate correctness within every `(subject, option_position, truth_label)` stratum, thereby preserving subject difficulty, option-position difficulty, positive/negative candidate difficulty, and exact stratum marginal correctness while destroying within-QA cross-candidate coupling.

```text
N_PERM = 50,000
SEED   = 260816
```

Early:

```text
Q_exact observed         = 0.3695920890
Q_fact deterministic     = 0.3345309654
permutation mean         = 0.3345034363
95% interval             = [0.3152039555, 0.3535228677]
location                 = ABOVE_FACTORIZED_95
R_joint                  = +0.0350611236
```

Preserved:

```text
Q_exact observed         = 0.3844252163
Q_fact deterministic     = 0.3486960905
permutation mean         = 0.3487336959
95% interval             = [0.3300370828, 0.3683559951]
location                 = ABOVE_FACTORIZED_95
R_joint                  = +0.0357291258
```

## D3 — what remains after candidate marginals

```text
Delta Q_exact observed   = +0.0148331273
Delta Q_fact             = +0.0141651251
Delta R_joint            = +0.0006680022
```

Thus the P1 exact-set movement is nearly reproduced by the frozen factorized candidate-error null. Both arms show positive within-QA correctness dependence relative to the factorized reference; the diagnostic does not identify the cause of that dependence. Latent QA difficulty, answer-set structure, or other unmodeled dependence remain possible.

## Authority-preserving conclusion

The diagnostic does **not** identify an excess joint-composition penalty. It also does not prove joint composition is irrelevant. It establishes only that:

1. P1 primarily reduced false negatives / missing required options while false positives changed little.
2. The resulting increase in complete true-set recovery split into exact and over-inclusive outcomes.
3. Exact-set accuracy in both arms exceeded the frozen factorized candidate-error reference.
4. The P1 change in exact-set accuracy required almost no additional change in the residual beyond candidate marginals (`Delta R_joint = +0.000668`).

Therefore no joint decoder, CARS/CCA mechanism, richer representation, or P2 intervention is authorized by this diagnostic alone.
