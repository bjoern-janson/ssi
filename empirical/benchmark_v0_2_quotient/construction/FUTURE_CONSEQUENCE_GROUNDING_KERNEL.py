#!/usr/bin/env python3
"""Pure treatment-blind grounding kernel for future distinction evidence.

This module does not fetch or run a future release. It consumes externally
produced repeated migration outcomes under the frozen consequence contract and
maps them to consequence signatures and complete grounding rows.

No arm, Gamma, M_Gamma, Phi_path, Reach, DeltaPi, score, or outcome input is
part of the runtime grounding interface.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping

IDENTIFIED = "IDENTIFIED"
DISTINGUISHED = "DISTINGUISHED"
EQUIVALENT = "EQUIVALENT"
NOT_IDENTIFIED = "NOT_IDENTIFIED"


@dataclass(frozen=True, slots=True)
class MigrationRun:
    completed: bool
    exit_code: int | None
    biome_json: bytes | None


@dataclass(frozen=True, slots=True)
class Consequence:
    status: str
    signature_json: str | None
    signature_sha256: str | None
    reason: str | None


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _parse_strict_json(data: bytes) -> Any:
    if type(data) is not bytes:
        raise TypeError("strict JSON input must be bytes")
    return json.loads(data.decode("utf-8"))


def _ptr_token(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def _path(parent: str, token: str) -> str:
    return parent + "/" + _ptr_token(token)


def semantic_delta(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    """Return a deterministic JSON-tree delta.

    Object key order is representation only. Array order is retained as
    semantic data; unequal arrays are replaced as a whole at their path.
    """
    if type(before) is dict and type(after) is dict:
        out: list[dict[str, Any]] = []
        keys = sorted(set(before) | set(after))
        for key in keys:
            child = _path(path, str(key))
            if key not in before:
                out.append({"op": "ADD", "path": child, "after": after[key]})
            elif key not in after:
                out.append({"op": "REMOVE", "path": child, "before": before[key]})
            else:
                out.extend(semantic_delta(before[key], after[key], child))
        return out
    if type(before) is list and type(after) is list:
        if before == after:
            return []
        return [{"op": "REPLACE", "path": path or "/", "before": before, "after": after}]
    if before == after and type(before) is type(after):
        return []
    return [{"op": "REPLACE", "path": path or "/", "before": before, "after": after}]


def consequence_signature(baseline_biome_json: bytes, run_1: MigrationRun, run_2: MigrationRun) -> Consequence:
    """Identify one source fact's future migration consequence fail-closed."""
    if type(run_1) is not MigrationRun or type(run_2) is not MigrationRun:
        raise TypeError("MigrationRun required")
    for idx, run in enumerate((run_1, run_2), 1):
        if not run.completed:
            return Consequence(NOT_IDENTIFIED, None, None, f"RUN_{idx}_NOT_COMPLETED")
        if run.exit_code != 0:
            return Consequence(NOT_IDENTIFIED, None, None, f"RUN_{idx}_NONZERO_EXIT")
        if type(run.biome_json) is not bytes:
            return Consequence(NOT_IDENTIFIED, None, None, f"RUN_{idx}_OUTPUT_MISSING")
    try:
        baseline = _parse_strict_json(baseline_biome_json)
        future_1 = _parse_strict_json(run_1.biome_json)
        future_2 = _parse_strict_json(run_2.biome_json)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError):
        return Consequence(NOT_IDENTIFIED, None, None, "STRICT_JSON_PARSE_FAILURE")

    if _canonical(future_1) != _canonical(future_2):
        return Consequence(NOT_IDENTIFIED, None, None, "NONDETERMINISTIC_FUTURE_OUTPUT")

    delta_1 = semantic_delta(baseline, future_1)
    delta_2 = semantic_delta(baseline, future_2)
    sig_1 = _canonical(delta_1)
    sig_2 = _canonical(delta_2)
    if sig_1 != sig_2:
        return Consequence(NOT_IDENTIFIED, None, None, "NONDETERMINISTIC_DELTA")
    return Consequence(
        IDENTIFIED,
        sig_1,
        hashlib.sha256(sig_1.encode("utf-8")).hexdigest(),
        None,
    )


def ground_status(left: Consequence, right: Consequence) -> str:
    """Ground one future distinction by consequence equality only."""
    if type(left) is not Consequence or type(right) is not Consequence:
        raise TypeError("Consequence required")
    if left.status != IDENTIFIED or right.status != IDENTIFIED:
        return NOT_IDENTIFIED
    if left.signature_json == right.signature_json:
        return EQUIVALENT
    return DISTINGUISHED


def ground_table(domain: Mapping[str, Any], consequence_by_fact: Mapping[str, Consequence]) -> list[dict[str, str]]:
    """Return every frozen grounding unit; missing facts become NOT_IDENTIFIED."""
    if type(domain) is not dict or type(consequence_by_fact) is not dict:
        raise TypeError("dict inputs required")
    rows: list[dict[str, str]] = []
    for unit in domain["grounding_units"]:
        left_id = unit["left_fact_id"]
        right_id = unit["right_fact_id"]
        left = consequence_by_fact.get(left_id, Consequence(NOT_IDENTIFIED, None, None, "MISSING_CONSEQUENCE"))
        right = consequence_by_fact.get(right_id, Consequence(NOT_IDENTIFIED, None, None, "MISSING_CONSEQUENCE"))
        rows.append({
            "unit_id": unit["unit_id"],
            "left_fact_id": left_id,
            "right_fact_id": right_id,
            "status": ground_status(left, right),
        })
    return rows


def lift_path_surfaces(domain: Mapping[str, Any], grounding_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Lift one source-pair grounding status to its frozen relation-kind surfaces."""
    status_by_unit = {row["unit_id"]: row["status"] for row in grounding_rows}
    if set(status_by_unit) != {unit["unit_id"] for unit in domain["grounding_units"]}:
        raise ValueError("grounding rows must cover the complete frozen unit domain")
    out = []
    for surface in domain["path_surfaces"]:
        out.append({
            "unit_id": surface["unit_id"],
            "relation_kind": surface["relation_kind"],
            "left_ref": list(surface["left_ref"]),
            "right_ref": list(surface["right_ref"]),
            "status": status_by_unit[surface["unit_id"]],
        })
    return out


def future_kernel_adjudication(grounding_rows: list[dict[str, str]]) -> str:
    """Adjudicate the q-kernel inclusion question without imputing missing rows."""
    statuses = [row["status"] for row in grounding_rows]
    if any(x == DISTINGUISHED for x in statuses):
        return "NONINCLUSION_WITNESS"
    if any(x == NOT_IDENTIFIED for x in statuses):
        return NOT_IDENTIFIED
    if all(x == EQUIVALENT for x in statuses):
        return "INCLUSION_ON_FROZEN_KERNEL_DOMAIN"
    raise ValueError("unexpected grounding status")
