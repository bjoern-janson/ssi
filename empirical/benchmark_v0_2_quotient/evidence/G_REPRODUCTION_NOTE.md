# G reproduction note

The predicate-G attack is deterministic and authorization-side. The selector, common-bundle, and temporal invariants were reproduced against the frozen logic before `G=PASS` was entered into `AUTHORIZATION_STATUS.json`.

This is **not** represented as a GitHub Actions or external-CI execution. The recorded checks use synthetic blinded candidate streams only; no real post-cutoff Biome release or prospective obligation was fetched or inspected.

The initial synthetic fixture contained one timestamp error: a decoy intended to be pre-freeze was placed after the synthetic freeze. That fixture was corrected before adjudication. The benchmark selector, treatment, source contract, and prospective rules were unchanged.

`G` here authorizes only the treatment-free selection/disclosure mechanism. The realized common-cause certificate remains uninstantiated and must later be committed before either arm receives the real selected bundle.
