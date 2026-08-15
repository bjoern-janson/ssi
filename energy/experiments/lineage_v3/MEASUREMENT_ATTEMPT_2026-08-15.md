# V3 Physical-Energy Measurement Attempt — 2026-08-15

## Status

**NO PHYSICAL-ENERGY CONTRAST IDENTIFIED.**

This attempt tried to open the already-frozen V3 measurement bridge without substituting CPU time, wall time, TDP, utilization, or inferred joules.

The V3 treatment was **not** executed because no admissible physical-energy boundary could be invoked from the available execution environments.

## 1. Local KVM runtime

Observed runtime:

- Linux `6.18.35`, x86_64;
- AMD EPYC 9V74 host-visible CPU;
- KVM full virtualization;
- 5 vCPUs exposed.

No readable cumulative physical-energy interface was present:

- no `/sys/class/powercap/**/energy_uj`;
- no `/sys/devices/virtual/powercap/**/energy_uj`;
- no hwmon cumulative energy input;
- no hwmon power input/average channel;
- no `/dev/cpu/*/msr` device;
- no power PMU under `/sys/bus/event_source/devices`;
- no NVIDIA/AMD GPU telemetry tool/device;
- no `perf`, `turbostat`, LIKWID, PAPI, or `powertop` executable.

The container runs as uid 0 but does not hold `CAP_SYS_MODULE`, `CAP_SYS_RAWIO`, `CAP_SYS_ADMIN`, or `CAP_PERFMON`.

Attempts to load `amd_rapl`, `amd_energy`, and Intel RAPL modules failed because the matching kernel modules are not present under `/lib/modules/6.18.35` and the container lacks module-loading capability.

Therefore the physical-energy gate remained closed.

## 2. Hosted macOS capability-probe attempt

A temporary GitHub Actions workflow was created solely to probe whether a hosted macOS runner exposed a physically grounded `powermetrics` channel. It contained no A/B treatment execution.

Two app-authored branch pushes were made while the workflow existed. GitHub reported zero workflow runs for both pushed commit SHAs. The current repository connection does not expose a workflow-dispatch action, so the hosted probe could not be invoked.

The temporary `.github/workflows/` file and trigger file were then deleted. The final branch diff returns to the intended energy-suite isolation; the capability-probe plan remains under `energy/experiments/lineage_v3/` only.

No macOS power measurements were observed and no inference is taken from this route.

## 3. External instrumentation integrations

Available/installable integrations were searched for remote shell/cloud-compute and smart-meter/home-energy capabilities. No usable integration was available in the current session.

## 4. Adjudication

The evidential state remains:

```text
V0  supported: synthetic traversal economy
V1  supported: executed CPU-work economy
V2  supported: heterogeneous executed corrective-work economy
V3  OPEN:      CPU work -> measured physical energy
```

Formally,

$$
\Delta E_{\rm physical}
=E_A-E_B
=\texttt{NOT_IDENTIFIED}.
$$

This means no numerical physical-energy effect has been estimated. It is neither zero, negative, nor positive.

## 5. Next admissible measurement

The next V3 treatment run requires direct access to one of:

1. bare-metal or sufficiently privileged Linux exposing a documented cumulative energy counter such as `energy_uj`;
2. another documented cumulative hardware-energy counter with explicit units; or
3. a synchronized external power/energy meter around the complete A/B batch boundary.

Once such a device is visible, freeze the exact device/counter path, units, counter-wrap rule, batch duration/size, A/B block randomization, thermal/background controls, and minimum identified replicate count **before** observing A/B energy results.

Until then the V3 stopping rule remains active.