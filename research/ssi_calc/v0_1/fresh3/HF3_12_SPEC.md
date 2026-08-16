# HF3-12 — Obligation Resolution Fresh Terrain

## Role

HF3-12 is constituted **after** successor-v3 was frozen at merge `559ce29d0ace8f518009067639a39ba6ac3994dc` and **before first successor-v3 exposure**.

Its sole purpose is to test the HF2-24-earned obligation-resolution distinction:

```text
ALTERNATIVE_SUFFICIENT
!= CONJUNCTIVE_REQUIRED
!= ACTIVE_DEFEATER
```

It is a targeted post-repair white-box generalization set, not a broad niche benchmark.

## Frozen objects

```text
CASE_COUNT = 12
CASE_IDS = CASE-401..CASE-412
LICENSED = 6
NON_AUTHORIZED = 6
```

Structural roles:

```text
ALTERNATIVE_SUFFICIENT = 6
CONJUNCTIVE_REQUIRED = 4
ACTIVE_DEFEATER = 2
```

The cases span identity, future preservation, transport, provenance, regime comparison, substitution, and composition. They reuse the frozen schema and R1..R11 vocabulary but combine live, inactive, required, and defeating evidence in placements not used to repair successor-v3.

## Scientific hypotheses

### Alternative sufficiency

If a live, well-typed path independently discharges `G`, an inactive or unresolved alternative route does not veto `G`.

### Conjunctive requirement

If the operation's existing contract requires multiple prerequisites, one live prerequisite is not an alternative substitute for another required prerequisite.

### Active defeater

A live targeted counterexample/defeater remains relevant even when favorable but irrelevant or incomplete structure is also present.

No new calculus rule is introduced or implied.

## Frozen identifiers

```text
SUCCESSOR_V3_FREEZE_MERGE = 559ce29d0ace8f518009067639a39ba6ac3994dc
HF3_12_PLAIN_SHA256 = 0747244689af2caca39c4f692e4c0eccf7ce39cda386c5855620bb8ce286ae33
HF3_12_GZIP_SHA256  = 3be543c9b303f9220687e0d933ff0d9eb887ff2ddae7d8d089d9ae36a822ef76
```

## Firewall

Before this freeze merges:

```text
SUCCESSOR_V3_EXECUTED_ON_HF3_12 = FALSE
```

After first exposure:

```text
DELTA_HF3_12 = 0
DELTA_EXPECTED = 0
DELTA_SUCCESSOR_DURING_FIRST_RUN = 0
DELTA_THRESHOLDS = 0
```

HF3-12 permanently loses generalization authority if it is later used for repair.

## Prospective labels

```text
HF3_12_STRONG_PASS:
  decision = 12/12
  overreach = 0
  false_refusal = 0

HF3_12_PASS:
  decision >= 11/12
  overreach <= 1/6
  false_refusal <= 1/6

HF3_12_PARTIAL:
  decision >= 9/12 but PASS fails

HF3_12_FAILED:
  decision < 9/12 or overreach > 2/6
```

Maximum claim even under `STRONG_PASS`:

```text
POST_OBLIGATION_RESOLUTION_WHITEBOX_GENERALIZATION_SUPPORTED_IN_HF3_12
```

This cannot establish external niche advantage.
