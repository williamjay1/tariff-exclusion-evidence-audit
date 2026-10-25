"""Recompute the prior guard's refutation losses without changing old outputs."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent;PROJ=ROOT.parents[1]
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf8').splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    files={'reference':PROJ/'revision_20261009/evidence_numeric/evidence_operational_reference.jsonl',
           'qwen4':PROJ/'results/benchmark_qwen4.jsonl','numeric':PROJ/'results/numeric_traces.jsonl',
           'benchmark':PROJ/'datasets/benchmark.jsonl'}
    inp={k:{r['case_id']:r for r in read(p)} for k,p in files.items()};records=[]
    for cid,r in inp['reference'].items():
        if r['operational_evidence_state']!='refute':continue
        pred=inp['qwen4'][cid];numeric=inp['numeric'][cid];raw=pred['selective_prediction']
        old=0 if numeric['state']=='fail' else (-1 if numeric['state']=='unknown' else raw)
        records.append({'case_id':cid,'old_reference':'refute','raw_native':raw,'old_guard_native':old,
                        'numeric_state':numeric['state'],'raw_refutation_lost':raw==0 and old==-1,
                        'refuted_conditions':[c for c in r['conditions'] if c['evidence_state']=='refute'],
                        'numeric_trace':numeric,'facts':inp['benchmark'][cid]['facts'],'rule_text':inp['benchmark'][cid]['rule_text'],
                        'policy_diagnosis':'The old implementation maps every numeric unknown to referral regardless of the model sign. This is a trust policy, not conjunctive three-valued aggregation.'})
    result={'reference':'Prior AI-assisted diagnostic evidence states; pending new source re-audit. No expert gold assumed.',
            'input_hashes':{k:sha(p) for k,p in files.items()},'n_refuted':len(records),
            'raw_correct':sum(r['raw_native']==0 for r in records),'old_guard_correct':sum(r['old_guard_native']==0 for r in records),
            'lost_raw_refutations':[r['case_id'] for r in records if r['raw_refutation_lost']],
            'records':records,'logic_rule':'A verified refutation of any mandatory conjunct dominates unrelated missing conditions. An unsupported model-negative may instead be referred under an explicit trust policy.',
            'proposed_diagnostic':'Measure whether independent condition evidence verifies each old lost negative; do not preserve arbitrary model negatives by definition.'}
    (ROOT/'old_guard_diagnostic.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    summary={k:v for k,v in result.items() if k!='records'}
    text=['# Old numeric guard: refutation-loss reconstruction','',json.dumps(summary,indent=2,ensure_ascii=False),'']
    for r in records:
        text+=['## '+r['case_id'],f"Raw {r['raw_native']} -> guard {r['old_guard_native']}; numerical state {r['numeric_state']}."]
        for c in r['refuted_conditions']:
            text+=['Rule: '+c['rule_quote'],'Evidence: '+json.dumps(c['fact_evidence'],ensure_ascii=False),'Prior rationale: '+c['rationale']]
        text+=['']
    (ROOT/'old_guard_diagnostic.md').write_text('\n'.join(text),encoding='utf8')
    print(json.dumps({k:v for k,v in summary.items() if k!='input_hashes'},indent=2))
if __name__=='__main__':main()
