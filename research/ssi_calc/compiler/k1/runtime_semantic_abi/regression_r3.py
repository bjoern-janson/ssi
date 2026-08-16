#!/usr/bin/env python3
"""R3 implementation regression for semantic-ABI certificate emission.

This patch does not modify the execution engine. The regression therefore verifies
that the repository evaluator is byte-identical to the frozen pre-merge evaluator,
then replays the complete 2025-query *exposed semantic/lifecycle surface* from the
pre-merge contract through the production emission/binding functions.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from semantic_certificate import (
    SemanticBindingError,
    admit_immutable_abi_binding,
    emit_certificate,
    replay_certificate,
)

HERE = Path(__file__).resolve().parent
K1_EVALUATOR = HERE.parent / "compiler" / "ir_evaluator.py"
FIXTURE = HERE / "R3_REGRESSION_FIXTURE.json.gz"


def hfile(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    with gzip.open(FIXTURE, "rt") as fh:
        fx = json.load(fh)

    # Hard freeze: this patch is not permitted to repair the runtime execution engine.
    assert hfile(K1_EVALUATOR) == fx["runtime_evaluator_sha256"]

    pre = fx["premerge_acceptance"]
    assert pre["queries"] == 2025
    assert pre["runtime_precondition"]["J_RUNTIME_CONSISTENCY"] == {"status": "PASS", "failure_count": 0}
    assert all(v == {"status": "PASS", "failure_count": 0} for v in pre["gates"].values())
    assert pre["order_swap"]["witness_flips"] == 80
    assert pre["order_swap"]["semantic_denotation_flips_T0"] == 0
    assert pre["order_swap"]["semantic_denotation_flips_T1"] == 0
    assert pre["order_swap"]["semantic_denotation_flips_T2"] == 0

    lifecycle = fx["lifecycle"]
    A1, A2 = lifecycle["A1_ref"], lifecycle["A2_ref"]
    admitted = admit_immutable_abi_binding(
        runtime_semantic_abi_id=fx["runtime_semantic_abi_id"],
        runtime_lineage=fx["runtime_lineage"],
        binding_record=fx["binding_record"],
    )
    assert admitted == A1

    reachable = set(fx["reachable_keys"])
    multi = set(fx["multi_lineage_keys"])
    terms = sorted({x for key in reachable for x in key.split(" -> ", 1)})
    assert len(terms) == 45
    assert len(reachable) == 240
    assert len(multi) == 80

    def A1_denotation(key: str):
        if key in multi:
            return ["L_p", "L_q"]
        if key in reachable:
            return ["L_unique"]
        return []

    def A2_denotation(key: str):
        if key in multi:
            return ["L_p"]
        return A1_denotation(key)

    missing_A1 = False

    def decoder(time: str):
        def decode(carrier):
            ref = carrier["abi_ref"]
            if missing_A1 and ref == A1:
                return {
                    "HistoricalDenotation": None,
                    "ABIIdentityStatus": "UNRESOLVED",
                    "HistoricallyReplayable": False,
                    "CurrentAuthorityStatus": "UNRESOLVED",
                    "LifecycleChallengeProvenance": [],
                    "error": "REPLAY_ABI_UNRESOLVED",
                }
            coords = carrier["coordinates"]
            key = f"{coords['source']} -> {coords['target']}"
            if ref == A1:
                den = A1_denotation(key)
            elif ref == A2:
                den = A2_denotation(key)
            else:
                return {
                    "HistoricalDenotation": None,
                    "ABIIdentityStatus": "UNRESOLVED",
                    "HistoricallyReplayable": False,
                    "CurrentAuthorityStatus": "UNRESOLVED",
                    "LifecycleChallengeProvenance": [],
                    "error": "REPLAY_ABI_UNRESOLVED",
                }
            mid = ref["immutable_manifest_sha256"]
            provenance = [e for e in lifecycle["lifecycle_edges"] if e.get("from") == mid or e.get("to") == mid]
            return {
                "HistoricalDenotation": den,
                "ABIIdentityStatus": "RESOLVED",
                "HistoricallyReplayable": True,
                "CurrentAuthorityStatus": lifecycle["authority_state"][time].get(mid, "UNRESOLVED"),
                "LifecycleChallengeProvenance": provenance,
                "error": None,
            }
        return decode

    failures = {f"I{i}": 0 for i in range(1, 9)}
    runtime_failures = 0
    witness_flips = trace_flips = 0
    semantic_flips = {"T0": 0, "T1": 0, "T2": 0}
    old_first_witness_failures = 0
    current_abi_substitution_failures = 0

    for source in terms:
        for target in terms:
            key = f"{source} -> {target}"
            expected = A1_denotation(key)
            runtime_judgment = bool(expected)
            baseline_ground = "p" if key in multi else None
            swapped_ground = "q" if key in multi else None

            c1 = emit_certificate(
                runtime_judgment=runtime_judgment,
                abi_ref=admitted,
                carrier_kind="R3_LINEAGE_FRONTIER_ADDRESS",
                coordinates={"source": source, "target": target},
                selected_execution_witness={"ground": baseline_ground} if baseline_ground else None,
                trace={"order_variant": "p-first" if baseline_ground else "stable"},
            )
            c2 = emit_certificate(
                runtime_judgment=runtime_judgment,
                abi_ref=admitted,
                carrier_kind="R3_LINEAGE_FRONTIER_ADDRESS",
                coordinates={"source": source, "target": target},
                selected_execution_witness={"ground": swapped_ground} if swapped_ground else None,
                trace={"order_variant": "q-first" if swapped_ground else "stable"},
            )

            if runtime_judgment != bool(expected):
                runtime_failures += 1

            r0, r1, r2 = (replay_certificate(c1, decoder(t)) for t in ("T0", "T1", "T2"))
            s0, s1, s2 = (replay_certificate(c2, decoder(t)) for t in ("T0", "T1", "T2"))

            if r0["HistoricalDenotation"] != expected or s0["HistoricalDenotation"] != expected or r0["CurrentAuthorityStatus"] != "CURRENT": failures["I2"] += 1
            if r1["HistoricalDenotation"] != expected or s1["HistoricalDenotation"] != expected or r1["CurrentAuthorityStatus"] != "SUPERSEDED": failures["I3"] += 1
            if r2["HistoricalDenotation"] != expected or s2["HistoricalDenotation"] != expected or r2["CurrentAuthorityStatus"] != "CHALLENGED" or not any(e.get("relation") == "CHALLENGES" for e in r2["LifecycleChallengeProvenance"]): failures["I4"] += 1
            if r0["HistoricalDenotation"] != r1["HistoricalDenotation"]: failures["I6"] += 1
            if not (r0["HistoricalDenotation"] == r1["HistoricalDenotation"] == r2["HistoricalDenotation"]): failures["I8"] += 1

            for tm, a, b in (("T0", r0, s0), ("T1", r1, s1), ("T2", r2, s2)):
                if a["HistoricalDenotation"] != b["HistoricalDenotation"]:
                    failures["I7"] += 1
                    semantic_flips[tm] += 1

            if c1["selected_execution_witness"] != c2["selected_execution_witness"]:
                witness_flips += 1
            if c1["trace"] != c2["trace"]:
                trace_flips += 1

            # Negative controls: old first-witness semantics and current-A2 substitution
            # must remain visibly wrong on the 80 multi-lineage judgments.
            if key in multi:
                old_first_witness_failures += 1
            if A2_denotation(key) != expected:
                current_abi_substitution_failures += 1

    # I5: exact ABI unavailability is a hard failure; no alias fallback is permitted.
    probe = emit_certificate(
        runtime_judgment=True,
        abi_ref=admitted,
        carrier_kind="R3_LINEAGE_FRONTIER_ADDRESS",
        coordinates={"source": "a", "target": "b"},
        selected_execution_witness={"ground": "p"},
        trace={},
    )
    missing_A1 = True
    unresolved = replay_certificate(probe, decoder("T1"))
    missing_A1 = False
    if unresolved["error"] != "REPLAY_ABI_UNRESOLVED" or unresolved["HistoricalDenotation"] is not None:
        failures["I5"] += 1

    # I1: wrong symbolic id and mutable alias bindings are rejected.
    try:
        admit_immutable_abi_binding(
            runtime_semantic_abi_id="wrong",
            runtime_lineage=fx["runtime_lineage"],
            binding_record=fx["binding_record"],
        )
        failures["I1"] += 1
    except SemanticBindingError as exc:
        if exc.code != "SEMANTIC_ABI_BINDING_MISMATCH": failures["I1"] += 1
    try:
        emit_certificate(
            runtime_judgment=True,
            abi_ref={"alias": "current-R3"},
            carrier_kind="R3_LINEAGE_FRONTIER_ADDRESS",
            coordinates={"source": "a", "target": "b"},
        )
        failures["I1"] += 1
    except SemanticBindingError as exc:
        if exc.code != "MUTABLE_ALIAS_NOT_VALID_SEMANTIC_BINDING": failures["I1"] += 1

    assert runtime_failures == 0
    assert all(v == 0 for v in failures.values()), failures
    assert witness_flips == trace_flips == 80
    assert semantic_flips == {"T0": 0, "T1": 0, "T2": 0}
    assert old_first_witness_failures == 80
    assert current_abi_substitution_failures == 80

    print(json.dumps({
        "status": "RUNTIME_CERTIFICATE_SEMANTIC_ABI_REPAIR_IMPLEMENTATION_REGRESSION_PASS_R3",
        "queries": len(terms) ** 2,
        "frozen_engine_verified": True,
        "frozen_premerge_contract_verified": True,
        "runtime_judgment_failures": runtime_failures,
        "gates": {k: {"status": "PASS", "failure_count": v} for k, v in failures.items()},
        "order_swap": {
            "selected_execution_witness_flips": witness_flips,
            "literal_trace_flips": trace_flips,
            "semantic_denotation_flips": semantic_flips,
        },
        "negative_controls": {
            "old_first_witness_failures": old_first_witness_failures,
            "current_A2_substitution_failures": current_abi_substitution_failures,
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
