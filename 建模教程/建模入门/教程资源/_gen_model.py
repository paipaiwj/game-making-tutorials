# -*- coding: utf-8 -*-
# Blender 建模入门教程（面向 Unity + VRChat）— 配图生成脚本
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _render_svg import *


def draw_cube(dwg, ox, oy, w, h, dx=55, dy=-35, stroke="#3a3a3a", width=1.5):
    """画一个等距立方体线框，返回 8 个顶点 (A,B,C,D,A2,B2,C2,D2)"""
    A = (ox, oy); B = (ox + w, oy); C = (ox + w, oy + h); D = (ox, oy + h)
    A2 = (ox + dx, oy + dy); B2 = (ox + w + dx, oy + dy)
    C2 = (ox + w + dx, oy + h + dy); D2 = (ox + dx, oy + h + dy)
    for p, q in [(A2, B2), (B2, C2), (C2, D2), (D2, A2)]:
        add_line(dwg, p[0], p[1], q[0], q[1], stroke="#2f2f2f", stroke_width=width)
    for p, q in [(A, B), (B, C), (C, D), (D, A)]:
        add_line(dwg, p[0], p[1], q[0], q[1], stroke=stroke, stroke_width=width)
    for p, q in [(A, A2), (B, B2), (C, C2), (D, D2)]:
        add_line(dwg, p[0], p[1], q[0], q[1], stroke="#2f2f2f", stroke_width=width)
    return A, B, C, D, A2, B2, C2, D2


def fill_face(dwg, pts, fill=ACCENT, opacity=0.18):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts) + " Z"
    dwg.add(dwg.path(d=d, fill=fill, opacity=opacity, stroke="none"))


def draw_polygon_circle(dwg, cx, cy, r, n, stroke=ACCENT, width=2, fill=None):
    pts = [(cx + r * math.cos(i * 2 * math.pi / n), cy + r * math.sin(i * 2 * math.pi / n))
           for i in range(n)]
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        add_line(dwg, p[0], p[1], q[0], q[1], stroke=stroke, stroke_width=width)
    if fill:
        d = "M" + " L".join(f"{x},{y}" for x, y in pts) + " Z"
        dwg.add(dwg.path(d=d, fill=fill, opacity=0.4, stroke="none"))
    return pts


# ============================================================
# L01 — 图1: 顶点/边/面
# ============================================================
def make_L01_01_vertex_edge_face():
    W, H = 900, 540
    dwg = new_svg(W, H)
    add_text(dwg, "3D 模型三要素：顶点、边、面", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "所有 3D 模型，都是由这三样东西拼出来的", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # 立方体
    A, B, C, D, A2, B2, C2, D2 = draw_cube(dwg, 140, 170, 180, 160, dx=80, dy=-55, stroke=TEXT_DIM)
    # 顶面高亮（面 Face）
    fill_face(dwg, [A, B, B2, A2], fill=ACCENT, opacity=0.22)
    add_text(dwg, "面 Face", 270, 143, fill=ACCENT, size=12.5, weight="bold", anchor="middle")
    # 边高亮（顶面后边 A2-B2）
    add_line(dwg, A2[0], A2[1], B2[0], B2[1], stroke=SUCCESS, stroke_width=3)
    add_line(dwg, 320, 105, 320, 92, stroke=SUCCESS, stroke_width=1.5)
    add_text(dwg, "边 Edge", 320, 86, fill=SUCCESS, size=12.5, weight="bold", anchor="middle")
    # 顶点高亮 D
    add_ellipse(dwg, D[0], D[1], 7, 7, fill=WARM)
    add_line(dwg, D[0], D[1], 108, 348, stroke=WARM, stroke_width=1.5)
    add_text(dwg, "顶点 Vertex", 40, 352, fill=WARM, size=12.5, weight="bold")

    # 右侧三张卡片
    cards = [
        ("顶点 Vertex", "网格的交点，决定形状轮廓\n移动顶点 = 改变形状", ACCENT),
        ("边 Edge", "连接两个顶点的线段\n边围起来才形成面", SUCCESS),
        ("面 Face", "三个以上顶点围成的区域\n渲染时真正看到的表面", WARM),
    ]
    for i, (title, desc, color) in enumerate(cards):
        y = 92 + i * 122
        add_rect(dwg, 410, y, 440, 108, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_ellipse(dwg, 440, y + 26, 7, 7, fill=color)
        add_text(dwg, title, 462, y + 32, fill="#fff", size=14, weight="bold")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, 462, y + 62 + j * 20, fill=TEXT_DIM, size=12)

    add_rect(dwg, 100, 456, 700, 56, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "网格 Mesh = 顶点 + 边 + 面的集合。VRChat 世界里你看到的每个道具、家具，都是网格", 450, 488, fill=SUCCESS, size=13, anchor="middle")
    save_svg_and_png(dwg, "L01_01_vertex_edge_face")


# ============================================================
# L01 — 图2: 面数 vs 质量
# ============================================================
def make_L01_02_polycount():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "面数 Polycount：少而精", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "面数越多越精细，但越吃性能 —— VRChat 里要平衡", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # 低模
    add_rect(dwg, 60, 92, 360, 240, fill=PANEL, stroke=WARM, rx=10, stroke_width=2)
    draw_polygon_circle(dwg, 240, 205, 78, 8, stroke=WARM, width=2)
    add_text(dwg, "低模 Low Poly", 240, 275, fill="#fff", size=14, weight="bold", anchor="middle")
    add_text(dwg, "几百 ~ 几千面", 240, 300, fill=TEXT_DIM, size=12, anchor="middle")

    # 高模
    add_rect(dwg, 480, 92, 360, 240, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    draw_polygon_circle(dwg, 660, 205, 78, 24, stroke=ACCENT, width=1.2)
    add_text(dwg, "高模 High Poly", 660, 275, fill="#fff", size=14, weight="bold", anchor="middle")
    add_text(dwg, "几万 ~ 百万面", 660, 300, fill=TEXT_DIM, size=12, anchor="middle")

    add_arrow(dwg, 432, 205, 466, 205, stroke=TEXT_MUTED, stroke_width=2)
    add_text(dwg, "vs", 449, 195, fill=TEXT_MUTED, size=12, weight="bold", anchor="middle")

    add_rect(dwg, 60, 360, 780, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "VRChat 性能要点", 90, 388, fill=WARN, size=14, weight="bold")
    add_text(dwg, "场景道具建议几千面以内，整世界控制在百万面以内；面数越多，别人进入你的世界越卡", 90, 414, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "技巧：高模只用来雕刻细节，最终进 VRChat 的用低模 + 法线贴图模拟细节", 90, 438, fill=SUCCESS, size=12.5)
    save_svg_and_png(dwg, "L01_02_polycount")


# ============================================================
# L02 — 图1: Blender 界面布局
# ============================================================
def make_L02_01_blender_ui():
    W, H = 900, 520
    dwg = new_svg(W, H)
    add_text(dwg, "Blender 界面布局（打开就是这样一个窗口）", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 主窗口
    add_rect(dwg, 60, 60, 780, 400, fill="#242424", stroke=BORDER, rx=8, stroke_width=2)
    # 菜单栏
    add_rect(dwg, 60, 60, 780, 30, fill=PANEL, stroke=BORDER, rx=0)
    add_text(dwg, "File   Edit   Render   Window   Help", 76, 80, fill=TEXT_MUTED, size=11)
    add_text(dwg, "顶部菜单栏", 640, 80, fill="#555555", size=10)
    # 3D 视图
    add_rect(dwg, 60, 90, 540, 250, fill="#191919", stroke="#333333")
    for i in range(6):
        add_line(dwg, 80 + i * 85, 90, 80 + i * 85, 340, stroke="#242424", stroke_width=1)
    for i in range(5):
        add_line(dwg, 60, 110 + i * 48, 600, 110 + i * 48, stroke="#242424", stroke_width=1)
    # 3D 视图中心小立方体
    draw_cube(dwg, 300, 190, 55, 55, dx=20, dy=-14, stroke="#888888", width=1.5)
    # 坐标轴指示（右下角）
    add_line(dwg, 560, 320, 575, 308, stroke="#e06060", stroke_width=2.5)
    add_line(dwg, 560, 320, 560, 304, stroke="#60b060", stroke_width=2.5)
    add_line(dwg, 560, 320, 576, 322, stroke="#6090e0", stroke_width=2.5)
    add_text(dwg, "X", 580, 306, fill="#e06060", size=10, weight="bold")
    add_text(dwg, "Y", 561, 299, fill="#60b060", size=10, weight="bold")
    add_text(dwg, "Z", 582, 326, fill="#6090e0", size=10, weight="bold")
    add_text(dwg, "3D 视图：建模主战场（网格地面 + 中心物体）", 78, 116, fill=ACCENT, size=12.5, weight="bold")
    # 大纲
    add_rect(dwg, 600, 90, 240, 250, fill="#1f1f1f", stroke="#333333")
    add_text(dwg, "大纲 Outliner：场景对象列表", 616, 116, fill=SUCCESS, size=12.5, weight="bold")
    for i, name in enumerate(["Scene 场景", "Cube 方块", "Camera 相机", "Light 灯光"]):
        add_ellipse(dwg, 624, 148 + i * 36, 4, 4, fill=ACCENT)
        add_text(dwg, name, 636, 152 + i * 36, fill=TEXT_DIM, size=11.5)
    # 属性面板
    add_rect(dwg, 600, 340, 240, 120, fill="#1f1f1f", stroke="#333333")
    add_text(dwg, "属性面板 Properties", 616, 366, fill=WARM, size=12.5, weight="bold")
    add_text(dwg, "调整选中对象的参数", 616, 388, fill=TEXT_DIM, size=11)
    # 时间线
    add_rect(dwg, 60, 340, 540, 120, fill="#1c1c1c", stroke="#333333")
    add_text(dwg, "时间线 Timeline（做动画才用）", 76, 366, fill=TEXT_DIM, size=12.5, weight="bold")
    add_line(dwg, 76, 386, 580, 386, stroke="#333333", stroke_width=2)
    add_ellipse(dwg, 110, 386, 5, 5, fill=WARM)
    add_text(dwg, "帧指针", 122, 390, fill=TEXT_MUTED, size=10.5)

    add_rect(dwg, 100, 478, 700, 32, fill="#1a1a1a", stroke=BORDER, rx=16)
    add_text(dwg, "先适应视图：鼠标滚轮缩放、中键拖动旋转 —— 建模期 80% 时间都在 3D 视图里", 450, 499, fill=TEXT_DIM, size=12, anchor="middle")
    save_svg_and_png(dwg, "L02_01_blender_ui")


# ============================================================
# L02 — 图2: 常用快捷键卡片
# ============================================================
def make_L02_02_shortcuts():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "建模三巨头：移动 / 旋转 / 缩放", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    cards = [
        ("G", "移动 Move", "选中物体 → 按 G\n拖动鼠标移动\nG + X / Y / Z 沿指定轴", ACCENT),
        ("R", "旋转 Rotate", "选中物体 → 按 R\n拖动鼠标旋转\nR + X 绕 X 轴旋转", SUCCESS),
        ("S", "缩放 Scale", "选中物体 → 按 S\n拖动鼠标缩放\nS + 数字输入比例", WARM),
    ]
    for i, (key, name, desc, color) in enumerate(cards):
        x = 60 + i * 270
        add_rect(dwg, x, 90, 250, 200, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, key, x + 125, 150, fill=color, size=42, weight="bold", anchor="middle")
        add_text(dwg, name, x + 125, 185, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + 125, 210 + j * 20, fill=TEXT_DIM, size=11.5, anchor="middle")

    add_text(dwg, "正交视图（数字小键盘 NumPad）", W//2, 325, fill=TEXT, size=14, weight="bold", anchor="middle")
    views = [("1", "前视图"), ("3", "右视图"), ("7", "顶视图"), ("5", "透视图")]
    for i, (num, name) in enumerate(views):
        x = 165 + i * 150
        add_rect(dwg, x, 340, 120, 40, fill="#1a1a1a", stroke=ACCENT, rx=8)
        add_text(dwg, num, x + 22, 366, fill="#9ecbff", size=15, weight="bold", anchor="middle")
        add_text(dwg, name, x + 62, 366, fill=TEXT_DIM, size=12, anchor="middle")

    add_text(dwg, "小提示：先按字母键，再移动鼠标；左键点击确认，右键取消", W//2, 430, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L02_02_shortcuts")


# ============================================================
# L03 — 图1: 挤出操作
# ============================================================
def make_L03_01_extrude():
    W, H = 900, 520
    dwg = new_svg(W, H)
    add_text(dwg, "挤出 Extrude（E）：建模最常用的操作", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "把选中的面「拉长」出一段新网格，造箱子、椅子、墙都靠它", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # 左：挤出前
    add_rect(dwg, 60, 90, 360, 300, fill=PANEL, stroke=BORDER, rx=10)
    A, B, C, D, A2, B2, C2, D2 = draw_cube(dwg, 140, 195, 170, 150, dx=55, dy=-38, stroke=TEXT_DIM)
    fill_face(dwg, [A, B, B2, A2], fill=ACCENT, opacity=0.22)
    add_text(dwg, "选中顶面", 245, 168, fill=ACCENT, size=12, weight="bold", anchor="middle")
    add_text(dwg, "挤出前", 240, 372, fill="#fff", size=13.5, weight="bold", anchor="middle")

    # 箭头
    add_arrow(dwg, 432, 290, 466, 290, stroke=WARM, stroke_width=2.5)

    # 右：挤出后（两段）
    add_rect(dwg, 480, 90, 360, 300, fill=PANEL, stroke=BORDER, rx=10)
    A, B, C, D, A2, B2, C2, D2 = draw_cube(dwg, 540, 240, 170, 150, dx=55, dy=-38, stroke=TEXT_DIM)
    # 上段
    A3 = (A[0], A[1] - 62); B3 = (B[0], B[1] - 62); B4 = (B2[0], B2[1] - 62); A4 = (A2[0], A2[1] - 62)
    for p, q in [(A3, B3), (B3, B4), (B4, A4), (A4, A3)]:
        add_line(dwg, p[0], p[1], q[0], q[1], stroke=SUCCESS, stroke_width=2)
    for p, q in [(A, A3), (B, B3), (B2, B4), (A2, A4)]:
        add_line(dwg, p[0], p[1], q[0], q[1], stroke=SUCCESS, stroke_width=2)
    fill_face(dwg, [A3, B3, B4, A4], fill=SUCCESS, opacity=0.2)
    add_text(dwg, "按 E 后向上拖动", 620, 218, fill=SUCCESS, size=12, weight="bold", anchor="middle")
    add_text(dwg, "挤出后（高亮=新长出的一段）", 660, 372, fill="#fff", size=13.5, weight="bold", anchor="middle")

    add_rect(dwg, 60, 410, 780, 80, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "操作步骤", 90, 438, fill=WARN, size=14, weight="bold")
    add_text(dwg, "① Tab 进入编辑模式  ② 选中顶面（右键）  ③ 按 E  ④ 向上拖动鼠标  ⑤ 左键确认", 90, 462, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "配合 Ctrl+R 环切加分段，可以继续拉伸、压扁，做出椅子腿、桌面等形状", 90, 484, fill=SUCCESS, size=12.5)
    save_svg_and_png(dwg, "L03_01_extrude")


# ============================================================
# L03 — 图2: 修改器
# ============================================================
def make_L03_02_modifiers():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "常用修改器 Modifiers（属性面板里的扳手图标）", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    mods = [
        ("细分 Subdivision", "让模型变光滑\n面数会变多", SUCCESS),
        ("镜像 Mirror", "只做一半\n自动对称另一半", ACCENT),
        ("布尔 Boolean", "用 A 减去 B\n挖洞、开窗", WARM),
        ("实体化 Solidify", "给薄片加厚度\n薄墙变厚墙", "#c084fc"),
    ]
    for i, (title, desc, color) in enumerate(mods):
        x = 60 + i * 200
        add_rect(dwg, x, 80, 185, 250, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + 92, 108, fill="#fff", size=12.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + 92, 134 + j * 18, fill=TEXT_DIM, size=11, anchor="middle")
        # 小示意图
        sy, sh = 175, 130
        if i == 0:
            for gx in range(3):
                for gy in range(3):
                    add_ellipse(dwg, x + 45 + gx * 45, sy + 20 + gy * 42, 5, 5, fill=SUCCESS)
            add_text(dwg, "2 级细分", x + 92, sy + 150, fill=TEXT_MUTED, size=10.5, anchor="middle")
        elif i == 1:
            d = f"M{x+60},{sy+20} A 45,45 0 0 0 {x+60},{sy+110} Z"
            dwg.add(dwg.path(d=d, fill=ACCENT, opacity=0.5, stroke=ACCENT, stroke_width=1.5))
            add_line(dwg, x + 105, sy + 10, x + 105, sy + 120, stroke=TEXT_MUTED, stroke_width=1.5, dash=[4, 3])
            add_text(dwg, "镜像轴", x + 105, sy + 145, fill=TEXT_MUTED, size=10.5, anchor="middle")
        elif i == 2:
            add_rect(dwg, x + 35, sy + 10, 75, 55, fill="none", stroke=WARM, stroke_width=2)
            add_ellipse(dwg, x + 100, sy + 45, 28, 28, fill=WARM, opacity=0.5, stroke=WARM, stroke_width=1.5)
            add_text(dwg, "A 减 B = 挖洞", x + 92, sy + 145, fill=TEXT_MUTED, size=10.5, anchor="middle")
        else:
            add_line(dwg, x + 40, sy + 40, x + 140, sy + 40, stroke=TEXT_MUTED, stroke_width=3)
            add_arrow(dwg, x + 100, sy + 95, x + 135, sy + 95, stroke="#c084fc", stroke_width=2)
            add_rect(dwg, x + 35, sy + 80, 55, 30, fill="#c084fc", opacity=0.4, stroke="#c084fc", stroke_width=1.5)
            add_text(dwg, "加厚度", x + 92, sy + 145, fill=TEXT_MUTED, size=10.5, anchor="middle")

    add_rect(dwg, 60, 350, 780, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "修改器不会破坏原始网格，可随时开关、调参数、删除", 90, 380, fill=SUCCESS, size=13, weight="bold")
    add_text(dwg, "但导出到 Unity 前一定要在修改器上点 Apply 应用 —— 否则 Unity 里看不到效果", 90, 406, fill=WARN, size=12.5)
    add_text(dwg, "注意：细分、布尔会显著增加面数，应用前先想好预算", 90, 430, fill=TEXT_DIM, size=12.5)
    save_svg_and_png(dwg, "L03_02_modifiers")


# ============================================================
# L04 — 图1: UV 展开
# ============================================================
def make_L04_01_uv_unwrap():
    W, H = 900, 520
    dwg = new_svg(W, H)
    add_text(dwg, "展 UV：把 3D 表面摊平成 2D 地图", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "给立方体每个面编号 —— 展开后贴图才能准确贴到每个面上", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # 左：3D 立方体带编号
    add_rect(dwg, 60, 90, 300, 300, fill=PANEL, stroke=BORDER, rx=10)
    A, B, C, D, A2, B2, C2, D2 = draw_cube(dwg, 115, 205, 170, 150, dx=55, dy=-38, stroke=TEXT_DIM)
    add_text(dwg, "1", 242, 152, fill=ACCENT, size=13, weight="bold", anchor="middle")
    add_text(dwg, "5", 112, 280, fill=WARM, size=13, weight="bold", anchor="middle")
    add_text(dwg, "3", 200, 330, fill=SUCCESS, size=13, weight="bold", anchor="middle")
    add_text(dwg, "3D 立方体", 210, 375, fill="#fff", size=13, weight="bold", anchor="middle")

    # 箭头
    add_arrow(dwg, 372, 250, 410, 250, stroke=ACCENT, stroke_width=2.5)
    add_text(dwg, "U 菜单", 380, 214, fill=ACCENT, size=11, weight="bold", anchor="middle")
    add_text(dwg, "→ Unwrap", 380, 236, fill=ACCENT, size=11, weight="bold", anchor="middle")

    # 右：UV 展开十字
    add_rect(dwg, 430, 90, 420, 300, fill=PANEL, stroke=SUCCESS, rx=10)
    cells = [
        (620, 112, "1", ACCENT),
        (570, 162, "3", SUCCESS),
        (620, 162, "5", WARM),
        (670, 162, "4", "#c084fc"),
        (720, 162, "6", "#ffcc66"),
        (620, 212, "2", TEXT_MUTED),
    ]
    for (cx, cy, label, color) in cells:
        add_rect(dwg, cx - 22, cy - 22, 44, 44, fill="#1a1a1a", stroke=color, rx=4, stroke_width=2)
        add_text(dwg, label, cx, cy + 6, fill=color, size=14, weight="bold", anchor="middle")
    add_text(dwg, "UV 编辑器：六个面摊平成十字", 640, 295, fill="#fff", size=12.5, weight="bold", anchor="middle")
    add_text(dwg, "贴图图片", 760, 120, fill=TEXT_DIM, size=11, anchor="middle")

    add_rect(dwg, 60, 410, 780, 80, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "操作：编辑模式 → A 全选 → U 菜单 → Unwrap", 90, 438, fill=ACCENT, size=12.5, weight="bold")
    add_text(dwg, "UV 坐标告诉贴图「这个面的颜色从图片的哪一块取」—— 展得越平整，贴图越不拉伸变形", 90, 462, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "简单物体（箱子/墙）自动 Unwrap 就够；复杂物体要手动切缝（Mark Seam）", 90, 482, fill=WARN, size=11.5)
    save_svg_and_png(dwg, "L04_01_uv_unwrap")


# ============================================================
# L04 — 图2: 材质与贴图流程
# ============================================================
def make_L04_02_material():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "材质 Material：给模型上色", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "完整流程：建模 → 展 UV → 画贴图 → 建材质 → 指定贴图", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1 建模", "做好形状\n检查面数", ACCENT),
        ("2 展 UV", "U → Unwrap\n摊平表面", SUCCESS),
        ("3 画贴图", "PS / 在线工具\n画颜色细节", WARM),
        ("4 建材质", "材质属性面板\n(球图标) → New", "#c084fc"),
        ("5 指定贴图", "Base Color 选贴图\n或直接填颜色", "#ff9e4e"),
    ]
    card_w, card_h = 155, 170
    start_x = (W - (card_w * 5 + 15 * 4)) // 2
    for i, (title, desc, color) in enumerate(steps):
        x = start_x + i * (card_w + 15)
        add_rect(dwg, x, 95, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 122, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 150 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")
        if i < 4:
            add_arrow(dwg, x + card_w + 2, 180, x + card_w + 13, 180, stroke=color, stroke_width=2)

    add_rect(dwg, 60, 290, 780, 70, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "材质面板操作：选中模型 → 右侧属性面板 → 材质（球图标）→ New → Base Color 选颜色或贴图片", 90, 318, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "只想要纯色？不用画贴图，Base Color 直接选颜色就行", 90, 342, fill=SUCCESS, size=12)

    add_rect(dwg, 60, 380, 780, 70, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "贴图尺寸：VRChat 常用 1024 / 2048", 90, 408, fill=WARN, size=13, weight="bold")
    add_text(dwg, "贴图越大越清晰也越吃显存 —— 小物件 512/1024 就够，别一上来就 4096；多个小物件共用一张贴图（合图）最省", 90, 432, fill=TEXT_DIM, size=12.5)
    save_svg_and_png(dwg, "L04_02_material")


# ============================================================
# L05 — 图1: 导出流程
# ============================================================
def make_L05_01_export_flow():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "导出流程：Blender → FBX → Unity", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "FBX 是 Unity 与 Blender 之间的「通用语言」，VRChat 世界资产都用它", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    boxes = [
        ("Blender 建模", ["建模完成", "检查法线：编辑模式全选", "Shift+N 重算法线", "Ctrl+A 应用全部变换"], ACCENT),
        ("导出 FBX", ["File → Export → FBX", "勾选 Apply Transforms", "勾选 Mesh / 材质", "路径别用中文"], SUCCESS),
        ("Unity 导入", ["FBX 拖进 Assets", "Scale Factor 保持 1", "材质若丢失重新指定", "给物体加 Collider"], WARM),
    ]
    for i, (title, items, color) in enumerate(boxes):
        x = 60 + i * 265
        add_rect(dwg, x, 95, 245, 200, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + 122, 124, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, item in enumerate(items):
            add_text(dwg, "· " + item, x + 18, 152 + j * 22, fill=TEXT_DIM, size=11.5)
        if i < 2:
            add_arrow(dwg, x + 250, 195, x + 258, 195, stroke=color, stroke_width=2.5)

    add_rect(dwg, 60, 320, 780, 110, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "关于缩放（重要，别被老教程带偏）", 90, 350, fill=WARN, size=14, weight="bold")
    add_text(dwg, "Blender 默认单位是米，Unity 也是米 —— 正常 1:1 导入即可，不要乘 0.01", 90, 378, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "只有当你发现模型巨大/微小、或导出前单位被改成厘米/英尺时，才需要检查 Scale", 90, 402, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "标准做法：Blender 单位确认是米 + 导出勾 Apply Transforms + Unity Scale Factor = 1", 90, 424, fill=SUCCESS, size=12.5)
    save_svg_and_png(dwg, "L05_01_export_flow")


# ============================================================
# L05 — 图2: Unity 导入要点
# ============================================================
def make_L05_02_import_unity():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "Unity 导入 FBX 后的检查要点", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 左卡片：导入设置
    add_rect(dwg, 60, 85, 380, 270, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    add_text(dwg, "导入设置（选中 FBX → Inspector）", 84, 115, fill="#fff", size=13.5, weight="bold")
    rows_l = [
        ("Scale Factor", "保持 1（单位都是米）", ACCENT),
        ("Read/Write", "默认勾选即可", TEXT_DIM),
        ("材质导入", "Standard / PBR 材质", SUCCESS),
        ("动画", "无动画的网格不用勾", TEXT_DIM),
    ]
    for i, (name, val, color) in enumerate(rows_l):
        y = 140 + i * 34
        add_text(dwg, name, 84, y, fill=color, size=12, weight="bold")
        add_text(dwg, val, 200, y, fill=TEXT_DIM, size=12)
    add_rect(dwg, 80, 285, 340, 48, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "改了设置要点右下角 Apply 才生效", 250, 314, fill=WARN, size=12, anchor="middle")

    # 右卡片：进场景后
    add_rect(dwg, 460, 85, 380, 270, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=2)
    add_text(dwg, "拖进场景后", 484, 115, fill="#fff", size=13.5, weight="bold")
    rows_r = [
        ("黑面 / 半透明", ["法线反了 → 回 Blender 全选", "Shift+N 重算 / Flip Normals 再导出"], WARN),
        ("没贴图发白", ["FBX 没带材质 → 贴图放 Assets", "在材质面板重新指定"], TEXT_DIM),
        ("位置 / 朝向偏", ["没应用变换 → 回 Blender", "Ctrl+A 后再导出一次"], TEXT_DIM),
    ]
    for i, (name, lines, color) in enumerate(rows_r):
        y = 140 + i * 66
        add_text(dwg, "· " + name, 484, y, fill=color, size=12, weight="bold")
        for j, line in enumerate(lines):
            add_text(dwg, line, 484, y + 22 + j * 19, fill=TEXT_DIM, size=11)

    add_rect(dwg, 60, 375, 780, 75, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "Collider 碰撞体：Unity 里没有 Collider 的物体，玩家能「穿过」它", 90, 403, fill=ACCENT, size=13, weight="bold")
    add_text(dwg, "简单形状（地板/墙）用 Box Collider 最省；复杂道具用 Mesh Collider（不要勾 Convex 以免变形）", 90, 427, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "VRChat 中拾取物体（Pickup）需要 Collider + Rigidbody（isKinematic）", 90, 447, fill=TEXT_DIM, size=11.5)
    save_svg_and_png(dwg, "L05_02_import_unity")


# ============================================================
# L06 — 图1: 快捷键速查表
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "Blender 快捷键速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    items = [
        ("Tab", "编辑模式 / 对象模式 切换", ACCENT),
        ("G", "移动 Move（G+X 沿 X 轴）", ACCENT),
        ("R", "旋转 Rotate（R+X 绕 X 轴）", ACCENT),
        ("S", "缩放 Scale（S+数字 输入比例）", ACCENT),
        ("E", "挤出 Extrude（编辑模式）", SUCCESS),
        ("Ctrl+R", "环切 Loop Cut（加分段）", SUCCESS),
        ("A", "全选 / Alt+A 取消全选", SUCCESS),
        ("Z", "切换线框 / 实体显示", SUCCESS),
        ("Shift+右键", "设置 3D 游标位置", WARM),
        ("Ctrl+Z", "撤销 Undo", WARM),
        ("X", "删除所选（Del）", WARM),
        ("Ctrl+A", "应用变换 Apply（导出前必做）", WARM),
    ]
    col_w = 390
    for i, (key, desc, color) in enumerate(items):
        row, col = divmod(i, 2)
        x = 60 + col * (col_w + 30)
        y = 68 + row * 76
        add_rect(dwg, x, y, col_w, 62, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        add_rect(dwg, x + 14, y + 14, 92, 34, fill="#1a1a1a", stroke=color, rx=6)
        add_text(dwg, key, x + 60, y + 37, fill="#9ecbff", size=13, weight="bold", anchor="middle")
        add_text(dwg, desc, x + 126, y + 37, fill=TEXT_DIM, size=12)

    add_text(dwg, "记不住没关系：多用就熟了。建模时手边放这张表，一周后就能记住八成", W//2, 542, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_01_cheatsheet")


# ============================================================
# L06 — 图2: 常见问题对照表
# ============================================================
def make_L06_02_common_issues():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "常见问题对照表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    col_w = [160, 250, 370]
    xs = [60, 230, 490]
    for hd, x in zip(["问题现象", "常见原因", "解决办法"], xs):
        add_rect(dwg, x, 66, col_w[0], 34, fill=PANEL, stroke=ACCENT, stroke_width=1.5)
        add_text(dwg, hd, x + col_w[0]//2, 88, fill=ACCENT, size=13, weight="bold", anchor="middle")

    rows = [
        ("模型是黑的 / 半透明", "法线方向反了", "编辑模式全选 → Shift+N 重算法线；必要时 Flip Normals 再导出", WARN),
        ("导入后巨大或微小", "单位或 Scale 不对", "确认 Blender 单位是米，导出勾 Apply Transforms，Scale Factor=1", WARN),
        ("导出后发白没贴图", "材质 / 贴图没带上", "FBX 勾选嵌入贴图，或贴图放 Assets 重新指定", WARN),
        ("面数爆炸、进世界卡", "细分 / 网格太密", "看三角面数统计，降细分等级，用减面修改器或 LOD", ACCENT),
        ("位置 / 朝向不对", "没应用变换", "导出前 Ctrl+A 应用全部变换，再重新导出", ACCENT),
        ("布尔后破面烂边", "布尔网格质量差", "布尔前先 Ctrl+A 并检查法线；必要时手动补面", SUCCESS),
    ]
    for i, (prob, cause, sol, color) in enumerate(rows):
        y = 100 + i * 70
        add_rect(dwg, 60, y, col_w[0], 62, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, prob, 60 + col_w[0]//2, y + 36, fill="#fff", size=12, weight="bold", anchor="middle")
        add_rect(dwg, 230, y, col_w[1], 62, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, cause, 230 + col_w[1]//2, y + 36, fill=color, size=12, anchor="middle")
        add_rect(dwg, 490, y, col_w[2], 62, fill=PANEL, stroke=SUCCESS, rx=6)
        add_text(dwg, sol, 506, y + 36, fill=SUCCESS, size=11, anchor="start")

    add_text(dwg, "调试心法：先检查法线，再检查单位 —— 模型 80% 的怪问题出在这两处", W//2, 548, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_02_common_issues")


# ============================================================
# L06 — 图3: 进阶路线图
# ============================================================
def make_L06_03_roadmap():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "建模进阶路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "按这个顺序学，每一步都建立在上一部之上", W//2, 60, fill=TEXT_DIM, size=13, anchor="middle")

    stages = [
        ("入门 · 会基础操作", "认识界面 + 快捷键\n做出箱子和椅子", ACCENT, "1 周"),
        ("熟练 · 会做小道具", "挤出 / 修改器 / 对称\n桌、凳、柜、路牌", SUCCESS, "2-4 周"),
        ("进阶 · 会完整资产", "展 UV + 材质 + 贴图\n优化面数 + 导出 Unity", WARM, "1-2 月"),
        ("精通 · 会做场景", "整套场景资产\n性能达标 + 布景", "#c084fc", "长期"),
    ]
    box_w, box_h = 180, 150
    start_x = (W - (box_w * 4 + 30 * 3)) // 2
    for i, (title, desc, color, time) in enumerate(stages):
        x = start_x + i * (box_w + 30)
        y = 88
        add_rect(dwg, x, y, box_w, box_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, y + 28, fill="#fff", size=12.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + box_w//2, y + 56 + j * 19, fill=TEXT_DIM, size=11, anchor="middle")
        add_text(dwg, f"{time}", x + box_w//2, y + box_h - 14, fill=color, size=11.5, anchor="middle")
        if i < 3:
            add_arrow(dwg, x + box_w + 2, y + box_h//2, x + box_w + 28, y + box_h//2, stroke=color, stroke_width=2)

    add_rect(dwg, 60, 272, 780, 150, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "学习建议", 90, 300, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "① 每天 20 分钟，跟着本篇从头做一遍箱子 → 椅子，比看十小时视频有用", 90, 328, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "② 快捷键先记住 G/R/S/E/Tab 五个，其他的用到再查表", 90, 352, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "③ 从身边小物件开始：杯子、板凳、路灯 —— 做完立刻导出进 VRChat 测试", 90, 376, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "④ 面数意识从第一天就要有：能少一分的面，绝不白白多加", 90, 400, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L06_03_roadmap")


if __name__ == "__main__":
    for f in [make_L01_01_vertex_edge_face, make_L01_02_polycount,
              make_L02_01_blender_ui, make_L02_02_shortcuts,
              make_L03_01_extrude, make_L03_02_modifiers,
              make_L04_01_uv_unwrap, make_L04_02_material,
              make_L05_01_export_flow, make_L05_02_import_unity,
              make_L06_01_cheatsheet, make_L06_02_common_issues, make_L06_03_roadmap]:
        print(f"生成 {f.__name__} ...")
        f()
    print("全部完成")
