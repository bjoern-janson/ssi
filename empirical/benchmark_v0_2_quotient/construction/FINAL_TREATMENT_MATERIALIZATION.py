#!/usr/bin/env python3
"""Trusted treatment materialization in common semantic coordinates.

Raw Gamma path IDs and raw class-label values terminate here. The output is the
same fixed 24x24 equality matrix shape used by predicate E, but its coordinates
are defined by the common semantic coordinate map rather than raw path-ID sort.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

PATH_COUNT = 24
MATRIX_SIDE = 24
MATRIX_BYTES = 576


@dataclass(frozen=True, slots=True)
class MaterializationTrace:
    path_record_reads: int
    semantic_coordinate_lookups: int
    class_label_lookups: int
    matrix_comparisons: int
    matrix_writes: int
    output_bytes: int


def _semantic_key(record: Mapping[str, Any]) -> str:
    if type(record) is not dict:
        raise TypeError("path record must be dict")
    kind = record.get("relation_kind")
    fact = record.get("source_fact_id")
    if type(kind) is not str or type(fact) is not str or not kind or not fact:
        raise TypeError("semantic fields required")
    return f"{kind}|{fact}"


def compile_semantic_matrix(gamma: dict[str, Any], coordinate_map: dict[str, int]) -> tuple[bytes, MaterializationTrace]:
    if type(gamma) is not dict or type(coordinate_map) is not dict:
        raise TypeError("dict inputs required")
    records = gamma.get("path_records")
    classes = gamma.get("equivalence_class")
    if type(records) is not list or len(records) != PATH_COUNT or type(classes) is not dict:
        raise TypeError("invalid Gamma shape")
    if set(coordinate_map.values()) != set(range(PATH_COUNT)) or len(coordinate_map) != PATH_COUNT:
        raise ValueError("coordinate map must be a bijection onto 0..23")

    label_by_coordinate: list[str | None] = [None] * PATH_COUNT
    seen_path_ids = set()
    seen_semantic = set()
    for record in records:
        path_id = record.get("path_id")
        if type(path_id) is not str or not path_id or path_id in seen_path_ids:
            raise ValueError("unique path_id required")
        seen_path_ids.add(path_id)
        if path_id not in classes or type(classes[path_id]) is not str:
            raise ValueError("equivalence label required for every path")
        semantic = _semantic_key(record)
        if semantic in seen_semantic or semantic not in coordinate_map:
            raise ValueError("semantic reference domain mismatch")
        seen_semantic.add(semantic)
        label_by_coordinate[coordinate_map[semantic]] = classes[path_id]

    if seen_semantic != set(coordinate_map) or set(classes) != seen_path_ids:
        raise ValueError("Gamma and semantic coordinate domains must match exactly")
    if any(x is None for x in label_by_coordinate):
        raise AssertionError("unfilled semantic coordinate")

    labels = tuple(label_by_coordinate)
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

    return bytes(out), MaterializationTrace(
        path_record_reads=PATH_COUNT,
        semantic_coordinate_lookups=PATH_COUNT,
        class_label_lookups=PATH_COUNT,
        matrix_comparisons=comparisons,
        matrix_writes=writes,
        output_bytes=len(out),
    )
