# Authorization Re-audit Addendum — Predicate G

This addendum advances the fresh quotient-treatment authorization audit from the previously documented A–F state to the current machine-readable state.

Authoritative status is `AUTHORIZATION_STATUS.json`.

```text
A = PASS
B = PASS
C = PASS
D = PASS
E = PASS
F = PASS
G = PASS
H = NOT_EVALUATED
I = NOT_EVALUATED
```

Predicate G is re-earned from the treatment-free common-cause mechanism in:

- `construction/G_COMMON_CAUSE_MANIFEST.json`
- `construction/G_COMMON_CAUSE_KERNEL.py`
- `construction/G_COMMON_CAUSE_ATTACK.py`
- `construction/g_common_cause_audit.json`
- `construction/G_REALIZED_COMMON_CAUSE_CERTIFICATE_TEMPLATE.json`
- `evidence/G_COMMON_CAUSE_PASS.md`

The authorization-side attack uses synthetic blinded candidate streams only. A concrete real future candidate pool is intentionally not known before freeze. The selector has no arm/treatment input, packaging is one global immutable common bundle, and the realized certificate remains uninstantiated until after external selection and before disclosure.

Current authority boundary:

```text
FUTURE_OBLIGATION_ACCESSED = FALSE
G_ACTIVATION               = PROHIBITED
DELTA_PI                    = NOT_EVALUATED
KERNEL_FUTURE_INCLUSION     = NOT_EVALUATED
FREEZE_PACKET               = NOT_FROZEN
AUTHORIZATION_CERTIFICATE  = NOT_ISSUED
FUTURE_RUN                  = NOT_AUTHORIZED
```

The next admissible authorization predicate is H: confound-ledger completeness and residual-confound veto.
