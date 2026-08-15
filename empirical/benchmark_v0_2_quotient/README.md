# VFA-0.2 — Quotient Revision Topology

## Lineage identity

```text
VFA-0.1-REJECTED_RETRIEVAL_LEAKAGE
    ->
VFA-0.2-DORMANT-CORRECTIVE-RESERVE
    ->
VFA-0.2-HOSTILE-FACTORIZATION-ATTACK-1
    -> OPEN_CAPABILITY_SURFACE
    ->
VFA-0.2-QUOTIENT-REVISION-TOPOLOGY
```

This lineage preserves the earlier failures. It does not repair or overwrite them.

The redesign removes the deeper semantic confound in which topology separation could also mean correct versus corrupted provenance.

## Governing wager

> **A distinction can have zero present behavioral value yet positive future corrective option value.**

Dual:

> **Present behavioral equivalence does not certify future corrective equivalence.**

## Treatment identity

Both arms share one immutable validated substrate:

\[
\mathcal W_A=\mathcal W_B=\mathcal W.
\]

The arm difference lives only in revision-path equivalence structure:

\[
D_A=(\mathcal W,\Gamma_A),\qquad D_B=(\mathcal W,\Gamma_B).
\]

`VALIDATED_SUBSTRATE.json` is literally the same truth-bearing object for both arms. `GAMMA_A.json` and `GAMMA_B.json` contain the same 24 path records and the same source-fact references. Neither Gamma carries truth values, validation status, or transformation-class payloads.

The treatment is only the partition of those identical path records into revision-equivalence classes.

## Quotient

\[
q:\Gamma_A\rightarrow\Gamma_B
\]

acts only on path-equivalence labels. Within each relation kind, source case IDs are sorted lexicographically and adjacent IDs are merged. There is no seed search, semantic-score search, or future-obligation information in the quotient rule.

Thus B is a coarser quotient of the same validated substrate, not a scrambled or false substrate.

## Construction audit 1

The known-domain requirement is:

\[
F\circ q=F.
\]

Result:

```text
D_SEMANTIC                 = PASS
D_TOPOLOGY                 = PASS
F_COMP_Q_EQUALS_F          = PASS
ordinary tasks             = 249
ordinary trace mismatches  = 0
kernel merged path pairs   = 12
```

Arm representation symmetry:

```text
path records               = 24 / 24
canonical Gamma bytes      = 3189 / 3189
validated substrate        = identical object
truth-bearing Gamma fields = none
```

Path descriptor:

```text
Phi_path A:
  distinct path classes        24
  singleton path fraction      1.0
  mean equivalence class size  1.0
  reopen distinct classes      6

Phi_path B:
  distinct path classes        12
  singleton path fraction      0.0
  mean equivalence class size  2.0
  reopen distinct classes      3
```

Aggregation of these dimensions is prohibited.

## Hardened preactivation attack 1

The redesigned object was then attacked through the full construction-side `N0 -> N4` ladder under the frozen `PREACTIVATION_CALLER_V1` capability model.

```text
N0 endpoint equality        = PASS
N1 full trace equality      = PASS
N2 metamorphic invariance   = PASS
N3 transitive non-use       = PASS
N4 capability surface       = PASS

N2 comparisons              = 101592
N2 mismatches               = 0
module-global checks        = 2988
module-global mismatches    = 0
gate comparisons            = 170
gate mismatches             = 0
capability-smuggling tries  = 530
capability-smuggling accepted = 0
```

Therefore the current construction status is:

```text
D_PRE_ACTIVATION_HARDENED = PASS
SCOPE = PREACTIVATION_CALLER_V1
```

This scope matters. The certificate covers hostile caller inputs, arbitrary dormant Gamma objects, serialization/order/allocation perturbations, extra-field/argument smuggling, and unrelated Gamma-named global injection. It is not an OS sandbox or arbitrary in-process code-rewrite claim.

## Fresh authorization re-audit 1

The quotient treatment then received a fresh authorization audit rather than inheriting the rejected VFA-0.1 A–D states mechanically.

```text
A = PASS
B = PASS
C = PASS
D = PASS
E = NOT_EVALUATED
F = NOT_EVALUATED
G = NOT_EVALUATED
H = NOT_EVALUATED
I = NOT_EVALUATED
```

A is re-earned from the unchanged prospective source/scope selector. B is re-earned from the same-truth quotient construction and frozen `Phi_path` descriptor. C is re-earned from exact present-state equality outside the declared partition. D is re-earned from `F o q = F`, exact full-trace identity on all 249 ordinary pre-freeze tasks, and the hardened metamorphic audit.

The audit stops at E because no complete content-addressed A/B resource-information-exposure manifest exists yet. Equal Gamma bytes, path counts, preactivation traces, and N4 closure are not sufficient to infer equality of runtime, compute, memory, post-gate operation budget, tools, evaluator access, stopping rule, or disclosure evidence.

Current authorization state:

```text
CONSTRUCTION_VALID = YES
AUTHORIZATION_VALID = NO
FUTURE_HYPOTHESIS_TESTED = NO

FUTURE_OBLIGATION_ACCESSED = FALSE
G_ACTIVATION = PROHIBITED
DELTA_PI = NOT_EVALUATED
FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
FUTURE_RUN = NOT_AUTHORIZED
```

See:

- `AUTHORIZATION_REAUDIT.md`
- `AUTHORIZATION_STATUS.json`
- `evidence/E_RESOURCE_INFORMATION_EXPOSURE_GAP.md`

## Deliberately unresolved

The prospective kernel question is still not assumed:

\[
\ker q\stackrel{?}{\subseteq}\ker T_{\rm future}.
\]

```text
FUTURE_OBLIGATION_ACCESSED      = FALSE
G_ACTIVATION                    = PROHIBITED
DELTA_PI                        = NOT_EVALUATED
FREEZE_PACKET                   = NOT_FROZEN
AUTHORIZATION_CERTIFICATE       = NOT_ISSUED
FUTURE_RUN                      = NOT_AUTHORIZED
```

A construction-side D pass does **not** authorize a prospective run.

## Eventual first scientific endpoint

If and only if this lineage later survives the remaining pre-freeze authorization predicates, the first post-gate scientific endpoint is revision-probe reachability:

\[
G\rightarrow\Delta\Pi.
\]

The intended ladder is:

\[
\mathcal W\rightarrow\Gamma\rightarrow\Delta\Pi\rightarrow E_{\rm fresh}\rightarrow CCA\rightarrow CARS\rightarrow R_{t+1}.
\]

A newly reachable probe earns possibility, not authority.

## Key files

- `construction/VALIDATED_SUBSTRATE.json` — one shared truth-bearing substrate.
- `construction/GAMMA_A.json` / `GAMMA_B.json` — identical path records, different equivalence partitions.
- `construction/QUOTIENT_MAP.json` — deterministic quotient rule.
- `construction/QUOTIENT_CONSTRUCTION_AUDIT.py` / `quotient_construction_audit.json` — same-truth/topology/known-domain audit.
- `construction/CAPABILITY_THREAT_MODEL.json` — frozen scope of the N4 claim.
- `construction/CLOSED_PREACTIVATION_INTERFACE.py` — closed ordinary and gate surfaces.
- `construction/HARDENED_N_LADDER_ATTACK.py` / `hardened_n_ladder_audit.json` — N0-N4 attack.
- `evidence/HARDENED_N_LADDER_ATTACK_1.md` — result interpretation and stop boundary.
- `AUTHORIZATION_REAUDIT.md` / `AUTHORIZATION_STATUS.json` — fresh quotient-treatment authorization audit.
- `evidence/E_RESOURCE_INFORMATION_EXPOSURE_GAP.md` — first unresolved authorization prerequisite.

## Stop condition

No `G=1`. No future obligation. No prospective runner.

The next admissible action is to construct and attack the frozen A/B resource-information-exposure manifest required by predicate E. F–I remain unadjudicated until E passes.
