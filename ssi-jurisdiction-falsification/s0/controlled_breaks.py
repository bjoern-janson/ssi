#!/usr/bin/env python3
"""Controlled synthetic jurisdiction cases for SSI-JURISDICTION-FALSIFICATION/S0.

Construction labels are written only to the oracle key. The assay input contains
operational probe transcripts and nuisance fields, never injected-break labels.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Iterable

CLASS_BY_BREAK = {
    "D": "CHALLENGE_BLIND",
    "R": "CHALLENGE_BLOCKED",
    "L": "AUTHORITY_INERT",
    "I": "CHALLENGE_CIRCULAR",
}
COMPONENTS = ("D", "R", "L", "I")


def _token(rng: random.Random, stem: str) -> str:
    return f"{stem}_{rng.getrandbits(48):012x}"


def _encode(bit: int, polarity: int, salt: int) -> int:
    # Reversible nuisance encoding. The assay never needs to invert it; it only
    # compares equality/inequality under controlled interventions.
    return polarity * (11 if bit else -11) + salt


def build_case(case_id: str, breaks: Iterable[str], seed: int, family: str) -> tuple[dict, dict]:
    breaks = frozenset(breaks)
    unknown = breaks.difference(COMPONENTS)
    if unknown:
        raise ValueError(f"unknown break(s): {sorted(unknown)}")
    rng = random.Random(seed)
    polarity = rng.choice((-1, 1))
    salt = rng.randint(-7, 7)
    path_len = rng.randint(1, 6)
    decoys = [_token(rng, "decoy") for _ in range(rng.randint(1, 5))]

    # D probe: reality changes while authority is clamped. Intact challenge
    # evidence must preserve that identifying distinction.
    if "D" in breaks:
        d0 = d1 = _encode(rng.randint(0, 1), polarity, salt)
    else:
        d0 = _encode(0, polarity, salt)
        d1 = _encode(1, polarity, salt)

    # R probe: externally validated contradiction is injected downstream of
    # detection. Receipt is audited at the authority boundary, independently
    # from whether authority subsequently changes.
    receipt_nonce = _token(rng, "receipt") if "R" not in breaks else None

    # L probe: same validated contradiction, authority starts at 1 and should
    # move downward. Reachability failure also prevents a change, but the assay
    # can distinguish it from leverage using the independent receipt audit.
    authority_before = 1.0
    authority_after = 0.25 if ("R" not in breaks and "L" not in breaks) else 1.0

    # I probe: hold reality fixed while intervening on authority. An independent
    # challenge signal must not change as a function of the authority it tests.
    fixed_reality = rng.randint(0, 1)
    base_i = _encode(fixed_reality, polarity, salt)
    if "I" in breaks:
        i_low = base_i - 17
        i_high = base_i + 17
    else:
        i_low = i_high = base_i

    case = {
        "case_id": case_id,
        "schema_version": 1,
        "operational_probes": {
            "detectability": {
                "authority_clamp": 0.5,
                "reality_0_signal": d0,
                "reality_1_signal": d1,
            },
            "reachability": {
                "validated_challenge_id": _token(rng, "challenge"),
                "authority_boundary_receipt_nonce": receipt_nonce,
                "path_hops_reported": path_len,
            },
            "leverage": {
                "validated_direction": "DECREASE",
                "authority_before": authority_before,
                "authority_after": authority_after,
            },
            "independence": {
                "fixed_reality_id": _token(rng, "reality"),
                "authority_clamp_low_signal": i_low,
                "authority_clamp_high_signal": i_high,
            },
        },
        "nuisance": {
            "family": family,
            "transport_hops": path_len,
            "decoy_tokens": decoys,
            "opaque_scalar": rng.random(),
        },
    }
    component_state = {c: c not in breaks for c in COMPONENTS}
    if not breaks:
        required = "J=1"
    elif len(breaks) == 1:
        required = CLASS_BY_BREAK[next(iter(breaks))]
    else:
        required = "MULTIPLE_BREAKS"
    oracle = {
        "case_id": case_id,
        "intact_components": component_state,
        "required_classification": required,
        "jurisdiction_required": not breaks,
    }
    return case, oracle


def constitution_suite() -> tuple[list[dict], list[dict]]:
    plan = [
        ("intact", ()),
        ("d", ("D",)),
        ("r", ("R",)),
        ("l", ("L",)),
        ("i", ("I",)),
        ("dr", ("D", "R")),
        ("dl", ("D", "L")),
        ("ri", ("R", "I")),
        ("li", ("L", "I")),
        ("drl", ("D", "R", "L")),
        ("all", ("D", "R", "L", "I")),
    ]
    cases, key = [], []
    for idx, (name, breaks) in enumerate(plan):
        case, oracle = build_case(
            f"constit_{idx:02d}_{hashlib.sha256(name.encode()).hexdigest()[:8]}",
            breaks,
            2026081600 + idx * 7919,
            "constitution",
        )
        cases.append(case)
        key.append(oracle)
    return cases, key


def write_suite(cases: list[dict], key: list[dict], cases_path: Path, key_path: Path) -> None:
    cases_path.write_text(json.dumps({"cases": cases}, indent=2, sort_keys=True) + "\n")
    key_path.write_text(json.dumps({"oracle": key}, indent=2, sort_keys=True) + "\n")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cases", required=True, type=Path)
    p.add_argument("--key", required=True, type=Path)
    args = p.parse_args()
    cases, key = constitution_suite()
    write_suite(cases, key, args.cases, args.key)


if __name__ == "__main__":
    main()
