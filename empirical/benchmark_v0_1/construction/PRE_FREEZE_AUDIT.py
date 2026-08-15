#!/usr/bin/env python3
"""Adversarial pre-freeze C/D audit.

No future obligation is read. C tests exact present-state equality on all
non-treatment payload dimensions. D exhaustively tests every nonempty subset of
the frozen migration-class universe that is not one of the six exact historical
signatures, using the same topology-assisted two-neighbor resolver for both arms.

A nonzero deterministic D difference blocks equivalence; no null-hypothesis
significance test is used as evidence of equality.
"""

from __future__ import annotations
import itertools, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIG = json.loads((HERE / "MIGRATION_SIGNATURES.json").read_text())
A = json.loads((HERE / "state_A.json").read_text())
B = json.loads((HERE / "state_B.json").read_text())
OUT = HERE / "pre_freeze_audit.json"

TOP_K = 2


def dump(x):
    return json.dumps(x, indent=2, sort_keys=True) + "\n"


def edge_key(a, b):
    return "|".join(sorted((a, b)))


FEATURES = {c: set(v["features"]) for c, v in SIG["cases"].items()}
CASE_IDS = sorted(FEATURES)
UNIVERSE = sorted(SIG["transformation_classes"])


def jaccard(a, b):
    return len(a & b) / len(a | b)


def resolve(state, query):
    q = set(query)
    exact = sorted(c for c in CASE_IDS if FEATURES[c] == q)
    if len(exact) == 1:
        return {
            "mode": "DIRECT",
            "anchor": exact[0],
            "neighbors": [],
            "recovered": sorted(FEATURES[exact[0]]),
        }

    anchors = sorted(
        ((jaccard(q, FEATURES[c]), c) for c in CASE_IDS),
        key=lambda row: (-row[0], row[1]),
    )
    anchor = anchors[0][1]

    neighbors = sorted(
        (
            (state["topology_weights"][edge_key(anchor, c)], c)
            for c in CASE_IDS
            if c != anchor
        ),
        key=lambda row: (-row[0], row[1]),
    )[:TOP_K]

    recovered = set(FEATURES[anchor])
    for _, c in neighbors:
        recovered |= FEATURES[c]

    return {
        "mode": "TOPOLOGY_ASSISTED",
        "anchor": anchor,
        "neighbors": [c for _, c in neighbors],
        "recovered": sorted(recovered),
    }


def q_state(state):
    pairs = state["direct_historical_pairs"]
    return {
        "case_count": state["case_count"],
        "edge_count": state["edge_count"],
        "direct_pair_count": len(pairs),
        "transformation_class_count": len({f for r in pairs.values() for f in r["features"]}),
        "known_pair_availability_rate": sum(
            bool(r["input_locator"]) and bool(r["output_snapshot_git_blob_sha1"])
            for r in pairs.values()
        ) / len(pairs),
        "topology_weight_multiset": sorted(state["topology_weights"].values()),
    }


def surrogate_universe():
    historical = list(FEATURES.values())
    tasks = []
    for r in range(1, len(UNIVERSE) + 1):
        for comb in itertools.combinations(UNIVERSE, r):
            s = set(comb)
            if any(s == h for h in historical):
                continue
            tasks.append(comb)
    return tasks


def q_adapt(state, tasks):
    rows = []
    for task in tasks:
        result = resolve(state, task)
        q = set(task)
        recovered = set(result["recovered"])
        recall = len(q & recovered) / len(q)
        rows.append({
            "query": list(task),
            "anchor": result["anchor"],
            "neighbors": result["neighbors"],
            "recall": recall,
            "full_recovery": recall == 1.0,
        })
    return {
        "task_universe_rule": "all nonempty subsets of frozen transformation classes excluding the six exact historical signatures",
        "task_count": len(rows),
        "top_k": TOP_K,
        "mean_recovery_recall": sum(r["recall"] for r in rows) / len(rows),
        "full_recovery_rate": sum(r["full_recovery"] for r in rows) / len(rows),
        "full_recovery_count": sum(r["full_recovery"] for r in rows),
        "rows": rows,
    }


def main():
    qs_a, qs_b = q_state(A), q_state(B)
    tasks = surrogate_universe()
    qa_a, qa_b = q_adapt(A, tasks), q_adapt(B, tasks)

    c_dims = [
        "case_count", "edge_count", "direct_pair_count",
        "transformation_class_count", "known_pair_availability_rate",
        "topology_weight_multiset",
    ]
    C_pass = all(qs_a[k] == qs_b[k] for k in c_dims)

    d_compare = {
        "task_count": {"A": qa_a["task_count"], "B": qa_b["task_count"], "delta": 0},
        "mean_recovery_recall": {
            "A": qa_a["mean_recovery_recall"],
            "B": qa_b["mean_recovery_recall"],
            "delta": qa_a["mean_recovery_recall"] - qa_b["mean_recovery_recall"],
        },
        "full_recovery_rate": {
            "A": qa_a["full_recovery_rate"],
            "B": qa_b["full_recovery_rate"],
            "delta": qa_a["full_recovery_rate"] - qa_b["full_recovery_rate"],
        },
        "full_recovery_count": {
            "A": qa_a["full_recovery_count"],
            "B": qa_b["full_recovery_count"],
            "delta": qa_a["full_recovery_count"] - qa_b["full_recovery_count"],
        },
    }

    # Deterministic exhaustive finite surrogate universe: exact equality is
    # required for D. This is stronger than using p>0.05 as "equivalence".
    D_pass = all(v["delta"] == 0 for v in d_compare.values())

    differing_rows = []
    for ra, rb in zip(qa_a["rows"], qa_b["rows"]):
        if ra["recall"] != rb["recall"]:
            differing_rows.append({
                "query": ra["query"],
                "A": {k: ra[k] for k in ["anchor", "neighbors", "recall", "full_recovery"]},
                "B": {k: rb[k] for k in ["anchor", "neighbors", "recall", "full_recovery"]},
            })
    differing_query_blob = dump([row["query"] for row in differing_rows]).encode()
    differing_query_sha256 = __import__("hashlib").sha256(differing_query_blob).hexdigest()

    out = {
        "benchmark_id": "independent-future-adaptation-v0.1",
        "future_obligation_accessed": False,
        "C": {
            "adjudication": "PASS" if C_pass else "FAIL",
            "equivalence_rule": "EXACT_EQUALITY",
            "A": qs_a,
            "B": qs_b,
        },
        "D": {
            "adjudication": "PASS" if D_pass else "FAIL",
            "equivalence_rule": "EXACT_EQUALITY on exhaustive deterministic pre-freeze surrogate universe",
            "A": {k: v for k, v in qa_a.items() if k != "rows"},
            "B": {k: v for k, v in qa_b.items() if k != "rows"},
            "comparison": d_compare,
            "differing_task_count": len(differing_rows),
            "differing_task_queries_sha256": differing_query_sha256,
        },
        "interpretation_boundary": {
            "C": "current payload/capability identity is established only on the frozen current-state dimensions above",
            "D": "current A/B construction is not ordinary-adaptation matched; the shot is blocked before freeze",
        },
    }
    OUT.write_text(dump(out))
    print(dump({
        "C": out["C"]["adjudication"],
        "D": out["D"]["adjudication"],
        "D_comparison": d_compare,
        "D_differing_task_count": len(differing_rows),
    }), end="")


if __name__ == "__main__":
    main()
