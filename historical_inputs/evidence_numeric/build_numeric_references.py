"""Test-only numeric fields hand specified by an AI from outcome-masked inputs.
No evaluated parser, predictions, or administrative y is read in this script.
"""
from pathlib import Path
import json,hashlib
from collections import Counter
R=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (R/'evidence_visible_inputs.jsonl').read_text('utf8').splitlines()]
entries=[]
def add(i,quote,attribute,dimension,unit,lo,li,hi,ui,fquote='',flo=None,fhi=None,reason='',state=None):
    r=rows[i]
    def sp(t,q):
        if q not in t:raise ValueError((i,q))
        return [t.index(q),t.index(q)+len(q)]
    fq=[fquote] if isinstance(fquote,str) and fquote else fquote if isinstance(fquote,list) else []
    constraint=dict(attribute=attribute,dimension=dimension,unit=unit,lower=None if lo is None else str(lo),lower_inclusive=li,
                    upper=None if hi is None else str(hi),upper_inclusive=ui,quote=quote,span=sp(r['rule_text'],quote))
    fields=[] if flo is None else [dict(attribute=attribute,dimension=dimension,unit=unit,lower=str(flo),upper=str(fhi),
                    source_quotes=[dict(quote=q,span=sp(r['facts'],q)) for q in fq],bound_interpretation=reason)]
    entries.append(dict(case_id=r['case_id'],opportunity_id=f"{r['case_id']}_n{sum(e['case_id']==r['case_id'] for e in entries)+1}",
      constraint=constraint,reference_fields=fields,evidence_quotes=[dict(quote=q,span=sp(r['facts'],q)) for q in fq],
      source_coding_reason=reason,expected_numeric_state=state,
      reference_status='AI source-coded test-only reference; not expert gold',
      decisive_role='A definite numeric violation defeats a conjunctive scope; numeric satisfaction alone never proves nonnumeric conditions.'))

add(0,'voltage exceeding 1,000 V','voltage','voltage','V',1000,False,None,None,'2000V',2000,2000,'The visible specification gives 2000 V. Encoded 35kV product names are not alternative measured fields.', 'pass')
add(2,'power not exceeding 1,500 W','power','power','W',None,None,1500,True,'power not exceeding 1,500 W','-Infinity',1500,'One-sided upper interval; no unstated lower bound is needed to verify this ceiling.','pass')
add(2,'tank capacity not over 4 liters','volume','volume','L',None,None,4,True,'dust receptacle capacity not over 4 liters','-Infinity',4,'The supplied upper bound pertains to the collection receptacle/tank.','pass')
add(3,'valued over $70','value','value','USD',70,False,None,None,reason='No value appears in the visible facts.',state='unknown')
add(6,'weighing not more than 21 kg','weight','mass','g',None,None,21000,True,'weigh less than 21Kg.', '-Infinity',21000,'The true source interval has an open upper endpoint; the closed hull remains sufficient for the inclusive rule, so this conservative executor representation preserves the result.','pass')
add(8,'weighing more than 4 kg but less than 8kg','weight','mass','g',4000,False,8000,False,'weigh between 4.3kg to 5.1kg.',4300,5100,'Explicit product weight range, normalized from kg to g.','pass')
add(9,'each with three or four wheels','wheel_count','count','count',3,True,4,True,reason='A discrete OR over integer counts {3,4}; no wheel count is supplied. The interval encoding is only valid with the integer domain.',state='unknown')
add(10,'width of at least 135 cm but not more than 150 cm','width','length','mm',1350,True,1500,True,reason='No width appears in visible facts.',state='unknown')
add(10,'weighing at least 206 g/m2 but not more than 500 g/m2','areal_mass','areal_mass','g/m2',206,True,500,True,reason='Areal mass, not ordinary mass; no measurement appears.',state='unknown')
for i in [14,16]:add(i,'granules measuring 0.25 to 0.6 mm in diameter','diameter','length','mm',0.25,True,0.6,True,'synthetic silica gel granules, 0.25 to 0.6 millimeters (mm)',0.25,0.6,'The ordinary granule-size reading is diameter and the stated to-range includes its endpoints; both are explicit coding assumptions.','pass')
for attr,hi,lo,fh in [('length',810,610,610),('width',410,302,302),('height',250,152,152)]:
    add(18,'not more than 81 cm by 41 cm by 25 cm',attr,'length','mm',None,None,hi,True,'61 centimeters (cm) by 30.2 cm by 15.2 cm (exclusive of handle)',None,None,'Independent AI audit identified that the reported dimensions explicitly exclude the handle while the rule does not establish that measurement scope. Complete-article dimension fields are unavailable; the corresponding numeric conditions remain unknown.','unknown')
add(18,'weighing not more than 52 kg','weight','mass','g',None,None,52000,True,'weighs 26.4 kilograms (kg)',26400,26400,'Own mass is separate from lifting capacity.','pass')
add(19,'lifting capacity of not more than 550 kg','mass_capacity','mass','g',None,None,550000,True,'lifting capacity of 6,000 pounds','2721554.22','2721554.22','Exact international avoirdupois conversion: 6000 x 453.59237 g; own mass is irrelevant.','fail')
add(20,'power not exceeding 1,500 W','power','power','W',None,None,1500,True,reason='No motor power is supplied.',state='unknown')
add(20,'dust receptacle capacity not exceeding 1 liter','volume','volume','L',None,None,1,True,'dust receptacle capacity is 0.64 L',0.64,0.64,'The 1.9 L bin volume is a separately named attribute, not this dust-receptacle capacity.','pass')
add(22,'containing less than 50 percent by weight of textile fibers','percentage','fraction','%',None,None,50,False,['48% polyester','approximately 76% textile'],48,76,'Two source claims straddle the threshold. The hull is only a witness to conflict, not a fabricated continuous measurement; the approximate report has no tolerance, preserving unknown.','unknown')
power={32:([250,300],['300-watt','250-watt']),34:([250],['250 watt electric motor']),40:([350,450,600,720,500],['350 watts','450 watts','600 watts','720 watts','500 watt']),41:([500],['500 watt electric motor']),42:([500],['500-watt']),49:([750],['750W rear-mounted hub motor']),51:([1000],['1,000W rear-mounted brushless motor']),60:([350,350,500],['350W','500W']),61:([750,350],['750W','350W']),65:([750],['750W motor']),66:([350],['350W electric bicycle']),67:([1000],['2 x 500-Watt electric motors']),68:([350],['350-watt capacity']),69:([1000,3000],['nominal power of 1,000W','maximum peak power of 3,000W']),71:([250],['250W electric motor'])}
for i,(vs,qs) in power.items():
    reason='All specified product powers are represented by their minimum/maximum hull; this preserves threshold state for a shared upper ceiling.'
    if i==67:reason='Two drive motors rated 500 W each give 1000 W total; sum is test-only transparent arithmetic, not extraction by the evaluated parser.'
    if i==69:reason='The literal rule does not resolve nominal versus peak power; 1000/3000 W alternatives straddle the threshold.'
    add(i,'each of a power not exceeding 1,000 W','power','power','W',None,None,1000,True,qs,min(vs),max(vs),reason,'unknown' if i==69 else 'pass')
add(33,'power output exceeding 500 W','power','power','W',500,False,None,None,'maximum power output of 850 Watts',850,850,'Output power is explicitly supplied.','pass')
for attr,v,f in [('length',148,140),('width',43,150),('height',335,86)]:
    add(33,'measuring 148mm in length, 43 mm in width and 335 mm in height',attr,'length','mm',v,True,v,True,'measuring 140 mm by 150 mm by 86 mm',f,f,'Exact required dimensions; the source ordering is used for the test-only fields. No permutation of the source dimensions matches the required triple, so the aggregate violation is orientation-independent.','fail')
add(36,'voltage exceeding 60 V but not over 250 V','voltage','voltage','V',60,False,250,True,['coil voltage rating of 12 VAC','coil voltage rating of 110 VDC','coil voltage rating of 48 VDC','contact voltage rating of 277 VAC'],None,None,'Keep the four products distinct. For products 1, 3 and 4, both coil and contact voltage lie outside (60,250] V; product 2 remains rating-ambiguous. A definite violating product refutes the all-listed-products proposition. No legal priority between coil and contact is assumed.','fail')
for product,coil in [(1,12),(2,110),(3,48),(4,48)]:
    entries[-1]['reference_fields'].append({'attribute':'voltage','dimension':'voltage','unit':'V',
      'subject':f'listed_relay_{product}',
      'interpretations':[{'attribute':'voltage','dimension':'voltage','unit':'V','lower':str(coil),'upper':str(coil),'rating':'coil'},
                         {'attribute':'voltage','dimension':'voltage','unit':'V','lower':'277','upper':'277','rating':'contact'}],
      'interpretation_operator':'all_alternatives_agree_else_unknown','subject_operator':'all_listed_products',
      'source_quotes':entries[-1]['evidence_quotes'],
      'bound_interpretation':'Discrete alternatives are not filled into a continuous interval; every listed product must satisfy the rule.'})
add(36,'contacts rated at 10 A or more','current','current','A',10,True,None,None,['rated at 30 A','at 40 A'],30,40,'All stated contact-current ratings satisfy the lower bound.','pass')
add(38,'voltage not exceeding 1,000 V','voltage','voltage','V',None,None,1000,True,'rated at 12 VDC',12,12,'The stated switches are 12 VDC; DC is a voltage qualifier.','pass')
add(39,'power not exceeding 250W','power','power','W',None,None,250,True,'250W brushless motor',250,250,'Stated propulsion power is on the inclusive boundary.','pass')
add(55,'output not exceeding 150 W','power','power','W',None,None,150,True,'maximum power output of 1.5 W',1.5,1.5,'The explicitly stated output is used, not an inferred new electrical quantity.','pass')
assert len({e['opportunity_id'] for e in entries})==len(entries)
f=R/'numeric_reference_fields.jsonl'
f.write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in entries),encoding='utf8')
s={'opportunities':len(entries),'cases':len({e['case_id'] for e in entries}),'expected_states':dict(Counter(e['expected_numeric_state'] for e in entries)),
   'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source':'73 outcome-masked visible inputs; no administrative labels, parser output or model predictions read',
   'status':'source-coded test-only reference, AI authored; no expert annotation',
   'known_semantic_assumptions':['ordered dimension correspondence for power-supply test fields; aggregate failure invariant to axis permutation','inclusive simple to-ranges','ordinary granule-size diameter interpretation','sum of two stated 500 W motors','rating ambiguity remains unknown','multiple product values collapsed only when interval threshold semantics preserve the state'],
   'independent_ai_audit_erratum':['H318593_1 dimensions exclude the handle. Three initially supported dimension conditions changed to unknown before final reporting; the source-coded fields are unavailable for the unqualified whole-article measurement. The qualitative operational case remains unknown.',
     'N311039_33: collapsing different products and rating alternatives into a continuous hull obscured definite violations. Per-product discrete alternatives replace the hull; products 1, 3 and 4 violate both candidate voltage interpretations, so the all-products claim is refuted. This is a source-based third AI review correction, not the initial two-pass agreement.']}
(R/'numeric_reference_manifest.json').write_text(json.dumps(s,indent=2),encoding='utf8')
print(json.dumps(s,indent=2))
