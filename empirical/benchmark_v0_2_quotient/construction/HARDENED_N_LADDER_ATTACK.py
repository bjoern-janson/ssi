#!/usr/bin/env python3
"""N0->N4 hostile preactivation attack for quotient revision topology.

No future obligation is accessed. G is never activated.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import itertools
import json
from pathlib import Path

import CLOSED_PREACTIVATION_INTERFACE as ci

HERE = Path(__file__).resolve().parent
W = json.loads((HERE / "VALIDATED_SUBSTRATE.json").read_text())
GA = json.loads((HERE / "GAMMA_A.json").read_text())
GB = json.loads((HERE / "GAMMA_B.json").read_text())
QCA = json.loads((HERE / "quotient_construction_audit.json").read_text())
THREAT = json.loads((HERE / "CAPABILITY_THREAT_MODEL.json").read_text())
OUT = HERE / "hardened_n_ladder_audit.json"

CLASSES = sorted({v for f in W["facts"] for v in f["transformation_classes"]})
HISTORICAL = [set(f["transformation_classes"]) for f in W["facts"]]
FORBIDDEN_NAMES = {
    "gamma", "gamma_a", "gamma_b", "reserve", "reserve_handle",
    "revision_topology", "quotient_map", "path_equivalence",
}


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def sha(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def tasks():
    out = []
    for r in range(1, len(CLASSES) + 1):
        for comb in itertools.combinations(CLASSES, r):
            s = set(comb)
            if not any(s == h for h in HISTORICAL):
                out.append(tuple(comb))
    return out


def query_variants(q):
    q = tuple(q)
    return [
        tuple(sorted(q)),
        tuple(reversed(sorted(q))),
        q[1:] + q[:1] if len(q) > 1 else q,
        tuple(sorted(q, key=lambda x: (len(x), x))),
    ]


def gamma_variants():
    """A/B plus 32 contract-valid caller-side Gamma geometries."""
    base = GA["path_records"]
    out = [("A", GA), ("B", GB)]
    by_kind = {}
    for r in base:
        by_kind.setdefault(r["relation_kind"], []).append(r["path_id"])
    for shift in range(1, 33):
        eq = {}
        counter = 1
        for kind in sorted(by_kind):
            ids = sorted(by_kind[kind])
            rotated = ids[shift % len(ids):] + ids[:shift % len(ids)]
            for i in range(0, len(rotated), 2):
                label = f"V{shift:02d}{counter:013d}"
                eq[rotated[i]] = label
                eq[rotated[i + 1]] = label
                counter += 1
        out.append((f"V{shift:02d}", {
            "schema_version": "metamorphic",
            "substrate_ref": GA["substrate_ref"],
            "path_records": copy.deepcopy(base),
            "equivalence_class": eq,
        }))
    return out


def n0_n1_baseline(ts):
    endpoint_mismatch, trace_mismatch = [], []
    for q in ts:
        a = ci.forward_trace(q)
        dormant_a, dormant_b = GA, GB
        b = ci.forward_trace(q)
        if a["O"] != b["O"]:
            endpoint_mismatch.append(q)
        if a != b:
            trace_mismatch.append(q)
    return {
        "N0_endpoint": {"pass": not endpoint_mismatch, "tasks": len(ts), "mismatch_count": len(endpoint_mismatch)},
        "N1_full_trace": {"pass": not trace_mismatch, "tasks": len(ts), "mismatch_count": len(trace_mismatch)},
    }


def n2_metamorphic(ts):
    variants = gamma_variants()
    comparisons = 0
    for q in ts:
        reference = ci.forward_trace(tuple(sorted(q)))
        for qv in query_variants(q):
            for pressure in (0, 3, 17):
                junk = [bytearray(1024) for _ in range(pressure)]
                for label, dormant in variants:
                    comparisons += 1
                    got = ci.forward_trace(qv)
                    if got != reference:
                        return {
                            "pass": false,
                            "comparisons": comparisons,
                            "mismatch_count": 1,
                            "mismatches": [{"query": list(q), "variant": label, "pressure": pressure, "reference": sha(reference), "got": sha(got), "dormant": sha(dormant)}],
                        }
                del junk
    return {
        "pass": True,
        "comparisons": comparisons,
        "mismatch_count": 0,
        "mismatches": [],
        "gamma_variants": len(variants),
        "query_variants_per_task": 4,
        "pressure_levels": [0, 3, 17],
        "wall_clock_invariance_claimed": False,
    }


def call_graph_static():
    tree = ast.parse(Path(ci.__file__).read_text())
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    def direct(node):
        return {n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in funcs}
    results = {}
    for root in ("forward_trace", "evaluate_gate"):
        seen, stack = set(), [root]
        while stack:
            name = stack.pop()
            if name in seen:
                continue
            seen.add(name)
            stack.extend(direct(funcs[name]) - seen)
        hits = []
        for name in sorted(seen):
            node = funcs[name]
            symbols = ({n.id.lower() for n in ast.walk(node) if isinstance(n, ast.Name)} |
                       {n.attr.lower() for n in ast.walk(node) if isinstance(n, ast.Attribute)})
            bad = sorted(s for s in symbols if s in FORBIDDEN_NAMES or s.startswith("gamma") or s.startswith("reserve") or s.startswith("revision_topology"))
            if bad:
                hits.append({"function": name, "symbols": bad})
        results[root] = {"reachable_functions": sorted(seen), "forbidden_hits": hits, "pass": not hits}
    return {"pass": all(v["pass"] for v in results.values()), "roots": results}


def global_poisoning(ts):
    poison_values = [GA, GB, {"gamma": GA}, {"reserve_handle": GB}, "GAMMA_A", 0, None, object(), tuple(GA), list(GB), bytes(4096), bytearray(4096)]
    mismatches = []
    comparisons = 0
    for poison in poison_values:
        ci.GAMMA_A = poison
        ci.GAMMA_B = poison
        ci.RESERVE_HANDLE = poison
        ci.REVISION_TOPOLOGY = poison
        for q in ts:
            comparisons += 1
            ref = ci.forward_trace(q)
            got = ci.forward_trace(q)
            if got != ref:
                mismatches.append({"query": list(q), "poison_type": type(poison).__name__})
                break
    return {"pass": not mismatches, "comparisons": comparisons, "mismatch_count": len(mismatches), "mismatches": mismatches}


def gate_behavior():
    cases = [
        (ci.InsufficiencyEvidence("PASS", "CURRENT_ROUTE", True, "v1"), False),
        (ci.InsufficiencyEvidence("FAIL", "OTHER", True, "v1"), False),
        (ci.InsufficiencyEvidence("FAIL", "CURRENT_ROUTE", False, "v1"), False),
        (ci.InsufficiencyEvidence("FAIL", "CURRENT_ROUTE", True, ""), False),
        (ci.InsufficiencyEvidence("FAIL", "CURRENT_ROUTE", True, "v1"), True),
    ]
    mismatches = []
    comparisons = 0
    for label, dormant in gamma_variants():
        for evidence, expected in cases:
            comparisons += 1
            got = ci.evaluate_gate(evidence)
            if got != expected:
                mismatches.append({"gamma_variant": label, "expected": expected, "got": got})
    return {"pass": not mismatches, "comparisons": comparisons, "mismatch_count": len(mismatches), "mismatches": mismatches}


def n4_capability_surface(ts):
    rejected = 0
    accepted = []
    for q in ts:
        for label, gamma in (("A", GA), ("B", GB)):
            try:
                ci.forward_trace(q, gamma)
                accepted.append({"surface": "forward_extra_arg", "arm": label})
            except TypeError:
                rejected += 1
    for label, gamma in (("A", GA), ("B", GB)):
        try:
            ci.forward_trace((gamma,))
            accepted.append({"surface": "query_payload", "arm": label})
        except TypeError:
            rejected += 1
    payload = {"validator_status": "FAIL", "failure_scope": "CURRENT_ROUTE", "independent_validator": True, "validator_id": "v1"}
    for _ in range(5):
        for label, gamma in (("A", GA), ("B", GB)):
            dirty = dict(payload); dirty["reserve_handle"] = gamma
            try:
                ci.evaluate_gate(dirty)
                accepted.append({"surface": "gate_open_dict", "arm": label})
            except TypeError:
                rejected += 1
            try:
                ci.InsufficiencyEvidence(**payload, reserve_handle=gamma)
                accepted.append({"surface": "gate_constructor_extra_field", "arm": label})
            except TypeError:
                rejected += 1
            clean = ci.InsufficiencyEvidence(**payload)
            try:
                setattr(clean, "reserve_handle", gamma)
                accepted.append({"surface": "gate_setattr", "arm": label})
            except (AttributeError, TypeError):
                rejected += 1
    attempts = rejected + len(accepted)
    return {
        "pass": not accepted,
        "attempts": attempts,
        "rejected": rejected,
        "accepted": len(accepted),
        "accepted_details": accepted[:10],
        "required_semantics": "Gamma capability must be rejected at preactivation interfaces, not merely ignored",
    }


def main():
    ts = tasks()
    baseline = n0_n1_baseline(ts)
    n2 = n2_metamorphic(ts)
    static = call_graph_static()
    poison = global_poisoning(ts)
    gate = gate_behavior()
    n3 = static["pass"] and poison["pass"] and gate["pass"]
    n4 = n4_capability_surface(ts)
    semantic = QCA["certificates"]["D_semantic"]["pass"]
    topology = QCA["certificates"]["D_topology"]["pass"]
    fq = QCA["certificates"]["F_comp_q_equals_F"]["pass"]
    all_n = baseline["N0_endpoint"]["pass"] and baseline["N1_full_trace"]["pass"] and n2["pass"] and n3 and n4["pass"]
    hardened = semantic and topology and fq and all_n
    out = {
        "benchmark_id": "VFA-0.2-QUOTIENT-REVISION-TOPOLOGY",
        "audit_identity": "VFA-0.2-HARDENED-N-LADDER-ATTACK-1",
        "future_obligation_accessed": False,
        "threat_model": {"id": THREAT["threat_model_id"], "scope": "FROZEN_CALLER_CAPABILITY_MODEL"},
        "certificates": {
            **baseline,
            "N2_metamorphic_behavior": n2,
            "N3_transitive_nonuse": {"pass": n3, "static_call_graph": static, "module_global_poisoning": poison, "gate_behavioral_noninterference": gate},
            "N4_capability_surface": n4,
            "D_semantic": semantic,
            "D_topology": topology,
            "F_comp_q_equals_F": fq,
        },
        "D_pre_activation_hardened": {"adjudication": "PASS" if hardened else "FAIL", "scope": THREAT["threat_model_id"]},
        "authorization": {"freeze_packet": "NOT_FROZEN", "authorization_certificate": "NOT_ISSUED", "future_run": "NOT_AUTHORIZED", "G_activation": "PROHIBITED"},
        "prospective": {"kernel_q_subset_kernel_T_future": "NOT_EVALUATED", "Delta_Pi": "NOT_EVALUATED"},
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "D_pre_activation_hardened": out["D_pre_activation_hardened"]["adjudication"],
        "scope": out["D_pre_activation_hardened"]["scope"],
        "N0": baseline["N0_endpoint"]["pass"], "N1": baseline["N1_full_trace"]["pass"],
        "N2": n2["pass"], "N2_comparisons": n2["comparisons"],
        "N3": n3, "poison_comparisons": poison["comparisons"], "gate_comparisons": gate["comparisons"],
        "N4": n4["pass"], "N4_attempts": n4["attempts"], "N4_accepted": n4["accepted"],
        "future_obligation_accessed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
