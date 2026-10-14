# -*- coding: utf-8 -*-
"""
card_theme.py — 麦门情绪小票 · 情绪卡套件（token 锁定版）

把 `references/visual-design-rules.md` 的锁定设计系统落成**可复用构件**：
品牌行 / 金横幅 / 四格 2×2 栅格 / 今日情绪配餐（含真实券条）/ TODAY'S MESSAGE /
情绪结算条 / 卡脚。每张新卡只需提供「四格面板 + 文案与数据」，版式与视觉自动守规范。

硬约束（改这里等于改设计系统，需同步改 references/visual-design-rules.md）：
  · 字号死线：正文 ≥24px、说明 ≥20px、meta ≥18px
  · 色相 ≤3：品牌金（横幅）+ 品牌红（券标/条码）+ 1 个情绪主题色
  · 字越大越细：大标题 w600，禁 w800/900
  · 间距只用 8/12/16/24/32/40/48/64/80/96
  · 卡面不出现运维/溯源信息（取数来源、券有效期等）
所有图形均为内联 SVG 参数化绘制，不调用任何 AI 画图。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_comic_card import txt, est_w, ticket, barcode, arches, F_MONO, DEFS  # noqa: E402

# ══════════════════ token（锁定）══════════════════
CW, CH = 1080, 1920
M = 48
IW = CW - M * 2                          # 984

PAPER    = "#FAF6EF"   # 奶油纸底
SURFACE  = "#FFFFFF"   # 卡面
OAT      = "#EDE4D3"   # 燕麦（信息区底）
INK      = "#33291F"   # 墨
MUTED    = "#8A7C6B"   # 次要
HAIR     = "#E2D8C6"   # 发丝线
GOLD     = "#FFC72C"   # 品牌金（仅横幅，≤12%）
GOLD_INK = "#5C4A08"
RED      = "#DB0007"   # 品牌红（仅券标/条码，≤1%）

# 字号层级
F_DISPLAY, F_SUB = 68, 26
F_KICKER = 20
F_TALK, F_LABEL = 23, 20
F_META = 18
F_H2, F_H3 = 32, 21
F_ROW = 21                 # 配餐明细（2026-10-14 反馈：明细字小一点）
F_TOTAL = 34
F_MSG = 44
F_SETTLE_T, F_SETTLE_L, F_SETTLE_V = 28, 22, 26
F_FOOT1, F_FOOT2 = 20, 18

# 版式栅格
BANNER_Y, BANNER_H = 96, 208
PW, PH, PGX, PGY = 478, 340, 28, 24
ROW1_Y = 336
ROW2_Y = ROW1_Y + PH + PGY               # 700
MEAL_Y, MEAL_H = ROW2_Y + PH + 32, 336   # 1072
MSG_KICK_Y, MSG_Y = 1440, 1498
SETTLE_Y, SETTLE_H = 1520, 286
FOOT_RULE, FOOT1, FOOT2 = 1834, 1858, 1882


def dotted(x0, x1, y, color=HAIR, w=1.4):
    return (f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" '
            f'stroke="{color}" stroke-width="{w}" stroke-dasharray="3 5"/>')


def hair(x0, x1, y, color=HAIR, w=1.2):
    return (f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" '
            f'stroke="{color}" stroke-width="{w}"/>')


# ══════════════════ 卡头 ══════════════════
def header(date_line, kicker_no, big_title, status, theme, deco=None):
    """卡头。deco：可选的横幅装饰 SVG 片段（如生日卡的薯条蜡烛）。"""
    o = [arches(M + 22, 38, 34),
         txt(M + 56, 62, "麦门情绪小票", F_KICKER, INK, weight="700", ls=1),
         txt(CW - M, 62, date_line, F_META, MUTED, anchor="end", font=F_MONO)]
    bx, by = M, BANNER_Y
    o.append(f'<rect x="{bx}" y="{by}" width="{IW}" height="{BANNER_H}" rx="24" fill="{GOLD}"/>')
    if deco:
        o.append(deco)
    o.append(txt(bx + 40, by + 56, f"MOOD RECEIPT / {kicker_no}", F_KICKER, GOLD_INK,
                 ls=2, font=F_MONO))
    o.append(txt(bx + 40, by + 136, big_title, F_DISPLAY, INK, weight="600"))
    o.append(txt(bx + 40, by + 182, status, F_SUB, GOLD_INK))
    return "".join(o)


# ══════════════════ 四格栅格 ══════════════════
def panel_block(fn, idx, y):
    px = M + (idx % 2) * (PW + PGX)
    return "".join([
        f'<rect x="{px}" y="{y}" width="{PW}" height="{PH}" rx="20" '
        f'fill="{SURFACE}" stroke="{HAIR}" stroke-width="1.6"/>',
        f'<g transform="translate({px},{y + 20})">{fn()}</g>'])


# ══════════════════ 今日情绪配餐 ══════════════════
def meal_block(theme, rows, total, reason_lines, coupon=None, y=MEAL_Y):
    """rows=[(名, 价)]；reason_lines=[两行说明]；coupon=(券名, 用券价, 原价说明) 或 None。

    coupon 必须来自 `query-store-coupons` + `calculate-price` 实证；**无券不硬凑**。
    """
    x0, lx = M, M + 36
    rx0, rx1 = M + 520, M + IW - 36
    o = [f'<rect x="{x0}" y="{y}" width="{IW}" height="{MEAL_H}" rx="20" '
         f'fill="{OAT}" stroke="{HAIR}" stroke-width="1.6"/>',
         txt(lx, y + 60, "今日情绪配餐", F_H2, INK, weight="800"),
         txt(lx, y + 102, reason_lines[0], F_H3, MUTED),
         txt(lx, y + 136, reason_lines[1], F_H3, MUTED)]
    ry = y + 60
    for nm, pr in rows:
        o.append(txt(rx0, ry, nm, F_ROW, INK))
        o.append(dotted(rx0 + est_w(nm, F_ROW) + 12, rx1 - est_w(pr, F_ROW) - 12, ry - 6))
        o.append(txt(rx1, ry, pr, F_ROW, INK, anchor="end"))
        ry += 40
    o.append(dotted(rx0, rx1, ry - 10))
    o.append(txt(rx0, ry + 26, "合计", F_SETTLE_L, MUTED))
    o.append(txt(rx1, ry + 30, total, F_TOTAL, theme, anchor="end", weight="800"))
    if coupon:
        cy0, ch = y + 232, 80
        name, cprice, corig = coupon
        o.append(f'<rect x="{x0 + 24}" y="{cy0}" width="{IW - 48}" height="{ch}" rx="12" '
                 f'fill="{SURFACE}" stroke="{HAIR}" stroke-width="1.4"/>')
        o.append(f'<rect x="{x0 + 44}" y="{cy0 + 23}" width="34" height="34" rx="8" fill="{RED}"/>')
        o.append(txt(x0 + 61, cy0 + 46, "券", F_FOOT2, "#FFFFFF", anchor="middle", weight="700"))
        o.append(txt(x0 + 92, cy0 + 51, name, F_LABEL, INK, weight="700"))
        o.append(txt(rx1 - 24, cy0 + 40, "用券 " + cprice, F_ROW + 3, RED,
                     anchor="end", weight="800"))
        o.append(txt(rx1 - 24, cy0 + 66, corig, F_FOOT2, MUTED, anchor="end"))
    return "".join(o)


# ══════════════════ TODAY'S MESSAGE / 结算条 / 卡脚 ══════════════════
def message(verdict):
    return "".join([
        txt(M + 2, MSG_KICK_Y, "TODAY'S MESSAGE", F_KICKER, MUTED, ls=3, font=F_MONO),
        txt(M + 2, MSG_Y, verdict, F_MSG, INK, weight="600")])


def settle(rows, seed, footer=None):
    y0, w = SETTLE_Y, IW
    cx = M + w / 2
    o = [f'<path d="{ticket(M, y0, w, SETTLE_H, tooth=14, depth=7)}" fill="#FCF9F2" '
         f'stroke="{HAIR}" stroke-width="1.4"/>',
         f'<path d="{ticket(M, y0, w, SETTLE_H, tooth=14, depth=7)}" fill="url(#scan)"/>',
         txt(cx, y0 + 54, "今日结算", F_SETTLE_T, INK, anchor="middle", weight="800", ls=10),
         dotted(M + 90, M + w - 90, y0 + 76)]
    ry = y0 + 116
    for lb, val in rows:
        o.append(txt(M + 80, ry, lb, F_SETTLE_L, MUTED))
        o.append(txt(M + 224, ry, val, F_SETTLE_V, INK, weight="700"))
        ry += 40
    o.append(dotted(M + 90, M + w - 90, y0 + 184))
    o.append(barcode(M + 140, y0 + 202, seed, w - 280, 32))
    o.append(txt(cx, y0 + 262, footer or "本小票不能报销，但可以报销心情", F_FOOT2, MUTED,
                 anchor="middle", ls=1))
    return "".join(o)


def foot(cta="麦门情绪小票 · 长按保存，分享今天"):
    return "".join([
        hair(340, 740, FOOT_RULE),
        txt(CW / 2, FOOT1, cta, F_FOOT1, INK, anchor="middle", weight="700", ls=2),
        txt(CW / 2, FOOT2, "mcd-soul-receipt · 餐品与价格来自麦当劳 MCP 真实数据",
            F_FOOT2, MUTED, anchor="middle", ls=0.8)])


def build_svg(title, desc, panels, header_args, meal_args, verdict, settle_rows,
              seed, cta=None):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" '
             f'width="{CW}" height="{CH}" role="img">',
             f'<title>{title}</title>', f'<desc>{desc}</desc>',
             f'<rect width="{CW}" height="{CH}" fill="{PAPER}"/>', DEFS,
             header(*header_args),
             panel_block(panels[0], 0, ROW1_Y), panel_block(panels[1], 1, ROW1_Y),
             panel_block(panels[2], 2, ROW2_Y), panel_block(panels[3], 3, ROW2_Y),
             meal_block(**meal_args), message(verdict), settle(settle_rows, seed),
             foot(cta) if cta else foot(),
             '</svg>']
    return "\n".join(parts)


ASSETS = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"))


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.getsize(path)


def emit(filename, content):
    """把 SVG 写进仓库 assets/ 目录（相对本文件解析，与当前工作目录无关）。"""
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, filename)
    n = write(path, content)
    print("written {} ({} bytes)".format(path, n))
    return path
