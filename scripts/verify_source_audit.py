"""Verify current source audit against immutable snapshots and frozen inputs.

This checks provenance and arithmetic, not the legal correctness of AI coding.
"""
from pathlib import Path
import json,hashlib,collections
ROOT=Path(__file__).resolve().parents[1]
PROJ=ROOT.parent
A=ROOT/'source_audit'
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf8').splitlines() if x.strip()]
def load(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=read(A/'condition_audit_long.jsonl');cases=read(A/'case_audit.jsonl')
manifest=load(A/'source_manifest.json')['sources']
visible={r['case_id']:r for r in read(PROJ/'revision_20261009/evidence_numeric/evidence_visible_inputs.jsonl')}
sources={}
for s in manifest:
    path=Path(s['raw_path']);assert sha(path)==s['raw_sha256']
    raw=load(path);text=raw['text']
    assert hashlib.sha256(text.encode()).hexdigest()==s['text_sha256']
    sources[s['ruling_id']]=text

checks=collections.Counter();unresolved=[]
def checkloc(loc,text,context):
    if not loc:return
    if loc.get('raw_text_span') is not None:
        a,b=loc['raw_text_span'];assert text[a:b]==loc['quote'],context
        checks['continuous_source_spans']+=1
    elif loc.get('source_spans'):
        for span in loc['source_spans']:checkloc(span,text,context)
        checks['noncontiguous_evidence_entries']+=1
    else:unresolved.append({'context':context,'locator':loc})

assert len(rows)==208 and len(cases)==73 and len(sources)==67
assert len({r['condition_key'] for r in rows})==208
for r in rows:
    k=r['condition_key'];v=visible[r['case_id']];text=sources[r['ruling_id']]
    a,b=r['rule_span'];assert v['rule_text'][a:b]==r['rule_quote'],k
    checkloc(r['rule_source_locator'],text,k+':rule')
    for e in r['fact_evidence']:
        a,b=e['frozen_span'];assert v['facts'][a:b]==e['frozen_quote'],k
        checkloc(e['source_locator'],text,k+':fact')
    for e in r['recovered_fact_evidence']:checkloc(e,text,k+':recovered')
    assert r['expert_validated'] is False and r['administrative_y_used_as_criterion'] is False
    assert r['reference_tier'] in ['direct','interpretive','insufficient','disputed']
    assert r['object']['product_scope'] and r['object']['quantifier'] and r['attribute']
    assert r['logical_role'] and r['inference_basis']
bycase=collections.defaultdict(list)
for r in rows:bycase[r['case_id']].append(r)
for c in cases:
    rs=bycase[c['case_id']]
    assert set(c['condition_keys'])=={r['condition_key'] for r in rs}
    for col,target in [('strict_excerpt_state','strict_excerpt_state'),('strict_full_source_state','strict_full_source_state')]:
        states=[r[col] for r in rs if r[col]!='not_applicable']
        expected=('refute' if 'refute' in states else ('support' if set(states)=={'support'} else 'unknown')) if c['safe_flat_conjunction'] else 'logic_unresolved'
        assert c[target]==expected,c['case_id']
summary=load(A/'source_audit_summary.json')
assert summary['reference_tier_counts']==dict(collections.Counter(r['reference_tier'] for r in rows))
assert summary['strict_excerpt_condition_counts']==dict(collections.Counter(r['strict_excerpt_state'] for r in rows))
assert summary['strict_full_condition_counts']==dict(collections.Counter(r['strict_full_source_state'] for r in rows))
assert summary['strict_case_full_counts']==dict(collections.Counter(c['strict_full_source_state'] for c in cases))
restored=[r for r in rows if r['strict_excerpt_state']=='unknown' and r['strict_full_source_state']=='support']
assert {r['condition_key'] for r in restored}=={'H330938_1:c4','H322923_1:c2','H340899_1:c3','H340899_1:c4'}
assert all(c['strict_excerpt_state']==c['strict_full_source_state'] for c in cases)
assert bycase['H330938_1'][0]['strict_full_source_state']=='unknown'
out={'status':'PASS' if not unresolved else 'LOCATOR_REPAIR_REQUIRED','checks':dict(checks),
 'cases':73,'condition_units':208,'sources':67,'raw_sources_hash_match':True,
 'reference_tiers':summary['reference_tier_counts'],'direct_recovered_conditions':[r['condition_key'] for r in restored],
 'unresolved_source_locators':unresolved,
 'limit':'Exact span matches and recomputation establish provenance and internal consistency, not independent legal validity.',
 'input_hashes':{p.name:sha(p) for p in [A/'condition_audit_long.jsonl',A/'case_audit.jsonl',A/'source_audit_summary.json']}}
(ROOT/'verification/source_audit_independent_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
