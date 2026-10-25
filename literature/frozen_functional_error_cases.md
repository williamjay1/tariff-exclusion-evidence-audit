# 冻结受控输出的限定错误审读

已对108条 checklist 原始 `raw_output` 重新解析JSON，并逐条确认与保留的 `parsed` 一致；仅使用冻结 `controlled_cases.jsonl` 和结果前 `annotation_erratum.json`。未读取来源恢复任务的任何部分输出，未修改数据、模型或正式统计。

逐条件独立对照得到216项中5项状态错误、3项可接受引用集合不符、4项必要请求遗漏、0项额外请求。这些是不同维度，不能把3个引用错误当作全部无依据决定的数量：预期unknown的空引用集合有时与模型的空引用相同，但模型同时错误地产生了确定状态。状态与证据联合指标用于暴露这一差别。

以下最多三个代表案例均可回到原输入和逐字输出；解释只涉及可见行为，不推断模型内部原因。

## 1. CF01_other_only：目标对象证据缺失被输出为反驳

- 要求：A无连接器；A电压超过1000V。
- 事实：f1称B无连接器，f2称A为2000V。
- 参照：c1 unknown、c2 supported，整案unknown，请求c1。
- checklist：c1 refuted，引用空；c2 supported并引用f2；整案refuted，无请求。
- direct：整案supported，也错。

准确解释：在目标A的连接器属性没有给出的情况下，checklist输出了无事实支持的反驳，并遗漏必要请求。此例不能写成“checklist把B的无连接器事实当成A的支持证据”：它实际没有引用B，并输出了反向的refuted。两臂在同一输入上产生方向不同的过度确定结论。

可用英文：

> In CF01_other_only, the input states that Product B lacks connectors and that Product A is rated at 2,000 V. It says nothing about A's connectors. The checklist nevertheless marks A's connector condition as refuted, supplies no supporting fact, and omits the necessary request. The direct arm instead returns supported. Both answers exceed the evidence, in opposite directions.

## 2. CF10_deleted：一般材料类别不支持具体排除条件

- 要求：A框架不是柚木；A有木框。
- 唯一事实f2：A是带木框的软垫餐椅。
- 参照：c1 unknown、c2 supported，整案unknown，请求c1。
- checklist：用f2支持c1与c2，整案supported，无请求。
- direct：整案supported，也错。

准确解释：木框支持第二条件，不能排除属于木材的柚木，因而不支持第一条件。错误是引用内容不蕴涵目标要求，而不是错误引用了另一个产品；本输入没有B。原本语法正确、事实ID有效的引用仍不等于正确证据关系。

可用英文：

> In CF10_deleted, the only fact establishes a wooden frame. The checklist cites that fact for both the wooden-frame requirement and the requirement that the frame not be teak. The first inference is supported; the second is not, because the stated material category does not exclude teak. The model therefore produces an unsupported affirmative decision and fails to request the missing species information despite using a valid fact identifier.

## 3. CF10_refute_missing：正确整案结论掩盖伴随条件遗漏

- 要求与上例相同；唯一事实f1：A框架由柚木制成。
- 勘误参照：c1 refuted、c2 supported；两者均可由f1建立；整案refuted，无请求。
- checklist：c1 refuted并引用f1，但c2 unknown、引用空；整案refuted，无请求。
- direct：整案refuted，正确。

准确解释：teak对“不是柚木”构成反例，同时蕴涵wood，模型遗漏后一个关系。整体否定以及不再请求都仍正确，说明整案准确无法覆盖伴随条件和证据关系。该条是结果前勘误新增的一项状态错误，使原冻结参照的212/216变为修正参照的211/216；不能将这次降分描述为模型行为改变。

可用英文：

> CF10_refute_missing illustrates the opposite entailment direction. A teak-frame statement refutes the exclusion of teak and also supports the wooden-frame condition. The checklist recognizes the decisive refutation but leaves the companion condition unknown with no evidence. Its overall decision and empty request set are correct. Applying the pre-outcome semantic erratum exposes the missed companion inference without changing any model response or whole-input reference decision.

逐条机器可读错误记录：`frozen_functional_error_audit.json`。本审读只解释冻结受控句子的状态和引用关系，不把这些构造案例称为新的真实海关裁决、专家金标或现实业务效益验证。
