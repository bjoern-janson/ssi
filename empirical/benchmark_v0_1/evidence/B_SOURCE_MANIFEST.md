# B Evidence Input — Frozen Construction Source Manifest

## Status

```text
B_SOURCE_MANIFEST = FROZEN_INPUT
B_ADJUDICATION = NOT_EVALUATED
```

This artifact freezes the pre-disclosure upstream objects permitted as historical migration evidence for constructing the A/B treatment. It does **not** define the final treatment, does not compute $\Phi_A$ or $\Phi_B$, and therefore cannot by itself pass predicate B.

Its purpose is anti-selection: after this manifest is committed, historical migration examples may not be added, removed, or replaced because they make the eventual topology contrast easier to obtain.

## Upstream cutoff

```text
UPSTREAM_REPOSITORY = biomejs/biome
CONSTRUCTION_SOURCE_COMMIT = b51d8b1598effd064c3490c3866d5b2d60ebd5f8
```

All objects below are addressed inside that immutable commit.

## Migration test source

```text
crates/biome_cli/tests/cases/migrate_v2.rs
GIT_BLOB_SHA1 = 4e9d629645b23af728d1145bd7c26d0ae3e5ac7c
```

This source contains the pre-migration configuration fixtures and invokes the same Biome `migrate --write` machinery whose outputs are snapshot-tested.

## Migration implementation source

```text
crates/biome_cli/src/commands/migrate.rs
GIT_BLOB_SHA1 = f3381ceb588bb0183343dd04eba3257294777e18
```

## V2 migration snapshot tree

```text
crates/biome_cli/tests/snapshots/main_cases_migrate_v2
GIT_TREE_SHA1 = d24f2716b94d1537294c915d82a6084ca6f517fa
```

The tree is complete at the cutoff and contains exactly the following six snapshot blobs:

| Snapshot | Git blob SHA-1 | Bytes |
|---|---|---:|
| `should_migrate_aws_config.snap` | `2ae1e3acf91568190079695c138a38d7750a1111` | 1476 |
| `should_migrate_issue_5465.snap` | `91f096105cf96900b5e6ee10388bda9a5c940934` | 1596 |
| `should_migrate_nested_config.snap` | `c922fe4ecc3603a658bce07cf12ee8125fee83e5` | 1965 |
| `should_successfully_migrate_ariakit.snap` | `6afbb5fa2b7dc7791596f45af99fc56a02385d2a` | 1997 |
| `should_successfully_migrate_knip.snap` | `9d8c80e3bead3e126196fcda3fc0400b87cf5a83` | 3318 |
| `should_successfully_migrate_sentry.snap` | `f045f4304519f41b2980f966f3b44d7f57ae146f` | 5540 |

The six snapshots include project-scale and regression/nested migration cases. They are historical pre-freeze evidence only; none is the future confirmatory obligation.

## Broader configuration source identities

The configuration implementation subtree at the cutoff is rooted under:

```text
crates/biome_configuration/src/**
```

and the generated-configuration subtree has:

```text
crates/biome_configuration/src/generated
GIT_TREE_SHA1 = 41b679c432570eb7869516aa8be4cbd0d1f605af
```

These sources may be used only through a deterministic extraction procedure committed before B is adjudicated. Manual outcome-aware extraction is prohibited.

## Allowed use

The B construction may derive treatment data only from:

1. the immutable objects listed above;
2. other objects at `CONSTRUCTION_SOURCE_COMMIT` that are added to this manifest **before any A/B construction score or $\Phi$ value is observed**;
3. deterministic construction code committed in the SSI benchmark branch.

Once any A/B construction score or $\Phi$ value has been observed, this manifest is closed: no further historical object may be admitted into the confirmatory construction lineage.

## Forbidden use

```text
- post-cutoff Biome commits or releases
- the realized future obligation
- future-outcome-dependent choice of historical fixtures
- hand-selected migration relations added after observing Phi_A - Phi_B
- post-hoc deletion of difficult or null historical cases
```

## B pass requirements still outstanding

Predicate B remains `NOT_EVALUATED` until all of the following exist and are frozen:

```text
- exact A construction
- exact B construction
- deterministic topology-scrambling operator
- executable measurement for every Phi component
- admissible transformation / missingness rules
- expected direction of the A/B topology contrast
- recomputation evidence showing the recorded Phi values reproduce
```

This manifest is therefore construction evidence, not authorization evidence by itself.
