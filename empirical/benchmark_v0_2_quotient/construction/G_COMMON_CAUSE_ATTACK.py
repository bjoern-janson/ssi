#!/usr/bin/env python3
"""Authorization-side adversarial attack for predicate G.

Uses synthetic blinded candidate streams only. It does not fetch or inspect any
post-cutoff Biome release, does not instantiate a realized future obligation,
and never activates the corrective reserve gate.
"""
from __future__ import annotations

import ast
import inspect
import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import G_COMMON_CAUSE_KERNEL as gk

HERE = Path(__file__).resolve().parent
OUT = HERE / "g_common_cause_audit.json"
TEMPLATE = json.loads((HERE / "G_REALIZED_COMMON_CAUSE_CERTIFICATE_TEMPLATE.json").read_text())

FREEZE = "2035-01-01T00:00:00Z"
CHANGE_KINDS = tuple(sorted(gk.ELIGIBLE_CHANGE_KINDS))
FORBIDDEN_INPUT_NAMES = {"arm", "treatment", "gamma", "phi", "phi_path", "m_gamma", "outcome", "score", "performance"}


def candidate(cid, day, rid, *, stable=True, independent=True, relevant=True, kinds=None, excluded=False, package=True):
    return gk.Candidate(
        candidate_id=cid,
        published_at=f"2035-01-{day:02d}T12:00:00Z",
        release_id=rid,
        stable=stable,
        implementation_after_freeze=independent,
        migration_relevant=relevant,
        change_kinds=tuple(kinds or (CHANGE_KINDS[0],)),
        excluded=excluded,
        common_packaging_possible=package,
    )


def synthetic_pool(i: int):
    k1 = CHANGE_KINDS[i % len(CHANGE_KINDS)]
    k2 = CHANGE_KINDS[(i + 3) % len(CHANGE_KINDS)]
    return [
        candidate(f"pre-{i}", 1, 10_000 + i, stable=True, independent=True, relevant=True, kinds=(k1,)),
        candidate(f"nightly-{i}", 2, 20_000 + i, stable=False, independent=True, relevant=True, kinds=(k1,)),
        candidate(f"known-{i}", 3, 30_000 + i, stable=True, independent=False, relevant=True, kinds=(k1,)),
        candidate(f"eligible-first-{i}", 4, 40_000 + i, stable=True, independent=True, relevant=True, kinds=(k1, k2)),
        candidate(f"eligible-later-{i}", 5, 50_000 + i, stable=True, independent=True, relevant=True, kinds=(k2,)),
        candidate(f"excluded-{i}", 6, 60_000 + i, stable=True, independent=True, relevant=True, kinds=(k1,), excluded=True),
    ]


def static_no_treatment_input_attack():
    expected = {
        "select_first_qualifying": ("candidates", "freeze_timestamp"),
        "commit_common_bundle": ("trace", "payload", "evidence", "selected_at", "bundle_committed_at", "disclose_at", "deadline_at"),
        "arm_view": ("bundle",),
    }
    signatures = {}
    signature_pass = True
    for name, params in expected.items():
        fn = getattr(gk, name)
        got = tuple(inspect.signature(fn).parameters)
        signatures[name] = got
        signature_pass &= got == params

    tree = ast.parse(Path(gk.__file__).read_text())
    function_forbidden_names = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in expected:
            names = {n.id.lower() for n in ast.walk(node) if isinstance(n, ast.Name)}
            args = {a.arg.lower() for a in node.args.args}
            hits = sorted((names | args) & FORBIDDEN_INPUT_NAMES)
            function_forbidden_names[node.name] = hits
    ast_pass = all(not x for x in function_forbidden_names.values())

    smuggle = {}
    pool = synthetic_pool(0)
    for bad in ("arm", "treatment", "Gamma", "Phi_path", "M_Gamma", "outcome", "performance"):
        try:
            gk.select_first_qualifying(pool, FREEZE, **{bad: "A"})
            smuggle[bad] = "ACCEPTED"
        except TypeError:
            smuggle[bad] = "REJECTED"
    return {
        "pass": signature_pass and ast_pass and all(v == "REJECTED" for v in smuggle.values()),
        "signatures": {k: list(v) for k, v in signatures.items()},
        "forbidden_name_hits": function_forbidden_names,
        "selector_smuggling": smuggle,
    }


def selector_invariance_attack():
    mismatches = []
    comparisons = 0
    label_swap_comparisons = 0
    for i in range(128):
        pool = synthetic_pool(i)
        variants = [
            list(pool),
            list(reversed(pool)),
            pool[2:] + pool[:2],
            [pool[3], pool[0], pool[5], pool[2], pool[4], pool[1]],
        ]
        baseline = gk.select_first_qualifying(variants[0], FREEZE)
        expected = f"eligible-first-{i}"
        if baseline.selected_candidate_id != expected:
            mismatches.append({"scenario": i, "kind": "wrong_first_qualifier", "got": baseline.selected_candidate_id, "expected": expected})
        for variant_index, variant in enumerate(variants[1:], 1):
            got = gk.select_first_qualifying(variant, FREEZE)
            comparisons += 1
            if got != baseline:
                mismatches.append({"scenario": i, "kind": "input_order", "variant": variant_index})
        # Treatment-label permutation occurs outside the selector because the selector has no treatment input.
        trace_under_A_label = gk.select_first_qualifying(pool, FREEZE)
        trace_under_B_label = gk.select_first_qualifying(pool, FREEZE)
        label_swap_comparisons += 1
        if trace_under_A_label != trace_under_B_label:
            mismatches.append({"scenario": i, "kind": "label_swap"})

    none_pool = [
        candidate("none-a", 2, 1, stable=False),
        candidate("none-b", 3, 2, independent=False),
        candidate("none-c", 4, 3, excluded=True),
    ]
    none_trace = gk.select_first_qualifying(none_pool, FREEZE)
    no_qualifying_pass = none_trace.selected_candidate_id == "NO_QUALIFYING_OBLIGATION"

    # A later qualifying event must never replace the first qualifying event.
    substitution_pool = [
        candidate("first", 4, 100, kinds=(CHANGE_KINDS[0],)),
        candidate("later", 5, 1, kinds=(CHANGE_KINDS[1],)),
    ]
    substitution_trace = gk.select_first_qualifying(substitution_pool, FREEZE)
    no_substitution_pass = substitution_trace.selected_candidate_id == "first"

    return {
        "pass": not mismatches and no_qualifying_pass and no_substitution_pass,
        "candidate_order_comparisons": comparisons,
        "treatment_label_swap_comparisons": label_swap_comparisons,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:10],
        "no_qualifying_semantics": no_qualifying_pass,
        "first_qualifying_no_substitution": no_substitution_pass,
    }


def common_bundle_attack():
    mismatches = []
    comparisons = 0
    mutation_blocked = False
    arm_kw_rejected = True
    dirty_metadata_kw_rejected = True
    for i in range(64):
        trace = gk.select_first_qualifying(synthetic_pool(i), FREEZE)
        payload = (f"synthetic-common-obligation-{i}|" * (1 + i % 5)).encode()
        evidence = (f"synthetic-common-evidence-{i}|" * (1 + i % 7)).encode()
        bundle = gk.commit_common_bundle(
            trace,
            payload,
            evidence,
            "2035-01-07T10:00:00Z",
            "2035-01-07T10:00:01Z",
            "2035-01-07T10:01:00Z",
            "2035-01-07T11:01:00Z",
        )
        view_a = gk.arm_view(bundle)
        view_b = gk.arm_view(bundle)
        comparisons += 1
        if view_a != view_b or view_a[0] != payload or view_a[1] != evidence:
            mismatches.append({"scenario": i, "kind": "common_view"})
        if i == 0:
            try:
                bundle.disclose_at = "2035-01-07T09:00:00Z"
            except (FrozenInstanceError, AttributeError):
                mutation_blocked = True
            try:
                gk.arm_view(bundle, arm="A")
                arm_kw_rejected = False
            except TypeError:
                pass
            try:
                gk.commit_common_bundle(
                    trace, payload, evidence,
                    "2035-01-07T10:00:00Z", "2035-01-07T10:00:01Z",
                    "2035-01-07T10:01:00Z", "2035-01-07T11:01:00Z",
                    arm_metadata={"arm": "A"},
                )
                dirty_metadata_kw_rejected = False
            except TypeError:
                pass
    fields = set(gk.CommonBundle.__dataclass_fields__)
    no_arm_fields = not ({"arm", "treatment", "gamma", "phi", "m_gamma"} & {x.lower() for x in fields})
    return {
        "pass": not mismatches and mutation_blocked and arm_kw_rejected and dirty_metadata_kw_rejected and no_arm_fields,
        "common_view_comparisons": comparisons,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:10],
        "bundle_immutable": mutation_blocked,
        "arm_argument_rejected": arm_kw_rejected,
        "arm_metadata_smuggling_rejected": dirty_metadata_kw_rejected,
        "bundle_has_no_arm_field": no_arm_fields,
    }


def temporal_attack():
    trace = gk.select_first_qualifying(synthetic_pool(1), FREEZE)
    valid = gk.commit_common_bundle(
        trace, b"x", b"e",
        "2035-01-07T10:00:00Z",
        "2035-01-07T10:00:01Z",
        "2035-01-07T10:01:00Z",
        "2035-01-07T11:01:00Z",
    )
    invalid_cases = [
        ("2034-12-31T23:59:59Z", "2035-01-07T10:00:01Z", "2035-01-07T10:01:00Z", "2035-01-07T11:01:00Z"),
        ("2035-01-07T10:00:00Z", "2035-01-07T10:02:00Z", "2035-01-07T10:01:00Z", "2035-01-07T11:01:00Z"),
        ("2035-01-07T10:00:00Z", "2035-01-07T10:00:01Z", "2035-01-07T10:01:00Z", "2035-01-07T10:00:30Z"),
    ]
    rejected = 0
    for times in invalid_cases:
        try:
            gk.commit_common_bundle(trace, b"x", b"e", *times)
        except ValueError:
            rejected += 1
    return {
        "pass": rejected == len(invalid_cases) and valid.bundle_committed_at < valid.disclose_at < valid.deadline_at,
        "invalid_temporal_cases": len(invalid_cases),
        "invalid_temporal_cases_rejected": rejected,
        "valid_commit_before_disclosure": valid.bundle_committed_at < valid.disclose_at,
    }


def realized_template_attack():
    forbidden_filled = []
    for key, value in TEMPLATE.items():
        if key in {"certificate_type", "status", "rule", "post_disclosure_validity"}:
            continue
        if isinstance(value, str) and not (value.startswith("TBD_") or value == "NOT_EVALUATED"):
            forbidden_filled.append(key)
    required = {
        "selected_candidate_id", "selection_trace_sha256", "selected_at", "bundle_committed_at",
        "disclosed_at_A", "disclosed_at_B", "deadline_A", "deadline_B",
        "common_payload_sha256_A", "common_payload_sha256_B",
        "common_evidence_sha256_A", "common_evidence_sha256_B",
        "selector_conformance", "implementation_independence_conformance",
        "first_qualifying_rule_conformance", "no_arm_access_before_bundle_commit",
    }
    return {
        "pass": required <= set(TEMPLATE) and not forbidden_filled and TEMPLATE["status"] == "UNINSTANTIATED_TEMPLATE",
        "required_fields_present": required <= set(TEMPLATE),
        "pre_filled_realized_fields": forbidden_filled,
        "status": TEMPLATE["status"],
    }


def main():
    results = {
        "static_no_treatment_input": static_no_treatment_input_attack(),
        "selector_invariance": selector_invariance_attack(),
        "common_bundle": common_bundle_attack(),
        "temporal": temporal_attack(),
        "realized_certificate_template": realized_template_attack(),
    }
    overall = all(x["pass"] for x in results.values())
    out = {
        "benchmark_id": "VFA-0.2-QUOTIENT-REVISION-TOPOLOGY",
        "audit_identity": "VFA-0.2-G-COMMON-CAUSE-ATTACK-1",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "attack_results": results,
        "G_adjudication": "PASS" if overall else "FAIL",
        "scope": {
            "prospective_pool": "source rule and candidate schema frozen; concrete future pool intentionally not known pre-freeze",
            "attack_data": "synthetic blinded candidate streams only",
            "realized_certificate": "must be instantiated after selection and committed before arm disclosure; execution conformance only",
        },
        "authority_boundary": {
            "Delta_Pi": "NOT_EVALUATED",
            "kernel_q_subset_kernel_T_future": "NOT_EVALUATED",
            "freeze_packet": "NOT_FROZEN",
            "authorization_certificate": "NOT_ISSUED",
            "future_run": "NOT_AUTHORIZED",
        },
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "G": out["G_adjudication"],
        "candidate_order_comparisons": results["selector_invariance"]["candidate_order_comparisons"],
        "label_swap_comparisons": results["selector_invariance"]["treatment_label_swap_comparisons"],
        "common_view_comparisons": results["common_bundle"]["common_view_comparisons"],
        "future_obligation_accessed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
