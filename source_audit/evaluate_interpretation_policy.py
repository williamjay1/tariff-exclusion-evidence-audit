"""Explicit interpretation sensitivity, not a new truth label.

Input JSON is {"name": "...", "context": "full_source" or "excerpt",
"overrides": {"H330938_1:c1": "single_pole_system", ...}}.
No overrides are selected automatically. Output stays in source_audit.
"""
import json,sys
from pathlib import Path
from collections import Counter
from build_source_audit import OUT,readl,dump

def evaluate(config):
    context=config.get('context','full_source');assert context in ['full_source','excerpt']
    field='strict_full_source_state' if context=='full_source' else 'strict_excerpt_state'
    rows=readl(OUT/'condition_audit_long.jsonl');by={r['condition_key']:r for r in rows}
    states={k:r[field] for k,r in by.items()};changes=[]
    for key,policy in config.get('overrides',{}).items():
        if key not in by:raise ValueError('Unknown condition '+key)
        options={o['policy']:o for o in by[key]['interpretation_options']}
        if policy not in options:raise ValueError('Unknown option '+key+':'+policy)
        choice=options[policy]
        if context=='excerpt' and choice['required_context']!='frozen_excerpt_plus_declared_mapping':
            raise ValueError('Policy requires full-source or added definition context: '+key)
        changes.append({'condition_key':key,'before':states[key],'after':choice['state'],**choice})
        states[key]=choice['state']
    cases=[]
    for c in readl(OUT/'case_audit.jsonl'):
        ss=[states[k] for k in c['condition_keys'] if states[k]!='not_applicable']
        if not c['safe_flat_conjunction']:result='logic_unresolved'
        elif 'refute' in ss:result='refute'
        elif all(s=='support' for s in ss):result='support'
        else:result='unknown'
        cases.append({'case_id':c['case_id'],'state':result,'safe_flat_conjunction':c['safe_flat_conjunction']})
    return {'name':config.get('name','unnamed'),'context':context,'warning':'Interpretation sensitivity only. These choices are neither legal truth nor independent validation. Administrative labels are not read by this evaluator.',
      'changes':changes,'cases':cases,'counts':dict(Counter(x['state'] for x in cases))}

if __name__=='__main__':
    config=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')) if len(sys.argv)>1 else {'name':'strict_full_source_no_interpretation','context':'full_source','overrides':{}}
    result=evaluate(config)
    name=config.get('name','unnamed')
    if not all(c.isalnum() or c in '-_' for c in name):raise ValueError('Use a simple output name')
    dump(OUT/('policy_'+name+'.json'),result)
    print(json.dumps(result['counts']))
