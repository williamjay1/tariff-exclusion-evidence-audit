"""Validate locators and write compact reports from the source audit."""
import json,hashlib,collections
from pathlib import Path
from build_source_audit import OUT,OLD,readl,dump,load

GROUPS={
'excerpt_omission':{'excerpt_omission','excerpt_omission_and_definition','excerpt_omission_party_assertion','implicit_component_inference'},
'no_sufficient_attribute_in_public_source':{'public_source_attribute_absent','object_and_public_source_gap','object_scope_and_public_source_gap','unsupported_party_claim'},
'definition_category_or_use':{'definition_required','category_or_use_mapping','chemical_function_definition','functional_use_scope','part_and_material_scope','incorporated_heading_definition','incorporated_definition_unavailable','incorporated_definition_and_exception','mixed_material_scope','competing_use_interpretations','definition_and_conflicting_sources'},
'object_component_or_measurement_scope':{'component_material_scope','measurement_scope_mismatch','component_quantifier_scope','part_versus_machine_scope','assembly_category_scope','object_and_public_source_gap','object_scope_and_public_source_gap','composite_component_binding','mixed_material_scope'},
'source_or_interpretation_conflict':{'source_conflict','definition_and_conflicting_sources','unsupported_party_claim','competing_use_interpretations','rating_basis_ambiguity'},
}

def main():
    rows=readl(OUT/'condition_audit_long.jsonl');cases=readl(OUT/'case_audit.jsonl')
    op,initial,vis,src=load();by={r['condition_key']:r for r in rows}
    audit=json.loads((OUT/'source_audit_summary.json').read_text(encoding='utf-8'))
    checked={'rule_source_spans':0,'frozen_fact_spans':0,'continuous_fact_source_spans':0,'recovery_spans':0}
    def verifyloc(rid,loc):
        if loc.get('source_spans'):
            for l in loc['source_spans']:verifyloc(rid,l)
            return
        assert loc['locator_status']!='not_located',loc
        a,b=loc['raw_text_span'];assert src[rid]['text'][a:b]==loc['quote']
        checked['continuous_fact_source_spans']+=1
    for r in rows:
        checked['rule_source_spans']+=1;verifyloc(r['ruling_id'],r['rule_source_locator'])
        for e in r['fact_evidence']:
            checked['frozen_fact_spans']+=1;a,b=e['frozen_span'];assert vis[r['case_id']]['facts'][a:b]==e['frozen_quote']
            verifyloc(r['ruling_id'],e['source_locator'])
    for r in readl(OUT/'recovered_attribute_spans.jsonl'):
        verifyloc(r['case_id'].split('_')[0],r);checked['recovery_spans']+=1
    u=[r for r in rows if r['historical_operational_case_state']=='unknown']
    old_u=[r for r in u if r['historical_operational_condition_state']=='unknown']
    provenance={}
    for group,reasons in GROUPS.items():
        rr=[r for r in u if r['unknown_reason'] in reasons and r['strict_excerpt_state']=='unknown']
        provenance[group]={'case_ids':sorted({r['case_id'] for r in rr}),'case_n':len({r['case_id'] for r in rr}),
          'condition_keys':[r['condition_key'] for r in rr],'condition_n':len(rr),
          'historically_unknown_condition_n':sum(r['historical_operational_condition_state']=='unknown' for r in rr)}
    audit['unknown_provenance_sets']=provenance
    audit['historical_unknown_subset']={'cases':47,'all_conditions':len(u),'historically_unknown_conditions':len(old_u),'strict_unknown_conditions':sum(r['strict_excerpt_state']=='unknown' for r in u),
      'note':'These sets overlap. A case can have omitted evidence and an unresolved definition simultaneously. Source recovery does not imply whole-case support.'}
    audit['locator_verification']=checked
    audit['historical_unknown_review_rulings']=len({r['ruling_id'] for r in u})
    audit['historical_unknown_direct_restored_conditions']=[r['condition_key'] for r in rows if r['historical_operational_condition_state']=='unknown' and r['strict_full_source_state']=='support' and r['strict_excerpt_state']=='unknown']
    # Write a review record for every case. The source-review scope is explicit;
    # exact source matching is not a claim of independent semantic validation.
    review=[]
    for c in cases:
        rr=[r for r in rows if r['case_id']==c['case_id']]
        review.append({'case_id':c['case_id'],'condition_keys':c['condition_keys'],'reviewed_all_historical_units':True,
          'manual_product_attribute_assignments':True,'full_public_source_review':c['historical_operational_case_state']=='unknown',
          'review_scope':c['full_source_review_scope'],'source_text_sha256':c['source_text_sha256'],
          'strict_unknown_conditions':[r['condition_key'] for r in rr if r['strict_excerpt_state']=='unknown'],
          'unresolved_fields_permitted':True,'prior_outcome_exposure':True,'expert_validation':False})
    (OUT/'case_review_records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in review),encoding='utf-8')
    # Five complete evidence chains, all condition units and raw spans included.
    chains=[]
    explanations={
      'H330938_1':'The omitted connector fact is explicit in the analysis and changes c4 from unknown to support. Monopolar topology and copper-shield scope remain interpretation-dependent. Therefore source restoration alone does not create a strict supported case.',
      'H318593_1':'The stated 61 x 30.2 x 15.2 cm excludes the handle, while the candidate ceiling does not. The full source does not establish the complete dimensions. The separate 550 kg rule in H318593_2 is decisively refuted by the stated 6000 lb load capacity (2721.55422 kg). Neither observation establishes overall legal eligibility.',
      'N311039_33':'The rule is (60,250] V with contacts >=10 A. Bind 12/277, 110/277, 48/277, 48/277 V to four products as coil/contact alternatives, not a pooled interval. Products 1, 3 and 4 fail either rating-role interpretation; product 2 alone is unresolved. Under all-listed-products quantification the voltage condition is refuted. Contact ratings 30/40/40/40 A satisfy their independent threshold.',
      'H333371_1':'The party supplies 48 percent textile, whereas a reported CBP laboratory result is about 76 percent. Both passages are visible. No text-recovery operation resolves the conflict; laboratory priority and party priority deliberately produce different optional states.',
      'H333673_1':'The full source identifies only the front-light sensor as using passive infrared for light switching. The assembly also contains other sensors. Whether using passive infrared applies existentially to a component or universally to an apparatus is not encoded as a mandatory all-components rule. Preserve unresolved logic.'}
    for case,note in explanations.items():
        related=[case]+(['H318593_2'] if case=='H318593_1' else [])
        chains.append({'case_id':case,'related_case_ids':related,'explanation':note,
          'source':{k:v for k,v in src[case.split('_')[0]].items() if k not in ['text','paragraphs']},
          'cases':[c for c in cases if c['case_id'] in related],
          'conditions':[r for r in rows if r['case_id'] in related]})
    dump(OUT/'case_chains.json',chains)
    md=['# Source and condition-reference audit','',
      'This is an AI-assisted audit of 73 historical case–scope pairs and their 208 existing condition units, linked to 67 official CBP ruling snapshots. It is not human or expert gold. The auditor has previously seen administrative outcomes; this work cannot be called a fresh blind annotation. Administrative outcomes were not used as acceptance criteria, and no requirement to match those outcomes was imposed. The candidate scope is the quotation used in each ruling, not a replacement taken from the 2024 exclusion inventory.','',
      '## What was checked','',
      'Every historical condition, its complete frozen factual input, its cited evidence and its object/property assignment was read. All 47 historically unknown cases received additional review of relevant facts and analysis throughout the full official public ruling. For the remaining cases the audit checks complete frozen facts and source spans, with targeted context for numeric/refuted cases. A program verifies literal spans and assembles the table; it does not infer the object labels or decide the condition tiers. Direct means an explicit source-text attribute relation with ordinary arithmetic or lexical equivalence. It does not mean that the public statement has been empirically corroborated or legally validated.','',
      'The final tiers are **132 direct units (130 scoreable and 2 nonbinding), 45 interpretive, 19 insufficient and 12 disputed**. The strict excerpt states are **125 support, 5 refute, 76 unknown and 2 not applicable**. Adding the admitted independent full-source attributes gives **129 support, 5 refute, 72 unknown and 2 not applicable**. The two nonbinding units are an illustrative “including” list and a “whether or not” permission; they are not mandatory positive conditions.','',
      'The 208 units are inherited review units, not a claim that every exclusion has been fully or atomically formalized. Local disjunctions, negative exclusions, component quantifiers and illustrative examples remain marked. **58 cases** permit the restricted outer conjunction over the signed condition units; **15 cases** remain outside that flat interface. This strict diagnostic produces **10 supported, 3 refuted, 45 unknown and 15 logic-unresolved cases** for both excerpt and directly restored views. It must not be substituted for, or merged with, the historical AI-coded 21/5/47 reference. The unchanged case totals coexist with meaningful changes to individual conditions.','',
      '## What full-source recovery changes','',
      '| Case and condition | Independent source attribute | Boundary |','|---|---|---|',
      '| H330938 c4 | Submitted documentation describes imported cables without connectors. | Repairs the earlier claim that no connector-specific fact appears anywhere in the ruling. It does not settle monopolar or conductor-material scope. |',
      '| H322923 c2 | Wagons are fitted with four wheels. | Class-of-use interpretation remains separate. |',
      '| H340899 c3 | Vacuums have self-contained electric motors. | The historical c3 was already inferred as support; the strict layer had withheld that inference. |',
      '| H340899 c4 | Motor power does not exceed 1500 W. | Backpack versus commercial upright-vacuum category remains unresolved. |','',
      'These are four directly restored condition relations in three cases. Only three were historically unknown conditions: H330938 c4, H322923 c2 and H340899 c4. Other recoverable passages are retained separately: H341677 explicitly denies wireless-network transmission but needs a communications definition of “wireless”; H314080 supplies party-attributed width and areal-mass claims; H333673 supplies component-specific functionality. No legal applicability or holding sentence is appended as an observed product property.','',
      '## Provenance of the 47 historical unknown cases','',
      f'These cases contain {len(u)} historical units, of which {len(old_u)} were historically unknown and {sum(r["strict_excerpt_state"]=="unknown" for r in u)} are unknown under the stricter relation-only policy. The following sets overlap and their case counts must not be added to 47. A case can contain both an omitted attribute and an unresolved definition.','',
      '| Source of unresolved evidence | Cases / 47 | Strict-unknown condition units |','|---|---:|---:|']
    for name,x in provenance.items():md.append(f'| {name.replace("_"," ")} | {x["case_n"]} | {x["condition_n"]} |')
    md+=['','The machine-readable summary includes the actual case and condition membership of every set. The “public source absent” designation means no sufficient independent assertion was located in this public ruling, not that the underlying technical document or real-world fact cannot exist. No negative attribute is inferred merely from silence.','',
      '## Exact locations and excerpt construction','',
      'All 208 rule-unit quotations locate in the raw official text, allowing only recorded whitespace or typographic normalization. Every frozen condition evidence quotation now has one or more verified continuous source spans. N314745_self and N314745_pedal deliberately concatenate nonadjacent product paragraphs: the audit preserves their frozen concatenated span and supplies separate original spans for each selected product. No artificial continuous source span is claimed. N316485 has a truncated individual-import context in the excerpt; the full procedural sentence is retained as context, not as proof that plywood is unfinished.','',
      'Raw JSON byte hashes and decoded-text hashes are separately recorded. Offsets address Python Unicode character positions in the unmodified decoded text; hashes identify the byte-level snapshot. Exact quote matching proves location, not legal validity. The full public source itself occasionally has apparent wording inconsistencies (for example the Kent product name in the N308085 reasoning); these are not silently used to supply object-specific facts.','',
      '## Five auditable chains','']
    for case,note in explanations.items():md += [f'### {case}','',note,'']
    md += ['## Reuse and limits','',
      '`condition_audit_long.jsonl` contains object scope, property, signed logical role, local formula, numeric/unit scope, both historical states, strict excerpt/full-source states, exact evidence locations and optional interpretation policies. `case_audit.jsonl` exposes the flat-interface boundary. `recovered_attribute_spans.jsonl` is the restoration interface; only entries marked direct_attribute enter `facts_direct_restored`. `case_chains.json` provides all conditions and locators for the five examples.','',
      '`evaluate_interpretation_policy.py` applies only explicitly named policies supplied in a JSON configuration. It never selects a policy to agree with the administrative result. Changing interpretation can yield a contrary determinate state; such results are retained. The evaluator refuses to flatten marked unresolved logic and does not read administrative outcome y. These sensitivity states are declared assumptions, not a single replacement silver label.','',
      'No new experts, external measurements, or unseen-case validation are claimed. No historical input, reference, prediction or raw snapshot was overwritten. The remaining direct-property resource supports a bounded evidence-interface experiment; it does not evaluate general legal eligibility.']
    (OUT/'source_audit_report.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    dump(OUT/'source_audit_summary.json',audit)
    paths=['condition_audit_long.jsonl','case_audit.jsonl','recovered_attribute_spans.jsonl','source_audited_inputs.jsonl','case_review_records.jsonl','case_chains.json','source_audit_summary.json','source_audit_report.md','policy_sensitivity.json','policy_sensitivity.md','manual_condition_review.py','assemble_condition_audit.py','evaluate_interpretation_policy.py','policy_sensitivity.py','finish_audit_report.py','controlled_interface_readonly_review.md']
    paths=[p for p in paths if (OUT/p).exists()]
    manifest={'status':'SOURCE_AUDIT_COMPLETE_WITH_DECLARED_INTERPRETIVE_LIMITS','sha256':{name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in paths},'read_only_old_sources':True,'verification':checked,'unresolved_source_locators':0}
    dump(OUT/'audit_delivery_manifest.json',manifest)
    print(json.dumps({'status':manifest['status'],'provenance':provenance,'verification':checked},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
