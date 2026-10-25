"""Freeze the parent-reviewed controlled diagnostic inputs before inference."""
import datetime, hashlib, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'constructed_design_manifest.json').read_text(encoding='utf8'))
expected={'constructed_cases_draft.jsonl':'ec31de7be7b6b11a3f01b119fbd4791ad0f3bc2d54d913bcdca6da55811fd5d9',
          'constructed_pairs_draft.jsonl':'7ba9a001f942f5344eea0d1334597fe4abb703e81422da2a17bc25a3f32dd7e8'}
for src,digest in expected.items():
    p=ROOT/src;assert sha(p)==digest
    dst=ROOT/src.replace('_draft','')
    if dst.exists():assert sha(dst)==digest
    else:shutil.copyfile(p,dst)
summaries={k:json.loads((ROOT/'outputs'/f'qwen14_qualification_cases_{k}_summary.json').read_text()) for k in ['direct','checklist']}
assert all(v['passed'] for v in summaries.values())
record={**manifest,'status':'frozen_before_formal_inference','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'independent_review':{'reviewer':'parent AI research agent /root; not a human expert',
 'record':'Parent independently read build_interventions.py, all twelve full source provisions, expected states and source spans, and explicitly approved the current 108 inputs and 96 dependent relationships. Deletion removes only f1 without renumbering f2.'},
 'interpretation_boundary':['The every-granule quantifier and the frame-species scope are explicitly supplied controlled interpretations, not validated legal interpretations.',
 'Every task uses a two-condition excerpt rather than a complete exclusion rule.',
 'This is a deliberately constructed diagnostic domain, not an exhaustive boundary test or a held-out sample of new adjudications.',
 'Direct receives raw excerpt plus facts; checklist additionally receives a supplied canonical condition representation. The comparison contains an input-representation privilege.',
 'Direct condition, evidence and request metrics are not applicable.',
 'Ninety-six relationships share 108 endpoints; restoration reuses the original base endpoint. Relationships are not independent observations.'],
 'qualification':summaries,
 'qualification_functional_caveat':'Q_negation_3 correctly returns unknown but omits the necessary c1 request. This was not a frozen qualification gate; it remains a reported functional failure.',
 'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'constructed_cases.jsonl',ROOT/'constructed_pairs.jsonl',ROOT/'constructed_source_spans.jsonl',ROOT/'constructed_structural_audit.json',ROOT/'protocol.py',ROOT/'run_evidence_audit.py',ROOT/'qualification_manifest.json']}}
out=ROOT/'constructed_freeze.json'
if out.exists():
    prior=json.loads(out.read_text());assert prior['hashes']==record['hashes']
else:out.write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({'status':'frozen','input_sha256':sha(ROOT/'constructed_cases.jsonl'),'n':108,'pairs':96}))
