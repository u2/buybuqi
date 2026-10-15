#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_subs.py — 「买不起」系列字幕生成器（文字绝不交给图像模型，代码排版铁律）

用法:
  python3 gen_subs.py subs.json -o subs.ass

subs.json 格式（全部字段可选，按需给）:
{
  "title":    {"text": "如 何 把 三 蹦 子 拍 成 买 不 起 的 样 子", "start": 0.3, "end": 3.7},
  "events": [
    {"start": 3.9, "end": 7.7, "text": "第一步，找一条离你家十万八千里的路"},
    {"start": 20.5, "end": 23.5, "text": "不 是 被 看 见　而 是 无 法 被 忽 略", "style": "quote"}
  ],
  "slogan":   {"text": "全 新 一 代 · 重 新 出 发", "start": 30.7, "end": 34.2, "y": 930}
}

样式三档（与原片逐帧逆向一致，1080p）:
  title  开场大标题   Bold 76px 居中屏高45%  白色无描边
  narr   教程旁白     Regular 48px 底部居中(MarginV 110)
  quote  大字金句     Bold 68px 居中屏高42% 字间距拉开
  slogan 结尾slogan   Bold 44px 字间距fsp10 定位盾徽下方
"""
import json, argparse, sys

def ts(sec: float) -> str:
    h = int(sec // 3600); m = int(sec % 3600 // 60); s = sec % 60
    return f"{h}:{m:02d}:{int(s):02d}.{int(round((s - int(s)) * 100)):02d}"

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Noto Sans CJK SC,76,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,10,10,0,1
Style: Narr,Noto Sans CJK SC,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,10,10,110,1
Style: Quote,Noto Sans CJK SC,68,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,8,0,1,0,0,5,10,10,0,1
Style: Slogan,Noto Sans CJK SC,44,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,10,0,1,0,0,5,10,10,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("-o", "--out", default="subs.ass")
    args = ap.parse_args()
    spec = json.load(open(args.spec, encoding="utf-8"))
    lines = [HEADER]
    t = spec.get("title")
    if t:
        lines.append(f"Dialogue: 0,{ts(t['start'])},{ts(t['end'])},Title,,0,0,0,,{t['text']}")
    for e in spec.get("events", []):
        # ASS 样式名大小写敏感：narr/quote/title/slogan 一律转为首字母大写
        style = e.get("style", "narr").capitalize()
        text = e["text"] if style != "quote" else e["text"]
        lines.append(f"Dialogue: 0,{ts(e['start'])},{ts(e['end'])},{style},,0,0,0,,{text}")
    s = spec.get("slogan")
    if s:
        y = s.get("y", 930)
        text = s["text"].replace("{", "").replace("}", "")
        lines.append(f"Dialogue: 0,{ts(s['start'])},{ts(s['end'])},Slogan,,0,0,0,,{{\\pos(960,{y})}}{text}")
    open(args.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"OK: {args.out} ({len(lines)-1} events)")

if __name__ == "__main__":
    main()
