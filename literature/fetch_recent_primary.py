from pathlib import Path
import requests,fitz,hashlib,json,os,re
ROOT=Path(__file__).resolve().parent
RAW=Path(r'F:\AcademicData\tariff_scope_20261007\raw\revision_20261023_literature_v1')
items=[('clause_2026.pdf','https://aclanthology.org/2026.findings-eacl.305.pdf'),('tribenchko_2026.pdf','https://arxiv.org/pdf/2605.03792')]
out=[]
for name,url in items:
 p=RAW/name
 if not p.exists():
  r=requests.get(url,timeout=90);r.raise_for_status();assert r.content.startswith(b'%PDF')
  with p.open('xb') as f:f.write(r.content)
  os.chmod(p,0o444)
 with fitz.open(p) as d:
  txt='\n\n'.join(f'=== PDF PAGE {i+1} ===\n'+re.sub(r' {3,}',' ',page.get_text(sort=False)) for i,page in enumerate(d))
  pages=len(d)
 (ROOT/'extracted'/name.replace('.pdf','.txt')).write_text(txt,encoding='utf-8')
 out.append(dict(name=name,url=url,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pages=pages,path=str(p)))
(ROOT/'recent_fetch_manifest.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
