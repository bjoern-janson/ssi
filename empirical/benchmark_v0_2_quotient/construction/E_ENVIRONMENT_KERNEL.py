#!/usr/bin/env python3
"""Construction-side E environment kernel.

No future obligation is selected, read, or simulated here, and G is never
activated. This module only defines the arm-symmetric treatment exposure and
logical execution-cost contract required by predicate E.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any

PATH_COUNT = 24
MATRIX_SIDE = 24
MATRIX_BYTES = MATRIX_SIDE * MATRIX_SIDE
PAIR_SLOTS = PATH_COUNT * (PATH_COUNT - 1) // 2


@dataclass(frozen=True, slots=True)
class CommonEvidence:
    payload: bytes
    sha256: str

    @classmethod
    def bind(cls, payload: bytes) -> "CommonEvidence":
        if type(payload) is not bytes:
            raise TypeError("common evidence must be bytes")
        return cls(payload=payload, sha256=hashlib.sha256(payload).hexdigest())


@dataclass(frozen=True, slots=True)
class MaterializationTrace:
    path_record_reads: int
    path_sort_items: int
    class_label_lookups: int
    matrix_comparisons: int
    matrix_byte_writes: int
    pair_slots: int
    output_bytes: int


def _validate_gamma(gamma: dict[str, Any]) -> tuple[tuple[str, ...], dict[str, str]]:
    if type(gamma) is not dict:
        raise TypeError("Gamma must be a dict at construction-audit boundary")
    records = gamma.get("path_records")
    classes = gamma.get("equivalence_class")
    if type(records) is not list or len(records) != PATH_COUNT or type(classes) is not dict:
        raise TypeError("invalid Gamma shape")
    ids_raw = tuple(r["path_id"] for r in records)
    if len(set(ids_raw)) != PATH_COUNT or set(ids_raw) != set(classes):
        raise ValueError("Gamma path/class domains must match")
    if not all(type(classes[p]) is str for p in ids_raw):
        raise TypeError("class labels must be strings")
    # Coordinate order is representation-invariant and common to both arms.
    ids = tuple(sorted(ids_raw))
    return ids, classes


def compile_equivalence_matrix(gamma: dict[str, Any]) -> tuple[bytes, MaterializationTrace]:
    """Expose equality structure only; raw class-label values never cross the boundary."""
    ids, classes = _validate_gamma(gamma)
    labels = tuple(classes[p] for p in ids)
    out = bytearray(MATRIX_BYTES)
    k = 0
    comparisons = 0
    writes = 0
    for i in range(PATH_COUNT):
        for j in range(PATH_COUNT):
            out[k] = 1 if labels[i] == labels[j] else 0
            k += 1
            comparisons += 1
            writes += 1
    trace = MaterializationTrace(
        path_record_reads=PATH_COUNT,
        path_sort_items=PATH_COUNT,
        class_label_lookups=PATH_COUNT,
        matrix_comparisons=comparisons,
        matrix_byte_writes=writes,
        pair_slots=PAIR_SLOTS,
        output_bytes=len(out),
    )
    return bytes(out), trace


def scan_pair_slots(matrix: bytes) -> tuple[int, ...]:
    """Fixed 276-slot scan; no topology-dependent early stop or dedup."""
    if type(matrix) is not bytes or len(matrix) != MATRIX_BYTES:
        raise TypeError("fixed 24x24 equivalence matrix required")
    result = []
    for i in range(PATH_COUNT):
        for j in range(i + 1, PATH_COUNT):
            result.append(matrix[i * MATRIX_SIDE + j])
    if len(result) != PAIR_SLOTS:
        raise AssertionError("pair schedule drift")
    return tuple(result)


def arm_exposure(common_evidence: CommonEvidence, matrix: bytes) -> tuple[str, bytes]:
    """Only common-evidence identity and fixed-size treatment matrix cross the boundary."""
    if type(common_evidence) is not CommonEvidence:
        raise TypeError("CommonEvidence required")
    if type(matrix) is not bytes or len(matrix) != MATRIX_BYTES:
        raise TypeError("fixed matrix required")
    return common_evidence.sha256, matrix
