"""Local, frozen-input evidence audit runner; no labels enter requests."""
import argparse,ctypes,datetime,hashlib,json,os,socket,subprocess,time,urllib.request
from pathlib import Path
from protocol import prompt,schema,parse,aggregate,STATES
ROOT=Path(__file__).resolve().parent
PROJ=ROOT.parents[1]
OLD=PROJ/'revision_20261009'/'models'
OUTPUT=ROOT/'outputs';OUTPUT.mkdir(exist_ok=True)
TEMP=ROOT/'temp';TEMP.mkdir(exist_ok=True)
os.environ.update(TEMP=str(TEMP),TMP=str(TEMP),HF_HOME=str(ROOT/'cache'),PYTHONDONTWRITEBYTECODE='1')
PORT=18983

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return [json.loads(s) for s in p.read_text(encoding='utf8').splitlines()] if p.exists() else []
def write(p,r):
    with p.open('a',encoding='utf8') as f:f.write(json.dumps(r,ensure_ascii=False)+'\n')
def call(ep,obj=None,timeout=1800):
    req=urllib.request.Request(f'http://127.0.0.1:{PORT}'+ep,data=None if obj is None else json.dumps(obj).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)
def memory():
    class M(ctypes.Structure):
        _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(k,ctypes.c_ulonglong) for k in ['total','available','total_pagefile','available_pagefile','total_virtual','available_virtual','extended']]
    m=M();m.length=ctypes.sizeof(m);ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return {k:getattr(m,k) for k,_ in m._fields_}

DIRECT='''Use only the stated facts to audit the supplied rule for the named target. All rule conditions are mandatory unless an explicit alternative is given. Return supported only if the facts establish all mandatory requirements; refuted if a stated fact contradicts a mandatory requirement; otherwise unknown. One decisive contradiction remains refuted even when other facts are missing. Silence is not negation. Keep each value or attribute attached to its product, component and measurement basis. Do not infer facts from product names. Return only {"decision":"supported"}, {"decision":"refuted"}, or {"decision":"unknown"}.'''

def invoke(case,kind):
    if kind=='checklist':u=prompt(case);j=schema(case);budget=min(1024,192+64*len(case['conditions']))
    else:
        u=DIRECT+'\n\nINPUT:\n'+json.dumps({k:case[k] for k in ['target','rule_text','facts']},ensure_ascii=False)
        j={'type':'object','properties':{'decision':{'type':'string','enum':STATES}},'required':['decision'],'additionalProperties':False};budget=48
    p=call('/apply-template',{'messages':[{'role':'user','content':u}],'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False,'thinking':False}})['prompt']
    assert p.count('<think>')==p.count('</think>')
    tokens=call('/tokenize',{'content':p,'add_special':False})['tokens']
    if len(tokens)+budget>4096:
        return {'case_id':case['case_id'],'kind':kind,'valid':False,'error':'context_cap_before_inference','input_tokens':len(tokens),'budget':budget,'user_prompt':u}
    start=time.monotonic()
    ans=call('/completion',{'prompt':p,'n_predict':budget,'temperature':0,'seed':20261023,'repeat_penalty':1.0,'cache_prompt':False,'json_schema':j,'return_tokens':True})
    rec={'case_id':case['case_id'],'kind':kind,'user_prompt':u,'prompt':p,'json_schema':j,'input_tokens':len(tokens),'output_tokens':ans.get('tokens_predicted'),'output_budget':budget,'raw_output':ans['content'],'seconds':time.monotonic()-start,'truncated':ans.get('truncated',False),'stopped_limit':ans.get('stop_type')=='limit' or ans.get('stopped_limit',False),'llama_response':ans}
    try:
        if kind=='checklist':obj=parse(ans['content'],case)
        else:
            obj=json.loads(ans['content']);assert set(obj)=={'decision'} and obj['decision'] in STATES
        rec.update(valid=True,parsed=obj)
        if kind=='checklist':
            rec['complete_condition_ids']={c['id'] for c in obj['conditions']}=={c['id'] for c in case['conditions']}
            rec['aggregated_decision']=aggregate([c['state'] for c in obj['conditions']]) if rec['complete_condition_ids'] else None
    except (AssertionError,KeyError,TypeError,ValueError) as e:rec.update(valid=False,error=type(e).__name__+': '+str(e))
    return rec

def score(data,pred):
    byid={r['case_id']:r for r in pred};n=len(data);valid=correct=cc=cn=bad_support=refmiss=0;miss=[]
    for r in data:
        p=byid.get(r['case_id']);gold=r['expected'];cn+=len(r['conditions'])
        if p and p.get('valid') and p.get('complete_condition_ids',True) and not p.get('stopped_limit') and not p.get('truncated'):
            valid+=1;x=p['parsed'];correct+=x['decision']==gold['decision'];bad_support+=x['decision']=='supported' and gold['decision']!='supported'
            if p['kind']=='checklist':
                cs={c['id']:c for c in x['conditions']};cc+=sum(cs[k]['state']==v for k,v in gold['states'].items())
                okay=(x['decision']==gold['decision'] and set(x['requests'])==set(gold['requests']) and all(cs[k]['state']==v for k,v in gold['states'].items()))
            else:okay=x['decision']==gold['decision']
            if r['mechanism']=='decisive_refutation_with_missing':refmiss+=okay
            if not okay:miss.append(r['case_id'])
        else:miss.append(r['case_id'])
    kind=pred[0]['kind'] if pred else None
    gate=valid==n and correct>=n-1 and bad_support==0 and refmiss==sum(r['mechanism']=='decisive_refutation_with_missing' for r in data)
    if kind=='checklist':gate=gate and cc/cn>=.95
    return {'n':n,'conditions_n':cn,'valid':valid,'correct_decisions':correct,'correct_conditions':cc if kind=='checklist' else None,'unsupported_affirmations':bad_support,'decisive_refutation_missing_passes':refmiss,'passed':gate,'failed_ids':miss}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model',choices=['qwen14','granite8'],default='qwen14');ap.add_argument('--dataset');ap.add_argument('--dev-only',action='store_true');ap.add_argument('--kind',choices=['both','direct','checklist'],default='both');args=ap.parse_args()
    name=args.model;meta=next(m for m in json.loads((OLD/'outputs'/'model_manifest.json').read_text()) if m['name']==name)
    minimum=(6 if name=='qwen14' else 4)*1024**3
    if memory()['available']<minimum:raise RuntimeError('RAM gate: '+json.dumps(memory()))
    cmd=[str(OLD/'runtime'/'llama-server.exe'),'-m',meta['inference_path'],'--host','127.0.0.1','--port',str(PORT),'-t','6','-tb','6','-c','4096','-np','1','-b','512','-ub','128','-ngl','0','--fit','off','--jinja','--reasoning','off','--chat-template-kwargs',json.dumps({'enable_thinking':False,'thinking':False}),'--no-webui']
    with socket.socket() as s:s.bind(('127.0.0.1',PORT))
    token=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');log=(OUTPUT/f'{name}_{token}_server.log').open('w',encoding='utf8')
    provenance={'created_utc':token,'model':meta,'command':cmd,'protocol_sha256':sha(ROOT/'protocol.py'),'runner_sha256':sha(Path(__file__)),'memory_before':memory(),'temperature':0,'seed':20261023,'context':4096,'template_thinking':False,'grammar_constrained':True,'data_status':'post-hoc revision; official cases are not protocol-development data'}
    proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW);provenance['pid']=proc.pid;start=time.monotonic();write(OUTPUT/'run_sessions.jsonl',provenance)
    try:
        for _ in range(240):
            if proc.poll() is not None:raise RuntimeError('server exited')
            try:
                if call('/health',timeout=1).get('status')=='ok':break
            except Exception:pass
            time.sleep(1)
        else:raise TimeoutError('server load')
        provenance['load_seconds']=time.monotonic()-start;provenance['props']=call('/props')
        datasets=[Path(args.dataset)] if args.dataset else [ROOT/'development_cases.jsonl']+([] if args.dev_only else [ROOT/'qualification_cases.jsonl'])
        for source in datasets:
            data=rows(source);freeze={'source':str(source),'sha256':sha(source),'case_ids':[r['case_id'] for r in data],'protocol_sha256':provenance['protocol_sha256'],'model_sha256':meta['sha256']}
            freeze_path=OUTPUT/f'{name}_{source.stem}_freeze.json'
            if freeze_path.exists():assert json.loads(freeze_path.read_text())==freeze,'Refuse resume changed inputs/protocol'
            else:freeze_path.write_text(json.dumps(freeze,indent=2),encoding='utf8')
            for kind in (['direct','checklist'] if args.kind=='both' else [args.kind]):
                path=OUTPUT/f'{name}_{source.stem}_{kind}.jsonl';done={r['case_id'] for r in rows(path)}
                for i,r in enumerate(data,1):
                    if r['case_id'] in done:continue
                    a=invoke(r,kind);a.update(model=name,dataset_sha256=freeze['sha256'],protocol_sha256=freeze['protocol_sha256']);write(path,a)
                    print(name,source.stem,kind,i,'/',len(data),'valid',a['valid'],'seconds',round(a.get('seconds',0),2),flush=True)
                if all('expected' in r for r in data):
                    result=score(data,rows(path));(OUTPUT/f'{name}_{source.stem}_{kind}_summary.json').write_text(json.dumps(result,indent=2),encoding='utf8');print('SUMMARY',kind,json.dumps(result),flush=True)
    finally:
        if proc.poll() is None:proc.terminate();proc.wait(timeout=30)
        log.close();provenance.update(wall_seconds=time.monotonic()-start,memory_after=memory())
        (OUTPUT/f'{name}_{token}_session.json').write_text(json.dumps(provenance,indent=2),encoding='utf8')

if __name__=='__main__':main()
