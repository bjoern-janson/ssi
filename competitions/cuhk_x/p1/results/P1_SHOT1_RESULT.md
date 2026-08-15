# CUHK-X P1 — Shot 1 result 🧊🎱

## Frozen adjudication

```text
P1_A = NOT_SUPPORTED_PRESERVED_COMPOSITION
P1_B.sequence    = NOT_IDENTIFIED_UNCONSTITUTED_BRANCH
P1_B.combination = NOT_IDENTIFIED_UNCONSTITUTED_BRANCH
P1_B.emotion     = NOT_IDENTIFIED_UNCONSTITUTED_BRANCH
P1_C = NOT_IDENTIFIED_UNCONSTITUTED_TRANSFER_COMPARATOR
LEADERBOARD_AUTHORITY = NONE
SSI_PACKET7_AUTHORITY = NONE
```

P1-A was the only scientifically scored primary branch in the authorized shot.

## P1-A gate

Frozen requirements:

```text
delta exact-set accuracy >= +0.03
abs(delta candidate balanced accuracy) <= 0.01
nonnegative exact-set gain in >= 4/5 folds
```

Observed:

```text
early exact-set       = 0.3695920889987639
preserved exact-set   = 0.38442521631644005
delta exact-set       = +0.014833127317676165

early candidate BalAcc     = 0.7577211493846145
preserved candidate BalAcc = 0.7675894984769360
delta candidate BalAcc     = +0.009868349092321482

nonnegative exact-set folds = 4/5
```

Therefore P1 fails the preregistered materiality requirement on exact-set gain:

```text
+0.0148331 < +0.03
```

while satisfying the frozen candidate-BalAcc ceiling and the 4/5 fold-stability condition.

The required adjudication is therefore:

```text
NOT_SUPPORTED_PRESERVED_COMPOSITION
```

## Descriptive decomposition — no authority upgrade

The preserved arm descriptively changed the HAU-multi population as follows:

```text
candidate accuracy        +0.0092707046
candidate balanced acc    +0.0098683491
candidate macro-F1        +0.0094979793
required-option recall    +0.0185799602
false-positive option rate -0.0011567380
full-set recovery         +0.0284301607
exact-set accuracy        +0.0148331273
```

These descriptive changes do not rescue P1-A because the preregistered exact-set materiality gate was not met.

Fold exact-set deltas were:

```text
fold 0  +0.00735294
fold 1  +0.03389831
fold 2  +0.02205882
fold 3  -0.00581395
fold 4  +0.01595745
```

The subject-level effects are retained in the frozen metrics artifact; they may not be subset-selected to redefine the primary result.

## P1-B

The identical post-encoder intervention was not constituted for HAU sequence, combination, or emotion in the authorized implementation. Per the frozen fail-closed rule, all three remain:

```text
NOT_IDENTIFIED_UNCONSTITUTED_BRANCH
```

No category-specific architecture is permitted as a post-result repair.

## P1-C

The retained authorized artifacts provide the outer OOF evidence used by P1-A, but not the fully nested inner-subject OOF evidence required by the frozen familiar-subject comparator for P1-C.

Therefore:

```text
P1_C = NOT_IDENTIFIED_UNCONSTITUTED_TRANSFER_COMPARATOR
```

Ordinary outer OOF predictions are not substituted for the preregistered nested comparator.

## Preserved pre-score failure

Execution authorization 1 stopped before truth/label attachment because the evaluator zipped a canonically sorted candidate object against physical archive row order. No P1 metric or adjudication was produced. That failure is preserved separately.

The evaluator-only repair changed row alignment to the exact key `(qa_id, option, action)`, was separately reauthorized, and did not change the specification, treatment, constituted predictions, reasoner, or thresholds.

## Stopping rule

The preregistered branch rule now applies:

> P1-A is not supported; therefore the larger preserved-evidence architecture is **not justified as a P1 rescue** in this frozen composition scope.

This result does not establish that preservation is useless, that the descriptive gain is zero, that P1-C is negative, or that SSI/MAGIKARP is contradicted. It establishes only that this minimal constituted intervention failed the frozen P1-A support criterion.
