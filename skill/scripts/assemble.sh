#!/bin/bash
# assemble.sh — 拼接视频片段并烧入 ASS 字幕（配合 HY-Image/HY-Video 复刻工作流）
# 用法: assemble.sh <输出.mp4> <subs.ass> <clip1.mp4> [clip2.mp4 ...]
# 依赖: imageio-ffmpeg 静态 ffmpeg（含 libass）；中文字体 Noto Serif CJK SC
set -euo pipefail

OUT="$1"; ASS="$2"; shift 2
FF=$(ls /home/u2/.workbuddy/binaries/python/envs/default/lib/python3.13/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v* | head -1)
# 注意：/tmp 常是小容量 tmpfs，工作目录放在输出文件同目录下
W="$(dirname "$(realpath "$OUT")")/.assemble_work_$$"
mkdir -p "$W"
trap 'rm -rf "$W"' EXIT
FADE=0.35; TAIL=0.6

dur() { # 秒（ffmpeg 仅探测时退出码为 1，需吞掉）
  ($FF -i "$1" 2>&1 || true) | grep -oP 'Duration: \K[0-9:.]+' | awk -F: '{print $1*3600+$2*60+$3}'
}

i=1; n=$#
for c in "$@"; do
  D=$(dur "$c")
  FO=$(awk -v d="$D" -v f="$FADE" -v t="$TAIL" -v i="$i" -v n="$n" 'BEGIN{print (i==n)? d-f-t : d-f}')
  $FF -y -i "$c" \
    -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1,fps=24,fade=t=in:st=0:d=$FADE,fade=t=out:st=${FO}:d=$FADE,format=yuv420p" \
    -af "aresample=44100,afade=t=in:st=0:d=$FADE,afade=t=out:st=${FO}:d=$FADE" \
    -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 128k "$W/seg$i.mp4" -loglevel error
  echo "file 'seg$i.mp4'" >> "$W/list.txt"
  i=$((i+1))
done

$FF -y -f concat -safe 0 -i "$W/list.txt" -c copy "$W/merged.mp4" -loglevel error
$FF -y -i "$W/merged.mp4" -vf "ass=$(realpath "$ASS")" -c:v libx264 -preset medium -crf 18 -c:a copy "$OUT" -loglevel error
echo "OK: $OUT ($($FF -i "$OUT" 2>&1 | grep -oP 'Duration: \K[0-9:.]+'))"
