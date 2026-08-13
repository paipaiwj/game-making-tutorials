# -*- coding: utf-8 -*-
"""
VFX 教程渲染工具：
  - svgwrite 生成 SVG（站点原生文字，浏览器可编辑）
  - resvg 渲染 PNG（高质量中英文字体回退）
"""

import os
import io
import svgwrite
import resvg_py
from PIL import Image

# ============ 站点配色（与 style.css CSS 变量保持一致） ============
BG = "#1e1e1e"
PANEL = "#2b2b2b"
BORDER = "#3a3a3a"
ACCENT = "#4ea1ff"
WARM = "#ff9e4e"
SUCCESS = "#6bcf7f"
WARN = "#ffcc66"
TEXT = "#dddddd"
TEXT_DIM = "#9aa0a6"
TEXT_MUTED = "#6e6e6e"

FONT_FAMILY = "Microsoft YaHei, PingFang SC, Noto Sans SC, sans-serif"

RENDER_SCALE = 2
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def new_svg(width, height, bg=BG):
    dwg = svgwrite.Drawing(
        size=(f"{width}px", f"{height}px"),
        viewBox=f"0 0 {width} {height}",
    )
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=bg))
    return dwg


def add_text(dwg, text, x, y, *, fill=TEXT, size=14, weight="normal",
             anchor="start", italic=False):
    style = {
        "font-family": FONT_FAMILY,
        "font-size": f"{size}px",
        "font-weight": weight,
        "fill": fill,
    }
    if italic:
        style["font-style"] = "italic"
    text_anchor = {"start": "start", "middle": "middle", "end": "end"}[anchor]
    el = svgwrite.text.Text(text, insert=(x, y), text_anchor=text_anchor, **style)
    dwg.add(el)


def add_rect(dwg, x, y, w, h, *, fill=PANEL, stroke=BORDER, rx=6, ry=6,
             stroke_width=1.5, opacity=1.0, dash=None):
    attrs = {"rx": rx, "ry": ry, "fill": fill, "stroke": stroke,
             "stroke-width": stroke_width}
    if opacity != 1.0:
        attrs["opacity"] = opacity
    if dash:
        attrs["stroke-dasharray"] = dash
    el = dwg.rect(insert=(x, y), size=(w, h), **attrs)
    dwg.add(el)
    return el


def add_line(dwg, x1, y1, x2, y2, *, stroke=ACCENT, stroke_width=1.5,
             dash=None, with_arrow=False, opacity=1.0):
    attrs = {"stroke": stroke, "stroke-width": stroke_width}
    if dash:
        attrs["stroke-dasharray"] = dash
    if with_arrow:
        marker = dwg.marker(insert=(8, 5), size=(10, 10), orient="auto",
                             refX=9, refY=5, id="arrowhead")
        marker.add(dwg.path(d="M0,0 L0,10 L10,5 z", fill=stroke))
        dwg.defs.add(marker)
        attrs["marker-end"] = "url(#arrowhead)"
    if opacity != 1.0:
        attrs["opacity"] = opacity
    el = dwg.line(start=(x1, y1), end=(x2, y2), **attrs)
    dwg.add(el)
    return el


def add_arrow(dwg, x1, y1, x2, y2, *, stroke=ACCENT, stroke_width=1.5):
    return add_line(dwg, x1, y1, x2, y2, stroke=stroke,
                    stroke_width=stroke_width, with_arrow=True)


def add_ellipse(dwg, cx, cy, rx, ry, *, fill=ACCENT, stroke="none",
                stroke_width=1.0, opacity=1.0):
    el = dwg.ellipse(center=(cx, cy), r=(rx, ry), fill=fill,
                     stroke=stroke, stroke_width=stroke_width,
                     opacity=opacity)
    dwg.add(el)
    return el


def save_svg_and_png(dwg, name, scale=RENDER_SCALE):
    os.makedirs(OUT_DIR, exist_ok=True)
    svg_path = os.path.join(OUT_DIR, f"{name}.svg")
    png_path = os.path.join(OUT_DIR, f"{name}.png")

    dwg.saveas(svg_path)

    w_attr = dwg.attribs["width"]
    h_attr = dwg.attribs["height"]
    base_w = int(str(w_attr).rstrip("px"))
    base_h = int(str(h_attr).rstrip("px"))

    with open(svg_path, "r", encoding="utf-8") as f:
        svg_text = f.read()
    png_bytes = resvg_py.svg_to_bytes(
        svg_string=svg_text,
        width=base_w * scale,
        height=base_h * scale,
    )
    img = Image.open(io.BytesIO(png_bytes))
    img.save(png_path, "PNG")
    print(f"  -> {svg_path}")
    print(f"  -> {png_path}  ({img.size[0]}x{img.size[1]})")
    return png_path
