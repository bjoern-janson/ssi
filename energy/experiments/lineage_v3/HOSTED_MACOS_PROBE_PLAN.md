# V3 Hosted macOS Measurement-Capability Probe Plan

## Status

**CAPABILITY PROBE ONLY — NO A/B TREATMENT DATA.**

The local KVM runtime does not expose a preregistration-admissible physical-energy interface. Before changing the V3 evidential status, a separate hosted-hardware capability probe may test whether a macOS runner exposes a physically grounded power/energy channel through the operating system.

This probe does not execute treatment A or B and therefore cannot support or contradict the V3 hypothesis.

## Gate

A hosted runner is admissible for a subsequent V3 hardware-specific preregistration only if all of the following are observed before any A/B execution:

1. a documented OS/hardware power or cumulative-energy channel is readable;
2. its units are explicit and convertible to joules;
3. repeated reads over an idle and a CPU-loaded interval show non-degenerate, workload-responsive measurements;
4. the sampling command can be synchronized around a batch whose duration is long relative to measurement resolution;
5. no provider-derived utilization-to-energy estimate is substituted for the physical channel.

If these conditions do not hold, hosted-hardware V3 remains `NOT_IDENTIFIED`.

## Probe target

The initial target is GitHub-hosted macOS and the system `powermetrics` utility, queried only for capability and raw sampler behavior.

The probe may record:

- hardware and OS identity;
- `powermetrics --help` / available samplers;
- whether privileged invocation is allowed;
- raw CPU/package power sampler output at idle;
- raw CPU/package power sampler output during a fixed CPU load;
- sampler interval and units.

No integration rule, treatment batch size, thermal-control rule, or V3 energy estimand is evaluated until after this capability probe. If the gate passes, those items must be frozen in a separate hardware-specific addendum before treatment execution.