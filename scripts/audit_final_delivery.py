"""Final finite consistency gate; this is not an acceptance prediction."""
from pathlib import Path
import re,json,hashlib,zipfile
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    preservation=load(R/'verification/preserved_inputs.json')
    for item in preservation['files']:
        p=Path(item['path']);assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],p
    source=load(R/'source_audit/source_audit_summary.json')
    inventor=load(R/'verification/inventory_policy_independent_audit.json')
    final=load(R/'experiments/outputs/experiment_final_summary.json')
    check_paths=['verification/source_audit_independent_checks.json',
       'verification/inventory_policy_independent_audit.json',
       'verification/constructed_design_independent_audit.json',
       'verification/functional_results_independent_recount.json',
       'artwork/qa/export_integrity.json']
    for rel in check_paths:assert load(R/rel)['status']=='PASS',rel
    docs=load(R/'verification/docx_content_audit.json')
    for item in docs:
        assert item['paragraphs_exact'] and item['table_cells_exact']
        p=Path(item['output']);assert sha(p)==item['sha256']
        with zipfile.ZipFile(p) as z:assert z.testzip() is None
    texts={name:(R/'manuscript'/name).read_text(encoding='utf8') for name in ['manuscript.md','supplement.md']}
    for name,text in texts.items():
        for term in ['still running','will be populated','TODO','TBD','待主代理']:
            assert term.lower() not in text.lower(),(name,term)
        # The supplement describes literal schema placeholders in the actual
        # model protocol. Do not confuse that ordinary noun with a draft marker.
        assert not re.search(r'\bPLACEHOLDER\b',text),(name,'draft marker')
        assert not re.search(r'\b[A-Z]:[\\/]',text),name
        for relative in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):
            assert (R/'manuscript'/relative).resolve().is_file(),relative
    main_text=texts['manuscript.md'];supp=texts['supplement.md']
    main_tables=re.findall(r'^Table (\d+)\s+[^\n]+\n\n\|',main_text,re.M)
    assert main_tables==['1','2','3','4'],main_tables
    # Captions immediately follow their figure; introductory prose can also
    # start with "Figure 1" and must not be counted as a duplicate caption.
    fig_captions=re.findall(r'^!\[Figure (\d+)\]\([^\n]+\)\n\nFigure \1\s+[^\n]+',main_text,re.M)
    assert fig_captions==['1','2','3'],fig_captions
    assert len(re.findall(r'^!\[Figure ',main_text,re.M))==3
    s_tables=re.findall(r'^Table (S[\d.]+)\.?\s+[^\n]+\n\n\|',supp,re.M)
    expected=['S1','S2.1','S2.2','S2.3']+[f'S4.{n}' for n in range(1,6)]+[f'S5.{n}' for n in range(1,10)]
    assert [s.rstrip('.') for s in s_tables]==expected,s_tables
    checklist=load(R/'REVISION_CHECKLIST.json')
    assert len(checklist['items'])==42
    assert all(item['status'] in ['addressed','bounded_without_claim'] and item['evidence'] for item in checklist['items'])
    for item in checklist['items']:
        for entry in item['evidence']:
            # A locator has a real path followed by an optional human-readable anchor.
            path=entry.split(' :: ',1)[0]
            assert (R/path).exists(),(item['id'],entry)
    for item in docs:
        stem=Path(item['output']).stem
        meta=load(R/'verification/rendered'/stem/'render_metadata.json')
        images=list((R/'verification/rendered'/stem).glob('page-*.png'))
        assert len(images)==meta['pages'] and meta['pages']>0
    visual=load(R/'verification/visual_inspection.json')
    assert visual['status']=='PASS' and visual['all_document_pages_viewed']
    assert visual['figures_viewed']==['figure1_source_protocol','figure2_source_audit','figure3_controlled_diagnostics']
    ledger={'source_audit':source,'independent_inventory_and_policy':inventor,
      'functional_raw_recount':load(R/'verification/functional_results_independent_recount.json'),
      'historical_recount':load(R/'verification/historical_context.json'),
      'main_display_locators':{'source_layers':'§5.1; Figure 2',
       'unknown_causes':'§5.2; Table 2','joint_policies':'§5.3; Table 3',
       'functional_counts':'§5.4; Table 4; Figure 3',
       'source_restoration_behavior':'§5.5','legacy_context':'§5.6; Supplement S5'},
      'status':'PASS','boundary':'Exact retained-source and response arithmetic; AI semantic coding remains inspectable and unvalidated by experts.'}
    (R/'verification/final_result_ledger.json').write_text(json.dumps(ledger,indent=2),encoding='utf8')
    result={'status':'PASS','stage':'Revised evidence-audit manuscript and reproducibility delivery',
      'critique_items_closed':42,'original_input_hashes_unchanged':True,
      'main_tables':4,'main_figures':3,'supplement_tables':len(expected),
      'word_content_matches':True,'all_pages_and_figures_visually_reviewed':True,
      'files':{name:sha(R/'manuscript'/name) for name in texts},
      'limits':'Not a guarantee of acceptance, legal correctness, representative generalization or measured operational savings.'}
    (R/'verification/final_delivery_audit.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
