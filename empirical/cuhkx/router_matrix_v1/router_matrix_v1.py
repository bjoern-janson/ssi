#!/usr/bin/env python3
"""CUHK-X Router Matrix V1.

Evaluates only pre-existing predictor families against the frozen S1 branch routes.
No new model is trained in this script.
"""
from __future__ import annotations
import argparse, json, math, zipfile
from pathlib import Path
import pandas as pd

MATERIAL = 0.01
MIN_NONNEG_FOLDS = 4
BRANCH_MAP = {
    ("HAU","multi"): "HAU_MULTI",
    ("HAU","single"): "HAU_SINGLE",
    ("HAU","combination"): "HAU_COMBINATION",
    ("HAU","emotion"): "HAU_EMOTION",
    ("HAU","sequence"): "HAU_SEQUENCE",
    ("HARn","single"): "HARN_SINGLE",
    ("HARn","object_interaction"): "HARN_OBJECT",
}

def read_training(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        hits=[n for n in names if n.endswith("training_qa.csv")]
        if len(hits)!=1: raise RuntimeError(f"training_qa.csv ambiguity: {hits}")
        q=pd.read_csv(z.open(hits[0]))
    q["qa_id"]=q.qa_id.astype(str); q["path"]=q.path.astype(str)
    return q

def read_s1_oof(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        hits=[n for n in z.namelist() if n.endswith("oof_exact_predictions.csv")]
        if len(hits)!=1: raise RuntimeError(f"S1 OOF artifact ambiguity: {hits}")
        d=pd.read_csv(z.open(hits[0]))
    d["qa_id"]=d.qa_id.astype(str); d["path"]=d.path.astype(str)
    return d

def read_v7(path: Path):
    with zipfile.ZipFile(path) as z:
        c=pd.read_csv(z.open("V7_all809_candidate_predictions.csv"))
        e=pd.read_csv(z.open("V7_all809_exact_set_predictions.csv"))
    c["qa_id"]=c.qa_id.astype(str); c["path"]=c.path.astype(str); c["action"]=c.action.astype(str)
    e["qa_id"]=e.qa_id.astype(str)
    return c,e

def score(pred: pd.DataFrame, base: pd.DataFrame, branch: str):
    b=base[base.branch==branch][["qa_id","fold","exact"]].rename(columns={"exact":"base_exact"})
    p=pred[["qa_id","exact"]].rename(columns={"exact":"alt_exact"})
    m=b.merge(p,on="qa_id",validate="one_to_one")
    if len(m)!=len(b): raise RuntimeError(f"coverage drift {branch}: {len(m)} != {len(b)}")
    base_acc=float(m.base_exact.mean()); alt_acc=float(m.alt_exact.mean()); delta=alt_acc-base_acc
    fold=[]
    for f in range(5):
        x=m[m.fold==f]
        if x.empty: raise RuntimeError(f"empty fold {f} {branch}")
        d=float(x.alt_exact.mean()-x.base_exact.mean())
        fold.append(d)
    nonneg=sum(d>=0 for d in fold)
    selected=bool(delta>=MATERIAL and nonneg>=MIN_NONNEG_FOLDS)
    return {"s1_exact":base_acc,"alternative_exact":alt_acc,"delta_exact":delta,
            "fold_deltas":fold,"fold_nonnegative":nonneg,
            "material_required":MATERIAL,"fold_nonnegative_required":MIN_NONNEG_FOLDS,
            "status":"CONSTITUTED_SELECTED" if selected else "CONSTITUTED_REJECTED"}

def v7_margin_map(c: pd.DataFrame):
    dup=c.duplicated(["path","action"],keep=False)
    if dup.any():
        # Exact repeated path/action with differing fold/model values is not safe to collapse.
        bad=c.loc[dup,["path","action"]].drop_duplicates()
        raise RuntimeError(f"duplicate archived V7 path/action margins: {len(bad)}")
    return {(r.path,r.action):float(r.margin) for r in c.itertuples(index=False)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--training",required=True,type=Path)
    ap.add_argument("--s1-oof",required=True,type=Path)
    ap.add_argument("--v7-results",required=True,type=Path)
    ap.add_argument("--out",default="router_matrix_result.json",type=Path)
    args=ap.parse_args()

    q=read_training(args.training)
    base=read_s1_oof(args.s1_oof)
    c,e=read_v7(args.v7_results)
    results={}

    # 1) HAU multi: pure V7 exact predictions are directly archived.
    pe=e.rename(columns={"true_answer":"truth","pred_answer":"pred"}).copy()
    pe["exact"]=(pe.pred.astype(str)==pe.truth.astype(str)).astype(int)
    results["HAU_MULTI__PURE_V7_IR"]=score(pe,base,"HAU_MULTI")

    # Build unique archived V7 margin map. If this fails, both cross-branch alternatives are unconstituted.
    try:
        mm=v7_margin_map(c)
        margin_error=None
    except Exception as exc:
        mm={}; margin_error=f"{type(exc).__name__}: {exc}"

    # 2) HAU single: offered-option argmax using existing V7 per-action margins.
    try:
        if margin_error: raise RuntimeError(margin_error)
        qs=q[(q.source=="HAU")&(q.category=="single")].copy()
        base_ids=set(base.loc[base.branch=="HAU_SINGLE","qa_id"])
        qs=qs[qs.qa_id.isin(base_ids)]
        rows=[]
        for r in qs.itertuples(index=False):
            vals=[]
            for l in "ABCD":
                v=getattr(r,l)
                if pd.isna(v): continue
                k=(str(r.path),str(v))
                if k not in mm: raise KeyError(k)
                vals.append((mm[k],-ord(l),l))
            pred=max(vals)[2]; truth=str(r.answer)
            rows.append({"qa_id":str(r.qa_id),"exact":int(pred==truth)})
        pred=pd.DataFrame(rows)
        if len(pred)!=len(base_ids): raise RuntimeError(f"full branch coverage failed: {len(pred)} != {len(base_ids)}")
        results["HAU_SINGLE__V7_PER_ACTION"]=score(pred,base,"HAU_SINGLE")
    except Exception as exc:
        results["HAU_SINGLE__V7_PER_ACTION"]={"status":"NOT_CONSTITUTED","reason":f"{type(exc).__name__}: {exc}"}

    # 3) HAU combination: exact S1 set conversion requires all 40 action margins for each path.
    try:
        if margin_error: raise RuntimeError(margin_error)
        qc=q[(q.source=="HAU")&(q.category=="combination")].copy()
        base_ids=set(base.loc[base.branch=="HAU_COMBINATION","qa_id"])
        qc=qc[qc.qa_id.isin(base_ids)]
        action_vocab=sorted(set(q.loc[(q.source=="HAU")&(q.category=="multi"),["A","B","C","D"]].stack().astype(str)))
        rows=[]
        for r in qc.itertuples(index=False):
            margins={a:mm[(str(r.path),a)] for a in action_vocab}  # KeyError => NOT_CONSTITUTED
            presence={a:int(margins[a]>=0.0) for a in action_vocab}
            choices=[]
            for l in "ABCD":
                text=str(getattr(r,l)); aset={x.strip() for x in text.split(",") if x.strip()}
                hamming=sum(int(presence[a] != int(a in aset)) for a in action_vocab)
                conf=sum((1.0 if a in aset else -1.0)*math.tanh(margins[a]) for a in action_vocab)
                choices.append((-hamming,conf,-ord(l),l))
            pred=max(choices)[3]; rows.append({"qa_id":str(r.qa_id),"exact":int(pred==str(r.answer))})
        pred=pd.DataFrame(rows)
        if len(pred)!=len(base_ids): raise RuntimeError(f"full branch coverage failed: {len(pred)} != {len(base_ids)}")
        results["HAU_COMBINATION__V7_ACTION_PRESENCE"]=score(pred,base,"HAU_COMBINATION")
    except Exception as exc:
        results["HAU_COMBINATION__V7_ACTION_PRESENCE"]={"status":"NOT_CONSTITUTED","reason":f"{type(exc).__name__}: {exc}"}

    # 4) B0 historical artifact lacks full class score vectors, so exact option scoring is not constituted here.
    for branch in ["HARN_SINGLE","HARN_OBJECT"]:
        results[f"{branch}__B0_SKELETON"]={
            "status":"NOT_CONSTITUTED",
            "reason":"historical B0 artifact records top-1/top-3 classes but not the full class-score vector required for S1-style offered-option exact scoring"
        }

    # Fixed branches.
    results["HAU_EMOTION__S1_ONLY"]={"status":"S1_ONLY"}
    results["HAU_SEQUENCE__S1_ONLY"]={"status":"S1_ONLY"}

    selected=[k for k,v in results.items() if v.get("status")=="CONSTITUTED_SELECTED"]
    out={
        "matrix_id":"CUHKX_ROUTER_MATRIX_V1",
        "selection_gate":{"delta_exact_min":MATERIAL,"nonnegative_folds_min":MIN_NONNEG_FOLDS,"public_lb_used":False},
        "results":results,
        "selected_route_changes":selected,
        "matrix_terminal_state":"ROUTE_CHANGES_EARNED" if selected else "NO_ROUTE_CHANGES",
        "authority":"Only selected branch substitutions are eligible to constitute a later S2. NOT_CONSTITUTED is not a negative performance result."
    }
    args.out.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__": main()
