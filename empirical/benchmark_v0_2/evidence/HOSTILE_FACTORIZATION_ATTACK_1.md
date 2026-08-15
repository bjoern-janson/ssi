# VFA-0.2 Hostile Factorization Attack 1

## Adjudication

```text
ATTACK = VFA-0.2-HOSTILE-FACTORIZATION-ATTACK-1
BEHAVIORAL_NONINTERFERENCE = PASS
HARD_NONINTERFERENCE = FAIL
FAILURE_CODE = OPEN_CAPABILITY_SURFACE
FUTURE_OBLIGATION_ACCESSED = FALSE
FREEZE_PACKET = NOT_FROZEN
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
FUTURE_RUN = NOT_AUTHORIZED
```

This is a construction failure, not evidence against the future-adaptation hypothesis.

## Question

The first VFA-0.2 certificate established exact trace equality for the implemented A/B reserves. This attack asks a stronger question:

> While `G=0`, is dormant reserve merely unused, or is it architecturally impossible for the ordinary forward path or insufficiency gate to receive a dereference-capable reserve reference?

The governing invariant is:

\[
G=0
\Rightarrow
D\nrightarrow T_{\rm forward}
\quad\land\quad
D\nrightarrow G
\]

where the arrow is interpreted as a capability path as well as an observed behavioral effect.

## Attacks that survived

### Metamorphic reserve-null attack

The suite generated 32 deterministic contract-valid reserve geometries in addition to A and B. Every generated reserve preserves:

- the same six cases;
- the same four binding kinds;
- the same 24 edges;
- the same source multiset per binding kind;
- the same target multiset per binding kind;
- the same 587-byte canonical serialized length.

For each of the 249 inherited pre-freeze surrogate tasks, the suite varied:

- query ordering: canonical, reversed, rotated, duplicate-preserving semantic form;
- dormant reserve geometry: 34 reserve variants total;
- equal caller-side allocation/serialization pressure proxies: 0, 3, and 17 churn iterations.

Total forward comparisons:

```text
101592
```

Material trace mismatches:

```text
0
```

This supports behavioral reserve-null invariance under the tested deterministic pressure proxy. It does not claim wall-clock or physical-memory invariance.

### Module-global poisoning

The suite injected A and B into six plausible module-global names:

```text
RESERVE
RESERVE_HANDLE
D
D_T
ARM
DORMANT_STATE
```

Across all 249 tasks:

```text
comparisons = 2988
mismatches = 0
```

### Gate interface perturbation

Five frozen gate cases were tested under four evidence-map presentations and all 34 reserve geometries held live in the caller.

```text
comparisons = 680
mismatches = 0
```

### Transitive static audit

The call-graph closure reachable from `forward_trace` is:

```text
forward_trace -> {_jaccard, _edge_key}
```

and the closure from `evaluate_gate` contains only `evaluate_gate`.

No reserve symbol or reflection/file/environment access primitive was found in either reachable closure under the frozen static scanner.

## Failure: capability smuggling

The stronger architecture nevertheless fails.

Both protected entry points accept open-ended Python dictionaries:

```text
forward_trace(query, shared_forward)
evaluate_gate(evidence)
```

The attack inserted a dormant reserve object into an otherwise valid argument:

```text
shared_forward["reserve_handle"] = D
```

and separately:

```text
evidence["reserve_handle"] = D
```

A closed capability boundary should reject these reserve-bearing inputs. Instead:

```text
forward smuggling attempts = 498
forward accepted           = 498
forward behavior changes   = 0

gate smuggling attempts    = 10
gate accepted               = 10
gate behavior changes       = 0
```

Thus the current implementation demonstrates **behavioral non-use**, but not the stronger architectural claim that `F_forward` and `G` receive no object from which reserve could be dereferenced.

The distinction is:

\[
\boxed{
D\text{ is ignored}
\;\not\Rightarrow\;
D\text{ is inaccessible}
}
\]

## Localization

The failure locus is the **interface/capability surface**, not the forward algorithm and not the reserve geometry.

The previous certificate remains historically correct for its narrower test:

```text
D_PRE_ACTIVATION_INITIAL = PASS
```

but the stronger current construction status is:

```text
D_PRE_ACTIVATION_HARDENED = FAIL
```

with failure code:

```text
OPEN_CAPABILITY_SURFACE
```

## Consequence

Do not activate the reserve, inspect a future obligation, freeze the packet, issue authorization, or run a future-adaptation experiment.

A new hardening step must close the argument schemas so that ordinary forward execution and gate evaluation cannot receive reserve-bearing payloads at all. That revision must then be attacked again; a behavioral pass after silently ignoring reserve fields is insufficient.
