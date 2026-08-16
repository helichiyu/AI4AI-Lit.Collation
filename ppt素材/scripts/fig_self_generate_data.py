# -*- coding: utf-8 -*-
"""
"自生成数据方向"大图：左半STaR闭环，右半Self-Instruct闭环（含种子任务池结构）。
参考 notes_深入讲解.md 第2节。

坐标全部手工核对，确保每个框都落在画布[0,1]x[0,1]内，不依赖会甩出画布的大弧形箭头。
循环回路用直角折线路径(Path+FancyArrowPatch)手动画在每列外侧，不用arc3。
数学变量(x_i, y_i, r_i, y_i带hat等)全部用mathtext($...$)渲染，保证上下标/hat符号正确。
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon
from matplotlib.path import Path as MplPath

fig, ax = new_fig(13.5, 8.6)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

def box(x, y, w, h, label, sub=None, accent=False, fontsize=11.5):
    edge, fill, tcolor = (ACCENT, ACCENT_FILL, ACCENT) if accent else (INK, BG, INK)
    b = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.010,rounding_size=0.020",
        linewidth=1.5, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(b)
    if sub:
        text(ax, x, y + h*0.19, label, size=fontsize, color=tcolor, bold=True)
        text(ax, x, y - h*0.27, sub, size=fontsize*0.72, color=INK_SOFT, linespacing=1.4)
    else:
        text(ax, x, y, label, size=fontsize, color=tcolor, bold=True)
    return dict(x=x, y=y, w=w, h=h, shape="rect")

def diamond(x, y, w, h, label, fontsize=10.5):
    pts = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
    poly = Polygon(pts, closed=True, linewidth=1.5, edgecolor=INK, facecolor="#F7F5F0")
    ax.add_patch(poly)
    text(ax, x, y, label, size=fontsize, color=INK, bold=True)
    return dict(x=x, y=y, w=w, h=h, shape="diamond")

def edge_point(b, tx, ty):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    dx, dy = tx - x, ty - y
    if dx == 0 and dy == 0:
        return (x, y)
    hw, hh = w/2, h/2
    if b["shape"] == "diamond":
        # 菱形边界: |dx|/hw + |dy|/hh = 1 沿射线方向的交点
        denom = abs(dx)/hw + abs(dy)/hh
        scale = 1.0 / denom if denom else 0
    else:
        scale = min(abs(hw/dx) if dx else float("inf"), abs(hh/dy) if dy else float("inf"))
    return (x + dx*scale, y + dy*scale)

def straight(b1, b2, label=None, label_offset=(0, 0), color=ARROW, lw=1.4,
             fontsize=8.6, label_color=None, extra_shrink=9):
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

def right_angle_loop(points, color=ACCENT_SOFT, lw=1.4):
    """按给定的一串折点画直角折线箭头，箭头在最后一段末端；两端各留出一点空隙。"""
    codes = [MplPath.MOVETO] + [MplPath.LINETO] * (len(points) - 1)
    path = MplPath(points, codes)
    patch = FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=13,
                             linewidth=lw, color=color, shrinkA=9, shrinkB=9)
    ax.add_patch(patch)

# ============ 标题 + 分隔线 ============
text(ax, 0.25, 0.975, "STaR", size=18, color=INK, bold=True)
text(ax, 0.75, 0.975, "Self-Instruct", size=18, color=INK, bold=True)
ax.plot([0.5, 0.5], [0.02, 0.95], color="#D8D8D8", linewidth=1.2, linestyle=(0, (4, 3)))

# =====================================================================
# 左半：STaR 闭环
# =====================================================================
s1 = box(0.25, 0.89, 0.30, 0.075, "当前模型 + few-shot示例",
         r"输入: 问题 $x_i$", fontsize=11.3)
s2 = box(0.25, 0.745, 0.32, 0.08, "生成推理链 + 预测答案",
         r"输出: 推理链 $r_i$ ，预测答案 $\hat{y}_i$", fontsize=11.3)
straight(s1, s2)

dec = diamond(0.25, 0.605, 0.18, 0.11, r"$\hat{y}_i = y_i$ ?", fontsize=10.3)
straight(s2, dec, extra_shrink=10)

# 正确分支（右侧）
ok = box(0.365, 0.465, 0.17, 0.075, "保留", r"$(x_i,\ r_i,\ y_i)$", fontsize=10.3)
straight(dec, ok, "正确", label_offset=(0.028, 0.02), extra_shrink=10)

# 错误分支（左侧）：rationalization
wrong = box(0.145, 0.465, 0.20, 0.095, "rationalization",
            "把正确答案当提示喂回去,\n反向编出推理链", fontsize=10.0)
straight(dec, wrong, "错误", label_offset=(-0.028, 0.02), extra_shrink=10)
wrong_keep = box(0.145, 0.325, 0.17, 0.07, "保留", r"$(x_i,\ r_i',\ y_i)$", fontsize=10.3)
straight(wrong, wrong_keep)

# 汇总 + 微调
agg = box(0.25, 0.165, 0.34, 0.10, "汇总本轮全部数据 → 微调模型",
          "每轮都从最初的预训练模型重新微调\n(不在上一轮基础上继续训练)", fontsize=10.6, accent=True)
straight(ok, agg)
straight(wrong_keep, agg)

# 循环回到起点：直角折线，走左侧外沿(x=0.02)，从agg左边出发，绕到s1左边进入
right_angle_loop([
    (agg["x"] - agg["w"]/2, agg["y"]),
    (0.02, agg["y"]),
    (0.02, s1["y"]),
    (s1["x"] - s1["w"]/2, s1["y"]),
])

# =====================================================================
# 右半：Self-Instruct 闭环
# =====================================================================
pool = box(0.75, 0.89, 0.36, 0.075, "种子任务池 (175条,人工写)",
           "每条 = 指令 + 输入 + 输出 三元组", fontsize=11.3, accent=True)

card_w, card_h = 0.36, 0.115
card_y = 0.775
card_x0 = 0.75 - card_w/2
card_y0 = card_y - card_h/2
card = FancyBboxPatch((card_x0, card_y0), card_w, card_h,
                       boxstyle="round,pad=0.008,rounding_size=0.016",
                       linewidth=1.1, edgecolor=INK_SOFT, facecolor="#FAFAF8",
                       linestyle=(0, (3, 2)))
ax.add_patch(card)
text(ax, card_x0 + 0.014, card_y0 + card_h - 0.024, "指令: 判断以下文本的情感", size=8.4, color=INK, ha="left")
text(ax, card_x0 + 0.014, card_y0 + card_h - 0.056, "输入: 这部电影太精彩了 (可为空)", size=8.4, color=INK, ha="left")
text(ax, card_x0 + 0.014, card_y0 + card_h - 0.088, "输出: 正面", size=8.4, color=INK, ha="left")
card_node = dict(x=0.75, y=card_y, w=card_w, h=card_h, shape="rect")
text(ax, 0.7 + card_w/2, card_y+0.05, "结构示例", size=8.2, color=INK_SOFT)

sample = box(0.75, 0.60, 0.32, 0.075, "采样几条已有指令", "作为 few-shot 示例", fontsize=10.6)
straight(card_node, sample)

st1 = box(0.75, 0.475, 0.32, 0.075, "Step1 指令生成", "prompt模型写一条全新指令", fontsize=10.6)
straight(sample, st1)

st2 = box(0.75, 0.35, 0.32, 0.075, "Step2 判断任务类型", "output-first / input-first", fontsize=10.6)
straight(st1, st2)

st3 = box(0.75, 0.225, 0.32, 0.075, "Step3 实例生成", "补全对应的输入输出样例", fontsize=10.6)
straight(st2, st3)

st4 = box(0.75, 0.10, 0.32, 0.075, "Step4 过滤", "ROUGE相似度 + 格式检查", fontsize=10.6)
straight(st3, st4)

# 循环回到起点：直角折线，走右侧外沿(x=0.98)，从st4右边出发，绕到pool右边进入
right_angle_loop([
    (st4["x"] + st4["w"]/2, st4["y"]),
    (0.98, st4["y"]),
    (0.98, pool["y"]),
    (pool["x"] + pool["w"]/2, pool["y"]),
])

text(ax, 0.75, 0.02, "最终约5.2万条指令、8.2万条实例，用于微调GPT-3本身", size=9.2, color=INK_SOFT)

save(fig, "fig_self_generate_data.png")
