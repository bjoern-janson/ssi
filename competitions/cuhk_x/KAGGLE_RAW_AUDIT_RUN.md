# Kaggle RAW_AUDIT — clean CUHK-X restart

This run is **audit only**. It must not import old CUHK-X experiment outputs and must not train or score a model.

## Kaggle setup

Attach the competition data to the notebook. GitHub should be connected so the notebook can clone the SSI repository.

Run this single cell:

```python
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

REPO = Path('/kaggle/working/ssi')
BRANCH = 'agent/cuhkx-restart-clean'
AUDIT = REPO / 'competitions/cuhk_x/audit_kaggle_mount.py'

if REPO.exists():
    shutil.rmtree(REPO)

subprocess.run([
    'git', 'clone', '--depth', '1', '--branch', BRANCH,
    'https://github.com/bjoern-janson/ssi.git', str(REPO)
], check=True)

# Record the exact repo commit whose audit code is executing.
head = subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip()
print('AUDIT_GIT_COMMIT =', head)

# Run only the Kaggle raw audit. The script auto-discovers the mounted
# cuhk-x-competition-large-model-track directory under /kaggle/input.
subprocess.run([
    sys.executable, str(AUDIT),
    '--input-root', '/kaggle/input',
    '--out', '/kaggle/working/cuhkx_raw_audit'
], check=True)

bundle = Path('/kaggle/working/cuhkx_raw_audit_bundle.zip')
if not bundle.exists():
    raise FileNotFoundError(bundle)

print('RAW_AUDIT_BUNDLE =', bundle)
print('STOP = RAW_AUDIT_ONLY')
```

## Required terminal output

The run must terminate with:

```text
STATUS = RAW_AUDIT_COMPLETE
MODELING_AUTHORITY = NONE
STOP = RAW_AUDIT_ONLY
```

Bring back:

```text
/kaggle/working/cuhkx_raw_audit_bundle.zip
```

The bundle contains:

```text
RAW_AUDIT.json
RAW_MANIFEST.csv
```

The console also prints:

```text
AUDIT_GIT_COMMIT
REPORT_SHA256
MANIFEST_SHA256
BUNDLE_SHA256
```

Do not run any baseline, feature extraction, prompting, model fitting, thresholding, or submission construction in the same notebook execution before the audit has been reviewed.

## Why the Kaggle-specific auditor exists

`audit_kaggle_mount.py` extends the original assumption-light auditor in one operational respect only: if Kaggle mounts CSV/TSV metadata inside ZIP archives, it reads those small tabular members directly from the archive without extracting media payloads. This is required to recover the current train/test/schema/episode contract from the actual mounted competition bytes.
