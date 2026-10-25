# 近邻全文比较与贡献重构（2026-10-23）

## 调研结论

本轮适宜保留的主线是：**公开行政裁决的来源构造如何改变规则适用评价中“可由输入支持的答案”；提供逐条件来源审计、输入恢复及对象绑定检查的可重算资源。** 这是一项法律 AI 评价与资源贡献。三值标签、证据跨度、规则分解、数值比较、风险诊断和抽取接符号推理均已有直接先例，不应单独作为创新声明。以下比较以原始全文中的方法、标注和实验章节为依据；没有把他人论文的自称“首次”当作已证实的优先权。此处为有界的近邻核验，不是系统综述。

| 工作及原始来源 | 问题、材料与目标 | 证据构造和抽取／推理 | 验证及主要边界 | 本研究需要具体增加什么 |
|---|---|---|---|---|
| Koreeda & Manning (2021), [ContractNLI](https://aclanthology.org/2021.findings-emnlp.164/) | 607 份 NDA；17 个固定假设；entailment / contradiction / not-mentioned | 对前两类定位句子／列表项证据，允许多段、不连续证据；联合证据识别和 NLI；定义与例外可跨段 | §§2,5–7，Appendix A.1.1；423/61/123 文档划分；oracle-evidence 对照与例外误差分析。不是全部律师标注：假设经 paralegal 审查，标注涉及计算语言学研究者及筛选后的众包人员 | 不再声称首次三值、证据对齐或证据 oracle。增加裁决来源中的属性事实与法律解释分离；被裁剪而非不存在的信息；逐条件输入版本的评价目标变更 |
| Holzenberger & Van Durme (2023), [Connecting Symbolic Statutory Reasoning with Legal Information Extraction](https://aclanthology.org/2023.nllp-1.12/) | SARA 美国税法半合成案例；判断法条适用及数额；提供人工形式化法律 | span-anchored 事件／实体及属性抽取 → 知识库 → Prolog；predicted / partial-gold / empty KB 对照；语义表示及模型可抽取范围明确 | §§3–7、附录；5 编码器、多次运行；修改4个有歧义案例，讨论 closed-world、隐含信息、事件／属性与论元错误。partial-gold 只是模型可表达子集，并非完整真实案件知识 | 最接近的直接先例。不能把对象绑定、抽取推理接口或分层 oracle 当作新发明。新增公共行政裁决中**来源片段的角色与准入规则**、裁剪所致信息缺失、不可安全恢复的解释性判断，以及这三类原因对评分的不同影响 |
| Medvedeva & McBride (2023), [Legal Judgment Prediction: If You Are Going to Do It, Do It Right](https://aclanthology.org/2023.nllp-1.9/) | 审查171篇2014至2023年8月的预测研究；任务对象、实际使用者、可获得输入是否对应未来预测 | 指出判决中的“事实”是选择和叙述后的材料；去掉结论或 reasoning 仍不能恢复审前信息环境 | 主文及任务核查讨论；仅12篇符合其面向未来预测的定义。此比例属于该历史样本，不是2026法律AI总体质量估计 | 不再把“判决文本不是未来输入”当新发现。将原则实施为可复核的行政裁决来源编码和可重算输入版本，且持续称 retrospective evaluation，不声称报关前部署效能 |
| Gogani-Khiabani et al. (2025), [VITA test](https://doi.org/10.1007/s10506-025-09465-7) | IRS 2022 Form 6744 的130题（60 basic、70 advanced）和260变体；六模型；T/F、选择、开放数值问答 | 原场景与两种保持税务答案的变体；不删关键税务信息，金额不变；场景内问题与直接提示；另报告初步 RAG | §§2.2–2.5、3、4、6；两位税务专家独立作答并协商，两个争议题由第三人解决；开放数值题更困难。变体稳定或不稳定都不能单独证明“理解而非记忆” | 不把金融／税务场景、数字推理困难或输入扰动称新。我们的变化必须有来源依据与明确方向：恢复关键独立属性应改变可判定性；无关材料应保持结论；保留不能由字面自动解决的解释边界 |
| Roy Choudhury et al. (2026), [CLAUSE](https://aclanthology.org/2026.findings-eacl.305/) | CUAD/ContractNLI 衍生的合同扰动；内部／外部法冲突×5类别，含 omission、术语错位、结构问题 | 生成、RAG 法源核对、自动过滤；定位跨度、说明及法源引用；存在原文／扰动文档输入设置差别 | §§2–5、Limitations、Appendix A.3；专家角色需分开：NLP人员审较大子集，持证法律从业者约100份文档。解释／引用评分含 LLM judges；不能称全部律师金标 | 不再宣称首次受控法律信息扰动、遗漏诊断或来源元数据。区别在于**已公布行政来源的筛选错误审计**，不是生成合同缺陷；恢复操作需能追溯原文且不偷渡裁决结论 |
| Lee et al. (2026), [TriBench-Ko](https://arxiv.org/abs/2605.03792)（预印本） | 1,414 个二值项目，31个司法任务×风险组合；公开韩国判决、改写事实和合成诉状；13模型 | 任务分摘要、检索、争点、证据；风险含遗漏、错误适用、过度顺从等；输入依任务变化 | §§3–5；前法官检查任务指令，三名持证律师审全部文本与标签，并检查信息完整性、法源和干扰项，争议不能解决则排除。这里只核验论文声称，未独立复现其数据 | 不声称首次任务风险矩阵或完整性审查。新增条件级来源轨迹与保留争议的操作参照；把“输入构造导致未知”同模型遗漏、原来源缺失及法律解释区分，并可重算不同输入／参照版本 |

## 必须据此修改的论证

1. **来源审计不能只看章节标题。** 独立的产品属性可能出现在 ANALYSIS 中；该位置不是排除事实的充分理由。允许恢复的是可逐字指认、独立于待预测适用结论的属性陈述；“因此满足该豁免”“属于某法律范畴”及机构适用结论不得伪装成属性补全。H330938 是否有连接器应由其他代理的完整来源编码证实，不能仅由旧备注决定。
2. **缺失必须拆因。** 区分研究者裁剪、公开来源根本未记载、外部定义未提供、部件／整品或测量对象未绑定、文本截断，以及编码争议。Unknown 是评价参照的结果，不是独立法律真值。说明不确定的原由比提升 unknown 准确率更有知识价值。[ContractNLI](https://aclanthology.org/2021.findings-emnlp.164/)、[Holzenberger & Van Durme](https://aclanthology.org/2023.nllp-1.12/) 已揭示相邻问题；新贡献是来源归属与可复算实例。
3. **行政结果 y 与输入条件参照 z 分开。** 恢复公开全文仍是事后材料，不等于当时私人档案，也不是前瞻报关输入。对 y 的不一致和对 z 的不一致应分别解释。[Medvedeva & McBride](https://aclanthology.org/2023.nllp-1.9/)
4. **配对操作验证知识增量。** 同一项目保留原输入、恢复独立属性、移除决定性属性、添加无关属性、改变决定性属性及对象绑定变体；每项预定应变／不变关系，并记录无法唯一确定的变体。这属于有解释的诊断，不是通过新参考标签反复挑选最高分。[VITA](https://doi.org/10.1007/s10506-025-09465-7)、[CLAUSE](https://aclanthology.org/2026.findings-eacl.305/) 已有相邻扰动验证，故本研究须证明来源审计对这些操作的必要性。
5. **库存支撑覆盖边界，不充当复杂度真值。** 397只是一个官方索引版本的转录范围；43条 code-only 与354条 product-description 必须分开。必要条件数取决于本体及拆分粒度；词法标记不能替代语义条件数。逐条件来源跨度、对象与关系编码比单一“复杂度”分数更可核查。

## 可供正文改写的贡献段（候选，不预报新结果）

Existing legal benchmarks already support evidence-linked inference, symbolic statutory reasoning, and controlled diagnostic perturbations. Our contribution concerns the construction of the evidence presented to those systems. We develop a source-auditing protocol for public administrative rulings that distinguishes independently reported product attributes from legal interpretations, applications of a rule, and the recorded disposition. The protocol tracks whether an unresolved condition reflects information removed during input construction, information absent from the public record, an unresolved definition, or an unresolved object or quantifier binding. By retaining source spans and alternative input versions, the resource makes the consequences of these choices recomputable. Its empirical value must be established through source-supported restoration and controlled sensitivity tests, rather than by treating agreement with an AI-produced reference as independent legal validation.

## 核验范围与尚存不确定

- 六篇均取得完整 PDF；本轮深读方法、数据构造、评价、误差／限制章节。ContractNLI 另核附录标注流程；Holzenberger 另核表示、partial-gold 与案例修订；CLAUSE 另核法律专家与 NLP 审查范围；TriBench-Ko 另核律师复核及输入构造。没有宣称重新运行这些研究或完整复核其全部参考文献。
- CLAUSE 正文“25% / 13,275 perturbation instances”与表1的文档／扰动计数口径不能直接对齐；此处不引用该比例或用它估算专家标注量。可确认的持证法律从业者审查规模为 Appendix A.3 所述约100份文档。
- TriBench-Ko 按检索时 arXiv v1 状态标为预印本；不虚构录用会议。最新进展检索是定向补充，未声称穷尽2026全部工作。
- Springer 直接 requests 下载返回的3038字节安全页不是文章全文；VITA 实际阅读依据为成功取得的 NSF 公共论文 PDF 和 Jina 读取的出版商正文；其余期刊范围／首页以成功 Jina及网页工具读取的官方页为准。

## 阶段判断

**重构阶段 CONDITIONAL，建议推进。** 资源／评价主线有可成立的实质差异，但增量不能仅靠重新命名“证据感知”或换税则语料。条件是实际完成来源角色编码、公开说明 AI 编码边界，并证明恢复、裁剪和对象绑定检查能区分不同失败原因。现有近邻不会自动否定该方向，也不能替代本项目自身的验证。
