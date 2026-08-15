#!/usr/bin/env python3
"""Capability-only probe for the frozen V3 CPU-package energy boundary.

This script does NOT run A/B treatments. It discovers cumulative physical-energy
interfaces, verifies readable units/path metadata, and checks whether counters
move under a short deterministic CPU load.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import platform
import time
from pathlib import Path


def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception:
        return None


def read_int(path: Path):
    text = read_text(path)
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def powercap_records():
    seen = set()
    records = []
    patterns = [
        "/sys/class/powercap/**/energy_uj",
        "/sys/devices/virtual/powercap/**/energy_uj",
    ]
    for pattern in patterns:
        for raw in glob.glob(pattern, recursive=True):
            path = Path(raw).resolve()
            if path in seen or not os.access(path, os.R_OK):
                continue
            seen.add(path)
            zone = path.parent
            name = read_text(zone / "name")
            max_range = read_int(zone / "max_energy_range_uj")
            records.append(
                {
                    "kind": "powercap",
                    "path": str(path),
                    "zone": str(zone),
                    "name": name,
                    "unit": "microjoule",
                    "max_energy_range_uj": max_range,
                    "package_candidate": bool(name and ("package" in name.lower() or "pkg" in name.lower())),
                }
            )
    return records


def hwmon_records():
    records = []
    for raw in glob.glob("/sys/class/hwmon/hwmon*/energy*_input"):
        path = Path(raw).resolve()
        if not os.access(path, os.R_OK):
            continue
        hwmon = path.parent
        stem = path.name.replace("_input", "")
        label = read_text(hwmon / f"{stem}_label")
        chip = read_text(hwmon / "name")
        lower = " ".join(x for x in [chip, label] if x).lower()
        records.append(
            {
                "kind": "hwmon",
                "path": str(path),
                "hwmon": str(hwmon),
                "chip": chip,
                "label": label,
                "unit": "microjoule",
                "max_energy_range_uj": None,
                "package_candidate": any(token in lower for token in ("socket", "package", "pkg")),
            }
        )
    return records


def cpu_load(seconds: float = 1.5):
    deadline = time.perf_counter() + seconds
    x = b"ssi-v3-package-energy-capability-probe"
    loops = 0
    while time.perf_counter() < deadline:
        for _ in range(5000):
            x = hashlib.blake2b(x, digest_size=32).digest()
            loops += 1
    return loops, x.hex()


def counter_delta(before: int | None, after: int | None, max_range: int | None):
    if before is None or after is None:
        return None, "READ_FAILURE"
    if after >= before:
        return after - before, "OK"
    if max_range is not None and max_range > 0:
        return (max_range - before) + after, "WRAP_HANDLED"
    return None, "NEGATIVE_DELTA_WRAP_UNRESOLVED"


def main():
    records = powercap_records() + hwmon_records()
    before = {r["path"]: read_int(Path(r["path"])) for r in records}
    loops, digest = cpu_load()
    after = {r["path"]: read_int(Path(r["path"])) for r in records}

    for r in records:
        delta, status = counter_delta(
            before[r["path"]], after[r["path"]], r.get("max_energy_range_uj")
        )
        r["before_uj"] = before[r["path"]]
        r["after_uj"] = after[r["path"]]
        r["delta_uj_under_probe_load"] = delta
        r["delta_status"] = status
        r["moved_positive"] = bool(delta is not None and delta > 0)

    package_candidates = [
        r for r in records if r["package_candidate"] and r["moved_positive"]
    ]
    status = (
        "PACKAGE_ENERGY_CANDIDATE_IDENTIFIED"
        if package_candidates
        else "NOT_IDENTIFIED_NO_MOVING_PACKAGE_COUNTER"
    )

    result = {
        "status": status,
        "treatment_run_performed": False,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "kernel": platform.release(),
        "load_seconds": 1.5,
        "load_loops": loops,
        "load_digest": digest,
        "records": records,
        "package_candidates": package_candidates,
        "interpretation": (
            "A moving cumulative package/socket energy counter was found. Freeze the exact device path, domain, wrap semantics, and batch calibration before any V3 A/B run."
            if package_candidates
            else "No admissible moving CPU-package/socket cumulative energy counter was identified. Do not run V3 A/B or substitute timing-derived joules."
        ),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
