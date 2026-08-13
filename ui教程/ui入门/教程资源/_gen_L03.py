# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Noto Sans SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 13

DARK_BG = '#1e1e1e'; PANEL = '#2b2b2b'; BORDER = '#3a3a3a'; TEXT = '#e6e6e6'
MUTED = '#9aa0a6'; ACCENT = '#4ea1ff'; ACCENT_WARM = '#ff9e4e'; GREEN = '#6bcf7f'
RED = '#f87171'; PURPLE = '#a78bfa'; YELLOW = '#fbbf24'

OUT = 'D:/bangong/unity/vrc/ass/ceshi/Assets/UITutorial/Site/img'

def save(name):
    plt.savefig(OUT + '/' + name, dpi=150, bbox_inches='tight', facecolor=DARK_BG, edgecolor='none')
    plt.close()
    print(f'Saved {name}')

# === L03_01: Button Anatomy ===
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis('off')
ax.set_title('Button 的组成结构', color='#fff', fontsize=18, fontweight='bold', pad=15)

btn = FancyBboxPatch((3.5, 1.8), 3, 1.2, boxstyle="round,pad=0.1", facecolor=PANEL, edgecolor=ACCENT, linewidth=2)
ax.add_patch(btn)
ax.text(5, 2.4, '点击我', color='#fff', fontsize=14, ha='center', va='center')

annotations = [
    (1.8, 3.2, 'Text (TMP)\n显示的文字'),
    (5, 1.1, 'Image\n背景图片'),
    (8.5, 3.2, 'Button 组件\n处理点击'),
]
for x, y, label in annotations:
    ax.annotate(label, xy=(5, 2.4), xytext=(x, y), color=ACCENT, fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.2))

ax.text(0.5, 4.5, 'Button = Text (TMP) + Image + Button 组件', color=MUTED, fontsize=11)
ax.text(0.5, 4.1, '右键 Hierarchy → UI → Button - TextMeshPro 即可创建', color=MUTED, fontsize=10)
save('L03_01_button_anatomy.png')

# === L03_02: Click Flow ===
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.5); ax.axis('off')
ax.set_title('Button 点击流程', color='#fff', fontsize=18, fontweight='bold', pad=15)

steps = ['① 用户点击\nButton', '② EventSystem\n检测点击', '③ 查找 OnClick\n事件列表', '④ 执行绑定的\n方法']
for i, s in enumerate(steps):
    x = 1 + i * 2.2
    box = FancyBboxPatch((x, 1.5), 1.8, 1.2, boxstyle="round,pad=0.05",
                          facecolor=PANEL, edgecolor=ACCENT if i < 3 else GREEN, linewidth=2)
    ax.add_patch(box)
    ax.text(x + 0.9, 2.1, s, color='#fff', fontsize=10, ha='center', va='center')
    if i < 3:
        ax.annotate('', xy=(x + 2.0, 2.1), xytext=(x + 2.4, 2.1),
                    arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2))

ax.text(5, 0.7, 'EventSystem 是 Unity 自动创建的，负责检测所有 UI 交互', color=MUTED, fontsize=10, ha='center')
save('L03_02_click_flow.png')

# === L03_03: Button States ===
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.5); ax.axis('off')
ax.set_title('Button 的四种交互状态', color='#fff', fontsize=18, fontweight='bold', pad=15)

states = [
    ('普通状态', PANEL, '#fff', 'Normal'),
    ('高亮（悬停）', '#3a4a5a', ACCENT, 'Highlighted'),
    ('按下状态', '#2a3a4a', '#cce', 'Pressed'),
    ('禁用状态', '#2a2a2a', MUTED, 'Disabled'),
]
for i, (cn, bg, tc, eng) in enumerate(states):
    x = 0.8 + i * 2.3
    btn = FancyBboxPatch((x, 1.5), 1.8, 1, boxstyle="round,pad=0.08",
                          facecolor=bg, edgecolor=BORDER if i == 3 else ACCENT, linewidth=2)
    ax.add_patch(btn)
    ax.text(x + 0.9, 2.2, cn, color=tc, fontsize=12, ha='center', va='center')
    ax.text(x + 0.9, 1.7, eng, color=MUTED, fontsize=9, ha='center', va='center')

ax.text(5, 3.8, '通过 Button 组件的 Transition 属性切换状态', color=MUTED, fontsize=11, ha='center')
ax.text(5, 3.4, '常用 Color Tint（颜色变化）或 Sprite Swap（图片切换）', color=MUTED, fontsize=10, ha='center')
save('L03_03_button_states.png')

# === L03_04: OnClick Panel ===
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 5.5); ax.axis('off')
ax.set_title('OnClick 事件绑定面板', color='#fff', fontsize=18, fontweight='bold', pad=15)

panel = FancyBboxPatch((0.3, 0.3), 9.4, 4.6, boxstyle="round,pad=0.1", facecolor=PANEL, edgecolor=BORDER, linewidth=1)
ax.add_patch(panel)
ax.text(0.8, 4.6, 'On Click ()', color='#fff', fontsize=14, fontweight='bold')

events = [
    ('Cube', 'GameObject.SetActive', GREEN),
    ('AudioSource', 'AudioSource.Play', ACCENT),
    ('Canvas', 'Canvas.enabled', MUTED),
]
for i, (target, method, color) in enumerate(events):
    y = 4.0 - i * 0.6
    row = FancyBboxPatch((0.6, y - 0.2), 8.8, 0.5, boxstyle="round,pad=0.02",
                          facecolor=DARK_BG, edgecolor=BORDER, linewidth=0.5)
    ax.add_patch(row)
    ax.text(0.9, y, target, color=ACCENT, fontsize=10)
    ax.text(3.5, y, method, color=color, fontsize=10)
    ax.text(8.8, y, '☑', color=GREEN, fontsize=12)

ax.text(5, 0.8, '步骤：点击 + → 拖入目标对象 → 选择方法 → 完成绑定', color=MUTED, fontsize=10, ha='center')
save('L03_04_onclick_panel.png')

# === L03_05: Button Inspector ===
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
ax.set_title('Button 组件 Inspector 完整面板', color='#fff', fontsize=18, fontweight='bold', pad=15)

panel = FancyBboxPatch((0.3, 0.2), 9.4, 5.3, boxstyle="round,pad=0.1", facecolor=PANEL, edgecolor=BORDER, linewidth=1)
ax.add_patch(panel)

rows = [
    ('Interactable', '☑ 可交互（勾选）', GREEN, '取消勾选后按钮变灰，不可点击'),
    ('Transition', 'Color Tint ▼', ACCENT, '状态切换方式：变色/换图/动画'),
    ('Target Graphic', 'Button (Image)', ACCENT, '状态变化应用到的图形'),
    ('Normal Color', '■ 白色', '#fff', '普通状态颜色'),
    ('Highlighted Color', '■ 浅蓝色', ACCENT, '鼠标悬停颜色'),
    ('Pressed Color', '■ 深蓝色', '#7799cc', '按下时颜色'),
    ('Disabled Color', '■ 灰色', MUTED, '禁用时颜色'),
    ('Navigation', 'Automatic ▼', MUTED, '键盘/手柄导航'),
]
for i, (label, value, color, desc) in enumerate(rows):
    y = 5.1 - i * 0.55
    ax.text(0.6, y, label, color=MUTED, fontsize=10)
    ax.text(3.5, y, value, color=color, fontsize=10)
    ax.text(6.5, y, desc, color=MUTED, fontsize=9)

save('L03_05_button_inspector.png')
print('L03 done!')
