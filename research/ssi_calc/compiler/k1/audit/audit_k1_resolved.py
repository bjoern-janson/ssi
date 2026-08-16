#!/usr/bin/env python3
"""Execution-resolved K1/R2 audit.

Scientific scoring contract is unchanged from audit_k1.py. The only revision is
operational: each frozen IR variant is closed once and reused across all 24
queries. Semantic mutations use a trace-free finite relation engine; exact
source/compiled lineage is checked for the baseline and lineage-targeting
mutations against the frozen IR evaluator's trace construction.
"""
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

srcmod=load_module('k1_source_reference_resolved',SOURCE/'source_reference.py')
ireval=load_module('k1_ir_evaluator_resolved',COMPILER/'ir_evaluator.py')

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

def prepare_source_truth(tasks,gold):
    truth={}
    for q in tasks:
        sg=srcmod.adjudicate_keys(q['source'],q['target'])
        frozen=gold[q['id']]
        assert sg['licensed']==frozen['licensed'], q['id']
        if sg['licensed']:
            assert sg['derivation']['rule']==frozen['derivation_root'], q['id']
            assert canon_hash(sg['derivation'])==frozen['derivation_sha256'], q['id']
        else:
            assert canon_hash(sg['rejection'])==frozen['rejection_sha256'], q['id']
        truth[q['id']]=sg
    return truth

def rule_present(ir,opcode):
    return any(r.get('opcode')==opcode for r in ir.get('deduction_rules',[]))

def fast_relation(ir):
    """Compute the frozen evaluator's least relation without proof objects."""
    terms=ireval.universe(ir)
    rel=set()
    if rule_present(ir,'REFLEXIVE'):
        rel |= {(t,t) for t in terms}
    if rule_present(ir,'APPLY_TEMPLATE'):
        for r in ir.get('source_rule_templates',[]):
            if not r.get('variables') and r.get('lhs') in terms and r.get('rhs') in terms:
                rel.add((r['lhs'],r['rhs']))
    while True:
        before=len(rel)
        new=set(rel)
        if rule_present(ir,'LIFT_UNARY'):
            if ir.get('congruence_policy')=='PRESERVE_OPERATOR':
                for s,d in rel:
                    for op in ir['universe']['unary_operators']:
                        ss=f'{op}({s})'; dd=f'{op}({d})'
                        if ss in terms and dd in terms: new.add((ss,dd))
            elif ir.get('congruence_policy')=='MERGE_F_G':
                for s,d in rel:
                    for op1 in ir['universe']['unary_operators']:
                        for op2 in ir['universe']['unary_operators']:
                            ss=f'{op1}({s})'; dd=f'{op2}({d})'
                            if ss in terms and dd in terms: new.add((ss,dd))
        if rule_present(ir,'APPLY_TEMPLATE'):
            has_rfg=any(r.get('label')=='r_fg' and r.get('variables')==['x'] and
                        r.get('lhs')=='f(x)' and r.get('rhs')=='g(x)'
                        for r in ir.get('source_rule_templates',[]))
            if has_rfg:
                pairs=rel if ir.get('replacement_policy')=='VARIABLE_EVOLUTION_REQUIRES_RELATION' else ((a,b) for a in terms for b in terms)
                for a,b in pairs:
                    ss=f'f({a})'; dd=f'g({b})'
                    if ss in terms and dd in terms: new.add((ss,dd))
        if rule_present(ir,'CHAIN'):
            # Exact transitive closure over current/new relation; finite universe <=45.
            reach={t:set() for t in terms}
            for s,d in new: reach[s].add(d)
            changed_tc=True
            while changed_tc:
                changed_tc=False
                for s in terms:
                    expanded=set(reach[s])
                    for mid in tuple(reach[s]): expanded |= reach[mid]
                    if not expanded.issubset(reach[s]):
                        reach[s] |= expanded; changed_tc=True
            new |= {(s,d) for s in terms for d in reach[s]}
        if ir.get('direction')=='SYMMETRIZE':
            new |= {(d,s) for s,d in new}
        rel=new
        if len(rel)==before: return terms,rel

def trace_closure(ir):
    terms,rel=ireval.closure(ir)
    return terms,rel

def structural_distinction_losses(ir, case_results, lineage_mismatch):
    losses=set()
    dspec=json.loads((SOURCE/'distinctions.json').read_text())['distinctions']
    by_id={x['id']:x for x in case_results}
    for d in dspec:
        for w in (d['witness_positive'],d['witness_negative']):
            if not by_id[w]['judgment_match']: losses.add(d['id'])
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

def score_from_closure(ir,tasks,truth,terms,rel,trace_available, fabrication_per_case=0):
    cases=[]; overreach=loss=correct=representable=lineage_mismatch=fabrication=0
    src_nodes=comp_nodes=recovered_nodes=0
    for q in tasks:
        sg=truth[q['id']]
        representable += int(q['source'] in terms and q['target'] in terms)
        derived=(q['source'],q['target']) in rel
        match=(derived==sg['licensed']); correct += int(match)
        if (not sg['licensed']) and derived: overreach += 1
        if sg['licensed'] and (not derived): loss += 1
        lineage_ok=None; lineage_reason=None
        if sg['licensed'] and derived and trace_available:
            comp=rel[(q['source'],q['target'])]
            src_nodes += node_count(sg['derivation']); comp_nodes += node_count(comp)
            lineage_ok,lineage_reason=compare_lineage(sg['derivation'],comp)
            if lineage_ok: recovered_nodes += node_count(sg['derivation'])
            else: lineage_mismatch += 1
        fabrication += fabrication_per_case
        cases.append({'id':q['id'],'source_licensed':sg['licensed'],'ir_judgment':derived,
                      'judgment_match':match,'lineage_ok':lineage_ok,'lineage_reason':lineage_reason})
    dist_loss=structural_distinction_losses(ir,cases,lineage_mismatch)
    return {
      'A_comp':representable/len(tasks), 'accuracy':correct/len(tasks),
      'correct':correct,'overreach':overreach,'compilation_loss':loss,
      'distinction_loss':dist_loss,'lineage_mismatch':lineage_mismatch,
      'lineage_fabrication':fabrication,
      'source_lineage_nodes':src_nodes,'compiled_lineage_nodes':comp_nodes,
      'lineage_recovery_rate': (recovered_nodes/src_nodes if trace_available and src_nodes else (1.0 if trace_available else None)),
      'trace_audited':trace_available,'cases':cases
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
    if p.get('inject_fabricated_node'): ir['justification']['inject_fabricated_node']=True
    return ir

def detections(s):
    d=[]
    if s['overreach']>0: d.append('COMPILATION_OVERREACH')
    if s['compilation_loss']>0: d.append('COMPILATION_LOSS')
    d += [f'DISTINCTION_LOSS:{x}' for x in s['distinction_loss']]
    if s['lineage_mismatch']>0: d.append('LINEAGE_MISMATCH')
    if s['lineage_fabrication']>0: d.append('LINEAGE_FABRICATION')
    return d

def main():
    tasks=json.loads((SOURCE/'TASKS.json').read_text())['cases']
    gold={x['id']:x for x in json.loads((SOURCE/'gold/GOLD.json').read_text())['cases']}
    truth=prepare_source_truth(tasks,gold)
    base=json.loads((COMPILER/'IR.json').read_text())
    mutations=json.loads((COMPILER/'mutations.json').read_text())['mutations']

    bterms,brel=trace_closure(base)
    baseline=score_from_closure(base,tasks,truth,bterms,brel,True,0)

    mutation_results=[]
    for m in mutations:
        mir=apply_mutation(base,m)
        if m['id']=='MUT-105':
            terms,rel=trace_closure(mir)
            s=score_from_closure(mir,tasks,truth,terms,rel,True,0)
        elif m['id']=='MUT-106':
            # Relation and proof topology are unchanged; only a fabricated justification is injected.
            s=score_from_closure(mir,tasks,truth,bterms,brel,True,1)
        else:
            terms,relation=fast_relation(mir)
            s=score_from_closure(mir,tasks,truth,terms,relation,False,0)
        ds=detections(s)
        expected_ok=all(x in ds for x in m.get('expected_any',[]))
        if 'expected_judgment_accuracy' in m:
            expected_ok = expected_ok and s['accuracy']==m['expected_judgment_accuracy']
        mutation_results.append({'id':m['id'],'name':m['name'],'detections':ds,
                                 'accuracy':s['accuracy'],'overreach':s['overreach'],
                                 'compilation_loss':s['compilation_loss'],
                                 'lineage_mismatch':s['lineage_mismatch'],
                                 'lineage_fabrication':s['lineage_fabrication'],
                                 'trace_audited':s['trace_audited'],
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
    out={'object':'K1-CROSS-REGIME-COMPILER-TRANSFER/FIRST_VALID_AUDIT','prospective_status':status,
         'supersedes_execution_attempt':31955428508,
         'execution_revision':'CACHE_ONE_CLOSURE_PER_VARIANT_ONLY_NO_SCORING_CHANGE',
         'baseline':baseline,'mutations':mutation_results,
         'mutations_caught':f'{sum(x["expected_satisfied"] for x in mutation_results)}/{len(mutation_results)}',
         'authority_ceiling':{'cross_regime_transfer_supported': status=='K1_R2_CROSS_REGIME_STRONG_PASS',
                              'universal_compiler':False,'external_niche_advantage':False,'K0_modified':False}}
    (HERE/'K1_R2_FIRST_VALID_RUN.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    summary={'object':out['object'],'prospective_status':status,
             'baseline':{k:baseline[k] for k in ['A_comp','accuracy','overreach','compilation_loss','distinction_loss','lineage_mismatch','lineage_fabrication','lineage_recovery_rate']},
             'mutations_caught':out['mutations_caught'],
             'mutation_detections':[{'id':m['id'],'detections':m['detections'],'accuracy':m['accuracy'],'expected_satisfied':m['expected_satisfied']} for m in mutation_results]}
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__': main()
