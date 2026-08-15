# VFA-0.2 Hardened N-Ladder Attack 1

## Scope

```text
LINEAGE = VFA-0.2-QUOTIENT-REVISION-TOPOLOGY
THREAT_MODEL = PREACTIVATION_CALLER_V1
FUTURE_OBLIGATION_ACCESSED = FALSE
G_ACTIVATION = PROHIBITED
```

This attack follows the semantic redesign in which A and B share one validated substrate and differ only in revision-path equivalence structure.

## Result

```text
D_PRE_ACTIVATION_HARDENED = PASS
scope = PREACTIVATION_CALLER_V1

N0 endpoint equality        = PASS
N1 full trace equality      = PASS
N2 metamorphic invariance   = PASS
N3 transitive non-use       = PASS
N4 capability surface       = PASS
```

### N2

Across 249 ordinary pre-freeze tasks, 34 caller-side Gamma geometries, four semantically equivalent query presentations, and three equal caller-side allocation-pressure levels:

```text
comparisons = 101592
mismatches  = 0
```

No wall-clock invariance claim is made.

### N3

```text
transitive static call graph = PASS
module-global poisoning comparisons = 2988
module-global mismatches = 0
gate comparisons = 170
gate mismatches = 0
```

Neither protected call graph reaches Gamma/revision-topology symbols.

### N4

The previous dormant-reserve construction failed because open dictionaries accepted reserve-bearing fields even though the implementation ignored them.

The redesigned interface uses a closed ordinary call and a frozen slotted evidence schema. The attack attempted extra positional Gamma arguments, Gamma-as-query payloads, open-dict gate payloads, extra constructor fields, and post-construction capability attachment.

```text
capability-smuggling attempts = 530
rejected                     = 530
accepted                     = 0
```

Therefore, within `PREACTIVATION_CALLER_V1`, the preactivation interface rejects Gamma capability rather than merely declining to use it.

## Threat-model boundary

This is an architectural caller-interface certificate, not an OS or language-runtime sandbox proof. The frozen threat model permits hostile caller inputs, arbitrary dormant Gamma objects, serialization/order/allocation perturbations, extra-field/argument smuggling, and unrelated Gamma-named global injection.

It does not grant the attacker arbitrary mutation of trusted function code, reassignment of the frozen forward constant, `ctypes`/debugger memory mutation, or filesystem mutation of trusted artifacts during the run.

## Scientific boundary

This remains construction-audit evidence.

```text
kernel(q) subset kernel(T_future) = NOT_EVALUATED
Delta_Pi                         = NOT_EVALUATED
FREEZE_PACKET                    = NOT_FROZEN
AUTHORIZATION_CERTIFICATE       = NOT_ISSUED
FUTURE_RUN                      = NOT_AUTHORIZED
```

The result does not establish future corrective option value. It establishes that the same-truth/different-path treatment currently survives the frozen preactivation attack surface.
