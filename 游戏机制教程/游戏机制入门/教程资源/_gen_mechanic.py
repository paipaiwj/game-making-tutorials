# -*- coding: utf-8 -*-
# Unity 游戏机制入门教程（面向 VRChat）— 配图生成脚本
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _render_svg import *

_grad_counter = [0]

def _gid():
    _grad_counter[0] += 1
    return f"g{_grad_counter[0]}"

def radial_grad(dwg, stops, cx=None, cy=None, r=None):
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


# ============================================================
# L01 — 图1: 游戏机制四要素
# ============================================================
def make_L01_01_what_is_mechanic():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "游戏机制 = 游戏的「规则」", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "机制是「玩家能做什么、世界怎么回应」，而不是画面和声音", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    items = [
        ("目标", "玩家要达成的目的\n（得分、存活、到达终点）", ACCENT),
        ("规则", "能做什么、不能做什么\n（每次只能走一步）", SUCCESS),
        ("反馈", "世界对行为的回应\n（加分、掉血、音效）", WARM),
        ("挑战", "难度与成长曲线\n（越来越难但能通过）", "#c084fc"),
    ]
    card_w, card_h = 190, 150
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(items):
        cx = start_x + i * (card_w + 26)
        cy = 110
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_ellipse(dwg, cx + card_w//2, cy + 34, 18, 18, fill=color, opacity=0.6)
        add_text(dwg, title, cx + card_w//2, cy + 76, fill="#fff", size=14, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, cy + 102 + j * 18, fill=TEXT_DIM, size=11.5, anchor="middle")

    add_rect(dwg, 100, 300, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "举个例子：VRChat 捉迷藏", 130, 330, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "目标：找到所有藏起来的玩家   规则：藏的人不能移动", 130, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "反馈：找到时播放音效+记一分   挑战：时间限制越来越紧", 130, 382, fill=TEXT_DIM, size=12.5)

    add_text(dwg, "做游戏 = 先定机制，再做画面。机制不好玩，画面再好看也没用", W//2, 450, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L01_01_what_is_mechanic")


# ============================================================
# L01 — 图2: 核心循环
# ============================================================
def make_L01_02_core_loop():
    W, H = 900, 400
    dwg = new_svg(W, H)
    add_text(dwg, "核心循环 Core Loop", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "玩家反复做的最小动作圈，整个游戏的骨架", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    boxes = [("行动", "捡起、投掷、触碰", ACCENT, 80),
             ("反馈", "得分、音效、变化", SUCCESS, 340),
             ("推进", "解锁、升级、下一关", WARM, 600)]
    box_w = 180
    for title, desc, color, x in boxes:
        add_rect(dwg, x, 110, box_w, 130, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, 145, fill="#fff", size=15, weight="bold", anchor="middle")
        add_text(dwg, desc, x + box_w//2, 175, fill=TEXT_DIM, size=12, anchor="middle")
    add_arrow(dwg, 268, 172, 332, 172, stroke=ACCENT, stroke_width=2.5)
    add_arrow(dwg, 528, 172, 592, 172, stroke=SUCCESS, stroke_width=2.5)
    # 回环
    add_line(dwg, 690, 252, 170, 252, stroke=WARM, stroke_width=2, with_arrow=True)
    add_text(dwg, "循环回到行动", 430, 244, fill="#bbbbbb", size=11, anchor="middle")

    add_rect(dwg, 100, 280, 700, 80, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "例：扔飞镖  →  命中+分数+音效  →  解锁新飞镖  →  再扔", 130, 310, fill=TEXT_DIM, size=13)
    add_text(dwg, "小游戏只用 1 个循环就够；循环越顺，游戏越好玩", 130, 338, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L01_02_core_loop")


# ============================================================
# L02 — 图1: 游戏状态
# ============================================================
def make_L02_01_game_state():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "游戏状态：一场游戏分几个阶段", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    states = [
        ("准备 Ready", "玩家入场、倒计时", ACCENT),
        ("进行 Playing", "核心循环运行中", SUCCESS),
        ("结束 Over", "胜负已定、结算", WARM),
    ]
    card_w, card_h = 220, 150
    start_x = (W - (card_w * 3 + 40 * 2)) // 2
    for i, (title, desc, color) in enumerate(states):
        x = start_x + i * (card_w + 40)
        add_rect(dwg, x, 100, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 140, fill="#fff", size=14, weight="bold", anchor="middle")
        add_text(dwg, desc, x + card_w//2, 172, fill=TEXT_DIM, size=12, anchor="middle")
        if i < 2:
            add_arrow(dwg, x + card_w + 6, 175, x + card_w + 34, 175, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 290, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "为什么必须分状态？", 130, 320, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "因为「游戏还没开始时，玩家按按钮不该算分」——所有行为都要先问：现在是什么状态？", 130, 350, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "代码里用 enum 或字符串存当前状态，一处判定，处处生效", 130, 374, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L02_01_game_state")


# ============================================================
# L02 — 图2: 状态机
# ============================================================
def make_L02_02_state_machine():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "状态机 State Machine", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "状态 + 触发条件 + 转移 = 状态机。游戏逻辑的万能骨架", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 三个状态 + 连线
    nodes = [("Ready 准备", (140, 180), ACCENT), ("Playing 进行", (450, 180), SUCCESS), ("Over 结束", (760, 180), WARM)]
    for title, (cx, cy), color in nodes:
        add_rect(dwg, cx - 90, cy - 40, 180, 80, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx, cy + 6, fill="#fff", size=14, weight="bold", anchor="middle")
    # 转移
    add_line(dwg, 235, 180, 352, 180, stroke=ACCENT, stroke_width=2, with_arrow=True)
    add_text(dwg, "倒计时结束", 294, 168, fill=TEXT_DIM, size=10.5, anchor="middle")
    add_line(dwg, 545, 180, 662, 180, stroke=SUCCESS, stroke_width=2, with_arrow=True)
    add_text(dwg, "达成胜负条件", 604, 168, fill=TEXT_DIM, size=10.5, anchor="middle")
    add_line(dwg, 670, 235, 140, 250, stroke=WARM, stroke_width=2, dash=[6, 4], with_arrow=True)
    add_rect(dwg, 330, 236, 110, 24, fill="#222222", stroke=BORDER, rx=12)
    add_text(dwg, "重新开始", 385, 253, fill="#dddddd", size=10.5, anchor="middle")

    add_rect(dwg, 100, 310, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "每个状态只干一件事", 130, 340, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "Ready：只管等待和倒计时    Playing：只管核心循环    Over：只管结算和重置", 130, 368, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "状态分得越清楚，bug 越少 —— 想不出 bug 在哪？先看状态对不对", 130, 392, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L02_02_state_machine")


# ============================================================
# L02 — 图3: 计数与变量
# ============================================================
def make_L02_03_counter():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "计数：游戏里到处是「数」", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    items = [
        ("分数", "score += 10", "每次命中加分", ACCENT),
        ("生命", "lives -= 1", "归零即失败", SUCCESS),
        ("时间", "timeLeft -= deltaTime", "每秒减少", WARM),
        ("次数", "attempts += 1", "统计玩家操作", "#c084fc"),
        ("开关", "isPlaying = true", "真假两种状态", "#ff9e4e"),
    ]
    card_w, card_h = 156, 200
    start_x = (W - (card_w * 5 + 14 * 4)) // 2
    for i, (name, code, desc, color) in enumerate(items):
        x = start_x + i * (card_w + 14)
        add_rect(dwg, x, 90, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, name, x + card_w//2, 118, fill="#fff", size=13.5, weight="bold", anchor="middle")
        add_rect(dwg, x + 12, 132, card_w - 24, 60, fill="#1a1a1a", stroke=BORDER, rx=6)
        add_text(dwg, code, x + card_w//2, 164, fill="#9ecbff", size=12, anchor="middle")
        add_text(dwg, desc, x + card_w//2, 228, fill=TEXT_DIM, size=11.5, anchor="middle")
        add_text(dwg, "初始化=0", x + card_w//2, 250, fill=TEXT_MUTED, size=10.5, anchor="middle")

    add_rect(dwg, 100, 320, 700, 70, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "所有变量在游戏开始（Ready）时归零/复位 —— 否则上一局的数据会带到下一局", 130, 350, fill=WARN, size=12.5)
    add_text(dwg, "VRChat 多人时变量要同步，见《网络同步》教程", 130, 374, fill=TEXT_MUTED, size=12)
    save_svg_and_png(dwg, "L02_03_counter")


# ============================================================
# L03 — 图1: 计分流程
# ============================================================
def make_L03_01_score_flow():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "计分流程：事件 → 判定 → 加分 → 显示", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    steps = [
        ("1. 事件发生", "玩家命中目标\n触发碰撞/交互", ACCENT),
        ("2. 状态判定", "游戏在进行中？\n是不是有效目标？", SUCCESS),
        ("3. 修改分数", "score += 10\n（变量同步）", WARM),
        ("4. 反馈与显示", "加分音效+特效\nUI 文本更新", "#c084fc"),
    ]
    card_w, card_h = 190, 150
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 26)
        cy = 100
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 128, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 156 + j * 20, fill=TEXT_DIM, size=11.5, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 175, cx + card_w + 24, 175, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 290, 700, 80, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "最重要的一步是第 2 步（状态判定）", 130, 320, fill=SUCCESS, size=13, weight="bold")
    add_text(dwg, "「游戏没开始、已经结束、重复命中」都要在这拦截 —— 这就是防作弊和防 bug 的关键", 130, 346, fill=TEXT_DIM, size=12.5)
    save_svg_and_png(dwg, "L03_01_score_flow")


# ============================================================
# L03 — 图2: 计时器
# ============================================================
def make_L03_02_timer():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "计时器：让游戏有节奏", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    add_rect(dwg, 60, 90, 780, 230, fill=PANEL, stroke=BORDER, rx=10)
    # 时间条
    add_text(dwg, "60", 90, 130, fill="#fff", size=16, weight="bold")
    add_text(dwg, "剩余秒数（每秒 -1）", 90, 155, fill=TEXT_MUTED, size=11.5)
    add_rect(dwg, 220, 110, 560, 24, fill="#1a1a1a", stroke=BORDER, rx=12)
    for i in range(4):
        add_rect(dwg, 220 + i * 140, 110, 132, 24, fill=ACCENT, rx=10, opacity=0.85)
    add_text(dwg, "时间条 / 数字，任选一种", 220, 160, fill=TEXT_DIM, size=11)
    # 三种用途
    uses = [
        ("倒计时", "限时挑战：时间到 = 结束", WARM),
        ("正计时", "统计用时：越快越好", SUCCESS),
        ("节奏感", "音效+光效随秒变化", "#c084fc"),
    ]
    for i, (title, desc, color) in enumerate(uses):
        x = 100 + i * 250
        add_ellipse(dwg, x, 240, 6, 6, fill=color)
        add_text(dwg, f"{title}：{desc}", x + 18, 244, fill=TEXT_DIM, size=12)

    add_text(dwg, "Udon 里用 Time.deltaTime 累加；时间只在「进行中」才走（状态机）", W//2, 380, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L03_02_timer")


# ============================================================
# L04 — 图1: 胜负判定
# ============================================================
def make_L04_01_win_lose():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "胜负判定：什么时候结束？谁赢了？", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 判定条件
    conds = [
        ("分数达到目标", "score >= 100", ACCENT),
        ("时间耗尽", "timeLeft <= 0", WARM),
        ("生命归零", "lives == 0", "#ff88cc"),
        ("完成目标", "所有目标达成", SUCCESS),
    ]
    card_w, card_h = 190, 110
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, code, color) in enumerate(conds):
        cx = start_x + i * (card_w + 26)
        add_rect(dwg, cx, 90, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 120, fill="#fff", size=13, weight="bold", anchor="middle")
        add_text(dwg, code, cx + card_w//2, 150, fill="#9ecbff", size=12, anchor="middle")

    # 流程
    add_text(dwg, "判定流程", 90, 250, fill=TEXT, size=14, weight="bold")
    flow = [("每次计分/计时后检查", ACCENT), ("满足条件？", SUCCESS), ("是 → 切到 Over 状态", WARM), ("结算并广播结果", "#c084fc")]
    fx = 90
    for i, (txt, color) in enumerate(flow):
        add_rect(dwg, fx, 262, 170, 50, fill="#1a1a1a", stroke=color, rx=8)
        add_text(dwg, txt, fx + 85, 292, fill=TEXT_DIM, size=11.5, anchor="middle")
        fx += 180
        if i < 3:
            add_arrow(dwg, fx - 4, 287, fx + 8, 287, stroke=color, stroke_width=2)

    add_rect(dwg, 100, 350, 700, 70, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "多人游戏：结果要广播给所有玩家（网络事件），并防止「每个人各判各的」", 130, 380, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L04_01_win_lose")


# ============================================================
# L04 — 图2: 重置流程
# ============================================================
def make_L04_02_reset():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "重置：让游戏可以再玩一次", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    steps = [
        ("1. 结算", "显示成绩/名次\n播结束音效", WARM),
        ("2. 清零", "分数=0 时间=初始\n物体回原位", ACCENT),
        ("3. 广播", "通知所有玩家\n各端同时复位", SUCCESS),
        ("4. 回 Ready", "回到准备状态\n等待下一局", "#c084fc"),
    ]
    card_w, card_h = 190, 150
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 26)
        cy = 90
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 118, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 146 + j * 20, fill=TEXT_DIM, size=11.5, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 165, cx + card_w + 24, 165, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 280, 700, 80, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "最容易忘的：物体位置、旋转、粒子、音效状态也要重置", 130, 310, fill=WARN, size=12.5)
    add_text(dwg, "建议写一个 ResetAll() 统一调用，而不是到处散落复位代码", 130, 338, fill=TEXT_DIM, size=12.5)
    save_svg_and_png(dwg, "L04_02_reset")


# ============================================================
# L05 — 图1: 小游戏步骤
# ============================================================
def make_L05_01_steps():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "实战：做一个「抢答得分」小游戏", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "目标：玩家按按钮得分，先到 10 分获胜 —— 覆盖状态、计分、胜负、重置", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 定规则", "状态机：Ready/Playing/Over\n目标 10 分", ACCENT),
        ("2. 搭场景", "按钮 + 计分板 UI\n倒计时文本", SUCCESS),
        ("3. 写逻辑", "按钮→判定→加分\nUdon 组件", WARM),
        ("4. 连信号", "按架构：Trigger→\nSignal→Component", "#c084fc"),
        ("5. 测试", "Build & Test\n三人联机试玩", "#ff9e4e"),
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

    add_text(dwg, "按你项目的架构来：按钮 Trigger → SignalSender 路由 → GameComponent 记分", W//2, 340, fill=TEXT_DIM, size=13, anchor="middle")
    add_rect(dwg, 150, 370, 600, 60, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "从「能玩」开始，别一上来加特效 —— 机制通了再美化", 450, 406, fill=WARN, size=12.5, anchor="middle")
    save_svg_and_png(dwg, "L05_01_steps")


# ============================================================
# L05 — 图2: 小游戏逻辑结构
# ============================================================
def make_L05_02_result():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "抢答小游戏的完整结构", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 左侧：组件
    add_text(dwg, "组件（Component）", 120, 80, fill=TEXT, size=14, weight="bold")
    comps = [
        ("GameManagerComponent", "状态机 + 胜负判定 + 重置", ACCENT),
        ("ScoreComponent", "分数变量 + 加分 + 广播", SUCCESS),
        ("TimerComponent", "倒计时 + 时间到信号", WARM),
        ("ScoreboardComponent", "UI 计分板显示", "#c084fc"),
    ]
    for i, (name, desc, color) in enumerate(comps):
        y = 95 + i * 78
        add_rect(dwg, 60, y, 260, 62, fill=PANEL, stroke=color, rx=8, stroke_width=2)
        add_text(dwg, name, 80, y + 24, fill="#fff", size=12.5, weight="bold")
        add_text(dwg, desc, 80, y + 46, fill=TEXT_DIM, size=11)

    # 右侧：流程
    add_text(dwg, "信号流（Signal）", 480, 80, fill=TEXT, size=14, weight="bold")
    flows = [
        ("按钮 Trigger", "Interact → Execute", ACCENT),
        ("加分信号", "Signal → ScoreComponent", SUCCESS),
        ("倒计时信号", "Timer → GameManager", WARM),
        ("胜负信号", "GameManager → 全部", "#c084fc"),
    ]
    for i, (title, desc, color) in enumerate(flows):
        y = 95 + i * 78
        add_rect(dwg, 420, y, 420, 62, fill=PANEL, stroke=color, rx=8, stroke_width=2)
        add_text(dwg, title, 440, y + 24, fill="#fff", size=12.5, weight="bold")
        add_text(dwg, desc, 440, y + 46, fill=TEXT_DIM, size=11)

    # 底部
    add_rect(dwg, 100, 404, 700, 60, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "每个组件只干一件事，信号只走一条路 —— 这就是你项目架构的意义", 450, 440, fill=SUCCESS, size=13, anchor="middle")
    save_svg_and_png(dwg, "L05_02_result")


# ============================================================
# L06 — 图1: 术语速查
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "游戏机制术语速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    terms = [
        ("机制 Mechanic", "游戏的规则：玩家能做什么、世界怎么回应", ACCENT),
        ("核心循环", "玩家反复做的最小动作圈", ACCENT),
        ("游戏状态", "准备/进行/结束 等阶段", ACCENT),
        ("状态机", "状态 + 条件 + 转移的逻辑骨架", ACCENT),
        ("目标 Goal", "玩家要达成的目的", SUCCESS),
        ("规则 Rule", "能做什么、不能做什么", SUCCESS),
        ("反馈 Feedback", "世界对行为的回应（分数/音效）", SUCCESS),
        ("挑战 Difficulty", "难度曲线，让游戏有成长", SUCCESS),
        ("计分系统", "事件 → 判定 → 加分 → 显示", WARM),
        ("倒计时", "限时机制，制造紧张感", WARM),
        ("胜负判定", "分数/时间/生命的结束条件", WARM),
        ("重置 Reset", "清空状态让游戏可重玩", WARM),
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
        ("还没开始就能得分", "没有状态判定", "加分前检查游戏状态", "#ff88cc"),
        ("上一局分数带到下一局", "没有重置逻辑", "写 ResetAll() 统一清零", WARN),
        ("按钮狂点刷分", "没做防重复判定", "每人限一次 / 冷却时间", WARN),
        ("游戏卡在某个状态", "状态转移条件没写全", "把转移条件画成状态机图", ACCENT),
        ("两个人分数不一样", "变量没同步", "用 [UdonSynced] 同步", SUCCESS),
        ("时间不走了", "计时逻辑写在非进行状态", "只在进行中累加时间", SUCCESS),
    ]
    col_w = [170, 300, 310]
    xs = [60, 245, 560]
    for hd, x in zip(["问题现象", "常见原因", "解决办法"], xs):
        add_rect(dwg, x, 70, col_w[0], 34, fill=PANEL, stroke=ACCENT, stroke_width=1.5)
        add_text(dwg, hd, x + col_w[0]//2, 92, fill=ACCENT, size=13, weight="bold", anchor="middle")
    for i, (prob, cause, sol, color) in enumerate(rows):
        y = 104 + i * 70
        add_rect(dwg, 60, y, col_w[0], 60, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, prob, 60 + col_w[0]//2, y + 34, fill="#fff", size=12, weight="bold", anchor="middle")
        add_rect(dwg, 245, y, col_w[1], 60, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, cause, 245 + col_w[1]//2, y + 34, fill=TEXT_DIM, size=11.5, anchor="middle")
        add_rect(dwg, 560, y, col_w[2], 60, fill=PANEL, stroke=SUCCESS, rx=6)
        add_text(dwg, sol, 560 + col_w[2]//2, y + 34, fill=SUCCESS, size=11.5, anchor="middle")

    add_text(dwg, "调试心法：先问「现在是什么状态？」再看代码 —— 八成 bug 是状态不对", W//2, 532, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_02_common_issues")


# ============================================================
# L06 — 图3: 进阶路线
# ============================================================
def make_L06_03_roadmap():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "进阶路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    stages = [
        ("入门 · 会做小游戏", "状态机 + 计分\n做一个抢答/钓鱼", ACCENT, "现在"),
        ("熟练 · 会做多玩法", "网络同步 / 多玩家\n玩家权限管理", SUCCESS, "1 周"),
        ("进阶 · 会做系统", "经济系统 / 背包\n数据存档", WARM, "1 个月"),
        ("精通 · 会做设计", "数值平衡 / 关卡设计\n让机制有趣", "#c084fc", "长期"),
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
            add_arrow(dwg, x + box_w + 2, y + box_h//2, x + box_w + 28, y + box_h//2, stroke=color, stroke_width=2)

    add_rect(dwg, 100, 300, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "学习建议", 130, 330, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "① 每个游戏先写「规则一句话」，再写代码  ② 状态机画在纸上，比写代码先", 130, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "③ 机制先能玩再美化  ④ 玩别人的小游戏，反推它的规则", 130, 382, fill=TEXT_DIM, size=12.5)

    save_svg_and_png(dwg, "L06_03_roadmap")


if __name__ == "__main__":
    for f in [make_L01_01_what_is_mechanic, make_L01_02_core_loop,
              make_L02_01_game_state, make_L02_02_state_machine, make_L02_03_counter,
              make_L03_01_score_flow, make_L03_02_timer,
              make_L04_01_win_lose, make_L04_02_reset,
              make_L05_01_steps, make_L05_02_result,
              make_L06_01_cheatsheet, make_L06_02_common_issues, make_L06_03_roadmap]:
        print(f"生成 {f.__name__} ...")
        f()
    print("全部完成")
