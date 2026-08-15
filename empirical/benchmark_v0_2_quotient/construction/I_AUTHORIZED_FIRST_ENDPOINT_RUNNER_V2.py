#!/usr/bin/env python3
"""Authorized VFA-0.2 runner wrapper with temporal-hardening custody v2.

Stdlib-only bootstrap. It verifies and loads the previously audited import-isolated
runner by exact sibling path/blob, redirects that runner to the temporally hardened
custody kernel, and makes the base runner's self-identity check bind this wrapper
as the packet-authorized entrypoint.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

BASE_RUNNER_FILENAME = "I_AUTHORIZED_FIRST_ENDPOINT_RUNNER.py"
BASE_RUNNER_GIT_BLOB = "5edf546835b27157d71eefc614f14e52ff2ef618"
CUSTODY_V2_FILENAME = "I_CHAIN_OF_CUSTODY_KERNEL_V2.py"
CUSTODY_V2_GIT_BLOB = "184c31de33a8ba617f1ec51b66dbdfe5ad0d9413"


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _load_base_runner():
    path = Path(__file__).resolve().with_name(BASE_RUNNER_FILENAME)
    data = path.read_bytes()
    if _git_blob_sha1(data) != BASE_RUNNER_GIT_BLOB:
        raise RuntimeError("base authorized-runner blob mismatch")
    name = "vfa_i_authorized_runner_base"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load base authorized runner")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base_runner()
_base.EXPECTED_CUSTODY_BLOB = CUSTODY_V2_GIT_BLOB
_base.CUSTODY_RELATIVE_PATH = "empirical/benchmark_v0_2_quotient/construction/" + CUSTODY_V2_FILENAME
# The base runner's self-identity check must bind the actual authorized wrapper.
_base.__file__ = str(Path(__file__).resolve())

run_authorized_first_endpoint = _base.run_authorized_first_endpoint
validate_runtime_platform = _base.validate_runtime_platform


def main() -> None:
    if len(sys.argv) != 8:
        raise SystemExit("usage: I_AUTHORIZED_FIRST_ENDPOINT_RUNNER_V2.py REPO_ROOT PACKET ANCHOR AUTH_CERT REALIZED_RECORD GROUNDING_ENVELOPE REALIZED_G_CERT")
    result = run_authorized_first_endpoint(*sys.argv[1:])
    sys.stdout.buffer.write(_base._canonical(result) + b"\n")


if __name__ == "__main__":
    main()
