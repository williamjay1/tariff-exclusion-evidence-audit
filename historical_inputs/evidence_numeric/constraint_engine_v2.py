"""Post hoc general parser repairs. Not an independently validated new model.

The frozen engine is loaded into a separate in-memory module, never edited.
Repairs: identifier boundaries; lb/inch conversion; comparative fact intervals;
postposed 'or less'; mass/capacity lexical binding; explicit motor/lamp subjects.
Unsupported logical scope remains unknown. No case IDs or reference fields read.
Trace spans refer to explicitly returned normalized texts, not original offsets.
"""
from pathlib import Path
from decimal import Decimal
import re,importlib.util
OLD=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('engine_v2_private_base',OLD/'scripts/constraint_engine.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
base.NUM=r'(?<![A-Za-z0-9])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'
base.UNIT=r'(?:pounds?|lbs?|inches|inch|in|'+base.UNIT[3:-1]+r')'
base.MAPPING.update({'lb':('mass',Decimal('453.59237'),'g'),'lbs':('mass',Decimal('453.59237'),'g'),
 'pound':('mass',Decimal('453.59237'),'g'),'inch':('length',Decimal('25.4'),'mm'),'inches':('length',Decimal('25.4'),'mm'),'in':('length',Decimal('25.4'),'mm')})
oldattribute=base.attribute;oldparse=base.parse_constraints;oldextract=base.extract_facts
def normal(text):
    text=re.sub(r'\bmust not exceed\b','not exceeding',text,flags=re.I)
    text=re.sub(r'\bnot longer than\b','not more than',text,flags=re.I)
    text=re.sub(r'\bbelow\b','less than',text,flags=re.I)
    text=re.sub(r'\babove\b','more than',text,flags=re.I)
    return text
def local(text,pos):
    left=0;right=len(text)
    for m in re.finditer(r';|(?<!\d)\.|\.(?!\d)',text):
        if m.end()<=pos:left=m.end()
        elif m.start()>pos:right=m.start();break
    return text[left:right],pos-left
def attribute(unit,text,pos):
    norm=base.normalize_unit(unit)
    if norm and norm[0]=='mass':
        sentence,rel=local(text,pos);prefix=sentence[:rel]
        cues=list(re.finditer(r'\b(?:lifting capacity|capacity|load|weight|weighs|weighing)\b',prefix,re.I))
        if cues:
            cue=cues[-1][0].lower();return 'mass_capacity' if cue in ['lifting capacity','capacity','load'] else 'weight'
    return oldattribute(unit,text,pos)
base.attribute=attribute
def subject(text,pos):
    s,p=local(text,pos)
    cues=list(re.finditer(r'\b(motor|lamp)\s+power\b',s[:p],re.I))
    return cues[-1][1].lower() if cues else None
def parse(text):
    cs=oldparse(text)
    for m in re.finditer(rf'(?P<v>{base.NUM})\s*(?P<u>{base.UNIT})\s+or less',text,re.I):
        if any(c['span'][0]<=m.start()<c['span'][1] for c in cs):continue
        dim,scale,unit=base.normalize_unit(m['u'])
        cs.append({'attribute':attribute(m['u'],text,m.start()),'dimension':dim,'unit':unit,
          'lower':None,'lower_inclusive':None,'upper':base.number(m['v'])*scale,'upper_inclusive':True,'quote':m[0],'span':[m.start(),m.end()]})
    for c in cs:c['subject']=subject(text,c['span'][0])
    return cs
def facts(text):
    fs=oldextract(text);cs=parse(text)
    for c in cs:
        # Only actual comparative fact assertions become intervals; the generic
        # old parser already rejects unsupported compound units.
        a,b=c['span'];fs=[f for f in fs if not (a<=f['span'][0]<b)]
        fs.append({'attribute':c['attribute'],'dimension':c['dimension'],'unit':c['unit'],
          'lower':c['lower'] if c['lower'] is not None else Decimal('-Infinity'),
          'upper':c['upper'] if c['upper'] is not None else Decimal('Infinity'),
          'lower_inclusive':c['lower_inclusive'] if c['lower'] is not None else False,
          'upper_inclusive':c['upper_inclusive'] if c['upper'] is not None else False,
          'quote':text[a:b],'span':[a,b],'from_comparative':True})
    tolerance=rf'(?P<v>{base.NUM})\s*(?P<u>{base.UNIT})\s+with an uncertainty of plus or minus\s*(?P<t>{base.NUM})\s*(?P<tu>{base.UNIT})'
    for m in re.finditer(tolerance,text,re.I):
        n=base.normalize_unit(m['u']);tn=base.normalize_unit(m['tu'])
        if n[0]!=tn[0]:continue
        value=base.number(m['v'])*n[1];tol=base.number(m['t'])*tn[1]
        fs=[f for f in fs if not (m.start()<=f['span'][0]<m.end())]
        fs.append({'attribute':attribute(m['u'],text,m.start()),'dimension':n[0],'unit':n[2],
          'lower':value-tol,'upper':value+tol,'quote':m[0],'span':[m.start(),m.end()],
          'from_explicit_tolerance':True})
    for m in re.finditer(rf'\b(?:approximately|about)\s*(?P<v>{base.NUM})\s*(?P<u>{base.UNIT})(?![A-Za-z])',text,re.I):
        # A dropped approximate measurement must not let another exact reading
        # become a false certificate. Without a supplied tolerance, preserve U.
        n=base.normalize_unit(m['u'])
        fs=[f for f in fs if not (m.start()<=f['span'][0]<m.end())]
        fs.append({'attribute':attribute(m['u'],text,m.start()),'dimension':n[0],'unit':n[2],
          'lower':Decimal('-Infinity'),'upper':Decimal('Infinity'),'lower_inclusive':False,'upper_inclusive':False,
          'quote':m[0],'span':[m.start(),m.end()],'from_unspecified_approximation':True})
    for f in fs:
        f.setdefault('lower_inclusive',True);f.setdefault('upper_inclusive',True)
        f['subject']=subject(text,f['span'][0])
    return fs
def interval(c,f):
    lo,hi=f['lower'],f['upper'];li=f.get('lower_inclusive',True);ui=f.get('upper_inclusive',True)
    lower_ok=c['lower'] is None or lo>c['lower'] or (lo==c['lower'] and (c['lower_inclusive'] or not li))
    upper_ok=c['upper'] is None or hi<c['upper'] or (hi==c['upper'] and (c['upper_inclusive'] or not ui))
    if lower_ok and upper_ok:return 'pass'
    if c['lower'] is not None and (hi<c['lower'] or hi==c['lower'] and (not c['lower_inclusive'] or not ui)):return 'fail'
    if c['upper'] is not None and (lo>c['upper'] or lo==c['upper'] and (not c['upper_inclusive'] or not li)):return 'fail'
    return 'unknown'
def verify_numeric(original_facts,original_rule):
    ft,rt=normal(original_facts),normal(original_rule)
    old=base.verify_numeric(ft,rt);cs=parse(rt);fs=facts(ft);trace=[]
    for c in cs:
        ms=[f for f in fs if f['attribute']==c['attribute'] and f['dimension']==c['dimension'] and (c['subject'] is None or c['subject']==f['subject'])]
        states=[interval(c,f) for f in ms]
        # All admissible reported intervals must agree; inconsistent threshold
        # states are unknown. This does not assign priority to one report.
        state=states[0] if states and len(set(states))==1 else 'unknown'
        trace.append({'constraint':c,'candidates':ms,'candidate_states':states,'state':state})
    scope=re.split(r'\(\s*(?:as )?described',rt,flags=re.I)[0]
    raw=list(re.finditer(rf'(?:\$\s*{base.NUM}|{base.NUM}\s*{base.UNIT})(?![A-Za-z])',scope,re.I))
    unparsed=[m[0] for m in raw if not any(c['span'][0]<=m.start()<c['span'][1] for c in cs)]
    for m in re.finditer(rf'{base.OPS}\s*(?:\$\s*)?{base.NUM}',scope,re.I):
        if not any(c['span'][0]<=m.start()<c['span'][1] for c in cs):unparsed.append(m[0])
    unsupported_logic=bool(re.search(r'\b(?:except|unless)\b',scope,re.I)) or len(cs)>1 and bool(re.search(r'\bor\b(?!\s+(?:more|less))',scope[min(c['span'][0] for c in cs):max(c['span'][1] for c in cs)],re.I))
    states=[t['state'] for t in trace]
    state='unknown' if unsupported_logic else 'fail' if 'fail' in states else 'unknown' if 'unknown' in states or unparsed else 'pass' if states else 'not_parsed'
    return {'state':state,'trace':trace,'unparsed_quantities':unparsed,'unsupported_logic':unsupported_logic,
      'normalized_facts':ft,'normalized_rule':rt,'version':'posthoc_v2_general_parser_repair',
      'limitation':'No general legal semantics, compound-unit algebra, all-product quantifier extraction, or external heading interpretation.'}
if __name__=='__main__':
    # Development controls are transparent and are not held-out evaluation data.
    assert verify_numeric('Model AB99999W. Motor power is 900 W.','Motor power not exceeding 1000 W.')['state']=='pass'
    assert verify_numeric('Motor power is 900 W. Lamp power is 1500 W.','Motor power not exceeding 1000 W.')['state']=='pass'
    assert verify_numeric('The lifting capacity is 6000 lb.','Lifting capacity not more than 550 kg.')['state']=='fail'
    assert verify_numeric('Weight is less than 10 kg.','Weight less than 10 kg.')['state']=='pass'
    assert verify_numeric('Weight is more than 10 kg.','Weight not more than 10 kg.')['state']=='fail'
    assert verify_numeric('Weight is 10 kg or less.','Weight not more than 10 kg.')['state']=='pass'
    assert verify_numeric('Weight is approximately 9 kg.','Weight not more than 10 kg.')['state']=='unknown'
    assert verify_numeric('Weight is 10 kg with an uncertainty of plus or minus 0.5 kg.','Weight not more than 10 kg.')['state']=='unknown'
    print('Post hoc v2 development controls passed.')
