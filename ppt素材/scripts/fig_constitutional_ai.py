# -*- coding: utf-8 -*-
"""
Constitutional AI (CAI) 两阶段流程大图。参考 notes_深入讲解.md 第4节。
左列：阶段1 SL-CAI（监督阶段），4个节点竖排——初始模型(纯helpfulness RLHF)
     → 生成初始回答 → 批评→修订(accent高亮:AI自我批评) → SL-CAI模型(checkpoint)
右侧：阶段2 RL-CAI（RLAIF）虚线容器，内部4个节点——SL-CAI模型采样两个回答
     → 按prompt类型分岔(harmless AI判断accent / helpfulness人类偏好frozen)
     → 汇总训练PM → PPO微调(checkpoint)
左右两栏各自内部走竖直方向的主干箭头，唯一跨栏的箭头是"SL-CAI模型→采样两个回答"，
横向从左栏顶部区域指向右栏顶部，天然协调，不需要跨越大片空白。
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, ax = new_fig(12.5, 9.6)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

FROZEN_EDGE = INK_SOFT
FROZEN_FILL = "#F2F2F2"

def box(x, y, w, h, label, sub=None, style_kind="plain", fontsize=11.2):
    """style_kind: plain / accent(AI新机制,蓝) / checkpoint(模型产出,黑色加粗边) / frozen(未改变,灰)"""
    if style_kind == "accent":
        edge, fill, tcolor, lw = ACCENT, ACCENT_FILL, ACCENT, 1.6
    elif style_kind == "checkpoint":
        edge, fill, tcolor, lw = INK, BG, INK, 2.3
    elif style_kind == "frozen":
        edge, fill, tcolor, lw = FROZEN_EDGE, FROZEN_FILL, INK_SOFT, 1.6
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
        text(ax, x, y - h*0.24, sub, size=fontsize*0.70, color=INK_SOFT, linespacing=1.45)
    else:
        text(ax, x, y, label, size=fontsize, color=tcolor, bold=True)
    return dict(x=x, y=y, w=w, h=h, shape="rect")

def edge_point(b, tx, ty):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    dx, dy = tx - x, ty - y
    if dx == 0 and dy == 0:
        return (x, y)
    hw, hh = w/2, h/2
    scale = min(abs(hw/dx) if dx else float("inf"), abs(hh/dy) if dy else float("inf"))
    return (x + dx*scale, y + dy*scale)

def straight(b1, b2, label=None, label_offset=(0, 0.028), color=ARROW, lw=1.5,
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
text(ax, 0.5, 0.975, "Constitutional AI (CAI)：两阶段自对齐流程", size=16, color=INK, bold=True)
text(ax, 0.5, 0.940, "两个阶段依次各执行一次，不像Self-Rewarding那样反复循环多轮", size=9.4, color=INK_SOFT)

# ============ 左列：阶段1 SL-CAI ============
text(ax, 0.22, 0.895, "阶段 1 · SL-CAI （监督阶段）", size=12, color=ACCENT, bold=True)

LX = 0.22
r1a = box(LX, 0.79, 0.36, 0.11, "初始模型",
          "纯helpfulness RLHF (尚未处理有害性)", style_kind="plain", fontsize=11.5)
r1b = box(LX, 0.635, 0.36, 0.11, "生成初始回答",
          "对红队提示 (约18.3万条)", style_kind="plain", fontsize=11.5)
r1c = box(LX, 0.465, 0.38, 0.145, "批评 → 修订",
          "随机抽1条宪法原则指出问题,\n重复4轮打磨（AI自我批评）",
          style_kind="accent", fontsize=11.5)
r1d = box(LX, 0.28, 0.38, 0.145, "SL-CAI 模型",
          "汇总修订后回答+helpfulness\n样本，做SFT训练得到",
          style_kind="checkpoint", fontsize=11.8)

straight(r1a, r1b)
straight(r1b, r1c)
straight(r1c, r1d)

# ============ 右侧：阶段2 RL-CAI 虚线容器 ============
frame_x0, frame_y0, frame_x1, frame_y1 = 0.44, 0.045, 0.98, 0.895
frame = FancyBboxPatch(
    (frame_x0, frame_y0), frame_x1 - frame_x0, frame_y1 - frame_y0,
    boxstyle="round,pad=0.012,rounding_size=0.018",
    linewidth=1.3, linestyle=(0, (5, 3)), edgecolor=ACCENT_SOFT, facecolor="none",
)
ax.add_patch(frame)
text(ax, frame_x0 + 0.02, frame_y1 - 0.045, "阶段 2 · RL-CAI （强化学习 / RLAIF）",
     size=12, color=ACCENT, bold=True, ha="left")
text(ax, frame_x0 + 0.02, frame_y1 - 0.088,
     "把「人类标注偏好」这一步，部分替换成「AI按宪法原则判断」",
     size=8.8, color=INK_SOFT, ha="left")

RX = 0.71
c1 = box(RX, 0.72, 0.42, 0.11, "SL-CAI模型 采样两个回答", style_kind="plain", fontsize=11.5)
straight(r1d, c1, extra_shrink=6)

c2a = box(0.605, 0.51, 0.24, 0.135, "harmless prompt",
          "AI按宪法原则判断\n哪个回答更好\n→ 生成AI偏好标签",
          style_kind="accent", fontsize=10.2)
c2b = box(0.895, 0.51, 0.21, 0.135, "helpfulness prompt",
          "沿用之前收集的\n人类偏好标签\n(未改变)",
          style_kind="frozen", fontsize=10.2)
straight(c1, c2a)
straight(c1, c2b)

c3 = box(RX, 0.30, 0.40, 0.135, "训练偏好模型 PM",
         "AI标注的harmless偏好 +\n人类标注的helpful偏好", style_kind="plain", fontsize=11.3)
straight(c2a, c3)
straight(c2b, c3)

c4 = box(RX, 0.135, 0.36, 0.115, "PPO 微调 → RL-CAI 模型",
         style_kind="checkpoint", fontsize=11.6)
straight(c3, c4)

save(fig, "fig_constitutional_ai.png")
