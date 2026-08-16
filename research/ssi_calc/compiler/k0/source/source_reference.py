#!/usr/bin/env python3
"""Independent source-level checker for the frozen K0 STLC contract.

This module implements only the source calculus frozen in this directory.
It does not import SSI-CALC, any K0 compiler, or any SSI-IR evaluator.
"""

from __future__ import annotations
import copy
import json
from pathlib import Path

BOOL = {"tag": "Bool"}


def arrow(a, b):
    return {"tag": "Arrow", "from": a, "to": b}


def judgment(ctx, term, ty):
    return {"context": copy.deepcopy(ctx), "term": copy.deepcopy(term), "type": copy.deepcopy(ty)}


class SourceReject(Exception):
    def __init__(self, witness):
        super().__init__(json.dumps(witness, sort_keys=True))
        self.witness = witness


def synth(term, env):
    tag = term["tag"]

    if tag == "True":
        return BOOL, {"rule": "T_Tru", "judgment": judgment(env, term, BOOL), "premises": []}

    if tag == "False":
        return BOOL, {"rule": "T_Fls", "judgment": judgment(env, term, BOOL), "premises": []}

    if tag == "Var":
        name = term["name"]
        if name not in env:
            raise SourceReject({
                "code": "UNBOUND_VARIABLE",
                "term": copy.deepcopy(term),
                "variable": name,
                "context": copy.deepcopy(env),
            })
        ty = env[name]
        return ty, {
            "rule": "T_Var",
            "judgment": judgment(env, term, ty),
            "premises": [],
            "lookup": {"variable": name, "type": copy.deepcopy(ty)},
        }

    if tag == "Abs":
        env2 = dict(env)
        env2[term["param"]] = term["param_type"]
        try:
            body_ty, body_proof = synth(term["body"], env2)
        except SourceReject as exc:
            raise SourceReject({
                "code": exc.witness["code"],
                "rule_frontier": "T_Abs",
                "parameter": term["param"],
                "parameter_type": copy.deepcopy(term["param_type"]),
                "nested": exc.witness,
            })
        result_ty = arrow(term["param_type"], body_ty)
        return result_ty, {
            "rule": "T_Abs",
            "judgment": judgment(env, term, result_ty),
            "premises": [body_proof],
            "context_extension": {
                "variable": term["param"],
                "type": copy.deepcopy(term["param_type"]),
            },
        }

    if tag == "App":
        try:
            fn_ty, fn_proof = synth(term["fn"], env)
        except SourceReject as exc:
            raise SourceReject({
                "code": exc.witness["code"],
                "rule_frontier": "T_App.fn",
                "nested": exc.witness,
            })

        if fn_ty.get("tag") != "Arrow":
            raise SourceReject({
                "code": "APPLICATION_NON_FUNCTION",
                "rule_frontier": "T_App",
                "function_type": copy.deepcopy(fn_ty),
                "term": copy.deepcopy(term["fn"]),
            })

        try:
            arg_ty, arg_proof = synth(term["arg"], env)
        except SourceReject as exc:
            raise SourceReject({
                "code": exc.witness["code"],
                "rule_frontier": "T_App.arg",
                "nested": exc.witness,
            })

        if arg_ty != fn_ty["from"]:
            raise SourceReject({
                "code": "APPLICATION_ARGUMENT_TYPE_MISMATCH",
                "rule_frontier": "T_App",
                "required": copy.deepcopy(fn_ty["from"]),
                "observed": copy.deepcopy(arg_ty),
            })

        result_ty = fn_ty["to"]
        return result_ty, {
            "rule": "T_App",
            "judgment": judgment(env, term, result_ty),
            "premises": [fn_proof, arg_proof],
        }

    if tag == "If":
        try:
            cond_ty, cond_proof = synth(term["cond"], env)
        except SourceReject as exc:
            raise SourceReject({
                "code": exc.witness["code"],
                "rule_frontier": "T_Test.cond",
                "nested": exc.witness,
            })

        if cond_ty != BOOL:
            raise SourceReject({
                "code": "IF_GUARD_NOT_BOOL",
                "rule_frontier": "T_Test",
                "observed": copy.deepcopy(cond_ty),
            })

        try:
            then_ty, then_proof = synth(term["then"], env)
        except SourceReject as exc:
            raise SourceReject({
                "code": exc.witness["code"],
                "rule_frontier": "T_Test.then",
                "nested": exc.witness,
            })

        try:
            else_ty, else_proof = synth(term["else"], env)
        except SourceReject as exc:
            raise SourceReject({
                "code": exc.witness["code"],
                "rule_frontier": "T_Test.else",
                "nested": exc.witness,
            })

        if then_ty != else_ty:
            raise SourceReject({
                "code": "IF_BRANCH_TYPE_MISMATCH",
                "rule_frontier": "T_Test",
                "then_type": copy.deepcopy(then_ty),
                "else_type": copy.deepcopy(else_ty),
            })

        return then_ty, {
            "rule": "T_Test",
            "judgment": judgment(env, term, then_ty),
            "premises": [cond_proof, then_proof, else_proof],
        }

    raise ValueError(f"unknown source term tag: {tag}")


def adjudicate(case):
    try:
        inferred, derivation = synth(case["term"], case["context"])
        if inferred == case["expected_type"]:
            return {
                "id": case["id"],
                "judgment": True,
                "inferred_type": inferred,
                "derivation": derivation,
                "rejection": None,
            }
        return {
            "id": case["id"],
            "judgment": False,
            "inferred_type": inferred,
            "derivation": derivation,
            "rejection": {
                "code": "EXPECTED_TYPE_MISMATCH",
                "required": case["expected_type"],
                "observed": inferred,
                "rule_frontier": "QUERY_TYPE_CHECK",
            },
        }
    except SourceReject as exc:
        return {
            "id": case["id"],
            "judgment": False,
            "inferred_type": None,
            "derivation": None,
            "rejection": exc.witness,
        }


def evaluate_all(tasks):
    return [adjudicate(case) for case in tasks]


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    tasks = json.loads((root / "TASKS.json").read_text())["cases"]
    result = evaluate_all(tasks)
    print(json.dumps({
        "case_count": len(result),
        "positive": sum(1 for x in result if x["judgment"]),
        "negative": sum(1 for x in result if not x["judgment"]),
        "cases": result,
    }, indent=2, sort_keys=True))
