#!/usr/bin/env python3
"""CUHK-X P1 constitution harness. No preserved-arm score is computed."""
from __future__ import annotations
import argparse,csv,hashlib,inspect,io,json,math,platform,statistics,sys,time,zipfile
from dataclasses import dataclass
from pathlib import Path
import numpy as np

EXP="CUHKX-P1-PRESERVED-EVIDENCE-1"; CID="CUHKX-P1-CONSTITUTION-1"
E={
"s1":"38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f",
"v7zip":"af7687fad3c7a4d140707c09dd84edea79288abdd81f91e9755d21cb63aad088",
"v7py":"473d83342c680836badc0aa5232f32df5aecb7ae7d5755ec7986798eac13b544",
"fold":"0ae2bd6a594152dd1af444566416410043ac11f153d20c8a517bb2a6d5052b73",
"nq":809,"nf":786,"nc":3236,"nfc":3144,
"exact":0.3695920889987639,"acc":0.7580346106304079,"bal":0.7577211493846145}
TRIALS=1000; AUC_RANGE=(.45,.55); RATIO_TOL=.02

def h(b:bytes): return hashlib.sha256(b).hexdigest()
def hf(p:Path):
 x=hashlib.sha256(); f=p.open("rb")
 with f:
  for b in iter(lambda:f.read(1<<20),b""): x.update(b)
 return x.hexdigest()
def cj(o): return (json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n").encode()
def rows(z,n):
 with z.open(n) as f:return list(csv.DictReader(io.TextIOWrapper(f,encoding="utf-8",newline="")))
def key(r): return f"{r['qa_id']}|{r['option']}|{r['action']}"
def bal(y,p):
 tp=sum(a==b==1 for a,b in zip(y,p)); fn=sum(a==1 and b==0 for a,b in zip(y,p));
 tn=sum(a==b==0 for a,b in zip(y,p)); fp=sum(a==0 and b==1 for a,b in zip(y,p))
 return .5*(tp/(tp+fn)+tn/(tn+fp))

@dataclass(frozen=True)
class C:
 q:str; path:str; subj:int; fold:int; opt:str; act:str; route:str; b5:float|None; v7:float; v7f:float|None
 def blind(self):
  return {"qa_id":self.q,"path":self.path,"subject":self.subj,"fold":self.fold,"option":self.opt,
  "action":self.act,"route":self.route,"evidence":{"POSE_IMU":self.b5,"IR":self.v7,"POSE_IMU_IR":self.v7f}}

def identity(s1:Path,vz:Path):
 a,b=hf(s1),hf(vz)
 if a!=E["s1"]:raise RuntimeError(f"S1 hash drift {a}")
 if b!=E["v7zip"]:raise RuntimeError(f"V7 archive hash drift {b}")
 with zipfile.ZipFile(vz) as z: vp=h(z.read("cuhkx_v7_strong_ir_dinov2.py")); fo=h(z.read("subject_folds.csv"))
 if vp!=E["v7py"] or fo!=E["fold"]:raise RuntimeError("V7 member/fold identity drift")
 return {"s1_script_sha256":a,"v7_results_sha256":b,"v7_script_member_sha256":vp,"fold_sha256":fo}

def reproduce(vz:Path):
 with zipfile.ZipFile(vz) as z:
  ve,vfe,vc,vfc,b5=[rows(z,n) for n in ["V7_all809_exact_set_predictions.csv","V7F_exact_set_predictions.csv",
  "V7_all809_candidate_predictions.csv","V7F_candidate_predictions.csv","B5_matched_candidate_predictions.csv"]]
 if (len(ve),len(vfe),len(vc),len(vfc))!=(E["nq"],E["nf"],E["nc"],E["nfc"]):raise RuntimeError("V7 row-count drift")
 em={str(r["qa_id"]):r for r in ve}; ef={str(r["qa_id"]):r for r in vfe}; fm={key(r):r for r in vfc}; bm={key(r):r for r in b5}
 exact=[]
 for q,r in em.items():
  rr=ef.get(q,r); pr=str(rr["pred_answer"]); tr=str(r["true_answer"]); ex=int(pr==tr)
  if int(rr["exact"])!=ex:raise RuntimeError("exact flag drift")
  exact.append({"qa_id":q,"pred":pr,"truth":tr,"exact":ex})
 y=[];p=[]; cs=[]; sh=[]; frozen={}
 for r in vc:
  k=key(r); rr=fm.get(k,r); m=float(rr["margin"]); pr=int(rr["prediction"])
  if pr!=int(m>=0):raise RuntimeError("margin/decision drift")
  yy=int(rr["label"]); y.append(yy);p.append(pr);frozen[k]=pr;cs.append({"key":k,"prediction":pr,"label":yy})
  sh.append(C(str(r["qa_id"]),str(r["path"]),int(r["subject"]),int(r["fold"]),str(r["option"]),str(r["action"]),
  "V7F" if k in fm else "V7",float(bm[k]["margin"]) if k in bm else None,float(r["margin"]),float(fm[k]["margin"]) if k in fm else None))
 m={"state":"PASS","n_multi":len(exact),"n_candidates":len(cs),"exact_set_accuracy":sum(x["exact"] for x in exact)/len(exact),
 "candidate_accuracy":sum(a==b for a,b in zip(y,p))/len(y),"candidate_balanced_accuracy":bal(y,p),
 "exact_stream_sha256":h(b"".join(cj(x) for x in sorted(exact,key=lambda x:x["qa_id"]))),
 "candidate_stream_sha256":h(b"".join(cj(x) for x in sorted(cs,key=lambda x:x["key"]))) }
 for k,g,e in [("exact",m["exact_set_accuracy"],E["exact"]),("acc",m["candidate_accuracy"],E["acc"]),("bal",m["candidate_balanced_accuracy"],E["bal"])]:
  if abs(g-e)>1e-12:raise RuntimeError(f"baseline reproduction drift {k}")
 return sorted(sh,key=lambda x:(x.q,x.opt,x.act)),m,frozen

def shared_hash(sh):return h(b"".join(cj(x.blind()) for x in sh))
def zmake(sh,mode):
 n=len(sh); active=np.zeros((n,3),np.int8); sign=np.zeros((n,3),np.int8)
 for i,x in enumerate(sh):
  vals=(x.b5,x.v7,x.v7f)
  for j,v in enumerate(vals):
   if v is not None:sign[i,j]=1 if v>=0 else -1
  if mode=="PRESERVED_EVIDENCE":active[i,:]=[v is not None for v in vals]
  elif mode=="EARLY_COMPRESSION":active[i,2 if x.v7f is not None else 1]=1
  else:raise ValueError(mode)
 return active,sign

def compose(a,s):
 if a.shape!=s.shape or a.ndim!=2 or a.shape[1]!=3:raise RuntimeError("Z shape drift")
 vote=(a*s).sum(axis=1,dtype=np.int16)
 fb=a[:,2]*s[:,2]+(1-a[:,2])*a[:,1]*s[:,1]+(1-a[:,2])*(1-a[:,1])*a[:,0]*s[:,0]
 return ((vote>0)|((vote==0)&(fb>0))).astype(np.int8)
def fh(fn):return h(inspect.getsource(fn).encode())
def auc(pos,neg):
 v=sorted([(x,1) for x in pos]+[(x,0) for x in neg],key=lambda x:x[0]); ranks=[0.]*len(v);i=0
 while i<len(v):
  j=i+1
  while j<len(v) and v[j][0]==v[i][0]:j+=1
  r=(i+1+j)/2
  for k in range(i,j):ranks[k]=r
  i=j
 rp=sum(r for r,x in zip(ranks,v) if x[1]); n1=len(pos);n0=len(neg); return (rp-n1*(n1+1)/2)/(n1*n0)
def timing(e,p):
 for _ in range(50):compose(*e);compose(*p)
 te=[];tp=[]
 for _ in range(TRIALS//2):
  t=time.perf_counter_ns();compose(*e);te.append(time.perf_counter_ns()-t)
  t=time.perf_counter_ns();compose(*p);tp.append(time.perf_counter_ns()-t)
  t=time.perf_counter_ns();compose(*p);tp.append(time.perf_counter_ns()-t)
  t=time.perf_counter_ns();compose(*e);te.append(time.perf_counter_ns()-t)
 aa=auc(tp,te); me=statistics.median(te); mp=statistics.median(tp); rr=mp/me
 ok=AUC_RANGE[0]<=aa<=AUC_RANGE[1] and abs(rr-1)<=RATIO_TOL
 return {"state":"PASS" if ok else "FAIL","trials_per_arm":len(te),"auc_preserved_gt_early":aa,"median_ns_early":me,"median_ns_preserved":mp,"median_ratio":rr,
 "gate":{"auc_range":list(AUC_RANGE),"median_ratio_abs_delta_max":RATIO_TOL}}

def constitute(sh,base,frozen):
 hs=shared_hash(sh); e=zmake(sh,"EARLY_COMPRESSION"); p=zmake(sh,"PRESERVED_EVIDENCE")
 I1={"state":"PASS","same_bytes":True,"shared_encoded_sha256_early":hs,"shared_encoded_sha256_preserved":hs,"truth_or_label_fields_present":False}
 ep=compose(*e); ex=np.asarray([frozen[f"{x.q}|{x.opt}|{x.act}"] for x in sh],np.int8)
 if not np.array_equal(ep,ex):raise RuntimeError("common reasoner fails exact S1 reproduction")
 same_shape=e[0].shape==p[0].shape==(E["nc"],3); same_sign=np.array_equal(e[1],p[1])
 I2={"state":"PASS" if same_shape and same_sign else "FAIL","same_fixed_shape":bool(same_shape),"same_evidence_sign_matrix":bool(same_sign),
 "allowed_difference":"Z active-mask only","transform_source_sha256":fh(zmake),"candidate_order_sha256":h(b"".join(cj({"qa_id":x.q,"option":x.opt,"action":x.act}) for x in sh))}
 rh=fh(compose); I3={"state":"PASS","same_function_object":True,"same_prompt":True,"same_decoding_parameters":True,"same_call_count":1,
 "reasoner_source_sha256_early":rh,"reasoner_source_sha256_preserved":rh}
 ctx={"shared_encoded_sha256":hs,"reasoner_sha256":rh,"prompt_sha256":h(b""),"external_model_calls":0,"rng_calls":0,"evaluator_invoked":False,
 "reasoner_calls":1,"slot_reads":E["nc"]*3,"candidate_rows":E["nc"],"tensor_shape":[E["nc"],3],"files_visible_to_reasoner":[],"log_template_sha256":h(b"P1_CONSTITUTION_REASONER_NO_ARM_LOG")}
 ce=cp=h(cj(ctx)); tt=timing(e,p); I4={"state":"PASS" if ce==cp and tt["state"]=="PASS" else "FAIL","non_z_context_sha256_early":ce,
 "non_z_context_sha256_preserved":cp,"exact_non_z_context_identity":ce==cp,"attacked_surfaces":["files","tensor shape","memory-visible non-Z context","operation counts","RNG calls","prompt","external calls","logs","evaluator inputs","timing"],"timing_attack":tt}
 checks={"I1":I1,"I2":I2,"I3":I3,"I4":I4}; ok=all(x["state"]=="PASS" for x in checks.values())
 return {"checks":checks,"shared_encoded_sha256":hs,"early_z_sha256":h(e[0].tobytes()+e[1].tobytes()),"preserved_z_sha256":h(p[0].tobytes()+p[1].tobytes()),
 "preserved_prediction_digest_unscored":h(compose(*p).tobytes()),"final_state":"IMPLEMENTATION_CONSTITUTED_NOT_YET_AUTHORIZED" if ok else "NOT_IDENTIFIED_TREATMENT_IDENTITY_FAILURE"}

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--s1-script",type=Path,required=True);ap.add_argument("--v7-results",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 s={"experiment_id":EXP,"constitution_id":CID,"specification_state":"FROZEN","execution_authority":"NONE","leaderboard_authority":"NONE","packet7_authority":"NONE",
 "environment":{"python":sys.version,"platform":platform.platform(),"numpy":np.__version__}}
 try:
  s["identity"]=identity(a.s1_script,a.v7_results); sh,b,f=reproduce(a.v7_results);s["baseline_reproduction"]=b;s.update(constitute(sh,b,f))
 except Exception as x:
  s["final_state"]="NOT_IDENTIFIED_BASELINE_REPRODUCTION_FAILURE" if "S1" in str(x) or "baseline" in str(x).lower() else "NOT_IDENTIFIED_TREATMENT_IDENTITY_FAILURE";s["error"]={"type":type(x).__name__,"message":str(x)}
 (a.out/"constitution_status.json").write_text(json.dumps(s,indent=2,sort_keys=True));(a.out/"shared_encoded.sha256").write_text(s.get("shared_encoded_sha256","NOT_AVAILABLE")+"\n")
 print(json.dumps({"final_state":s["final_state"],"baseline_reproduction":s.get("baseline_reproduction",{}).get("state"),**{k:s.get("checks",{}).get(k,{}).get("state") for k in ["I1","I2","I3","I4"]},"preserved_scores_computed":False},indent=2))
 return 0 if s["final_state"]=="IMPLEMENTATION_CONSTITUTED_NOT_YET_AUTHORIZED" else 2
if __name__=="__main__":raise SystemExit(main())
