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

The redesign removes the semantic confound in which topology separation could also mean correct versus corrupted provenance.

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

Current result:

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

## Deliberately unresolved

The prospective kernel question is not assumed:

\[
\ker q\stackrel{?}{\subseteq}\ker T_{\rm future}.
\]

```text
FUTURE_OBLIGATION_ACCESSED      = FALSE
N0_TO_N4_ON_REDESIGN            = NOT_EVALUATED
CAPABILITY_SURFACE_HARDENING    = NOT_EVALUATED
G_ACTIVATION                    = PROHIBITED
DELTA_PI                        = NOT_EVALUATED
FREEZE_PACKET                   = NOT_FROZEN
AUTHORIZATION_CERTIFICATE       = NOT_ISSUED
FUTURE_RUN                      = NOT_AUTHORIZED
```

If this construction later survives the full preactivation audit and prospective authorization, the first post-gate scientific endpoint is revision-probe reachability:

\[
G\rightarrow\Delta\Pi.
\]

A newly reachable probe earns possibility, not authority.

## Stop condition

This construction audit licenses only one next question: whether the redesigned object survives the full preactivation noninterference/capability ladder.

No `G=1`. No future obligation. No prospective runner.
