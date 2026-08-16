# SSI-CALC v0.1 — Compass Orchestration Repair

Status: `KNOWN_FAILURES_REPAIRED_NOT_GENERALIZATION`

This lineage implements the H24 failure analysis without changing the R1..R11 kernel, B64, H24, schema, SPEC, or any frozen expected result.

## Experimental roles

```text
B64     = contract conformance
H24     = known-failure regression only
H_fresh = future generalization object; not yet constituted
```

H24 permanently lost generalization authority after its first exposure. A perfect H24 regression result therefore means only that its known failures have been repaired.

## Frozen repair hypothesis

The merged H24 analysis classified all 17 exact-certificate mismatches as implementation/orchestration defects:

```text
H1 IMPLEMENTATION / ORCHESTRATION = 17
H2 REPRESENTATION / SPECIFICATION = 0
H3 MISSING CALCULUS CAPABILITY     = 0
R12_AUTHORIZED                     = NO
```

The successor evaluator therefore leaves `RULES = R1..R11` unchanged and adds execution semantics for:

```text
ACTIVE_AUTHORITY_GATING
EXACT_TRANSFER_TARGET_MATCHING
TRANSFER_PATH_COMPOSITION_THROUGH_R9
CERTIFICATE_COVERS_REQUESTED_COMPOSITION
COMPONENT_JURISDICTION_VALIDATION
POSITIVE_CONSTITUTED_BRIDGE_RECOGNITION
CROSS_RULE_GATE_ADVANCEMENT
INDIRECT_INFORMATION_FLOW_LINEAGE_REACHABILITY
```

The architectural change is from isolated first-match recognition toward derivation-state orchestration. The frozen reference checker remains intact; `checker_orchestrated.py` is a successor evaluator that delegates to it after orchestration-specific gates.

## Remote regression lineage

The first remote successor run preserved B64 exactly and moved H24 sharply:

| Metric | H24 first exposure | Successor run 1 |
|---|---:|---:|
| Decision accuracy | 50.0% | 95.8% |
| Overreach | 50.0% | 0.0% |
| False refusal | 50.0% | 8.3% |
| Exact certificate | 29.2% | 70.8% |

`B64 = 64/64 exact` throughout.

That intermediate state is preserved because it was diagnostically useful. One decision failure remained (`CASE-106`) and six additional certificates were semantically correct but not exact.

A diagnostic replay exposed the immutable inputs for those seven cases. Two implementation distinctions remained:

1. provenance-only lineage can establish information-flow ancestry without acquiring semantic/action authority;
2. composition certificates for transfer chains refer to semantic route names (`k1_to_k2`) rather than incidental fact identifiers (`f2`).

Five remaining differences were exact frozen missing-authority labels, not changed decision semantics.

## Final frozen regression

GitHub Actions run `31949237633`, job `95170013092` executed the unchanged B64 and H24 objects against the successor evaluator.

```text
KERNEL_RULE_COUNT       = 11
RULES_ADDED_BEYOND_R11  = 0

B64:
  cases                  = 64
  decision_accuracy      = 100%
  overreach              = 0%
  false_refusal          = 0%
  exact_certificate      = 100%
  mismatches             = 0

H24:
  cases                  = 24
  decision_accuracy      = 100%
  overreach              = 0%
  false_refusal          = 0%
  exact_status           = 100%
  shallowest_locus       = 100%
  preservation           = 100%
  missing_authority      = 100%
  reopened_set           = 100%
  exact_certificate      = 100%
  mismatches             = 0
```

The uploaded regression artifact was GitHub artifact `9264161443`; its ZIP SHA-256 was:

`6413b40752d85cea868b2c6be687d81ecefa0443e37b55f97ef6455424125142`

## What this result earns

It supports the narrow engineering diagnosis:

> **The observed H24 failure was repairable by cross-rule authority orchestration under the existing R1..R11 rule partition.**

In particular, the change:

```text
H24 overreach: 50% -> 0%
H24 false refusal: 50% -> 0%
B64 exact:      100% -> 100%
Delta |K|:       0
```

is strong regression evidence that simple conservatism was not the only mechanism. The successor became both less overreaching and less falsely refusing while preserving the original contract benchmark.

It does **not** establish that R1..R11 are complete, sound in a theorem-prover sense, externally competitive, or generalizable to unseen compositions.

## Authority ceiling

```text
INTERNAL_FROZEN_CONTRACT_PASS = PRESERVED
H24_FIRST_EXPOSURE             = FAILED (PRESERVED)
H24_KNOWN_FAILURE_REGRESSION   = PASSED
R12_AUTHORIZED                 = NO
NICHE_ADVANTAGE_ESTABLISHED    = NO
GENERALIZATION_ESTABLISHED     = NO
```

The next earned experiment is not further H24 tuning. It is:

```text
freeze successor implementation
    -> constitute H_fresh without executing successor
    -> freeze H_fresh
    -> expose immutable successor
    -> preserve the first fresh-terrain result
```

The fresh set must use novel compositions that were not among the 17 repair witnesses. H24 remains regression history permanently.
