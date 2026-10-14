# -*- coding: utf-8 -*-
"""
麦门灵魂小票 · 情绪漫画长卡 002 ——「不想上班」（补电型）
=========================================================
场景：今天真的不想上班 / 语义意图「补电型」（tone = gentle_comfort）
数据：2026-10-14 15:55 麦当劳 MCP 实时返回（门店 1400757，到店自取）
      · calculate-price → 合计 ¥48.00（traceId 9f9f986ef034da66bab485febeba3679，discount 0）
      · 板烧鸡腿堡 1406 ¥24.00 / 中薯条 4810 ¥14.00 / 小杯鲜萃咖啡 520689 ¥10.00
      · query-store-coupons → 「中薯条买一送一」券与本配餐直接相关，用券实证 ¥13.50
        （原 ¥27.00 · 已省 ¥13.50，traceId 8c6d44d820a33ab53fc92c19f5d3b0d0）
规范依据：references/visual-design-rules.md（锁定 token）+ references/comic-spec.md
版式实现：card_theme.py（可复用构件，本文件只负责四格与文案）
所有图形均为内联 SVG 参数化绘制，不调用任何 AI 画图。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_comic_card as B                                                    # noqa: E402
from gen_comic_card import (txt, maizai, bubble, desk, monitor, wavy, F_MONO)  # noqa: E402
import card_theme as T                                                        # noqa: E402

THEME = "#4C6E9E"        # 情绪色·补电型 → 低电量蓝（锁定表取值）
B.THEME = THEME          # 让基座 monitor 的进度条与本卡主题色一致

RED = T.RED
INK, MUTED = T.INK, T.MUTED
BLANK, BLANK_E = "#AEBAD6", "#93A1C4"


def meta(s):
    return txt(458, 42, s, T.F_META, T.MUTED, anchor="end")


# ══════════════════ 本卡专用道具（参数化 SVG）══════════════════
def ic_fries(cx, cy, s=1.0):
    """中薯条：经典红盒 + 四根薯条。"""
    o = []
    for dx, rot in ((-14, -9), (-5, -3), (5, 3), (14, 9)):
        x = cx + dx * s
        o.append(f'<g transform="rotate({rot} {x:.1f} {cy - 16 * s:.1f})">'
                 f'<rect x="{x - 5 * s:.1f}" y="{cy - 36 * s:.1f}" width="{10 * s:.1f}" '
                 f'height="{32 * s:.1f}" rx="{4 * s:.1f}" fill="{B.FRY}" '
                 f'stroke="{B.FRY_ED}" stroke-width="{1.3 * s:.2f}"/></g>')
    ht, hb, bt = 27 * s, 22 * s, cy - 8 * s
    bb = cy + 30 * s
    o.append(f'<path d="M{cx - ht:.1f} {bt:.1f} L{cx + ht:.1f} {bt:.1f} '
             f'L{cx + hb:.1f} {bb:.1f} L{cx - hb:.1f} {bb:.1f} Z" fill="{RED}"/>')
    o.append(f'<path d="M{cx - ht:.1f} {bt:.1f} L{cx + ht:.1f} {bt:.1f}" '
             f'stroke="#A80006" stroke-width="{1.5 * s:.2f}"/>')
    o.append(f'<path d="{wavy(cx - ht + 3 * s, bt + 13 * s, ht * 2 - 6 * s, 1.8 * s, 4)}" '
             f'fill="none" stroke="#FFFFFF" stroke-width="{2 * s:.2f}" opacity="0.9"/>')
    return "".join(o)


def ic_coffee(cx, cy, s=1.0):
    """小杯鲜萃咖啡：白杯 + 咖啡液面 + 杯盖 + 热气。"""
    w, h = 36 * s, 42 * s
    top, bot = cy - h / 2 + 7 * s, cy + h / 2
    return "".join([
        f'<path d="M{cx - w / 2:.1f} {top:.1f} L{cx + w / 2:.1f} {top:.1f} '
        f'L{cx + w / 2 - 6 * s:.1f} {bot:.1f} L{cx - w / 2 + 6 * s:.1f} {bot:.1f} Z" '
        f'fill="{T.SURFACE}" stroke="#BFB9AE" stroke-width="{1.5 * s:.2f}"/>',
        f'<path d="M{cx - w / 2 + 3 * s:.1f} {cy - 2 * s:.1f} L{cx + w / 2 - 3 * s:.1f} {cy - 2 * s:.1f} '
        f'L{cx + w / 2 - 5 * s:.1f} {cy + 12 * s:.1f} L{cx - w / 2 + 5 * s:.1f} {cy + 12 * s:.1f} Z" '
        f'fill="#8A5A2B"/>',
        f'<rect x="{cx - w / 2 - 3 * s:.1f}" y="{cy - h / 2:.1f}" width="{w + 6 * s:.1f}" '
        f'height="{8 * s:.1f}" rx="{3 * s:.1f}" fill="#E8E4DC" stroke="#BFB9AE" '
        f'stroke-width="{1.2 * s:.2f}"/>',
        f'<path d="{wavy(cx - 7 * s, cy - h / 2 - 12 * s, 14 * s, 2.6 * s, 2)}" fill="none" '
        f'stroke="#BFB9AE" stroke-width="{2.2 * s:.2f}" stroke-linecap="round" opacity="0.8"/>'])


def alarm(cx, cy, r):
    """闹钟：双铃 + 指针 + 抖动的声波。"""
    return "".join([
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{T.SURFACE}" stroke="{INK}" stroke-width="3.2"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 6:.1f}" fill="none" stroke="{T.HAIR}" stroke-width="1.4"/>',
        f'<path d="M{cx - r * 0.62:.1f} {cy - r * 0.95:.1f} L{cx - r * 1.0:.1f} {cy - r * 1.3:.1f}" '
        f'stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>',
        f'<path d="M{cx + r * 0.62:.1f} {cy - r * 0.95:.1f} L{cx + r * 1.0:.1f} {cy - r * 1.3:.1f}" '
        f'stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>',
        f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r * 0.55:.1f}" stroke="{INK}" '
        f'stroke-width="3" stroke-linecap="round"/>',
        f'<line x1="{cx}" y1="{cy}" x2="{cx + r * 0.42:.1f}" y2="{cy + r * 0.18:.1f}" '
        f'stroke="{RED}" stroke-width="3" stroke-linecap="round"/>',
        f'<line x1="{cx - r * 1.5:.1f}" y1="{cy - r * 0.4:.1f}" x2="{cx - r * 1.9:.1f}" '
        f'y2="{cy - r * 0.55:.1f}" stroke="{MUTED}" stroke-width="2.6" stroke-linecap="round"/>',
        f'<line x1="{cx + r * 1.5:.1f}" y1="{cy - r * 0.4:.1f}" x2="{cx + r * 1.9:.1f}" '
        f'y2="{cy - r * 0.55:.1f}" stroke="{MUTED}" stroke-width="2.6" stroke-linecap="round"/>'])


def battery(x, y, w, h):
    """电量条：空壳 + 8% 红格。"""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h * 0.32:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="2.6"/>'
            f'<rect x="{x + w + 3:.1f}" y="{y + h * 0.3:.1f}" width="6" height="{h * 0.4:.1f}" '
            f'rx="2" fill="{INK}"/>'
            f'<rect x="{x + 4:.1f}" y="{y + 4:.1f}" width="{(w - 8) * 0.08:.1f}" '
            f'height="{h - 8:.1f}" rx="2.5" fill="{RED}"/>')


# ══════════════════ 四格（内部 478×320）══════════════════
def panel1():
    """01 起 · 今天发生了什么：07:00，第三个闹钟，身体没有跟上。"""
    return "".join([
        bubble(20, 24, 258, ["今天真的不想上班！"], T.F_TALK,
               tail=("down", 170, 0), lh=30),
        alarm(72, 168, 34),
        f'<rect x="150" y="200" width="140" height="46" rx="20" '
        f'fill="#E8ECF5" stroke="#C9CEDC" stroke-width="1.6"/>',
        maizai(272, 174, 1.15, "丧", arms="down", tilt=-2),
        f'<rect x="152" y="238" width="238" height="82" rx="16" '
        f'fill="{BLANK}" stroke="{BLANK_E}" stroke-width="1.8"/>',
        f'<path d="{wavy(170, 266, 202, 2.6, 5)}" fill="none" stroke="#FFFFFF" '
        f'stroke-width="2.2" opacity="0.65"/>',
        txt(408, 136, "Zzz", 22, MUTED, weight="600"),
        meta("07:00 · 第 3 个闹钟"),
    ])


def panel2():
    """02 承 · 情绪被看见：10:00 工位上，电量只剩 3%。"""
    return "".join([
        bubble(18, 26, 200, ["我想暂停一下。"], T.F_LABEL,
               tail=("down", 120, 0), lh=26),
        desk(292, 20, 458),
        monitor(226, 138, 196, 118),
        battery(276, 182, 84, 32),
        txt(376, 206, "3%", 22, RED, weight="700"),
        maizai(116, 216, 1.12, "累", arms="down"),
        meta("10:00 · 工位"),
    ])


def panel3():
    """03 转 · 麦门出场：三样真实在售餐品（画面不出价格）。"""
    o = [desk(292, 20, 458),
         txt(24, 42, "12:30 · 麦门", T.F_META, MUTED)]
    for cx, fn, nm in ((96, B.ic_burger, "板烧鸡腿堡"),
                       (230, ic_fries, "中薯条"),
                       (364, ic_coffee, "小杯鲜萃咖啡")):
        o.append(fn(cx, 142, 1.55))
        o.append(txt(cx, 240, nm, T.F_LABEL, INK, anchor="middle", weight="700"))
    return "".join(o)


def panel4():
    """04 合 · 故事的结尾：先吃饭，其他的先待机（不强行开心）。"""
    return "".join([
        desk(292, 20, 458),
        maizai(148, 208, 1.16, "喜", arms="hold"),
        ic_coffee(228, 178, 1.12),
        bubble(276, 46, 194, ["先吃饭。", "其他的，待机。"], T.F_LABEL,
               tail=("left", 0, 126), lh=28),
        meta("12:47"),
    ])


SVG = T.build_svg(
    title="麦门灵魂小票 · 情绪漫画长卡 002（今天真的不想上班）",
    desc="1080×1920 长卡：四格漫画为故事主体，餐品只在 03 格作道具出场（格内不含价格）；"
         "价格与券仅出现在「今日情绪配餐」信息区。板烧鸡腿堡 ¥24.00 / 中薯条 ¥14.00 / "
         "小杯鲜萃咖啡 ¥10.00，合计 ¥48.00，均来自麦当劳 MCP 2026-10-14 15:55 实时核价"
         "（门店 1400757，traceId 9f9f986ef034da66bab485febeba3679）。券「中薯条买一送一」"
         "与本配餐相关，用券实证 ¥13.50（原 ¥27.00，traceId 8c6d44d820a33ab53fc92c19f5d3b0d0）。"
         "角色「麦仔」为原创设定。",
    panels=[panel1, panel2, panel3, panel4],
    header_args=("2026-10-14 · 补电型", "002",
                 "今天真的不想上班！",
                 "今日状态：电量不足，急需暂停。", THEME),
    meal_args=dict(
        theme=THEME,
        rows=[("板烧鸡腿堡", "¥24.00"),
              ("中薯条", "¥14.00"),
              ("小杯鲜萃咖啡", "¥10.00")],
        total="¥48.00",
        reason_lines=["推荐理由：咖啡因优先 · 温热补电 · 不催你振作",
                      "情绪基调：不解决所有问题，只解决这一顿。"],
        coupon=("中薯条买一送一", "¥13.50", "原 ¥27.00 · 已省 ¥13.50")),
    verdict="今天不想解决所有问题，那就先解决这一顿。",
    settle_rows=[("今日消耗", "假装在工位的一整天"),
                 ("今日找零", "一杯热咖啡的十分钟")],
    seed=20261015)

T.emit("comic-card-02.svg", SVG)
