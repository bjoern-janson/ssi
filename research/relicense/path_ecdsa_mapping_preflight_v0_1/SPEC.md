# SSI Path Witness Mapping Preflight V0.1

```text
OBJECT = SSI_PATH_WITNESS_MAPPING_PREFLIGHT_V0.1
STATUS = PRE_EXECUTION_SPEC
PARENT_M_F = SSI_EXTERNAL_TO_LOCAL_INPUT_MAPPING_V0.1
```

## Sole question

Can the exact, previously frozen external transition records from the ECDSA-style path witness be admitted through the already frozen mapper `M_F` without modifying, enriching, or reinterpreting them?

For each exact raw transition record `e_i` appearing in the frozen path files:

\[
M_F(e_i) \in \{\texttt{MAPPED},\texttt{NOT_EVALUABLE},\texttt{CONTRACT_VIOLATION}\}.
\]

The preflight stops before SSI execution unless every transition record is `MAPPED`.

## Frozen witness identity

The external path files are copied byte-for-byte from the prior path experiment and must retain these SHA-256 values:

```text
PATH_A_EXTERNAL.json = d19411ffefb4ce9b8b81e6fd1a61ef0e4d4fbd7c700b4ab77804592172b574a5
PATH_B_EXTERNAL.json = 80a79ae43880ccb0db7f36e8ee5d3f8f3f4c4f91ff117fc6e9f1734aedc0310a
```

The independently constituted path-consequence records are frozen for provenance only and MUST NOT be read by the mapper preflight:

```text
PATH_A_ORACLE.json = 7fffc12915ae968434f72f97691b5d87ef2d04ca258dcc14fb92d0baa3a1b8c3
PATH_B_ORACLE.json = 78e144c5d9d2b129797ebc37b68f28664e4d361a21f140834db9b2e191f5096d
```

## No-fit prohibition

The witness may not be changed to fit `M_F`.

Forbidden before the preflight result:

```text
- renaming transcript fields into SSI/mapping vocabulary
- synthesizing entities/claims/licenses/action from transcript content
- adding path fields to SSI
- omitting transcript fields to obtain admission
- letting M_F inspect Y_path, prior certificate outputs, or desired diagnosis
- running the SSI checker after any NOT_EVALUABLE or CONTRACT_VIOLATION result
```

## Decision rule

```text
ALL_RAW_TRANSITIONS_MAPPED
    -> MAPPING_PREFLIGHT_PASSED
       -> SSI path execution may be separately frozen later

ANY_RAW_TRANSITION_NOT_EVALUABLE
    -> MAPPING_BOUNDARY
       -> STOP before SSI checker

ANY_RAW_TRANSITION_CONTRACT_VIOLATION
    -> MAPPING_CONTRACT_VIOLATION
       -> STOP before SSI checker
```

A `MAPPING_BOUNDARY` result does not establish certificate projection loss, composition insufficiency, path-level SSI inadequacy, a new coordinate, or a repair.

## Authority ceiling

```text
PATH_LEVEL_INADEQUACY = NOT_ESTABLISHED
CERTIFICATE_PROJECTION_LOSS = NOT_TESTED
RELATIONAL_COMPOSITION_FAILURE = NOT_TESTED
COMPOSITION_INSUFFICIENCY = NOT_ESTABLISHED
COMPOSITION_THEOREM = NOT_EARNED
NEW_COORDINATE = NOT_EARNED
REPAIR = NOT_EARNED
SSI_CALC_KERNEL_DELTA = 0
```
