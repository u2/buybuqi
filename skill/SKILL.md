---
name: ai-video-remake-hunyuan
description: 用 WorkBuddy 内置腾讯混元 HY-Image（ImageGen）/ HY-Video（VideoGen）复刻热门短视频（B站/抖音梗视频等），专精「如何把XXX拍成买不起的样子」一句话出片。当用户给出视频链接或创意概念，要求"复刻/仿拍/AI 重制/拍成 XX 的样子"时使用。流程：拉原片解构 → 品牌系统设计 → HY-Image 关键帧（先验收再动） → HY-Video 图生视频 → ffmpeg 拼接+代码排版字幕+品牌水印+结尾卡成片。
---

# AI 复刻短视频（HY-Image + HY-Video + ffmpeg）

目标：对梗视频做"同款精神"的 AI 复刻。旗舰案例：王左导演「买不起」系列（B站 BV1CDaw6ZEKg 三蹦子 / BV1K2af6ZEy7 人字拖 / BV1vNhb6nEdf 塑料凳《GDSD》）。**理想交互：用户输入「把XX拍成买不起的样子」→ 直接输出成片**，按下面 SOP 走，中途不问问题（缺细节就做合理假设并注明）。

## 核心公式

**教程体旁白（一本正经的"拍摄指令"）× 奢华广告影像（崭新物件+史诗自然景）× 恶搞大牌反转 = 反差喜剧**

笑点机制 =「这么高级干净的片子里居然是辆三蹦子」——**物件越破越不好笑，越新越好笑**。

## 美学铁律（v2 翻车教训，写提示词前必读）

- **物件必须崭新锃亮**：无锈、无泥、无划痕。提示词末尾显式加 `brand-new, spotless, no dirt no rust no mud`。禁用 weathered/rusty/mud/vintage-worn 类词。
- **背景必须是干净的自然大片景**：旷野笔直公路、海边悬崖、戈壁雅丹日落、草原、干净摄影棚渐变背景。**忌**城中村、湿地柏油路、杂物入镜。
- **构图极简**：物件在画面里常常只是小点，天空/景观占大半。
- **一盏有方向的光**（奢侈品广告法则）：单一主光源（金色暮光/柔和棚光），深而柔的阴影过渡；忌电商平光、多光源、无理由光晕。
- **一个色彩世界**：整片锁定一个主色调（如"锃亮蒂芙尼蓝 × 金色暮色"），每个镜头都住在这个色世界里。
- **人物表演「淡漠厌世感」**：一切欲望满足后的倦怠贵族脸，绝不嬉笑（原片原文：模特要保持"一切欲望满足后的淡漠与厌世感"）。

## 第一步：解构（有原片链接时两层都要拿到）

1. **文案层**：WebFetch 视频页 + WebSearch 搜"标题 + 分镜/文案/台词/旁白"（王左导演系列有大量拆解文章，比抽帧更快拿到完整台词）。
2. **视觉层（强烈建议）**：yt-dlp 拉原片抽帧，确认字幕字体/位置/配色和结尾结构：
   ```bash
   VENV=/home/u2/.workbuddy/binaries/python/envs/default
   FF=$(ls $VENV/lib/python3.13/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v* | head -1)
   # 单格式分别下载（--download-sections 会触发其内置 ffmpeg 段错误，别用）
   $VENV/bin/python -m yt_dlp --ffmpeg-location "$FF" -f 30064 --no-playlist -o ref_v.mp4 <URL>   # 720p
   $VENV/bin/python -m yt_dlp --ffmpeg-location "$FF" -f 30280 --no-playlist -o ref_a.m4a <URL>   # 音频
   $FF -y -i ref_v.mp4 -i ref_a.m4a -c copy ref.mp4
   # 均匀抽帧（每 4~8s 一帧）目检；若当前模型不支持读图，改用 WebSearch 拆解文 + 元数据兜底
   ```
   格式 ID：30032≈480p，30064=720p H.264，30080=1080p，30280=音频。游客最高 720p/普通1080p。

## 第二步：品牌系统设计（出片前先定，全片贯彻）

**1. 品牌名三条路**（选一）：
- 拼音盾徽流：物件名全拼大写 → **SANBENGZI**（保时捷盾徽恶搞）
- 伪洋牌流：谐音嫁接奢侈品牌 → **TERMES 托马仕**（爱马仕恶搞）/ 梅赛德斯·三 Benz
- 缩写大LOGO流：品类雅称拼音缩写 → **GDSD**（广东省凳，雷霆大字结尾）

**2. 奢华色名法**（塑料凳集核心模块）：给物件的廉价原色起高定色名——国际流「卡地亚红」「蒂芙尼蓝」「夏帕瑞丽粉」，国风流「绛艳红」「天水碧」「闲云卿粉」。蓝三蹦子→蒂芙尼蓝；红塑料凳→卡地亚红。字幕点破即可，画面配合色彩微距。

**3. 标题通感替代**（开场第一个梗）：人字拖→「广东省鞋」；塑料凳→「广东省凳」。把俗名换成更高雅的品类称谓。

**4. 金句库**（两大句式，插播用）：
- 「不是……而是……」：不是被看见，而是无法被忽略 / 不是消费，而是收藏
- 「真正的……从来不……」：真正的经典，从不追赶经典 / 真正从容的人，从不急着依靠
- 谐音成语改造：心如脱缰 →「心 如 脱 马　自 成 其 势」

**5. 教学模块按题材混搭**（系列三集真正差异——文案统一教程体，教的内容不同）：
- **运镜教学**（三蹦子）：「找一条离你家十万八千里的路」「一定要望向远方」「不能有目的地」「方向盘必须摸」「就是——永远不抵达」
- **品牌教学**（人字拖）：「打出品牌名」「或者干脆创始人姓马」
- **工艺教学**（塑料凳）：「千万不要着急拍全貌」「越不能让大家认出来」+ 设计蓝图 + 色名 + 「功能不能说是功能」
- 混配建议：运镜 2~3 句 + 工艺/品牌 2 句 + 悬念收尾 1 句

## 第三步：分镜（奢侈品广告弧线 × 系列镜头库）

**弧线**（ComfyUI 产品广告工作流方法论）：Hero 揭晓 → Detail 细节 → Feature 卖点梗 → Lifestyle 生活/贵族场景 → Outro 大远景收势。5 镜起，每镜 4~6s，一句旁白一镜。

**镜头库（三集实测汇总，按需挑 5~6 个）**：
- 英雄镜头：低角度 + 金色光线 + 干净反光地面
- 细节微距：材质怼脸拍（漆面/水珠/纹理），手表级打光——**「千万不要着急拍全貌」**
- 框式构图：透过物件孔洞/框架拍天空（塑料凳腿洞看晚霞）——「越不能让大家认出来」
- 设计蓝图：手绘线稿+尺寸标注俯拍——「百年工艺的传承故事」
- 色彩微距：纯色漆面/塑料面光泽横扫——配奢华色名
- 产品融入贵族场景：三蹦子方向盘 / 人字拖踩马镫（缺啥配置拍啥）
- 天空空镜 / 鼻孔仰拍 / 悬浮产品+光斑
- 人与自然和谐远景：人物背影走向地平线
- 产品家族照：多色产品排列如时装系列（红蓝粉三凳）

**关键帧工作流（validate before you scale，奢侈品广告铁律）**：先全部静帧生成 → 逐张验收（物件形制错了立即重生成）→ **挑最完美一张做 image-to-image 参考图派生其他镜头**保证主体一致 → 静帧全过才进视频。

## 第四步：HY-Image 关键帧

参数：`size:"1280x720"`、`quality:"high"`、`revise:false`、`output_dir` 到项目目录。~5-10 积分/张。

模板（英文更稳，形制具体）：
```
Cinematic wide shot of a brand-new spotless glossy <颜色> <物件英文名+形制> in <干净自然景>,
golden-hour lighting, single motivated light source, minimalist epic composition,
the object small in the vast landscape, luxury car commercial aesthetic,
photorealistic, 8k, no dirt no rust no mud, no text
```

**反AI感要点**（融合广告设计专家）：画面里**绝不出现任何文字**（AI 汉字必错，字幕一律 libass 代码排版）；材质要有真实反光与细微痕迹；避免强制对称居中（结尾卡除外）；光只保留一个方向。

**logo/盾徽生成**（英文字母混元较稳，黑底白线稿）：
```
Minimalist luxury brand crest emblem, heraldic shield outline in thin white line art on
pure black background. Inside the shield: a simple line drawing of <物件英文>. Across the
top band, the word "<拼音大写>" in clean capital letters. Flat vector, centered, no other text.
```

**去"AI生成"水印**（结尾卡必须）：`crop=1280:630:0:0,scale=1920:946,pad=1920:1080:0:67`。

**中央品牌水印**（贯穿全片，colorkey 黑底转透明）：
```bash
$FF -i merged.mp4 -i logo.png -filter_complex \
 "[1:v]colorkey=0x000000:0.1:0.1,format=rgba,colorchannelmixer=aa=0.9,scale=420:-1[wm];\
  [0:v][wm]overlay=(W-w)/2:(H-h)/3" ...
```

## 第五步：HY-Video 图生视频

**图生视频**（主体一致性远好于文生视频）：`image`=关键帧路径、`prompt` 只写运镜不重复画面、`resolution:"1080P"`、`enable_audio` 按需。~50-100 积分/条，1-3 分钟，**多镜头同消息并行调用**。

运镜词库：slow push-in / slow orbit / lateral tracking / aerial pull-back & rise / gentle tilt-up / rack focus。修饰：smooth stable camera, no fast motion, epic serene mood。

**高频坑**：
- DeferExecuteTool 调 ImageGen/VideoGen 可能**静默失败**——每次生成后 `ls` 核对文件数，缺了重发。VideoGen 重试会产生多余片段，按文件名时间戳挑自己那批。
- 输出通常 1920x1080/24fps/~5.04s/h264+aac，但**先 `ffmpeg -i` 逐条核对**再拼。

## 第六步：合成（ffmpeg + 代码排版字幕）

**字幕铁律**：文字绝不交给图像模型，一律 libass 代码排版。字体 `Noto Sans CJK SC` 白色无描边无底框，四档样式已固化在 `scripts/gen_subs.py`：
- Title 开场大标题：Bold 76px 居中屏高45%，字与字加空格
- Narr 教程旁白：Regular 48px 底部居中，一次一句 ≥2.2s
- Quote 大字金句：Bold 68px 字间距拉开，居中屏高42%
- Slogan 结尾：Bold 44px + fsp10 字间距，定位 logo 下方

```bash
python3 scripts/gen_subs.py subs.json -o subs.ass
```

**结尾卡通用做法**：`-loop 1 -t 4.2` 静帧 + fade 0.8s + `anullsrc` 静音轨，先 concat 再统一烧字幕。

**成片脚本**：`scripts/assemble.sh <输出.mp4> <subs.ass> <clip1.mp4> ...`（自动淡入淡出/统一 1080p24/concat/烧字幕）。

**去"AI生成"水印（画面镜头，已实测）**：混元生成的片段自带角标水印（右下"AI生成 WORKBUDDY"或左上小标），淡入淡出阶段加 delogo 双角抹除：
```bash
-vf "delogo=x=1695:y=990:w=220:h=85,delogo=x=5:y=5:w=170:h=60,fade=...,format=yuv420p"
```
结尾盾徽卡因 logo 居中在下半区，用裁切法（crop 去底部 12.5% 再 pad 补黑），不用 delogo。

**环境坑**：ffmpeg 用隔离 venv 的 imageio-ffmpeg 静态二进制（含 libass）；中间产物放输出同目录 work/；`set -e` 下 `ffmpeg -i` 探测须 `|| true`（assemble.sh 已内置）；字体确认 `fc-list | grep -i "NotoSansCJK"`。

## 第六步半：声音设计（三声部混音，缺了就没有"广告片味"）

原片拆解结论（对 ref 音轨 3s 粒度 volumedetect 扫描实测）：
- **解说峰值 ≈ -16~-18dB，BGM 底 ≈ -25~-27dB，两者相差约 10dB**；片尾 1s 内淡出归零
- 生成片段自带的自然声/环境声**全部丢弃**（`-map 0:v` 重新配轨），原片画面下没有环境音

### 声部规格

| 声部 | 音色（edge-tts） | 语速/音高 | 内容 | 目标响度 |
|---|---|---|---|---|
| 解说 | `zh-CN-YunyangNeural`（云扬，新闻男声，葛优式平铺直叙） | rate -6%~-12%，pitch -8Hz | "如何拍"的教学台词（对应底部 Narr 字幕） | mean ≈ **-15dB（全片最大声）** |
| 广告语 | `zh-CN-YunjianNeural`（云健，沉稳广告男声） | rate +0%，pitch -5~-6Hz | 金句/意境句/结尾 slogan（对应 Quote/Slogan 字幕） | mean ≈ **-21dB（比解说小 6dB）** |
| BGM | HY-Video 生成（提示词：luxury commercial background music, soft piano + ambient strings, no vocals no percussion）→ 抽音轨循环 | — | 全片铺垫 | mean ≈ **-31dB（几乎不可闻）**，lowpass 6kHz |

**TTS 工具**：隔离 venv `pip install edge-tts`，免凭证直连；注意 rate 必须带符号（`+0%` 合法、`0%` 报错）。

### 台词-声部分配原则
- 教程指令句（"千万不要着急拍全貌/找一个厨师"）→ 解说
- 意境句与品牌金句（"让金属自己说话/不是一只盆而是一件器"）→ 广告语（更慢更沉）
- 结尾 slogan 单独一条，压着盾徽卡起点开始

### 混音配比（ffmpeg 单命令实现）
1. **层次铁律（v1 翻车教训）**：解说 -15 / 广告语 -21 / BGM -31，三个声部各差 6dB、10dB——差距必须拉大，差 2dB 人耳分不出主次
2. 先测每条 VO 的 mean_volume，换算 gain 对准上面三个目标值（例：mean -26.4dB 的解说加 11.4dB）
2. BGM：`-stream_loop` 循环 → `atrim` 到片长 → `lowpass=f=6000` → `volume` 补到 -27dB → 首尾 fade
3. 各 VO 用 `adelay=ms|ms` 排时间轴（对齐字幕 start，句间 ≥0.3s，时长超窗就提速重生成而不是硬叠）
4. `amix=inputs=N:normalize=0` + `alimiter=limit=0.95` → `-t <片长>`
5. 合成：`-map 0:v -map 1:a -c:v copy`（画面无重编码）

### 时间轴排布技巧
- 先按字幕稿列 VO 清单（文本/声部/字幕窗口），TTS 后测实际时长，**总 VO 时长必须 ≤ 窗口总长**，超了统一提速（rate 从 -25% 逐步提到 +0%）
- 金句卡在屏上停留时间短于语音时，让语音拖到卡后面说完（声音可以晚于卡片，不能早于）

## 第七步：验收清单

- [ ] 有原片时：字幕样式/教学模块/结尾卡形态确认过（抽帧或拆解文）
- [ ] 品牌系统三件套齐：品牌名 + 色名 + 金句
- [ ] 关键帧数量与分镜一致，物件形制全对（ls 核对 + 逐张验收）
- [ ] 每条片段时长/分辨率/音轨核对过
- [ ] logo 卡水印已裁除、品牌名拼写正确
- [ ] 成片抽 5+ 帧目检字幕渲染（模型不支持读图时用时长+流信息校验并向用户说明）
- [ ] 全片一个色彩世界、一盏主光、无 AI 文字
- [ ] 声音三声部齐：解说/广告语/BGM 分层清晰（BGM 比人声低 ~10dB），生成片段原环境声已全部丢弃
- [ ] 交付：成片 mp4 + 关键帧 + subs.ass，present_files 汇总

## 案例档案

**案例一：三蹦子（BV1CDaw6ZEKg，2:16 原片 / 复刻 v3-v4）**

| 段 | 镜头 | 旁白 |
|---|---|---|
| 标题 | 旷野笔直公路金色日落，蓝三蹦子驶向远方 | 「如 何 把 三 蹦 子 拍 成 买 不 起 的 样 子」 |
| 1 | 同上 | 第一步，找一条离你家十万八千里的路 |
| 1.5 | 车漆微距（v4 新增，色名模块） | 颜色要起一个高定的名字——蒂芙尼蓝 |
| 1.6 | 设计蓝图（v4 新增，工艺模块） | 再编一段，百年工艺的传承故事 |
| 2 | 海边悬崖，革夹克男望海（淡漠厌世感） | 然后再找一个男人 / 一定要望向远方，不能有目的地 |
| 3 | 公路侧跟踪 | 不是被看见　而是无法被忽略（金句插播） |
| 4 | 航拍：戈壁雅丹，三蹦子小如尘埃 | 就是——永远不抵达 |
| 卡 | SANBENGZI 盾徽 | 全 新 一 代 · 重 新 出 发 |

**案例二：人字拖（BV1K2af6ZEy7，2:02，品牌教学+TERMES 水印+大远景 logo 卡）**
标题「广东省鞋」；旁白「然后你需要一个人」「打出品牌名」「创始人姓马」；金句「心如脱马 自成其势」；结尾大远景+居中 TERMES logo。

**案例三：塑料凳《GDSD》（BV1vNhb6nEdf，2:28，工艺教学+色名+大LOGO）**
标题「如何拍一支地道的奢侈品大片」，开场人物坐小红凳于橙色渐变棚景；「千万不要着急拍全貌」（红漆微距）→「越不能让大家认出来」（凳腿洞框式构图看晚霞）→ 设计蓝图+尺寸 → 色名「夏帕瑞丽粉/卡地亚红/天水碧」→ 产品家族照（红蓝粉三凳）→ 模特淡漠厌世特写「哇好漂亮的凳子」→ 金句「真正的经典 从不追赶经典」→ 仰拍提凳「而是一个关于存在主义的问题」→ 骑行途中凳子悬浮慢镜「熟练使用」→ 结尾雷霆大 LOGO「GDSD」。

## 外部方法论来源（已融合）

- ComfyUI 产品广告工作流：风格常量锁定（一色板/一盏灯/一环境/一材质母题）+ Hero→Detail→Feature→Lifestyle→Outro 弧线
- GPT-Image-2-Seedance2-Workflow（github.com/hzt045858）：分镜网格→逐帧动画，时间戳提示词
- muapi 珠宝广告技能：先静帧验收再动图（validate before you scale）
- Balenciaga x Chess 案例：艺术指导→情绪板→十构图书→验证→多比例→动画的完整漏斗
- ad-design-director 反AI感清单：单光源、反无意义装饰、文字代码化、色彩有出处
