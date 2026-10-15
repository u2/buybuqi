# 买不起影业 · BuyBuQi Studio

> **把任何便宜东西，拍成你买不起的样子。**
> 输入一句话「把XXX拍成买不起的样子」→ 输出一条 30 秒左右的伪奢侈品广告大片。

灵感致敬 B 站UP主 **@王左导演** 的「买不起」系列（三蹦子 / 人字拖 / GDSD 塑料凳）。本项目用 **AI 全流程复刻**了这套广告美学，并将其沉淀为一条可复用的自动化流水线。

## 成片效果

| 案例 | 成片 | 结构 |
|---|---|---|
| 三蹦子·复刻版 | `examples/sanbengzi/final_sanbengzi_v3.mp4`（24.4s） | 旷野公路→悬崖望海→侧跟特写→戈壁航拍→SANBENGZI 盾徽卡，旁白逐镜复刻原片台词 |
| 三蹦子·扩展版 | `examples/sanbengzi/final_sanbengzi_v4.mp4`（34.5s） | 标题→旷野公路→蒂芙尼蓝微距→设计蓝图→悬崖望海→金句→航拍→SANBENGZI 盾徽卡 |
| 不锈钢盆 | `examples/pen/final_pen_luxury.mp4`（29.4s） | 「厨房的鼎」→钢卷边微距→主厨抱盆→悬浮金句→和谐远景→GANGPEN 盾徽卡 |

所有画面均为 AI 生成（腾讯混元 HY-Image / HY-Video），不含任何原视频素材。

## 核心公式

```
教程体旁白（一本正经的"拍摄指令"）
× 奢华广告影像（崭新物件 + 史诗自然景 + 单光源极简构图）
× 恶搞大牌反转（拼音盾徽 / 伪洋牌 / 缩写大LOGO）
= 反差喜剧
```

笑点机制 =「这么高级干净的片子里居然是辆三蹦子」——**物件越崭新越好笑**。

## 流水线（七步 SOP）

```
① 解构      WebSearch 拆解文 + yt-dlp 拉原片抽帧（可选）
② 品牌系统   品牌名三条路 / 奢华色名法 / 金句句式 / 标题通感
③ 分镜      Hero→Detail→Feature→Lifestyle→Outro 弧线 × 8 镜头库
④ 关键帧    HY-Image 生成 → 逐张验收 → image-to-image 派生保主体一致
⑤ 视频      HY-Video 图生视频（1080P，多镜头并行）
⑥ 合成      ffmpeg 拼接 + delogo 去水印 + libass 代码排版字幕 + 盾徽卡
⑦ 验收      形制/时长/字幕/水印逐项核对
```

完整方法论（美学铁律、提示词模板、坑册）见 [`skill/SKILL.md`](skill/SKILL.md)。

## 快速使用

字幕生成（JSON → ASS，四档样式：标题/旁白/金句/slogan）：

```bash
python3 skill/scripts/gen_subs.py examples/pen/subs.json -o subs.ass
```

成片合成（片段淡入淡出 + 拼接 + 烧字幕）：

```bash
bash skill/scripts/assemble.sh output.mp4 subs.ass clip1.mp4 clip2.mp4 ...
```

依赖：ffmpeg（含 libass）+ Noto Sans CJK SC 字体 + Python 3。

## 目录结构

```
buybuqi/
├── README.md
├── skill/
│   ├── SKILL.md            # 完整方法论（配方/模板/坑册）
│   └── scripts/
│       ├── assemble.sh     # 片段合成脚本
│       └── gen_subs.py     # 字幕生成器（文字绝不交给AI生图）
├── examples/
│   ├── sanbengzi/          # 三蹦子案例（成片+字幕+关键帧）
│   └── pen/                # 不锈钢盆案例
└── templates/
    └── subs.template.json  # 字幕规格模板
```

## 致谢与声明

- 方法论灵感来自 [@王左导演](https://space.bilibili.com/) 的「买不起」系列，本项目与其无关联，成片均为 AI 生成的原创演绎，仅供学习研究。
- 请勿用本流水线制作冒充真实品牌或误导消费者的内容。

## License

MIT
