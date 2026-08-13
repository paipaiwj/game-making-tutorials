# -*- coding: utf-8 -*-
# Unity 色彩入门教程 — 配图生成脚本
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

def hsv_hex(h, s, v):
    r, g, b = colorsys_hsv(h, s, v)
    return "#%02x%02x%02x" % (r, g, b)

def colorsys_hsv(h, s, v):
    from colorsys import hsv_to_rgb
    r, g, b = hsv_to_rgb(h / 360.0, s / 100.0, v / 100.0)
    return int(r * 255), int(g * 255), int(b * 255)

def pie_slice(dwg, cx, cy, r, a0, a1, fill, stroke=BG, sw=3):
    a0r = math.radians(a0 - 90)
    a1r = math.radians(a1 - 90)
    x0 = cx + r * math.cos(a0r)
    y0 = cy + r * math.sin(a0r)
    x1 = cx + r * math.cos(a1r)
    y1 = cy + r * math.sin(a1r)
    d = f"M{cx},{cy} L{x0:.2f},{y0:.2f} A{r},{r} 0 0 1 {x1:.2f},{y1:.2f} Z"
    el = dwg.path(d=d, fill=fill, stroke=stroke, stroke_width=sw)
    dwg.add(el)
    return el

def swatch(dwg, x, y, w, h, color, label=None, lcolor=TEXT_DIM, lsize=11, rx=6):
    add_rect(dwg, x, y, w, h, fill=color, stroke="#000000", stroke_width=1, rx=rx)
    if label:
        add_text(dwg, label, x + w // 2, y + h + 16, fill=lcolor, size=lsize, anchor="middle")

def hue_stops():
    return [(0.0, "#ff4d4d", 1.0), (0.1667, "#ffd94d", 1.0), (0.3333, "#7dff4d", 1.0),
            (0.5, "#4dffe1", 1.0), (0.6667, "#4d7bff", 1.0), (0.8333, "#e14dff", 1.0),
            (1.0, "#ff4d4d", 1.0)]

def hex_to_rgb(c):
    return int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)

def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return "#%02x%02x%02x" % (int(r1 + (r2 - r1) * t), int(g1 + (g2 - g1) * t), int(b1 + (b2 - b1) * t))

def color_ramp(c1, c2, n):
    return [lerp_color(c1, c2, i / (n - 1)) for i in range(n)]

def hue_ramp(n):
    return [hsv_hex(360 * i / (n - 1), 100, 100) for i in range(n)]

def grad_bar(dwg, x, y, w, h, colors, rx=0):
    n = len(colors)
    seg = w / n
    for i, c in enumerate(colors):
        r = min(rx, seg / 2, h / 2) if (i == 0 or i == n - 1) else 0
        add_rect(dwg, x + i * seg, y, seg + 0.4, h, fill=c, stroke="none", rx=r)


# ============================================================
# L01 — 图1: 色轮（12 色环）
# ============================================================
def make_L01_01_color_wheel():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "色轮 Color Wheel：把颜色排成一个圈", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "12 色环 = 原色 + 二次色 + 三次色，配色方案的起点", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    cx, cy, r = 250, 330, 170
    for i in range(12):
        pie_slice(dwg, cx, cy, r, i * 30, (i + 1) * 30, hsv_hex(i * 30, 100, 96))
    add_ellipse(dwg, cx, cy, 62, 62, fill=BG, stroke="#3a3a3a", stroke_width=2)
    add_text(dwg, "12 色环", cx, cy - 6, fill=TEXT, size=14, weight="bold", anchor="middle")
    add_text(dwg, "每 30° 一个颜色", cx, cy + 16, fill=TEXT_MUTED, size=10.5, anchor="middle")

    add_text(dwg, "色环的三个层次", 500, 96, fill=TEXT, size=14, weight="bold")
    groups = [
        ("原色 Primary", ["#ff4d4d", "#ffd94d", "#4d7bff"], "红 黄 蓝 —— 无法用别的颜色混合出来"),
        ("二次色 Secondary", ["#ff9e4e", "#7dff4d", "#e14dff"], "橙 绿 紫 —— 原色两两混合"),
        ("三次色 Tertiary", ["#ff7d4d", "#b4ff4d", "#4dffe1"], "红橙 黄绿 青蓝 … 原色+二次色混合"),
    ]
    for i, (title, colors, desc) in enumerate(groups):
        y = 124 + i * 118
        add_rect(dwg, 490, y, 350, 98, fill=PANEL, stroke=BORDER, rx=8)
        add_text(dwg, title, 510, y + 26, fill="#fff", size=13, weight="bold")
        for j, c in enumerate(colors):
            add_rect(dwg, 510 + j * 66, y + 38, 58, 34, fill=c, stroke="#000", stroke_width=1, rx=4)
        add_text(dwg, desc, 510, y + 88, fill=TEXT_DIM, size=10.5)

    add_text(dwg, "看色轮画彩虹：红 → 橙 → 黄 → 绿 → 青 → 蓝 → 紫，回到红", W//2, 540, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L01_01_color_wheel")


# ============================================================
# L01 — 图2: HSV 三维示意
# ============================================================
def make_L01_02_hsv():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "HSV：一个颜色的三个数字", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "色相 Hue（什么颜色）· 饱和度 Saturation（多鲜艳）· 明度 Value（多亮）", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    bars = [
        ("H 色相", hue_ramp(25), "0° 红 → 60° 黄 → 120° 绿 → 180° 青 → 240° 蓝 → 300° 紫 → 360° 红", ACCENT),
        ("S 饱和度", [hsv_hex(210, s, 90) for s in range(0, 101, 5)], "左：灰蒙蒙   右：鲜艳 —— 饱和度越高越不「脏」", SUCCESS),
        ("V 明度", [hsv_hex(210, 80, v) for v in range(0, 101, 5)], "左：全黑   右：最亮 —— 明度是画面明暗对比的源头", WARM),
    ]
    y0 = 100
    for i, (title, colors, desc, color) in enumerate(bars):
        y = y0 + i * 96
        add_rect(dwg, 60, y, 780, 74, fill=PANEL, stroke=BORDER, rx=8)
        add_text(dwg, title, 90, y + 26, fill="#fff", size=13.5, weight="bold")
        add_rect(dwg, 190, y + 12, 440, 26, fill="#1a1a1a", stroke=BORDER, rx=13)
        grad_bar(dwg, 190, y + 12, 440, 26, colors, rx=13)
        add_text(dwg, desc, 90, y + 62, fill=TEXT_DIM, size=11.5)

    add_rect(dwg, 60, 396, 780, 96, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "三个数一起变，才是完整的颜色", 90, 426, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "调色口诀：想要别的颜色 → 动 H；想要不脏 → 提高 S；想要亮暗 → 动 V", 90, 456, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "Unity 颜色面板里可以随时切换 RGB / HSV 两种模式", 90, 478, fill=WARN, size=12.5)

    add_text(dwg, "HSV 对应现实认知：人眼先识别颜色（H），再看鲜艳度（S）和亮暗（V）", W//2, 534, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L01_02_hsv")


# ============================================================
# L02 — 图1: 五大配色方案
# ============================================================
def make_L02_01_schemes():
    W, H = 900, 700
    dwg = new_svg(W, H)
    add_text(dwg, "五大配色方案", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "在色轮上取色，按几何关系搭配 —— 先选方案，再挑颜色", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    rows = [
        ("单色 Monochromatic", "同一色相，只变饱和度和明度", ["#1a3a8a", "#2e5fd6", "#4ea1ff", "#9ecbff", "#d6e9ff"], "干净、专业、容易统一，适合 UI 和仪表盘", ACCENT),
        ("互补 Complementary", "色轮上相对的两个颜色（180°）", ["#e74c3c", "#ff8a7a", "#c0392b", "#4ea1ff", "#9ecbff"], "对比最强、最醒目，适合按钮、血条、阵营对立", WARM),
        ("近似 Analogous", "色轮上相邻的几个颜色", ["#ffd94d", "#9acd32", "#2e8b57", "#26c6da", "#3a7bd5"], "和谐自然，适合场景远景、树木草地", SUCCESS),
        ("三角 Triadic", "色轮上 120° 间隔的三个颜色", ["#e74c3c", "#ffd94d", "#4d7bff"], "活泼均衡、色彩丰富，适合角色区分、儿童游戏", "#c084fc"),
        ("分裂互补 Split", "一个主色 + 互补色两侧的两个", ["#4d7bff", "#ffb04d", "#ff7d4d", "#2e5fd6"], "对比柔和些，既醒目又耐看，适合氛围场景", "#ff88cc"),
    ]
    y0 = 92
    row_h = 112
    gap = 8
    def sw_for(n):
        return 110 if n == 3 else (80 if n == 4 else 70)
    for i, (name, rule, colors, style, color) in enumerate(rows):
        y = y0 + i * row_h
        add_rect(dwg, 60, y, 780, row_h - 12, fill=PANEL, stroke=color, rx=10, stroke_width=1.8)
        add_text(dwg, name, 84, y + 28, fill="#fff", size=14, weight="bold")
        add_text(dwg, rule, 84, y + 52, fill=TEXT_DIM, size=11.5)
        sw = sw_for(len(colors))
        start_x = 470 - (len(colors) * sw + (len(colors) - 1) * gap) // 2
        for j, c in enumerate(colors):
            add_rect(dwg, start_x + j * (sw + gap), y + 16, sw, 54, fill=c, stroke="#000", stroke_width=1, rx=7)
        add_text(dwg, style, 84, y + 88, fill=WARN, size=11.5)

    add_text(dwg, "记住：方案决定「颜色之间的关系」，具体色相由场景情绪决定", 60, H - 24, fill=TEXT_MUTED, size=12, italic=True)
    save_svg_and_png(dwg, "L02_01_schemes")


# ============================================================
# L02 — 图2: 配色用途对比
# ============================================================
def make_L02_02_usage():
    W, H = 900, 600
    dwg = new_svg(W, H)
    add_text(dwg, "配色方案怎么选？看用途", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "同一个游戏里，不同用途可以用不同方案 —— 先定功能，再定方案", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    rows = [
        ("单色", "UI 面板 / 数据界面", "信息要清楚，不能抢戏", ["#2e5fd6", "#4ea1ff", "#9ecbff"], ACCENT),
        ("互补", "按钮 / 血条 / 阵营", "一眼分出「我方 / 敌方」", ["#e74c3c", "#4ea1ff", "#9ecbff"], WARM),
        ("近似", "场景远景 / 植被材质", "看着自然舒服，不刺眼", ["#9acd32", "#2e8b57", "#26c6da"], SUCCESS),
        ("三角", "角色 / 物品区分", "颜色多但依然均衡", ["#e74c3c", "#ffd94d", "#4d7bff"], "#c084fc"),
        ("分裂互补", "氛围场景主色", "有对比但耐看，可久视", ["#4d7bff", "#ffb04d", "#ff7d4d"], "#ff88cc"),
    ]
    y0 = 92
    row_h = 84
    for i, (name, use, why, colors, color) in enumerate(rows):
        y = y0 + i * row_h
        add_rect(dwg, 60, y, 780, row_h - 10, fill=PANEL, stroke=BORDER, rx=8)
        add_rect(dwg, 76, y + 14, 96, 44, fill="#1a1a1a", stroke=color, rx=6, stroke_width=1.5)
        add_text(dwg, name, 124, y + 42, fill="#fff", size=13, weight="bold", anchor="middle")
        add_text(dwg, use, 210, y + 30, fill=TEXT, size=12.5, weight="bold")
        add_text(dwg, why, 210, y + 52, fill=TEXT_DIM, size=11)
        for j, c in enumerate(colors):
            add_rect(dwg, 620 + j * 50, y + 14, 40, 44, fill=c, stroke="#000", stroke_width=1, rx=6)

    add_rect(dwg, 60, 514, 780, 60, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "举例：抢答小游戏 = 单色 UI + 互补的「对/错」反馈 + 近似色的场景", 450, 542, fill=WARN, size=12.5, anchor="middle")
    add_text(dwg, "Unity 里取色：右键任意颜色字段 → Copy Color，Ctrl+V 粘贴到别的颜色框", 450, 564, fill=TEXT_DIM, size=11.5, anchor="middle")
    save_svg_and_png(dwg, "L02_02_usage")


# ============================================================
# L03 — 图1: 冷暖色对比
# ============================================================
def make_L03_01_warm_cold():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "冷暖色：颜色也有「温度」", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "暖色 = 热情 / 危险 / 温暖   冷色 = 平静 / 神秘 / 疏离", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 暖色组
    add_rect(dwg, 60, 92, 380, 300, fill="#3a2416", stroke="#ff7043", rx=12, stroke_width=2)
    add_text(dwg, "暖色 Warm", 250, 124, fill="#ffb74d", size=16, weight="bold", anchor="middle")
    warm_cols = [("#ff5252", "红 刺激·紧急"), ("#ff9800", "橙 活力·食欲"), ("#ffd740", "黄 快乐·注意")]
    for i, (c, t) in enumerate(warm_cols):
        add_rect(dwg, 90 + i * 118, 150, 100, 76, fill=c, stroke="#000", stroke_width=1, rx=8)
        add_text(dwg, t, 140 + i * 118, 254, fill="#ffd0b0", size=11, anchor="middle")
    add_text(dwg, "→ 篝火、夕阳、警告灯、爆炸特效", 250, 292, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "→ 离得近的感觉、紧张感", 250, 316, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "→ 危险区、血量低、热源", 250, 340, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "暖色向观众「靠近」", 250, 372, fill="#ff8a50", size=12, weight="bold", anchor="middle")

    # 冷色组
    add_rect(dwg, 460, 92, 380, 300, fill="#16233a", stroke="#4ea1ff", rx=12, stroke_width=2)
    add_text(dwg, "冷色 Cool", 650, 124, fill="#9ecbff", size=16, weight="bold", anchor="middle")
    cold_cols = [("#4d7bff", "蓝 平静·理性"), ("#26c6da", "青 凉爽·科技"), ("#9575cd", "紫 神秘·梦幻")]
    for i, (c, t) in enumerate(cold_cols):
        add_rect(dwg, 490 + i * 118, 150, 100, 76, fill=c, stroke="#000", stroke_width=1, rx=8)
        add_text(dwg, t, 540 + i * 118, 254, fill="#b0d0ff", size=11, anchor="middle")
    add_text(dwg, "→ 月光、水面、深夜、冰霜", 650, 292, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "→ 安静的感觉、孤独感", 650, 316, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "→ 安全区、血量高、冷静", 650, 340, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "冷色向远处「退去」", 650, 372, fill="#4ea1ff", size=12, weight="bold", anchor="middle")

    add_rect(dwg, 60, 416, 780, 108, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "场景里的用法", 90, 446, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "① 主光暖、阴影冷 —— 画面立刻有层次  ② 前景暖 / 远景冷 —— 拉开纵深", 90, 476, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "③ 用冷暖对比引导视线：最亮最暖的地方，就是玩家该看的地方", 90, 500, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L03_01_warm_cold")


# ============================================================
# L03 — 图2: 三种氛围
# ============================================================
def make_L03_02_mood():
    W, H = 900, 680
    dwg = new_svg(W, H)
    add_text(dwg, "色彩情绪：同一片场景，三种颜色三种气氛", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "色相定「是什么氛围」，饱和度定「多强烈」，明度定「多暗」", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    moods = [
        ("温馨 Cozy", "暖色 + 高饱和", ["#ff7043", "#ffb74d", "#ffe0a3", "#8d6e63"], "温暖、安全、亲切、食欲", "壁炉旁、咖啡店、黄昏村庄", "#ffb74d", "#3a2416"),
        ("恐怖 Horror", "冷色 + 低饱和", ["#3b4a5a", "#4a4e69", "#2f2f35", "#6b6b6b"], "压抑、不安、孤独、危险", "废弃医院、深夜森林、密室", "#9aa0a6", "#1a1a22"),
        ("科技 Tech", "青色 + 霓虹", ["#00e5ff", "#00b0ff", "#7c4dff", "#0d1b2a"], "未来、冷静、精密、酷炫", "赛博都市、实验室、数据世界", "#00e5ff", "#0a1628"),
    ]
    start_x = 60
    card_w = 780
    card_h = 170
    for i, (title, rule, colors, words, example, accent, cardbg) in enumerate(moods):
        y = 92 + i * (card_h + 18)
        add_rect(dwg, start_x, y, card_w, card_h, fill=PANEL, stroke=accent, rx=10, stroke_width=1.8)
        add_text(dwg, title, 90, y + 30, fill="#fff", size=15, weight="bold")
        add_text(dwg, rule, 90, y + 56, fill=TEXT_DIM, size=12)
        for j, c in enumerate(colors):
            add_rect(dwg, 90 + j * 58, y + 74, 48, 66, fill=c, stroke="#000", stroke_width=1, rx=6)
        add_text(dwg, "情绪词：" + words, 420, y + 92, fill=accent, size=12, weight="bold")
        add_text(dwg, "参考场景：" + example, 420, y + 116, fill=TEXT_DIM, size=11.5)
        tips = ["暖色 + 高饱和 = 亲切温暖", "冷色 + 低饱和 + 低明度 = 压抑", "青色 + 高饱和 = 未来感"]
        add_text(dwg, tips[i], 420, y + 140, fill=TEXT_MUTED, size=11)

    add_text(dwg, "VRChat 里最经典的恐怖世界，几乎都是「低饱和蓝绿 + 极低明度」", W//2, H - 22, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L03_02_mood")


# ============================================================
# L04 — 图1: Unity 颜色面板示意
# ============================================================
def make_L04_01_unity_color():
    W, H = 900, 600
    dwg = new_svg(W, H)
    add_text(dwg, "Unity 颜色面板 Color 控件", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "选中材质/灯光/天空盒，点开颜色字段即可看到", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 主面板
    add_rect(dwg, 60, 90, 780, 360, fill="#2f2f2f", stroke="#4ea1ff", rx=10, stroke_width=1.8)
    add_text(dwg, "Color", 90, 122, fill="#fff", size=14, weight="bold")

    # 色轮（简化：12 扇形 + 中心明度圆）
    cx, cy, r = 190, 330, 110
    for i in range(12):
        pie_slice(dwg, cx, cy, r, i * 30, (i + 1) * 30, hsv_hex(i * 30, 100, 92), stroke="#2f2f2f", sw=2)
    add_ellipse(dwg, cx, cy, 34, 34, fill="#4ea1ff", stroke="#ffffff", stroke_width=1.5)
    add_text(dwg, "拖动选择\n色相+饱和度", cx, cy + 50, fill="#ffffff", size=10, anchor="middle")

    # 右侧滑块区
    sx = 340
    sliders = [
        ("R", 255, "#ff5252", color_ramp("#000000", "#ff5252", 21)),
        ("G", 128, "#4dff4d", color_ramp("#000000", "#4dff4d", 21)),
        ("B", 96, "#4d7bff", color_ramp("#000000", "#4d7bff", 21)),
    ]
    sy = 140
    for i, (ch, val, color, colors) in enumerate(sliders):
        y = sy + i * 58
        add_text(dwg, ch, sx, y + 18, fill=color, size=13, weight="bold")
        add_text(dwg, str(val), sx + 10, y + 18, fill=TEXT_DIM, size=12)
        add_rect(dwg, sx + 40, y + 4, 310, 18, fill="#1a1a1a", stroke=BORDER, rx=9)
        grad_bar(dwg, sx + 40, y + 4, 310, 18, colors, rx=9)
        add_rect(dwg, sx + 40 + int(310 * val / 255), y + 0, 6, 26, fill="#ffffff", stroke="#000", stroke_width=1, rx=3)

    # HSV 模式滑块（简化）
    add_text(dwg, "HSV 模式（点面板右上角 ⇄ 切换）", sx, sy + 3 * 58 + 20, fill="#9ecbff", size=12, weight="bold")
    hsv_rows = [("H", "210°", hue_ramp(21)), ("S", "88%", [hsv_hex(210, s, 90) for s in range(0, 101, 5)])]
    for i, (ch, val, colors) in enumerate(hsv_rows):
        y = sy + 3 * 58 + 44 + i * 52
        add_text(dwg, ch, sx, y + 16, fill="#9ecbff", size=13, weight="bold")
        add_text(dwg, val, sx + 10, y + 16, fill=TEXT_DIM, size=12)
        add_rect(dwg, sx + 40, y + 2, 310, 18, fill="#1a1a1a", stroke=BORDER, rx=9)
        grad_bar(dwg, sx + 40, y + 2, 310, 18, colors, rx=9)
        add_rect(dwg, sx + 40 + 240, y - 2, 6, 26, fill="#ffffff", stroke="#000", stroke_width=1, rx=3)

    # 预览色块
    add_rect(dwg, 60, 96 + 0, 90, 60, fill="#4e7dd6", stroke="#fff", stroke_width=1.5, rx=6)
    add_text(dwg, "当前颜色", 105, 112, fill="#ffffff", size=11, weight="bold")
    add_text(dwg, "#4E7DD6", 105, 134, fill="#ffffff", size=10.5)

    add_rect(dwg, 60, 474, 780, 56, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "取色器 Eyedropper：点面板左下角吸管，在 Game 视图里点任意物体即可取色", 450, 500, fill=WARN, size=12.5, anchor="middle")
    add_text(dwg, "把「Hex 码」记下来，材质与灯光用同一颜色时直接粘贴，保证统一", 450, 522, fill=TEXT_DIM, size=11.5, anchor="middle")
    save_svg_and_png(dwg, "L04_01_unity_color")


# ============================================================
# L04 — 图2: 灯光色温对比
# ============================================================
def make_L04_02_light_temperature():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "灯光色温：用 K（开尔文）控制冷暖", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "K 值越低越暖（橙），K 值越高越冷（蓝）—— 和直觉相反，记住就行", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    # 两张对比卡
    warm_cols = color_ramp("#ff6a2a", "#ffd9b0", 21)
    add_rect(dwg, 60, 92, 380, 190, fill=PANEL, stroke=WARM, rx=12, stroke_width=2)
    add_text(dwg, "暖光 3200K（夕阳 / 篝火）", 250, 122, fill="#ffd9b0", size=15, weight="bold", anchor="middle")
    grad_bar(dwg, 90, 140, 320, 90, warm_cols, rx=8)
    add_text(dwg, "→ 傍晚露营、室内烛光、温馨的小屋", 250, 260, fill=TEXT_DIM, size=12, anchor="middle")

    cold_cols = color_ramp("#b0d0ff", "#3a5fd6", 21)
    add_rect(dwg, 460, 92, 380, 190, fill=PANEL, stroke=ACCENT, rx=12, stroke_width=2)
    add_text(dwg, "冷光 6500K（阴天 / 月光）", 650, 122, fill="#b0d0ff", size=15, weight="bold", anchor="middle")
    grad_bar(dwg, 490, 140, 320, 90, cold_cols, rx=8)
    add_text(dwg, "→ 深夜森林、废墟、冷静的实验室", 650, 260, fill=TEXT_DIM, size=12, anchor="middle")

    # 色温刻度条
    add_text(dwg, "常见色温参考", 90, 320, fill=TEXT, size=14, weight="bold")
    temp_keys = ["#ff8a3a", "#ffc37a", "#ffe8c9", "#fff0d6", "#b0d0ff", "#5a7fff"]
    temp_cols = []
    for i in range(len(temp_keys) - 1):
        temp_cols += color_ramp(temp_keys[i], temp_keys[i + 1], 5)[:-1]
    temp_cols.append(temp_keys[-1])
    add_rect(dwg, 90, 338, 720, 22, fill="#1a1a1a", stroke=BORDER, rx=11)
    grad_bar(dwg, 90, 338, 720, 22, temp_cols, rx=11)
    marks = [("2000K", "烛光", 90), ("3200K", "暖白·夕阳", 300), ("5500K", "正午日光", 450), ("6500K", "阴天·默认", 590), ("10000K", "蓝色阴影", 790)]
    for label, sub, x in marks:
        add_text(dwg, label, x, 382, fill=TEXT, size=11.5, weight="bold", anchor="middle")
        add_text(dwg, sub, x, 400, fill=TEXT_MUTED, size=10, anchor="middle")

    add_rect(dwg, 60, 424, 780, 96, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "Unity 操作", 90, 454, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "选中 Directional Light → 勾选 Use Color Temperature → 拖动 Temperature 到想要的 K 值", 90, 482, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "小技巧：白天世界用 5500~6500K；想渲染黄昏/清晨，把主光降到 3000~3500K", 90, 506, fill=WARN, size=12.5)
    save_svg_and_png(dwg, "L04_02_light_temperature")


# ============================================================
# L05 — 图1: 实战五步
# ============================================================
def make_L05_01_steps():
    W, H = 900, 540
    dwg = new_svg(W, H)
    add_text(dwg, "实战流程：给露营场景定色调", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "按顺序走五步，不要跳步 —— 从情绪出发，到后处理收尾", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    steps = [
        ("1 定情绪", "想要什么感觉？\n温馨？神秘？", WARM),
        ("2 选配色方案", "主色+辅色+强调\n近似或分裂互补", ACCENT),
        ("3 天空+主光", "天空盒颜色\n主光色温 3000K", SUCCESS),
        ("4 材质统一色板", "所有材质\n只从色板取色", "#c084fc"),
        ("5 后处理微调", "曝光/对比/白平衡\n色调映射收尾", "#ff88cc"),
    ]
    card_w, card_h = 156, 190
    start_x = (W - (card_w * 5 + 14 * 4)) // 2
    for i, (title, desc, color) in enumerate(steps):
        x = start_x + i * (card_w + 14)
        add_rect(dwg, x, 90, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 118, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 148 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")
        if i < 4:
            add_arrow(dwg, x + card_w + 2, 185, x + card_w + 12, 185, stroke=color, stroke_width=2)

    add_rect(dwg, 60, 312, 780, 180, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "每一步检查什么", 90, 342, fill=SUCCESS, size=14, weight="bold")
    checks = [
        ("① 定情绪后：把「温馨」「神秘」写进需求文档，之后所有调色都对照它", ACCENT),
        ("② 选好方案后：色板最多 5 个色相，先存成截图贴在屏幕旁", SUCCESS),
        ("③ 天空+主光后：先不管材质，场景整体氛围已经出现", WARM),
        ("④ 材质统一后：任何颜色都从色板取，禁止手写其他颜色", "#c084fc"),
        ("⑤ 后处理最后做：材质没统一前，调后处理是白费功夫", "#ff88cc"),
    ]
    for i, (txt, color) in enumerate(checks):
        add_text(dwg, txt, 110, 372 + i * 22, fill=TEXT_DIM, size=12)

    add_text(dwg, "顺序不能反：先整体后细节，先灯光后后期", W//2, 518, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L05_01_steps")


# ============================================================
# L05 — 图2: 露营场景色板
# ============================================================
def make_L05_02_palette():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "露营场景色板（夜晚 · 篝火）", W//2, 34, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "情绪：温馨 + 一点神秘 —— 暖色篝火 + 冷色夜空", W//2, 64, fill=TEXT_DIM, size=13, anchor="middle")

    add_text(dwg, "主色（大面积 · 天空/远景/地面）", 90, 96, fill=ACCENT, size=13, weight="bold")
    mains = [
        ("#1c2b4a", "夜空深蓝", "天空盒/远景\n大面积底色"),
        ("#2f4a3a", "树影墨绿", "树木/灌木\n植被"),
        ("#8a6a4f", "大地暖棕", "地面/木台\n帐篷帆布"),
    ]
    for i, (c, name, use) in enumerate(mains):
        x = 90 + i * 250
        add_rect(dwg, x, 108, 220, 96, fill=c, stroke="#000", stroke_width=1, rx=8)
        add_text(dwg, name, x + 110, 230, fill="#fff", size=12.5, weight="bold", anchor="middle")
        for j, line in enumerate(use.split("\n")):
            add_text(dwg, line, x + 110, 250 + j * 16, fill=TEXT_DIM, size=10.5, anchor="middle")

    add_text(dwg, "辅色（中等面积 · 细节材质）", 90, 292, fill=SUCCESS, size=13, weight="bold")
    subs = [
        ("#5a3e2b", "木柴深棕", "桌椅/栅栏", "#ffffff"),
        ("#a88b6a", "原木浅棕", "地板/木桶", "#2b2b2b"),
        ("#4a5d46", "草绿", "草地小面积", "#ffffff"),
    ]
    for i, (c, name, use, tcolor) in enumerate(subs):
        x = 90 + i * 250
        add_rect(dwg, x, 304, 220, 60, fill=c, stroke="#000", stroke_width=1, rx=8)
        add_text(dwg, name, x + 12, 330, fill=tcolor, size=12, weight="bold")
        add_text(dwg, use, x + 12, 352, fill=tcolor, size=10.5)

    add_text(dwg, "强调色（小面积 · 光源和交互物）", 90, 396, fill=WARM, size=13, weight="bold")
    accs = [
        ("#ff8c42", "篝火橙", "火焰/火把/交互物"),
        ("#ffd166", "暖黄", "灯光/火苗亮部"),
        ("#ffe8d6", "暖白", "高光/最亮处"),
    ]
    for i, (c, name, use) in enumerate(accs):
        x = 90 + i * 250
        add_rect(dwg, x, 408, 220, 60, fill=c, stroke="#000", stroke_width=1, rx=8)
        add_text(dwg, name, x + 12, 434, fill="#1e1e1e", size=12, weight="bold")
        add_text(dwg, use, x + 12, 456, fill="#333333", size=10.5)

    add_rect(dwg, 60, 486, 780, 52, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "面积比大约 6:3:1 —— 主色占 60%、辅色 30%、强调色 10%，画面才稳", 450, 516, fill=WARN, size=12.5, anchor="middle")
    save_svg_and_png(dwg, "L05_02_palette")


# ============================================================
# L06 — 图1: 术语速查
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 900, 640
    dwg = new_svg(W, H)
    add_text(dwg, "色彩术语速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "12 个高频词，配图对照记忆", W//2, 60, fill=TEXT_DIM, size=13, anchor="middle")

    terms = [
        ("色相 Hue", "颜色本身：红/橙/黄/绿…", ACCENT),
        ("饱和度 Saturation", "鲜艳程度：0% 灰 → 100% 纯", ACCENT),
        ("明度 Value", "亮暗程度：0% 黑 → 100% 最亮", ACCENT),
        ("色环 Color Wheel", "12 色排列成环，配色的地图", ACCENT),
        ("冷暖色", "暖=热情危险，冷=平静神秘", WARM),
        ("互补色", "色轮相对（180°），对比最强", WARM),
        ("近似色", "色轮相邻，和谐自然", WARM),
        ("三角配色", "120° 间隔三色，活泼均衡", WARM),
        ("色温 K 值", "灯光冷暖：低=暖橙，高=冷蓝", SUCCESS),
        ("白平衡", "把「白色」调回真正的白", SUCCESS),
        ("色调映射 Tonemap", "HDR 高光压回可见范围", SUCCESS),
        ("色板 Palette", "固定一组颜色，全局只用它", SUCCESS),
    ]
    col_w = 390
    for i, (term, desc, color) in enumerate(terms):
        row, col = divmod(i, 3)
        x = 60 + col * (col_w + 30)
        y = 84 + row * 82
        add_rect(dwg, x, y, col_w, 64, fill=PANEL, stroke=color, rx=8, stroke_width=1.5)
        add_text(dwg, term, x + 16, y + 26, fill="#fff", size=13, weight="bold")
        add_text(dwg, desc, x + 16, y + 48, fill=TEXT_DIM, size=11)

    add_text(dwg, "记不住没关系 —— 需要时回来查，用多了自然记住", W//2, H - 22, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_01_cheatsheet")


# ============================================================
# L06 — 图2: 常见问题对照表
# ============================================================
def make_L06_02_common_issues():
    W, H = 900, 620
    dwg = new_svg(W, H)
    add_text(dwg, "常见问题对照表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "看到问题 → 查原因 → 按方法修", W//2, 60, fill=TEXT_DIM, size=13, anchor="middle")

    rows = [
        ("颜色发灰、脏", "饱和度低 + 明度太接近", "提高 S，拉开明度差（亮处更亮暗处更暗）", WARN),
        ("画面过曝发白", "灯光太强 / 后处理曝光过高", "主光强度降到 0.5~1，曝光 -0.5 起调", WARN),
        ("颜色又脏又土", "色相太多、太杂", "限定 2~3 个色相，建色板统一取色", ACCENT),
        ("灯光总是偏色", "色温 K 值没调对", "白天 5500~6500K，黄昏 3000~3500K", ACCENT),
        ("整体统一感差", "材质颜色各自为战", "共用色板 + 最后统一调色节点", SUCCESS),
        ("色盲玩家看不清", "只用颜色做区分", "加形状/亮度/图标辅助信息", SUCCESS),
    ]
    col_w = [170, 290, 320]
    xs = [60, 245, 550]
    for hd, x in zip(["问题现象", "常见原因", "解决办法"], xs):
        add_rect(dwg, x, 84, col_w[0], 34, fill=PANEL, stroke=ACCENT, stroke_width=1.5)
        add_text(dwg, hd, x + col_w[0]//2, 106, fill=ACCENT, size=13, weight="bold", anchor="middle")
    for i, (prob, cause, sol, color) in enumerate(rows):
        y = 118 + i * 74
        add_rect(dwg, 60, y, col_w[0], 64, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, prob, 60 + col_w[0]//2, y + 36, fill="#fff", size=12, weight="bold", anchor="middle")
        add_rect(dwg, 245, y, col_w[1], 64, fill=PANEL, stroke=BORDER, rx=6)
        add_text(dwg, cause, 245 + col_w[1]//2, y + 36, fill=TEXT_DIM, size=11.5, anchor="middle")
        add_rect(dwg, 550, y, col_w[2], 64, fill=PANEL, stroke=color, rx=6)
        add_text(dwg, sol, 550 + col_w[2]//2, y + 36, fill=color, size=11.5, anchor="middle")

    add_text(dwg, "调色心法：先解决「最亮和最暗」，再调中间层次 —— 对比对了，画面就立住了", W//2, 604, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_02_common_issues")


# ============================================================
# L06 — 图3: 进阶路线图
# ============================================================
def make_L06_03_roadmap():
    W, H = 900, 520
    dwg = new_svg(W, H)
    add_text(dwg, "色彩进阶路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "从会用工具，到有自己的风格", W//2, 60, fill=TEXT_DIM, size=13, anchor="middle")

    stages = [
        ("入门 · 会用色", "HSV 三参数\n认得出 12 色环", ACCENT, "本课完成"),
        ("熟练 · 会配色", "五大方案随手用\n能定场景情绪", SUCCESS, "约 1 周"),
        ("进阶 · 会调光", "色温/天空盒/环境光\n后处理全链路", WARM, "约 1 个月"),
        ("精通 · 有风格", "自建色板库\n风格化 Look 调色", "#c084fc", "长期"),
    ]
    box_w, box_h = 180, 150
    start_x = (W - (box_w * 4 + 30 * 3)) // 2
    for i, (title, desc, color, time) in enumerate(stages):
        x = start_x + i * (box_w + 30)
        y = 92
        add_rect(dwg, x, y, box_w, box_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, y + 28, fill="#fff", size=13, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + box_w//2, y + 58 + j * 19, fill=TEXT_DIM, size=11, anchor="middle")
        add_text(dwg, time, x + box_w//2, y + box_h - 14, fill=color, size=11, anchor="middle")
        if i < 3:
            add_arrow(dwg, x + box_w + 2, y + box_h//2, x + box_w + 28, y + box_h//2, stroke=color, stroke_width=2)

    add_rect(dwg, 60, 288, 780, 170, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "练习建议", 90, 318, fill=SUCCESS, size=14, weight="bold")
    adds = [
        "① 每个场景先写一句话情绪（温馨/恐怖/科技…），再动手调色",
        "② 收集喜欢游戏的截图，用取色器拆它的色板，模仿配色",
        "③ 一个场景尝试 2 种情绪版本：同样布局，调色后完全不同",
        "④ 调色后截图对比：把「调色前/后」并排看，进步最快",
        "⑤ 遵守 6:3:1 面积比，颜色越多越难统一",
    ]
    for i, txt in enumerate(adds):
        add_text(dwg, txt, 90, 346 + i * 22, fill=TEXT_DIM, size=12)

    add_text(dwg, "色彩是美术的「全局变量」—— 学会它，你的世界立刻有质感", W//2, 492, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_03_roadmap")


if __name__ == "__main__":
    for f in [make_L01_01_color_wheel, make_L01_02_hsv,
              make_L02_01_schemes, make_L02_02_usage,
              make_L03_01_warm_cold, make_L03_02_mood,
              make_L04_01_unity_color, make_L04_02_light_temperature,
              make_L05_01_steps, make_L05_02_palette,
              make_L06_01_cheatsheet, make_L06_02_common_issues, make_L06_03_roadmap]:
        print(f"生成 {f.__name__} ...")
        f()
    print("全部完成")
