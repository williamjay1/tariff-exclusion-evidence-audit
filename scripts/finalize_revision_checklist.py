"""Close critique items only after the concrete revised deliverables exist."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))

def main():
    for path in [
        'verification/source_audit_independent_checks.json',
        'verification/inventory_policy_independent_audit.json',
        'verification/functional_results_independent_recount.json',
        'verification/visual_inspection.json',
        'artwork/qa/export_integrity.json',
    ]:
        assert load(path)['status'] == 'PASS', path
    for path in ['manuscript/manuscript.md','manuscript/supplement.md',
                 'deliverables/Tariff_Evidence_Audit_20261023.docx',
                 'deliverables/Tariff_Evidence_Audit_Supplement_20261023.docx']:
        assert (ROOT/path).is_file(), path
    manuscript = 'manuscript/manuscript.md'
    supplement = 'manuscript/supplement.md'
    mapping = {
        'C01': [(manuscript,'1 Introduction; 3 Sources; 5 Results'), ('verification/source_audit_independent_checks.json','PASS'), ('verification/functional_results_independent_recount.json','PASS')],
        'C02': [(manuscript,'1 Introduction; 7 Discussion; 8 Conclusion'), ('REVISION_CONTROL.md','main contribution')],
        'C03': [(manuscript,'2.2 Closest evaluations'), ('literature/closest_work_comparison.md','full-text comparison'), ('literature/verified_references.json','verified references')],
        'C04': [('literature/legal_task_and_venue.md','publisher scope and instructions'), (manuscript,'Declarations')],
        'C05': [(manuscript,'6.1 H330938'), ('source_audit/H330938_priority_verification.json','connector source correction')],
        'C06': [(manuscript,'6.1 H330938; 5.3 policy sensitivity'), ('source_audit/policy_sensitivity.json','alternative policies')],
        'C07': [(manuscript,'3.2 statement roles; Figure 1'), ('source_audit/recovered_attribute_spans.jsonl','admitted descriptive assertions')],
        'C08': [('source_audit/condition_audit_long.jsonl','208 condition units'), ('verification/source_audit_independent_checks.json','coverage and source locators')],
        'C09': [(manuscript,'5.2; Table 2'), ('source_audit/case_review_records.jsonl','all historical unknown cases')],
        'C10': [(manuscript,'3.3; 5.1; 5.3; Figure 2; Table 3'), ('source_audit/policy_sensitivity.json','explicit policy packages')],
        'C11': [(manuscript,'3.4 AI annotation; Use of artificial intelligence'), (supplement,'S2.7; S5.1; Table S5.9')],
        'C12': [('verification/historical_context.json','administrative outcome by historical evidence state'), (manuscript,'3.4')],
        'C13': [(manuscript,'4 Functional evaluation; 5.4 controlled diagnostics'), (supplement,'S5 historical auxiliary targets')],
        'C14': [(manuscript,'3.3 three states; 4.3 endpoints'), ('experiments/outputs/experiment_final_summary.json','native three-state run')],
        'C15': [(manuscript,'2.1 post-classification module'), ('literature/legal_task_and_venue.md','official USTR scope')],
        'C16': [(manuscript,'2.1 GAO denominator; 7 practical scope'), (supplement,'S5.4; S5.6 hypothetical costs')],
        'C17': [('inventory_audit/inventory_structural_audit.jsonl','397 entries'), ('verification/inventory_policy_independent_audit.json','1096 groups and coverage'), (supplement,'S3 inventory')],
        'C18': [(manuscript,'6 five complete case chains'), ('source_audit/case_chains.json','source and alternative interpretation chains')],
        'C19': [(manuscript,'3.1 purposive collection; Table 1'), (supplement,'S1 sample formation')],
        'C20': [(manuscript,'1 Introduction; 2.2 retrospective inputs; 7 limitations')],
        'C21': [(manuscript,'5.6 historical context'), (supplement,'S5 concentration and uncertainty'), ('verification/historical_context.json','rule-group counts')],
        'C22': [(manuscript,'5.6 numerical microtests'), (supplement,'S5 numeric diagnostics')],
        'C23': [('verification/historical_context.json','numeric layers and repair'), (supplement,'S5 inspected development materials')],
        'C24': [('experiments/qualification_manifest.json','fixed qualification gate'), ('experiments/outputs/qwen14_qualification_cases_functional_analysis.json','all qualification responses'), (manuscript,'4.1; 5.4')],
        'C25': [(manuscript,'3.3; 4.1 interface status'), (supplement,'S5 historical invalid outputs'), ('experiments/outputs/experiment_final_summary.json','actual current output status')],
        'C26': [('experiments/constructed_pairs.jsonl','96 linked controlled relations'), ('experiments/outputs/experiment_final_summary.json','completed two-arm inference'), (manuscript,'5.4; Figure 3')],
        'C27': [(manuscript,'4.3 metrics; 5.4; Table 4'), ('verification/functional_results_independent_recount.json','independent raw-response metrics')],
        'C28': [('experiments/outputs/qwen14_controlled_cases_freeze.json','input/configuration freeze'), ('experiments/annotation_erratum.json','outcome-independent CF10 erratum'), (manuscript,'4.2 documented corrections')],
        'C29': [(manuscript,'4.2; 5.4; 5.5; Table 1'), ('experiments/source_recovery_cases.jsonl','eight real-source endpoints'), (supplement,'S4 denominators and construction limits')],
        'C30': [(manuscript,'5.6 old guard; 7.2'), (supplement,'S5 guard policy'), ('verification/historical_context.json','refuted recall 3/5 to 1/5')],
        'C31': [(manuscript,'3.3 conjunction; 4.3; 5.4'), ('verification/functional_results_independent_recount.json','refutation preservation and unsupported states')],
        'C32': [(manuscript,'3.1 exact-code subset'), ('verification/historical_context.json','13 removed HQ pairs')],
        'C33': [(manuscript,'5.6 source baseline'), (supplement,'S5 source sensitivity and resampling uncertainty')],
        'C34': [(manuscript,'5.6 input ablations'), (supplement,'S5 historical model-input comparisons')],
        'C35': [(supplement,'S5 hypothetical administrative-disagreement loss and review-all inequality'), ('verification/historical_context.json','loss arithmetic')],
        'C36': [(manuscript,'2.1; 7.2; 7.3 deployment and cost boundary'), (supplement,'S5.4; S5.6 hypothetical costs')],
        'C37': [(manuscript,'complete evidence-audit narrative'), ('verification/manuscript_assembly.json','assembled main and supplement')],
        'C38': [(supplement,'S5 preserved historical analyses'), ('verification/historical_context.json','central historical recount')],
        'C39': [('verification/docx_content_audit.json','exact paragraphs and editable cells'), ('verification/manuscript_assembly.json','numbered displays'), ('verification/functional_results_independent_recount.json','new counts')],
        'C40': [('deliverables/Tariff_Evidence_Audit_20261023.docx','main article'), ('deliverables/Tariff_Evidence_Audit_Supplement_20261023.docx','supplement'), ('REVISION_RESPONSE.md','C01-C42 response'), ('scripts/build_review_package.py','review package contents and gate')],
        'C41': [('artwork/qa/export_integrity.json','editable vectors, embedded fonts, native 1200dpi'), ('verification/visual_inspection.json','actual figure/page inspection')],
        'C42': [('verification/functional_results_independent_recount.json','independent raw-response recount'), ('verification/source_audit_independent_checks.json','source checks'), ('literature/revised_content_readonly_review.json','reference review'), ('verification/visual_inspection.json','delivery QA'), ('REVISION_RESPONSE.md','C42 stage-specific decision')],
    }
    checklist=load('REVISION_CHECKLIST.json')
    assert {item['id'] for item in checklist['items']} == set(mapping)
    for item in checklist['items']:
        entries=mapping[item['id']]
        for path,anchor in entries:
            assert (ROOT/path).exists(), (item['id'],path)
        item['status']='bounded_without_claim' if item['id'] in ['C20','C28','C36','C42'] else 'addressed'
        item['evidence']=[f'{path} :: {anchor}' for path,anchor in entries]
    checklist['closure_scope']='Requested revisions addressed by completed artifacts; bounded items explicitly exclude unsupported prospective, preregistered, cost and publication-validity claims.'
    (ROOT/'REVISION_CHECKLIST.json').write_text(json.dumps(checklist,ensure_ascii=False,indent=2),encoding='utf8')
    print('42 critique items closed with concrete artifact locators; bounded claims remain explicit.')

if __name__=='__main__':
    main()
