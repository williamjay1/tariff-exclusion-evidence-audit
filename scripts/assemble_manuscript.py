"""Assemble a single main text and a single supplement after results freeze."""
from pathlib import Path
import re,json,hashlib
R=Path(__file__).resolve().parents[1];M=R/'manuscript'
def read(name):return (M/name).read_text(encoding='utf8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert (R/'experiments/outputs/experiment_final_summary.json').is_file(),'Await complete fixed inference queue'
    check=json.loads((R/'verification/functional_results_independent_recount.json').read_text(encoding='utf8'))
    assert check['status']=='PASS'
    front=read('front_matter_and_methods.md')
    title,body=front.split('\n',1)
    abstract=read('abstract.md')
    parts=[title,abstract,body.strip(),read('source_results.md'),read('functional_results.md'),read('historical_main.md'),read('cases_and_discussion.md'),read('references_verified.md')]
    main_text='\n\n'.join(parts)+'\n'
    s2=read('supplement_source_audit.md')
    for old,new in [('Table S2','Table S2.1'),('Table S3','Table S2.2'),('Table S4','Table S2.3')]:
        s2=re.sub(re.escape(old)+r'(?![\d.])',new,s2)
    s3=read('supplement_inventory.md').replace('## Supplement: Structure and coverage of the exclusion inventory','## S3 Structure and coverage of the exclusion inventory')
    n=0
    def renumber(match):
        nonlocal n;n+=1
        return f'### S3.{n} '+match[1]
    s3=re.sub(r'^### (.+)$',renumber,s3,flags=re.M)
    s4=read('supplement_functional.md')
    s4=re.sub(r'^# S4\. ', '## S4 ',s4,flags=re.M)
    s4=re.sub(r'^## (S4\.\d+)\. ',r'### \1 ',s4,flags=re.M)
    # Preserve final result captions while including the two methods tables in
    # one nonduplicated section-based numbering sequence.
    s4=re.sub(r'Table S4\.([123])\.',lambda m:f'Table S4.{int(m[1])+2}.',s4)
    s4=s4.replace('| Source family |','Table S4.1 Source families and selected attributes\n\n| Source family |')
    s4=s4.replace('| Isolated source condition |','Table S4.2 Isolated source-restoration conditions\n\n| Isolated source condition |')
    table_number=len(re.findall(r'^Table S4\.\d+',s4,flags=re.M))
    assert table_number==5
    supplement='\n\n'.join(['# Supplementary material',f'*{title[2:]}*',read('supplement_overview.md'),s2,s3,s4,read('supplement_legacy.md')])+'\n'
    banned=['still running','will be populated','NEW RESULT FREEZE PENDING','TODO','TBD','待主代理填入']
    for text in [main_text,supplement]:
        assert not any(s.lower() in text.lower() for s in banned),'Unresolved result placeholder'
        assert not re.search(r'\b[A-Z]:[\\/]',text),'Local machine path in article'
    (M/'manuscript.md').write_text(main_text,encoding='utf8')
    (M/'supplement.md').write_text(supplement,encoding='utf8')
    report={'status':'PASS','main_words':len(main_text.split()),'supplement_words':len(supplement.split()),
      'main_sha256':sha(M/'manuscript.md'),'supplement_sha256':sha(M/'supplement.md'),
      'functional_table_captions':table_number,'sources':{p.name:sha(p) for p in M.glob('*.md') if p.name not in ['manuscript.md','supplement.md']}}
    (R/'verification/manuscript_assembly.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
