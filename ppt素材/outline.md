# 自迭代模型 —— PPT大纲总表

风格约束：每页最多"标题 + 正文 + 图片"三个元素；不做目录页/总览页/总结页/参考文献页；直接逐个讲具体理论。图片比例按内容形状决定，不统一为16:9。

共13页。

| # | 标题 | 一句话定位 | 是否配图 | 图片建议 | 主要参考论文 |
|---|------|-----------|---------|---------|------------|
| 1 | 封面 | 标题/副标题/日期/你的名字 | 否 | - | - |
| 2 | 自迭代模型是什么 | 数据/反馈来源从"人类"变为"模型自己"，闭环取代开环 | 是 | 横向对比图，约4:3，居中偏下，配合上方文字 | - |
| 3 | 理论原型：AlphaGo Zero的自对弈闭环 | 不靠人类棋谱，自己和自己下棋，策略网络自我迭代变强 | 是 | 环形闭环图，接近正方形1:1，放页面右侧，文字在左 | Mastering the game of Go without human knowledge |
| 4 | 方向一：自生成数据（STaR / Self-Instruct） | 模型自己出题+答题+筛选，自举训练数据 | 是 | 横向流程条，约16:6宽幅，放正文下方 | STaR; Self-Instruct |
| 5 | 方向二：自我反馈迭代精炼（Self-Refine） | 同一模型"生成→批评→修改"多轮迭代，不更新参数 | 是 | 三节点循环图，约1:1，放右侧 | Self-Refine |
| 6 | 方向三：自对齐与自奖励（CAI / Self-Rewarding） | 用AI当评委代替人类反馈，模型给自己的输出打分 | 是 | 双层闭环图（监督阶段+RL阶段），约4:3 | Constitutional AI; Self-Rewarding Language Models |
| 7 | 方向四：自对弈微调（SPIN） | 新模型与自己的旧版本对抗，弱模型练成强模型 | 是 | 迭代对抗图，约3:2 | Self-Play Fine-Tuning (SPIN) |
| 8 | 方向五：从有限自我修正到递归自我改进 | 用综述视角把方向一~四串成一条进阶谱系，引出"前沿"部分 | 是 | 阶梯/谱系图，约16:9宽幅 | A Survey on Self-Evolution of LLMs; Recursive Self-Improvement in AI (2026) |
| 9 | 前沿一：BigBang —— 可验证前沿任务的自合成 | generator + critic 对抗式协同进化，任务难度持续自升级 | 是 | 架构闭环图，约4:3 | BigBang |
| 10 | 前沿二：Absolute Zero —— 零数据自对弈推理 | 一个模型同时出题（maximize learning progress）和解题，代码执行器做验证 | 是 | 自博弈循环图，约1:1 | Absolute Zero |
| 11 | 前沿三：AlphaEvolve —— 进化式代码智能体 | LLM流水线+进化搜索+自动评估器，发现新算法/新公式 | 是 | 进化循环图（变异-评估-选择），约3:2 | AlphaEvolve |
| 12 | 具身智能中的自迭代：现状 | 自迭代思想进入机器人领域——策略自我改进、任务自生成、失败驱动的重采样 | 是 | 环境交互-策略更新闭环图，约4:3 | ENPIRE; Self-Evolving Learning for Embodied AI (Criticality Model); AGT-World; Self-Improving Robot Policy w/ Compositional World Model |
| 13 | 具身智能中的自迭代：挑战与展望 | 安全性、验证难度、仿真-真实差距、样本效率 | 是 | 挑战雷达图或分栏对比图，约4:3 | 同上 + Recursive Self-Improvement in AI (2026) |

## 页面间的叙事逻辑

1. 先给"自迭代"下一个清晰定义（第2页），建立"闭环 vs 开环"的核心区分。
2. 用AlphaGo Zero（第3页）讲清楚这个概念的最初理论原型：自我博弈+自己当老师。
3. 五个方向（第4-8页）是AlphaGo Zero思想在LLM时代的分化：自生成数据 → 自我反馈 → 自对齐/自奖励 → 自对弈微调 → 综述给出的进阶谱系（自然过渡到"前沿"）。
4. 前沿三篇（第9-11页）是2026.8为止最具代表性的突破：BigBang（任务自合成）、Absolute Zero（零数据自对弈）、AlphaEvolve（进化式发现），三者分别对应"造任务"、"造数据"、"造算法"三种不同的自迭代对象。
5. 最后两页把视角切到具身智能，讲清楚同样的闭环思想目前如何落地到机器人（现状），以及尚未解决的问题（展望）。

## 图片文件清单（对应 figures/ 目录）

| 图片文件名 | 对应页 | 建议比例 |
|-----------|-------|---------|
| fig02_open_vs_closed_loop.png | 2 | 4:3 |
| fig03_alphago_zero_loop.png | 3 | 1:1 |
| fig04_self_generate_pipeline.png | 4 | 16:6 (宽幅条状) |
| fig05_self_refine_loop.png | 5 | 1:1 |
| fig06_rlaif_self_reward.png | 6 | 4:3 |
| fig07_spin_selfplay.png | 7 | 3:2 |
| fig08_rsi_ladder.png | 8 | 16:9 |
| fig09_bigbang_loop.png | 9 | 4:3 |
| fig10_absolute_zero_loop.png | 10 | 1:1 |
| fig11_alphaevolve_loop.png | 11 | 3:2 |
| fig12_embodied_selfimprove_loop.png | 12 | 4:3 |
| fig13_embodied_challenges.png | 13 | 4:3 |

共12张图（第1页封面不配图）。
