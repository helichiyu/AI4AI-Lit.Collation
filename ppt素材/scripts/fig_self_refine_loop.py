# -*- coding: utf-8 -*-
"""
Self-Refine 中图：四个主节点摆成菱形（gen左/fb上/refine右/stop下），整体轮廓呈菱形。
"否"分支走左侧外侧直角折线绕回fb——折线的x坐标(0.04)严格小于Generator左边界(0.10)，
留出安全间隙，不会贴着/穿过Generator。整体下移，与顶部标题/副标题拉开间距。
所有箭头标签用"垂直于线段方向、偏向图形外侧"的自动定位，避免文字被箭头线压住。
参考 notes_深入讲解.md 第3节。全程只做test-time迭代，不更新模型参数。
"""

import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon
from matplotlib.path import Path as MplPath

fig, ax = new_fig(7.6, 6.4)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

CENTER = (0.53, 0.50)  # 图形大致中心，用于把箭头标签推到离中心更远的一侧

def box(x, y, w, h, label, sub=None, accent=False, fontsize=11.5):
    edge, fill, tcolor = (ACCENT, ACCENT_FILL, ACCENT) if accent else (INK, BG, INK)
    b = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.010,rounding_size=0.022",
        linewidth=1.6, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(b)
    if sub:
        text(ax, x, y + h*0.19, label, size=fontsize, color=tcolor, bold=True)
        text(ax, x, y - h*0.26, sub, size=fontsize*0.72, color=INK_SOFT, linespacing=1.35)
    else:
        text(ax, x, y, label, size=fontsize, color=tcolor, bold=True)
    return dict(x=x, y=y, w=w, h=h, shape="rect")

def diamond(x, y, w, h, label, fontsize=10.5):
    pts = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
    poly = Polygon(pts, closed=True, linewidth=1.6, edgecolor=INK, facecolor="#F7F5F0")
    ax.add_patch(poly)
    text(ax, x, y, label, size=fontsize, color=INK, bold=True, linespacing=1.4)
    return dict(x=x, y=y, w=w, h=h, shape="diamond")

def edge_point(b, tx, ty):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    dx, dy = tx - x, ty - y
    if dx == 0 and dy == 0:
        return (x, y)
    hw, hh = w/2, h/2
    if b["shape"] == "diamond":
        denom = abs(dx)/hw + abs(dy)/hh
        scale = 1.0/denom if denom else 0
    else:
        scale = min(abs(hw/dx) if dx else float("inf"), abs(hh/dy) if dy else float("inf"))
    return (x + dx*scale, y + dy*scale)

def perp_label_point(p1, p2, dist, away_from=CENTER):
    mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]
    length = math.hypot(dx, dy) or 1.0
    ux, uy = -dy/length, dx/length
    c1 = (mx + ux*dist, my + uy*dist)
    c2 = (mx - ux*dist, my - uy*dist)
    d1 = math.hypot(c1[0]-away_from[0], c1[1]-away_from[1])
    d2 = math.hypot(c2[0]-away_from[0], c2[1]-away_from[1])
    return c1 if d1 > d2 else c2

def straight(b1, b2, label=None, dist=0.05, color=ARROW, lw=1.5,
             fontsize=9.0, label_color=None, extra_shrink=9):
    x1, y1 = b1["x"], b1["y"]
    x2, y2 = b2["x"], b2["y"]
    p1 = edge_point(b1, x2, y2)
    p2 = edge_point(b2, x1, y1)
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14, linewidth=lw,
                         color=color, shrinkA=extra_shrink, shrinkB=extra_shrink)
    ax.add_patch(a)
    if label:
        lx, ly = perp_label_point(p1, p2, dist)
        text(ax, lx, ly, label, size=fontsize, color=label_color or INK_SOFT)

def right_angle_loop(points, color=ACCENT_SOFT, lw=1.6):
    codes = [MplPath.MOVETO] + [MplPath.LINETO] * (len(points) - 1)
    path = MplPath(points, codes)
    patch = FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=14,
                             linewidth=lw, color=color, shrinkA=8, shrinkB=8)
    ax.add_patch(patch)

# ============ 标题（单独留出顶部空间） ============
text(ax, 0.5, 0.975, "Self-Refine：生成 → 批评 → 修改", size=15.5, color=INK, bold=True)
text(ax, 0.5, 0.930, "测试时（test-time）迭代，不更新模型参数", size=9.6, color=INK_SOFT)

# ============ 四个主节点：菱形四个顶点（整体下移，与标题拉开间距） ============
gen = box(0.20, 0.50, 0.20, 0.115, "Generator",
          "原始任务 → 初始答案", fontsize=11.3)

fb = box(0.53, 0.80, 0.24, 0.12, "Feedback",
         "当前答案 → 诊断问题", fontsize=11.3, accent=True)

refine = box(0.86, 0.50, 0.20, 0.115, "Refine",
             "答案+反馈 → 改进答案", fontsize=11.3)

stop = diamond(0.53, 0.20, 0.30, 0.20, "轮数已到 /\n模型自判无需再改?", fontsize=9.6)

final = box(0.20, 0.145, 0.20, 0.085, "输出最终答案", fontsize=10.5)

# ============ 菱形四条边 ============
straight(gen, fb, "初始答案", dist=0.045)
straight(fb, refine, "反馈：哪里有问题", dist=0.05)
straight(refine, stop, "改进后的答案", dist=0.05)

# stop -> final："是"
straight(stop, final, "是", dist=0.035)

# stop -> fb："否"：直线直接指向Feedback，不绕折线
straight(stop, fb, "否：继续下一轮", dist=0.045, color=ACCENT, lw=1.6, label_color=ACCENT)

# ============ 说明小卡片：放在图右下角，与stop菱形保持间隙 ============
note_x0, note_y0, note_w, note_h = 0.68, 0.05, 0.30, 0.16
note = FancyBboxPatch((note_x0, note_y0), note_w, note_h,
                       boxstyle="round,pad=0.008,rounding_size=0.016",
                       linewidth=1.0, edgecolor=INK_SOFT, facecolor="#FAFAF8",
                       linestyle=(0, (3, 2)))
ax.add_patch(note)
text(ax, note_x0 + note_w/2, note_y0 + note_h - 0.032,
     "每轮只带\"当前最新答案+反馈\"", size=8.5, color=INK)
text(ax, note_x0 + note_w/2, note_y0 + note_h - 0.070,
     "不叠加此前所有轮次的历史", size=8.5, color=INK)
text(ax, note_x0 + note_w/2, note_y0 + note_h - 0.115,
     "停止条件：固定轮数(如4轮)\n或模型自判无需再改", size=7.9, color=INK_SOFT, linespacing=1.4)

save(fig, "fig_self_refine_loop.png")
