## Object / scope

<!-- Exact object name or administrative scope. -->

```text
OBJECT =
CHANGE_TYPE = SCIENTIFIC | ADMINISTRATIVE | REPRODUCTION
```

## Parent provenance

```text
BASE_BRANCH =
BASE_COMMIT =
PARENT_OBJECT =
```

<!-- If stacked, use the exact frozen parent head. -->

## Question / purpose

<!-- One bounded question. For administrative work, state what is being made clearer or safer. -->

> **...**

## Frozen dependency lineage

<!-- Delete stages that do not apply. Do not fill future stages speculatively. -->

```text
SPEC      =
CASES     =
BINDINGS  =
ORACLE    =
PROTOCOL  =
EVALUATOR =
RESULT    =
```

## What changed

- 
- 
- 

## What did **not** change

<!-- Explicitly name frozen artifacts / authority surfaces left untouched. -->

```text
...
```

## First-result / negative-result preservation

<!-- For scientific work: record whether this PR contains a first run, repair, or no execution. -->

```text
FIRST_RESULT = NOT_RUN | FROZEN | NOT_APPLICABLE
UPSTREAM_REPAIR_AFTER_FIRST_RUN = NO
```

Negative / non-evaluable witnesses preserved:

- 

## Strongest earned claim

<!-- Use the narrowest status supported by the frozen evidence. -->

```text
...
```

## Authority ceiling

<!-- State what this PR does NOT establish or open. -->

```text
...
```

## Scientific firewalls

- [ ] Candidate output does not define oracle truth.
- [ ] Protocol comparison does not issue evaluator judgment.
- [ ] `NOT_EVALUABLE` is not relabeled as `NOT_SUPPORTED`.
- [ ] `UNPROVEN` is not relabeled as `REVOKED`.
- [ ] No scalar score hides independently typed failures.
- [ ] A successful repair does not rewrite a failed frozen first result.
- [ ] No new boundary semantics, repair authority, composition authority, or SSI-CALC kernel rule is implied without a separately constituted object.

## Frozen-artifact integrity

- [ ] I did not modify a frozen upstream scientific artifact used by downstream evidence.
- [ ] If a defect required repair, the repair is prospective and separately versioned.
- [ ] Administrative files are clearly non-authoritative summaries.

## Validation

<!-- Commands, frozen evaluator execution, link checks, or read-only verification. -->

```text
...
```

## Administrative provenance incidents

<!-- Record wrong-branch writes, failed routing calls, duplicate PR attempts, or other history-affecting incidents. Write NONE if none occurred. -->

```text
NONE
```

## Merge

- [ ] This PR is ready for review.
- [ ] Merge has been explicitly requested / authorized.

> **Do not infer merge authorization from scientific completion alone.**
