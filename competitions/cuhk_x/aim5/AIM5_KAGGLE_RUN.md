# CUHK-X AIM5 — Kaggle execution contract

AIM5 is an internal aiming experiment. It does **not** create or upload S2.

The execution boundary is now explicitly two-stage:

```text
STAGE 1: MECHANICAL PRECHECK
        -> STOP
        -> POST-PRECHECK BYTE FREEZE / AUTHORIZATION
STAGE 2: EXACT AIM5 RUN
```

A passing precheck does **not** itself authorize the AIM5 run.

## Required attached inputs

Attach:

1. official competition `Training-20260813T154030Z-1-002.zip`;
2. private `cuhkx_aim5_private_inputs.zip` created by `prepare_CUHKX_AIM5_Kaggle_bundle.py`.

The private bundle must contain the exact frozen derived inputs plus:

```text
cuhkx_aim4_structured_set.py
cuhkx_aim5_conditional_setmap.py
cuhkx_aim5_precheck.py
```

The organizer Training ZIP remains outside the private bundle.

## Frozen hashes before precheck

```text
AIM4 helper SHA-256
ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5

AIM5 executable SHA-256
620e35da4256e3368359e202729e45489b916687ef890e3f9d887e91f11a0605
```

The mechanical precheck's SHA-256 and the private bundle SHA-256 are recorded at staging time and become part of the post-precheck authorization record if the precheck passes.

---

# Stage 1 — mechanical precheck only

Use a normal CPU Kaggle notebook with the official competition data and the private AIM5 dataset attached.

Run this cell and **stop when it completes**:

```python
from pathlib import Path
import hashlib, os, shutil, subprocess, sys, zipfile

INPUT = Path('/kaggle/input')
RUN = Path('/kaggle/working/aim5_precheck_run')
EXPECTED_AIM4 = 'ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5'
EXPECTED_AIM5 = '620e35da4256e3368359e202729e45489b916687ef890e3f9d887e91f11a0605'


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def unique_name(name):
    hits = sorted(INPUT.rglob(name))
    if len(hits) != 1:
        raise RuntimeError(f'Expected exactly one {name!r}; found {len(hits)}: {hits}')
    return hits[0]

if RUN.exists():
    shutil.rmtree(RUN)
RUN.mkdir(parents=True)

bundle = unique_name('cuhkx_aim5_private_inputs.zip')
BUNDLE_SHA = sha256_file(bundle)
with zipfile.ZipFile(bundle) as z:
    z.extractall(RUN)

training = unique_name('Training-20260813T154030Z-1-002.zip')
os.symlink(training, RUN/'Training-20260813T154030Z-1-002.zip')

aim4 = RUN/'cuhkx_aim4_structured_set.py'
aim5 = RUN/'cuhkx_aim5_conditional_setmap.py'
precheck = RUN/'cuhkx_aim5_precheck.py'

if sha256_file(aim4) != EXPECTED_AIM4:
    raise RuntimeError('AIM4 helper SHA mismatch')
if sha256_file(aim5) != EXPECTED_AIM5:
    raise RuntimeError('AIM5 executable SHA mismatch')
PRECHECK_SHA = sha256_file(precheck)

print('PRIVATE_BUNDLE_SHA256 =', BUNDLE_SHA)
print('AIM5_PRECHECK_SHA256 =', PRECHECK_SHA)

# This is the only executable action permitted in Stage 1.
subprocess.run([
    sys.executable, str(precheck), '--workdir', str(RUN)
], check=True)

report = RUN/'cuhkx_aim5_precheck_report.json'
if not report.exists():
    raise FileNotFoundError(report)
shutil.copy2(report, '/kaggle/working/cuhkx_aim5_precheck_report.json')
print('PRECHECK_REPORT = /kaggle/working/cuhkx_aim5_precheck_report.json')
print('STOP = RETURN_PRECHECK_REPORT_FOR_BYTE_FREEZE')
```

### What Stage 1 mechanically verifies

The precheck must establish:

```text
outer_subject_isolation                 = PASS
inner_base_model_isolation              = PASS
training_only_margin_normalization      = PASS_BY_COMPOSITION
training_only_meta_fitting              = PASS
no_query_leakage                        = PASS
aim4_comparator_frozen                  = PASS
s1_candidate_sign_reproduction          = PASS
s1_decision_operator_reproduction       = PASS
```

It also runs the actual AIM5 `build_inner_meta` control flow with a recorder so the intended three-fold base-training / one-fold inner-scoring topology is exercised mechanically, not merely asserted in prose.

For the S1 reproduction gate it fits the frozen S1 candidate models under each outer split, checks exact V7/V7F candidate-sign reproduction, and independently verifies the S1 `margin >= 0` plus forced-singleton decision operator.

A failed precheck is:

```text
NOT_IDENTIFIED
```

not evidence against AIM5.

---

# Mandatory stop — post-precheck byte freeze

After Stage 1, do **not** execute AIM5 yet.

Return/store:

```text
cuhkx_aim5_precheck_report.json
PRIVATE_BUNDLE_SHA256
AIM5_PRECHECK_SHA256
```

The post-precheck authorization record must freeze at minimum:

```text
AIM4 helper SHA-256
AIM5 executable SHA-256
AIM5 precheck SHA-256
private bundle SHA-256
all frozen input SHA-256 values from the precheck report
PRECHECK = PASS
RUN_AUTHORIZATION = AUTHORIZED
```

If any byte changes after this freeze, the authorization is invalid and Stage 1 must be repeated.

---

# Stage 2 — exact AIM5 run

Stage 2 is allowed only after the post-precheck authorization record is committed.

Use the **same byte-identical private bundle** and verify its SHA-256 against the authorization record before extraction. Then verify AIM4/AIM5/precheck hashes again. Finally execute exactly:

```python
subprocess.run([
    sys.executable,
    str(RUN/'cuhkx_aim5_conditional_setmap.py'),
    '--workdir',
    str(RUN),
], check=True)
```

No parameter, feature, fold, decoder, input, or support-gate change is permitted between Stage 1 and Stage 2.

The result must be copied out as:

```text
/kaggle/working/cuhkx_aim5_conditional_setmap_results.zip
```

## Expected AIM5 runtime behavior

For each outer subject fold, AIM5 regenerates four inner-held-out meta folds by fitting the frozen S1 candidate models on only three canonical folds at a time. It then fits the frozen action-aware candidate utility and cardinality models on those inner OOF margins, refits the S1 base candidate models on the four outer-training folds, and scores the untouched outer fold.

The outer candidate signs must exactly reproduce the frozen V7/V7F OOF signs. Failure there terminates as `NOT_IDENTIFIED_BASE_REPRODUCTION_FAILURE`.

## Terminal adjudications

```text
NOT_IDENTIFIED_BASE_REPRODUCTION_FAILURE
NOT_SUPPORTED_CONDITIONAL_SETMAP
SUPPORTED_CONDITIONAL_SETMAP_IN_FROZEN_MULTI_SCOPE
```

Only the final state yields:

```text
S2 = PACKAGING_CANDIDATE_AUTHORIZED
```

Even then, the external shot remains blocked until a separate S2 package freezes the full-training analogue of the candidate utility/cardinality models, proves all non-multi S1 outputs unchanged, passes smoke tests, and freezes package provenance.
