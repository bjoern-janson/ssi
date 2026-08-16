#!/usr/bin/env python3
"""K0 compiler: frozen external STLC source contract -> SSI-IR/K0-STLC-v0.1.

This compiler is intentionally source-specific. It compiles only the source
fragment frozen in ../source and never reads source gold judgments.
"""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "source"
SOURCE_MANIFEST_SHA256 = "27e5d9675453f36289bee9af8fc020655c9874799905bdac3a2ea700d6207345"

RULE_SPECS = {
    "T_Var": {
        "id": "IR-T-VAR",
        "term_kind": "VAR",
        "opcode": "LOOKUP",
        "requirements": ["EXACT_CONTEXT_BINDING"],
    },
    "T_Abs": {
        "id": "IR-T-ABS",
        "term_kind": "ABS",
        "opcode": "ABS_EXTEND",
        "requirements": ["EXTEND_CONTEXT_WITH_BINDER", "TYPE_BODY"],
    },
    "T_App": {
        "id": "IR-T-APP",
        "term_kind": "APP",
        "opcode": "APP_ARROW",
        "requirements": ["FUNCTION_HAS_ARROW_TYPE", "ARGUMENT_MATCHES_ARROW_DOMAIN"],
    },
    "T_Tru": {
        "id": "IR-T-TRU",
        "term_kind": "TRUE",
        "opcode": "CONST_BOOL",
        "requirements": [],
    },
    "T_Fls": {
        "id": "IR-T-FLS",
        "term_kind": "FALSE",
        "opcode": "CONST_BOOL",
        "requirements": [],
    },
    "T_Test": {
        "id": "IR-T-TEST",
        "term_kind": "IF",
        "opcode": "IF_BOOL_BRANCH_EQ",
        "requirements": ["GUARD_HAS_BOOL_TYPE", "BRANCH_TYPES_EQUAL"],
    },
}

DISTINCTION_TARGETS = {
    "DIST-001": ["context.lookup", "IR-T-VAR"],
    "DIST-002": ["type_system.constructors.BOOL", "type_system.constructors.ARROW", "type_system.equality"],
    "DIST-003": ["IR-T-APP.requirements.FUNCTION_HAS_ARROW_TYPE"],
    "DIST-004": ["IR-T-APP.requirements.ARGUMENT_MATCHES_ARROW_DOMAIN"],
    "DIST-005": ["IR-T-TEST.requirements.GUARD_HAS_BOOL_TYPE"],
    "DIST-006": ["IR-T-TEST.requirements.BRANCH_TYPES_EQUAL"],
    "DIST-007": ["context.extension", "IR-T-ABS"],
    "DIST-008": ["type_system.constructors.ARROW.ordered_fields", "IR-T-APP"],
}


def canonical(obj):
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source_contract():
    manifest = SOURCE / "MANIFEST.json"
    if sha256(manifest) != SOURCE_MANIFEST_SHA256:
        raise RuntimeError("frozen source manifest hash changed")

    syntax = json.loads((SOURCE / "syntax.json").read_text())
    rules = json.loads((SOURCE / "typing_rules.json").read_text())
    distinctions = json.loads((SOURCE / "distinctions.json").read_text())

    source_rules = [r["name"] for r in rules["rules"]]
    if source_rules != ["T_Var", "T_Abs", "T_App", "T_Tru", "T_Fls", "T_Test"]:
        raise RuntimeError(f"unexpected source rule order/content: {source_rules}")

    if set(syntax["types"]) != {"Bool", "Arrow"}:
        raise RuntimeError("unexpected source type constructors")
    if set(syntax["terms"]) != {"Var", "Abs", "App", "True", "False", "If"}:
        raise RuntimeError("unexpected source term constructors")

    dist_ids = [d["id"] for d in distinctions["distinctions"]]
    if dist_ids != [f"DIST-{i:03d}" for i in range(1, 9)]:
        raise RuntimeError("unexpected frozen distinction inventory")

    return syntax, rules, distinctions


def build_ir():
    load_source_contract()

    rules = []
    correspondence = {}
    for source_rule in ["T_Var", "T_Abs", "T_App", "T_Tru", "T_Fls", "T_Test"]:
        spec = dict(RULE_SPECS[source_rule])
        spec["source_rule"] = source_rule
        rules.append(spec)
        correspondence[source_rule] = spec["id"]

    return {
        "object": "SSI-IR/K0-STLC-v0.1",
        "source": {
            "object": "K0-SOURCE-TYPE-SYSTEM-COMPILER/SOURCE",
            "manifest_sha256": SOURCE_MANIFEST_SHA256,
            "external_regime": "Software Foundations PLF 5.6 Stlc Bool+Arrow typing relation",
        },
        "encoding": {
            "types": {
                "Bool": {"kind": "BOOL"},
                "Arrow": {
                    "kind": "ARROW",
                    "ordered_fields": {"from": "domain", "to": "codomain"},
                },
            },
            "terms": {
                "Var": {"kind": "VAR", "field_map": {"name": "name"}},
                "Abs": {
                    "kind": "ABS",
                    "field_map": {
                        "param": "binder",
                        "param_type": "binder_type",
                        "body": "body",
                    },
                },
                "App": {
                    "kind": "APP",
                    "field_map": {"fn": "function", "arg": "argument"},
                },
                "True": {"kind": "TRUE", "field_map": {}},
                "False": {"kind": "FALSE", "field_map": {}},
                "If": {
                    "kind": "IF",
                    "field_map": {
                        "cond": "guard",
                        "then": "then_branch",
                        "else": "else_branch",
                    },
                },
            },
            "context": {
                "source": "mapping variable -> type",
                "target": "ordered list of {variable,type} sorted by variable for input snapshots",
            },
        },
        "type_system": {
            "constructors": {
                "BOOL": {"arity": 0},
                "ARROW": {"arity": 2, "ordered_fields": ["domain", "codomain"]},
            },
            "equality": "STRUCTURAL_EXACT",
        },
        "context": {
            "representation": "ORDERED_BINDING_LIST",
            "lookup": "LATEST_EXACT_VARIABLE_NAME",
            "extension": "APPEND_BINDING_SHADOWS_EARLIER",
        },
        "rules": rules,
        "query_contract": {
            "fields": ["context", "term", "expected_type"],
            "result": ["JUDGMENT_LICENSED", "JUDGMENT_REJECTED"],
            "expected_type_check": "STRUCTURAL_EXACT",
        },
        "justification": {
            "source_correspondence": correspondence,
            "trace_node_fields": [
                "ir_rule",
                "source_rule_ancestor",
                "judgment",
                "premises",
                "evidence",
            ],
            "fabricated_source_ancestor_forbidden": True,
        },
        "distinction_targets": DISTINCTION_TARGETS,
        "authority_ceiling": {
            "source_justification_is_not_automatically_ssi_authority": True,
            "this_ir_establishes_compilation_generalization": False,
            "this_ir_modifies_R1_R11": False,
        },
    }


def compile_type(source_type):
    tag = source_type["tag"]
    if tag == "Bool":
        return {"kind": "BOOL"}
    if tag == "Arrow":
        return {
            "kind": "ARROW",
            "domain": compile_type(source_type["from"]),
            "codomain": compile_type(source_type["to"]),
        }
    raise ValueError(f"unrepresentable source type: {tag}")


def compile_term(source_term):
    tag = source_term["tag"]
    if tag == "Var":
        return {"kind": "VAR", "name": source_term["name"]}
    if tag == "Abs":
        return {
            "kind": "ABS",
            "binder": source_term["param"],
            "binder_type": compile_type(source_term["param_type"]),
            "body": compile_term(source_term["body"]),
        }
    if tag == "App":
        return {
            "kind": "APP",
            "function": compile_term(source_term["fn"]),
            "argument": compile_term(source_term["arg"]),
        }
    if tag == "True":
        return {"kind": "TRUE"}
    if tag == "False":
        return {"kind": "FALSE"}
    if tag == "If":
        return {
            "kind": "IF",
            "guard": compile_term(source_term["cond"]),
            "then_branch": compile_term(source_term["then"]),
            "else_branch": compile_term(source_term["else"]),
        }
    raise ValueError(f"unrepresentable source term: {tag}")


def compile_context(source_context):
    return [
        {"variable": name, "type": compile_type(source_context[name])}
        for name in sorted(source_context)
    ]


def compile_query(case):
    return {
        "source_case_id": case["id"],
        "context": compile_context(case["context"]),
        "term": compile_term(case["term"]),
        "expected_type": compile_type(case["expected_type"]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-ir")
    parser.add_argument("--compile-query-file")
    args = parser.parse_args()

    if args.emit_ir:
        Path(args.emit_ir).write_text(canonical(build_ir()))
    elif args.compile_query_file:
        case = json.loads(Path(args.compile_query_file).read_text())
        print(canonical(compile_query(case)), end="")
    else:
        print(canonical(build_ir()), end="")


if __name__ == "__main__":
    main()
