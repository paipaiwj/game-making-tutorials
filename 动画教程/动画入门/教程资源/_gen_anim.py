# -*- coding: utf-8 -*-
# Unity 动画入门教程（面向 VRChat）— 配图生成脚本
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _render_svg import *


# ============================================================
# L01 — 图1: 动画三层结构
# ============================================================
def make_L01_01_animation_layers():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "游戏动画的三层结构", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "剪辑存动作  →  控制器管规则  →  参数做开关", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    layers = [
        ("① Animation Clip 剪辑", "存一段动作：旋转、位移、颜色\n例：门从 0° 转到 90°\n就像一个录像片段", ACCENT),
        ("② Animator Controller 状态机", "管理何时播放哪段剪辑\n例：doorOpen=true 时\n播放「开门」", SUCCESS),
        ("③ 参数 Parameters", "连接逻辑与动画的开关\nFloat / Bool / Trigger\n供 Udon 设置", WARM),
    ]
    card_w, card_h = 240, 180
    start_x = (W - (card_w * 3 + 40 * 2)) // 2
    for i, (title, desc, color) in enumerate(layers):
        x = start_x + i * (card_w + 40)
        add_rect(dwg, x, 100, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 130, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 158 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")
        if i < 2:
            add_arrow(dwg, x + card_w + 6, 190, x + card_w + 34, 190, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 320, 700, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "一句话理解", 130, 350, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "剪辑 = 动作内容 ｜ 控制器 = 播放规则 ｜ 参数 = 外部开关", 130, 378, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "VRChat 世界里：门、按钮、传送带、NPC 都是这个套路", 130, 400, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L01_01_animation_layers")


# ============================================================
# L01 — 图2: Animator 组件字段
# ============================================================
def make_L01_02_animator_component():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "Animator 组件：把控制器挂到物体上", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    add_rect(dwg, 60, 80, 360, 310, fill=PANEL, stroke=BORDER, rx=10)
    add_text(dwg, "Animator 组件（Inspector）", 90, 110, fill="#fff", size=14, weight="bold")
    fields = [
        ("Controller", "门_Controller", ACCENT),
        ("Avatar", "None（世界物件不需要）", TEXT_DIM),
        ("Apply Root Motion", "关", TEXT_DIM),
        ("Update Mode", "Normal", TEXT_DIM),
        ("Culling Mode", "Always Animate", TEXT_DIM),
    ]
    for i, (name, val, color) in enumerate(fields):
        y = 130 + i * 50
        add_rect(dwg, 85, y, 310, 38, fill="#1a1a1a", stroke=BORDER, rx=6)
        add_text(dwg, name, 100, y + 25, fill=color, size=12, weight="bold")
        add_text(dwg, val, 330, y + 25, fill=TEXT, size=12, anchor="end")

    notes = [
        ("Controller", "唯一必填项：选择你做好的状态机 Asset", ACCENT),
        ("Avatar", "只有角色动画才需要；世界物件不填", SUCCESS),
        ("Apply Root Motion", "角色的根运动，与物件动画无关", WARM),
        ("Culling Mode", "离开视野也在动（持续播放）", SUCCESS),
    ]
    for i, (name, desc, color) in enumerate(notes):
        y = 80 + i * 76
        add_rect(dwg, 460, y, 380, 64, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        add_text(dwg, name, 480, y + 24, fill="#fff", size=12.5, weight="bold")
        add_text(dwg, desc, 480, y + 46, fill=TEXT_DIM, size=11)

    add_text(dwg, "一个物体挂一个 Animator；动画对象 = Animator + Controller + 剪辑", W//2, 440, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L01_02_animator_component")


# ============================================================
# L02 — 图1: 状态机示意图
# ============================================================
def make_L02_01_state_machine():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "状态机：状态 + 转换 + 参数", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "物体一直处于某个状态；转换决定什么时候切到另一个状态", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    nodes = [
        ("Idle", "门关着\n（待机）", (150, 190), ACCENT),
        ("Open", "门开着\n（保持开启）", (450, 190), SUCCESS),
        ("Close", "关门过程\n（过渡动画）", (750, 190), WARM),
    ]
    for title, desc, (cx, cy), color in nodes:
        add_rect(dwg, cx - 90, cy - 50, 180, 100, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx, cy + 2, fill="#fff", size=14, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx, cy + 26 + j * 18, fill=TEXT_DIM, size=10.5, anchor="middle")
    # 转换
    add_line(dwg, 245, 190, 352, 190, stroke=ACCENT, stroke_width=2, with_arrow=True)
    add_text(dwg, "doorOpen = true", 298, 176, fill=ACCENT, size=10.5, anchor="middle")
    add_line(dwg, 545, 190, 652, 190, stroke=SUCCESS, stroke_width=2, with_arrow=True)
    add_text(dwg, "doorOpen = false", 598, 176, fill=SUCCESS, size=10.5, anchor="middle")
    add_line(dwg, 660, 255, 240, 258, stroke=WARM, stroke_width=2, dash=[6, 4], with_arrow=True)
    add_text(dwg, "也可以把「开门/关门」做成过渡动画，\n写在转换上，切换时自动播放", 660, 288, fill=WARN, size=10.5, anchor="middle")

    add_rect(dwg, 60, 330, 780, 110, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "读法：Idle →（doorOpen=true）→ Open →（doorOpen=false）→ Idle，循环开关", 90, 360, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "Close 是可选状态：把关门做成过渡动画，也可以直接播放后回到 Idle", 90, 386, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "状态机永远只有「一个当前状态」—— 想改表现，就切换状态", 90, 412, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L02_01_state_machine")


# ============================================================
# L02 — 图2: 三种参数
# ============================================================
def make_L02_02_parameters():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "三种参数：动画与代码之间的开关", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    params = [
        ("Float 浮点", "带小数的数字\n风速、速度、进度\n如传送带速度 1.5", ACCENT,
         'SetFloat("speed", 1.5f)'),
        ("Bool 布尔", "真假开关\n门开没开、灯亮没亮\n只有 true / false", SUCCESS,
         'SetBool("doorOpen", true)'),
        ("Trigger 触发", "一次性信号\n拉一下、按一下\n自动归位，不占状态", WARM,
         'SetTrigger("pull")'),
    ]
    card_w, card_h = 240, 220
    start_x = (W - (card_w * 3 + 40 * 2)) // 2
    for i, (title, desc, color, code) in enumerate(params):
        x = start_x + i * (card_w + 40)
        add_rect(dwg, x, 90, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 120, fill="#fff", size=14, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 148 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")
        add_rect(dwg, x + 15, 225, card_w - 30, 62, fill="#1a1a1a", stroke=BORDER, rx=6)
        add_text(dwg, code, x + card_w//2, 262, fill="#9ecbff", size=11.5, anchor="middle")

    add_rect(dwg, 100, 340, 700, 80, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "选型建议：开关用 Bool，一次性动作用 Trigger，连续数值用 Float", 130, 370, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "参数名要记牢 —— 代码写错名字，动画就不会动（见常见坑）", 130, 396, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L02_02_parameters")


# ============================================================
# L02 — 图3: Any State 与 Exit
# ============================================================
def make_L02_03_any_state():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "两个特殊节点：Any State 与 Exit", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    add_rect(dwg, 60, 90, 320, 240, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    add_text(dwg, "Any State（任意状态）", 90, 120, fill="#fff", size=13.5, weight="bold")
    add_text(dwg, "从任意状态都能切走", 90, 150, fill=TEXT_DIM, size=11.5)
    states = ["Idle", "Open", "Close"]
    for i, s in enumerate(states):
        add_rect(dwg, 90, 168 + i * 36, 100, 30, fill="#1a1a1a", stroke=BORDER, rx=6)
        add_text(dwg, s, 140, 188 + i * 36, fill=TEXT_DIM, size=11, anchor="middle")
        add_arrow(dwg, 198, 183 + i * 36, 240, 183 + i * 36, stroke=ACCENT, stroke_width=1.8)
    add_rect(dwg, 248, 183, 110, 60, fill="#1a1a1a", stroke=ACCENT, rx=6)
    add_text(dwg, "重置状态", 303, 205, fill="#fff", size=11.5, weight="bold", anchor="middle")
    add_text(dwg, "条件满足即切换", 303, 227, fill=TEXT_DIM, size=10, anchor="middle")
    add_text(dwg, "用途：紧急动画（重置回位）", 90, 294, fill=TEXT_DIM, size=10.5)
    add_text(dwg, "不管在哪，一触发就切过去", 90, 312, fill=TEXT_DIM, size=10.5)

    add_rect(dwg, 440, 90, 400, 270, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=2)
    add_text(dwg, "Exit（退出）", 470, 120, fill="#fff", size=13.5, weight="bold")
    add_text(dwg, "播放完就退出状态机，不再播动画", 470, 150, fill=TEXT_DIM, size=11.5)
    add_rect(dwg, 470, 175, 130, 45, fill="#1a1a1a", stroke=SUCCESS, rx=6)
    add_text(dwg, "开场动画", 535, 202, fill="#fff", size=11.5, weight="bold", anchor="middle")
    add_arrow(dwg, 608, 197, 688, 197, stroke=SUCCESS, stroke_width=1.8)
    add_rect(dwg, 696, 180, 60, 60, fill="#1a1a1a", stroke="#ff88cc", rx=6)
    add_text(dwg, "Exit", 726, 201, fill="#ff88cc", size=12, weight="bold", anchor="middle")
    add_text(dwg, "播放结束", 726, 222, fill=TEXT_DIM, size=10.5, anchor="middle")
    add_text(dwg, "VRChat 场景里一般不退出，\n物体保持动画状态，\n新手先用好普通状态", 470, 280, fill=WARN, size=10.5)

    add_rect(dwg, 100, 370, 700, 50, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "先学会普通状态 + 转换，再碰 Any State；Exit 用到再说", 450, 399, fill=SUCCESS, size=12.5, anchor="middle")
    save_svg_and_png(dwg, "L02_03_any_state")


# ============================================================
# L03 — 图1: 录制动画流程
# ============================================================
def make_L03_01_record_animation():
    W, H = 900, 470
    dwg = new_svg(W, H)
    add_text(dwg, "录制动画：Animation 窗口四步", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "先做好模型 → 选中它 → Create → Animation 开始录制", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 创建剪辑", "选中门模型\nCreate → Animation\n命名为「开门」", ACCENT),
        ("2. 打开窗口", "Window → Animation\n（快捷键 Ctrl+6）\n选中物体后编辑", SUCCESS),
        ("3. 按录制", "点红色 ● 录制\n时间轴停在 0 秒\n先记一个初始关键帧", WARM),
        ("4. 改属性", "拖时间轴到结束点\n改旋转/位移/颜色\n自动记录关键帧", "#c084fc"),
    ]
    card_w, card_h = 190, 170
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 26)
        cy = 100
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 128, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 156 + j * 20, fill=TEXT_DIM, size=10.5, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 185, cx + card_w + 24, 185, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 310, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "录制时：改属性 = 自动加关键帧（时间轴上出现橙色菱形）", 130, 340, fill=SUCCESS, size=13, weight="bold")
    add_text(dwg, "记得 0 秒先录一个「初始值」，否则播放会跳变", 130, 366, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "录制完成：再点一次红色 ● 退出录制模式", 130, 390, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L03_01_record_animation")


# ============================================================
# L03 — 图2: 关键帧时间轴
# ============================================================
def make_L03_02_keyframe_timeline():
    W, H = 900, 470
    dwg = new_svg(W, H)
    add_text(dwg, "关键帧与时间轴：中间的部分自动补", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "你只管定「关键的点」，两点之间 Unity 自动插值（补间）", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 时间轴
    add_rect(dwg, 70, 105, 760, 60, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_line(dwg, 150, 135, 750, 135, stroke="#555", stroke_width=2)
    for i, t in enumerate([0.0, 0.5, 1.0, 1.5, 2.0]):
        x = 150 + i * 150
        add_line(dwg, x, 130, x, 140, stroke="#777", stroke_width=2)
        add_text(dwg, f"{t:g}s", x, 120, fill=TEXT_DIM, size=11, anchor="middle")
    # 关键帧菱形
    keys = [
        (150, "0° 门关着", ACCENT),
        (300, "45° 半开", WARM),
        (450, "90° 全开", SUCCESS),
        (600, "90° 停住", SUCCESS),
        (750, "0° 门关上", WARM),
    ]
    for x, label, color in keys:
        add_rect(dwg, x - 6, 131, 12, 8, fill=color, rx=2)
        add_text(dwg, label, x, 175, fill=TEXT_DIM, size=11, anchor="middle")

    # 曲线面板
    add_rect(dwg, 70, 205, 360, 170, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "曲线面板（Curves）", 100, 232, fill="#fff", size=12.5, weight="bold")
    add_line(dwg, 100, 260, 400, 260, stroke="#555", stroke_width=1.5)
    add_line(dwg, 120, 240, 120, 340, stroke="#555", stroke_width=1.5)
    add_line(dwg, 120, 340, 300, 260, stroke=ACCENT, stroke_width=2)
    add_text(dwg, "直线 = 匀速", 200, 285, fill=TEXT_DIM, size=11, anchor="middle")
    add_ellipse(dwg, 300, 260, 5, 5, fill=ACCENT)
    add_text(dwg, "关键帧1 → 关键帧2", 200, 318, fill=TEXT_DIM, size=10.5, anchor="middle")

    add_rect(dwg, 460, 205, 380, 170, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "调曲线让动作更好看", 490, 232, fill="#fff", size=12.5, weight="bold")
    add_line(dwg, 490, 260, 790, 260, stroke="#555", stroke_width=1.5)
    add_line(dwg, 500, 240, 500, 340, stroke="#555", stroke_width=1.5)
    add_line(dwg, 500, 340, 580, 300, stroke=WARM, stroke_width=2)
    add_line(dwg, 580, 300, 660, 280, stroke=WARM, stroke_width=2)
    add_line(dwg, 660, 280, 760, 262, stroke=WARM, stroke_width=2)
    add_ellipse(dwg, 580, 300, 5, 5, fill=WARM)
    add_ellipse(dwg, 660, 280, 5, 5, fill=WARM)
    add_text(dwg, "曲线越陡 = 动得越快", 650, 318, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "开头缓、结尾缓 = 更自然", 650, 340, fill=WARN, size=11, anchor="middle")

    add_text(dwg, "只录关键点（0° → 45° → 90°），中间的过程 Unity 自动补", W//2, 425, fill=SUCCESS, size=12.5, anchor="middle")
    add_text(dwg, "修改方法：选中菱形关键帧 → 直接改属性，或拖动微调时间", W//2, 448, fill=TEXT_MUTED, size=11.5, anchor="middle")
    save_svg_and_png(dwg, "L03_02_keyframe_timeline")


# ============================================================
# L04 — 图1: 交互触发动画流程
# ============================================================
def make_L04_01_interact_flow():
    W, H = 900, 470
    dwg = new_svg(W, H)
    add_text(dwg, "交互触发动画：玩家的手 → 动画", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    steps = [
        ("玩家交互", "按按钮 / 碰门\nVRC_Interactable\n触发 Interact 事件", ACCENT),
        ("Udon 脚本", "收到事件\n调 SetBool 改参数\ndoorOpen = true", SUCCESS),
        ("Animator 参数", "doorOpen 变成 true\n状态机感知到变化", WARM),
        ("状态机切换", "Open 转换条件满足\n播放「开门」剪辑", "#c084fc"),
    ]
    card_w, card_h = 190, 160
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 26)
        cy = 90
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 118, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 146 + j * 20, fill=TEXT_DIM, size=10.5, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 170, cx + card_w + 24, 170, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 290, 700, 110, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "核心代码（Udon 里只需这一句）", 130, 320, fill=SUCCESS, size=13, weight="bold")
    add_text(dwg, 'animator.SetBool("doorOpen", !doorOpen);   // 开→关、关→开', 130, 348, fill="#9ecbff", size=12.5)
    add_text(dwg, "Udon 不改动画本身，只改参数 —— 播什么、怎么播，全交给状态机", 130, 374, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L04_01_interact_flow")


# ============================================================
# L04 — 图2: 常见坑
# ============================================================
def make_L04_02_pitfalls():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "常见坑：动画不动？先查这四件事", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    items = [
        ("动画被 Udon 覆盖", "Udon 每帧改 Transform\n和动画抢同一属性\n动画自然「动不起来」", WARM),
        ("Apply Root Motion", "那是角色的根运动\n世界物件动画无关\n保持默认「关」即可", ACCENT),
        ("Animator 权重/层", "多层动画按权重混合\n层权重=0 就不播\n新手只用 Layer 0", "#c084fc"),
        ("参数名写错", "SetBool 名字和 Animator\n面板对不上 = 无效\n永远先核对拼写", SUCCESS),
    ]
    card_w, card_h = 190, 170
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(items):
        cx = start_x + i * (card_w + 26)
        cy = 90
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 118, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 146 + j * 20, fill=TEXT_DIM, size=10.5, anchor="middle")

    add_rect(dwg, 100, 300, 700, 130, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "排查顺序（按概率从高到低）", 130, 330, fill=SUCCESS, size=13, weight="bold")
    add_text(dwg, "① 参数名对不对    ② 属性有没有被 Udon 抢    ③ 状态机转换方向对吗", 130, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "④ 物体有没有挂 Animator    ⑤ 控制器 Asset 有没有选对", 130, 382, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "金科玉律：一个属性只让一个东西控制（动画 or 代码，二选一）", 130, 408, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L04_02_pitfalls")


# ============================================================
# L05 — 图1: 实战五步
# ============================================================
def make_L05_01_steps():
    W, H = 900, 470
    dwg = new_svg(W, H)
    add_text(dwg, "实战：做一个「开关门」", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "目标：玩家碰按钮 → 门开，再碰 → 门关", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 录关门动画", "门从 90° 转到 0°\n（录制 1 秒）", ACCENT),
        ("2. 录开门动画", "门从 0° 转到 90°\n（录制 1 秒）", SUCCESS),
        ("3. 搭状态机", "两个状态：Idle/Open\n两条转换 + doorOpen 参数", WARM),
        ("4. 写 Udon", "DoorToggleComponent\nInteract 时 SetBool 取反", "#c084fc"),
        ("5. 场景连线", "按钮 → Udon 脚本\nAnimator 挂门模型上", "#ff9e4e"),
    ]
    card_w, card_h = 156, 180
    start_x = (W - (card_w * 5 + 14 * 4)) // 2
    for i, (title, desc, color) in enumerate(steps):
        x = start_x + i * (card_w + 14)
        add_rect(dwg, x, 90, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 118, fill="#fff", size=12.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 146 + j * 20, fill=TEXT_DIM, size=10.5, anchor="middle")
        if i < 4:
            add_arrow(dwg, x + card_w + 2, 180, x + card_w + 12, 180, stroke=color, stroke_width=2)

    add_rect(dwg, 100, 310, 700, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "验收标准：门打开 → 再碰 → 门关上 → 再碰 → 门打开……循环不断", 130, 340, fill=SUCCESS, size=13, weight="bold")
    add_text(dwg, "全程不需要改任何代码：开关逻辑 = 状态机 + 一个 SetBool", 130, 366, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "先做到「能动」，再去加音效、粒子、按钮动画", 130, 390, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L05_01_steps")


# ============================================================
# L05 — 图2: 门的完整结构
# ============================================================
def make_L05_02_result():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "开关门的完整结构", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    add_text(dwg, "场景里的物件", 120, 80, fill=TEXT, size=14, weight="bold")
    comps = [
        ("门模型 Door", "带 Animator 组件\nController = 门_Controller", ACCENT),
        ("两个动画剪辑", "开门.anim / 关门.anim\n各 1 秒的旋转动画", SUCCESS),
        ("状态机 Controller", "Idle / Open 两状态\ndoorOpen Bool 参数", WARM),
        ("Udon 组件", "DoorToggleComponent\n持有 Animator 引用", "#c084fc"),
    ]
    for i, (name, desc, color) in enumerate(comps):
        y = 95 + i * 84
        add_rect(dwg, 60, y, 280, 70, fill=PANEL, stroke=color, rx=8, stroke_width=2)
        add_text(dwg, name, 80, y + 24, fill="#fff", size=12.5, weight="bold")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, 80, y + 46 + j * 17, fill=TEXT_DIM, size=10.5)

    add_text(dwg, "触发链路", 500, 80, fill=TEXT, size=14, weight="bold")
    flows = [
        ("按钮 Trigger", "VRC_Interactable → Interact 事件", ACCENT),
        ("Udon 响应", 'SetBool("doorOpen", !doorOpen)', SUCCESS),
        ("Animator 参数", "doorOpen 变化 → 转换条件满足", WARM),
        ("状态机播放", "Open 状态 → 播放「开门」剪辑", "#c084fc"),
    ]
    for i, (title, desc, color) in enumerate(flows):
        y = 95 + i * 84
        add_rect(dwg, 460, y, 380, 70, fill=PANEL, stroke=color, rx=8, stroke_width=2)
        add_text(dwg, title, 480, y + 24, fill="#fff", size=12.5, weight="bold")
        add_text(dwg, desc, 480, y + 48, fill=TEXT_DIM, size=11)

    add_rect(dwg, 100, 420, 700, 55, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "关键：Udon 只碰参数，动画只归状态机管 —— 各干各的，互不打架", 450, 452, fill=SUCCESS, size=13, anchor="middle")
    save_svg_and_png(dwg, "L05_02_result")


# ============================================================
# L06 — 图1: 术语速查
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "动画术语速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    terms = [
        ("Clip 剪辑", "一段记录的动画：属性 + 关键帧", ACCENT),
        ("Animator", "播放动画的组件，挂到物体上", ACCENT),
        ("Controller 控制器", "状态机的载体 Asset", ACCENT),
        ("状态 State", "物体的一种形态（门关着/开着）", ACCENT),
        ("转换 Transition", "状态之间的切换规则 + 过渡动画", SUCCESS),
        ("Float 参数", "带小数点的数字（速度/进度）", SUCCESS),
        ("Bool 参数", "真假开关（doorOpen = true）", SUCCESS),
        ("Trigger 参数", "一次性触发信号（拉一下）", SUCCESS),
        ("关键帧 Keyframe", "某一时刻的属性快照（菱形）", WARM),
        ("时间轴 Timeline", "时间刻度，关键帧排在上面", WARM),
        ("录制 Record", "边改属性边自动记关键帧", WARM),
        ("权重 Weight", "动画层混合比例（0~1）", WARM),
    ]
    col_w = 390
    for i, (term, desc, color) in enumerate(terms):
        row, col = divmod(i, 2)
        x = 60 + col * (col_w + 30)
        y = 70 + row * 76
        add_rect(dwg, x, y, col_w, 60, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        add_text(dwg, term, x + 16, y + 24, fill="#fff", size=13, weight="bold")
        add_text(dwg, desc, x + 16, y + 46, fill=TEXT_DIM, size=11)

    add_text(dwg, "记不住没关系：遇到问题回来翻这一页", W//2, 540, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_01_cheatsheet")


# ============================================================
# L06 — 图2: 常见问题对照表
# ============================================================
def make_L06_02_common_issues():
    W, H = 900, 540
    dwg = new_svg(W, H)
    add_text(dwg, "动画常见问题对照表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    rows = [
        ("动画不动", "参数名写错 / 属性被 Udon 覆盖", "核对参数拼写；一个属性只归一处管", "#ff88cc"),
        ("两个动画互抢", "多个地方改同一个属性", "确定唯一控制方（动画 or 代码）", WARN),
        ("参数没生效", "Animator 里没这个参数", "在 Animator 面板添加并核对名字", WARN),
        ("Udon 改不了动画", "Animator 引用没连对", "检查引用；Animator 在自身或子物体", ACCENT),
        ("门开关顺序反了", "状态转换方向连反", "检查 Idle→Open 用 doorOpen=true", ACCENT),
        ("开一次就停", "用 Trigger 做开关没有保持", "开关用 Bool 做双稳态更稳", SUCCESS),
    ]
    col_w = [170, 270, 340]
    xs = [60, 245, 530]
    for hd, x in zip(["问题现象", "常见原因", "解决办法"], xs):
        add_rect(dwg, x, 70, col_w[0], 34, fill=PANEL, stroke=ACCENT, stroke_width=1.5)
        add_text(dwg, hd, x + col_w[0]//2, 92, fill=ACCENT, size=13, weight="bold", anchor="middle")
    for i, (prob, cause, sol, color) in enumerate(rows):
        y = 104 + i * 66
        add_rect(dwg, 60, y, col_w[0], 56, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, prob, 60 + col_w[0]//2, y + 34, fill="#fff", size=12, weight="bold", anchor="middle")
        add_rect(dwg, 245, y, col_w[1], 56, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, cause, 245 + col_w[1]//2, y + 34, fill=TEXT_DIM, size=11.5, anchor="middle")
        add_rect(dwg, 530, y, col_w[2], 56, fill=PANEL, stroke=SUCCESS, rx=6)
        add_text(dwg, sol, 530 + col_w[2]//2, y + 34, fill=SUCCESS, size=11.5, anchor="middle")

    add_text(dwg, "调试心法：先问「参数对不对、谁在改这个属性」，八成问题在这里", W//2, 530, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_02_common_issues")


# ============================================================
# L06 — 图3: 进阶路线
# ============================================================
def make_L06_03_roadmap():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "动画进阶路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    stages = [
        ("入门 · 会开关门", "Clip + 状态机\nSetBool 交互", ACCENT, "现在"),
        ("熟练 · 复杂交互", "多状态 / 传送带\n按钮、NPC 动画", SUCCESS, "1 周"),
        ("进阶 · 会做表现", "曲线调手感\n动画与音效粒子配合", WARM, "1 个月"),
        ("精通 · 会做演出", "Timeline 编排\n动画事件、道具装配", "#c084fc", "长期"),
    ]
    box_w, box_h = 180, 150
    start_x = (W - (box_w * 4 + 30 * 3)) // 2
    for i, (title, desc, color, time) in enumerate(stages):
        x = start_x + i * (box_w + 30)
        y = 100
        add_rect(dwg, x, y, box_w, box_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, y + 30, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + box_w//2, y + 60 + j * 19, fill=TEXT_DIM, size=11, anchor="middle")
        add_text(dwg, f"⏱ {time}", x + box_w//2, y + box_h - 14, fill=color, size=11, anchor="middle")
        if i < 3:
            add_arrow(dwg, x + box_w + 2, y + box_h//2, x + box_w + 28, y + box_h//2, stroke=color, stroke_width=2)

    add_rect(dwg, 100, 300, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "学习建议", 130, 330, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "① 第一个动画就做「门」，最经典也最能练全流程  ② 参数名写纸上，别靠记", 130, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "③ 动画不动先按「排查四件事」走一遍  ④ 看到好世界，拆它的动画结构", 130, 382, fill=TEXT_DIM, size=12.5)

    save_svg_and_png(dwg, "L06_03_roadmap")


if __name__ == "__main__":
    for f in [make_L01_01_animation_layers, make_L01_02_animator_component,
              make_L02_01_state_machine, make_L02_02_parameters, make_L02_03_any_state,
              make_L03_01_record_animation, make_L03_02_keyframe_timeline,
              make_L04_01_interact_flow, make_L04_02_pitfalls,
              make_L05_01_steps, make_L05_02_result,
              make_L06_01_cheatsheet, make_L06_02_common_issues, make_L06_03_roadmap]:
        print(f"生成 {f.__name__} ...")
        f()
    print("全部完成")
