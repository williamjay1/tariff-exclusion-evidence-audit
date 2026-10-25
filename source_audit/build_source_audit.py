"""Source audit utilities. Reads frozen inputs and immutable CBP snapshots only."""
from pathlib import Path
import json, hashlib, re, sys

ROOT = Path('D:/MLWork/tariff_scope_20261007')
OUT = ROOT / 'revision_20261023/source_audit'
OLD = ROOT / 'revision_20261009/evidence_numeric'

def readl(p):
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]

def dump(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def load():
    operational = readl(OLD/'evidence_operational_reference.jsonl')
    initial = {x['case_id']:x for x in readl(OLD/'evidence_condition_codes.jsonl')}
    visible = {x['case_id']:x for x in readl(OLD/'evidence_visible_inputs.jsonl')}
    derived = {x['rulingNumber']:x for x in readl(ROOT/'datasets/cbp_rulings_derived.jsonl')}
    sources={}
    for x in operational:
        rid=x['case_id'].split('_')[0]
        if rid in sources: continue
        rec=derived[rid]; p=Path(rec['raw_path']); blob=p.read_bytes(); raw=json.loads(blob)
        assert raw['text']==rec['text'], rid
        ps=[]
        for m in re.finditer(r'[^\r\n]+',raw['text']):
            if m.group().strip(): ps.append({'paragraph_id':f'p{len(ps)+1:03d}', 'raw_span':[m.start(),m.end()], 'text':m.group()})
        sources[rid]={'ruling_id':rid,'official_url':rec['official_url'],'raw_path':str(p),'raw_sha256':hashlib.sha256(blob).hexdigest(),'text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest(),'text':raw['text'],'paragraphs':ps}
    return operational,initial,visible,sources

def main():
    op,ini,vis,src=load()
    if len(sys.argv)>1 and sys.argv[1]=='show':
        for key in sys.argv[2:]:
            x=next((x for x in op if x['case_id']==key),None)
            rid=key.split('_')[0]
            print('\nRULING',rid)
            if x:
                print('VISIBLE FACTS',vis[key]['facts'])
                print('RULE',vis[key]['rule_text'])
                print('CONDITIONS',json.dumps(x['conditions'],ensure_ascii=False))
            for p in src[rid]['paragraphs']: print(p['paragraph_id'],p['raw_span'],p['text'])
        return
    dump(OUT/'source_manifest.json',{'scope':'73 purposively selected pairs; source audit is AI-assisted, not expert legal validation','sources':[{k:v for k,v in x.items() if k not in ['text','paragraphs']} for x in src.values()]})
    (OUT/'source_paragraphs.jsonl').write_text(''.join(json.dumps({'ruling_id':rid,**p},ensure_ascii=False)+'\n' for rid,x in src.items() for p in x['paragraphs']),encoding='utf-8')
    h=src['H330938']; q='Lastly, the submitted documentation describes the subject cables as imported on reels at very long lengths without connectors.'; start=h['text'].index(q)
    dump(OUT/'H330938_priority_verification.json',{'status':'MATERIAL_SOURCE_ERROR_CONFIRMED','source':{k:v for k,v in h.items() if k not in ['text','paragraphs']},'quote':q,'raw_text_span':[start,start+len(q)],'old_input_contains_quote':q in vis['H330938_1']['facts'],'correct_scope':'The restricted factual excerpt omits connector status; the full official ruling explicitly attributes absence of connectors to submitted documentation.','correction':'Delete the claim that the full analysis offers no connector-specific factual statement.','boundary':'Restoring this direct attribute does not independently validate the monopolar technical/legal classification; keep that inference in an interpretive layer.'})
    print('sources',len(src),'cases',len(op),'conditions',sum(len(x['conditions']) for x in op))

if __name__=='__main__': main()
