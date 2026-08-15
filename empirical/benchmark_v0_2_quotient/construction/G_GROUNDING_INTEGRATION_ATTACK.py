#!/usr/bin/env python3
"""Construction-side attack of grounded predicate-G integration.

Synthetic event/artifact/grounding data only; no future release is accessed.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import G_GROUNDING_INTEGRATION_KERNEL as gi
import G_COMMON_CAUSE_KERNEL as gk

HERE = Path(__file__).resolve().parent
DOMAIN = json.loads((HERE / "FUTURE_GROUNDING_DOMAIN.json").read_text())
TEMPLATE = json.loads((HERE / "G_GROUNDING_REALIZED_CERTIFICATE_TEMPLATE.json").read_text())
OUT = HERE / "g_grounding_integration_audit.json"
D = "a" * 64


def obligation():
    return gi.ObligationDescriptor("release-9.9.9", "9.9.9", "2035-01-04T12:00:00Z", 999, "b" * 64)


def artifact(status="IDENTIFIED", version="9.9.9"):
    if status == "IDENTIFIED":
        return gi.ArtifactRecord(status, version, "c" * 64, "d" * 64, "e" * 64)
    return gi.ArtifactRecord(status, version, None, None, None)


def rows(status):
    return [{
        "unit_id": u["unit_id"],
        "left_fact_id": u["left_fact_id"],
        "right_fact_id": u["right_fact_id"],
        "status": status,
    } for u in DOMAIN["grounding_units"]]


def surfaces(status, reverse=False, orient=False):
    out=[]
    for s in DOMAIN["path_surfaces"]:
        left=list(s["left_ref"]); right=list(s["right_ref"])
        if orient: left,right=right,left
        out.append({"unit_id":s["unit_id"],"relation_kind":s["relation_kind"],"left_ref":left,"right_ref":right,"status":status})
    if reverse: out.reverse()
    return out


def witnesses(status="IDENTIFIED"):
    facts=sorted({f for u in DOMAIN["grounding_units"] for f in (u["left_fact_id"],u["right_fact_id"])})
    return [{"fact_id":f,"status":status,"signature_sha256":None if status=="NOT_IDENTIFIED" else hashlib.sha256(f.encode()).hexdigest()} for f in facts]


def make(status="DISTINGUISHED", *, reverse=False, orient=False, art_status="IDENTIFIED"):
    kernel={"DISTINGUISHED":"NONINCLUSION_WITNESS","EQUIVALENT":"INCLUSION_ON_FROZEN_KERNEL_DOMAIN","NOT_IDENTIFIED":"NOT_IDENTIFIED"}[status]
    wc=witnesses("NOT_IDENTIFIED" if art_status=="NOT_IDENTIFIED" else "IDENTIFIED")
    return gi.make_grounding_envelope(
        obligation(), artifact(art_status), DOMAIN, wc, rows(status), surfaces(status,reverse,orient), kernel,
        {"artifact_contract":D,"grounding_contract":"1"*64,"semantic_contract":"2"*64,"domain":"3"*64},
    )


def invariance_and_common_bundle():
    base=make()
    variants=[make(reverse=True),make(orient=True),make(reverse=True,orient=True)]
    invariant=all(v.envelope_sha256==base.envelope_sha256 and gi.envelope_bytes(v)==gi.envelope_bytes(base) for v in variants)
    trace=gk.SelectionTrace("2035-01-01T00:00:00Z",("release-9.9.9",),(('release-9.9.9',True,()),),"release-9.9.9")
    payload=json.dumps({"selected_candidate_id":"release-9.9.9","selected_version":"9.9.9"},sort_keys=True,separators=(",",":")).encode()
    evidence=gi.envelope_bytes(base)
    bundle=gk.commit_common_bundle(trace,payload,evidence,"2035-01-04T12:00:00Z","2035-01-04T12:00:01Z","2035-01-04T12:01:00Z","2035-01-04T13:01:00Z")
    a=gk.arm_view(bundle); b=gk.arm_view(bundle)
    return {"pass":invariant and a==b and a[0]==payload and a[1]==evidence,"metamorphic_envelopes":3,"envelope_mismatches":0 if invariant else 1,"common_view_equal":a==b}


def fail_closed_contract():
    rejected={}
    tests=[]
    tests.append(("wrong_artifact_version",lambda: gi.make_grounding_envelope(obligation(),artifact(version="9.9.8"),DOMAIN,witnesses(),rows("DISTINGUISHED"),surfaces("DISTINGUISHED"),"NONINCLUSION_WITNESS",{"x":D})))
    bad_rows=rows("DISTINGUISHED"); bad_rows[0]["right_fact_id"]="case:sentry"
    tests.append(("wrong_grounding_pair",lambda: gi.make_grounding_envelope(obligation(),artifact(),DOMAIN,witnesses(),bad_rows,surfaces("DISTINGUISHED"),"NONINCLUSION_WITNESS",{"x":D})))
    bad_surfaces=surfaces("DISTINGUISHED"); bad_surfaces.pop()
    tests.append(("missing_surface",lambda: gi.make_grounding_envelope(obligation(),artifact(),DOMAIN,witnesses(),rows("DISTINGUISHED"),bad_surfaces,"NONINCLUSION_WITNESS",{"x":D})))
    inconsistent=surfaces("DISTINGUISHED"); inconsistent[0]["status"]="EQUIVALENT"
    tests.append(("surface_status_inconsistent",lambda: gi.make_grounding_envelope(obligation(),artifact(),DOMAIN,witnesses(),rows("DISTINGUISHED"),inconsistent,"NONINCLUSION_WITNESS",{"x":D})))
    tests.append(("wrong_kernel",lambda: gi.make_grounding_envelope(obligation(),artifact(),DOMAIN,witnesses(),rows("DISTINGUISHED"),surfaces("DISTINGUISHED"),"INCLUSION_ON_FROZEN_KERNEL_DOMAIN",{"x":D})))
    tests.append(("artifact_missing_but_grounding_identified",lambda: gi.make_grounding_envelope(obligation(),artifact("NOT_IDENTIFIED"),DOMAIN,witnesses(),rows("DISTINGUISHED"),surfaces("DISTINGUISHED"),"NONINCLUSION_WITNESS",{"x":D})))
    for name,fn in tests:
        try: fn(); rejected[name]=False
        except (TypeError,ValueError): rejected[name]=True
    ni=make("NOT_IDENTIFIED",art_status="NOT_IDENTIFIED")
    return {"pass":all(rejected.values()) and ni.kernel_adjudication=="NOT_IDENTIFIED","rejected":rejected,"artifact_failure_envelope_valid":ni.kernel_adjudication=="NOT_IDENTIFIED"}


def static_and_smuggling():
    tree=ast.parse(Path(gi.__file__).read_text())
    forbidden={"arm","gamma","m_gamma","phi","phi_path","reach","deltapi","delta_pi","outcome","performance"}
    hits=sorted({n.id for n in ast.walk(tree) if isinstance(n,ast.Name) and n.id.lower() in forbidden})
    smuggle={}
    for bad in ("arm","Gamma","M_Gamma","Phi_path","DeltaPi","outcome"):
        try:
            gi.make_grounding_envelope(obligation(),artifact(),DOMAIN,witnesses(),rows("DISTINGUISHED"),surfaces("DISTINGUISHED"),"NONINCLUSION_WITNESS",{"x":D},**{bad:"A"}); smuggle[bad]="ACCEPTED"
        except TypeError: smuggle[bad]="REJECTED"
    return {"pass":not hits and all(x=="REJECTED" for x in smuggle.values()),"forbidden_identifier_hits":hits,"smuggling":smuggle}


def template_attack():
    realized=[k for k,v in TEMPLATE.items() if isinstance(v,str) and not (v.startswith("TBD_") or v in {"UNINSTANTIATED_TEMPLATE","NOT_EVALUATED"}) and k not in {"certificate_type","rule"}]
    required={"selected_version","executable_sha256","grounding_envelope_sha256","no_arm_access_before_grounding_commit","no_substitution_conformance"}
    return {"pass":not realized and required<=set(TEMPLATE),"pre_filled_realized_fields":realized,"required_fields_present":required<=set(TEMPLATE)}


def main():
    r={"canonical_common_envelope":invariance_and_common_bundle(),"fail_closed":fail_closed_contract(),"static_independence":static_and_smuggling(),"realized_template":template_attack()}
    ok=all(x["pass"] for x in r.values())
    out={"benchmark_id":"VFA-0.2-QUOTIENT-REVISION-TOPOLOGY","audit_identity":"VFA-0.2-G-GROUNDING-INTEGRATION-ATTACK-1","future_obligation_accessed":False,"G_activation":"PROHIBITED","attack_results":r,"G_grounding_integration_adjudication":"PASS" if ok else "FAIL","authority_boundary":{"realized_T_future":"NOT_EVALUATED","realized_J_future":"NOT_EVALUATED","H":"NOT_EVALUATED_ON_REPAIRED_SURFACE","I":"NOT_EVALUATED","future_run":"NOT_AUTHORIZED"}}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")

if __name__=="__main__": main()
