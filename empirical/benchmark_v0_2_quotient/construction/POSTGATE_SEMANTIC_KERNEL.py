#!/usr/bin/env python3
"""Reference-based post-gate semantic kernel for VFA-0.2.

Construction-side only. This module does not read a future obligation, activate G,
or assign semantics to raw Gamma labels/statistics. Gamma is used only as an
equivalence relation over canonical semantic references.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

ALLOWED_RELATIONS = frozenset({"PROVENANCE", "CHALLENGE", "ALTERNATIVE", "REOPEN"})
ALLOWED_STATUS = frozenset({"DISTINGUISHED", "EQUIVALENT", "NOT_IDENTIFIED"})


@dataclass(frozen=True, order=True, slots=True)
class SemanticRef:
    relation_kind: str
    source_fact_id: str

    def __post_init__(self):
        if self.relation_kind not in ALLOWED_RELATIONS:
            raise ValueError("undeclared relation kind")
        if type(self.source_fact_id) is not str or not self.source_fact_id:
            raise TypeError("source_fact_id required")

    @property
    def key(self) -> str:
        return f"{self.relation_kind}|{self.source_fact_id}"


@dataclass(frozen=True, slots=True)
class RevisionPartition:
    refs: tuple[SemanticRef, ...]
    block_by_ref: tuple[tuple[str, tuple[str, ...]], ...]

    def block(self, ref: SemanticRef) -> tuple[str, ...]:
        table = dict(self.block_by_ref)
        try:
            return table[ref.key]
        except KeyError as e:
            raise KeyError("semantic reference not in partition") from e


@dataclass(frozen=True, order=True, slots=True)
class Probe:
    operation: str
    relation_kind: str
    left_block: tuple[str, ...]
    right_block: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DistinctionRow:
    left: SemanticRef
    right: SemanticRef
    status: str

    def __post_init__(self):
        if self.status not in ALLOWED_STATUS:
            raise ValueError("invalid distinction status")
        if self.left == self.right:
            raise ValueError("distinction pair requires two references")
        if self.left.relation_kind != self.right.relation_kind:
            raise ValueError("COMPARE is licensed only within one relation kind")

    @property
    def pair_key(self) -> tuple[str, str]:
        return tuple(sorted((self.left.key, self.right.key)))


def semantic_ref(record: dict[str, Any]) -> SemanticRef:
    """Raw path_id is intentionally ignored as representation metadata."""
    return SemanticRef(record["relation_kind"], record["source_fact_id"])


def canonical_partition(gamma: dict[str, Any]) -> RevisionPartition:
    """Compile Gamma to a label-free partition over semantic references.

    Raw equivalence labels are consumed only through equality grouping. Their
    spelling, ordering, and namespace carry no semantics.
    """
    if type(gamma) is not dict:
        raise TypeError("Gamma must be a dict")
    records = gamma.get("path_records")
    eq = gamma.get("equivalence_class")
    if type(records) is not list or type(eq) is not dict:
        raise TypeError("invalid Gamma shape")

    semantic_for_path: dict[str, SemanticRef] = {}
    for record in records:
        if type(record) is not dict:
            raise TypeError("invalid path record")
        path_id = record.get("path_id")
        if type(path_id) is not str or not path_id:
            raise TypeError("path_id required at representation boundary")
        if path_id in semantic_for_path:
            raise ValueError("duplicate path_id")
        semantic_for_path[path_id] = semantic_ref(record)

    if set(semantic_for_path) != set(eq):
        raise ValueError("equivalence domain mismatch")
    refs = tuple(sorted(semantic_for_path.values()))
    if len(refs) != len(set(refs)):
        raise ValueError("semantic references must be unique")

    by_label: dict[str, list[SemanticRef]] = {}
    for path_id, ref in semantic_for_path.items():
        label = eq[path_id]
        if type(label) is not str:
            raise TypeError("raw equivalence labels must be strings")
        by_label.setdefault(label, []).append(ref)

    block_for_key: dict[str, tuple[str, ...]] = {}
    for members in by_label.values():
        kinds = {x.relation_kind for x in members}
        if len(kinds) != 1:
            raise ValueError("revision block may not cross relation kinds")
        block = tuple(sorted(x.key for x in members))
        for ref in members:
            block_for_key[ref.key] = block

    return RevisionPartition(
        refs=refs,
        block_by_ref=tuple(sorted(block_for_key.items())),
    )


def _unary_probe(operation: str, required_relation: str, partition: RevisionPartition, ref: SemanticRef) -> Probe:
    if ref.relation_kind != required_relation:
        raise ValueError(f"{operation} requires {required_relation} reference")
    return Probe(operation, ref.relation_kind, partition.block(ref))


def trace(partition: RevisionPartition, ref: SemanticRef) -> Probe:
    return _unary_probe("TRACE", "PROVENANCE", partition, ref)


def follow(partition: RevisionPartition, ref: SemanticRef) -> Probe:
    return _unary_probe("FOLLOW", "ALTERNATIVE", partition, ref)


def challenge(partition: RevisionPartition, ref: SemanticRef) -> Probe:
    return _unary_probe("CHALLENGE", "CHALLENGE", partition, ref)


def reopen(partition: RevisionPartition, ref: SemanticRef) -> Probe:
    return _unary_probe("REOPEN", "REOPEN", partition, ref)


def compare(partition: RevisionPartition, left: SemanticRef, right: SemanticRef) -> Probe | None:
    """Licensed distinction operation. No class-count or density statistic is read."""
    if left.relation_kind != right.relation_kind:
        raise ValueError("COMPARE requires one relation kind")
    a = partition.block(left)
    b = partition.block(right)
    if a == b:
        return None
    x, y = sorted((a, b))
    return Probe("COMPARE", left.relation_kind, x, y)


def split(*_args, **_kwargs):
    raise PermissionError("SPLIT is not licensed at the first post-gate endpoint")


def evaluate_pair_reachability(
    partition: RevisionPartition,
    rows: Iterable[DistinctionRow],
) -> tuple[dict[str, Any], ...]:
    """Representation-invariant V_Pi over a grounded future-distinction table."""
    out = []
    seen = set()
    for row in rows:
        if row.pair_key in seen:
            raise ValueError("duplicate future-distinction pair")
        seen.add(row.pair_key)
        if row.status == "NOT_IDENTIFIED":
            reachable = None
            probe = None
        elif row.status == "EQUIVALENT":
            reachable = False
            probe = None
        else:
            probe = compare(partition, row.left, row.right)
            reachable = probe is not None
        out.append({
            "pair": row.pair_key,
            "status": row.status,
            "reachable": reachable,
            "probe": None if probe is None else {
                "operation": probe.operation,
                "relation_kind": probe.relation_kind,
                "left_block": probe.left_block,
                "right_block": probe.right_block,
            },
        })
    return tuple(sorted(out, key=lambda x: x["pair"]))
