# -*- coding: utf-8 -*-
"""
传统RLHF全流程大图（简化版，减少交叉箭头）。
上半：预训练模型 → SFT → 收集人类偏好数据 → 训练奖励模型PM，主线直线箭头。
下半：PPO强化学习微调虚线大框，内部四个模型摆成2x2网格（policy/reward_model同一行，
value/ref_model同一行），减少斜向交叉；"策略模型由SFT初始化""参考模型是SFT冻结副本"
这类关系直接写进各自框内的说明文字，不再额外画穿插箭头。反馈箭头(优势→策略模型)
绕左侧弧线返回，避开中间的数据流箭头。
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, ax = new_fig(12.5, 7.6)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

FROZEN_EDGE = INK_SOFT
FROZEN_FILL = "#F2F2F2"

def box(x, y, w, h, label, sub=None, accent=False, frozen=False, fontsize=13):
    if accent:
        edge, fill, tcolor = ACCENT, ACCENT_FILL, ACCENT
    elif frozen:
        edge, fill, tcolor = FROZEN_EDGE, FROZEN_FILL, INK_SOFT
    else:
        edge, fill, tcolor = INK, BG, INK
    b = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.03",
        linewidth=1.6, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(b)
    if sub:
        text(ax, x, y + h*0.20, label, size=fontsize, color=tcolor, bold=True)
        text(ax, x, y - h*0.26, sub, size=fontsize*0.60, color=INK_SOFT)
    else:
        text(ax, x, y, label, size=fontsize, color=tcolor, bold=True)
    return (x, y, w, h)

def edge_point(b, tx, ty):
    x, y, w, h = b
    dx, dy = tx - x, ty - y
    if dx == 0 and dy == 0:
        return (x, y)
    hw, hh = w/2, h/2
    scale = min(abs(hw/dx) if dx else float("inf"), abs(hh/dy) if dy else float("inf"))
    return (x + dx*scale, y + dy*scale)

def arrow(b1, b2, label=None, label_offset=(0, 0.024), color=ARROW, lw=1.5,
          style="-|>", fontsize=9.3, label_color=None, rad=None):
    x1, y1, *_ = b1
    x2, y2, *_ = b2
    p1 = edge_point(b1, x2, y2)
    p2 = edge_point(b2, x1, y1)
    kw = dict(arrowstyle=style, mutation_scale=14, linewidth=lw, color=color,
              shrinkA=3, shrinkB=3)
    if rad is not None:
        kw["connectionstyle"] = f"arc3,rad={rad}"
    a = FancyArrowPatch(p1, p2, **kw)
    ax.add_patch(a)
    if label:
        mx, my = (p1[0]+p2[0])/2 + label_offset[0], (p1[1]+p2[1])/2 + label_offset[1]
        text(ax, mx, my, label, size=fontsize, color=label_color or INK_SOFT)

# ============ 标题（单独留出足够的行高，不与下方内容抢空间） ============
text(ax, 0.5, 0.965, "传统 RLHF 全流程", size=17, color=INK, bold=True)

# ============ 上半：主线性流程 ============
top_y = 0.845
b1 = box(0.10, top_y, 0.155, 0.095, "预训练模型", "自监督/下一词预测", fontsize=12)
b2 = box(0.335, top_y, 0.16, 0.095, "SFT监督微调", "人工问答对", fontsize=12)
b3 = box(0.60, top_y, 0.20, 0.095, "收集人类偏好数据", "同一问题两回答,标注哪个更好", fontsize=12)
b4 = box(0.865, top_y, 0.18, 0.095, "训练奖励模型 PM", "输入问答→输出标量分数", fontsize=12)

arrow(b1, b2)
arrow(b2, b3)
arrow(b3, b4)

# ============ 下半：PPO强化学习微调（虚线大框，内部2x2网格） ============
frame_x0, frame_y0, frame_x1, frame_y1 = 0.05, 0.05, 0.95, 0.68
frame = FancyBboxPatch(
    (frame_x0, frame_y0), frame_x1 - frame_x0, frame_y1 - frame_y0,
    boxstyle="round,pad=0.012,rounding_size=0.02",
    linewidth=1.3, linestyle=(0, (5, 3)), edgecolor=ACCENT_SOFT, facecolor="none",
)
ax.add_patch(frame)
text(ax, frame_x0 + 0.015, frame_y1 - 0.04, "PPO 强化学习微调", size=13.5, color=ACCENT, bold=True, ha="left")
text(ax, frame_x0 + 0.015, frame_y1 - 0.078, "同时维护 4 个模型，是 PPO 工程复杂度的来源", size=9, color=INK_SOFT, ha="left")

# 2x2网格：policy/reward_model同一行(上)，value/ref_model同一行(下)
policy = box(0.24, 0.46, 0.20, 0.115, "策略模型 π_θ", "训练中·由SFT初始化", accent=True, fontsize=12.5)
reward_model = box(0.70, 0.46, 0.19, 0.115, "奖励模型 PM", "冻结·对(x,y)打分 r", frozen=True, fontsize=12.5)
value = box(0.24, 0.18, 0.20, 0.115, "价值网络 V", "训练中·预测预期奖励", accent=True, fontsize=12.5)
ref_model = box(0.70, 0.18, 0.19, 0.115, "参考模型", "冻结的SFT副本·算KL惩罚", frozen=True, fontsize=12.5)
adv = box(0.47, 0.335, 0.16, 0.09, "优势 advantage", "r − KL惩罚 − 预期奖励", fontsize=10.5)

# 数据流：policy生成的回答y，分别送到reward_model打分、ref_model算KL
arrow(policy, reward_model, "回答 y →打分 r", label_offset=(0, 0.028))
arrow(policy, ref_model, "对比算 KL", label_offset=(0.05, -0.01), rad=0.18)

# reward_model / ref_model / value 三路汇入 advantage
arrow(reward_model, adv, "r", label_offset=(0.018, 0.012))
arrow(ref_model, adv, "−KL", label_offset=(0.02, -0.012))
arrow(value, adv, "预期奖励", label_offset=(-0.03, 0))

# advantage 反馈回策略模型：绕左侧弧线返回，避开中间数据流箭头
arrow(adv, policy, "策略梯度更新\n(clip概率比)", color=ACCENT, lw=1.8,
      label_offset=(-0.13, -0.02), fontsize=9.2, label_color=ACCENT, rad=0.35)

# 主线程"训练奖励模型PM" 接入框内的奖励模型（唯一连接上下两部分的箭头）
connector = FancyArrowPatch(
    (b4[0], top_y - b4[3]/2), (reward_model[0], reward_model[1] + reward_model[3]/2 + 0.035),
    arrowstyle="-|>", mutation_scale=14, linewidth=1.4, color=ARROW,
)
ax.add_patch(connector)

save(fig, "fig_rlhf_pipeline.png")
