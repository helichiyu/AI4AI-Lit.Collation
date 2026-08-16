# -*- coding: utf-8 -*-
"""
"自迭代模型统一框架"配图。
节点布局回到第一版的斜向环状构图（生成器/候选/评估者/更新对象四个点错开摆放），
但箭头改成直线（沿两个框的边界连接，不用弧线）；评估信号可靠性色块条也放回
第一版的位置/大小（挂在"评估者"节点右下方、不单独占一整行），只是把此前漏画的
三个等级标签补在色块下方。
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

fig, ax = new_fig(6.4, 5.0)
ax.set_ylim(-0.06, 1.0)  # 给底部标签留一点余量

# ---------- 四个核心节点：斜向环状布局（比第一版略大一点，避免文字溢出） ----------
box_w, box_h = 0.32, 0.175

nodes = [
    ("生成器",   0.22, 0.72, "模型自身/历史版本"),
    ("候选",     0.62, 0.86, "数据·策略·任务"),
    ("评估者",   0.78, 0.42, "规则/裁判/自评"),
    ("更新对象", 0.32, 0.24, "输出/参数/评估器"),
]

positions = {}
for name, x, y, sub in nodes:
    accent = (name == "评估者")
    box = FancyBboxPatch(
        (x - box_w/2, y - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.014,rounding_size=0.038",
        linewidth=1.7,
        edgecolor=ACCENT if accent else INK,
        facecolor=ACCENT_FILL if accent else BG,
    )
    ax.add_patch(box)
    text(ax, x, y + 0.035, name, size=14, color=ACCENT if accent else INK, bold=True)
    text(ax, x, y - 0.038, sub, size=8.3, color="#3E5A70" if accent else INK_SOFT)
    positions[name] = (x, y)

# ---------- 直线箭头：连接两个矩形边界上、朝向对方的点，不用弧线 ----------
def rect_edge_point(cx, cy, w, h, tx, ty):
    """从矩形中心(cx,cy)朝目标点(tx,ty)方向，求与矩形边界的交点。"""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return (cx, cy)
    hw, hh = w / 2, h / 2
    scale = min(
        abs(hw / dx) if dx != 0 else float("inf"),
        abs(hh / dy) if dy != 0 else float("inf"),
    )
    return (cx + dx * scale, cy + dy * scale)

order = ["生成器", "候选", "评估者", "更新对象", "生成器"]
for i in range(len(order) - 1):
    n1, n2 = order[i], order[i + 1]
    x1, y1 = positions[n1]
    x2, y2 = positions[n2]
    p1 = rect_edge_point(x1, y1, box_w, box_h, x2, y2)
    p2 = rect_edge_point(x2, y2, box_w, box_h, x1, y1)
    arrow = FancyArrowPatch(
        p1, p2,
        arrowstyle="-|>",
        mutation_scale=15,
        linewidth=1.5,
        color=ARROW,
        shrinkA=4, shrinkB=4,
    )
    ax.add_patch(arrow)

# ---------- 评估信号可靠性：色块条放回第一版的位置/大小，标签补在下方 ----------
bar_x0, bar_y0 = 0.60, 0.10
bar_w, bar_h = 0.36, 0.045

levels = [
    ("形式化验证器", ACCENT),
    ("裁判/奖励", ACCENT_SOFT),
    ("模型自评", "#C9D3DA"),
]
seg_w = bar_w / len(levels)
for i, (label, color) in enumerate(levels):
    x0 = bar_x0 + i * seg_w
    rect = Rectangle((x0, bar_y0), seg_w, bar_h,
                      facecolor=color, edgecolor=INK, linewidth=0.9)
    ax.add_patch(rect)
    text(ax, x0 + seg_w/2, bar_y0 - 0.045, label, size=7.6, color=INK)

text(ax, bar_x0 + bar_w/2, bar_y0 + bar_h + 0.03, "评估信号可靠性", size=8.6, color=INK_SOFT)

save(fig, "fig_self_iteration_framework.png")
