# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans SC", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 13
DARK_BG = "#1e1e1e"; PANEL = "#2b2b2b"; BORDER = "#3a3a3a"; TEXT = "#e6e6e6"
MUTED = "#9aa0a6"; ACCENT = "#4ea1ff"; ACCENT_WARM = "#ff9e4e"; GREEN = "#6bcf7f"
RED = "#f87171"; PURPLE = "#a78bfa"; YELLOW = "#fbbf24"
OUT = "D:/bangong/unity/vrc/ass/ceshi/Assets/UITutorial/Site/img"
def save(name):
    plt.savefig(OUT + "/" + name, dpi=150, bbox_inches="tight", facecolor=DARK_BG, edgecolor="none")
    plt.close()
    print("Saved " + name)
# === L04_04: 9-Slice (Sliced) principle ===
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 11); ax.set_ylim(0, 5.5); ax.axis("off")
ax.set_title("九宫格切片（Sliced）原理", color="#fff", fontsize=18, fontweight="bold", pad=15)

orig = FancyBboxPatch((0.3, 2.5), 2, 2, boxstyle="round,pad=0.08",
                       facecolor="#3a3a5a", edgecolor=ACCENT, linewidth=2)
ax.add_patch(orig)
ax.text(1.3, 4.8, "原图", color=ACCENT, fontsize=12, ha="center", fontweight="bold")

for bx in [0.8, 1.8]:
    ax.axvline(x=bx, ymin=0.46, ymax=0.82, color=GREEN, linewidth=1, linestyle="--")
for by in [2.9, 3.9]:
    ax.axhline(y=by, xmin=0.027, xmax=0.227, color=GREEN, linewidth=1, linestyle="--")

ax.annotate("", xy=(2.8, 3.5), xytext=(3.5, 3.5),
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=3))

ax.add_patch(FancyBboxPatch((3.8, 2.5), 3.5, 2, boxstyle="round,pad=0.08",
                             facecolor="none", edgecolor=GREEN, linewidth=1.5, linestyle="--"))

cells = [
    (3.8, 3.9, 0.7, 0.6, "角\n固定", GREEN),
    (4.5, 3.9, 2.1, 0.6, "边 -> 水平拉伸", ACCENT_WARM),
    (6.6, 3.9, 0.7, 0.6, "角\n固定", GREEN),
    (3.8, 3.3, 0.7, 0.6, "边\n|\n垂直拉伸", ACCENT_WARM),
    (4.5, 3.3, 2.1, 0.6, "中心 -> 双向拉伸", PURPLE),
    (6.6, 3.3, 0.7, 0.6, "边\n|\n垂直拉伸", ACCENT_WARM),
    (3.8, 2.5, 0.7, 0.8, "角\n固定", GREEN),
    (4.5, 2.5, 2.1, 0.8, "边 -> 水平拉伸", ACCENT_WARM),
    (6.6, 2.5, 0.7, 0.8, "角\n固定", GREEN),
]
for x, y, w, h, label, color in cells:
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="none", alpha=0.15))
    ax.text(x+w/2, y+h/2, label, color=color, fontsize=8, ha="center", va="center")

ax.text(5.55, 5.1, "拉伸后的效果", color=GREEN, fontsize=11, ha="center")

ax.text(5.5, 0.7, "关键：必须在图片资源的 Sprite Editor 中设置 Border（绿色边框线）", color=ACCENT, fontsize=12, ha="center", fontweight="bold")
ax.text(5.5, 0.3, "选中图片 -> Inspector -> Sprite Editor -> 拖动绿色线 -> Apply", color=MUTED, fontsize=10, ha="center")

ax.add_patch(Rectangle((0.3, 0.5), 0.3, 0.2, facecolor=GREEN, edgecolor="none", alpha=0.5))
ax.text(0.7, 0.6, "四角保持原始形状", color=GREEN, fontsize=9)
ax.add_patch(Rectangle((2.8, 0.5), 0.3, 0.2, facecolor=ACCENT_WARM, edgecolor="none", alpha=0.5))
ax.text(3.2, 0.6, "四边单向拉伸", color=ACCENT_WARM, fontsize=9)
ax.add_patch(Rectangle((5.5, 0.5), 0.3, 0.2, facecolor=PURPLE, edgecolor="none", alpha=0.5))
ax.text(5.9, 0.6, "中心双向拉伸", color=PURPLE, fontsize=9)

save("L04_04_nineslice.png")
print("L04_04 done")
