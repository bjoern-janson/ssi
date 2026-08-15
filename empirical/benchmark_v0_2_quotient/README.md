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

The redesigned object was attacked through the construction-side `N0 -> N4` ladder under frozen caller-capability model `PREACTIVATION_CALLER_V1`.

```text
N0 endpoint equality           = PASS
N1 full trace equality         = PASS
N2 metamorphic invariance      = PASS
N3 transitive non-use          = PASS
N4 capability surface          = PASS
N2 comparisons                 = 101592
N2 mismatches                  = 0
module-global checks           = 2988
module-global mismatches       = 0
gate comparisons               = 170
gate mismatches                = 0
capability-smuggling attempts  = 530
accepted                       = 0
```

Therefore:

```text
D_PRE_ACTIVATION_HARDENED = PASS
SCOPE = PREACTIVATION_CALLER_V1
```

This is caller-interface capability nonreachability, not an OS sandbox or arbitrary in-process code-rewrite claim.

## Fresh authorization re-audit

The quotient treatment receives fresh authorization adjudication rather than inheriting treatment-sensitive VFA-0.1 states.

Current spine:

```text
A = PASS
B = PASS
C = PASS
D = PASS
E = PASS
F = PASS
G = NOT_EVALUATED
H = NOT_EVALUATED
I = NOT_EVALUATED
```

### A — prospective scope

Re-earned from the unchanged Biome source cutoff, admissible future-change class, 180-day horizon, deterministic first-qualifying selector, exclusions, and prospective independence rule.

### B — treatment identity

Re-earned from the same-truth quotient construction:

```text
W_A = W_B
path_records_A = path_records_B
Gamma_B = q(Gamma_A)
```

`Phi_path` is frozen component-wise; aggregation is prohibited.

### C/D — present and ordinary causal equivalence

Re-earned from shared substrate/state and:

\[
F\circ q=F
\]

with exact full-trace identity on all 249 ordinary pre-freeze surrogate tasks and zero mismatches in the hardened preactivation attack.

### E — resource, information, and execution symmetry

E is decomposed as:

\[
E=(E_{\rm capacity},E_{\rm information},E_{\rm execution}).
\]

All three pass under a deterministic logical-resource contract. Raw Gamma labels are hidden behind a fixed treatment view:

\[
M_\Gamma\in\{0,1\}^{24\times24}.
\]

Both arms receive a 576-byte treatment buffer, 24 path slots, 576 materialization comparisons/writes, all 276 unordered pair slots, the same common-evidence interface, and no topology-dependent early stop, randomness, concurrency, cache, tool, API, or network advantage.

The hostile E attack records 192 metamorphic execution-cost comparisons with zero mismatches.

E does **not** claim equal CPU cycles, joules, cache misses, or wall-clock time. Those quantities do not control stopping or the confirmatory estimand in this benchmark version.

### F — treatment isolation and hidden asymmetry

F treats the full equivalence relation `M_Gamma` as the declared treatment object. `Phi_path` is a structural descriptor, not the complete conditioning object.

After masking `M_Gamma` and preregistered deterministic consequences of it:

```text
metamorphic A/B pairs        = 64
residual observable mismatches = 0
```

Blind holdout recovery from residual observables remains at chance:

```text
exact memorizer     = 0.500
categorical stump   = 0.500
1-NN Hamming        = 0.500
chance              = 0.500
```

The primary evidence is exact paired residual identity; classifier failure is secondary.

Positive sensitivity control: raw repository metadata *does* reveal the arm at 100% (`GAMMA_A.json` / `GAMMA_B.json`, raw label namespace, raw Gamma hash). Those channels are explicitly classified as non-material only because predicate E proves they terminate at the trusted materialization boundary and never become arm/evaluator-visible.

```text
unclassified observables            = 0
material undeclared distinguishers  = 0
F                                   = PASS
```

## Current authorization state

```text
CONSTRUCTION_VALID = YES
A_THROUGH_F = PASS
AUTHORIZATION_VALID = NO
FUTURE_HYPOTHESIS_TESTED = NO

FUTURE_OBLIGATION_ACCESSED = FALSE
G_ACTIVATION = PROHIBITED
DELTA_PI = NOT_EVALUATED
KERNEL_FUTURE_INCLUSION = NOT_EVALUATED
FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
FUTURE_RUN = NOT_AUTHORIZED
```

## Deliberately unresolved

The prospective kernel question is still not assumed:

\[
\ker q\stackrel{?}{\subseteq}\ker T_{\rm future}.
\]

Nothing in A–F answers it.

## Eventual first scientific endpoint

If and only if the lineage later survives the remaining pre-freeze authorization predicates, the first post-gate scientific endpoint is revision-probe reachability:

\[
G\rightarrow\Delta\Pi.
\]

The intended ladder is:

\[
\mathcal W\rightarrow\Gamma\rightarrow\Delta\Pi\rightarrow E_{\rm fresh}\rightarrow CCA\rightarrow CARS\rightarrow R_{t+1}.
\]

A newly reachable probe earns possibility, not authority.

## Key files

- `construction/VALIDATED_SUBSTRATE.json` — shared truth-bearing substrate.
- `construction/GAMMA_A.json` / `GAMMA_B.json` — identical path records, different equivalence partitions.
- `construction/QUOTIENT_MAP.json` — deterministic quotient rule.
- `construction/QUOTIENT_CONSTRUCTION_AUDIT.py` / `quotient_construction_audit.json` — same-truth/topology/known-domain audit.
- `construction/CAPABILITY_THREAT_MODEL.json` — frozen N4 scope.
- `construction/CLOSED_PREACTIVATION_INTERFACE.py` — closed ordinary and insufficiency-gate surfaces.
- `construction/HARDENED_N_LADDER_ATTACK.py` / `hardened_n_ladder_audit.json` — N0–N4 attack.
- `construction/E_ENVIRONMENT_MANIFEST.json` — E capacity/information/execution contract.
- `construction/E_ENVIRONMENT_KERNEL.py` — fixed-cost equivalence-matrix exposure kernel.
- `construction/E_ENVIRONMENT_ATTACK.py` / `e_environment_audit.json` — adversarial E audit.
- `evidence/E_RESOURCE_INFORMATION_EXECUTION_PASS.md` — E interpretation and scope.
- `construction/F_TREATMENT_ISOLATION_MANIFEST.json` — F observable/disposition contract.
- `construction/F_TREATMENT_ISOLATION_ATTACK.py` / `f_treatment_isolation_audit.json` — blind residual treatment-recovery attack.
- `evidence/F_TREATMENT_ISOLATION_PASS.md` — F interpretation and positive sensitivity control.
- `AUTHORIZATION_REAUDIT.md` / `AUTHORIZATION_STATUS.json` — current authorization spine.

## Stop condition

No `G=1`. No future obligation. No prospective runner.

The next admissible action is predicate G: re-audit and freeze the prospective common-cause obligation-selection/disclosure mechanism for the quotient lineage. Passing F licenses only that audit; it does not license disclosure or activation.
