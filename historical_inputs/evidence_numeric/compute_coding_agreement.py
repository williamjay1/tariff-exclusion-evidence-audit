"""Agreement for independently completed copies of the unlabelled review packet.
Usage: python compute_coding_agreement.py coder_a.jsonl coder_b.jsonl
No placeholder form is counted as completed annotation.
"""
import json,argparse
from pathlib import Path
from collections import Counter
def load(p):
    raw=p.read_text('utf8')
    try:
        x=json.loads(raw);rows=x['records'] if isinstance(x,dict) and 'records' in x else x
    except json.JSONDecodeError:rows=[json.loads(x) for x in raw.splitlines() if x.strip()]
    out={}
    conv={'support':'support','supported':'support','refute':'refute','refuted':'refute','unknown':'unknown'}
    for r in rows:
        k=r.get('item_id',r.get('case_id'));d=r.get('response',r)
        v=d.get('evidence_state',d.get('state',d.get('aggregate_evidence_state')))
        if v is None:continue
        if k in out or v not in conv:raise ValueError((k,v))
        out[k]=conv[v]
    return out
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('first',type=Path);a.add_argument('second',type=Path);a.add_argument('--output',type=Path)
    args=a.parse_args();x=load(args.first);y=load(args.second);keys=sorted(set(x)&set(y));n=len(keys)
    if not n:raise SystemExit('No jointly completed annotations; agreement is not estimable.')
    cx,cy=Counter(x[k] for k in keys),Counter(y[k] for k in keys)
    po=sum(x[k]==y[k] for k in keys)/n;pe=sum(cx[k]*cy[k] for k in ['support','refute','unknown'])/n**2
    result={'n_jointly_completed':n,'only_first':sorted(set(x)-set(y)),'only_second':sorted(set(y)-set(x)),
      'agreement':po,'cohen_kappa':(po-pe)/(1-pe) if pe!=1 else None,
      'confusion':dict(Counter(x[k]+'->'+y[k] for k in keys)),
      'interpretation':'Agreement concerns coding reproducibility only. It does not establish expertise, independent validity, or source correctness.'}
    if args.output:args.output.write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result,indent=2))
