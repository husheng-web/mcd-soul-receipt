# -*- coding: utf-8 -*-
"""
麦门灵魂小票 · 情绪漫画长卡 001 ——「导师改稿」（发泄型）
=====================================================
场景：被导师改崩溃 / 语义意图「发泄型」（tone = vent）
数据：2026-10-14 15:55 麦当劳 MCP 实时返回（门店 1400757，到店自取）
      · calculate-price → 合计 ¥46.50（traceId a4a00e466e46f5769001935afd289211，discount 0）
      · 麦辣鸡腿汉堡 1440 ¥23.00 / 那么大鸡排（椒盐风味）521156 ¥14.00 / 可乐 9900008751 ¥9.50
      · query-store-coupons → 门店仅「中薯条买一送一」「王牌小食拼」两张，与本配餐无关
        → 按规范「无券不硬凑」，本卡不放券条
规范依据：references/visual-design-rules.md（锁定 token）+ references/comic-spec.md
版式实现：card_theme.py（可复用构件，本文件只负责四格与文案）
所有图形均为内联 SVG 参数化绘制，不调用任何 AI 画图。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_comic_card import (txt, est_w, maizai, bubble, paper, pile, monitor,   # noqa: E402
                            lamp, desk, red_mark, ic_burger, ic_chicken, ic_cola,
                            F_MONO, DEFS)
import card_theme as T                                                          # noqa: E402

THEME = "#5A6BA8"        # 情绪色·发泄型 → 憋屈蓝紫（锁定表取值）


def meta(s):
    """格内右上角时间戳。"""
    return txt(458, 42, s, T.F_META, T.MUTED, anchor="end")


# ══════════════════ 四格（内部 478×320）══════════════════
def panel1():
    """01 起 · 今天发生了什么：23:47 宿舍，第 8 版改到崩溃。"""
    return "".join([
        desk(292, 20, 458),
        lamp(34, 92),
        monitor(236, 122, 182, 122),
        red_mark(250, 146, 46),
        red_mark(258, 162, 32),
        pile(48, 290, 36, 54, 3),
        paper(100, 238, 30, 40),
        maizai(134, 206, 1.12, "丧", arms="down", tilt=-1.5),
        bubble(18, 28, 218, ["被导师改崩溃了。"], T.F_TALK,
               tail=("down", 106, 0), lh=30),
        meta("23:47 · 宿舍"),
    ])


def panel2():
    """02 承 · 情绪被看见：稿子铺满一桌，红批从第一页改到最后一页。"""
    o = []
    base = 296
    for px, ph in ((30, 68), (104, 100), (182, 134), (262, 106), (334, 76)):
        o.append(pile(px, base, 46, ph, 3))
    for rx, ry, rw in ((196, 120, 40), (206, 138, 30), (52, 152, 34),
                       (286, 92, 30), (122, 110, 26)):
        o.append(red_mark(rx, ry, rw))
    o.append(f'<g transform="rotate(-7 118 88)">{paper(102, 66, 32, 44)}</g>')
    o.append(f'<g transform="rotate(8 306 80)">{paper(290, 58, 32, 44)}</g>')
    o.append(maizai(56, 220, 0.98, "惊", arms="up"))
    o.append(bubble(158, 30, 232, ["导师批注：", "再改改（指全文）"], T.F_TALK,
                    tail=("left", 0, 74), lh=30))
    o.append(meta("第 8 版"))
    return "".join(o)


def panel3():
    """03 转 · 麦门出场：三样真实在售餐品（画面不出价格）。"""
    o = [desk(292, 20, 458),
         txt(24, 42, "00:12 · 麦门（24h 店）", T.F_META, T.MUTED)]
    for cx, fn, names in ((96, ic_burger, ["麦辣鸡腿汉堡"]),
                          (230, ic_chicken, ["那么大鸡排", "（椒盐风味）"]),
                          (364, ic_cola, ["可乐"])):
        o.append(fn(cx, 142, 1.55))
        ly = 236
        for i, nm in enumerate(names):
            o.append(txt(cx, ly, nm, T.F_LABEL if i == 0 else T.F_META,
                         T.INK if i == 0 else T.MUTED, anchor="middle",
                         weight="700" if i == 0 else "400"))
            ly += 26
    return "".join(o)


def panel4():
    """04 合 · 故事的结尾：先咬两口出气，改稿的事明天再说（不强行开心）。"""
    return "".join([
        desk(292, 20, 458),
        maizai(130, 208, 1.14, "无语", arms="hold"),
        f'<g transform="rotate(-13 202 178)">{ic_burger(204, 180, 1.0)}</g>',
        bubble(244, 42, 214, ["今天先咬两口出气，", "改稿的事，明天再说。"], T.F_LABEL,
               tail=("left", 0, 120), lh=28),
        meta("00:26"),
    ])


SVG = T.build_svg(
    title="麦门灵魂小票 · 情绪漫画长卡 001（被导师改崩溃了）",
    desc="1080×1920 长卡：四格漫画为故事主体，餐品只在 03 格作道具出场（格内不含价格）；"
         "价格仅出现在「今日情绪配餐」信息区。麦辣鸡腿汉堡 ¥23.00 / 那么大鸡排（椒盐风味）"
         "¥14.00 / 可乐 ¥9.50，合计 ¥46.50，均来自麦当劳 MCP 2026-10-14 15:55 实时核价"
         "（门店 1400757，traceId a4a00e466e46f5769001935afd289211）。门店券与本配餐无关，"
         "按「无券不硬凑」规则不放券条。角色「麦仔」为原创设定。",
    panels=[panel1, panel2, panel3, panel4],
    header_args=("2026-10-14 · 发泄型", "001",
                 "被导师改崩溃了",
                 "确诊「导师性精神内耗」· 第 8 版仍在改。", THEME),
    meal_args=dict(
        theme=THEME,
        rows=[("麦辣鸡腿汉堡", "¥23.00"),
              ("那么大鸡排（椒盐风味）", "¥14.00"),
              ("可乐", "¥9.50")],
        total="¥46.50",
        reason_lines=["推荐理由：大块咬感 + 重口 + 冰爽，咬下去有回声",
                      "情绪基调：不劝你看开，先让你咬两口。"],
        coupon=None),
    verdict="稿子改不完，但今晚可以先咬两口。",
    settle_rows=[("今日消耗", "第 8 版的「好的老师」"),
                 ("今日找零", "咬下去的那两秒安静")],
    seed=20261014)

T.emit("comic-card-01.svg", SVG)
