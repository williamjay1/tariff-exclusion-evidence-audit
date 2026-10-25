"""Paired linked-group resampling of frozen numerical agreement indicators.

This reads saved predictions only. It does not rerun or alter any parser, field,
reference, benchmark group, or prediction. The sample is the 33 numerical cases.
"""
from pathlib import Path
from collections import defaultdict
import hashlib, json
import numpy as np

R = Path(__file__).resolve().parent
OLD = R.parents[1]
def read(p):
    return [json.loads(x) for x in p.read_text('utf8').splitlines() if x.strip()]
def norm(x):
    return 'unknown' if x == 'not_parsed' else x
benchmark_path = OLD/'datasets/benchmark.jsonl'
bench = {x['case_id']: x for x in read(benchmark_path)}
layers = read(R/'numeric_layer_predictions.jsonl')
v2 = {x['case_id']: x for x in read(R/'real_numeric_v2_predictions.jsonl')}
assert len(layers) == 33 and len({x['case_id'] for x in layers}) == 33
assert set(v2) == {x['case_id'] for x in layers}
members = defaultdict(list)
indicators = []
for row in layers:
    cid = row['case_id']
    assert bench[cid]['code_match'] == 1
    assert v2[cid]['gold'] == row['numeric_reference_state']
    scores = {k: int(norm(v['state']) == row['numeric_reference_state']) for k,v in row['layers'].items()}
    scores['v2'] = int(v2[cid]['prediction'] == row['numeric_reference_state'])
    assert bool(scores['v2']) == v2[cid]['correct']
    members[bench[cid]['group']].append(cid)
    indicators.append({'case_id':cid, 'group':bench[cid]['group'],
        'numeric_reference_state':row['numeric_reference_state'], 'agreement':scores})
groups = sorted(members)
index = {g: np.array([i for i,r in enumerate(indicators) if r['group']==g],dtype=int) for g in groups}
seed = 20261007
B = 2000
rng = np.random.default_rng(seed)
draws = rng.integers(len(groups),size=(B,len(groups)))
samples = [np.concatenate([index[groups[int(j)]] for j in draw]) for draw in draws]
comparisons = [
    ('reference_fields_minus_automatic_fields_fixed_reference_rule', 'reference_rule_reference_fields', 'reference_rule_auto_fields'),
    ('reference_fields_minus_automatic_fields_fixed_automatic_rule', 'auto_rule_reference_fields', 'auto_rule_auto_fields'),
    ('reference_rule_minus_automatic_rule_fixed_reference_fields', 'reference_rule_reference_fields', 'auto_rule_reference_fields'),
    ('reference_rule_minus_automatic_rule_fixed_automatic_fields', 'reference_rule_auto_fields', 'auto_rule_auto_fields'),
    ('v2_minus_frozen_fully_automatic', 'v2', 'auto_rule_auto_fields'),
]
results = {}
for name, better, baseline in comparisons:
    a = np.array([r['agreement'][better] for r in indicators],dtype=int)
    b = np.array([r['agreement'][baseline] for r in indicators],dtype=int)
    delta = a-b
    values = np.array([delta[ix].mean() for ix in samples])
    assert np.isfinite(values).all()
    results[name] = {'comparison_A':better,'comparison_B':baseline,
        'A_agreement_count':int(a.sum()),'B_agreement_count':int(b.sum()),'n':len(a),
        'A_minus_B_agreement_rate':float(delta.mean()),
        'A_minus_B_percentage_points':float(delta.mean()*100),
        'A_correct_B_incorrect':int(np.sum((a==1)&(b==0))),
        'A_incorrect_B_correct':int(np.sum((a==0)&(b==1))),
        'both_correct':int(np.sum((a==1)&(b==1))), 'both_incorrect':int(np.sum((a==0)&(b==0))),
        'percentile_95_interval_rate':np.quantile(values,[.025,.975]).tolist(),
        'percentile_95_interval_percentage_points':(100*np.quantile(values,[.025,.975])).tolist(),
        'valid_resamples':int(np.isfinite(values).sum()), 'requested_resamples':B,
        'A_correct_B_incorrect_ids':[r['case_id'] for i,r in enumerate(indicators) if delta[i]==1],
        'A_incorrect_B_correct_ids':[r['case_id'] for i,r in enumerate(indicators) if delta[i]==-1],
    }
out = {
    'metric':'Exact agreement with three-state source-coded numeric reference, not administrative accuracy or causal effect',
    'n_cases':len(indicators), 'n_linked_groups':len(groups), 'seed':seed, 'bootstrap_replicates':B,
    'bootstrap_unit':'Original frozen benchmark linked groups, restricted to the 33 numerical cases; each sampled group contributes all its retained cases',
    'statistic':'Pooled case-weighted paired difference within each bootstrap sample; no refitting; identical group draws for all contrasts',
    'group_members':dict(sorted(members.items())), 'largest_restricted_group':max(map(len,members.values())),
    'resampled_case_count_range':[min(map(len,samples)),max(map(len,samples))],
    'comparisons':results,
    'input_sha256':{str(p.relative_to(OLD)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [benchmark_path,R/'numeric_layer_predictions.jsonl',R/'real_numeric_v2_predictions.jsonl',R/'numeric_reference_fields.jsonl']},
    'limitations':'Conditional fixed-prediction summaries for 33 purposively selected numeric cases. Reference fields and the relay adapter provide test-only binding information. Reference/reference agreement is internal execution consistency. V2 was developed on inspected diagnostics. Intervals do not establish legal validity, deployment benefit, causality, reference-label validity, or independent generalization.'
}
(R/'numeric_paired_differences.json').write_text(json.dumps(out,indent=2),encoding='utf8')
(R/'numeric_paired_case_indicators.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in indicators),encoding='utf8')
(R/'numeric_paired_bootstrap_draws.json').write_text(json.dumps({'seed':seed,'group_order':groups,'drawn_group_indexes':draws.tolist()}),encoding='utf8')
print(json.dumps({'n_cases':len(indicators),'groups':len(groups),'largest_group':out['largest_restricted_group'],
    'differences':{k:{f:v[f] for f in ['A_agreement_count','B_agreement_count','A_minus_B_percentage_points','percentile_95_interval_percentage_points','valid_resamples']} for k,v in results.items()}},indent=2))
