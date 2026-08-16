# K1 semantic-ABI certificate emission

This module implements the frozen R3 repair at the certificate emission/binding layer only.

Invariant:

```text
semantic carrier -> certificate denotation
execution witness -> operational metadata only
trace             -> implementation history only
```

`semantic_certificate.py` is deliberately ABI-generic. It does not assume that future semantic ABIs can be addressed by endpoints. R3 uses `{source,target}` only in the regression fixture.

The regression preserves the frozen K1 compiler, SSI-IR evaluator, R3 source/audit semantics, and historical artifacts. It checks the 2025-query pre-merge contract, including supersession/challenge/unavailability, p/q order noninterference, and the two 80-case negative controls.

Run from this directory:

```bash
python regression_r3.py
```
