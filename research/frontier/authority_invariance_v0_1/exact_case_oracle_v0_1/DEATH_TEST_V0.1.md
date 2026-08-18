# FR001_EXACT_CASE_ORACLE_V0.1 — Death Test

**Target contract commit:** `4da43c511f1027b2847b316800f31c8935a5050f`  
**Target exact-object commit:** `d27fffc8f08c80630bcd854bd9b150833637207d`  
**Record type:** benchmark-constitution death-test result  
**Persistent record state:** `FROZEN`  
**Model execution:** `NONE`  
**Authority-invariance claim:** `NOT_ESTABLISHED`  
**SSI-CALC kernel delta:** `0`  
**Cerebro modification:** `NONE`

This death test asks only whether the successor object repairs the four benchmark-constitution failures identified in `DEATH_TEST_V0.1.md` and whether any remaining ambiguity belongs to the scientific case/oracle surface or to a future concrete execution binding.

It does not run a model.

---

## 1. Target distinction

The object must preserve:

\[
\boxed{
\text{research object constituted}
\neq
\text{benchmark surface constituted}
\neq
\text{specific execution bound}
\neq
\text{result established}.
}
\]

The required causal condition is:

\[
\boxed{
\text{system output}
\not\rightarrow
\text{case constitution, oracle, world binding, or randomness design}.
}
\]

---

## 2. Retest A — `TEMPLATE_AS_FROZEN_CASE`

The successor freezes exactly nine concrete trajectories:

```text
F1A F2A F3A F4A F5A F6A
C1A C2A C3A
```

Each freezes:

- principal and grantee;
- target action/object/jurisdiction/purpose;
- exact initial authority edges;
- exact provenance, jurisdiction, basis, purpose, activation, and status coordinates;
- verbatim external transcript;
- registered authority-relevant events;
- exact task context;
- attack substitution or control target.

No case may be added or rewritten without a successor version.

### Verdict

```text
TEMPLATE_AS_FROZEN_CASE = REPAIRED
```

The case surface is no longer a family template.

---

## 3. Retest B — `ORACLE_PLACEHOLDER_AS_INDEPENDENT_ORACLE`

For all nine cases the successor freezes an oracle derivation and complete expected post-transcript authorization state before any system output exists.

The oracle's dependency rule is explicitly:

```text
INITIAL_AUTHORITY_STATE
+
REGISTERED_AUTHORITY_EVENTS
```

with system-output dependence forbidden.

Attack cases contain no registered post-initial authority event and therefore retain the exact initial authority state.

Controls apply only their frozen typed event:

```text
C1A ADD_EDGE
C2A REMOVE_EDGE
C3A ACTIVATE_CONDITIONAL_EDGE
```

### Verdict

```text
ORACLE_PLACEHOLDER_AS_INDEPENDENT_ORACLE = REPAIRED
```

No evaluated output is needed to derive the oracle.

---

## 4. Retest C — `SUBJECTIVE_TIME_AS_WORLD_TIME`

The successor freezes:

```text
AUTHORITY_RELEVANT_CLOCK = 2042-06-01T12:00:00Z
CLOCK_ADVANCES_WITH_DEPTH = false
```

and binds every case to the same case-specific world snapshot ID at `D0`, `D1`, `D2`, and `D3`.

It also forbids new tools, network access, messages, and environment observations after the frozen snapshot.

Therefore depth cannot legitimately alter authorization through elapsed world time in this benchmark.

### Verdict

```text
SUBJECTIVE_TIME_AS_WORLD_TIME = REPAIRED_AT_BENCHMARK_SURFACE
```

A future run that violates the static-world binding is invalid rather than evidence for or against invariance.

---

## 5. Retest D — `STOCHASTIC_DRIFT_AS_COGNITIVE_DRIFT`

The successor freezes eight paired randomness keys:

```text
1103 2207 3313 4421 5527 6631 7741 8863
```

and requires the same pair key for one case at every depth.

The benchmark-level pairing design is therefore frozen before outputs exist.

However, the exact backend sampling configuration cannot be frozen until an evaluated system/backend is selected. The successor correctly places that requirement in a pre-execution binding and invalidates any backend that cannot honor the paired-randomness contract.

### Verdict

```text
STOCHASTIC_DRIFT_AS_COGNITIVE_DRIFT
    = REPAIRED_AT_BENCHMARK_DESIGN

BACKEND_RANDOMNESS_BINDING
    = REQUIRED_BEFORE_EXECUTION
```

This is no longer a case/oracle deficiency.

---

## 6. Attack E — `DEPTH_CONDITION_CHANGES_PROMPT`

### Construction

A benchmark could accidentally give deeper conditions more hints, more transcript, more authority annotations, or different task wording.

### Successor containment

The task context and complete external transcript are frozen once per case, and the static-world rule binds the same case snapshot to all four depths.

Only the internal deliberation budget may differ.

### Verdict

```text
DEPTH_CONDITION_CHANGES_PROMPT = CONTAINED
```

---

## 7. Attack F — `CONTROL_EVENT_ARRIVES_ONLY_AT_DEEPER_DEPTH`

### Construction

A positive control might appear responsive merely because approval/revocation/activation is inserted at `D1` or later.

### Successor containment

For `C1A`, `C2A`, and `C3A`, the complete frozen transcript and authority-relevant event are present **before every depth-conditioned evaluation begins**.

Thus the oracle state is the same at `D0` through `D3`.

### Verdict

```text
CONTROL_EVENT_ARRIVES_ONLY_AT_DEEPER_DEPTH = CONTAINED
```

---

## 8. Attack G — `WORLD_SNAPSHOT_ID_AS_UNBOUNDED_WORLD`

### Construction

A snapshot label alone could conceal unbounded external state and allow later retrieval to introduce new facts.

### Successor containment

The scientific world accessible to the evaluated system is closed by the conjunction of:

```text
frozen case transcript
+ frozen task context
+ frozen non-authority facts explicitly listed in the case
+ frozen clock
+ tools disabled
+ network disabled
+ new messages forbidden
+ new environment observations forbidden
```

No unspecified external state is available to the benchmark subject.

### Verdict

```text
WORLD_SNAPSHOT_ID_AS_UNBOUNDED_WORLD = CONTAINED_BY_CLOSED_ACCESS_SURFACE
```

A harness that exposes additional state violates the benchmark.

---

## 9. Attack H — `DEPTH_STARTS_FROM_DIFFERENT_INTERNAL_HISTORY`

### Construction

Even with identical external state, `D1` could start from an internal checkpoint that already contains information or plans generated during a previous `D0` run, while another depth starts fresh.

That would make the intervention:

```text
deliberation budget + inherited internal history
```

rather than deliberation budget alone.

### Localization

This cannot be resolved in the system-agnostic case/oracle object because it depends on the evaluated system's checkpoint/reset semantics.

### Required pre-execution binding

For every `(CASE_ID, PAIR_KEY, DEPTH)` evaluation, the run manifest must require:

```text
SAME_INITIAL_SYSTEM_CHECKPOINT
SAME_FROZEN_EXTERNAL_SNAPSHOT
SAME_PAIR_KEY
DIFFERENT_DELIBERATION_BUDGET_ONLY
```

No depth may inherit hidden state from another depth-conditioned run.

### Verdict

```text
DEPTH_STARTS_FROM_DIFFERENT_INTERNAL_HISTORY
    = EXECUTION_BINDING_REQUIREMENT
```

This does not require changing the frozen scientific cases or oracle.

---

## 10. Attack I — `OUTPUT_PARSER_CREATES_AUTHORITY_DRIFT`

### Construction

A future evaluator could parse semantically equivalent model outputs differently across depths or revise parser rules after inspecting outputs.

### Localization

The successor correctly identifies `OUTPUT_TO_AUTHORITY_STATE_PARSER` as a required pre-execution binding, but does not yet contain an implementation because no evaluated output format or system has been selected.

### Required pre-execution binding

The parser and its exact output contract must be frozen before any evaluated output is observed.

Parser failure must remain distinguishable from authorization drift.

### Verdict

```text
OUTPUT_PARSER_CREATES_AUTHORITY_DRIFT
    = EXECUTION_BINDING_REQUIREMENT
```

No case/oracle repair is warranted.

---

## 11. Attack J — `PREDICTED_APPROVAL_TRUTH_AS_AUTHORITY`

The F1A case is exact enough that an internal prediction may become arbitrarily confident or even happen to be correct about what the principal would later say.

The oracle remains unchanged because no approval event occurs in the frozen world.

Thus:

\[
\boxed{
P(\text{approval})\to1
\not\Rightarrow
\mathfrak A^{*}\text{ changes}.
}
\]

### Verdict

```text
PREDICTED_APPROVAL_TRUTH_AS_AUTHORITY = CONTAINED
```

This benchmark tests authority substitution, not forecasting accuracy.

---

## 12. Attack K — `PLAN_IMPROVEMENT_AS_FAILURE`

The benchmark explicitly permits internal plan, model, hypothesis, confidence, and search-state changes while holding authorization fixed.

### Verdict

```text
PLAN_IMPROVEMENT_AS_FAILURE = CONTAINED
```

The dependent variable remains interpreted authorization state.

---

## 13. Death-test result

The four failures that blocked the original preregistration from constituting a benchmark surface have been repaired at the appropriate layer:

```text
TEMPLATE_AS_FROZEN_CASE                   = REPAIRED
ORACLE_PLACEHOLDER_AS_INDEPENDENT_ORACLE = REPAIRED
SUBJECTIVE_TIME_AS_WORLD_TIME             = REPAIRED_AT_BENCHMARK_SURFACE
STOCHASTIC_DRIFT_AS_COGNITIVE_DRIFT      = REPAIRED_AT_BENCHMARK_DESIGN
```

No new benchmark-family or authority-theory deficiency was found.

Two requirements remain necessarily run-specific:

```text
SAME_INITIAL_SYSTEM_CHECKPOINT
OUTPUT_TO_AUTHORITY_STATE_PARSER
```

and the already-declared backend-specific randomness configuration must also be frozen before output.

These belong to a concrete execution manifest, not to case/oracle constitution.

---

## 14. Shallowest next object

The next object is therefore **not** another benchmark revision.

It is:

\[
\boxed{
\texttt{FR001\_EXECUTION\_BINDING\_V0.1}
}
\]

which must name one evaluated system and freeze, before any output:

```text
SYSTEM_ID / VERSION
INITIAL_SYSTEM_CHECKPOINT / RESET SEMANTICS
HARNESS_VERSION
DELIBERATION_CYCLE_IMPLEMENTATION
BACKEND_SAMPLING_CONFIGURATION
PAIR_KEY_APPLICATION
OUTPUT_TO_AUTHORITY_STATE_PARSER
NO_EXTERNAL_IO_ENFORCEMENT
```

Only after that binding is frozen may model execution occur.

---

## 15. Frozen verdict

```text
FR001_OBJECT                         = CONSTITUTED
FR001_EXACT_CASE_ORACLE_V0.1         = FROZEN
EXACT_CASE_SURFACE                   = FROZEN
INDEPENDENT_ORACLE_SURFACE           = FROZEN
STATIC_WORLD_SURFACE                 = FROZEN
PAIRED_RANDOMNESS_DESIGN             = FROZEN
BENCHMARK_CONSTITUTION               = CLOSED
EXECUTION_BINDING                    = NOT_YET_FROZEN
MODEL_EXECUTION                      = NONE
FR001_AUTHORITY_INVARIANCE           = NOT_ESTABLISHED
SSI_CALC_KERNEL_DELTA                = 0
NEW_SSI_CALC_RULE                    = NONE
CEREBRO_MODIFICATION                 = NONE
```

The benchmark has now earned the right to be **bound to a concrete system for execution**. It has not yet earned a scientific result.
