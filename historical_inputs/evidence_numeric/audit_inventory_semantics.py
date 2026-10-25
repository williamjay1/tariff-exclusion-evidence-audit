"""AI semantic audit of every disagreement between two frozen inventory proxies.
Do not promote regex marker counts to validated prevalence estimates.
"""
from pathlib import Path
from collections import Counter
import json,re,hashlib
R=Path(__file__).resolve().parent;OLD=R.parents[1]
rows=[json.loads(x) for x in (OLD/'datasets/statutory_rules.jsonl').read_text('utf8').splitlines()]
# Read directly from the 38 literal scope descriptions, not from model outputs.
numeric={87:'excluded discrete voltage ratings',118:'width and length intervals',155:'specified BTU rating',164:'four copper layers',166:'two copper layers',195:'three wind cups and at least one solar panel',199:'60-minute operating duration',223:'net weight greater than 4.5 kg',235:'concentration up to 45 percent',247:'composition percentage intervals',281:'density and maximum number of edges',297:'9.5 mm drive-shaft dimension',372:'width and length intervals'}
non={89:'digits in chemical nomenclature',110:'referenced tariff heading',135:'temporal statistical-code transition',137:'incorporated tariff headings',177:'referenced tariff subheading',178:'SAE material grade',180:'SAE material grade',181:'SAE material grade',182:'ZF material grade',183:'SAE material grade',228:'chemical nomenclature and CAS identifier',229:'chemical nomenclature and CAS identifier',230:'chemical nomenclature and CAS identifier',246:'chemical nomenclature and CAS identifiers',291:'minimum required component inventory, not a scalar measured limit',294:'CAS identifier',299:'temporal statistical-code transition',303:'referenced tariff heading',307:'referenced tariff headings',351:'CAS identifier',353:'DIN connector standard identifier',365:'regulatory device class',369:'CAS identifier',373:'CAS identifier',374:'excluded tariff subheadings'}
audit=[]
for i,r in enumerate(rows):
    if r['quantitative_marker']==r['number_outside_code']:continue
    assert (i in numeric) != (i in non)
    audit.append({'rule_id':r['rule_id'],'scope':r['scope'],'quantitative_marker':r['quantitative_marker'],
      'number_outside_code':r['number_outside_code'],'explicit_measurable_or_count_requirement':i in numeric,
      'source_based_semantic_reason':numeric.get(i,non.get(i)),
      'reference_status':'AI source-coded semantic audit; not expert validation',
      'sampling':'All disagreement cases between the two frozen marker definitions; purposive diagnostic audit, not random validation.'})
assert len(audit)==38
(R/'inventory_marker_disagreement_audit.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in audit),encoding='utf8')
# Whole-code diagnostics separate full-HTS scope from code mentions and dated
# code replacements. Every retained code-only record is available below.
hts=r'\b\d{4}\.\d{2}\.\d{4}\b'
whole=[]
for r in rows:
    temporal_candidate=bool(re.match(hts,r['scope'].strip())) and bool(re.search(r'\b(?:prior to|effective)\b',r['scope'],re.I))
    if not r['whole_code'] and not temporal_candidate:continue
    scope=r['scope'];plain=bool(re.fullmatch(hts,scope.strip()))
    temporal=not plain and bool(re.search(r'\b(?:prior to|effective)\b',scope,re.I))
    whole.append({'rule_id':r['rule_id'],'scope':scope,'codes':re.findall(hts,scope),'frozen_whole_code_flag':r['whole_code'],
      'classification':'single statistical code' if plain else 'dated statistical-code transition' if temporal else 'requires additional scope review',
      'semantic_note':'Whole-code scope for the relevant historical code/version does not imply one timeless identifier. Dates are code-version conditions, not product measurements.' if temporal else 'No separate physical product description.'})
(R/'whole_code_semantic_audit.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in whole),encoding='utf8')
summary={'rules':len(rows),'frozen_marker_counts':{k:sum(bool(r[k]) for r in rows) for k in ['whole_code','quantitative_marker','number_outside_code','negation_marker','purpose_marker']},
  'proxy_disagreements':len(audit),'true_measurable_or_count_conditions_among_disagreements':sum(r['explicit_measurable_or_count_requirement'] for r in audit),
  'nonmeasurement_numbers_among_disagreements':sum(not r['explicit_measurable_or_count_requirement'] and r['number_outside_code'] for r in audit),
  'component_inventory_at_least_without_numeral':sum(not r['number_outside_code'] for r in audit),
  'whole_code_classifications':dict(Counter(r['classification'] for r in whole)),
  'unresolved_whole_codes':[r['rule_id'] for r in whole if r['classification']=='requires additional scope review'],
  'claim_boundary':'The original counts 162 quantitative markers, 198 outside-code digits, 163 negation markers, and 89 purpose markers describe surface features. They do not estimate prevalence of semantically quantified, negative or purpose requirements. This disagreement audit is not a population correction or precision/recall estimate.',
  'measurement_definition':'A stated physical, monetary, temporal-duration or item-count magnitude; excludes tariff/CAS/material-grade/standard identifiers and statutory dates. Minimum named component inventories are recorded separately.',
  'whole_code_boundary_note':'The frozen whole_code flag means exactly one standalone statistical code (41 records). Two additional code-only descriptions contain historical code replacements and dates and are not marked by that strict regex. They should not silently be counted as physical product descriptions; report 41 standalone codes plus 2 temporal code-only entries when using semantic scope categories.',
  'data_product_scope':'A versioned machine-readable transcription of one official USTR index; not a complete historical legal ontology or an independently expert-coded corpus.'}
(R/'inventory_semantic_audit.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
