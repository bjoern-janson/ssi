# I freeze packet candidate 6 — rejected before authorization

```text
PACKET_ID = VFA-0.2-FROZEN-PACKET-6
PACKET_SHA256 = 08f8907abf636234699c7155a672b7173645df6a60c0179e45e5475206026a1b
EXECUTION_ROOT_SHA256 = 2fb148232b4da373095ccac97ec4691e90da2f7f6820c2b947f035b8aaeb31e8
PACKET_MANIFEST_GIT_BLOB_SHA1 = 1c5b1cf658eb2fff448549389bf11830e07fbfa2
FREEZE_CANDIDATE_COMMIT = a9f2a3a0d28b315d024249552b4f13e57b8e5317
FREEZE_CANDIDATE_TREE = d8ad527d3d78e72f11789163f8f7a2831ea62976
FREEZE_CANDIDATE_TIMESTAMP_UTC = 2026-08-15T18:44:24Z
FREEZE_ANCHOR_SHA256 = c427a76810199ab17d847d833be540a336cfd4e3d91605126c7e72a213344b0c
FREEZE_ANCHOR_GIT_BLOB_SHA1 = 324c982404b6c0a51974fca0a38f8913e339a218
AUTHORIZATION_CERTIFICATE = NOT_ISSUED
STATUS = REJECTED_BEFORE_I_ADJUDICATION
```

Candidate 6 repaired the version-specific anchor bug and produced a generalized sequential packet/anchor identity.

The full execution-path review then found a remaining Frankenstein channel in the authorized runner: project modules were imported by ordinary Python module resolution before the packet member set and blobs were validated. A stale or shadowing same-name module on `sys.path` could therefore execute before the later hash check, even though the expected packet files themselves were correct.

This violates the strengthened predicate-I execution requirement that identity rejection precede scientific execution.

Minimal repair:

- remove all top-level project-module imports from the authorized runner;
- make the runner a stdlib-only bootstrap;
- pin the expected custody-kernel Git blob inside the runner;
- verify and load that exact custody file by absolute path before trusting packet authority;
- after custody validation and exact execution-root verification, load the G integration kernel, treatment materializer, and endpoint evaluator only from their packet-authorized absolute paths using isolated module names;
- reject ambient/project import shadowing rather than relying on `sys.path` order.

Candidate 6 must never receive an authorization certificate. No future obligation, package, `T_future`, `J_future`, `DeltaPi`, or outcome was accessed during this rejection.
