# Frozen V0.x artifact preservation

This directory preserves the recovered payload for the closed synthetic V0.x ladder.

## Preservation invariant

> **Preserve exactly what was executed.**

No archived executable or result is refactored, cleaned up, bug-fixed, renamed, threshold-adjusted, or reinterpreted during preservation.

## Recovery status

- `results/FROZEN_RESULTS.md` is the authoritative manifest on the foundation history.
- 25 manifest-listed artifacts were recovered and SHA-256 verified byte-for-byte against that manifest before packaging.
- One manifest-listed artifact was not recovered and is deliberately **not reconstructed**:
  - `v0_8_evidence_to_authority_scientific_runner.py`
  - expected SHA-256: `73f0c97db3b59503ae066be022ecf3b4a805c3bbbe2f99f76f2c587640c2f98e`
- Archive status is therefore **25/26 recovered**, not complete recovery.

## Transport representation

The 25 verified files are packaged losslessly as `v0x_frozen_artifacts.tar.xz`. Because the repository connector accepts text Git blobs rather than a local binary-file handoff, the package is stored as ordered Base64 transport fragments under `transport/`.

This encoding is transport only. `RESTORE.sh` reconstructs the archive, verifies the package digest, extracts the files, and re-verifies every recovered artifact against `SHA256SUMS.recovered`.

Archive SHA-256:

`9fc212811ff8b98e385e490a46145dbe995a8f7931e8c64854342f4af8dc2ca9`

## Scientific status

```text
V0.X = CLOSED
```

This archival import does not reopen, extend, reinterpret, or supersede the synthetic ladder.
