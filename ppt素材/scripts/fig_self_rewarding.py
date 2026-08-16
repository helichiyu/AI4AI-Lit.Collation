# -*- coding: utf-8 -*-
"""
Self-Rewarding Language Models 大图。参考 notes_深入讲解.md 第5节。
主体：①在顶部单独一个节点，②③④⑤按 "5 2 / 4 3" 摆放（左上=⑤,右上=②,右下=③,左下=④），
沿 ①->②(右上)->③(右下)->④(左下)->⑤(左上)->回到① 形成一个顺时针矩形环，
不再需要外侧折线绕回，闭环箭头本身就是矩形的最后一条边，天然不交叉。
次要：右下角DPO公式面板，改成用带边框的小方块盛放公式（跟主图节点风格一致），
填满面板的纵向空间，不再是大片空白+悬浮文字。
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, ax = new_fig(12.2, 9.4)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

def box(x, y, w, h, label, sub=None, style_kind="plain", fontsize=11.0):
    if style_kind == "accent":
        edge, fill, tcolor, lw = ACCENT, ACCENT_FILL, ACCENT, 1.6
    elif style_kind == "checkpoint":
        edge, fill, tcolor, lw = INK, BG, INK, 2.2
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
text(ax, 0.5, 0.978, "Self-Rewarding Language Models", size=16.5, color=INK, bold=True)
text(ax, 0.5, 0.940, "同一个模型既是选手也是评委：每轮自己出题、自己答题、自己打分、自己训练自己",
     size=9.6, color=INK_SOFT)

# ============ 起点 ============
start = box(0.35, 0.875, 0.42, 0.08,
            "预训练模型 + 少量人类种子数据 → SFT → 种子模型 $M_0$",
            style_kind="plain", fontsize=10.4)

# ============ ① 单独一个节点，在网格正上方中间 ============
n1 = box(0.35, 0.735, 0.30, 0.115, "① 生成新prompt",
         "$M_t$ 自己生成一批instruction-\nfollowing测试问题",
         style_kind="plain", fontsize=10.6)
straight(start, n1, "$M_0$ 作为起点", label_offset=(0.12, 0), extra_shrink=6)

# ============ ②③④⑤ 按 "5 2 / 4 3" 摆放：左上=⑤ 右上=② 右下=③ 左下=④ ============
TL = (0.2, 0.535)  # ⑤
TR = (0.57, 0.535)  # ②
BR = (0.57, 0.2)   # ③
BL = (0.2, 0.2)   # ④
gw, gh = 0.26, 0.155

n2 = box(*TR, gw, gh, "② 生成候选回答",
         "对每个新prompt生成\n4个候选回答", style_kind="plain", fontsize=10.6)
n3 = box(*BR, gw, gh, "③ 自我打分",
         "LLM-as-Judge模板\n评分细则打0-5分",
         style_kind="accent", fontsize=10.6)
n4 = box(*BL, gw, gh, "④ 构造偏好对",
         "最高分为chosen $y_w$\n最低分为rejected $y_l$",
         style_kind="plain", fontsize=10.6)
n5 = box(*TL, gw, gh, "⑤ DPO训练",
         "拉高好回答/压低差回答的\n相对似然 → 得到 $M_{t+1}$",
         style_kind="accent", fontsize=10.6)

# 顺时针矩形环：①(顶部)->②(右上)->③(右下)->④(左下)->⑤(左上)->回到①
straight(n1, n2, extra_shrink=7)                 # 顶部 -> 右上
straight(n2, n3, extra_shrink=7)                 # 右上 -> 右下
straight(n3, n4, extra_shrink=7)                 # 右下 -> 左下
straight(n4, n5, extra_shrink=7)                 # 左下 -> 左上
straight(n5, n1, "$M_{t+1}$：重复步骤①-⑤",       # 左上 -> 顶部，闭环，天然不交叉
         label_offset=(-0.135, 0.03), color=ACCENT, lw=1.7, label_color=ACCENT,
         fontsize=8.8, extra_shrink=8)

# ============ 底部局限说明 ============
text(ax, 0.35, 0.045,
     "局限：论文只跑了3轮，未验证长期是否饱和/崩塌；\n「评委」与「选手」是同一模型，存在系统性偏差自我强化的风险",
     size=8.4, color=INK_SOFT, linespacing=1.5)

# ============ 右下角：DPO公式面板（用带边框小方块盛放公式，填满纵向空间） ============
panel_x0, panel_y0, panel_w, panel_h = 0.775, 0.045, 0.205, 0.83
panel = FancyBboxPatch((panel_x0, panel_y0), panel_w, panel_h,
                        boxstyle="round,pad=0.008,rounding_size=0.016",
                        linewidth=1.0, edgecolor=ACCENT_SOFT, facecolor="#FAFAF8",
                        linestyle=(0, (3, 2)))
ax.add_patch(panel)
cx2 = panel_x0 + panel_w/2
text(ax, cx2, panel_y0 + panel_h - 0.035, "⑤ DPO 损失函数", size=10.5, color=ACCENT, bold=True)

mini_w = panel_w - 0.03

boxA = box(cx2, panel_y0 + panel_h - 0.185, mini_w, 0.155,
           "$A=\\beta[\\log p_\\theta(y_w|x)$\n$-\\log p_{ref}(y_w|x)]$",
           style_kind="accent", fontsize=9.8)
text(ax, cx2, panel_y0 + panel_h - 0.285, "好回答的相对分数", size=8.0, color=INK_SOFT)

boxB = box(cx2, panel_y0 + panel_h - 0.44, mini_w, 0.155,
           "$B=\\beta[\\log p_\\theta(y_l|x)$\n$-\\log p_{ref}(y_l|x)]$",
           style_kind="plain", fontsize=9.8)
text(ax, cx2, panel_y0 + panel_h - 0.54, "差回答的相对分数", size=8.0, color=INK_SOFT)

boxL = box(cx2, panel_y0 + panel_h - 0.685, mini_w, 0.13,
           "$\\mathcal{L}_{DPO}=-\\log\\,\\sigma(A-B)$",
           style_kind="checkpoint", fontsize=10.5)

straight(boxA, boxB, extra_shrink=10, lw=1.3)
straight(boxB, boxL, extra_shrink=10, lw=1.3)

text(ax, cx2, panel_y0 + panel_h - 0.725,
     "A比B领先越多\n损失越小", size=8.2, color=ACCENT, linespacing=1.5)

text(ax, cx2, panel_y0 + 0.03,
     "$\\beta$ 越大，偏好\n信号越强", size=7.8, color=INK_SOFT, linespacing=1.5)

save(fig, "fig_self_rewarding.png")
