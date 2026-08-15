#!/usr/bin/env python3
"""Grounding-aware H completeness and residual-veto audit.

No future obligation is accessed. The audit verifies the bounded causal-rival
ledger, evidence-path presence, dispositions, and the frozen residual veto.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = json.loads((HERE / "H_MATERIAL_RIVAL_MANIFEST_GROUNDED.json").read_text())
OUT = HERE / "h_grounded_residual_audit.json"
ALLOWED = {"BLOCKED","MEASURED","RANDOMIZED","RESIDUAL"}
MANDATORY_BASE = {
    "H_capacity","H_information","H_ordinary_adapt","H_current_distribution","H_future_distribution",
    "H_resources","H_implementation","H_label_leakage","H_future_selection","H_differential_exposure",
    "H_evaluator","H_missingness",
}
REQUIRED_REPAIRS = {
    "H_quotient_interpretation","H_challenge_recognizability","H_future_artifact_choice",
    "H_future_grounding_circularity","H_witness_reconstruction","H_Tfuture_measurement",
    "H_pseudoreplication","H_grounding_domain_selection","H_structural_endpoint_tautology",
}


def evidence_path(path: str) -> Path:
    p = Path(path)
    return (ROOT / p).resolve()


def main():
    rivals=MANIFEST["rivals"]
    ids=[r.get("id") for r in rivals]
    duplicates=[x for x,c in Counter(ids).items() if c>1]
    missing_base=sorted(MANDATORY_BASE-set(ids))
    missing_repairs=sorted(REQUIRED_REPAIRS-set(ids))
    unclassified=[]
    missing_fields=[]
    evidence_gaps=[]
    residual_veto=[]
    for r in rivals:
        for field in ("id","entry","material","disposition","unbounded","effect_explaining","evidence","bound"):
            if field not in r:
                missing_fields.append({"id":r.get("id"),"field":field})
        if r.get("disposition") not in ALLOWED:
            unclassified.append(r.get("id"))
        evidence=r.get("evidence",[])
        if r.get("disposition") in {"BLOCKED","MEASURED","RANDOMIZED"}:
            if not evidence:
                evidence_gaps.append({"id":r.get("id"),"path":"<NONE>"})
            else:
                for path in evidence:
                    if not evidence_path(path).is_file():
                        evidence_gaps.append({"id":r.get("id"),"path":path})
        if r.get("disposition")=="RESIDUAL" and r.get("material") is True and r.get("unbounded") is True and r.get("effect_explaining") is True:
            residual_veto.append(r.get("id"))

    completeness=not duplicates and not missing_base and not missing_repairs and not unclassified and not missing_fields and not evidence_gaps
    passed=completeness and not residual_veto
    out={
        "benchmark_id":"VFA-0.2-QUOTIENT-REVISION-TOPOLOGY",
        "audit_identity":"VFA-0.2-H-GROUNDED-RESIDUAL-AUDIT-1",
        "future_obligation_accessed":False,
        "G_activation":"PROHIBITED",
        "ledger":{
            "rival_count":len(rivals),
            "duplicate_ids":duplicates,
            "missing_mandatory_base":missing_base,
            "missing_required_grounding_repairs":missing_repairs,
            "unclassified":unclassified,
            "missing_required_fields":missing_fields,
            "evidence_gaps":evidence_gaps,
            "disposition_counts":dict(Counter(r["disposition"] for r in rivals)),
            "residual_ids":[r["id"] for r in rivals if r["disposition"]=="RESIDUAL"],
            "residual_veto_ids":residual_veto,
            "completeness_pass":completeness,
        },
        "H_adjudication":"PASS" if passed else "FAIL",
        "interpretation":"The previously vetoing post-gate semantics, evaluator, and challenge-recognizability rivals are bounded by the consequence-grounded reference semantics. Added artifact-choice, grounding-circularity, witness, measurement, domain-selection, pseudoreplication, and structural-endpoint rivals all have explicit dispositions. Remaining residuals concern transport, downstream CCA/CARS, and physical cost outside the first estimand and cannot explain the paired first-endpoint contrast under the frozen scope.",
        "authority_boundary":{
            "realized_T_future":"NOT_EVALUATED",
            "realized_J_future":"NOT_EVALUATED",
            "Delta_Pi":"NOT_EVALUATED",
            "kernel_q_subset_kernel_T_future":"NOT_EVALUATED",
            "I":"NOT_EVALUATED",
            "freeze_packet":"NOT_FROZEN",
            "authorization_certificate":"NOT_ISSUED",
            "future_run":"NOT_AUTHORIZED"
        }
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")

if __name__=="__main__": main()
