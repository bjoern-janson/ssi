#!/usr/bin/env python3
"""Independent executor for SSI-IR/K1-MAUDE-RW-v0.1."""
from __future__ import annotations
import copy

def rule_by_opcode(ir, opcode):
    for r in ir["deduction_rules"]:
        if r["opcode"] == opcode: return r
    return None

def depth_key(s): return s.count("(")

def universe(ir):
    terms=set(ir["universe"]["constants"])
    for d in range(1, ir["universe"]["max_depth"]+1):
        prev=sorted(t for t in terms if depth_key(t)==d-1)
        for a in prev:
            for op in ir["universe"]["unary_operators"]:
                terms.add(f"{op}({a})")
    return terms

def node(ir_rule, source, target, premises, **extra):
    x={"ir_rule":ir_rule["id"],"source_rule_ancestor":ir_rule.get("source_rule_ancestor"),
       "source":source,"target":target,"premises":premises}
    x.update(extra); return x

def closure(ir):
    terms=universe(ir); rel={}
    def add(s,d,p):
        if s in terms and d in terms and (s,d) not in rel:
            rel[(s,d)]=p; return True
        return False
    rfl=rule_by_opcode(ir,"REFLEXIVE"); cong=rule_by_opcode(ir,"LIFT_UNARY")
    repl=rule_by_opcode(ir,"APPLY_TEMPLATE"); chain=rule_by_opcode(ir,"CHAIN")
    if rfl:
        for t in terms: add(t,t,node(rfl,t,t,[]))
    if repl:
        for r in ir["source_rule_templates"]:
            if not r["variables"]:
                add(r["lhs"],r["rhs"],node(repl,r["lhs"],r["rhs"],[],source_rule_label=r["label"],substitution={}))
    while True:
        changed=False
        for (s,d),p in list(rel.items()):
            if cong:
                if ir.get("congruence_policy")=="PRESERVE_OPERATOR":
                    for op in ir["universe"]["unary_operators"]:
                        changed |= add(f"{op}({s})",f"{op}({d})",node(cong,f"{op}({s})",f"{op}({d})",[copy.deepcopy(p)],operator=op))
                elif ir.get("congruence_policy")=="MERGE_F_G":
                    for op1 in ir["universe"]["unary_operators"]:
                        for op2 in ir["universe"]["unary_operators"]:
                            changed |= add(f"{op1}({s})",f"{op2}({d})",node(cong,f"{op1}({s})",f"{op2}({d})",[copy.deepcopy(p)],operator=f"{op1}->{op2}"))
            if repl:
                for tmpl in ir["source_rule_templates"]:
                    if tmpl["variables"]==["x"] and tmpl["lhs"]=="f(x)" and tmpl["rhs"]=="g(x)":
                        pairs=list(rel.items()) if ir["replacement_policy"]=="VARIABLE_EVOLUTION_REQUIRES_RELATION" else [((a,b),None) for a in terms for b in terms]
                        for (a,b),prem in pairs:
                            ps=[] if prem is None else [copy.deepcopy(prem)]
                            changed |= add(f"f({a})",f"g({b})",node(repl,f"f({a})",f"g({b})",ps,source_rule_label=tmpl["label"],substitution={"x":{"source":a,"target":b}}))
        if chain:
            outgoing={}; incoming={}
            for (s,d),p in list(rel.items()):
                outgoing.setdefault(s,[]).append((d,p)); incoming.setdefault(d,[]).append((s,p))
            for mid in set(outgoing)&set(incoming):
                for s,p1 in incoming[mid]:
                    for d,p2 in outgoing[mid]:
                        if s!=d: changed |= add(s,d,node(chain,s,d,[copy.deepcopy(p1),copy.deepcopy(p2)],middle=mid))
        if ir.get("direction")=="SYMMETRIZE":
            for (s,d),p in list(rel.items()):
                if s!=d: changed |= add(d,s,{"ir_rule":"IR-MUT-SYMMETRY","source_rule_ancestor":None,"source":d,"target":s,"premises":[copy.deepcopy(p)]})
        if not changed: return terms,rel

def evaluate(source,target,ir):
    terms,rel=closure(ir)
    fabricated=[]
    if ir.get("justification",{}).get("inject_fabricated_node"):
        fabricated=[{"ir_rule":"IR-FABRICATED-JUSTIFICATION","source_rule_ancestor":None,"source_rule_label":None,"claim":"fabricated compiled justification"}]
    if source not in terms or target not in terms:
        return {"judgment":False,"derivation":None,"rejection":{"code":"IR_OUTSIDE_TERM_UNIVERSE"},"fabricated_justification":fabricated}
    if (source,target) in rel:
        return {"judgment":True,"derivation":rel[(source,target)],"rejection":None,"fabricated_justification":fabricated}
    return {"judgment":False,"derivation":None,"rejection":{"code":"IR_NOT_DERIVABLE","reachable_targets":sorted(d for (s,d) in rel if s==source)},"fabricated_justification":fabricated}
