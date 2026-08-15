# V2.2 Gate Calibration — Frozen from V2.1

This calibration is completed before any V2.2 treatment run.

The gate feature is the nearest-lineage distance already computed by the similarity router:

\[
d_{\min}=\min_i d_i.
\]

The only admissible threshold family is:

\[
\tau\in\{0/32,1/32,\ldots,32/32\}.
\]

For each V2.1 episode, the similarity-only and frozen `q/c` candidate orders were reconstructed from the frozen seeds and lineage state. Candidate-work cost was evaluated with the V2-frozen median candidate-cost field. The V2.1 measured mean incremental router cost was charged as:

\[
\widehat C_{\rm route,inc}=7762.43017578125\ \mathrm{ns}.
\]

Threshold selection minimized predicted net executable contrast:

\[
\widehat\Delta(\tau)
=
\frac1K\sum_k
\mathbf 1[d_{\min,k}\ge\tau]
\left(
\widehat C_{q/c,k}-\widehat C_{S,k}
+7762.43017578125
\right).
\]

The minimizing threshold is:

\[
\boxed{\tau=11/32=0.34375.}
\]

Calibration diagnostics at the selected threshold:

- V2.1 episodes: `6144`;
- gate-open episodes: `267`;
- gate-open fraction: `0.04345703125`;
- predicted mean net contrast over all V2.1 episodes: `-261.84198292096454 ns/episode`.

The realized V2.1 total-CPU contrast was not part of the threshold objective. V2.2 uses fresh seeds and fresh held-out worlds. The threshold cannot be changed after V2.2 execution.
