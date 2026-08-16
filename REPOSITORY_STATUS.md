# Repository Status and Navigation

Status snapshot: 2026-08-16.

This file is a **navigation and authority map**, not a scientific artifact. It does not override frozen benchmark bytes, authorization certificates, preregistrations, or preserved negative results. If a summary here conflicts with a content-addressed scientific object, the scientific object governs.

## Current repository shape

The repository intentionally contains several kinds of material:

1. **foundation theory** — the core SSI state, Future Sufficiency, CCA/CARS, and the closed V0.x localization program;
2. **preserved scientific lineage** — failed, rejected, superseded, and authorized benchmark states retained for provenance;
3. **active prospective experiment** — VFA-0.2 Packet 7, frozen and authorized but not yet realized;
4. **post-authorization interpretation/theory** — blind outcome adjudication and Future-Safe Option Structure, explicitly outside Packet 7;
5. **jurisdiction-falsification work** — one failed executed S0 lineage plus a separate semantic-constitution lineage whose current frontier is V8 identity constitution;
6. **parallel research tracks** — archival recovery, A1 statehood work, energy experiments, and competition work that do not automatically inherit authority from VFA or jurisdiction falsification.

The repository should therefore not be read as "latest filename wins." Scientific authority is local to an explicitly identified lineage and object.

## Authoritative VFA state

The current prospective benchmark is:

```text
BENCHMARK = VFA-0.2-QUOTIENT-REVISION-TOPOLOGY
PACKET = VFA-0.2-FROZEN-PACKET-7
A = PASS
B = PASS
C = PASS
D = PASS
E = PASS
F = PASS
G = PASS
H = PASS
I = PASS
STATE = AUTHORIZED_FUTURE_NOT_YET_REALIZED
FUTURE_OBLIGATION_ACCESSED = FALSE
FUTURE_RUN = NOT_EXECUTED
```

Authoritative routing:

- `empirical/benchmark_v0_2_quotient/AUTHORIZATION_STATUS.json` — current A-I and authority state.
- `empirical/benchmark_v0_2_quotient/construction/I_FREEZE_PACKET_V7.json` — frozen Packet 7 manifest.
- `empirical/benchmark_v0_2_quotient/construction/I_FREEZE_ANCHOR_V7.json` — packet-to-Git freeze anchor.
- `empirical/benchmark_v0_2_quotient/construction/I_AUTHORIZATION_CERTIFICATE.json` — issued authorization certificate.
- `empirical/benchmark_v0_2_quotient/evidence/I_CHAIN_OF_CUSTODY_PASS.md` — predicate-I interpretation and external execution evidence.
- `research/post_authorization/VFA_0_2_BLIND_OUTCOME_ADJUDICATION.json` — blind interpretation map; **no execution authority**.
- `theory/FUTURE_SAFE_OPTION_STRUCTURE.md` — post-authorization theory note; **not a Packet 7 member**.

Packet 7 identifiers:

```text
PACKET_SHA256 = 2d8b64e28f8207b51d1acae2459d0cf89774e7be0c10cb5a2a04808029ade3b7
EXECUTION_ROOT_SHA256 = 56d2f3a996f6dc71183fa7325af06d738e8ba994f9b62a2ba454f85c5fe8fe1d
FREEZE_COMMIT = b8c39ebc751c30f9d2e3164160fc5ca31904ba46
FREEZE_TIMESTAMP_UTC = 2026-08-15T18:50:48Z
AUTHORIZATION_CERTIFICATE_SHA256 = 17335f0a5893406763fb7660e4f23c06b9343cc0818a1bc63db3abad9e0e4e1e
```

The next scientific transition is externally generated:

```text
AUTHORIZED_FUTURE_NOT_YET_REALIZED
    -> AUTHORIZED_FUTURE_REALIZED
```

No Packet 7 engineering, selector peeking, post-freeze guard addition, or outcome-contingent repair is permitted.

## VFA lineage and stacked PR topology

The active VFA history is intentionally stacked so rejected states remain reviewable:

```text
main
  |
  +-- PR #3  independent future-adaptation specification / VFA-0.1
        |
        +-- PR #5  dormant corrective reserve
              |    preserved failed/superseded construction
              |
              +-- PR #6  quotient revision topology
                    |
                    +-- PR #9  consequence-grounded future distinctions
                          |
                          +-- PR #11  Packet 7 freeze + authorization
                                |
                                +-- PR #12  blind adjudication + FSO theory
```

Interpretation:

- **PR #3** establishes the independent benchmark contract; its first concrete A/B construction was later rejected at predicate D for treatment-mechanism leakage into ordinary adaptation.
- **PR #5** preserves the dormant-reserve route, including semantic and capability-boundary failures. It is scientific provenance, not the current treatment definition.
- **PR #6** changes the treatment identity to identical validated facts with different revision-equivalence topology.
- **PR #9** repairs future semantic grounding by deriving distinctions from observable future migration consequences.
- **PR #11** freezes and authorizes Packet 7; this is the execution-authority lineage.
- **PR #12** constrains later interpretation and develops FSO theory without changing Packet 7.

Do not squash this stack merely to reduce PR count. The intermediate failures are part of the evidence chain.

## SSI jurisdiction falsification and semantic constitution

This is a separate scientific lineage from Packet 7 and CUHK-X.

### S0 Lineage 1 — preserved executed failure

PR #18 (`agent/ssi-jurisdiction-falsification-s0`) froze and executed `SSI-JURISDICTION-FALSIFICATION/S0`.

Terminal result:

```text
constitution = 8/11
fresh        = 38/48
S0_VALID     = false
terminal     = OPERATIONALIZATION_INADEQUATE
Stage 1      = NONE_STOP
```

The failure is specifically an `R/L` identification confound: the frozen leverage rule was conditional on reachability, so `R↓` forced the assay to report both `R=0` and `L=0` even when leverage itself was intact.

This is an **assay operationalization failure**, not support or falsification of the SSI kernel. PR #18 remains failed and must not be repaired in place.

### S0 Lineage 2 — semantic layer before measurement

The successor work moved upstream and asks whether the intended `D, R, L_cap, I_cap` target can be semantically constituted before an observation operator is allowed to exist.

The full handoff is:

- [`research/semantic_constitution/README.md`](research/semantic_constitution/README.md)

Current state:

```text
V1 = FAILED_STATIC_CLOSURE
V2 = CLOSED -> SEMANTICALLY_REJECTED
V3 = FAILED_STATIC_CLOSURE
V4 = CLOSED -> SEMANTICALLY_REJECTED
V5 = CLOSED -> SEMANTICALLY_REJECTED
V6 = FAILED_STATIC_CLOSURE
V7 = CLOSED -> SEMANTICALLY_REJECTED
V8 = NOT_YET_CONSTITUTED
O = UNDEFINED
ASSAY = UNDEFINED
```

Current frontier:

> **What independently makes a relation among licensed inputs part of the identity of the composed semantic object?**

The semantic lineage enforces the permanent distinction:

```text
formal closure
    != semantic adequacy
    != observational identifiability
    != executed assay validity
```

No successor should build a second assay or observation operator until V8 identity constitution has itself passed static closure and hostile semantic attack.

## Other repository tracks

These tracks are scientifically separate unless a later artifact explicitly establishes a bridge:

- **PR #2 — V0.x archival preservation.** Preserves recovered frozen artifacts separately from the VFA stack; one manifest-listed runner remains explicitly unreconstructed.
- **PR #7 — A1 corrective-statehood preregistration.** Separate state-sufficiency experiment; it does not inherit VFA execution authority.
- **PR #4 — energy suite.** Merged isolated energy/computation lineage. Its evidence cannot retroactively redefine SSI core theory or VFA.
- **PR #8 / #10 — historical CUHK-X branches.** Historical/closed provenance, not current VFA or SSI-jurisdiction authority.
- **PR #14–#20 — current CUHK-X competitive/diagnostic lineages.** Separate competition work. Competitive results do not acquire SSI scientific authority automatically.

Because several tracks branch independently from `main`, a single branch is not necessarily the union of every repository experiment.

## What is intentionally not cleaned up

The following may look redundant but are **provenance-bearing** and should not be renamed, moved, coalesced, or deleted casually:

- rejected VFA constructions;
- old A-I re-audit/addendum files;
- hostile attack scripts and their result JSON;
- failed H/post-gate semantic candidates;
- Packet 1-6 candidates and rejection evidence;
- failed and repaired predicate-I attack fixtures;
- freeze anchors and content-addressed manifests;
- exact files named in Packet 7;
- PR #18 Stage-0 failure artifacts;
- semantic-contract versions and hostile/static failure witnesses once they are materialized into the semantic Lineage 2 ledger.

In particular, the crowded `empirical/benchmark_v0_2_quotient/construction/` directory is an append-only scientific lineage more than a conventional software package.

## Reader path

For a fast but correct pass through the repository:

1. `README.md` — program thesis and current empirical/semantic boundaries.
2. `REPOSITORY_STATUS.md` — authority map and branch/track routing.
3. `ARCHITECTURE.md` — core state/authority architecture.
4. `research/semantic_constitution/README.md` — current jurisdiction-falsification semantic frontier and exact takeover instructions.
5. `retrospective/LOCALIZATION_CALCULUS.md` — V0.x localization grammar.
6. `benchmarks/V0X_LINEAGE.md` — closed synthetic benchmark lineage.
7. `empirical/README.md` — empirical lineage index.
8. `empirical/benchmark_v0_2_quotient/AUTHORIZATION_STATUS.json` — current VFA authority state.
9. `research/post_authorization/VFA_0_2_BLIND_OUTCOME_ADJUDICATION.json` — blind post-shot interpretation tree.
10. `theory/FUTURE_SAFE_OPTION_STRUCTURE.md` — current theory extension outside the authorized shot.

## Takeover rule

A new researcher should first determine **which lineage they are entering** before changing anything.

For the current semantic frontier:

```text
read PR #18 failure
    -> read research/semantic_constitution/README.md
    -> preserve V1-V7 as failed/rejected provenance
    -> constitute only the minimal V8 identity candidate
    -> run static closure first
    -> hostile semantic attack only if CLOSED
    -> do not define O or an assay yet
```

For the prospective VFA experiment, do not modify Packet 7; the next information must come from the frozen external future-obligation process.

## Cleanup rule

Repository cleanliness is subordinate to scientific identity:

> **Clean navigation aggressively; clean evidence destructively only when no scientific identity, provenance, or future reproducibility depends on it.**
