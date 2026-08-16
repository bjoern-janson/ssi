"""Semantic-ABI-bound certificate emission.

This layer deliberately does not interpret execution witnesses as semantic authority.
A certificate's denotation is determined only by its semantic carrier and immutable
ABI reference.  Execution witness and trace remain operational metadata.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Mapping


class SemanticBindingError(ValueError):
    """Raised when a semantic ABI binding is absent, mutable, or inconsistent."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _is_sha256(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def validate_abi_ref(abi_ref: Mapping[str, Any]) -> dict[str, str]:
    """Return a normalized immutable ABI reference or reject the binding."""
    if not isinstance(abi_ref, Mapping):
        raise SemanticBindingError("SEMANTIC_ABI_BINDING_REQUIRED")
    if "alias" in abi_ref:
        raise SemanticBindingError("MUTABLE_ALIAS_NOT_VALID_SEMANTIC_BINDING")
    namespace = abi_ref.get("namespace")
    identity = abi_ref.get("immutable_manifest_sha256")
    if not isinstance(namespace, str) or not namespace or not _is_sha256(identity):
        raise SemanticBindingError("SEMANTIC_ABI_BINDING_REQUIRED")
    return {"namespace": namespace, "immutable_manifest_sha256": identity}


def admit_immutable_abi_binding(
    *,
    runtime_semantic_abi_id: str,
    runtime_lineage: Mapping[str, str],
    binding_record: Mapping[str, Any],
) -> dict[str, str]:
    """Admit a symbolic runtime ABI id to one immutable ABIRef.

    Admission is by exact frozen lineage equality, never by a mutable alias or name.
    The binding record is expected to contain evidence entries with both the runtime
    contract hash and the immutable ABI hash for every lineage field supplied here.
    """
    if binding_record.get("runtime_semantic_abi_id") != runtime_semantic_abi_id:
        raise SemanticBindingError("SEMANTIC_ABI_BINDING_MISMATCH")
    if binding_record.get("mutable_alias_admissible_as_bridge") is not False:
        raise SemanticBindingError("MUTABLE_ALIAS_NOT_VALID_SEMANTIC_BINDING")

    evidence = binding_record.get("evidence")
    if not isinstance(evidence, Mapping):
        raise SemanticBindingError("SEMANTIC_ABI_LINEAGE_MISMATCH")
    for field, runtime_hash in runtime_lineage.items():
        item = evidence.get(field)
        if not isinstance(item, Mapping):
            raise SemanticBindingError("SEMANTIC_ABI_LINEAGE_MISMATCH")
        if item.get("runtime_contract") != runtime_hash or item.get("A1") != runtime_hash:
            raise SemanticBindingError("SEMANTIC_ABI_LINEAGE_MISMATCH")

    return validate_abi_ref(binding_record.get("immutable_abi_ref", {}))


def emit_certificate(
    *,
    runtime_judgment: bool,
    abi_ref: Mapping[str, Any],
    carrier_kind: str,
    coordinates: Mapping[str, Any],
    selected_execution_witness: Any = None,
    trace: Any = None,
) -> dict[str, Any]:
    """Emit a certificate without coercing the execution witness into semantics."""
    ref = validate_abi_ref(abi_ref)
    if not isinstance(carrier_kind, str) or not carrier_kind:
        raise ValueError("SEMANTIC_CARRIER_KIND_REQUIRED")
    if not isinstance(coordinates, Mapping):
        raise ValueError("SEMANTIC_CARRIER_COORDINATES_REQUIRED")

    witness = None
    if selected_execution_witness is not None:
        witness = {
            "value": deepcopy(selected_execution_witness),
            "authority_type": "OPERATIONAL_TRACE_ONLY",
        }

    return {
        "runtime_judgment": bool(runtime_judgment),
        "semantic_carrier": {
            "kind": carrier_kind,
            "abi_ref": ref,
            "coordinates": deepcopy(dict(coordinates)),
        },
        "selected_execution_witness": witness,
        "trace": deepcopy(trace),
    }


def replay_certificate(
    certificate: Mapping[str, Any],
    decode_semantic_carrier: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> dict[str, Any]:
    """Replay through the semantic carrier only.

    The decoder cannot observe the selected execution witness or trace through this
    interface, which prevents those operational fields from selecting certificate
    meaning.  Lifecycle/current-authority fields returned by the decoder are passed
    through separately from the operational execution metadata.
    """
    carrier = certificate.get("semantic_carrier")
    if not isinstance(carrier, Mapping):
        raise SemanticBindingError("SEMANTIC_CARRIER_REQUIRED")
    # Re-validate at replay so malformed persisted certificates cannot bypass binding.
    validate_abi_ref(carrier.get("abi_ref", {}))
    decoded = dict(decode_semantic_carrier(deepcopy(dict(carrier))))
    decoded["runtime_judgment"] = bool(certificate.get("runtime_judgment"))
    decoded["selected_execution_witness"] = deepcopy(certificate.get("selected_execution_witness"))
    decoded["trace"] = deepcopy(certificate.get("trace"))
    return decoded
