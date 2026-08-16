#!/usr/bin/env python3
import copy, json

MAX_DEPTH=3
CONSTANTS=("a","b","c")
OPS=("f","g")

def const(c): return {"tag":"Const","name":c}
def unary(op,arg): return {"tag":"Unary","op":op,"arg":arg}
def key(t): return t["name"] if t["tag"]=="Const" else f'{t["op"]}({key(t["arg"])})'
def depth(t): return 0 if t["tag"]=="Const" else 1+depth(t["arg"])

def universe():
    terms={c:const(c) for c in CONSTANTS}
    for d in range(1,MAX_DEPTH+1):
        prev=[t for t in list(terms.values()) if depth(t)==d-1]
        for a in prev:
            for op in OPS:
                x=unary(op,a); terms[key(x)]=x
    return terms

def closure():
    terms=universe(); rel={}
    def add(s,d,p):
        if (s,d) not in rel:
            rel[(s,d)]=p; return True
        return False
    for k in terms:
        add(k,k,{"rule":"REFLEXIVITY","source":k,"target":k,"premises":[]})
    add("a","b",{"rule":"REPLACEMENT","source_rule":"r_ab","source":"a","target":"b","substitution":{},"premises":[]})
    add("b","c",{"rule":"REPLACEMENT","source_rule":"r_bc","source":"b","target":"c","substitution":{},"premises":[]})
    while True:
        changed=False
        for (s,d),p in list(rel.items()):
            for op in OPS:
                ss=f"{op}({s})"; dd=f"{op}({d})"
                if ss in terms and dd in terms:
                    changed |= add(ss,dd,{"rule":"CONGRUENCE","operator":op,"source":ss,"target":dd,"premises":[copy.deepcopy(p)]})
            ss=f"f({s})"; dd=f"g({d})"
            if ss in terms and dd in terms:
                changed |= add(ss,dd,{"rule":"REPLACEMENT","source_rule":"r_fg","source":ss,"target":dd,
                                      "substitution":{"x":{"source":s,"target":d}},"premises":[copy.deepcopy(p)]})
        outgoing={}; incoming={}
        for (s,d),p in list(rel.items()):
            outgoing.setdefault(s,[]).append((d,p)); incoming.setdefault(d,[]).append((s,p))
        for mid in set(outgoing)&set(incoming):
            for s,p1 in incoming[mid]:
                for d,p2 in outgoing[mid]:
                    if s != d:
                        changed |= add(s,d,{"rule":"TRANSITIVITY","source":s,"target":d,"middle":mid,
                                            "premises":[copy.deepcopy(p1),copy.deepcopy(p2)]})
        if not changed: return terms,rel

def adjudicate_keys(source,target):
    terms,rel=closure()
    if source not in terms or target not in terms:
        return {"licensed":False,"derivation":None,"rejection":{"code":"OUTSIDE_FROZEN_TERM_UNIVERSE"}}
    if (source,target) in rel:
        return {"licensed":True,"derivation":rel[(source,target)],"rejection":None}
    return {"licensed":False,"derivation":None,"rejection":{"code":"NOT_DERIVABLE_IN_FROZEN_FINITE_FRAGMENT",
            "reachable_targets":sorted({d for (s,d) in rel if s==source})}}
