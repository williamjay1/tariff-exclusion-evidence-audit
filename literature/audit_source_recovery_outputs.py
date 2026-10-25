"""Bounded raw-answer verification for four completed source-restoration pairs."""
from pathlib import Path
import json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
N=Path(r'D:\MLWork\tariff_scope_20261007\revision_20261023');E=N/'experiments'
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x]
inputs={x['case_id']:x for x in read(E/'source_recovery_cases.jsonl')}
expected_hash={'direct':'e38e1f755f89822c9b176f141611a6062eadd13ecea63214d395e0372c65714e','checklist':'09ad53d74b93e7d59bf1480bb43a415f2a3ac7f0b116fd102709f6f19cb945e5'}
outputs={};summary={}
for kind,digest in expected_hash.items():
    p=E/'outputs'/f'qwen14_source_recovery_cases_{kind}.jsonl'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
    raw=read(p);assert len(raw)==len({x['case_id'] for x in raw})==8
    assert {x['case_id'] for x in raw}==set(inputs)
    outputs[kind]={x['case_id']:x for x in raw}
    for x in raw:
        assert json.loads(x['raw_output'])==x['parsed']
        assert x['valid'] and not x['truncated'] and not x['stopped_limit']
    correct=sum(x['parsed']['decision']==inputs[x['case_id']]['expected']['decision'] for x in raw)
    wrongR=sum(x['parsed']['decision']=='refuted' and inputs[x['case_id']]['expected']['decision']!='refuted' for x in raw)
    wrongS=sum(x['parsed']['decision']=='supported' and inputs[x['case_id']]['expected']['decision']!='supported' for x in raw)
    summary[kind]={'n':8,'correct':correct,'unsupported_refutations':wrongR,'unsupported_affirmations':wrongS}
pairs=[]
for pair in read(E/'source_recovery_pairs.jsonl'):
    row={'pair':pair['pair_id'],'source_condition':inputs[pair['left']]['source_condition_key'],'rule':inputs[pair['left']]['rule_text'],'restored_assertion':inputs[pair['right']]['source_recovered_span']['quote'],'reference':['unknown','supported']}
    for kind in outputs:
        v=[outputs[kind][pair[k]]['parsed'] for k in ['left','right']]
        row[kind]=v
        row[kind+'_success']=[z['decision'] for z in v]==['unknown','supported']
    pairs.append(row)
for kind in outputs:summary[kind]['pair_success']=sum(x[kind+'_success'] for x in pairs)
assert summary['direct']=={'n':8,'correct':7,'unsupported_refutations':0,'unsupported_affirmations':0,'pair_success':3}
assert summary['checklist']=={'n':8,'correct':6,'unsupported_refutations':2,'unsupported_affirmations':0,'pair_success':3}
motor=inputs['REC_H340899_1_c3_before']
report={'scope':'Completed source recovery only; hashes and raw JSON independently verified; no inference rerun.','summary':summary,'pairs':pairs,'verified_output_sha256':expected_hash,'motor_before_facts':motor['facts'],'interpretation_limit':'Responses contain labels and fact IDs but no explanation. The cause of unchanged motor outputs is not identifiable from these records. The model receives only one isolated supplied condition; no whole-exclusion or legal disposition is evaluated.'}
(N/'literature/source_recovery_output_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
