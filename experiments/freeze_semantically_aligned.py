"""Pre-outcome correction: both arms receive the same complete controlled clause."""
import datetime,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:[json.loads(s) for s in p.read_text(encoding='utf8').splitlines()]
old=ROOT/'constructed_cases.jsonl'
assert sha(old)=='ec31de7be7b6b11a3f01b119fbd4791ad0f3bc2d54d913bcdca6da55811fd5d9'
rows=read(old)
for row in rows:
    row['rule_text']='Controlled two-condition clause: '+ ' AND '.join(c['requirement'] for c in row['conditions'])
    row['scope']='Only these two supplied controlled conditions are tested. Original source quotations are provenance, not a complete exclusion rule.'
data=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows)
path=ROOT/'controlled_cases.jsonl'
if path.exists():assert path.read_text(encoding='utf8')==data
else:path.write_text(data,encoding='utf8')
sources=[ROOT/'constructed_pairs.jsonl',ROOT/'constructed_source_spans.jsonl',ROOT/'protocol.py',ROOT/'run_evidence_audit.py',ROOT/'qualification_manifest.json']
pilots=list((ROOT/'outputs').glob('qwen14_constructed_cases_*'))
# Preserve all superseded files; count/hash bytes without inspecting predictions.
record={'status':'frozen_before_formal_inference','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'n_unique_inputs':108,'n_source_families':12,'n_dependent_relationships':96,
 'input_sha256':sha(path),'hashes':{str(p.relative_to(ROOT)):sha(p) for p in sources},
 'change_reason':'Parent identified semantic information asymmetry before any formal predictions were examined. The direct clause previously lacked the explicit every-granule and frame-scope interpretation supplied to the checklist. Both arms now receive exactly the same complete two-condition controlled clause; checklist adds only the structured duplicate condition representation and IDs.',
 'approval':'Parent requested this precise pre-outcome correction after reviewing all twelve source clauses and the full draft; all facts, expected states, pair links, qualification prompts and thresholds remain fixed.',
 'superseded_input_sha256':sha(old),
 'superseded_pilot_preserved':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'jsonl_lines':len(p.read_bytes().splitlines()) if p.suffix=='.jsonl' else None} for p in pilots],
 'scope':['Synthetic, source-anchored two-condition excerpts, not complete legal exclusions.',
 'Every-granule quantification and frame-species scope are supplied controlled interpretations, not verified legal interpretations.',
 'Restoration reuses base endpoints. The 96 relationships are not 96 independent cases.',
 'Direct condition/evidence/request metrics are NA. Both arms share semantic clause content; condition representation and requested output differ.',
 'No model/prompt selection used the superseded pilot or the formal outcomes.'],
 'qualification_model':'qwen14','qualification_decisions':{'direct':'24/24','checklist':'24/24'},'qualification_condition_accuracy':'27/27',
 'qualification_limit':'One unknown qualification item omitted its necessary request. This was not among the frozen qualification thresholds and remains a reported error.'}
freeze=ROOT/'controlled_freeze.json'
if freeze.exists():assert json.loads(freeze.read_text())['input_sha256']==record['input_sha256']
else:freeze.write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({'input_sha256':sha(path),'n':len(rows),'superseded_pilot':[{'path':p['path'],'n':p['jsonl_lines']} for p in record['superseded_pilot_preserved']]}))
