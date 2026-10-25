"""Reconcile frozen AI passes conservatively; then join outcomes/predictions.
This script never changes either initial coding pass or administrative outcomes.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,random,copy
R=Path(__file__).resolve().parent;OLD=R.parents[1]
def read(p):return [json.loads(x) for x in p.read_text('utf8').splitlines()]
def write(n,x): (R/n).write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf8')
def jsonl(n,rs):(R/n).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs),encoding='utf8')
first=read(R/'evidence_condition_codes.jsonl');f={r['case_id']:r for r in first}
second=json.loads((R/'root_visible_evidence_review.json').read_text('utf8'))['records']
stateconvert={'supported':'support','refuted':'refute','unknown':'unknown'}
s={r['case_id']:{**r,'state':stateconvert[r['state']]} for r in second}
assert set(f)==set(s) and len(f)==73
disagreements=[{'case_id':cid,'first_state':f[cid]['aggregate_evidence_state'],'second_state':s[cid]['state'],
  'second_rationale':s[cid]['reason'],'resolution':'unknown','resolution_basis':'Unresolved category/use/incorporated-heading/multiple-product reading; no administrative disposition used to adjudicate.'}
  for cid in f if f[cid]['aggregate_evidence_state']!=s[cid]['state']]
disputed={r['case_id'] for r in disagreements};final=[]
for r in first:
    z=copy.deepcopy(r);cid=z['case_id'];z['first_pass_state']=z['aggregate_evidence_state'];z['second_pass_state']=s[cid]['state']
    z['operational_evidence_state']='unknown' if cid in disputed else z['aggregate_evidence_state']
    if cid=='N311039_33':z['operational_evidence_state']='refute';z['third_pass_source_correction']='Discrete coil/contact alternatives for products 1, 3 and 4 each violate (60,250] V. The all-products claim is refuted regardless of the unresolved rating interpretation for product 2.'
    z['second_pass_rationale']=s[cid]['reason'];z['coding_disagreement']=cid in disputed
    z['operational_policy']='Conservative AI evidence policy: unresolved inter-pass semantic disagreements remain unknown. Not validated legal gold.'
    for c in z['conditions']:
        if cid=='N311039_33' and c['rule_quote']=='for a voltage exceeding 60 V but not over 250 V':
            c['evidence_state']='refute';c['rationale']='For the first relay, both 12 V coil and 277 V contact ratings violate (60,250] V; further listed relays likewise violate both alternatives. Do not replace these discrete, per-product alternatives by a continuous hull.'
        if cid=='H318593_1' and c['rule_quote']=='of steel':
            c['evidence_state']='unknown';c['rationale']='Mixed steel/aluminum composition requires a legal material-category interpretation; second AI pass did not regard majority steel as sufficient.'
        if cid=='H318593_1' and '81 cm by 41 cm' in c['rule_quote']:
            c['evidence_state']='unknown';c['rationale']='Independent numeric audit found that visible dimensions explicitly exclude the handle; the rule does not specify the same measurement scope.'
        if cid=='N312588' and '8541' in c['rule_quote']:
            c['evidence_state']='unknown';c['rationale']='Source facts name semiconductors/integrated circuits, but incorporation of the specific tariff-heading definitions is not supplied in the visible input.'
        if cid=='N309775_buttons':
            c['evidence_state']='unknown';c['rationale']='The button pack fits the literal category; the separately described silicone switch pad is not unambiguously a molded button under the supplied text.'
    final.append(z)
assert Counter(r['operational_evidence_state'] for r in final)=={'support':21,'refute':5,'unknown':47}
jsonl('evidence_operational_reference.jsonl',final)
# Initial agreement is calculated before any reconciliation and remains immutable
# with respect to later operational labels.
a=[f[c]['aggregate_evidence_state'] for c in f];b=[s[c]['state'] for c in f];n=len(a)
ca,cb=Counter(a),Counter(b);agreement=sum(x==y for x,y in zip(a,b))/n
chance=sum(ca[k]*cb[k] for k in ['support','refute','unknown'])/n**2
agreement_report={'n':n,'matching':sum(x==y for x,y in zip(a,b)),'agreement':agreement,'cohen_kappa':(agreement-chance)/(1-chance),
 'first_counts':dict(ca),'second_counts':dict(cb),'initial_confusion':dict(Counter(x+'->'+y for x,y in zip(a,b))),
 'disagreements':disagreements,'final_counts':dict(Counter(r['operational_evidence_state'] for r in final)),
 'interpretation':'Reproducibility of two same-lineage AI readings of outcome-masked inputs, not independence from prior project knowledge or proof of legal validity.',
 'human_expert_review':False,'post_reconciliation_agreement_not_reported':True,
 'third_pass_source_corrections':['H318593_1 handle-excluded dimensions remain unknown','N311039_33 discrete per-product coil/contact alternatives establish a numerical counterexample and change operational unknown to refute'],
 'first_pass_sha256':hashlib.sha256((R/'evidence_condition_codes.jsonl').read_bytes()).hexdigest(),
 'second_pass_sha256':hashlib.sha256((R/'root_visible_evidence_review.json').read_bytes()).hexdigest()}
write('evidence_agreement.json',agreement_report)
# Outcome and model joins occur only here, after the first and second references.
bench={r['case_id']:r for r in read(OLD/'datasets/benchmark.jsonl')}
targets={'first_AI_pass':{c:f[c]['aggregate_evidence_state'] for c in f},
 'second_AI_pass':{c:s[c]['state'] for c in f},'conservative_operational':{r['case_id']:r['operational_evidence_state'] for r in final}}
def metrics(g,p):
    labels=['support','refute','unknown'];conf=Counter(x+'->'+y for x,y in zip(g,p));pc=Counter(p);gc=Counter(g)
    recall={};f1={}
    for k in labels:
        tp=sum(x==k and y==k for x,y in zip(g,p));recall[k]=tp/gc[k] if gc[k] else None
        den=gc[k]+pc[k];f1[k]=2*tp/den if den else None
    return {'n':len(g),'correct':sum(x==y for x,y in zip(g,p)),'accuracy':sum(x==y for x,y in zip(g,p))/len(g),
       'macro_recall':sum(recall.values())/3,'macro_f1':sum(f1.values())/3,'class_recall':recall,'class_f1':f1,
       'prediction_counts':dict(pc),'confusion':dict(conf)}
preds={}
for model in ['nli','qwen','qwen4']:
    ps={r['case_id']:r for r in read(OLD/f'results/benchmark_{model}.jsonl')}
    preds[model]={c:{1:'support',0:'refute',-1:'unknown'}[ps[c]['selective_prediction']] for c in f}
preds['always_unknown_diagnostic']={c:'unknown' for c in f}
scores={target:{model:metrics([g[c] for c in f],[p[c] for c in f]) for model,p in preds.items()} for target,g in targets.items()}
joined=[]
for cid in f:
    joined.append({'case_id':cid,'administrative_y':bench[cid]['y'],'source':bench[cid]['source'],
       'group':bench[cid]['group'],'evidence_states':{k:v[cid] for k,v in targets.items()},'native_ternary_predictions':{k:v[cid] for k,v in preds.items()}})
jsonl('evidence_outcome_prediction_join.jsonl',joined)
result={'n':73,'target_definition':'Frozen facts/literal-rule evidence support, not administrative eligibility',
 'disposition_by_operational_evidence':dict(Counter(('eligible' if r['administrative_y'] else 'ineligible')+'->'+r['evidence_states']['conservative_operational'] for r in joined)),
 'source_by_operational_evidence':dict(Counter(r['source']+'->'+r['evidence_states']['conservative_operational'] for r in joined)),
 'metrics_by_reference_policy':scores,'uncertainty':'Small purposive corpus; report counts and coding-policy sensitivity. Agreement is not expert validity.',
 'native_prediction_definition':'Argmax of the original three class probabilities (selective_prediction), mapped 1/support, 0/refute, -1/unknown. No binary collapse or numeric guard is used here.'}
write('evidence_target_analysis.json',result)
# Join the independently source-coded numeric opportunities, distinguishing a
# numeric certificate from an entire product-scope evidence certificate.
layers=read(R/'numeric_layer_predictions.jsonl');op=[]
for r in layers:
    cid=r['case_id'];z=targets['conservative_operational'][cid];state=r['numeric_reference_state']
    op.append({'case_id':cid,'numeric_reference_state':state,'whole_scope_evidence_state':z,'administrative_y':bench[cid]['y'],
       'all_qualitative_conditions_supported':z=='support' if state=='pass' else None,
       'numeric_violation_certificate':state=='fail','reference_numeric_only_can_resolve_whole_scope':state=='fail',
       'native_predictions':{m:preds[m][cid] for m in ['nli','qwen','qwen4']},
       'incorrect_native_affirmations_correctable_by_numeric_violation':[m for m in ['nli','qwen','qwen4'] if state=='fail' and preds[m][cid]=='support'],
       'frozen_auto_state':r['layers']['auto_rule_auto_fields']['state'],
       'reference_numeric_fields_are_test_only':True})
jsonl('real_numeric_opportunity_table.jsonl',op)
opsummary={'n_numeric_cases':len(op),'numeric_by_whole_scope_evidence':dict(Counter(r['numeric_reference_state']+'->'+r['whole_scope_evidence_state'] for r in op)),
  'definite_numeric_violations':[r['case_id'] for r in op if r['numeric_violation_certificate']],
  'whole_scope_supported_with_numeric_conditions':[r['case_id'] for r in op if r['whole_scope_evidence_state']=='support'],
  'correctable_native_affirmation_counts':{m:sum(m in r['incorrect_native_affirmations_correctable_by_numeric_violation'] for r in op) for m in ['nli','qwen','qwen4']},
  'interpretation':'Only definite numeric violations justify a negative override on numeric evidence alone. Numeric passes do not establish absent nonnumeric criteria; this is an oracle-field opportunity diagnosis, not achieved auto-extraction performance.'}
write('real_numeric_opportunity_summary.json',opsummary)
# An unlabelled shuffled packet is available for future human or additional AI
# checks. It is an available instrument, not a study claimed to have happened.
visible=read(R/'evidence_visible_inputs.jsonl');random.Random(20261009).shuffle(visible)
packet=[];key=[]
for i,r in enumerate(visible,1):
    pid=f'V{i:03d}';packet.append({'item_id':pid,'facts':r['facts'],'rule_text':r['rule_text'],
      'response':{'evidence_state':None,'conditions':[],'rationale':None,'coder':None,'model_or_expertise':None}})
    key.append({'item_id':pid,'case_id':r['case_id']})
jsonl('unlabelled_review_packet.jsonl',packet);jsonl('review_packet_private_key.jsonl',key)
print(json.dumps(agreement_report,indent=2));print(json.dumps(result,indent=2));print(json.dumps(opsummary,indent=2))
