"""Independent recount from raw replies, without importing the experiment evaluator."""
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,json
R=Path(__file__).resolve().parents[1];E=R/'experiments';O=E/'outputs'
STATES={'supported','refuted','unknown'}
def read(p):return [json.loads(s) for s in p.read_text(encoding='utf8').splitlines()]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def aggregate(states):
    return 'refuted' if 'refuted' in states else 'supported' if all(s=='supported' for s in states) else 'unknown'
def raw_parse(p,row,kind):
    try:
        x=json.loads(p['raw_output'])
        assert x['decision'] in STATES
        if kind=='direct':assert set(x)=={'decision'}
        else:
            assert set(x)=={'conditions','decision','requests'}
            ids=[c['id'] for c in x['conditions']]
            required={c['id'] for c in row['conditions']};facts={f['id'] for f in row['facts']}
            assert len(ids)==len(set(ids)) and set(ids)<=required
            assert isinstance(x['requests'],list) and set(x['requests'])<=required
            assert len(x['requests'])==len(set(x['requests']))
            for c in x['conditions']:
                assert set(c)=={'id','state','evidence'} and c['state'] in STATES
                assert isinstance(c['evidence'],list) and set(c['evidence'])<=facts
        syntactic=True
    except (ValueError,KeyError,TypeError,AssertionError):x=None;syntactic=False
    assert syntactic==p.get('valid',False),(row['case_id'],'recorded parse status')
    if syntactic:assert x==p['parsed']
    if not syntactic or p.get('stopped_limit') or p.get('truncated'):return None
    return x
def recount(rows,raw,kind):
    count=Counter();decisions={};total_requests=0
    for row in rows:
        key=row['case_id'];p=raw[key];ref=row['expected'];x=raw_parse(p,row,kind)
        # Whitelisted input identity, reconstructed from the saved user prompt.
        chunk=p['user_prompt'].split('\n\nINPUT:\n',1)[1].split('\n\nJSON FORMAT:',1)[0]
        supplied=json.loads(chunk)
        wanted={k:row[k] for k in (['target','rule_text','conditions','facts'] if kind=='checklist' else ['target','rule_text','facts'])}
        assert supplied==wanted,(key,'prompt identity')
        count['n']+=1
        decision=x['decision'] if x else None;decisions[key]=decision
        count['valid']+=bool(x)
        count['decision_correct']+=decision==ref['decision']
        count['unsupported_case_affirmations']+=decision=='supported' and ref['decision']!='supported'
        count['unsupported_case_refutations']+=decision=='refuted' and ref['decision']!='refuted'
        count['determinate_n']+=decision in ('supported','refuted')
        count['determinate_errors']+=decision in ('supported','refuted') and decision!=ref['decision']
        mixed=ref['decision']=='refuted' and 'unknown' in ref['states'].values()
        count['refute_missing_decision_n']+=mixed
        count['refute_missing_decision_correct']+=mixed and decision=='refuted'
        if kind=='direct':continue
        predicted={c['id']:c for c in x['conditions']} if x else {}
        expected=ref['states'];ids=set(expected)
        count['condition_n']+=len(expected)
        count['complete_condition_records']+=bool(x) and set(predicted)==ids
        count['condition_correct']+=sum(k in predicted and predicted[k]['state']==v for k,v in expected.items())
        if x and set(predicted)==ids:
            predicted_aggregate=aggregate([predicted[k]['state'] for k in expected])
            count['aggregation_correct']+=predicted_aggregate==ref['decision']
            count['overall_aggregation_consistency_n']+=1
            count['overall_matches_predicted_aggregation']+=decision==predicted_aggregate
        count['unsupported_condition_affirmations']+=sum(c['state']=='supported' and expected[k]!='supported' for k,c in predicted.items())
        count['unsupported_condition_refutations']+=sum(c['state']=='refuted' and expected[k]!='refuted' for k,c in predicted.items())
        real_gaps={k for k,v in expected.items() if v=='unknown'}
        pred_gaps={k for k,c in predicted.items() if c['state']=='unknown'}
        for metric,value in [('gap_tp',len(real_gaps&pred_gaps)),('gap_fp',len(pred_gaps-real_gaps)),('gap_fn',len(real_gaps-pred_gaps))]:count[metric]+=value
        required=set(ref['requests']);req=set(x['requests']) if x else set()
        count['request_tp']+=len(req&required);count['request_fp']+=len(req-required);count['request_fn']+=len(required-req)
        count['request_exact']+=bool(x) and req==required;total_requests+=len(req)
        count['refute_missing_n']+=mixed
        count['refute_missing_pass']+=mixed and decision=='refuted' and not req
        for cid,ev in ref.get('evidence',{}).items():
            allowed=ref.get('evidence_allowed_sets',{}).get(cid,[ev])
            valid_evidence=cid in predicted and any(set(predicted[cid]['evidence'])==set(a) for a in allowed)
            count['citation_n']+=1;count['citation_pass']+=valid_evidence
            count['determinate_citation_n']+=expected[cid]!='unknown'
            count['determinate_citation_pass']+=valid_evidence and expected[cid]!='unknown'
            count['joint_citation_state_pass']+=valid_evidence and predicted[cid]['state']==expected[cid]
    return count,decisions
def check_analysis(stem,tag='',erratum=False,exclude=False,pairs=False):
    source=E/(stem+'.jsonl');rows=read(source)
    if erratum:
        edits=json.loads((E/'annotation_erratum.json').read_text(encoding='utf8'))
        assert edits['input_sha256']==digest(source)
        lookup={r['case_id']:r for r in rows}
        for e in edits['edits']:
            gold=lookup[e['case_id']]['expected'];gold['states'][e['condition_id']]=e['state']
            gold.setdefault('evidence_allowed_sets',{})[e['condition_id']]=e['acceptable_evidence_sets']
    full_ids={r['case_id'] for r in rows}
    if exclude:rows=[r for r in rows if r['family']!='frame_species']
    suffix='_'+tag if tag else ''
    path=O/('qwen14_'+stem+'_functional_analysis'+suffix+'.json')
    analysis=json.loads(path.read_text(encoding='utf8'));results={}
    for kind in ['direct','checklist']:
        raw_rows=read(O/('qwen14_'+stem+'_'+kind+'.jsonl'))
        raw={r['case_id']:r for r in raw_rows}
        assert len(raw_rows)==len(raw)==len(full_ids) and set(raw)==full_ids
        count,decisions=recount(rows,raw,kind);reported=analysis['reports'][kind]['overall']
        for k in ['n','valid','decision_correct','unsupported_case_affirmations','unsupported_case_refutations','determinate_n','determinate_errors']:
            assert count[k]==reported[k],(stem,tag,kind,k,count[k],reported[k])
        if kind=='checklist':
            for k in ['condition_n','complete_condition_records','condition_correct','aggregation_correct','unsupported_condition_affirmations','unsupported_condition_refutations']:
                assert count[k]==reported[k],(stem,tag,k)
            for k in ['tp','fp','fn']:assert count['gap_'+k]==reported['gap_localization'][k]
            for mine,theirs in [('request_tp','tp'),('request_fp','unnecessary'),('request_fn','missing_necessary'),('request_exact','exact_case_sets')]:assert count[mine]==reported['requests'][theirs]
            for mine,theirs in [('citation_n','scored'),('citation_pass','correct'),('determinate_citation_n','determinate_scored'),('determinate_citation_pass','determinate_correct'),('joint_citation_state_pass','joint_state_and_evidence_correct')]:assert count[mine]==reported['evidence_id_acceptable'][theirs]
            assert count['refute_missing_n']==reported['refutation_with_missing']['n']
            assert count['refute_missing_pass']==reported['refutation_with_missing']['correct_with_no_request']
        if pairs:
            lookup={r['case_id']:r for r in rows};success=Counter();totals=Counter()
            for pair in read(E/'constructed_pairs.jsonl'):
                a,b=pair['left'],pair['right']
                if a not in lookup or b not in lookup:continue
                correct=decisions[a]==lookup[a]['expected']['decision'] and decisions[b]==lookup[b]['expected']['decision']
                relation=(decisions[a]==decisions[b]) if pair['expected_relation']=='same' else (decisions[a]!=decisions[b])
                totals[pair['operation']]+=1;success[pair['operation']]+=bool(correct and relation)
            assert sum(totals.values())==analysis['reports'][kind]['pairs']['n']
            assert sum(success.values())==analysis['reports'][kind]['pairs']['success']
            for op,n in totals.items():assert {'n':n,'success':success[op]}==analysis['reports'][kind]['pairs']['by_operation'][op]
        results[kind]=dict(count)
    return {'analysis':path.name,'counts':results,'analysis_sha256':digest(path)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--qualification-only',action='store_true');args=ap.parse_args()
    report=[check_analysis('qualification_cases')]
    if not args.qualification_only:
        report += [check_analysis('controlled_cases',erratum=True,pairs=True),check_analysis('controlled_cases','frozen_reference',pairs=True),check_analysis('controlled_cases','excluding_frame_species',erratum=True,exclude=True,pairs=True),check_analysis('source_recovery_cases')]
    out={'status':'PASS','independent_raw_JSON_recount':True,'whitelisted_prompt_inputs_equal':True,'reports':report,'boundary':'Checks retained response scoring and provenance; does not independently validate legal annotation.'}
    name='qualification_independent_recount.json' if args.qualification_only else 'functional_results_independent_recount.json'
    (R/'verification'/name).write_text(json.dumps(out,indent=2),encoding='utf8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
