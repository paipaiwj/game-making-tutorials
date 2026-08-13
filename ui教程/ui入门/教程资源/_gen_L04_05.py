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
# === L04_05: Alpha transparency demo ===
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
ax.set_title("不同 Alpha 值的效果对比", color="#fff", fontsize=18, fontweight="bold", pad=15)

alphas = [
    (255, "完全不透明\nColor Alpha=255"),
    (200, "半透明（常用）\nAlpha=200"),
    (150, "较透明\nAlpha=150"),
    (100, "很透明\nAlpha=100"),
    (50, "几乎透明\nAlpha=50"),
]

for i, (alpha, label) in enumerate(alphas):
    x = 0.5 + i * 2.3
    
    # Background text to show transparency
    ax.text(x+1, 2.2, "背景文字", color=MUTED, fontsize=16, ha="center", va="center", alpha=0.5)
    
    # Panel overlay
    a = alpha / 255.0
    panel = FancyBboxPatch((x, 1.2), 2, 2.5, boxstyle="round,pad=0.08",
                            facecolor="#000000", edgecolor=ACCENT if alpha > 150 else BORDER, linewidth=1.5, alpha=a)
    ax.add_patch(panel)
    
    # Label on panel
    ax.text(x+1, 3.2, "Alpha=" + str(alpha), color="#fff" if alpha > 120 else MUTED, fontsize=12, ha="center", fontweight="bold")
    ax.text(x+1, 2.5, "前景面板", color="#fff" if alpha > 120 else MUTED, fontsize=11, ha="center")
    
    ax.text(x+1, 0.7, label, color=MUTED, fontsize=9, ha="center")

ax.text(6, 4.5, "Alpha 值越低，背景越能透过来。180 左右是最常用的半透明效果。", color=MUTED, fontsize=11, ha="center")
save("L04_05_alpha_demo.png")
print("L04_05 done")
