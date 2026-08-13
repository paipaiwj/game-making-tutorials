# -*- coding: utf-8 -*-
# Unity VFX 入门教程 — 配图生成脚本
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _render_svg import *


# ============================================================
# L01 — 图1: 什么是特效 / 特效在游戏中的作用
# ============================================================
def make_L01_01_what_is_vfx():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "游戏特效是什么？", W//2, 36, fill=TEXT, size=22, weight="bold", anchor="middle")
    add_text(dwg, "VFX（Visual Effects）是游戏中增强视觉表现力的动态元素", W//2, 66, fill=TEXT_DIM, size=13, anchor="middle")

    # 四类特效卡片
    items = [
        ("粒子特效", "火焰、烟雾、\n爆炸、魔法", ACCENT),
        ("轨迹特效", "刀光、拖尾、\n光束、弹道", SUCCESS),
        ("环境特效", "雨雪、落叶、\n灰尘、光晕", WARM),
        ("UI特效", "按钮光效、\n转场动画", "#c084fc"),
    ]
    card_w, card_h = 180, 160
    start_x = (W - (card_w * 4 + 20 * 3)) // 2
    for i, (title, desc, color) in enumerate(items):
        cx = start_x + i * (card_w + 20)
        cy = 110
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_ellipse(dwg, cx + card_w//2, cy + 36, 20, 20, fill=color, stroke="none", opacity=0.6)
        add_text(dwg, title, cx + card_w//2, cy + 74, fill="#fff", size=15, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, cy + 100 + j * 18, fill=TEXT_DIM, size=12, anchor="middle")

    add_text(dwg, "Unity 中最核心的特效工具：Shuriken Particle System（粒子系统）", W//2, H - 40, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L01_01_what_is_vfx")


# ============================================================
# L01 — 图2: Particle System 组件全貌
# ============================================================
def make_L01_02_particle_system_overview():
    W, H = 900, 600
    dwg = new_svg(W, H)
    add_text(dwg, "Particle System 组件结构", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 左侧：GameObject 层级
    add_text(dwg, "GameObject", 60, 80, fill=TEXT_DIM, size=12)
    add_rect(dwg, 40, 90, 220, 400, fill=PANEL, stroke=BORDER, rx=8)
    # Transform
    add_rect(dwg, 55, 105, 190, 35, fill="#1a1a1a", stroke=BORDER, rx=4)
    add_text(dwg, "Transform", 70, 127, fill=TEXT_DIM, size=13)
    # Particle System
    add_rect(dwg, 55, 150, 190, 35, fill=ACCENT, stroke=ACCENT, rx=4, opacity=0.2)
    add_text(dwg, "Particle System", 70, 172, fill=ACCENT, size=13, weight="bold")
    # 子模块列表
    modules = [
        ("Main", "主模块"),
        ("Emission", "发射"),
        ("Shape", "形状"),
        ("Velocity over Lifetime", "速度"),
        ("Color over Lifetime", "颜色"),
        ("Size over Lifetime", "大小"),
        ("Renderer", "渲染"),
    ]
    for i, (mod, desc) in enumerate(modules):
        y = 200 + i * 36
        add_rect(dwg, 55, y, 190, 30, fill="#1a1a1a", stroke=BORDER, rx=4)
        add_text(dwg, mod, 70, y + 20, fill=TEXT, size=12)
        add_text(dwg, desc, 180, y + 20, fill=TEXT_MUTED, size=10, anchor="end")

    # 右侧：说明
    rx = 310
    add_rect(dwg, rx, 90, 560, 180, fill=PANEL, stroke=ACCENT, rx=8, stroke_width=1.5)
    add_text(dwg, "核心概念", rx + 20, 120, fill=ACCENT, size=16, weight="bold")
    concepts = [
        "粒子 = 一个个小图片（Quad），以极高速度生成、运动、消失",
        "粒子系统 = 控制这些粒子的「导演」：在哪里生、怎么飞、长什么样",
        "模块化设计 = 每个模块独立控制一个方面，勾选即启用",
        "一个 GameObject 可以有多个 Particle System 协同工作",
    ]
    for i, c in enumerate(concepts):
        add_ellipse(dwg, rx + 30, 150 + i * 28, 4, 4, fill=ACCENT)
        add_text(dwg, c, rx + 45, 154 + i * 28, fill=TEXT_DIM, size=13)

    # 下方：生命周期的示意
    add_text(dwg, "粒子生命周期", rx + 20, 300, fill=TEXT, size=15, weight="bold")
    add_rect(dwg, rx, 320, 560, 160, fill="#1a1a1a", stroke=BORDER, rx=8)
    # 时间线
    add_line(dwg, rx + 30, 380, rx + 530, 380, stroke=ACCENT, stroke_width=2)
    add_arrow(dwg, rx + 520, 380, rx + 545, 380, stroke=ACCENT, stroke_width=2)
    add_text(dwg, "出生", rx + 30, 370, fill=SUCCESS, size=11, anchor="middle")
    add_text(dwg, "运动+变化", rx + 200, 370, fill=WARM, size=11, anchor="middle")
    add_text(dwg, "消亡", rx + 480, 370, fill=TEXT_MUTED, size=11, anchor="middle")
    # 粒子示意
    for i in range(5):
        px = rx + 60 + i * 100
        size = 6 + i * 6
        alpha = 1.0 - i * 0.18
        add_ellipse(dwg, px, 380, size, size, fill=ACCENT, opacity=alpha)
    # 下方说明
    add_text(dwg, "Duration（持续时间）", rx + 60, 420, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "Start Lifetime", rx + 200, 420, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "每个粒子的存活时间", rx + 200, 438, fill=TEXT_MUTED, size=11, anchor="middle")
    add_text(dwg, "循环 / 一次性", rx + 400, 420, fill=TEXT_DIM, size=12, anchor="middle")

    save_svg_and_png(dwg, "L01_02_particle_system_overview")


# ============================================================
# L01 — 图3: 创建一个简单的粒子系统
# ============================================================
def make_L01_03_create_particles():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "创建第一个粒子系统", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 步骤
    steps = [
        ("1", "Hierarchy 右键", "Effects → Particle System"),
        ("2", "选中粒子物体", "查看 Inspector"),
        ("3", "展开 Main 模块", "设置 Duration=5, Looping=勾上"),
        ("4", "调整 Start Speed", "设为 3，粒子飞得更快"),
    ]
    for i, (num, title, desc) in enumerate(steps):
        x = 40 + i * 215
        add_rect(dwg, x, 70, 195, 160, fill=PANEL, stroke=BORDER, rx=8)
        add_ellipse(dwg, x + 25, 95, 16, 16, fill=ACCENT)
        add_text(dwg, num, x + 25, 100, fill="#fff", size=14, weight="bold", anchor="middle")
        add_text(dwg, title, x + 50, 98, fill="#fff", size=14, weight="bold")
        add_text(dwg, desc, x + 16, 135, fill=TEXT_DIM, size=12)
        if i < 3:
            add_arrow(dwg, x + 195, 150, x + 215, 150, stroke=ACCENT)

    # 结果预览
    add_rect(dwg, 40, 260, 820, 100, fill="#1a1a1a", stroke=SUCCESS, rx=8, stroke_width=1.5)
    add_text(dwg, "点击 Play 后你应该看到：", 70, 290, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "场景中出现了向上飘散的白色小方块 — 这就是你的第一个粒子特效！", 70, 320, fill=TEXT_DIM, size=13)
    add_text(dwg, "默认材质是 Default-Particle，白色方块是默认的粒子形状", 70, 342, fill=TEXT_MUTED, size=12)

    save_svg_and_png(dwg, "L01_03_create_particles")


# ============================================================
# L02 — 图1: Shuriken 模块全景
# ============================================================
def make_L02_01_module_overview():
    W, H = 920, 620
    dwg = new_svg(W, H)
    add_text(dwg, "Shuriken 粒子系统 — 核心模块一览", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    modules = [
        ("Main", "持续时间、循环、预热、\n起始生命/速度/大小/颜色", ACCENT, True),
        ("Emission", "每秒发射多少粒子、\n爆发式发射", SUCCESS, True),
        ("Shape", "粒子从什么形状发射\n球形/锥形/盒形/网格", WARM, True),
        ("Velocity over\nLifetime", "粒子飞行过程中的\n速度变化", "#c084fc", False),
        ("Color over\nLifetime", "粒子颜色随时间渐变\n(需要 Gradient)", "#f472b6", False),
        ("Size over\nLifetime", "粒子大小随时间变化\n从小到大或从大到小", "#60a5fa", False),
        ("Rotation over\nLifetime", "粒子旋转动画", "#fbbf24", False),
        ("Renderer", "用什么材质/贴图渲染\n朝向摄像机模式", TEXT_DIM, True),
    ]

    card_w, card_h = 210, 130
    cols = 4
    gap_x, gap_y = 15, 15
    start_x = (W - (card_w * cols + gap_x * (cols - 1))) // 2

    for i, (name, desc, color, required) in enumerate(modules):
        col = i % cols
        row = i // cols
        cx = start_x + col * (card_w + gap_x)
        cy = 70 + row * (card_h + gap_y)
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        # 标题
        add_text(dwg, name, cx + card_w//2, cy + 28, fill="#fff", size=13, weight="bold", anchor="middle")
        # 标签
        tag = "必用" if required else "常用"
        tag_color = SUCCESS if required else WARN
        add_rect(dwg, cx + card_w//2 - 22, cy + 40, 44, 18, fill=tag_color, rx=9, stroke="none", opacity=0.3)
        add_text(dwg, tag, cx + card_w//2, cy + 53, fill=tag_color, size=10, weight="bold", anchor="middle")
        # 描述
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, cy + 72 + j * 18, fill=TEXT_DIM, size=11, anchor="middle")

    save_svg_and_png(dwg, "L02_01_module_overview")


# ============================================================
# L02 — 图2: Emission 与 Shape 详解
# ============================================================
def make_L02_02_emission_shape():
    W, H = 900, 520
    dwg = new_svg(W, H)
    add_text(dwg, "Emission（发射）与 Shape（形状）", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # Emission 区域
    add_rect(dwg, 30, 65, 400, 200, fill=PANEL, stroke=SUCCESS, rx=8, stroke_width=1.5)
    add_text(dwg, "Emission 模块", 50, 95, fill=SUCCESS, size=16, weight="bold")
    add_text(dwg, "控制「每秒产生多少粒子」", 50, 118, fill=TEXT_DIM, size=12)

    emit_items = [
        ("Rate over Time", "每秒发射 N 个粒子（持续流）", "默认 10"),
        ("Rate over Distance", "每移动 N 单位发射粒子（拖尾用）", "默认 0"),
        ("Bursts", "在特定时间点爆发 N 个粒子（爆炸用）", "点击 + 添加"),
    ]
    for i, (prop, desc, default) in enumerate(emit_items):
        y = 140 + i * 40
        add_text(dwg, prop, 60, y, fill=ACCENT, size=13, weight="bold")
        add_text(dwg, desc, 60, y + 18, fill=TEXT_DIM, size=11)
        add_text(dwg, default, 380, y + 18, fill=TEXT_MUTED, size=11, anchor="end")

    # Shape 区域
    add_rect(dwg, 460, 65, 410, 200, fill=PANEL, stroke=WARM, rx=8, stroke_width=1.5)
    add_text(dwg, "Shape 模块", 480, 95, fill=WARM, size=16, weight="bold")
    add_text(dwg, "控制「粒子从什么形状的区域发射出来」", 480, 118, fill=TEXT_DIM, size=12)

    shapes = [
        ("Sphere", "球形发射 — 最常用"),
        ("Cone", "锥形发射 — 喷火/魔法"),
        ("Box", "盒形发射 — 方形区域"),
        ("Circle", "圆形发射 — 地面光环"),
        ("Mesh", "从模型表面发射"),
    ]
    for i, (shape, desc) in enumerate(shapes):
        y = 140 + i * 30
        add_ellipse(dwg, 490, y + 4, 4, 4, fill=WARM)
        add_text(dwg, shape, 505, y + 10, fill=ACCENT, size=12, weight="bold")
        add_text(dwg, desc, 590, y + 10, fill=TEXT_DIM, size=12)

    # 底部示意
    add_text(dwg, "组合示例", 50, 295, fill=TEXT, size=15, weight="bold")
    add_rect(dwg, 30, 315, 840, 185, fill="#1a1a1a", stroke=BORDER, rx=8)

    examples = [
        ("火焰", "Cone + Rate 50", "锥形向上喷大量粒子", ACCENT),
        ("爆炸", "Sphere + Burst 100", "球形一次性爆发", WARM),
        ("雨", "Box(宽扁) + Rate 200", "大范围持续下落", SUCCESS),
        ("拖尾", "Circle + Rate/Distance", "随移动发射粒子", "#c084fc"),
    ]
    for i, (name, combo, desc, color) in enumerate(examples):
        x = 50 + i * 200
        add_rect(dwg, x, 335, 180, 145, fill=PANEL, stroke=color, rx=6, stroke_width=1)
        add_text(dwg, name, x + 90, 360, fill="#fff", size=14, weight="bold", anchor="middle")
        add_text(dwg, combo, x + 90, 385, fill=color, size=12, anchor="middle")
        add_text(dwg, desc, x + 90, 410, fill=TEXT_DIM, size=11, anchor="middle")
        add_text(dwg, "Shape + Emission", x + 90, 440, fill=TEXT_MUTED, size=10, anchor="middle", italic=True)

    save_svg_and_png(dwg, "L02_02_emission_shape")


# ============================================================
# L02 — 图3: Color/Size over Lifetime
# ============================================================
def make_L02_03_color_size_lifetime():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "Color over Lifetime & Size over Lifetime", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "让粒子在生命周期中动态变化", W//2, 58, fill=TEXT_DIM, size=13, anchor="middle")

    # Color over Lifetime
    add_rect(dwg, 30, 85, 400, 170, fill=PANEL, stroke="#f472b6", rx=8, stroke_width=1.5)
    add_text(dwg, "Color over Lifetime", 50, 115, fill="#f472b6", size=15, weight="bold")
    add_text(dwg, "粒子颜色随时间渐变", 50, 138, fill=TEXT_DIM, size=12)
    add_text(dwg, "使用 Gradient 编辑器：", 50, 160, fill=TEXT_DIM, size=12)
    # Gradient 示意
    colors = ["#ffffff", "#ffcc00", "#ff6600", "#330000"]
    seg_w = 85
    for i, c in enumerate(colors):
        add_rect(dwg, 60 + i * seg_w, 178, seg_w, 24, fill=c, stroke=BORDER, rx=0)
    add_text(dwg, "0%", 60, 216, fill=TEXT_MUTED, size=10, anchor="middle")
    add_text(dwg, "25%", 60 + seg_w, 216, fill=TEXT_MUTED, size=10, anchor="middle")
    add_text(dwg, "50%", 60 + seg_w * 2, 216, fill=TEXT_MUTED, size=10, anchor="middle")
    add_text(dwg, "100%", 60 + seg_w * 3, 216, fill=TEXT_MUTED, size=10, anchor="middle")
    add_text(dwg, "白→黄→橙→暗红（火焰渐变）", 60 + seg_w * 2, 240, fill=TEXT_DIM, size=11, anchor="middle")

    # Size over Lifetime
    add_rect(dwg, 460, 85, 410, 170, fill=PANEL, stroke="#60a5fa", rx=8, stroke_width=1.5)
    add_text(dwg, "Size over Lifetime", 480, 115, fill="#60a5fa", size=15, weight="bold")
    add_text(dwg, "粒子大小随时间变化", 480, 138, fill=TEXT_DIM, size=12)
    add_text(dwg, "使用 Curve 曲线编辑器：", 480, 160, fill=TEXT_DIM, size=12)
    # Curve 示意
    add_rect(dwg, 480, 178, 370, 60, fill="#1a1a1a", stroke=BORDER, rx=4)
    add_line(dwg, 490, 230, 490, 188, stroke=TEXT_MUTED, stroke_width=0.5)
    add_line(dwg, 490, 230, 840, 230, stroke=TEXT_MUTED, stroke_width=0.5)
    # 一条曲线示意（从小到大再到小）
    add_line(dwg, 490, 225, 560, 200, stroke="#60a5fa", stroke_width=2)
    add_line(dwg, 560, 200, 680, 195, stroke="#60a5fa", stroke_width=2)
    add_line(dwg, 680, 195, 840, 230, stroke="#60a5fa", stroke_width=2)
    add_text(dwg, "time", 830, 250, fill=TEXT_MUTED, size=10, anchor="end")
    add_text(dwg, "size", 500, 182, fill=TEXT_MUTED, size=10)
    add_text(dwg, "从小到大再缩小（爆发效果）", 665, 252, fill=TEXT_DIM, size=11, anchor="middle")

    # 底部：常见组合
    add_text(dwg, "经典组合公式", 50, 290, fill=TEXT, size=15, weight="bold")
    add_rect(dwg, 30, 310, 840, 145, fill="#1a1a1a", stroke=BORDER, rx=8)

    combos = [
        ("火焰", "Color: 白→黄→红→透明", "Size: 大到小", "Cone + 大量粒子"),
        ("魔法光球", "Color: 亮蓝→紫→淡出", "Size: 小到大", "Sphere + Burst"),
        ("烟雾", "Color: 灰→淡灰→透明", "Size: 小到大", "Sphere + 低速"),
        ("星光闪烁", "Color: 白→黄→透明", "Size: 随机大小", "Sphere + 小量"),
    ]
    for i, (name, col, siz, shape) in enumerate(combos):
        x = 50 + i * 205
        add_text(dwg, name, x, 335, fill="#fff", size=13, weight="bold")
        add_text(dwg, col, x, 358, fill="#f472b6", size=11)
        add_text(dwg, siz, x, 376, fill="#60a5fa", size=11)
        add_text(dwg, shape, x, 394, fill=WARM, size=11)

    save_svg_and_png(dwg, "L02_03_color_size_lifetime")


# ============================================================
# L03 — 图1: 粒子材质与贴图
# ============================================================
def make_L03_01_material_texture():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "粒子材质与贴图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 材质选择
    add_rect(dwg, 30, 65, 270, 200, fill=PANEL, stroke=ACCENT, rx=8, stroke_width=1.5)
    add_text(dwg, "材质（Material）", 50, 95, fill=ACCENT, size=15, weight="bold")
    mats = [
        "Default-Particle — Unity 内置，白色方形",
        "Particles/Additive — 叠加混合，发光效果",
        "Particles/Alpha Blended — 标准透明",
        "Particles/Multiply — 正片叠底，阴影效果",
    ]
    for i, m in enumerate(mats):
        add_text(dwg, m, 50, 122 + i * 28, fill=TEXT_DIM, size=11)

    # Shader 选择
    add_rect(dwg, 320, 65, 270, 200, fill=PANEL, stroke=SUCCESS, rx=8, stroke_width=1.5)
    add_text(dwg, "Shader 类型", 340, 95, fill=SUCCESS, size=15, weight="bold")
    add_text(dwg, "Particles/Standard Surface", 340, 122, fill=ACCENT, size=12, weight="bold")
    add_text(dwg, "受光照影响，有立体感", 340, 142, fill=TEXT_DIM, size=11)
    add_text(dwg, "Particles/Standard Unlit", 340, 168, fill=WARM, size=12, weight="bold")
    add_text(dwg, "不受光照，始终保持亮度", 340, 188, fill=TEXT_DIM, size=11)
    add_text(dwg, "VRChat 推荐 Unlit", 340, 210, fill=SUCCESS, size=11, weight="bold")

    # 贴图
    add_rect(dwg, 610, 65, 260, 200, fill=PANEL, stroke=WARM, rx=8, stroke_width=1.5)
    add_text(dwg, "贴图（Texture）", 630, 95, fill=WARM, size=15, weight="bold")
    add_text(dwg, "粒子形状由贴图决定", 630, 122, fill=TEXT_DIM, size=12)
    add_text(dwg, "默认是白色方块", 630, 148, fill=TEXT_MUTED, size=11)
    add_text(dwg, "换成圆形贴图→圆形粒子", 630, 170, fill=TEXT_DIM, size=11)
    add_text(dwg, "换成光晕贴图→发光粒子", 630, 192, fill=TEXT_DIM, size=11)
    add_text(dwg, "推荐：Default-Particle", 630, 218, fill=SUCCESS, size=11, weight="bold")
    add_text(dwg, "（Unity 内置圆形光点）", 630, 236, fill=TEXT_MUTED, size=10)

    # 底部：Renderer 模块
    add_text(dwg, "Renderer 模块关键设置", 50, 300, fill=TEXT, size=15, weight="bold")
    add_rect(dwg, 30, 320, 840, 155, fill="#1a1a1a", stroke=BORDER, rx=8)

    settings = [
        ("Render Mode", "Billboard（始终面朝摄像机）", "最常用，粒子始终对着玩家"),
        ("Stretched Billboard", "拉伸面片 — 适合速度感拖尾", "按速度方向拉伸粒子"),
        ("Horizontal Billboard", "水平面片 — 地面特效", "粒子平行于地面"),
        ("Material", "指定粒子的材质球", "决定 Shader + 贴图"),
        ("Sort Mode", "排序模式 — By Distance 最常用", "远处粒子先渲染"),
    ]
    for i, (prop, desc, note) in enumerate(settings):
        y = 340 + i * 26
        add_text(dwg, prop, 50, y + 4, fill=ACCENT, size=12, weight="bold")
        add_text(dwg, desc, 210, y + 4, fill=TEXT_DIM, size=12)
        add_text(dwg, note, 580, y + 4, fill=TEXT_MUTED, size=11)

    save_svg_and_png(dwg, "L03_01_material_texture")


# ============================================================
# L03 — 图2: 常用特效贴图类型
# ============================================================
def make_L03_02_texture_types():
    W, H = 900, 380
    dwg = new_svg(W, H)
    add_text(dwg, "常用粒子贴图类型", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    types = [
        ("圆形光点", "最通用 — 魔法球、\n光点、火花", ACCENT, 1.0),
        ("环形", "冲击波、光环、\n护盾", SUCCESS, 0.8),
        ("放射线", "光束、激光、\n能量射线", WARM, 0.9),
        ("烟雾/云", "烟雾、尘土、\n蒸汽", TEXT_DIM, 0.6),
        ("星形", "闪光、星星、\n魔法光点", "#f472b6", 0.9),
    ]

    card_w = 160
    gap = 15
    start_x = (W - (card_w * 5 + gap * 4)) // 2

    for i, (name, desc, color, alpha) in enumerate(types):
        cx = start_x + i * (card_w + gap)
        add_rect(dwg, cx, 70, card_w, 240, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        # 粒子示意
        add_ellipse(dwg, cx + card_w//2, 110, 35, 35, fill=color, stroke="none", opacity=alpha * 0.3)
        add_ellipse(dwg, cx + card_w//2, 110, 20, 20, fill=color, stroke="none", opacity=alpha * 0.6)
        add_ellipse(dwg, cx + card_w//2, 110, 8, 8, fill="#fff", stroke="none", opacity=alpha)

        add_text(dwg, name, cx + card_w//2, 155, fill="#fff", size=14, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 180 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")

    add_text(dwg, "贴图可在 Unity Asset Store 或粒子特效包中找到，也可以用 Photoshop/GIMP 自制", W//2, H - 30, fill=TEXT_MUTED, size=11, anchor="middle", italic=True)

    save_svg_and_png(dwg, "L03_02_texture_types")


# ============================================================
# L04 — 图1: VRChat 特效限制
# ============================================================
def make_L04_01_vrc_limits():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "VRChat 中的特效限制与注意事项", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 限制列表
    limits = [
        ("最大粒子数", "每个 Particle System ≤ 10000 个粒子", "超过会严重影响性能"),
        ("材质限制", "Shader 必须使用 VRChat 允许的列表", "Particles/Standard Unlit 是安全选择"),
        ("音频联动", "粒子系统不能直接播放音频", "需要单独的 AudioSource"),
        ("碰撞", "粒子碰撞 (Collision) 开销极大", "尽量用 World 模式而非 3D 碰撞"),
        ("VR 性能", "Quest 平台性能更紧张", "粒子总数建议控制在 2000 以内"),
    ]

    for i, (title, desc, note) in enumerate(limits):
        y = 70 + i * 78
        add_rect(dwg, 30, y, 840, 65, fill=PANEL, stroke=WARN if i < 2 else BORDER, rx=8, stroke_width=1)
        add_text(dwg, title, 55, y + 22, fill=WARM, size=14, weight="bold")
        add_text(dwg, desc, 55, y + 44, fill=TEXT_DIM, size=12)
        add_text(dwg, note, 600, y + 30, fill=TEXT_MUTED, size=11)

    # 底部建议
    add_text(dwg, "VRChat 特效黄金法则", 50, 465, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "少即是多：少量精心调校的粒子  >  大量粗糙的粒子", 50, 485, fill=TEXT_DIM, size=13)

    save_svg_and_png(dwg, "L04_01_vrc_limits")


# ============================================================
# L04 — 图2: 性能优化建议
# ============================================================
def make_L04_02_performance():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "粒子系统性能优化", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    tips = [
        ("Max Particles", "限制最大粒子数", "默认 1000，按需降低", SUCCESS),
        ("贴图尺寸", "粒子贴图 ≤ 256×256", "越小越好，视觉差别不大", SUCCESS),
        ("Simulation Speed", "模拟速度", "0.5 = 慢动作，省粒子", ACCENT),
        ("Culling Mode", "剔除模式", "离远自动暂停，必开", SUCCESS),
        ("Prewarm", "预热", "仅在需要开场特效时开", WARN),
    ]

    for i, (prop, desc, note, color) in enumerate(tips):
        y = 70 + i * 62
        add_rect(dwg, 30, y, 840, 50, fill=PANEL, stroke=color, rx=6, stroke_width=1)
        add_text(dwg, prop, 55, y + 18, fill=color, size=13, weight="bold")
        add_text(dwg, desc, 220, y + 18, fill=TEXT_DIM, size=13)
        add_text(dwg, note, 500, y + 18, fill=TEXT_MUTED, size=12)
        tag = "推荐" if color == SUCCESS else "可选"
        add_rect(dwg, 770, y + 15, 40, 20, fill=color, rx=4, stroke="none", opacity=0.2)
        add_text(dwg, tag, 790, y + 28, fill=color, size=10, weight="bold", anchor="middle")

    # 底部
    add_rect(dwg, 30, 380, 840, 30, fill="#1a2a1a", stroke=SUCCESS, rx=6, stroke_width=1, opacity=0.5)
    add_text(dwg, "在 Game 视图的 Stats 面板中可以查看粒子数 — 保持它在合理范围内", W//2, 399, fill=SUCCESS, size=12, anchor="middle")

    save_svg_and_png(dwg, "L04_02_performance")


# ============================================================
# L05 — 图1: 传送门特效步骤
# ============================================================
def make_L05_01_portal_steps():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "动手：制作一个传送门特效", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "一个完整的传送门由 3 个粒子系统组合而成", W//2, 58, fill=TEXT_DIM, size=13, anchor="middle")

    # 三个粒子系统
    systems = [
        ("光环", "环形粒子旋转", "Shape: Circle\nRate: 20\nColor: 蓝→紫\nSize: 中等恒定", ACCENT),
        ("上升粒子", "从光环向上飘散", "Shape: Circle\nRate: 50\nColor: 白→蓝→透明\nSize: 小→大", SUCCESS),
        ("中心光球", "中心发光核心", "Shape: Sphere(小)\nRate: 5\nColor: 亮白→淡蓝\nSize: 大→小", WARM),
    ]

    for i, (name, desc, params, color) in enumerate(systems):
        x = 30 + i * 290
        add_rect(dwg, x, 80, 270, 180, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        add_text(dwg, f"系统 {i+1}: {name}", x + 20, 108, fill="#fff", size=14, weight="bold")
        add_text(dwg, desc, x + 20, 130, fill=TEXT_DIM, size=12)
        for j, line in enumerate(params.split("\n")):
            add_text(dwg, line, x + 20, 160 + j * 22, fill=color, size=12)

    # 步骤
    add_text(dwg, "制作步骤", 50, 295, fill=TEXT, size=15, weight="bold")
    add_rect(dwg, 30, 315, 840, 155, fill="#1a1a1a", stroke=BORDER, rx=8)

    steps = [
        "1. 创建空 GameObject 命名为「Portal」，作为三个粒子系统的父物体",
        "2. 在 Portal 下创建三个 Particle System，分别命名为 Ring / Rising / Core",
        "3. 按上表配置每个系统的参数（Shape、Rate、Color、Size）",
        "4. 调整 Transform：光环水平放置（X旋转90°），上升粒子竖直（默认），光球居中",
        "5. 播放测试，微调各系统的 Rate 和 Color 直到满意",
    ]
    for i, s in enumerate(steps):
        add_text(dwg, s, 50, 338 + i * 26, fill=TEXT_DIM, size=12)

    save_svg_and_png(dwg, "L05_01_portal_steps")


# ============================================================
# L05 — 图2: 传送门最终效果示意
# ============================================================
def make_L05_02_portal_result():
    W, H = 900, 350
    dwg = new_svg(W, H)
    add_text(dwg, "传送门最终效果", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 光环（水平环）
    add_ellipse(dwg, W//2, 180, 120, 30, fill="none", stroke=ACCENT, stroke_width=3, opacity=0.8)
    add_ellipse(dwg, W//2, 180, 100, 22, fill="none", stroke="#7cb8ff", stroke_width=2, opacity=0.5)

    # 上升粒子示意
    for i in range(8):
        px = W//2 - 80 + i * 22
        py = 180 - (i % 3) * 30 - 10
        size = 3 + (i % 4)
        alpha = 0.3 + (i % 3) * 0.2
        add_ellipse(dwg, px, py, size, size, fill=ACCENT, opacity=alpha)

    # 中心光球
    add_ellipse(dwg, W//2, 180, 18, 18, fill="#fff", stroke="none", opacity=0.9)
    add_ellipse(dwg, W//2, 180, 30, 30, fill=ACCENT, stroke="none", opacity=0.4)
    add_ellipse(dwg, W//2, 180, 50, 50, fill=ACCENT, stroke="none", opacity=0.15)

    # 标签
    add_text(dwg, "光环（水平环形）", W//2 - 140, 140, fill=ACCENT, size=11, anchor="middle")
    add_text(dwg, "上升粒子", W//2 + 160, 110, fill=SUCCESS, size=11, anchor="middle")
    add_text(dwg, "中心光球", W//2 + 160, 220, fill=WARM, size=11, anchor="middle")

    # 箭头
    add_line(dwg, W//2 - 40, 150, W//2 - 20, 165, stroke=TEXT_MUTED, stroke_width=1)
    add_line(dwg, W//2 + 120, 130, W//2 + 80, 155, stroke=TEXT_MUTED, stroke_width=1)
    add_line(dwg, W//2 + 120, 200, W//2 + 60, 190, stroke=TEXT_MUTED, stroke_width=1)

    add_text(dwg, "三个系统叠加 = 完整的传送门效果", W//2, H - 30, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)

    save_svg_and_png(dwg, "L05_02_portal_result")


# ============================================================
# L06 — 图1: 速查表
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 920, 600
    dwg = new_svg(W, H)
    add_text(dwg, "Unity 粒子特效速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 模块速查
    add_text(dwg, "核心模块速查", 30, 65, fill=ACCENT, size=14, weight="bold")

    headers = ["模块", "关键参数", "常用值", "说明"]
    col_x = [30, 200, 430, 560]
    col_w = [160, 220, 120, 320]

    # 表头
    for j, (hdr, cx, cw) in enumerate(zip(headers, col_x, col_w)):
        add_rect(dwg, cx, 75, cw, 28, fill=PANEL, stroke=BORDER, rx=0)
        add_text(dwg, hdr, cx + 8, 94, fill=ACCENT, size=12, weight="bold")

    rows = [
        ("Main", "Duration / Looping / Start Lifetime", "5 / 勾上 / 2", "粒子系统持续时间和每个粒子存活时间"),
        ("Emission", "Rate over Time / Bursts", "20 / 按需", "每秒粒子数；爆发用于爆炸等一次性效果"),
        ("Shape", "Shape / Radius / Angle", "Cone / 1 / 15°", "粒子发射的形状和范围"),
        ("Color over Lifetime", "Color (Gradient)", "白→橙→红→透明", "粒子颜色随时间渐变"),
        ("Size over Lifetime", "Size (Curve)", "从大到小", "粒子大小随时间变化曲线"),
        ("Velocity over Lifetime", "Linear X/Y/Z", "Y: 2 (上升)", "粒子飞行中的速度变化"),
        ("Renderer", "Render Mode / Material", "Billboard / Default-Particle", "粒子如何渲染，材质决定外观"),
        ("Noise", "Strength / Frequency", "1 / 0.5", "给粒子运动添加随机扰动（风、飘动）"),
    ]

    for i, (mod, params, common, desc) in enumerate(rows):
        y = 107 + i * 30
        bg = "#1a1a1a" if i % 2 == 0 else PANEL
        for j, (text, cx, cw) in enumerate(zip([mod, params, common, desc], col_x, col_w)):
            add_rect(dwg, cx, y, cw, 26, fill=bg, stroke=BORDER, rx=0, stroke_width=0.5)
            color = ACCENT if j == 0 else (WARN if j == 2 else TEXT_DIM)
            add_text(dwg, text, cx + 8, y + 18, fill=color, size=11)

    # 常见问题
    add_text(dwg, "常见问题", 30, 360, fill=WARM, size=14, weight="bold")

    faq = [
        ("粒子不显示？", "检查 Duration > 0, Looping 是否勾上，Play 是否按下"),
        ("粒子是粉色的？", "材质丢失 — 给 Renderer 模块指定一个材质"),
        ("粒子不动？", "Start Speed = 0，需要设置大于 0 的值"),
        ("粒子太小看不到？", "Start Size 默认是 1，调大到 3-5 试试"),
        ("VRChat 中粒子不跟随？", "粒子系统必须放在有 Transform 的 GameObject 上"),
        ("性能太差？", "降低 Max Particles 和 Rate，减小贴图尺寸"),
    ]

    for i, (q, a) in enumerate(faq):
        y = 385 + i * 32
        add_text(dwg, q, 45, y + 8, fill=WARM, size=12, weight="bold")
        add_text(dwg, a, 220, y + 8, fill=TEXT_DIM, size=12)

    save_svg_and_png(dwg, "L06_01_cheatsheet")


# ============================================================
# L06 — 图2: 学习路线图
# ============================================================
def make_L06_02_roadmap():
    W, H = 900, 400
    dwg = new_svg(W, H)
    add_text(dwg, "特效学习路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    nodes = [
        ("入门", "理解粒子系统\n创建第一个特效", ACCENT, 60),
        ("核心模块", "掌握 Main/Emission/\nShape 三大模块", SUCCESS, 280),
        ("视觉打磨", "Color/Size over\nLifetime 动态变化", WARM, 500),
        ("实战", "组合多个系统\n制作完整特效", "#c084fc", 720),
    ]

    for i, (title, desc, color, cx) in enumerate(nodes):
        cy = 120
        add_rect(dwg, cx - 80, cy, 160, 130, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_ellipse(dwg, cx, cy + 28, 22, 22, fill=color, stroke="none", opacity=0.4)
        add_text(dwg, title, cx, cy + 60, fill="#fff", size=15, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx, cy + 82 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + 80, cy + 65, cx + 120, cy + 65, stroke=ACCENT, stroke_width=2)

    # 底部建议
    add_text(dwg, "进阶方向", W//2, 285, fill=TEXT, size=14, weight="bold", anchor="middle")
    advanced = [
        "学习 Sub Emitter（子发射器）— 粒子消亡时生成新粒子",
        "学习 Noise 模块 — 给粒子添加随机扰动",
        "学习 Triggers 模块 — 粒子碰撞触发事件",
        "学习 Custom Data — 在 Shader 中读取粒子自定义数据",
    ]
    for i, a in enumerate(advanced):
        add_ellipse(dwg, 100, 315 + i * 24, 4, 4, fill=ACCENT)
        add_text(dwg, a, 120, 319 + i * 24, fill=TEXT_DIM, size=12)

    save_svg_and_png(dwg, "L06_02_roadmap")


# ============================================================
if __name__ == "__main__":
    print("生成 L01 配图...")
    make_L01_01_what_is_vfx()
    make_L01_02_particle_system_overview()
    make_L01_03_create_particles()
    print("生成 L02 配图...")
    make_L02_01_module_overview()
    make_L02_02_emission_shape()
    make_L02_03_color_size_lifetime()
    print("生成 L03 配图...")
    make_L03_01_material_texture()
    make_L03_02_texture_types()
    print("生成 L04 配图...")
    make_L04_01_vrc_limits()
    make_L04_02_performance()
    print("生成 L05 配图...")
    make_L05_01_portal_steps()
    make_L05_02_portal_result()
    print("生成 L06 配图...")
    make_L06_01_cheatsheet()
    make_L06_02_roadmap()
    print("\n全部配图生成完毕！")
