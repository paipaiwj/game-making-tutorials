# -*- coding: utf-8 -*-
# Unity 网络同步入门教程（VRChat / UdonSharp）— 配图生成脚本
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _render_svg import *


# ============================================================
# L01 — 图1: 本地 vs 网络同步
# ============================================================
def make_L01_01_local_vs_sync():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "本地播放 vs 网络同步", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "同一段代码，单机只在一个客户端跑；多人世界里每个玩家的客户端都在各跑一份", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 左：本地
    add_rect(dwg, 60, 95, 370, 190, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    add_text(dwg, "本地播放（只在自己机器上变）", 245, 125, fill="#fff", size=14, weight="bold", anchor="middle")
    for i, p in enumerate(["玩家A 的客户端", "玩家B 的客户端", "玩家C 的客户端"]):
        x = 82 + i * 118
        add_rect(dwg, x, 150, 90, 60, fill="#1a1a1a", stroke=BORDER, rx=8)
        add_text(dwg, p, x + 45, 178, fill=TEXT_DIM, size=10.5, anchor="middle")
        add_text(dwg, "各算各的", x + 45, 198, fill=TEXT_MUTED, size=9.5, anchor="middle")
    add_text(dwg, "✗ 只有按按钮的人能看到变化", 245, 255, fill="#ff88cc", size=12, anchor="middle")

    # 右：同步
    add_rect(dwg, 470, 95, 370, 190, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=2)
    add_text(dwg, "网络同步（大家一起变）", 655, 125, fill="#fff", size=14, weight="bold", anchor="middle")
    for i, p in enumerate(["玩家A", "玩家B", "玩家C"]):
        x = 492 + i * 118
        add_rect(dwg, x, 150, 90, 60, fill="#1a1a1a", stroke=SUCCESS, rx=8)
        add_text(dwg, p, x + 45, 178, fill=TEXT_DIM, size=10.5, anchor="middle")
        add_text(dwg, "同一份数据", x + 45, 198, fill="#6bcf7f", size=9.5, anchor="middle")
    add_text(dwg, "✓ 所有人看到同一个分数", 655, 255, fill=SUCCESS, size=12, anchor="middle")

    add_rect(dwg, 100, 315, 700, 120, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "一句话概念：[UdonSynced] 变量 = 会被网络同步的变量", 130, 346, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "owner（所有者）= 唯一有资格修改同步变量的玩家，改完自动发给其他玩家", 130, 374, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "同步的东西只有两种：① 变量（数据）  ② 事件（通知），本教程就是讲这两个", 130, 402, fill=WARM, size=12.5)

    save_svg_and_png(dwg, "L01_01_local_vs_sync")


# ============================================================
# L01 — 图2: 同步总览（变量 + 事件）
# ============================================================
def make_L01_02_sync_concept():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "网络同步的两件套：变量 + 事件", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "变量传「数据」，事件传「通知」—— 两者分工不同，常常配合使用", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 左卡：同步变量
    add_rect(dwg, 60, 95, 370, 230, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    add_text(dwg, "① 同步变量 [UdonSynced]", 245, 125, fill="#fff", size=14, weight="bold", anchor="middle")
    add_rect(dwg, 85, 140, 320, 60, fill="#1a1a1a", stroke=BORDER, rx=6)
    add_text(dwg, "[UdonSynced] public int score;", 245, 165, fill="#9ecbff", size=12, anchor="middle")
    add_text(dwg, "传什么：数字、布尔、字符串等数据", 245, 195, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "典型用途：分数、开关、游戏状态", 245, 217, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "谁改：只有 owner 能改，改完全网同步", 245, 239, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "收端：OnDeserialization() 被自动调用", 245, 261, fill=TEXT_DIM, size=11, anchor="middle")

    # 右卡：同步事件
    add_rect(dwg, 470, 95, 370, 230, fill=PANEL, stroke=WARM, rx=10, stroke_width=2)
    add_text(dwg, "② 同步事件 SendCustomNetworkEvent", 655, 125, fill="#fff", size=14, weight="bold", anchor="middle")
    add_rect(dwg, 495, 140, 320, 60, fill="#1a1a1a", stroke=BORDER, rx=6)
    add_text(dwg, "SendCustomNetworkEvent(\"PlaySound\")", 655, 165, fill="#9ecbff", size=12, anchor="middle")
    add_text(dwg, "传什么：一个方法名 + 想传的参数", 655, 195, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "典型用途：播放音效、开特效、触发动画", 655, 217, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "谁发：任何玩家都能发起广播", 655, 239, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "收端：所有客户端同时调用该方法", 655, 261, fill=TEXT_DIM, size=11, anchor="middle")

    add_rect(dwg, 100, 350, 700, 70, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "口诀：数据用变量同步，动作用事件广播", 450, 380, fill=SUCCESS, size=13.5, weight="bold", anchor="middle")
    add_text(dwg, "事件只广播一次：新加入的玩家不会重放 —— 所以要给新玩家「现状」要用变量", 450, 404, fill=TEXT_DIM, size=11.5, anchor="middle")

    save_svg_and_png(dwg, "L01_02_sync_concept")


# ============================================================
# L02 — 图1: 同步变量工作原理
# ============================================================
def make_L02_01_synced_var():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "同步变量工作原理", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "owner 修改 → 数据发送到网络 → 其他客户端收到并覆盖本地值", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 三格流程
    add_rect(dwg, 60, 95, 240, 190, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    add_text(dwg, "① owner 修改", 180, 125, fill="#fff", size=13.5, weight="bold", anchor="middle")
    add_rect(dwg, 85, 140, 190, 56, fill="#1a1a1a", stroke=BORDER, rx=6)
    add_text(dwg, "score = 10;", 180, 164, fill="#9ecbff", size=12, anchor="middle")
    add_text(dwg, "只有 owner 有资格写", 180, 192, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "非 owner 改了会丢/被纠正", 180, 212, fill=TEXT_MUTED, size=10, anchor="middle")

    add_rect(dwg, 330, 95, 240, 190, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=2)
    add_text(dwg, "② 网络发送", 450, 125, fill="#fff", size=13.5, weight="bold", anchor="middle")
    add_ellipse(dwg, 450, 160, 62, 34, fill="#1a1a1a", stroke=SUCCESS, stroke_width=1.5)
    add_text(dwg, "同步网络", 450, 166, fill=SUCCESS, size=12, anchor="middle")
    add_text(dwg, "VRChat 服务器转发", 450, 218, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "自动进行，不用写代码", 450, 240, fill=TEXT_MUTED, size=10, anchor="middle")

    add_rect(dwg, 600, 95, 240, 190, fill=PANEL, stroke=WARM, rx=10, stroke_width=2)
    add_text(dwg, "③ 其他端接收", 720, 125, fill="#fff", size=13.5, weight="bold", anchor="middle")
    add_rect(dwg, 625, 140, 190, 56, fill="#1a1a1a", stroke=BORDER, rx=6)
    add_text(dwg, "score = 10;", 720, 164, fill="#9ecbff", size=12, anchor="middle")
    add_text(dwg, "本地值被新数据覆盖", 720, 192, fill=TEXT_DIM, size=11, anchor="middle")
    add_text(dwg, "OnDeserialization() 触发", 720, 212, fill=WARM, size=10.5, anchor="middle")

    add_arrow(dwg, 308, 190, 322, 190, stroke=ACCENT, stroke_width=2.5)
    add_arrow(dwg, 578, 190, 592, 190, stroke=SUCCESS, stroke_width=2.5)

    add_rect(dwg, 100, 315, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "关键规则：谁改谁负责", 130, 345, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "① 只有 owner 改同步变量，其他人改会被服务器纠正  ② 收到数据后不要马上再改回去，会死循环", 130, 372, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "③ 想显示最新值：在 OnDeserialization() 里更新 UI / 播放反馈", 130, 396, fill=WARM, size=12.5)

    save_svg_and_png(dwg, "L02_01_synced_var")


# ============================================================
# L02 — 图2: OnDeserialization 流程
# ============================================================
def make_L02_02_ondeserialization():
    W, H = 900, 430
    dwg = new_svg(W, H)
    add_text(dwg, "OnDeserialization() —— 收端更新入口", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "同步变量到达本地后，Udon 自动调用这个函数 —— 这是你刷新 UI 的地方", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 数据到达", "网络数据到达本端\n本地变量被覆盖", ACCENT),
        ("2. 自动回调", "OnDeserialization()\n被自动调用", SUCCESS),
        ("3. 刷新显示", "更新 UI 文本\n播放反馈", WARM),
        ("4. 保持现状", "不要再改变量\n否则死循环", "#c084fc"),
    ]
    card_w, card_h = 190, 150
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 26)
        add_rect(dwg, cx, 100, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 128, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 156 + j * 20, fill=TEXT_DIM, size=11.5, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 175, cx + card_w + 24, 175, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 290, 700, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "典型代码", 130, 318, fill=SUCCESS, size=13.5, weight="bold")
    add_text(dwg, "public override void OnDeserialization() { scoreText.text = score.ToString(); }", 130, 344, fill="#9ecbff", size=12)
    add_text(dwg, "注意：修改同步变量的端不会收到回调（因为数据本来就在本地）", 130, 366, fill=TEXT_MUTED, size=11.5)

    save_svg_and_png(dwg, "L02_02_ondeserialization")


# ============================================================
# L03 — 图1: 网络事件流程
# ============================================================
def make_L03_01_network_event():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "网络事件：SendCustomNetworkEvent 广播", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "任何玩家发起 → 全网所有客户端同时调用同一个方法 —— 适合音效、特效、动画", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 中央发起者
    add_rect(dwg, 360, 116, 180, 98, fill=PANEL, stroke=WARM, rx=10, stroke_width=2)
    add_text(dwg, "玩家A（触发者）", 450, 143, fill="#fff", size=13, weight="bold", anchor="middle")
    add_rect(dwg, 378, 156, 144, 36, fill="#1a1a1a", stroke=BORDER, rx=6)
    add_text(dwg, "SendCustomNetworkEvent", 450, 175, fill="#9ecbff", size=10.5, anchor="middle")
    add_text(dwg, "(\"PlaySound\")", 450, 189, fill="#9ecbff", size=10.5, anchor="middle")

    # 三接收端
    recv = [("玩家A 自己", 80, ACCENT), ("玩家B", 390, SUCCESS), ("玩家C", 700, WARM)]
    for name, x, color in recv:
        add_rect(dwg, x, 280, 140, 90, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, name, x + 70, 308, fill="#fff", size=12.5, weight="bold", anchor="middle")
        add_text(dwg, "PlaySound()", x + 70, 334, fill="#9ecbff", size=11.5, anchor="middle")
        add_text(dwg, "播放音效", x + 70, 354, fill=TEXT_DIM, size=10.5, anchor="middle")
        add_arrow(dwg, 450, 216, x + 70, 272, stroke=WARM, stroke_width=2)

    add_rect(dwg, 100, 395, 700, 50, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "注意：事件不重放 —— 新玩家中途加入，不会听到已经播过的音效", 450, 425, fill=WARM, size=12.5, anchor="middle")

    save_svg_and_png(dwg, "L03_01_network_event")


# ============================================================
# L03 — 图2: 事件 vs 变量对比
# ============================================================
def make_L03_02_event_vs_var():
    W, H = 900, 470
    dwg = new_svg(W, H)
    add_text(dwg, "同步事件 vs 同步变量 —— 怎么选？", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")

    headers = [("", 90), ("同步变量 [UdonSynced]", 320), ("同步事件 NetworkEvent", 580)]
    add_rect(dwg, 60, 75, 780, 34, fill=PANEL, stroke=ACCENT, stroke_width=1.5)
    add_text(dwg, "对比项", 150, 97, fill=ACCENT, size=13, weight="bold", anchor="middle")
    add_text(dwg, "同步变量 [UdonSynced]", 415, 97, fill=ACCENT, size=13, weight="bold", anchor="middle")
    add_text(dwg, "同步事件 NetworkEvent", 700, 97, fill=ACCENT, size=13, weight="bold", anchor="middle")

    rows = [
        ("传什么", "数据（分数/开关/状态）", "一个方法名（通知）"),
        ("典型用途", "分数、状态、开关", "音效、特效、动画"),
        ("谁修改/发起", "只有 owner 能写", "任何玩家都能发"),
        ("收端如何感知", "OnDeserialization 回调", "直接调用该方法"),
        ("新玩家加入", "变量会同步给新玩家", "不重放，会漏掉"),
        ("能不能带参数", "天然带数据", "不能带，靠变量传参"),
    ]
    for i, (item, var_desc, ev_desc) in enumerate(rows):
        y = 109 + i * 56
        add_rect(dwg, 60, y, 780, 46, fill="#1a1a1a", stroke=BORDER, rx=6)
        add_text(dwg, item, 150, y + 28, fill="#fff", size=12, weight="bold", anchor="middle")
        add_text(dwg, var_desc, 415, y + 28, fill="#6bcf7f", size=11.5, anchor="middle")
        add_text(dwg, ev_desc, 700, y + 28, fill="#ff9e4e", size=11.5, anchor="middle")

    add_text(dwg, "一句话选择：要「新玩家也能拿到现状」→ 用变量；只想「动作播一次」→ 用事件", W//2, 452, fill=TEXT_DIM, size=12, anchor="middle", italic=True)

    save_svg_and_png(dwg, "L03_02_event_vs_var")


# ============================================================
# L04 — 图1: owner 概念
# ============================================================
def make_L04_01_owner():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "owner（所有者）：同步变量的「唯一管理员」", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "同一个 UdonBehaviour，在每个人眼里 owner 可能是不同的人 —— 只有 owner 有写权限", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 三个玩家视图
    views = [
        ("玩家A 视角", "owner = 玩家A ✓", "可以修改", ACCENT, True),
        ("玩家B 视角", "owner = 玩家A ✗", "只能读取", SUCCESS, False),
        ("玩家C 视角", "owner = 玩家A ✗", "只能读取", WARM, False),
    ]
    for i, (view, owner_txt, perm, color, is_owner) in enumerate(views):
        x = 80 + i * 265
        add_rect(dwg, x, 95, 230, 150, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, view, x + 115, 125, fill="#fff", size=13, weight="bold", anchor="middle")
        add_ellipse(dwg, x + 115, 155, 30, 22, fill="#1a1a1a", stroke=color)
        add_text(dwg, "★" if is_owner else "☆", x + 115, 161, fill=color, size=13, anchor="middle")
        add_text(dwg, owner_txt, x + 115, 195, fill=color, size=11.5, anchor="middle")
        add_text(dwg, perm, x + 115, 220, fill=TEXT_DIM, size=11, anchor="middle")

    add_rect(dwg, 100, 275, 700, 130, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "代码里怎么判断", 130, 305, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "if (Networking.LocalPlayer.IsOwner(gameObject)) { // 我是 owner，可以写 }", 130, 332, fill="#9ecbff", size=12)
    add_text(dwg, "想改同步变量？先申请所有权：SendCustomNetworkEvent(\"RequestOwnership\") 或 VRC_ObjectSync", 130, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "两个玩家同时抢所有权时，服务器会裁决 —— 只有一个人最终成为 owner", 130, 382, fill=WARM, size=12.5)

    save_svg_and_png(dwg, "L04_01_owner")


# ============================================================
# L04 — 图2: 请求所有权流程
# ============================================================
def make_L04_02_request_ownership():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "RequestOwnership() 请求所有权流程", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "想让别的玩家拥有同步变量？发起请求，等服务器裁决后 OnOwnershipTransferred 通知", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 请求", "SendCustomNetworkEvent\n(\"RequestOwnership\")", ACCENT),
        ("2. 服务器裁决", "VRChat 服务器判定\n可否转移", SUCCESS),
        ("3. 所有权转移", "OnOwnershipTransferred()\n被调用通知全端", WARM),
        ("4. 获得权限", "新 owner 可以修改\n同步变量了", "#c084fc"),
    ]
    card_w, card_h = 190, 150
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 26)
        add_rect(dwg, cx, 100, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 128, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 156 + j * 20, fill=TEXT_DIM, size=11.5, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 175, cx + card_w + 24, 175, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 290, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "为什么需要 VRC_ObjectSync？", 130, 320, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "① 让物体位置/旋转也能同步  ② 物体被拿起时自动把所有权交给拿它的人", 130, 348, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "注意：所有权转移不是立刻生效 —— 等回调确认后才好放心写数据", 130, 372, fill=WARN, size=12.5)

    save_svg_and_png(dwg, "L04_02_request_ownership")


# ============================================================
# L05 — 图1: 实战五步
# ============================================================
def make_L05_01_steps():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "实战：多人同步计分小游戏", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "目标：每端一个按钮 +1，所有人看到同一个分数 —— 覆盖变量同步 + 网络事件", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 建组件", "GameManagerComponent\n负责同步变量", ACCENT),
        ("2. 写同步变量", "[UdonSynced] score\nOnDeserialization", SUCCESS),
        ("3. 写加分逻辑", "按钮 → AddScore\nowner 检查", WARM),
        ("4. 广播事件", "播放音效\nSendCustomNetworkEvent", "#c084fc"),
        ("5. 联机测试", "两人进世界\n比分实时同步", "#ff9e4e"),
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

    add_rect(dwg, 100, 320, 700, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "核心思路：一个组件管同步（GameManager），UI 只负责读和显示", 130, 350, fill=SUCCESS, size=13, weight="bold")
    add_text(dwg, "按钮触发 → SignalSender 路由 → GameManager 加分 → OnDeserialization 刷新所有计分板", 130, 376, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "所有玩家点自己的按钮，但只有 owner 那个组件真正改分数 —— 别各算各的", 130, 398, fill=WARM, size=12.5)

    save_svg_and_png(dwg, "L05_01_steps")


# ============================================================
# L05 — 图2: 同步计分板结构
# ============================================================
def make_L05_02_result():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "同步计分板完整结构", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "一个 owner 写分，所有端显示，音效全网广播 —— 数据一致，动作一次", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 左列：玩家按钮
    add_text(dwg, "每个玩家的按钮", 120, 92, fill=TEXT, size=13.5, weight="bold")
    for i in range(3):
        y = 102 + i * 70
        add_rect(dwg, 60, y, 200, 56, fill=PANEL, stroke=ACCENT, rx=8, stroke_width=2)
        add_text(dwg, f"玩家{i+1} 的按钮 +1", 160, y + 24, fill="#fff", size=12, weight="bold", anchor="middle")
        add_text(dwg, "Interact → AddScore", 160, y + 44, fill=TEXT_DIM, size=10.5, anchor="middle")
        add_arrow(dwg, 268, y + 28, 292, y + 28, stroke=ACCENT, stroke_width=2)

    # 中列：GameManager
    add_rect(dwg, 300, 132, 300, 250, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=2)
    add_text(dwg, "GameManagerComponent", 450, 162, fill="#fff", size=14, weight="bold", anchor="middle")
    add_rect(dwg, 325, 182, 250, 40, fill="#1a1a1a", stroke=BORDER, rx=6)
    add_text(dwg, "[UdonSynced] score", 450, 207, fill="#9ecbff", size=12, anchor="middle")
    add_text(dwg, "AddScore()：owner 才加分", 450, 252, fill=TEXT_DIM, size=11.5, anchor="middle")
    add_text(dwg, "OnDeserialization：刷新所有计分板", 450, 276, fill=TEXT_DIM, size=11.5, anchor="middle")
    add_text(dwg, "发送 PlayScore 事件全网广播", 450, 300, fill=TEXT_DIM, size=11.5, anchor="middle")
    add_text(dwg, "（放在房间中任意一个物体上）", 450, 332, fill=TEXT_MUTED, size=10, anchor="middle")
    add_text(dwg, "是同步的「核心」，其他端都听它的", 450, 356, fill=WARM, size=10.5, anchor="middle")

    # 右列：计分板 + 音效
    add_text(dwg, "每个玩家的显示端", 670, 92, fill=TEXT, size=13.5, weight="bold")
    for i, name in enumerate(["计分板 UI", "音效播放器"]):
        y = 102 + i * 70
        add_rect(dwg, 610, y, 230, 56, fill=PANEL, stroke=WARM, rx=8, stroke_width=2)
        add_text(dwg, name, 725, y + 24, fill="#fff", size=12, weight="bold", anchor="middle")
        add_text(dwg, "读 score 显示 / 收事件播放", 725, y + 44, fill=TEXT_DIM, size=10.5, anchor="middle")
        add_arrow(dwg, 608, y + 28, 584, y + 28, stroke=WARM, stroke_width=2)
    add_text(dwg, "变量同步", 585, 116, fill=SUCCESS, size=10, anchor="end")
    add_text(dwg, "事件广播", 585, 188, fill=WARM, size=10, anchor="end")

    add_rect(dwg, 100, 400, 700, 56, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "原则：分数只在一处算（owner），其他地方只读 —— 这是多人数据一致性的核心", 450, 436, fill=SUCCESS, size=12.5, anchor="middle")

    save_svg_and_png(dwg, "L05_02_result")


# ============================================================
# L06 — 图1: 术语速查
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 900, 620
    dwg = new_svg(W, H)
    add_text(dwg, "网络同步术语速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    terms = [
        ("同步变量 [UdonSynced]", "会被网络同步的变量，只有 owner 能写", ACCENT),
        ("OnDeserialization()", "收到同步数据后自动调用的回调", ACCENT),
        ("同步事件", "SendCustomNetworkEvent 广播方法调用", ACCENT),
        ("owner（所有者）", "唯一有资格修改同步变量的玩家", ACCENT),
        ("LocalPlayer", "本端玩家，用于判断身份", ACCENT),
        ("RequestOwnership()", "请求成为某物体的 owner", ACCENT),
        ("反序列化", "把网络数据解包还原成变量的过程", SUCCESS),
        ("序列化", "把变量打包成网络数据的过程", SUCCESS),
        ("VRC_ObjectSync", "同步物体位置/旋转的组件", SUCCESS),
        ("IsOwner", "判断本端玩家是否拥有物体", SUCCESS),
        ("OnOwnershipTransferred", "所有权转移后触发的回调", SUCCESS),
        ("SendCustomEvent", "本地调用自己的方法（不同步）", WARM),
    ]
    col_w = 390
    for i, (term, desc, color) in enumerate(terms):
        row, col = divmod(i, 2)
        x = 60 + col * (col_w + 30)
        y = 70 + row * 80
        add_rect(dwg, x, y, col_w, 62, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        add_text(dwg, term, x + 16, y + 24, fill="#fff", size=12.5, weight="bold")
        add_text(dwg, desc, x + 16, y + 47, fill=TEXT_DIM, size=11)

    add_rect(dwg, 100, 556, 700, 50, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "记忆锚点：变量同步「现状」，事件广播「动作」", 450, 586, fill=WARM, size=12.5, anchor="middle")

    save_svg_and_png(dwg, "L06_01_cheatsheet")


# ============================================================
# L06 — 图2: 常见问题
# ============================================================
def make_L06_02_common_issues():
    W, H = 900, 620
    dwg = new_svg(W, H)
    add_text(dwg, "网络同步常见问题对照表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    col_w = [170, 300, 310]
    xs = [60, 245, 560]
    for hd, x in zip(["问题现象", "常见原因", "解决办法"], xs):
        add_rect(dwg, x, 70, col_w[0], 34, fill=PANEL, stroke=ACCENT, stroke_width=1.5)
        add_text(dwg, hd, x + col_w[0]//2, 92, fill=ACCENT, size=13, weight="bold", anchor="middle")

    rows = [
        ("别人看不到我改的分", "变量没加 [UdonSynced]", "加 [UdonSynced] 属性", WARN),
        ("非 owner 改了没反应", "只有 owner 能写", "先 RequestOwnership 再改", WARN),
        ("新玩家没有分数状态", "事件不重放", "用同步变量存状态", ACCENT),
        ("分数每个人不一样", "各端各算分数", "统一由 owner 算分", ACCENT),
        ("改分后 UI 不刷新", "没写 OnDeserialization", "在回调里更新 UI", SUCCESS),
        ("拿东西权限冲突", "所有权没转移", "加 VRC_ObjectSync 组件", SUCCESS),
    ]
    for i, (prob, cause, sol, color) in enumerate(rows):
        y = 104 + i * 76
        add_rect(dwg, 60, y, col_w[0], 66, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, prob, 60 + col_w[0]//2, y + 36, fill="#fff", size=12, weight="bold", anchor="middle")
        add_rect(dwg, 245, y, col_w[1], 66, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, cause, 245 + col_w[1]//2, y + 36, fill=TEXT_DIM, size=11.5, anchor="middle")
        add_rect(dwg, 560, y, col_w[2], 66, fill=PANEL, stroke=SUCCESS, rx=6)
        add_text(dwg, sol, 560 + col_w[2]//2, y + 36, fill=SUCCESS, size=11.5, anchor="middle")

    add_text(dwg, "调试心法：先问「谁是 owner？」再看「变量加没加 [UdonSynced]」", W//2, 612, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)

    save_svg_and_png(dwg, "L06_02_common_issues")


# ============================================================
# L06 — 图3: 进阶路线
# ============================================================
def make_L06_03_roadmap():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "网络同步进阶路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    stages = [
        ("入门 · 同步变量", "[UdonSynced] + 回调\n同步一个分数", ACCENT, "现在"),
        ("熟练 · 同步事件", "网络事件广播\n音效/特效播放", SUCCESS, "几天"),
        ("进阶 · 所有权", "RequestOwnership\n拿东西/抢控制权", WARM, "1 周"),
        ("精通 · 一致与优化", "谁算分/谁权威\n同步频率与带宽", "#c084fc", "长期"),
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

    add_rect(dwg, 100, 285, 700, 130, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "学习建议", 130, 315, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "① 先只同步一个分数，跑通全流程  ② 所有改动都先想清楚：谁是 owner？", 130, 343, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "③ 别在非 owner 端算逻辑，统一一处算  ④ 事件只用来广播「动作」，别传数据", 130, 367, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "⑤ 网络有延迟：写完变量过一会其他人才看到，这是正常的", 130, 391, fill=WARN, size=12.5)

    save_svg_and_png(dwg, "L06_03_roadmap")


if __name__ == "__main__":
    for f in [make_L01_01_local_vs_sync, make_L01_02_sync_concept,
              make_L02_01_synced_var, make_L02_02_ondeserialization,
              make_L03_01_network_event, make_L03_02_event_vs_var,
              make_L04_01_owner, make_L04_02_request_ownership,
              make_L05_01_steps, make_L05_02_result,
              make_L06_01_cheatsheet, make_L06_02_common_issues, make_L06_03_roadmap]:
        print(f"生成 {f.__name__} ...")
        f()
    print("全部完成")
