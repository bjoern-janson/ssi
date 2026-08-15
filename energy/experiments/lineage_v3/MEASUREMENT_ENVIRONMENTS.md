# V3 Measurement Environments — Ranked Acquisition Plan

Status: **environment search only; no V3 A/B treatment result.**

Scan date: **2026-08-15**.

The scientific boundary is already frozen in `MEASUREMENT_BOUNDARY.md`: V3-primary requires a cumulative **CPU-package physical-energy** counter. Hardware is ranked by whether it can satisfy that object, not by whether it provides some other convenient proxy.

## Priority 0 — Existing bare-metal Linux machine

Cost: **€0 if available.**

Run:

```bash
python3 energy/experiments/lineage_v3/probe_package_energy.py
```

An admissible candidate is a moving cumulative package/socket energy interface such as Linux powercap `energy_uj` or a standard hwmon cumulative socket/package energy channel.

If the probe reports no moving package counter, stop. Do not substitute CPU time or estimated joules.

A Linux live environment on an existing physical x86 machine is acceptable for the capability probe; a VM/container that does not expose the hardware counter is not.

## Priority 1 — Short-lived dedicated bare-metal Intel server

If no local package counter exists, the cheapest remote route identified in the current scan is a dedicated server rented only long enough to pass the capability gate and, if successful, run V3.

Hetzner Server Auction currently advertises refurbished **dedicated** servers with full root access, hourly prices, no setup fee, and immediate cancellation. Current indexed listings include Intel Core i7-6700/i7-7700 systems around roughly **€0.065–€0.08/hour excl. VAT**, depending on the specific auction listing.

Acquisition rule:

1. Prefer an Intel i7-6700/i7-7700 bare-metal auction machine.
2. Boot the rescue/Linux environment.
3. Clone the frozen branch.
4. Run only `probe_package_energy.py` first.
5. If a moving package `energy_uj` counter is not identified, cancel the server; no treatment run.
6. If the counter passes, freeze the exact counter path/domain, wrap semantics, meter-resolution calibration, batch multiplier, and block order before any A/B energy observation.

This route is attractive because the spend required to test the measurement gate is measured in hours rather than a monthly commitment. Availability and auction prices are dynamic.

## Priority 2 — Whole-node/wall replication, not V3-primary

A cumulative wall-energy meter is a useful stronger physical-coverage replication after package-level V3, but it does **not** substitute for the already frozen primary package-energy object.

One inexpensive current example is Shelly Plug S Gen3. Shelly documents a cumulative active-energy counter (`aenergy.total`) in Watt-hours through its local RPC interface, and the device provides power/energy metering. Current German pricing observed in the scan was approximately **€16.80–€24 including VAT**, depending on variant/promotion.

A wall-meter replication would require a separately frozen node/wall boundary and substantially larger A/B batches because whole-node background energy dominates microsecond-scale correction work.

## Official measurement semantics used by the plan

Linux powercap documents `energy_uj` as the cumulative energy counter in microjoules, with `max_energy_range_uj` providing the counter range.

Linux hwmon documents `energy[1-*]_input` as cumulative energy use in microjoules.

AMD documents CPU core/socket energy counters based on RAPL/MSR interfaces on supported bare-metal CPUs.

These are admissible because they report cumulative physical-energy quantities directly. Timing-derived conversion remains prohibited.

## Stop rule

Do not search indefinitely for an instrument and do not redesign the workload around the instrument.

The next transition is only:

```text
measurement boundary identified
    -> freeze meter-specific calibration/batch contract
    -> run frozen V2 A/B mechanism under V3
```

Otherwise V3 remains `NOT_IDENTIFIED`.
