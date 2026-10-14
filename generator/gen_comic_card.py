# -*- coding: utf-8 -*-
"""
麦门灵魂小票 · SVG 基础构件库（shared primitives）
====================================================
整套视觉的底层积木：文字排版 / 角色「麦仔」/ 场景道具（桌面・显示器・台灯・纸堆）/
餐品图标（汉堡・鸡排・可乐）/ 对话气泡 / 结算条锯齿路径 / 条码 / 扫描纹理。

不含版式与文案 —— 版式锁定在 `card_theme.py`，单卡故事在 `gen_card_NN.py`。
所有图形均为内联 SVG 参数化绘制，零依赖、不调用任何 AI 画图。
"""

# -*- coding: utf-8 -*-
"""
麦门灵魂小票 · 数字情绪漫画卡 v1（首张样卡）
场景：被导师改崩溃 / 语义意图「发泄型」
数据：2026-10-14 麦当劳 MCP 真实返回（门店 1400757）

规范依据：references/comic-spec.md + references/receipt-spec.md
所有图形均为内联 SVG，不调用任何 AI 画图。
"""
import os


INK     = "#26221C"
MUTED   = "#8D8577"
GOLD    = "#FFC72C"
PAPER   = "#FCF9F2"
EDGE    = "#DDD5C4"
FRY     = "#F5C244"
FRY_ED  = "#C98A12"
DARK    = "#3A2A16"
THEME   = "#5A6BA8"   # 默认主题色（monitor 使用；单卡以 card_theme 的主题色覆盖）
REDBOX  = "#DB0007"   # 薯条盒红

F_TXT  = '"PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif'
F_KAI  = '"KaiTi","STKaiti","楷体","Microsoft YaHei",serif'
F_MONO = '"SFMono-Regular","Menlo","Consolas","Microsoft YaHei",monospace'


def q(s):
    return "'" + s + "'"


QT, QK, QM = q(F_TXT), q(F_KAI), q(F_MONO)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=12, color=INK, anchor="start", weight="400",
        ls=0, font=F_TXT, opacity=None):
    fq = QK if font is F_KAI else (QM if font is F_MONO else QT)
    extra = f' letter-spacing="{ls}"' if ls else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family={fq} font-size="{size}" '
            f'fill="{color}" text-anchor="{anchor}" font-weight="{weight}"'
            f'{extra}{op}>{esc(s)}</text>')


def est_w(s, size):
    w = 0.0
    for ch in s:
        o = ord(ch)
        if o > 0x2E7F:
            w += size
        elif ch in "·™'":
            w += size * 0.5
        elif ch in "，。、：（）「」":
            w += size
        else:
            w += size * 0.55
    return w


def arches(cx, y0, h, color=GOLD):
    """金色拱门 M。逻辑 0 0 48 44 缩放到 h。"""
    s = h / 44.0
    w = 48 * s
    x = cx - w / 2
    p = ("M2,44 C2,14 9,2 14,2 C19,2 22,12 24,26 "
         "C26,12 29,2 34,2 C39,2 46,14 46,44 "
         "L38,44 C38,20 35,10 34,10 C33,10 30,24 30,44 "
         "L18,44 C18,24 15,10 14,10 C13,10 10,20 10,44 Z")
    return (f'<g transform="translate({x:.1f},{y0:.1f}) scale({s:.4f})">'
            f'<path d="{p}" fill="{color}"/></g>')


def wavy(x0, y, w, amp=1.5, n=4):
    step = w / n
    d = f"M{x0:.1f} {y:.1f}"
    for i in range(n):
        a = amp if i % 2 == 0 else -amp
        d += f" q {step / 2:.2f} {a:.2f} {step:.2f} 0"
    return d


# ══════════════════════════════════ 角色：麦仔 ══
BW, BH = 60.0, 96.0          # 基准身宽 60 / 身高 96 → 1:1.6
BOX_RATIO = 0.28             # 薯条盒占全身高度


def _eyes(kind, cx, cy, s):
    lx, rx = cx - 10.2 * s, cx + 10.2 * s
    r = 3.0 * s
    C = DARK
    o = []
    if kind == "呆":
        for ex in (lx, rx):
            o.append(f'<circle cx="{ex:.1f}" cy="{cy:.1f}" r="{r:.2f}" fill="{C}"/>')
            o.append(f'<circle cx="{ex - r * 0.32:.1f}" cy="{cy - r * 0.36:.1f}" '
                     f'r="{r * 0.3:.2f}" fill="#FFFFFF" opacity="0.85"/>')
    elif kind == "喜":
        for ex in (lx, rx):
            o.append(f'<path d="M{ex - r * 1.5:.1f} {cy + r * 0.45:.1f} '
                     f'A {r * 1.5:.2f} {r * 1.7:.2f} 0 0 1 {ex + r * 1.5:.1f} {cy + r * 0.45:.1f}" '
                     f'fill="none" stroke="{C}" stroke-width="{1.9 * s:.2f}" stroke-linecap="round"/>')
    elif kind == "丧":
        for ex in (lx, rx):
            o.append(f'<circle cx="{ex:.1f}" cy="{cy:.1f}" r="{r:.2f}" fill="{C}"/>')
            o.append(f'<line x1="{ex - r * 1.6:.1f}" y1="{cy - r * 0.55:.1f}" '
                     f'x2="{ex + r * 1.6:.1f}" y2="{cy - r * 0.55:.1f}" '
                     f'stroke="{C}" stroke-width="{1.9 * s:.2f}" stroke-linecap="round"/>')
    elif kind == "惊":
        for ex in (lx, rx):
            o.append(f'<circle cx="{ex:.1f}" cy="{cy:.1f}" r="{r * 1.4:.2f}" fill="{C}"/>')
            o.append(f'<circle cx="{ex - r * 0.45:.1f}" cy="{cy - r * 0.5:.1f}" '
                     f'r="{r * 0.42:.2f}" fill="#FFFFFF" opacity="0.85"/>')
    elif kind == "累":
        for ex, d in ((lx, -1), (rx, 1)):
            o.append(f'<path d="M{ex - d * r * 1.3:.1f} {cy - r:.1f} '
                     f'L{ex + d * r * 0.3:.1f} {cy:.1f} '
                     f'L{ex - d * r * 1.3:.1f} {cy + r:.1f}" fill="none" stroke="{C}" '
                     f'stroke-width="{1.9 * s:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
    elif kind == "无语":
        for ex in (lx, rx):
            o.append(f'<line x1="{ex - r * 1.6:.1f}" y1="{cy:.1f}" '
                     f'x2="{ex + r * 1.6:.1f}" y2="{cy:.1f}" stroke="{C}" '
                     f'stroke-width="{1.9 * s:.2f}" stroke-linecap="round"/>')
    return "".join(o)


def _mouth(kind, cx, cy, s):
    C = DARK
    w = 12.0 * s
    sw = 1.9 * s
    if kind == "下弯":
        return (f'<path d="M{cx - w / 2:.1f} {cy + w * 0.22:.1f} '
                f'Q {cx:.1f} {cy - w * 0.3:.1f} {cx + w / 2:.1f} {cy + w * 0.22:.1f}" '
                f'fill="none" stroke="{C}" stroke-width="{sw:.2f}" stroke-linecap="round"/>')
    if kind == "上弯":
        return (f'<path d="M{cx - w / 2:.1f} {cy - w * 0.18:.1f} '
                f'Q {cx:.1f} {cy + w * 0.36:.1f} {cx + w / 2:.1f} {cy - w * 0.18:.1f}" '
                f'fill="none" stroke="{C}" stroke-width="{sw:.2f}" stroke-linecap="round"/>')
    if kind == "平直":
        return (f'<line x1="{cx - w * 0.38:.1f}" y1="{cy:.1f}" '
                f'x2="{cx + w * 0.38:.1f}" y2="{cy:.1f}" stroke="{C}" '
                f'stroke-width="{sw:.2f}" stroke-linecap="round"/>')
    if kind == "O":
        return (f'<ellipse cx="{cx:.1f}" cy="{cy + w * 0.1:.1f}" rx="{w * 0.2:.1f}" '
                f'ry="{w * 0.26:.1f}" fill="none" stroke="{C}" stroke-width="{sw:.2f}"/>')
    if kind == "波浪":
        return (f'<path d="M{cx - w / 2:.1f} {cy:.1f} q {w / 6:.1f} {-w * 0.22:.1f} {w / 3:.1f} 0 '
                f'q {w / 6:.1f} {w * 0.22:.1f} {w / 3:.1f} 0" fill="none" stroke="{C}" '
                f'stroke-width="{sw:.2f}" stroke-linecap="round"/>')
    return ""


EXPR = {
    "丧":   ("丧", "下弯"),
    "呆":   ("呆", "平直"),
    "惊":   ("惊", "O"),
    "喜":   ("喜", "上弯"),
    "累":   ("累", "波浪"),
    "无语": ("无语", "平直"),
}


def maizai(cx, cy, s=1.0, expr="呆", arms="down", tilt=0.0):
    """麦仔。(cx,cy) 为身体中心，s 为缩放。
    身体比例与薯条盒高度恒定，表情只改眼型嘴型。"""
    bw, bh = BW * s, BH * s
    x0, y0 = cx - bw / 2, cy - bh / 2
    ex, em = EXPR[expr]
    o = []
    if tilt:
        o.append(f'<g transform="rotate({tilt:.2f} {cx:.1f} {cy:.1f})">')

    # 手臂（画在身体后面）
    if arms == "down":
        o.append(f'<path d="M{x0 + 3:.1f} {cy + 3:.1f} L{x0 - 19 * s:.1f} {cy + 17 * s:.1f}" '
                 f'fill="none" stroke="{FRY_ED}" stroke-width="{3.4 * s:.2f}" stroke-linecap="round"/>')
        o.append(f'<path d="M{x0 + bw - 3:.1f} {cy + 3:.1f} L{x0 + bw + 19 * s:.1f} {cy + 17 * s:.1f}" '
                 f'fill="none" stroke="{FRY_ED}" stroke-width="{3.4 * s:.2f}" stroke-linecap="round"/>')
    elif arms == "up":
        o.append(f'<path d="M{x0 + 3:.1f} {cy - 4:.1f} L{x0 - 15 * s:.1f} {cy - 27 * s:.1f}" '
                 f'fill="none" stroke="{FRY_ED}" stroke-width="{3.4 * s:.2f}" stroke-linecap="round"/>')
        o.append(f'<path d="M{x0 + bw - 3:.1f} {cy - 4:.1f} L{x0 + bw + 15 * s:.1f} {cy - 27 * s:.1f}" '
                 f'fill="none" stroke="{FRY_ED}" stroke-width="{3.4 * s:.2f}" stroke-linecap="round"/>')
    elif arms == "hold":
        o.append(f'<path d="M{x0 + 3:.1f} {cy + 2:.1f} L{x0 - 18 * s:.1f} {cy + 15 * s:.1f}" '
                 f'fill="none" stroke="{FRY_ED}" stroke-width="{3.4 * s:.2f}" stroke-linecap="round"/>')
        o.append(f'<path d="M{x0 + bw - 4:.1f} {cy + 1:.1f} L{x0 + bw + 20 * s:.1f} {cy - 10 * s:.1f}" '
                 f'fill="none" stroke="{FRY_ED}" stroke-width="{3.4 * s:.2f}" stroke-linecap="round"/>')

    # 身体（一根薯条）
    o.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
             f'rx="{13 * s:.1f}" fill="{FRY}" stroke="{FRY_ED}" stroke-width="{1.7 * s:.2f}"/>')
    o.append(f'<path d="M{cx - 11 * s:.1f} {y0 + 9 * s:.1f} L{cx - 11 * s:.1f} {y0 + bh * 0.6:.1f}" '
             f'stroke="#FFDD8E" stroke-width="{2.6 * s:.2f}" stroke-linecap="round" opacity="0.85"/>')
    o.append(f'<path d="M{cx - 2 * s:.1f} {y0 + 7 * s:.1f} L{cx - 2 * s:.1f} {y0 + bh * 0.52:.1f}" '
             f'stroke="#FFDD8E" stroke-width="{2.2 * s:.2f}" stroke-linecap="round" opacity="0.7"/>')

    # 薯条盒（下半身 28%）
    box_h = bh * BOX_RATIO
    bt = y0 + bh - box_h
    ht, hb = bw * 0.545, bw * 0.475
    o.append(f'<path d="M{cx - ht:.1f} {bt:.1f} L{cx + ht:.1f} {bt:.1f} '
             f'L{cx + hb:.1f} {y0 + bh:.1f} L{cx - hb:.1f} {y0 + bh:.1f} Z" fill="{REDBOX}"/>')
    o.append(f'<path d="M{cx - ht:.1f} {bt:.1f} L{cx + ht:.1f} {bt:.1f}" '
             f'stroke="#A80006" stroke-width="{1.6 * s:.2f}"/>')
    o.append(f'<path d="{wavy(cx - ht + 2 * s, bt + box_h * 0.38, (ht * 2 - 4 * s), 1.5 * s, 4)}" '
             f'fill="none" stroke="#FFFFFF" stroke-width="{1.7 * s:.2f}" opacity="0.9"/>')
    o.append(f'<path d="{wavy(cx - hb + 1 * s, bt + box_h * 0.72, (hb * 2 - 2 * s), 1.5 * s, 4)}" '
             f'fill="none" stroke="#FFFFFF" stroke-width="{1.5 * s:.2f}" opacity="0.65"/>')

    # 脸
    ey = y0 + bh * 0.40
    o.append(_eyes(ex, cx, ey, s))
    o.append(_mouth(em, cx, y0 + bh * 0.60, s))
    for sx in (cx - 17 * s, cx + 17 * s):
        o.append(f'<ellipse cx="{sx:.1f}" cy="{ey + 9 * s:.1f}" rx="{5.2 * s:.1f}" '
                 f'ry="{3.4 * s:.1f}" fill="#F09A6A" opacity="0.4"/>')

    if tilt:
        o.append('</g>')
    return "".join(o)


# ══════════════════════════════ 场景素材 ══
def paper(x, y, w, h, fill="#FFFFFF", edge="#D6D0C2"):
    o = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="1.5" '
         f'fill="{fill}" stroke="{edge}" stroke-width="0.8"/>']
    ly = y + 6.5
    while ly < y + h - 4:
        o.append(f'<line x1="{x + 5:.1f}" y1="{ly:.1f}" x2="{x + w - 5:.1f}" y2="{ly:.1f}" '
                 f'stroke="#D2CCBE" stroke-width="0.75"/>')
        ly += 6.0
    return "".join(o)


def pile(x, y_bot, w, h, n=3, edge="#D6D0C2"):
    """一摞（错位纸张），底边对齐 y_bot"""
    o = []
    for i in range(n):
        dx = (i - (n - 1) / 2) * 1.6
        o.append(paper(x + dx, y_bot - h - i * 1.4, w, h, edge=edge))
    return "".join(o)


def monitor(x, y, w, h, glow=True):
    o = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="4" '
         f'fill="#4A4E5C" stroke="#3A3E4A" stroke-width="1.4"/>',
         f'<rect x="{x + 4:.1f}" y="{y + 4:.1f}" width="{w - 8:.1f}" height="{h - 8:.1f}" rx="2" '
         f'fill="{"#E9EDF7" if glow else "#DDE1EA"}"/>']
    ly = y + 13
    ws = [0.72, 0.55, 0.8, 0.4, 0.66, 0.32]
    for i, fr in enumerate(ws):
        if ly > y + h - 8:
            break
        c = "#B9C0D2" if i % 3 else THEME
        o.append(f'<rect x="{x + 10:.1f}" y="{ly:.1f}" width="{(w - 22) * fr:.1f}" height="3.2" '
                 f'rx="1.6" fill="{c}" opacity="{0.85 if i % 3 == 0 else 0.55}"/>')
        ly += 7.4
    o.append(f'<rect x="{x + w / 2 - 9:.1f}" y="{y + h:.1f}" width="18" height="8" fill="#4A4E5C"/>')
    o.append(f'<rect x="{x + w / 2 - 20:.1f}" y="{y + h + 7:.1f}" width="40" height="3.4" rx="1.7" '
             f'fill="#4A4E5C"/>')
    return "".join(o)


def lamp(x, y):
    o = [f'<path d="M{x:.1f} {y + 78:.1f} L{x:.1f} {y + 20:.1f} L{x + 26:.1f} {y:.1f}" '
         f'fill="none" stroke="#8A8F9E" stroke-width="2.6" stroke-linecap="round" '
         f'stroke-linejoin="round"/>',
         f'<path d="M{x + 18:.1f} {y - 6:.1f} L{x + 44:.1f} {y + 8:.1f} L{x + 30:.1f} {y + 22:.1f} Z" '
         f'fill="#F0D9A0" stroke="#C9A75C" stroke-width="1.3"/>',
         f'<ellipse cx="{x:.1f}" cy="{y + 79:.1f}" rx="13" ry="3.4" fill="#B9BEC9"/>']
    return "".join(o)


def desk(y, x0, x1, color="#C6CAD6"):
    return (f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke="{color}" '
            f'stroke-width="2.4" stroke-linecap="round"/>')


def red_mark(x, y, w=24, n=3):
    """红色批改波浪线（导师批注痕迹）"""
    return (f'<path d="{wavy(x, y, w, 1.7, n)}" fill="none" stroke="#D8352E" '
            f'stroke-width="1.5" stroke-linecap="round" opacity="0.78"/>')


# ══════════════════════════ 餐品简笔图标 ══
def ic_burger(cx, cy, s=1.0):
    w = 46 * s
    o = [f'<path d="M{cx - w / 2:.1f} {cy - 9 * s:.1f} A {w / 2:.1f} {17 * s:.1f} 0 0 1 '
         f'{cx + w / 2:.1f} {cy - 9 * s:.1f} Z" fill="#E8A85C" stroke="#C98A12" '
         f'stroke-width="{1.4 * s:.2f}"/>',
         f'<rect x="{cx - w / 2 + 1 * s:.1f}" y="{cy - 8.6 * s:.1f}" width="{w - 2 * s:.1f}" '
         f'height="{7 * s:.1f}" rx="2.4" fill="#8A5A2B"/>',
         f'<rect x="{cx - w / 2 + 1 * s:.1f}" y="{cy - 1.4 * s:.1f}" width="{w - 2 * s:.1f}" '
         f'height="{5 * s:.1f}" rx="1.6" fill="#5FA84E" opacity="0.9"/>',
         f'<path d="M{cx - w / 2:.1f} {cy + 4 * s:.1f} L{cx + w / 2:.1f} {cy + 4 * s:.1f} '
         f'L{cx + w / 2 - 2 * s:.1f} {cy + 14 * s:.1f} L{cx - w / 2 + 2 * s:.1f} {cy + 14 * s:.1f} Z" '
         f'fill="#E8A85C" stroke="#C98A12" stroke-width="{1.4 * s:.2f}"/>']
    for i in range(3):
        o.append(f'<circle cx="{cx - 12 * s + i * 12 * s:.1f}" cy="{cy - 15 * s:.1f}" '
                 f'r="{1.7 * s:.1f}" fill="#FFF3D6" opacity="0.95"/>')
    return "".join(o)


def ic_chicken(cx, cy, s=1.0):
    w, h = 50 * s, 34 * s
    o = [f'<path d="M{cx - w / 2:.1f} {cy + 2 * s:.1f} '
         f'Q {cx - w / 2 + 3 * s:.1f} {cy - h / 2:.1f} {cx:.1f} {cy - h / 2 + 1 * s:.1f} '
         f'Q {cx + w / 2 - 2 * s:.1f} {cy - h / 2 - 2 * s:.1f} {cx + w / 2 - 2 * s:.1f} {cy + 4 * s:.1f} '
         f'Q {cx + w / 2 - 6 * s:.1f} {cy + h / 2:.1f} {cx:.1f} {cy + h / 2 - 1 * s:.1f} '
         f'Q {cx - w / 2 + 4 * s:.1f} {cy + h / 2 + 2 * s:.1f} {cx - w / 2:.1f} {cy + 2 * s:.1f} Z" '
         f'fill="#E8B055" stroke="#C98A12" stroke-width="{1.4 * s:.2f}"/>']
    for i, yy in enumerate((-1, 0.1, 1.2)):
        o.append(f'<path d="M{cx - w * 0.30:.1f} {cy + yy * 8 * s:.1f} '
                 f'q {w * 0.3:.1f} {-4 * s:.1f} {w * 0.6:.1f} 0" fill="none" stroke="#C98A12" '
                 f'stroke-width="{1.1 * s:.2f}" opacity="0.55"/>')
    return "".join(o)


def ic_cola(cx, cy, s=1.0):
    w, h = 34 * s, 48 * s
    o = [f'<path d="M{cx - w / 2:.1f} {cy - h / 2:.1f} L{cx + w / 2:.1f} {cy - h / 2:.1f} '
         f'L{cx + w / 2 - 5 * s:.1f} {cy + h / 2:.1f} L{cx - w / 2 + 5 * s:.1f} {cy + h / 2:.1f} Z" '
         f'fill="#D8352E" stroke="#A8241F" stroke-width="{1.4 * s:.2f}"/>',
         f'<rect x="{cx - w / 2 - 2 * s:.1f}" y="{cy - h / 2 - 5 * s:.1f}" width="{w + 4 * s:.1f}" '
         f'height="{6 * s:.1f}" rx="2" fill="#E8E4DC" stroke="#BFB9AE" stroke-width="1"/>',
         f'<path d="M{cx + 2 * s:.1f} {cy - h / 2 - 5 * s:.1f} L{cx + 8 * s:.1f} '
         f'{cy - h / 2 - 26 * s:.1f}" stroke="#E8E4DC" stroke-width="{4 * s:.2f}" '
         f'stroke-linecap="round"/>',
         f'<path d="M{cx + 6 * s:.1f} {cy - h / 2 - 20 * s:.1f} q {6 * s:.1f} {-3 * s:.1f} '
         f'{9 * s:.1f} {-6 * s:.1f}" stroke="#C0554F" stroke-width="{3 * s:.2f}" '
         f'stroke-linecap="round" opacity="0.75"/>',
         f'<rect x="{cx - w / 2 + 3 * s:.1f}" y="{cy - h / 2 + 10 * s:.1f}" width="{w - 6 * s:.1f}" '
         f'height="{14 * s:.1f}" rx="1.5" fill="#FFFFFF" opacity="0.9"/>']
    return "".join(o)


# ══════════════════════════════ 气泡 ══
def bubble(x, y, w, lines, size=12.5, tail=None, lh=19.5, pad=11,
           fill="#FFFFFF", edge=INK, color=INK, weight="500"):
    n = len(lines)
    h = pad * 2 + (n - 1) * lh + size
    o = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="9" '
         f'fill="{fill}" stroke="{edge}" stroke-width="1.15"/>']
    if tail:
        d, tx, ty = tail
        if d == "down":
            o.append(f'<path d="M{tx - 6:.1f} {y + h - 1:.1f} L{tx:.1f} {y + h + 12:.1f} '
                     f'L{tx + 6:.1f} {y + h - 1:.1f} Z" fill="{fill}" stroke="{edge}" '
                     f'stroke-width="1.15" stroke-linejoin="round"/>')
            o.append(f'<rect x="{tx - 5.4:.1f}" y="{y + h - 3:.1f}" width="10.8" height="4" fill="{fill}"/>')
        elif d == "left":
            o.append(f'<path d="M{x + 1:.1f} {ty - 6:.1f} L{x - 11:.1f} {ty:.1f} '
                     f'L{x + 1:.1f} {ty + 6:.1f} Z" fill="{fill}" stroke="{edge}" '
                     f'stroke-width="1.15" stroke-linejoin="round"/>')
            o.append(f'<rect x="{x - 1:.1f}" y="{ty - 5.4:.1f}" width="4" height="10.8" fill="{fill}"/>')
        elif d == "right":
            o.append(f'<path d="M{x + w - 1:.1f} {ty - 6:.1f} L{x + w + 11:.1f} {ty:.1f} '
                     f'L{x + w - 1:.1f} {ty + 6:.1f} Z" fill="{fill}" stroke="{edge}" '
                     f'stroke-width="1.15" stroke-linejoin="round"/>')
            o.append(f'<rect x="{x + w - 3:.1f}" y="{ty - 5.4:.1f}" width="4" height="10.8" fill="{fill}"/>')
    ly = y + pad + size * 0.82
    for ln in lines:
        o.append(txt(x + pad + 2, ly, ln, size, color, weight=weight))
        ly += lh
    return "".join(o)



def ticket(x0, y0, w, h, tooth=7, depth=4):
    n = int(w // tooth)
    p = [f"M{x0} {y0 + depth}"]
    x = x0
    for _ in range(n):
        p.append(f"L{x + tooth / 2} {y0} L{x + tooth} {y0 + depth}")
        x += tooth
    base = y0 + h - depth
    p.append(f"L{x0 + w} {base}")
    x = x0 + w
    for _ in range(n):
        p.append(f"L{x - tooth / 2} {y0 + h} L{x - tooth} {base}")
        x -= tooth
    p.append("Z")
    return " ".join(p)


def barcode(x0, y, seed, wmax, h=22):
    bars, x, s = [], x0, seed
    while x < x0 + wmax:
        s = (s * 1103515245 + 12345) % 2147483648
        bw = 0.9 + (s % 3) * 0.9
        bars.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{h}" fill="{INK}" '
                    f'opacity="0.82"/>')
        x += bw + 1.1 + ((s >> 7) % 3) * 0.9
    return "".join(bars)


DEFS = ('<defs><pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#3A2F1E" opacity="0.03"/></pattern></defs>')
