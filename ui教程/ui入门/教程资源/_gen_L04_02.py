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
# === L04_02: Panel as container ===
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 5.5); ax.axis("off")
ax.set_title("Panel 只是一个 Image 做容器", color="#fff", fontsize=18, fontweight="bold", pad=15)

canvas = FancyBboxPatch((0.5, 0.5), 9, 4.3, boxstyle="round,pad=0.05",
                         facecolor="#1a1a2e", edgecolor=BORDER, linewidth=1, linestyle="--")
ax.add_patch(canvas)
ax.text(1, 4.5, "Canvas", color=MUTED, fontsize=10)

panel = FancyBboxPatch((1.5, 1), 7, 3, boxstyle="round,pad=0.1",
                        facecolor="#1a1a2a", edgecolor=ACCENT, linewidth=2, alpha=0.9)
ax.add_patch(panel)
ax.text(2, 3.7, "Panel (Image 组件)", color=ACCENT, fontsize=12, fontweight="bold")

children = [
    (2.2, 2.8, "Text (TMP) - 标题", "#fff"),
    (2.2, 2.1, "Text (TMP) - 描述文字...", MUTED),
    (5.5, 1.3, "Button - 确认", ACCENT_WARM),
]
for cx, cy, label, color in children:
    child = FancyBboxPatch((cx, cy-0.2), 3.5, 0.45, boxstyle="round,pad=0.03",
                            facecolor=PANEL, edgecolor=color, linewidth=1)
    ax.add_patch(child)
    ax.text(cx+0.2, cy, label, color=color, fontsize=10)

ax.annotate("Image 组件\n提供背景", xy=(3, 1.5), xytext=(0.3, 2.2), color=ACCENT, fontsize=10,
            arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.5))
ax.annotate("子元素\n放在 Panel 下面", xy=(5, 2.5), xytext=(9, 3.8), color=GREEN, fontsize=10, ha="center",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))

ax.text(5, 0.3, "Panel = Image + 半透明颜色 + 作为其他UI元素的父级容器", color=MUTED, fontsize=11, ha="center")
save("L04_02_panel_background.png")
print("L04_02 done")
