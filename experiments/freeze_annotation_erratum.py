"""Record a source-semantic correction before any formal predictions are read."""
import datetime,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
inputs=ROOT/'controlled_cases.jsonl'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
variants=['base','irrelevant','changed','refute_missing','binding_original','binding_swapped','equivalent']
edits=[]
for variant in variants:
    ids=['f1'] if variant=='refute_missing' else (['f1','f3'] if variant in ['binding_original','binding_swapped'] else ['f1','f2'])
    sets=[[x] for x in ids]+([ids] if len(ids)>1 else [])
    edits.append({'case_id':'CF10_'+variant,'condition_id':'c2','state':'supported','acceptable_evidence_sets':sets})
record={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'pre-result reference erratum; no model input, prompt, raw output or original expected field modified',
 'input_sha256':sha(inputs),'reason':'Oak and teak are kinds of wood. A fact that the target frame is made of oak or teak establishes the wooden-frame companion condition, even without the separately worded wood fact.',
 'discovery':'The source-audit agent independently reread all 108 inputs and identified this issue without reading any formal model output. The parent then fixed this handling before reading formal results.',
 'parent_decision':'Main case decisions and 96 linked case relationships remain unchanged. Main condition/citation evaluation uses this erratum, with original-reference and whole-family-exclusion sensitivity retained. No inference is rerun.',
 'edits':edits,
 'effect':'One condition state, CF10_refute_missing c2, changes unknown to supported. Seven c2 citation references allow equivalent target-frame facts. Requests and whole-input states are unchanged.',
 'strict_refutation_with_other_unknown_denominator':11,
 'excluded_family_sensitivity':{'family':'frame_species','unique_inputs':99,'conditions':198,'linked_relationships':88},
 'independent_review_path':'../source_audit/controlled_interface_readonly_review.md',
 'forbidden_alternatives':'Facts about Product B or unrelated properties do not enter any acceptable evidence set.'}
path=ROOT/'annotation_erratum.json'
if path.exists():
    prior=json.loads(path.read_text());assert prior['edits']==record['edits'] and prior['input_sha256']==record['input_sha256']
else:path.write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({'status':'recorded','sha256':sha(path),'edits':len(edits)}))
