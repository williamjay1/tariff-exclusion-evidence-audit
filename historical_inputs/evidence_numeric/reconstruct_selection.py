"""Reconstruct only stages proved by saved retrieval manifests and curated files."""
from pathlib import Path
from collections import Counter,defaultdict
import json,re,hashlib,random,difflib
R=Path(__file__).resolve().parent;OLD=R.parents[1];D=OLD/'datasets'
def read(name):return [json.loads(x) for x in (D/name).read_text('utf8').splitlines()]
def norm(s):return re.sub(r'\s+',' ',s).strip()
def write(name,x): (R/name).write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf8')
derived=read('cbp_rulings_derived.jsonl');by={r['rulingNumber']:r for r in derived}
refs=read('hq_reference.jsonl')+read('ny_reference.jsonl');bench=read('benchmark.jsonl')
br={r['case_id']:r for r in bench};rr=defaultdict(list)
for r in refs:rr[r['rulingNumber']].append(r)
qby=defaultdict(set);queries=[];querycounts={};searchsets=[]
for fn in ['cbp_search_index_20261007T143403Z.json','cbp_supplement_index_20261007T143907Z.json']:
    ix=json.loads((D/fn).read_text('utf8'));ss=set()
    for r in ix['rulings']:
        ss.add(r['rulingNumber']);qby[r['rulingNumber']].update(r.get('queries',[]))
    searchsets.append(ss)
    for q in ix['queries']:
        queries.append(dict(query=q['query'],pages=q['pages'],reported_total=q['reported_total'],retrieved=q['retrieved'],unique=q['unique']))
        assert q['reported_total']==q['retrieved']==q['unique']==sum(p['n'] for p in q['pages'])
searchunion=set.union(*searchsets)
assert searchunion<=set(by)
bm=json.loads((OLD/'results/benchmark_manifest.json').read_text('utf8'));exc={r['case_id']:r['reason'] for r in bm['excluded']}
inventory=[]
for r in derived:
    rid=r['rulingNumber'];records=rr.get(rid,[])
    inventory.append({'rulingNumber':rid,'official_url':r['official_url'],'collection':r['collection'].upper(),
        'queries':sorted(qby[rid]),'retrieval_source':'query_result' if rid in searchunion else 'explicit_seed',
        'curated_case_ids':[x['case_id'] for x in records],
        'retained_case_ids':[x['case_id'] for x in records if x['case_id'] in br],
        'excluded_curated_records':[dict(case_id=x['case_id'],reason=exc.get(x['case_id'])) for x in records if x['case_id'] not in br],
        'precuration_status':'curated_record_exists' if records else 'no_curated_record; individual screening decision not logged',
        'saved_automatic_screening_flags':r.get('screening_flags'),
        'raw_path':r['raw_path'],'derived_text_sha256':hashlib.sha256(r['text'].encode()).hexdigest()})
(R/'retrieval_to_sample_ledger.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in inventory),encoding='utf8')
# Verify each retained item against its actual saved official source and the
# curated extraction, rather than merely verifying that files contain 86 rows.
refmap={r['case_id']:r for r in refs};checks=[]
for b in bench:
    r=refmap[b['case_id']];source=by[b['rulingNumber']];text=norm(source['text'])
    fs=r['facts'] if isinstance(r['facts'],list) else [r['facts']]
    facts=[{'quote_sha256':hashlib.sha256(norm(f).encode()).hexdigest(),'exact_normalized_substring':norm(f) in text,'characters':len(norm(f))} for f in fs]
    rule=norm(r['rule_text']);reference=norm(r['reference_quote'])
    composition=None
    if not all(q['exact_normalized_substring'] for q in facts):
        target=b['facts'];blocks=difflib.SequenceMatcher(None,text,target,autojunk=False).get_matching_blocks()
        covered=set(j for block in blocks for j in range(block.b,block.b+block.size))
        unmatched=''.join(ch for j,ch in enumerate(target) if j not in covered)
        composition={'method':'Ordered exact character matching of whitespace-normalized official text; unmatched joining whitespace allowed.',
          'unmatched_nonwhitespace':re.sub(r'\s','',unmatched),'all_content_characters_source_grounded':not re.sub(r'\s','',unmatched),
          'source_spans':[[m.a,m.a+m.size] for m in blocks if m.size],'target_spans':[[m.b,m.b+m.size] for m in blocks if m.size],
          'explanation':{'N309775_buttons':'Joins source paragraphs for first and fourth products, omitting the intervening knob products.',
             'N314745_self':'Joins first, second and fourth product descriptions; third pedal-only product is omitted from this pair.',
             'N314745_pedal':'Joins third and fifth product descriptions; fourth self-propelled product is omitted from this pair.',
             'N316485':'Joins seat-component paragraphs, dimension sentence and final import-condition phrase; omits separate padding description and intervening prior-ruling history. The appended if-fragment is syntactically incomplete and the multi-product reference remains unknown.'}[b['case_id']]}
        assert composition['all_content_characters_source_grounded'],(b['case_id'],unmatched)
    checks.append({'case_id':b['case_id'],'rulingNumber':b['rulingNumber'],'official_url':source['official_url'],
      'source_collection':source['collection'].upper(),'source_collection_matches_benchmark':source['collection'].upper()==b['source'],
      'facts_match_curated':b['facts']==norm('\n'.join(fs)),'rule_matches_curated':b['rule_text']==rule,
      'factual_quotes':facts,'rule_exact_normalized_substring':rule in text,'reference_exact_normalized_substring':reference in text,
      'saved_facts_locators':r.get('facts_locators'),'saved_rule_locator':r.get('rule_locator'),'saved_reference_locator':r.get('reference_locator'),
      'administrative_label_matches_curated':b['y']==int(r['reference_disposition']=='eligible'),
      'noncontiguous_composition_audit':composition,
      'review_required':None if composition or all(f['exact_normalized_substring'] for f in facts) else 'Unresolved provenance discrepancy'})
(R/'retained_source_checks.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in checks),encoding='utf8')
summary={'snapshot_date':'2026-10-07','source':'Official CBP CROSS saved responses','endpoint':'https://rulings.cbp.gov/api/search',
 'parameters':{'fromDate':'2018-01-01','toDate':'2026-10-07','pageSize':100,'sortBy':'DATE_ASC'},
 'queries':queries,'query_hit_occurrences':sum(q['retrieved'] for q in queries),
 'first_query_union':len(searchsets[0]),'broad_query_union':len(searchsets[1]),'all_query_union':len(searchunion),
 'explicit_seed_ids_outside_query_union':sorted(set(by)-searchunion),'first_detail_requests':1916,'supplemental_new_details':566,
 'retried_detail_ids':['H323646','N326929'],'final_unique_official_records':len(derived),
 'curated_records':len(refs),'curated_unique_rulings':len(rr),'unrepresented_rulings':len(set(by)-set(rr)),
 'retained_pairs':len(bench),'retained_rulings':len({r['rulingNumber'] for r in bench}),
 'curated_exclusions':dict(Counter(exc.values())),'samecode_pairs':sum(r['code_match']==1 for r in bench),
 'source_checks':{'facts_match_curated':sum(r['facts_match_curated'] for r in checks),'rules_match_curated':sum(r['rule_matches_curated'] for r in checks),
   'all_fact_quotes_exact_after_whitespace_normalization':sum(all(f['exact_normalized_substring'] for f in r['factual_quotes']) for r in checks),
   'rule_quote_exact_after_whitespace_normalization':sum(r['rule_exact_normalized_substring'] for r in checks),
   'reference_quote_exact_after_whitespace_normalization':sum(r['reference_exact_normalized_substring'] for r in checks),
   'collection_correct':sum(r['source_collection_matches_benchmark'] for r in checks),'outcomes_match_curated':sum(r['administrative_label_matches_curated'] for r in checks),
   'noncontiguous_fact_compositions':[{k:r[k] for k in ['case_id','noncontiguous_composition_audit']} for r in checks if r['noncontiguous_composition_audit']]},
 'not_identified':['Number of records read manually or by an AI before curation','Complete record-level reasons for the 2390 unrepresented rulings','Recall of relevant product-specific exclusions across CROSS','Any human or expert annotation agreement'],
 'interpretation':'The 2482-to-102 transition is an AI-assisted purposive curation step with incomplete precuration decision logging, not a documented exhaustive systematic screening. The later 102-to-86 exclusions and retrieval coverage are reproducible.',
 'data_statement':{'language':'English','jurisdiction':'United States customs rulings, China Section 301 product-exclusion scope',
  'population':'A purposively curated official-ruling corpus; not a random sample of import transactions, all exclusions, or compliance users',
  'source_type':'HQ review/dispute rulings and NY prospective classification letters differ in administrative selection and drafting',
  'labels':'Published administrative dispositions, extracted and organized with AI assistance; separate outcome-masked evidence states are AI-assisted diagnostic references',
  'fact_limit':'Model inputs omit later legal analysis and may omit facts or definitions essential to the administrative disposition',
  'intended_use':'Retrospective restricted-text decision-support evaluation, diagnostic failure analysis and reproducibility research',
  'not_validated_for':'Live customs advice, autonomous legal decisions, new jurisdictions or deployment prevalence estimates',
  'human_experts':0,'raw_source_immutability':'Original response files remain unmodified; this revision writes only separate derived audit products'}}
write('selection_audit.json',summary)
print(json.dumps({k:v for k,v in summary.items() if k not in ['queries','data_statement']},indent=2))
