#!/usr/bin/env python3
"""Build and measure the frozen A/B corrective-topology construction.

Construction only. This is not the future-obligation runner.

The direct historical migration pairs are identical in A and B. The treatment
changes only second-order cross-case analogy weights. A stores evidence-derived
Jaccard similarity between coarse migration-class signatures. B applies one
fixed deterministic cyclic permutation of the complete graph's edge-weight
multiset. No seed search is permitted.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIG_PATH = HERE / "MIGRATION_SIGNATURES.json"
STATE_A_PATH = HERE / "state_A.json"
STATE_B_PATH = HERE / "state_B.json"
PHI_PATH = HERE / "phi_measurement.json"

SCRAMBLE_SEED = "ssi-independent-future-adaptation-v0.1/B/topology-scramble/1"
TOP_K = 2
RECONF_JACCARD_THRESHOLD = 0.5


def canonical_dump(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def edge_key(a: str, b: str) -> str:
    return "|".join(sorted((a, b)))


def jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    if not union:
        raise ValueError("empty migration signature is not admissible")
    return len(a & b) / len(union)


def build_states(signatures: dict) -> tuple[dict, dict, dict[str, float]]:
    cases = signatures["cases"]
    case_ids = sorted(cases)
    feature_sets = {case: set(cases[case]["features"]) for case in case_ids}
    all_features = set(signatures["transformation_classes"])

    if any(not fs for fs in feature_sets.values()):
        raise ValueError("missing feature set: NOT_IDENTIFIED; no imputation")
    if set().union(*feature_sets.values()) != all_features:
        raise ValueError("frozen transformation-class universe is not fully represented")

    direct_pairs = {
        case: {
            "input_locator": {
                "git_blob_sha1": signatures["upstream"]["test_source"]["git_blob_sha1"],
                "test_function": {
                    "ariakit": "should_successfully_migrate_ariakit",
                    "aws": "should_migrate_aws_config",
                    "issue_5465": "should_migrate_issue_5465",
                    "knip": "should_successfully_migrate_knip",
                    "nested": "should_migrate_nested_config",
                    "sentry": "should_successfully_migrate_sentry",
                }[case],
            },
            "output_snapshot_git_blob_sha1": cases[case]["snapshot_blob_sha1"],
            "features": sorted(feature_sets[case]),
        }
        for case in case_ids
    }

    edge_ids = [edge_key(a, b) for a, b in itertools.combinations(case_ids, 2)]
    true_weights = {}
    for a, b in itertools.combinations(case_ids, 2):
        true_weights[edge_key(a, b)] = jaccard(feature_sets[a], feature_sets[b])

    # First and only frozen scramble: hash-order edges, then rotate A weights by one.
    scramble_order = sorted(
        edge_ids,
        key=lambda e: hashlib.sha256(f"{SCRAMBLE_SEED}|{e}".encode()).hexdigest(),
    )
    ordered_weights = [true_weights[e] for e in scramble_order]
    b_weights = {
        scramble_order[i]: ordered_weights[(i + 1) % len(ordered_weights)]
        for i in range(len(scramble_order))
    }

    if sorted(true_weights.values()) != sorted(b_weights.values()):
        raise AssertionError("scramble failed to preserve the edge-weight multiset")
    if all(true_weights[e] == b_weights[e] for e in edge_ids):
        raise AssertionError("scramble is identity")

    common = {
        "benchmark_id": "independent-future-adaptation-v0.1",
        "upstream": signatures["upstream"],
        "direct_historical_pairs": direct_pairs,
        "case_count": len(case_ids),
        "edge_count": len(edge_ids),
        "topology_is_complete_graph": True,
        "edge_semantics": "cross-case analogy/provenance affinity",
        "weight_semantics": "stored migration-class similarity",
        "weight_range": [0.0, 1.0],
    }

    state_a = {
        **common,
        "arm": "A",
        "treatment": "genuine_pre_freeze_cross_case_topology",
        "topology_weights": dict(sorted(true_weights.items())),
    }
    state_b = {
        **common,
        "arm": "B",
        "treatment": "fixed_weight_multiset_scramble",
        "scramble_seed": SCRAMBLE_SEED,
        "scramble_rule": "sha256-seeded edge order; cyclic weight rotation by +1",
        "scramble_order": scramble_order,
        "topology_weights": dict(sorted(b_weights.items())),
    }

    # Non-topological identity checks.
    assert state_a["direct_historical_pairs"] == state_b["direct_historical_pairs"]
    assert state_a["case_count"] == state_b["case_count"]
    assert state_a["edge_count"] == state_b["edge_count"]
    assert sorted(state_a["topology_weights"].values()) == sorted(
        state_b["topology_weights"].values()
    )

    return state_a, state_b, true_weights


def measure_phi(state: dict, signatures: dict, true_weights: dict[str, float]) -> dict:
    cases = signatures["cases"]
    case_ids = sorted(cases)
    features = {case: set(cases[case]["features"]) for case in case_ids}
    stored = state["topology_weights"]

    def ranked_neighbors(case: str):
        rows = []
        for other in case_ids:
            if other == case:
                continue
            key = edge_key(case, other)
            rows.append(
                {
                    "case": other,
                    "stored_weight": stored[key],
                    "evidence_similarity": true_weights[key],
                }
            )
        rows.sort(key=lambda row: (-row["stored_weight"], row["case"]))
        return rows

    neighbors = {case: ranked_neighbors(case) for case in case_ids}

    # C_cover_pre: correction-class payload coverage, intentionally invariant
    # to topology scrambling because A/B retain the same migration evidence.
    represented = set().union(*(features[c] for c in case_ids))
    C_cover_pre = len(represented) / len(signatures["transformation_classes"])

    # R_reconf: fraction of held-out historical cases whose top stored analog
    # has evidence-derived similarity >= frozen threshold.
    R_reconf = sum(
        neighbors[c][0]["evidence_similarity"] >= RECONF_JACCARD_THRESHOLD
        for c in case_ids
    ) / len(case_ids)

    # C_challenge: among each case's top-K stored analogs, fraction that provide
    # a non-zero independently grounded overlap with that case.
    C_challenge = sum(
        sum(row["evidence_similarity"] > 0 for row in neighbors[c][:TOP_K]) / TOP_K
        for c in case_ids
    ) / len(case_ids)

    # A_preserve: all historical alternatives/direct pairs remain retained.
    A_preserve = len(state["direct_historical_pairs"]) / len(case_ids)

    # L_prov: mean edge-level agreement between stored affinity and
    # evidence-derived affinity. Each term is 1 - absolute error on [0,1].
    L_prov = sum(
        1.0 - abs(stored[e] - true_weights[e])
        for e in sorted(true_weights)
    ) / len(true_weights)

    # R_reopen: mean held-out feature recall obtainable by reopening the
    # top-K stored analogs for each case.
    recalls = {}
    for case in case_ids:
        reopened = set()
        for row in neighbors[case][:TOP_K]:
            reopened |= features[row["case"]]
        recalls[case] = len(features[case] & reopened) / len(features[case])
    R_reopen = sum(recalls.values()) / len(recalls)

    values = {
        "C_cover_pre": C_cover_pre,
        "R_reconf": R_reconf,
        "C_challenge": C_challenge,
        "A_preserve": A_preserve,
        "L_prov": L_prov,
        "R_reopen": R_reopen,
    }

    return {
        "values": values,
        "parameters": {
            "TOP_K": TOP_K,
            "RECONF_JACCARD_THRESHOLD": RECONF_JACCARD_THRESHOLD,
        },
        "per_case_reopen_recall": recalls,
        "top_neighbors": {c: neighbors[c][:TOP_K] for c in case_ids},
    }


def main() -> None:
    signatures = json.loads(SIG_PATH.read_text())
    state_a, state_b, true_weights = build_states(signatures)
    phi_a = measure_phi(state_a, signatures, true_weights)
    phi_b = measure_phi(state_b, signatures, true_weights)

    a_text = canonical_dump(state_a)
    b_text = canonical_dump(state_b)

    STATE_A_PATH.write_text(a_text)
    STATE_B_PATH.write_text(b_text)

    delta = {
        key: phi_a["values"][key] - phi_b["values"][key]
        for key in phi_a["values"]
    }

    # Frozen directional contrast: payload-preserving dimensions equal;
    # relational dimensions A >= B, with at least one strict positive.
    equal_dims = ["C_cover_pre", "A_preserve"]
    relational_dims = ["R_reconf", "C_challenge", "L_prov", "R_reopen"]
    if any(abs(delta[k]) > 1e-12 for k in equal_dims):
        raise AssertionError("payload-preserving Phi dimensions must remain equal")
    if any(delta[k] < -1e-12 for k in relational_dims):
        raise AssertionError("frozen treatment produced wrong directional contrast")
    if not any(delta[k] > 1e-12 for k in relational_dims):
        raise AssertionError("no strict relational Phi contrast")

    measurement = {
        "benchmark_id": "independent-future-adaptation-v0.1",
        "construction_only": True,
        "missingness_rule": "any missing case, signature, edge, or required value => NOT_IDENTIFIED; no imputation; B cannot PASS",
        "admissible_measurement_transform": "IDENTITY_ONLY",
        "confirmatory_phi_interpretation": {
            "aggregation": "PROHIBITED",
            "expected_equal_dimensions": equal_dims,
            "expected_A_ge_B_dimensions": relational_dims,
            "required_strict_positive_count_min": 1,
        },
        "state_sha256": {
            "A": sha256_text(a_text),
            "B": sha256_text(b_text),
        },
        "A": phi_a,
        "B": phi_b,
        "delta_A_minus_B": delta,
        "treatment_invariants": {
            "same_direct_historical_pairs": True,
            "same_case_count": True,
            "same_edge_count": True,
            "same_edge_weight_multiset": True,
            "same_transformation_class_payload": True,
            "topology_binding_only_difference": True,
        },
        "scramble": {
            "seed": SCRAMBLE_SEED,
            "rule": "first specified seed; no seed search; sha256-seeded edge order; cyclic +1 weight rotation",
        },
    }
    PHI_PATH.write_text(canonical_dump(measurement))

    print(canonical_dump({
        "state_A_sha256": measurement["state_sha256"]["A"],
        "state_B_sha256": measurement["state_sha256"]["B"],
        "phi_A": phi_a["values"],
        "phi_B": phi_b["values"],
        "delta_A_minus_B": delta,
    }), end="")


if __name__ == "__main__":
    main()
