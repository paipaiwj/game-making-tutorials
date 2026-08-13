# -*- coding: utf-8 -*-
# Unity 音频入门教程（面向 VRChat）— 配图生成脚本
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

def shade(c, f):
    return tuple(max(0, min(255, int(x * f))) for x in c)

def rgb(c):
    return f"rgb({c[0]},{c[1]},{c[2]})"

def sine_wave(dwg, x0, y0, width, amp, cycles, color, stroke_width=2, step=6, opacity=1.0):
    """画正弦波折线，y0 是中线，x 从左到右。"""
    pts = []
    n = max(2, int(width / step))
    for i in range(n + 1):
        x = x0 + width * i / n
        y = y0 - amp * math.sin(2 * math.pi * cycles * i / n)
        pts.append((x, y))
    poly = dwg.polyline(pts, fill="none", stroke=color, stroke_width=stroke_width)
    if opacity != 1.0:
        poly.attribs["opacity"] = opacity
    dwg.add(poly)
    return poly


# ============================================================
# L01 — 图1: 声音是什么
# ============================================================
def make_L01_01_sound_wave():
    W, H = 900, 520
    dwg = new_svg(W, H)
    add_text(dwg, "声音是什么？", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "声音 = 空气的振动。振得快 → 音高高；振得猛 → 音量响", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # 频率对比
    add_text(dwg, "① 频率 Frequency — 决定「音高」", 60, 100, fill="#fff", size=14, weight="bold")
    sine_wave(dwg, 60, 150, 360, 30, 2, ACCENT, stroke_width=2)
    add_text(dwg, "低频：低沉（鼓、轰鸣）", 60, 185, fill=TEXT_DIM, size=12)
    sine_wave(dwg, 60, 230, 360, 30, 6, ACCENT, stroke_width=2, step=3)
    add_text(dwg, "高频：尖锐（鸟叫、叮声）", 60, 265, fill=TEXT_DIM, size=12)

    # 音量对比
    add_text(dwg, "② 振幅 Amplitude — 决定「音量」", 480, 100, fill="#fff", size=14, weight="bold")
    sine_wave(dwg, 480, 150, 360, 14, 4, SUCCESS, stroke_width=2)
    add_text(dwg, "振幅小 = 安静（耳语）", 480, 185, fill=TEXT_DIM, size=12)
    sine_wave(dwg, 480, 230, 360, 45, 4, SUCCESS, stroke_width=2)
    add_text(dwg, "振幅大 = 响亮（爆炸）", 480, 265, fill=TEXT_DIM, size=12)

    # 单位说明
    add_rect(dwg, 60, 300, 780, 110, fill=PANEL, stroke=BORDER, rx=10)
    add_text(dwg, "常用单位", 90, 330, fill=TEXT, size=14, weight="bold")
    add_text(dwg, "频率：Hz（赫兹）—— 人耳大约能听到 20Hz ~ 20kHz", 90, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "音量：dB（分贝）—— 对数单位！每 +10dB ≈ 感觉响 2 倍", 90, 382, fill=WARN, size=12.5)
    add_text(dwg, "音乐作品一般压到 -14 ~ -16 LUFS；0 dBFS 以上会爆音（clipping）", 90, 406, fill=TEXT_DIM, size=12.5)

    add_text(dwg, "记住：dB 是对数的！「音量滑块」别直接当 dB 用，Unity 里用 AudioMixer 换算", W//2, 490, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L01_01_sound_wave")


# ============================================================
# L01 — 图2: Unity 音频组件
# ============================================================
def make_L01_02_audio_components():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "Unity 音频两大组件", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "AudioListener（耳朵）+ AudioSource（声源）—— 声音从源传到听者", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # AudioSource 卡片
    add_rect(dwg, 80, 100, 330, 170, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    add_text(dwg, "Audio Source（声源）", 245, 128, fill="#fff", size=14, weight="bold", anchor="middle")
    for j, line in enumerate(["挂在「发声」的物体上", "AudioClip：要播的音频文件", "Volume / Pitch：音量 / 音高", "3D：距离越远越小声", "Loop：循环播放（音乐、环境音）"]):
        add_text(dwg, line, 245, 156 + j * 20, fill=TEXT_DIM, size=12, anchor="middle")

    # AudioListener 卡片
    add_rect(dwg, 490, 100, 330, 170, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=2)
    add_text(dwg, "Audio Listener（听者）", 655, 128, fill="#fff", size=14, weight="bold", anchor="middle")
    for j, line in enumerate(["全场景只能有一个！", "挂在玩家 / 相机上", "负责「听」所有声音", "VRChat 里挂玩家身上", "两个 Listener = 报错"]):
        add_text(dwg, line, 655, 156 + j * 20, fill=TEXT_DIM, size=12, anchor="middle")

    # 中间箭头
    add_arrow(dwg, 420, 185, 480, 185, stroke=WARM, stroke_width=3)

    # 底部示意
    add_rect(dwg, 80, 300, 740, 90, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "工作流程", 110, 328, fill=SUCCESS, size=13, weight="bold")
    add_text(dwg, "声源（篝火）→ 声音按 3D 规则衰减传播 → 玩家身上的听者收到 → 混音器 → 扬声器/耳机", 110, 354, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "世界里有 100 个声源也没关系，没有听者就全都不响（反之亦然）", 110, 378, fill=WARN, size=12)

    save_svg_and_png(dwg, "L01_02_audio_components")


# ============================================================
# L02 — 图1: 音频格式
# ============================================================
def make_L02_01_formats():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "音频文件格式怎么选", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    items = [
        ("WAV", "无损，巨大", "音效、UI 点击\n（短而精，几十 KB~几 MB）\nUnity 首选", ACCENT),
        ("MP3", "有损压缩", "音乐、长对白\n（小，兼容性好）\nVRChat 推荐", WARM),
        ("OGG", "有损压缩", "音乐、环境音\n（小，流式播放友好）\nVRChat 推荐", SUCCESS),
    ]
    card_w, card_h = 250, 230
    start_x = (W - (card_w * 3 + 30 * 2)) // 2
    for i, (title, subtitle, desc, color) in enumerate(items):
        x = start_x + i * (card_w + 30)
        add_rect(dwg, x, 80, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 112, fill="#fff", size=17, weight="bold", anchor="middle")
        add_text(dwg, subtitle, x + card_w//2, 136, fill=color, size=12, anchor="middle")
        add_line(dwg, x + 20, 150, x + card_w - 20, 150, stroke=BORDER, stroke_width=1)
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 176 + j * 20, fill=TEXT_DIM, size=12, anchor="middle")

    add_text(dwg, "音频会先被 Unity 转成 AudioClip（.meta 里记录导入设置），VRChat 上传时还会再转码", W//2, 400, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L02_01_formats")


# ============================================================
# L02 — 图2: 导入设置
# ============================================================
def make_L02_02_import_settings():
    W, H = 900, 500
    dwg = new_svg(W, H)
    add_text(dwg, "导入设置（Inspector 里选音频文件时）", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    rows = [
        ("Load Type", "Decompress On Load：短音效，加载时解压，占内存小播放快", ACCENT),
        ("Load Type", "Streaming：长音乐/环境音，边播边读，省内存", ACCENT),
        ("Compression Format", "Vorbis（OGG 压缩）：推荐，体积小质量好", SUCCESS),
        ("Quality", "音乐 60~80，音效 90+，质量越高文件越大", WARM),
        ("Sample Rate", "44100 / 48000 都行，别用 96000（白占体积）", WARN),
        ("Force To Mono", "3D 音效可勾选，体积减半；音乐不要勾", "#c084fc"),
    ]
    y0 = 80
    for i, (k, v, color) in enumerate(rows):
        y = y0 + i * 62
        add_rect(dwg, 60, y, 780, 50, fill=PANEL, stroke=BORDER, rx=8)
        if k:
            add_rect(dwg, 75, y + 8, 190, 34, fill="#1a1a1a", stroke=color, rx=6)
            add_text(dwg, k, 170, y + 31, fill=color, size=13, weight="bold", anchor="middle")
            add_text(dwg, v, 290, y + 31, fill=TEXT_DIM, size=12.5)
        else:
            add_text(dwg, v, 290, y + 31, fill=TEXT_DIM, size=12.5)

    add_rect(dwg, 60, 460 - 62, 780, 50, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "经验：短音效用 Decompress + 高质量；音乐/环境音用 Streaming + Vorbis 60~80", 450, 460 - 31, fill=WARN, size=12.5, anchor="middle")
    save_svg_and_png(dwg, "L02_02_import_settings")


# ============================================================
# L03 — 图1: 3D 声音
# ============================================================
def make_L03_01_3d_sound():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "3D 声音：声音有位置感", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "声源在左边 → 左边耳机响；越远越小声 → 用距离衰减曲线控制", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # 衰减曲线
    add_rect(dwg, 60, 90, 780, 250, fill="#1a1a1a", stroke=BORDER, rx=10)
    add_text(dwg, "音量", 40, 130, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "距离 →", 810, 320, fill=TEXT_DIM, size=12, anchor="middle")
    # 坐标轴
    add_line(dwg, 90, 120, 90, 310, stroke=BORDER, stroke_width=1.5)
    add_line(dwg, 90, 310, 790, 310, stroke=BORDER, stroke_width=1.5)
    # 曲线1：快速衰减
    pts = [(90, 130)]
    for i in range(1, 30):
        x = 90 + i * 700 / 29
        y = 310 - 180 * math.exp(-i / 6.0)
        pts.append((x, y))
    dwg.add(dwg.polyline(pts, fill="none", stroke=ACCENT, stroke_width=2.5))
    add_text(dwg, "3D 衰减（近距离听清，远了快速消失）", 680, 140, fill=ACCENT, size=12, anchor="middle")
    # 曲线2：恒定
    add_line(dwg, 90, 170, 790, 170, stroke=SUCCESS, stroke_width=2, dash=[6, 4])
    add_text(dwg, "2D 恒定音量（UI 音效 / 全局音乐）", 680, 198, fill=SUCCESS, size=12, anchor="middle")

    # 左右声道示意
    add_text(dwg, "空间化 Pan（立体声定位）", 90, 370, fill="#fff", size=14, weight="bold")
    add_rect(dwg, 60, 380, 200, 60, fill="#2a2a2a", stroke=BORDER, rx=8)
    add_text(dwg, "左声道", 110, 412, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "▲ 声源在左", 210, 412, fill=ACCENT, size=12, anchor="middle")
    add_rect(dwg, 280, 380, 200, 60, fill="#2a2a2a", stroke=BORDER, rx=8)
    add_text(dwg, "右声道", 330, 412, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "▼ 声源在右", 430, 412, fill=ACCENT, size=12, anchor="middle")
    add_rect(dwg, 500, 380, 340, 60, fill="#2a2a2a", stroke=BORDER, rx=8)
    add_text(dwg, "VRChat 里玩家转头，声音会跟着变 → 世界真实感的核心", 670, 412, fill=SUCCESS, size=12, anchor="middle")

    save_svg_and_png(dwg, "L03_01_3d_sound")


# ============================================================
# L03 — 图2: 混音总线
# ============================================================
def make_L03_02_mixer_buses():
    W, H = 900, 520
    dwg = new_svg(W, H)
    add_text(dwg, "Audio Mixer：总线混音", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "所有声音先进「总线」，再汇入 Master —— 调分组音量，不一个个调", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # Master
    add_rect(dwg, 350, 90, 200, 54, fill="#3a3a3a", stroke="#ffffff", rx=8, stroke_width=2)
    add_text(dwg, "Master（总输出）", 450, 124, fill="#fff", size=15, weight="bold", anchor="middle")

    # 五个子总线
    children = [
        ("Music 音乐", "BGM、主题曲", ACCENT),
        ("SFX 音效", "点击、交互、技能", SUCCESS),
        ("Ambience 环境", "风、水、鸟鸣", WARM),
        ("UI 界面", "按钮、提示音", "#c084fc"),
        ("Voice 语音", "对白、旁白", "#ff9e4e"),
    ]
    card_w, card_h = 156, 120
    start_x = (W - (card_w * 5 + 14 * 4)) // 2
    for i, (name, desc, color) in enumerate(children):
        x = start_x + i * (card_w + 14)
        add_rect(dwg, x, 230, card_w, card_h, fill=PANEL, stroke=color, rx=8, stroke_width=2)
        add_text(dwg, name, x + card_w//2, 258, fill="#fff", size=13, weight="bold", anchor="middle")
        add_text(dwg, desc, x + card_w//2, 284, fill=TEXT_DIM, size=11, anchor="middle")
        add_line(dwg, x + card_w//2, 210, 450, 144, stroke=color, stroke_width=2, opacity=0.7)
    add_ellipse(dwg, 450, 144, 5, 5, fill="#ffffff", opacity=0.7)

    # 右侧说明
    add_rect(dwg, 60, 380, 780, 110, fill=PANEL, stroke=BORDER, rx=10)
    add_text(dwg, "为什么用总线？", 90, 410, fill=SUCCESS, size=14, weight="bold")
    add_text(dwg, "① 玩家想「关音乐」→ 一个开关关 Music 总线，不用动几百个音源", 90, 438, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "② 音量是 dB 单位：-6dB ≈ 响度减半；总线音量 = 分组音量，永不单独调每个 AudioClip", 90, 462, fill=WARN, size=12.5)

    save_svg_and_png(dwg, "L03_02_mixer_buses")


# ============================================================
# L03 — 图3: Ducking 闪避
# ============================================================
def make_L03_03_ducking():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "Ducking：音乐自动给对白让路", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "说话时背景音乐自动压低，说完恢复 —— 用侧链压缩器实现", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # 上：语音
    add_text(dwg, "Voice 总线（触发）", 120, 100, fill=SUCCESS, size=13, weight="bold")
    add_rect(dwg, 60, 112, 780, 60, fill="#1a1a1a", stroke=SUCCESS, rx=8)
    add_text(dwg, "对白开始", 110, 150, fill=TEXT_DIM, size=12)
    add_text(dwg, "对白进行中", 420, 150, fill=SUCCESS, size=13, anchor="middle")
    add_text(dwg, "对白结束", 730, 150, fill=TEXT_DIM, size=12)

    # 下：音乐
    add_text(dwg, "Music 总线（被压）", 120, 210, fill=ACCENT, size=13, weight="bold")
    add_rect(dwg, 60, 222, 780, 92, fill="#1a1a1a", stroke=ACCENT, rx=8)
    # 音乐音量曲线
    pts = [(80, 258), (230, 258), (250, 290), (560, 290), (580, 258), (820, 258)]
    dwg.add(dwg.polyline(pts, fill="none", stroke=ACCENT, stroke_width=3))
    add_text(dwg, "正常音量 0dB", 105, 246, fill=TEXT_DIM, size=11)
    add_text(dwg, "压低到 -12dB", 400, 246, fill=WARN, size=11, anchor="middle")
    add_text(dwg, "恢复", 690, 246, fill=TEXT_DIM, size=11)

    # 参数建议
    add_rect(dwg, 60, 330, 780, 90, fill=PANEL, stroke=BORDER, rx=8)
    add_text(dwg, "参数建议：Threshold -30dB（触发线）  Ratio 8:1（压多狠）  Attack 10ms（快速让开）  Release 300~500ms（平滑恢复）", 450, 358, fill=TEXT_DIM, size=12, anchor="middle")
    add_text(dwg, "在 Music 总线挂 Compressor，Sidechain 选 Voice 总线即可", 450, 394, fill=WARN, size=12.5, anchor="middle")

    save_svg_and_png(dwg, "L03_03_ducking")


# ============================================================
# L04 — 图1: VRChat 音频播放方式
# ============================================================
def make_L04_01_vrc_audio_flow():
    W, H = 900, 400
    dwg = new_svg(W, H)
    add_text(dwg, "VRChat 里怎么播放声音", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")
    add_text(dwg, "两种方式：本地播放 vs 全网同步播放", W//2, 62, fill=TEXT_DIM, size=13, anchor="middle")

    # 本地
    add_rect(dwg, 60, 90, 370, 200, fill=PANEL, stroke=ACCENT, rx=10, stroke_width=2)
    add_text(dwg, "本地播放", 245, 118, fill="#fff", size=15, weight="bold", anchor="middle")
    for j, line in enumerate(["AudioSource.Play()", "只有自己听到", "适合：UI 音、个人交互反馈", "最简单，0 网络开销", "但别人听不到！"]):
        add_text(dwg, line, 245, 148 + j * 22, fill=TEXT_DIM, size=12.5, anchor="middle")

    # 同步
    add_rect(dwg, 470, 90, 370, 200, fill=PANEL, stroke=SUCCESS, rx=10, stroke_width=2)
    add_text(dwg, "全网同步播放", 655, 118, fill="#fff", size=15, weight="bold", anchor="middle")
    for j, line in enumerate(["SendCustomNetworkEvent", "所有玩家一起听到", "适合：开关音乐、事件音", "用 Udon 发送网络事件", "触发者向全网广播"]):
        add_text(dwg, line, 655, 148 + j * 22, fill=TEXT_DIM, size=12.5, anchor="middle")

    add_text(dwg, "原则：全局音乐、公共事件用网络事件；个人 UI 反馈用本地播放", W//2, 380, fill=TEXT_MUTED, size=12.5, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L04_01_vrc_audio_flow")


# ============================================================
# L04 — 图2: Udon 播放音频
# ============================================================
def make_L04_02_udon_audio():
    W, H = 900, 420
    dwg = new_svg(W, H)
    add_text(dwg, "Udon 控制音频播放", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    boxes = [
        ("GameObject", "挂 AudioSource\n（勾上需要的 3D/循环）", ACCENT, 60),
        ("UdonBehaviour", "Interact 或自定义事件\n里调用播放", WARM, 300),
        ("播放命令", "Play() / Stop()\nPause() / SetVolume()", SUCCESS, 540),
    ]
    box_w = 180
    for title, desc, color, x in boxes:
        add_rect(dwg, x, 90, box_w, 150, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + box_w//2, 120, fill="#fff", size=14, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + box_w//2, 152 + j * 20, fill=TEXT_DIM, size=11.5, anchor="middle")
        if x < 540:
            add_arrow(dwg, x + box_w + 4, 165, x + box_w + 20, 165, stroke=boxes[boxes.index((title, desc, color, x)) + 1][2], stroke_width=2)

    # 代码示例
    add_rect(dwg, 60, 270, 780, 120, fill="#1a1a1a", stroke=BORDER, rx=10)
    add_text(dwg, "UdonSharp 里：", 90, 300, fill=SUCCESS, size=13, weight="bold")
    for j, line in enumerate([
        "public AudioSource audioSource;   // Inspector 拖入",
        "public void PlaySound() { audioSource.Play(); }  // 本地播放",
        "public void PlayForEveryone() { SendCustomNetworkEvent(\"PlaySound\"); }  // 全网播放",
    ]):
        add_text(dwg, line, 90, 330 + j * 26, fill="#9ecbff", size=12, anchor="start")

    save_svg_and_png(dwg, "L04_02_udon_audio")


# ============================================================
# L04 — 图3: VRChat 音频限制
# ============================================================
def make_L04_03_limits():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "VRChat 音频注意事项", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    items = [
        ("格式", "支持 WAV / MP3 / OGG\n上传时自动转码", ACCENT),
        ("体积", "音频会进世界包体\n音乐别整首塞，压缩或用短循环", WARM),
        ("性能", "AudioSource 别堆几百个\n远处听不到的音源也别一直放", SUCCESS),
        ("2D vs 3D", "UI 音用 2D 恒定\n环境音用 3D 衰减", "#c084fc"),
        ("Quest", "安卓端音频限制更严\n内存小，避免大体积音频", "#ff9e4e"),
    ]
    card_w, card_h = 156, 220
    start_x = (W - (card_w * 5 + 14 * 4)) // 2
    for i, (title, desc, color) in enumerate(items):
        x = start_x + i * (card_w + 14)
        add_rect(dwg, x, 80, card_w, card_h, fill=PANEL, stroke=color, rx=10, stroke_width=2)
        add_text(dwg, title, x + card_w//2, 110, fill="#fff", size=13.5, weight="bold", anchor="middle")
        for j, line in enumerate(desc.split("\n")):
            add_text(dwg, line, x + card_w//2, 140 + j * 20, fill=TEXT_DIM, size=11, anchor="middle")

    add_text(dwg, "测试音效：VRChat → Build & Test 里戴上耳机走一圈，听距离衰减和左右声道", W//2, 420, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L04_03_limits")


# ============================================================
# L05 — 图1: 环境音制作步骤
# ============================================================
def make_L05_01_steps():
    W, H = 900, 460
    dwg = new_svg(W, H)
    add_text(dwg, "动手：做一个篝火环境音", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    steps = [
        ("1. 备音频", "网上找/自己录\n篝火噼啪声（短循环）", ACCENT),
        ("2. 导入设置", "Loop 循环勾上\nDecompress + Vorbis", SUCCESS),
        ("3. 挂声源", "场景放空物体\n挂 AudioSource", WARM),
        ("4. 3D 衰减", "勾 3D，调曲线\n半径 10~15m", "#c084fc"),
        ("5. 接总线", "Audio Mixer 建\nAmbience 总线", "#ff9e4e"),
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

    add_text(dwg, "同理可以扩展：瀑布（白噪音）、风（低频）、鸟鸣（高频点缀）", W//2, 350, fill=TEXT_DIM, size=13, anchor="middle")
    add_rect(dwg, 200, 380, 500, 50, fill="#1a1a1a", stroke=BORDER, rx=8)
    add_text(dwg, "3 层声音叠起来：近处篝火 + 远处瀑布 + 头顶鸟鸣 = 沉浸感", 450, 410, fill=WARN, size=12.5, anchor="middle")
    save_svg_and_png(dwg, "L05_01_steps")


# ============================================================
# L05 — 图2: 环境音布局
# ============================================================
def make_L05_02_layout():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "篝火场景音频布局", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    # 地面
    add_rect(dwg, 60, 320, 780, 60, fill="#202020", stroke=BORDER, rx=8)

    # 玩家
    add_ellipse(dwg, 450, 300, 30, 22, fill="#5a8f4e", opacity=0.6)
    add_text(dwg, "玩家（AudioListener）", 450, 350, fill="#fff", size=12, anchor="middle")

    # 篝火（近）
    add_ellipse(dwg, 620, 300, 36, 26, fill="#ff9e4e", opacity=0.5)
    add_text(dwg, "🔥 篝火", 620, 290, fill="#ffcc66", size=13, anchor="middle")
    add_text(dwg, "3D 衰减 10m", 620, 350, fill=TEXT_DIM, size=10.5, anchor="middle")

    # 瀑布（远）
    add_ellipse(dwg, 160, 300, 34, 24, fill="#4ea1ff", opacity=0.4)
    add_text(dwg, "瀑布", 160, 290, fill="#9ecbff", size=13, anchor="middle")
    add_text(dwg, "3D 衰减 30m", 160, 350, fill=TEXT_DIM, size=10.5, anchor="middle")

    # 鸟鸣（高）
    add_ellipse(dwg, 300, 220, 18, 18, fill="#6bcf7f", opacity=0.5)
    add_text(dwg, "鸟鸣", 300, 205, fill="#86efac", size=12, anchor="middle")
    add_text(dwg, "2D 恒定（世界常驻）", 300, 240, fill=TEXT_DIM, size=10.5, anchor="middle")

    # 距离线
    add_line(dwg, 450, 285, 620, 285, stroke="#ff9e4e", stroke_width=1.5, dash=[5, 4], opacity=0.7)
    add_line(dwg, 450, 285, 160, 285, stroke="#4ea1ff", stroke_width=1.5, dash=[5, 4], opacity=0.7)

    add_text(dwg, "远近分层：离得近的声源用小衰减半径，远的用大半径 —— 玩家走动时声音自然变化", W//2, 420, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L05_02_layout")


# ============================================================
# L06 — 图1: 术语速查
# ============================================================
def make_L06_01_cheatsheet():
    W, H = 900, 560
    dwg = new_svg(W, H)
    add_text(dwg, "音频术语速查表", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    terms = [
        ("Hz 赫兹", "频率单位：20Hz~20kHz 人耳范围", ACCENT),
        ("dB 分贝", "音量单位（对数）：+10dB 响 2 倍", ACCENT),
        ("AudioSource", "声源组件：挂在发声物体上", ACCENT),
        ("AudioListener", "听者组件：全场景唯一，挂玩家", ACCENT),
        ("AudioClip", "音频文件导入后的数据资源", SUCCESS),
        ("AudioMixer", "混音器：总线分组调音量", SUCCESS),
        ("3D 声音", "带位置感的音效（距离衰减）", SUCCESS),
        ("2D 声音", "恒定音量（UI、BGM）", SUCCESS),
        ("Ducking", "侧链闪避：对白时压低音乐", WARM),
        ("Streaming", "流式加载：长音频边播边读", WARM),
        ("Loop 循环", "音频循环播放", WARM),
        ("SendCustomNetworkEvent", "Udon 全网广播事件（同步播放）", WARM),
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
        ("没有声音", "听者缺失 / 声源音量 0\n/ 没勾 Play On Awake", "检查 AudioListener\n检查音量与 3D 距离", "#ff88cc"),
        ("两个 Listener 报错", "场景里挂了两份听者\n（如相机 + 玩家各一个）", "只留一个", WARN),
        ("声音太远听不见", "3D 衰减半径太小", "拉大 Min/Max Distance", WARN),
        ("声音发闷/破音", "音量超过 0dB 爆音\n文件质量太低", "调总线音量\n换高质量音频源", ACCENT),
        ("只有自己听到", "用了本地 Play()", "改 SendCustomNetworkEvent", SUCCESS),
        ("音乐一直停不下来", "没做 Stop/条件控制", "Udon 里加 Stop()", SUCCESS),
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
        for j, line in enumerate(cause.split("\n")):
            add_text(dwg, line, 245 + col_w[1]//2, y + 24 + j * 18, fill=TEXT_DIM, size=11, anchor="middle")
        add_rect(dwg, 560, y, col_w[2], 60, fill=PANEL, stroke=SUCCESS, rx=6)
        for j, line in enumerate(sol.split("\n")):
            add_text(dwg, line, 560 + col_w[2]//2, y + 24 + j * 18, fill=SUCCESS, size=11, anchor="middle")

    add_text(dwg, "调试：Scene 视图选中声源可看到衰减圈；用 AudioMixer 看各总线是否在响", W//2, 520, fill=TEXT_MUTED, size=12, anchor="middle", italic=True)
    save_svg_and_png(dwg, "L06_02_common_issues")


# ============================================================
# L06 — 图3: 进阶路线
# ============================================================
def make_L06_03_roadmap():
    W, H = 900, 440
    dwg = new_svg(W, H)
    add_text(dwg, "进阶路线图", W//2, 32, fill=TEXT, size=20, weight="bold", anchor="middle")

    stages = [
        ("入门 · 会出声", "挂声源、会导入\n会调音量", ACCENT, "现在"),
        ("熟练 · 会混音", "总线分组 / Ducking\n3D 衰减调出空间感", SUCCESS, "1 周"),
        ("进阶 · 会编程", "Udon 控制音频\n网络事件同步播放", WARM, "1 个月"),
        ("精通 · 会设计", "动态音乐（分层切换）\n音频反馈设计", "#c084fc", "长期"),
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
    add_text(dwg, "① 每个音效都问：它该是 2D 还是 3D？该进哪条总线？  ② 音量用 dB 思考，别拍脑袋", 130, 358, fill=TEXT_DIM, size=12.5)
    add_text(dwg, "③ 反复听优秀世界的音频设计  ④ 混音永远在最终设备上验证（耳机 + 外放）", 130, 382, fill=TEXT_DIM, size=12.5)

    save_svg_and_png(dwg, "L06_03_roadmap")


if __name__ == "__main__":
    for f in [make_L01_01_sound_wave, make_L01_02_audio_components,
              make_L02_01_formats, make_L02_02_import_settings,
              make_L03_01_3d_sound, make_L03_02_mixer_buses, make_L03_03_ducking,
              make_L04_01_vrc_audio_flow, make_L04_02_udon_audio, make_L04_03_limits,
              make_L05_01_steps, make_L05_02_layout,
              make_L06_01_cheatsheet, make_L06_02_common_issues, make_L06_03_roadmap]:
        print(f"生成 {f.__name__} ...")
        f()
    print("全部完成")
