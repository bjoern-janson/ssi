#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Mapping

REPRESENTATION_SUFFICIENT = "REPRESENTATION_SUFFICIENT"
AUTHORIZED_DISTINCTION_LOST = "AUTHORIZED_DISTINCTION_LOST"
REPRESENTATION_NOT_IDENTIFIED = "REPRESENTATION_NOT_IDENTIFIED"


def _canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _not_identified(reason: str, **extra: Any) -> Dict[str, Any]:
    out = {
        "status": REPRESENTATION_NOT_IDENTIFIED,
        "recoverable": None,
        "reason": reason,
        "collisions": [],
    }
    out.update(extra)
    return out


def _audit_partition(*, purpose: str, observable_id: str, samples: Iterable[Mapping[str, Any]], representation_field: str, domain_complete: bool) -> Dict[str, Any]:
    if not isinstance(purpose, str) or not purpose:
        return _not_identified("PURPOSE_NOT_BOUND")
    if not isinstance(observable_id, str) or not observable_id:
        return _not_identified("OBSERVABLE_NOT_CONSTITUTED")

    rows: List[Mapping[str, Any]] = list(samples)
    if not rows:
        return _not_identified("EMPTY_AUDIT_DOMAIN", purpose=purpose, observable_id=observable_id)

    for row in rows:
        if "state_id" not in row:
            return _not_identified("STATE_ID_MISSING", purpose=purpose, observable_id=observable_id)
        if representation_field not in row:
            return _not_identified("REPRESENTATION_VALUE_MISSING", purpose=purpose, observable_id=observable_id, state_id=row.get("state_id"))
        if "observable_value" not in row:
            return _not_identified("OBSERVABLE_VALUE_MISSING", purpose=purpose, observable_id=observable_id, state_id=row.get("state_id"))

    blocks: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        blocks[_canon(row[representation_field])].append(row)

    collisions: List[Dict[str, Any]] = []
    for rep_key, block in blocks.items():
        obs_groups: Dict[str, List[str]] = defaultdict(list)
        obs_values: Dict[str, Any] = {}
        for row in block:
            ok = _canon(row["observable_value"])
            obs_groups[ok].append(str(row["state_id"]))
            obs_values[ok] = row["observable_value"]
        if len(obs_groups) > 1:
            collisions.append({
                "representation_value": json.loads(rep_key),
                "observable_groups": [
                    {"observable_value": obs_values[k], "state_ids": sorted(v)}
                    for k, v in sorted(obs_groups.items())
                ],
            })

    base = {
        "purpose": purpose,
        "observable_id": observable_id,
        "representation_field": representation_field,
        "domain_complete": bool(domain_complete),
        "sample_count": len(rows),
        "representation_block_count": len(blocks),
        "collisions": collisions,
    }

    if collisions:
        return {
            **base,
            "status": AUTHORIZED_DISTINCTION_LOST,
            "recoverable": False,
            "reason": "KERNEL_CONTAINMENT_VIOLATED",
        }

    if not domain_complete:
        return {
            **base,
            "status": REPRESENTATION_NOT_IDENTIFIED,
            "recoverable": None,
            "reason": "AUDIT_DOMAIN_INCOMPLETE",
        }

    return {
        **base,
        "status": REPRESENTATION_SUFFICIENT,
        "recoverable": True,
        "reason": "FINITE_KERNEL_CONTAINMENT_ESTABLISHED",
    }


def check_sufficiency(case: Mapping[str, Any]) -> Dict[str, Any]:
    return _audit_partition(
        purpose=case.get("purpose", ""),
        observable_id=case.get("observable_id", ""),
        samples=case.get("samples", []),
        representation_field="representation_value",
        domain_complete=bool(case.get("domain_complete", False)),
    )


def check_mask_sufficiency(case: Mapping[str, Any]) -> Dict[str, Any]:
    mask_id = case.get("mask_id")
    if not isinstance(mask_id, str) or not mask_id:
        return _not_identified("MASK_NOT_BOUND")
    out = _audit_partition(
        purpose=case.get("purpose", ""),
        observable_id=case.get("observable_id", ""),
        samples=case.get("samples", []),
        representation_field="masked_representation_value",
        domain_complete=bool(case.get("domain_complete", False)),
    )
    out["mask_id"] = mask_id
    return out


def evaluate(case: Mapping[str, Any]) -> Dict[str, Any]:
    op = case.get("operation")
    if op == "CHECK_SUFFICIENCY":
        return check_sufficiency(case)
    if op == "CHECK_MASK_SUFFICIENCY":
        return check_mask_sufficiency(case)
    return _not_identified("OPERATION_NOT_IMPLEMENTED", operation=op)
