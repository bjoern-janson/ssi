# SSI — Safe Self-Improvement

> **Research on reality-tracking interfaces, scoped authority, evidence typing, and corrigible transformation.**

SSI studies a recurring failure mode in adaptive systems: a system can produce a locally correct answer, transformation, or certificate while still lacking the information or authority needed to generalize that success across a boundary.

The program therefore keeps several distinctions explicit:

```text
Can != May != Did
information != evidence != authority
representation != legitimacy of representation
semantic identity != evidence admission != provenance != uncertainty
validity != transportability != composability
local preservation != path preservation
```

The repository is empirical-first. Claims are frozen at the narrowest scope actually supported by constituted cases, oracles, protocols, evaluators, and first results.

---

## Current frontier

The current research state is summarized in [`research/CURRENT_FRONTIER.md`](research/CURRENT_FRONTIER.md).

The empirical ladder now includes:

```text
PR59  transition-role separation
PR60  held-out structural transport
PR61  semantic / evidential transport
PR63  adequacy / reopening governor
PR64  H9 positive-adequacy constitution collision
PR65  negative one-bit candidate search
PR67  external-to-SSI mapping contract M_F [draft / branch-local]
```

The important correction after PR67 is that an apparent path-level collision was **not** a valid SSI path collision. Localization found that the external paths had been collapsed while constructing SSI-local inputs, before the frozen SSI certificate boundary was reached.

Current status:

```text
FIRST_ECDSA_RESULT
    = INVALID_AS_PATH_COLLISION
      __PRE_CERTIFICATE_MAPPING_COLLAPSE

M_F
    = FROZEN_ON_PR67
      __SUPPORTED_ON_FROZEN_ABSTRACT_MAPPING_SUITE

COMPLETE_PATH_RUN_BUNDLE
    = NOT_CONSTITUTED

PATH_RUN_AFTER_M_F
    = NOT_EXECUTED

PATH_LEVEL_INADEQUACY
    = NOT_ESTABLISHED

CERTIFICATE_PROJECTION_LOSS
    = NOT_TESTED

RELATIONAL_COMPOSITION_FAILURE
    = NOT_TESTED

COMPOSITION_INSUFFICIENCY
    = NOT_ESTABLISHED

SSI_CALC_KERNEL_DELTA
    = 0
```

The current hard methodological rule is:

> **Constitute the witness at every interface it is supposed to falsify.**

The next scientific increment is not a new theory object or checker repair. It is a self-contained, independently resolvable path-run dependency bundle.

---

## Core research architecture

A central object is a licensed transition:

```text
X_t --T--> X_{t+1}
```

The governing question is:

> **What independently constituted warrant licenses T?**

A recurring failure pattern is:

```text
A, B !=> standing for R(A,B)
```

or, more compactly:

> **The standing of individually legitimate ingredients does not automatically become the standing of the relation that consumes them.**

This is why SSI separates evidence validity, evidence admission, provenance, authority, transport, and composition rather than allowing one successful local result to authorize all downstream uses.

---

## Read the repository in the right order

### Fast route

1. **[`research/CURRENT_FRONTIER.md`](research/CURRENT_FRONTIER.md)** — exact current research stop.
2. **This README** — front-door orientation.
3. **[`RESEARCH_MAP.md`](RESEARCH_MAP.md)** — research topology.
4. **[`REPOSITORY_STATUS.md`](REPOSITORY_STATUS.md)** — administrative/scientific status board.
5. **[`research/SSI_BIG_PICTURE.md`](research/SSI_BIG_PICTURE.md)** — non-authoritative synthesis.
6. **[`research/relicense/README.md`](research/relicense/README.md)** — transition/relicense lineage.

### Evidence route

For a frozen experiment, follow its dependency order whenever those artifacts exist:

```text
SPEC
-> CASES
-> BINDINGS / CANDIDATE
-> independent ORACLE
-> PROTOCOL
-> EVALUATOR / RUNNER
-> FIRST RESULT
```

A later success never rewrites an earlier frozen failure.

---

## Current empirical spine

### PR59 — role separation

The task-relative transition tuple

```text
K = (S, L, V, Lambda)
```

was separable on the frozen constructed suite.

Strongest result:

```text
FOUR_COORDINATE_TRANSITION_INTERFACE_SEPARABILITY
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE
```

### PR60 — held-out structural transport

The factorization survived the evaluable held-out axes. Observation-channel novelty remained:

```text
NOT_EVALUABLE_UNDER_FROZEN_BINDING
```

This preserves the distinction between information existing and the frozen interface being entitled to consume it.

### PR61 — semantic / evidential transport

Already constituted meaning crossed changed carriers on the frozen constructed cross-carrier suite while semantic identity, evidence type, provenance, uncertainty, and role identity remained separated.

Strongest result:

```text
TRANSITION_SEMANTIC_TRANSPORT
    = SUPPORTED_ON_FROZEN_CONSTRUCTED_CROSS_CARRIER_SUITE
```

### PR63–65 — disciplined reopening

PR63 supplied a narrow adequacy/reopening governor. PR64/H9 exposed:

```text
coverage assertion != coverage warrant
```

PR65 then tested five plausible one-bit repairs and found:

```text
NO_EXACT_CANDIDATE
```

No repair or new coordinate was licensed.

### PR67 — constituted external-to-SSI mapping

PR67 freezes:

```text
M_F : E(T) -> I_F(T)
```

with explicit dispositions:

```text
PRESERVE
NORMALIZE
EXCLUDE_WITH_BASIS
NOT_EVALUABLE
```

and a backward-flow firewall preventing path consequences, certificate outputs, collision expectations, or desired diagnoses from influencing the mapping.

Mapper-only first exposure: `12/12` on the frozen abstract mapping suite.

PR67 is branch-local / draft and remains bounded by its own authority ceiling.

---

## Current path question

The path-level target remains conceptually:

```text
Psi_F(P_A) == Psi_F(P_B)
AND
Y_path(P_A) != Y_path(P_B)
```

but it is meaningful only after the complete experiment is constituted through every interface:

```text
external path
-> frozen M_F
-> SSI local input
-> frozen SSI certificate
-> ordered certificate history
-> independent path consequence
```

The previous apparent collision failed this requirement because the mapper constructed equal SSI inputs rather than deriving them from the external path records.

The next run is blocked until the entire dependency closure is frozen and independently resolvable.

---

## Reproducibility boundary

For a run dependency set

```text
D_R = {
  M_F,
  P_A,
  P_B,
  Y_path evaluator,
  one-shot runner,
  freeze manifest,
  exact SSI dependencies
}
```

every dependency must be:

```text
identified
AND immutable
AND resolvable by the executor
```

Important nonrules:

```text
artifact exists != artifact is addressable
artifact is addressable != artifact is reachable by this executor
research-state assertion != reproducibly accessible artifact
```

A package that requires reconstructing scientific state from conversation or hidden repository knowledge is not yet a valid experimental artifact.

---

## What is deliberately not established

```text
GENERAL_SAFE_SELF_IMPROVEMENT             = NOT_ESTABLISHED
LEVEL_3_INTERFACE_INVENTION               = OPEN
PATH_LEVEL_SSI_INADEQUACY                 = NOT_ESTABLISHED
CERTIFICATE_PROJECTION_LOSS               = NOT_TESTED
RELATIONAL_COMPOSITION_FAILURE            = NOT_TESTED
COMPOSITION_INSUFFICIENCY                 = NOT_ESTABLISHED
COMPOSITION_THEOREM                       = NOT_EARNED
NEW_RELATION                              = NOT_EARNED
NEW_COORDINATE                            = NOT_EARNED
SSI_NOVELTY                               = NOT_ESTABLISHED
SSI_CALC_KERNEL_DELTA                     = 0
```

The absence of a claim is part of the scientific state, not an invitation to infer it.

---

## Research discipline

1. **Constitute before evaluating.** Candidate output must not define oracle truth.
2. **Preserve typed negative results.** `NOT_EVALUABLE`, `NOT_SUPPORTED`, `UNPROVEN`, and `REVOKED` are different states.
3. **Localize before repairing.** Revise at the shallowest supported failure locus.
4. **Preserve first results.** Later repairs do not rewrite earlier failures.
5. **Do not manufacture collisions by mapping.** Equality at a tested interface must be a derived result.
6. **Preserve authority ceilings.** Validity does not automatically grant transport, composition, repair, or execution authority.
7. **Require dependency closure for reproducibility.** Described provenance is not enough if an executor cannot resolve the exact bytes.

---

## Repository map

```text
.
├── README.md
├── RESEARCH_MAP.md
├── REPOSITORY_STATUS.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── benchmarks/
├── empirical/
├── energy/
├── research/
│   ├── CURRENT_FRONTIER.md
│   ├── SSI_BIG_PICTURE.md
│   ├── ledger/
│   ├── relicense/
│   ├── semantic_constitution/
│   └── ssi_calc/
├── results/
├── retrospective/
└── theory/
```

---

## Status of this README

This README is navigation, not a scientific authority source. If it conflicts with a frozen experiment artifact, first-result ledger, or exact authority ceiling, the frozen object governs.

> **Newest file wins is not an epistemic rule in this repository.**

---

## License

See [`LICENSE`](LICENSE).
