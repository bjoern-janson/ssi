# CUHK-X AIM5 — Kaggle execution contract

AIM5 is an internal aiming experiment. It does **not** create or upload S2.

## Required attached inputs

Attach:

1. official competition `Training-20260813T154030Z-1-002.zip`;
2. private `cuhkx_aim5_private_inputs.zip` created by `prepare_CUHKX_AIM5_Kaggle_bundle.py`.

The private bundle must contain the exact frozen derived inputs plus:

```text
cuhkx_aim4_structured_set.py
cuhkx_aim5_conditional_setmap.py
```

The organizer Training ZIP remains outside the private bundle.

## Frozen hashes

```text
AIM4 helper SHA-256
ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5

AIM5 executable SHA-256
620e35da4256e3368359e202729e45489b916687ef890e3f9d887e91f11a0605
```

## Execution cell

Use a normal CPU Kaggle notebook with the official competition data and the private AIM5 dataset attached.

```python
from pathlib import Path
import hashlib, os, shutil, subprocess, sys, zipfile

INPUT = Path('/kaggle/input')
RUN = Path('/kaggle/working/aim5_run')
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
with zipfile.ZipFile(bundle) as z:
    z.extractall(RUN)

training = unique_name('Training-20260813T154030Z-1-002.zip')
os.symlink(training, RUN/'Training-20260813T154030Z-1-002.zip')

aim4 = RUN/'cuhkx_aim4_structured_set.py'
aim5 = RUN/'cuhkx_aim5_conditional_setmap.py'
if sha256_file(aim4) != EXPECTED_AIM4:
    raise RuntimeError('AIM4 helper SHA mismatch')
if sha256_file(aim5) != EXPECTED_AIM5:
    raise RuntimeError('AIM5 executable SHA mismatch')

# A failed precheck is NOT_IDENTIFIED, never a negative result.
subprocess.run([
    sys.executable, str(aim5), '--workdir', str(RUN), '--precheck-only'
], check=True)

# Execute the frozen nested experiment once.
subprocess.run([
    sys.executable, str(aim5), '--workdir', str(RUN)
], check=True)

result = RUN/'cuhkx_aim5_conditional_setmap_results.zip'
if not result.exists():
    raise FileNotFoundError(result)
shutil.copy2(result, '/kaggle/working/cuhkx_aim5_conditional_setmap_results.zip')
print('RESULT = /kaggle/working/cuhkx_aim5_conditional_setmap_results.zip')
```

## Expected runtime behavior

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
