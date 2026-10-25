# 英文内容精修建议（限定只读）

检查了五份当前稿件：`front_matter_and_methods.md`、`source_results.md`、`historical_main.md`、`cases_and_discussion.md`、`supplement_overview.md`。本次只检查读者理解与措辞边界，没有重复文献或技术审计，没有查看正式模型部分输出，也没有编辑稿件。

下列六处均给出可直接采用的替换句。其余两份 `source_results.md` 与 `historical_main.md` 的术语和论证衔接未发现本轮必须修改的问题；不为凑数增加一般润色。

## 1. 开篇明确“接纳”是评价输入的选择

位置：`front_matter_and_methods.md`，Introduction 第一句。

原句：

> An answer to a legal applicability question depends on what has been admitted as evidence.

替换：

> In a text-based evaluation of legal applicability, an answer depends on which source statements are admitted to the model input.

理由：明确本文所说的 admission 是来源到评价输入的选择，避免法律读者先理解为法院的正式证据可采性裁定。后文的实际法律任务边界保持不变。

## 2. 不能把应当变化的关系称为 invariance

位置：`front_matter_and_methods.md`，Introduction，功能诊断概述末句。

原句：

> A system cannot earn invariance credit merely by returning unknown at both ends of a change that requires a different answer.

替换：

> Returning unknown at both endpoints earns no credit when the specified transformation requires the answer to change.

理由：原句把 invariance 与 change-required 关系放在一起，容易让读者误解关系评分。替换保留原意，也与 §4.3 的 pair-success 定义一致。

## 3. 请求只在需要时产生

位置：`front_matter_and_methods.md`，§2.1。

原句：

> The output is a condition audit and, where a defensible logical representation is available, a restricted-input conclusion with a specific information request.

替换：

> The output is a condition audit and, where a defensible logical representation is available, a conclusion based on the admitted input, accompanied by a specific information request when needed.

理由：原句可被理解为每个结论都附带请求，与决定性反驳后不再请求的信息策略相冲突。替换同时把 restricted-input conclusion 解释成普通英文。

## 4. 图注不暗示必要条件已经获得外部法律验证

位置：`front_matter_and_methods.md`，Figure 1 图注最后一句。

原句：

> Whole-case conjunction is restricted to verified mandatory conditions; unresolved alternatives and exceptions require their own representation.

替换：

> Whole-case conjunction is used only where the audit represents the conditions as jointly necessary under the stated interpretation policy; unresolved alternatives and exceptions require their own representation.

理由：verified 容易比正文的 AI silver 审计承诺更强。替换把依据落在实际声明的解释政策与合取结构上，不增加新限制或新验证要求。

## 5. 资格通过证明有限功能，不排除正式任务中的接口失败

位置：`front_matter_and_methods.md`，§4.1 第二段。

原句：

> This procedure excludes a plainly malfunctioning interface as the sole explanation for formal failures; it does not establish customs expertise.

替换：

> Passing these checks establishes basic interface function on the qualification cases, without establishing customs expertise or ruling out task-specific failures on the formal inputs.

理由：excludes 的表达过强，容易把有限资格题解释为对全部正式失败原因的排除。替换仍清楚说明资格测试的正面作用，不弱化已经完成的验证。

## 6. 直接说清 CF10 暴露的是语义支持没有随删句消失

位置：`cases_and_discussion.md`，§7.3 最后一段。

原句：

> The frame-species erratum shows that even a transparent diagnostic can initially overstate uniqueness of evidence.

替换：

> The frame-species erratum shows that deleting one explicit statement need not remove semantic support for its condition: the remaining teak-frame statement still establishes that the frame is wooden.

理由：uniqueness of evidence 抽象且容易理解成重复引用问题；实际勘误来自 teak 蕴涵 wooden。替换能让读者直接理解为何一个条件状态和多个可接受引用集合同时发生变化。

## c1 构造边界与 CF10 自洽性结论

当前 §4.2 的 c1/c2 边界成立，不建议改动其设计说明。仅核对冻结输入定义、未读模型输出后确认：每族九个正式变体中，除原 `refute_missing` 外，c2 都为 supported；`other_only` 也仍保留目标产品的 c2 支持事实，并非两个条件一起未知。原十二组 `refute_missing` 的 c2 为 unknown，CF10 勘误把其中一项改为 supported，因此修正后只剩十一组。整案参照决定不变，c1 主导整案变化、不能据此证明普遍多条件整合的说明准确。

方法中的勘误段、讨论及补充概述均保持：输入与预测不改、修改一个条件参照与七个引用端点、保留原参照和整族排除敏感性。没有发现内在矛盾。第6条仅让其实际语义原因更易懂。
