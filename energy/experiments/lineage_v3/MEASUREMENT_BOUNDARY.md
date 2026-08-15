# Lineage Corrective Economy V3 — Frozen Physical-Energy Boundary

Status: **FROZEN BEFORE ANY IDENTIFIED V3 A/B ENERGY RUN.**

This document fixes the scientific energy object before choosing hardware. Hardware must satisfy this boundary; the boundary must not be changed to fit available hardware after treatment results are observed.

## 1. Primary physical-energy object

The primary V3 energy estimand is **CPU-package physical energy**:

\[
E_{\rm pkg}.
\]

V3 therefore chooses a **device/package boundary**, not a process, whole-node, or wall boundary.

The primary treatment contrast is:

\[
\Delta E_{\rm pkg}
=
E_{\rm pkg}^{A}
-
E_{\rm pkg}^{B},
\]

where:

- `A = Lambda_preserved`;
- `B = Lambda_unavailable`;
- the treatment and heterogeneous corrective workload are the frozen V2 mechanism;
- no V2.1/V2.2 cost-aware or gated router is permitted.

The directional hypothesis is:

\[
\mathbb E[\Delta E_{\rm pkg}]<0.
\]

## 2. Why package rather than process/node/wall

`E_process` is rejected as the primary object because no direct hardware process-energy counter is assumed, and attributing package or wall energy to a process by CPU-time conversion would recreate the unearned bridge V3 is meant to test.

`E_node` and `E_wall` are scientifically useful stronger boundaries but include additional components and background sources not required for the first physical bridge. They may be tested later as separately frozen replications; they cannot be substituted post hoc to rescue V3.

The package boundary is chosen because the earned V2 mechanism is CPU-executed and because cumulative hardware package-energy counters can be independently read without converting CPU time into joules.

## 3. Included work

Inside each measured treatment batch, the package-energy interval must include all treatment-specific CPU-package work from the frozen V2 accounting boundary:

- lineage retrieval and similarity ordering;
- candidate repair execution;
- exact validation;
- lineage update;
- treatment-specific indexing or memory-controller/package work that occurs inside the measured package domain.

The frozen V2 common challenge-generation work remains outside the A/B treatment interval:

- clean-payload generation;
- corruption generation;
- frozen challenge construction common to both arms.

No treatment-specific work may be moved outside the measured interval.

## 4. Explicitly outside the primary boundary

Unless physically included in the hardware package counter, V3-primary does **not** claim energy effects for:

- external DRAM DIMMs;
- SSD/storage devices;
- NIC/network equipment;
- fans or chassis cooling;
- GPU/accelerator devices;
- display/peripherals;
- PSU conversion losses;
- whole-node or wall-plug energy.

Accordingly, a positive V3-primary result licenses only a **CPU-package physical-energy** claim on the measured hardware. It is not automatically a node-energy or wall-energy claim.

## 5. Admissible measurement interface

Before any A/B treatment run, the environment must expose a directly readable cumulative package-energy counter with documented physical units, for example:

- Linux powercap/RAPL-style `energy_uj` for the CPU package;
- a documented AMD CPU socket/package cumulative energy counter;
- another independently documented cumulative package-energy interface with equivalent semantics.

The counter must provide a direct cumulative energy quantity in joules or exactly convertible units.

Not admissible as the primary V3 measurement:

- process CPU time;
- wall-clock time;
- TDP or rated power;
- utilization-derived energy;
- provider-estimated joules without a documented hardware energy counter;
- instantaneous power alone unless a separate sampling/integration protocol is frozen and validated before A/B observation.

If the interface is unavailable or its units/domain cannot be established:

`NOT_RUN_MEASUREMENT_BOUNDARY_NOT_IDENTIFIED`.

## 6. Counter validation gate

Before treatment results may be observed, the selected hardware must pass a measurement-only capability check establishing:

1. exact counter path/API and package-domain name;
2. documented units;
3. monotone or correctly wrapped cumulative behavior;
4. readable `max_energy_range` or otherwise specified wrap semantics;
5. observable counter movement under a calibration CPU load;
6. stable enough resolution to support batch measurement;
7. no treatment result is used to choose or validate the meter.

Counter failure is `NOT_IDENTIFIED`, not evidence against the treatment hypothesis.

## 7. Batch amplification

Single V2 corrections are too short to be treated as the physical measurement unit by default.

The V3 measurement unit is a **paired batch** containing repeated frozen V2 corrections:

\[
B_A=\sum_{k=1}^{M}A_k,
\qquad
B_B=\sum_{k=1}^{M}B_k.
\]

The batch multiplier `M` must be fixed from meter resolution/background calibration **before** observing the A/B energy contrast. `M` may not be selected to improve the treatment result.

## 8. Paired order and attribution

A/B batch order must be balanced within replicate blocks, e.g.:

`AB, BA, BA, AB, ...`

or an equivalent preregistered randomized balance.

The same frozen challenge exposures must be used for each paired A/B batch.

Because the package counter measures the package rather than a process, treatment attribution comes from:

- dedicated/bare-metal execution where feasible;
- controlled background load;
- paired identical workload exposure;
- balanced order;
- immediate pre/post cumulative counter reads.

No process-energy attribution model is permitted.

## 9. Correction-quality guard

The frozen V2 correction-quality contract remains unchanged:

\[
H_{\rm recover}=1,
\quad
R_{\rm collateral}=0,
\quad
R_{\rm reopen}=1,
\quad
\mathrm{Auth}=1.
\]

Physical-energy reduction cannot rescue a correction-quality failure.

## 10. Optional stronger replication

A future separately preregistered replication may measure:

\[
E_{\rm wall}
\]

with a cumulative wall-energy meter. That would include CPU package, external memory, storage, cooling, PSU losses, and other node loads inside the metered outlet boundary.

Such a replication is stronger in physical coverage but noisier in attribution. It is not required for, and cannot retroactively redefine, the primary V3 package-energy estimand.

## 11. Authority boundary

A positive primary result would support only:

> On the measured hardware package and under the frozen V2 heterogeneous executable correction workload, persistent validated lineage reduced measured CPU-package physical energy while preserving the same warranted correction criterion.

It would not establish whole-node energy savings, wall-plug energy savings, GPU/LLM savings, provider-scale savings, general AI energy efficiency, Axis I, or SSI core theory.
