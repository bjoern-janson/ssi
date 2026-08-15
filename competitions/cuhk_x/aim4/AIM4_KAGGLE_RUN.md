# CUHK-X AIM4 — Kaggle execution contract

AIM4 is an **internal aiming experiment**. It does not create or submit S2.

## Required attached inputs

Attach:

1. the official competition `Training-20260813T154030Z-1-002.zip`;
2. a private dataset containing `cuhkx_aim4_private_inputs.zip` produced by `prepare_CUHKX_AIM4_Kaggle_bundle.py`.

The private bundle contains only frozen derived/user artifacts:

- `cuhkx_submission1.py`;
- `cuhkx_v7_ir_dinov2_cache/features.npz`;
- `cuhkx_b2_hau_pose_cache/features.npz`;
- `cuhkx_b4_imu_v2_cache/features.npz`;
- `cuhkx_v7_strong_ir_dinov2_results.zip`.

Do not put the organizer Training ZIP inside the private bundle.

## Frozen executable

Repository path:

```text
competitions/cuhk_x/aim4/cuhkx_aim4_structured_set.py
```

Frozen SHA-256:

```text
ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5
```

The runner must verify that exact hash before execution.

## Kaggle staging cell

Create a normal CPU Kaggle notebook with the competition data and the private AIM4 dataset attached, then run this cell after placing the frozen executable text at `/kaggle/working/cuhkx_aim4_structured_set.py` (or downloading that exact blob by a separately verified route):

```python
from pathlib import Path
import hashlib, os, shutil, subprocess, sys, zipfile

INPUT = Path('/kaggle/input')
RUN = Path('/kaggle/working/aim4_run')
SCRIPT = Path('/kaggle/working/cuhkx_aim4_structured_set.py')
EXPECTED_SCRIPT_SHA = 'ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5'


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

if sha256_file(SCRIPT) != EXPECTED_SCRIPT_SHA:
    raise RuntimeError('AIM4 executable SHA mismatch')

if RUN.exists():
    shutil.rmtree(RUN)
RUN.mkdir(parents=True)

bundle = unique_name('cuhkx_aim4_private_inputs.zip')
with zipfile.ZipFile(bundle) as z:
    z.extractall(RUN)

training = unique_name('Training-20260813T154030Z-1-002.zip')
os.symlink(training, RUN/'Training-20260813T154030Z-1-002.zip')

# Precheck first. A failed precheck is NOT_IDENTIFIED, not a negative result.
subprocess.run([
    sys.executable, str(SCRIPT), '--workdir', str(RUN), '--precheck-only'
], check=True)

# Then execute the exact frozen AIM4 once.
subprocess.run([
    sys.executable, str(SCRIPT), '--workdir', str(RUN)
], check=True)

result = RUN/'cuhkx_aim4_structured_set_results.zip'
if not result.exists():
    raise FileNotFoundError(result)
shutil.copy2(result, '/kaggle/working/cuhkx_aim4_structured_set_results.zip')
print('RESULT = /kaggle/working/cuhkx_aim4_structured_set_results.zip')
```

## Adjudication

Do not alter the decoder after viewing the result.

Possible terminal states are:

```text
NOT_IDENTIFIED_BASE_REPRODUCTION_FAILURE
NOT_SUPPORTED_STRUCTURED_CARDINALITY_DECODER
SUPPORTED_STRUCTURED_CARDINALITY_DECODER_IN_FROZEN_MULTI_SCOPE
```

Only the third state yields:

```text
S2 = PACKAGING_CANDIDATE_AUTHORIZED
```

Even then, no leaderboard shot is authorized until a separate S2 package freezes the exact supported decoder, proves all non-multi S1 routes unchanged, passes smoke tests, and freezes package bytes/provenance.
