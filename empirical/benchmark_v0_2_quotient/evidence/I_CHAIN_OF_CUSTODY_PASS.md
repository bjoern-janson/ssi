# Predicate I — freeze identity, execution, and provenance PASS

```text
BENCHMARK = VFA-0.2-QUOTIENT-REVISION-TOPOLOGY
PREDICATE_I = PASS
FUTURE_OBLIGATION_ACCESSED = FALSE
REAL_FUTURE_EXECUTION = FALSE
```

## Frozen object

```text
PACKET_ID = VFA-0.2-FROZEN-PACKET-7
PACKET_SHA256 = 2d8b64e28f8207b51d1acae2459d0cf89774e7be0c10cb5a2a04808029ade3b7
PACKET_MANIFEST_GIT_BLOB_SHA1 = 9781f8c918263fba11ea6ad3a2e735f75755668f
EXECUTION_ROOT_SHA256 = 56d2f3a996f6dc71183fa7325af06d738e8ba994f9b62a2ba454f85c5fe8fe1d
FREEZE_COMMIT = b8c39ebc751c30f9d2e3164160fc5ca31904ba46
FREEZE_TREE = 81c406228b21127d104f264e0532fc50fdda3e8c
FREEZE_TIMESTAMP_UTC = 2026-08-15T18:50:48Z
FREEZE_ANCHOR_SHA256 = 8dd2afd4f32ac5d78618e6dfd89fe16c3a72410bf2c6beeb26196d864dcd732b
FREEZE_ANCHOR_GIT_BLOB_SHA1 = 94be872e1cc281ddb4dfefec0a851f0079e1c12f
```

GitHub commit/tree/blob inspection verified that the declared packet bytes occur at the recorded freeze commit/tree. The freeze commit is unsigned; this evidence therefore claims repository commit/tree/blob provenance for accidental, post-hoc, stale-certificate, and mixed-lineage drift. It does not claim cryptographic signer attestation or protection against a malicious repository administrator rewriting all history.

## I factorization

```text
I_identity     = PASS
I_completeness = PASS
I_immutability = PASS
I_execution    = PASS
I_provenance   = PASS
```

The packet binds exact path/blob/role identities, a closed packet/member/certificate/realization schema, a complete sequential lineage of six rejected uncertified packet candidates, the final evaluation rule, future-obligation rule, grounded common-cause rule, authorized-runner entrypoint, and the exact execution-member root.

The future-realization object is deliberately separate from the frozen packet. Future fields may instantiate only the exact frozen realized-record schema; they cannot extend or replace packet, evaluation, authority, or execution controls.

## Executable chain-of-custody attack

Machine result:

```text
construction/i_chain_of_custody_audit_v7.json
GIT_BLOB_SHA1 = 4a280b17fa1afbcac0034f240877448e7ecf5122
```

External GitHub Actions validation:

```text
WORKFLOW = VFA I chain-of-custody audit
PASSING_RUN_ID = 31902486711
PASSING_JOB_ID = 95055252842
RUNNER = ubuntu-latest
PYTHON = 3.13.5
SYSTEM = Linux
MACHINE = x86_64
CONCLUSION = success
```

The passing run executed the actual packet-7 authorized runner with synthetic contract-valid future objects. The positive execution produced:

```text
RESULT_SHA256 = 087f36d4e5c255e4757f191783a72d7a3818c2a9be3a90f2e3d154bb78e40eca
```

All 13 hostile cases were rejected:

```text
authorization_not_after_freeze
certificate_schema_smuggling
grounding_envelope_forge
modified_authorized_runner_bytes
realized_G_arm_identity_divergence
realized_G_envelope_mismatch
realized_G_temporal_violation
realized_future_status_forge
realized_schema_smuggling
rehashed_packet_under_old_anchor_certificate
missing_execution_member
extra_execution_member
wrong_execution_member_bytes
```

A malicious `PYTHONPATH` containing shadow modules named like the custody, grounding, materialization, and endpoint modules did not alter the valid execution; the runner uses exact packet-authorized absolute paths and Git blob checks after a stdlib-only bootstrap.

## Failed CI attempt preserved

The first external run was not hidden:

```text
FAILED_RUN_ID = 31902433823
FAILED_JOB_ID = 95055128523
CONCLUSION = failure
```

It failed before runner invocation because the audit fixture incorrectly expected a top-level `source_fact_ids` field in `FUTURE_GROUNDING_DOMAIN.json`. The frozen domain instead encodes the six facts through its three grounding-unit rows. The repair was limited to audit instrumentation (`I_CHAIN_OF_CUSTODY_ATTACK_V7B.py`); packet 7, its freeze anchor, treatment, evaluation rules, and execution root were unchanged. The second run then passed.

This preserves the corrective lineage:

```text
claim -> executable reality check -> discrepancy -> minimal fixture repair -> independent rerun -> PASS
```

## Authorization consequence

Predicate I now permits issuance of an authorization certificate over **exactly** packet 7 and its freeze anchor. It does not itself realize a future obligation or execute a real future endpoint.

After certificate issuance, the permitted pre-realization state is:

```text
AUTHORIZED_FUTURE_NOT_YET_REALIZED
```

The future may instantiate the frozen blanks; it may not rewrite the rules governing them.
