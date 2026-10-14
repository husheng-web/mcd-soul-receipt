#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""density_check.py — 卡片成图密度门禁（零依赖，只用标准库）。

来源：设计系统 `references/visual-design-rules.md` 第五节「密度门禁」。
参考实现思路与视觉设计套件 `card_audit.py` 一致（逐行横向边缘密度分析），
但改为纯标准库实现（自带 PNG 解码），不依赖 numpy / Pillow，任何机器可跑。

判据：
  - 内容纵向跨度 ≥ 80% 画高（SPAN_MIN）
  - 任何单块无理由空白 ≤ 15% 画高（DEAD_BAND_MAX）
  - 4 带自检（各 25%）：底部带（75-100%）必须有实质内容；相邻两带不得同时为空
  - 整体填充带数 ≥ 75%

用法：
  python density_check.py assets/comic-card-03.png
  python density_check.py assets/*.png --json
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
import zlib
from pathlib import Path

SPAN_MIN = 0.80
DEAD_BAND_MAX = 0.15
EDGE_TOL = 12          # 相邻像素灰度差 > 此值记为一个边缘
ROW_EDGE_FRAC = 0.006  # 一行中 >0.6% 像素是边缘 → 该行有内容


# ─────────────────────────── 极简 PNG 解码 ───────────────────────────
def _unfilter(raw: bytes, w: int, h: int, bpp: int, stride: int) -> bytearray:
    out = bytearray(h * stride)
    pos = 0
    prev = bytearray(stride)
    for y in range(h):
        ft = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        if ft == 1:      # Sub
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif ft == 2:    # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ft == 3:    # Average
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xFF
        elif ft == 4:    # Paeth
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return out


def gray_rows(path: Path):
    """解码 PNG → 每行灰度列表（仅支持 8/16bit、非隔行；Chrome 截图都符合）。"""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("不是 PNG 文件")
    pos, idat, ihdr = 8, [], None
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", body)
        elif typ == b"IDAT":
            idat.append(body)
        elif typ == b"IEND":
            break
        pos += 12 + ln
    w, h, depth, ctype, _, _, interlace = ihdr
    if interlace:
        raise ValueError("不支持隔行 PNG")
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    if depth == 16:
        ch *= 2
    bpp = ch
    stride = w * ch
    raw = zlib.decompress(b"".join(idat))
    px = _unfilter(raw, w, h, bpp, stride)
    step = 2 if depth == 16 else 1
    rows = []
    for y in range(h):
        base = y * stride
        g = [0] * w
        for x in range(w):
            o = base + x * ch
            if ch >= 3:
                r, gg, b = px[o], px[o + step], px[o + 2 * step]
            else:
                r = gg = b = px[o]
            g[x] = (r * 299 + gg * 587 + b * 114) // 1000
        rows.append(g)
    return w, h, rows


# ─────────────────────────── 密度分析 ───────────────────────────
def analyze(path: Path) -> dict:
    w, h, rows = gray_rows(path)
    flags, fracs = [], []
    for g in rows:
        n = sum(1 for i in range(w - 1) if abs(g[i + 1] - g[i]) > EDGE_TOL)
        f = n / max(1, w - 1)
        fracs.append(f)
        flags.append(f > ROW_EDGE_FRAC)

    content = [i for i, v in enumerate(flags) if v]
    if not content:
        return {"file": path.name, "verdict": "FAIL", "reason": "整图无内容"}

    top, bot = content[0], content[-1]
    span = (bot - top + 1) / h

    # 最大连续空白带
    dead, cur, best = 0, 0, 0
    for v in flags[top:bot + 1]:
        cur = cur + 1 if not v else 0
        best = max(best, cur)
    dead_r = best / h

    # 4 带
    bands = []
    for k in range(4):
        a, b2 = int(h * k / 4), int(h * (k + 1) / 4)
        filled = sum(flags[a:b2]) / max(1, b2 - a)
        bands.append(round(filled, 4))

    issues = []
    if span < SPAN_MIN:
        issues.append(f"纵向跨度 {span:.0%} < {SPAN_MIN:.0%}")
    if dead_r > DEAD_BAND_MAX:
        issues.append(f"最大空白带 {dead_r:.0%} > {DEAD_BAND_MAX:.0%}")
    if bands[3] < 0.05:
        issues.append(f"底部带近空（填充 {bands[3]:.1%}）")
    for k in range(3):
        if bands[k] < 0.02 and bands[k + 1] < 0.02:
            issues.append(f"第 {k + 1}/{k + 2} 带同时为空")
    if sum(1 for b in bands if b > 0.02) < 3:
        issues.append("有内容的带 < 3/4")

    return {
        "file": path.name,
        "size": f"{w}×{h}",
        "content_span": round(span, 4),
        "max_dead_band": round(dead_r, 4),
        "bands_25pct": bands,
        "verdict": "PASS" if not issues else "FAIL",
        "issues": issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="卡片成图密度门禁")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    results, bad = [], 0
    for f in a.files:
        try:
            r = analyze(Path(f))
        except Exception as e:  # noqa: BLE001
            r = {"file": Path(f).name, "verdict": "ERROR", "reason": str(e)}
        results.append(r)
        if r["verdict"] != "PASS":
            bad += 1
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            if r["verdict"] == "ERROR":
                print(f"[ERROR] {r['file']} — {r['reason']}")
                continue
            mark = "PASS" if r["verdict"] == "PASS" else "FAIL"
            print(f"[{mark}] {r['file']}  {r['size']}  "
                  f"跨度 {r['content_span']:.0%}  最大空白带 {r['max_dead_band']:.0%}  "
                  f"四带 {[f'{b:.0%}' for b in r['bands_25pct']]}")
            for i in r["issues"]:
                print(f"        · {i}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
