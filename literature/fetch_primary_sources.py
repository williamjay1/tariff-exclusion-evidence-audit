from pathlib import Path
import requests, json, hashlib, os
from concurrent.futures import ThreadPoolExecutor
import fitz
ROOT=Path(__file__).resolve().parent
RAW=Path(r'F:\AcademicData\tariff_scope_20261007\raw\revision_20261023_literature_v1')
RAW.mkdir(parents=True,exist_ok=True)
(ROOT/'extracted').mkdir(exist_ok=True)
SOURCES={
 'contractnli_2021.pdf':'https://aclanthology.org/2021.findings-emnlp.164.pdf',
 'holzenberger_vandurme_2023.pdf':'https://aclanthology.org/2023.nllp-1.12.pdf',
 'medvedeva_mcbride_2023.pdf':'https://aclanthology.org/2023.nllp-1.9.pdf',
 'vita_2025.pdf':'https://link.springer.com/content/pdf/10.1007/s10506-025-09465-7.pdf',
 'vita_2025.html':'https://link.springer.com/article/10.1007/s10506-025-09465-7',
 'ailaw_scope_20261023.html':'https://link.springer.com/journal/10506/aims-and-scope',
 'ailaw_guidelines_20261023.html':'https://link.springer.com/journal/10506/submission-guidelines',
 'ailaw_home_20261023.html':'https://link.springer.com/journal/10506',
 'gao_21_506_20261023.html':'https://www.gao.gov/products/gao-21-506',
 'ustr_20181221_notice.pdf':'https://ustr.gov/sites/default/files/enforcement/301Investigations/12.21.18_Notice_of_Product_Exclusions.pdf',
}
def run(kv):
 name,url=kv;p=RAW/name
 if p.exists():
  data=p.read_bytes();status='existing_immutable_snapshot_reused'
 else:
  r=requests.get(url,timeout=80,headers={'User-Agent':'Mozilla/5.0 (compatible; Academic source verification)'})
  r.raise_for_status();data=r.content
  if name.endswith('.pdf') and not data.startswith(b'%PDF'):raise ValueError('not PDF: '+url)
  with p.open('xb') as f:f.write(data)
  os.chmod(p,0o444);status='downloaded'
 result={'name':name,'url':url,'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'status':status}
 if name.endswith('.pdf'):
  with fitz.open(p) as d:
   txt='\n\n'.join(f'=== PDF PAGE {i+1} ===\n'+page.get_text(sort=True) for i,page in enumerate(d))
   result['pages']=len(d)
  out=ROOT/'extracted'/name.replace('.pdf','.txt');out.write_text(txt,encoding='utf-8');result['extracted']=str(out)
 return result
results=[]
with ThreadPoolExecutor(max_workers=4) as ex:
 futures={ex.submit(run,kv):kv for kv in SOURCES.items()}
 for f,kv in futures.items():
  try:r=f.result()
  except Exception as e:r={'name':kv[0],'url':kv[1],'error':str(e)}
  results.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
(ROOT/'source_fetch_manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
