#!/usr/bin/env python3
"""Domain-agnostic external -> frozen SSI local-input mapper.

This module does not import or execute SSI. It maps only to the derivation-visible
local payload: objects, facts, authority_edges, request.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Literal

Status = Literal["MAPPED", "NOT_EVALUABLE", "CONTRACT_VIOLATION"]

RESERVED_BACKWARD_FLOW_KEYS = {
    "path_consequence",
    "Y_path",
    "certificate_output",
    "Cert_F",
    "psi_output",
    "Psi_F",
    "collision_expectation",
    "desired_diagnosis",
}

TOP_LEVEL_KEYS = {
    "external_transition_id",
    "entities",
    "claims",
    "licenses",
    "action",
    "annotations",
    "path_relations",
}
ENTITY_KEYS = {"external_id", "class", "properties"}
CLAIM_KEYS = {
    "claim_id",
    "predicate",
    "arguments",
    "scope_jurisdiction",
    "source_provenance",
    "standing",
}
LICENSE_KEYS = {
    "edge_id",
    "grantor",
    "grantee",
    "scope_jurisdiction",
    "source_provenance",
    "supporting_claims",
    "allowed_operations",
    "conditions",
    "must_preserve",
}
ACTION_KEYS = {
    "verb",
    "arguments",
    "scope_jurisdiction",
    "recipient",
    "authority_requested",
}

STANDING_NORMALIZATION = {
    "constituted": "CONSTITUTED",
    "CONSTITUTED": "CONSTITUTED",
    "scoped": "SCOPED",
    "SCOPED": "SCOPED",
    "unresolved": "UNRESOLVED",
    "UNRESOLVED": "UNRESOLVED",
    "withdrawn": "WITHDRAWN",
    "WITHDRAWN": "WITHDRAWN",
    "provenance_only": "PROVENANCE_ONLY",
    "PROVENANCE_ONLY": "PROVENANCE_ONLY",
}

REQUIRED_TOP = {"external_transition_id", "entities", "claims", "licenses", "action"}
REQUIRED_ENTITY = {"external_id", "class"}
REQUIRED_CLAIM = {"claim_id", "predicate", "arguments"}
REQUIRED_LICENSE = {
    "edge_id",
    "grantor",
    "grantee",
    "scope_jurisdiction",
    "source_provenance",
    "supporting_claims",
    "allowed_operations",
    "conditions",
    "must_preserve",
}
REQUIRED_ACTION = {"verb", "arguments", "scope_jurisdiction"}


@dataclass(frozen=True)
class MappingResult:
    status: Status
    local_input: dict[str, Any] | None
    reason: str
    audit: tuple[dict[str, str], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "local_input": self.local_input,
            "reason": self.reason,
            "audit": list(self.audit),
        }


def _find_reserved(value: Any, path: str = "$") -> str | None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in RESERVED_BACKWARD_FLOW_KEYS:
                return f"{path}.{key}"
            hit = _find_reserved(child, f"{path}.{key}")
            if hit:
                return hit
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            hit = _find_reserved(child, f"{path}[{idx}]")
            if hit:
                return hit
    return None


def _unknown_keys(obj: dict[str, Any], allowed: set[str]) -> list[str]:
    return sorted(set(obj) - allowed)


def _not_evaluable(reason: str, audit: list[dict[str, str]] | None = None) -> MappingResult:
    return MappingResult("NOT_EVALUABLE", None, reason, tuple(audit or ()))


def _contract_violation(reason: str) -> MappingResult:
    return MappingResult("CONTRACT_VIOLATION", None, reason, ())


def map_transition(external: dict[str, Any]) -> MappingResult:
    if not isinstance(external, dict):
        return _not_evaluable("external transition must be an object")

    reserved = _find_reserved(external)
    if reserved:
        return _contract_violation(
            f"reserved backward-flow key present at {reserved}; B_BACKWARD_FLOW_FIREWALL"
        )

    unknown = _unknown_keys(external, TOP_LEVEL_KEYS)
    if unknown:
        return _not_evaluable(
            f"unknown top-level field(s): {unknown}; B_UNKNOWN_FIELD_FAIL_CLOSED"
        )

    missing = sorted(REQUIRED_TOP - set(external))
    if missing:
        return _not_evaluable(f"missing required top-level field(s): {missing}")

    if external.get("path_relations"):
        return _not_evaluable(
            "non-empty path_relations has no constituted V0.1 local-input route; "
            "B_PATH_RELATION_UNCONSTITUTED"
        )
    if "path_relations" in external and not isinstance(external["path_relations"], list):
        return _not_evaluable("path_relations must be a list when present")

    audit: list[dict[str, str]] = [
        {
            "field": "external_transition_id",
            "disposition": "EXCLUDE_WITH_BASIS",
            "basis": "B_EXTERNAL_RECORD_ID",
        }
    ]

    annotations = external.get("annotations")
    if annotations is not None:
        if not isinstance(annotations, dict):
            return _not_evaluable("annotations must be an object", audit)
        audit.append(
            {
                "field": "annotations",
                "disposition": "EXCLUDE_WITH_BASIS",
                "basis": "B_HUMAN_ANNOTATION",
            }
        )

    entities = external["entities"]
    claims = external["claims"]
    licenses = external["licenses"]
    action = external["action"]
    if not isinstance(entities, list) or not isinstance(claims, list) or not isinstance(licenses, list):
        return _not_evaluable("entities, claims, and licenses must be lists", audit)
    if not isinstance(action, dict):
        return _not_evaluable("action must be an object", audit)

    objects: list[dict[str, Any]] = []
    for i, entity in enumerate(entities):
        if not isinstance(entity, dict):
            return _not_evaluable(f"entities[{i}] must be an object", audit)
        u = _unknown_keys(entity, ENTITY_KEYS)
        m = sorted(REQUIRED_ENTITY - set(entity))
        if u:
            return _not_evaluable(f"unknown entities[{i}] field(s): {u}", audit)
        if m:
            return _not_evaluable(f"missing entities[{i}] field(s): {m}", audit)
        out = {"id": deepcopy(entity["external_id"]), "type": deepcopy(entity["class"])}
        if "properties" in entity:
            if not isinstance(entity["properties"], dict):
                return _not_evaluable(f"entities[{i}].properties must be an object", audit)
            out["attributes"] = deepcopy(entity["properties"])
        objects.append(out)

    facts: list[dict[str, Any]] = []
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            return _not_evaluable(f"claims[{i}] must be an object", audit)
        u = _unknown_keys(claim, CLAIM_KEYS)
        m = sorted(REQUIRED_CLAIM - set(claim))
        if u:
            return _not_evaluable(f"unknown claims[{i}] field(s): {u}", audit)
        if m:
            return _not_evaluable(f"missing claims[{i}] field(s): {m}", audit)
        out = {
            "id": deepcopy(claim["claim_id"]),
            "kind": deepcopy(claim["predicate"]),
            "args": deepcopy(claim["arguments"]),
        }
        if "scope_jurisdiction" in claim:
            out["jurisdiction"] = deepcopy(claim["scope_jurisdiction"])
        if "source_provenance" in claim:
            out["provenance"] = deepcopy(claim["source_provenance"])
        if "standing" in claim:
            standing = claim["standing"]
            if standing not in STANDING_NORMALIZATION:
                return _not_evaluable(
                    f"claims[{i}].standing has no frozen normalization: {standing!r}", audit
                )
            out["authority"] = STANDING_NORMALIZATION[standing]
        facts.append(out)

    authority_edges: list[dict[str, Any]] = []
    for i, license_ in enumerate(licenses):
        if not isinstance(license_, dict):
            return _not_evaluable(f"licenses[{i}] must be an object", audit)
        u = _unknown_keys(license_, LICENSE_KEYS)
        m = sorted(REQUIRED_LICENSE - set(license_))
        if u:
            return _not_evaluable(f"unknown licenses[{i}] field(s): {u}", audit)
        if m:
            return _not_evaluable(f"missing licenses[{i}] field(s): {m}", audit)
        authority_edges.append(
            {
                "id": deepcopy(license_["edge_id"]),
                "source": deepcopy(license_["grantor"]),
                "target": deepcopy(license_["grantee"]),
                "jurisdiction": deepcopy(license_["scope_jurisdiction"]),
                "provenance": deepcopy(license_["source_provenance"]),
                "evidence": deepcopy(license_["supporting_claims"]),
                "scope": deepcopy(license_["allowed_operations"]),
                "preconditions": deepcopy(license_["conditions"]),
                "preservation": deepcopy(license_["must_preserve"]),
            }
        )

    u = _unknown_keys(action, ACTION_KEYS)
    m = sorted(REQUIRED_ACTION - set(action))
    if u:
        return _not_evaluable(f"unknown action field(s): {u}", audit)
    if m:
        return _not_evaluable(f"missing action field(s): {m}", audit)
    request = {
        "operation": deepcopy(action["verb"]),
        "args": deepcopy(action["arguments"]),
        "jurisdiction": deepcopy(action["scope_jurisdiction"]),
    }
    if "recipient" in action:
        request["consumer"] = deepcopy(action["recipient"])
    if "authority_requested" in action:
        request["requested_authority"] = deepcopy(action["authority_requested"])

    audit.extend(
        [
            {"field": "entities", "disposition": "NORMALIZE", "basis": "B_SCHEMA_OBJECT"},
            {"field": "claims", "disposition": "NORMALIZE", "basis": "B_SCHEMA_FACT"},
            {"field": "licenses", "disposition": "NORMALIZE", "basis": "B_SCHEMA_AUTHORITY_EDGE"},
            {"field": "action", "disposition": "NORMALIZE", "basis": "B_SCHEMA_REQUEST"},
        ]
    )
    return MappingResult(
        "MAPPED",
        {
            "objects": objects,
            "facts": facts,
            "authority_edges": authority_edges,
            "request": request,
        },
        "mapped under frozen V0.1 jurisdiction",
        tuple(audit),
    )
