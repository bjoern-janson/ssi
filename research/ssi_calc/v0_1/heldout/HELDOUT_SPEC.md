# SSI-CALC v0.1 — White-Box Held-Out Attack H24

Status: `PROSPECTIVE_FREEZE_CANDIDATE`

This object is an adversarial **white-box** held-out test of the already-frozen SSI-CALC v0.1 reference checker.

It is not independent authorship: the attack designer knows the frozen checker. That is deliberate. The purpose is to search for overreach and missing composition behavior while forbidding checker adaptation after exposure.

## Frozen order

```text
freeze checker
  -> constitute H, B, M, F
  -> merge H/B/M/F without executing checker
  -> expose immutable checker to H
  -> run baselines
  -> compare
  -> preserve failures
```

Once this object is merged:

```text
DELTA_H_AFTER_EXPOSURE = 0
DELTA_EXPECTED_AFTER_EXPOSURE = 0
DELTA_METRICS_AFTER_EXPOSURE = 0
DELTA_BASELINE_CONTRACT_AFTER_EXPOSURE = 0
DELTA_CHECKER_DURING_HELDOUT_RUN = 0
```

Any later checker correction belongs to a successor version/run and must not overwrite the first held-out result.

## H: held-out cases

`H24` contains 24 cases: three per existing family. The cases reuse the v0.1 schema but are structurally novel compositions, not paraphrases of CASE-001..064.

High-priority attacks include:

- indirect information-flow lineage rather than direct oracle encoding;
- transfer rules that exist but target the wrong jurisdiction;
- multi-hop transfers requiring composition authority;
- pairwise composition versus whole-chain composition;
- explicit equivalence-to-identity transfer authority;
- provenance plus independently constituted semantic bridges;
- admission plus carrier-alignment composition;
- explicitly licensed non-injective transport semantics;
- withdrawn/unresolved evidence that must not be treated as active authority;
- future-preservation evidence whose authority status matters.

Family names and expected labels are benchmark metadata. The frozen checker must not consume them during derivation.

## B: baseline contract

Two intentionally generic deterministic baselines are frozen before execution. They are not claimed to represent Cedar, OPA, TLA+, Alloy, Lean, or expert human review.

### B0 — `MATCHING_EDGE_POLICY`

Authorize only when an explicit authority edge matches the requested jurisdiction and, when supplied, consumer. Otherwise return a generic refusal/unknown. It has no semantic-equivalence, provenance, transport, or future-sufficiency ontology.

### B1 — `EDGE_PLUS_COMPOSITION_GUARD`

B0 plus generic structural guards:

- for `compose`, all requested edges must exist and share the requested jurisdiction;
- a schema/type mismatch blocks composition;
- facts whose authority is `WITHDRAWN` or `UNRESOLVED` cannot by themselves discharge a required condition.

B1 still has no SSI-specific transfer, identity, provenance, regime, or future-sufficiency rules.

These are **internal engineering baselines**. Passing them cannot establish external niche advantage.

## M: frozen metrics

Primary metrics are reported separately; no scalar may hide tradeoffs.

```text
DECISION_ACCURACY
OVERREACH_RATE
FALSE_REFUSAL_RATE
EXACT_STATUS_ACCURACY
SHALLOWEST_LOCUS_ACCURACY
PRESERVATION_AWARE_REFUSAL_ACCURACY
MISSING_AUTHORITY_ACCURACY
REOPENED_SET_ACCURACY
SPECIFICATION_ATOMS_CONSUMED
```

`AUTHORIZED` and `AUTHORIZED_SCOPED` count as authorize decisions. All other statuses count as non-authorize decisions.

Overreach is weighted as the most serious error:

```text
OVERREACH = predicted authorize AND expected non-authorize
FALSE_REFUSAL = predicted non-authorize AND expected authorize
```

## Competitive conclusion rule

This H24 run is primarily a robustness attack. It can **falsify** a strong internal generalization claim, but it cannot by itself establish external niche advantage.

Provisional internal result labels:

- `WHITEBOX_HELDOUT_PASS`: decision accuracy >= 0.90, overreach <= 0.05, false refusal <= 0.10, and no benchmark mutation.
- `WHITEBOX_HELDOUT_PARTIAL`: decision accuracy >= 0.75 but pass thresholds fail.
- `WHITEBOX_HELDOUT_FAILED`: decision accuracy < 0.75 or overreach > 0.15.

Any `NICHE_ADVANTAGE_ESTABLISHED` claim remains forbidden until an external/practical baseline study is separately constituted.

## Scientific ceiling

A good result here means only that a frozen checker survives a hostile white-box set without adaptation. A bad result is useful: it localizes where the 11-rule reference implementation fails on novel compositions.
