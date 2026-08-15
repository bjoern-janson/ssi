#!/usr/bin/env python3
"""Final candidate post-gate runtime for the first reachability endpoint.

The runtime receives only:
- the common semantic coordinate map,
- the fixed 576-byte treatment matrix,
- the frozen grounding domain,
- the common grounded future-distinction surface rows.

It never receives raw Gamma, raw path IDs, raw equivalence labels, or an arm ID.
Every run scans all 276 unordered semantic-coordinate pairs before reading the
12 target q-kernel surfaces, preserving the predicate-E logical schedule.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PATH_COUNT = 24
MATRIX_SIDE = 24
MATRIX_BYTES = 576
PAIR_SLOTS = PATH_COUNT * (PATH_COUNT - 1) // 2
ALLOWED_STATUS = frozenset({"DISTINGUISHED", "EQUIVALENT", "NOT_IDENTIFIED"})


@dataclass(frozen=True, slots=True)
class RuntimeTrace:
    matrix_bytes_read: int
    pair_slots_scanned: int
    target_surfaces_read: int
    probe_slots_emitted: int


def _key(ref: list[str]) -> str:
    if type(ref) is not list or len(ref) != 2 or not all(type(x) is str and x for x in ref):
        raise TypeError("semantic reference must be [relation_kind, source_fact_id]")
    return f"{ref[0]}|{ref[1]}"


def _validate_coordinates(coordinates: dict[str, int]) -> None:
    if type(coordinates) is not dict or len(coordinates) != PATH_COUNT:
        raise TypeError("24-entry coordinate map required")
    if set(coordinates.values()) != set(range(PATH_COUNT)):
        raise ValueError("coordinate map must be bijective onto 0..23")


def scan_all_pair_slots(matrix: bytes) -> dict[tuple[int, int], int]:
    if type(matrix) is not bytes or len(matrix) != MATRIX_BYTES:
        raise TypeError("fixed 24x24 matrix required")
    out: dict[tuple[int, int], int] = {}
    for i in range(PATH_COUNT):
        for j in range(i + 1, PATH_COUNT):
            out[(i, j)] = matrix[i * MATRIX_SIDE + j]
    if len(out) != PAIR_SLOTS:
        raise AssertionError("pair schedule drift")
    return out


def evaluate_first_endpoint(
    matrix: bytes,
    coordinates: dict[str, int],
    domain: dict[str, Any],
    grounded_surfaces: list[dict[str, Any]],
) -> tuple[tuple[dict[str, Any], ...], RuntimeTrace]:
    """Evaluate grounded q-kernel reachability with fixed arm-symmetric cost."""
    _validate_coordinates(coordinates)
    pair_scan = scan_all_pair_slots(matrix)
    expected = {
        (
            surface["unit_id"], surface["relation_kind"],
            tuple(surface["left_ref"]), tuple(surface["right_ref"]),
        )
        for surface in domain["path_surfaces"]
    }
    if len(expected) != 12:
        raise ValueError("frozen domain must contain exactly 12 unique path surfaces")

    rows = {}
    for row in grounded_surfaces:
        ident = (
            row["unit_id"], row["relation_kind"],
            tuple(row["left_ref"]), tuple(row["right_ref"]),
        )
        if ident in rows:
            raise ValueError("duplicate grounded path surface")
        if row.get("status") not in ALLOWED_STATUS:
            raise ValueError("invalid grounded status")
        rows[ident] = row["status"]
    if set(rows) != expected:
        raise ValueError("grounded surfaces must exactly cover frozen q-kernel domain")

    out = []
    emitted = 0
    for ident in sorted(expected):
        unit_id, relation_kind, left_ref, right_ref = ident
        left = list(left_ref)
        right = list(right_ref)
        if left[0] != relation_kind or right[0] != relation_kind:
            raise ValueError("surface relation-kind mismatch")
        lk = _key(left)
        rk = _key(right)
        if lk not in coordinates or rk not in coordinates:
            raise ValueError("semantic reference absent from coordinate map")
        i, j = sorted((coordinates[lk], coordinates[rk]))
        status = rows[ident]
        same_block = pair_scan[(i, j)] == 1
        if status == "NOT_IDENTIFIED":
            reachable = None
            probe_id = None
        elif status == "EQUIVALENT":
            reachable = False
            probe_id = None
        else:
            reachable = not same_block
            probe_id = None if not reachable else "COMPARE|" + relation_kind + "|" + "|".join(sorted((lk, rk)))
            if probe_id is not None:
                emitted += 1
        out.append({
            "unit_id": unit_id,
            "relation_kind": relation_kind,
            "left_ref": left,
            "right_ref": right,
            "status": status,
            "reachable": reachable,
            "probe_id": probe_id,
        })

    return tuple(out), RuntimeTrace(
        matrix_bytes_read=MATRIX_BYTES,
        pair_slots_scanned=PAIR_SLOTS,
        target_surfaces_read=len(expected),
        probe_slots_emitted=emitted,
    )
