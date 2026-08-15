# 第9页：前沿一 —— BigBang

## 标题
前沿一：BigBang —— 可验证前沿任务的自合成

## 正文要点
- 出发点：LLM越来越强后，继续进步的瓶颈变成"训练任务的天花板由人类知识划定"——人类能出的题，模型很快就能学完
- 提出"可验证前沿任务"（verifiable frontier tasks）：处于当前知识边界、但候选解可以用形式化方法/计算/仿真/领域工具客观判定对错的问题
- 核心架构：generator agent（不断提出并求解越来越难的科研/技术问题）+ critic agent（评估正确性、可验证性、难度、可扩展性、多样性）
- 用held-out的真实研究任务校准critic，引导合成数据分布持续进化
- 通过generator-critic的持续对抗式协同，任务生成和评估策略本身也在被迭代改进——论文称之为"早期的数据层面递归自我改进"
- 效果：从Qwen3.6-35B-A3B起步训练，在科研、推理、代码、工具使用等基准上综合表现介于DeepSeek V4 Flash(284B)和V4 Pro(1.6T)之间

## 图片
fig09_bigbang_loop.png（4:3）
- 画双agent闭环：[Generator: 提出+求解前沿任务] ⇄ [Critic: 评估正确性/难度/多样性] → [训练数据] → [模型能力提升] → 反馈回Generator/Critic（用虚线表示"生成/评估策略本身也被更新"）
- 旁边加一个小分支：[Held-out真实研究任务] → 校准Critic

## 引用论文
BigBang Team, *BigBang: Pursuing Open-Ended Intelligence through Self-Evolving Synthesis of Verifiable Frontier Tasks*, 2026

## 演讲提示
和第8页的谱系对应：BigBang改进的对象不只是"策略"（回答问题的能力），还包括"生成器和评估器本身"，这是它比前面所有方向都更接近"开放式RSI"的地方。可以强调"可验证"这个词的分量——它是在回答第2页提出的核心问题"谁来判断候选的好坏"：BigBang选择用held-out真实任务不断校准critic，试图避免"自己骗自己"。
