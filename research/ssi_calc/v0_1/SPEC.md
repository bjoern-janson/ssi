# SSI-CALC v0.1 — Frozen Research Contract

Status: `PRE-CHECKER_BENCHMARK_FREEZE_CANDIDATE`

SSI-CALC v0.1 is an engineering hypothesis: a small typed calculus may detect and localize authority-transfer failures in semantic transformation pipelines with less modeling effort and better repair locality than practical baseline methods.

The v0.1 object is:

\[
\boxed{\texttt{SSI\_CALC\_V0.1}=(\mathcal K,\Sigma,\mathcal D,\mathcal B,\mathcal M)}
\]

where \(\mathcal K\) is the rule kernel, \(\Sigma\) the typed case language, \(\mathcal D\) the future evaluator, \(\mathcal B\) the frozen benchmark, and \(\mathcal M\) the later comparative scoring procedure.

This artifact freezes only the benchmark-facing contract. It does not implement the checker and does not claim niche advantage.

## 1. Hard rule budget

\[
\boxed{|\mathcal K_{v0.1}|\le 15}
\]

Initial rule names:

| Rule | Name | Intended jurisdiction |
|---|---|---|
| R1 | `DECLARE` | constitute typed objects and relations |
| R2 | `ADMIT` | admit an external regime for a declared scope |
| R3 | `LICENSE` | constitute a scoped authority-bearing transformation edge |
| R4 | `EQUIV` | constitute purpose-indexed semantic equivalence |
| R5 | `SUBSTITUTE` | consume an equivalence inside its licensed jurisdiction |
| R6 | `CONGRUENCE` | show preservation under a declared operation/context family |
| R7 | `TRANSPORT` | align/transport across constituted carriers |
| R8 | `QUOTIENT` | form a quotient only for an already licensed equivalence scope |
| R9 | `COMPOSE` | compose authority-bearing transformations only when explicitly licensed |
| R10 | `PRESERVE` | discharge a declared preservation/future-sufficiency obligation |
| R11 | `REOPEN` | restore alternatives when a prior contraction loses authority |

Four rule slots remain intentionally unused. `STOP` and refusal statuses are evaluator outcomes, not inference rules.

No new rule may enter \(\mathcal K\) before a frozen benchmark witness demonstrates missing derivation capability.

## 2. Authority is an edge, never a global scalar

The implementation must not contain a primitive equivalent to `Authority(x)=true`.

A licensed authority object is an edge:

\[
A:X\xrightarrow[\kappa]{P,J,E}Y
\]

where \(P\) is provenance, \(J\) is jurisdiction/scope, \(E\) is evidential basis, and \(\kappa\) is the semantic purpose. Authority at \(\kappa\) does not imply authority at \(\kappa'\). Any transfer between jurisdictions requires a derivation.

## 3. Benchmark-first invariant

Development order:

```text
benchmark -> schema -> minimal checker -> baseline comparison
```

The benchmark is the primary research artifact. The checker is the executable hypothesis evaluated against it.

The frozen benchmark contains exactly 64 cases: `8 families x 8 cases`.

| Family | Target failure class |
|---|---|
| `F1_ORACLE` | oracle / information-flow authority leakage |
| `F2_SUBSTITUTION` | equivalence-to-substitution scope leakage |
| `F3_COMPOSITION` | local-to-joint composition authority leakage |
| `F4_IDENTITY` | equivalence/reference-to-identity leakage |
| `F5_PROVENANCE` | provenance/metadata-to-semantics leakage |
| `F6_REGIME` | scoped-regime-to-broader-jurisdiction leakage |
| `F7_TRANSPORT` | cross-carrier alignment / transport leakage |
| `F8_FUTURE` | local quotient/congruence-to-future-sufficiency leakage |

Each family contains authorized cases, refused cases, at least one `NOT_IDENTIFIED`, and at least one `REOPEN`.

Every case freezes expected status, shallowest failure locus, valid facts that must survive refusal/revision, and missing authority required for success.

## 4. Preservation-aware refusal

A fact being present does not authorize every downstream use. An authority edge being present does not automatically compose with another authority edge.

A valid upstream derivation must survive a downstream refusal unless the case explicitly authorizes reopening or withdrawal.

\[
\boxed{\text{reject the illegal edge without destroying unaffected valid upstream structure}}
\]

## 5. Frozen evaluator outcomes

```text
AUTHORIZED
AUTHORIZED_SCOPED
NOT_IDENTIFIED
SEMANTIC_TYPE_ERROR
UNLICENSED_JURISDICTION_TRANSFER
UNLICENSED_TRANSPORT
CONGRUENCE_FAILURE
COMPOSITION_FAILURE
PROVENANCE_LEAK
REGIME_MISMATCH
JURISDICTIONAL_DIVERGENCE
FUTURE_UNSAFE
EXTERNAL_AUTHORITY_REQUIRED
REOPEN
```

## 6. Shallowest failure loci

```text
NONE DECLARE ADMIT LICENSE EQUIV SUBSTITUTE CONGRUENCE TRANSPORT
QUOTIENT COMPOSE PRESERVE TRANSFER PROVENANCE REOPEN
```

The checker is scored against the shallowest correct locus. A deeper explanation does not earn full localization credit if a shallower missing authority object already blocks the derivation.

## 7. Competitive hypothesis

\[
\boxed{H_{0.1}:\text{ SSI-CALC improves localization and/or specification cost on authority-transfer tasks without sacrificing detection accuracy.}}
\]

The niche is semantic transformations whose validity depends on jurisdiction, equivalence scope, provenance, composition, alignment, and preservation obligations.

\[
\boxed{\neg H_{0.1}\Rightarrow\texttt{NICHE\_ADVANTAGE\_NOT\_ESTABLISHED}}
\]

No theory-level reinterpretation may convert a failed comparison into success.

The baseline suite and metric weights are intentionally not frozen here; they must be constituted and frozen before comparative execution.

## 8. Non-goals

v0.1 does not claim to decide arbitrary truth, solve identity in general, replace theorem provers/model checkers/policy engines, infer semantic authority from provenance, force underdetermined cases to be determinate, prove general future safety, provide universal semantics, or validate SSI as a whole.

## 9. Rule-growth discipline

For any proposed `R12`–`R15`, record:

```text
trigger_case
observed_missing_capability
why_existing_rules_cannot_derive_it
minimal_new_rule
full_64_case_regression_result
```

If no frozen case requires the capability, the rule does not enter v0.1.

> **Benchmark first. No earned rule, no rule.**
