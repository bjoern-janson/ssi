# Frozen internal baselines

These baselines are deliberately generic and deterministic. They are engineering comparators, not stand-ins for named external tools.

## B0 — MATCHING_EDGE_POLICY

Input: semantic case with benchmark metadata removed.

Decision:

1. Validate the case schema.
2. Search for an authority edge whose jurisdiction equals the requested jurisdiction.
3. If a consumer is declared, require the edge target to equal that consumer.
4. If a match exists, `AUTHORIZE`; otherwise `NON_AUTHORIZE`.

B0 emits no SSI-specific failure locus.

## B1 — EDGE_PLUS_COMPOSITION_GUARD

B1 performs B0 and adds generic structural guards:

- `compose`: every requested edge must exist and each must use the requested jurisdiction;
- mismatched declared input/output contracts reject composition;
- an `UNRESOLVED` or `WITHDRAWN` fact cannot alone discharge a condition.

B1 does not implement semantic equivalence, identity, provenance-to-semantics bridges, regime comparison, transport semantics, or future sufficiency.

## Fairness rule

Baseline implementations may use objects, facts, authority edges, and the request. They may not read `family` or `expected`.

The baseline contracts are frozen before the first held-out execution. Implementation bugs may be corrected only if the contract already entails the correction, and the original run must remain preserved.
