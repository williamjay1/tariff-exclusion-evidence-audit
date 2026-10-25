"""Read-only snapshot checks for the evidence/numeric portions of three draft sections."""
from pathlib import Path
from collections import Counter
import hashlib, json
R = Path(__file__).resolve().parent
M = R.parent / 'manuscript'
def rows(name):
    return [json.loads(x) for x in (R/name).read_text('utf8').splitlines() if x.strip()]
def obj(name):
    return json.loads((R/name).read_text('utf8'))
first = rows('evidence_condition_codes.jsonl')
second = obj('root_visible_evidence_review.json')
if isinstance(second, dict):
    print('Second-pass top-level keys', list(second))
    second = second.get('records', second.get('reviews', second.get('cases', second)))
conditions = [c for x in first for c in x['conditions']]
final = rows('evidence_operational_reference.jsonl')
refs = rows('numeric_reference_fields.jsonl')
out = {
    'draft_snapshot_sha256': {n:hashlib.sha256((M/n).read_bytes()).hexdigest() for n in ['task_methods.md','results_core.md','discussion_conclusion.md']},
    'first_pass_n':len(first), 'conditions':len(conditions),
    'first_case_keys':list(first[0]),
    'condition_key_union':sorted(set().union(*(set(x) for x in conditions))),
    'condition_key_intersection':sorted(set.intersection(*(set(x) for x in conditions))),
    'second_pass_n':len(second),
    'second_record_keys':list(second[0]),
    'operational_counts':dict(Counter(x['operational_evidence_state'] for x in final)),
    'numeric_cases':len({x['case_id'] for x in refs}),
    'numeric_condition_count':len(refs),
    'numeric_record_keys':list(refs[0]),
    'whole_code_inventory':obj('inventory_semantic_audit.json'),
    'review_scope':'Evidence/numeric/selection claims only. New neural experiments and other agents’ output are outside this audit; placeholders are not treated as defects.'
}
(R/'manuscript_claim_check_snapshot.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k not in ['whole_code_inventory']},indent=2))
