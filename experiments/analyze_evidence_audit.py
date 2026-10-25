"""Functional endpoints for the frozen evidence-audit task, not y prediction."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,json,hashlib,random
from protocol import aggregate
ROOT=Path(__file__).resolve().parent
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf8').splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ratio(n,d):return n/d if d else None
def quantile(a,p):
    a=sorted(a);x=(len(a)-1)*p;i=int(x);return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(x-i)

def case_record(row,p):
    gold=row['expected'];expected=gold['states'];required=set(gold['requests'])
    result={'case_id':row['case_id'],'group':row.get('group',row.get('family',row['case_id'])),
            'mechanism':row.get('mechanism'),'variant':row.get('variant'),
            'gold':gold['decision'],'condition_n':len(expected),'required_request_n':len(required),
            'valid':False,'decision':None,'decision_correct':0,'aggregated_decision':None,
            'aggregation_correct':0,'complete_condition_ids':False,'condition_correct':0,
            'unsupported_affirmations':0,'unsupported_case_affirmation':0,
            'unsupported_refutations':0,'unsupported_case_refutation':0,
            'gap_tp':0,'gap_fp':0,'gap_fn':sum(v=='unknown' for v in expected.values()),
            'request_tp':0,'request_fp':0,'request_fn':len(required),'request_n':0,
            'request_set_correct':False,'evidence_exact_n':0,'evidence_scored_n':len(gold.get('evidence',{})),
            'determinate_evidence_exact_n':0,'determinate_evidence_scored_n':sum(expected[k]!='unknown' for k in gold.get('evidence',{})),
            'joint_state_and_evidence_correct':0,
            'refutation_with_missing':gold['decision']=='refuted' and 'unknown' in expected.values(),
            'refutation_retained_no_request':False}
    direct_na=['condition_n','required_request_n','aggregated_decision','aggregation_correct','complete_condition_ids','condition_correct',
                  'unsupported_affirmations','unsupported_refutations','gap_tp','gap_fp','gap_fn','request_tp','request_fp','request_fn',
                  'request_n','request_set_correct','evidence_exact_n','evidence_scored_n','refutation_retained_no_request',
                  'determinate_evidence_exact_n','determinate_evidence_scored_n','joint_state_and_evidence_correct']
    if p and p['kind']=='direct':
        for k in direct_na:result[k]=None
    if not p or not p.get('valid') or p.get('stopped_limit') or p.get('truncated'):return result
    x=p['parsed'];result.update(valid=True,decision=x['decision'],decision_correct=int(x['decision']==gold['decision']),unsupported_case_affirmation=int(x['decision']=='supported' and gold['decision']!='supported'),unsupported_case_refutation=int(x['decision']=='refuted' and gold['decision']!='refuted'))
    if p['kind']=='direct':
        return result
    cs={c['id']:c for c in x['conditions']};complete=set(cs)==set(expected)
    agg=aggregate([cs[k]['state'] for k in expected]) if complete else None
    result.update(complete_condition_ids=complete,aggregated_decision=agg,aggregation_correct=int(agg==gold['decision']))
    expected_gaps={k for k,v in expected.items() if v=='unknown'};pred_gaps={k for k,c in cs.items() if c['state']=='unknown'}
    req=set(x['requests'])
    result.update(condition_correct=sum(k in cs and cs[k]['state']==v for k,v in expected.items()),
                  unsupported_affirmations=sum(c['state']=='supported' and expected[k]!='supported' for k,c in cs.items()),
                  unsupported_refutations=sum(c['state']=='refuted' and expected[k]!='refuted' for k,c in cs.items()),
                  gap_tp=len(pred_gaps&expected_gaps),gap_fp=len(pred_gaps-expected_gaps),gap_fn=len(expected_gaps-pred_gaps),
                  request_tp=len(req&required),request_fp=len(req-required),request_fn=len(required-req),request_n=len(req),
                  request_set_correct=req==required,
                  refutation_retained_no_request=result['refutation_with_missing'] and x['decision']=='refuted' and not req)
    for k,allowed in gold.get('evidence',{}).items():
        if k not in cs:continue
        # Source-recovery inputs may lack a unique minimal citation set; only
        # rows with an explicit acceptable ID set enter this endpoint.
        acceptable=gold.get('evidence_allowed_sets',{}).get(k,[allowed])
        exact=any(set(cs[k]['evidence'])==set(v) for v in acceptable)
        result['evidence_exact_n']+=exact
        result['determinate_evidence_exact_n']+=exact and expected[k]!='unknown'
        result['joint_state_and_evidence_correct']+=exact and cs[k]['state']==expected[k]
    return result

def summarise(records,kind):
    n=len(records);s=lambda k:sum(r[k] for r in records);out={'n':n,'groups':len({r['group'] for r in records}),
        'valid':s('valid'),'decision_correct':s('decision_correct'),'decision_accuracy':ratio(s('decision_correct'),n),
        'prediction_counts':dict(Counter(r['decision'] or 'invalid' for r in records)),
        'unsupported_case_affirmations':s('unsupported_case_affirmation'),
        'unsupported_case_refutations':s('unsupported_case_refutation'),
        'state_confusion_matrix':{g:{p:sum(r['gold']==g and (r['decision'] or 'invalid')==p for r in records) for p in ['supported','refuted','unknown','invalid']} for g in ['supported','refuted','unknown']},
        'determinate_n':sum(r['decision'] in ['supported','refuted'] for r in records),
        'determinate_errors':sum(r['decision'] in ['supported','refuted'] and not r['decision_correct'] for r in records)}
    if kind=='checklist':
        out.update(complete_condition_records=s('complete_condition_ids'),condition_n=s('condition_n'),condition_correct=s('condition_correct'),
          condition_accuracy=ratio(s('condition_correct'),s('condition_n')),aggregation_correct=s('aggregation_correct'),aggregation_accuracy=ratio(s('aggregation_correct'),n),
          unsupported_condition_affirmations=s('unsupported_affirmations'),
          unsupported_condition_refutations=s('unsupported_refutations'),
          gap_localization={'tp':s('gap_tp'),'fp':s('gap_fp'),'fn':s('gap_fn'),'precision':ratio(s('gap_tp'),s('gap_tp')+s('gap_fp')),'recall':ratio(s('gap_tp'),s('gap_tp')+s('gap_fn'))},
          requests={'tp':s('request_tp'),'unnecessary':s('request_fp'),'missing_necessary':s('request_fn'),'precision':ratio(s('request_tp'),s('request_n')),'recall':ratio(s('request_tp'),s('required_request_n')),'exact_case_sets':s('request_set_correct')},
          evidence_id_acceptable={'correct':s('evidence_exact_n'),'scored':s('evidence_scored_n'),
             'determinate_correct':s('determinate_evidence_exact_n'),'determinate_scored':s('determinate_evidence_scored_n'),
             'joint_state_and_evidence_correct':s('joint_state_and_evidence_correct'),
             'definition':'Agreement with an acceptable fact-ID set; equivalent target-frame evidence is admitted under the pre-result erratum. This is not expert-validated legal entailment. Missing or invalid condition records count as failures.'},
          refutation_with_missing={'n':s('refutation_with_missing'),'correct_with_no_request':s('refutation_retained_no_request')})
    return out

def cluster_difference(a,b,constructed=False,counts_only=False):
    # Match all members of each source group in each bootstrap replicate.
    assert {r['case_id'] for r in a}=={r['case_id'] for r in b}
    bm={r['case_id']:r for r in b};groups=defaultdict(list)
    for r in a:groups[r['group']].append(r['decision_correct']-bm[r['case_id']]['decision_correct'])
    keys=sorted(groups);vals=[v for vv in groups.values() for v in vv]
    observed_n=len(vals);observed_difference=sum(vals)/len(vals)
    discordances=Counter('checklist_only_correct' if v==1 else 'direct_only_correct' if v==-1 else 'same_correctness' for v in vals)
    if constructed or counts_only:
        return {'n':len(vals),'source_families':len(keys),'difference':sum(vals)/len(vals),'discordances':dict(discordances),
                'family_differences':{k:sum(v)/len(v) for k,v in groups.items()},
                'interval':None,'meaning':'Exact counts in a deliberately selected diagnostic domain. No population CI. Clause semantics are shared; supplied structure and requested outputs differ, so this is not an isolated aggregation effect.'}
    rng=random.Random(20261023);dist=[]
    for _ in range(2000):
        sampled_vals=[v for k in rng.choices(keys,k=len(keys)) for v in groups[k]];dist.append(sum(sampled_vals)/len(sampled_vals))
    return {'n':observed_n,'groups':len(keys),'difference':observed_difference,'percentile_95ci':[quantile(dist,.025),quantile(dist,.975)],'resamples':2000,'seed':20261023,
            'discordances':dict(discordances),
            'meaning':'Paired checklist overall decision minus direct overall decision. Different supplied representations; not an isolated aggregation effect or population prevalence.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--dataset',required=True);ap.add_argument('--model',default='qwen14');ap.add_argument('--pairs');ap.add_argument('--erratum');ap.add_argument('--exclude-family');ap.add_argument('--output-tag',default='');args=ap.parse_args()
    source=Path(args.dataset);data=read(source);reports={};joined={};hashes={'input':sha(source)}
    full_ids={r['case_id'] for r in data}
    if args.erratum:
        ep=Path(args.erratum);erratum=json.loads(ep.read_text(encoding='utf8'));assert erratum['input_sha256']==sha(source)
        hashes['erratum']=sha(ep);byid={r['case_id']:r for r in data}
        for edit in erratum['edits']:
            expected=byid[edit['case_id']]['expected'];key=edit['condition_id'];expected['states'][key]=edit['state']
            expected.setdefault('evidence_allowed_sets',{})[key]=edit['acceptable_evidence_sets']
            assert aggregate(list(expected['states'].values()))==expected['decision']
    if args.exclude_family:data=[r for r in data if r.get('family')!=args.exclude_family]
    for kind in ['direct','checklist']:
        path=ROOT/'outputs'/f'{args.model}_{source.stem}_{kind}.jsonl'
        if not path.exists():continue
        raw_predictions=read(path);pred={r['case_id']:r for r in raw_predictions}
        assert len(raw_predictions)==len(pred)==len(full_ids) and set(pred)==full_ids,'Only score a complete, duplicate-free frozen output, including excluded-sensitivity cases'
        rr=[case_record(r,pred[r['case_id']]) for r in data];joined[kind]=rr;hashes[kind]=sha(path)
        reports[kind]={'overall':summarise(rr,kind),'by_mechanism':{m:summarise([r for r in rr if r['mechanism']==m],kind) for m in sorted({r['mechanism'] for r in rr})}}
        if args.pairs:
            lookup={r['case_id']:r for r in rr};ps=[p for p in read(Path(args.pairs)) if p['left'] in lookup and p['right'] in lookup];pair_records=[]
            for pair in ps:
                left,right=lookup[pair['left']],lookup[pair['right']]
                both=left['decision_correct'] and right['decision_correct']
                relation=left['decision']==right['decision'] if pair['expected_relation']=='same' else left['decision']!=right['decision']
                pair_records.append({**pair,'both_correct':bool(both),'expected_relation_observed':bool(relation),'success':bool(both and relation)})
            reports[kind]['pairs']={'n':len(ps),'success':sum(p['success'] for p in pair_records),'by_operation':{m:{'n':sum(p['operation']==m for p in pair_records),'success':sum(p['success'] and p['operation']==m for p in pair_records)} for m in sorted({p['operation'] for p in pair_records})},'records':pair_records}
    output={'model':args.model,'dataset':str(source),'hashes':hashes,'reports':reports,'case_records':joined,
            'reference_policy':'pre-result semantic erratum applied' if args.erratum else 'original frozen reference',
            'excluded_family':args.exclude_family,'effective_references':{r['case_id']:r['expected'] for r in data},
            'paired_representations':cluster_difference(joined['checklist'],joined['direct'],constructed=all(r.get('constructed') for r in data),counts_only=all(r.get('diagnostic_counts_only') for r in data)) if set(joined)=={'checklist','direct'} else None,
            'reference_status':'AI-assisted text-evidence diagnostic reference; constructed cases are synthetic, not new observed adjudications.'}
    suffix='_'+args.output_tag if args.output_tag else ''
    (ROOT/'outputs'/f'{args.model}_{source.stem}_functional_analysis{suffix}.json').write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({k:v['overall'] for k,v in reports.items()},indent=2))
if __name__=='__main__':main()
