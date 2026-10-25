# 科研绘图来源核验

2026-10-23通过agent-reach的GitHub路线实际查询上游；[SciencePlots](https://github.com/garrettj403/SciencePlots)当前HEAD仍为 `b9b16959570bd2fbc9ff5118bacc423c3bddd592`，本地已安装版本2.2.2，无新增安装。[固定版本nature样式](https://github.com/garrettj403/SciencePlots/blob/b9b16959570bd2fbc9ff5118bacc423c3bddd592/src/scienceplots/styles/journals/nature.mplstyle)和[MIT许可证](https://github.com/garrettj403/SciencePlots/blob/b9b16959570bd2fbc9ff5118bacc423c3bddd592/LICENSE)均已下载核验。它是社区维护的样式包，不是Nature官方合规认证；默认字体优先DejaVu Sans、字号7pt、图宽3.3inch，不能仅加载style就声称已经使用Arial或183mm宽。

[Nature官方尺寸与导出指南](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/)给出双栏183mm、单栏89mm、通常最高170mm；要求文字可编辑、不转轮廓、嵌入TrueType字体，优先Arial或Helvetica并保持高对比。官方列出的普通文字范围为5–7pt；这与本项目为可读性采用的更大字号并非同一要求，宜称“参考Nature设计原则”，不要声称逐项遵从Nature投稿规格。

[Nature官方制作规格](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)要求多面板字母为8pt加粗小写，避免文字重叠和繁杂背景，采用可辨色配色，并说明插值提高dpi不能改善真实细节。项目的PDF/SVG应保留向量文字与线条；1200dpi位图应从绘图代码按最终尺寸直接导出，而不是把300dpi预览放大。向量图没有与位图相同的固定dpi概念。

原始材料新增保存于F盘只读目录，字节数、URL、SHA及本地版本记录见 `supplementary_source_manifest.json`。未改图片、统计或用户技能。
