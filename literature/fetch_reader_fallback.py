from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests, json, hashlib, os, re
import fitz
ROOT=Path(__file__).resolve().parent
RAW=Path(r'F:\AcademicData\tariff_scope_20261007\raw\revision_20261023_literature_v1')
SOURCES={
 'vita_2025_jina.md':'https://r.jina.ai/https://link.springer.com/article/10.1007/s10506-025-09465-7',
 'ailaw_scope_20261023_jina.md':'https://r.jina.ai/https://link.springer.com/journal/10506/aims-and-scope',
 'ailaw_guidelines_20261023_jina.md':'https://r.jina.ai/https://link.springer.com/journal/10506/submission-guidelines',
 'ailaw_home_20261023_jina.md':'https://r.jina.ai/https://link.springer.com/journal/10506',
 'gao_21_506_20261023_jina.md':'https://r.jina.ai/https://www.gao.gov/products/gao-21-506',
 'vita_2025_nsf.pdf':'https://par.nsf.gov/servlets/purl/10649839',
}
def fetch(kv):
 name,url=kv;p=RAW/name
 if p.exists():data=p.read_bytes()
 else:
  r=requests.get(url,timeout=100);r.raise_for_status();data=r.content
  if name.endswith('.pdf') and not data.startswith(b'%PDF'):raise ValueError('not PDF')
  with p.open('xb') as f:f.write(data)
  os.chmod(p,0o444)
 return {'name':name,'url':url,'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
res=[]
with ThreadPoolExecutor(max_workers=4) as ex:
 for f,kv in [(ex.submit(fetch,kv),kv) for kv in SOURCES.items()]:
  try:r=f.result()
  except Exception as e:r={'name':kv[0],'url':kv[1],'error':str(e)}
  print(json.dumps(r),flush=True);res.append(r)
(ROOT/'reader_fallback_manifest.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
for p in RAW.glob('*.pdf'):
 with fitz.open(p) as d:
  txt='\n\n'.join(f'=== PDF PAGE {i+1} ===\n'+re.sub(r'[ \t]{3,}',' ',page.get_text(sort=False)) for i,page in enumerate(d))
 (ROOT/'extracted'/p.with_suffix('.txt').name).write_text(txt,encoding='utf-8')
