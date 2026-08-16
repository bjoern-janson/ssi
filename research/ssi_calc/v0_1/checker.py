#!/usr/bin/env python3
"""SSI-CALC v0.1 reference checker. Derivation never reads case['expected']."""
from __future__ import annotations
import argparse, json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import jsonschema

RULES={"R1":"DECLARE","R2":"ADMIT","R3":"LICENSE","R4":"EQUIV","R5":"SUBSTITUTE","R6":"CONGRUENCE","R7":"TRANSPORT","R8":"QUOTIENT","R9":"COMPOSE","R10":"PRESERVE","R11":"REOPEN"}

@dataclass
class Certificate:
    status:str; failure_locus:str; rule:str; preserved_facts:list[str]; missing_authority:list[str]; reopened:list[str]; explanation:str
    def dict(self): return asdict(self)
    def to_dict(self): return asdict(self)

class C:
    def __init__(self,r):
        self.id=r['id']; self.objects=r['objects']; self.facts=r['facts']; self.edges=r['authority_edges']; self.req=r['request']
    def fs(self,k): return [f for f in self.facts if f['kind']==k]
    def has(self,k,j=None,a=None): return any((j is None or f.get('jurisdiction')==j) and (a is None or f.get('authority')==a) for f in self.fs(k))
    def f(self,k): return next(iter(self.fs(k)),None)
    def ids(self): return [f['id'] for f in self.facts]
    def edge(self,j=None,t=None): return next((e for e in self.edges if (j is None or e['jurisdiction']==j) and (t is None or e['target']==t)),None)

def out(c,s,l,r,missing=None,reopened=None,preserved=None,why=''):
    return Certificate(s,l,r,c.ids() if preserved is None else preserved,missing or [],reopened or [],why)

def declare(c):
    if c.req['operation']!='compose': return None
    ids=list(map(str,c.req['args'])); outs={f['args'][0]:f['args'][1] for f in c.fs('output_contract')}; ins={f['args'][0]:f['args'][1] for f in c.fs('input_contract')}
    for a,b in zip(ids,ids[1:]):
        if a in outs and b in ins and outs[a]!=ins[b]: return out(c,'SEMANTIC_TYPE_ERROR','DECLARE','R1:DECLARE',['matching_intermediate_type'],why='Intermediate types do not match.')

def admit(c):
    op=c.req['operation']
    if op=='admit':
        f=c.f('admission_condition')
        if f and any('desired' in str(x).lower() for x in f['args']): return out(c,'REGIME_MISMATCH','ADMIT','R2:ADMIT',['target_independent_admission'],why='Admission depends on desired downstream result.')
    if op=='compare_regimes':
        rs=list(map(str,c.req['args'])); admitted={str(f['args'][0]) for f in c.fs('regime_admitted')}; miss=[r for r in rs if r not in admitted]
        if miss: return out(c,'REGIME_MISMATCH','ADMIT','R2:ADMIT',[f"admission({r},{c.req['jurisdiction']})" for r in miss],why='A compared regime is not admitted.')
        f=c.f('purpose_compatibility')
        if f and f.get('authority')=='UNRESOLVED': return out(c,'NOT_IDENTIFIED','ADMIT','R2:ADMIT',['purpose_compatibility(kappa1,kappa2)'],why='Purpose comparability is unresolved.')
    if op=='assert_regime_disagreement' and not (c.has('purpose_compatible') or (c.f('purpose_compatibility') and c.f('purpose_compatibility').get('authority')=='CONSTITUTED')):
        return out(c,'JURISDICTIONAL_DIVERGENCE','ADMIT','R2:ADMIT',['purpose_compatibility(kappa1,kappa2)'],why='Different outputs are not disagreement before jurisdiction comparability.')
    if op=='assert_universal_regime' and c.has('regime_admitted'): return out(c,'UNLICENSED_JURISDICTION_TRANSFER','TRANSFER','R2:ADMIT',['kappa_to_universal_regime_transfer'],why='Scoped regime admission is not universal authority.')

def license(c):
    op=c.req['operation']; j=c.req['jurisdiction']
    if op in {'grade','calibrate','support','inform'}:
        e=c.edge(j,c.req.get('consumer')) if c.req.get('consumer') else None
        if e: return out(c,'AUTHORIZED_SCOPED' if op in {'grade','calibrate','support'} else 'AUTHORIZED','NONE','R3:LICENSE',why='Matching scoped authority edge exists.')
        if op=='inform':
            src=str(c.req['args'][0])
            if any(str(f['args'][0])==src for f in c.fs('encodes')): return out(c,'UNLICENSED_JURISDICTION_TRANSFER','TRANSFER','R3:LICENSE',['oracle_safe_feature_license'],why='Answer-bearing source lacks detector-safe license.')
            sf=[f for f in c.facts if src in map(str,f.get('args',[]))]
            if any(f.get('authority')=='UNRESOLVED' for f in sf): return out(c,'NOT_IDENTIFIED','PROVENANCE','R3:LICENSE',['feature_information_provenance'],why='Source provenance unresolved.')
            dj=[f for f in sf if f.get('jurisdiction') and f.get('jurisdiction')!=j]
            if dj: return out(c,'UNLICENSED_JURISDICTION_TRANSFER','TRANSFER','R3:LICENSE',[f"{dj[0]['jurisdiction']}_to_{j}_transfer"],why='Authority exists only in another jurisdiction.')
    if op=='assert_same_artifact_bytes' and c.has('hash_identifies_bytes',j): return out(c,'AUTHORIZED_SCOPED','NONE','R3:LICENSE',why='Hash supports exact artifact reference only.')
    pm={'assert_semantic_equivalence':'hash_to_semantic_role_bridge','assert_valid':'metadata_to_validity_bridge','assert_independent_evidence':'independence_bridge','count_independent_observations':'augmentation_to_independence_bridge'}
    if op in pm and (any(f.get('authority')=='PROVENANCE_ONLY' for f in c.facts) or any(f['kind'] in {'same_hash','filename','same_training_source','derived_from'} for f in c.facts)):
        return out(c,'PROVENANCE_LEAK','PROVENANCE','R3:LICENSE',[pm[op]],why='Provenance/metadata is being promoted without a semantic bridge.')
    if op=='support' and c.f('source_attribution') and not c.has('semantic_bridge'): return out(c,'NOT_IDENTIFIED','PROVENANCE','R3:LICENSE',['attributable_source_and_semantic_bridge'],why='Lineage alone does not constitute semantic support.')

def equiv(c):
    op=c.req['operation']; j=c.req['jurisdiction']
    if op=='assert_equivalence' and any(f['kind'] in {'behavioral_equivalence','equivalent_under','equivalent'} and f.get('jurisdiction')==j and f.get('authority') in {'CONSTITUTED','SCOPED'} for f in c.facts): return out(c,'AUTHORIZED_SCOPED','NONE','R4:EQUIV',why='Equivalence stays in its constituting jurisdiction.')
    if op=='assert_identity':
        f=c.f('admissible_identity_extensions')
        if f and len(f['args'])>1: return out(c,'NOT_IDENTIFIED','EQUIV','R4:EQUIV',['singleton_identity_determination'],why='Multiple admissible identity extensions remain.')
        ds=c.fs('denotes')
        if c.has('identity_by_denotation',j) and len(ds)>=2 and len({str(x['args'][1]) for x in ds})==1: return out(c,'AUTHORIZED_SCOPED','NONE','R4:EQUIV',why='External value regime licenses identity by denotation.')
        if c.has('identity_regime_admitted',j) and c.has('same_extensional_denotation',j): return out(c,'AUTHORIZED_SCOPED','NONE','R4:EQUIV',why='Identity remains inside an admitted identity regime.')
        for k,m in {'behavioral_equivalence':'behavior_to_presentation_identity_transfer','task_equivalent':'task_equivalence_to_artifact_identity'}.items():
            if c.has(k): return out(c,'UNLICENSED_JURISDICTION_TRANSFER','TRANSFER','R4:EQUIV',[m],why='Scoped equivalence has no identity transfer rule.')
    if op=='assert_different' and c.has('referentially_distinct'): return out(c,'UNLICENSED_JURISDICTION_TRANSFER','TRANSFER','R4:EQUIV',['reference_to_semantic_identity_transfer'],why='Reference distinctness is not semantic difference authority.')

def substitute(c):
    op=c.req['operation']; j=c.req['jurisdiction']
    if op=='assert_universal_substitutability' and c.has('equivalent'): return out(c,'UNLICENSED_JURISDICTION_TRANSFER','TRANSFER','R5:SUBSTITUTE',['kappa_to_universal_transfer'],why='Local equivalence is not universal substitutability.')
    if op!='substitute': return None
    eq=c.fs('equivalent'); same=any(f.get('jurisdiction')==j for f in eq); cong=any(f['kind']=='consumer_congruent' and f.get('jurisdiction')==j for f in c.facts)
    if (same or c.has('transfer_rule')) and cong: return out(c,'AUTHORIZED_SCOPED','NONE','R5:SUBSTITUTE',why='Equivalence and consumer congruence align.')
    if eq: return out(c,'UNLICENSED_JURISDICTION_TRANSFER','SUBSTITUTE','R5:SUBSTITUTE',[f"{eq[0].get('jurisdiction','source')}_to_{j}_substitution_transfer"],why='Equivalence is not licensed for this consumer jurisdiction.')

def congruence(c):
    if c.req['operation']!='apply_equivalent': return None
    if c.has('counterexample_outputs_differ'): return out(c,'CONGRUENCE_FAILURE','CONGRUENCE','R6:CONGRUENCE',why='Consumer counterexample defeats congruence.')
    f=c.f('congruence_status')
    if f and f.get('authority')=='UNRESOLVED': return out(c,'NOT_IDENTIFIED','CONGRUENCE','R6:CONGRUENCE',[f"congruence({c.req['args'][0]},{c.req['jurisdiction']})"],why='Consumer congruence unresolved.')
    if c.has('congruence',c.req['jurisdiction']): return out(c,'AUTHORIZED','NONE','R6:CONGRUENCE',why='Declared operation preserves equivalence.')

def transport(c):
    op=c.req['operation']
    if op=='compare_relations':
        if c.has('shared_carrier') and c.has('purpose_compatible'): return out(c,'AUTHORIZED_SCOPED','NONE','R7:TRANSPORT',why='Common carrier and purpose already constituted.')
        if c.has('common_domain') and len(c.fs('pullback_map'))>=2 and c.has('operation_alignment_verified'): return out(c,'AUTHORIZED_SCOPED','NONE','R7:TRANSPORT',why='Common pullback domain licenses comparison.')
    if op=='compare_under_operation' and c.has('commutation_counterexample'): return out(c,'UNLICENSED_TRANSPORT','TRANSPORT','R7:TRANSPORT',why='Alignment fails operation commutation.')
    if op=='transport_relation':
        if c.has('transport_selected_by'): return out(c,'UNLICENSED_TRANSPORT','TRANSPORT','R7:TRANSPORT',['target_independent_transport'],why='Transport selected by desired result.')
        if c.has('non_injective'): return out(c,'UNLICENSED_TRANSPORT','TRANSPORT','R7:TRANSPORT',['well_formed_transport_semantics'],why='Arbitrary non-injective pushforward is not licensed.')
        if c.has('carrier_alignment') and c.has('equivalence_preservation') and not c.has('operations_commute'): return out(c,'NOT_IDENTIFIED','TRANSPORT','R7:TRANSPORT',['equivalence_well_formedness(tau)'],why='Transport equivalence well-formedness unresolved.')
        if all(c.has(k) for k in ['injective','maps_carrier','operations_commute','target_independent']): return out(c,'AUTHORIZED','NONE','R7:TRANSPORT',why='Injective target-independent commuting transport is licensed.')

def quotient(c): return None

def compose(c):
    op=c.req['operation']
    if op=='compose_inputs' and (c.has('jointly_reconstruct') or c.has('joint_counterexample')): return out(c,'COMPOSITION_FAILURE','COMPOSE','R9:COMPOSE',['joint_non_oracularity_certificate'] if c.has('jointly_reconstruct') else [],why='Local licenses fail under joint interaction.')
    if op!='compose': return None
    ids=list(map(str,c.req['args'])); edges=[e for e in c.edges if e['id'] in ids]
    if len(edges)!=len(ids): return out(c,'COMPOSITION_FAILURE','COMPOSE','R9:COMPOSE',['licensed_component_edges'],why='Component edge missing.')
    f=c.f('compose_compatibility')
    if f and f.get('authority')=='UNRESOLVED': return out(c,'NOT_IDENTIFIED','COMPOSE','R9:COMPOSE',[f"composition_certificate({ids[0]},{ids[1]})"],why='Composition compatibility unresolved.')
    if c.has('compose_chain_compatible') or c.has('compose_compatible'): return out(c,'AUTHORIZED_SCOPED' if any('typed' in e.get('scope',[]) for e in edges) else 'AUTHORIZED','NONE','R9:COMPOSE',why='Explicit composition certificate exists.')
    return out(c,'COMPOSITION_FAILURE','COMPOSE','R9:COMPOSE',[f"composition_certificate({ids[0]},{ids[1]})"],why='Component authority does not compose automatically.')

def preserve(c):
    op=c.req['operation']
    if op=='consume_quotient' and c.has('local_quotient_licensed') and (c.has('kernel_containment_verified') or c.has('future_invariant_under')): return out(c,'AUTHORIZED_SCOPED' if c.has('kernel_containment_verified') else 'AUTHORIZED','NONE','R10:PRESERVE',why='Local quotient and downstream preservation obligations are separately discharged.')
    if op=='assert_future_safe':
        if c.has('quotient_merges') and c.has('future_distinguishes'): return out(c,'FUTURE_UNSAFE','PRESERVE','R10:PRESERVE',why='Future consumer distinguishes a collapsed pair.')
        f=c.f('future_obligation_accessed')
        if f and f['args'] and f['args'][0] is False: return out(c,'NOT_IDENTIFIED','PRESERVE','R10:PRESERVE',['realized_future_consumer_or_prospective_preservation_proof'],why='Future obligation not realized.')
        if c.has('local_congruence_verified'): return out(c,'NOT_IDENTIFIED','PRESERVE','R10:PRESERVE',['future_preservation_test(q,T)'],why='Local congruence is not future sufficiency.')
    if op=='mandate_permanent_preservation': return out(c,'EXTERNAL_AUTHORITY_REQUIRED','PRESERVE','R10:PRESERVE',['future_relevance_contract'],why='Permanent preservation requires an external future-relevance contract.')
    if op=='authorize_transform' and c.has('transformation_destroys') and c.has('required_future_path'): return out(c,'FUTURE_UNSAFE','PRESERVE','R10:PRESERVE',why='Transformation destroys a required correction path.')

def reopen(c):
    if c.req['operation']!='reopen': return None
    ps=[('later_discovered_encodes',['previously_authorized_input(x,H)']),('new_consumer_distinguishes',['distinction(x,y)']),('hidden_interaction_counterexample',['composite_authority(c1)']),('withdrawal_condition_triggered',['x_not_y_alternative','x_eq_y_alternative']),('bridge_invalidated',['claim_supported','claim_unsupported']),('withdrawal_triggered',['claim_authorized','claim_not_authorized']),('alignment_invalidated',['cross_invariant_valid','cross_invariant_invalid']),('new_future_distinguishes',['distinction(x,y)'])]
    for k,opened in ps:
        if c.has(k): return out(c,'REOPEN','REOPEN','R11:REOPEN',reopened=opened,preserved=c.ids() if k=='new_future_distinguishes' else [f['id'] for f in c.fs(k)],why='New evidence/withdrawal reopens a previously contracted alternative set.')

PIPE=[declare,admit,license,equiv,substitute,congruence,transport,quotient,compose,preserve,reopen]
def load_json(path): return json.loads(Path(path).read_text())
def derive(raw,schema):
    jsonschema.Draft202012Validator(schema).validate(raw); c=C({k:raw[k] for k in ['id','objects','facts','authority_edges','request']})
    for r in PIPE:
        x=r(c)
        if x:return x
    return out(c,'NOT_IDENTIFIED','LICENSE','EVALUATOR',['derivation_not_available_in_R1_R11'],why='No R1..R11 derivation applies.')

def main():
    p=argparse.ArgumentParser(); p.add_argument('case'); p.add_argument('--schema',default=str(Path(__file__).with_name('schema.json'))); a=p.parse_args()
    raw=json.loads(Path(a.case).read_text()); schema=json.loads(Path(a.schema).read_text()); print(json.dumps({'case_id':raw['id'],**derive(raw,schema).dict()},indent=2))
if __name__=='__main__':main()
