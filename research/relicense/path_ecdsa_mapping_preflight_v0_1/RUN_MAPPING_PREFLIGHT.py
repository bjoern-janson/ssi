#!/usr/bin/env python3
"""First frozen mapping preflight for the unchanged external path witness.

This runner imports only the frozen M_F mapper. It does not import or execute SSI,
and it does not read the frozen path-consequence oracle files.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
MAPPER = HERE.parent / "external_to_ssi_mapping_v0_1" / "mapper.py"

EXPECTED = {
    "PATH_A_EXTERNAL.json": "d19411ffefb4ce9b8b81e6fd1a61ef0e4d4fbd7c700b4ab77804592172b574a5",
    "PATH_B_EXTERNAL.json": "80a79ae43880ccb0db7f36e8ee5d3f8f3f4c4f91ff117fc6e9f1734aedc0310a",
    "mapper.py": "87e42ef32167d3ac45d8d2b31d1ad5fdcc1fbaed25c3ef5ba86bb08d1b82a800",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_mapper():
    if sha256(MAPPER) != EXPECTED["mapper.py"]:
        raise RuntimeError("frozen mapper hash mismatch")
    spec = importlib.util.spec_from_file_location("mf_mapper_preflight", MAPPER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run() -> dict:
    mapper = load_mapper()
    records = []
    statuses = []

    for path_name in ("PATH_A_EXTERNAL.json", "PATH_B_EXTERNAL.json"):
        path = HERE / path_name
        observed_hash = sha256(path)
        if observed_hash != EXPECTED[path_name]:
            raise RuntimeError(f"witness hash mismatch: {path_name}")
        external_path = json.loads(path.read_text())
        transitions = external_path.get("transitions")
        if not isinstance(transitions, list):
            raise RuntimeError(f"frozen witness lacks transition list: {path_name}")

        for index, raw_transition in enumerate(transitions):
            result = mapper.map_transition(raw_transition).as_dict()
            statuses.append(result["status"])
            records.append({
                "path_file": path_name,
                "transition_index": index,
                "transition_id": raw_transition.get("transition_id"),
                "mapping_status": result["status"],
                "mapping_reason": result["reason"],
                "local_input": result["local_input"],
            })

    if any(s == "CONTRACT_VIOLATION" for s in statuses):
        decision = "MAPPING_CONTRACT_VIOLATION"
    elif any(s == "NOT_EVALUABLE" for s in statuses):
        decision = "MAPPING_BOUNDARY"
    elif statuses and all(s == "MAPPED" for s in statuses):
        decision = "MAPPING_PREFLIGHT_PASSED"
    else:
        decision = "UNKNOWN"

    return {
        "object": "SSI_PATH_WITNESS_MAPPING_PREFLIGHT_FIRST_RESULT_V0.1",
        "stage": "MAPPING_ONLY_FIRST_EXPOSURE",
        "mapper_sha256": sha256(MAPPER),
        "witness_sha256": {
            name: sha256(HERE / name)
            for name in ("PATH_A_EXTERNAL.json", "PATH_B_EXTERNAL.json")
        },
        "record_count": len(records),
        "records": records,
        "decision": decision,
        "ssi_checker_executed": False,
        "path_oracle_read_by_runner": False,
        "authority_ceiling": {
            "path_level_inadequacy": "NOT_ESTABLISHED",
            "certificate_projection_loss": "NOT_TESTED",
            "relational_composition_failure": "NOT_TESTED",
            "composition_insufficiency": "NOT_ESTABLISHED",
            "composition_theorem": "NOT_EARNED",
            "new_coordinate": "NOT_EARNED",
            "repair": "NOT_EARNED",
            "ssi_calc_kernel_delta": 0
        }
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
