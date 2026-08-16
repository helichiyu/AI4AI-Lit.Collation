# -*- coding: utf-8 -*-
"""风格自检图：验证字体/配色/箭头效果，画一个通用的三节点闭环。跑完看 figures/_demo_style_check.png"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, ax = new_fig(5, 5)

nodes = {
    "生成": (0.5, 0.82),
    "评估": (0.82, 0.32),
    "更新": (0.18, 0.32),
}

for i, (label, (x, y)) in enumerate(nodes.items()):
    accent = (i == 0)
    box = FancyBboxPatch(
        (x - 0.16, y - 0.08), 0.32, 0.16,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.6,
        edgecolor=ACCENT if accent else INK,
        facecolor=ACCENT_FILL if accent else BG,
    )
    ax.add_patch(box)
    text(ax, x, y, label, size=15, color=ACCENT if accent else INK, bold=accent)

def curved_arrow(p1, p2, rad=0.25):
    arrow = FancyArrowPatch(
        p1, p2,
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=1.4,
        color=ARROW,
        shrinkA=22, shrinkB=22,
    )
    ax.add_patch(arrow)

pts = list(nodes.values())
curved_arrow(pts[0], pts[1])
curved_arrow(pts[1], pts[2])
curved_arrow(pts[2], pts[0])

text(ax, 0.5, 0.06, "示意：自迭代闭环（生成 → 评估 → 更新）", size=11, color=INK_SOFT)

save(fig, "_demo_style_check.png")
