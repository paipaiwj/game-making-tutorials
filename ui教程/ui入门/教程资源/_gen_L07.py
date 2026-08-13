# -*- coding: utf-8 -*-
# L07 图片生成脚本
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle
import os

fm._load_fontmanager(try_read_cache=False)
available_fonts = [f.name for f in fm.fontManager.ttflist]
chinese_candidates = ['Microsoft YaHei', 'SimHei', 'Noto Sans SC']
chosen = None
for c in chinese_candidates:
    if c in available_fonts:
        chosen = c
        break
if chosen:
    plt.rcParams['font.sans-serif'] = [chosen, 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 13

BG = '#1e1e1e'; PANEL = '#2b2b2b'; BORDER = '#3a3a3a'
TEXT = '#e6e6e6'; MUTED = '#9aa0a6'; ACCENT = '#4ea1ff'
WARM = '#ff9e4e'; GREEN = '#6bcf7f'; RED = '#f87171'
PURPLE = '#a78bfa'
OUT = 'D:/bangong/unity/vrc/ass/ceshi/Assets/UITutorial/Site/img'

def save(name):
    plt.savefig(OUT + '/' + name, dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
    plt.close()
    print('Saved ' + name)

# L07_01: 三种RenderMode对比
fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.patch.set_facecolor(BG)
modes = [
    ('Screen Space\nOverlay', ACCENT, '贴在屏幕上\n始终在最上层\n忽略摄像机\n HUD/血条/准星'),
    ('Screen Space\nCamera', GREEN, '绑定到指定摄像机\n可被3D物体遮挡\n 瞄准镜/仪表盘'),
    ('World Space', WARM, '存在于3D世界中\n像真实物体一样放置\n VRChat唯一可用模式！'),
]
for i, (ax_i, (title, color, desc)) in enumerate(zip(axes, modes)):
    ax_i.set_facecolor(PANEL)
    ax_i.set_xlim(0, 4); ax_i.set_ylim(0, 5); ax_i.axis('off')
    ax_i.set_title(title, color=color, fontsize=14, fontweight='bold', pad=12)
    rect = FancyBboxPatch((0.2, 0.2), 3.6, 4.6, boxstyle='round,pad=0.1', facecolor='#222', edgecolor=color, linewidth=2)
    ax_i.add_patch(rect)
    ax_i.text(2, 2.5, desc, color=TEXT, fontsize=12, ha='center', va='center', linespacing=1.6)
    if i == 2:
        ax_i.text(2, 0.5, 'VRChat', color=RED, fontsize=11, ha='center', fontweight='bold')
plt.tight_layout()
save('L07_01_rendermodes.png')
print('DONE')
