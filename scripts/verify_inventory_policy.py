from pathlib import Path
from collections import Counter
from itertools import product
import hashlib,json
R=Path(__file__).resolve().parents[1]
def lines(p):return [json.loads(s) for s in p.read_text(encoding='utf8').splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inventory=lines(R/'inventory_audit/inventory_structural_audit.jsonl')
readings=lines(R/'inventory_audit/reviewed_condition_groups.jsonl')
assert len(inventory)==len(readings)==397
assert {r['index'] for r in readings}==set(range(397))
span_n=0
for row,reading in zip(inventory,readings):
    assert row['rule_id']==reading['rule_id'] and row['scope']==reading['scope']
    assert hashlib.sha256(row['scope'].encode()).hexdigest()==reading['scope_sha256']
    assert reading['coarse_required_group_count']==len(reading['groups'])==row['coarse_required_group_count']
    assert row['actual_reviewed'] and reading['complete_coarse_reading_silver']
    for g in reading['groups']:
        assert row['scope'][g['start']:g['end']]==g['quote'];span_n+=1
    if row['scope_format'].startswith('code_only'):assert len(reading['groups'])==0
assert sum(x['coarse_required_group_count'] for x in readings)==1096
assert Counter(x['scope_format'] for x in inventory)=={'code_only_single':41,'code_only_dated_transition':2,'product_description':354}
conditions=lines(R/'source_audit/condition_audit_long.jsonl')
cases=lines(R/'source_audit/case_audit.jsonl')
sensitivity=json.loads((R/'source_audit/policy_sensitivity.json').read_text(encoding='utf8'))
cond={x['condition_key']:x for x in conditions}
safe={x['case_id']:x for x in cases if x['safe_flat_conjunction']}
assert len(safe)==58
def agg(states):
    scored=[s for s in states if s!='not_applicable']
    return 'refute' if 'refute' in scored else 'support' if scored and all(s=='support' for s in scored) else 'unknown'
possible={}
for key,case in safe.items():
    opts=[]
    for ck in case['condition_keys']:
        c=cond[ck];base=c['strict_full_source_state']
        states={base}
        if c['reference_tier'] in ('interpretive','disputed'):
            states|={o['state'] for o in c['interpretation_options']}
        opts.append(states)
    possible[key]={agg(s) for s in product(*opts)}
for row in sensitivity['cases']:
    assert set(row['possible_states'])==possible[row['case_id']]
envelopes={s:{'necessarily_this_state':sum(v=={s} for v in possible.values()),'possibly_this_state':sum(s in v for v in possible.values())} for s in ['support','refute','unknown']}
assert envelopes==sensitivity['marginal_count_envelopes']
packages=[]
for package in sensitivity['explicit_policy_packages']:
    overrides=package['overrides'];counts=Counter();states={}
    for key,case in safe.items():
        vals=[]
        for ck in case['condition_keys']:
            c=cond[ck];state=c['strict_full_source_state']
            if ck in overrides:
                selected=overrides[ck]
                option=next(x for x in c['interpretation_options'] if x['policy']==selected)
                assert c['reference_tier'] in ('interpretive','disputed');state=option['state']
            vals.append(state)
        states[key]=agg(vals);counts[states[key]]+=1
    assert dict(counts)==package['counts']
    assert states=={x['case_id']:x['state'] for x in package['cases']}
    packages.append({'name':package['name'],'counts':dict(counts)})
report={'status':'PASS','inventory':397,'product_descriptions':354,'coarse_product_groups':1096,'coarse_group_spans_checked':span_n,'code_only_zero_additional_product_groups':43,'safe_conjunction_cases':58,'marginal_envelopes':envelopes,'joint_packages':packages,'boundary':'Mechanical source spans and declared-policy recomputation; not expert semantic validation.','hashes':{str(p.relative_to(R)):sha(p) for p in [R/'inventory_audit/inventory_structural_audit.jsonl',R/'inventory_audit/reviewed_condition_groups.jsonl',R/'source_audit/policy_sensitivity.json']}}
(R/'verification/inventory_policy_independent_audit.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
