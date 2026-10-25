"""Source-anchored constructed two-condition diagnostics, not observed cases."""
from pathlib import Path
import json,hashlib
from protocol import aggregate
ROOT=Path(__file__).resolve().parent;PROJ=ROOT.parents[1]
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf8').splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

# Primary requirement, companion requirement, and literal source quotes. Every
# fact below is purpose-built synthetic text. The original facts are not reused.
FAMILIES=[
 ('connectors','H330938_1',['not fitted with connectors','for a voltage exceeding 1,000 V'],
  ['Product A must not be fitted with connectors.','Product A must be for a voltage exceeding 1000 V.'],
  'Product A is not fitted with connectors.','Product A is fitted with connectors.','Product A has no connectors attached.','Product A is rated for 2000 V.'),
 ('lifting_capacity','H318593_2',['lifting capacity of not more than 550 kg','Hydraulic jacks of a kind for raising vehicles'],
  ['Product A must have a lifting capacity of at most 550 kg.','Product A must be a hydraulic jack of a kind for raising vehicles.'],
  'Product A has a lifting capacity of 500 kg.','Product A has a lifting capacity of 600 kg.','Product A has a lifting capacity of 0.5 metric tonnes.','Product A is a hydraulic jack designed for raising vehicles.'),
 ('motor_power','H340899_1',['power not exceeding 1,500 W','dust receptacle capacity not exceeding 1 liter'],
  ['Product A must have motor power not exceeding 1500 W.','Product A must have dust receptacle capacity not exceeding 1 liter.'],
  'The self-contained motor in Product A has power 1200 W.','The self-contained motor in Product A has power 1600 W.','The self-contained motor in Product A has power 1.2 kW.','Product A has a dust receptacle capacity of 0.5 liters.'),
 ('single_use','N310745',['single-use','of textile fabrics'],
  ['Product A must be single-use.','Product A must be made of textile fabrics.'],
  'Product A is a face mask designed for a single use only.','Product A is a reusable face mask, not a single-use mask.','Product A is a face mask intended to be used once and then discarded.','Product A is made of textile fabrics.'),
 ('precious_plating','H330005_1',['containing no article plated with precious metal','of stainless steel'],
  ['Product A must contain no article plated with precious metal.','Product A must be a set of stainless-steel flatware.'],
  'No article in Product A is plated with any precious metal.','One article in Product A is plated with gold, a precious metal.','Product A contains zero articles with precious-metal plating.','Product A is a set of stainless-steel flatware.'),
 ('textile_fraction','H333371_1',['containing less than 50 percent by weight of textile fibers','coated with rubber or plastics'],
  ['Product A must contain less than 50 percent by weight of textile fibers.','Product A must be coated with rubber or plastics.'],
  'Textile fibers constitute 20 percent of the total weight of Product A.','Textile fibers constitute 60 percent of the total weight of Product A.','Product A contains 20 grams of textile fibers per 100 grams of total weight.','Product A is a glove coated with rubber.'),
 ('granule_diameter','H332948_1',['granules measuring 0.25 to 0.6 mm in diameter','put up in retail packaging'],
  ['Every granule in Product A must have diameter from 0.25 to 0.6 mm.','Product A must be put up in retail packaging.'],
  'Every granule in Product A has a diameter of 0.4 mm.','Every granule in Product A has a diameter of 0.8 mm.','Every granule in Product A has a diameter of 400 micrometres.','Product A is put up in retail packaging.'),
 ('load_instrument_mass','H316154_1',['weighing more than 4 kg but less than 8kg','Programmable DC electronic load instruments'],
  ['Product A must weigh more than 4 kg and less than 8 kg.','Product A must be a programmable DC electronic load instrument.'],
  'Product A weighs 6 kg.','Product A weighs 9 kg.','Product A weighs 6000 grams.','Product A is a programmable DC electronic load instrument.'),
 ('electrical_power','N303860',['not electrically powered','of plastic'],
  ['Product A must not be electrically powered.','Product A must be made of plastic.'],
  'Product A is not electrically powered.','Product A is electrically powered.','Product A operates without electrical power.','Product A is a salad spinner made of plastic.'),
 ('frame_species','N309167',['other than of teak','with a wooden frame'],
  ['The frame of Product A must not be made of teak.','Product A must have a wooden frame.'],
  'The frame of Product A is made of oak, not teak.','The frame of Product A is made of teak.','The frame of Product A is oak and contains no teak.','Product A is an upholstered dining chair with a wooden frame.'),
 ('propulsion_power','N306552',['each of a power not exceeding 1,000 W','with electric power for propulsion'],
  ['Product A must have power not exceeding 1000 W.','Product A must use electric power for propulsion.'],
  'Product A has a power rating of 900 W.','Product A has a power rating of 1200 W.','Product A has a power rating of 0.9 kW.','Product A is a motorcycle that uses electric power for propulsion.'),
 ('fireplace_mass','H311957_1',['weighing not more than 21 kg','Electric fireplaces'],
  ['Product A must weigh not more than 21 kg.','Product A must be an electric fireplace.'],
  'Product A weighs 20 kg.','Product A weighs 22 kg.','Product A weighs 20000 grams.','Product A is an electric fireplace.'),
]

def main():
    bench={r['case_id']:r for r in read(PROJ/'datasets/benchmark.jsonl')};rows=[];pairs=[];sources=[]
    for fi,s in enumerate(FAMILIES,1):
        family,cid,quotes,requirements,good,bad,equiv,companion=s;b=bench[cid]
        # Lower/upper case in bracketed quote forms is preserved, not silently
        # normalised. All selected excerpts must occur in the original rule.
        assert all(q in b['rule_text'] for q in quotes),(cid,quotes,b['rule_text'])
        source={'family':family,'case_id':cid,'group':b['group'],'full_original_rule':b['rule_text'],
                'selected_rule_quotes':[{'quote':q,'span':[b['rule_text'].index(q),b['rule_text'].index(q)+len(q)]} for q in quotes],
                'supplied_condition_interpretations':requirements,
                'data_status':'AI-authored constructed diagnostic based on selected clause excerpts, not an observed product or complete exclusion rule'}
        sources.append(source)
        facts={
          'base':[good,companion],
          'deleted':[companion],
          'irrelevant':[good,companion,'The shipping carton is blue and the warehouse inventory code is UX1600W.'],
          'changed':[bad,companion],
          'refute_missing':[bad],
          'binding_original':[good,bad.replace('Product A','Product B'),companion],
          'binding_swapped':[bad,good.replace('Product A','Product B'),companion],
          'equivalent':[equiv,companion],
          'other_only':[good.replace('Product A','Product B'),companion],
        }
        states={v:['supported','supported'] for v in facts}
        states.update(deleted=['unknown','supported'],changed=['refuted','supported'],refute_missing=['refuted','unknown'],binding_swapped=['refuted','supported'],other_only=['unknown','supported'])
        for variant,ff in facts.items():
            cstates=states[variant];decision=aggregate(cstates)
            evidence={'c1':[] if cstates[0]=='unknown' else ['f1'],
                      'c2':[] if cstates[1]=='unknown' else (['f3'] if variant in ['binding_original','binding_swapped'] else ['f2'])}
            row={'case_id':f'CF{fi:02d}_{variant}','family':family,'group':b['group'],'source_case_id':cid,
                 'variant':variant,'mechanism':variant,'target':'Product A',
                 'rule_text':'Controlled two-condition excerpt: '+quotes[0]+'; AND '+quotes[1]+'. Both apply to Product A.',
                 'conditions':[{'id':f'c{i+1}','requirement':req} for i,req in enumerate(requirements)],
                 'facts':[{'id':f'f{i+2 if variant=="deleted" else i+1}','text':fact} for i,fact in enumerate(ff)],
                 'expected':{'states':dict(zip(['c1','c2'],cstates)),'evidence':evidence,'decision':decision,
                             'requests':[f'c{i+1}' for i,v in enumerate(cstates) if v=='unknown'] if decision=='unknown' else []},
                 'source_selected_quotes':source['selected_rule_quotes'],'constructed':True,
                 'scope':'Only the two selected conditions are tested. Other legal conditions are outside this artificial clause.'}
            rows.append(row)
        for operation,left,right,relation in [
          ('deletion','base','deleted','change'),('restoration','deleted','base','change'),
          ('irrelevant_addition','base','irrelevant','same'),('decisive_attribute','base','changed','change'),
          ('refutation_preservation','changed','refute_missing','same'),
          ('object_binding_swap','binding_original','binding_swapped','change'),
          ('semantic_equivalence','base','equivalent','same'),('wrong_object_only','base','other_only','change')]:
            pairs.append({'pair_id':f'CF{fi:02d}_{operation}','family':family,'group':b['group'],'operation':operation,
                          'left':f'CF{fi:02d}_{left}','right':f'CF{fi:02d}_{right}','expected_relation':relation})
    assert len(rows)==108 and len(pairs)==96
    assert len({json.dumps({k:r[k] for k in ['target','rule_text','conditions','facts']},sort_keys=True) for r in rows})==108
    for name,data in [('constructed_cases_draft.jsonl',rows),('constructed_pairs_draft.jsonl',pairs),('constructed_source_spans.jsonl',sources)]:
        (ROOT/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data),encoding='utf8')
    (ROOT/'constructed_design_manifest.json').write_text(json.dumps({'status':'draft_for_independent_input_audit_before_freeze','n_unique_inputs':108,'n_families':12,'n_source_groups':len({r['group'] for r in rows}),'n_linked_relationships':96,'reused_endpoints':'Restoration reverses deletion using the same base endpoint; pair results are dependent.','source_benchmark_sha256':sha(PROJ/'datasets/benchmark.jsonl'),'input_sha256':sha(ROOT/'constructed_cases_draft.jsonl'),'pairs_sha256':sha(ROOT/'constructed_pairs_draft.jsonl')},indent=2),encoding='utf8')
    print('Built 108 unique constructed inputs, 96 linked relations, 12 source families; pending independent source/logic audit.')
if __name__=='__main__':main()
