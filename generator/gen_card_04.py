# -*- coding: utf-8 -*-
"""
麦门灵魂小票 · 情绪漫画长卡 004 ——「想家型」
场景：我妈打电话问我吃了没 / 语义意图「思念·想家」（tone = gentle_comfort）
数据：2026-10-14 15:36 麦当劳 MCP 实时返回（门店 1400757，到店自取）
      · query-meals       → 麦香鸡 1450 / 月下相思扭扭薯 521901 / 纯牛奶(盒装) 3755
      · calculate-price   → 合计 ¥43.00（traceId 09a627bd6568a467bc6bcbf319c1544e，discount 0）
      · query-store-coupons + calculate-price 用券实证 → 中薯条买一送一 ¥13.50
        （原 ¥27.00 · 已省 ¥13.50，traceId c8e877313e62bc1499c1275bbf87aaf5）
规范依据：references/visual-design-rules.md（锁定 token）+ references/comic-spec.md
版式实现：card_theme.py（可复用构件，本文件只负责四格与文案）
所有图形均为内联 SVG 参数化绘制，不调用任何 AI 画图。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_comic_card import txt, maizai, bubble, desk, est_w          # noqa: E402
import card_theme as T                                                 # noqa: E402

THEME = "#9B7B4F"        # 情绪色·想家型 → 燕麦棕（锁定表取值）
FRY, FRY_ED = "#F5C244", "#C98A12"
CREAM, CREAM_ED = "#F6EBD6", "#DCC9A6"


# ══════════════════ 本卡新增道具（参数化 SVG）══════════════════
def moon(cx, cy, r):
    """窗外月亮：奶黄满月 + 淡晕 + 两点月斑。"""
    return "".join([
        f'<circle cx="{cx}" cy="{cy}" r="{r * 1.55:.1f}" fill="#FBEFCB" opacity="0.5"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="#F5D989" stroke="#D9BC74" '
        f'stroke-width="1.6"/>',
        f'<circle cx="{cx - r * 0.28:.1f}" cy="{cy - r * 0.22:.1f}" r="{r * 0.20:.1f}" '
        f'fill="#E8C877"/>',
        f'<circle cx="{cx + r * 0.24:.1f}" cy="{cy + r * 0.30:.1f}" r="{r * 0.13:.1f}" '
        f'fill="#E8C877"/>'])


def phone_call(x, y, w, h):
    """通话中的手机：联系人 + 通话时长 + 挂断圆钮。"""
    cx = x + w / 2
    o = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="20" '
         f'fill="#2C3038" stroke="#1C1F26" stroke-width="2.4"/>',
         f'<rect x="{x + 8:.1f}" y="{y + 10:.1f}" width="{w - 16:.1f}" height="{h - 20:.1f}" '
         f'rx="14" fill="#171A21"/>',
         f'<rect x="{cx - 22:.1f}" y="{y + 18:.1f}" width="44" height="7" rx="3.5" fill="#0D0F14"/>',
         # 头像
         f'<circle cx="{cx:.1f}" cy="{y + h * 0.28:.1f}" r="26" fill="#3A4150"/>',
         f'<circle cx="{cx:.1f}" cy="{y + h * 0.255:.1f}" r="9" fill="#7C8497"/>',
         f'<path d="M{cx - 15:.1f} {y + h * 0.325:.1f} q15 -14 30 0 Z" fill="#7C8497"/>',
         txt(cx, y + h * 0.47, "妈妈", 22, "#EDEFF5", anchor="middle", weight="700"),
         txt(cx, y + h * 0.58, "通话中 02:14", T.F_META, "#98A0B2", anchor="middle"),
         # 挂断钮
         f'<circle cx="{cx:.1f}" cy="{y + h * 0.82:.1f}" r="21" fill="#E0574F"/>',
         f'<path d="M{cx - 9:.1f} {y + h * 0.82 - 5:.1f} q9 -7 18 0 q-9 7 -18 0 Z" '
         f'fill="#FFFFFF"/>']
    return "".join(o)


def phone_off(x, y, w, h):
    """挂断后的手机：屏幕暗掉，只剩一层反光。"""
    o = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="20" '
         f'fill="#2C3038" stroke="#1C1F26" stroke-width="2.4"/>',
         f'<rect x="{x + 8:.1f}" y="{y + 10:.1f}" width="{w - 16:.1f}" height="{h - 20:.1f}" '
         f'rx="14" fill="#101319"/>',
         f'<path d="M{x + 24:.1f} {y + h - 34:.1f} L{x + w - 60:.1f} {y + 22:.1f} '
         f'L{x + w - 40:.1f} {y + 22:.1f} L{x + 44:.1f} {y + h - 34:.1f} Z" '
         f'fill="#FFFFFF" opacity="0.05"/>']
    return "".join(o)


def ic_chickenburg(cx, cy, s=1.0):
    """麦香鸡：上下包 + 金黄鸡排（画面的形态须与真实商品对得上）。"""
    w = 52 * s
    o = [f'<path d="M{cx - w / 2:.1f} {cy - 8 * s:.1f} Q {cx:.1f} {cy - 30 * s:.1f} '
         f'{cx + w / 2:.1f} {cy - 8 * s:.1f} Z" fill="#E9AE5E" stroke="#C98A12" '
         f'stroke-width="{1.4 * s:.2f}"/>',
         f'<rect x="{cx - w / 2 + 2 * s:.1f}" y="{cy - 8 * s:.1f}" width="{w - 4 * s:.1f}" '
         f'height="{11 * s:.1f}" rx="{5 * s:.1f}" fill="#EFC272" stroke="#C98A12" '
         f'stroke-width="{1.3 * s:.2f}"/>',
         f'<path d="M{cx - w / 2 + 1 * s:.1f} {cy + 3 * s:.1f} '
         f'Q {cx - w / 2 - 2 * s:.1f} {cy + 20 * s:.1f} {cx:.1f} {cy + 20 * s:.1f} '
         f'Q {cx + w / 2 + 2 * s:.1f} {cy + 20 * s:.1f} {cx + w / 2 - 1 * s:.1f} {cy + 3 * s:.1f} Z" '
         f'fill="#E9AE5E" stroke="#C98A12" stroke-width="{1.4 * s:.2f}"/>']
    return "".join(o)


def ic_twist(cx, cy, s=1.0):
    """月下相思扭扭薯：波纹薯条 + 联名色纸盒（波浪形态 = 商品真实形态）。"""
    bw, bt, bb = 54 * s, cy + 2 * s, cy + 32 * s
    o = [f'<path d="M{cx - bw / 2:.1f} {bt:.1f} L{cx + bw / 2:.1f} {bt:.1f} '
         f'L{cx + bw / 2 - 7 * s:.1f} {bb:.1f} L{cx - bw / 2 + 7 * s:.1f} {bb:.1f} Z" '
         f'fill="{T.SURFACE}" stroke="#BFB9AE" stroke-width="{1.5 * s:.2f}"/>',
         f'<path d="M{cx - bw / 2 + 1.6 * s:.1f} {bt + 8 * s:.1f} L{cx + bw / 2 - 1.6 * s:.1f} '
         f'{bt + 8 * s:.1f} L{cx + bw / 2 - 3.4 * s:.1f} {bt + 19 * s:.1f} '
         f'L{cx - bw / 2 + 3.4 * s:.1f} {bt + 19 * s:.1f} Z" fill="{THEME}" opacity="0.88"/>']
    for i, dx in enumerate((-16, -5.5, 5.5, 16)):
        x0 = cx + dx * s
        top = bt - (24 if i % 2 == 0 else 20) * s
        d = (f"M{x0:.1f} {bt - 2 * s:.1f} "
             f"L{x0 + 4 * s:.1f} {bt - 8 * s:.1f} L{x0 - 1 * s:.1f} {bt - 13 * s:.1f} "
             f"L{x0 + 4 * s:.1f} {bt - 18 * s:.1f} L{x0 - 1 * s:.1f} {top + 1 * s:.1f}")
        o.append(f'<path d="{d}" fill="none" stroke="{FRY_ED}" stroke-width="{6.2 * s:.2f}" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(f'<path d="{d}" fill="none" stroke="{FRY}" stroke-width="{4 * s:.2f}" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(o)


def ic_milk(cx, cy, s=1.0):
    """纯牛奶（盒装）：白色屋顶纸盒 + 联名色标签。"""
    w, h = 44 * s, 52 * s
    top = cy - h / 2 + 12 * s
    o = [f'<path d="M{cx - w / 2:.1f} {top:.1f} L{cx:.1f} {cy - h / 2:.1f} '
         f'L{cx + w / 2:.1f} {top:.1f} Z" fill="#F1EDE4" stroke="#C6BCA8" '
         f'stroke-width="{1.4 * s:.2f}" stroke-linejoin="round"/>',
         f'<rect x="{cx - w / 2:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h - 12 * s:.1f}" '
         f'rx="{2.5 * s:.1f}" fill="{T.SURFACE}" stroke="#C6BCA8" stroke-width="{1.4 * s:.2f}"/>',
         f'<rect x="{cx - w / 2 + 3 * s:.1f}" y="{cy + 2 * s:.1f}" width="{w - 6 * s:.1f}" '
         f'height="{15 * s:.1f}" rx="{2 * s:.1f}" fill="{THEME}" opacity="0.85"/>',
         f'<circle cx="{cx:.1f}" cy="{cy - 8 * s:.1f}" r="{7 * s:.1f}" fill="#EDE4D3" '
         f'stroke="#C6BCA8" stroke-width="{1.1 * s:.2f}"/>']
    return "".join(o)


# ══════════════════ 四格（内部 478×320）══════════════════
def panel1():
    """01 今天发生了什么：19:40 妈妈来电，报了个平安。"""
    return "".join([
        phone_call(272, 46, 182, 240),
        maizai(102, 206, 1.12, "呆", arms="hold", tilt=-1.5),
        bubble(18, 24, 214, ["吃了吃了，", "你别忙了。"], T.F_TALK, tail=("down", 102, 0), lh=30),
        txt(458, 42, "19:40 · 妈妈来电", T.F_META, T.MUTED, anchor="end")])


def panel2():
    """02 情绪被看见：挂了电话，屏幕暗了，才发现自己还没吃。"""
    return "".join([
        desk(288, 20, 458),
        phone_off(272, 52, 182, 232),
        maizai(102, 208, 1.14, "丧", arms="down"),
        bubble(18, 26, 176, ["其实", "我还没吃。"], T.F_LABEL, tail=("down", 102, 0), lh=26),
        txt(458, 42, "19:42", T.F_META, T.MUTED, anchor="end")])


def panel3():
    """03 麦门出场：三样真实在售餐品（画面不出价格）。"""
    o = [desk(288, 20, 458),
         txt(24, 42, "20:05 · 麦门（24h 店）", T.F_META, T.MUTED)]
    for cx, fn, names in [(84, ic_chickenburg, ["麦香鸡"]),
                          (236, ic_twist, ["月下相思扭扭薯"]),
                          (388, ic_milk, ["纯牛奶", "（盒装）"])]:
        o.append(fn(cx, 144, 1.5))
        ly = 232
        for i, nm in enumerate(names):
            o.append(txt(cx, ly, nm, T.F_LABEL if i == 0 else T.F_META,
                         T.INK if i == 0 else T.MUTED, anchor="middle",
                         weight="700" if i == 0 else "400"))
            ly += 26
    return "".join(o)


def panel4():
    """04 故事的结尾：一个人吃，但月亮和家里是同一轮（不强行开心）。"""
    return "".join([
        desk(292, 20, 458),
        moon(60, 84, 24),
        maizai(122, 212, 1.18, "喜", arms="hold"),
        ic_twist(246, 168, 1.28),
        bubble(282, 46, 186, ["想家就说想家，", "不用先说吃了。"], T.F_LABEL,
               tail=("left", 0, 112), lh=28),
        txt(458, 42, "20:20", T.F_META, T.MUTED, anchor="end")])


SVG = T.build_svg(
    title="麦门灵魂小票 · 情绪漫画长卡 004（我妈问我吃了没，我说吃了）",
    desc="1080×1920 长卡：四格漫画为故事主体，餐品只在 03 格作道具出场（格内不含价格）；"
         "价格与券仅出现在「今日情绪配餐」信息区。麦香鸡 / 月下相思扭扭薯 / 纯牛奶(盒装) "
         "与券「中薯条买一送一（¥13.50）」均来自麦当劳 MCP 2026-10-14 实时返回（门店 1400757），"
         "核价 ¥43.00。角色「麦仔」为原创设定。",
    panels=[panel1, panel2, panel3, panel4],
    header_args=("2026-10-14 · 想家型", "004",
                 "我妈问我吃了没，我说吃了",
                 "其实还没吃。挂了电话，才发现是真的想家。", THEME),
    meal_args=dict(
        theme=THEME,
        rows=[("麦香鸡", "¥17.00"),
              ("月下相思扭扭薯", "¥15.50"),
              ("纯牛奶（盒装）", "¥10.50")],
        total="¥43.00",
        reason_lines=["推荐理由：热牛奶 + 名字带「相思」的扭扭薯",
                      "情绪基调：想家是正经情绪，不用理由。"],
        coupon=("中薯条买一送一", "¥13.50", "原 ¥27.00 · 已省 ¥13.50")),
    verdict="家不会跑，但牛奶会凉。",
    settle_rows=[("今日消耗", "跟妈妈说的那句「吃了」"),
                 ("今日找零", "一包叫「月下相思」的扭扭薯")],
    seed=20261014)

T.emit("comic-card-04.svg", SVG)
