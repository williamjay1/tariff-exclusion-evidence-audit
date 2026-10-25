from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parent
f=R/'numeric_reference_fields.jsonl';raw=f.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='03e71823e044593f326f853bb40ae81d08189b208111c889eff492bbc036502b'
(R/'numeric_reference_fields_handle_corrected_v2.jsonl').write_bytes(raw)
rows=[json.loads(x) for x in raw.decode().splitlines()]
reason='Corresponding ordered enclosure dimensions are paired; all three source values are below their corresponding ceilings. Axes are test-only ordinal length/width/height bindings.'
vis={r['case_id']:r for r in map(json.loads,(R/'evidence_visible_inputs.jsonl').read_text('utf8').splitlines())}
quote='61 centimeters (cm) by 30.2 cm by 15.2 cm';start=vis['H318593_1']['facts'].index(quote)
for r in rows:
    if r['case_id']=='H318593_1' and r['constraint']['dimension']=='length':
        attr=r['constraint']['attribute'];v={'length':'610','width':'302','height':'152'}[attr]
        qs=[{'quote':quote,'span':[start,start+len(quote)]}]
        r['reference_fields']=[dict(attribute=attr,dimension='length',unit='mm',lower=v,upper=v,source_quotes=qs,bound_interpretation=reason)]
        r['evidence_quotes']=qs;r['source_coding_reason']=reason;r['expected_numeric_state']='pass'
initial=''.join(json.dumps(r,ensure_ascii=False)+'\r\n' for r in rows).encode()
assert hashlib.sha256(initial).hexdigest()=='e5a9bb70d39976667b0311a3fa23e855c0df297eb2adc71b15640e23d863f2f3'
(R/'numeric_reference_fields_initial_v1.jsonl').write_bytes(initial)
(R/'numeric_reference_history.json').write_text(json.dumps({'v1':{'sha256':hashlib.sha256(initial).hexdigest(),'recovery':'Byte-identical reconstruction of original saved source-coded fields from recorded code and original SHA-256, verified against pre-audit hash.'},'v2':{'sha256':hashlib.sha256(raw).hexdigest(),'change':'Handle-excluded jack dimensions changed from pass to unavailable/unknown.'}},indent=2),encoding='utf8')
print('Preserved v2; recovered v1 verified byte-identical against recorded SHA-256.')
