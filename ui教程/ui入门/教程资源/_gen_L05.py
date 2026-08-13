# -*- coding: utf-8 -*-
"""L05 配图生成器：Slider / InputField / Toggle / Selectable / Comparison。
基于 _render_svg 工具，输出 SVG（可编辑源）+ PNG（站点引用）。"""
import os
import sys
# _render_svg.py 跟 _gen_L05.py 在同一目录
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _render_svg import (
    new_svg, add_text, add_rect, add_line, add_arrow,
    add_ellipse, save_svg_and_png,
    BG, PANEL, BORDER, ACCENT, WARM, SUCCESS, WARN, TEXT, TEXT_DIM, TEXT_MUTED,
)


def make_slider_structure():
    """L05_01: Slider 内部结构图。"""
    W, H = 900, 380
    dwg = new_svg(W, H)
    add_text(dwg, "Slider 内部结构", W // 2, 36, fill=TEXT, size=20,
             weight="bold", anchor="middle")
    # Slider 容器框
    cx, cy, cw, ch = 80, 130, 740, 120
    add_rect(dwg, cx, cy, cw, ch, fill=PANEL, stroke=ACCENT, rx=4, stroke_width=2)
    add_text(dwg, "Slider", cx + 12, cy + 22, fill=TEXT_DIM, size=12)
    # Background 轨道
    tx, ty, tw, th = cx + 20, cy + 45, cw - 40, 30
    add_rect(dwg, tx, ty, tw, th, fill="#3a3a3a", stroke=BORDER, rx=4, stroke_width=1)
    add_text(dwg, "Background  轨道", tx, ty - 8, fill=ACCENT, size=13, weight="bold")
    # Fill
    fill_w = int(tw * 0.5)
    add_rect(dwg, tx, ty, fill_w, th, fill=ACCENT, rx=4, stroke="none", opacity=0.95)
    # Handle Slide Area 虚线
    add_line(dwg, tx, ty - 4, tx + tw, ty - 4, stroke=BORDER, stroke_width=1, dash="3,3")
    # Handle 圆形
    hcx, hcy = tx + fill_w, ty + th // 2
    add_ellipse(dwg, hcx, hcy, 16, 18, fill=TEXT, stroke=ACCENT, stroke_width=2)
    # 标注：Handle
    add_text(dwg, "Handle", hcx + 28, hcy + 5, fill=WARM, size=13, weight="bold")
    add_arrow(dwg, hcx + 25, hcy - 5, hcx + 12, hcy)
    # 标注：Fill
    add_text(dwg, "Fill  已填充部分", tx + fill_w * 0.5, ty - 8 + 50,
             fill=SUCCESS, size=12, anchor="middle", weight="bold")
    add_line(dwg, tx + fill_w * 0.5, ty - 8 + 44, tx + fill_w * 0.5, ty + 4,
             stroke=SUCCESS, stroke_width=1.2)
    # 标注：Handle Slide Area
    add_text(dwg, "Handle Slide Area", cx + cw - 130, ty - 10,
             fill=TEXT_DIM, size=11)
    # 底部说明
    add_text(dwg, "拖动 Handle -> Fill 长度变化 -> 触发 OnValueChanged(float)",
             W // 2, H - 60, fill=TEXT_DIM, size=13, anchor="middle", italic=True)
    # 左侧层级标签
    layers = [
        "① Background（轨道灰底）",
        "② Fill Area + Fill（蓝色已选）",
        "③ Handle Slide Area + Handle（白圆）",
    ]
    for i, txt in enumerate(layers):
        add_text(dwg, txt, 30, 290 + i * 24, fill=TEXT, size=11)
    save_svg_and_png(dwg, "L05_01_slider_structure")


def make_inputfield_structure():
    """L05_02: InputField 结构图。"""
    W, H = 900, 360
    dwg = new_svg(W, H)
    add_text(dwg, "InputField 结构", W // 2, 36, fill=TEXT, size=20,
             weight="bold", anchor="middle")
    # 容器
    cx, cy, cw, ch = 100, 130, 700, 110
    add_rect(dwg, cx, cy, cw, ch, fill=PANEL, stroke=ACCENT, rx=4, stroke_width=2)
    add_text(dwg, "InputField (TMP)", cx + 12, cy + 22, fill=TEXT_DIM, size=12)
    # Text Area
    tx, ty, tw, th = cx + 20, cy + 40, cw - 40, 60
    add_rect(dwg, tx, ty, tw, th, fill="#1a1a1a", stroke=BORDER, rx=3, stroke_width=1)
    add_text(dwg, "Text Area", tx, ty - 6, fill=TEXT_DIM, size=11)
    # Placeholder（虚线框，灰文字）
    ph_x, ph_y, ph_w, ph_h = tx + 12, ty + 10, tw - 24, th - 20
    add_rect(dwg, ph_x, ph_y, ph_w, ph_h, fill="none", stroke=TEXT_MUTED,
             rx=2, stroke_width=1, dash="4,3", opacity=0.7)
    add_text(dwg, "Placeholder  请输入昵称...", ph_x + ph_w // 2,
             ph_y + ph_h // 2 + 5, fill=TEXT_MUTED, size=14, anchor="middle")
    # Text（实线高亮）
    t_x, t_y, t_w, t_h = tx + 12, ty + 10, int((tw - 24) * 0.55), ph_h
    add_rect(dwg, t_x, t_y, t_w, t_h, fill="#2a3850", stroke=SUCCESS, rx=2,
             stroke_width=1.5, opacity=0.6)
    add_text(dwg, "HelloUnity", t_x + 10, t_y + t_h // 2 + 5,
             fill=SUCCESS, size=14, weight="bold")
    # 标注：Placeholder
    add_text(dwg, "Placeholder  占位提示", ph_x, ph_y - 8,
             fill=TEXT_DIM, size=12)
    add_arrow(dwg, ph_x + 30, ph_y - 4, ph_x + 30, ph_y + 4)
    # 标注：Text
    add_text(dwg, "Text  实际输入内容", t_x, t_y + t_h + 20,
             fill=SUCCESS, size=12, weight="bold")
    add_arrow(dwg, t_x + 30, t_y + t_h + 14, t_x + 20, t_y + t_h + 2)
    # 底部说明
    add_text(dwg,
             "Placeholder 灰色，Text 亮色；OnValueChanged / OnEndEdit 事件传 string",
             W // 2, H - 30, fill=TEXT_DIM, size=13, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L05_02_inputfield_structure")


def make_toggle_states():
    """L05_03: Toggle 三种状态。"""
    W, H = 900, 320
    dwg = new_svg(W, H)
    add_text(dwg, "Toggle 三种状态", W // 2, 36, fill=TEXT, size=20,
             weight="bold", anchor="middle")
    states = [
        ("ON",        ACCENT,   SUCCESS,    True,  "静音"),
        ("OFF",       ACCENT,   TEXT_MUTED, False, "全屏"),
        ("DISABLED",  "#555555", TEXT_MUTED, False, "隐藏 HUD"),
    ]
    box_w, box_h = 220, 90
    gap = 50
    total_w = box_w * 3 + gap * 2
    start_x = (W - total_w) // 2
    base_y = 110
    for i, (label, box_color, check_color, checked, lbl_text) in enumerate(states):
        x = start_x + i * (box_w + gap)
        add_rect(dwg, x, base_y, box_w, box_h, fill=PANEL, stroke=BORDER,
                 rx=6, stroke_width=1.5, opacity=0.9)
        # 复选框
        cb_x, cb_y, cb_w = x + 18, base_y + (box_h - 30) // 2, 30
        add_rect(dwg, cb_x, cb_y, cb_w, cb_w, fill=box_color, stroke=BORDER,
                 rx=4, stroke_width=1.5)
        # 对勾
        if checked:
            add_line(dwg, cb_x + 6, cb_y + 15, cb_x + 13, cb_y + 22,
                     stroke=SUCCESS, stroke_width=3)
            add_line(dwg, cb_x + 13, cb_y + 22, cb_x + 24, cb_y + 8,
                     stroke=SUCCESS, stroke_width=3)
        # Label
        add_text(dwg, lbl_text, x + 70, base_y + box_h // 2 + 5,
                 fill=TEXT, size=15)
        # 状态标题
        title_color = SUCCESS if label == "ON" else (
            TEXT_MUTED if label == "DISABLED" else WARM
        )
        add_text(dwg, label, x + box_w // 2, base_y + box_h + 24,
                 fill=title_color, size=15, weight="bold", anchor="middle")
    # 底部说明
    add_text(dwg, "OnValueChanged(bool) 在勾选切换时触发；isOn 反映当前状态",
             W // 2, H - 32, fill=TEXT_DIM, size=13, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L05_03_toggle_states")


def make_comparison_table():
    """L05_04: 三控件对比表。"""
    W, H = 900, 360
    dwg = new_svg(W, H)
    add_text(dwg, "Slider / InputField / Toggle 对比", W // 2, 32,
             fill=TEXT, size=20, weight="bold", anchor="middle")
    headers = [
        ("控件",      ACCENT),
        ("用途",      SUCCESS),
        ("值类型",    WARM),
        ("事件",      "#a78bfa"),
    ]
    rows = [
        ("Slider",     "在范围内选数值", "float",  "OnValueChanged"),
        ("InputField", "输入文字",       "string", "OnValueChanged / OnEndEdit"),
        ("Toggle",     "二选一开关",     "bool",   "OnValueChanged"),
    ]
    table_x, table_y = 60, 70
    col_w = [140, 240, 170, 290]
    header_h = 38
    row_h = 60
    table_w = sum(col_w)
    # 外框
    add_rect(dwg, table_x, table_y, table_w, header_h + row_h * len(rows),
             fill=PANEL, stroke=BORDER, rx=6, stroke_width=1.5)
    # 表头
    x = table_x
    for (title, color), w in zip(headers, col_w):
        add_rect(dwg, x, table_y, w, header_h, fill="#333333", stroke=BORDER,
                 stroke_width=1)
        add_text(dwg, title, x + w // 2, table_y + header_h // 2 + 6,
                 fill=color, size=15, weight="bold", anchor="middle")
        x += w
    # 行
    for ri, row in enumerate(rows):
        y_row = table_y + header_h + ri * row_h
        if ri % 2 == 0:
            add_rect(dwg, table_x + 1, y_row, table_w - 2, row_h,
                     fill="#252525", stroke="none", opacity=0.5)
        x = table_x
        for ci, (cell, w) in enumerate(zip(row, col_w)):
            if ci > 0:
                add_line(dwg, x, y_row, x, y_row + row_h, stroke=BORDER,
                         stroke_width=0.5, opacity=0.5)
            if ci == 0:
                add_text(dwg, cell, x + w // 2, y_row + row_h // 2 + 5,
                         fill=ACCENT, size=14, weight="bold", anchor="middle")
            else:
                add_text(dwg, cell, x + 12, y_row + row_h // 2 + 5,
                         fill=TEXT, size=13, anchor="start")
            x += w
        if ri < len(rows) - 1:
            add_line(dwg, table_x, y_row + row_h, table_x + table_w,
                     y_row + row_h, stroke=BORDER, stroke_width=0.5, opacity=0.4)
    # 底部说明
    add_text(dwg, "Button 用 OnClick（无参），其余三个用 OnValueChanged，参数类型不同",
             W // 2, H - 18, fill=TEXT_DIM, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L05_04_comparison_table")


def make_selectable_tree():
    """L05_05: Selectable 继承树。"""
    W, H = 1000, 540
    dwg = new_svg(W, H)
    add_text(dwg, "Selectable 继承树", W // 2, 36, fill=TEXT, size=22,
             weight="bold", anchor="middle")
    add_text(dwg, "共享 Interactable / Transition / Navigation 属性",
             W // 2, 64, fill=TEXT_DIM, size=14, anchor="middle", italic=True)

    # Selectable 根节点（带接口图标）
    root_w, root_h = 280, 80
    root_x = (W - root_w) // 2
    root_y = 95
    add_rect(dwg, root_x, root_y, root_w, root_h, fill=ACCENT, stroke="none",
             rx=10, stroke_width=2, opacity=0.95)
    # 节点图标：一个圆里面一个方块（代表 UI 元素）
    add_rect(dwg, root_x + 18, root_y + 20, 40, 40, fill="#1e1e1e", rx=4,
             stroke_width=2, stroke="#fff", opacity=0.9)
    add_rect(dwg, root_x + 28, root_y + 30, 20, 20, fill=ACCENT, rx=2,
             stroke_width=1, stroke="none", opacity=0.95)
    add_text(dwg, "Selectable", root_x + root_w // 2 + 30,
             root_y + root_h // 2 + 7, fill="#1e1e1e", size=20, weight="bold",
             anchor="middle")

    # 4 个子控件（带各自的小图标）
    children = [
        ("Button",     WARM,    "rect"),
        ("Slider",     SUCCESS, "slider"),
        ("InputField", "#ffcc66", "input"),
        ("Toggle",     "#a78bfa", "toggle"),
    ]
    child_w, child_h = 170, 110
    child_y = root_y + root_h + 80
    gap = (W - child_w * 4) // 5

    def draw_button(dwg, x, y, w, h, color):
        bw, bh = 110, 42
        bx = x + (w - bw) // 2
        by = y + 40
        add_rect(dwg, bx, by, bw, bh, fill=color, stroke="none", rx=4,
                 stroke_width=1.5, opacity=0.95)
        add_text(dwg, "Button", bx + bw // 2, by + bh // 2 + 5,
                 fill="#1e1e1e", size=13, weight="bold", anchor="middle")

    def draw_slider(dwg, x, y, w, h, color):
        tw, th = 130, 8
        tx = x + (w - tw) // 2
        ty = y + 56
        add_rect(dwg, tx, ty, tw, th, fill="#3a3a3a", rx=4, stroke_width=1,
                 stroke="none", opacity=0.9)
        add_rect(dwg, tx, ty, int(tw * 0.55), th, fill=color, rx=4,
                 stroke_width=1, stroke="none", opacity=1)
        add_ellipse(dwg, tx + int(tw * 0.55), ty + 4, 10, 10, fill="#fff",
                     stroke=color, stroke_width=2.5)

    def draw_input(dwg, x, y, w, h, color):
        iw, ih = 130, 36
        ix = x + (w - iw) // 2
        iy = y + 42
        add_rect(dwg, ix, iy, iw, ih, fill="#1a1a1a", stroke=color, rx=4,
                 stroke_width=1.8, opacity=0.9)
        # 输入光标
        add_text(dwg, "|", ix + 10, iy + ih // 2 + 5, fill=color, size=16,
                 weight="bold")
        add_text(dwg, "text", ix + 24, iy + ih // 2 + 4, fill=TEXT_DIM,
                 size=13, italic=True)

    def draw_toggle(dwg, x, y, w, h, color):
        # 开关底座
        tw, th = 100, 36
        tx = x + (w - tw) // 2
        ty = y + 42
        add_rect(dwg, tx, ty, tw, th, fill=color, rx=18, stroke="none",
                 stroke_width=1, opacity=0.95)
        # 白点
        add_ellipse(dwg, tx + tw - 24, ty + 6, 24, 24, fill="#fff",
                     stroke="none", stroke_width=1, opacity=1)

    drawers = {
        "Button": draw_button,
        "Slider": draw_slider,
        "InputField": draw_input,
        "Toggle": draw_toggle,
    }

    for i, (name, color, _kind) in enumerate(children):
        cx = gap + i * (child_w + gap)
        # 子节点容器
        add_rect(dwg, cx, child_y, child_w, child_h, fill=PANEL, stroke=color,
                 rx=8, stroke_width=2.5)
        # 子类名
        add_text(dwg, name, cx + child_w // 2, child_y + 20, fill=color,
                 size=15, weight="bold", anchor="middle")
        # 小图标预览
        drawers[name](dwg, cx, child_y, child_w, child_h, color)
        # 粗实线连接父节点
        add_line(dwg,
                 cx + child_w // 2, child_y,
                 root_x + root_w // 2, root_y + root_h,
                 stroke=color, stroke_width=2.5, opacity=0.85)
        # 空心三角形箭头（UML extends 风格，指向父类）
        tri_w, tri_h = 12, 8
        tip_x = root_x + root_w // 2
        tip_y = root_y + root_h - 2
        # 三角形内部填充同背景色，外描边为颜色
        add_line(dwg,
                 tip_x, tip_y,
                 tip_x - tri_w // 2, tip_y + tri_h,
                 stroke=color, stroke_width=2, opacity=1)
        add_line(dwg,
                 tip_x, tip_y,
                 tip_x + tri_w // 2, tip_y + tri_h,
                 stroke=color, stroke_width=2, opacity=1)
        add_line(dwg,
                 tip_x - tri_w // 2, tip_y + tri_h,
                 tip_x + tri_w // 2, tip_y + tri_h,
                 stroke=color, stroke_width=2, opacity=1)
        # 覆盖内部填背景色（形成空心效果）
        add_line(dwg,
                 tip_x - 1, tip_y + 1,
                 tip_x - 1, tip_y + tri_h - 1,
                 stroke=BG, stroke_width=0.6)
        add_line(dwg,
                 tip_x + 1, tip_y + 1,
                 tip_x + 1, tip_y + tri_h - 1,
                 stroke=BG, stroke_width=0.6)

    # 共享属性框
    props_y = child_y + child_h + 50
    props_x = 80
    props_w = W - 160
    props_h = 130
    add_rect(dwg, props_x, props_y, props_w, props_h, fill=PANEL,
             stroke="#a78bfa", rx=10, stroke_width=2)
    add_text(dwg, "共享属性（所有子控件都有）", props_x + props_w // 2,
             props_y + 26, fill="#a78bfa", size=16, weight="bold",
             anchor="middle")
    props = [
        ("Interactable", "可交互；关闭后变灰，无法点击/拖拽", ACCENT),
        ("Transition",   "状态切换：Color Tint / Sprite Swap / Animation",
         SUCCESS),
        ("Navigation",   "手柄/键盘导航：Horizontal / Vertical / Explicit / None",
         WARN),
    ]
    for i, (name, desc, color) in enumerate(props):
        y = props_y + 58 + i * 22
        add_text(dwg, "* " + name, props_x + 20, y, fill=color, size=13,
                 weight="bold")
        add_text(dwg, "— " + desc, props_x + 170, y, fill=TEXT, size=12)

    save_svg_and_png(dwg, "L05_05_selectable_tree")


if __name__ == "__main__":
    print("=== 重新生成 L05 五张配图 ===")
    make_slider_structure()
    make_inputfield_structure()
    make_toggle_states()
    make_comparison_table()
    make_selectable_tree()
    print("=== 全部完成 ===")
