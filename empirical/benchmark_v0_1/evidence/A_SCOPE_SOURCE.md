# A Evidence — Prospective Scope and Source

## Status

This artifact supplies the evidence required to adjudicate predicate A before benchmark freeze.

It fixes the external project, construction cutoff, admissible future-change class, exclusions, observation horizon, and deterministic first-qualifying-obligation rule. It does **not** disclose or select a realized future obligation.

## Upstream project

```text
UPSTREAM_REPOSITORY = biomejs/biome
UPSTREAM_OWNERSHIP = external public open-source project
DEFAULT_BRANCH = main
```

Biome is independent of the SSI repository and exposes a versioned configuration surface (`biome.json` / `biome.jsonc`) with published JSON schemas and migration machinery.

## Construction cutoff

The construction source cutoff is the immutable Biome commit:

```text
CONSTRUCTION_SOURCE_COMMIT = b51d8b1598effd064c3490c3866d5b2d60ebd5f8
CONSTRUCTION_SOURCE_COMMIT_TIME = 2026-08-15T11:23:09Z
```

The current stable CLI release observed before SSI freeze is:

```text
BASELINE_STABLE_RELEASE = @biomejs/biome@2.5.8
BASELINE_RELEASE_ID = 368434108
BASELINE_PUBLISHED_AT = 2026-08-11T08:52:51Z
```

The benchmark construction may use only information at or before `CONSTRUCTION_SOURCE_COMMIT` plus artifacts explicitly vendored into the construction packet. No later Biome commit, release, schema, PR implementation, or migration patch may enter A/B construction, matching, or Phi measurement.

## Configuration-source scope

The configuration-obligation source is restricted to the Biome configuration and migration surface. The source paths used to detect and audit a qualifying change are:

```text
crates/biome_configuration/**
crates/biome_service/src/configuration.rs
xtask/codegen/src/generate_schema.rs
crates/biome_cli/tests/cases/migrate*.rs
```

Versioned published JSON schemas for stable CLI releases are also admissible evidence. The official Biome configuration reference states that Biome publishes a JSON schema for `biome.json` / `biome.jsonc`, both inside the `@biomejs/biome` package as `configuration_schema.json` and through versioned `biomejs.dev/schemas/<version>/schema.json` URLs.

## Prospective horizon

```text
OBSERVATION_HORIZON = 180 calendar days after t_freeze
```

If no qualifying obligation occurs within the horizon:

```text
OUTCOME = NO_QUALIFYING_OBLIGATION
```

The horizon may not be extended and a later event may not be substituted without creating a new benchmark identity.

## Admissible future-change class

A future release is eligible only if all of the following are true:

1. it is a stable `@biomejs/biome@<version>` CLI release published strictly after `t_freeze`;
2. the relevant configuration-changing implementation becomes public strictly after `t_freeze`;
3. the release contains at least one non-additive, migration-relevant change to the configuration surface;
4. the change can be established from the frozen source paths and/or the versioned published JSON schema;
5. the same qualifying obligation can be disclosed identically to A and B.

A change is **migration-relevant** if at least one of the following holds relative to the immediately preceding stable CLI release:

```text
PROPERTY_REMOVED
PROPERTY_RENAMED
PROPERTY_PATH_MOVED
ACCEPTED_TYPE_CHANGED
ENUM_OR_DOMAIN_NARROWED
REQUIREDNESS_CHANGED
VERSIONED_CONFIGURATION_SEMANTICS_CHANGED
```

The last category qualifies only when a frozen pre-freeze configuration fixture that is valid under the baseline is mechanically shown to require a configuration migration, become invalid, or change configuration semantics under the candidate stable release.

## Exclusions

The following do not qualify:

```text
PRERELEASE_OR_NIGHTLY
LSP_ONLY_RELEASE
EDITOR_EXTENSION_ONLY_RELEASE
DOCS_ONLY_CHANGE
ADDITIVE_ONLY_CONFIG_OPTION
ADDITIVE_ONLY_LINT_RULE
PERFORMANCE_ONLY_CHANGE
BUGFIX_WITH_NO_CONFIG_MIGRATION_OBLIGATION
CHANGE_WHOSE_RELEVANT_IMPLEMENTATION_WAS_PUBLIC_BEFORE_t_freeze
```

A release is not promoted into eligibility merely because it produces a large A/B difference.

## Earliest-public-availability rule

For the configuration change that would make a release qualify, the audit must establish that its relevant implementation content was not public before `t_freeze`.

Preferred proof:

```text
SOURCE_PR_CREATED_AT > t_freeze
AND
SOURCE_PR_MERGED_AT > t_freeze
```

If no source PR exists, the qualifying implementation commit must have both author and committer timestamps after `t_freeze`, and the audit must find no pre-freeze repository object containing the equivalent implementation patch.

If this independence check cannot be established, that release is excluded.

## Deterministic first-qualifying-obligation rule

After `t_freeze`:

1. enumerate official stable `@biomejs/biome@<version>` releases with `published_at > t_freeze`;
2. order them by `(published_at, GitHub release id)` ascending;
3. for each release in order, apply the admissibility and exclusion rules above without inspecting A/B future outcomes;
4. select the first release that qualifies;
5. define the migration-relevant configuration delta from the immediately preceding stable CLI release to that selected release as `O_future`.

No later release may replace the first qualifying release because the later release is easier, cleaner, or produces a larger effect.

## Evidence coordinates

Observed before freeze:

- `biomejs/biome` is an active public repository with default branch `main`.
- `main` resolved to `b51d8b1598effd064c3490c3866d5b2d60ebd5f8` at evidence collection.
- stable release `@biomejs/biome@2.5.8` was published at `2026-08-11T08:52:51Z`.
- the repository contains configuration generation code and explicit migration tests, including `xtask/codegen/src/generate_schema.rs` and `crates/biome_cli/tests/cases/migrate_v2.rs`.
- Biome's official configuration reference documents the published versioned JSON schema mechanism.

These are source-selection facts only. They do not contain the future obligation.

## Predicate-A adjudication rule

This evidence permits predicate A to pass before disclosure iff:

```text
- this artifact is content-addressed;
- the construction cutoff commit is immutable and used as declared;
- all source-selection fields above remain unchanged;
- no future obligation has been selected by discretionary inspection;
- the first-qualifying rule remains the only authorized selector.
```

Realized-event conformance is checked after disclosure as part of faithful execution. It does not retroactively alter predicate A or the authorization certificate.
