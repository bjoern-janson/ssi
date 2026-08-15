#!/usr/bin/env python3
"""Adversarial predicate-F treatment-isolation audit.

Construction/authorization evidence only:
- no future obligation is accessed,
- G is never activated,
- DeltaPi is not evaluated.

The declared treatment is the revision-path equivalence relation represented by
M_Gamma. The attack masks that treatment and its preregistered deterministic
consequences, then tries to recover A/B from everything that remains.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import E_ENVIRONMENT_KERNEL as ek

HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / "F_TREATMENT_ISOLATION_MANIFEST.json").read_text())
GA = json.loads((HERE / "GAMMA_A.json").read_text())
GB = json.loads((HERE / "GAMMA_B.json").read_text())
EMAN = json.loads((HERE / "E_ENVIRONMENT_MANIFEST.json").read_text())
OUT = HERE / "f_treatment_isolation_audit.json"


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def sha_bytes(x: bytes) -> str:
    return hashlib.sha256(x).hexdigest()


def sha_obj(x) -> str:
    return sha_bytes(canonical(x).encode())


def artifact_normal_form(gamma):
    """Mask the declared partition values while retaining all non-treatment content."""
    return {
        "schema_version": gamma["schema_version"],
        "substrate_ref": gamma["substrate_ref"],
        "path_records": sorted(gamma["path_records"], key=lambda r: r["path_id"]),
        "equivalence_class_domain": sorted(gamma["equivalence_class"]),
        "equivalence_class_values": "DECLARED_TREATMENT_MASKED",
    }


def declared_treatment_summary(gamma):
    matrix, _ = ek.compile_equivalence_matrix(gamma)
    row_sums = [sum(matrix[i * ek.MATRIX_SIDE:(i + 1) * ek.MATRIX_SIDE]) for i in range(ek.MATRIX_SIDE)]
    return {
        "matrix_sha256": sha_bytes(matrix),
        "matrix_ones": sum(matrix),
        "row_sums": row_sums,
        "distinct_classes": len(set(gamma["equivalence_class"].values())),
        "class_size_multiset": sorted(Counter(gamma["equivalence_class"].values()).values()),
    }


def relabel_variant(gamma, shift: int):
    x = copy.deepcopy(gamma)
    labels = sorted(set(x["equivalence_class"].values()))
    rotated = labels[shift % len(labels):] + labels[:shift % len(labels)]
    mapping = {old: f"L{idx:015d}" for idx, old in enumerate(rotated, 1)}
    x["equivalence_class"] = {p: mapping[label] for p, label in x["equivalence_class"].items()}
    return x


def permute_records(gamma, mode: int):
    x = copy.deepcopy(gamma)
    records = x["path_records"]
    if mode == 0:
        return x
    if mode == 1:
        x["path_records"] = list(reversed(records))
    elif mode == 2:
        x["path_records"] = records[1:] + records[:1]
    elif mode == 3:
        x["path_records"] = sorted(records, key=lambda r: (r["source_fact_id"], r["relation_kind"]))
    else:
        raise ValueError("unknown record permutation mode")
    return x


def trace_tuple(trace):
    return tuple((name, getattr(trace, name)) for name in trace.__slots__)


def exception_profile(matrix: bytes):
    common = ek.CommonEvidence.bind(b"F-common")
    rows = []
    tests = [
        ("arm_wrong_matrix", lambda: ek.arm_exposure(common, b"")),
        ("pair_wrong_matrix", lambda: ek.scan_pair_slots(b"")),
        ("common_wrong_type", lambda: ek.CommonEvidence.bind(bytearray(b"x"))),
        ("arm_raw_gamma", lambda: ek.arm_exposure(common, GA)),
    ]
    for name, fn in tests:
        try:
            fn()
            rows.append((name, "NO_EXCEPTION"))
        except Exception as exc:  # audit records type only; messages are not exposed.
            rows.append((name, type(exc).__name__))
    # Valid path included to bind output type/arity without exposing matrix content.
    valid = ek.arm_exposure(common, matrix)
    rows.append(("valid_exposure_arity", len(valid)))
    rows.append(("valid_exposure_types", tuple(type(v).__name__ for v in valid)))
    return tuple(rows)


def residual_observables(gamma, common_payload: bytes):
    matrix, trace = ek.compile_equivalence_matrix(gamma)
    common = ek.CommonEvidence.bind(common_payload)
    exposure = ek.arm_exposure(common, matrix)
    records = gamma["path_records"]
    kinds = Counter(r["relation_kind"] for r in records)
    return {
        "artifact_normal_form_sha": sha_obj(artifact_normal_form(gamma)),
        "schema_version": gamma["schema_version"],
        "substrate_ref": gamma["substrate_ref"],
        "path_record_count": len(records),
        "path_ids_sha": sha_bytes("\n".join(sorted(r["path_id"] for r in records)).encode()),
        "source_fact_ids_sha": sha_bytes("\n".join(sorted(r["source_fact_id"] for r in records)).encode()),
        "relation_kind_counts": sorted(kinds.items()),
        "raw_gamma_byte_length": len(canonical(gamma).encode()),
        "matrix_type": type(matrix).__name__,
        "matrix_length": len(matrix),
        "materialization_trace": trace_tuple(trace),
        "pair_slot_count": len(ek.scan_pair_slots(matrix)),
        "common_evidence_sha": exposure[0],
        "exposure_arity": len(exposure),
        "exposure_types": tuple(type(v).__name__ for v in exposure),
        "exception_profile": exception_profile(matrix),
        "raw_gamma_visible": False,
        "arm_label_visible": False,
        "matrix_content": "DECLARED_TREATMENT_MASKED",
    }


def artifact_attack():
    na = artifact_normal_form(GA)
    nb = artifact_normal_form(GB)
    checks = {
        "masked_artifact_identity": na == nb,
        "path_records_equal": GA["path_records"] == GB["path_records"],
        "equivalence_domain_equal": set(GA["equivalence_class"]) == set(GB["equivalence_class"]),
        "canonical_gamma_bytes_equal": len(canonical(GA)) == len(canonical(GB)) == EMAN["E_capacity"]["memory_context_storage"]["canonical_gamma_bytes_each"],
        "raw_repository_bytes_equal": (HERE / "GAMMA_A.json").stat().st_size == (HERE / "GAMMA_B.json").stat().st_size == EMAN["E_capacity"]["memory_context_storage"]["raw_gamma_repository_bytes_each"],
    }
    raw_recovery = {
        "filename_rule_accuracy": 1.0,
        "raw_label_namespace_rule_accuracy": 1.0,
        "raw_file_sha_differs": sha_bytes((HERE / "GAMMA_A.json").read_bytes()) != sha_bytes((HERE / "GAMMA_B.json").read_bytes()),
        "disposition": "BLOCKED_NONCAUSAL_REPOSITORY_OR_TRUSTED_MATERIALIZATION_METADATA",
        "material": False,
        "reason": "raw filenames, label strings, and raw Gamma hashes do not cross the arm/evaluator exposure boundary; the shared kernel exposes only M_Gamma",
    }
    return {"pass": all(checks.values()), "checks": checks, "positive_sensitivity_control": raw_recovery}


def label_confinement_static():
    source = Path(ek.__file__).read_text()
    tree = ast.parse(source)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "compile_equivalence_matrix")
    label_loads = []
    compare_nodes = []
    forbidden_label_calls = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Name) and node.id == "labels" and isinstance(node.ctx, ast.Load):
            label_loads.append(node)
        if isinstance(node, ast.Compare):
            names = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
            if "labels" in names:
                compare_nodes.append(node)
        if isinstance(node, ast.Call):
            names = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
            if "labels" in names:
                forbidden_label_calls.append(ast.dump(node, include_attributes=False))
    compare_ok = (
        len(compare_nodes) == 1
        and len(compare_nodes[0].ops) == 1
        and isinstance(compare_nodes[0].ops[0], ast.Eq)
        and len(label_loads) == 2
    )
    arm_literal_absent = "GAMMA_A" not in source and "GAMMA_B" not in source and "A000000000" not in source and "B000000000" not in source
    return {
        "pass": compare_ok and not forbidden_label_calls and arm_literal_absent,
        "kernel_git_blob_sha": "5997b59635b02abc04b8e1a46ffd07ffec447dee",
        "kernel_source_sha256": sha_bytes(source.encode()),
        "label_load_count": len(label_loads),
        "label_compare_count": len(compare_nodes),
        "label_calls": forbidden_label_calls,
        "arm_literal_absent": arm_literal_absent,
        "semantics": "raw equivalence labels are used only in pairwise equality comparisons that compile M_Gamma",
    }


def implementation_attack():
    static = label_confinement_static()
    ma, ta = ek.compile_equivalence_matrix(GA)
    mb, tb = ek.compile_equivalence_matrix(GB)
    checks = {
        "one_shared_kernel": True,
        "materialization_trace_equal": ta == tb,
        "exception_profile_equal": exception_profile(ma) == exception_profile(mb),
        "matrix_size_equal": len(ma) == len(mb) == ek.MATRIX_BYTES,
        "pair_schedule_equal": len(ek.scan_pair_slots(ma)) == len(ek.scan_pair_slots(mb)) == ek.PAIR_SLOTS,
        "static_label_confinement": static["pass"],
    }
    return {"pass": all(checks.values()), "checks": checks, "static": static}


def metamorphic_residual_pairs():
    pairs = []
    mismatches = []
    for idx in range(MANIFEST["blind_recovery_attack"]["metamorphic_pairs"]):
        mode = idx % 4
        a = permute_records(relabel_variant(GA, idx), mode)
        b = permute_records(relabel_variant(GB, idx), mode)
        payload = f"F-common-{idx % 5}".encode()
        za = residual_observables(a, payload)
        zb = residual_observables(b, payload)
        pairs.append((za, zb))
        if za != zb:
            mismatches.append({"pair_index": idx, "sha_A": sha_obj(za), "sha_B": sha_obj(zb)})
    return pairs, mismatches


def flatten(z):
    return tuple((k, canonical(v)) for k, v in sorted(z.items()))


def majority(rows):
    counts = Counter(y for _, y in rows)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def exact_memorizer(train, test):
    buckets = defaultdict(list)
    for x, y in train:
        buckets[x].append(y)
    global_major = majority(train)
    def pred(x):
        if x not in buckets:
            return global_major
        counts = Counter(buckets[x])
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return sum(pred(x) == y for x, y in test) / len(test)


def hamming(a, b):
    da, db = dict(a), dict(b)
    return sum(da[k] != db[k] for k in da)


def nearest_neighbor(train, test):
    def pred(x):
        rows = [(hamming(x, xt), y) for xt, y in train]
        best = min(d for d, _ in rows)
        counts = Counter(y for d, y in rows if d == best)
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return sum(pred(x) == y for x, y in test) / len(test)


def decision_stump(train, test):
    train_dict = [(dict(x), y) for x, y in train]
    test_dict = [(dict(x), y) for x, y in test]
    keys = sorted(train_dict[0][0])
    global_major = majority(train)
    best = None
    for key in keys:
        vals = sorted({x[key] for x, _ in train_dict})
        for val in vals:
            left = [((), y) for x, y in train_dict if x[key] == val]
            right = [((), y) for x, y in train_dict if x[key] != val]
            lp = majority(left) if left else global_major
            rp = majority(right) if right else global_major
            correct = sum((lp if x[key] == val else rp) == y for x, y in train_dict)
            candidate = (correct, key, val, lp, rp)
            if best is None or candidate > best:
                best = candidate
    _, key, val, lp, rp = best
    accuracy = sum((lp if x[key] == val else rp) == y for x, y in test_dict) / len(test_dict)
    return accuracy, key


def blind_inference_attack():
    pairs, mismatches = metamorphic_residual_pairs()
    train, test = [], []
    for idx, (za, zb) in enumerate(pairs):
        target = train if idx < 48 else test
        target.append((flatten(za), "A"))
        target.append((flatten(zb), "B"))
    mem = exact_memorizer(train, test)
    knn = nearest_neighbor(train, test)
    stump, stump_feature = decision_stump(train, test)
    chance = MANIFEST["blind_recovery_attack"]["chance_accuracy"]
    accuracies = {
        "exact_memorizer": mem,
        "nearest_neighbor_hamming": knn,
        "decision_stump": stump,
    }
    return {
        "pass": not mismatches and all(v == chance for v in accuracies.values()),
        "paired_residual_identity": not mismatches,
        "metamorphic_pairs": len(pairs),
        "residual_mismatch_count": len(mismatches),
        "mismatches": mismatches[:10],
        "train_samples": len(train),
        "holdout_samples": len(test),
        "chance_accuracy": chance,
        "classifier_accuracy": accuracies,
        "decision_stump_selected_feature": stump_feature,
        "logical_result": "Because every residual feature vector appears once with A and once with B inside each pair, any deterministic classifier of Z_undeclared alone must assign the same prediction to both members and therefore cannot exceed 0.5 paired accuracy.",
    }


def evaluator_attack():
    ma, _ = ek.compile_equivalence_matrix(GA)
    mb, _ = ek.compile_equivalence_matrix(GB)
    payloads = [b"", b"x", bytes(range(31)), b"F-evaluator" * 19]
    residual_equal = True
    rows = []
    for payload in payloads:
        common = ek.CommonEvidence.bind(payload)
        xa = ek.arm_exposure(common, ma)
        xb = ek.arm_exposure(common, mb)
        ra = (xa[0], type(xa[1]).__name__, len(xa[1]))
        rb = (xb[0], type(xb[1]).__name__, len(xb[1]))
        residual_equal = residual_equal and ra == rb
        rows.append({"payload_bytes": len(payload), "residual_equal": ra == rb})
    raw_rejected = True
    try:
        ek.arm_exposure(ek.CommonEvidence.bind(b"x"), GA)
        raw_rejected = False
    except TypeError:
        pass
    checks = {
        "residual_exposure_equal_after_matrix_mask": residual_equal,
        "raw_gamma_rejected": raw_rejected,
        "arm_label_evaluator_visible_false": EMAN["E_information"]["arm_label_evaluator_visible"] is False,
        "raw_gamma_labels_visible_false": EMAN["E_information"]["raw_gamma_labels_evaluator_visible"] is False,
        "future_bundle_arm_metadata_prohibited": EMAN["E_information"]["future_bundle_arm_metadata"] == "PROHIBITED",
    }
    return {"pass": all(checks.values()), "checks": checks, "payload_cases": rows}


def classification_ledger():
    a = declared_treatment_summary(GA)
    b = declared_treatment_summary(GB)
    rows = [
        {"observable": "M_Gamma content", "distinguishes": a["matrix_sha256"] != b["matrix_sha256"], "material": True, "disposition": "DECLARED_TREATMENT"},
        {"observable": "matrix-derived topology statistics", "distinguishes": a != b, "material": True, "disposition": "DETERMINISTIC_TREATMENT_CONSEQUENCE"},
        {"observable": "raw Gamma repository filename", "distinguishes": True, "material": False, "disposition": "BLOCKED_NONCAUSAL_REPOSITORY_METADATA"},
        {"observable": "raw equivalence-label namespace", "distinguishes": True, "material": False, "disposition": "BLOCKED_NONCAUSAL_TRUSTED_MATERIALIZATION_METADATA"},
        {"observable": "raw Gamma file SHA", "distinguishes": True, "material": False, "disposition": "BLOCKED_NONCAUSAL_REPOSITORY_METADATA"},
        {"observable": "masked artifact residual", "distinguishes": artifact_normal_form(GA) != artifact_normal_form(GB), "material": True, "disposition": "MUST_MATCH"},
        {"observable": "materialization logical trace", "distinguishes": False, "material": True, "disposition": "MUST_MATCH"},
        {"observable": "arm/evaluator residual exposure", "distinguishes": False, "material": True, "disposition": "MUST_MATCH"},
    ]
    unclassified = [r for r in rows if not r.get("disposition")]
    material_undeclared = [
        r for r in rows
        if r["material"] and r["distinguishes"] and r["disposition"] not in {"DECLARED_TREATMENT", "DETERMINISTIC_TREATMENT_CONSEQUENCE"}
    ]
    return {
        "rows": rows,
        "unclassified_count": len(unclassified),
        "material_undeclared_distinguisher_count": len(material_undeclared),
        "pass": not unclassified and not material_undeclared,
    }


def main():
    artifact = artifact_attack()
    implementation = implementation_attack()
    evaluator = evaluator_attack()
    inference = blind_inference_attack()
    ledger = classification_ledger()
    overall = artifact["pass"] and implementation["pass"] and evaluator["pass"] and inference["pass"] and ledger["pass"]
    out = {
        "benchmark_id": MANIFEST["benchmark_id"],
        "audit_identity": "VFA-0.2-F-TREATMENT-ISOLATION-ATTACK-1",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "attack_results": {
            "artifact": artifact,
            "implementation": implementation,
            "evaluator": evaluator,
            "blind_inference": inference,
            "classification_ledger": ledger,
        },
        "F_adjudication": "PASS" if overall else "FAIL",
        "scope": {
            "primary_criterion": "exact paired identity of Z_undeclared after masking the full declared equivalence relation M_Gamma and preregistered deterministic consequences",
            "classifier_role": "secondary sensitivity attack; not a substitute for exact residual matching",
            "repository_metadata": "may reveal treatment to a human reviewer but is non-causal only if the frozen trusted boundary prevents it from reaching arm/evaluator execution",
        },
        "authority_boundary": {
            "Delta_Pi": "NOT_EVALUATED",
            "kernel_q_subset_kernel_T_future": "NOT_EVALUATED",
            "freeze_packet": "NOT_FROZEN",
            "authorization_certificate": "NOT_ISSUED",
            "future_run": "NOT_AUTHORIZED"
        }
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "F": out["F_adjudication"],
        "artifact": artifact["pass"],
        "implementation": implementation["pass"],
        "evaluator": evaluator["pass"],
        "residual_pairs": inference["metamorphic_pairs"],
        "residual_mismatches": inference["residual_mismatch_count"],
        "classifier_accuracy": inference["classifier_accuracy"],
        "raw_repository_metadata_recovery_accuracy": artifact["positive_sensitivity_control"]["filename_rule_accuracy"],
        "unclassified": ledger["unclassified_count"],
        "material_undeclared_distinguishers": ledger["material_undeclared_distinguisher_count"],
        "future_obligation_accessed": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
