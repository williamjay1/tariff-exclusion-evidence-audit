"""Unit fixtures for metric bookkeeping; these are not model observations."""
import copy,datetime,json
from pathlib import Path
import analyze_evidence_audit as a
from protocol import aggregate,prompt
ROOT=Path(__file__).resolve().parent
rows=a.read(ROOT/'controlled_cases.jsonl');checks=[]
def prediction(r,state=None):
    g=r['expected'];states=g['states'] if state is None else {k:state for k in g['states']}
    return {'kind':'checklist','case_id':r['case_id'],'valid':True,'parsed':{
       'conditions':[{'id':k,'state':v,'evidence':g['evidence'][k] if state is None else []} for k,v in states.items()],
       'decision':g['decision'] if state is None else aggregate(list(states.values())),
       'requests':g['requests'] if state is None else []}}
s=a.summarise([a.case_record(r,prediction(r)) for r in rows],'checklist')
assert s['decision_correct']==108 and s['condition_correct']==216
assert s['gap_localization']=={'tp':36,'fp':0,'fn':0,'precision':1.0,'recall':1.0}
assert s['requests']['tp']==24 and s['evidence_id_acceptable']['correct']==216
checks.append('Perfect synthetic fixture gives 108/108 case,216/216 condition,36 gaps,24 required requests.')
u=a.summarise([a.case_record(r,prediction(r,'unknown')) for r in rows],'checklist')
assert u['decision_correct']==24 and u['gap_localization']['fp']==180 and u['requests']['missing_necessary']==24
lookup={r['case_id']:a.case_record(r,prediction(r,'unknown')) for r in rows}
assert sum(lookup[p['left']]['decision_correct'] and lookup[p['right']]['decision_correct'] for p in a.read(ROOT/'constructed_pairs.jsonl'))==0
checks.append('Always-unknown fixture earns zero successful linked relationships; stability alone cannot pass.')
s=a.summarise([a.case_record(r,prediction(r,'supported')) for r in rows],'checklist')
assert s['decision_correct']==48 and s['unsupported_case_affirmations']==60
checks.append('Always-supported fixture yields 60 unsupported whole-input affirmations.')
r=rows[0];bad={'case_id':r['case_id'],'kind':'direct','valid':False}
assert a.case_record(r,bad)['request_tp'] is None and a.case_record(r,bad)['condition_n'] is None
checks.append('Direct condition and request endpoints remain NA even for invalid output.')
incomplete=prediction(r);incomplete['parsed']['conditions']=incomplete['parsed']['conditions'][:1]
z=a.case_record(r,incomplete)
assert z['evidence_scored_n']==2 and z['evidence_exact_n']==1 and not z['complete_condition_ids']
checks.append('Missing condition/citation remains in the reference denominator instead of disappearing.')
err=json.loads((ROOT/'annotation_erratum.json').read_text());corrected=copy.deepcopy(rows);byid={r['case_id']:r for r in corrected}
for e in err['edits']:
    g=byid[e['case_id']]['expected'];g['states'][e['condition_id']]=e['state'];g.setdefault('evidence_allowed_sets',{})[e['condition_id']]=e['acceptable_evidence_sets']
assert sum('unknown' in r['expected']['states'].values() and r['expected']['decision']=='refuted' for r in corrected)==11
for r in corrected:assert aggregate(list(r['expected']['states'].values()))==r['expected']['decision']
assert all(r['expected']['decision']==o['expected']['decision'] for r,o in zip(corrected,rows))
frame=byid['CF10_binding_original'];p=prediction(frame);p['parsed']['conditions'][1]['evidence']=['f1'];assert a.case_record(frame,p)['evidence_exact_n']==2
p['parsed']['conditions'][1]['evidence']=['f2'];assert a.case_record(frame,p)['evidence_exact_n']==1
checks.append('Erratum retains all whole-input states and admits only target-frame alternatives, never Product B evidence.')
for r in rows:
    changed=copy.deepcopy(r);changed['expected']={'hidden':'arbitrary'};changed['source_case_id']='hidden';assert prompt(r)==prompt(changed)
    assert all(c['requirement'] in r['rule_text'] for c in r['conditions'])
checks.append('All formal prompts omit outcome/provenance metadata; clause semantics contain every supplied condition in both interfaces.')
records=[{'case_id':str(i),'group':g,'decision_correct':v} for i,(g,v) in enumerate([('a',1),('a',1),('a',0),('b',0)])]
base=[{**r,'decision_correct':0} for r in records]
diff=a.cluster_difference(records,base);assert diff['n']==4 and diff['difference']==.5
checks.append('Bootstrap uses observed n and difference, not the last resampled group collection.')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','fixture_only':True,'not_model_results':True,'checks':checks}
(ROOT/'analysis_logic_audit.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
