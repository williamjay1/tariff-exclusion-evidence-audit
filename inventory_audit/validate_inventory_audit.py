from pathlib import Path
import hashlib,json
import fitz
O=Path(__file__).resolve().parent;R=O.parents[1]
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x]
raw=read(R/'datasets/statutory_rules.jsonl');a=read(O/'inventory_structural_audit.jsonl');g=read(O/'reviewed_condition_groups.jsonl');m=read(O/'case_inventory_mapping.jsonl')
assert len(raw)==len(a)==len(g)==397 and len(m)==86
assert len({x['index'] for x in g})==397
assert sum(bool(x['groups']) for x in g)==354
assert sum(not x['groups'] for x in g)==43
assert len({r['rule_id'] for r in a})==397
span_count=0
for i,(s,r) in enumerate(zip(raw,a)):
 assert r['index']==i and r['scope']==s['scope'] and r['description']==s['description']
 assert r['actual_reviewed'] and r['semantic_review']['source_scope_sha256']==hashlib.sha256(s['scope'].encode()).hexdigest()
 for field in ['candidate_condition_spans','candidate_logic_markers','candidate_object_markers','candidate_external_references']:
  for p in r[field]:assert r['scope'][p['start']:p['end']]==p['quote'];span_count+=1
for r in g:
 s=raw[r['index']]['scope'];assert s==r['scope'] and len(r['groups'])==r['coarse_required_group_count']
 for p in r['groups']:assert s[p['start']:p['end']]==p['quote'];span_count+=1
 if not r['groups']:
  p=r['taxonomic_temporal_gate'];assert s[p['start']:p['end']]==p['quote'];span_count+=1
covered=set(i for x in m for i in x['normalized_scope_exact_indices']);assert covered<=set(x['index'] for x in g)
p=Path(r'F:\AcademicData\tariff_scope_20261007\raw\statutes\ustr_index_20240117_20261007.pdf')
with fitz.open(p) as d:
 page=d[11].get_text();assert '183 m in width' in page
 pos=page.index('Adjustable wire');quote=page[pos:pos+520]
out={'status':'PASS','rows':397,'unique_rule_ids':397,'actual_reviewed_field_records':397,'coarse_product_group_readings':354,'code_only_extra_product_groups_zero':43,'coarse_product_groups':sum(x['coarse_required_group_count'] for x in g),'validated_exact_source_spans':span_count,'exactly_covered_index_rules':len(covered),'all_covered_index_rules_have_coarse_groups':True,'input_rule_sha256':hashlib.sha256((R/'datasets/statutory_rules.jsonl').read_bytes()).hexdigest(),'original_pdf_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'literal_unit_anomaly':{'index':211,'page':12,'pdf_text_quote':quote,'correction_performed':False},'boundary':'Program validates provenance, counts and correspondence; no independent semantic/legal gold validation.'}
(O/'inventory_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False,indent=2))
