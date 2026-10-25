"""Assemble the manually reviewed 208-unit audit; no prediction model is used.

Usage: python assemble_condition_audit.py
All writes are confined to this script's directory. Historical data are read-only.
"""
from pathlib import Path
import json, re, hashlib, collections
from build_source_audit import load, readl, dump, OLD, OUT
from manual_condition_review import CASES, OVERRIDES, LOGIC, UNSAFE_CASES, RELAY_OBJECTS, COMPONENTS

def norm_map(text):
    chars=[]; offsets=[]
    trans={'\u201c':'"','\u201d':'"','\u2018':"'",'\u2019':"'",'\u2013':'-','\u2014':'-','\u00a0':' '}
    for n,c in enumerate(text):
        c=trans.get(c,c)
        if c.isspace():
            if chars and chars[-1]!=' ': chars.append(' '); offsets.append(n)
        else: chars.append(c);offsets.append(n)
    return ''.join(chars),offsets

def locate(src, quote, required=True):
    text=src['text']; a=text.find(quote)
    mode='exact'
    if a<0:
        nt,mp=norm_map(text); nq=norm_map(quote)[0].strip(); j=nt.find(nq)
        if j<0:
            if required: raise ValueError((src['ruling_id'],quote))
            return {'requested_quote':quote,'locator_status':'not_located','raw_text_span':None}
        a=mp[j]; b=mp[j+len(nq)-1]+1;mode='whitespace_or_typographic_normalization'
    else: b=a+len(quote)
    return {'quote':text[a:b], 'requested_quote':quote,'raw_text_span':[a,b],
            'paragraph_ids':[p['paragraph_id'] for p in src['paragraphs'] if p['raw_span'][0]<b and p['raw_span'][1]>a],
            'locator_status':mode,'source_text_sha256':src['text_sha256']}

def locate_frozen_fact(src, quote):
    loc=locate(src,quote,False)
    if loc['locator_status']!='not_located':return loc
    # N314745 subsets concatenate nonadjacent original product paragraphs.
    # Preserve each continuous source span and never manufacture a single span.
    if src['ruling_id']=='N314745':
        parts=[p.strip() for p in re.split(r'(?=The (?:first|second|third|fourth|fifth) model)',quote) if p.strip()]
        if len(parts)>1:
            spans=[locate(src,p,True) for p in parts]
            return {'locator_status':'noncontiguous_product_paragraph_concatenation',
              'requested_quote':quote,'raw_text_span':None,'source_spans':spans,
              'note':'Frozen quote concatenates selected product paragraphs; intervening products are deliberately excluded, not missing source words within a product.'}
    return loc

# Each entry was independently read as an attribute assertion, not copied from a
# case outcome. Subsentence extractions explicitly stop before legal conclusions.
RECOVERIES = [
 ('H330938_1','c4','Lastly, the submitted documentation describes the subject cables as imported on reels at very long lengths without connectors.','support','direct_attribute','submitted documentation','LAW AND ANALYSIS'),
 ('H330938_1','c1','The subject merchandise consists of a single cable with an aluminum conducting core that functions within a monopolar system to transmit power via a single phase and a single energized pole.','unknown','definition_dependent_attribute','agency technical description','LAW AND ANALYSIS'),
 ('H322923_1','c2','The subject wagons are fitted with four wheels, for use in household shopping and transporting personal goods, and are not mechanically propelled.','support','direct_attribute','agency description','LAW AND ANALYSIS'),
 ('H322923_1','c3','The subject wagons are fitted with four wheels, for use in household shopping and transporting personal goods, and are not mechanically propelled.','unknown','use_class_mapping_required','agency description','LAW AND ANALYSIS'),
 ('H340899_1','c3','Specifically, they are bagless vacuum cleaners with self-contained electric motors of a power not exceeding 1,500 W and have a dust receptacle capacity not exceeding 1 liter.','support','direct_attribute','agency description','LAW AND ANALYSIS'),
 ('H340899_1','c4','Specifically, they are bagless vacuum cleaners with self-contained electric motors of a power not exceeding 1,500 W and have a dust receptacle capacity not exceeding 1 liter.','support','direct_attribute','agency description','LAW AND ANALYSIS'),
 ('H341677_1','c2','The subject breathalyzers do not transmit the BAC information to a smart phone, tablet or computer via Bluetooth or Wi-Fi.','unknown','definition_dependent_attribute','agency description','LAW AND ANALYSIS'),
 ('H341677_1','c2','While the breathalyzers are battery operated and do not require a cord, they process all the data themselves and do not communicate using a wireless network.','unknown','definition_dependent_attribute','agency description','LAW AND ANALYSIS'),
 ('H314080_1','c3','fabrics of man-made micro-denier fibers impregnated, coated, covered, or laminated with polyurethane, of a width of at least 135 cm but no more than 150 cm, weighing at least 206 g/m2 but not more than 500 g/m2.','unknown','attributed_party_assertion','Protestant description; not independently measured','FACTS'),
 ('H314080_1','c4','fabrics of man-made micro-denier fibers impregnated, coated, covered, or laminated with polyurethane, of a width of at least 135 cm but no more than 150 cm, weighing at least 206 g/m2 but not more than 500 g/m2.','unknown','attributed_party_assertion','Protestant description; not independently measured','FACTS'),
 ('H323452_1','c1','Further, the golf simulator pads do not control the movement of a cursor on a computer screen to a desired location, nor can they use a cursor to delimit an area of the screen.','unknown','definition_dependent_attribute','agency description','LAW AND ANALYSIS'),
 ('H323452_1','c1','They also lack buttons or fingertip controls for performing functions in an application.','unknown','definition_dependent_attribute','agency description','LAW AND ANALYSIS'),
 ('H333673_1','c1','Out of the four ancillary sensors, only the front light sensor uses passive infrared detection to turn lights (i.e., the vehicle’s low beams) on and off.','unknown','component_quantifier_unresolved','agency component description','LAW AND ANALYSIS'),
 ('N318455','c1','In this case, the electric bicycle is capable of movement via the electric motor without the use of the pedals.','unknown','definition_dependent_attribute','agency drive-system description','BODY'),
 ('N319331','c1','As the subject merchandise is equipped with side-by-side rather than inline wheels','unknown','component_quantifier_unresolved','agency attribute clause; following conclusion excluded','BODY'),
 ('N316485','c2','Subsequently, a ruling request was made as to the classification of the seat components if imported individually and packaged in separate cartons.','unknown','object_scope_context','request context; no classification conclusion extracted','BODY'),
]

# Optional mappings expose, rather than conceal, interpretation. These are not
# authoritative replacement labels and are never used to repair administrative y.
OPTIONS = {
('H330938_1','c1'):[('single_pole_system','support','Map the full-source single phase/single energized pole description to monopolar.'),('no_domain_definition','unknown','Do not equate one visible conducting core with monopolar-system scope.')],
('H330938_1','c3'):[('conducting_core_only','support','Apply material restriction to the aluminum conductor, not the copper protective shield.'),('all_materials','refute','If any copper-bearing part counts, the explicitly described copper shield defeats the restriction.')],
('H341677_1','c2'):[('wireless_means_network_communication','refute','Full source expressly denies wireless-network communication, Bluetooth and Wi-Fi transmission.'),('cordless_is_sufficient','support','Battery-operated cordless sense would support, but differs from communications reading.')],
('H323452_1','c1'):[('cursor_control_is_necessary','refute','Full source expressly denies cursor control; the cited mouse definition requires it.')],
('H322923_1','c3'):[('stated_household_shopping_use_suffices','support','Full source explicitly says use in household shopping; accepts that as the class-of-use criterion.')],
('H314080_1','c3'):[('accept_attributed_party_specification','support','Party description supplies the exact width interval, without independent laboratory corroboration.')],
('H314080_1','c4'):[('accept_attributed_party_specification','support','Party description supplies the exact areal-mass interval, without independent laboratory corroboration.')],
('H332948_1','c4'):[('explicit_marketing_use_suffices','support','Retail packaging identifies flower drying and gives flower-drying instructions.')],
('H332948_3','c4'):[('any_advertised_use_suffices','support','Instructions mention flower drying.'),('principal_marketed_use_controls','refute','Cat-litter presentation, trade and principal use govern despite alternative-use instructions.')],
('H318593_1','c2'):[('predominant_base_metal','support','Treat 68.5 percent steel as controlling despite aluminum parts.')],
('H340899_1','c2'):[('commercial_floor_upright_category','refute','Backpack vacuum is distinct from the commercial upright floor-vacuum category.'),('physical_upright_orientation','support','A broader physical-orientation reading could include backpack position; not adopted as legal truth.')],
('H333371_1','c2'):[('laboratory_priority','refute','Accept laboratory 76 percent textile over the party 48 percent assertion.'),('party_priority','support','Accept party 48 percent textile; disputed by laboratory measurement.')],
('N312588','c2'):[('accept_component_heading_classification','refute','Treat the described diodes/transistors/ICs as heading 8541/8542 goods using incorporated tariff definitions.')],
('N327114','c3'):[('peak_output','refute','3000 W peak exceeds 1000 W.'),('nominal_output','support','1000 W nominal meets an inclusive 1000 W ceiling.')],
('N336939','c3'):[('accept_agency_heading_absence_assertion','support','Full source expressly asserts no 8541/8542 articles other than LEDs, but this is a classification-dependent negative statement.')],
}

def tier_state(tier,state): return state if tier=='direct' else 'unknown'

def main():
    op,initial,visible,sources=load()
    assert set(CASES)=={r['case_id'] for r in op}
    recovered=[]; rec_index=collections.defaultdict(list)
    for case,cid,q,state,admit,attribution,section in RECOVERIES:
        src=sources[case.split('_')[0]];loc=locate(src,q)
        entry={'case_id':case,'condition_id':cid,'condition_key':case+':'+cid,
         **loc,'official_url':src['official_url'],'source_path':src['raw_path'],'raw_sha256':src['raw_sha256'],
         'section':section,'admissibility':admit,'attribution':attribution,
         'strict_condition_state_after_restoration':state,
         'is_new_relative_to_excerpt':norm_map(loc['quote'])[0] not in norm_map(visible[case]['facts'])[0],
         'note':'Independent factual clause only; neither legal applicability sentence nor holding is inserted.'}
        recovered.append(entry);rec_index[(case,cid)].append(entry)
    numeric=readl(OLD/'numeric_reference_fields.jsonl')
    rows=[];cases=[];exceptions=[]
    for rec in op:
        case=rec['case_id']; v=visible[case];src=sources[case.split('_')[0]]
        product,attrs=CASES[case];attrs=attrs.split('|');assert len(attrs)==len(rec['conditions']),case
        original={c['condition_id']:c for c in initial[case]['conditions']}
        crow=[]
        for c,attr in zip(rec['conditions'],attrs):
            cid=c['condition_id'];key=(case,cid);rs=c['rule_span'];assert v['rule_text'][rs[0]:rs[1]]==c['rule_quote']
            state=c['evidence_state']
            tier,reason,basis=OVERRIDES.get(key,('direct',None,'The stated product property is explicitly supported/refuted by the cited factual span; ordinary unit conversion, set membership or bound comparison is allowed.'))
            assert state!='unknown' or key in OVERRIDES,(key,'unknown must be explicitly reviewed')
            role,formula=LOGIC.get(key,('required_condition','signed literal condition; negative wording is not negated again'))
            evidence=[]
            for e in c['fact_evidence']:
                a,b=e['span'];assert v['facts'][a:b]==e['quote'],(key,e)
                loc=locate_frozen_fact(src,e['quote'])
                if loc['locator_status']=='not_located':exceptions.append({'case_id':case,'condition_id':cid,**loc})
                evidence.append({'frozen_quote':e['quote'],'frozen_span':[a,b],'source_locator':loc})
            num=[n for n in numeric if n['case_id']==case and (c['rule_quote'].find(n['constraint']['quote'])>=0 or (rs[0]<=n['constraint']['span'][0] and n['constraint']['span'][1]<=rs[1]))]
            fields=[{'constraint':n['constraint'],'reference_fields':n['reference_fields'],'source_coding_reason':n['source_coding_reason'],'status':'previous test-only AI source fields, independently re-read here; no expert gold'} for n in num]
            if case=='N311039_33' and cid in ['c2','c3']:
                fields=[{'objects':RELAY_OBJECTS,'unit':'V' if cid=='c2' else 'A','rule_interval':{'lower':60,'lower_inclusive':False,'upper':250,'upper_inclusive':True} if cid=='c2' else {'lower':10,'lower_inclusive':True,'upper':None},'scope':'each product; alternative coil/contact voltage roles remain discrete, not an interval','aggregation':'all four listed products must satisfy; products 1, 3, 4 violate voltage under both roles; product 2 role-ambiguous'}]
            if case=='H322923_1' and cid=='c2':fields=[{'unit':'count','attribute':'wheels','allowed_set':[3,4],'frozen_value':None,'full_source_value':4}]
            if case=='N327114' and cid=='c3':fields=[{'unit':'W','attribute':'motor power','upper':1000,'upper_inclusive':True,'discrete_rating_fields':[{'rating':'nominal','value':1000},{'rating':'peak','value':3000}],'scope':'rating basis not named by literal rule; never a [1000,3000] uncertainty interval'}]
            input_state=tier_state(tier,state)
            rr=rec_index.get(key,[])
            direct_restored=[r['strict_condition_state_after_restoration'] for r in rr if r['admissibility']=='direct_attribute']
            full_state=direct_restored[0] if direct_restored else input_state
            if role.startswith('nonbinding'):input_state=full_state='not_applicable'
            options=OPTIONS.get(key,[])
            if tier in ['interpretive','disputed'] and state!='unknown' and not options:
                options=[('retain_original_mapping',state,basis)]
            row={'case_id':case,'condition_id':cid,'condition_key':case+':'+cid,
             'ruling_id':src['ruling_id'],'scope_source':'actual candidate exclusion quotation in the individual ruling; not substituted by 2024 inventory',
             'rule_quote':c['rule_quote'],'rule_span':rs,'rule_source_locator':locate(src,c['rule_quote'],False),
             'object':{'product_scope':product,'visible_product_description':v['facts'].split('. ')[0],
              'component':('coil and contact separately' if case=='N311039_33' else COMPONENTS.get(key,'whole article or explicitly named property-bearing part in cited factual span')),
              'quantifier':'all listed products in this pair unless explicitly marked unresolved; no inference to other products in ruling'},
             'attribute':attr,'logical_role':role,'logical_formula_note':formula,
             'compound':role not in ['required_condition','nonbinding_example','nonbinding_permission'],
             'numeric_unit_scope':fields,'fact_evidence':evidence,'fact_quote':[e['quote'] for e in c['fact_evidence']],
             'original_state':original[cid]['evidence_state'],'historical_operational_condition_state':state,
             'historical_operational_case_state':rec['operational_evidence_state'],
             'reference_tier':tier,'strict_excerpt_state':input_state,'strict_full_source_state':full_state,
             'input_available':bool(c['fact_evidence']),'unknown_reason':reason,
             'inference_basis':basis,'recovered_fact_evidence':rr,
             'interpretation_options':[{'policy':p,'state':st,'reason':why,
               'required_context':'frozen_excerpt_plus_declared_mapping' if p=='retain_original_mapping' else 'full_public_source_or_declared_definition_policy'} for p,st,why in options],
             'review_method':'AI reread of this rule, complete frozen facts and cited spans; for all historical-unknown cases, relevant facts and analysis throughout official full ruling also examined. Not an outcome-blind audit.',
             'expert_validated':False,'administrative_y_used_as_criterion':False}
            rows.append(row);crow.append(row)
        safe=case not in UNSAFE_CASES
        def aggregate(k):
            states=[r[k] for r in crow if r[k]!='not_applicable']
            if not safe:return 'logic_unresolved'
            if 'refute' in states:return 'refute'
            if all(x=='support' for x in states):return 'support'
            return 'unknown'
        cases.append({'case_id':case,'ruling_id':src['ruling_id'],'original_case_state':initial[case]['aggregate_evidence_state'],
          'historical_operational_case_state':rec['operational_evidence_state'],'safe_flat_conjunction':safe,
          'logic_unresolved':not safe,'logic_note':UNSAFE_CASES.get(case,'Conjunction of signed historical condition units at case level; this is not a completeness guarantee.'),
          'original_logical_structure':rec['logical_structure'],'strict_excerpt_state':aggregate('strict_excerpt_state'),
          'strict_full_source_state':aggregate('strict_full_source_state'),'condition_keys':[r['condition_key'] for r in crow],
          'full_source_review_scope':'complete relevant factual and analytical source text checked' if rec['operational_evidence_state']=='unknown' else 'complete frozen facts and source span validation; targeted context for numeric/refuted cases',
          'raw_sha256':src['raw_sha256'],'source_text_sha256':src['text_sha256']})
    assert len(rows)==208 and len(cases)==73
    def write_jsonl(name,xs):
        (OUT/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in xs),encoding='utf-8')
    write_jsonl('condition_audit_long.jsonl',rows);write_jsonl('case_audit.jsonl',cases)
    write_jsonl('recovered_attribute_spans.jsonl',recovered)
    # Model-visible expanded input: all source-only additions retain provenance.
    # Only direct attributes are appended automatically. Interpretation/party
    # claims are separate selectable payloads, never smuggled into the input.
    expanded=[]
    for rec in op:
        cid=rec['case_id'];extras=[]
        for r in recovered:
            if r['case_id']==cid and r['admissibility']=='direct_attribute' and r['quote'] not in extras:extras.append(r['quote'])
        expanded.append({**visible[cid],'facts_frozen':visible[cid]['facts'],'facts_direct_restored':visible[cid]['facts']+('\n'+'\n'.join(extras) if extras else ''),'added_attribute_quotes':extras})
    write_jsonl('source_audited_inputs.jsonl',expanded)
    old_unknown={c['case_id'] for c in cases if c['historical_operational_case_state']=='unknown'}
    counts=lambda k,x:dict(collections.Counter(r[k] for r in x))
    summary={'cases':73,'conditions':208,'underlying_rulings':len(sources),'historical_unknown_cases':len(old_unknown),
     'reference_tier_counts':counts('reference_tier',rows),'strict_excerpt_condition_counts':counts('strict_excerpt_state',rows),
     'strict_full_condition_counts':counts('strict_full_source_state',rows),'safe_flat_conjunction_cases':sum(c['safe_flat_conjunction'] for c in cases),
     'strict_case_excerpt_counts':counts('strict_excerpt_state',cases),'strict_case_full_counts':counts('strict_full_source_state',cases),
     'condition_excerpt_to_full':dict(collections.Counter(r['strict_excerpt_state']+' -> '+r['strict_full_source_state'] for r in rows)),
     'historical_to_strict_excerpt_case':dict(collections.Counter(c['historical_operational_case_state']+' -> '+c['strict_excerpt_state'] for c in cases)),
     'unknown_reason_condition_counts':dict(collections.Counter(r['unknown_reason'] for r in rows if r['case_id'] in old_unknown and r['strict_excerpt_state']=='unknown')),
     'unknown_reason_case_counts':dict(collections.Counter(reason for case in sorted(old_unknown) for reason in sorted({r['unknown_reason'] for r in rows if r['case_id']==case and r['strict_excerpt_state']=='unknown'}))),
     'recovery_rows':len(recovered),'direct_recovery_rows':sum(r['admissibility']=='direct_attribute' for r in recovered),
     'source_locator_exceptions':exceptions,
     'noncontiguous_fact_quote_rows':[r['condition_key'] for r in rows if any(e['source_locator']['locator_status']=='noncontiguous_product_paragraph_concatenation' for e in r['fact_evidence'])],
     'direct_scorable_conditions':sum(r['reference_tier']=='direct' and r['strict_excerpt_state']!='not_applicable' for r in rows),
     'nonbinding_conditions':sum(r['strict_excerpt_state']=='not_applicable' for r in rows),
     'direct_restoration_cases':sorted({r['case_id'] for r in recovered if r['admissibility']=='direct_attribute'}),
     'unknown_provenance_denominators':{'cases':47,'conditions':'all strict-unknown conditions within those 47 historical-unknown cases; causes overlap; do not sum counts to 47'},
     'guardrails':['208 are historical condition units, not guaranteed atomic or complete.','AI auditors have prior administrative-outcome exposure.','No human/expert validation; interpretation options are policies, not legal truth.','Full-source public-text audit cannot establish facts absent from the public ruling.','2024 inventory is context, not the historical case sampling frame.']}
    dump(OUT/'source_audit_summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
