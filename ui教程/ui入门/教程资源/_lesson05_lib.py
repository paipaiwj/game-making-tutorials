"""L05 共用工具模块。
- 配色与站点 style.css CSS 变量对齐
- svgwrite 生成 SVG（浏览器原生文字渲染、可编辑）
- Pillow 同步生成 PNG 预览，方便 view_image 自验中文
"""

import os
import svgwrite
from PIL import Image, ImageDraw, ImageFont

# 站点配色（与 style.css CSS 变量一致）
BG = "#1e1e1e"          # --bg
PANEL = "#2b2b2b"       # --panel
BORDER = "#3a3a3a"      # --border
ACCENT = "#4ea1ff"      # --accent 蓝
WARM = "#ff9e4e"        # --accent-warm 橙
SUCCESS = "#6bcf7f"     # --success 绿
WARN = "#ffcc66"        # --warn 黄
PURPLE = "#a78bfa"      # 紫
MUTED = "#9aa0a6"       # 灰
TEXT = "#dddddd"
TEXT_DIM = "#aaaaaa"

# 字体路径（Windows 微软雅黑）
FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
FONT_PREVIEW_PATH = None
for _p in [r"C:\Windows\Fonts\msyh.ttc",
           r"C:\Windows\Fonts\msyh.ttf",
           r"C:\Windows\Fonts\Microsoft YaHei UI.ttf"]:
    if os.path.exists(_p):
        FONT_PREVIEW_PATH = _p
        break

OUT_DIR = r"D:\bangong\unity\vrc\ass\ceshi\Assets\UITutorial\Site\img"


def make_svg(width=900, height=520, bg=BG):
    dwg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"),
                           viewBox=f"0 0 {width} {height}")
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=bg))
    return dwg


def add_text(dwg, text, x, y, *, fill=TEXT, size=18, weight="normal",
             anchor="start", family=None):
    style = {"font-family": family or "Microsoft YaHei, 'PingFang SC', sans-serif",
             "font-size": f"{size}px",
             "font-weight": weight,
             "fill": fill}
    align = {"start": "start", "middle": "middle", "end": "end"}[anchor]
    el = dwg.text(text, insert=(x, y), text_anchor=align, **style)
    dwg.add(el)


def add_box(dwg, x, y, w, h, *, fill=PANEL, stroke=BORDER, rx=8, ry=8,
            stroke_width=1.5, opacity=1.0):
    if opacity != 1.0:
        g = dwg.g(opacity=opacity)
    else:
        g = dwg.g()
    g.add(dwg.rect(insert=(x, y), size=(w, h), rx=rx, ry=ry,
                   fill=fill, stroke=stroke, stroke_width=stroke_width))
    return g


def add_line(dwg, x1, y1, x2, y2, *, stroke=ACCENT, width=2):
    return dwg.line((x1, y1), (x2, y2), stroke=stroke, stroke_width=width)


def add_arrow(dwg, x1, y1, x2, y2, *, stroke=ACCENT, width=2, marker_id=None):
    marker = dwg.marker(insert=(8, 4), size=(8, 8), orient="auto",
                        refX=8, refY=4)
    marker.add(dwg.path(d="M0,0 L8,4 L0,8 z", fill=stroke))
    if marker_id is not None:
        marker["id"] = marker_id
        dwg.defs.add(marker)
    kwargs = {"marker-end": f"url(#{marker_id})"} if marker_id else {}
    return dwg.line((x1, y1), (x2, y2), stroke=stroke, stroke_width=width, **kwargs)


def add_caption_box(dwg, x, y, w, h, text, *, fill=PANEL, stroke=ACCENT):
    g = dwg.g()
    g.add(dwg.rect(insert=(x, y), size=(w, h), rx=4, ry=4,
                   fill=fill, stroke=stroke, stroke_width=1.2,
                   opacity=0.85))
    add_text(dwg, text, x + 12, y + h / 2 + 5, fill=TEXT, size=14,
             anchor="start")
    return g


def make_preview_canvas(width, height, bg=BG):
    return Image.new("RGB", (width, height), bg)


def load_preview_font(size):
    if FONT_PREVIEW_PATH:
        return ImageFont.truetype(FONT_PREVIEW_PATH, size)
    return ImageFont.load_default()


def draw_text(img, xy, text, *, fill=TEXT, size=18, anchor="lt", font=None):
    d = ImageDraw.Draw(img)
    f = font or load_preview_font(size)
    if anchor == "lt":
        d.text(xy, text, fill=fill, font=f)
    elif anchor == "center":
        bbox = d.textbbox((0, 0), text, font=f)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x, y = xy
        d.text((x - w / 2, y - h / 2), text, fill=fill, font=f)
    elif anchor == "rt":
        bbox = d.textbbox((0, 0), text, font=f)
        w = bbox[2] - bbox[0]
        x, y = xy
        d.text((x - w, y), text, fill=fill, font=f)


def text_size(d, text, font):
    bbox = d.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]
