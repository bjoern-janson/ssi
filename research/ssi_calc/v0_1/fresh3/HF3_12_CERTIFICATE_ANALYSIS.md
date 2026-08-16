# HF3-12 Certificate Mismatch Analysis

## Scope

This is an analysis-only lineage after the immutable HF3-12 first run was merged at `4b498aac06b89a0bb236da3f8b4938717d388911`.

No checker, case, expected certificate, threshold, schema, metric, or R1..R11 rule changes in this analysis.

## First-run fact

HF3-12 prospectively earned the decision-level label:

```text
HF3_12_STRONG_PASS
```

with:

```text
DECISION_ACCURACY = 12/12
OVERREACH = 0/6
FALSE_REFUSAL = 0/6
```

One exact-certificate mismatch remained:

```text
CASE-402
expected: AUTHORIZED_SCOPED
observed: AUTHORIZED
```

The authorize/refuse decision, failure locus, preserved facts, missing-authority set, and reopen set all matched.

## Competing explanations

### H1 — evaluator status-granularity bug

Prediction: an earlier frozen `consume_quotient` case using the same `future_invariant_under` route should require `AUTHORIZED_SCOPED`, so emitting `AUTHORIZED` would violate established evaluator semantics.

### H2 — fresh expected-certificate specification defect

Prediction: the earlier frozen contract should already treat `local_quotient_licensed + future_invariant_under` as `AUTHORIZED`, while another route may legitimately carry the scoped label.

### H3 — missing calculus capability

Prediction: R1..R11 and the prior frozen contract do not determine the status distinction.

## Independent discrimination

The pre-existing B64 corpus decides this without using HF3-12 to repair itself.

`CASE-060` is a frozen `consume_quotient` case with:

```text
local_quotient_licensed
+
future_invariant_under
```

and its frozen expected status is:

```text
AUTHORIZED
```

That is the same operative future-invariance route used by the successful live path behind CASE-402.

By contrast, `CASE-057` is a frozen `consume_quotient` case with:

```text
local_quotient_licensed
+
kernel_containment_verified
```

and its frozen expected status is:

```text
AUTHORIZED_SCOPED
```

So the existing contract already distinguishes these two positive preservation routes at status granularity.

Result:

```text
H1 = 0
H2 = 1
H3 = 0
R12_AUTHORIZED = NO
SUCCESSOR_V4_AUTHORIZED = NO
```

The shallowest sufficient diagnosis is:

```text
STATUS_GRANULARITY_EXPECTATION_DEFECT
```

in CASE-402's frozen expected certificate.

## Minimal counterfactual

Had CASE-402 been authored consistently with the already-frozen CASE-060 route semantics, its expected status would have been `AUTHORIZED` rather than `AUTHORIZED_SCOPED`.

That is a counterfactual diagnosis only. HF3-12 has already been exposed and therefore remains immutable. Its first-run exact-certificate score stays historically recorded as 11/12.

No benchmark repair is performed.

## Scientific interpretation

The prospective decision-level result stands:

```text
HF3_12_STRONG_PASS
DECISION = 12/12
OVERREACH = 0%
FALSE_REFUSAL = 0%
```

The immutable first-run certificate result also stands:

```text
EXACT_CERTIFICATE = 11/12
```

After independent contract discrimination, the one mismatch is attributed to an over-scoped frozen expectation rather than to successor-v3 or to a missing calculus rule.

Strongest claim:

```text
POST_OBLIGATION_RESOLUTION_WHITEBOX_GENERALIZATION_SUPPORTED_AT_DECISION_LEVEL_IN_HF3_12
```

This remains synthetic, targeted, and white-box. It does not establish external validation or niche advantage.
