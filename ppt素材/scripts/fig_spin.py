# -*- coding: utf-8 -*-
"""
SPIN (Self-Play Fine-Tuning) 大图。参考 notes_深入讲解.md 第6节。
主体：4个节点摆成正方形四角，顺时针闭环，不产生交叉线——
  TL=①θ_t(冻结,对手玩家) -> TR=②采样负样本y' -> BR=③SPIN损失(accent) ->
  BL=④梯度下降更新→θ_{t+1}(checkpoint) -> 闭环回到TL(θ_{t+1}变成下一轮θ_t)
顶部单独交代"没有独立判别器网络"这个常见误解澄清；右下角小面板放SPIN损失公式。
风格与 fig_self_rewarding.py 一致（同一套box/straight写法、配色语义）。
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, ax = new_fig(12.2, 9.0)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

def box(x, y, w, h, label, sub=None, style_kind="plain", fontsize=11.0):
    if style_kind == "accent":
        edge, fill, tcolor, lw = ACCENT, ACCENT_FILL, ACCENT, 1.6
    elif style_kind == "checkpoint":
        edge, fill, tcolor, lw = INK, BG, INK, 2.2
    elif style_kind == "frozen":
        edge, fill, tcolor, lw = INK_SOFT, "#F2F2F2", INK_SOFT, 1.6
    else:
        edge, fill, tcolor, lw = INK, BG, INK, 1.5
    b = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.010,rounding_size=0.020",
        linewidth=lw, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(b)
    if sub:
        text(ax, x, y + h*0.20, label, size=fontsize, color=tcolor, bold=True)
        text(ax, x, y - h*0.25, sub, size=fontsize*0.72, color=INK_SOFT, linespacing=1.4)
    else:
        text(ax, x, y, label, size=fontsize, color=tcolor, bold=True)
    return dict(x=x, y=y, w=w, h=h)

def edge_point(b, tx, ty):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    dx, dy = tx - x, ty - y
    if dx == 0 and dy == 0:
        return (x, y)
    hw, hh = w/2, h/2
    scale = min(abs(hw/dx) if dx else float("inf"), abs(hh/dy) if dy else float("inf"))
    return (x + dx*scale, y + dy*scale)

def straight(b1, b2, label=None, label_offset=(0, 0.03), color=ARROW, lw=1.5,
             fontsize=8.8, label_color=None, extra_shrink=8):
    x1, y1 = b1["x"], b1["y"]
    x2, y2 = b2["x"], b2["y"]
    p1 = edge_point(b1, x2, y2)
    p2 = edge_point(b2, x1, y1)
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=13, linewidth=lw,
                         color=color, shrinkA=extra_shrink, shrinkB=extra_shrink)
    ax.add_patch(a)
    if label:
        mx = (p1[0]+p2[0])/2 + label_offset[0]
        my = (p1[1]+p2[1])/2 + label_offset[1]
        text(ax, mx, my, label, size=fontsize, color=label_color or INK_SOFT)

# ============ 标题 ============
text(ax, 0.5, 0.978, "SPIN：Self-Play Fine-Tuning", size=16.5, color=INK, bold=True)
text(ax, 0.5, 0.938,
     "只有一个正在训练的模型——没有独立判别器网络，「判别」只是类比，体现在损失函数的数学形式里",
     size=9.4, color=INK_SOFT)

# ============ 起点 ============
start = box(0.35, 0.855, 0.40, 0.075,
            "初始化：$\\theta_0$ = 某个已经SFT过的模型",
            style_kind="plain", fontsize=10.6)

# ============ 4个节点：正方形四角，顺时针闭环 ============
TL = (0.16, 0.66)  # ① θ_t 冻结/对手玩家
TR = (0.57, 0.66)  # ② 采样负样本 y'
BR = (0.57, 0.3)  # ③ SPIN损失
BL = (0.16, 0.3)  # ④ 梯度下降 → θ_{t+1}
gw, gh = 0.30, 0.155

n1 = box(*TL, gw, gh, "① $\\theta_t$（冻结）",
         "上一轮训好的参数，复制一份\n当「对手玩家」，只当参照基准",
         style_kind="frozen", fontsize=10.4)
n2 = box(*TR, gw, gh, "② 采样负样本 $y'$",
         "用 $\\theta_t$ 对SFT问题 $x_i$\n生成回答 $y'\\sim p_{\\theta_t}(\\cdot|x_i)$",
         style_kind="plain", fontsize=10.4)
n3 = box(*BR, gw, gh, "③ SPIN 损失",
         "拉高 $y$（人类标准答案）/\n压低 $y'$ 的相对似然",
         style_kind="accent", fontsize=10.4)
n4 = box(*BL, gw, gh, "④ 梯度下降更新",
         "「主玩家」$\\theta$ 被训练\n→ 得到 $\\theta_{t+1}$",
         style_kind="checkpoint", fontsize=10.4)

straight(start, n1, extra_shrink=6)
straight(n1, n2, extra_shrink=7)
straight(n2, n3, extra_shrink=7)
straight(n3, n4, extra_shrink=7)
straight(n4, n1, "$\\theta_{t+1}$ 变成下一轮的 $\\theta_t$，$\\theta_t$「退休」",
         label_offset=(0, 0.0), color=ACCENT, lw=1.7, label_color=ACCENT,
         fontsize=8.4, extra_shrink=8)

# ============ 底部说明 ============
text(ax, 0.35, 0.05,
     "关键：第0轮 $\\theta$ 和 $\\theta_0$ 数值相同，损失非零起点(约0.693)，但梯度不为零——$\\theta_t$ 被冻结(detach)，\n"
     "训练照样能推进，不是「没意义」",
     size=8.2, color=INK_SOFT, linespacing=1.5)

# ============ 右下角：SPIN损失公式面板 ============
panel_x0, panel_y0, panel_w, panel_h = 0.775, 0.045, 0.205, 0.78
panel = FancyBboxPatch((panel_x0, panel_y0), panel_w, panel_h,
                        boxstyle="round,pad=0.008,rounding_size=0.016",
                        linewidth=1.0, edgecolor=ACCENT_SOFT, facecolor="#FAFAF8",
                        linestyle=(0, (3, 2)))
ax.add_patch(panel)
cx2 = panel_x0 + panel_w/2
text(ax, cx2, panel_y0 + panel_h - 0.035, "③ SPIN 损失函数", size=10.5, color=ACCENT, bold=True)

mini_w = panel_w - 0.03

boxA = box(cx2, panel_y0 + panel_h - 0.195, mini_w, 0.165,
           "$A=\\lambda[\\log p_\\theta(y|x)$\n$-\\log p_{\\theta_t}(y|x)]$",
           style_kind="accent", fontsize=9.6)
text(ax, cx2, panel_y0 + panel_h - 0.25, "好例子($y$=标准答案)\n的相对分数", size=7.6, color=INK_SOFT, linespacing=1.4)

boxB = box(cx2, panel_y0 + panel_h - 0.465, mini_w, 0.165,
           "$B=\\lambda[\\log p_\\theta(y'|x)$\n$-\\log p_{\\theta_t}(y'|x)]$",
           style_kind="plain", fontsize=9.6)
text(ax, cx2, panel_y0 + panel_h - 0.52, "差例子($y'$=$\\theta_t$自产)\n的相对分数", size=7.6, color=INK_SOFT, linespacing=1.4)

boxL = box(cx2, panel_y0 + panel_h - 0.705, mini_w, 0.125,
           "$\\mathcal{L}_{SPIN}=-\\log\\,\\sigma(A-B)$",
           style_kind="checkpoint", fontsize=10.0)

straight(boxA, boxB, extra_shrink=10, lw=1.3)
straight(boxB, boxL, extra_shrink=10, lw=1.3)

save(fig, "fig_spin.png")
