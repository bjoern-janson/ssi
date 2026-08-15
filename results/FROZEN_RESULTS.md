# Frozen Results and Artifact Lineage

This manifest records the frozen benchmark results and hashes currently recovered from the V0.x lineage. It is a provenance index, not a replacement for the benchmark artifacts themselves.

The V0.x ladder is closed. New empirical work should not mutate these frozen objects retroactively.

## V0.1

Executable:

```text
generative_probe_benchmark_v0_1.py
```

SHA-256:

```text
429a7e47b0ed29b6638c92b0127657ddc88b34de8799781c05a8b832d03056b5
```

Adjudication:

```text
V0.1 = MECHANISM_UNIT_TEST_PASS
```

## V0.2

Executable:

```text
generative_probe_benchmark_v0_2.py
```

SHA-256:

```text
90b61950827e8dff5f7772c02f8f48c74d4ad97522e551c55f97689e492fbddb
```

Adjudication:

```text
V0.2 = G1_PARTIAL_PASS
```

## V0.3

Executable:

```text
generative_probe_benchmark_v0_3.py
```

SHA-256:

```text
6e810715d9a2d8cd1a09361560a8cc0cd658572c89b2bd323a6b4fd147991654
```

Adjudication: strong G1 partial pass; $H/V$ separation not established.

## V0.4

Executable:

```text
generative_probe_benchmark_v0_4.py
```

SHA-256:

```text
3c8855f1daab1e392ca31fb7982d6a83d7728ef01809c06e9451b791eab8e3b3
```

Adjudications:

```text
V0.4_H/V_FACTORIZATION = PASS
V0.4_FRESH_VETO        = PASS
```

## V0.5

Executable:

```text
generative_probe_benchmark_v0_5.py
```

SHA-256:

```text
a851143e9123f04694c0f197054817ce79465de75f9e152334a9c90df147163d
```

Adjudications:

```text
V0.5_STRUCTURED_FUTURE_ROUTE_PRESERVATION = PASS
V0.5_ADAPTIVE_CONTRACTION_SUPERIORITY     = NOT_ESTABLISHED
```

## V0.6a

Executable:

```text
generative_probe_benchmark_v0_6a.py
```

SHA-256:

```text
570ce076f98e2e49b1235b7b7c12cd40ff950689b13638f0d59d2f2f86bdf450
```

Adjudication: resource-bounded Future Sufficiency passed; adaptive-retention superiority not established.

## V0.6b

Executable:

```text
generative_probe_benchmark_v0_6b.py
```

SHA-256:

```text
3e3bf738c473daaf456c86aadfb4521abbdf318f20d8d2187ee72ca2942a3cc7
```

Adjudication:

```text
V0.6b_TRANSITION_FS = STRONG_PARTIAL_PASS
```

## V0.6c

Executable:

```text
generative_probe_benchmark_v0_6c.py
```

SHA-256:

```text
a338942ccfa90f883f27775c8e74248eb42b1ddaa4ee4360d24b10100ba0eea1
```

Scientific summary:

```text
generative_probe_v0_6c_run_summary.json
SHA-256 68d28ac8d3852167f12f08d72692a408f7ab36054f6da3eed8a2555028524f96
```

Raw run:

```text
generative_probe_v0_6c_full_run.txt
SHA-256 2261a1ec219598f303fe6def9079df9fcebb8e19b090e02093d6c5f5923c444c
```

Adjudication:

```text
V0.6c_FS_SELECT = PASS
```

## V0.6d

Executable:

```text
generative_probe_benchmark_v0_6d.py
```

SHA-256:

```text
fac8c8c8ab91e91050d14fe0d82fd16128848b3050b44cb8deaec23fa2b4d6ba
```

Scientific result:

```text
TFS_T = 0.930
TFS_C = 0.257
TFS_S = 0.239
TFS_R = 0.236
```

Primary contrasts:

```text
delta_TFS_T_minus_C     = +0.673
delta_R_trans_T_minus_C = +0.43533333333333335
delta_TFS_T_minus_S     = +0.691
```

Run-summary artifact recovered during the current session:

```text
generative_probe_v0_6d_run_summary.json
SHA-256 e51ac5ea9a8bc7bfa18e56edf5240594e6c6230a5fdf5f9290b5caa7390c8e1f
```

Raw run:

```text
generative_probe_v0_6d_full_run.txt
SHA-256 ff947e08d57214c3481e37c3fe9d4671594b0d90062e33ab1bf679364dbd5511
```

Adjudications:

```text
V0.6d_SCALAR_INTERFACE_INSUFFICIENCY  = PASS
V0.6d_RELATIONAL_INTERFACE_SUFFICIENCY = PASS
RELATIONAL_SEMANTICS_DISCOVERY         = NOT_ESTABLISHED
```

## V0.7 — Relational semantics acquisition

Construction executable:

```text
generative_probe_benchmark_v0_7.py
```

SHA-256:

```text
8be8278b7a8215fe532ad9a49b6f7ac7f049f0d7bf2f7644b65faadae54ab993
```

Construction audit:

```text
generative_probe_v0_7_construction_audit.json
SHA-256 e1592b2799edd556001cc17784aa400a97bc89dcbd58313c32286dd61761587a
```

First scientific runner:

```text
generative_probe_v0_7_first_scientific_runner.py
SHA-256 c84af39a03bfc0f0a31a5bf76bea6acbf460e6e5eda34f54017f96f5428a4239
```

Scientific result:

```text
TFS_T      = 0.947
TFS_C      = 0.230
TFS_M      = 0.250
TFS_S      = 0.250
TFS_R      = 0.257
R_trans_T  = 0.9823333333333333
R_trans_C  = 0.4953333333333333
```

Primary contrasts:

```text
delta_TFS_T_minus_C          = +0.717
delta_R_trans_T_minus_C      = +0.487
delta_semantic_rank_corr_T_C = +0.9741808556987767
```

Scientific summary:

```text
generative_probe_v0_7_first_scientific_run_summary.json
SHA-256 ea31ba99b83c4ce946210d0fb43ea8b56c7160e652400f6250858799d8b77ea7
```

Raw run:

```text
generative_probe_v0_7_first_scientific_run.txt
SHA-256 1c5005d16685c9ced0d4bdf6988d20510292ffa0bdca09a0506ae2e8d1a0439f
```

Boundary:

```text
V0.7 != general semantic learning
V0.7 != general Future Sufficiency
V0.7 != mechanistic identification
```

## V0.7 Junction Diagnostic

Diagnostic executable:

```text
generative_probe_v0_7_junction_diagnostic.py
SHA-256 4437d587e0963496dd8cd1f56496c936b2e33be8b10c5a073a9b4e273cf5ea69
```

Failure decomposition:

```text
20 semantic-estimation failures
21 current-evidence ambiguity / premature commitment
12 point-reduction / authority failures
```

Summary:

```text
generative_probe_v0_7_junction_diagnostic_summary.json
SHA-256 8d50be96919003d4d07729ce49d1b89a6368ca57126b7245d0d4cb843da6c642
```

Full diagnostic:

```text
generative_probe_v0_7_junction_diagnostic_full.json
SHA-256 a9981dc85e810dc399b050204f4a1c86a70ac0146e15cee1a1abd3a5ecaf71fe
```

Authority: post-hoc diagnostic only; confirmatory CCA/CARS claim not authorized from this object alone.

## V0.8 — Evidence to authority

Frozen construction/preregistration:

```text
v0_8_evidence_to_authority.py
SHA-256 30834e0791220ceccb36ffa6c34a964e03408bdfa389259b1155381eb71ccee9
```

Construction audit:

```text
v0_8_evidence_to_authority_construction_audit.json
SHA-256 f25b0b7a829211f6e51b1403458e0a28374a47f4bfc528badcda4864bb4cdab7
```

Scientific runner:

```text
v0_8_evidence_to_authority_scientific_runner.py
SHA-256 73f0c97db3b59503ae066be022ecf3b4a805c3bbbe2f99f76f2c587640c2f98e
```

Fresh scientific run: 1000 matched quartets, preregistered namespace-separated execution.

### D3 — point compression

```text
A_auth P1 = 0.476
A_auth P2 = 1.000
A_auth P3 = 1.000
H_future P1 = 0.8253333333333334
H_future P2 = 1.000
H_future P3 = 1.000
```

### D2 — authority overreach

For both ambiguous factorial cells:

```text
A_auth P1 = 0
A_auth P2 = 0
A_auth P3 = 1
bad_commit P1/P2 = 0.524
bad_commit P3 = 0
STOP P3 = 1
H_future P1/P2 = 0.8253333333333334
H_future P3 = 1
```

Forced policies achieved accidental future-safe outcomes in 476/1000 ambiguous worlds while still having $A_{\rm auth}=0$.

All preregistered directional gates passed.

Scientific summary:

```text
v0_8_evidence_to_authority_scientific_run_summary.json
SHA-256 e5ce445a5209cdb2a9ddda9a439f77204575980c119c871aad75ccd569b77d21
```

Full run:

```text
v0_8_evidence_to_authority_scientific_run_full.json
SHA-256 2486a7cbdb428376b01452e0420e96e309a7137a9a857d0df2fa8bde792c2175
```

Adjudications:

```text
V0.8_D3_EVIDENCE_COMPRESSION      = PASS
V0.8_D2_AUTHORITY_OVERREACH       = PASS
V0.8_AUTHORITY_OUTCOME_SEPARATION = PASS
V0.8_EVIDENCE_TO_AUTHORITY        = PASS
```

# Status

```text
V0.x = CLOSED
LOCALIZATION_CALCULUS = ESTABLISHED_IN_CONTROLLED_CONSTRUCTIONS
NEXT_MAJOR_OBJECT = INDEPENDENT_FUTURE_ADAPTATION
```

Future changes should add new artifacts rather than revise these adjudications post hoc.
