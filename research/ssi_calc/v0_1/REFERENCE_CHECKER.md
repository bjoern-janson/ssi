# SSI-CALC Reference Checker v0.1

Status: `INITIAL_FROZEN_BENCHMARK_RUN_COMPLETE`

This artifact is the first executable adjudicator for the benchmark frozen by PR #24.

It deliberately does not modify the benchmark, schema, or v0.1 rule budget.

## 1. Execution contract

The checker performs only:

```text
load
  -> validate
  -> derive under R1..R11
  -> refuse / retain uncertainty / reopen when derivation fails
  -> emit certificate
```

The derivation engine does not read the benchmark `expected` object. `run_benchmark.py` compares the emitted certificate to `expected` only after derivation.

Authority remains an edge. There is no global `Authority(x)=true` primitive.

## 2. Frozen kernel

No rules were added.

```text
R1  DECLARE
R2  ADMIT
R3  LICENSE
R4  EQUIV
R5  SUBSTITUTE
R6  CONGRUENCE
R7  TRANSPORT
R8  QUOTIENT
R9  COMPOSE
R10 PRESERVE
R11 REOPEN
```

```text
RULES_ADDED_BEYOND_R11 = 0
```

## 3. First run — preserved failure

The first run was executed against all 64 already-frozen cases before any benchmark-directed correction.

Result:

```text
STATUS_ACCURACY            = 63 / 64 = 98.4375%
LOCUS_ACCURACY             = 63 / 64 = 98.4375%
PRESERVED_FACTS_ACCURACY   = 64 / 64 = 100%
MISSING_AUTHORITY_ACCURACY = 63 / 64 = 98.4375%
REOPENED_ACCURACY          = 64 / 64 = 100%
EXACT_CERTIFICATE_ACCURACY = 63 / 64 = 98.4375%
```

The only miss was:

```text
CASE-044
F6_REGIME
Admission rule depends on the desired downstream result
```

Expected shallowest result:

```text
REGIME_MISMATCH @ ADMIT
missing = target_independent_admission
```

Observed first-run result:

```text
NOT_IDENTIFIED @ LICENSE
missing = derivation_not_available_in_R1_R11
```

The initial result, including the full CASE-044 mismatch certificate, is preserved in `RUN_LEDGER.json`.

## 4. Failure-locus classification

The witness did **not** demonstrate a missing calculus capability.

`R2:ADMIT` already contained the intended rule:

> an admission condition that depends on the desired downstream result cannot constitute an external semantic regime.

The defect was shallower: the reference implementation recognized an admission argument only when its string *started* with `desired`, while the frozen benchmark encoded:

```text
matches_desired_result
```

Classification:

```text
FAILURE_LOCUS = IMPLEMENTATION / INFERENCE MATCHER
KERNEL_GROWTH_REQUIRED = FALSE
```

Minimal correction:

```text
startswith("desired")
    ->
contains("desired")
```

No benchmark case, expected label, rule name, rule count, or authority boundary changed.

## 5. Full regression after minimal correction

The complete 64-case benchmark was rerun.

```text
STATUS_ACCURACY            = 64 / 64 = 100%
LOCUS_ACCURACY             = 64 / 64 = 100%
PRESERVED_FACTS_ACCURACY   = 64 / 64 = 100%
MISSING_AUTHORITY_ACCURACY = 64 / 64 = 100%
REOPENED_ACCURACY          = 64 / 64 = 100%
EXACT_CERTIFICATE_ACCURACY = 64 / 64 = 100%
RULES_ADDED_BEYOND_R11     = 0
```

The regression aggregate is preserved in `RUN_LEDGER.json`; `run_benchmark.py` regenerates per-case records on demand.

This is an **internal frozen-contract result**, not evidence of competitive niche advantage. The benchmark was designed from the same research lineage as the calculus. External/baseline comparison remains required for `H_0.1`.

## 6. Certificate semantics

A checker certificate contains:

```text
status
failure_locus
rule
preserved_facts
missing_authority
reopened
explanation
```

A downstream refusal does not erase unaffected upstream facts.

Example:

```text
CASE-026
behavioral_equivalence(q1,q2)
    -> requested presentation identity

UNLICENSED_JURISDICTION_TRANSFER
failure_locus = TRANSFER
rule = R4:EQUIV
preserved = behavioral_equivalence(q1,q2)
missing = behavior_to_presentation_identity_transfer
```

## 7. Reproduction

From `research/ssi_calc/v0_1/`:

```bash
python -m pip install -r requirements.txt
python run_benchmark.py --output LOCAL_RESULT.json
```

Single case:

```bash
python checker.py benchmark/CASE-026.json
```

## 8. Authority ceiling

This execution establishes only:

```text
THE_FROZEN_11_RULE_REFERENCE_IMPLEMENTATION
CAN_EXACTLY_ADJUDICATE_THE_FROZEN_64_CASE_INTERNAL_BENCHMARK
AFTER_ONE_PRESERVED_IMPLEMENTATION_DEFECT_AND_MINIMAL_CORRECTION
```

It does not establish:

- that the benchmark labels are externally correct;
- that the calculus generalizes to unseen authority-transfer cases;
- that SSI-CALC beats Cedar, OPA, Alloy, TLA+, Lean, provenance systems, or human review;
- that `H_0.1` is supported;
- that rules R12..R15 are unnecessary outside this benchmark.

The next scientific transition is a **separately frozen baseline / held-out comparison**, not additional rule construction.
