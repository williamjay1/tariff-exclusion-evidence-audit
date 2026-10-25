"""Read only frozen controlled outputs; never opens source-recovery outputs."""
from pathlib import Path
import json
N=Path(r'D:\MLWork\tariff_scope_20261007\revision_20261023')
E=N/'experiments'
def rows(p):return [json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s]
data={r['case_id']:r for r in rows(E/'controlled_cases.jsonl')}
raw=rows(E/'outputs/qwen14_controlled_cases_checklist.jsonl')
direct={r['case_id']:r for r in rows(E/'outputs/qwen14_controlled_cases_direct.jsonl')}
assert len(raw)==len({r['case_id'] for r in raw})==108
err=json.loads((E/'annotation_erratum.json').read_text(encoding='utf-8'))
for x in err['edits']:
    g=data[x['case_id']]['expected'];g['states'][x['condition_id']]=x['state']
    g.setdefault('evidence_allowed_sets',{})[x['condition_id']]=x['acceptable_evidence_sets']
errors=[];counts={'conditions':0,'condition_errors':0,'evidence_errors':0,'missing_requests':0,'unnecessary_requests':0}
for out in raw:
    r=data[out['case_id']];g=r['expected'];p=json.loads(out['raw_output'])
    assert p==out['parsed'] and out['valid'] and not out['truncated'] and not out['stopped_limit']
    cs={x['id']:x for x in p['conditions']}
    ce=[];ee=[]
    for k,v in g['states'].items():
        counts['conditions']+=1
        if cs[k]['state']!=v:ce.append({'condition':k,'expected':v,'predicted':cs[k]['state']})
        sets=g.get('evidence_allowed_sets',{}).get(k,[g['evidence'][k]])
        if not any(set(cs[k]['evidence'])==set(z) for z in sets):ee.append({'condition':k,'allowed':sets,'predicted':cs[k]['evidence']})
    missing=sorted(set(g['requests'])-set(p['requests']));extra=sorted(set(p['requests'])-set(g['requests']))
    counts['condition_errors']+=len(ce);counts['evidence_errors']+=len(ee);counts['missing_requests']+=len(missing);counts['unnecessary_requests']+=len(extra)
    if ce or ee or missing or extra:
        errors.append({'case_id':r['case_id'],'conditions':r['conditions'],'facts':r['facts'],'expected':g,'checklist':p,'direct':direct[r['case_id']]['parsed'],'condition_errors':ce,'evidence_errors':ee,'missing_requests':missing,'unnecessary_requests':extra})
payload={'counts':counts,'errors':errors,'reference':'pre-result semantic erratum'}
(N/'literature/frozen_functional_error_audit.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(payload,ensure_ascii=False,indent=2))
