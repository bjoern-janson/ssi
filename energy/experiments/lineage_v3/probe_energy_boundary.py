#!/usr/bin/env python3
"""Probe whether the current runtime exposes a V3-admissible physical-energy boundary.

This is a measurement-capability probe only. It does not execute A/B treatment episodes.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
from pathlib import Path


def readable_files(patterns: list[str]) -> list[str]:
    found: list[str] = []
    for pattern in patterns:
        for path in Path("/").glob(pattern.lstrip("/")):
            try:
                if path.is_file() and os.access(path, os.R_OK):
                    found.append(str(path))
            except OSError:
                pass
    return sorted(set(found))


def main() -> None:
    cumulative_energy = readable_files(
        [
            "/sys/class/powercap/**/energy_uj",
            "/sys/devices/virtual/powercap/**/energy_uj",
            "/sys/class/hwmon/**/energy*_input",
        ]
    )
    instantaneous_power = readable_files(
        [
            "/sys/class/hwmon/**/power*_input",
            "/sys/class/hwmon/**/power*_average",
        ]
    )
    msr_devices = readable_files(["/dev/cpu/*/msr"])
    tools = {
        name: shutil.which(name)
        for name in ("perf", "turbostat", "likwid-perfctr", "papi_avail")
    }

    gate_pass = bool(cumulative_energy)
    status = (
        "MEASUREMENT_BOUNDARY_IDENTIFIED"
        if gate_pass
        else "NOT_RUN_MEASUREMENT_BOUNDARY_NOT_IDENTIFIED"
    )

    result = {
        "status": status,
        "gate_pass": gate_pass,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cumulative_energy_interfaces": cumulative_energy,
        "instantaneous_power_interfaces": instantaneous_power,
        "msr_devices": msr_devices,
        "tools": tools,
        "interpretation": (
            "At least one directly readable cumulative physical-energy counter is exposed."
            if gate_pass
            else "No directly readable cumulative physical-energy counter is exposed; V3 A/B treatment execution is prohibited by preregistration."
        ),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
