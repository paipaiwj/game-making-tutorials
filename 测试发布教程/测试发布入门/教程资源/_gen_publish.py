# -*- coding: utf-8 -*-
# Unity 测试与发布入门教程（面向 VRChat）— 配图生成脚本
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
# L01 — 图1: 测试类型对比
# ============================================================
def make_L01_01_test_types():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "测试类型：四种都要做", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "功能 / 性能 / 多人 / 边界 —— 覆盖世界能出问题的所有方向", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    items = [
        ("功能测试", "按钮能按吗？\n逻辑对不对？\n答案是预期吗？", ACCENT),
        ("性能测试", "帧数稳不稳？\n会不会卡顿？\n内存涨不涨？", SUCCESS),
        ("多人测试", "两人状态同步吗？\n权限正确吗？\n拔线后正常吗？", WARM),
        ("边界测试", "狂点按钮？\n中途加入？\n极端数值？", "#c084fc"),
    ]
    card_w, card_h = 190, 160
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(items):
        cx = start_x + i * (card_w + 26)
        cy = 100
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_ellipse(dwg, cx + card_w//2, cy + 32, 18, 18, fill=color, opacity=0.6)
        add_text(dwg, title, cx + card_w//2, cy + 74, fill="#fff", size=14, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, cy + 102 + j * 18, fill=TEXT_DIM, size=11.5, anchor="middle")

    add_rect(dwg, 100, 300, 700, 100, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "别只测「能玩」", 130, 330, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "能玩 ≠ 没问题：功能正确只是及格线，性能/多人/边界才是 VRChat 世界里翻车重灾区", 130, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "测试不是发布前的临时任务，而是每次改完代码都要做一遍的日常", 130, 382, fill=WARN, size=12.5)

    add_text(dwg, "原则：先自测 → 再朋友测 → 最后公开 —— 越多人测，问题暴露得越早", W//2, 450, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L01_01_test_types")


# ============================================================
# L01 — 图2: 测试流程（自测→朋友→公开）
# ============================================================
def make_L01_02_test_flow():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "测试流程：从自己到全世界", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "问题越早发现，修起来越便宜 —— 公开后一个 bug 等于几十个人帮你找", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    stages = [
        ("第 1 步 · 自测", "Play Mode + 本地测试\n自己把每个功能点过一遍", ACCENT),
        ("第 2 步 · 朋友测试", "双开 + 拉 1-2 个朋友\n测多人同步、权限、抢操作", SUCCESS),
        ("第 3 步 · 公开测试", "发布后叫朋友进世界\n收集真实反馈再迭代", WARM),
    ]
    box_w, box_h = 220, 150
    start_x = (W - (box_w * 3 + 40 * 2)) // 2
    for i, (title, desc, color) in enumerate(stages):
        x = start_x + i * (box_w + 40)
        add_rect(dwg, x, 100, box_w, box_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, 132, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + box_w//2, 164 + j * 20, fill=TEXT_DIM, size=11.5, anchor="middle")
        if i < 2:
            add_arrow(dwg, x + box_w + 6, 175, x + box_w + 34, 175, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 290, 700, 80, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "每一轮都记问题清单，改完再回到第 1 步重新自测", 130, 320, fill=WARN, size=13)
    add_text(dwg, "公开测试的反馈不只看「有没有 bug」—— 更要看「好不好玩、卡不卡、会不会迷路」", 130, 348, fill=TEXT_DIM, size=12.5)

    save_svg_and_png(dwg, "L01_02_test_flow")


# ============================================================
# L02 — 图1: Build & Test 流程
# ============================================================
def make_L02_01_build_test():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "Build & Test：一键本地测试世界", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "VRChat SDK 提供的最重要的测试工具 —— 不发布也能完整玩到你的世界", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 打开 SDK 菜单", "VRChat SDK\n→ Show Control Panel\n→ Build & Test", ACCENT),
        ("2. 选择场景", "确认构建的\n是当前场景", SUCCESS),
        ("3. 点击 Build & Test", "自动构建世界\n并启动 VRChat", WARM),
        ("4. 进入世界", "单人进入测试\n先自测全部功能", "#c084fc"),
    ]
    card_w, card_h = 190, 160
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 26)
        cy = 100
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 128, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 156 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 180, cx + card_w + 24, 180, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 300, 700, 80, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "Build & Test 启动的 VRChat 只有你自己能看到这个世界，可以放心乱试", 130, 330, fill=WARN, size=12.5)
    add_text(dwg, "提示：每次改完代码都 Build & Test 一次，别攒着一起测 —— 问题会互相掩盖", 130, 358, fill=TEXT_DIM, size=12.5)

    save_svg_and_png(dwg, "L02_01_build_test")


# ============================================================
# L02 — 图2: Console 窗口解读
# ============================================================
def make_L02_02_console():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "Console 窗口：错误都写在这里", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "Unity 把所有日志、警告、错误集中显示 —— 报错第一件事就是看它", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 左侧模拟窗口
    wx, wy, ww, wh = 60, 100, 430, 300
    add_rect(dwg, wx, wy, ww, wh, fill="#131313", stroke=BORDER, rx=8)
    add_rect(dwg, wx, wy, ww, 30, fill="#222222", stroke="none", rx=8)
    add_text(dwg, "Console", wx + 16, wy + 20, fill=TEXT_DIM, size=11.5, weight="bold")
    lines = [
        ("Clear | Collapse | Clear on Play", TEXT_MUTED, 10.5, False),
        ("[Info] Scene loaded: MyWorld", "#6ecfff", 11.5, False),
        ("[Warning] Material not found", WARN, 11.5, False),
        ("[Warning] 音频组件未赋值", WARN, 11.5, False),
        ("[Error] NullReferenceException", "#ff6b6b", 11.5, True),
        ("  at GameComponent.Update", "#ff8f8f", 10.5, False),
        ("[Info] Debug.Log 测试输出", "#6ecfff", 11.5, False),
    ]
    for i, (txt, col, size, bold) in enumerate(lines):
        yy = wy + 44 + i * 26
        add_text(dwg, txt, wx + 14, yy, fill=col, size=size, weight="bold" if bold else "normal")

    # 右侧解读
    rx = 540
    add_text(dwg, "怎么读这个窗口", rx, 100, fill=TEXT, size=14, weight="bold")
    reads = [
        ("Info（蓝）", "正常运行信息，可忽略或当调试输出", "#6ecfff"),
        ("Warning（黄）", "可能有隐患，如材质丢失、组件没赋值", WARN),
        ("Error（红）", "代码出错了，点开看堆栈定位", "#ff6b6b"),
        ("点行数", "跳转到出错的代码文件那一行", ACCENT),
    ]
    for i, (title, desc, color) in enumerate(reads):
        y = 128 + i * 52
        add_rect(dwg, rx - 10, y, 350, 40, fill=PANEL, stroke=BORDER, rx=6)
        add_ellipse(dwg, rx, y + 20, 5, 5, fill=color)
        add_text(dwg, title, rx + 14, y + 17, fill=color, size=12, weight="bold")
        add_text(dwg, desc, rx + 14, y + 33, fill=TEXT_DIM, size=10.5)

    add_rect(dwg, 60, 420 - 40, 780, 46, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "红色 Error 通常伴随「世界没反应」：先看 Console 再瞎猜，多数 bug 是「某个引用没连」", 450, 402, fill=WARN, size=12, anchor="middle")
    save_svg_and_png(dwg, "L02_02_console")


# ============================================================
# L03 — 图1: Stats 面板指标说明
# ============================================================
def make_L03_01_stats_panel():
    W, H = 900, 480
    dwg = new_svg(W, H)
    add_text(dwg, "Game 窗口 Stats 面板：性能体检表", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "Game 窗口右上角 → Stats，实时显示渲染与性能指标（运行时点击可停/续）", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 左侧模拟面板
    wx, wy, ww, wh = 60, 100, 330, 310
    add_rect(dwg, wx, wy, ww, wh, fill="#131313", stroke=BORDER, rx=8)
    add_rect(dwg, wx, wy, ww, 28, fill="#222222", stroke="none", rx=8)
    add_text(dwg, "Audio: 0.0 % DSP load", wx + 14, wy + 20, fill=TEXT_DIM, size=10.5)
    rows = [
        ("Draw Call", "42", ACCENT),
        ("SetPass calls", "31", ACCENT),
        ("Tris", "86.4 K", SUCCESS),
        ("Verts", "152 K", SUCCESS),
        ("Batches", "42", WARM),
        ("Saved by batching", "12", WARM),
        ("Shadow casters", "18", "#c084fc"),
        ("Visible skinned meshes", "6", "#c084fc"),
    ]
    for i, (k, v, c) in enumerate(rows):
        yy = wy + 40 + i * 31
        add_text(dwg, k, wx + 16, yy, fill=TEXT_DIM, size=11)
        add_text(dwg, v, wx + ww - 16, yy, fill=c, size=11, weight="bold", anchor="end")

    # 右侧解读
    rx = 460
    add_text(dwg, "重点看这三个", rx, 100, fill=TEXT, size=14, weight="bold")
    expl = [
        ("Draw Call", "引擎一次「画命令」，越小越好，VRChat 建议 < 60", ACCENT),
        ("SetPass calls", "切换着色器 pass 的次数，越高越伤 GPU", ACCENT),
        ("Tris 三角面数", "画面里的三角形数量，性能报告会给出评级", SUCCESS),
        ("Batches", "合并后的绘制批次，与 Draw Call 接近才正常", WARM),
    ]
    for i, (title, desc, color) in enumerate(expl):
        y = 124 + i * 76
        add_rect(dwg, rx - 10, y, 390, 66, fill=PANEL, stroke=color, rx=6, stroke_width=1.5)
        add_text(dwg, title, rx, y + 22, fill="#fff", size=12.5, weight="bold")
        add_text(dwg, desc, rx, y + 46, fill=TEXT_DIM, size=11)

    add_rect(dwg, 60, 424, 780, 40, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "心里要有一根线：Draw Call 破百就要警惕；点开 Frame Debugger 找到底是谁在刷", 450, 448, fill=WARN, size=12, anchor="middle")
    save_svg_and_png(dwg, "L03_01_stats_panel")


# ============================================================
# L03 — 图2: VRChat 性能报告示意
# ============================================================
def make_L03_02_perf_report():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "VRChat 性能报告 Performance Report", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "发布上传时自动生成：告诉 VRChat 你的世界有多「重」，别人能不能流畅打开", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 三个评级卡片
    cards = [
        ("整体评级", "Good / Poor\n按最差项决定", "#6bcf7f"),
        ("关卡/对象", "场景复杂度、\n碰撞体数量", ACCENT),
        ("图形", "材质、贴图、\n着色器复杂度", WARM),
        ("音频", "音频源数量、\n压缩格式", "#c084fc"),
    ]
    card_w, card_h = 190, 130
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(cards):
        cx = start_x + i * (card_w + 26)
        add_rect(dwg, cx, 100, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 130, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 158 + j * 18, fill=TEXT_DIM, size=11, anchor="middle")

    # 评级说明条
    badges = [
        ("Good", "绿 · 流畅运行", "#6bcf7f"),
        ("Medium", "黄 · 降级运行", "#ffcc66"),
        ("Poor", "红 · 可能卡顿", "#ff6b6b"),
    ]
    for i, (name, desc, color) in enumerate(badges):
        x = 130 + i * 230
        add_ellipse(dwg, x, 280, 8, 8, fill=color)
        add_text(dwg, f"{name}：{desc}", x + 18, 284, fill=TEXT_DIM, size=12)

    add_rect(dwg, 100, 310, 700, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "报出 Poor 不阻止发布，但玩家设备会降级渲染，甚至直接打不开", 130, 340, fill=WARN, size=12.5)
    add_text(dwg, "对标目标：全绿再上传。这份报告就是 VRChat 给你发的「体检单」，比任何人评论都权威", 130, 368, fill=TEXT_DIM, size=12.5)

    add_text(dwg, "细节：报告把光照/碰撞/性能预算逐项打分，点每一项能看具体原因", W//2, 435, fill=TEXT_MUTED, size=11.5, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L03_02_perf_report")


# ============================================================
# L03 — 图3: 性能杀手清单
# ============================================================
def make_L03_03_perf_killers():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "常见性能杀手清单", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "世界卡顿 90% 来自这几样 —— 先用它们排查，再考虑其他", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    items = [
        ("实时光源", "每个实时灯都是额外着色开销\n静态场景用烘焙光照替代", WARM, "高"),
        ("粒子系统", "粒子多 + 生命长 = 同时活跃量大\n限制数量与发射率", "#ff6b6b", "高"),
        ("材质数量", "材质越多 Draw Call 越多\n同类物体共用材质", ACCENT, "高"),
        ("贴图太大", "4K 贴图是内存杀手\n远处物体用 512/1024", SUCCESS, "中"),
        ("网格过细", "几万个面的模型毫无必要\n按距离做 LOD 简化", "#c084fc", "中"),
        ("透明物体", "透明 = 排序开销，越多越卡\n非必要不用透明", WARN, "中"),
    ]
    row_h = 42
    ys = 90
    for i, (name, desc, color, level) in enumerate(items):
        y = ys + i * (row_h + 8)
        add_rect(dwg, 60, y, 170, row_h, fill=PANEL, stroke=color, rx=8, stroke_width=2)
        add_text(dwg, name, 145, y + 27, fill="#fff", size=13, weight="bold", anchor="middle")
        add_rect(dwg, 245, y, 480, row_h, fill="#1a1a1a", stroke=BORDER, rx=8)
        add_text(dwg, desc.split("\n")[0], 260, y + 19, fill=TEXT_DIM, size=11.5)
        add_text(dwg, desc.split("\n")[1], 260, y + 36, fill=TEXT_MUTED, size=10.5)
        add_ellipse(dwg, 792, y + 22, 24, 15, fill=color, opacity=0.25)
        add_text(dwg, level, 792, y + 26, fill=color, size=11, weight="bold", anchor="middle")

    add_rect(dwg, 100, 392, 700, 50, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "性能细节见《渲染入门》第 4 篇 —— 排查顺序：粒子 → 材质 → 实时光 → 贴图", 450, 423, fill=WARN, size=12, anchor="middle")
    save_svg_and_png(dwg, "L03_03_perf_killers")


# ============================================================
# L04 — 图1: 上传发布流程
# ============================================================
def make_L04_01_publish_flow():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "上传发布：把世界交给全 VRChat", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "SDK 控制面板里走完三步，你的世界就出现在世界的公开列表里", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 填写信息", "世界名称 / 描述\n上传预览图", ACCENT),
        ("2. Build & Test", "最后再本地验证一次\n（这次一定要测）", SUCCESS),
        ("3. 点击 Publish", "构建并上传\n等待进度完成", WARM),
        ("4. 完成", "得到世界 ID\n别人可搜索进入", "#c084fc"),
    ]
    card_w, card_h = 190, 160
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 26)
        cy = 100
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 128, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 156 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 180, cx + card_w + 24, 180, stroke=color, stroke_width=2.5)

    add_rect(dwg, 100, 300, 700, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "首次发布必须要有「已通过的预览图」，名称和描述写清楚别人才能搜到", 130, 330, fill=WARN, size=12.5)
    add_text(dwg, "发布后世界立即上线，任何人搜索名字都能进来 —— 所以发布前务必完成全部测试", 130, 358, fill=TEXT_DIM, size=12.5)

    add_text(dwg, "菜单位置：VRChat SDK → Show Control Panel → Content Manager → 你的世界", W//2, 420, fill=TEXT_MUTED, size=11.5, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L04_01_publish_flow")


# ============================================================
# L04 — 图2: 版本更新流程
# ============================================================
def make_L04_02_update_flow():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "版本更新：改完就重新上传", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "VRChat 世界更新是「覆盖式」的 —— 没有版本号概念，重新 Publish 即可", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 修改内容", "改代码 / 改场景\n想清楚再动手", ACCENT),
        ("2. Build & Test", "本地验证新改动\n没测过不要传", SUCCESS),
        ("3. 重新 Publish", "同一世界 ID\n内容被覆盖", WARM),
        ("4. 进世界验证", "自己先进去确认\n新内容真的生效", "#c084fc"),
    ]
    card_w, card_h = 190, 160
    start_x = (W - (card_w * 4 + 26 * 3)) // 2
    for i, (title, desc, color) in enumerate(steps):
        cx = start_x + i * (card_w + 26)
        cy = 100
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, 128, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, 156 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, 180, cx + card_w + 24, 180, stroke=color, stroke_width=2.5)

    # 回环
    add_line(dwg, 690, 268, 170, 268, stroke=WARM, stroke_width=2, dash=[6, 4], with_arrow=True)
    add_rect(dwg, 350, 258, 160, 22, fill="#1e1e1e", stroke=BORDER, rx=11)
    add_text(dwg, "下次修改 → 再来一轮", 430, 275, fill="#bbbbbb", size=11, anchor="middle")

    add_rect(dwg, 100, 310, 700, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "覆盖式更新的后果：旧版本不存在！上传失败或漏传 = 世界还是旧内容", 130, 330, fill=WARN, size=12.5)
    add_text(dwg, "老玩家在更新前进入的世界仍是旧版（会话不重载），新进的人才是新版 —— 别以为重启就更新", 130, 358, fill=TEXT_DIM, size=12.5)

    add_text(dwg, "想安全改回旧版：上传前把工程备份好，或用 git 记录每次发布点", W//2, 420, fill=TEXT_MUTED, size=11.5, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L04_02_update_flow")


# ============================================================
# L05 — 图1: 实战步骤
# ============================================================
def make_L05_01_steps():
    W, H = 900, 512
    dwg = new_svg(W, H)
    add_text(dwg, "实战：完整发布一个世界", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "按顺序走完这 6 步，从「刚做完」到「全世界可玩」", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1. 备份工程", "复制工程文件夹\n或 git 提交存档", ACCENT),
        ("2. 性能检查", "Stats 面板\n性能报告全绿", SUCCESS),
        ("3. Build & Test", "单人进世界\n自测所有功能", WARM),
        ("4. 双开多人测试", "复制 VRChat 快捷方式\n加 -multi 参数", "#c084fc"),
        ("5. 上传发布", "填信息 → Publish\n等进度完成", "#ff9e4e"),
        ("6. 进世界验证", "自己重新进世界\n确认新内容生效", "#6bcf7f"),
    ]
    card_w, card_h = 270, 170
    start_x = (W - (card_w * 3 + 30 * 2)) // 2
    for i, (title, desc, color) in enumerate(steps):
        col, row = divmod(i, 3)
        cx = start_x + col * (card_w + 30)
        cy = 96 + row * (card_h + 24)
        add_rect(dwg, cx, cy, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, cx + card_w//2, cy + 32, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, cx + card_w//2, cy + 64 + j * 20, fill=TEXT_DIM, size=11.5, anchor="middle")
        if i < 3:
            add_arrow(dwg, cx + card_w + 2, cy + 85, cx + card_w + 28, cy + 85, stroke=color, stroke_width=2)

    add_rect(dwg, 100, 470, 700, 36, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "顺序不能乱：不备份就上传，翻车了连回滚都没得回", 450, 494, fill=WARN, size=12, anchor="middle")
    save_svg_and_png(dwg, "L05_01_steps")


# ============================================================
# L05 — 图2: 发布前检查清单
# ============================================================
def make_L05_02_checklist():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "发布前检查清单", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "全打勾再点 Publish —— 缺一项都可能翻车", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    items = [
        ("工程已备份（复制文件夹/git 提交）", SUCCESS),
        ("Console 无红色 Error", SUCCESS),
        ("Stats 面板 Draw Call 正常（< 60 左右）", SUCCESS),
        ("性能报告全绿或可接受", SUCCESS),
        ("Build & Test 单人玩过全部功能", SUCCESS),
        ("双开 / 朋友多人测过同步与权限", SUCCESS),
        ("边界情况：狂点按钮、中途加入、拔线", SUCCESS),
        ("世界名称、描述、预览图已填写", SUCCESS),
        ("首屏体验 OK：进世界第一眼不迷路", SUCCESS),
        ("确认发布的就是当前场景（最易被坑）", SUCCESS),
    ]
    for i, (txt, color) in enumerate(items):
        col, row = divmod(i, 5)
        x = 60 + col * 420
        y = 96 + row * 70
        add_rect(dwg, x, y, 380, 56, fill=PANEL, stroke=BORDER, rx=8)
        add_ellipse(dwg, x + 28, y + 28, 12, 12, fill=color, opacity=0.3)
        add_text(dwg, "✓", x + 28, y + 33, fill=color, size=14, weight="bold", anchor="middle")
        add_text(dwg, txt, x + 54, y + 26, fill="#fff", size=11.5, weight="bold")
        add_text(dwg, "已完成", x + 54, y + 44, fill=TEXT_MUTED, size=10)

    add_rect(dwg, 100, 464, 700, 62, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "最后一条最容易被坑：场景开错了，传上去的还是老世界", 450, 492, fill=WARN, size=12.5, anchor="middle")
    add_text(dwg, "检查清单可以打印贴屏幕边，每次发布对照一遍", 450, 514, fill=TEXT_MUTED, size=11, anchor="middle")
    save_svg_and_png(dwg, "L05_02_checklist")


# ============================================================
# L06 — 图1: 术语速查表
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "测试与发布术语速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    terms = [
        ("Build & Test", "SDK 一键构建并本地启动世界（不发布）", ACCENT),
        ("Publish", "上传世界到 VRChat，公开可搜索", ACCENT),
        ("Play Mode", "编辑器内直接运行场景，快速测逻辑", ACCENT),
        ("双开 / -multi", "复制快捷方式加参数，同时开两个 VRChat", ACCENT),
        ("Console", "Unity 日志窗口，看 Info/Warn/Error", SUCCESS),
        ("Stats 面板", "Game 窗口性能指标（Draw Call/Tris）", SUCCESS),
        ("Frame Debugger", "逐帧看每个绘制调用，找卡顿元凶", SUCCESS),
        ("性能报告", "上传时生成的关卡/图形/音频评级", SUCCESS),
        ("边界测试", "极端情况下测试：狂点、拔线、中途加入", WARM),
        ("版本更新", "重新 Publish 覆盖内容，无版本号概念", WARM),
        ("回滚", "恢复旧版内容（靠 git/备份）", WARM),
        ("预览图", "上传的世界缩略图，需审核通过", WARM),
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
# L06 — 图2: 常见问题对照表
# ============================================================
def make_L06_02_common_issues():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "常见问题对照表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    rows = [
        ("上传失败 / 报错", "网络问题或 SDK 版本过旧", "重试；更新 SDK 到最新版本", WARN),
        ("没有发布权限", "VRChat 账号没完成设置", "检查账号邮箱验证/内容创建者设置", WARN),
        ("世界太大传不上", "工程里有超大贴图/模型", "压缩贴图、清理未用资源后再传", ACCENT),
        ("别人说我世界卡", "性能报告或实测数据差", "看 Stats + 性能报告，逐个砍性能杀手", ACCENT),
        ("更新没生效", "老会话不重载 / 忘了重传", "重新进世界；确认重新 Publish 成功", SUCCESS),
        ("预览图不对", "图没上传或还在审核", "重新上传预览图并等审核通过", SUCCESS),
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

    add_text(dwg, "调试心法：先看 Console 报错，再看 Stats 数据，最后才问别人 —— 90% 的问题自己能查到", W//2, 544, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_02_common_issues")


# ============================================================
# L06 — 图3: 进阶路线图
# ============================================================
def make_L06_03_roadmap():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "进阶路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    stages = [
        ("入门 · 能测会传", "Build & Test + 双开\n完整走一遍发布流程", ACCENT, "现在"),
        ("熟练 · 会查性能", "Stats + Frame Debugger\n看懂性能报告并优化", SUCCESS, "1 周"),
        ("进阶 · 自动化测试", "网络同步边界测试\n多人玩法压力测试", WARM, "1 个月"),
        ("精通 · 全流程", "测试 → 发布 → 迭代\n运营自己的世界", "#c084fc", "长期"),
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
    add_text(dwg, "① 每次发布都按第 5 篇清单走  ② 卡了先看 Console 和 Stats，别乱猜", 130, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "③ 备份和 git 是回滚的唯一依靠  ④ 多玩别人的世界，观察它是卡还是顺", 130, 382, fill=TEXT_DIM, size=12.5)

    save_svg_and_png(dwg, "L06_03_roadmap")


if __name__ == "__main__":
    for f in [make_L01_01_test_types, make_L01_02_test_flow,
              make_L02_01_build_test, make_L02_02_console,
              make_L03_01_stats_panel, make_L03_02_perf_report, make_L03_03_perf_killers,
              make_L04_01_publish_flow, make_L04_02_update_flow,
              make_L05_01_steps, make_L05_02_checklist,
              make_L06_01_cheatsheet, make_L06_02_common_issues, make_L06_03_roadmap]:
        print(f"生成 {f.__name__} ...")
        f()
    print("全部完成")
