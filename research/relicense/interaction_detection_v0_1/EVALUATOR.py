#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

with open(HERE / "WORLDS.json", "r", encoding="utf-8") as f:
    worlds = json.load(f)
with open(HERE / "DETECTORS.json", "r", encoding="utf-8") as f:
    detectors = json.load(f)
with open(HERE / "ORACLE.json", "r", encoding="utf-8") as f:
    oracle = json.load(f)


def d0(local_interface):
    return {
        "state": "LOCAL_QUOTIENT_ONLY",
        "summary": json.dumps(local_interface, sort_keys=True),
    }


def d1(local_interface, local_closure):
    return {
        "state": "LOCAL_DERIVED_ONLY",
        "summary": json.dumps(
            {"local": local_interface, "closure": local_closure}, sort_keys=True
        ),
    }


def d2(probe):
    if probe.get("coverage") == "UNKNOWN":
        return {"state": "UNKNOWN", "fact": None}

    probe_type = probe["probe_type"]

    if probe_type == "ALIAS_TOKEN_PROBE":
        present = probe["phase12_token"] == probe["phase23_token"]
        return {
            "state": "INTERACTION_PRESENT" if present else "INTERACTION_ABSENT",
            "fact": (
                "ALIASED_WITH_AUTHORITY_SENSITIVE_COLLISION"
                if present
                else "DISJOINT"
            ),
        }

    if probe_type == "ORDER_REVERSAL_PROBE":
        present = (
            probe["forward_authority_state"]
            != probe["reverse_authority_state"]
        )
        return {
            "state": "INTERACTION_PRESENT" if present else "INTERACTION_ABSENT",
            "fact": (
                "NONCOMMUTATIVE_AUTHORITY_GUARD_FLIP"
                if present
                else "COMMUTES_ON_AUTHORITY_RELEVANT_STATE"
            ),
        }

    if probe_type == "EFFECT_TRACE_PROBE":
        present = any(
            write.get("target") == "J3.admissibility_state"
            for write in probe.get("writes", [])
        )
        return {
            "state": "INTERACTION_PRESENT" if present else "INTERACTION_ABSENT",
            "fact": (
                "WRITE_ALTERS_J3_ADMISSIBILITY_STATE"
                if present
                else "NO_WRITE_TO_J3_ADMISSIBILITY_STATE"
            ),
        }

    if probe_type == "COMPOSED_PRECONDITION_PROBE":
        present = probe["j2_post_quota"] < probe["j3_required_quota_min"]
        return {
            "state": "INTERACTION_PRESENT" if present else "INTERACTION_ABSENT",
            "fact": (
                "COMPOSED_PRECONDITION_VIOLATION"
                if present
                else "COMPOSED_PRECONDITION_SATISFIED"
            ),
        }

    raise ValueError(f"unknown probe type: {probe_type}")


local_interface = worlds["canonical_local_interface"]
local_closure = worlds["canonical_local_derived_closure"]

world_lookup = {}
for pair in worlds["primary_pairs"]:
    for side in ("a", "b"):
        world = pair[side]
        assert world["local_interface_ref"] == "canonical_local_interface"
        assert world["local_derived_closure_ref"] == "canonical_local_derived_closure"
        world_lookup[world["world_id"]] = world

# D3 uses exactly the frozen primary probe multiset with correspondence destroyed.
d3_map = detectors["detectors"]["D3"]["recipient_to_source_world"]
assert set(d3_map.keys()) == set(world_lookup.keys())
assert set(d3_map.values()) == set(world_lookup.keys())

d3_output = {
    recipient: d2(world_lookup[source]["probe"])
    for recipient, source in d3_map.items()
}

pair_results = []
d0_separated = 0
d1_separated = 0
d2_separated = 0
d3_separated = 0
d2_state_exact = 0
d2_fact_exact = 0
primary_world_count = 0

for pair in worlds["primary_pairs"]:
    pid = pair["pair_id"]
    a = pair["a"]
    b = pair["b"]

    out_d0_a = d0(local_interface)
    out_d0_b = d0(local_interface)
    out_d1_a = d1(local_interface, local_closure)
    out_d1_b = d1(local_interface, local_closure)
    out_d2_a = d2(a["probe"])
    out_d2_b = d2(b["probe"])
    out_d3_a = d3_output[a["world_id"]]
    out_d3_b = d3_output[b["world_id"]]

    sep0 = out_d0_a["state"] != out_d0_b["state"]
    sep1 = out_d1_a["state"] != out_d1_b["state"]
    sep2 = out_d2_a["state"] != out_d2_b["state"]
    sep3 = out_d3_a["state"] != out_d3_b["state"]

    d0_separated += int(sep0)
    d1_separated += int(sep1)
    d2_separated += int(sep2)
    d3_separated += int(sep3)

    expected = oracle["primary"][pid]
    for side, output in (("a", out_d2_a), ("b", out_d2_b)):
        primary_world_count += 1
        d2_state_exact += int(output["state"] == expected[side]["state"])
        d2_fact_exact += int(output["fact"] == expected[side]["fact"])

    pair_results.append(
        {
            "pair_id": pid,
            "D0_separated": sep0,
            "D1_separated": sep1,
            "D2_separated": sep2,
            "D3_separated": sep3,
            "D2_a": out_d2_a,
            "D2_b": out_d2_b,
            "D3_a": out_d3_a,
            "D3_b": out_d3_b,
        }
    )

original_probes = [world["probe"] for world in world_lookup.values()]
d3_probes = [world_lookup[source]["probe"] for source in d3_map.values()]

original_type_hist = Counter(p["probe_type"] for p in original_probes)
d3_type_hist = Counter(p["probe_type"] for p in d3_probes)
original_state_hist = Counter(d2(p)["state"] for p in original_probes)
d3_state_hist = Counter(d2(p)["state"] for p in d3_probes)

# Identifier-only control.
id_control = worlds["controls"]["identifier_leakage_pair"]
id_a = d2(id_control["a"]["probe"])
id_b = d2(id_control["b"]["probe"])
identifier_only_separations = int(id_a != id_b)

# UNKNOWN must remain epistemically distinct from negative observation.
unknown_control = worlds["controls"]["unknown_coverage_pair"]
unknown_a = d2(unknown_control["a"]["probe"])
unknown_b = d2(unknown_control["b"]["probe"])
unknown_as_negative_collapses = int(unknown_a["state"] == "INTERACTION_ABSENT")

# No primary world contains mutable local certificate bytes: all reference one canonical object.
local_certificate_mutations = 0

# Actual detector outputs must not contain transition-entitlement vocabulary.
forbidden_entitlement_values = {
    "PRESERVED",
    "EXTENDED",
    "REVOKED",
    "UNPROVEN",
    "WITNESS_SUFFICIENT",
    "COMPOSITION_VALID",
}
all_actual_outputs = []
for row in pair_results:
    all_actual_outputs.extend([row["D2_a"], row["D2_b"], row["D3_a"], row["D3_b"]])
all_actual_outputs.extend([id_a, id_b, unknown_a, unknown_b])
serialized_outputs = json.dumps(all_actual_outputs, sort_keys=True)
oracle_entitlement_label_leakage = sum(
    1 for value in forbidden_entitlement_values if value in serialized_outputs
)

pair_leakage = d0_separated > 0 or d1_separated > 0 or identifier_only_separations > 0

controls_pass = all(
    [
        d0_separated == 0,
        d1_separated == 0,
        d3_separated == 0,
        len(original_probes) == len(d3_probes),
        original_type_hist == d3_type_hist,
        original_state_hist == d3_state_hist,
        identifier_only_separations == 0,
        unknown_as_negative_collapses == 0,
        local_certificate_mutations == 0,
        oracle_entitlement_label_leakage == 0,
    ]
)

detection_supported = all(
    [
        not pair_leakage,
        d2_separated == len(worlds["primary_pairs"]),
        d2_state_exact == primary_world_count,
        d2_fact_exact == primary_world_count,
        controls_pass,
    ]
)

if pair_leakage:
    scientific_status = "PAIR_LEAKAGE"
elif detection_supported:
    scientific_status = "DETECTION_SUPPORTED"
else:
    scientific_status = "DETECTION_BLINDNESS"

result = {
    "object": "SSI_RELICENSE_INTERACTION_DETECTION_V0.1/EXECUTION",
    "scientific_status": scientific_status,
    "bounded_claim": (
        "INDEPENDENT_HIGHER_ORDER_DETECTION_SUPPORTED_ON_FROZEN_CONSTRUCTED_SUITE"
        if detection_supported
        else None
    ),
    "metrics": {
        "PRIMARY_PAIRS": len(worlds["primary_pairs"]),
        "PRIMARY_WORLDS": primary_world_count,
        "D0_PAIR_SEPARATION": f"{d0_separated}/{len(worlds['primary_pairs'])}",
        "D1_PAIR_SEPARATION": f"{d1_separated}/{len(worlds['primary_pairs'])}",
        "D2_PAIR_SEPARATION": f"{d2_separated}/{len(worlds['primary_pairs'])}",
        "D2_STATE_EXACT": f"{d2_state_exact}/{primary_world_count}",
        "D2_FACT_EXACT": f"{d2_fact_exact}/{primary_world_count}",
        "D3_PAIR_SEPARATION": f"{d3_separated}/{len(worlds['primary_pairs'])}",
        "D3_PROBE_COUNT_PRESERVED": len(original_probes) == len(d3_probes),
        "D3_PROBE_TYPE_HISTOGRAM_PRESERVED": original_type_hist == d3_type_hist,
        "D3_STATE_MARGINAL_PRESERVED": original_state_hist == d3_state_hist,
        "IDENTIFIER_ONLY_SEPARATIONS": identifier_only_separations,
        "UNKNOWN_AS_NEGATIVE_COLLAPSES": unknown_as_negative_collapses,
        "LOCAL_CERTIFICATE_MUTATIONS": local_certificate_mutations,
        "ORACLE_ENTITLEMENT_LABEL_LEAKAGE": oracle_entitlement_label_leakage,
    },
    "D0_classification": "CHALLENGE_DEPENDENCE",
    "D1_classification": "CHALLENGE_DEPENDENCE",
    "D2_classification": scientific_status if scientific_status == "DETECTION_SUPPORTED" else "DETECTION_BLINDNESS",
    "D3_control": {
        "original_probe_type_histogram": dict(sorted(original_type_hist.items())),
        "destroyed_probe_type_histogram": dict(sorted(d3_type_hist.items())),
        "original_state_histogram": dict(sorted(original_state_hist.items())),
        "destroyed_state_histogram": dict(sorted(d3_state_hist.items())),
    },
    "unknown_control": {"a": unknown_a, "b": unknown_b},
    "identifier_control": {"a": id_a, "b": id_b},
    "pair_results": pair_results,
    "authority_ceiling": {
        "witness_sufficiency_tested": False,
        "transition_entitlement_derived": False,
        "W_int_sufficient": False,
        "W_comp_defined": False,
        "composition_rule_admitted": False,
        "formal_soundness_established": False,
        "empirical_real_world_detection_claimed": False,
        "ssi_calc_kernel_delta": 0,
        "jepa": "PARKED",
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
