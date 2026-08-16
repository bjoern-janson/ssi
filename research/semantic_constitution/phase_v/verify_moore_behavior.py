#!/usr/bin/env python3
"""Deterministic verifier for the frozen E2-A Moore behavioral-equivalence audit.

Jurisdiction:
- computes behavioral equivalence on the declared presentation states;
- verifies immediate-readout agreement and transition congruence;
- verifies that the immediate output partition is already behaviorally stable;
- does NOT construct or constrain presentation-state identity;
- does NOT test future sufficiency or cross-regime comparison.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

HERE = Path(__file__).resolve().parent
WORLD_PATH = HERE / "E2A_WORLD.json"
RESULT_PATH = HERE / "E2A_MOORE_BEHAVIOR_RESULT.json"


def canonical_partition(blocks: List[List[str]]) -> List[List[str]]:
    return sorted((sorted(block) for block in blocks), key=lambda b: b[0])


def output(world: dict, q: str) -> Tuple[str, str]:
    return (world["types"][q], world["observations"][q])


def initial_output_partition(world: dict) -> List[List[str]]:
    groups: Dict[Tuple[str, str], List[str]] = {}
    for q in world["states"]:
        groups.setdefault(output(world, q), []).append(q)
    return canonical_partition(list(groups.values()))


def block_index(partition: List[List[str]]) -> Dict[str, int]:
    idx = {}
    for i, block in enumerate(partition):
        for q in block:
            idx[q] = i
    return idx


def refine_once(world: dict, partition: List[List[str]]) -> List[List[str]]:
    idx = block_index(partition)
    groups = {}
    for q in world["states"]:
        signature = (
            output(world, q),
            tuple(idx[world["step"][q][u]] for u in world["actions"]),
        )
        groups.setdefault(signature, []).append(q)
    return canonical_partition(list(groups.values()))


def behavioral_partition(world: dict):
    partition = initial_output_partition(world)
    refinements = 0
    while True:
        refined = refine_once(world, partition)
        if refined == partition:
            return partition, refinements
        partition = refined
        refinements += 1


def relation_pairs(partition: List[List[str]]) -> List[List[str]]:
    pairs = []
    for block in partition:
        for x in block:
            for y in block:
                pairs.append([x, y])
    return sorted(pairs)


def verify_congruence(world: dict, partition: List[List[str]]) -> dict:
    idx = block_index(partition)
    readout_ok = True
    transition_ok = True
    witnesses = []
    for block in partition:
        for x in block:
            for y in block:
                if output(world, x) != output(world, y):
                    readout_ok = False
                    witnesses.append({
                        "kind": "READOUT_MISMATCH",
                        "x": x,
                        "y": y,
                    })
                for u in world["actions"]:
                    sx = world["step"][x][u]
                    sy = world["step"][y][u]
                    if idx[sx] != idx[sy]:
                        transition_ok = False
                        witnesses.append({
                            "kind": "TRANSITION_CLASS_MISMATCH",
                            "x": x,
                            "y": y,
                            "action": u,
                            "step_x": sx,
                            "step_y": sy,
                        })
    return {
        "immediate_readout_preservation": readout_ok,
        "one_step_transition_congruence": transition_ok,
        "congruence_verified": readout_ok and transition_ok,
        "witnesses": witnesses,
    }


def verify_last_action_property(world: dict) -> dict:
    """Prove the nonempty-word observation property by checking its one-step generator."""
    per_action_outputs = {}
    ok = True
    for u in world["actions"]:
        outputs = sorted({output(world, world["step"][q][u]) for q in world["states"]})
        per_action_outputs[u] = [list(v) for v in outputs]
        if len(outputs) != 1:
            ok = False
    return {
        "verified": ok,
        "proof_basis":
            "For each action u, every source state transitions to a state with the "
            "same declared output. Therefore the output after any nonempty word "
            "depends only on its final action.",
        "per_action_successor_outputs": per_action_outputs,
    }


def main() -> None:
    world = json.loads(WORLD_PATH.read_text())
    initial = initial_output_partition(world)
    behavior, refinements = behavioral_partition(world)
    congruence = verify_congruence(world, behavior)
    last_action = verify_last_action_property(world)

    result = {
        "object": "SEMANTIC_EQUIVALENCE_REGIME_AUDIT/E2-A/MOORE_BEHAVIOR",
        "audit_method": "EXECUTABLE_DETERMINISTIC_FINITE_PARTITION_REFINEMENT",
        "world_object": world["object"],
        "regime": "DETERMINISTIC_MOORE_COALGEBRAIC_BEHAVIOR",
        "purpose": "FINITE_INPUT_OBSERVATIONAL_BEHAVIOR",
        "presentation_sort": "Q",
        "denotation_sort": "(Theta x Y)^(U*)",
        "initial_output_partition": initial,
        "behavioral_partition": behavior,
        "behavioral_equivalence_pairs": relation_pairs(behavior),
        "number_of_classes": len(behavior),
        "partition_refinement_rounds_beyond_output_partition": refinements,
        "behavioral_equivalence_equals_immediate_output_equivalence": behavior == initial,
        "congruence": congruence,
        "u_star_closure": (
            "VERIFIED_BY_ONE_STEP_CONGRUENCE_INDUCTION"
            if congruence["congruence_verified"]
            else "REJECTED"
        ),
        "nonempty_word_last_action_property": last_action,
        "identity_authorization": "NOT_IN_SCOPE",
        "identity_regime_membership": "NOT_AUTHORIZED",
        "future_sufficiency": "NOT_IN_SCOPE",
        "cross_regime_comparison": "NOT_IN_SCOPE",
        "terminal_status": (
            "PASS"
            if congruence["congruence_verified"] and last_action["verified"]
            else "REJECTED"
        ),
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
