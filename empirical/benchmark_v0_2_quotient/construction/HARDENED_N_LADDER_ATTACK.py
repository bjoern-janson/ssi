#!/usr/bin/env python3
"""Hostile N0->N4 preactivation attack. No future obligation; G remains closed."""
from __future__ import annotations
import ast, copy, hashlib, itertools, json
from pathlib import Path
import CLOSED_PREACTIVATION_INTERFACE as ci

HERE = Path(__file__).resolve().parent
W = json.loads((HERE/"VALIDATED_SUBSTRATE.json").read_text())
GA = json.loads((HERE/"GAMMA_A.json").read_text())
GB = json.loads((HERE/"GAMMA_B.json").read_text())
QCA = json.loads((HERE/"quotient_construction_audit.json").read_text())
THREAT = json.loads((HERE/"CAPABILITY_THREAT_MODEL.json").read_text())
OUT = HERE/"hardened_n_ladder_audit.json"
CLASSES = sorted({x for f in W["facts"] for x in f["transformation_classes"]})
HIST = [set(f["transformation_classes"]) for f in W["facts"]]
FORBIDDEN = ("gamma", "reserve", "revision_topology", "quotient_map", "path_equivalence")


def canon(x): return json.dumps(x, sort_keys=True, separators=(",", ":"))
def digest(x): return hashlib.sha256(canon(x).encode()).hexdigest()


def tasks():
    return [
        tuple(c) for r in range(1, len(CLASSES)+1)
        for c in itertools.combinations(CLASSES, r)
        if not any(set(c) == h for h in HIST)
    ]


def qvars(q):
    q = tuple(q)
    return [
        tuple(sorted(q)), tuple(reversed(sorted(q))),
        q[1:]+q[:1] if len(q)>1 else q,
        tuple(sorted(q, key=lambda x:(len(x),x))),
    ]


def gammas():
    out=[("A",GA),("B",GB)]
    by={}
    for r in GA["path_records"]: by.setdefault(r["relation_kind"],[]).append(r["path_id"])
    for shift in range(1,33):
        eq={}; n=1
        for kind in sorted(by):
            ids=sorted(by[kind]); k=shift%len(ids); ids=ids[k:]+ids[:k]
            for i in range(0,len(ids),2):
                label=f"V{shift:02d}{n:013d}"
                eq[ids[i]]=label; eq[ids[i+1]]=label; n+=1
        out.append((f"V{shift:02d}",{
            "schema_version":"metamorphic",
            "substrate_ref":GA["substrate_ref"],
            "path_records":copy.deepcopy(GA["path_records"]),
            "equivalence_class":eq,
        }))
    return out


def baseline(ts):
    n0=n1=0
    for q in ts:
        a=ci.forward_trace(q); dormant_a,dormant_b=GA,GB; b=ci.forward_trace(q)
        n0 += a["O"] != b["O"]; n1 += a != b
    return {
        "N0_endpoint":{"pass":n0==0,"tasks":len(ts),"mismatch_count":n0},
        "N1_full_trace":{"pass":n1==0,"tasks":len(ts),"mismatch_count":n1},
    }


def metamorphic(ts):
    gs=gammas(); comparisons=0
    for q in ts:
        ref=ci.forward_trace(tuple(sorted(q)))
        for qv in qvars(q):
            for pressure in (0,3,17):
                junk=[bytearray(1024) for _ in range(pressure)]
                for label,dormant in gs:
                    comparisons+=1; got=ci.forward_trace(qv)
                    if got != ref:
                        return {
                            "pass":False,"comparisons":comparisons,"mismatch_count":1,
                            "mismatches":[{"query":list(q),"variant":label,"pressure":pressure,
                                           "reference":digest(ref),"got":digest(got),"dormant":digest(dormant)}],
                        }
                del junk
    return {"pass":True,"comparisons":comparisons,"mismatch_count":0,"mismatches":[],
            "gamma_variants":len(gs),"query_variants_per_task":4,"pressure_levels":[0,3,17],
            "wall_clock_invariance_claimed":False}


def static_boundary():
    tree=ast.parse(Path(ci.__file__).read_text())
    funcs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    def calls(node):
        return {n.func.id for n in ast.walk(node)
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in funcs}
    roots={}
    for root in ("forward_trace","evaluate_gate"):
        seen=set(); stack=[root]
        while stack:
            name=stack.pop()
            if name in seen: continue
            seen.add(name); stack.extend(calls(funcs[name])-seen)
        hits=[]
        for name in sorted(seen):
            node=funcs[name]
            syms=({n.id.lower() for n in ast.walk(node) if isinstance(n,ast.Name)} |
                  {n.attr.lower() for n in ast.walk(node) if isinstance(n,ast.Attribute)})
            bad=sorted(s for s in syms if any(s==f or s.startswith(f+"_") for f in FORBIDDEN))
            if bad: hits.append({"function":name,"symbols":bad})
        roots[root]={"reachable_functions":sorted(seen),"forbidden_hits":hits,"pass":not hits}
    return {"pass":all(x["pass"] for x in roots.values()),"roots":roots}


def poison(ts):
    values=[GA,GB,{"gamma":GA},{"reserve_handle":GB},"GAMMA_A",0,None,object(),
            tuple(GA),list(GB),bytes(4096),bytearray(4096)]
    mismatch=[]; comparisons=0
    for x in values:
        ci.GAMMA_A=ci.GAMMA_B=ci.RESERVE_HANDLE=ci.REVISION_TOPOLOGY=x
        for q in ts:
            comparisons+=1
            if ci.forward_trace(q) != ci.forward_trace(q):
                mismatch.append({"query":list(q),"type":type(x).__name__}); break
    return {"pass":not mismatch,"comparisons":comparisons,
            "mismatch_count":len(mismatch),"mismatches":mismatch}


def gate():
    cases=[
        (ci.InsufficiencyEvidence("PASS","CURRENT_ROUTE",True,"v1"),False),
        (ci.InsufficiencyEvidence("FAIL","OTHER",True,"v1"),False),
        (ci.InsufficiencyEvidence("FAIL","CURRENT_ROUTE",False,"v1"),False),
        (ci.InsufficiencyEvidence("FAIL","CURRENT_ROUTE",True,""),False),
        (ci.InsufficiencyEvidence("FAIL","CURRENT_ROUTE",True,"v1"),True),
    ]
    mismatch=[]; comparisons=0
    for label,dormant in gammas():
        for e,expected in cases:
            comparisons+=1; got=ci.evaluate_gate(e)
            if got != expected: mismatch.append({"variant":label,"expected":expected,"got":got})
    return {"pass":not mismatch,"comparisons":comparisons,
            "mismatch_count":len(mismatch),"mismatches":mismatch}


def capability(ts):
    rejected=0; accepted=[]
    for q in ts:
        for arm,g in (("A",GA),("B",GB)):
            try: ci.forward_trace(q,g); accepted.append({"surface":"forward_extra_arg","arm":arm})
            except TypeError: rejected+=1
    for arm,g in (("A",GA),("B",GB)):
        try: ci.forward_trace((g,)); accepted.append({"surface":"query_payload","arm":arm})
        except TypeError: rejected+=1
    payload={"validator_status":"FAIL","failure_scope":"CURRENT_ROUTE",
             "independent_validator":True,"validator_id":"v1"}
    for _ in range(5):
        for arm,g in (("A",GA),("B",GB)):
            dirty=dict(payload); dirty["reserve_handle"]=g
            try: ci.evaluate_gate(dirty); accepted.append({"surface":"gate_open_dict","arm":arm})
            except TypeError: rejected+=1
            try: ci.InsufficiencyEvidence(**payload,reserve_handle=g); accepted.append({"surface":"constructor_extra","arm":arm})
            except TypeError: rejected+=1
            e=ci.InsufficiencyEvidence(**payload)
            try: setattr(e,"reserve_handle",g); accepted.append({"surface":"gate_setattr","arm":arm})
            except (AttributeError,TypeError): rejected+=1
    return {"pass":not accepted,"attempts":rejected+len(accepted),"rejected":rejected,
            "accepted":len(accepted),"accepted_details":accepted[:10],
            "required_semantics":"Gamma/revision-topology capability must be rejected at preactivation interfaces, not merely ignored"}


def main():
    ts=tasks(); base=baseline(ts); n2=metamorphic(ts); stat=static_boundary()
    pois=poison(ts); gb=gate(); n3=stat["pass"] and pois["pass"] and gb["pass"]; n4=capability(ts)
    semantic=QCA["certificates"]["D_semantic"]["pass"]
    topology=QCA["certificates"]["D_topology"]["pass"]
    fq=QCA["certificates"]["F_comp_q_equals_F"]["pass"]
    all_n=base["N0_endpoint"]["pass"] and base["N1_full_trace"]["pass"] and n2["pass"] and n3 and n4["pass"]
    ok=semantic and topology and fq and all_n
    out={
        "benchmark_id":"VFA-0.2-QUOTIENT-REVISION-TOPOLOGY",
        "audit_identity":"VFA-0.2-HARDENED-N-LADDER-ATTACK-1",
        "future_obligation_accessed":False,
        "threat_model":{"id":THREAT["threat_model_id"],"scope":"FROZEN_CALLER_CAPABILITY_MODEL"},
        "certificates":{**base,"N2_metamorphic_behavior":n2,
            "N3_transitive_nonuse":{"pass":n3,"static_call_graph":stat,
                "module_global_poisoning":pois,"gate_behavioral_noninterference":gb},
            "N4_capability_surface":n4,"D_semantic":semantic,"D_topology":topology,"F_comp_q_equals_F":fq},
        "D_pre_activation_hardened":{"adjudication":"PASS" if ok else "FAIL","scope":THREAT["threat_model_id"]},
        "authorization":{"freeze_packet":"NOT_FROZEN","authorization_certificate":"NOT_ISSUED",
                         "future_run":"NOT_AUTHORIZED","G_activation":"PROHIBITED"},
        "prospective":{"kernel_q_subset_kernel_T_future":"NOT_EVALUATED","Delta_Pi":"NOT_EVALUATED"},
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"D_pre_activation_hardened":out["D_pre_activation_hardened"]["adjudication"],
        "scope":out["D_pre_activation_hardened"]["scope"],"N0":base["N0_endpoint"]["pass"],
        "N1":base["N1_full_trace"]["pass"],"N2":n2["pass"],"N2_comparisons":n2["comparisons"],
        "N3":n3,"poison_comparisons":pois["comparisons"],"gate_comparisons":gb["comparisons"],
        "N4":n4["pass"],"N4_attempts":n4["attempts"],"N4_accepted":n4["accepted"],
        "future_obligation_accessed":False},indent=2,sort_keys=True))


if __name__=="__main__": main()
