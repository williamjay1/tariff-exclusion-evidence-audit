"""Freeze isolated source-attribute recovery, without full-rule dispositions."""
import datetime,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent;SOURCE=ROOT.parent/'source_audit'
read=lambda p:[json.loads(s) for s in p.read_text(encoding='utf8').splitlines()]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
conditions={r['condition_key']:r for r in read(SOURCE/'condition_audit_long.jsonl')}
inputs={r['case_id']:r for r in read(SOURCE/'source_audited_inputs.jsonl')}
SPEC=[('H330938_1:c4','The subject cables must not be fitted with connectors.'),
 ('H322923_1:c2','Each subject wagon must have three or four wheels.'),
 ('H340899_1:c3','Each subject vacuum cleaner must have a self-contained electric motor.'),
 ('H340899_1:c4','Each subject vacuum cleaner must have motor power not exceeding 1500 W.')]
records=[];pairs=[];snapshots=[]
for key,req in SPEC:
    c=conditions[key];src=inputs[c['case_id']];cid=c['condition_id']
    assert c['strict_excerpt_state']=='unknown' and c['strict_full_source_state']=='support'
    admitted=[r for r in c['recovered_fact_evidence'] if r['admissibility']=='direct_attribute']
    assert len(admitted)==1
    a=admitted[0];raw=Path(a['source_path']);assert sha(raw)==a['raw_sha256']
    rawtext=json.loads(raw.read_text(encoding='utf8'))['text'];lo,hi=a['raw_text_span']
    assert rawtext[lo:hi]==a['quote']
    assert a['quote'] not in src['facts_frozen']
    snapshots.append({'condition':c,'frozen_facts':src['facts_frozen'],'admitted_attribute':a})
    for phase,state in [('before','unknown'),('after','supported')]:
        facts=[{'id':'f1','text':src['facts_frozen']}]
        if phase=='after':facts.append({'id':'f2','text':a['quote']})
        records.append({'case_id':'REC_'+key.replace(':','_')+'_'+phase,'group':c['ruling_id'],
          'family':key,'source_case_id':c['case_id'],'source_condition_key':key,
          'variant':phase,'mechanism':'source_attribute_recovery','target':c['object']['product_scope'],
          'rule_text':'Isolated required condition: '+req,'conditions':[{'id':cid,'requirement':req}],
          'facts':facts,'expected':{'states':{cid:state},'decision':state,'requests':[cid] if phase=='before' else [],
           'evidence':{cid:[] if phase=='before' else ['f2']}},'constructed':False,'diagnostic_counts_only':True,
          'source_rule_quote':c['rule_quote'],'source_recovered_span':a,
          'scope':'Only the isolated literal attribute condition is evaluated. No whole-exclusion or administrative outcome is inferred.',
          'reference_policy':'Explicit attribute evidence only. The motor item was historically interpreted as supported; here its frozen excerpt is unknown under the stricter stated policy.'})
    pairs.append({'pair_id':'REC_'+key,'family':key,'group':c['ruling_id'],'operation':'source_attribute_restoration',
       'left':'REC_'+key.replace(':','_')+'_before','right':'REC_'+key.replace(':','_')+'_after','expected_relation':'change'})
for name,rows in [('source_recovery_cases.jsonl',records),('source_recovery_pairs.jsonl',pairs),('source_recovery_source_snapshot.jsonl',snapshots)]:
    path=ROOT/name;data=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows)
    if path.exists():assert path.read_text(encoding='utf8')==data,'Frozen recovery data changed'
    else:path.write_text(data,encoding='utf8')
manifest={'status':'frozen_before_inference','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'n_endpoints':8,'n_conditions':4,'n_rulings':3,'n_distinct_restored_sentences':3,
 'parent_approval':'Four admitted direct attributes only, evaluated as isolated conditions with full frozen facts and the single source-only addition.',
 'data_agent_confirmation':'All four keys and strict U-to-S values independently rechecked against the cited official text; no expert labeling is claimed.',
 'limits':['Restoration is increased explicit product-attribute availability, not correction of four historical reference errors.',
 'The motor condition had historical support under an implicit component inference; its strict before-state is now unknown.',
 'Source audit and condition selection are post hoc. No held-out legal generalization is claimed.',
 'H340899 motor and power conditions share one restored sentence and one source, so the four pairs are dependent.',
 'Exact citation-ID matching checks retrieval of the admitted source sentence, not expert legal entailment.'],
 'hashes':{str(p.relative_to(ROOT.parent)):sha(p) for p in [SOURCE/'condition_audit_long.jsonl',SOURCE/'source_audited_inputs.jsonl',ROOT/'source_recovery_cases.jsonl',ROOT/'source_recovery_pairs.jsonl',ROOT/'source_recovery_source_snapshot.jsonl']}}
path=ROOT/'source_recovery_freeze.json'
if not path.exists():path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({'n':len(records),'pairs':len(pairs),'hash':sha(ROOT/'source_recovery_cases.jsonl')}))
