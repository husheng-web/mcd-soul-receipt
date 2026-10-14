# generator/ · 视觉生成器

本目录是 `assets/` 里所有视觉资产的**可复现源代码**。整套视觉不使用任何 AI 画图——
每一根线条、每一个角色表情、每一处版式，都是这里的 Python 代码参数化画出来的内联 SVG。

## 运行

```bash
# 零第三方依赖，任何 Python ≥3.8 可跑
python generator/gen_card_01.py    # 输出到 ../assets/comic-card-01.svg
```

PNG 由浏览器渲染 SVG 得到（Chrome headless）：

```bash
chrome --headless --disable-gpu \
  --screenshot=assets/comic-card-01@1x.png \
  --window-size=1080,1920 \
  file://<仓库路径>/assets/comic-card-01.svg
# 加 --force-device-scale-factor=2 即得 2x 高清版（2160×3840）
```

## 三层结构

| 文件 | 职责 | 改它意味着 |
|---|---|---|
| `gen_comic_card.py` | **基础构件库**：文字排版、角色「麦仔」、场景道具、餐品图标、气泡、结算条锯齿、条码 | 改角色长相或新增道具 |
| `card_theme.py` | **版式套件（锁定）**：卡头金横幅 / 四格 2×2 栅格 / 今日情绪配餐 / TODAY'S MESSAGE / 情绪结算条 / 卡脚，全部按 `references/visual-design-rules.md` 的锁定 token 实现 | 等于改设计系统，须同步改规范文档 |
| `gen_card_NN.py` | **单卡故事**：只写四格画面与文案，配餐数据来自 MCP 实时核价 | 新增一张卡 = 新增一个文件 |

## 关键约定（与 SKILL.md 一致）

- **四格内不出价格**——价格只出现在「今日情绪配餐」信息区
- **配餐与券必须真实**——`calculate-price` 核价 + `query-store-coupons` 实证；无券不硬凑
- **交付前必过密度门禁**：`python tools/density_check.py assets/comic-card-NN@1x.png`
  （内容纵向跨度 ≥80%、任何空白带 ≤15%）
- **角色一致性**：`maizai()` 的身体比例恒定，表情只换眼睛和嘴巴——跨格一致的全部秘密

## 卡片清单

| 文件 | 情绪 | 主题色 | 输入原型 |
|---|---|---|---|
| `gen_card_01.py` | 导师改稿 · 发泄型 | 憋屈蓝紫 `#5A6BA8` | 「被导师改崩溃了」 |
| `gen_card_02.py` | 不想上班 · 补电型 | 低电量蓝 `#4C6E9E` | 「今天真的不想上班！」 |
| `gen_card_03.py` | 生日 · 仪式型 | 安慰玫瑰 `#B0748E` | 「今天是我生日，但没人记得」 |
| `gen_card_04.py` | 想家 · gentle_comfort | 燕麦棕 `#9B7B4F` | 「我妈问我吃了没，我说吃了」 |
