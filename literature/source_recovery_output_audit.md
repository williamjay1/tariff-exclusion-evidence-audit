# 八个来源恢复端点的原始回答复核

结论：完整文件的两项SHA与模型代理交付值一致；各8个唯一端点均重新解析原始JSON，和保留的parsed一致，无无效、截断或输出限额事件。独立复算确认direct为7/8，checklist为6/8；两者均成功完成3/4个恢复关系。checklist有2次无依据反驳、0次无依据支持。没有重跑推理或修改任何参照。

| 孤立条件 | 严格参照前→后 | Direct前→后 | Checklist前→后 | Checklist引用/请求 |
|---|---|---|---|---|
| H330938:c4，无连接器 | U→S | U→S | U→S | 前请求c4；后引用新增f2且不请求 |
| H322923:c2，三或四轮 | U→S | U→S | U→S | 前请求c2；后引用新增f2且不请求 |
| H340899:c3，自带电动机 | U→S | U→U | R→R | 前引f1；后引f1、f2；两个端点均无请求 |
| H340899:c4，功率不超过1500W | U→S | U→S | U→S | 前请求c4；后引用新增f2且不请求 |

S、R、U分别表示supported、refuted、unknown。这是每次仅给一个孤立条件的诊断，不是完整排除条款或整个裁决的结论。

## 电机失败的准确解释边界

H340899:c3恢复后新增的f2明确包含“self-contained electric motors”。Direct仍返回unknown；checklist仍返回refuted，并把包含该明确支持语句的f2列入引用。可据此报告标签与所引用陈述不相容、恢复后未出现预期更新。原始输出只有状态和事实ID，没有理由文本，因此不能断言模型混淆了电池供电与自带电机、误解背包结构、忽略了整个段落或采用了某种内部法律分类。

同一恢复陈述还包含功率上限，在单独测试H340899:c4时，两臂都由unknown更新为supported。这个可见差别进一步要求将失败限定到本次电机谓词，不写成两个接口对整个恢复段落都没有反应。c3的恢复前unknown来自严格直接文本参照，历史编码曾把它推断为supported，正文应继续保留这个参照版本说明。

可用英文：

> Both interfaces made the expected unknown-to-supported update for connector absence, wheel count and the power ceiling. Neither updated correctly for the self-contained-motor condition. The direct interface remained unknown, whereas the checklist remained refuted and, after restoration, cited the added statement that explicitly describes self-contained electric motors. The responses provide no explanation, so the cause of this inconsistency cannot be identified from the retained outputs. The same added passage supported a correct update for the separately tested power condition. These four pairs therefore document condition-specific responses to source restoration, rather than a general restoration success rate or whole-exclusion accuracy.

机器可读复核见 `source_recovery_output_audit.json`，包含逐对原回答、恢复语句及输出SHA。首次打印遇Windows终端GBK无法表示字符的接口问题，UTF-8输出设置修正后脚本实际exit0；该问题不涉及输入、模型输出、参照或复算结果。
