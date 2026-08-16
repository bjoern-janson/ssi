#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
K1=HERE.parent
SOURCE=K1/'source'
COMPILER=K1/'compiler'


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

srcmod=load_module('k1_source_reference',SOURCE/'source_reference.py')
ireval=load_module('k1_ir_evaluator',COMPILER/'ir_evaluator.py')

def canon_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def node_count(p):
    if not p: return 0
    return 1+sum(node_count(x) for x in p.get('premises',[]))

def compare_lineage(src, comp):
    if src is None or comp is None:
        return False, 'MISSING_DERIVATION'
    if src.get('rule') != comp.get('source_rule_ancestor'):
        return False, f'ANCESTRY:{src.get("rule")}!={comp.get("source_rule_ancestor")}'
    if src.get('source') != comp.get('source') or src.get('target') != comp.get('target'):
        return False, 'JUDGMENT_ENDPOINT_MISMATCH'
    rule=src.get('rule')
    if rule=='REPLACEMENT':
        if src.get('source_rule') != comp.get('source_rule_label'):
            return False, 'SOURCE_RULE_LABEL_MISMATCH'
        if src.get('substitution',{}) != comp.get('substitution',{}):
            return False, 'SUBSTITUTION_MISMATCH'
    if rule=='CONGRUENCE' and src.get('operator') != comp.get('operator'):
        return False, 'CONGRUENCE_OPERATOR_MISMATCH'
    if rule=='TRANSITIVITY' and src.get('middle') != comp.get('middle'):
        return False, 'TRANSITIVITY_MIDDLE_MISMATCH'
    sp=src.get('premises',[]); cp=comp.get('premises',[])
    if len(sp)!=len(cp): return False, 'PREMISE_ARITY_MISMATCH'
    for a,b in zip(sp,cp):
        ok,why=compare_lineage(a,b)
        if not ok: return False, why
    return True, None

def structural_distinction_losses(ir, case_results, lineage_mismatch):
    losses=set()
    # Frozen witness decisions are checked for every distinction.
    dspec=json.loads((SOURCE/'distinctions.json').read_text())['distinctions']
    by_id={x['id']:x for x in case_results}
    for d in dspec:
        for w in (d['witness_positive'],d['witness_negative']):
            if not by_id[w]['judgment_match']:
                losses.add(d['id'])
    if ir.get('direction')!='FORWARD_ONLY': losses.add('DIST-001')
    labels={r['label'] for r in ir.get('source_rule_templates',[])}
    if not {'r_ab','r_bc'}.issubset(labels): losses.add('DIST-002')
    if ir.get('congruence_policy')!='PRESERVE_OPERATOR': losses.add('DIST-003')
    rfg=[r for r in ir.get('source_rule_templates',[]) if r.get('label')=='r_fg']
    if not rfg or rfg[0].get('variables')!=['x']: losses.add('DIST-004')
    if ir.get('replacement_policy')!='VARIABLE_EVOLUTION_REQUIRES_RELATION': losses.add('DIST-005')
    if not any(r.get('opcode')=='CHAIN' for r in ir.get('deduction_rules',[])): losses.add('DIST-006')
    if ir.get('congruence_policy')!='PRESERVE_OPERATOR' or ir.get('direction')!='FORWARD_ONLY': losses.add('DIST-007')
    if lineage_mismatch: losses.add('DIST-008')
    return sorted(losses)

def score(ir,tasks,gold):
    universe=ireval.universe(ir)
    cases=[]; overreach=loss=correct=representable=lineage_mismatch=fabrication=0
    src_nodes=comp_nodes=recovered_nodes=0
    for q in tasks:
        sg=srcmod.adjudicate_keys(q['source'],q['target'])
        frozen=gold[q['id']]
        assert sg['licensed']==frozen['licensed']
        if sg['licensed']:
            assert sg['derivation']['rule']==frozen['derivation_root']
            assert canon_hash(sg['derivation'])==frozen['derivation_sha256']
        else:
            assert canon_hash(sg['rejection'])==frozen['rejection_sha256']
        representable += int(q['source'] in universe and q['target'] in universe)
        got=ireval.evaluate(q['source'],q['target'],ir)
        match=(got['judgment']==sg['licensed'])
        correct += int(match)
        if (not sg['licensed']) and got['judgment']: overreach += 1
        if sg['licensed'] and (not got['judgment']): loss += 1
        lineage_ok=None; lineage_reason=None
        if sg['licensed'] and got['judgment']:
            src_nodes += node_count(sg['derivation']); comp_nodes += node_count(got['derivation'])
            lineage_ok,lineage_reason=compare_lineage(sg['derivation'],got['derivation'])
            if lineage_ok: recovered_nodes += node_count(sg['derivation'])
            else: lineage_mismatch += 1
        fabrication += len(got.get('fabricated_justification',[]))
        cases.append({'id':q['id'],'source_licensed':sg['licensed'],'ir_judgment':got['judgment'],
                      'judgment_match':match,'lineage_ok':lineage_ok,'lineage_reason':lineage_reason})
    dist_loss=structural_distinction_losses(ir,cases,lineage_mismatch)
    return {
      'A_comp':representable/len(tasks), 'accuracy':correct/len(tasks),
      'correct':correct,'overreach':overreach,'compilation_loss':loss,
      'distinction_loss':dist_loss,'lineage_mismatch':lineage_mismatch,
      'lineage_fabrication':fabrication,
      'source_lineage_nodes':src_nodes,'compiled_lineage_nodes':comp_nodes,
      'lineage_recovery_rate': (recovered_nodes/src_nodes if src_nodes else 1.0),
      'cases':cases
    }

def apply_mutation(base,m):
    ir=copy.deepcopy(base); p=m['patch']
    if 'direction' in p: ir['direction']=p['direction']
    if 'drop_source_rule' in p:
        ir['source_rule_templates']=[r for r in ir['source_rule_templates'] if r['label']!=p['drop_source_rule']]
    if 'congruence_policy' in p: ir['congruence_policy']=p['congruence_policy']
    if 'replacement_policy' in p: ir['replacement_policy']=p['replacement_policy']
    if 'rule_ancestry' in p:
        for r in ir['deduction_rules']:
            if r['id'] in p['rule_ancestry']: r['source_rule_ancestor']=p['rule_ancestry'][r['id']]
    if p.get('inject_fabricated_node'):
        ir['justification']['inject_fabricated_node']=True
    return ir

def detections(score):
    d=[]
    if score['overreach']>0: d.append('COMPILATION_OVERREACH')
    if score['compilation_loss']>0: d.append('COMPILATION_LOSS')
    d += [f'DISTINCTION_LOSS:{x}' for x in score['distinction_loss']]
    if score['lineage_mismatch']>0: d.append('LINEAGE_MISMATCH')
    if score['lineage_fabrication']>0: d.append('LINEAGE_FABRICATION')
    return d

def main():
    tasks=json.loads((SOURCE/'TASKS.json').read_text())['cases']
    gold={x['id']:x for x in json.loads((SOURCE/'gold/GOLD.json').read_text())['cases']}
    base=json.loads((COMPILER/'IR.json').read_text())
    mutations=json.loads((COMPILER/'mutations.json').read_text())['mutations']
    baseline=score(base,tasks,gold)
    mutation_results=[]
    for m in mutations:
        s=score(apply_mutation(base,m),tasks,gold); ds=detections(s)
        expected_ok=all(x in ds for x in m.get('expected_any',[]))
        if 'expected_judgment_accuracy' in m:
            expected_ok = expected_ok and s['accuracy']==m['expected_judgment_accuracy']
        mutation_results.append({'id':m['id'],'name':m['name'],'detections':ds,
                                 'accuracy':s['accuracy'],'overreach':s['overreach'],
                                 'compilation_loss':s['compilation_loss'],
                                 'lineage_mismatch':s['lineage_mismatch'],
                                 'lineage_fabrication':s['lineage_fabrication'],
                                 'expected_satisfied':expected_ok})
    baseline_strong=(baseline['A_comp']==1 and baseline['accuracy']==1 and baseline['overreach']==0 and
        baseline['compilation_loss']==0 and baseline['distinction_loss']==[] and baseline['lineage_mismatch']==0 and
        baseline['lineage_fabrication']==0 and baseline['lineage_recovery_rate']==1)
    mutations_strong=all(x['expected_satisfied'] for x in mutation_results)
    if baseline_strong and mutations_strong:
        status='K1_R2_CROSS_REGIME_STRONG_PASS'
    elif baseline['accuracy']>=0.875 and baseline['overreach']<=1:
        status='K1_R2_CROSS_REGIME_PARTIAL'
    else:
        status='K1_R2_CROSS_REGIME_FAILED'
    out={'object':'K1-CROSS-REGIME-COMPILER-TRANSFER/FIRST_AUDIT','prospective_status':status,
         'baseline':baseline,'mutations':mutation_results,'mutations_caught':f'{sum(x["expected_satisfied"] for x in mutation_results)}/{len(mutation_results)}',
         'authority_ceiling':{'cross_regime_transfer_supported': status=='K1_R2_CROSS_REGIME_STRONG_PASS',
                              'universal_compiler':False,'external_niche_advantage':False,'K0_modified':False}}
    (HERE/'K1_R2_FIRST_RUN.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    summary={'object':out['object'],'prospective_status':status,
             'baseline':{k:baseline[k] for k in ['A_comp','accuracy','overreach','compilation_loss','distinction_loss','lineage_mismatch','lineage_fabrication','lineage_recovery_rate']},
             'mutations_caught':out['mutations_caught'],
             'mutation_detections':[{'id':m['id'],'detections':m['detections'],'accuracy':m['accuracy'],'expected_satisfied':m['expected_satisfied']} for m in mutation_results]}
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__': main()
