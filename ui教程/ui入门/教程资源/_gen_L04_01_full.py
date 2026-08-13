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
# === L04_01: Four Image Types comparison ===
fig, ax = plt.subplots(figsize=(12, 5.5))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 12); ax.set_ylim(0, 5.5); ax.axis("off")
ax.set_title("Image \u7ec4\u4ef6\u7684\u56db\u79cd Image Type", color="#fff", fontsize=18, fontweight="bold", pad=15)

types = [
    ("Simple", "\u76f4\u63a5\u62c9\u4f38\n\u4e0d\u4fdd\u6301\u6bd4\u4f8b", "#ff9e4e"),
    ("Sliced", "\u4e5d\u5bab\u683c\u5207\u7247\n\u56db\u89d2\u4e0d\u52a8\uff0c\u4e2d\u95f4\u62c9\u4f38", "#4ea1ff"),
    ("Tiled", "\u5e73\u94fa\u91cd\u590d\n\u50cf\u94fa\u74f7\u7816", "#6bcf7f"),
    ("Filled", "\u90e8\u5206\u586b\u5145\n\u7528\u4e8e\u8fdb\u5ea6\u6761/\u51b7\u5374", "#a78bfa"),
]

for i, (name, desc, color) in enumerate(types):
    x = 0.6 + i * 2.9
    outer = FancyBboxPatch((x, 2.2), 2.4, 2.3, boxstyle="round,pad=0.08",
                           facecolor=PANEL, edgecolor=color, linewidth=2)
    ax.add_patch(outer)
    
    if name == "Simple":
        for j in range(3):
            ax.add_patch(FancyBboxPatch((x+0.3, 3.5-j*0.45), 1.8, 0.35, boxstyle="round,pad=0.02",
                                       facecolor=color, edgecolor="none", alpha=0.5-0.1*j))
    elif name == "Sliced":
        ax.add_patch(Rectangle((x+0.3, 3.7), 0.5, 0.5, facecolor=color, edgecolor="none", alpha=0.9))
        ax.add_patch(Rectangle((x+1.6, 3.7), 0.5, 0.5, facecolor=color, edgecolor="none", alpha=0.9))
        ax.add_patch(Rectangle((x+0.3, 2.7), 0.5, 0.5, facecolor=color, edgecolor="none", alpha=0.9))
        ax.add_patch(Rectangle((x+1.6, 2.7), 0.5, 0.5, facecolor=color, edgecolor="none", alpha=0.9))
        ax.add_patch(Rectangle((x+0.8, 3.7), 0.8, 0.5, facecolor=color, edgecolor="none", alpha=0.4))
        ax.add_patch(Rectangle((x+0.8, 2.7), 0.8, 0.5, facecolor=color, edgecolor="none", alpha=0.4))
        ax.add_patch(Rectangle((x+0.3, 3.2), 0.5, 0.5, facecolor=color, edgecolor="none", alpha=0.4))
        ax.add_patch(Rectangle((x+1.6, 3.2), 0.5, 0.5, facecolor=color, edgecolor="none", alpha=0.4))
        ax.add_patch(Rectangle((x+0.8, 3.2), 0.8, 0.5, facecolor=color, edgecolor="none", alpha=0.2))
    elif name == "Tiled":
        for r in range(3):
            for c in range(4):
                ax.add_patch(Rectangle((x+0.25+c*0.5, 2.4+r*0.6), 0.4, 0.5,
                                      facecolor=color, edgecolor="none", alpha=0.3+0.1*(r+c)))
    elif name == "Filled":
        ax.add_patch(FancyBboxPatch((x+0.3, 2.7), 1.8, 1.5, boxstyle="round,pad=0.02",
                                   facecolor=color, edgecolor="none", alpha=0.15))
        ax.add_patch(FancyBboxPatch((x+0.3, 2.7), 1.15, 1.5, boxstyle="round,pad=0.02",
                                   facecolor=color, edgecolor="none", alpha=0.6))
        ax.text(x+1.2, 3.45, "64%", color="#fff", fontsize=12, ha="center", va="center", fontweight="bold")
    
    ax.text(x+1.2, 1.85, name, color=color, fontsize=13, ha="center", va="center", fontweight="bold")
    ax.text(x+1.2, 1.45, desc, color=MUTED, fontsize=9, ha="center", va="center")

ax.text(6, 0.4, "\u5728 Inspector \u7684 Image \u7ec4\u4ef6\u4e2d\uff0cImage Type \u4e0b\u62c9\u9009\u62e9", color=MUTED, fontsize=11, ha="center")
save("L04_01_image_types.png")
print("L04_01 done")
