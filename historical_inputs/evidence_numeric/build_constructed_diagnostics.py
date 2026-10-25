"""Designed diagnostic cases. Labels are specified independently of the old engine.
These are constructed examples, not additional CBP rulings or human annotations.
"""
from pathlib import Path
from collections import Counter
import json,hashlib
R=Path(__file__).resolve().parent
rows=[]
def pair(family,k,rule,a,b,ga,gb,reason,kind='decisive_change',rule_b=None):
    for side,facts,state,scope in [('a',a,ga,rule),('b',b,gb,rule_b or rule)]:
        rows.append(dict(case_id=f'D_{family}_{k}_{side}',facts=facts,rule_text=scope,
          gold=state,y={'pass':1,'fail':0,'unknown':None}[state],group=family,
          mechanism=family,pair_id=f'{family}_{k}',pair_type=kind,
          reference_rationale=reason,constructed=True,
          reference_status='AI-authored design reference, not human/expert validation',
          non_numeric_conditions='Assumed satisfied; only explicitly stated predicates are evaluated.',
          source='new constructed diagnostic; no administrative ruling label'))

# Identifier insertions must preserve the state, including missing-evidence cases.
for k,(p,state) in enumerate([(900,'pass'),(1100,'fail'),(1000,'pass'),(None,'unknown')],1):
    fact=f'The motor power is {p} W.' if p is not None else 'The motor power is unspecified.'
    pair('identifier',k,'Motor power not exceeding 1,000 W.',fact,f'Model ZX72600W. {fact}',state,state,
         'An explicitly identified model name is not a measured physical quantity.','equivalence')
# Subject binding: lamp and motor may share units without sharing a predicate.
for k,(p,q,state) in enumerate([(900,1500,'pass'),(1100,100,'fail'),(1000,1200,'pass'),(1001,999,'fail')],1):
    pair('component_binding',k,'Motor power not exceeding 1,000 W.',
         f'The motor power is {p} W. The lamp power is {q} W.',
         f'The lamp power is {q} W. The motor power is {p} W.',state,state,
         'Only motor power is constrained; clause order cannot change the binding.','equivalence')
# Own mass and lifting capacity are not interchangeable.
for k,(mass,load,state) in enumerate([(40,500,'pass'),(40,600,'fail'),(600,500,'pass'),(600,600,'fail')],1):
    pair('mass_capacity',k,'Lifting capacity not more than 550 kg.',
         f'The lifting capacity is {load} kg. The jack weighs {mass} kg.',
         f'The jack weighs {mass} kg. Its lifting capacity is {load} kg.',state,state,
         'The predicate refers to lifted mass, not the mass of the jack.','equivalence')
# Comparative facts are sets of possible values, not point assertions.
comparatives=[('The weight is less than 10 kg.','The weight is more than 10 kg.','pass','fail'),
 ('The weight is not more than 10 kg.','The weight is at least 10 kg.','pass','unknown'),
 ('The weight is below 9 kg.','The weight is from 9 to 11 kg.','pass','unknown'),
 ('The weight is 10 kg.','The weight is more than 11 kg.','pass','fail')]
for k,(a,b,ga,gb) in enumerate(comparatives,1):
    pair('comparative_facts',k,'Weight not more than 10 kg.',a,b,ga,gb,
         'Pass requires every value consistent with the fact to satisfy the ceiling; straddling intervals are unknown.')
# Inconsistent reports have no priority unless the text expressly assigns one.
for k,(a,b,ga,gb) in enumerate([
 ('The motor power is 900 W.','The specification states 900 W; a second report states 1,100 W.','pass','unknown'),
 ('The motor power is 1,100 W.','The specification states 1,100 W; a second report states 900 W.','fail','unknown'),
 ('The specification states 900 W; a second report states 950 W.','The specification states 900 W; a second report states 1,100 W.','pass','unknown'),
 ('The specification states 1,100 W; a second report states 1,200 W.','The specification states 1,100 W; a second report states 900 W.','fail','unknown')],1):
    pair('conflicting_reports',k,'Motor power not exceeding 1,000 W.',a,b,ga,gb,
         'Conflicting possible readings produce unknown if they disagree on compliance; uniformly inside/outside readings retain that state.')
# Exact unit equivalences, including units unsupported by the frozen engine.
for k,(rule,a,b,state,why) in enumerate([
 ('Weight not more than 1 kg.','The weight is 1 kg.','The weight is 1,000 g.','pass','1 kg = 1000 g.'),
 ('Lifting capacity not more than 550 kg.','The lifting capacity is 2721.55422 kg.','The lifting capacity is 6,000 lb.','fail','1 international avoirdupois lb = 0.45359237 kg exactly.'),
 ('Length not more than 25.4 mm.','The length is 25.4 mm.','The length is 1 inch.','pass','1 international inch = 25.4 mm exactly.'),
 ('Power not exceeding 1,000 W.','The power is 1,001 W.','The power is 1.001 kW.','fail','1 kW = 1000 W.')],1):
    pair('unit_equivalence',k,rule,a,b,state,state,why,'equivalence')
for k,(a,b,ga,gb) in enumerate([
 ('The fabric areal mass is 206 g/m2.','The fabric areal mass is 205 g/m2.','pass','fail'),
 ('The fabric areal mass is 500 g/m2.','The fabric areal mass is 501 g/m2.','pass','fail'),
 ('The fabric areal mass is 300 g/m2.','The fabric areal mass is 0.3 kg/m2.','pass','pass'),
 ('The fabric areal mass is 0.6 kg/m2.','The fabric areal mass is 600 g/m2.','fail','fail')],1):
    pair('compound_units',k,'Fabric areal mass at least 206 g/m2 but not more than 500 g/m2.',a,b,ga,gb,
         'Areal mass cannot be interpreted as ordinary mass. Both inclusive endpoints apply.','equivalence' if ga==gb else 'decisive_change')
for k,(x,y,ga,gb) in enumerate([(4,4.001,'fail','pass'),(7.999,8,'pass','fail'),(3.999,4,'fail','fail'),(6,7,'pass','pass')],1):
    pair('two_sided_bounds',k,'Weight more than 4 kg but less than 8 kg.',f'The weight is {x} kg.',f'The weight is {y} kg.',ga,gb,
         'The admissible interval is (4, 8) kg; both endpoints are excluded.','decisive_change' if ga!=gb else 'same_state_control')
for k,(a,b,ga,gb) in enumerate([
 ('Length is 80 cm; width is 40 cm; height is 24 cm.','Length is 82 cm; width is 40 cm; height is 24 cm.','pass','fail'),
 ('Length is 80 cm; width is 40 cm; height is 24 cm.','Length is 80 cm; width is 42 cm; height is 24 cm.','pass','fail'),
 ('Length is 80 cm; width is 40 cm; height is 24 cm.','Height is 24 cm; length is 80 cm; width is 40 cm.','pass','pass'),
 ('Length is 80 cm; width is 40 cm; height is 26 cm.','Height is 26 cm; length is 80 cm; width is 40 cm.','fail','fail')],1):
    pair('dimension_binding',k,'Length not more than 81 cm, width not more than 41 cm, and height not more than 25 cm.',a,b,ga,gb,
         'Three named dimensions are jointly required; facts are bound by dimension name, not nearest number.','equivalence' if ga==gb else 'decisive_change')
for k,(a,b,ga,gb) in enumerate([
 ('Width is 6 cm; height is 8 cm.','Width is 6 cm; height is 11 cm.','pass','fail'),
 ('Width is 4 cm; height is 11 cm.','Width is 6 cm; height is 11 cm.','pass','fail'),
 ('Width is 4 cm; height is unspecified.','Width is 6 cm; height is unspecified.','pass','unknown'),
 ('Width is unspecified; height is 8 cm.','Width is unspecified; height is 11 cm.','pass','unknown')],1):
    pair('disjunction',k,'Width not over 5 cm or height not over 10 cm.',a,b,ga,gb,
         'A true branch satisfies OR; both false branches refute it; a false branch plus a missing branch is unknown.')
for k,(a,b,ga,gb) in enumerate([
 ('The item weighs 8 kg and is not battery-powered.','The item weighs 8 kg and is battery-powered.','pass','fail'),
 ('The item weighs 7 kg and is battery-powered.','The item weighs 7.1 kg and is battery-powered.','pass','fail'),
 ('The item weighs 6 kg; battery status is unspecified.','The item weighs 8 kg; battery status is unspecified.','pass','unknown'),
 ('The item weighs 10 kg and is not battery-powered.','The item weighs 10.1 kg and is not battery-powered.','pass','fail')],1):
    pair('nested_exception',k,'Weight not over 10 kg, except that battery-powered items must weigh not over 7 kg.',a,b,ga,gb,
         'If battery-powered use the 7 kg limit, otherwise use 10 kg. Missing battery status is resolvable only if both branches agree.')
for k,(a,b,ga,gb) in enumerate([
 ('The weight is 9 kg with an uncertainty of plus or minus 0.5 kg.','The weight is 10 kg with an uncertainty of plus or minus 0.5 kg.','pass','unknown'),
 ('The weight is 11 kg with an uncertainty of plus or minus 0.5 kg.','The weight is 10 kg with an uncertainty of plus or minus 0.5 kg.','fail','unknown'),
 ('The weight is 9 kg.','The weight is approximately 9 kg, with no tolerance specified.','pass','unknown'),
 ('The weight is 11 kg.','The weight is approximately 11 kg, with no tolerance specified.','fail','unknown')],1):
    pair('measurement_uncertainty',k,'Weight not more than 10 kg.',a,b,ga,gb,
         'A specified tolerance defines a closed interval; an unbounded approximation does not prove either side of the threshold.')

assert len(rows)==96 and len({r['case_id'] for r in rows})==96
assert all(r['gold'] in ['pass','fail','unknown'] for r in rows)
dest=R/'constructed_diagnostics.jsonl'
dest.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf8')
summary={'n':len(rows),'families':dict(Counter(r['mechanism'] for r in rows)),
         'gold':dict(Counter(r['gold'] for r in rows)),'pair_types':dict(Counter(r['pair_type'] for r in rows)),
         'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'design':'12 purposive failure mechanisms x 4 pairs x 2 variants; authored independently of engine outputs; not a random sample of statutory language',
         'status':'constructed AI-authored diagnostic references; independent AI review required; no human expert validation',
         'label_semantics':'pass=all admissible values satisfy rule; fail=all admissible values violate rule; unknown=missing, ambiguous, or straddling evidence',
         'scope':'Only stated predicates; nonnumeric product-category criteria assumed satisfied. No administrative labels.',
         'design_erratum':'After the first frozen-engine diagnostic run, the 8 component-binding rules were changed from The motor power must not exceed 1,000 W. to Motor power not exceeding 1,000 W. to remove a known unsupported-grammar confound. Facts and reference states were unchanged; initial design and predictions are retained. This is disclosed post-run design repair, not a pre-run claim.'}
(R/'constructed_diagnostics_design.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
