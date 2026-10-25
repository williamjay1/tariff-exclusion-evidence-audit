"""Actual four-layer execution with the frozen numerical comparator.
Reference input fields were frozen separately, without importing this engine.
"""
from pathlib import Path
from decimal import Decimal
from collections import Counter,defaultdict
import json,hashlib,importlib.util
R=Path(__file__).resolve().parent
OLD=R.parents[1]
spec=importlib.util.spec_from_file_location('frozen_numeric_engine',OLD/'scripts/constraint_engine.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
def read(p):return [json.loads(x) for x in p.read_text('utf8').splitlines()]
def save(name,x):
    (R/name).write_text(json.dumps(x,indent=2,ensure_ascii=False,default=str),encoding='utf8')
def jsonify(x):return json.loads(json.dumps(x,default=str))
refs=read(R/'numeric_reference_fields.jsonl')
inputs={r['case_id']:r for r in read(R/'evidence_visible_inputs.jsonl')}
refby=defaultdict(list)
for r in refs:refby[r['case_id']].append(r)
def converted(d):
    d=d.copy()
    for k in ['lower','upper']:
        if d.get(k) is not None:d[k]=Decimal(d[k])
    if 'interpretations' in d:d['interpretations']=[converted(x) for x in d['interpretations']]
    return d
def agg(states):
    return 'fail' if 'fail' in states else 'unknown' if 'unknown' in states or not states else 'pass'
def execute(cs,fs,unparsed=None,unsupported_disjunction=False):
    # Same attribute/dimension matching and unique-interval policy as frozen engine.
    trace=[]
    for c in cs:
        matches=[f for f in fs if f['attribute']==c['attribute'] and f['dimension']==c['dimension']]
        if matches and all('interpretations' in f for f in matches):
            subject_states=[]
            for field in matches:
                alternatives=[engine.interval_state(c,v) for v in field['interpretations']]
                subject_states.append({'subject':field['subject'],'alternative_states':alternatives,
                    'state':alternatives[0] if len(set(alternatives))==1 else 'unknown'})
            state=agg([t['state'] for t in subject_states])
            trace.append({'constraint':c,'state':state,'candidates':matches,'subject_states':subject_states,
              'reference_only_binding_adapter':True,'unknown_reason':'discrete_rating_interpretation' if state=='unknown' else None})
            continue
        distinct={(f['lower'],f['upper']) for f in matches}
        state=engine.interval_state(c,matches[0]) if len(distinct)==1 else 'unknown'
        trace.append({'constraint':c,'state':state,'candidates':matches,
          'unknown_reason':('missing_or_binding_mismatch' if not matches else 'multiple_distinct_fields' if len(distinct)!=1 else 'straddling_interval') if state=='unknown' else None})
    states=[t['state'] for t in trace]
    st='unknown' if unsupported_disjunction else 'fail' if 'fail' in states else 'unknown' if 'unknown' in states or unparsed else 'pass' if states else 'not_parsed'
    return {'state':st,'trace':trace,'unparsed_quantities':unparsed or [],'unsupported_disjunction':unsupported_disjunction}
def norm(state):return 'unknown' if state=='not_parsed' else state
out=[]
for cid,rr in refby.items():
    x=inputs[cid];rc=[converted(r['constraint']) for r in rr];rf=[converted(f) for r in rr for f in r['reference_fields']]
    fullauto=engine.verify_numeric(x['facts'],x['rule_text'])
    ac=[t['constraint'] for t in fullauto['trace']];af=engine.extract_facts(x['facts'])
    layers={'reference_rule_reference_fields':execute(rc,rf),
            'auto_rule_reference_fields':execute(ac,rf,fullauto['unparsed_quantities'],fullauto['unsupported_disjunction']),
            'reference_rule_auto_fields':execute(rc,af),
            'auto_rule_auto_fields':fullauto}
    expected=agg([r['expected_numeric_state'] for r in rr])
    out.append({'case_id':cid,'numeric_reference_state':expected,'n_numeric_conditions':len(rr),'layers':layers,
       'numeric_violation_sufficient_to_refute':expected=='fail',
       'reference_fields_support_all_numeric_conditions':expected=='pass',
       'numeric_reference_does_not_resolve_nonnumeric_conditions':True})
    # Scope of claim: engine cannot silently be replaced by a mathematically different oracle.
    assert norm(layers['reference_rule_reference_fields']['state'])==expected,(cid,expected,layers['reference_rule_reference_fields'])
(R/'numeric_layer_predictions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,default=str)+'\n' for r in out),encoding='utf8')
summary={'n_cases':len(out),'n_conditions':len(refs),'reference_states':dict(Counter(r['numeric_reference_state'] for r in out)),
 'engine_sha256':hashlib.sha256((OLD/'scripts/constraint_engine.py').read_bytes()).hexdigest(),
 'reference_fields_sha256':hashlib.sha256((R/'numeric_reference_fields.jsonl').read_bytes()).hexdigest(),
 'layer_results':{},'unknown_reasons':{},
 'design':'Actual frozen Decimal interval_state execution. Ordinary fields use frozen matching policy. For source-coded relay fields only, an explicit test-only binding adapter evaluates each product and its discrete rating alternatives, then aggregates all listed products; this is not functionality of the frozen extractor. Interventions never use administrative outcomes.',
 'limitation':'Reference fields encode reviewed subject bindings and conservative hulls. This is a test-only diagnostic intervention, not a deployable extractor or evidence of full legal correctness.'}
for layer in out[0]['layers']:
    summary['layer_results'][layer]={'states':dict(Counter(norm(r['layers'][layer]['state']) for r in out)),
       'three_state_correct':sum(norm(r['layers'][layer]['state'])==r['numeric_reference_state'] for r in out),
       'n':len(out),'confusion':dict(Counter(r['numeric_reference_state']+'->'+norm(r['layers'][layer]['state']) for r in out))}
    cc=Counter()
    for r in out:
        z=r['layers'][layer]
        if norm(z['state'])!='unknown':continue
        if z.get('unsupported_disjunction'):cc['unsupported_disjunction']+=1
        if z.get('unparsed_quantities'):cc['unparsed_rule_quantity']+=1
        if not z['trace']:cc['no_parsed_constraint']+=1
        for t in z['trace']:
            if t['state']=='unknown':
                ms=t['candidates'];cc['discrete_rating_interpretation' if t.get('reference_only_binding_adapter') else 'missing_or_binding_mismatch' if not ms else 'multiple_distinct_fields' if len({(f['lower'],f['upper']) for f in ms})!=1 else 'straddling_interval']+=1
    summary['unknown_reasons'][layer]=dict(cc)
summary['unknown_reason_count_unit']='Constraint occurrences except unparsed rule/disjunction/no constraints, which count cases; categories can overlap.'
save('numeric_layer_analysis.json',summary)
# Evaluate independently authored, explicitly constructed stress cases only after
# the reference and design manifest have been saved.
constructed=read(R/'constructed_diagnostics.jsonl');cp=[]
for r in constructed:
    pred=engine.verify_numeric(r['facts'],r['rule_text'])
    cp.append({'case_id':r['case_id'],'group':r['group'],'mechanism':r['mechanism'],'pair_id':r['pair_id'],'pair_type':r['pair_type'],
               'gold':r['gold'],'prediction':norm(pred['state']),'raw_state':pred['state'],'correct':norm(pred['state'])==r['gold'],'trace':pred})
(R/'constructed_frozen_engine_predictions.jsonl').write_text(''.join(json.dumps(r,default=str)+'\n' for r in cp),encoding='utf8')
pairgroups=defaultdict(list)
for r in cp:pairgroups[r['pair_id']].append(r)
cs={'n':len(cp),'correct':sum(r['correct'] for r in cp),'by_mechanism':{},'pair_results':{},
    'reference_sha256':hashlib.sha256((R/'constructed_diagnostics.jsonl').read_bytes()).hexdigest(),
    'status':'constructed diagnostic only; results are not real-ruling performance'}
for m in sorted({r['mechanism'] for r in cp}):
    s=[r for r in cp if r['mechanism']==m]
    cs['by_mechanism'][m]={'n':len(s),'correct':sum(r['correct'] for r in s),'confusion':dict(Counter(r['gold']+'->'+r['prediction'] for r in s))}
for kind in sorted({r['pair_type'] for r in cp}):
    ps=[v for v in pairgroups.values() if v[0]['pair_type']==kind]
    cs['pair_results'][kind]={'pairs':len(ps),'both_correct':sum(all(r['correct'] for r in v) for v in ps),
        'predictions_same':sum(v[0]['prediction']==v[1]['prediction'] for v in ps),
        'interpretation':'For equivalence, same predictions is invariance but can be consistently wrong; both_correct is stronger.' if kind=='equivalence' else 'For decisive changes both_correct is required, not mere output change.'}
save('constructed_frozen_engine_analysis.json',cs)
print(json.dumps(summary,indent=2));print(json.dumps(cs,indent=2))
