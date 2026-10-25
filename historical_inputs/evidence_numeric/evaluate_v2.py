"""Evaluate post hoc v2 on the same disclosed development diagnostics.
No result here is claimed to be an independent held-out estimate.
"""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,importlib.util
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('numeric_repair_v2',R/'constraint_engine_v2.py');v2=importlib.util.module_from_spec(spec);spec.loader.exec_module(v2)
def read(n):return [json.loads(x) for x in (R/n).read_text('utf8').splitlines()]
def norm(x):return 'unknown' if x=='not_parsed' else x
def metrics(rs):return {'n':len(rs),'correct':sum(r['correct'] for r in rs),'confusion':dict(Counter(r['gold']+'->'+r['prediction'] for r in rs))}
inp={r['case_id']:r for r in read('evidence_visible_inputs.jsonl')};real=[]
for r in read('numeric_layer_predictions.jsonl'):
    x=inp[r['case_id']];p=v2.verify_numeric(x['facts'],x['rule_text']);st=norm(p['state'])
    real.append({'case_id':r['case_id'],'gold':r['numeric_reference_state'],'prediction':st,'correct':st==r['numeric_reference_state'],
      'frozen_prediction':norm(r['layers']['auto_rule_auto_fields']['state']),'trace':p})
constructed=[];constructed_inputs=read('constructed_diagnostics.jsonl')
for r in constructed_inputs:
    p=v2.verify_numeric(r['facts'],r['rule_text']);st=norm(p['state'])
    constructed.append({k:r[k] for k in ['case_id','mechanism','pair_id','pair_type','gold']}|{'prediction':st,'correct':st==r['gold'],'trace':p})
for name,rows in [('real_numeric_v2_predictions.jsonl',real),('constructed_v2_predictions.jsonl',constructed)]:
    (R/name).write_text(''.join(json.dumps(r,default=str)+'\n' for r in rows),encoding='utf8')
summary={'version':'posthoc_v2_general_parser_repairs','frozen_engine_unchanged':True,
 'v2_sha256':hashlib.sha256((R/'constraint_engine_v2.py').read_bytes()).hexdigest(),
 'numeric_reference_sha256':hashlib.sha256((R/'numeric_reference_fields.jsonl').read_bytes()).hexdigest(),
 'constructed_input_sha256':hashlib.sha256((R/'constructed_diagnostics.jsonl').read_bytes()).hexdigest(),
 'real33':metrics(real),'constructed96':metrics(constructed),
 'constructed_by_mechanism':{m:metrics([r for r in constructed if r['mechanism']==m]) for m in sorted({r['mechanism'] for r in constructed})},
 'real_changes':[{'case_id':r['case_id'],'gold':r['gold'],'frozen':r['frozen_prediction'],'v2':r['prediction']} for r in real if r['frozen_prediction']!=r['prediction']],
 'claim_boundary':'A post hoc repair evaluated on the same already inspected diagnostic suite and restricted-text cases. No new held-out generalization, deployability or expert validity is inferred; unsupported compound units and logic remain limitations.'}
unique={}
for r,p in zip(constructed_inputs,constructed):unique[(r['facts'],r['rule_text'])]=p
summary['constructed_unique_inputs']=metrics(list(unique.values()))
pairgroups=defaultdict(list)
for r in constructed:pairgroups[r['pair_id']].append(r)
summary['pair_results']={}
for kind in sorted({r['pair_type'] for r in constructed}):
    ps=[v for v in pairgroups.values() if v[0]['pair_type']==kind]
    summary['pair_results'][kind]={'pairs':len(ps),'both_correct':sum(all(r['correct'] for r in v) for v in ps),
       'same_prediction':sum(v[0]['prediction']==v[1]['prediction'] for v in ps)}
summary['development_history']={'first_v2_real_correct':23,'first_v2_constructed_correct':70,
 'subsequent_general_bugfix':'The first post hoc run revealed that dropped approximate reports could falsely certify an exact competing reading. Unspecified approximations now remain unbounded unknown fields; explicitly stated plus/minus tolerances are represented as intervals. Initial summary retained. This additional repair was developed after inspecting these diagnostics, not independently validated.'}
(R/'numeric_v2_analysis.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
