#!/usr/bin/env python3
"""Adversarial predicate-E environment audit for VFA-0.2 quotient topology.

Construction/authorization evidence only:
- no future obligation is accessed,
- G is never activated,
- DeltaPi is not evaluated.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import platform
from pathlib import Path

import E_ENVIRONMENT_KERNEL as ek

HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / "E_ENVIRONMENT_MANIFEST.json").read_text())
GA = json.loads((HERE / "GAMMA_A.json").read_text())
GB = json.loads((HERE / "GAMMA_B.json").read_text())
W = json.loads((HERE / "VALIDATED_SUBSTRATE.json").read_text())
OUT = HERE / "e_environment_audit.json"

FORBIDDEN_IMPORTS = {
    "random", "time", "threading", "multiprocessing", "asyncio",
    "subprocess", "socket", "requests",
}


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def sha256_bytes(x: bytes) -> str:
    return hashlib.sha256(x).hexdigest()


def sha256_obj(x) -> str:
    return sha256_bytes(canonical(x).encode())


def runtime_check():
    expected = MANIFEST["E_capacity"]["runtime"]
    got_impl = platform.python_implementation()
    got_version = platform.python_version()
    return {
        "pass": got_impl == expected["implementation"] and got_version == expected["version"],
        "expected": expected,
        "observed": {
            "implementation": got_impl,
            "version": got_version,
            "third_party_dependencies_used_by_kernel": [],
        },
    }


def substrate_check():
    expected = MANIFEST["E_information"]["validated_substrate_sha256"]
    got = sha256_obj(W)
    return {
        "pass": got == expected and W["arm_usage"]["A"] == "IDENTICAL_OBJECT" and W["arm_usage"]["B"] == "IDENTICAL_OBJECT",
        "expected_sha256": expected,
        "observed_sha256": got,
        "arm_usage": W["arm_usage"],
    }


def _trace_dict(trace):
    return {name: getattr(trace, name) for name in trace.__slots__}


def gamma_representation_check():
    raw_a = (HERE / "GAMMA_A.json").read_bytes()
    raw_b = (HERE / "GAMMA_B.json").read_bytes()
    ca = canonical(GA).encode()
    cb = canonical(GB).encode()
    ma, ta = ek.compile_equivalence_matrix(GA)
    mb, tb = ek.compile_equivalence_matrix(GB)
    budget = MANIFEST["E_capacity"]["compute_budget"]
    mem = MANIFEST["E_capacity"]["memory_context_storage"]
    expected_trace = {
        "path_record_reads": budget["materialization_path_records"],
        "path_sort_items": budget["materialization_path_records"],
        "class_label_lookups": budget["materialization_class_lookups"],
        "matrix_comparisons": budget["materialization_matrix_comparisons"],
        "matrix_byte_writes": budget["materialization_matrix_writes"],
        "pair_slots": budget["pair_scan_slots"],
        "output_bytes": mem["equivalence_matrix_bytes"],
    }
    trace_a = _trace_dict(ta)
    trace_b = _trace_dict(tb)
    checks = {
        "raw_bytes_equal": len(raw_a) == len(raw_b) == mem["raw_gamma_repository_bytes_each"],
        "canonical_bytes_equal": len(ca) == len(cb) == mem["canonical_gamma_bytes_each"],
        "path_records_equal": GA["path_records"] == GB["path_records"],
        "matrix_size_equal": len(ma) == len(mb) == mem["equivalence_matrix_bytes"],
        "logical_materialization_cost_equal": trace_a == trace_b == expected_trace,
        "pair_scan_slots_equal": len(ek.scan_pair_slots(ma)) == len(ek.scan_pair_slots(mb)) == budget["pair_scan_slots"],
        "treatment_matrix_differs": ma != mb,
        "matrix_alphabet_closed": set(ma) <= {0, 1} and set(mb) <= {0, 1},
    }
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "matrix_sha256_A": sha256_bytes(ma),
        "matrix_sha256_B": sha256_bytes(mb),
        "trace_A": trace_a,
        "trace_B": trace_b,
    }


def relabel_variant(gamma, shift: int, reverse_records: bool):
    x = copy.deepcopy(gamma)
    labels = sorted(set(x["equivalence_class"].values()))
    rotated = labels[shift % len(labels):] + labels[:shift % len(labels)]
    mapping = {old: f"C{idx:015d}" for idx, old in enumerate(rotated, 1)}
    x["equivalence_class"] = {p: mapping[label] for p, label in x["equivalence_class"].items()}
    if reverse_records:
        x["path_records"] = list(reversed(x["path_records"]))
    return x


def metamorphic_cost_attack():
    base_a, trace_a = ek.compile_equivalence_matrix(GA)
    base_b, trace_b = ek.compile_equivalence_matrix(GB)
    mismatches = []
    comparisons = 0
    for arm, gamma, base, base_trace in [
        ("A", GA, base_a, trace_a),
        ("B", GB, base_b, trace_b),
    ]:
        for shift in range(16):
            for reverse in (False, True):
                variant = relabel_variant(gamma, shift, reverse)
                for pressure in (0, 3, 17):
                    junk = [bytearray(1024) for _ in range(pressure)]
                    matrix, trace = ek.compile_equivalence_matrix(variant)
                    comparisons += 1
                    if matrix != base or trace != base_trace:
                        mismatches.append({
                            "arm": arm,
                            "shift": shift,
                            "reverse_records": reverse,
                            "pressure": pressure,
                        })
                    del junk
    order_runs = []
    for order in ((("A", GA), ("B", GB)), (("B", GB), ("A", GA))):
        row = []
        for arm, gamma in order:
            matrix, trace = ek.compile_equivalence_matrix(gamma)
            row.append((arm, sha256_bytes(matrix), tuple(getattr(trace, n) for n in trace.__slots__)))
        order_runs.append(row)
    order_pass = dict((arm, (m, t)) for arm, m, t in order_runs[0]) == dict((arm, (m, t)) for arm, m, t in order_runs[1])
    return {
        "pass": not mismatches and order_pass,
        "comparisons": comparisons,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:10],
        "AB_BA_order_invariance": order_pass,
    }


def information_exposure_attack():
    ma, _ = ek.compile_equivalence_matrix(GA)
    mb, _ = ek.compile_equivalence_matrix(GB)
    payloads = [
        b"",
        b"x",
        bytes(range(31)),
        b"future-common-evidence-test" * 41,
        bytes(65536),
    ]
    mismatches = []
    for payload in payloads:
        common = ek.CommonEvidence.bind(payload)
        xa = ek.arm_exposure(common, ma)
        xb = ek.arm_exposure(common, mb)
        if xa[0] != xb[0]:
            mismatches.append({"size": len(payload), "kind": "common_evidence_hash"})
        if len(xa[1]) != len(xb[1]) or set(xa[1]) - {0, 1} or set(xb[1]) - {0, 1}:
            mismatches.append({"size": len(payload), "kind": "treatment_view_shape"})
    rejection_checks = []
    for dirty in ({"payload": b"x"}, [b"x"], "x", bytearray(b"x")):
        try:
            ek.CommonEvidence.bind(dirty)
            rejection_checks.append(False)
        except TypeError:
            rejection_checks.append(True)
    try:
        ek.arm_exposure(ek.CommonEvidence.bind(b"x"), GA)
        raw_gamma_rejected = False
    except TypeError:
        raw_gamma_rejected = True
    source = Path(ek.__file__).read_text()
    raw_label_literal_absent = "A000000000" not in source and "B000000000" not in source
    return {
        "pass": not mismatches and all(rejection_checks) and raw_gamma_rejected and raw_label_literal_absent,
        "common_payload_cases": len(payloads),
        "mismatches": mismatches,
        "dirty_common_evidence_rejected": all(rejection_checks),
        "raw_gamma_at_exposure_boundary_rejected": raw_gamma_rejected,
        "raw_arm_label_literals_absent_from_kernel": raw_label_literal_absent,
        "tools": MANIFEST["E_information"]["tool_permissions"],
        "apis": MANIFEST["E_information"]["api_permissions"],
        "network_access": MANIFEST["E_information"]["network_access"],
    }


def static_execution_attack():
    source = Path(ek.__file__).read_text()
    tree = ast.parse(source)
    imported = set()
    calls = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)
    forbidden_import_hits = sorted(imported & FORBIDDEN_IMPORTS)
    forbidden_call_hits = sorted(calls & {
        "time", "perf_counter", "sleep", "seed", "random",
        "Thread", "Process", "create_task", "Popen",
    })
    execution = MANIFEST["E_execution"]
    manifest_checks = {
        "randomness_none": execution["randomness"] == "NONE",
        "single_thread": execution["concurrency"] == "NONE_SINGLE_THREAD",
        "persistent_cache_none": execution["persistent_cache"] == "NONE",
        "wall_clock_not_stop": execution["wall_clock_measurement"] == "NOT_AN_ENDPOINT_OR_STOP_RULE",
        "logical_budget_only": "logical budget" in execution["timeout_rule"].lower(),
        "paired_failure": "PAIRED" in execution["failure_rule"],
    }
    return {
        "pass": not forbidden_import_hits and not forbidden_call_hits and all(manifest_checks.values()),
        "forbidden_import_hits": forbidden_import_hits,
        "forbidden_call_hits": forbidden_call_hits,
        "manifest_checks": manifest_checks,
        "kernel_sha256": sha256_bytes(source.encode()),
    }


def capacity_manifest_attack():
    cap = MANIFEST["E_capacity"]
    budget = cap["compute_budget"]
    mem = cap["memory_context_storage"]
    checks = {
        "fixed_path_slots": mem["path_slots"] == ek.PATH_COUNT == 24,
        "fixed_matrix_bytes": mem["equivalence_matrix_bytes"] == ek.MATRIX_BYTES == 576,
        "fixed_pair_slots": mem["pair_slots"] == ek.PAIR_SLOTS == 276,
        "probe_slots_equal_pair_slots": budget["probe_generation_slots"] == ek.PAIR_SLOTS,
        "validation_slots_equal_pair_slots": budget["fresh_evidence_validation_slots"] == ek.PAIR_SLOTS,
        "no_arm_private_extra_storage": mem["arm_private_extra_storage"] == 0,
        "treatment_buffer_fixed": mem["arm_private_treatment_buffer_bytes"] == ek.MATRIX_BYTES,
        "common_evidence_cap_shared": mem["max_common_evidence_bytes"] == MANIFEST["E_information"]["future_disclosure_contract"]["max_payload_bytes"],
        "stdlib_only": cap["runtime"]["third_party_dependencies"] == [],
    }
    return {"pass": all(checks.values()), "checks": checks}


def main():
    results = {
        "runtime": runtime_check(),
        "substrate": substrate_check(),
        "capacity_manifest": capacity_manifest_attack(),
        "gamma_representation_and_cost": gamma_representation_check(),
        "metamorphic_execution_cost": metamorphic_cost_attack(),
        "information_exposure": information_exposure_attack(),
        "execution_static": static_execution_attack(),
    }
    e_capacity = all(results[k]["pass"] for k in (
        "runtime", "capacity_manifest", "gamma_representation_and_cost", "metamorphic_execution_cost"
    ))
    e_information = results["substrate"]["pass"] and results["information_exposure"]["pass"]
    e_execution = results["gamma_representation_and_cost"]["pass"] and results["metamorphic_execution_cost"]["pass"] and results["execution_static"]["pass"]
    overall = e_capacity and e_information and e_execution

    out = {
        "benchmark_id": MANIFEST["benchmark_id"],
        "audit_identity": "VFA-0.2-E-ENVIRONMENT-ATTACK-1",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "certificates": {
            "E_capacity": {"pass": e_capacity},
            "E_information": {"pass": e_information},
            "E_execution": {"pass": e_execution},
        },
        "attack_results": results,
        "E_adjudication": "PASS" if overall else "FAIL",
        "scope": {
            "cost_claim": "deterministic logical operation/resource schedule; no CPU-cycle, joule, or wall-clock equality claim",
            "future_common_cause_realization": "deferred to predicate G",
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
        "E": out["E_adjudication"],
        "E_capacity": e_capacity,
        "E_information": e_information,
        "E_execution": e_execution,
        "metamorphic_cost_comparisons": results["metamorphic_execution_cost"]["comparisons"],
        "metamorphic_cost_mismatches": results["metamorphic_execution_cost"]["mismatch_count"],
        "matrix_bytes": ek.MATRIX_BYTES,
        "pair_slots": ek.PAIR_SLOTS,
        "future_obligation_accessed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
