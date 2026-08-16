# -*- coding: utf-8 -*-
"""
统一绘图风格模块。所有配图脚本都从这里导入配色、字体、通用绘制小工具，
保证整套PPT素材图片风格一致。不要在单个图的脚本里重新定义颜色/字体。

用法：
    from style import *
    fig, ax = new_fig(6, 6)   # 或者自己 plt.subplots + apply_axes_style(ax)
    ...
    save(fig, "fig_xx_名字.png")
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ---------- 字体：思源黑体（中文），找不到就退回默认 ----------
_FONT_CANDIDATES = [
    r"E:\简历\01-简历\19_SourceHanSansCN\SubsetOTF\CN\SourceHanSansCN-Regular.otf",
    r"E:\简历\01-简历\19_SourceHanSansCN\SubsetOTF\CN\SourceHanSansCN-Medium.otf",
]
_FONT_BOLD_CANDIDATES = [
    r"E:\简历\01-简历\19_SourceHanSansCN\SubsetOTF\CN\SourceHanSansCN-Bold.otf",
    r"E:\简历\01-简历\19_SourceHanSansCN\SubsetOTF\CN\SourceHanSansCN-Medium.otf",
]

def _first_existing(paths):
    for p in paths:
        if os.path.isfile(p):
            return p
    return None

_REGULAR_PATH = _first_existing(_FONT_CANDIDATES)
_BOLD_PATH = _first_existing(_FONT_BOLD_CANDIDATES)

if _REGULAR_PATH:
    fm.fontManager.addfont(_REGULAR_PATH)
    FONT_REGULAR = fm.FontProperties(fname=_REGULAR_PATH)
    _FAMILY_NAME = fm.FontProperties(fname=_REGULAR_PATH).get_name()
    matplotlib.rcParams["font.family"] = _FAMILY_NAME
else:
    FONT_REGULAR = fm.FontProperties()
    matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]

if _BOLD_PATH:
    fm.fontManager.addfont(_BOLD_PATH)
    FONT_BOLD = fm.FontProperties(fname=_BOLD_PATH)
else:
    FONT_BOLD = FONT_REGULAR

matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["savefig.dpi"] = 200
matplotlib.rcParams["figure.dpi"] = 150

# ---------- 配色：黑白为主，灰蓝高亮 ----------
BG = "#FFFFFF"          # 背景：纯白
INK = "#2B2B2B"         # 主文字/主线条：深灰（接近黑，不用纯黑更柔和）
INK_SOFT = "#5A5A5A"    # 次要文字/说明性文字：中灰
LINE = "#3D3D3D"        # 常规线框
ARROW = "#8C8C8C"       # 箭头：浅灰
ACCENT = "#5B7C99"      # 灰蓝高亮：关键节点/强调框/强调文字
ACCENT_FILL = "#DCE6EC" # 灰蓝的浅色填充（节点底色用）
ACCENT_SOFT = "#9DB4C4" # 灰蓝的浅一档，用于次要强调/虚线
GRID = "#E5E5E5"        # 极浅灰，仅在极少数需要网格/分隔线时用

def new_fig(w, h):
    """新建一个指定宽高（英寸）的白底画布，并返回 fig, ax（关闭默认坐标轴）。"""
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax

def text(ax, x, y, s, size=13, color=INK, bold=False, ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=size, color=color,
            fontproperties=(FONT_BOLD if bold else FONT_REGULAR),
            ha=ha, va=va, **kw)

def save(fig, filename, out_dir=None):
    if out_dir is None:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    fig.savefig(path, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("saved:", path)
    return path
