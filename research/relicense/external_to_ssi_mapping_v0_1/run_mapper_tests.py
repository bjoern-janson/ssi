#!/usr/bin/env python3
"""Run only the frozen M_F mapping suite. This file never imports SSI."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def load_mapper():
    spec = importlib.util.spec_from_file_location("mf_mapper", HERE / "mapper.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mutate(base: dict, mutations: list[dict]) -> dict:
    value = deepcopy(base)
    for mutation in mutations:
        path = mutation["path"]
        parent = value
        for key in path[:-1]:
            parent = parent[key]
        leaf = path[-1]
        if mutation["op"] == "set":
            parent[leaf] = deepcopy(mutation["value"])
        elif mutation["op"] == "delete":
            del parent[leaf]
        else:
            raise ValueError(f"unknown mutation op: {mutation['op']}")
    return value


def run() -> dict:
    mapper = load_mapper()
    suite = json.loads((HERE / "MAPPER_TESTS.json").read_text())
    baseline = suite["baseline"]
    records = []
    failures = []

    for case in suite["cases"]:
        cid = case["id"]
        if case["kind"] == "single":
            external = mutate(baseline, case.get("mutations", []))
            result = mapper.map_transition(external).as_dict()
            ok = result["status"] == case["expect_status"]
            record = {
                "id": cid,
                "kind": "single",
                "observed_status": result["status"],
                "expected_status": case["expect_status"],
                "ok": ok,
            }
        else:
            left = mapper.map_transition(deepcopy(baseline)).as_dict()
            right_external = mutate(baseline, case["right_mutations"])
            right = mapper.map_transition(right_external).as_dict()
            if left["status"] == right["status"] == "MAPPED":
                relation = "SAME" if left["local_input"] == right["local_input"] else "DIFFERENT"
            else:
                relation = "UNAVAILABLE"
            ok = (
                left["status"] == "MAPPED"
                and right["status"] == "MAPPED"
                and relation == case["expect_relation"]
            )
            if "expect_audit_basis" in case:
                bases = {entry["basis"] for entry in right["audit"]}
                ok = ok and case["expect_audit_basis"] in bases
            record = {
                "id": cid,
                "kind": "pair",
                "left_status": left["status"],
                "right_status": right["status"],
                "local_input_relation": relation,
                "expected_relation": case["expect_relation"],
                "ok": ok,
            }
        records.append(record)
        if not ok:
            failures.append(cid)

    result = (
        "MAPPING_SUPPORTED_ON_FROZEN_ABSTRACT_SUITE"
        if not failures
        else "MAPPING_NOT_SUPPORTED_ON_FROZEN_ABSTRACT_SUITE"
    )
    return {
        "object": suite["object"],
        "stage": "MAPPER_ONLY_FIRST_EXECUTION",
        "suite_sha256": sha256(HERE / "MAPPER_TESTS.json"),
        "mapper_sha256": sha256(HERE / "mapper.py"),
        "case_count": len(records),
        "records": records,
        "failure_ids": failures,
        "result": result,
        "strongest_earned_claim": (
            "EXTERNAL_TO_SSI_MAPPING_CONSTITUTION = SUPPORTED_ON_FROZEN_ABSTRACT_MAPPING_SUITE"
            if not failures
            else "NO_POSITIVE_MAPPING_CLAIM"
        ),
        "authority_ceiling": suite["authority_ceiling"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
