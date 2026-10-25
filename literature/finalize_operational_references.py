"""Retain small official provenance sources and update only owned references."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, shutil
import requests

N = Path(r'D:\MLWork\tariff_scope_20261007\revision_20261023')
RAW = Path(r'F:\AcademicData\tariff_scope_20261007\raw\revision_20261023_literature_v1')
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
free = {d: shutil.disk_usage(d + ':\\').free for d in ['D','E','F']}
assert free['F'] > 20_000_000 and free['D'] > 20_000_000
sources = [
 ('qwen14_modelcard', 'https://huggingface.co/Qwen/Qwen3-14B/raw/main/README.md', '.md'),
 ('qwen14_gguf_modelcard', 'https://huggingface.co/Qwen/Qwen3-14B-GGUF/raw/main/README.md', '.md'),
 ('qwen14_repository_metadata', 'https://huggingface.co/api/models/Qwen/Qwen3-14B', '.json'),
 ('llamacpp_b11516_release', 'https://api.github.com/repos/ggml-org/llama.cpp/releases/tags/b11516', '.json'),
 ('cbp_cross_official_catalog', 'https://catalog.data.gov/dataset/cbp-customs-rulings-online-search-system-cross', '.html'),
]
manifest = {'retrieved_utc':stamp, 'free_bytes_before':free, 'raw_immutable':True,'sources':[]}
fetched = {}
for key,url,ext in sources:
    response = requests.get(url,timeout=45)
    response.raise_for_status()
    content = response.content
    out = RAW / f'{key}_{stamp}{ext}'
    with out.open('xb') as f: f.write(content)
    os.chmod(out, 0o444)
    fetched[key] = content
    manifest['sources'].append({'key':key,'url':url,'path':str(out),'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),'http_status':response.status_code})

model_meta=json.loads(fetched['qwen14_repository_metadata'])
release=json.loads(fetched['llamacpp_b11516_release'])
assert model_meta['id']=='Qwen/Qwen3-14B'
assert model_meta['createdAt'].startswith('2025-')
assert release['tag_name']=='b11516' and release['published_at'].startswith('2026-10-09')
assert release['prerelease'] is True
manifest['verified_metadata']={'model_repository_created_at':model_meta['createdAt'],'model_revision':model_meta['sha'],'software_tag':release['tag_name'],'software_published_at':release['published_at'],'software_prerelease':release['prerelease']}

index = Path(r'F:\AcademicData\tariff_scope_20261007\raw\statutes\ustr_index_20240117_20261007.pdf')
manifest['existing_immutable_ustr_index']={'path':str(index),'sha256':hashlib.sha256(index.read_bytes()).hexdigest(),'url':'https://ustr.gov/sites/default/files/Updated%20Index%20of%20Exclusions%20for%20Extension%201.17.24.pdf','title_from_pdf_footer':'Index of Exclusions for Possible Extension','version_from_pdf_footer':'1/17/24','pages':23,'verified_online_again':'2026-10-23','redownloaded':False}
(N/'literature/operational_source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

p=N/'literature/verified_references.json'
j=json.loads(p.read_text(encoding='utf-8'))
entries=[
 {'key':'ustr2024index','organization':'Office of the United States Trade Representative','year':2024,'title':'Index of Exclusions for Possible Extension','version_date':'2024-01-17','url':manifest['existing_immutable_ustr_index']['url'],'locator':'23-page PDF, dated footer; individual note identifiers','supports':'Frozen inventory source and literal scope wording only; not a current effective-exclusion list or all historical versions'},
 {'key':'cbp_cross','organization':'U.S. Customs and Border Protection','year':None,'title':'Customs Rulings Online Search System (CROSS)','resource_type':'Public database','url':'https://rulings.cbp.gov/','metadata_source':'https://catalog.data.gov/dataset/cbp-customs-rulings-online-search-system-cross','accessed':'2026-10-23','supports':'Official public searchable rulings, HQ/NY collections, modification and revocation links','access_note':'Current database landing page returned HTTP 403 to web reader; official DHS Data.gov entry read, source rulings independently retained and verified. Catalog modified date is not a terminal date for rulings.'},
 {'key':'qwen2025qwen3_14b','organization':'Qwen Team','year':2025,'title':'Qwen3-14B','resource_type':'Model and model card','url':'https://huggingface.co/Qwen/Qwen3-14B','official_gguf_url':'https://huggingface.co/Qwen/Qwen3-14B-GGUF','accessed':'2026-10-23','repository_created_at':model_meta['createdAt'],'license':'Apache-2.0','supports':'Checkpoint identity, official GGUF provenance and non-thinking mode interface; deterministic temperature zero is our experimental setting, not the recommended sampling setting'},
 {'key':'ggml2026llamacpp','organization':'ggml-org','year':2026,'title':'llama.cpp','resource_type':'Computer software','version':'b11516','published_at':release['published_at'],'status':'Pre-release','url':'https://github.com/ggml-org/llama.cpp/releases/tag/b11516','supports':'Exact inference-runtime build provenance; does not independently validate numerical or legal outputs'}
]
keys={e['key'] for e in entries}
j['official_task_and_venue_sources']=[e for e in j['official_task_and_venue_sources'] if e['key'] not in keys]+entries
j['scope']='Six closest legal-AI texts, four directly relevant customs/behavioral-testing references, and official task/data/model/software/venue sources; per-reference reading depth is explicit. Not a systematic literature census.'
p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')

p=N/'manuscript/references_verified.md'
text=p.read_text(encoding='utf-8')
paragraphs=[x for x in text.split('\n\n') if x.strip() and not x.startswith('##')]
paragraphs=[re.sub(r'(?<!\()https://doi.org/([^\s]+)',r'[DOI: \1](https://doi.org/\1)',x) for x in paragraphs]
paragraphs=[re.sub(r'(?<!\()https://www.gao.gov/products/gao-21-506',r'[Official report](https://www.gao.gov/products/gao-21-506)',x) for x in paragraphs]
u='https://ustr.gov/sites/default/files/enforcement/301Investigations/12.21.18_Notice_of_Product_Exclusions.pdf'
paragraphs=[x.replace(u,f'[Official notice]({u})') if '[Official notice]' not in x else x for x in paragraphs]
new=[
 'ggml-org. (2026). *llama.cpp* (build b11516) [Computer software; pre-release published 9 October 2026]. [Official release](https://github.com/ggml-org/llama.cpp/releases/tag/b11516).',
 'Qwen Team. (2025). *Qwen3-14B* [Model and model card]. [Official model card](https://huggingface.co/Qwen/Qwen3-14B); [official GGUF distribution](https://huggingface.co/Qwen/Qwen3-14B-GGUF). Accessed 23 October 2026.',
 'U.S. Customs and Border Protection (CBP). (n.d.). *Customs Rulings Online Search System (CROSS)* [Public database]. [CROSS](https://rulings.cbp.gov/); [official Department of Homeland Security catalog record](https://catalog.data.gov/dataset/cbp-customs-rulings-online-search-system-cross). Accessed 23 October 2026.',
 'U.S. Trade Representative (USTR). (2024). *Index of exclusions for possible extension* (17 January 2024 version). [Official index](https://ustr.gov/sites/default/files/Updated%20Index%20of%20Exclusions%20for%20Extension%201.17.24.pdf).',
]
for x in new:
    if x not in paragraphs: paragraphs.append(x)
paragraphs.sort(key=str.casefold)
p.write_text('## References\n\n'+'\n\n'.join(paragraphs)+'\n',encoding='utf-8')
print(json.dumps({'sources_saved':len(sources),'references':len(paragraphs),'metadata':manifest['verified_metadata']},ensure_ascii=False))
