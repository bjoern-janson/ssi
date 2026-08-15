#!/usr/bin/env python3
"""Pure verifier/resolver for the exact future Biome CLI npm artifact.

Network fetching is intentionally outside this module. The caller supplies the
exact-version official npm tarball bytes plus registry-provided SRI strings.
This module verifies bytes, package-internal metadata, platform constraints,
and extracts the one frozen linux-x64-glibc executable member.

No arm, Gamma, treatment, reachability, or outcome input exists.
"""
from __future__ import annotations

from dataclasses import dataclass
import base64
import hashlib
import io
import json
import tarfile
from typing import Any


@dataclass(frozen=True, slots=True)
class ResolvedArtifact:
    status: str
    selected_version: str
    wrapper_tar_sha256: str | None
    platform_tar_sha256: str | None
    executable_sha256: str | None
    executable: bytes | None
    reason: str | None


IDENTIFIED = "IDENTIFIED"
NOT_IDENTIFIED = "NOT_IDENTIFIED"
WRAPPER_NAME = "@biomejs/biome"
PLATFORM_NAME = "@biomejs/cli-linux-x64"
EXECUTABLE_MEMBER = "package/biome"
PACKAGE_JSON_MEMBER = "package/package.json"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _verify_sha512_sri(data: bytes, integrity: str) -> bool:
    if type(data) is not bytes or type(integrity) is not str:
        return False
    tokens = integrity.split()
    sha512_tokens = [x for x in tokens if x.startswith("sha512-")]
    if len(sha512_tokens) != 1:
        return False
    try:
        expected = base64.b64decode(sha512_tokens[0][len("sha512-"):], validate=True)
    except Exception:
        return False
    return hashlib.sha512(data).digest() == expected


def _regular_member(tar_bytes: bytes, path: str) -> bytes:
    if type(tar_bytes) is not bytes or type(path) is not str:
        raise TypeError("bytes and path required")
    try:
        with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:*") as tf:
            matches = [m for m in tf.getmembers() if m.name == path]
            if len(matches) != 1:
                raise ValueError("required tar member must occur exactly once")
            member = matches[0]
            if not member.isfile() or member.issym() or member.islnk() or member.isdev():
                raise ValueError("required tar member must be a regular file")
            f = tf.extractfile(member)
            if f is None:
                raise ValueError("required tar member unreadable")
            return f.read()
    except (tarfile.TarError, OSError) as e:
        raise ValueError("invalid tarball") from e


def _manifest(tar_bytes: bytes) -> dict[str, Any]:
    raw = _regular_member(tar_bytes, PACKAGE_JSON_MEMBER)
    try:
        obj = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ValueError("invalid package.json") from e
    if type(obj) is not dict:
        raise ValueError("package.json must be object")
    return obj


def _exact_list(value: Any, expected: list[str]) -> bool:
    return type(value) is list and value == expected


def resolve_exact_linux_x64(
    selected_version: str,
    wrapper_tarball: bytes,
    wrapper_integrity: str,
    platform_tarball: bytes,
    platform_integrity: str,
) -> ResolvedArtifact:
    """Fail-closed exact-version official-package artifact resolution."""
    if type(selected_version) is not str or not selected_version:
        raise TypeError("selected_version required")
    if not _verify_sha512_sri(wrapper_tarball, wrapper_integrity):
        return ResolvedArtifact(NOT_IDENTIFIED, selected_version, None, None, None, None, "WRAPPER_INTEGRITY_FAILURE")
    if not _verify_sha512_sri(platform_tarball, platform_integrity):
        return ResolvedArtifact(NOT_IDENTIFIED, selected_version, _sha256(wrapper_tarball), None, None, None, "PLATFORM_INTEGRITY_FAILURE")

    try:
        wrapper = _manifest(wrapper_tarball)
        platform = _manifest(platform_tarball)
        if wrapper.get("name") != WRAPPER_NAME or wrapper.get("version") != selected_version:
            raise ValueError("wrapper identity mismatch")
        optional = wrapper.get("optionalDependencies")
        if type(optional) is not dict or optional.get(PLATFORM_NAME) != selected_version:
            raise ValueError("wrapper does not pin exact linux-x64 platform version")
        if platform.get("name") != PLATFORM_NAME or platform.get("version") != selected_version:
            raise ValueError("platform identity mismatch")
        # Current pre-freeze package semantics explicitly declare these constraints.
        # If future packages omit/change them, do not infer compatibility.
        if not _exact_list(platform.get("os"), ["linux"]):
            raise ValueError("platform os constraint mismatch")
        if not _exact_list(platform.get("cpu"), ["x64"]):
            raise ValueError("platform cpu constraint mismatch")
        if not _exact_list(platform.get("libc"), ["glibc"]):
            raise ValueError("platform libc constraint mismatch")
        executable = _regular_member(platform_tarball, EXECUTABLE_MEMBER)
        if not executable:
            raise ValueError("empty executable")
    except (TypeError, ValueError):
        return ResolvedArtifact(
            NOT_IDENTIFIED,
            selected_version,
            _sha256(wrapper_tarball),
            _sha256(platform_tarball),
            None,
            None,
            "PACKAGE_SHAPE_OR_IDENTITY_FAILURE",
        )

    return ResolvedArtifact(
        IDENTIFIED,
        selected_version,
        _sha256(wrapper_tarball),
        _sha256(platform_tarball),
        _sha256(executable),
        executable,
        None,
    )
