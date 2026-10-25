"""Summarise complete frozen z experiments, including all functional failures."""
import datetime,hashlib,json,statistics,subprocess,sys
from pathlib import Path
from protocol import prompt
from run_evidence_audit import DIRECT
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'outputs'
read=lambda p:[json.loads(s) for s in p.read_text(encoding='utf8').splitlines()]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
datasets=['qualification_cases','controlled_cases','source_recovery_cases']
report={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model':'Qwen3-14B Q4_K_M',
 'status':'complete','scope':'Evidence-state diagnostic, not administrative disposition or unseen legal generalization.',
 'datasets':{},'source_selection':'4 isolated conditions, 3 rulings, 8 endpoints; no whole-case legal labels',
 'qualification_caveat':'Q_negation_3 correctly returned unknown but omitted the required request; this functional failure is retained.',
 'historical_guard_diagnostic':json.loads((ROOT/'old_guard_diagnostic.json').read_text(encoding='utf8'))}
report['completed_sessions']=[{'file':p.name,'sha256':sha(p),**{k:v for k,v in json.loads(p.read_text(encoding='utf8')).items() if k in ['created_utc','pid','load_seconds','wall_seconds','memory_before','memory_after','runner_sha256','protocol_sha256']}} for p in sorted(OUT.glob('qwen14_*_session.json'))]
report['timing_interpretation']='Wall-clock elapsed seconds, CPU-only six-thread execution, uncontrolled shared-host load including external CPU contention during formal checklist inference; not a fair efficiency ranking or isolated speed benchmark.'
report['development_analysis']=json.loads((OUT/'qwen14_development_cases_functional_analysis.json').read_text(encoding='utf8'))
lines=['# Evidence audit experiment results','',
 'This report concerns agreement with explicit, AI-assisted diagnostic references. The controlled cases are purpose-built synthetic examples anchored to selected source clauses. The source-restoration cases evaluate isolated attributes, not full legal eligibility. No new adjudications, expert gold, or population prevalence are claimed.','',
 'The same local Qwen3-14B Q4_K_M configuration passed the frozen independent qualification gate in both interfaces. Both obtained 24/24 case states; the checklist obtained 27/27 condition states. All outputs were valid, and there were no unsupported affirmative decisions. One unknown item omitted its required information request (7/8 necessary requests), showing that qualification did not imply perfect downstream behavior.','',
 'For the formal controlled comparison, both interfaces receive the same complete clause and numbered facts. The checklist additionally duplicates the clause as numbered conditions and requests condition states, fact citations and follow-up IDs. This joint representation/output change does not isolate an aggregation effect. The every-granule quantifier and frame-species scope are supplied interpretations within a two-condition diagnostic, not verified interpretations of complete legal provisions.','']
for name in datasets:
    source=ROOT/(name+'.jsonl');data=read(source);expected={r['case_id']:r for r in data}
    result=json.loads((OUT/f'qwen14_{name}_functional_analysis.json').read_text(encoding='utf8'))
    d={'n':len(data),'input_sha256':sha(source),'analysis':result,'arms':{}}
    for kind in ['direct','checklist']:
        path=OUT/f'qwen14_{name}_{kind}.jsonl';rows=read(path)
        assert len(rows)==len(data) and {r['case_id'] for r in rows}==set(expected)
        for r in rows:
            case=expected[r['case_id']]
            reconstructed=prompt(case) if kind=='checklist' else DIRECT+'\n\nINPUT:\n'+json.dumps({k:case[k] for k in ['target','rule_text','facts']},ensure_ascii=False)
            assert reconstructed==r['user_prompt'],'Prompt/input integrity mismatch'
        d['arms'][kind]={'sha256':sha(path),'n':len(rows),'request_seconds':sum(r.get('seconds',0) for r in rows),
          'median_request_seconds':statistics.median(r.get('seconds',0) for r in rows),
          'max_input_tokens':max(r.get('input_tokens',0) for r in rows),
          'output_tokens':sum(r.get('output_tokens',0) or 0 for r in rows),
          'invalid':sum(not r.get('valid') for r in rows),'incomplete':sum(not r.get('complete_condition_ids',True) for r in rows),
          'truncation':sum(bool(r.get('truncated') or r.get('stopped_limit')) for r in rows),
          'prompt_reconstruction':'all exact; expected states/source metadata absent from model input'}
    report['datasets'][name]=d
    if name=='qualification_cases':continue
    direct=result['reports']['direct'];check=result['reports']['checklist'];ds=direct['overall'];cs=check['overall']
    lines += [f'## {name}', '',
      f'The direct interface matched {ds["decision_correct"]}/{len(data)} reference states. The checklist overall decision matched {cs["decision_correct"]}/{len(data)}, and deterministic aggregation of its condition states matched {cs["aggregation_correct"]}/{len(data)}. Condition-state agreement was {cs["condition_correct"]}/{cs["condition_n"]}. Unsupported affirmative case conclusions were {ds["unsupported_case_affirmations"]} in direct and {cs["unsupported_case_affirmations"]} in checklist. As an additional descriptive check, unsupported case refutations were {ds["unsupported_case_refutations"]} in direct and {cs["unsupported_case_refutations"]} in checklist; the checklist had {cs["unsupported_condition_refutations"]} unsupported refuted conditions. Complete reference-by-prediction matrices are retained in the JSON summary.','',
      f'Gap localization had {cs["gap_localization"]["tp"]} true positives, {cs["gap_localization"]["fp"]} false positives and {cs["gap_localization"]["fn"]} missed gaps. Required follow-up had {cs["requests"]["tp"]} correctly requested conditions, {cs["requests"]["missing_necessary"]} missing necessary requests and {cs["requests"]["unnecessary"]} unnecessary requests. Exact request sets matched in {cs["requests"]["exact_case_sets"]}/{len(data)} inputs. These metrics are not applicable to the decision-only direct interface.','',
      f'Acceptable citation-ID sets matched {cs["evidence_id_acceptable"]["correct"]}/{cs["evidence_id_acceptable"]["scored"]} conditions, including {cs["evidence_id_acceptable"]["determinate_correct"]}/{cs["evidence_id_acceptable"]["determinate_scored"]} determinate conditions. This is fact-ID retrieval agreement, not expert-validated legal entailment.','',
      '| Controlled relationship | Direct: both endpoints correct | Checklist: both endpoints correct |',
      '|---|---:|---:|']
    for op,v in direct.get('pairs',{}).get('by_operation',{}).items():
        cv=check['pairs']['by_operation'][op]
        lines.append(f'| {op} | {v["success"]}/{v["n"]} | {cv["success"]}/{cv["n"]} |')
    lines+=['', 'Pair success requires both endpoint states to be correct and the required invariance/change. Shared endpoints are retained as dependent diagnostics; no population confidence interval is attached to this selected domain.','',
      f'Recorded request time was {d["arms"]["direct"]["request_seconds"]:.3f} s for direct and {d["arms"]["checklist"]["request_seconds"]:.3f} s for checklist. These are actual request times on the available CPU host; model loading and other runs are recorded separately in session files.','']
    failures=[]
    for kind in ['direct','checklist']:
        byid={r['case_id']:r for r in read(OUT/f'qwen14_{name}_{kind}.jsonl')}
        for rr in result['case_records'][kind]:
            failed=not rr['decision_correct'] or (kind=='checklist' and (rr['condition_correct']!=rr['condition_n'] or not rr['request_set_correct'] or rr['evidence_exact_n']!=rr['evidence_scored_n']))
            if failed:failures.append({'kind':kind,'case_id':rr['case_id'],'reference':result['effective_references'][rr['case_id']],'actual':byid[rr['case_id']].get('parsed'),'functional_record':rr})
    d['all_functional_failures']=failures
    lines += [f'All {len(failures)} arm-by-input functional failure records are retained in experiment_final_summary.json, including cases whose whole-input decision is correct.','']
    if name=='source_recovery_cases':
        lookup={kind:{r['case_id']:r for r in result['case_records'][kind]} for kind in ['direct','checklist']}
        d['restoration_transitions']=[]
        lines += ['| Isolated condition | Direct before → after | Checklist before → after | Reference |','|---|---|---|---|']
        for pair in read(ROOT/'source_recovery_pairs.jsonl'):
            transition={'condition_key':pair['family'],'left':pair['left'],'right':pair['right'],'reference':['unknown','supported']}
            for kind in ['direct','checklist']:
                transition[kind]=[lookup[kind][pair[k]]['decision'] or 'invalid' for k in ['left','right']]
            d['restoration_transitions'].append(transition)
            lines.append(f'| {pair["family"]} | {" → ".join(transition["direct"])} | {" → ".join(transition["checklist"])} | unknown → supported |')
        lines += ['','All four transitions are shown, including the motor condition whose before-reference depends on the strict explicit-attribute policy. The motor condition remained unknown in direct output and refuted in checklist output after its explicit supporting source sentence was added. The historical before-state policy does not explain away this after-restoration failure; the responses do not establish its internal cause.','']
    if name=='controlled_cases':
        alternatives={tag:json.loads((OUT/f'qwen14_{name}_functional_analysis_{tag}.json').read_text(encoding='utf8')) for tag in ['frozen_reference','excluding_frame_species']}
        d['reference_sensitivity']=alternatives
        orig=alternatives['frozen_reference']['reports']['checklist']['overall'];ex=alternatives['excluding_frame_species']['reports']['checklist']['overall']
        lines += ['Before any formal outcomes were read, a separate AI-assisted source audit found that oak/teak implies a wooden frame. The frozen input and predictions remain unchanged. A timestamped erratum changes one CF10 condition from unknown to supported and admits equivalent target-frame citations in seven inputs; all whole-input states and linked case relationships remain unchanged.','',
          f'The original frozen reference gives checklist condition agreement {orig["condition_correct"]}/{orig["condition_n"]}; the erratum gives {cs["condition_correct"]}/{cs["condition_n"]}. Excluding the entire frame family leaves 99 inputs, 198 conditions and 88 linked relationships: condition agreement {ex["condition_correct"]}/{ex["condition_n"]}. Strict refutation-with-another-unknown now has eleven cases; {cs["refutation_with_missing"]["correct_with_no_request"]}/{cs["refutation_with_missing"]["n"]} retain refutation without a request.','']
lines+=['## Scope and historical diagnostic','',
 'Source recovery tests explicit evidence availability. The motor condition was supported in the historical annotation through an implicit component inference; its before-state is unknown only under the present stricter evidence policy. The two vacuum conditions share one restored sentence. The four pairs must not be described as four corrected historical labels or four independent rulings.','',
 'The old refuted-three-to-one loss is reproduced separately: an unknown numeric status triggered referral even when the neural model was negative. The two lost cases include a 6000-pound lifting capacity against a 550-kg maximum and enclosure dimensions inconsistent with the stipulated exact dimensions. The old policy is preserved as an archival comparator, not silently repaired.','',
 'A three-request pilot with semantically unequal clause wording was stopped before predictions were inspected and is preserved under the superseded constructed_cases filenames. Formal controlled_cases outputs use the corrected common clause; no formal outcome selected the wording or model.','']
(OUT/'experiment_final_summary.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
(ROOT/'EXPERIMENT_RESULTS.md').write_text('\n'.join(lines),encoding='utf8')
subprocess.run([sys.executable,'-B',str(ROOT/'write_functional_supplement.py')],check=True)
print(json.dumps({'status':'complete','datasets':{k:v['n'] for k,v in report['datasets'].items()}}))
