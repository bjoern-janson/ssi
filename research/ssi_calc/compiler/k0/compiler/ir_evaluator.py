#!/usr/bin/env python3
"""Independent executor for frozen SSI-IR/K0-STLC-v0.1 artifacts.

The evaluator consumes compiled queries and an IR contract. It does not import
the source reference checker or source gold judgments.
"""

from __future__ import annotations
import copy
import json


class IRReject(Exception):
    def __init__(self, witness):
        super().__init__(json.dumps(witness, sort_keys=True))
        self.witness = witness


def rules_by_kind(ir):
    return {r["term_kind"]: r for r in ir["rules"]}


def type_equal(a, b, ir):
    policy = ir["type_system"]["equality"]
    if policy == "STRUCTURAL_EXACT":
        return a == b
    if policy == "COLLAPSE_BOOL_ARROW":
        return True
    raise ValueError(f"unknown type equality policy: {policy}")


def lookup(context, name, ir):
    policy = ir["context"]["lookup"]
    if policy == "DISABLED":
        raise IRReject({
            "code": "UNBOUND_VARIABLE",
            "variable": name,
            "compiler_boundary_hint": "CONTEXT_LOOKUP_DISABLED",
        })
    if policy != "LATEST_EXACT_VARIABLE_NAME":
        raise ValueError(f"unknown context lookup policy: {policy}")

    for binding in reversed(context):
        if binding["variable"] == name:
            return copy.deepcopy(binding["type"]), {
                "kind": "CONTEXT_BINDING",
                "variable": name,
                "type": copy.deepcopy(binding["type"]),
            }
    raise IRReject({"code": "UNBOUND_VARIABLE", "variable": name})


def trace(rule, context, term, ty, premises, evidence=None):
    return {
        "ir_rule": rule["id"],
        "source_rule_ancestor": rule.get("source_rule"),
        "judgment": {
            "context": copy.deepcopy(context),
            "term": copy.deepcopy(term),
            "type": copy.deepcopy(ty),
        },
        "premises": premises,
        "evidence": evidence or [],
    }


def synth(term, context, ir):
    rules = rules_by_kind(ir)
    kind = term["kind"]
    if kind not in rules:
        raise IRReject({"code": "IR_TERM_KIND_UNSUPPORTED", "term_kind": kind})

    rule = rules[kind]
    opcode = rule["opcode"]
    req = set(rule.get("requirements", []))

    if opcode == "CONST_BOOL":
        ty = {"kind": "BOOL"}
        return ty, trace(rule, context, term, ty, [])

    if opcode == "LOOKUP":
        ty, ev = lookup(context, term["name"], ir)
        return ty, trace(rule, context, term, ty, [], [ev])

    if opcode == "ABS_EXTEND":
        if ir["context"]["extension"] != "APPEND_BINDING_SHADOWS_EARLIER":
            raise ValueError("unsupported context extension policy")
        context2 = list(copy.deepcopy(context))
        binding = {
            "variable": term["binder"],
            "type": copy.deepcopy(term["binder_type"]),
        }
        context2.append(binding)
        try:
            body_ty, body_trace = synth(term["body"], context2, ir)
        except IRReject as exc:
            raise IRReject({
                "code": exc.witness["code"],
                "rule_frontier": rule["id"],
                "nested": exc.witness,
            })
        ty = {
            "kind": "ARROW",
            "domain": copy.deepcopy(term["binder_type"]),
            "codomain": body_ty,
        }
        return ty, trace(rule, context, term, ty, [body_trace], [{
            "kind": "CONTEXT_EXTENSION",
            **binding,
        }])

    if opcode == "APP_ARROW":
        try:
            fn_ty, fn_trace = synth(term["function"], context, ir)
        except IRReject as exc:
            raise IRReject({
                "code": exc.witness["code"],
                "rule_frontier": f'{rule["id"]}.function',
                "nested": exc.witness,
            })

        if "FUNCTION_HAS_ARROW_TYPE" in req and fn_ty.get("kind") != "ARROW":
            raise IRReject({
                "code": "APPLICATION_NON_FUNCTION",
                "rule_frontier": rule["id"],
                "function_type": fn_ty,
            })

        if fn_ty.get("kind") != "ARROW":
            # This branch is reachable only in a deliberately mutated IR that
            # removed the source Arrow prerequisite.
            domain = {"kind": "BOOL"}
            codomain = {"kind": "BOOL"}
        else:
            domain = fn_ty["domain"]
            codomain = fn_ty["codomain"]

        try:
            arg_ty, arg_trace = synth(term["argument"], context, ir)
        except IRReject as exc:
            raise IRReject({
                "code": exc.witness["code"],
                "rule_frontier": f'{rule["id"]}.argument',
                "nested": exc.witness,
            })

        if (
            "ARGUMENT_MATCHES_ARROW_DOMAIN" in req
            and not type_equal(arg_ty, domain, ir)
        ):
            raise IRReject({
                "code": "APPLICATION_ARGUMENT_TYPE_MISMATCH",
                "rule_frontier": rule["id"],
                "required": domain,
                "observed": arg_ty,
            })

        return codomain, trace(rule, context, term, codomain, [fn_trace, arg_trace])

    if opcode == "IF_BOOL_BRANCH_EQ":
        try:
            guard_ty, guard_trace = synth(term["guard"], context, ir)
        except IRReject as exc:
            raise IRReject({
                "code": exc.witness["code"],
                "rule_frontier": f'{rule["id"]}.guard',
                "nested": exc.witness,
            })

        bool_ty = {"kind": "BOOL"}
        if "GUARD_HAS_BOOL_TYPE" in req and not type_equal(guard_ty, bool_ty, ir):
            raise IRReject({
                "code": "IF_GUARD_NOT_BOOL",
                "rule_frontier": rule["id"],
                "observed": guard_ty,
            })

        try:
            then_ty, then_trace = synth(term["then_branch"], context, ir)
            else_ty, else_trace = synth(term["else_branch"], context, ir)
        except IRReject as exc:
            raise IRReject({
                "code": exc.witness["code"],
                "rule_frontier": rule["id"],
                "nested": exc.witness,
            })

        if "BRANCH_TYPES_EQUAL" in req and not type_equal(then_ty, else_ty, ir):
            raise IRReject({
                "code": "IF_BRANCH_TYPE_MISMATCH",
                "rule_frontier": rule["id"],
                "then_type": then_ty,
                "else_type": else_ty,
            })

        return then_ty, trace(
            rule, context, term, then_ty, [guard_trace, then_trace, else_trace]
        )

    raise ValueError(f"unknown IR opcode: {opcode}")


def evaluate_query(query, ir):
    fabricated = []
    if ir.get("justification", {}).get("inject_fabricated_node"):
        fabricated.append({
            "ir_rule": "IR-FABRICATED-AUTHORITY",
            "source_rule_ancestor": None,
            "claim": "synthetic justification edge inserted by hostile mutation",
        })

    try:
        inferred, derivation = synth(query["term"], query["context"], ir)
        licensed = type_equal(inferred, query["expected_type"], ir)
        if licensed:
            return {
                "source_case_id": query["source_case_id"],
                "status": "JUDGMENT_LICENSED",
                "judgment": True,
                "inferred_type": inferred,
                "derivation": derivation,
                "rejection": None,
                "fabricated_justification": fabricated,
            }
        return {
            "source_case_id": query["source_case_id"],
            "status": "JUDGMENT_REJECTED",
            "judgment": False,
            "inferred_type": inferred,
            "derivation": derivation,
            "rejection": {
                "code": "EXPECTED_TYPE_MISMATCH",
                "required": query["expected_type"],
                "observed": inferred,
                "rule_frontier": "IR_QUERY_TYPE_CHECK",
            },
            "fabricated_justification": fabricated,
        }
    except IRReject as exc:
        return {
            "source_case_id": query["source_case_id"],
            "status": "JUDGMENT_REJECTED",
            "judgment": False,
            "inferred_type": None,
            "derivation": None,
            "rejection": exc.witness,
            "fabricated_justification": fabricated,
        }
