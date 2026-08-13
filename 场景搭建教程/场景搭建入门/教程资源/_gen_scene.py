# -*- coding: utf-8 -*-
# Unity 场景搭建入门教程（面向 VRChat）— 配图生成脚本
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _render_svg import *

_grad_counter = [0]

def _gid():
    _grad_counter[0] += 1
    return f"g{_grad_counter[0]}"

def linear_grad(dwg, x1, y1, x2, y2, stops):
    gid = _gid()
    grad = dwg.linearGradient(start=(x1, y1), end=(x2, y2), id=gid)
    for off, col, op in stops:
        grad.add_stop_color(offset=off, color=col, opacity=op)
    dwg.defs.add(grad)
    return f"url(#{gid})"

# 伪 3D 方块（顶面 + 前面 + 右侧面）
def draw_box(dwg, x, y, w, h, d=16, dh=12, top="#3a3a3a", front="#2f2f2f",
             side="#282828", stroke="#4a4a4a"):
    dwg.add(dwg.polygon(points=[(x, y), (x + d, y - dh), (x + w + d, y - dh),
                                (x + w, y)], fill=top, stroke=stroke, stroke_width=1.2))
    add_rect(dwg, x, y, w, h, fill=front, stroke=stroke)
    dwg.add(dwg.polygon(points=[(x + w, y), (x + w + d, y - dh),
                                (x + w + d, y - dh + h), (x + w, y + h)],
                        fill=side, stroke=stroke, stroke_width=1.2))

# 底部说明卡片
def bottom_note(dwg, title, lines, y, H=900):
    add_rect(dwg, 60, y, H - 120, 86, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, title, 85, y + 26, fill=SUCCESS, size=13.5, weight="bold")
    for j, line in enumerate(lines):
        add_text(dwg, line, 85, y + 50 + j * 20, fill=TEXT_DIM, size=12)


# ============================================================
# L01 — 图1: 白盒 vs 成品
# ============================================================
def make_L01_01_blockout():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "场景搭建：先白盒，再美术", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "用 Cube 搭骨架确定布局，验证没问题后再换正式美术资源", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 左：白盒
    add_rect(dwg, 60, 90, 370, 260, fill=PANEL, stroke=BORDER, rx=10)
    add_text(dwg, "① 白盒 Blockout", 235, 120, fill="#fff", size=14, weight="bold", anchor="middle")
    draw_box(dwg, 110, 170, 70, 50)
    draw_box(dwg, 205, 155, 60, 65)
    draw_box(dwg, 290, 180, 80, 45)
    draw_box(dwg, 140, 240, 90, 60)
    draw_box(dwg, 255, 245, 100, 55)
    add_text(dwg, "全是灰盒子，只关心位置对不对", 235, 328, fill=TEXT_DIM, size=11.5, anchor="middle")

    # 右：成品
    add_rect(dwg, 470, 90, 370, 260, fill=PANEL, stroke=BORDER, rx=10)
    add_text(dwg, "② 美术化", 655, 120, fill="#fff", size=14, weight="bold", anchor="middle")
    # 房子
    draw_box(dwg, 540, 180, 90, 70, top="#8a6a4a", front="#a07a50", side="#7a5c40")
    dwg.add(dwg.polygon(points=[(535, 180), (585, 140), (635, 180)],
                        fill="#b0563a", stroke="#c06848", stroke_width=1.2))
    # 树
    add_rect(dwg, 700, 235, 14, 35, fill="#6a4a30")
    dwg.add(dwg.ellipse(center=(707, 210), r=(26, 30), fill="#4a9a5a", opacity=0.9))
    dwg.add(dwg.ellipse(center=(692, 222), r=(16, 18), fill="#55aa66", opacity=0.9))
    # 火把 + 光
    add_rect(dwg, 490, 235, 8, 40, fill="#7a6a4a")
    add_ellipse(dwg, 494, 225, 14, 10, fill=WARM, opacity=0.35)
    add_ellipse(dwg, 494, 226, 6, 5, fill="#ffcc66")
    add_text(dwg, "树、房子、灯 —— 换成成品资源", 655, 328, fill=TEXT_DIM, size=11.5, anchor="middle")

    add_arrow(dwg, 435, 220, 462, 220, stroke=TEXT_MUTED, stroke_width=2.5)

    bottom_note(dwg, "为什么先白盒？",
                ["白盒改一个位置只要 1 分钟，成品模型挪一次可能 1 小时 —— 布局问题要趁早发现",
                 "白盒阶段反复按 Play 试走动线，满意了再进入美术化，能省掉大量返工"], 380)
    save_svg_and_png(dwg, "L01_01_blockout")


# ============================================================
# L01 — 图2: 玩家动线
# ============================================================
def make_L01_02_player_flow():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "玩家动线：入口 → 主体 → 出口", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "玩家从哪里来、看到什么、去哪 —— 动线决定世界的第一印象", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    nodes = [
        ("入口", "传送点 / 大门\n让玩家看清「这是什么地方」", ACCENT),
        ("主体", "核心区域：篝火、桌子、\n玩法点 —— 一眼能找到", SUCCESS),
        ("出口", "开阔视野 / 出口方向\n留下「还想再来」的念头", WARM),
    ]
    card_w, card_h = 250, 150
    start_x = (W - (card_w * 3 + 34 * 2)) // 2
    for i, (title, desc, color) in enumerate(nodes):
        cx = start_x + i * (card_w + 34)
        add_rect(dwg, cx, 100, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 128, fill="#fff", size=14, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 156 + j * 20, fill=TEXT_DIM, size=11.5, anchor="middle")
        if i < 2:
            add_arrow(dwg, cx + card_w + 6, 175, cx + card_w + 28, 175, stroke=color, stroke_width=2.5)

    bottom_note(dwg, "动线设计三问",
                ["玩家一进来会先看到哪？那里必须是「最好看 / 最重要」的地方",
                 "主体区域要一眼看懂「这里能玩什么」；出口要留悬念，让人愿意再来"], 290)
    save_svg_and_png(dwg, "L01_02_player_flow")


# ============================================================
# L02 — 图1: 碰撞体类型
# ============================================================
def make_L02_01_collider_types():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "Collider 碰撞体类型", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "碰撞体决定物体的物理边界 —— 不是所有东西都需要精细碰撞", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    cards = [
        ("Box 盒体", 90, "箱子、地板、墙面\n一个矩形就够了", "add_box"),
        ("Sphere 球体", 280, "球类、果实、小件\n圆形的用圆", "add_sphere"),
        ("Capsule 胶囊", 470, "柱子、树干、人形\n两端圆的柱体", "add_capsule"),
        ("Mesh 网格", 660, "复杂地形、雕塑\n最精确也最贵", "add_mesh"),
    ]
    card_w, card_h = 180, 200
    for title, x, desc, kind in cards:
        add_rect(dwg, x, 90, card_w, card_h, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=1.5)
        if kind == "add_box":
            draw_box(dwg, x + 52, 140, 76, 55)
        elif kind == "add_sphere":
            add_ellipse(dwg, x + 90, 165, 42, 38, fill="#2f2f2f", stroke=ACCENT, stroke_width=1.5)
        elif kind == "add_capsule":
            add_rect(dwg, x + 72, 128, 36, 74, fill="#2f2f2f", stroke=ACCENT, stroke_width=1.5)
            add_ellipse(dwg, x + 90, 128, 18, 18, fill="#2f2f2f", stroke=ACCENT, stroke_width=1.5)
            add_ellipse(dwg, x + 90, 202, 18, 18, fill="#2f2f2f", stroke=ACCENT, stroke_width=1.5)
        elif kind == "add_mesh":
            dwg.add(dwg.polygon(points=[(x + 55, 190), (x + 80, 130), (x + 120, 140),
                                        (x + 135, 175), (x + 110, 205), (x + 70, 200)],
                                fill="#2f2f2f", stroke=ACCENT, stroke_width=1.5))
        add_text(dwg, title, x + card_w//2, 238, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 262 + j * 19, fill=TEXT_DIM, size=11, anchor="middle")

    bottom_note(dwg, "实践建议",
                ["地面 / 墙用 Box 就够，别用 Mesh Collider 精细碰每一块石头",
                 "Collider 在游戏里看不见 —— Scene 视图选中物体看绿色线框检查；Mesh Collider 记得勾 Convex"],
                320)
    save_svg_and_png(dwg, "L02_01_collider_types")


# ============================================================
# L02 — 图2: 触发区工作原理
# ============================================================
def make_L02_02_trigger_zone():
    W, H = 900, 540
    dwg = new_svg(W, H)
    add_text(dwg, "Trigger 触发区：看不见的「感应门」", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "不阻挡移动，玩家一进入就发出事件 —— 配合 Udon 实现开关门、触发玩法", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 场景示意
    add_rect(dwg, 80, 330, 740, 10, fill="#2c2c2c", rx=4)
    add_rect(dwg, 420, 170, 260, 150, fill=ACCENT, stroke=ACCENT, rx=12,
             stroke_width=2, opacity=0.10, dash=[8, 5])
    add_text(dwg, "Trigger 区域", 550, 235, fill=ACCENT, size=13, weight="bold", anchor="middle")
    add_text(dwg, "（勾选 Is Trigger）", 550, 262, fill=TEXT_DIM, size=11, anchor="middle")
    add_ellipse(dwg, 250, 250, 24, 24, fill=ACCENT, opacity=0.9)
    add_text(dwg, "玩家", 250, 310, fill=TEXT_DIM, size=11, anchor="middle")
    add_arrow(dwg, 282, 250, 410, 250, stroke=ACCENT, stroke_width=2.5)

    # 流程
    steps = [
        ("1. 进入区域", "玩家走进\nTrigger 范围", ACCENT),
        ("2. 收到事件", "OnTriggerEnter\n被调用", SUCCESS),
        ("3. 发送信号", "SignalSender\n路由给组件", WARM),
        ("4. 执行逻辑", "开门 / 播歌\n开始玩法", "#c084fc"),
    ]
    card_w, card_h = 178, 110
    start_x = (W - (card_w * 4 + 22 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 22)
        add_rect(dwg, cx, 360, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 386, fill="#fff", size=12.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 410 + j * 19, fill=TEXT_DIM, size=11, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 415, cx + card_w + 20, 415, stroke=color, stroke_width=2)

    bottom_note(dwg, "要点",
                ["Trigger 不需要 Collider 参与物理阻挡 —— 玩家是穿过去的，但事件照常触发",
                 "UdonSharp 里写 OnTriggerEnter() 接收事件，再走你项目的 Trigger → SignalSender → Component 架构"],
                500)
    save_svg_and_png(dwg, "L02_02_trigger_zone")


# ============================================================
# L03 — 图1: 打光三件套
# ============================================================
def make_L03_01_light_setup():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "打光三件套：主光 + 补光 + 环境光", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "三层光各管一件事 —— 九成场景靠这三样就能亮起来", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 场景侧视
    add_rect(dwg, 80, 350, 740, 12, fill="#2c2c2c", rx=5)
    # 帐篷剪影
    dwg.add(dwg.polygon(points=[(370, 250), (450, 320), (530, 250)], fill="#3a4a6a", stroke="#4a5a8a", stroke_width=1.5))
    add_rect(dwg, 418, 292, 64, 44, fill="#2c3a58")
    # 树剪影
    add_rect(dwg, 200, 280, 12, 56, fill="#4a3a28")
    add_ellipse(dwg, 206, 260, 30, 32, fill="#2f4a35", stroke="#3a5a42", stroke_width=1.5)
    add_rect(dwg, 640, 280, 12, 56, fill="#4a3a28")
    add_ellipse(dwg, 646, 260, 30, 32, fill="#2f4a35", stroke="#3a5a42", stroke_width=1.5)
    # 太阳（主光）
    add_ellipse(dwg, 680, 130, 30, 30, fill=WARM, opacity=0.9)
    for i in range(8):
        a = i * math.pi / 4
        x1, y1 = 680 + 40 * math.cos(a), 130 + 40 * math.sin(a)
        x2, y2 = 680 + 56 * math.cos(a), 130 + 56 * math.sin(a)
        add_line(dwg, x1, y1, x2, y2, stroke=WARM, stroke_width=2)
    add_line(dwg, 648, 152, 455, 250, stroke=WARM, stroke_width=2, dash=[6, 5], with_arrow=True)
    add_text(dwg, "主光 Directional（平行光，定明暗基调）", 668, 96, fill=WARM, size=11.5, anchor="end")
    # 补光
    add_ellipse(dwg, 140, 340, 40, 40, fill=ACCENT, opacity=0.12)
    add_ellipse(dwg, 140, 340, 10, 10, fill=ACCENT)
    add_text(dwg, "补光 Point", 140, 388, fill=ACCENT, size=11.5, anchor="middle")
    # 环境光标注
    add_text(dwg, "环境光：由天空盒提供，全局底色", 560, 156, fill=TEXT_DIM, size=12, anchor="middle")
    add_line(dwg, 560, 166, 560, 342, stroke=TEXT_DIM, stroke_width=1.2, dash=[4, 4], with_arrow=True)

    # 三张卡
    cards = [
        ("主光 Directional", "像太阳：一个方向打进来\n决定影子与体积感", WARM),
        ("补光 Point", "放在阴影侧：把暗部照亮\n提升可读性", ACCENT),
        ("环境光 Skybox", "天空盒自带的环境照明\n调强度控制全局亮暗", SUCCESS),
    ]
    for i, (title, desc, color) in enumerate(cards):
        x = 60 + i * 270
        add_rect(dwg, x, 410, 250, 95, fill=PANEL, stroke=color, rx=10, stroke_width=1.5)
        add_text(dwg, title, x + 14, 436, fill="#fff", size=13, weight="bold")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + 14, 460 + j * 19, fill=TEXT_DIM, size=11)

    add_text(dwg, "实时光源越少越好 —— 每盏实时灯都是成本（见第 4 篇），能烘焙的走烘焙", W//2, 540, fill=WARN, size=12.5, anchor="middle")
    save_svg_and_png(dwg, "L03_01_light_setup")


# ============================================================
# L03 — 图2: 天空盒与雾
# ============================================================
def make_L03_02_skybox_fog():
    W, H = 900, 470
    dwg = new_svg(W, H)
    add_text(dwg, "天空盒与雾：先定「天」，再定「氛围」", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "天空盒决定白天还是黄昏，雾让远处与天空融合", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 左：天空盒
    add_rect(dwg, 60, 90, 370, 240, fill=PANEL, stroke=BORDER, rx=10)
    add_text(dwg, "天空盒 Skybox", 245, 120, fill="#fff", size=14, weight="bold", anchor="middle")
    sky = linear_grad(dwg, 80, 140, 80, 290,
                      [(0, "#24344e", 1.0), (0.55, "#3d5a80", 1.0), (1, "#8a7a5a", 1.0)])
    add_rect(dwg, 80, 140, 330, 130, fill=sky, rx=6)
    add_ellipse(dwg, 330, 175, 22, 22, fill=WARN, opacity=0.9)
    add_text(dwg, "Window → Rendering → Lighting → Environment", 245, 290, fill=TEXT_DIM, size=11.5, anchor="middle")
    add_text(dwg, "指定 Skybox Material（白天 / 黄昏 / 星空）", 245, 312, fill=TEXT_MUTED, size=11, anchor="middle")

    # 右：雾
    add_rect(dwg, 470, 90, 370, 270, fill=PANEL, stroke=BORDER, rx=10)
    add_text(dwg, "雾 Fog", 655, 120, fill="#fff", size=14, weight="bold", anchor="middle")
    add_rect(dwg, 490, 278, 330, 10, fill="#3d4a5a", rx=3)
    add_rect(dwg, 730, 232, 60, 46, fill=SUCCESS, opacity=0.3, rx=4)
    add_rect(dwg, 660, 217, 70, 61, fill=SUCCESS, opacity=0.55, rx=4)
    add_rect(dwg, 585, 202, 80, 76, fill=SUCCESS, opacity=0.85, rx=4)
    add_text(dwg, "近处清晰，远处融入天空", 655, 318, fill=TEXT_DIM, size=11.5, anchor="middle")
    add_text(dwg, "Lighting → Fog：勾选后调 Density（越大越浓）", 655, 342, fill=TEXT_MUTED, size=11, anchor="middle")

    bottom_note(dwg, "搭配建议",
                ["白天世界：浅蓝天空盒 + 很轻的雾；黄昏世界：暖色天空盒 + 浓一点的雾，氛围立刻不同",
                 "雾还能掩盖远处物体「突然出现」的加载痕迹 —— 视线尽头记得放个雾墙"], 375)
    save_svg_and_png(dwg, "L03_02_skybox_fog")


# ============================================================
# L04 — 图1: 合批原理
# ============================================================
def make_L04_01_batching():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "合批 Batching：把多次绘制合并成一次", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "Draw Call = CPU 通知 GPU 画一次的命令 —— 命令越少越流畅", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 左：不同材质
    add_text(dwg, "三个不同材质", 245, 105, fill="#ff8888", size=14, weight="bold", anchor="middle")
    draw_box(dwg, 110, 135, 70, 50, top="#7a4a4a", front="#8a5a5a", side="#6a4242", stroke="#a06a6a")
    draw_box(dwg, 215, 135, 70, 50, top="#4a6a7a", front="#5a7a8a", side="#42586a", stroke="#6a8a9a")
    draw_box(dwg, 320, 135, 70, 50, top="#6a6a4a", front="#7a7a5a", side="#5a5a42", stroke="#8a8a6a")
    add_rect(dwg, 60, 210, 370, 46, fill="#1a1a1a", stroke="#ff8888", rx=8)
    add_text(dwg, "GPU 收到 3 次绘制指令", 245, 238, fill="#ff8888", size=12.5, weight="bold", anchor="middle")

    # 右：共享材质
    add_text(dwg, "三个共享同一材质", 655, 105, fill=SUCCESS, size=14, weight="bold", anchor="middle")
    draw_box(dwg, 520, 135, 70, 50, top="#4a6a7a", front="#5a7a8a", side="#42586a", stroke="#6a8a9a")
    draw_box(dwg, 625, 135, 70, 50, top="#4a6a7a", front="#5a7a8a", side="#42586a", stroke="#6a8a9a")
    draw_box(dwg, 730, 135, 70, 50, top="#4a6a7a", front="#5a7a8a", side="#42586a", stroke="#6a8a9a")
    add_rect(dwg, 470, 210, 370, 46, fill="#1a1a1a", stroke=SUCCESS, rx=8)
    add_text(dwg, "GPU 收到 1 次绘制指令", 655, 238, fill=SUCCESS, size=12.5, weight="bold", anchor="middle")

    add_arrow(dwg, 440, 175, 462, 175, stroke=TEXT_MUTED, stroke_width=2.5)

    bottom_note(dwg, "合批的前提：材质完全相同",
                ["同一材质 = 同一个着色器 + 同一张贴图 + 同一组参数，连颜色都不能差",
                 "VRChat 里：减少材质种类、共用贴图图集，是省 Draw Call 最有效的手段"], 285)
    save_svg_and_png(dwg, "L04_01_batching")


# ============================================================
# L04 — 图2: 性能预算表
# ============================================================
def make_L04_02_perf_budget():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "VRChat 世界性能预算（参考值）", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "目标是评级 Good 以上 —— 数值随 SDK 版本会变，以 Unity 里性能检查器为准", W//2, 62, fill=TEXT_DIM, size=12.5, anchor="middle")

    col_x = [60, 245, 410]
    col_w = [170, 150, 380]
    heads = ["项目", "参考预算", "说明"]
    for i, hd in enumerate(heads):
        add_rect(dwg, col_x[i], 78, col_w[i], 34, fill=PANEL, stroke=ACCENT, stroke_width=1.5)
        add_text(dwg, hd, col_x[i] + col_w[i]//2, 100, fill=ACCENT, size=13, weight="bold", anchor="middle")

    rows = [
        ("共享材质数", "≤ 30", "同类物体用同一材质，越多越难合批", WARN),
        ("实时光源", "≤ 1 盏", "其余灯光全部走烘焙，实时灯每盏都贵", WARN),
        ("同时播放的粒子", "≤ 2 套", "循环粒子用完就停，别让它们挂满场景", WARN),
        ("单张纹理尺寸", "≤ 1024", "远景 512 就够；2048 以上几乎必踩坑", WARN),
        ("多边形总数", "≤ 10 万", "靠 LOD 和遮挡剔除控制（见本篇第 4 章）", WARN),
        ("Udon 行为数量", "≤ 16 个", "逻辑集中到管理器，别在满场景挂脚本", WARN),
    ]
    for i, (item, budget, note, color) in enumerate(rows):
        y = 112 + i * 58
        add_rect(dwg, col_x[0], y, col_w[0], 48, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, item, col_x[0] + col_w[0]//2, y + 29, fill="#fff", size=12, weight="bold", anchor="middle")
        add_rect(dwg, col_x[1], y, col_w[1], 48, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, budget, col_x[1] + col_w[1]//2, y + 29, fill=color, size=12, weight="bold", anchor="middle")
        add_rect(dwg, col_x[2], y, col_w[2], 48, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, note, col_x[2] + 12, y + 29, fill=TEXT_DIM, size=11)

    bottom_note(dwg, "怎么看预算？",
                ["Build 世界时 VRChat SDK 会自动评级（Poor → Excellent），红了就说明超了",
                 "完整优化方法见《渲染教程》第 4 篇 —— 本篇先把「数清 + 减量」做到位"], 470)
    save_svg_and_png(dwg, "L04_02_perf_budget")


# ============================================================
# L05 — 图1: 实战五步
# ============================================================
def make_L05_01_steps():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "实战：搭一个小露营场景", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "五步走完，一个能逛、能聚会、性能合格的场景就出来了", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 白盒", "Cube 搭骨架\n定大小和位置", ACCENT),
        ("2. 地面材质", "地面+天空定色调\n先铺大色块", SUCCESS),
        ("3. 灯光天空", "打光三件套\n白天/黄昏二选一", WARM),
        ("4. 摆放道具", "树、帐篷、桌椅\n统一材质风格", "#c084fc"),
        ("5. 烘焙+检查", "烘焙光照\n查 Draw Call 数", "#ff9e4e"),
    ]
    card_w, card_h = 156, 200
    start_x = (W - (card_w * 5 + 14 * 4)) // 2
    for i, (title, desc, color) in enumerate(steps):
        x = start_x + i * (card_w + 14)
        add_rect(dwg, x, 90, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 118, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 146 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")
        if i < 4:
            add_arrow(dwg, x + card_w + 2, 190, x + card_w + 12, 190, stroke=color, stroke_width=2)

    bottom_note(dwg, "每步都检查",
                ["白盒阶段反复 Play 试走动线；之后每一步「只改一个变量」，出问题立刻知道是谁",
                 "第 5 步达标标准：性能评级 Good 以上、无碰撞穿透、视觉完成度 80%"], 320)
    save_svg_and_png(dwg, "L05_01_steps")


# ============================================================
# L05 — 图2: 露营场景完成示意（俯视）
# ============================================================
def make_L05_02_result():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "露营场景完成示意（俯视）", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "入口 → 篝火聚集点 → 营地各处 —— 动线 + 聚集点 + 氛围灯光的综合成品", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    add_rect(dwg, 80, 90, 740, 290, fill="#2a2a2a", stroke=BORDER, rx=14)

    # 入口路径
    add_ellipse(dwg, 300, 372, 12, 12, fill=ACCENT, opacity=0.7)
    add_line(dwg, 312, 368, 423, 304, stroke=WARM, stroke_width=2.5, dash=[8, 6], with_arrow=True)
    add_text(dwg, "入口", 300, 396, fill=WARM, size=11.5, anchor="middle")

    # 篝火（中心聚集点）
    add_ellipse(dwg, 450, 240, 62, 62, fill=WARM, opacity=0.10)
    add_ellipse(dwg, 450, 240, 34, 34, fill="#3a2f22", stroke="#5a4a30", stroke_width=1.5)
    add_ellipse(dwg, 450, 240, 16, 16, fill=WARM, opacity=0.9)
    add_ellipse(dwg, 444, 236, 6, 6, fill="#ffcc66")
    add_text(dwg, "篝火 = 聚集点", 522, 250, fill=WARM, size=11.5, anchor="start")

    # 帐篷
    dwg.add(dwg.polygon(points=[(140, 205), (195, 165), (250, 205)], fill="#4a5a8a", stroke="#5a6a9a", stroke_width=1.5))
    add_rect(dwg, 155, 205, 80, 55, fill="#3a4a7a", rx=4)
    add_rect(dwg, 185, 230, 20, 30, fill="#26304e")
    add_text(dwg, "帐篷（休息/换装）", 195, 280, fill=TEXT_DIM, size=11, anchor="middle")

    # 树（围合）
    add_ellipse(dwg, 110, 140, 26, 26, fill=SUCCESS, opacity=0.85)
    add_rect(dwg, 105, 156, 10, 16, fill="#4a3a28")
    add_ellipse(dwg, 720, 130, 30, 30, fill=SUCCESS, opacity=0.75)
    add_rect(dwg, 715, 148, 10, 18, fill="#4a3a28")
    add_ellipse(dwg, 690, 330, 24, 24, fill=SUCCESS, opacity=0.8)
    add_rect(dwg, 686, 344, 8, 14, fill="#4a3a28")
    add_text(dwg, "树 = 围合视野", 720, 200, fill=TEXT_DIM, size=11, anchor="middle")

    # 桌子
    add_rect(dwg, 580, 275, 90, 34, fill="#6a5a40", stroke="#7a6a4a", rx=6)
    add_text(dwg, "桌椅", 625, 295, fill="#ddd", size=10.5, anchor="middle")
    add_text(dwg, "桌椅 = 交谈点", 560, 350, fill=TEXT_DIM, size=11, anchor="middle")

    # 火把
    add_ellipse(dwg, 330, 150, 26, 26, fill=WARM, opacity=0.12)
    add_ellipse(dwg, 330, 150, 8, 8, fill=WARM)
    add_text(dwg, "火把", 330, 180, fill=TEXT_DIM, size=11, anchor="middle")
    add_ellipse(dwg, 560, 140, 26, 26, fill=WARM, opacity=0.12)
    add_ellipse(dwg, 560, 140, 8, 8, fill=WARM)

    # 图例
    add_rect(dwg, 60, 408, 780, 70, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "设计要点：入口路径直指篝火（玩家一进门就被引导到聚集点）；树围出边界不让视线一眼看穿；火把连线形成光的引导", 450, 439, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "地面统一共享材质、光源全烘焙 —— 性能合格的前提下，氛围照样到位", 450, 463, fill=WARN, size=12, anchor="middle")
    save_svg_and_png(dwg, "L05_02_result")


# ============================================================
# L06 — 图1: 术语速查
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "场景搭建术语速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    terms = [
        ("白盒 Blockout", "用 Cube 搭骨架，先验证布局再上美术", ACCENT),
        ("动线 Player Flow", "玩家从哪来、看到什么、去哪的路线", ACCENT),
        ("Collider 碰撞体", "决定物体物理边界的形状", ACCENT),
        ("Trigger 触发区", "不阻挡移动、只发事件的感应区", ACCENT),
        ("Layer 碰撞层", "控制哪些层之间互相碰撞", ACCENT),
        ("天空盒 Skybox", "无限远背景 + 环境光的来源", SUCCESS),
        ("Fog 雾", "远处与天空融合，营造氛围", SUCCESS),
        ("后处理", "色彩分级 / 泛光 / 景深等画面效果", SUCCESS),
        ("烘焙", "预计算光影，存进光照贴图", SUCCESS),
        ("LOD", "远处自动切换低模，省性能", WARM),
        ("合批 Batching", "共享材质合并绘制，省 Draw Call", WARM),
        ("遮挡剔除", "相机看不到的物体不绘制", WARM),
    ]
    col_w = 390
    for i, (term, desc, color) in enumerate(terms):
        row, col = divmod(i, 2)
        x = 60 + col * (col_w + 30)
        y = 70 + row * 76
        add_rect(dwg, x, y, col_w, 60, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        add_text(dwg, term, x + 16, y + 24, fill="#fff", size=13, weight="bold")
        add_text(dwg, desc, x + 16, y + 46, fill=TEXT_DIM, size=11)

    add_text(dwg, "每个术语的展开讲解都在本篇对应章节，忘记时回来翻", W//2, 536, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_01_cheatsheet")


# ============================================================
# L06 — 图2: 常见问题对照表
# ============================================================
def make_L06_02_common_issues():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "常见问题对照表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    rows = [
        ("掉帧卡顿", "材质太多 / 实时灯太多\n循环粒子泛滥", "共享材质 + 烘焙灯光\n关闭闲置粒子，评级 Good", "#ff8888"),
        ("碰撞穿透", "Collider 比模型小\n薄墙用了 Mesh Collider", "调大 Collider\n薄墙用 Box，检查 Layer 矩阵", WARN),
        ("场景太暗", "环境光太弱\n天空盒太暗", "补齐打光三件套\n调高环境光强度", WARN),
        ("画面过曝", "主光太强\n泛光阈值太低", "降低主光强度\n后处理里调 Bloom 阈值", ACCENT),
        ("烘焙太慢", "烘焙范围太大\n分辨率太高", "缩小范围、降分辨率\n分区域烘焙", SUCCESS),
        ("地面塌陷", "地面没有 Collider\n地形未生成碰撞", "确认地面有 Collider\n用简化碰撞网格", SUCCESS),
    ]
    col_w = [180, 290, 300]
    xs = [60, 255, 560]
    for hd, x in zip(["问题现象", "常见原因", "解决办法"], xs):
        add_rect(dwg, x, 70, col_w[0], 34, fill=PANEL, stroke=ACCENT, stroke_width=1.5)
        add_text(dwg, hd, x + col_w[0]//2, 92, fill=ACCENT, size=13, weight="bold", anchor="middle")
    for i, (prob, cause, sol, color) in enumerate(rows):
        y = 104 + i * 70
        add_rect(dwg, 60, y, col_w[0], 60, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, prob, 60 + col_w[0]//2, y + 25, fill="#fff", size=12, weight="bold", anchor="middle")
        add_rect(dwg, 255, y, col_w[1], 60, fill=PANEL, stroke=BORDER, rx=6)
        for j, line in enumerate(cause.split("\n")):
            add_text(dwg, line, 255 + col_w[1]//2, y + 25 + j * 17, fill=TEXT_DIM, size=11, anchor="middle")
        add_rect(dwg, 560, y, col_w[2], 60, fill=PANEL, stroke=SUCCESS, rx=6)
        for j, line in enumerate(sol.split("\n")):
            add_text(dwg, line, 560 + col_w[2]//2, y + 25 + j * 17, fill=SUCCESS, size=11, anchor="middle")

    add_text(dwg, "调试心法：先看性能评级和 Scene 视图线框，再动手改 —— 八成问题一眼就能定位", W//2, 534, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_02_common_issues")


# ============================================================
# L06 — 图3: 进阶路线图
# ============================================================
def make_L06_03_roadmap():
    W, H = 900, 470
    dwg = new_svg(W, H)
    add_text(dwg, "进阶路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    stages = [
        ("入门 · 会搭场景", "白盒 → 美术化\n动线清晰、能逛能聚会", ACCENT, "现在"),
        ("熟练 · 会做氛围", "灯光 / 雾 / 后处理\n性能评级 Good", SUCCESS, "1 周"),
        ("进阶 · 会做世界", "社交空间 / 玩法区域\nUdon 交互挂上去", WARM, "1 个月"),
        ("精通 · 会做设计", "关卡结构 / 性能优化\n评级到 Excellent", "#c084fc", "长期"),
    ]
    box_w, box_h = 180, 150
    start_x = (W - (box_w * 4 + 30 * 3)) // 2
    for i, (title, desc, color, time) in enumerate(stages):
        x = start_x + i * (box_w + 30)
        y = 90
        add_rect(dwg, x, y, box_w, box_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, y + 30, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + box_w//2, y + 60 + j * 19, fill=TEXT_DIM, size=11, anchor="middle")
        add_text(dwg, f"⏱ {time}", x + box_w//2, y + box_h - 14, fill=color, size=11, anchor="middle")
        if i < 3:
            add_arrow(dwg, x + box_w + 2, y + box_h//2, x + box_w + 28, y + box_h//2, stroke=color, stroke_width=2)

    bottom_note(dwg, "学习建议",
                ["① 每个场景先白盒再美术，布局满意前别急着换模型  ② 每做完一步按一次 Play",
                 "③ 进别人的世界，先分析它的动线与打光  ④ 性能从第一天就盯着，别等最后返工"], 280)
    save_svg_and_png(dwg, "L06_03_roadmap")


if __name__ == "__main__":
    for f in [make_L01_01_blockout, make_L01_02_player_flow,
              make_L02_01_collider_types, make_L02_02_trigger_zone,
              make_L03_01_light_setup, make_L03_02_skybox_fog,
              make_L04_01_batching, make_L04_02_perf_budget,
              make_L05_01_steps, make_L05_02_result,
              make_L06_01_cheatsheet, make_L06_02_common_issues, make_L06_03_roadmap]:
        print(f"生成 {f.__name__} ...")
        f()
    print("全部完成")
