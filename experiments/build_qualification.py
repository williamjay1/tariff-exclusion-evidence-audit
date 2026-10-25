"""Freeze independent synthetic interface qualification before inference."""
from pathlib import Path
import json,hashlib,datetime
from protocol import aggregate
ROOT=Path(__file__).resolve().parent

def row(cid,target,requirements,facts,states,evidence,mechanism):
    conditions=[{'id':f'c{i+1}','requirement':v} for i,v in enumerate(requirements)]
    d=aggregate(states)
    return {'case_id':cid,'target':target,'rule_text':' AND '.join(requirements),
            'conditions':conditions,'facts':[{'id':f'f{i+1}','text':v} for i,v in enumerate(facts)],
            'expected':{'states':dict(zip([c['id'] for c in conditions],states)),
                        'evidence':dict(zip([c['id'] for c in conditions],evidence)),
                        'decision':d,'requests':[c['id'] for c,s in zip(conditions,states) if s=='unknown'] if d=='unknown' else []},
            'mechanism':mechanism,'data_status':'independent constructed protocol qualification, not a customs case'}

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    out=[]
    specs=[
      ('material','panel',['The panel must be made of steel.'],['The panel is made of steel.','The panel is made of plastic, not steel.','The panel has a smooth surface.']),
      ('shape','disc',['The disc must be circular.'],['The disc is circular.','The disc is rectangular, not circular.','The disc is 3 mm thick.']),
      ('strict_bound','parcel',['The parcel must weigh more than 7 kg.'],['The parcel weighs 8 kg.','The parcel weighs 7 kg.','The parcel has a blue exterior.']),
      ('interval','lamp',['The lamp must operate at more than 200 V and at most 250 V.'],['The lamp operates at 230 V.','The lamp operates at 110 V.','The lamp consumes 20 W.']),
      ('negation','lead',['The lead must not have connectors.'],['The lead has no connectors.','The lead has connectors at both ends.','The lead is 4 m long.']),
      ('object_binding','rack frame',['The rack frame must be made of steel.'],['The rack frame is made of steel. Its screws are plastic.','The rack frame is plastic, not steel. Its screws are steel.','The rack screws are steel. The frame is painted white.']),
      ('measurement_basis','crate',['The crate net mass must be at most 20 kg.'],['The crate net mass is 18 kg and gross mass is 23 kg.','The crate net mass is 23 kg.','The crate gross mass is 18 kg. Its net mass is not stated.']),
    ]
    for fam,target,req,variants in specs:
        for i,(facts,state) in enumerate(zip(variants,['supported','refuted','unknown'])):
            out.append(row(f'Q_{fam}_{i+1}',target,req,[facts],[state],[['f1'] if state!='unknown' else []],fam))
    req=['The module must be waterproof.','The module must weigh less than 5 kg.']
    out+=[row('Q_conjunction_1','module',req,['The module is waterproof.','The module weighs 3 kg.'],['supported','supported'],[['f1'],['f2']],'conjunction'),
          row('Q_conjunction_2','module',req,['The module is explicitly not waterproof. Its mass is not stated.'],['refuted','unknown'],[['f1'],[]],'decisive_refutation_with_missing'),
          row('Q_conjunction_3','module',req,['The module is waterproof. Its mass is not stated.'],['supported','unknown'],[['f1'],[]],'conjunction_missing')]
    assert len(out)==24
    # Separate miniature engineering dev set. No legal test condition appears.
    dev=[row('DEV_S','bead',['The bead must be green.'],['The bead is green.'],['supported'],[['f1']],'direct_attribute'),
         row('DEV_R','bead',['The bead must be green.'],['The bead is black and not green.'],['refuted'],[['f1']],'direct_attribute'),
         row('DEV_U','bead',['The bead must be green.'],['The bead is made of glass.'],['unknown'],[[]],'direct_attribute'),
         row('DEV_RU','tube',['The tube must be transparent.','The tube must weigh less than 9 kg.'],['The tube is opaque, not transparent.'],['refuted','unknown'],[['f1'],[]],'decisive_refutation_with_missing')]
    manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'frozen_before_inference',
              'threshold':{'qualification_cases':24,'minimum_decisions_correct':23,'minimum_condition_accuracy':.95,
                           'maximum_invalid':0,'maximum_unsupported_affirmations':0,'decisive_refutation_with_missing_must_pass':True},
              'model_order':['qwen14','granite8'],'selection_policy':'First fixed model meeting every qualification criterion; if neither meets them, development changes and requalification are explicitly logged, not hidden.',
              'semantics':'Textual evidence only. Unknown means input insufficiency, not administrative ineligibility.',
              'task_limit':'Conjunctive checklist supplied. Does not measure automatic condition extraction or nested legal interpretation.'}
    for name,rs in [('qualification_cases.jsonl',out),('development_cases.jsonl',dev)]:
        data=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs).encode()
        p=ROOT/name
        if p.exists():assert p.read_bytes()==data,'Frozen inputs differ'
        else:p.write_bytes(data)
        manifest[name+'_sha256']=hashlib.sha256(data).hexdigest()
    p=ROOT/'qualification_manifest.json'
    if not p.exists():p.write_text(json.dumps(manifest,indent=2),encoding='utf8')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
