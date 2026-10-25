from pathlib import Path
import requests,json,hashlib,datetime,importlib.metadata,os,re
import fitz
O=Path(__file__).resolve().parent
R=Path(r'F:\AcademicData\tariff_scope_20261007\raw\revision_20261023_literature_v1')
R.mkdir(parents=True,exist_ok=True)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
C='b9b16959570bd2fbc9ff5118bacc423c3bddd592'
items={
 'hscodecomp':('https://aclanthology.org/2026.acl-long.937.pdf','pdf'),
 'checklist':('https://aclanthology.org/2020.acl-main.442.pdf','pdf'),
 'hsgraphagent':('https://aclanthology.org/2026.acl-long.2072/','html'),
 'explainable_customs_kaist':('https://pure.kaist.ac.kr/en/publications/explainable-product-classification-for-customs/','html'),
 'scienceplots_nature':(f'https://raw.githubusercontent.com/garrettj403/SciencePlots/{C}/src/scienceplots/styles/journals/nature.mplstyle','txt'),
 'scienceplots_license':(f'https://raw.githubusercontent.com/garrettj403/SciencePlots/{C}/LICENSE','txt'),
 'nature_building':('https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/','html'),
 'nature_specifications':('https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/','html'),
}
out=[]
for key,(url,ext) in items.items():
 try:
  resp=requests.get(url,timeout=60);resp.raise_for_status();data=resp.content
  p=R/f'{key}_{stamp}.{ext}'
  with p.open('xb') as f:f.write(data)
  os.chmod(p,0o444)
  row={'key':key,'url':url,'final_url':resp.url,'raw_path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'status':'saved; content needs checking'}
  if ext=='pdf':
   with fitz.open(p) as doc:
    pages=[x.get_text(sort=False) for x in doc];row['pages']=len(pages)
   target=O/'extracted'/f'{key}_{stamp}.txt';target.parent.mkdir(exist_ok=True)
   target.write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n'+re.sub(r' {3,}',' ',text) for i,text in enumerate(pages)),encoding='utf-8');row['derived_text']=str(target)
  out.append(row)
 except Exception as e:out.append({'key':key,'url':url,'error':repr(e)})
manifest={'retrieved_at_utc':stamp,'scienceplots_commit':C,'scienceplots_installed_version':importlib.metadata.version('SciencePlots'),'items':out}
(O/'supplementary_source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
