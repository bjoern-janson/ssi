# B Evidence — Treatment and Phi Identity

## Adjudication

```text
B = PASS
```

This predicate concerns only treatment identity and pre-disclosure corrective-topology measurement. It does **not** establish present-capability equivalence (C), ordinary-adaptation equivalence (D), treatment isolation from every hidden asymmetry (F), or future predictive consequence.

## Frozen construction lineage

The historical source universe was frozen first in:

```text
empirical/benchmark_v0_1/evidence/B_SOURCE_MANIFEST.md
```

No post-cutoff Biome object and no realized future-obligation information enters the construction.

The construction artifacts are:

```text
empirical/benchmark_v0_1/construction/MIGRATION_SIGNATURES.json
empirical/benchmark_v0_1/construction/BUILD_STATES.py
empirical/benchmark_v0_1/construction/state_A.json
empirical/benchmark_v0_1/construction/state_B.json
empirical/benchmark_v0_1/construction/phi_measurement.json
```

Local construction SHA-256 values at adjudication:

```text
MIGRATION_SIGNATURES.json = d1db43698a36e0ab84226c7a0fb44a48ea03759a5724d63c9c4225195d949c53
BUILD_STATES.py          = 02650aaf2a2c41f7235682582996478670a3f8e06f58ec9890a3899a66101e02
state_A.json              = 353113d6e93717d037f7de4d46e686423ec7cfb165fead77397561de0bedaa3f
state_B.json              = 2952ada6d4a27acf05200097cc4b3b55161afae3afeecb6cd926ceef4555cb8a
phi_measurement.json      = 18d01e9262abb8f4e13caab0260f399a198a50b36c83d4896e5be66455d12b8e
```

## Coarse migration-class vocabulary

The six frozen historical before/after pairs are represented by eight coarse transformation classes:

```text
FILES_FILTER_MODEL_MIGRATION
FORMATTER_FILTER_MODEL_MIGRATION
IMPORT_ACTION_MODEL_MIGRATION
NESTED_CONFIG_ROOT_MIGRATION
OVERRIDE_SELECTOR_MIGRATION
RULE_GROUP_RELOCATION
RULE_ID_REPLACEMENT
RULE_PRESET_MODEL_MIGRATION
```

The vocabulary is deliberately coarser than individual option names. The purpose is to preserve migration-relevant relational structure without making the treatment a lookup table for specific future option names.

The assignments are frozen in `MIGRATION_SIGNATURES.json`; missing signatures are not imputed.

## A/B construction

The direct historical migration pairs are identical in A and B. Each arm retains the same:

- six case nodes;
- six direct input-to-output migration pair bindings;
- transformation-class payload;
- complete 15-edge cross-case graph;
- edge-weight multiset;
- object counts.

A stores the evidence-derived Jaccard similarity between the frozen migration-class signatures of each historical case.

B changes only the **binding of those same weights to cross-case edges**.

Frozen scramble:

```text
SEED = ssi-independent-future-adaptation-v0.1/B/topology-scramble/1
ORDER = sort edges by SHA256(SEED + "|" + edge_id)
TRANSFORM = cyclically rotate the ordered A-weight vector by +1
```

This was the first specified scramble seed. **No seed search, rejection sampling, or optimization over Phi separation was performed.** The resulting contrast is preserved as the construction rebound rather than tuned for a larger difference.

## Frozen Phi measurement

No scalar aggregation is licensed.

The raw vector is:

```text
Phi_A:
  C_cover_pre = 1.0000000000000000
  R_reconf    = 0.6666666666666666
  C_challenge = 1.0000000000000000
  A_preserve  = 1.0000000000000000
  L_prov      = 1.0000000000000000
  R_reopen    = 0.8611111111111112

Phi_B:
  C_cover_pre = 1.0000000000000000
  R_reconf    = 0.3333333333333333
  C_challenge = 0.6666666666666666
  A_preserve  = 1.0000000000000000
  L_prov      = 0.7523809523809525
  R_reopen    = 0.7777777777777778
```

Therefore:

```text
Delta(A-B):
  C_cover_pre = 0
  R_reconf    = +0.3333333333333333
  C_challenge = +0.33333333333333337
  A_preserve  = 0
  L_prov      = +0.24761904761904752
  R_reopen    = +0.08333333333333337
```

This is the desired structural pattern: payload-preserving dimensions remain equal while relational dimensions separate.

## Executable component definitions

`BUILD_STATES.py` freezes the executable definitions.

### C_cover_pre

Fraction of the frozen admissible migration-transformation-class universe represented in retained historical payload. Because payload is identical, this dimension is expected to be equal across A/B.

### R_reconf

Fraction of held-out historical cases whose top stored analog has evidence-derived Jaccard similarity at least the frozen threshold:

```text
RECONF_JACCARD_THRESHOLD = 0.5
```

### C_challenge

For each case, fraction of its top-K stored analogs that have independently grounded non-zero migration-class overlap with the case, averaged over cases.

```text
TOP_K = 2
```

### A_preserve

Fraction of frozen direct historical migration alternatives retained. Because the direct pair set is identical, this dimension is expected to be equal across A/B.

### L_prov

Mean edge-level agreement between stored affinity and evidence-derived affinity:

```text
mean(1 - abs(stored_weight - evidence_similarity))
```

on the frozen [0,1] scale.

### R_reopen

For each case, feature recall obtained by reopening the union of the top-K stored analogs, averaged over cases.

## Admissible transformations

```text
ADMISSIBLE_MEASUREMENT_TRANSFORM = IDENTITY_ONLY
```

The raw component scales above are the confirmatory B measurements. No monotone rescaling, weighting, z-scoring, scalarization, or component replacement is authorized inside this benchmark identity.

## Missingness

```text
missing case/signature/edge/required value
=> NOT_IDENTIFIED
=> no imputation
=> B cannot PASS
```

`NOT_IDENTIFIED` is not zero and is not a negative result.

## Frozen directional interpretation

No post-outcome reweighting is allowed.

Expected equality dimensions:

```text
C_cover_pre
A_preserve
```

Expected weak direction:

```text
R_reconf_A    >= R_reconf_B
C_challenge_A >= C_challenge_B
L_prov_A      >= L_prov_B
R_reopen_A    >= R_reopen_B
```

with at least one strict positive contrast required to establish treatment separation.

The first frozen construction satisfies that rule.

## What B does not establish

B PASS does not imply:

```text
Q_state_A ~= Q_state_B
Q_adapt_A ~= Q_adapt_B
resources/information are symmetric
hidden implementation asymmetry is absent
future obligation will use this topology
Phi predicts future adaptation
```

Those remain the jurisdiction of C–I and the later, authorized future shot.
