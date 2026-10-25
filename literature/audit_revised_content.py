"""Bounded read-only manuscript check; no fitting, inference or label changes."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import json, hashlib

N=Path(r'D:\MLWork\tariff_scope_20261007\revision_20261023')
def load(p): return json.loads((N/p).read_text(encoding='utf-8'))
def rows(p): return [json.loads(x) for x in (N/p).read_text(encoding='utf-8').splitlines() if x.strip()]
conditions=rows('source_audit/condition_audit_long.jsonl')
cases=rows('source_audit/case_audit.jsonl')
summary=load('source_audit/source_audit_summary.json')
policy=load('source_audit/policy_sensitivity.json')
assert len(conditions)==208 and len(cases)==73
assert len({x['ruling_id'] for x in cases})==67
assert dict(Counter(x['reference_tier'] for x in conditions))==summary['reference_tier_counts']
assert dict(Counter(x['strict_excerpt_state'] for x in conditions))==summary['strict_excerpt_condition_counts']
assert dict(Counter(x['strict_full_source_state'] for x in conditions))==summary['strict_full_condition_counts']
assert dict(Counter(x['strict_excerpt_state'] for x in cases))==summary['strict_case_excerpt_counts']
assert dict(Counter(x['strict_full_source_state'] for x in cases))==summary['strict_case_full_counts']
safe=[x for x in cases if x['safe_flat_conjunction']]
assert len(safe)==58 and sum(x['logic_unresolved'] for x in cases)==15
assert Counter(x['strict_full_source_state'] for x in safe)=={'support':10,'refute':3,'unknown':45}
restored=[x['condition_key'] for x in conditions if x['strict_excerpt_state']!=x['strict_full_source_state']]
assert set(restored)=={'H330938_1:c4','H322923_1:c2','H340899_1:c3','H340899_1:c4'}
for p in policy['explicit_policy_packages']:
    assert len(p['cases'])==58
    assert Counter(x['state'] for x in p['cases'])==p['counts']
assert [p['counts'] for p in policy['explicit_policy_packages']]==[
    {'unknown':45,'support':10,'refute':3},
    {'support':17,'unknown':33,'refute':8},
    {'refute':5,'unknown':34,'support':19}]
unknown_ids={x['case_id'] for x in cases if x['historical_operational_case_state']=='unknown'}
unknown_conditions=[x for x in conditions if x['case_id'] in unknown_ids]
assert len(unknown_ids)==47 and len(unknown_conditions)==137
assert sum(x['historical_operational_condition_state']=='unknown' for x in unknown_conditions)==59
assert sum(x['strict_excerpt_state']=='unknown' for x in unknown_conditions)==67
for group in summary['unknown_provenance_sets'].values():
    assert len(set(group['case_ids']))==group['case_n']
    assert len(set(group['condition_keys']))==group['condition_n']
    assert set(group['case_ids'])<=unknown_ids

source_rows=rows('source_audit/source_paragraphs.jsonl')
sensor=[x for x in source_rows if x['ruling_id']=='H333673' and x['paragraph_id']=='p046'][0]
assert 'only the front light sensor uses passive infrared detection' in sensor['text']
relay=[x for x in source_rows if x['ruling_id']=='N311039' and x['paragraph_id'] in ['p014','p015','p016','p017']]
assert len(relay)==4
for r, coil in zip(relay,['12 VAC','110 VDC','48 VDC','48 VDC']):
    assert 'coil voltage rating of '+coil in r['text'] and '277 VAC' in r['text']
assert 6000*0.45359237==2721.55422

paths=['manuscript/cases_and_discussion.md','manuscript/source_results.md','source_audit/condition_audit_long.jsonl','source_audit/case_audit.jsonl','source_audit/source_audit_summary.json','source_audit/policy_sensitivity.json','inventory_audit/inventory_validation.json']
report={
 'checked_utc':datetime.now(timezone.utc).isoformat(),
 'status':'PASS_WITH_NONBLOCKING_WORDING_SUGGESTION',
 'scope':'Read-only source/legal-contribution and numerical integration check of two manuscript sections; no review of partial formal model outputs and no new model evaluation.',
 'material_discrepancies':[],
 'recomputed':{'cases':73,'conditions':208,'sources':67,'safe_conjunctions':58,'logic_unresolved':15,'tier_counts':summary['reference_tier_counts'],'excerpt_states':summary['strict_excerpt_condition_counts'],'restored_states':summary['strict_full_condition_counts'],'direct_restored_keys':restored,'historical_unknown_case_n':47,'historical_unknown_condition_n':59,'strict_unknown_within_historical_unknown_case_n':67,'policy_packages':[{k:v for k,v in p.items() if k in ['name','counts']} for p in policy['explicit_policy_packages']]},
 'legal_scope_checks':[
  {'item':'administrative disposition versus admitted evidence','finding':'Distinct endpoints are explicit; no reassessment of legal entitlement is claimed.'},
  {'item':'H333673 passive infrared wording','finding':'Confirmed as an independently identifiable agency descriptive assertion in p046, raw text span 12120–12273; manuscript does not infer passivity from receiver-diode wording alone.'},
  {'item':'H318593 dimensions and capacity','finding':'Handle exclusion and own-mass/load distinction preserved; 6000 lb conversion is arithmetically exact using 0.45359237 kg/lb.'},
  {'item':'N311039 quantified ratings','finding':'Four coil/contact pairs and currents match source paragraphs p014–p017. All-listed-products refutation is explicitly a declared task, not a new independent entitlement for each product.'},
  {'item':'H333371 competing composition','finding':'48% party and approximately76% laboratory assertions retained; alternative evidentiary-priority policies are not presented as equally authoritative legal recommendations.'},
  {'item':'controlled demonstration','finding':'Supplied conditions, limited output schema, no automatic rule parser, no importer/workflow outcomes and no expert validation are stated. Final outcome-specific statements must still be aligned after complete experiment outputs are frozen.'},
  {'item':'inventory coverage','finding':'397/354/43/1096 and16/397 correspond to retained audit. Zero-based index convention now explicit in owned inventory supplement/report.'}],
 'nonblocking_suggestion':{'location':'cases_and_discussion.md §7.2 first sentence','current':'A supplied condition list offers an operational advantage when the task is to inspect what a decision rests on.','suggested':'A supplied condition list makes the reported basis of a decision more inspectable.','reason':'Avoid reading operational advantage as measured workflow benefit; following sentences already limit the claim, so this does not alter the substantive conclusion.'},
 'input_sha256':{p:hashlib.sha256((N/p).read_bytes()).hexdigest() for p in paths},
 'boundary':'Independent AI review of traceable records, not independent expert legal validation. Numeric verification here is deterministic recounting; no inference rerun or statistical refitting.'
}
(N/'literature/revised_content_readonly_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
md='''# 两节主稿的限定只读审核

结论：未发现材料性数字错误、法律结论越界或受控程序身份混淆。审核对象为 `cases_and_discussion.md` 与 `source_results.md`；没有读取尚未冻结的正式模型输出，没有运行新实验或修改主稿。

## 已实际复算与来源核验

- 从逐行记录重新计数：73例、208条件、67裁决；132 direct、45 interpretive、19 insufficient、12 disputed。两项 nonbinding 因而不计入130项直接可评分核心。
- strict excerpt 的125/5/76加2项不适用，以及恢复后的129/5/72加2项不适用，与主文一致。四项直接恢复定位在 H330938:c4、H322923:c2、H340899:c3/c4，属于三个案例；58项安全外层合取仍为10/3/45，15例逻辑未解决另列。
- 历史47例 unknown 对应137项条件，历史 unknown 为59项，strict excerpt unknown 为67项。五类原因分别5/7、10/12、36/38、11/12、5/5，重叠集合的行数与唯一键均一致。正文未把集合误当互斥分区。
- 三个政策包从58例逐案状态重新计数为10/3/45、17/8/33、19/5/34；正文把它们称诊断政策，未称权威法律解释。逐案可能数的边界也明确不是联合可达范围。
- H318593 的61×30.2×15.2 cm注明不含手柄，26.4 kg是自身质量；6000 lb到2721.55422 kg是载荷换算，两者未混用。N311039四个产品的线圈/触点电压与电流回查了源段 p014–p017，集合refutation明确限制在所声明的 all-listed-products 任务。
- H333371的48%与约76%分别保留当事人与实验室归属。H333673关于passive infrared的表述来自p046可独立定位的机构描述句，而不是由receiver diode自行推断；原裁决的法律结论没有被当作属性证据复制进条件。
- 库存397/354/43、1,096粗组及16/397覆盖与已通过的库存核验一致；已在我负责的库存补充材料与报告明确JSON零基索引约定。

## 贡献与程序边界

两节区分了行政结果、所接纳文本的支持状态和权威法律解释。公开文本恢复没有被写成对进口申报真实资料缺口的估计；AI语义标签没有被写成专家金标。受控程序明确使用给定条件，不能代表自动规则构建、现实完整业务准确率或专业工作时间节约。部署、经济收益与跨域表现也保持为尚未观察的外推边界。最终正式实验冻结后仍应由负责代理逐项对齐实际模型失败与成本；本审核不提前认证这些结果。

## 一项非阻断措辞建议

§7.2首句 “A supplied condition list offers an operational advantage…” 可改为 “A supplied condition list makes the reported basis of a decision more inspectable.” 前者可能被快速阅读为已证明业务优势；后续段落已经限定得当，因此这属于精确化而非主线缺陷。我没有修改主稿。

本次判断基于公开原文定位、AI编码记录和确定性复算，不替代独立法律专家验证。JSON报告保留本轮审查的输入指纹和全部关键检查项。
'''
(N/'literature/revised_content_readonly_review.md').write_text(md,encoding='utf-8')
print(json.dumps({'status':report['status'],'material_discrepancies':0,'cases':len(cases),'conditions':len(conditions),'output':'literature/revised_content_readonly_review.md'},ensure_ascii=False))
