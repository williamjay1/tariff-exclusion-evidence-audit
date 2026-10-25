"""Independent structural checks after source and semantic input review."""
from pathlib import Path
import json, hashlib, collections

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'experiments'
def read(name):
    return [json.loads(s) for s in (E/name).read_text(encoding='utf8').splitlines()]
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

rows=read('controlled_cases.jsonl')
pairs=read('constructed_pairs.jsonl')
sources=read('constructed_source_spans.jsonl')
by_id={r['case_id']:r for r in rows}
assert len(rows)==len(by_id)==108 and len(pairs)==96 and len(sources)==12
assert len({r['group'] for r in rows})==12
for r in rows:
    ids={f['id'] for f in r['facts']}
    expected=r['expected']; states=expected['states']
    assert set(states)=={'c1','c2'}
    out='refuted' if 'refuted' in states.values() else ('supported' if set(states.values())=={'supported'} else 'unknown')
    assert out==expected['decision']
    req=[c for c,s in states.items() if s=='unknown'] if out=='unknown' else []
    assert expected['requests']==req
    for cid,ev in expected['evidence'].items():
        assert set(ev)<=ids
        assert bool(ev)==(states[cid]!='unknown')
    if r['variant']=='deleted':
        base=by_id[r['case_id'].replace('_deleted','_base')]
        assert r['facts']==[f for f in base['facts'] if f['id']!='f1']
    assert r['constructed'] is True
    assert r['rule_text']=='Controlled two-condition clause: '+r['conditions'][0]['requirement']+' AND '+r['conditions'][1]['requirement']
for s in sources:
    for q in s['selected_rule_quotes']:
        a,b=q['span']; assert s['full_original_rule'][a:b]==q['quote']
for p in pairs:
    a,b=by_id[p['left']],by_id[p['right']]
    assert a['family']==b['family']==p['family']
    assert (a['expected']['decision']==b['expected']['decision'])==(p['expected_relation']=='same')

report={
 'status':'PASS', 'n_unique_constructed_inputs':108, 'n_linked_relations':96,
 'n_source_families':12, 'n_source_groups':12,
 'state_counts':dict(collections.Counter(r['expected']['decision'] for r in rows)),
 'review':'Root agent read all 12 full source rules and the common construction template before formal inference. This is AI input review, not expert legal validation.',
 'limits':[
  'Every-granule quantification and frame-specific teak scope are supplied controlled interpretations, not adjudicated legal readings.',
  'Two selected conditions do not represent the complete exclusion.',
  'Restoration reverses deletion with a reused base endpoint; linked relations are not independent observations.',
  'Both arms share the complete canonical clause and facts; the checklist adds a structured duplicate representation with condition IDs and requests richer output.',
  'No exhaustive boundary, prospective importer, or independent legal-validity claim.'
 ],
 'inputs':{name:digest(E/name) for name in ['controlled_cases.jsonl','constructed_pairs.jsonl','constructed_source_spans.jsonl']},
 'superseded_input_history':'The original short-quote draft was replaced before any predictions were examined; three unexamined pilot outputs are preserved in controlled_freeze.json. Qualification was unchanged.'
}
(ROOT/'verification/constructed_design_independent_audit.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
