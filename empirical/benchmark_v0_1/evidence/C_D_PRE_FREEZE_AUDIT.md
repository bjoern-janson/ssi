# C/D Evidence — Pre-Freeze Matching Audit

## Adjudication

```text
C = PASS
D = FAIL
```

Because D fails, this A/B construction is not eligible for freeze or run authorization. E–I are not promoted on this construction merely to complete a checklist.

## Evidence artifacts

```text
empirical/benchmark_v0_1/construction/PRE_FREEZE_AUDIT.py
empirical/benchmark_v0_1/construction/pre_freeze_audit.json
```

Local SHA-256 values at adjudication:

```text
PRE_FREEZE_AUDIT.py     = a2012984fb836a66411a02c22f177651c47f36642c01b43ce919c8ca05989156
pre_freeze_audit.json   = 523fbe8211253b8d8c859322f4dda48272f6a6c5c74650746c037a0053e3f94d
```

The audit accesses no future obligation.

---

# C — Present capability

C compares the frozen non-treatment present-state dimensions using exact equality.

Both arms have:

```text
case_count                       = 6
direct_pair_count                = 6
edge_count                       = 15
transformation_class_count       = 8
known_pair_availability_rate     = 1.0
```

They also preserve the exact same topology edge-weight **multiset**:

```text
[0, 0, 0,
 0.14285714285714285, 0.14285714285714285,
 0.16666666666666666, 0.16666666666666666,
 0.25, 0.25,
 0.2857142857142857,
 0.5, 0.5, 0.5, 0.5,
 0.7142857142857143]
```

The direct historical migration-pair payload is identical by construction and rechecked by `BUILD_STATES.py`.

Therefore, on the frozen current-state dimensions:

```text
C = PASS
```

Boundary: this does not establish ordinary adaptation equivalence. That is D.

---

# D — Ordinary adaptation

A narrow exact-known-case lookup probe would be guaranteed equal because direct historical pairs are identical. Treating that as sufficient D evidence would allow the topology treatment to hide an already-present generic analogical adaptation advantage.

The adversarial D probe therefore uses the same topology-assisted resolver that would be available for a novel obligation and constructs an exhaustive finite pre-freeze surrogate universe.

## Surrogate universe

Frozen transformation-class universe size:

```text
8
```

Enumerate every nonempty subset of those eight classes and remove the six subsets that exactly equal a historical case signature.

Result:

```text
D_TASK_COUNT = 249
```

No future configuration change is used.

## Shared resolver

For both arms:

1. if an exact historical signature exists, use its direct pair;
2. otherwise choose the historical anchor with maximum query/signature Jaccard similarity, lexical tie-break;
3. traverse the top two stored topology neighbors of that anchor;
4. define recovery as the fraction of requested migration classes present in the anchor-plus-neighbor union.

The two-neighbor budget is the same `TOP_K = 2` already frozen in the B topology measurement. The algorithm is identical across arms.

## Result

```text
                         A                    B                 A-B
mean recovery recall     0.8646921017402945   0.8494979919678715   +0.015194109772423081
full recovery rate       0.4738955823293173   0.4497991967871486   +0.024096385542168697
full recovery count      118                  112                  +6
```

29 of the 249 deterministic surrogate obligations produce different A/B recovery.

The canonical ordered query list for those differing obligations has SHA-256:

```text
4aabe30a77167773507a62c0116f4cbe9c0558fd527418c33c27504b9e4f3861
```

## Adjudication

The intended benchmark requires the objection

> "A was already a better ordinary adapter"

not to explain the later result.

This construction does not meet that burden. A already has a measurable advantage on pre-freeze novel-composition surrogates under the same adaptation procedure and budget.

Therefore:

```text
D = FAIL
```

No null-hypothesis non-significance criterion is used to relabel the difference as equivalence.

## Consequence

```text
FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
RUN = NOT_AUTHORIZED
```

The failure localizes to **construction -> ordinary-adaptation matching**. It does not negate predicate B's treatment separation and it does not test the flagship future-adaptation hypothesis.

The current A/B construction must not be fired as the confirmatory shot.
