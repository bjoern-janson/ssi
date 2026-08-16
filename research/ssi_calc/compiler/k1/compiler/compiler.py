#!/usr/bin/env python3
"""K1 source-specific compiler: frozen Maude finite rewrite fragment -> SSI-IR."""
from __future__ import annotations
import json
from pathlib import Path

def compile_contract(signature, source_rules):
    return {
        "object": "SSI-IR/K1-MAUDE-RW-v0.1",
        "semantic_kind": "DIRECTED_REWRITING_ENTAILMENT",
        "universe": {
            "constants": list(signature["constants"]),
            "unary_operators": list(signature["unary_operators"]),
            "max_depth": signature["max_depth"],
        },
        "direction": "FORWARD_ONLY",
        "congruence_policy": "PRESERVE_OPERATOR",
        "replacement_policy": "VARIABLE_EVOLUTION_REQUIRES_RELATION",
        "deduction_rules": [
            {"id":"IR-RFL","opcode":"REFLEXIVE","source_rule_ancestor":"REFLEXIVITY"},
            {"id":"IR-CONG","opcode":"LIFT_UNARY","source_rule_ancestor":"CONGRUENCE"},
            {"id":"IR-REPL","opcode":"APPLY_TEMPLATE","source_rule_ancestor":"REPLACEMENT"},
            {"id":"IR-TRANS","opcode":"CHAIN","source_rule_ancestor":"TRANSITIVITY"},
        ],
        "source_rule_templates": [
            {"label":r["label"],"lhs":r["lhs"],"rhs":r["rhs"],"variables":list(r["variables"])}
            for r in source_rules
        ],
        "justification": {"inject_fabricated_node": False},
    }

def main():
    here=Path(__file__).resolve().parent
    source=here.parent/"source"
    signature=json.loads((source/"signature.json").read_text())
    rules=json.loads((source/"rewrite_rules.json").read_text())
    ir=compile_contract(signature,rules)
    out=here/"IR.json"
    out.write_text(json.dumps(ir,indent=2,sort_keys=True)+"\n")
    print(out)

if __name__=="__main__": main()
