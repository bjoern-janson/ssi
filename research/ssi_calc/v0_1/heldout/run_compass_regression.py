#!/usr/bin/env python3
"""Regression harness for the SSI-CALC v0.1 Compass-orchestration successor.

Frozen inputs are not mutated. B64 remains contract conformance; H24 is regression only.
"""
from __future__ import annotations
import base64, gzip, hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import checker_orchestrated as checker

SCHEMA=json.loads((ROOT/'schema.json').read_text())
AUTHORIZED={'AUTHORIZED','AUTHORIZED_SCOPED'}
H24_SHA='0910569fe786b29f5f1d64c295f8be7f2857ec6447bd2cf3286a336fc121b941'

def load_h24():
    raw=gzip.decompress(base64.b64decode((HERE/'H24.json.gz.b64').read_text().strip()))
    assert hashlib.sha256(raw).hexdigest()==H24_SHA
    return json.loads(raw)

def score(cases, name):
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
        rows.append({'id':case['id'],'family':case.get('family'),'expected':exp,'observed':got,'checks':checks,'expected_authorize':ea,'predicted_authorize':pa})
    n=len(rows); licensed=sum(r['expected_authorize'] for r in rows); unlicensed=n-licensed
    fp=sum((not r['expected_authorize']) and r['predicted_authorize'] for r in rows)
    fn=sum(r['expected_authorize'] and (not r['predicted_authorize']) for r in rows)
    decision=sum(r['checks']['decision'] for r in rows)/n
    metrics={
        'cases':n,
        'decision_accuracy':decision,
        'overreach_rate':fp/unlicensed if unlicensed else 0.0,
        'false_refusal_rate':fn/licensed if licensed else 0.0,
        'status_accuracy':sum(r['checks']['status'] for r in rows)/n,
        'locus_accuracy':sum(r['checks']['locus'] for r in rows)/n,
        'preserved_accuracy':sum(r['checks']['preserved'] for r in rows)/n,
        'missing_accuracy':sum(r['checks']['missing'] for r in rows)/n,
        'reopened_accuracy':sum(r['checks']['reopened'] for r in rows)/n,
        'exact_certificate_accuracy':sum(r['checks']['exact'] for r in rows)/n,
        'mismatch_count':sum(not r['checks']['exact'] for r in rows),
        'decision_error_count':sum(not r['checks']['decision'] for r in rows),
    }
    return {'object':name,'metrics':metrics,'records':rows}

def main():
    b64=[json.loads(p.read_text()) for p in sorted((ROOT/'benchmark').glob('CASE-*.json'))]
    h24=load_h24()['cases']
    result={'kernel_rule_count':len(checker.RULES),'rules_added_beyond_R11':0,'B64':score(b64,'B64'),'H24':score(h24,'H24_REGRESSION')}
    out=HERE/'COMPASS_REGRESSION_RESULT.json'; out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'kernel_rule_count':result['kernel_rule_count'],'rules_added_beyond_R11':0,'B64':result['B64']['metrics'],'H24':result['H24']['metrics']},indent=2))
    for bucket in ('B64','H24'):
        bad=[r for r in result[bucket]['records'] if not r['checks']['exact']]
        if bad:
            print(f'--- {bucket} MISMATCHES ({len(bad)}) ---')
            for r in bad:
                print(json.dumps({'id':r['id'],'expected':{k:r['expected'][k] for k in ('status','failure_locus','preserved_facts','missing_authority','reopened')},'observed':r['observed'],'checks':r['checks']},sort_keys=True))
    if result['B64']['metrics']['exact_certificate_accuracy'] < 1.0:
        raise SystemExit(2)

if __name__=='__main__': main()
