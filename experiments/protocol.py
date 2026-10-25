"""Evidence-audit interface v1, independent development and qualification inputs.

No administrative disposition or reference evidence states enter model prompts.
This is a checklist-supplied diagnostic, not automatic rule extraction.
"""
import json

STATES=['supported','refuted','unknown']
POLICY='''Audit whether the numbered facts establish the numbered requirements for the specified target. Use only these facts, not likely properties or background expectations. A requirement can be negative: for "no connectors", explicit absence supports it, explicit presence refutes it, and silence leaves it unknown.
For each requirement return supported if the facts establish it, refuted if the facts explicitly contradict it, and unknown if neither. Keep attributes attached to the named product, component, operating state, and measurement basis. Facts about a different object do not establish or contradict the target requirement. Do not convert a model identifier into a physical value. Evidence must be a list of supplied fact IDs; unknown has an empty list.
The decision is refuted when ANY mandatory requirement is refuted, even if another requirement is unknown. Otherwise it is supported only when ALL requirements are supported, and unknown otherwise. Request the IDs of unknown requirements only when the decision is unknown. Request nothing after a decisive refutation, and do not request an already established property. The supplied checklist is conjunctive; it is a provided task input, not a hidden answer.
Return only the JSON object specified below. There is no need to explain the answer outside that object.'''

def prompt(case):
    clean={k:case[k] for k in ['target','rule_text','conditions','facts']}
    return POLICY+'\n\nINPUT:\n'+json.dumps(clean,ensure_ascii=False)+'\n\nJSON FORMAT:\n'+json.dumps({'conditions':[{'id':c['id'],'state':'supported|refuted|unknown','evidence':[]} for c in case['conditions']],'decision':'supported|refuted|unknown','requests':[]})

def schema(case):
    cids=[c['id'] for c in case['conditions']];fids=[f['id'] for f in case['facts']]
    # The grammar constrains syntax/vocabulary but not factual choices, counts,
    # condition coverage, or evidence validity. These remain separately scored.
    evidence={'type':'array','items':{'type':'string','enum':fids},'maxItems':len(fids)} if fids else {'type':'array','maxItems':0}
    return {'type':'object','properties':{'conditions':{'type':'array','items':{'type':'object','properties':{'id':{'type':'string','enum':cids},'state':{'type':'string','enum':STATES},'evidence':evidence},'required':['id','state','evidence'],'additionalProperties':False},'minItems':1,'maxItems':len(cids)},'decision':{'type':'string','enum':STATES},'requests':{'type':'array','items':{'type':'string','enum':cids},'maxItems':len(cids)}},'required':['conditions','decision','requests'],'additionalProperties':False}

def aggregate(states):
    return 'refuted' if 'refuted' in states else ('unknown' if 'unknown' in states else 'supported')

def parse(raw,case):
    x=json.loads(raw);assert set(x)=={'conditions','decision','requests'}
    assert x['decision'] in STATES
    expected={c['id'] for c in case['conditions']};fids={f['id'] for f in case['facts']}
    assert isinstance(x['conditions'],list) and isinstance(x['requests'],list)
    ids=[c['id'] for c in x['conditions']];assert len(ids)==len(set(ids))
    assert set(ids)<=expected
    for c in x['conditions']:
        assert set(c)=={'id','state','evidence'} and c['state'] in STATES
        assert isinstance(c['evidence'],list) and set(c['evidence'])<=fids
    assert len(x['requests'])==len(set(x['requests'])) and set(x['requests'])<=expected
    return x
