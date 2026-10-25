"""Enumerate only declared local interpretation options in the 58 safe cases.

This is conditional sensitivity of an AI audit, not a range of legal truth.
Direct relations are fixed; unresolved insufficient evidence stays unknown.
No administrative y values are read or optimized.
"""
from itertools import product
from collections import Counter
import json
from build_source_audit import OUT,readl,dump

def aggregate(states):
    ss=[s for s in states if s!='not_applicable']
    if 'refute' in ss:return 'refute'
    if all(s=='support' for s in ss):return 'support'
    return 'unknown'

def choices(row):
    base=row['strict_full_source_state']
    opts=[{'policy':'withhold_interpretation','state':base}]
    if row['reference_tier'] in ['interpretive','disputed']:
        opts += [{'policy':x['policy'],'state':x['state']} for x in row['interpretation_options']]
    # Insufficient attributes cannot be promoted by an optional party-acceptance
    # choice in this restricted analysis, and direct states cannot be changed.
    return opts

def main():
    rows=readl(OUT/'condition_audit_long.jsonl');by={r['condition_key']:r for r in rows}
    cases=[c for c in readl(OUT/'case_audit.jsonl') if c['safe_flat_conjunction']]
    assert len(cases)==58
    enumerated=[]
    for c in cases:
        rr=[by[k] for k in c['condition_keys']];arrays=[choices(r) for r in rr]
        combos=[]
        for selections in product(*arrays):
            combos.append({'selected_policies':{r['condition_key']:x['policy'] for r,x in zip(rr,selections)},
              'state':aggregate([x['state'] for x in selections])})
        enumerated.append({'case_id':c['case_id'],'possible_states':sorted({x['state'] for x in combos}),
          'enumerated_combinations':len(combos),'combinations':combos})
    # Marginal case-count envelopes are NOT presented as one attainable joint
    # result or evidence that shared legal terms can be interpreted independently.
    bounds={s:{'necessarily_this_state':sum(x['possible_states']==[s] for x in enumerated),
      'possibly_this_state':sum(s in x['possible_states'] for x in enumerated)} for s in ['support','refute','unknown']}
    # Two explicitly described, shared decision packages. They are illustrations
    # of the listed policies, not adjudicated or exhaustive legal doctrines.
    shared={r['condition_key']:'retain_original_mapping' for r in rows if any(x['policy']=='retain_original_mapping' for x in choices(r))}
    technical={**shared,
      'H330938_1:c1':'single_pole_system','H330938_1:c3':'conducting_core_only',
      'H323452_1:c1':'cursor_control_is_necessary','H322923_1:c3':'stated_household_shopping_use_suffices',
      'H332948_1:c4':'explicit_marketing_use_suffices','H332948_3:c4':'principal_marketed_use_controls',
      'H318593_1:c2':'predominant_base_metal','H340899_1:c2':'commercial_floor_upright_category',
      'H333371_1:c2':'laboratory_priority','N327114:c3':'peak_output'}
    alternative={**technical,'H330938_1:c3':'all_materials','H332948_3:c4':'any_advertised_use_suffices',
      'H340899_1:c2':'physical_upright_orientation','H333371_1:c2':'party_priority','N327114:c3':'nominal_output'}
    configs=[('strict_withhold',{}),('declared_technical_scope_lab_peak',technical),('declared_alternative_material_use_party_nominal',alternative)]
    comparisons=[]
    for name,settings in configs:
        out=[];used={}
        for c in cases:
            states=[]
            for k in c['condition_keys']:
                opts={x['policy']:x['state'] for x in choices(by[k])};p=settings.get(k,'withhold_interpretation')
                assert p in opts,(k,p)
                states.append(opts[p])
                if p!='withhold_interpretation':used[k]=p
            out.append({'case_id':c['case_id'],'state':aggregate(states)})
        comparisons.append({'name':name,'overrides':used,'counts':dict(Counter(x['state'] for x in out)),'cases':out})
    data={'scope':'58 safe outer-conjunction cases; full-public-source direct attributes fixed',
      'not_in_scope':'15 unresolved-logic cases; legal completeness; arbitrary unseen interpretations',
      'rules':['Every condition can retain strict unknown; only explicitly listed interpretive/disputed options may change it.',
      'Direct states fixed. Insufficient conditions remain unknown unless direct source recovery already resolved them.',
      'No-option interpretive conditions remain unknown. Administrative outcomes are not criteria.',
      'Per-case sets are local logical sensitivity, not independent probabilities or simultaneously coherent legal choices.',
      'Marginal count envelopes do not form a joint realizable total; explicit packages provide actual joint totals.'],
      'case_n':58,'cases':enumerated,'marginal_count_envelopes':bounds,'explicit_policy_packages':comparisons}
    dump(OUT/'policy_sensitivity.json',data)
    lines=['# Declared-interpretation sensitivity','',
      'This computation enumerates the options actually listed in the source audit for the 58 cases with safe outer conjunction. It does not enumerate all reasonable legal interpretations. Direct full-source properties remain fixed. Unresolved insufficient evidence remains unknown, including party-attributed specifications that lack independent support. Interpretive conditions with no listed option remain unknown. Each optional mapping can also be withheld. No administrative outcome is used to select a mapping.','',
      '| State | Cases necessarily in state | Cases that can enter state |','|---|---:|---:|']
    for s,b in bounds.items():lines.append(f'| {s} | {b["necessarily_this_state"]} | {b["possibly_this_state"]} |')
    lines+=['','These are **marginal envelopes**, not one jointly attainable result. They neither assume that shared legal terms can be independently redefined by case nor imply probabilities. For actual simultaneous comparisons, the following fully specified packages are evaluated; the machine-readable file records every override and every case result. The packages are diagnostic choices, not claims to coherent authoritative legal doctrine.','',
     '| Explicit package | Support | Refute | Unknown |','|---|---:|---:|---:|']
    for c in comparisons:lines.append('| '+c['name']+' | '+' | '.join(str(c['counts'].get(s,0)) for s in ['support','refute','unknown'])+' |')
    lines+=['','The technical package accepts a monopolar-system description and conducting-core material scope, cursor-control necessity, explicit household-shopping use, predominantly-steel composition, a commercial upright-vacuum category, laboratory priority for glove composition and peak motor output. The alternative package changes material scope, any-advertised-use versus principal use, upright orientation, party-versus-laboratory priority, and nominal-versus-peak output. Other unresolved definitions remain unresolved. H330938 topology and material policies are separate switches. N327114 retains two discrete ratings; it is never represented as a continuous uncertainty interval.','',
      'Only the cases below can change aggregate state under the listed local choices:','']
    for c in enumerated:
        if len(c['possible_states'])>1:lines.append('- '+c['case_id']+': '+', '.join(c['possible_states'])+'.')
    (OUT/'policy_sensitivity.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'bounds':bounds,'packages':[{k:v for k,v in c.items() if k in ['name','counts']} for c in comparisons]},indent=2))

if __name__=='__main__':main()
