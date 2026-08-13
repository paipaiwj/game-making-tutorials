# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np

plt.rcParams['font.family'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['font.size'] = 13

BG = '#1e1e1e'; PANEL = '#2b2b2b'; BORDER = '#3a3a3a'
TEXT = '#e6e6e6'; MUTED = '#9aa0a6'; ACCENT = '#4ea1ff'
WARM = '#ff9e4e'; GREEN = '#6bcf7f'; RED = '#f87171'
PURPLE = '#a78bfa'; YELLOW = '#fbbf24'
OUT = 'D:/bangong/unity/vrc/ass/ceshi/Assets/UITutorial/Site/img'

def save(name):
    plt.savefig(OUT + '/' + name, dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
    plt.close()

def add_box(ax, x, y, w, h, text, color, fontsize=11):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03", facecolor=color+'20', edgecolor=color, linewidth=1.5)
    ax.add_patch(b)
    ax.text(x+w/2, y+h/2, text, color='#fff', fontsize=fontsize, ha='center', va='center')

# L02_01: TMP vs Legacy
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
fig.patch.set_facecolor(BG)
for ax, title, color, quality, comp, perf, rec in [
    (ax1, 'Legacy Text (旧)', RED, '锯齿明显', 'Text', '一般', 'X 别用'),
    (ax2, 'TextMeshPro (新)', GREEN, '清晰锐利', 'TextMeshProUGUI', '好很多', 'O 就用它')]:
    ax.set_facecolor(BG); ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.axis('off')
    ax.set_title(title, color=color, fontsize=14, fontweight='bold', pad=10)
    txt = FancyBboxPatch((0.5, 2.5), 4, 1.5, boxstyle="round,pad=0.05", facecolor=color+'15', edgecolor=color, linewidth=1.5)
    ax.add_patch(txt)
    ax.text(2.5, 3.25, 'Hello World', color='#fff', fontsize=20, ha='center', va='center', fontweight='bold')
    ax.text(2.5, 1.8, quality, color=color, fontsize=13, ha='center', fontweight='bold')
    for i, (k, v) in enumerate([('组件名', comp), ('性能', perf), ('推荐', rec)]):
        ax.text(0.8, 1.2 - i*0.4, k + ':', color=MUTED, fontsize=10)
        ax.text(2.5, 1.2 - i*0.4, v, color='#fff', fontsize=10)
fig.suptitle('TextMeshPro vs Legacy Text', color='#fff', fontsize=17, fontweight='bold', y=1.02)
save('L02_01_tmp_vs_legacy.png')
print('L02_01 done')

# L02_02: Create Text steps
fig, axes = plt.subplots(1, 4, figsize=(13, 3.5))
fig.patch.set_facecolor(BG)
steps = [('1. 右键 Canvas', 'Canvas 上右键', ACCENT),
         ('2. UI > Text - TMP', '选 TextMeshPro', WARM),
         ('3. Import TMP', '点 Import 按钮', GREEN),
         ('4. Text 出现了', 'Canvas 下多了 TMP', PURPLE)]
for i, (title, desc, color) in enumerate(steps):
    ax = axes[i]; ax.set_facecolor(BG); ax.set_xlim(0, 5); ax.set_ylim(0, 4); ax.axis('off')
    ax.set_title(title, color=color, fontsize=12, fontweight='bold', pad=8)
    add_box(ax, 0.5, 1.5, 3.8, 1.5, desc, color)
    if i < 3:
        ax.annotate('', xy=(5, 2.25), xytext=(4.5, 2.25),
                    arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.5))
fig.suptitle('创建 Text 的四步流程', color='#fff', fontsize=17, fontweight='bold', y=1.05)
save('L02_02_create_text.png')
print('L02_02 done')

# L02_03: Inspector panels
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
ax.set_xlim(0, 9); ax.set_ylim(0, 5.5); ax.axis('off')
ax.set_title('TextMeshPro Inspector 面板解析', color='#fff', fontsize=17, fontweight='bold', pad=15)

sections = [('Text Input', '设置文字内容, Font Style, Font Size, Alignment', 1.2, 3.8, ACCENT),
            ('Main Settings', 'Font Asset, Material, Color, Spacing, Wrapping', 3.2, 3.8, GREEN),
            ('Extra Settings', 'Margins, Rich Text, Raycast Target', 5.2, 3.8, WARM)]
for title, desc, x, y, color in sections:
    box = FancyBboxPatch((x, y), 2.5, 1.3, boxstyle="round,pad=0.05", facecolor=color+'15', edgecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x+1.25, y+1.05, title, color=color, fontsize=12, ha='center', fontweight='bold')
    ax.text(x+1.25, y+0.45, desc, color=MUTED, fontsize=8, ha='center')

preview = FancyBboxPatch((0.5, 0.5), 8, 2.5, boxstyle="round,pad=0.05", facecolor='#111', edgecolor=BORDER, linewidth=1.5)
ax.add_patch(preview)
ax.text(4.5, 2.3, 'Hello World!', color='#fff', fontsize=24, ha='center', fontweight='bold')
ax.text(4.5, 1.5, 'Font: LiberationSans SDF  |  Size: 36  |  Color: White', color=MUTED, fontsize=11, ha='center')
ax.text(4.5, 1.0, '预览效果', color=MUTED, fontsize=10, ha='center', style='italic')
save('L02_03_inspector.png')
print('L02_03 done')

# L02_04: Text properties
fig, ax = plt.subplots(figsize=(9, 5))
ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
ax.set_xlim(0, 9); ax.set_ylim(0, 5); ax.axis('off')
ax.set_title('文字属性可视化', color='#fff', fontsize=17, fontweight='bold', pad=15)

for i, (size, label) in enumerate([(12, '小'), (18, '中'), (28, '大'), (40, '特大')]):
    ax.text(0.5, 4 - i*0.7, label + ' (' + str(size) + 'pt)', color=MUTED, fontsize=10)
    ax.text(2.5, 4 - i*0.7, 'Unity UI', color='#fff', fontsize=size, fontweight='bold')

colors_demo = [(RED, '红'), (WARM, '橙'), (YELLOW, '黄'), (GREEN, '绿'), (ACCENT, '蓝'), (PURPLE, '紫')]
for i, (color, label) in enumerate(colors_demo):
    ax.text(5 + i*0.55, 3.8, 'A', color=color, fontsize=18, fontweight='bold')
    ax.text(5 + i*0.55, 3.4, label, color=MUTED, fontsize=8, ha='center')

for i, (align, label) in enumerate([('left', '左对齐'), ('center', '居中'), ('right', '右对齐')]):
    box = FancyBboxPatch((5, 1.5 - i*0.6), 3.5, 0.45, boxstyle="round,pad=0.02", facecolor='#252525', edgecolor=BORDER, linewidth=1)
    ax.add_patch(box)
    x = 5.2 if align == 'left' else (8 if align == 'right' else 6.75)
    ax.text(x, 1.72 - i*0.6, label, color='#fff', fontsize=10, ha=align)

for i, (style, label) in enumerate([('normal', '普通'), ('bold', '粗体'), ('italic', '斜体')]):
    kw = {'fontweight': 'bold'} if style == 'bold' else {'fontstyle': 'italic'} if style == 'italic' else {}
    ax.text(0.5, 1.5 - i*0.6, label, color='#fff', fontsize=14, **kw)

save('L02_04_text_properties.png')
print('L02_04 done')

# L02_05: Hierarchy
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
ax.set_xlim(0, 7); ax.set_ylim(0, 4.5); ax.axis('off')
ax.set_title('创建 Text 后的 Hierarchy', color='#fff', fontsize=16, fontweight='bold', pad=15)

for i, (label, color, indent, highlight) in enumerate([
    ('Canvas', ACCENT, 0, False),
    ('EventSystem', YELLOW, 1, False),
    ('Text (TMP)  <-- 新增!', GREEN, 1, True)]):
    prefix = '  ' * indent + ('  L-- ' if indent > 0 else '  v ')
    box = FancyBboxPatch((0.5, 3.5 - i*0.8), 6, 0.55, boxstyle="round,pad=0.03",
                         facecolor=color+'25' if highlight else color+'15',
                         edgecolor=color, linewidth=2 if highlight else 1.2)
    ax.add_patch(box)
    ax.text(0.7, 3.77 - i*0.8, prefix + label, color='#fff', fontsize=13, va='center', fontfamily='monospace')

save('L02_05_hierarchy.png')
print('L02_05 done')

# L02_06: Rich Text
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
ax.set_xlim(0, 9); ax.set_ylim(0, 4.5); ax.axis('off')
ax.set_title('Rich Text 富文本示例', color='#fff', fontsize=17, fontweight='bold', pad=15)

examples = [('<b>粗体</b>', '粗体', GREEN), ('<i>斜体</i>', '斜体', ACCENT),
            ('<color=red>红色</color>', '红色', RED), ('<size=30>大字</size>', '大字', WARM),
            ('<s>删除线</s>', '删除线', MUTED)]
for i, (code, result, color) in enumerate(examples):
    y = 3.5 - i*0.7
    ax.text(0.5, y, code, color=MUTED, fontsize=11, fontfamily='monospace')
    ax.text(4.5, y, '-->', color=MUTED, fontsize=11)
    ax.text(5.5, y, result, color=color, fontsize=14, fontweight='bold')

ax.text(0.5, 0.8, '<b><color=#4ea1ff><size=24>VRChat</size></color></b>', color=MUTED, fontsize=10, fontfamily='monospace')
ax.text(4.5, 0.8, '-->', color=MUTED, fontsize=11)
ax.text(5.5, 0.8, 'VRChat', color=ACCENT, fontsize=20, fontweight='bold')

save('L02_06_rich_text.png')
print('L02_06 done')

print('ALL Lesson 2 done!')
