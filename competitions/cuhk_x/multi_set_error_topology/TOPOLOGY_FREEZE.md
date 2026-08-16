# CUHK-X Multi Set-Error Topology — frozen diagnostic 🧊

```text
DIAGNOSTIC_ID       = CUHKX-MULTI-SET-ERROR-TOPOLOGY-1
ROLE                = POST_P1_DIAGNOSIS_ONLY
MODEL_AUTHORITY     = NONE
TREATMENT_AUTHORITY = NONE
P2_AUTHORITY        = NONE
CARS_CAUSAL_LABEL   = NOT_IDENTIFIED
```

## 1. Frozen inputs

This diagnostic consumes only the already-frozen CUHK-X P1 shot-1 outputs.

```text
P1 result commit
43cda71f081f0cb179007f999cc08458421ad703

P1 raw result SHA-256
b3429ee3d9737a98cd4ded5865ffd1d519c812c03b77563c172c98cb2c64e248

P1 metrics SHA-256
f432d854c0973647071db771638191259623ad8a8a9ddff31fb25b3c29680488

scope = HAU / multi
QA rows = 809
candidate rows = 3236
candidate options per QA = 4
```

No model, representation, prediction, threshold, label, treatment, or P1 adjudication may be changed.

## 2. Question

The diagnostic asks only:

> After accounting for the observed candidate-level error structure, what exact-set error topology remains?

It does **not** assume that the candidate/exact gap identifies a joint-composition or commitment mechanism.

## 3. D0 — fully identified set-error topology

For each QA row and arm:

\[
FN=|S^*\setminus \hat S|,\qquad FP=|\hat S\setminus S^*|.
\]

Assign exactly one mutually exclusive class:

```text
E = FN == 0 and FP == 0
U = FN >  0 and FP == 0
O = FN == 0 and FP >  0
M = FN >  0 and FP >  0
```

Also report:

```text
mean FN
mean FP
mean Hamming set error = mean(FN + FP)
mean signed set-size error = mean(|S_pred| - |S_true|)
full-set recovery
exact-set accuracy
full-set minus exact = P(O)
```

Breakdowns are descriptive only and are frozen as:

```text
overall
canonical fold
subject
true answer-set size
```

## 4. D1 — P1 movement of topology

Report preserved-minus-early changes for every D0 quantity and the complete 4x4 transition matrix:

```text
E/U/O/M (early) -> E/U/O/M (preserved)
```

No transition receives a causal label.

## 5. D2 — primary candidate-error factorized null

The crude `p^4` calculation is not the diagnostic null.

For each arm define candidate correctness

\[
C_{q,o}=1[\hat y_{q,o}=y_{q,o}].
\]

The primary null preserves the empirical candidate-correctness multiset separately within every stratum

```text
(subject, option_position, truth_label)
```

and destroys only within-question coupling by independently permuting correctness values across QA rows inside each stratum.

Properties deliberately preserved by the primary null:

```text
subject-level difficulty
option-position difficulty
positive-vs-negative candidate difficulty
arm-specific marginal candidate correctness
exact number of correct/incorrect candidate decisions in every stratum
```

Property deliberately destroyed:

```text
cross-candidate dependence within the same QA row
```

### Deterministic factorized expectation

For each stratum `s`, let `p_s` be its observed correctness rate. For QA row `q`, with its four candidate strata `s(q,o)`, define

\[
P_{fact}(E_q)=\prod_{o\in\{A,B,C,D\}}p_{s(q,o)}.
\]

Then

\[
Q_{fact}=\frac{1}{809}\sum_q P_{fact}(E_q).
\]

This deterministic expectation is the primary `Q_fact`.

### Permutation reference distribution

Use exactly:

```text
N_PERM = 50000
RNG = numpy.random.Generator(PCG64)
SEED = 260816
```

For each replicate and arm:

1. independently permute candidate correctness within every frozen stratum;
2. reconstruct the four candidate correctness bits for every QA row;
3. compute exact-set accuracy as the fraction with all four bits correct.

Report the permutation mean, standard deviation, and central 95% interval `[q0.025, q0.975]`.

No permutation search, seed search, or null redefinition is allowed.

## 6. D3 — residual joint structure

For each arm:

\[
R_{joint}=Q_{exact,obs}-Q_{fact}.
\]

Report only one of these descriptive locations relative to the frozen permutation reference:

```text
ABOVE_FACTORIZED_95   if Q_exact_obs > q0.975
WITHIN_FACTORIZED_95  if q0.025 <= Q_exact_obs <= q0.975
BELOW_FACTORIZED_95   if Q_exact_obs < q0.025
```

For the P1 movement report:

\[
\Delta Q_{obs}=Q^P_{exact}-Q^E_{exact},
\]

\[
\Delta Q_{fact}=Q^P_{fact}-Q^E_{fact},
\]

and

\[
\Delta R_{joint}=\Delta Q_{obs}-\Delta Q_{fact}.
\]

`Delta R_joint` is descriptive. No materiality threshold is introduced post hoc.

## 7. Authority ceiling

This diagnostic may establish only observable error topology and deviation from the frozen factorized candidate-error null.

It may **not** by itself establish:

```text
joint-composition failure
authority-allocation failure
over-commitment
under-commitment
genuine ambiguity
measurement insufficiency
CARS/CCA as the generating mechanism
need for a joint decoder
need for more representation
SSI support or contradiction
Packet 7 support or contradiction
```

Those remain `NOT_IDENTIFIED` unless a later independently frozen experiment earns them.

## 8. Stop rule

After this diagnostic is executed and frozen:

```text
NO P2 BY DEFAULT
NO MODEL CHANGE
NO THRESHOLD TUNING
NO NULL REDEFINITION
NO FAVORABLE SUBSET SELECTION
```

A new intervention is scientifically earned only if a separate mechanistic hypothesis is motivated by the frozen diagnostic result and preregistered as a new object.
