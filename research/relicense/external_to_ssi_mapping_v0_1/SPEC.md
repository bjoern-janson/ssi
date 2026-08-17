# SSI External-to-Local Input Mapping V0.1

```text
OBJECT = SSI_EXTERNAL_TO_LOCAL_INPUT_MAPPING_V0.1
STAGE  = MAPPING_CONSTITUTION
STATUS = PRE_EXECUTION_SPEC
```

## 0. Sole scientific question

> When may an independently constituted external transition record be mapped into the frozen SSI local-input interface without silently losing, inventing, or laundering distinctions inside that interface's constituted jurisdiction?

This object does not evaluate SSI, path composition, certificate adequacy, or any path consequence.

The only target is:

\[
\boxed{M_F:E(T)\rightarrow I_F(T)}
\]

where:

- `E(T)` is an independently supplied external transition record under this specification;
- `I_F(T)` is the derivation-visible SSI local-input payload consisting only of `objects`, `facts`, `authority_edges`, and `request`.

The frozen SSI benchmark envelope (`spec_version`, case id/family/title, and `expected`) is not produced by `M_F`. In particular, benchmark `expected` is oracle/evaluation material and is outside mapper jurisdiction.

## 1. Parent boundary

The target SSI input schema is frozen by blob:

```text
SSI_SCHEMA_BLOB_SHA = 5c37ed034708f0968a44782866ef2741dbd51c3b
```

The frozen path-aware SSI derivation layer is identified only for boundary provenance:

```text
CHECKER_RESOLVED_BLOB_SHA = f1258d401bcc5d107938bbd37d031fe993119278
```

`M_F` does not import, call, simulate, or inspect that checker.

## 2. External transition record

`E(T)` has this constituted top-level vocabulary:

```text
external_transition_id
entities
claims
licenses
action
annotations        [optional]
path_relations     [optional]
```

The external names are intentionally not the SSI schema names.

### 2.1 entities

```text
external_id
class
properties         [optional]
```

### 2.2 claims

```text
claim_id
predicate
arguments
scope_jurisdiction [optional]
source_provenance  [optional]
standing           [optional]
```

### 2.3 licenses

```text
edge_id
grantor
grantee
scope_jurisdiction
source_provenance
supporting_claims
allowed_operations
conditions
must_preserve
```

### 2.4 action

```text
verb
arguments
scope_jurisdiction
recipient           [optional]
authority_requested [optional]
```

### 2.5 annotations

Human-facing record annotations. They are outside the frozen SSI local decision-input jurisdiction unless separately constituted later. Exclusion from `I_F` is not a claim of irrelevance to any external consequence.

### 2.6 path_relations

Cross-transition relations not already constituted as a local `claim` in the current external record. A non-empty `path_relations` field is `NOT_EVALUABLE` under V0.1. It may not be silently discarded or reclassified as irrelevant.

## 3. Disposition vocabulary

Every constituted external field class has exactly one mapping disposition:

\[
\boxed{
\operatorname{Disposition}_{M_F}(z)\in
\{
\texttt{PRESERVE},
\texttt{NORMALIZE},
\texttt{EXCLUDE\_WITH\_BASIS},
\texttt{NOT\_EVALUABLE}
\}
}
\]

### PRESERVE

The source value is copied without semantic rewriting into its frozen SSI target field.

### NORMALIZE

Only a transformation explicitly enumerated in `MAPPING_PROVENANCE.json` may occur. Normalization is not permission to merge arbitrary values.

### EXCLUDE_WITH_BASIS

The field is omitted from `I_F` only under a frozen jurisdictional basis. The basis establishes exclusion from the local SSI input question, not global irrelevance.

\[
\boxed{\text{excluded from }I_F\neq\text{irrelevant to }Y_{\rm path}}
\]

### NOT_EVALUABLE

The current mapping contract has no constituted route for the field or relation. Mapping stops. `NOT_EVALUABLE` may not be converted into omission.

## 4. Mapping

The frozen structural mapping is:

```text
entities  -> objects
claims    -> facts
licenses  -> authority_edges
action    -> request
```

Within those structures, source values are preserved except for the explicitly enumerated standing-vocabulary normalization.

`external_transition_id` and `annotations` are excluded only under their frozen jurisdictional bases.

A non-empty `path_relations` field returns `NOT_EVALUABLE`.

Any unknown field at any constituted record layer returns `NOT_EVALUABLE`; there is no permissive `additionalProperties` path.

## 5. Backward-flow firewall

`M_F` may not consume any field whose purpose is to expose downstream evaluation, including:

```text
path_consequence
Y_path
certificate_output
Cert_F
psi_output
Psi_F
collision_expectation
desired_diagnosis
```

Presence of any reserved backward-flow key anywhere in `E(T)` is a `CONTRACT_VIOLATION`.

Therefore:

\[
\boxed{
M_F\not\leftarrow
Y_{\rm path},
\operatorname{Cert}_F,
\Psi_F,
\text{collision expectation},
\text{desired diagnosis}
}
\]

The mapper may not use downstream information even to decide that two external transitions should map equally.

## 6. Equality rule

For two external transitions, local-input equality is always computed after two independent applications of the same frozen mapper:

\[
I_A=M_F(E_A),\qquad I_B=M_F(E_B).
\]

No mapper rule may take `(E_A,E_B)` jointly.

Thus:

\[
\boxed{I_A=I_B\text{ is a derived result, never an experimental premise}.}
\]

## 7. Mapping-only adversarial obligations

The frozen mapping-only suite must test at least:

1. an in-jurisdiction entity distinction survives;
2. an in-jurisdiction claim-argument distinction survives;
3. an in-jurisdiction authority-edge distinction survives;
4. an in-jurisdiction action distinction survives;
5. an explicitly enumerated equivalent standing encoding normalizes identically;
6. an annotation-only difference may collapse only with the frozen exclusion basis;
7. an unknown field becomes `NOT_EVALUABLE`, not omission;
8. a non-empty unconstituted cross-transition relation becomes `NOT_EVALUABLE`;
9. a reserved backward-flow field becomes `CONTRACT_VIOLATION`;
10. a missing required external structure becomes `NOT_EVALUABLE`.

No SSI checker may run during these tests.

## 8. Result vocabulary

Mapping-only execution may produce only:

```text
MAPPING_SUPPORTED_ON_FROZEN_ABSTRACT_SUITE
MAPPING_NOT_SUPPORTED_ON_FROZEN_ABSTRACT_SUITE
NOT_EVALUABLE_UNDER_FROZEN_MAPPING_CONTRACT
```

The maximum positive claim is:

```text
EXTERNAL_TO_SSI_MAPPING_CONSTITUTION
    = SUPPORTED_ON_FROZEN_ABSTRACT_MAPPING_SUITE
```

## 9. Authority ceiling

Even a fully positive mapping result does not establish:

```text
PATH_LEVEL_INADEQUACY
CERTIFICATE_PROJECTION_LOSS
RELATIONAL_COMPOSITION_FAILURE
INTERFACE_AUTHORITY_BOUNDARY
COMPOSITION_THEOREM
NEW_COORDINATE
REPAIR
SSI_CALC_KERNEL_CHANGE
```

The frozen ceiling remains:

```text
PATH_LEVEL_INADEQUACY = NOT_ESTABLISHED
CERTIFICATE_PROJECTION_LOSS = NOT_TESTED
RELATIONAL_COMPOSITION_FAILURE = NOT_TESTED
INTERFACE_AUTHORITY_BOUNDARY = UNKNOWN
COMPOSITION_THEOREM = NOT_EARNED
NEW_COORDINATE = NOT_EARNED
REPAIR = NOT_EARNED
SSI_CALC_KERNEL_DELTA = 0
```

## 10. Central falsification

The mapper fails its own contract if an in-jurisdiction external distinction is silently collapsed, an out-of-jurisdiction distinction is excluded without its frozen basis, an unrepresented relation is silently dropped, unknown information is silently ignored, or downstream evaluation information affects the mapping.

## 11. Non-rules

```text
EXCLUDED_FROM_LOCAL_INPUT != GLOBALLY_IRRELEVANT
UNMAPPABLE != IRRELEVANT
UNKNOWN_FIELD != SAFE_TO_DROP
NORMALIZATION != AUTHORITY_TO_MERGE
SAME_LOCAL_INPUT != SAME_EXTERNAL_TRANSITION
MAPPING_SUPPORT != SSI_ADEQUACY
MAPPING_SUPPORT != CERTIFICATE_ADEQUACY
MAPPING_SUPPORT != PATH_COMPOSITION_SUPPORT
MAPPING_SUPPORT != PATH_COLLISION
```
