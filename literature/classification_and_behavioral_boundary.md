# 税号分类与输入证据审计的界线

核验日期：2026-10-23。补充四篇直接相关文献，服务既定贡献比较，不声称系统综述。HSCodeComp 的任务、来源、标注和评价章节已实际阅读官方全文；CheckList 的§§1–2已读全文。HSGraphAgent 本轮核验官方摘要及元数据，Lee等2024通过作者机构页面核验摘要及元数据，未把两者标成全文已读。

| 研究 | 已验证的任务与来源 | 与本研究相接之处 | 可成立的区分 |
|---|---|---|---|
|Lan等，HSCodeComp，ACL2026|§3–4：真实电商产品标题、属性、类目、图像和价格输入；美国税则、专家规则与CROSS裁决知识；目标为10位税号。632产品，由26名专业人员组成的标注队伍执行双人标注、资深裁决及抽查程序。|层级规则、模糊属性、条件例外和事实依据都已被视为核心难点，不能声称首次发现这些能力问题。|我们固定已给税号和候选豁免，评价来源裁剪、独立属性与解释的分界及证据状态变化；不与其多模态税号准确率竞争。|
|Lee等，Explainable Product Classification for Customs，ACM TIST2024|作者机构摘要：与韩国海关合作，向925个有挑战性的6位子目提供可解释建议；评价5,000件分类申请及32名海关专家的用户研究。|海关分类支持系统和专业用户价值已有直接先例。|本研究没有专家用户研究，不将离线诊断称为已证明的操作效率收益；提供可审计、可复算的来源构造资源。|
|Xia等，HSGraphAgent，ACL2026|官方摘要：利用显式HS知识图谱、层级关系与分类排除规则，引导4位及6位税号选择。|图结构约束、可追踪规则路径和排除条款并非空白。|HS税目之间的分类排除与Section301附加税的产品豁免是不同决策模块；不能仅凭“exclusion”同词推断任务相同。|
|Ribeiro等，CheckList，ACL2020|§2：能力×测试类型矩阵，最小功能、保持不变、方向性预期；比较扰动前后的预测关系，支持有标签或适当无标签的行为检验。|本研究的无关信息不变、关键条件改变、删除／恢复测试属于已有行为测试传统。|新内容应落在行政来源的事实／解释角色审核、干预是否合法及参考状态能否随信息变化上，而非声称发明扰动评价。|

对应一手来源：[HSCodeComp全文](https://aclanthology.org/2026.acl-long.937.pdf)、[Lee等作者机构记录](https://pure.kaist.ac.kr/en/publications/explainable-product-classification-for-customs/)、[HSGraphAgent官方记录](https://aclanthology.org/2026.acl-long.2072/)、[CheckList全文](https://aclanthology.org/2020.acl-main.442.pdf)。

## 可直接整合的英文段落

Customs classification already provides substantial precedents for rule-guided AI. HSCodeComp combines commercial product profiles, tariff rules and historical customs rulings to evaluate ten-digit classification (Lan et al., 2026). Explainable classification support has also been evaluated with customs experts (Lee et al., 2024), while HSGraphAgent constrains classification through a hierarchy and regulatory exclusion relations (Xia et al., 2026). Our task begins with a supplied base classification and candidate Section 301 exclusion. It examines whether the retained product evidence supports the additional scope conditions, and how source selection changes that answer. This distinction does not remove domain interpretation or establish prospective availability of adjudicated facts. It isolates a source-construction problem that classification accuracy does not resolve. The paired tests follow the behavioral-testing tradition of CheckList (Ribeiro et al., 2020); their contribution is the documented connection between administrative source roles, admissible information changes and input-conditioned reference states.

## 不能据此写出的主张

- 未全面读HSGraphAgent或Lee2024全文，不断言它们完全没有类似错误分析；这里只核验任务目标差别。
- 不把HSCodeComp中的官方历史裁决知识当作本研究首先使用CROSS的证据；恰恰应承认该来源已有使用。
- 不将行为测试的成功推广为完整法律适用能力或真实海关部署效益。
- 多位专业人员参与的近邻基准与本项目AI银标签验证层级不同，不能用同一个“gold”词掩盖差异。
