#!/usr/bin/env python3
"""SSI-CALC v0.1 successor evaluator: implementation-only Compass orchestration repair.

The R1..R11 kernel is unchanged. This module wraps the frozen reference checker and
adds derivation-state orchestration required by the H24 implementation analysis.
It never reads benchmark family metadata or case['expected'] during derivation.
"""
from __future__ import annotations
from collections import deque
import jsonschema
import checker as frozen

RULES = frozen.RULES
Certificate = frozen.Certificate
ACTIVE = {None, "CONSTITUTED", "SCOPED"}

class C:
    def __init__(self, raw):
        self.objects=raw['objects']; self.facts=raw['facts']; self.edges=raw['authority_edges']; self.req=raw['request']
    def fs(self, kind): return [f for f in self.facts if f['kind']==kind]
    def active(self, fact): return fact.get('authority') in ACTIVE
    def afs(self, kind): return [f for f in self.fs(kind) if self.active(f)]
    def ahas(self, kind, jurisdiction=None):
        return any(jurisdiction is None or f.get('jurisdiction')==jurisdiction for f in self.afs(kind))
    def transfer(self, source, target):
        source,target=str(source),str(target)
        for f in self.afs('transfer_rule'):
            a=list(map(str,f.get('args',[])))
            if len(a)>=2 and a[0]==source and a[1]==target: return f
        return None
    def transfer_path(self, source, target):
        source,target=str(source),str(target); adj={}
        for f in self.afs('transfer_rule'):
            a=list(map(str,f.get('args',[])))
            if len(a)>=2: adj.setdefault(a[0],[]).append((a[1],f))
        q=deque([(source,[])]); seen={source}
        while q:
            node,path=q.popleft()
            if node==target: return path
            for nxt,f in adj.get(node,[]):
                if nxt not in seen: seen.add(nxt); q.append((nxt,path+[f]))
        return None

def cert(c,status,locus,rule,missing=None,preserved=None,why=''):
    return Certificate(status,locus,rule,[f['id'] for f in c.facts] if preserved is None else preserved,missing or [],[],why)

def args_cover(f, values):
    args=set(map(str,f.get('args',[]))); return all(str(v) in args for v in values)

def indirect_answer_lineage(c, source):
    source=str(source); enc={str(f['args'][0]) for f in c.afs('encodes') if f.get('args')}; parents={}
    for f in c.afs('derived_from'):
        a=list(map(str,f.get('args',[])))
        if len(a)>=2: parents.setdefault(a[0],[]).append(a[1])
    q=deque([source]); seen={source}
    while q:
        x=q.popleft()
        if x in enc: return True
        for p in parents.get(x,[]):
            if p not in seen: seen.add(p); q.append(p)
    return False

def composition_certificate_covers(c, ids):
    ids=list(map(str,ids))
    for f in c.afs('compose_chain_compatible'):
        if not f.get('args') or args_cover(f,ids): return True
    if len(ids)==2:
        for f in c.afs('compose_compatible'):
            if not f.get('args') or args_cover(f,ids): return True
    return False

def orchestrate(c):
    op=c.req['operation']; j=c.req['jurisdiction']; args=list(map(str,c.req.get('args',[])))

    if op=='inform' and args and indirect_answer_lineage(c,args[0]):
        return cert(c,'UNLICENSED_JURISDICTION_TRANSFER','TRANSFER','R3:LICENSE',['oracle_safe_feature_license'],why='Indirect answer-bearing lineage is not detector-safe authority.')

    if op=='substitute':
        eq=c.afs('equivalent'); cong=c.ahas('consumer_congruent',j)
        if eq:
            src=next((f.get('jurisdiction') for f in eq if f.get('jurisdiction')),None)
            if src and src!=j:
                direct=c.transfer(src,j)
                if direct and cong:
                    return cert(c,'AUTHORIZED_SCOPED','NONE','R5:SUBSTITUTE',why='Exact source-to-target substitution transfer is active.')
                path=c.transfer_path(src,j)
                if path and len(path)>1:
                    ids=[str(f['id']) for f in path]
                    if composition_certificate_covers(c,ids) and cong:
                        return cert(c,'AUTHORIZED_SCOPED','NONE','R5:SUBSTITUTE',why='A licensed transfer chain composes into the requested substitution jurisdiction.')
                    return cert(c,'COMPOSITION_FAILURE','COMPOSE','R9:COMPOSE',[f"composition_certificate({','.join(ids)})"],why='Multi-hop transfer does not compose automatically.')
                if c.afs('transfer_rule'):
                    return cert(c,'UNLICENSED_JURISDICTION_TRANSFER','SUBSTITUTE','R5:SUBSTITUTE',[f"{src}_to_{j}_substitution_transfer"],why='A transfer exists, but not to the requested jurisdiction.')

    if op=='compose':
        edge_by_id={str(e['id']):e for e in c.edges}; requested=args
        if all(i in edge_by_id for i in requested):
            bad=[]
            for i in requested:
                e=edge_by_id[i]; ej=e.get('jurisdiction')
                if ej!=j and not c.transfer(ej,j): bad.append(i)
            if bad:
                return cert(c,'COMPOSITION_FAILURE','COMPOSE','R9:COMPOSE',['component_authority_in_requested_jurisdiction'],why='A component edge is not licensed in the requested composition jurisdiction.')
            pairwise=bool(c.afs('compose_compatible')); chain=bool(c.afs('compose_chain_compatible'))
            if len(requested)>2 and pairwise and not chain:
                return cert(c,'COMPOSITION_FAILURE','COMPOSE','R9:COMPOSE',[f"composition_certificate({','.join(requested)})"],why='Pairwise compatibility does not authorize the whole chain.')
            if (pairwise or chain) and not composition_certificate_covers(c,requested):
                return cert(c,'COMPOSITION_FAILURE','COMPOSE','R9:COMPOSE',[f"composition_certificate({','.join(requested)})"],why='The available certificate does not cover the requested composition.')

    if op=='assert_identity':
        for f in c.afs('identity_transfer_rule'):
            a=list(map(str,f.get('args',[])))
            if len(a)>=2 and (a[1]==j or a[1]=='presentation_identity'):
                return cert(c,'AUTHORIZED_SCOPED','NONE','R4:EQUIV',why='An explicit identity transfer licenses this scoped identity judgment.')
        foreign=next((f for f in c.afs('identity_by_denotation') if f.get('jurisdiction') and f.get('jurisdiction')!=j),None)
        den=c.afs('denotes')
        if foreign and len(den)>=2 and len({str(f['args'][1]) for f in den})==1:
            src=foreign['jurisdiction']
            return cert(c,'NOT_IDENTIFIED','EQUIV','R4:EQUIV',[f"identity_transfer({src},{j})"],why='Identity authority is constituted only in a foreign regime.')

    if op=='assert_semantic_equivalence' and c.ahas('semantic_bridge',j):
        return cert(c,'AUTHORIZED_SCOPED','NONE','R3:LICENSE',why='A constituted semantic bridge licenses this scoped semantic use.')
    if op=='assert_independent_evidence' and c.ahas('independence_bridge',j):
        return cert(c,'AUTHORIZED_SCOPED','NONE','R3:LICENSE',why='A constituted independence bridge licenses this scoped independence judgment.')
    if op=='support' and c.fs('source_attribution') and c.ahas('semantic_bridge',j):
        consumer=c.req.get('consumer')
        matching=next((e for e in c.edges if e.get('jurisdiction')==j and (consumer is None or e.get('target')==consumer)),None)
        if not matching:
            return cert(c,'NOT_IDENTIFIED','LICENSE','R3:LICENSE',['consumer_scoped_support_authority'],why='Lineage and semantic bridge exist, but consumer-scoped support authority is still missing.')

    if op=='compare_regimes':
        regimes=args; admitted={str(f['args'][0]) for f in c.afs('regime_admitted') if f.get('args')}
        unresolved=next((f for f in c.fs('purpose_compatibility') if f.get('authority')=='UNRESOLVED'),None)
        if all(r in admitted for r in regimes) and not unresolved:
            purpose=c.ahas('purpose_compatible') or c.ahas('purpose_compatibility')
            if purpose:
                if c.ahas('shared_carrier'):
                    return cert(c,'AUTHORIZED_SCOPED','NONE','R7:TRANSPORT',why='Admitted purpose-compatible regimes already share a constituted carrier.')
                if c.ahas('common_domain') and len(c.afs('pullback_map'))>=2 and c.ahas('operation_alignment_verified'):
                    return cert(c,'AUTHORIZED_SCOPED','NONE','R7:TRANSPORT',why='Admitted regimes have a constituted pullback alignment.')
                return cert(c,'JURISDICTIONAL_DIVERGENCE','TRANSPORT','R7:TRANSPORT',['constituted_carrier_alignment'],why='Admission and purpose compatibility do not themselves constitute carrier alignment.')

    if op=='assert_universal_regime':
        source=next((f.get('jurisdiction') for f in c.afs('regime_admitted') if f.get('jurisdiction')),None)
        if source and (c.transfer(source,j) or c.transfer(source,'universal_regime')):
            return cert(c,'AUTHORIZED_SCOPED','NONE','R2:ADMIT',why='Explicit scoped-to-universal regime transfer is active.')

    if op=='transport_relation':
        if c.ahas('non_injective') and c.ahas('well_formed_transport_semantics',j) and c.ahas('operations_commute',j) and c.ahas('target_independent',j):
            return cert(c,'AUTHORIZED_SCOPED','NONE','R7:TRANSPORT',why='Constituted quotient-style semantics licenses this non-injective transport.')
        if c.fs('operations_commute') and not c.ahas('operations_commute'):
            return cert(c,'NOT_IDENTIFIED','TRANSPORT','R7:TRANSPORT',['active_operations_commute'],why='Withdrawn or unresolved commutation evidence cannot discharge transport.')

    if op=='consume_quotient' and c.ahas('local_quotient_licensed') and c.fs('future_invariant_under') and not c.ahas('future_invariant_under'):
        return cert(c,'NOT_IDENTIFIED','PRESERVE','R10:PRESERVE',['active_future_invariant_under'],why='Unresolved future invariance cannot discharge preservation.')
    if op=='assert_future_safe' and c.fs('future_distinguishes') and not c.ahas('future_distinguishes'):
        return cert(c,'NOT_IDENTIFIED','PRESERVE','R10:PRESERVE',['active_future_distinction_evidence'],why='Withdrawn future-distinction evidence cannot establish future unsafety.')

    return None

def derive(raw,schema):
    jsonschema.Draft202012Validator(schema).validate(raw)
    c=C({k:raw[k] for k in ['objects','facts','authority_edges','request']})
    advanced=orchestrate(c)
    if advanced is not None: return advanced
    return frozen.derive(raw,schema)

def load_json(path): return frozen.load_json(path)
