#!/usr/bin/env python3
"""Semantic/quotient construction audit for VFA-0.2.

No prospective future obligation is read or simulated. No G activation occurs.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = json.loads((HERE / "VALIDATED_SUBSTRATE.json").read_text())
GA = json.loads((HERE / "GAMMA_A.json").read_text())
GB = json.loads((HERE / "GAMMA_B.json").read_text())
Q = json.loads((HERE / "QUOTIENT_MAP.json").read_text())
FROZEN = json.loads(
    (HERE.parent.parent / "benchmark_v0_2" / "construction" / "SHARED_FORWARD.json").read_text()
)
OUT = HERE / "quotient_construction_audit.json"


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def sha(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def edge_key(a, b):
    return "|".join(sorted((a, b)))


def jaccard(a, b):
    u = a | b
    return 1.0 if not u else len(a & b) / len(u)


def cases():
    return {f["case"]: set(f["transformation_classes"]) for f in W["facts"]}


def universe():
    cs = cases()
    classes = sorted(FROZEN["transformation_classes"])
    historical = list(cs.values())
    out = []
    for r in range(1, len(classes) + 1):
        for comb in itertools.combinations(classes, r):
            s = set(comb)
            if not any(s == h for h in historical):
                out.append(list(comb))
    return out


def validate_gamma(g):
    fact_ids = {f["fact_id"] for f in W["facts"]}
    ids = [r["path_id"] for r in g["path_records"]]
    return (
        g["substrate_ref"] == "construction/VALIDATED_SUBSTRATE.json"
        and len(ids) == len(set(ids))
        and set(ids) == set(g["equivalence_class"])
        and all(r["source_fact_id"] in fact_ids for r in g["path_records"])
    )


def semantic_certificate():
    forbidden = {"truth", "truth_value", "status", "validated", "transformation_classes"}
    truth_fields = sorted(
        {k for g in (GA, GB) for r in g["path_records"] for k in r if k in forbidden}
    )
    out = {
        "shared_substrate_sha256": sha(W),
        "same_substrate_ref": GA["substrate_ref"] == GB["substrate_ref"],
        "same_path_records": GA["path_records"] == GB["path_records"],
        "same_canonical_byte_length": len(canonical(GA)) == len(canonical(GB)),
        "canonical_bytes_A": len(canonical(GA)),
        "canonical_bytes_B": len(canonical(GB)),
        "gamma_truth_bearing_fields": truth_fields,
        "gamma_A_valid": validate_gamma(GA),
        "gamma_B_valid": validate_gamma(GB),
    }
    out["pass"] = all([
        out["same_substrate_ref"], out["same_path_records"],
        out["same_canonical_byte_length"], not truth_fields,
        out["gamma_A_valid"], out["gamma_B_valid"],
    ])
    return out


def quotient_certificate():
    ae, be, m = GA["equivalence_class"], GB["equivalence_class"], Q["mapping"]
    total = set(m) == set(ae.values())
    surjective = set(m.values()) == set(be.values())
    matches = all(m[ae[p]] == be[p] for p in ae)
    merged = []
    ids = sorted(ae)
    for i, x in enumerate(ids):
        for y in ids[i + 1:]:
            if ae[x] != ae[y] and be[x] == be[y]:
                merged.append([x, y])
    rule = (
        Q.get("no_seed_search") is True
        and "sort source case IDs lexicographically and merge adjacent pairs" in Q.get("construction_rule", "")
    )
    return {
        "pass": total and surjective and matches and rule and bool(merged),
        "total": total,
        "surjective": surjective,
        "q_matches_GAMMA_B": matches,
        "construction_rule_frozen": rule,
        "kernel_nontrivial": bool(merged),
        "kernel_merged_pair_count": len(merged),
        "kernel_merged_pairs_sha256": sha(merged),
        "future_kernel_inclusion": "NOT_EVALUATED",
    }


def phi(g):
    eq = g["equivalence_class"]
    c = Counter(eq.values())
    reopen = {eq[p] for p in eq if p.startswith("REOPEN:")}
    return {
        "path_record_count": len(eq),
        "distinct_path_classes": len(c),
        "singleton_path_fraction": sum(v == 1 for v in c.values()) / len(eq),
        "mean_equivalence_class_size": len(eq) / len(c),
        "max_equivalence_class_size": max(c.values()),
        "reopen_distinct_classes": len(reopen),
    }


def topology_certificate():
    pa, pb = phi(GA), phi(GB)
    return {
        "pass": pa["path_record_count"] == pb["path_record_count"] and GA["equivalence_class"] != GB["equivalence_class"],
        "same_path_record_count": pa["path_record_count"] == pb["path_record_count"],
        "partition_differs": GA["equivalence_class"] != GB["equivalence_class"],
        "Phi_path_A": pa,
        "Phi_path_B": pb,
        "aggregation": "PROHIBITED",
    }


def forward_state(gamma):
    if not validate_gamma(gamma):
        raise AssertionError("invalid Gamma")
    return {
        "cases": {f["case"]: f["transformation_classes"] for f in W["facts"]},
        "topology_weights": FROZEN["topology_weights"],
        "top_k": FROZEN["top_k"],
    }


def trace(query, state):
    q = set(query)
    features = {k: set(v) for k, v in state["cases"].items()}
    ids = sorted(features)
    exact = [c for c in ids if features[c] == q]
    if len(exact) == 1:
        anchor, ranking, selected = exact[0], [], []
    else:
        anchors = sorted(((-jaccard(q, features[c]), c) for c in ids))
        anchor = anchors[0][1]
        ranked = []
        for c in ids:
            if c != anchor:
                ranked.append((state["topology_weights"][edge_key(anchor, c)], c))
        ranked.sort(key=lambda x: (-x[0], x[1]))
        ranking = [{"case": c, "weight": w} for w, c in ranked]
        selected = [c for _, c in ranked[:int(state["top_k"])]]
    recovered = set(features[anchor])
    for c in selected:
        recovered |= features[c]
    recall = len(q & recovered) / len(q) if q else 1.0
    return {
        "input": sorted(q), "anchor": anchor, "ranking": ranking,
        "selected": selected, "recovered": sorted(recovered),
        "recall": recall, "full_recovery": recall == 1.0,
    }


def forward_certificate():
    fa, fb = forward_state(GA), forward_state(GB)
    tasks = universe()
    mismatches = []
    rows_a, rows_b = [], []
    for task in tasks:
        a, b = trace(task, fa), trace(task, fb)
        rows_a.append(a); rows_b.append(b)
        if a != b:
            mismatches.append({"task": task, "A": sha(a), "B": sha(b)})
    def qadapt(rows):
        return {
            "task_count": len(rows),
            "mean_recovery_recall": sum(r["recall"] for r in rows) / len(rows),
            "full_recovery_count": sum(r["full_recovery"] for r in rows),
            "full_recovery_rate": sum(r["full_recovery"] for r in rows) / len(rows),
        }
    qa, qb = qadapt(rows_a), qadapt(rows_b)
    return {
        "pass": fa == fb and not mismatches and qa == qb,
        "ordinary_forward_state_equal": fa == fb,
        "task_count": len(tasks),
        "trace_mismatch_count": len(mismatches),
        "mismatches": mismatches[:10],
        "Q_adapt_A": qa, "Q_adapt_B": qb,
        "equivalence_rule": "EXACT_TRACE_IDENTITY on exhaustive deterministic pre-freeze surrogate universe",
    }


def main():
    semantic = semantic_certificate()
    quotient = quotient_certificate()
    topology = topology_certificate()
    forward = forward_certificate()
    ok = semantic["pass"] and quotient["pass"] and topology["pass"] and forward["pass"]
    out = {
        "benchmark_id": "VFA-0.2-QUOTIENT-REVISION-TOPOLOGY",
        "audit_identity": "VFA-0.2-QUOTIENT-CONSTRUCTION-AUDIT-1",
        "future_obligation_accessed": False,
        "central_wager": "A distinction can have zero present behavioral value yet positive future corrective option value.",
        "certificates": {
            "D_semantic": semantic,
            "quotient_q": quotient,
            "D_topology": topology,
            "F_comp_q_equals_F": forward,
        },
        "construction_adjudication": "PASS" if ok else "FAIL",
        "not_yet_evaluated": {
            "N0_to_N4_on_redesigned_treatment": "NOT_EVALUATED",
            "capability_surface_hardening": "NOT_EVALUATED",
            "G_activation": "PROHIBITED",
            "kernel_q_subset_kernel_T_future": "NOT_EVALUATED",
            "Delta_Pi": "NOT_EVALUATED",
        },
        "authorization": {
            "freeze_packet": "NOT_FROZEN",
            "authorization_certificate": "NOT_ISSUED",
            "future_run": "NOT_AUTHORIZED",
        },
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "construction": out["construction_adjudication"],
        "D_semantic": semantic["pass"], "D_topology": topology["pass"],
        "F_comp_q_equals_F": forward["pass"],
        "tasks": forward["task_count"], "trace_mismatches": forward["trace_mismatch_count"],
        "kernel_merged_pairs": quotient["kernel_merged_pair_count"],
        "future_obligation_accessed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
