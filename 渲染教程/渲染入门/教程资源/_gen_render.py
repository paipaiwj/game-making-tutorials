# -*- coding: utf-8 -*-
# Unity 渲染入门教程（面向 VRChat）— 配图生成脚本
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _render_svg import *

_grad_counter = [0]

def _gid():
    _grad_counter[0] += 1
    return f"g{_grad_counter[0]}"

def radial_grad(dwg, stops, cx=None, cy=None, r=None):
    """stops: [(offset, color, opacity), ...]"""
    gid = _gid()
    grad = dwg.radialGradient(id=gid, cx=cx, cy=cy, r=r)
    for off, col, op in stops:
        grad.add_stop_color(offset=off, color=col, opacity=op)
    dwg.defs.add(grad)
    return f"url(#{gid})"

def linear_grad(dwg, x1, y1, x2, y2, stops):
    gid = _gid()
    grad = dwg.linearGradient(start=(x1, y1), end=(x2, y2), id=gid)
    for off, col, op in stops:
        grad.add_stop_color(offset=off, color=col, opacity=op)
    dwg.defs.add(grad)
    return f"url(#{gid})"

def shade(c, f):
    return tuple(max(0, min(255, int(x * f))) for x in c)

def rgb(c):
    return f"rgb({c[0]},{c[1]},{c[2]})"

def draw_sphere(dwg, cx, cy, r, base, metallic=0.0, smooth=0.5, ring=None):
    """画一个带渐变高光的球体。metallic/smooth 影响高光与环境反射强度。"""
    light_dir = (cx - r * 0.4, cy - r * 0.45)
    bright = shade(base, 1.5 + smooth * 0.5)
    dark = shade(base, 0.35 + metallic * 0.2)
    grad = radial_grad(dwg,
        [(0.0, rgb(bright), 1.0), (0.55, rgb(base), 1.0), (1.0, rgb(dark), 1.0)],
        cx=light_dir[0], cy=light_dir[1], r=r * 1.6)
    dwg.add(dwg.circle(center=(cx, cy), r=r, fill=grad))
    if metallic > 0.4:
        sky_op = 0.25 + smooth * 0.35
        sky = linear_grad(dwg, cx - r, cy - r, cx + r, cy + r,
            [(0.0, "#dfeaff", sky_op), (0.5, "#dfeaff", sky_op * 0.22), (1.0, "#dfeaff", 0.0)])
        dwg.add(dwg.circle(center=(cx, cy), r=r, fill=sky))
    if smooth > 0.15:
        hr = r * (0.25 + smooth * 0.2)
        hg = radial_grad(dwg,
            [(0.0, "#ffffff", 1.0), (1.0, "#ffffff", 0.0)],
            cx=cx - r * 0.35, cy=cy - r * 0.4, r=hr * 2)
        dwg.add(dwg.circle(center=(cx - r * 0.35, cy - r * 0.4), r=hr, fill=hg))
    if metallic > 0.4:
        eg = linear_grad(dwg, cx - r, cy - r * 0.3, cx + r, cy + r * 0.7,
            [(0.0, "#ffffff", 0.4), (0.4, "#ffffff", 0.06), (1.0, "#ffffff", 0.0)])
        dwg.add(dwg.ellipse(center=(cx, cy + r * 0.55), rx=r * 0.75, ry=r * 0.28, fill=eg))
    if ring:
        dwg.add(dwg.circle(center=(cx, cy), r=r, fill="none", stroke=ring,
                           stroke_width=2, stroke_dasharray="none"))


# ============================================================
# L01 — 图1: 渲染管线流程
# ============================================================
def make_L01_01_render_pipeline():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "什么是渲染？一条流水线", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "渲染 = 把 3D 场景变成屏幕上 2D 像素的流水线", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    stages = [
        ("1. 场景输入", "模型 / 顶点 / 三角形\n相机 / 灯光 / 材质", ACCENT),
        ("2. 顶点着色", "Vertex Shader\n计算每个顶点的位置", SUCCESS),
        ("3. 光栅化", "Rasterization\n把三角形变成像素点", WARM),
        ("4. 片元着色", "Fragment Shader\n算每个像素的颜色", "#c084fc"),
    ]
    card_w, card_h = 190, 150
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(stages):
        cx = start_x + i * (card_w + 26)
        cy = 110
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, cy + 32, fill="#fff", size=14, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, cy + 60 + j * 18, fill=TEXT_DIM, size=12, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, cy + card_h//2, cx + card_w + 24, cy + card_h//2,
                      stroke=color, stroke_width=2)

    # 输出屏幕
    scr_w, scr_h = 380, 100
    sx = (W - scr_w) // 2
    sy = 320
    add_rect(dwg, sx, sy, scr_w, scr_h, fill="#101010", stroke="#6bcf7f", rx=8, stroke_width=2)
    add_text(dwg, "屏幕上的像素画面", sx + scr_w//2, sy + 34, fill="#fff", size=14, weight="bold", anchor="middle")
    add_text(dwg, "每秒约 60~144 次，这就是「帧率」", sx + scr_w//2, sy + 62, fill=TEXT_DIM, size=12, anchor="middle")
    # 折线：第 4 阶段底部 → 向下 → 向左 → 进入屏幕卡片顶部
    last_cx = start_x + 3 * (card_w + 26) + card_w // 2
    add_line(dwg, last_cx, 260, last_cx, 300, stroke=SUCCESS, stroke_width=2)
    add_line(dwg, last_cx, 300, 452, 300, stroke=SUCCESS, stroke_width=2)
    add_line(dwg, 452, 300, 452, 321, stroke=SUCCESS, stroke_width=2, with_arrow=True)

    add_text(dwg, "重点：物体的「形状」由顶点决定，「颜色」由片元着色器 + 材质 + 光照决定", W//2, 470, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L01_01_render_pipeline")


# ============================================================
# L01 — 图2: 一帧的流程 CPU/GPU
# ============================================================
def make_L01_02_frame_loop():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "一帧画面是怎么画出来的", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    boxes = [
        ("CPU · 场景逻辑", "Unity 更新逻辑、动画\n收集可见物体、准备渲染数据", ACCENT, 60),
        ("CPU · 提交命令", "一次「提交」= 1 个\nDraw Call（渲染调用）", WARM, 300),
        ("GPU · 执行渲染", "按流水线画出这一帧\n（上一图的那 4 步）", SUCCESS, 540),
        ("屏幕 · 显示画面", "画面送到显示器\n然后开始画下一帧", "#c084fc", 760),
    ]
    box_w = 160
    for title, desc, color, x in boxes:
        add_rect(dwg, x, 90, box_w, 150, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, 118, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + box_w//2, 148 + j * 18, fill=TEXT_DIM, size=11, anchor="middle")
    for i in range(3):
        bx = boxes[i][3] + box_w
        add_arrow(dwg, bx, 165, bx + 24, 165, stroke=boxes[i+1][2], stroke_width=2)

    # 循环箭头 + 帧时间
    add_line(dwg, 760 + box_w//2, 252, 60, 252, stroke=BORDER, stroke_width=2,
             with_arrow=True, opacity=0.6)
    add_rect(dwg, 328, 239, 164, 26, fill="#222222", stroke=BORDER, rx=13)
    add_text(dwg, "下一帧循环", 410, 257, fill="#dddddd", size=11, anchor="middle")

    add_rect(dwg, 60, 290, 780, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "帧率 = 每秒画的帧数", 100, 318, fill=ACCENT, size=13, weight="bold")
    add_text(dwg, "60 FPS = 每帧 16.6 毫秒内画完  |  90 FPS ≈ 11 毫秒  |  120 FPS ≈ 8.3 毫秒", 100, 344, fill=TEXT_DIM, size=12)
    add_text(dwg, "Draw Call 越少、渲染越轻 → 帧时间越短 → 帧率越高（VRChat 目标：90 FPS）", 100, 368, fill=WARN, size=12)

    save_svg_and_png(dwg, "L01_02_frame_loop")


# ============================================================
# L02 — 图1: 光照类型与反射
# ============================================================
def make_L02_01_light_types():
    import math
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "光照：直接光 + 环境光", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    items = [
        ("平行光 Directional", "太阳：无限远、平行光线\n全场景同一方向，几乎无成本", ACCENT),
        ("点光源 Point", "灯泡：从一点向四周发散\n有半径，数量多会卡", WARM),
        ("聚光灯 Spot", "手电筒：锥形光束\n适合做区域强调光", SUCCESS),
        ("环境光 Ambient", "天空盒反射：来自四面八方的光\n所有物体都收到，决定氛围", "#c084fc"),
    ]
    card_w, card_h = 190, 130
    start_x = (W - (card_w * 4 + 24 * 3)) // 2
    for i, (title, desc, color) in enumerate(items):
        cx = start_x + i * (card_w + 24)
        cy = 80
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, cy + 28, fill="#fff", size=12.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, cy + 56 + j * 18, fill=TEXT_DIM, size=11, anchor="middle")

    # 反射原理
    add_text(dwg, "光线打到物体上，产生两种反射", W//2, 250, fill=TEXT, size=15, weight="bold", anchor="middle")
    add_rect(dwg, 60, 272, 380, 240, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=1.5)
    add_text(dwg, "漫反射 Diffuse", 240, 300, fill="#fff", size=13, weight="bold", anchor="middle")
    add_text(dwg, "光线被粗糙表面向四面八方散射", 240, 328, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "→ 决定物体的「固有色」", 240, 350, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "→ 表面越粗糙，漫反射越强", 240, 372, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "漫反射示意", 240, 468, fill=TEXT_MUTED, size=10.5, anchor="middle")
    add_ellipse(dwg, 400, 432, 22, 22, fill="#8a6d4f")
    dwg.add(dwg.circle(center=(400, 432), r=22, fill="none", stroke="#c9a06f", stroke_width=1.5))
    for (ox, oy) in [(392, 426), (408, 434), (396, 442), (404, 422)]:
        add_ellipse(dwg, ox, oy, 2.2, 2.2, fill="#e8cfa8", opacity=0.8)
    for i in range(6):
        ang = 60 + i * 60
        a = math.radians(ang)
        add_line(dwg, 400, 432, 400 + 34*math.cos(a), 432 + 34*math.sin(a),
                 stroke=WARM, stroke_width=1.5, opacity=0.8)

    add_rect(dwg, 460, 272, 380, 240, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=1.5)
    add_text(dwg, "高光（镜面）Specular", 650, 300, fill="#fff", size=13, weight="bold", anchor="middle")
    add_text(dwg, "光线被光滑表面定向弹走", 650, 328, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "→ 决定物体的「反光亮点」", 650, 350, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "→ 表面越光滑，高光越集中", 650, 372, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "镜面反射示意", 650, 470, fill=TEXT_MUTED, size=10.5, anchor="middle")
    draw_sphere(dwg, 650, 438, 22, (60, 76, 100), metallic=0.6, smooth=0.85)
    add_line(dwg, 700, 408, 645, 430, stroke="#ffffff", stroke_width=1.5, opacity=0.5, with_arrow=True)
    add_line(dwg, 645, 430, 672, 404, stroke=SUCCESS, stroke_width=1.5, opacity=0.9, with_arrow=True)

    add_text(dwg, "真实感渲染（PBR）就是精确模拟这两者 + 环境光，材质看起来才「真实」", W//2, 540, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L02_01_light_types")


# ============================================================
# L02 — 图2: PBR 四参数
# ============================================================
def make_L02_02_pbr_params():
    W, H = 900, 540
    dwg = new_svg(W, H)
    add_text(dwg, "PBR 四大贴图/参数", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "PBR = Physically Based Rendering，按真实光学规律算颜色", W//2, 60, fill=TEXT_DIM, size=13, anchor="middle")

    items = [
        ("Base Map 颜色贴图", "物体「固有色」\n非金属用彩色贴图\n决定基色与细节", ACCENT),
        ("Normal 法线贴图", "骗过光照：平面表面\n模拟凹凸细节，不加模型面数", SUCCESS),
        ("Metallic 金属度", "灰阶图：黑=非金属\n白=金属（反射强、吸光）", WARM),
        ("Smoothness 光滑度", "灰阶图：黑=粗糙\n白=光滑（高光集中）", "#c084fc"),
    ]
    card_w, card_h = 190, 170
    start_x = (W - (card_w * 4 + 24 * 3)) // 2
    for i, (title, desc, color) in enumerate(items):
        cx = start_x + i * (card_w + 24)
        cy = 92
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        # 迷你贴图示意
        add_rect(dwg, cx + card_w//2 - 34, cy + 26, 68, 48, fill="#1a1a1a", stroke=color, rx=4, stroke_width=1)
        if i == 0:
            for rx_, ry_ in [(16,16),(46,16),(16,48),(46,48)]:
                add_ellipse(dwg, cx + card_w//2 - 34 + rx_, cy + 26 + ry_, 8, 8, fill=ACCENT, opacity=0.7)
        elif i == 1:
            add_line(dwg, cx + card_w//2 - 30, cy + 42, cx + card_w//2 - 14, cy + 30, stroke=SUCCESS, stroke_width=2)
            add_line(dwg, cx + card_w//2 - 14, cy + 30, cx + card_w//2 + 8, cy + 52, stroke=SUCCESS, stroke_width=2)
            add_line(dwg, cx + card_w//2 + 8, cy + 52, cx + card_w//2 + 24, cy + 40, stroke=SUCCESS, stroke_width=2)
        elif i == 2:
            add_rect(dwg, cx + card_w//2 - 34, cy + 26, 68, 24, fill="#c8c8c8")
            add_rect(dwg, cx + card_w//2 - 34, cy + 50, 68, 24, fill="#333333")
        else:
            add_rect(dwg, cx + card_w//2 - 34, cy + 26, 68, 24, fill="#dddddd")
            add_rect(dwg, cx + card_w//2 - 34, cy + 50, 68, 24, fill="#555555")
        add_text(dwg, title, cx + card_w//2, cy + 96, fill="#fff", size=12.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, cy + 120 + j * 17, fill=TEXT_DIM, size=10.5, anchor="middle")

    # 四个球对比
    add_text(dwg, "同样的光照下，四个球因为 PBR 参数不同而长得完全不同", W//2, 290, fill=TEXT, size=15, weight="bold", anchor="middle")
    balls = [
        ("金属·光滑", (170, 170, 178), 1.0, 0.9, WARM),
        ("金属·粗糙", (160, 160, 168), 1.0, 0.25, WARN),
        ("非金属·光滑", (80, 160, 220), 0.0, 0.9, ACCENT),
        ("非金属·粗糙", (180, 130, 90), 0.0, 0.25, SUCCESS),
    ]
    bx0 = (W - (120 * 4 + 40 * 3)) // 2
    for i, (label, col, met, sm, ring) in enumerate(balls):
        cx = bx0 + i * 160 + 60
        cy = 380
        draw_sphere(dwg, cx, cy, 42, col, metallic=met, smooth=sm, ring=ring)
        add_text(dwg, label, cx, cy + 70, fill=TEXT, size=12, anchor="middle")
        add_text(dwg, f"Metallic {met}  Smooth {sm}", cx, cy + 90, fill=TEXT_MUTED, size=10.5, anchor="middle")

    add_text(dwg, "结论：真实感不是「颜色调得好」，而是「参数调得对」——记住金属度+光滑度", W//2, 514, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L02_02_pbr_params")


# ============================================================
# L02 — 图3: 烘焙 vs 实时
# ============================================================
def make_L02_03_baked_vs_realtime():
    W, H = 900, 520
    dwg = new_svg(W, H)
    add_text(dwg, "烘焙光照 vs 实时光照", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 左：实时
    add_rect(dwg, 60, 80, 370, 330, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    add_text(dwg, "实时光照 Realtime", 245, 110, fill="#fff", size=15, weight="bold", anchor="middle")
    rows = [
        ("运行时即时计算", SUCCESS),
        ("灯光可移动、物体可动", SUCCESS),
        ("VRChat 中多人可见动态效果", SUCCESS),
        ("光源数量少（1~2 个点光即可）", WARN),
        ("每个实时光源都增加 GPU 开销", WARN),
    ]
    for i, (txt, col) in enumerate(rows):
        add_ellipse(dwg, 90, 148 + i * 42, 5, 5, fill=col)
        add_text(dwg, txt, 105, 152 + i * 42, fill=TEXT_DIM, size=12)

    # 右：烘焙
    add_rect(dwg, 470, 80, 370, 330, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=2)
    add_text(dwg, "烘焙光照 Baked", 655, 110, fill="#fff", size=15, weight="bold", anchor="middle")
    rows = [
        ("光照信息预先算好，存进光照贴图", SUCCESS),
        ("运行时零计算，世界更流畅", SUCCESS),
        ("只有静态物体能用", WARN),
        ("动态物体（捡起物）不在烘焙里", WARN),
        ("改灯光要重新烘焙，时间按分钟算", WARN),
    ]
    for i, (txt, col) in enumerate(rows):
        add_ellipse(dwg, 500, 148 + i * 42, 5, 5, fill=col)
        add_text(dwg, txt, 515, 152 + i * 42, fill=TEXT_DIM, size=12)

    # 光照贴图示意
    add_text(dwg, "光照贴图示意（Lightmap：记录光影明暗的贴图）", W//2, 450, fill=TEXT, size=13, weight="bold", anchor="middle")
    lm_x, lm_y = 340, 465
    for gx in range(6):
        for gy in range(2):
            v = 0.35 + ((gx * 31 + gy * 17) % 10) / 14.0
            col = rgb(shade((90, 120, 255), v * 1.6))
            dwg.add(dwg.rect(insert=(lm_x + gx * 26, lm_y + gy * 22), size=(25, 21),
                             fill=col, stroke=BORDER, stroke_width=0.5))
    save_svg_and_png(dwg, "L02_03_baked_vs_realtime")


# ============================================================
# L03 — 图1: Shader / 材质 / 贴图 关系
# ============================================================
def make_L03_01_material_shader():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "Shader / 材质 / 贴图 的关系", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # Shader 卡片
    add_rect(dwg, 60, 100, 220, 180, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    add_text(dwg, "Shader（程序）", 170, 128, fill="#fff", size=14, weight="bold", anchor="middle")
    for j, line in enumerate(["决定「怎么画」的代码", "光照算法 / 混合方式", "读取哪些贴图、如何计算", "VRChat 常用：URP Lit、", "卡通 UTS、Poiyomi、自定义"]):
        add_text(dwg, line, 170, 156 + j * 19, fill=TEXT_DIM, size=11.5, anchor="middle")

    # 材质卡片
    add_rect(dwg, 340, 100, 220, 180, fill=PANEL, stroke=WARM, rx=10, stroke_width=2)
    add_text(dwg, "Material（材质）", 450, 128, fill="#fff", size=14, weight="bold", anchor="middle")
    for j, line in enumerate(["Shader + 具体参数", "= 一张「配方表」", "例：Lit Shader", "+ 颜色 #3a6ea5", "+ 贴图、Metallic、Emission"]):
        add_text(dwg, line, 450, 156 + j * 19, fill=TEXT_DIM, size=11.5, anchor="middle")

    # 物体卡片
    add_rect(dwg, 620, 100, 220, 180, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=2)
    add_text(dwg, "GameObject + MeshRenderer", 730, 128, fill="#fff", size=13, weight="bold", anchor="middle")
    for j, line in enumerate(["MeshRenderer 上挂材质槽", "物体 1 → 材质 A", "物体 2 → 材质 A（共享！）", "物体 3 → 材质 B", "共享 = 省性能，见第 4 篇"]):
        add_text(dwg, line, 730, 156 + j * 19, fill=TEXT_DIM, size=11.5, anchor="middle")

    add_arrow(dwg, 280, 190, 340, 190, stroke=ACCENT, stroke_width=2)
    add_arrow(dwg, 560, 190, 620, 190, stroke=WARM, stroke_width=2)

    add_rect(dwg, 60, 310, 780, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "一句话总结", 90, 338, fill=SUCCESS, size=13, weight="bold")
    add_text(dwg, "Shader = 菜谱（程序）   材质 = 一张写好的菜谱（参数）   贴图 = 食材（图片数据）", 90, 364, fill=TEXT, size=13)
    add_text(dwg, "调「材质」不用写代码；换「Shader」才是换渲染算法（VRChat 粉色物体 = Shader 缺失）", 90, 388, fill=WARN, size=12)

    save_svg_and_png(dwg, "L03_01_material_shader")


# ============================================================
# L03 — 图2: 贴图通道
# ============================================================
def make_L03_02_texture_channels():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "一张贴图 = 一个通道，各管一件事", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    def mini_tex(x, y, kind):
        w, h = 130, 90
        add_rect(dwg, x, y, w, h, fill="#1a1a1a", stroke=BORDER, rx=6)
        if kind == "albedo":
            dwg.add(dwg.rect(insert=(x+4, y+4), size=(w-8, h-8), fill="#3a6ea5", rx=4))
            for (ox, oy) in [(28, 28), (70, 28), (28, 60), (70, 60)]:
                add_ellipse(dwg, x+ox, y+oy, 9, 9, fill="#a5d3ff", opacity=0.8)
            add_text(dwg, "彩色图", x+w//2, y+h+16, fill=TEXT_DIM, size=10.5, anchor="middle")
        elif kind == "normal":
            for (ox, oy) in [(34, 30), (62, 48), (90, 30)]:
                add_line(dwg, x+ox-8, y+oy, x+ox+8, y+oy, stroke="#b07cff", stroke_width=3)
            add_line(dwg, x+20, y+64, x+110, y+64, stroke="#6b5a8a", stroke_width=2)
            add_text(dwg, "紫色凹凸图", x+w//2, y+h+16, fill=TEXT_DIM, size=10.5, anchor="middle")
        elif kind == "metal":
            add_rect(dwg, x+4, y+4, w-8, (h-8)//2, fill="#d8d8d8")
            add_rect(dwg, x+4, y+4+(h-8)//2, w-8, (h-8)//2, fill="#2a2a2a")
            add_text(dwg, "黑白：白=金属", x+w//2, y+h+16, fill=TEXT_DIM, size=10.5, anchor="middle")
        elif kind == "smooth":
            add_rect(dwg, x+4, y+4, w-8, (h-8)//2, fill="#ffffff")
            add_rect(dwg, x+4, y+4+(h-8)//2, w-8, (h-8)//2, fill="#555555")
            add_text(dwg, "黑白：白=光滑", x+w//2, y+h+16, fill=TEXT_DIM, size=10.5, anchor="middle")
        elif kind == "emission":
            add_rect(dwg, x+4, y+4, w-8, h-8, fill="#101010", rx=4)
            for (ox, oy) in [(30, 30), (66, 48), (100, 32)]:
                add_ellipse(dwg, x+ox, y+oy, 12, 12, fill="#ffcf5e", opacity=0.9)
            add_text(dwg, "亮部=发光", x+w//2, y+h+16, fill=TEXT_DIM, size=10.5, anchor="middle")

    specs = [
        ("Base Map 颜色贴图", "物体固有色与细节", ACCENT, "albedo"),
        ("Normal Map 法线贴图", "模拟凹凸，省模型面数", SUCCESS, "normal"),
        ("Metallic Map 金属度", "哪部分是金属", WARM, "metal"),
        ("Smoothness 光滑度", "哪部分光滑/粗糙", "#c084fc", "smooth"),
        ("Emission 自发光", "自己发光的部分", "#ffcf5e", "emission"),
    ]
    col_w = 156
    start_x = (W - (col_w * 5 + 20 * 4)) // 2
    for i, (title, desc, color, kind) in enumerate(specs):
        x = start_x + i * (col_w + 20)
        y = 70
        add_text(dwg, title, x + col_w//2, y + 18, fill="#fff", size=12, weight="bold", anchor="middle")
        mini_tex(x + (col_w-130)//2, y + 30, kind)
        add_text(dwg, desc, x + col_w//2, y + 150, fill=TEXT_DIM, size=10.5, anchor="middle")

    # 说明
    add_rect(dwg, 60, 280, 780, 200, fill=PANEL, stroke=BORDER, rx=10)
    add_text(dwg, "Unity 材质面板与贴图的关系", 90, 310, fill=TEXT, size=14, weight="bold")
    rows = [
        ("① 把图片拖进 Project 窗口导入 → 它就是一张 Texture", ACCENT),
        ("② 在材质 Inspector 里，把 Texture 拖到对应插槽（Base Map / Normal Map…）", ACCENT),
        ("③ 贴图没做特殊压缩时：图越大越占显存，VRChat 上限 4096×4096", WARN),
        ("④ 不写 Shader 也能调好看：先学会这 4 个滑块（颜色/金属度/光滑度/自发光）", SUCCESS),
    ]
    for i, (txt, col) in enumerate(rows):
        add_text(dwg, txt, 90, 344 + i * 30, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "提示：Smoothness 和 Metallic 常共用一张「Mask 图」，不同通道存不同信息", 90, 468, fill=TEXT_MUTED, size=11.5, italic=True)

    save_svg_and_png(dwg, "L03_02_texture_channels")


# ============================================================
# L03 — 图3: 混合模式
# ============================================================
def make_L03_03_blend_modes():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "混合模式：透明物体怎么算颜色", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    modes = [
        ("Opaque 不透明", "完全不透明\n渲染快，世界中最常用\n墙体、地面、模型", ACCENT, None),
        ("Transparent 透明", "半透明混合（AlphaBlend）\n玻璃、水面、雾\n后画的物体在前，注意排序", SUCCESS, 0.5),
        ("Additive 加色", "颜色相加，越叠越亮\n发光、火焰、魔法、粒子\n不会变暗，适合光效", WARM, None),
    ]
    x0 = (W - (250 * 3 + 30 * 2)) // 2
    for i, (title, desc, color, alpha) in enumerate(modes):
        x = x0 + i * 280
        add_rect(dwg, x, 80, 250, 200, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        # 叠加圆示意
        c1 = (x + 90, 140); c2 = (x + 160, 150)
        if alpha is None and "Opaque" in title:
            dwg.add(dwg.circle(center=c1, r=38, fill="#2a6fb0"))
            dwg.add(dwg.circle(center=c2, r=38, fill="#b05a2a"))
            dwg.add(dwg.circle(center=((c1[0]+c2[0])//2, (c1[1]+c2[1])//2), r=16, fill="#b05a2a"))
        elif alpha is not None:
            dwg.add(dwg.circle(center=c1, r=38, fill="#2a6fb0", opacity=0.45))
            dwg.add(dwg.circle(center=c2, r=38, fill="#b05a2a", opacity=0.45))
            dwg.add(dwg.circle(center=((c1[0]+c2[0])//2, (c1[1]+c2[1])//2), r=16, fill="#c98a4e", opacity=0.8))
        else:
            dwg.add(dwg.circle(center=c1, r=38, fill="#2a6fb0", opacity=0.8))
            dwg.add(dwg.circle(center=c2, r=38, fill="#b05a2a", opacity=0.8))
            dwg.add(dwg.circle(center=((c1[0]+c2[0])//2, (c1[1]+c2[1])//2), r=16, fill="#ffdd88", opacity=0.95))
        add_text(dwg, title, x + 125, 215, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + 125, 240 + j * 18, fill=TEXT_DIM, size=11.5, anchor="middle")

    add_text(dwg, "粒子特效默认用 Additive 或 Transparent；材质混合模式在 Shader 里设置", W//2, 420, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L03_03_blend_modes")


# ============================================================
# L04 — 图1: VRChat 渲染技术栈
# ============================================================
def make_L04_01_vrc_stack():
    W, H = 900, 400
    dwg = new_svg(W, H)
    add_text(dwg, "VRChat 世界用的是什么渲染？", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    layers = [
        ("Unity 2022.3", "你开发用的引擎版本", ACCENT, 0),
        ("URP 渲染管线", "VRChat 官方使用的\n通用渲染管线（Universal RP）", SUCCESS, 1),
        ("你的材质与 Shader", "URP Lit / UTS / Poiyomi / 自写\n所有材质必须兼容 URP", WARM, 2),
        ("VRChat 客户端", "PC 与 Quest 的渲染能力不同\nQuest 限制更多", "#c084fc", 3),
    ]
    box_w = 170
    start_x = 74
    for title, desc, color, idx in layers:
        x = start_x + idx * (box_w + 24)
        add_rect(dwg, x, 90, box_w, 150, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, 120, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + box_w//2, 152 + j * 18, fill=TEXT_DIM, size=10.5, anchor="middle")
        if idx > 0:
            add_arrow(dwg, x - 22, 165, x - 2, 165, stroke=color, stroke_width=2)

    add_rect(dwg, 60, 270, 780, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "对世界制作者意味着什么", 90, 298, fill=WARM, size=13, weight="bold")
    add_text(dwg, "① 材质面板里选 URP 的 Shader（Lit、Simple Lit 等）   ② 自带的老「Standard」Shader 不兼容 URP", 90, 326, fill=TEXT_DIM, size=11.5)
    add_text(dwg, "③ 从商店/代码库拿资源时，先确认它是 URP 版本（VRChat 2022.3 之后的世界都是 URP）", 90, 350, fill=TEXT_DIM, size=11.5)

    save_svg_and_png(dwg, "L04_01_vrc_stack")


# ============================================================
# L04 — 图2: 性能预算
# ============================================================
def make_L04_02_budget():
    W, H = 900, 520
    dwg = new_svg(W, H)
    add_text(dwg, "渲染性能预算：四个数字盯住就行", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    bars = [
        ("Draw Calls（渲染批次）", "每帧 CPU 提交的渲染命令数\n越少越好：共享材质 / 合批", 15, 40, "≤100", ACCENT),
        ("材质数量", "每个材质 = 一份状态切换\n相同材质多个物体可合批", 50, 100, "≤50", SUCCESS),
        ("贴图内存", "4096×4096 ≈ 64MB 显存\n一般物体 1024/2048 足够", 40, 80, "总内存小", WARM),
        ("实时光源", "每个点/聚光灯都要每帧计算\n烘焙光照 + 1 个太阳光最省", 10, 25, "1~2 个", "#c084fc"),
    ]
    y0 = 90
    for i, (title, desc, val, maxv, target, color) in enumerate(bars):
        y = y0 + i * 105
        add_text(dwg, title, 60, y + 20, fill="#fff", size=13.5, weight="bold")
        add_text(dwg, desc, 60, y + 42, fill=TEXT_MUTED, size=11)
        # 条
        add_rect(dwg, 380, y + 8, 380, 26, fill="#1a1a1a", stroke=BORDER, rx=13)
        fill_w = max(18, int(380 * min(val / maxv, 1.0)))
        add_rect(dwg, 380, y + 8, fill_w, 26, fill=color, rx=13, opacity=0.85)
        # 刻度（显示百分比，统一口径）
        for t in [25, 50, 75]:
            add_text(dwg, f"{t}%", 380 + int(380 * t / 100), y + 46, fill=TEXT_MUTED, size=9, anchor="middle")
        add_text(dwg, f"建议：{target}", 776, y + 26, fill=color, size=11.5, weight="bold")

    add_text(dwg, "工具：Window → Rendering → Rendering Debugger（查看 Draw Calls）", 60, 498, fill=TEXT_MUTED, size=12)
    save_svg_and_png(dwg, "L04_02_budget")


# ============================================================
# L04 — 图3: 优化手段
# ============================================================
def make_L04_03_optimize():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "常用的渲染优化手段（按性价比排序）", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    items = [
        ("共享材质", "10 个箱子用同一个材质\n立即合批，Draw Call 大降", ACCENT),
        ("贴图图集 Atlas", "多张小贴图拼一张大图\n材质少 = 切换少 = 快", SUCCESS),
        ("减少实时光", "场景烘焙光照\n实光只留太阳 + 1 个点光", WARM),
        ("压缩贴图", "导入设置里选压缩格式\n图小一半，几乎看不出差别", "#c084fc"),
        ("关掉多余阴影", "远距离、地面细节的阴影关掉\n阴影很吃 GPU", "#ff9e4e"),
    ]
    start_x = 60
    card_w, card_h = 156, 250
    for i, (title, desc, color) in enumerate(items):
        x = start_x + i * (card_w + 10)
        add_rect(dwg, x, 80, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_ellipse(dwg, x + card_w//2, 108, 16, 16, fill=color, opacity=0.7)
        add_text(dwg, str(i+1), x + card_w//2, 113, fill="#fff", size=12, weight="bold", anchor="middle")
        add_text(dwg, title, x + card_w//2, 150, fill="#fff", size=12.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 178 + j * 18, fill=TEXT_DIM, size=10.5, anchor="middle")

    add_text(dwg, "做完一个优化 → 打开 VRChat 本地测试（Build & Test）看帧率变化，再决定下一个", W//2, 420, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L04_03_optimize")


# ============================================================
# L05 — 图1: 发光水晶制作步骤
# ============================================================
def make_L05_01_crystal_steps():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "动手：做一颗发光水晶", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "目标：体验完整渲染流程 — 模型 → 材质 → 自发光 → 打光", W//2, 60, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 建模型", "创建 Cube\n拉伸成水晶柱\n（1 个物体即可）", ACCENT),
        ("2. 建材质", "Create → Material\nShader 选 URP/Lit", SUCCESS),
        ("3. 调 PBR", "Base Map 调色\nMetallic 0 / Smooth 0.6\n加 Normal 贴图", WARM),
        ("4. 开自发光", "Emission 勾选\n颜色调亮蓝/紫\n强度拉到 1~3", "#c084fc"),
        ("5. 打光", "场景加 Directional Light\n水晶旁放 1 个点光源\n烘焙或实时都行", "#ff9e4e"),
    ]
    card_w, card_h = 156, 220
    start_x = (W - (card_w * 5 + 14 * 4)) // 2
    for i, (title, desc, color) in enumerate(steps):
        x = start_x + i * (card_w + 14)
        add_rect(dwg, x, 100, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 128, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 156 + j * 18, fill=TEXT_DIM, size=10.5, anchor="middle")
        if i < 4:
            add_arrow(dwg, x + card_w + 2, 210, x + card_w + 12, 210, stroke=color, stroke_width=2)

    # 时间线
    add_line(dwg, 120, 380, 780, 380, stroke=BORDER, stroke_width=2)
    add_ellipse(dwg, 120, 380, 7, 7, fill=ACCENT)
    add_ellipse(dwg, 450, 380, 7, 7, fill=WARM)
    add_ellipse(dwg, 780, 380, 7, 7, fill=SUCCESS)
    add_text(dwg, "5 分钟", 120, 410, fill=TEXT_MUTED, size=11, anchor="middle")
    add_text(dwg, "10 分钟", 450, 410, fill=TEXT_MUTED, size=11, anchor="middle")
    add_text(dwg, "做完去 VRChat 里看一眼！", 780, 410, fill=SUCCESS, size=11, anchor="middle")
    save_svg_and_png(dwg, "L05_01_crystal_steps")


# ============================================================
# L05 — 图2: 水晶成品效果
# ============================================================
def make_L05_02_crystal_result():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "发光水晶效果示意", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 左侧：普通球（无材质）
    add_rect(dwg, 60, 70, 360, 300, fill=PANEL, stroke=BORDER, rx=10)
    add_text(dwg, "❌ 没有材质 / 没有光照", 240, 96, fill=TEXT_MUTED, size=12, weight="bold", anchor="middle")
    draw_sphere(dwg, 240, 210, 60, (120, 120, 130), metallic=0.0, smooth=0.3)
    add_text(dwg, "灰蒙蒙一片，看不出体积感", 240, 320, fill=TEXT_DIM, size=11, anchor="middle")

    # 右侧：发光水晶
    add_rect(dwg, 470, 70, 370, 310, fill="#141d2b", stroke=ACCENT, rx=10, stroke_width=1.5)
    add_text(dwg, "✅ 材质 + 光照 + 自发光", 655, 96, fill=SUCCESS, size=12, weight="bold", anchor="middle")

    # 水晶（菱形 + 面）
    cx, cy = 590, 215
    pts_top = [(cx, cy - 72), (cx + 46, cy - 26), (cx, cy + 26), (cx - 46, cy - 26)]
    pts_bot = [(cx, cy + 64), (cx + 40, cy + 22), (cx, cy + 26), (cx - 40, cy + 22)]
    grad_a = radial_grad(dwg, [(0.0, "#9fd0ff", 0.95), (0.6, "#3a6ea5", 0.9), (1.0, "#1a3a5c", 0.9)], cx=cx-8, cy=cy-30, r=90)
    grad_b = linear_grad(dwg, cx, cy-20, cx, cy+80, [(0.0, "#7fb8ff", 0.85), (1.0, "#2a4a75", 0.85)])
    dwg.add(dwg.polygon(pts_top, fill=grad_a, stroke="#bfe0ff", stroke_width=1.5))
    dwg.add(dwg.polygon(pts_bot, fill=grad_b, stroke="#bfe0ff", stroke_width=1.5))
    # 高光棱
    add_line(dwg, cx, cy - 72, cx, cy + 64, stroke="#ffffff", stroke_width=2, opacity=0.8)
    # 辉光
    for rr, op in [(70, 0.25), (52, 0.4)]:
        glow = radial_grad(dwg, [(0.0, "#7fc4ff", op), (1.0, "#7fc4ff", 0.0)], cx=cx, cy=cy, r=rr)
        dwg.add(dwg.circle(center=(cx, cy), r=rr, fill=glow))
    # 地面反光
    ground = linear_grad(dwg, cx - 80, cy + 64, cx + 80, cy + 64, [(0.0, "#7fc4ff", 0.0), (0.5, "#7fc4ff", 0.5), (1.0, "#7fc4ff", 0.0)])
    dwg.add(dwg.polygon([(cx - 60, cy + 66), (cx + 60, cy + 66), (cx + 30, cy + 96), (cx - 30, cy + 96)], fill=ground))
    # 点光源
    add_ellipse(dwg, 780, 130, 10, 10, fill="#ffffff", opacity=0.9)
    for rr, op in [(22, 0.3), (36, 0.15)]:
        lg = radial_grad(dwg, [(0.0, "#fff5d0", op), (1.0, "#fff5d0", 0.0)], cx=780, cy=130, r=rr)
        dwg.add(dwg.circle(center=(780, 130), r=rr, fill=lg))
    add_text(dwg, "点光源", 780, 166, fill=TEXT_MUTED, size=10.5, anchor="middle")

    add_text(dwg, "水晶颜色 ← Base Map    发光 ← Emission", 655, 342, fill=TEXT_DIM, size=11.5, anchor="middle")
    add_text(dwg, "高光 ← 光源 + 光滑度，三者组合画面才「活」", 655, 362, fill=TEXT_DIM, size=11.5, anchor="middle")
    save_svg_and_png(dwg, "L05_02_crystal_result")


# ============================================================
# L06 — 图1: 术语速查表
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "渲染术语速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    terms = [
        ("渲染管线", "3D 场景变成屏幕像素的流程：顶点 → 光栅化 → 着色", ACCENT),
        ("Shader", "决定「怎么画」的 GPU 程序（菜谱）", ACCENT),
        ("材质 Material", "Shader + 参数 = 配方表，挂在物体上", ACCENT),
        ("贴图 Texture", "图片数据（食材），喂给材质使用", ACCENT),
        ("UV", "贴图在模型表面的坐标展开方式", SUCCESS),
        ("法线 Normal", "表面朝哪边，决定光照明暗", SUCCESS),
        ("PBR", "基于物理的渲染，金属度+光滑度两大参数", SUCCESS),
        ("烘焙 Baked", "预先算好光照存进贴图，运行时零成本", SUCCESS),
        ("Draw Call", "CPU 一次提交渲染命令，越少越快", WARM),
        ("批处理 Batching", "多个物体合成一次 Draw Call", WARM),
        ("后处理 PostFX", "渲染完成后整屏滤镜（色彩/模糊/光晕）", WARM),
        ("HDR / 强度", "颜色亮度可以超过 1.0，用于发光/泛光", WARM),
    ]
    col_w = 390
    for i, (term, desc, color) in enumerate(terms):
        row, col = divmod(i, 2)
        x = 60 + col * (col_w + 30)
        y = 70 + row * 76
        add_rect(dwg, x, y, col_w, 60, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        add_text(dwg, term, x + 16, y + 24, fill="#fff", size=13, weight="bold")
        add_text(dwg, desc, x + 16, y + 46, fill=TEXT_DIM, size=11)

    save_svg_and_png(dwg, "L06_01_cheatsheet")


# ============================================================
# L06 — 图2: 常见问题
# ============================================================
def make_L06_02_common_issues():
    W, H = 900, 540
    dwg = new_svg(W, H)
    add_text(dwg, "常见问题对照表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    rows = [
        ("粉色/紫黑物体", "Shader 不兼容 URP 或缺失\n（VRChat 里最常见）", "换用 URP Shader\n重设材质 Shader", "#ff88cc"),
        ("物体全黑", "没有光照 / 法线反了\n光线被遮住", "加 Directional Light\n检查模型法线", WARN),
        ("画面过曝发白", "灯光太强 / Emission 太高\nHDR 溢出", "调低灯光 Intensity\nEmission 降到 1~3", WARN),
        ("边缘锯齿/闪烁", "贴图太小 / 抗锯齿关闭\n两层面重叠 Z-fighting", "贴图 1024+ / 开抗锯齿\n分开面或拉开距离", ACCENT),
        ("渲染慢 / 掉帧", "Draw Call 多 / 贴图太大\n实时光源太多", "共享材质 / 压贴图\n烘焙光照", SUCCESS),
    ]
    col_w = [180, 300, 300]
    xs = [60, 255, 570]
    ys = [70, 92, 114]
    for hd, x in zip(["问题现象", "常见原因", "解决办法"], xs):
        add_rect(dwg, x, 70, col_w[0], 34, fill=PANEL, stroke=ACCENT, stroke_width=1.5)
        add_text(dwg, hd, x + col_w[0]//2, 92, fill=ACCENT, size=13, weight="bold", anchor="middle")
    for i, (prob, cause, sol, color) in enumerate(rows):
        y = 104 + i * 82
        add_rect(dwg, 60, y, col_w[0], 72, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, prob, 60 + col_w[0]//2, y + 38, fill="#fff", size=12.5, weight="bold", anchor="middle")
        add_rect(dwg, 255, y, col_w[1], 72, fill=PANEL, stroke=BORDER, rx=6)
        for j, line in enumerate(cause.split("\n")):
            add_text(dwg, line, 255 + col_w[1]//2, y + 28 + j * 18, fill=TEXT_DIM, size=11, anchor="middle")
        add_rect(dwg, 570, y, col_w[2], 72, fill=PANEL, stroke=SUCCESS, rx=6)
        for j, line in enumerate(sol.split("\n")):
            add_text(dwg, line, 570 + col_w[2]//2, y + 28 + j * 18, fill=SUCCESS, size=11, anchor="middle")

    add_text(dwg, "遇到问题先猜「渲染」而不是「代码」：粉色 = Shader，全黑 = 光照，锯齿 = 贴图/抗锯齿", W//2, 520, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_02_common_issues")


# ============================================================
# L06 — 图3: 进阶路线图
# ============================================================
def make_L06_03_roadmap():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "进阶路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    stages = [
        ("入门 · 会用材质", "调参数：颜色/金属度/光滑度\n理解贴图通道", ACCENT, "现在"),
        ("熟练 · 调出质感", "烘焙光照 / 优化预算\n图集与共享材质", SUCCESS, "1 周"),
        ("进阶 · 写 Shader", "URP 自定义 Shader\nGLSL/HLSL 基础语法", WARM, "1 个月"),
        ("精通 · 视觉风格", "后处理调色 / 自定义渲染\nVFX Graph 与灯光氛围", "#c084fc", "长期"),
    ]
    box_w, box_h = 180, 150
    start_x = (W - (box_w * 4 + 30 * 3)) // 2
    for i, (title, desc, color, time) in enumerate(stages):
        x = start_x + i * (box_w + 30)
        y = 100
        add_rect(dwg, x, y, box_w, box_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, y + 30, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + box_w//2, y + 60 + j * 19, fill=TEXT_DIM, size=11, anchor="middle")
        add_text(dwg, f"⏱ {time}", x + box_w//2, y + box_h - 14, fill=color, size=11, anchor="middle")
        if i < 3:
            add_arrow(dwg, x + box_w + 4, y + box_h//2, x + box_w + 26, y + box_h//2, stroke=color, stroke_width=2)

    # 学习建议
    add_rect(dwg, 100, 300, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "学习建议", 130, 330, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "① 每学一个概念，立刻在 Unity 里做一个最小实验  ② 多看 VRChat 好世界，拆解它们的画面", 130, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "③ 从「调参数」开始，不要一上来就写 Shader  ④ 问问题先贴截图和材质面板", 130, 382, fill=TEXT_DIM, size=12.5)

    save_svg_and_png(dwg, "L06_03_roadmap")


if __name__ == "__main__":
    for f in [make_L01_01_render_pipeline, make_L01_02_frame_loop,
              make_L02_01_light_types, make_L02_02_pbr_params, make_L02_03_baked_vs_realtime,
              make_L03_01_material_shader, make_L03_02_texture_channels, make_L03_03_blend_modes,
              make_L04_01_vrc_stack, make_L04_02_budget, make_L04_03_optimize,
              make_L05_01_crystal_steps, make_L05_02_crystal_result,
              make_L06_01_cheatsheet, make_L06_02_common_issues, make_L06_03_roadmap]:
        print(f"生成 {f.__name__} ...")
        f()
    print("全部完成")
