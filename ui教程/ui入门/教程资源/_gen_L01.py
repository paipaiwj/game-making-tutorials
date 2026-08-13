# -*- coding: utf-8 -*-
# L01 图片生成脚本：Canvas 与 UI 基础
exec(open("_header.py", encoding="utf-8").read())

# ── 图1: UI 系统全景图 ──
fig, ax = plt.subplots(figsize=(13, 7))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 13); ax.set_ylim(0, 7); ax.axis("off")
ax.set_title("Unity UI 系统全景图", color="#fff", fontsize=20, fontweight="bold", pad=20)

zones = [
    (0.5, 0.5, 3.8, 6, "Canvas\n画布", ACCENT, "所有 UI 的根容器\n决定渲染方式"),
    (4.8, 0.5, 3.8, 6, "UI 控件\nControls", GREEN, "Text / Image / Button\nSlider / Toggle / InputField"),
    (9.1, 0.5, 3.4, 6, "交互系统\nEventSystem", ORANGE, "处理点击、拖拽\n键盘输入等事件"),
]
for x, y, w, h, title, color, desc in zones:
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=PANEL, edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    ax.text(x+w/2, y+h-0.8, title, color=color, fontsize=14, fontweight="bold", ha="center", va="top")
    ax.text(x+w/2, y+h/2-0.2, desc, color=TEXT2, fontsize=11, ha="center", va="center")

for x1, x2 in [(4.3, 4.8), (8.6, 9.1)]:
    ax.annotate("", xy=(x2, 3.5), xytext=(x1, 3.5), arrowprops=dict(arrowstyle="->", color=MUTED, lw=2))

ax.text(6.5, 0.15, "三者协作才能构成完整的 UI 交互系统", color=TEXT2, fontsize=11, ha="center", style="italic")
save("L01_01_system_overview.png")

# ── 图2: Canvas 三种渲染模式 ──
fig, axes = plt.subplots(1, 3, figsize=(14, 5.5))
fig.patch.set_facecolor(DARK_BG)
modes = [
    ("Screen Space - Overlay", ACCENT, "覆盖在屏幕最上层\n始终可见，忽略摄像机\n适合 HUD、血条、准星"),
    ("Screen Space - Camera", GREEN, "绑定到指定摄像机\n可被 3D 物体遮挡\n适合瞄准镜、仪表盘"),
    ("World Space", ORANGE, "存在于 3D 世界中\n像普通物体一样放置\nVRChat 唯一可用模式！"),
]
for i, (ax_i, (title, color, desc)) in enumerate(zip(axes, modes)):
    ax_i.set_facecolor(PANEL)
    ax_i.set_xlim(0, 4); ax_i.set_ylim(0, 5); ax_i.axis("off")
    ax_i.set_title(title, color=color, fontsize=13, fontweight="bold", pad=10)
    rect = FancyBboxPatch((0.3, 0.3), 3.4, 4.4, boxstyle="round,pad=0.1", facecolor=PANEL2, edgecolor=color, linewidth=1.5)
    ax_i.add_patch(rect)
    ax_i.text(2, 2.5, desc, color=TEXT, fontsize=12, ha="center", va="center")
    if i == 2:
        ax_i.text(2, 0.6, "\u2605 VRChat \u4e13\u7528", color=RED, fontsize=10, ha="center", fontweight="bold")

plt.tight_layout()
save("L01_02_render_modes.png")

# ── 图3: Canvas 组件结构 ──
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
ax.set_title("Canvas 上的四大组件", color="#fff", fontsize=18, fontweight="bold", pad=15)

comps = [
    ("RectTransform", "位置/大小/锚点", ACCENT, 0.8),
    ("Canvas", "渲染模式/排序", GREEN, 3.6),
    ("Canvas Scaler", "缩放/适配", ORANGE, 6.4),
    ("Graphic Raycaster", "射线检测/点击", PURPLE, 9.2),
]
for name, desc, color, x in comps:
    rect = FancyBboxPatch((x, 1.2), 2.6, 3.2, boxstyle="round,pad=0.12", facecolor=PANEL, edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    ax.text(x+1.3, 3.8, name, color=color, fontsize=14, fontweight="bold", ha="center")
    ax.text(x+1.3, 2.6, desc, color=TEXT2, fontsize=11, ha="center")
    ax.text(x+1.3, 1.8, "\u5fc5\u987b", color=RED if name != "Canvas Scaler" else GREEN, fontsize=9, ha="center")

ax.text(6, 0.3, "Canvas Scaler \u867d\u6807\u8bb0\u4e3a\"\u53ef\u9009\"\uff0c\u4f46\u5728 VRChat \u4e2d\u5f3a\u70c8\u5efa\u8bae\u6dfb\u52a0\u4ee5\u9002\u914d\u4e0d\u540c\u5206\u8fa8\u7387", color=TEXT2, fontsize=10, ha="center", style="italic")
save("L01_03_canvas_components.png")

# ── 图4: RectTransform 锚点系统 ──
fig, axes = plt.subplots(2, 3, figsize=(13, 8))
fig.patch.set_facecolor(DARK_BG)
anchors = [
    ("\u5de6\u4e0a", (0, 0.5)), ("\u4e2d\u4e0a", (0.5, 0.5)), ("\u53f3\u4e0a", (1, 0.5)),
    ("\u5de6\u4e2d", (0, 0)), ("\u6b63\u4e2d", (0.5, 0)), ("\u53f3\u4e2d", (1, 0)),
]
for idx, ((name, (ax_pos, ay_pos)), ax_i) in enumerate(zip(anchors, axes.flat)):
    ax_i.set_facecolor(PANEL)
    ax_i.set_xlim(0, 4); ax_i.set_ylim(0, 4); ax_i.axis("off")
    ax_i.set_title(f"\u951a\u70b9: {name}", color=ACCENT2, fontsize=12, fontweight="bold")
    ax_i.add_patch(Rectangle((0.2, 0.2), 3.6, 3.6, fill=False, edgecolor=BORDER, lw=1))
    ax_i.plot(0.2 + ax_pos*3.6, 0.2 + ay_pos*3.6, "o", color=RED, markersize=10, zorder=5)
    w, h = 1.8, 1.2
    rx = 0.2 + ax_pos*3.6 - ax_pos*w
    ry = 0.2 + ay_pos*3.6 - ay_pos*h
    ax_i.add_patch(FancyBboxPatch((rx, ry), w, h, boxstyle="round,pad=0.05", facecolor=ACCENT+"30", edgecolor=ACCENT, lw=1.5))
    ax_i.text(rx+w/2, ry+h/2, "UI\n\u5143\u7d20", color=TEXT, fontsize=9, ha="center", va="center")

plt.suptitle("RectTransform \u951a\u70b9\u9884\u8bbe\uff086 \u79cd\u5e38\u7528\uff09", color="#fff", fontsize=16, fontweight="bold", y=1.01)
plt.tight_layout()
save("L01_04_anchor_presets.png")

# ── 图5: 创建 Canvas 的层级结构 ──
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_facecolor(DARK_BG); fig.patch.set_facecolor(DARK_BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
ax.set_title("\u521b\u5efa Canvas \u540e\u7684\u5c42\u7ea7\u7ed3\u6784", color="#fff", fontsize=18, fontweight="bold", pad=15)

nodes = [
    (5, 6.2, "Scene Root", MUTED, 2.0),
    (2.5, 4.8, "Canvas", ACCENT, 1.8),
    (7.5, 4.8, "EventSystem", ORANGE, 1.8),
    (2.5, 3.2, "Canvas \u5b50\u7269\u4f53\n(Text, Image, Button...)", GREEN, 2.4),
]
for x, y, label, color, w in nodes:
    rect = FancyBboxPatch((x-w/2, y-0.45), w, 0.9, boxstyle="round,pad=0.08", facecolor=PANEL, edgecolor=color, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, y, label, color=TEXT if color == MUTED else color, fontsize=11, ha="center", va="center", fontweight="bold" if color == ACCENT else "normal")

ax.plot([5, 2.5], [5.75, 5.25], color=MUTED, lw=1.5)
ax.plot([5, 7.5], [5.75, 5.25], color=MUTED, lw=1.5)
ax.plot([2.5, 2.5], [4.35, 3.65], color=MUTED, lw=1.5)

ax.annotate("Canvas \u548c EventSystem\n\u662f\u540c\u7ea7\u5173\u7cfb\uff0c\u4e0d\u662f\u7236\u5b50\uff01", xy=(5, 4.8), xytext=(8.5, 5.8),
    arrowprops=dict(arrowstyle="->", color=RED, lw=1.5), color=RED, fontsize=10, ha="center",
    bbox=dict(boxstyle="round,pad=0.3", facecolor=PANEL2, edgecolor=RED, alpha=0.9))

ax.text(5, 0.5, "EventSystem \u8d1f\u8d23\u5904\u7406\u6240\u6709\u8f93\u5165\u4e8b\u4ef6\uff0c\u6ca1\u6709\u5b83\u6309\u94ae\u5c06\u65e0\u6cd5\u70b9\u51fb", color=TEXT2, fontsize=10, ha="center", style="italic")
save("L01_05_hierarchy.png")

print("L01 all images generated!")
