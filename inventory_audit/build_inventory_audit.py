from pathlib import Path
import json,re,hashlib,unicodedata,difflib,collections
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
rules=read(ROOT/'datasets/statutory_rules.jsonl');cases=read(ROOT/'datasets/benchmark.jsonl')
refs=read(ROOT/'datasets/hq_reference.jsonl')+read(ROOT/'datasets/ny_reference.jsonl')
ref={x['case_id']:x for x in refs}
def norm(s):
 s=re.split(r'\s*\((?:described|provided)\b',s,flags=re.I)[0]
 s=unicodedata.normalize('NFKC',s).lower().replace('[','').replace(']','')
 return re.sub(r'[^a-z0-9]','',s)
def matches(s,pat):return [{'quote':m.group(),'start':m.start(),'end':m.end()} for m in re.finditer(pat,s,re.I)]
by_scope=collections.defaultdict(list);by_alias=collections.defaultdict(list)
for i,r in enumerate(rules):
 by_scope[norm(r['scope'])].append(i)
 for alias in r['aliases']:by_alias[alias.lower()].append(i)
mapping=[]
for c in cases:
 exact=by_scope.get(norm(c['rule_text']),[])
 note=ref.get(c['case_id'],{}).get('rule_note','')
 ids=re.findall(r'20\([a-z]+\)\([ivx]+\)\(\d+\)',note,re.I)
 alias=sorted(set(i for s in ids for i in by_alias.get(s.lower(),[])))
 cand=[]
 if not exact:
  pairs=sorted(((difflib.SequenceMatcher(None,norm(c['rule_text']),norm(r['scope'])).ratio(),i) for i,r in enumerate(rules)),reverse=True)
  cand=[{'index':i,'rule_id':rules[i]['rule_id'],'similarity':round(v,4)} for v,i in pairs[:2] if v>=.60]
 mapping.append({'case_id':c['case_id'],'same_code':bool(c['code_match']),'source':c['source'],'group':c['group'],'rule_note':note,'rule_text':c['rule_text'],'normalized_scope_exact_indices':exact,'indexed_note_alias_indices':alias,'unconfirmed_text_candidates':cand,'boundary':'Text match and note alias do not establish historical legal-version equivalence.'})
(OUT/'case_inventory_mapping.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in mapping)+'\n',encoding='utf-8')
manual_path=OUT/'semantic_review_codes.json'
manual=json.loads(manual_path.read_text(encoding='utf-8')) if manual_path.exists() else {}
group_path=OUT/'reviewed_condition_groups.jsonl'
group_readings={x['index']:x for x in read(group_path)} if group_path.exists() else {}
rows=[]
for i,r in enumerate(rules):
 s=r['scope']; temporal=i in (135,299)
 codes=manual.get(str(i))
 # These are candidate segmentation spans, not semantic atoms. No conjunction is resolved by this function.
 clauses=[]
 boundaries=[0]+[m.end() for m in re.finditer(r'(?<!\d),(?!\d)|;',s)]+[len(s)]
 for start,end in zip(boundaries,boundaries[1:]):
  while start<end and s[start].isspace():start+=1
  while end>start and (s[end-1].isspace() or s[end-1] in ',;'):end-=1
  if end>start:clauses.append({'quote':s[start:end],'start':start,'end':end,'kind':'punctuation_delimited_candidate_not_atom'})
 row={'index':i,'rule_id':r['rule_id'],'aliases':r['aliases'],'scope':s,'description':r['description'],'scope_sha256':hashlib.sha256(s.encode()).hexdigest(),'source_url':r['source_url'],'version':r['version'],'hts':r['hts'],
  'scope_format':'code_only_dated_transition' if temporal else 'code_only_single' if r['whole_code'] else 'product_description',
  'candidate_condition_spans':clauses,
  'candidate_logic_markers':matches(s,r'\b(?:and/or|and|or|other than|except|whether or not|including but not limited to|not)\b'),
  'candidate_object_markers':matches(s,r'\b(?:each|parts?|accessories|assembl(?:y|ies)|sets?|kits?|system|shaft|frame|housing|handle|whole|foregoing)\b'),
  'candidate_external_references':matches(s,r'\b(?:subheading|heading|CAS No\.|SAE|DIN|NEMA|Food and Drug Administration|Class 1)\b[^,;]*'),
  'actual_reviewed':codes is not None,'semantic_review':codes,
  'source_anchored_coarse_groups':group_readings.get(i),
  'coarse_required_group_count':group_readings.get(i,{}).get('coarse_required_group_count'),
  'necessary_condition_count':None,'count_boundary':'No ontology-independent atomic condition count is asserted. Candidate spans are retrieval aids only.',
  'case_coverage':{'normalized_scope_exact':[x['case_id'] for x in mapping if i in x['normalized_scope_exact_indices']], 'note_alias':[x['case_id'] for x in mapping if i in x['indexed_note_alias_indices']]}}
 for key in ['candidate_condition_spans','candidate_logic_markers','candidate_object_markers','candidate_external_references']:
  assert all(s[x['start']:x['end']]==x['quote'] for x in row[key])
 rows.append(row)
(OUT/'inventory_structural_audit.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in rows)+'\n',encoding='utf-8')
exactcase=[m for m in mapping if m['normalized_scope_exact_indices']]
exactrules=set(i for m in exactcase for i in m['normalized_scope_exact_indices'])
aliasrules=set(i for m in mapping for i in m['indexed_note_alias_indices'])
summary={'inventory_n':len(rules),'scope_format_counts':dict(collections.Counter(r['scope_format'] for r in rows)), 'actual_semantically_reviewed':sum(r['actual_reviewed'] for r in rows),'unreviewed':sum(not r['actual_reviewed'] for r in rows),'all_necessary_condition_counts_null':all(r['necessary_condition_count'] is None for r in rows),'source_span_validation':'all candidate spans equal immutable input substring','benchmark_cases':len(cases),'normalized_scope_exact_case_n':len(exactcase),'normalized_scope_exact_same_code_case_n':sum(m['same_code'] for m in exactcase),'normalized_scope_exact_rule_n':len(exactrules),'indexed_note_alias_case_n':sum(bool(m['indexed_note_alias_indices']) for m in mapping),'indexed_note_alias_rule_n':len(aliasrules),'normalized_scope_exact_rule_indices':sorted(exactrules),'note_alias_rule_indices':sorted(aliasrules),'original_rule_file_sha256':hashlib.sha256((ROOT/'datasets/statutory_rules.jsonl').read_bytes()).hexdigest(),'benchmark_sha256':hashlib.sha256((ROOT/'datasets/benchmark.jsonl').read_bytes()).hexdigest(),'coverage_boundary':'2024 index lexical scope/note mapping; not temporal equivalence, legal prevalence or representative population coverage','semantic_label_status':'AI source-coded silver; no independent expert validation; only reviewed fields, not a complete executable legal ontology'}
summary['source_anchored_coarse_group_readings']=len(group_readings)
summary['source_anchored_product_group_readings']=sum(bool(x['groups']) for x in group_readings.values())
summary['source_anchored_product_group_count']=sum(x['coarse_required_group_count'] for x in group_readings.values())
summary['zero_additional_product_group_code_rows']=sum(not x['groups'] for x in group_readings.values())
summary['coarse_group_count_boundary']='Explicit coarse source-reading representation, not atomic legal condition counts or intrinsic complexity scores.'
summary['all_exactly_covered_rules_have_coarse_group_reading']=exactrules.issubset(group_readings)
summary['candidate_condition_spans_n']=sum(len(r['candidate_condition_spans']) for r in rows)
summary['silver_semantic_unresolved_indices']=[r['index'] for r in rows if r['semantic_review'] and r['semantic_review']['interpretive_resolution']=='unresolved']
(OUT/'inventory_audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
