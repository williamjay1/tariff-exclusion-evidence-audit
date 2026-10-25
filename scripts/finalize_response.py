"""Finalize the itemized response only after inference and visual QA exist."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def main():
    checks=load('verification/functional_results_independent_recount.json')
    visual=load('verification/visual_inspection.json')
    assert checks['status']==visual['status']=='PASS'
    assert load('artwork/qa/export_integrity.json')['status']=='PASS'
    assert (R/'experiments/outputs/experiment_final_summary.json').is_file()
    d,c=checks['reports'][1]['counts']['direct'],checks['reports'][1]['counts']['checklist']
    f=checks['reports'][2]['counts']['checklist']
    e=checks['reports'][3]['counts']
    restoration=checks['reports'][4]['counts']
    p=R/'REVISION_RESPONSE.md';s=p.read_text(encoding='utf8')
    changes={
      '**状态：中文回应初稿。来源审计、贡献重构和历史结果重释已写入现稿；正式功能运行、最终结果整合与交付 QA 尚待主代理补齐。**':'**状态：实质修订与最终交付核验完成。本说明逐项记录已落实的修改、实际核验依据和仍保留的研究边界。**',
      '下文节号对应当前英文稿片段。':'下文节号对应最终英文主文与补充材料；各源文件保留对应修订记录。',
      'S4结果表号已确定，但数值仍待完整运行与核验，不能将已分配表号等同于结果已完成。':'S4方法和结果表均已由完成的运行及复算材料填入。',
      '`【待主代理填入：……】` 表示尚未完成的结果或交付环节，不能据此将对应条目关闭。本说明不改写清单文件中的状态字段。':'42项覆盖记录保存在 `REVISION_CHECKLIST.json`；其中有界处理表示明确限制相应主张，不能解读为专家法律验证。',
      '**处理：实质基础已完成；正式功能结果仍待整合。**':'**处理：来源审计、参照重构与受控功能评价已纳入修订。**',
      '功能检验的完成状态见 C26–C29；本项不提前宣称最终经验论证已闭合。':'功能评价的实际结果及边界见 C26–C29。',
      '**处理：已完成任务与评价合同修改，正式得分待补。**':'**处理：任务、评价合同及完成后的功能结果已统一。**',
      '正式主终点数值的待填位置见 C27。':'主要功能终点及其实际分母见 C27和对应结果表。',
      '**处理：资格阶段已完成；正式运行完整性待最终确认。**':'**处理：资格与正式运行的接口完整性已分别核验。**',
      '**处理：输入及关系已构建冻结，正式运行正在完成。**':'**处理：冻结输入的两臂运行及真实来源补回诊断已完成。**',
      '**处理：指标与计分程序已冻结，正式数值待填。**':'**处理：正式功能指标、错误案例与独立原始输出复算已完成。**',
      'SI S4.3–S4.4及待填S4.7':'SI S4.3–S4.4及S4.7',
      '独立核查脚本 `scripts/verify_functional_results.py` 已存在，但存在脚本不等于正式结果已通过。':'独立核查脚本 `scripts/verify_functional_results.py` 已实际执行，原始JSON复算结果为PASS。',
      '**处理：已记录设计及更正；全量运行一致性待最终核验。**':'**处理：设计、勘误、三套参照计分及完整冻结一致性已核验。**',
      '**处理：样本口径已完成明确，正式结果分母待逐项核实。**':'**处理：所有正式结果分母及共享端点已逐项核实。**',
      '**处理：逻辑规则及旧错误解释已完成，正式行为得分待填。**':'**处理：合取规则、旧错误解释与正式保留反证行为已分别核验。**',
      '正式计算时间只在全量日志完成后按 C27/C39补齐。':'完整请求日志及S4记录实际计算过程；共享主机负荷波动使其不构成公平速度基准，也不换算专业人员工时。',
      '**处理：结构重构已完成，正式结果段待闭合。**':'**处理：主文已按来源—参照—功能评价的贡献链重组。**',
      '受控功能设计、来源结果、历史诊断的有限含义':'受控功能设计、来源结果、受控功能与真实来源补回结果、历史诊断的有限含义',
      '正式功能结果将置于来源结果与§5.6之间。具体结果章的最后论断必须等全量分析完成后填写，不能先固定胜出叙事。':'受控功能结果与来源补回行为位于§§5.4–5.5。最后论断依据完整运行，保留必要请求遗漏、无依据判断及整案正确遮蔽条件错误的结果。',
      '**处理：来源、库存、资格和历史诊断已有核验；正式结果及整体一致性尚未关闭。**':'**处理：来源、库存、资格、正式功能、历史诊断及交付内容一致性已完成核验。**',
      '正文图1/图2和现有表格以这些冻结材料为依据。不能把这些分项通过写成尚未生成的最终结果表已全部通过。':'正文三图及全部结果表均关联实际冻结材料；独立复算覆盖两臂原始回答、三套构造参照和独立的来源补回端点。',
      '**处理：本回应与实质稿件片段已完成，最终合稿及包待生成。**':'**处理：最终主文、补充材料、逐项回应和可复核材料已按交付门整理。**',
      '### C41｜保持清晰的矢量科研图，最终逐页查看尚待完成':'### C41｜清晰的矢量科研图与最终逐页实看',
      '**处理：本轮图1/图2已有源文件与局部QA；最终图件、表格和Word/PDF整体验证待填。**':'**处理：三幅最终图、可编辑表格和两份Word的逐页视觉核验均已完成。**',
      '**定位与核查：** 正文图1/图2；':'**定位与核查：** 正文图1–3；',
      '这些记录不是整稿视觉PASS。':'最终整稿视觉记录见 `verification/visual_inspection.json`，不沿用上一轮文件的状态。',
      '**处理：分项核验和当前片段实质审查已完成，最终投稿阶段决定待定。**':'**处理：最终内容及交付核验完成，阶段决定按本文限定身份作出。**',
      '当前已审片段没有未解决的材料性矛盾；这一结论不涵盖尚未完成的功能结果和最终文档。':'正式功能错误另经原始JSON只读复查，最终两份文档的内容与逐页显示也已核验。已知模型失败、参照边界和无专家验证均明确保留。',
    }
    for old,new in changes.items():
        assert old in s,old
        s=s.replace(old,new)
    bodies={
      'C24':f'**完成核验：** 正式direct与checklist各完成108/108，无无效、不完整、截断或输出上限停止。资格成功和正式功能得分分别报告；原始输出及提示白名单由 `verification/functional_results_independent_recount.json` 重解析核实。',
      'C26':f'**完成结果：** 构造诊断每臂108个唯一输入，共216次正式回答；来源恢复每臂8个端点，共16次回答。恢复属于四条件、三来源句、三裁决，未并入构造样本。来源恢复direct为7/8、checklist为6/8，两臂均3/4个前后关系正确，未显示清单的一致优势。电机条件direct仍为U→U、checklist为R→R，后者产生两个无依据R；相同补回句的功率条件却成功，因此仅报告该电机条件的状态与引用不相容，不猜测模型内部原因。全部原始响应与三套正式分析见 `experiments/outputs/experiment_final_summary.json` 及其逐文件记录；正文§§5.4–5.5、表4、图3与SI S4.7报告结果。',
      'C27':f'**实际功能结果：** direct整案{d["decision_correct"]}/{d["n"]}，checklist整案{c["decision_correct"]}/{c["n"]}、条件{c["condition_correct"]}/{c["condition_n"]}、可接受引用ID集合{c["citation_pass"]}/{c["citation_n"]}、确定条件引用{c["determinate_citation_pass"]}/{c["determinate_citation_n"]}、状态与引用联合{c["joint_citation_state_pass"]}/{c["condition_n"]}。缺口TP31/FP1/FN4；必要请求20/24、额外0、精确请求集104/108；自身聚合一致108/108并不等于正确。配对成功84/96与90/96，另物证据关系4/12与10/12，删除/恢复两臂均10/12。正文§5.4和表4、图3；SI表S4.3–S4.5及12源族结果；原始输出独立复算见 `verification/functional_results_independent_recount.json`。三个明确失败案例和全部五项条件错误另见 `literature/frozen_functional_error_audit.json`，未以整体分数掩盖。',
      'C28':f'**三套参照均保留：** 原冻结参照的checklist条件{f["condition_correct"]}/{f["condition_n"]}、引用{f["citation_pass"]}/{f["citation_n"]}；勘误参照分别为{c["condition_correct"]}/{c["condition_n"]}、{c["citation_pass"]}/{c["citation_n"]}，因此修正实际降低模型分数，整案及配对得分不变。整族排除后direct {e["direct"]["decision_correct"]}/99、checklist {e["checklist"]["decision_correct"]}/99、条件196/198、引用198/198。原始输入和预测未更改；三套分析、勘误时间戳、三条被取代试运行及输入/输出指纹都保留。',
      'C29':'**分母核对完成：** 主实验108输入/216条件/96共享端点关系；排除CF10后99输入/198条件/88关系；严格反证并存未知端点11个；恢复为8个孤立条件端点/4条前后关系，由3句来源支持4条件。历史73配对/208单元与库存397项分别列示，均不相加为总体样本；正文表1、表4与SI S1/S4保持相同口径。',
      'C31':f'**实际行为：** 11个有效R+U端点中direct和checklist均11/11保留R，checklist均不请求未知伴随条件；全部正式输入中仍有direct无依据S10/R0、checklist无依据S3/R1，条件层无依据S3/R1。自身聚合一致{c["overall_matches_predicted_aggregation"]}/{c["overall_aggregation_consistency_n"]}，状态与引用联合{c["joint_citation_state_pass"]}/{c["condition_n"]}。CF01_other_only把缺少A连接器信息错判为R；CF10_refute_missing虽整案R正确却漏掉teak支持wood，均作为正面失败证据保留。',
      'C39':'**最终一致性：** 正文为表1–4、图1–3；补充为表S1、S2.1–S2.3、S4.1–S4.5、S5.1–S5.9，共18表。摘要、结果段与图3采用勘误参照；原参照和整族排除分别明确列出。两份Word的段落和可编辑单元格与最终源稿逐项匹配，见 `verification/manuscript_assembly.json`、`verification/docx_content_audit.json`；原始功能复算和最终图件检查均为实际执行结果。',
      'C40':'**最终交付定位：** 主文为 `deliverables/Tariff_Evidence_Audit_20261023.docx`，补充材料为 `deliverables/Tariff_Evidence_Audit_Supplement_20261023.docx`，本文件为完整中文逐项回应。最终审稿复核ZIP随交付附上，内含脚本、原始回答、官方快照、来源/库存审计、全部参照版本与保留的历史档案；其清单及实际校验记录由 `scripts/build_review_package.py` 和 `scripts/verify_package.py` 生成。该包是本地复核材料，不声称已获得DOI或已公开发布。',
      'C41':'**最终出图与实看：** 图1为183×153 mm，图2为183×145 mm，图3为183×170 mm；每图均提供可编辑SVG、嵌入字体PDF和原生1200 dpi PNG。程序核对文字框相交、文字/数据区域与文字/线条交叉，另核查矢量非位图嵌入、字体及PNG像素/物理尺寸。三幅最终图与两份Word全部页面均经实际查看；详细页数与逐页记录见 `verification/visual_inspection.json`，导出检验见 `artwork/qa/export_integrity.json`。采用SciencePlots的Nature风格元素，不冒称严格符合Nature所有期刊排版规范。',
      'C42':'**阶段决定：修订稿与复核材料交付 GO；按来源审计资源与评价协议身份的投稿内容审查 GO。** 一句话贡献是让公开裁决到模型输入再到条件证据的选择可检查、可替换并可重算。来源、数字、引文、正式错误及最终图文已分别核验，关键剩余风险仍是AI语义赋值缺少独立海关专家验证、回溯目的性样本及受控构造的外推边界；这些边界限制主张，不被机械校验消除。目标为Artificial Intelligence and Law；实际投稿仍由作者确认署名、机构、资助和利益冲突等真实声明并完成期刊系统操作。本决定不保证录用，不将本项目升级为已验证的自动法律判断或业务收益研究。',
    }
    for item,body in bodies.items():
        pattern=r'\*\*【待主代理填入：'+item+r'—[^\n]+】\*\*'
        s,n=re.subn(pattern,lambda m:body,s)
        assert n==1,(item,n)
    old='正式功能运行完成后，最终结果应决定辅助功能可以说到何种程度。若输入恢复或参照修正缩小了原来的缺口，这应成为新结论；若checklist未提高整案分数，但可可靠定位额外错误，也须用实际指标证明这一较窄用途；若功能失败，同样保留。以上均不是预设结果。本轮结束条件是完成已有冻结运行与必要交付核验，不再为维护原叙事无限增加模型、种子或开发集回放。'
    assert old in s
    s=s.replace(old,'本轮按冻结设计报告实际功能结果、失败及参照敏感性。给定清单改善了所测整案与部分绑定行为，同时保留四项必要请求遗漏、一次无依据反驳和木框语义错误；结论限于实际检验的条件、证据、请求与配对端点，不据整案分数主张全面合取能力。来源补回是三案四条件的定点诊断，既不扩大为总体准确率，也不再无限追加模型或已检查材料的回放。')
    s=re.sub(r'\*\*待填项集中索引：[^\n]+', '**覆盖记录：C01–C42均有具体修改和文件定位。** C20、C28、C36、C42按有界主张处理；13项库存解释未解决、无专家验证和其他实质限制继续保留。最终主文与SI合稿位于 `manuscript/manuscript.md` 与 `manuscript/supplement.md`。',s)
    assert '待主代理' not in s and '待填' not in s
    assert len(re.findall(r'^### C\d\d｜',s,re.M))==42
    p.write_text(s,encoding='utf8')
    print('Final response: all 42 items retain explicit completion and evidence boundaries.')
if __name__=='__main__':main()
