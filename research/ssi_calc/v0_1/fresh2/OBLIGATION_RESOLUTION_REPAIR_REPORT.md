# SSI-CALC v0.1 — Obligation Resolution Repair

## Status

```text
KNOWN_OBLIGATION_RESOLUTION_FAILURES_REPAIRED = YES
FOUR_SUITE_EXACT_REGRESSION_PASS = YES
R12_AUTHORIZED = NO
GENERALIZATION_ESTABLISHED = NO
NICHE_ADVANTAGE_ESTABLISHED = NO
```

HF2-24 exposed two false refusals caused by inactive or unresolved alternative proof channels vetoing distinct live sufficient routes. The repair changes only evaluator resolution ordering under the unchanged R1..R11 kernel.

## Earned resolution invariant

```text
If a live path already discharges G,
an inactive/unresolved alternative path may not veto G
unless G is explicitly conjunctive.
```

This does not authorize ignoring live counterevidence. Active evidence remains in the live-authority projection presented to the existing evaluator.

## Implementation boundary

The successor preserves the existing typed live-authority membrane and evaluates one goal in this order:

1. mandatory historical obligations;
2. typed provenance bridge obligations;
3. live-only R1..R11 candidate search;
4. if a live sufficient route authorizes the goal, discharge it;
5. otherwise evaluate represented-but-inactive obligations;
6. otherwise retain the live evaluator's refusal or non-identification.

No benchmark labels, family identifiers, or expected certificates enter derivation.

## Remote regression

GitHub Actions:

```text
RUN      = 31951331769
JOB      = 95175129022
ARTIFACT = 9264717259
DIGEST   = sha256:8dd29d3df67b832a0249b50691e0f2b8daf75674d9ca5be30a5c7e08fe229ca7
HEAD     = 864e4c793109035fc2a5e2f749fd49468e64306d
```

Exact certificate regression:

```text
B64    = 64 / 64
H24    = 24 / 24
HF16   = 16 / 16
HF2-24 = 24 / 24
TOTAL  = 128 / 128
```

Across every suite:

```text
OVERREACH = 0%
FALSE_REFUSAL = 0%
RULES_ADDED_BEYOND_R11 = 0
```

## Epistemic role

This result establishes only that the known obligation-resolution failure witnesses can be repaired without changing R1..R11 or regressing the exposed corpus.

HF2-24 has now participated in repair and permanently becomes regression evidence. It cannot support any future claim of generalization for this successor.

The next scientific object must be separately constituted after this implementation is frozen and must remain unexposed until its own freeze is merged.
