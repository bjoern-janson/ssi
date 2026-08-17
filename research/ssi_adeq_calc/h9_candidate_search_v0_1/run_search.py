from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
WORLDS_PATH = HERE / "WORLDS.json"

CANDIDATES: dict[str, Callable[[dict[str, Any]], Any]] = {
    "C1_INDEPENDENT_PROVENANCE":
        lambda w: bool(w["independent_provenance"]),
    "C2_TRUSTED_INPUT_BOUNDARY":
        lambda w: bool(w["trusted_input_boundary"]),
    "C3_CHECKABLE_COVERAGE_WITNESS":
        lambda w: bool(w["checkable_coverage_witness"]),
    "C4_INDEPENDENT_SELECTOR_DOMAIN":
        lambda w: bool(w["independently_constituted_selector_domain"]),
    "C5_CLAIM_SOURCE_STANDING":
        lambda w: bool(w["claim_source_has_standing"]),
}


def load_worlds() -> dict[str, Any]:
    return json.loads(WORLDS_PATH.read_text(encoding="utf-8"))


def pair_id(a: dict[str, Any], b: dict[str, Any]) -> str:
    return f"{a['id']}::{b['id']}"


def evaluate_candidate(
    worlds: list[dict[str, Any]],
    candidate_name: str,
    fn: Callable[[dict[str, Any]], Any],
    h9_anchor: list[str],
) -> dict[str, Any]:
    missed = []
    gratuitous = []
    consequential_total = 0
    inert_total = 0

    by_id = {w["id"]: w for w in worlds}
    anchor_a, anchor_b = (by_id[h9_anchor[0]], by_id[h9_anchor[1]])
    anchor_separated = fn(anchor_a) != fn(anchor_b)

    for a, b in combinations(worlds, 2):
        delta_y = a["Y_adequacy"] != b["Y_adequacy"]
        delta_phi = fn(a) != fn(b)

        if delta_y:
            consequential_total += 1
            if not delta_phi:
                missed.append(pair_id(a, b))
        else:
            inert_total += 1
            if delta_phi:
                gratuitous.append(pair_id(a, b))

    return {
        "candidate": candidate_name,
        "h9_anchor_separated": anchor_separated,
        "consequential_pairs": consequential_total,
        "inert_pairs": inert_total,
        "missed_consequential_count": len(missed),
        "missed_consequential_pairs": missed,
        "gratuitous_distinction_count": len(gratuitous),
        "gratuitous_distinction_pairs": gratuitous,
        "exact_partition_match": (
            anchor_separated
            and not missed
            and not gratuitous
        ),
    }


def main() -> int:
    suite = load_worlds()
    worlds = suite["worlds"]
    h9_anchor = suite["h9_anchor"]

    results = [
        evaluate_candidate(worlds, name, fn, h9_anchor)
        for name, fn in CANDIDATES.items()
    ]
    exact = [r["candidate"] for r in results if r["exact_partition_match"]]

    if len(exact) == 1:
        outcome = "UNIQUE_EXACT_CANDIDATE"
    elif len(exact) > 1:
        outcome = "AMBIGUOUS_EXACT_CANDIDATES"
    else:
        outcome = "NO_EXACT_CANDIDATE"

    print(json.dumps({
        "suite_id": suite["suite_id"],
        "authority_ceiling": suite["authority_ceiling"],
        "candidate_family_frozen": list(CANDIDATES),
        "world_count": len(worlds),
        "outcome": outcome,
        "exact_candidates": exact,
        "results": results,
        "repair_permitted": False,
        "new_ssi_coordinate_established": False,
        "ssi_calc_kernel_delta": 0,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
