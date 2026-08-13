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
# === L04_03: Image vs Raw Image ===
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
fig.patch.set_facecolor(DARK_BG)

for ax in [ax1, ax2]:
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.axis("off")

ax1.set_title("Image 组件", color=ACCENT, fontsize=16, fontweight="bold", pad=12)
ax2.set_title("Raw Image 组件", color=ACCENT_WARM, fontsize=16, fontweight="bold", pad=12)

# Image (left)
img_box1 = FancyBboxPatch((0.5, 1.2), 4, 2.8, boxstyle="round,pad=0.1",
                           facecolor=PANEL, edgecolor=ACCENT, linewidth=2)
ax1.add_patch(img_box1)
for i, (sx, sy, c) in enumerate([(1.5, 3.2, ACCENT), (2.5, 3.2, GREEN), (3.5, 3.2, PURPLE), (2, 2.2, YELLOW), (3, 2.2, RED)]):
    ax1.add_patch(Circle((sx, sy), 0.25, facecolor=c, edgecolor="none", alpha=0.8))
ax1.text(2.5, 3.8, "只接受 Sprite", color=ACCENT, fontsize=11, ha="center", fontweight="bold")
ax1.text(2.5, 1.5, "图片需设为 Sprite (2D and UI)\n才能拖入 Source Image", color=MUTED, fontsize=9, ha="center")

# Raw Image (right)
img_box2 = FancyBboxPatch((0.5, 1.2), 4, 2.8, boxstyle="round,pad=0.1",
                           facecolor=PANEL, edgecolor=ACCENT_WARM, linewidth=2)
ax2.add_patch(img_box2)
ax2.add_patch(Rectangle((1, 1.8), 3, 1.8, facecolor="#2a3a5a", edgecolor="none", alpha=0.6))
for j in range(5):
    ax2.add_patch(Rectangle((1+0.6*j, 1.8), 0.5, 1.8, facecolor="#3a4a6a", edgecolor="none", alpha=0.3))
ax2.text(2.5, 3.8, "接受任何 Texture", color=ACCENT_WARM, fontsize=11, ha="center", fontweight="bold")
ax2.text(2.5, 1.5, "RenderTexture / Texture2D\n无需改为 Sprite 格式", color=MUTED, fontsize=9, ha="center")

fig.suptitle("Image vs Raw Image —— 接受的数据类型不同", color="#fff", fontsize=17, fontweight="bold", y=0.98)
save("L04_03_image_vs_rawimage.png")
print("L04_03 done")
