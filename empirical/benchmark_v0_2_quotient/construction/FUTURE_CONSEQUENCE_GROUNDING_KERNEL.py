#!/usr/bin/env python3
"""Pure treatment-blind grounding kernel for future distinction evidence.

This module does not fetch or run a future release. It consumes externally
produced repeated migration outcomes under the frozen consequence contract and
maps them to future-effect signatures and complete grounding rows.

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
    files: tuple[tuple[str, bytes], ...] | None


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


def _normalize_path(path: str) -> str:
    x = path.replace("\\", "/").strip("/")
    if not x or x == ".." or x.startswith("../") or "/../" in x:
        raise ValueError("invalid relative file path")
    return x


def _run_files(run: MigrationRun) -> dict[str, bytes] | None:
    if run.files is None:
        return None
    out: dict[str, bytes] = {}
    for row in run.files:
        if type(row) is not tuple or len(row) != 2:
            return None
        path, data = row
        if type(path) is not str or type(data) is not bytes:
            return None
        try:
            path = _normalize_path(path)
        except ValueError:
            return None
        if path in out:
            return None
        out[path] = data
    return dict(sorted(out.items()))


def _baseline_files(files: Mapping[str, bytes]) -> dict[str, bytes]:
    if type(files) is not dict:
        raise TypeError("baseline filesystem must be dict")
    out: dict[str, bytes] = {}
    for path, data in files.items():
        if type(path) is not str or type(data) is not bytes:
            raise TypeError("baseline filesystem must map str paths to bytes")
        path = _normalize_path(path)
        if path in out:
            raise ValueError("duplicate baseline path")
        out[path] = data
    if not out:
        raise ValueError("baseline filesystem must be nonempty")
    return dict(sorted(out.items()))


def _ptr_token(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def _path(parent: str, token: str) -> str:
    return parent + "/" + _ptr_token(token)


def effect_delta(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    """Return a deterministic future-effect delta, excluding irrelevant prehistory.

    REMOVE records only operation/path. ADD and REPLACE record the resulting
    value. Thus two different pre-states that receive the same future-required
    effect can have the same T_future signature.
    """
    if type(before) is dict and type(after) is dict:
        out: list[dict[str, Any]] = []
        for key in sorted(set(before) | set(after)):
            child = _path(path, str(key))
            if key not in before:
                out.append({"op": "ADD", "path": child, "after": after[key]})
            elif key not in after:
                out.append({"op": "REMOVE", "path": child})
            else:
                out.extend(effect_delta(before[key], after[key], child))
        return out
    if type(before) is list and type(after) is list:
        if before == after:
            return []
        return [{"op": "REPLACE", "path": path or "/", "after": after}]
    if before == after and type(before) is type(after):
        return []
    return [{"op": "REPLACE", "path": path or "/", "after": after}]


def filesystem_effect_delta(baseline_files: Mapping[str, bytes], future_files: Mapping[str, bytes]) -> list[dict[str, Any]]:
    baseline = _baseline_files(baseline_files)
    if type(future_files) is not dict:
        raise TypeError("future filesystem must be dict")
    future: dict[str, bytes] = {}
    for path, data in future_files.items():
        if type(path) is not str or type(data) is not bytes:
            raise TypeError("future filesystem must map str paths to bytes")
        path = _normalize_path(path)
        if path in future:
            raise ValueError("duplicate future path")
        future[path] = data
    future = dict(sorted(future.items()))
    if set(future) != set(baseline):
        raise ValueError("future configuration path set differs from frozen witness")

    out: list[dict[str, Any]] = []
    for file_path in sorted(baseline):
        before = _parse_strict_json(baseline[file_path])
        after = _parse_strict_json(future[file_path])
        file_prefix = "/file/" + _ptr_token(file_path)
        out.extend(effect_delta(before, after, file_prefix))
    return out


def consequence_signature(baseline_files: Mapping[str, bytes], run_1: MigrationRun, run_2: MigrationRun) -> Consequence:
    """Identify one source fact's future migration effect fail-closed."""
    if type(run_1) is not MigrationRun or type(run_2) is not MigrationRun:
        raise TypeError("MigrationRun required")
    baseline = _baseline_files(baseline_files)
    run_maps: list[dict[str, bytes]] = []
    for idx, run in enumerate((run_1, run_2), 1):
        if not run.completed:
            return Consequence(NOT_IDENTIFIED, None, None, f"RUN_{idx}_NOT_COMPLETED")
        if run.exit_code != 0:
            return Consequence(NOT_IDENTIFIED, None, None, f"RUN_{idx}_NONZERO_EXIT")
        files = _run_files(run)
        if files is None:
            return Consequence(NOT_IDENTIFIED, None, None, f"RUN_{idx}_FILES_INVALID")
        if set(files) != set(baseline):
            return Consequence(NOT_IDENTIFIED, None, None, f"RUN_{idx}_PATH_SET_DRIFT")
        run_maps.append(files)

    try:
        canonical_1 = {p: _canonical(_parse_strict_json(b)) for p, b in run_maps[0].items()}
        canonical_2 = {p: _canonical(_parse_strict_json(b)) for p, b in run_maps[1].items()}
        if canonical_1 != canonical_2:
            return Consequence(NOT_IDENTIFIED, None, None, "NONDETERMINISTIC_FUTURE_FILESYSTEM")
        delta_1 = filesystem_effect_delta(baseline, run_maps[0])
        delta_2 = filesystem_effect_delta(baseline, run_maps[1])
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError):
        return Consequence(NOT_IDENTIFIED, None, None, "STRICT_JSON_OR_FILESYSTEM_FAILURE")

    sig_1 = _canonical(delta_1)
    sig_2 = _canonical(delta_2)
    if sig_1 != sig_2:
        return Consequence(NOT_IDENTIFIED, None, None, "NONDETERMINISTIC_EFFECT_DELTA")
    return Consequence(
        IDENTIFIED,
        sig_1,
        hashlib.sha256(sig_1.encode("utf-8")).hexdigest(),
        None,
    )


def ground_status(left: Consequence, right: Consequence) -> str:
    """Ground one future distinction by future-effect equality only."""
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
    expected = {unit["unit_id"] for unit in domain["grounding_units"]}
    if set(status_by_unit) != expected or len(status_by_unit) != len(grounding_rows):
        raise ValueError("grounding rows must cover the complete frozen unit domain exactly once")
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
    """Adjudicate the frozen q-kernel domain without imputing missing rows."""
    statuses = [row["status"] for row in grounding_rows]
    if any(x == DISTINGUISHED for x in statuses):
        return "NONINCLUSION_WITNESS"
    if any(x == NOT_IDENTIFIED for x in statuses):
        return NOT_IDENTIFIED
    if statuses and all(x == EQUIVALENT for x in statuses):
        return "INCLUSION_ON_FROZEN_KERNEL_DOMAIN"
    raise ValueError("unexpected or empty grounding status")
