#!/usr/bin/env python3
"""Construction-side attack for the future CLI artifact resolver.

Uses synthetic npm-style tarballs only. No future Biome release is fetched.
"""
from __future__ import annotations

import ast
import base64
import hashlib
import io
import json
from pathlib import Path
import tarfile

import FUTURE_EXECUTION_ARTIFACT_KERNEL as ak

HERE = Path(__file__).resolve().parent
OUT = HERE / "future_execution_artifact_audit.json"
VERSION = "9.9.9"


def sri(data: bytes) -> str:
    return "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode()


def tar_bytes(package_json: dict, executable: bytes | None = None, *, executable_kind="file", duplicate_binary=False) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz", format=tarfile.PAX_FORMAT) as tf:
        manifest = json.dumps(package_json, sort_keys=True, separators=(",", ":")).encode()
        info = tarfile.TarInfo("package/package.json")
        info.size = len(manifest)
        info.mode = 0o644
        tf.addfile(info, io.BytesIO(manifest))
        if executable is not None:
            if executable_kind == "file":
                bi = tarfile.TarInfo("package/biome")
                bi.size = len(executable)
                bi.mode = 0o755
                tf.addfile(bi, io.BytesIO(executable))
                if duplicate_binary:
                    bi2 = tarfile.TarInfo("package/biome")
                    bi2.size = len(executable)
                    bi2.mode = 0o755
                    tf.addfile(bi2, io.BytesIO(executable))
            elif executable_kind == "symlink":
                bi = tarfile.TarInfo("package/biome")
                bi.type = tarfile.SYMTYPE
                bi.linkname = "package/elsewhere"
                tf.addfile(bi)
            else:
                raise ValueError("bad kind")
    return buf.getvalue()


def good_pair():
    wrapper = {
        "name": "@biomejs/biome",
        "version": VERSION,
        "optionalDependencies": {"@biomejs/cli-linux-x64": VERSION},
    }
    platform = {
        "name": "@biomejs/cli-linux-x64",
        "version": VERSION,
        "os": ["linux"],
        "cpu": ["x64"],
        "libc": ["glibc"],
    }
    wt = tar_bytes(wrapper)
    pt = tar_bytes(platform, b"synthetic-biome-binary")
    return wt, pt


def static_independence():
    tree = ast.parse(Path(ak.__file__).read_text())
    forbidden = {"arm", "gamma", "m_gamma", "phi", "phi_path", "deltapi", "delta_pi", "reach", "outcome", "performance"}
    hits = sorted({n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id.lower() in forbidden})
    sig = tuple(__import__("inspect").signature(ak.resolve_exact_linux_x64).parameters)
    expected = ("selected_version", "wrapper_tarball", "wrapper_integrity", "platform_tarball", "platform_integrity")
    return {"pass": not hits and sig == expected, "forbidden_name_hits": hits, "signature": list(sig)}


def positive_control():
    wt, pt = good_pair()
    r1 = ak.resolve_exact_linux_x64(VERSION, wt, sri(wt), pt, sri(pt))
    r2 = ak.resolve_exact_linux_x64(VERSION, wt, sri(wt), pt, sri(pt))
    return {
        "pass": r1.status == ak.IDENTIFIED and r1 == r2 and r1.executable == b"synthetic-biome-binary",
        "status": r1.status,
        "deterministic": r1 == r2,
        "content_addressed": all((r1.wrapper_tar_sha256, r1.platform_tar_sha256, r1.executable_sha256)),
    }


def rejection_matrix():
    wt, pt = good_pair()
    cases = {}
    cases["wrapper_integrity"] = ak.resolve_exact_linux_x64(VERSION, wt + b"x", sri(wt), pt, sri(pt)).status
    cases["platform_integrity"] = ak.resolve_exact_linux_x64(VERSION, wt, sri(wt), pt + b"x", sri(pt)).status

    wrong_wrapper = tar_bytes({
        "name": "@biomejs/biome", "version": "9.9.8",
        "optionalDependencies": {"@biomejs/cli-linux-x64": VERSION},
    })
    cases["wrapper_version"] = ak.resolve_exact_linux_x64(VERSION, wrong_wrapper, sri(wrong_wrapper), pt, sri(pt)).status

    wrong_dep = tar_bytes({
        "name": "@biomejs/biome", "version": VERSION,
        "optionalDependencies": {"@biomejs/cli-linux-x64": "9.9.8"},
    })
    cases["dependency_version"] = ak.resolve_exact_linux_x64(VERSION, wrong_dep, sri(wrong_dep), pt, sri(pt)).status

    for field, value in (("os", ["darwin"]), ("cpu", ["arm64"]), ("libc", ["musl"])):
        manifest = {
            "name": "@biomejs/cli-linux-x64", "version": VERSION,
            "os": ["linux"], "cpu": ["x64"], "libc": ["glibc"],
        }
        manifest[field] = value
        bad = tar_bytes(manifest, b"binary")
        cases[field] = ak.resolve_exact_linux_x64(VERSION, wt, sri(wt), bad, sri(bad)).status

    no_binary = tar_bytes({
        "name": "@biomejs/cli-linux-x64", "version": VERSION,
        "os": ["linux"], "cpu": ["x64"], "libc": ["glibc"],
    })
    cases["missing_binary"] = ak.resolve_exact_linux_x64(VERSION, wt, sri(wt), no_binary, sri(no_binary)).status

    symlink = tar_bytes({
        "name": "@biomejs/cli-linux-x64", "version": VERSION,
        "os": ["linux"], "cpu": ["x64"], "libc": ["glibc"],
    }, b"ignored", executable_kind="symlink")
    cases["symlink_binary"] = ak.resolve_exact_linux_x64(VERSION, wt, sri(wt), symlink, sri(symlink)).status

    duplicate = tar_bytes({
        "name": "@biomejs/cli-linux-x64", "version": VERSION,
        "os": ["linux"], "cpu": ["x64"], "libc": ["glibc"],
    }, b"binary", duplicate_binary=True)
    cases["duplicate_binary"] = ak.resolve_exact_linux_x64(VERSION, wt, sri(wt), duplicate, sri(duplicate)).status

    return {"pass": all(v == ak.NOT_IDENTIFIED for v in cases.values()), "cases": cases}


def no_smuggling():
    wt, pt = good_pair()
    cases = {}
    for bad in ("arm", "Gamma", "M_Gamma", "Phi_path", "DeltaPi", "outcome", "performance"):
        try:
            ak.resolve_exact_linux_x64(VERSION, wt, sri(wt), pt, sri(pt), **{bad: "A"})
            cases[bad] = "ACCEPTED"
        except TypeError:
            cases[bad] = "REJECTED"
    return {"pass": all(v == "REJECTED" for v in cases.values()), "cases": cases}


def main():
    results = {
        "static_independence": static_independence(),
        "positive_control": positive_control(),
        "fail_closed_matrix": rejection_matrix(),
        "smuggling": no_smuggling(),
    }
    overall = all(x["pass"] for x in results.values())
    out = {
        "benchmark_id": "VFA-0.2-QUOTIENT-REVISION-TOPOLOGY",
        "audit_identity": "VFA-0.2-FUTURE-CLI-ARTIFACT-ATTACK-1",
        "future_obligation_accessed": false,
        "attack_results": results,
        "artifact_contract_adjudication": "PASS" if overall else "FAIL",
        "scope": "synthetic npm-style tarballs only; no future package fetched",
        "authority_boundary": {"realized_artifact": "NOT_EVALUATED", "future_run": "NOT_AUTHORIZED"},
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
