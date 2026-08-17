# Contributing to SSI

SSI is a research repository with unusually strict provenance requirements. A contribution can be technically correct and still be scientifically invalid if it changes the meaning, authority, or evaluation conditions of a frozen result.

This guide defines the default contribution protocol.

---

## 1. First principle

> **Preserve evidence before improving interpretation.**

A failed prediction, evaluator mismatch, non-evaluable case, or negative result is scientific data. Do not erase it by repairing the artifact that produced it after first execution.

The default flow is:

```text
constitute
-> freeze
-> execute
-> preserve first result
-> diagnose
-> repair prospectively
-> retest independently
```

---

## 2. Know what kind of change you are making

### Scientific change

Changes the object under study, candidate behavior, case geometry, evidence contract, oracle, protocol, evaluator, or result interpretation.

Examples:

```text
new benchmark case
new semantic binding rule
new target evidence type
candidate repair
evaluator classification rule
new theorem/candidate claim
```

Scientific changes require explicit lineage and authority accounting.

### Administrative / navigation change

Improves presentation or repository operation without changing scientific meaning.

Examples:

```text
README navigation
research indexes
spelling / formatting outside frozen artifacts
PR templates
status summaries
non-authoritative diagrams
```

Administrative files must not silently promote scientific claims.

### Reproduction / implementation change

Changes executable infrastructure while intending to preserve the frozen scientific object.

Examples:

```text
packaging
runner ergonomics
serialization utilities
CI wiring
```

These changes still need a preservation argument if they can affect outputs.

---

## 3. Frozen artifacts are immutable scientific evidence

Once a stage is frozen and used by a downstream stage, treat its bytes as evidence.

Typical stage order:

```text
SPEC
-> CASES
-> BINDINGS / CANDIDATE
-> INDEPENDENT ORACLE
-> PROTOCOL
-> EVALUATOR
-> RESULT
```

Not every experiment uses every stage, but the governing rule is the same:

> **Do not modify an upstream artifact after downstream evidence depends on it.**

If a defect is discovered, preserve the defective artifact and open a prospective repair object or version.

---

## 4. The candidate must not certify itself

Keep these roles independent:

```text
candidate behavior
!= oracle description
!= protocol comparison
!= evaluator judgment
```

Forbidden patterns include:

```text
candidate output -> redefine oracle
candidate failure -> edit cases until evaluable
candidate success -> weaken evaluator threshold
novel channel -> synthesize legacy evidence without a frozen transport rule
```

If a candidate cannot legitimately consume the evidence available, `NOT_EVALUABLE` may be the correct result.

---

## 5. Preserve typed epistemic states

Do not collapse distinct statuses into a generic pass/fail field.

Common SSI statuses include:

```text
SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
SUPPORTED_ON_FROZEN_HELDOUT_STRESS_AXIS
NOT_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
NOT_EVALUABLE_UNDER_FROZEN_BINDING
NOT_EVALUABLE_UNDER_FROZEN_TRANSPORT_CONTRACT
UNPROVEN
REVOKED
NOT_ESTABLISHED
NOT_OPENED
NOT_CONSTITUTED
PROSPECTIVE_NOT_EARNED
```

Important:

```text
NOT_EVALUABLE != NOT_SUPPORTED
UNPROVEN != REVOKED
NOT_ESTABLISHED != FALSE
SUPPORTED_ON_FROZEN_SUITE != UNIVERSALLY_TRUE
```

Use the narrowest correct status.

---

## 6. No scalar rescue

When obligations are independently typed, keep them independently typed.

Do not convert:

```text
semantic correctness
evidence admission
provenance preservation
uncertainty preservation
authority preservation
```

into a weighted average merely to claim overall success.

A single authority- or evidence-laundering counterexample can be qualitatively different from several benign correct cases.

---

## 7. Failure localization

When a result contradicts expectation, diagnose the shallowest supported locus:

```text
Observation
-> Inference
-> Mechanism
-> Representation
-> Interface
```

Recommended procedure:

1. Generate competing explanations.
2. Discriminate using evidence independent of the failing representation where possible.
3. Apply the minimal sufficient revision.
4. Preserve unaffected structure.
5. Retest on held-out evidence.
6. Keep competing hypotheses reopenable until repeated predictive success justifies consolidation.

Error is a signal of failure, not automatically its cause.

---

## 8. Authority discipline

SSI distinguishes what a system can do from what it is licensed to do and what it actually did:

```text
Can != May != Did
```

Likewise:

```text
validity != transportability != composability
semantic identity != evidence admission
role license != execution license
local preservation != path preservation
```

A positive result at one layer must not be promoted into authority at another layer without an independently constituted bridge.

---

## 9. Branch and PR lineage

For scientific work, prefer one bounded object per branch/PR.

A PR should record:

```text
OBJECT
PARENT BRANCH / COMMIT
QUESTION
FROZEN DEPENDENCIES
CURRENT STAGE
RESULT, if executed
STRONGEST EARNED CLAIM
AUTHORITY CEILING
```

If stacked on another unmerged experiment, use the exact frozen parent head as the base.

Never imply that a stacked child retroactively changes the parent result.

---

## 10. First-result discipline

Before first execution, freeze all evaluation logic that is supposed to be independent of the result.

After execution:

```text
FIRST RESULT = evidence
```

If it fails:

- preserve it,
- record the witness,
- localize the failure,
- do not edit the candidate/oracle/protocol/evaluator in place,
- create a prospective repair lineage if warranted.

If it succeeds:

- freeze the bounded positive,
- state the strongest earned claim,
- state what remains untested,
- do not expand the scope through prose.

---

## 11. Administrative provenance incidents

Operational mistakes should be recorded transparently when they affect repository history or could confuse scientific lineage.

Examples:

```text
wrong-branch metadata write
stray empty file on main
duplicate PR creation attempt
failed no-op routing call
```

Distinguish them from scientific mutations.

Do not rewrite Git history merely to make an incident disappear unless there is a compelling repository-safety reason.

---

## 12. Reader-facing summaries

Files such as `README.md`, `RESEARCH_MAP.md`, and `REPOSITORY_STATUS.md` are routing layers.

They should:

- make the current frontier legible,
- link to exact experiments,
- preserve negative/non-evaluable outcomes,
- state authority ceilings,
- explicitly identify themselves as non-authoritative summaries.

They should not:

- rewrite frozen statuses,
- promote candidates to theorems,
- imply that newer prose supersedes frozen evidence.

> **Newest file wins is not an epistemic rule.**

---

## 13. PR checklist

Before opening a PR, verify:

- [ ] I know whether this is scientific, administrative, or reproduction work.
- [ ] The parent branch/commit is explicit.
- [ ] I have not modified frozen upstream artifacts without opening a new lineage.
- [ ] Candidate, oracle, protocol, and evaluator roles remain separate where applicable.
- [ ] Negative or non-evaluable results are preserved.
- [ ] No scalar score hides typed failures.
- [ ] The strongest earned claim is narrower than or equal to the evidence scope.
- [ ] The authority ceiling is explicit.
- [ ] I am not implicitly opening boundary semantics, repair, composition, or SSI-CALC authority.
- [ ] Administrative incidents are recorded separately from scientific findings.

---

## 14. Current frontier guardrail

As of the post-PR61 state:

```text
POST_PR61_FRONTIER = UNCONSTITUTED
LOCAL_PRESERVATION_TO_PATH_PRESERVATION = NOT_ESTABLISHED
```

The following remain unopened:

```text
TRANSFORMATION_COMPOSITION
CERTIFICATE_COMPOSITION
AUTHORITY_COMPOSITION
CHALLENGE_PATH_PRESERVATION
MUTABILITY
```

Do not select one of these as the next scientific object through a cleanup, refactor, or convenience change.

---

## 15. Style

Prefer:

- exact object/status names,
- bounded claims,
- explicit non-rules,
- compact tables and status blocks,
- provenance over rhetoric,
- negative evidence over silent repair.

A good SSI contribution makes it easier for reality to force a future revision.
