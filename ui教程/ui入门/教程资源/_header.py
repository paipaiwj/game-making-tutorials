# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
import numpy as np
import os

fm._load_fontmanager(try_read_cache=False)

available_fonts = [f.name for f in fm.fontManager.ttflist]
chinese_candidates = ["Microsoft YaHei", "SimHei", "Noto Sans SC", "Noto Sans CJK SC", "WenQuanYi Micro Hei", "SimSun", "FangSong", "KaiTi"]
chosen = None
for c in chinese_candidates:
    if c in available_fonts:
        chosen = c
        break

if chosen:
    plt.rcParams["font.sans-serif"] = [chosen, "sans-serif"]
else:
    plt.rcParams["font.sans-serif"] = ["sans-serif"]

plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 13

DARK_BG = "#0f1117"
PANEL = "#1a1d27"
PANEL2 = "#222633"
BORDER = "#2a2f3d"
TEXT = "#e2e4e9"
TEXT2 = "#a0a4b0"
MUTED = "#6b7080"
ACCENT = "#7c5cfc"
ACCENT2 = "#5b8af7"
GREEN = "#4ec9b0"
ORANGE = "#f0a060"
RED = "#f44771"
PURPLE = "#a78bfa"
YELLOW = "#fbbf24"

OUT = os.path.dirname(os.path.abspath(__file__))

def save(name):
    path = os.path.join(OUT, name)
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG, edgecolor="none", pad_inches=0.3)
    plt.close()
    print(f"Saved {name} (font: {chosen})")
