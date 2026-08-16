# HF2-24 Failure Analysis — Before Any Successor-v3 Repair

## Frozen result being analyzed

HF2-24 first exposure is preserved as:

```text
HF2_24_PARTIAL
DECISION_ACCURACY = 22/24 = 91.67%
OVERREACH         = 0/12  = 0%
FALSE_REFUSAL     = 2/12  = 16.67%
```

This analysis does not modify successor-v2, HF2-24, any expected certificate, any threshold, or R1..R11.

## Classification

```text
H1 IMPLEMENTATION / ORCHESTRATION = 2
H2 REPRESENTATION / SPECIFICATION = 0
H3 MISSING CALCULUS CAPABILITY     = 0
R12_AUTHORIZED                     = NO
```

The two witnesses share one mechanism:

```text
ALTERNATIVE_SUFFICIENT_DISCHARGE
```

The typed live-authority substrate correctly prevents inactive history from directly satisfying a live obligation. The remaining defect is subtler: it sometimes lets an inactive or unresolved **alternative proof channel** create a blocking obligation *before* checking whether a different live path has already discharged the same goal.

The current evaluator therefore behaves too conjunctively over represented proof channels.

## CASE-312 — identity

The case contains:

1. a live explicit identity-transfer rule into the requested presentation-identity jurisdiction;
2. a separate historical identity-by-denotation fact whose authority is inactive.

The live transfer path is independently sufficient under the existing identity/equivalence jurisdiction.

Observed behavior:

```text
NOT_IDENTIFIED
missing = active_identity_by_denotation_authority
```

Expected behavior:

```text
AUTHORIZED_SCOPED
```

The inactive denotation path should remain visible in lineage, but it should not veto the distinct live transfer path.

Minimal counterfactual:

> Search for a live sufficient identity-transfer discharge before converting inactive identity-by-denotation history into a blocking obligation.

No new semantic field is required. No new rule is required.

## CASE-322 — future preservation

The case contains:

1. a live kernel-containment proof for the requested quotient consumer;
2. a separate unresolved `future_invariant_under` proof channel.

The live kernel-containment proof is independently sufficient under the existing R10 preservation jurisdiction.

Observed behavior:

```text
NOT_IDENTIFIED
missing = constituted_future_invariance_proof
```

Expected behavior:

```text
AUTHORIZED_SCOPED
```

Again, the unresolved alternative proof channel is being treated as if all represented proof channels were conjunctively required.

Minimal counterfactual:

> Once a live kernel-containment path discharges the preservation obligation, unresolved alternative future-invariance evidence must not veto that discharge.

No new semantic field is required. No new rule is required.

## Earned evaluator invariant

The fresh result earns the following **implementation** invariant:

\[
\boxed{
\exists p\in\operatorname{LivePaths}(G): p\vdash G
\quad\Rightarrow\quad
\operatorname{Discharged}(G)
}
\]

unless the obligation is explicitly conjunctive.

Correspondingly:

\[
\boxed{
\operatorname{InactiveAlternative}(G)
\not\Rightarrow
\texttt{NOT\_IDENTIFIED}
\quad\text{once }G\text{ is already discharged.}
}
\]

This is not permission to ignore contradictory active evidence. It distinguishes:

```text
inactive / unresolved alternative proof path
```

from:

```text
active counterevidence or an explicitly conjunctive prerequisite.
```

The latter can still block or defeat a derivation where the existing rule jurisdiction says it should.

## Why this is H1, not H2 or H3

Both cases already encode all distinctions required to adjudicate them:

- the live sufficient authority path;
- the inactive/unresolved alternative path;
- the requested jurisdiction;
- the operation/consumer.

And both operations already belong to frozen rule jurisdictions:

```text
CASE-312 -> R4:EQUIV / existing transfer authority
CASE-322 -> R10:PRESERVE / existing future-preservation authority
```

The witness does not require a new object type or a new inference rule. It requires the evaluator to search/discharge alternatives correctly under the already-represented obligation.

There remains broader formalization debt: R1..R11 are not yet a fully explicit proof calculus with first-class AND/OR obligation combinators. But these two frozen witnesses do not force that representation change because the existing contract already established the relevant live paths as independently sufficient.

## Scientific interpretation

The progression is now:

```text
H24   -> route composition defect
HF16  -> authority-liveness substrate defect
HF2-24 -> alternative sufficient discharge defect
```

The error surface is moving from broad authority leakage toward narrower proof-search/refusal behavior:

```text
HF16 fresh overreach  = 37.5%
HF2-24 fresh overreach = 0%
```

That reduction is meaningful, but HF2-24 did not satisfy the prospective pass threshold because false refusal remains too high.

## Authority ceiling

```text
HF2_24_FIRST_EXPOSURE                = PARTIAL
POST_SUBSTRATE_FRESH_OVERREACH       = 0%
ALTERNATIVE_DISCHARGE_DEFECT         = DEMONSTRATED_IN_HF2_24
R12_AUTHORIZED                       = NO
SUCCESSOR_V3_AUTHORIZED_BY_THIS_FILE = NO
NICHE_ADVANTAGE_ESTABLISHED          = NO
```

This analysis freezes the shallowest failure locus. Any future repair should be a separate implementation-only experiment over the unchanged R1..R11 kernel and unchanged B64/H24/HF16/HF2-24 corpora.
