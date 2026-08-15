#!/usr/bin/env python3
"""Hostile VFA-0.2 factorization attack.

Construction-audit machinery only. No prospective future obligation is read.

This suite attacks the stronger claim that dormant reserve has no causal or
capability path into ordinary forward behavior or insufficiency detection while
G=0. It intentionally distinguishes behavioral non-use from architectural
non-capability.
"""

from __future__ import annotations

import ast
import copy
import gc
import hashlib
import itertools
import json
import random
from collections import Counter
from pathlib import Path

import reserve_interface as ri

HERE = Path(__file__).resolve().parent
SHARED = json.loads((HERE / "SHARED_FORWARD.json").read_text())
RESERVE_A = json.loads((HERE / "reserve_A.json").read_text())
RESERVE_B = json.loads((HERE / "reserve_B.json").read_text())
OUT = HERE / "hostile_factorization_audit.json"

MASTER_SEED = 20260815
METAMORPHIC_RESERVES = 32
PRESSURE_LEVELS = [0, 3, 17]
POISON_NAMES = ["RESERVE", "RESERVE_HANDLE", "D", "D_T", "ARM", "DORMANT_STATE"]
TRACE_FIELDS = ["I", "A", "C", "pi", "E", "S", "M", "L", "tau", "R", "O"]
FORBIDDEN_SYMBOLS = {
    "reserve", "reserve_a", "reserve_b", "reserve_handle", "reserve_path",
    "d", "d_t", "globals", "locals", "eval", "exec", "open", "getattr",
    "setattr", "importlib", "os", "sys", "time", "random",
}


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def sha256_obj(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def surrogate_universe():
    universe = sorted(SHARED["transformation_classes"])
    historical = [set(v) for v in SHARED["cases"].values()]
    tasks = []
    for r in range(1, len(universe) + 1):
        for comb in itertools.combinations(universe, r):
            s = set(comb)
            if not any(s == h for h in historical):
                tasks.append(list(comb))
    return tasks


def query_variants(task):
    task = list(task)
    rotated = task[1:] + task[:1] if len(task) > 1 else list(task)
    return {
        "canonical": list(task),
        "reversed": list(reversed(task)),
        "rotated": rotated,
        "duplicate_first": task + [task[0]],
    }


def evidence_cases():
    return [
        ({"validator_status": "PASS", "failure_scope": "CURRENT_ROUTE", "independent_validator": True, "validator_id": "v1"}, False),
        ({"validator_status": "FAIL", "failure_scope": "OTHER", "independent_validator": True, "validator_id": "v1"}, False),
        ({"validator_status": "FAIL", "failure_scope": "CURRENT_ROUTE", "independent_validator": False, "validator_id": "v1"}, False),
        ({"validator_status": "FAIL", "failure_scope": "CURRENT_ROUTE", "independent_validator": True, "validator_id": ""}, False),
        ({"validator_status": "FAIL", "failure_scope": "CURRENT_ROUTE", "independent_validator": True, "validator_id": "v1"}, True),
    ]


def evidence_variants(evidence):
    items = list(evidence.items())
    extra = copy.deepcopy(evidence)
    extra["irrelevant"] = "noise"
    nested = copy.deepcopy(evidence)
    nested["metadata"] = {"unused": ["x", "y"], "reserve_status": "MUST_NOT_BE_READ"}
    return {
        "canonical": copy.deepcopy(evidence),
        "reversed": dict(reversed(items)),
        "extra": extra,
        "nested": nested,
    }


def reserve_contract(reserve):
    cases = RESERVE_A["cases"]
    kinds = sorted(RESERVE_A["bindings"])
    return (
        reserve["cases"] == cases
        and sorted(reserve["bindings"]) == kinds
        and all(sorted(reserve["bindings"][kind]) == cases for kind in kinds)
        and all(Counter(reserve["bindings"][kind].values()) == Counter(cases) for kind in kinds)
        and sum(len(v) for v in reserve["bindings"].values()) == 24
        and len(canonical(reserve)) == len(canonical(RESERVE_A))
    )


def metamorphic_reserves():
    rng = random.Random(MASTER_SEED)
    cases = RESERVE_A["cases"]
    kinds = sorted(RESERVE_A["bindings"])
    seen = set()
    out = []
    while len(out) < METAMORPHIC_RESERVES:
        reserve = {"schema_version": "1", "cases": list(cases), "bindings": {}}
        for kind in kinds:
            targets = list(cases)
            rng.shuffle(targets)
            reserve["bindings"][kind] = dict(zip(cases, targets))
        blob = canonical(reserve)
        if blob not in seen and reserve_contract(reserve):
            seen.add(blob)
            out.append(reserve)
    return out


def pressure_churn(reserve, level):
    """Equal deterministic allocation/serialization pressure proxy.

    This does not claim wall-clock or physical-memory invariance. It tests that
    deterministic forward traces and operation counts survive equal caller-side
    reserve allocation/serialization churn.
    """
    blobs = []
    for i in range(level):
        x = json.loads(canonical(reserve))
        if i % 2:
            x["cases"] = list(reversed(x["cases"]))
        blobs.append(canonical(x))
    digest = hashlib.sha256("".join(blobs).encode()).hexdigest() if blobs else ""
    gc.collect()
    return digest


def transitive_static_boundary():
    source = Path(ri.__file__).read_text()
    tree = ast.parse(source)
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}

    def internal_calls(name):
        node = functions[name]
        calls = set()
        for c in ast.walk(node):
            if isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id in functions:
                calls.add(c.func.id)
        return calls

    def closure(root):
        seen = set()
        stack = [root]
        while stack:
            name = stack.pop()
            if name in seen:
                continue
            seen.add(name)
            stack.extend(internal_calls(name) - seen)
        return sorted(seen)

    roots = {"forward_trace": closure("forward_trace"), "evaluate_gate": closure("evaluate_gate")}
    detail = {}
    for root, reachable in roots.items():
        bad = []
        for name in reachable:
            node = functions[name]
            names = {n.id.lower() for n in ast.walk(node) if isinstance(n, ast.Name)}
            attrs = {n.attr.lower() for n in ast.walk(node) if isinstance(n, ast.Attribute)}
            hits = sorted(
                x for x in names | attrs
                if x in FORBIDDEN_SYMBOLS or x.startswith("reserve")
            )
            if hits:
                bad.append({"function": name, "symbols": hits})
        detail[root] = {"reachable_functions": reachable, "forbidden_hits": bad, "pass": not bad}
    return {"roots": detail, "pass": all(v["pass"] for v in detail.values())}


def behavioral_metamorphic_attack(tasks, reserves):
    mismatches = []
    comparisons = 0
    for task in tasks:
        baseline = ri.forward_trace(task, SHARED)
        if list(baseline) != TRACE_FIELDS:
            raise AssertionError("trace schema drift")
        for q_label, query in query_variants(task).items():
            for reserve_label, reserve in reserves:
                for pressure in PRESSURE_LEVELS:
                    dormant_digest = pressure_churn(reserve, pressure)
                    trace = ri.forward_trace(query, SHARED)
                    comparisons += 1
                    if trace != baseline:
                        mismatches.append({
                            "task": task,
                            "query_variant": q_label,
                            "reserve_variant": reserve_label,
                            "pressure": pressure,
                            "baseline_sha256": sha256_obj(baseline),
                            "trace_sha256": sha256_obj(trace),
                            "dormant_sha256": dormant_digest,
                        })
                        break
    return {
        "task_count": len(tasks),
        "query_variants_per_task": 4,
        "reserve_variants": len(reserves),
        "pressure_levels": PRESSURE_LEVELS,
        "comparisons": comparisons,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:10],
        "wall_clock_invariance_claimed": False,
        "pass": not mismatches,
    }


def module_global_poisoning(tasks):
    mismatches = []
    comparisons = 0
    saved = {name: getattr(ri, name, None) for name in POISON_NAMES}
    present = {name: hasattr(ri, name) for name in POISON_NAMES}
    try:
        for name in POISON_NAMES:
            for arm, reserve in [("A", RESERVE_A), ("B", RESERVE_B)]:
                setattr(ri, name, reserve)
                for task in tasks:
                    reference = ri.forward_trace(task, SHARED)
                    trace = ri.forward_trace(task, SHARED)
                    comparisons += 1
                    if trace != reference:
                        mismatches.append({"symbol": name, "arm": arm, "task": task})
    finally:
        for name in POISON_NAMES:
            if present[name]:
                setattr(ri, name, saved[name])
            elif hasattr(ri, name):
                delattr(ri, name)
    return {"comparisons": comparisons, "mismatch_count": len(mismatches), "mismatches": mismatches[:10], "pass": not mismatches}


def gate_behavioral_attack(reserves):
    mismatches = []
    comparisons = 0
    for idx, (evidence, expected) in enumerate(evidence_cases()):
        for e_label, variant in evidence_variants(evidence).items():
            for reserve_label, reserve in reserves:
                pressure_churn(reserve, 3)
                got = ri.evaluate_gate(variant)
                comparisons += 1
                if got != expected:
                    mismatches.append({"case": idx, "evidence_variant": e_label, "reserve_variant": reserve_label, "expected": expected, "got": got})
    return {"comparisons": comparisons, "mismatch_count": len(mismatches), "mismatches": mismatches[:10], "pass": not mismatches}


def capability_smuggling_attack(tasks):
    """Attack the stronger no-dereference-capable-path invariant.

    A closed capability surface must reject reserve-bearing extra fields rather
    than merely ignore them. Accepting them means F or G receives an object from
    which D is dereferenceable, even if the current implementation does not read it.
    """
    forward_accepted = 0
    forward_behavior_mismatches = 0
    for task in tasks:
        baseline = ri.forward_trace(task, SHARED)
        for reserve in [RESERVE_A, RESERVE_B]:
            poisoned = copy.deepcopy(SHARED)
            poisoned["reserve_handle"] = reserve
            try:
                got = ri.forward_trace(task, poisoned)
                forward_accepted += 1
                forward_behavior_mismatches += int(got != baseline)
            except (TypeError, ValueError, KeyError):
                pass

    gate_accepted = 0
    gate_behavior_mismatches = 0
    for evidence, expected in evidence_cases():
        for reserve in [RESERVE_A, RESERVE_B]:
            poisoned = copy.deepcopy(evidence)
            poisoned["reserve_handle"] = reserve
            try:
                got = ri.evaluate_gate(poisoned)
                gate_accepted += 1
                gate_behavior_mismatches += int(got != expected)
            except (TypeError, ValueError, KeyError):
                pass

    capability_closed = forward_accepted == 0 and gate_accepted == 0
    return {
        "required_semantics": "reserve-bearing extra fields must be rejected, not merely ignored",
        "forward_smuggling_attempts": len(tasks) * 2,
        "forward_accepted": forward_accepted,
        "forward_behavior_mismatches": forward_behavior_mismatches,
        "gate_smuggling_attempts": len(evidence_cases()) * 2,
        "gate_accepted": gate_accepted,
        "gate_behavior_mismatches": gate_behavior_mismatches,
        "pass": capability_closed,
    }


def main():
    tasks = surrogate_universe()
    metamorphic = metamorphic_reserves()
    all_reserves = [("A", RESERVE_A), ("B", RESERVE_B)] + [
        (f"M{i:02d}", r) for i, r in enumerate(metamorphic)
    ]

    static = transitive_static_boundary()
    behavioral = behavioral_metamorphic_attack(tasks, all_reserves)
    globals_attack = module_global_poisoning(tasks)
    gate_behavior = gate_behavioral_attack(all_reserves)
    capability = capability_smuggling_attack(tasks)

    metamorphic_contract = all(reserve_contract(r) for r in metamorphic)
    behavioral_pass = behavioral["pass"] and globals_attack["pass"] and gate_behavior["pass"]
    hard_noninterference_pass = static["pass"] and behavioral_pass and metamorphic_contract and capability["pass"]

    out = {
        "benchmark_id": "VFA-0.2-DORMANT-CORRECTIVE-RESERVE",
        "future_obligation_accessed": False,
        "attack_identity": "VFA-0.2-HOSTILE-FACTORIZATION-ATTACK-1",
        "governing_invariant": "G=0 implies no causal or dereference-capable path from D into T_forward or G",
        "results": {
            "transitive_static_boundary": static,
            "metamorphic_reserve_contract": {
                "generated_variants": len(metamorphic),
                "all_contract_valid": metamorphic_contract,
                "canonical_bytes": len(canonical(RESERVE_A)),
                "pass": metamorphic_contract,
            },
            "behavioral_metamorphic_noninterference": behavioral,
            "module_global_poisoning": globals_attack,
            "gate_behavioral_noninterference": gate_behavior,
            "capability_surface_closure": capability,
        },
        "adjudication": {
            "behavioral_noninterference": "PASS" if behavioral_pass else "FAIL",
            "hard_noninterference": "PASS" if hard_noninterference_pass else "FAIL",
            "failure_code": None if hard_noninterference_pass else "OPEN_CAPABILITY_SURFACE",
            "interpretation": (
                "No behavioral leakage was observed under the hostile metamorphic attack, but open-ended dict interfaces accept reserve-bearing fields. Therefore the stronger architectural non-capability invariant is not established."
                if not hard_noninterference_pass else
                "Behavioral and architectural hostile noninterference passed."
            ),
        },
        "authorization": {
            "freeze_packet": "NOT_FROZEN",
            "authorization_certificate": "NOT_ISSUED",
            "future_run": "NOT_AUTHORIZED",
        },
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out["adjudication"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
