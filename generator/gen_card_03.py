# -*- coding: utf-8 -*-
"""
麦门灵魂小票 · 情绪漫画长卡 003 ——「生日」（仪式型）
=====================================================
场景：今天是我生日，但没人记得 / 语义意图「仪式型」（tone = ritual）
数据：2026-10-14 麦当劳 MCP 实时返回（门店 1400757，到店自取）
      · calculate-price → 合计 ¥36.00（discount 0）
      · 泷愿成真麦旋风——大米风味 521917 ¥16.00 / 心形薯饼5块 9900016082 ¥15.00
        / 圆筒冰淇淋 515837 ¥5.00
      · query-store-coupons → 「中薯条买一送一」券可用，用券实证 ¥13.50
        （原 ¥27.00 · 已省 ¥13.50，traceId c0ac9d29b406e84e12e1833c47748ea3）
规范依据：references/visual-design-rules.md（锁定 token）+ references/comic-spec.md
版式实现：card_theme.py（可复用构件，本文件只负责四格与文案）
所有图形均为内联 SVG 参数化绘制，不调用任何 AI 画图。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_comic_card import txt, maizai, bubble, desk                                # noqa: E402
import card_theme as T                                                              # noqa: E402

THEME = "#B0748E"        # 情绪色·仪式型 → 安慰玫瑰（锁定表取值）

SURFACE, HAIR, INK, MUTED = T.SURFACE, T.HAIR, T.INK, T.MUTED
F_TALK, F_LABEL, F_META = T.F_TALK, T.F_LABEL, T.F_META
dotted = T.dotted


# ══════════════════ 本卡专用道具（参数化 SVG）══════════════════
def flame(cx, cy, s=1.0):
    return "".join([
        f'<path d="M{cx} {cy - 15 * s:.1f} C {cx - 10 * s:.1f} {cy - 4 * s:.1f} '
        f'{cx - 7 * s:.1f} {cy + 7 * s:.1f} {cx} {cy + 7 * s:.1f} '
        f'C {cx + 7 * s:.1f} {cy + 7 * s:.1f} {cx + 10 * s:.1f} {cy - 4 * s:.1f} '
        f'{cx} {cy - 15 * s:.1f} Z" fill="#FFB03A"/>',
        f'<path d="M{cx} {cy - 6 * s:.1f} C {cx - 4.5 * s:.1f} {cy - 1 * s:.1f} '
        f'{cx - 3.4 * s:.1f} {cy + 6 * s:.1f} {cx} {cy + 6 * s:.1f} '
        f'C {cx + 3.4 * s:.1f} {cy + 6 * s:.1f} {cx + 4.5 * s:.1f} {cy - 1 * s:.1f} '
        f'{cx} {cy - 6 * s:.1f} Z" fill="#FFE07A"/>'])


def candle_fry(cx, cy, s=1.0):
    """一根薯条当蜡烛，插在甜品上。"""
    o = [f'<g transform="rotate(9 {cx:.1f} {cy:.1f})">'
         f'<rect x="{cx - 6.5 * s:.1f}" y="{cy - 30 * s:.1f}" width="{13 * s:.1f}" '
         f'height="{58 * s:.1f}" rx="{4.5 * s:.1f}" fill="#F5C244" stroke="#C98A12" '
         f'stroke-width="{1.4 * s:.2f}"/>'
         f'<path d="M{cx - 2.6 * s:.1f} {cy - 24 * s:.1f} L{cx - 2.6 * s:.1f} {cy + 16 * s:.1f}" '
         f'stroke="#FFDD8E" stroke-width="{2 * s:.2f}" stroke-linecap="round" opacity="0.8"/>'
         f'</g>']
    o.append(flame(cx + 2 * s, cy - 42 * s, s))
    return "".join(o)


def cream_tiers(cx, top, s, wds, color="#F6EBD6", edge="#DCC9A6"):
    return "".join(
        f'<ellipse cx="{cx:.1f}" cy="{top + dy * s:.1f}" rx="{wd / 2 * s:.1f}" '
        f'ry="{6.5 * s:.1f}" fill="{color}" stroke="{edge}" stroke-width="{1.1 * s:.2f}"/>'
        for wd, dy in wds)


def ic_flurry(cx, cy, s=1.0):
    """泷愿成真麦旋风：白杯 + 限定紫环 + 奶油旋。"""
    cw = 44 * s
    top, bot = cy + 2 * s, cy + 26 * s
    o = [f'<path d="M{cx - cw / 2:.1f} {top:.1f} L{cx + cw / 2:.1f} {top:.1f} '
         f'L{cx + cw / 2 - 7 * s:.1f} {bot:.1f} L{cx - cw / 2 + 7 * s:.1f} {bot:.1f} Z" '
         f'fill="{SURFACE}" stroke="#BFB9AE" stroke-width="{1.5 * s:.2f}"/>',
         f'<path d="M{cx - cw / 2 + 1.8 * s:.1f} {top + 7 * s:.1f} L{cx + cw / 2 - 1.8 * s:.1f} '
         f'{top + 7 * s:.1f} L{cx + cw / 2 - 3.6 * s:.1f} {top + 16 * s:.1f} '
         f'L{cx - cw / 2 + 3.6 * s:.1f} {top + 16 * s:.1f} Z" fill="#9B7BC8" opacity="0.85"/>',
         f'<rect x="{cx - cw / 2 - 2.5 * s:.1f}" y="{top - 6.5 * s:.1f}" '
         f'width="{cw + 5 * s:.1f}" height="{7.5 * s:.1f}" rx="{3.4 * s:.1f}" '
         f'fill="#F3EFF9" stroke="#BFB9AE" stroke-width="{1.2 * s:.2f}"/>']
    o.append(cream_tiers(cx, top - 8 * s, s, [(34, 0), (27, -8), (17, -15)]))
    for dx, dy in ((-6, -17), (5, -20), (0, -12)):
        o.append(f'<circle cx="{cx + dx * s:.1f}" cy="{top + dy * s:.1f}" r="{1.5 * s:.1f}" '
                 f'fill="#9B7BC8" opacity="0.8"/>')
    return "".join(o)


def ic_hashbrown(cx, cy, s=1.0):
    """心形薯饼：金色心形 + 脆皮颗粒。"""
    p = (f"M{cx:.1f} {cy + 15 * s:.1f} "
         f"C {cx - 29 * s:.1f} {cy - 2 * s:.1f} {cx - 21 * s:.1f} {cy - 23 * s:.1f} "
         f"{cx:.1f} {cy - 10 * s:.1f} "
         f"C {cx + 21 * s:.1f} {cy - 23 * s:.1f} {cx + 29 * s:.1f} {cy - 2 * s:.1f} "
         f"{cx:.1f} {cy + 15 * s:.1f} Z")
    o = [f'<path d="{p}" fill="#E8B04A" stroke="#C98A12" stroke-width="{1.6 * s:.2f}" '
         f'stroke-linejoin="round"/>']
    for dx, dy in ((-10, -6), (7, -9), (-2, 2), (11, 3), (-13, 5), (2, -3)):
        o.append(f'<circle cx="{cx + dx * s:.1f}" cy="{cy + dy * s:.1f}" r="{1.5 * s:.1f}" '
                 f'fill="#F7D98F" opacity="0.92"/>')
    return "".join(o)


def ic_cone(cx, cy, s=1.0):
    """圆筒冰淇淋：华夫锥 + 双拼奶油。"""
    w, tip, top = 34 * s, cy + 26 * s, cy - 3 * s
    o = [f'<path d="M{cx - w / 2:.1f} {top:.1f} L{cx + w / 2:.1f} {top:.1f} '
         f'L{cx:.1f} {tip:.1f} Z" fill="#E3B168" stroke="#C08A3A" stroke-width="{1.4 * s:.2f}"/>']
    for i in range(1, 4):
        yy = top + (tip - top) * i / 4
        o.append(f'<line x1="{cx - w / 2 * (1 - i / 4):.1f}" y1="{yy:.1f}" '
                 f'x2="{cx + w / 2 * (1 - i / 4):.1f}" y2="{yy:.1f}" stroke="#C08A3A" '
                 f'stroke-width="{0.9 * s:.2f}" opacity="0.6"/>')
    o.append(cream_tiers(cx, top - 4 * s, s, [(30, 0), (20, -9)]))
    return "".join(o)


def phone_lock(x, y, w, h):
    """锁屏手机：大时钟 + 没有新消息。"""
    o = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="20" '
         f'fill="#2C3038" stroke="#1C1F26" stroke-width="2.4"/>',
         f'<rect x="{x + 8:.1f}" y="{y + 10:.1f}" width="{w - 16:.1f}" height="{h - 20:.1f}" '
         f'rx="14" fill="#171A21"/>',
         f'<rect x="{x + w / 2 - 22:.1f}" y="{y + 18:.1f}" width="44" height="7" rx="3.5" '
         f'fill="#0D0F14"/>',
         txt(x + w / 2, y + h * 0.40, "00:07", 44, "#EDEFF5", anchor="middle", weight="700"),
         txt(x + w / 2, y + h * 0.48, "10月14日 周二", F_META, "#98A0B2", anchor="middle")]
    o.append(f'<line x1="{x + 28:.1f}" y1="{y + h * 0.60:.1f}" x2="{x + w - 28:.1f}" '
             f'y2="{y + h * 0.60:.1f}" stroke="#3A3F4C" stroke-width="1.4" '
             f'stroke-dasharray="3 4"/>')
    o.append(txt(x + w / 2, y + h * 0.70, "没有新消息", F_META, "#7C8497", anchor="middle"))
    o.append(f'<path d="M{x + w / 2 - 20:.1f} {y + h * 0.79:.1f} L{x + w / 2:.1f} '
             f'{y + h * 0.83:.1f} L{x + w / 2 + 20:.1f} {y + h * 0.79:.1f}" fill="none" '
             f'stroke="#5A6070" stroke-width="2" stroke-linecap="round"/>')
    return "".join(o)


def phone_app(x, y, w, h):
    """麦麦 APP 商品卡（格内只讲商品，不出价格）。"""
    o = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16" '
         f'fill="{SURFACE}" stroke="{HAIR}" stroke-width="1.6"/>',
         txt(x + 22, y + 42, "麦麦 · 甜品站", 22, THEME, weight="700"),
         dotted(x + 22, x + w - 22, y + 58)]
    o.append(ic_flurry(x + 46, y + 104, 0.95))
    o.append(txt(x + 86, y + 98, "泷愿成真麦旋风", 21, INK, weight="700"))
    o.append(txt(x + 86, y + 124, "——大米风味", F_META, MUTED))
    o.append(dotted(x + 22, x + w - 22, y + 152))
    o.append(txt(x + 22, y + 184, "今日限定 · 愿望成真", F_META, MUTED))
    o.append(txt(x + 22, y + 212, "给你自己点一个吧。", F_LABEL, INK, weight="600"))
    return "".join(o)


# ══════════════════ 四格（内部 478×320）══════════════════
def panel1():
    """01 起 · 今天发生了什么：00:07，锁屏上没有一条新消息。"""
    return "".join([
        phone_lock(274, 50, 180, 236),
        maizai(104, 206, 1.12, "呆", arms="hold", tilt=-1.5),
        bubble(20, 24, 240, ["今天是我生日，", "但没人记得。"], F_TALK,
               tail=("down", 104, 0), lh=30),
        txt(458, 42, "00:07 · 生日当天", F_META, MUTED, anchor="end")])


def panel2():
    """02 承 · 情绪被看见：那就自己，给自己，点一个。"""
    return "".join([
        phone_app(196, 50, 250, 236),
        maizai(96, 214, 1.12, "丧", arms="down"),
        bubble(20, 26, 160, ["那就自己", "给自己", "点一个。"], F_LABEL,
               tail=("down", 96, 0), lh=26),
        txt(458, 42, "00:07", F_META, MUTED, anchor="end")])


def panel3():
    """03 转 · 麦门出场：三样真实在售餐品（画面不出价格）。"""
    o = [desk(288, 20, 458),
         txt(24, 42, "00:09 · 麦门（24h 店）", F_META, MUTED)]
    for cx, fn, names in ((84, ic_flurry, ["泷愿成真麦旋风", "——大米风味"]),
                          (236, ic_hashbrown, ["心形薯饼5块"]),
                          (388, ic_cone, ["圆筒冰淇淋"])):
        o.append(fn(cx, 148, 1.5))
        ly = 236
        for i, nm in enumerate(names):
            o.append(txt(cx, ly, nm, F_LABEL if i == 0 else F_META,
                         INK if i == 0 else MUTED, anchor="middle",
                         weight="700" if i == 0 else "400"))
            ly += 26
    return "".join(o)


def panel4():
    """04 合 · 故事的结尾：没人记得，那我自己记得，愿望照样算数。"""
    return "".join([
        desk(292, 20, 458),
        maizai(132, 212, 1.18, "喜", arms="hold"),
        ic_flurry(244, 166, 1.3),
        candle_fry(244, 118, 1.0),
        bubble(292, 42, 182, ["没人记得，", "那我自己记得。", "愿望照样算数。"], F_LABEL,
               tail=("left", 0, 112), lh=28),
        txt(458, 42, "00:09", F_META, MUTED, anchor="end")])


SVG = T.build_svg(
    title="麦门灵魂小票 · 情绪漫画长卡 003（今天是我生日，但没人记得）",
    desc="1080×1920 长卡：四格漫画为故事主体，餐品只在 03 格作道具出场（格内不含价格）；"
         "价格与券仅出现在「今日情绪配餐」信息区。泷愿成真麦旋风 ¥16.00 / 心形薯饼5块 "
         "¥15.00 / 圆筒冰淇淋 ¥5.00，合计 ¥36.00，均来自麦当劳 MCP 2026-10-14 实时核价"
         "（门店 1400757）。券「中薯条买一送一」用券实证 ¥13.50"
         "（traceId c0ac9d29b406e84e12e1833c47748ea3）。角色「麦仔」为原创设定。",
    panels=[panel1, panel2, panel3, panel4],
    header_args=("2026-10-14 · 仪式型", "003",
                 "今天是我生日，但没人记得",
                 "今日状态：零点过了，祝福还没到。", THEME,
                 candle_fry(T.M + T.IW - 64, T.BANNER_Y + 66, 0.6)),
    meal_args=dict(
        theme=THEME,
        rows=[("泷愿成真麦旋风——大米风味", "¥16.00"),
              ("心形薯饼5块", "¥15.00"),
              ("圆筒冰淇淋", "¥5.00")],
        total="¥36.00",
        reason_lines=["推荐理由：仪式感优先 · 自己给自己许愿",
                      "情绪基调：不催你开心，只陪你过完这一天。"],
        coupon=("中薯条买一送一", "¥13.50", "原 ¥27.00 · 已省 ¥13.50")),
    verdict="生日不会因为没人记得，就不是生日。",
    settle_rows=[("今日消耗", "等了一整天的「生日快乐」"),
                 ("今日找零", "一根插在麦旋风上的薯条蜡烛")],
    seed=20261014)

T.emit("comic-card-03.svg", SVG)
