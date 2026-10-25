"""Structural intervention checks before inference; semantic review is separate."""
from pathlib import Path
from collections import Counter
import json,re,hashlib
from protocol import aggregate
ROOT=Path(__file__).resolve().parent
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf8').splitlines()]
def main():
    rows=read(ROOT/'constructed_cases_draft.jsonl');byid={r['case_id']:r for r in rows};pairs=read(ROOT/'constructed_pairs_draft.jsonl');checks=[]
    for r in rows:
        assert r['expected']['decision']==aggregate(list(r['expected']['states'].values()))
        fids={f['id'] for f in r['facts']}
        assert all(set(ids)<=fids for ids in r['expected']['evidence'].values())
        expected_requests=[k for k,v in r['expected']['states'].items() if v=='unknown'] if r['expected']['decision']=='unknown' else []
        assert r['expected']['requests']==expected_requests
    for p in pairs:
        a,b=byid[p['left']],byid[p['right']]
        for k in ['target','rule_text','conditions']:assert a[k]==b[k],(p,k)
        fa,fb=({x['id']:x['text'] for x in r['facts']} for r in [a,b])
        op=p['operation']
        if op=='deletion':assert fb=={k:v for k,v in fa.items() if k!='f1'}
        elif op=='restoration':assert fa=={k:v for k,v in fb.items() if k!='f1'}
        elif op=='irrelevant_addition':assert all(fb[k]==v for k,v in fa.items()) and len(fb)==len(fa)+1
        elif op in ['decisive_attribute','semantic_equivalence','wrong_object_only']:
            assert fa.keys()==fb.keys() and [k for k in fa if fa[k]!=fb[k]]==['f1']
        elif op=='refutation_preservation':assert fb=={k:v for k,v in fa.items() if k!='f2'}
        elif op=='object_binding_swap':
            # All token and number frequencies are identical: only their
            # assignment to A versus B changes. Companion fact is untouched.
            assert fa['f3']==fb['f3']
            bag=lambda d:Counter(re.findall(r'\w+|[^\w\s]',' '.join(d.values())))
            assert bag(fa)==bag(fb)
            assert fa['f1']==fb['f2'].replace('Product B','Product A')
            assert fa['f2'].replace('Product B','Product A')==fb['f1']
        actual='same' if a['expected']['decision']==b['expected']['decision'] else 'change'
        assert actual==p['expected_relation']
        checks.append({'pair_id':p['pair_id'],'operation':op,'pass':True})
    source=read(ROOT/'constructed_source_spans.jsonl')
    for s in source:
        for q in s['selected_rule_quotes']:assert s['full_original_rule'][slice(*q['span'])]==q['quote']
    out={'status':'PASS','inputs':len(rows),'relations':len(pairs),'families':len(source),'checks':checks,
         'not_checked':'Source-clause interpretation, synthetic fact semantics and legal scope require independent source review; this script only checks construction invariants.',
         'input_sha256':hashlib.sha256((ROOT/'constructed_cases_draft.jsonl').read_bytes()).hexdigest(),
         'pair_sha256':hashlib.sha256((ROOT/'constructed_pairs_draft.jsonl').read_bytes()).hexdigest()}
    (ROOT/'constructed_structural_audit.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
if __name__=='__main__':main()
