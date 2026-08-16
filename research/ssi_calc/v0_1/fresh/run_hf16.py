#!/usr/bin/env python3
"""First-exposure runner for frozen SSI-CALC HF16 fresh terrain."""
from __future__ import annotations
import base64, gzip, hashlib, json, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT))
import checker_orchestrated as checker

AUTHORIZED={'AUTHORIZED','AUTHORIZED_SCOPED'}
HF16_SHA='0744abe38f6d32b32eace1862b571246d5bb256f47b76b4bf179b5c9404372a7'
SCHEMA=json.loads((ROOT/'schema.json').read_text())

def load_hf16():
    raw=gzip.decompress(base64.b64decode((HERE/'HF16.json.gz.b64').read_text().strip()))
    assert hashlib.sha256(raw).hexdigest()==HF16_SHA
    return json.loads(raw),raw

def score(cases):
    rows=[]
    for case in cases:
        got=checker.derive(case,SCHEMA).dict(); exp=case['expected']
        pa=got['status'] in AUTHORIZED; ea=exp['status'] in AUTHORIZED
        checks={
            'decision':pa==ea,
            'status':got['status']==exp['status'],
            'locus':got['failure_locus']==exp['failure_locus'],
            'preserved':set(got['preserved_facts'])==set(exp['preserved_facts']),
            'missing':set(got['missing_authority'])==set(exp['missing_authority']),
            'reopened':set(got['reopened'])==set(exp['reopened']),
        }
        checks['exact']=all(checks[k] for k in ('status','locus','preserved','missing','reopened'))
        rows.append({'id':case['id'],'family':case['family'],'title':case['title'],'input':{'facts':case['facts'],'authority_edges':case['authority_edges'],'request':case['request']},'expected':exp,'observed':got,'expected_authorize':ea,'predicted_authorize':pa,'checks':checks})
    n=len(rows); licensed=sum(r['expected_authorize'] for r in rows); unlicensed=n-licensed
    tp=sum(r['expected_authorize'] and r['predicted_authorize'] for r in rows)
    fp=sum((not r['expected_authorize']) and r['predicted_authorize'] for r in rows)
    fn=sum(r['expected_authorize'] and (not r['predicted_authorize']) for r in rows)
    tn=sum((not r['expected_authorize']) and (not r['predicted_authorize']) for r in rows)
    metrics={
        'decision_accuracy':(tp+tn)/n,
        'overreach_rate':fp/unlicensed,
        'false_refusal_rate':fn/licensed,
        'exact_status_accuracy':sum(r['checks']['status'] for r in rows)/n,
        'shallowest_locus_accuracy':sum(r['checks']['locus'] for r in rows)/n,
        'preservation_aware_refusal_accuracy':sum(r['checks']['preserved'] for r in rows)/n,
        'missing_authority_accuracy':sum(r['checks']['missing'] for r in rows)/n,
        'reopened_set_accuracy':sum(r['checks']['reopened'] for r in rows)/n,
        'exact_certificate_accuracy':sum(r['checks']['exact'] for r in rows)/n,
    }
    if metrics['decision_accuracy']==1.0 and fp==0 and fn==0:
        label='HF16_STRONG_PASS'
    elif metrics['decision_accuracy']>=0.875 and metrics['overreach_rate']<=0.125 and metrics['false_refusal_rate']<=0.125:
        label='HF16_PASS'
    elif metrics['decision_accuracy']<0.75 or metrics['overreach_rate']>0.25:
        label='HF16_FAILED'
    else:
        label='HF16_PARTIAL'
    return {
        'object':'SSI_CALC_V0.1/HF16_FIRST_EXPOSURE',
        'successor_merge_commit':'87322c273ca9db1e9ae8d90a2ceb7faf272f75c1',
        'hf16_freeze_merge_commit':'61ef09fa28959a6c7a5124c4e0c42a4f59d5bfc6',
        'hf16_sha256':HF16_SHA,
        'kernel_rule_count':len(checker.RULES),
        'rules_added_beyond_R11':0,
        'confusion_matrix':{'TP':tp,'FP_overreach':fp,'FN_false_refusal':fn,'TN':tn,'licensed':licensed,'unlicensed':unlicensed},
        'metrics':metrics,
        'threshold_status':label,
        'mismatch_count':sum(not r['checks']['exact'] for r in rows),
        'decision_error_count':fp+fn,
        'records':rows,
    }

def main():
    bundle,_=load_hf16(); result=score(bundle['cases'])
    out=HERE/'HF16_FIRST_RUN.json'; out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('object','kernel_rule_count','rules_added_beyond_R11','confusion_matrix','metrics','threshold_status','mismatch_count','decision_error_count')},indent=2))
    bad=[r for r in result['records'] if not r['checks']['exact']]
    if bad:
        print(f'--- HF16 MISMATCHES ({len(bad)}) ---')
        for r in bad:
            print(json.dumps({'id':r['id'],'family':r['family'],'input':r['input'],'expected':{k:r['expected'][k] for k in ('status','failure_locus','preserved_facts','missing_authority','reopened')},'observed':r['observed'],'checks':r['checks']},sort_keys=True))

if __name__=='__main__': main()
