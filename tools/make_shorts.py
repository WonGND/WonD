#!/usr/bin/env python3
"""쇼츠 조립 시뮬레이터 — 전자책 파이프라인 검증용.

Vrew(GUI) 대신 서버 환경에서 전자책 4장의 공정을 재현한다:
  대본(문장 리스트) → TTS → 문장별 자막 + 카드 비주얼 + 줌 모션 → 1080x1920 MP4

사용법: python3 tools/make_shorts.py
입력:  스크립트 내 SCENES (문장·비주얼 매핑)
출력:  output/test/microwave_test.mp4
의존:  ffmpeg, espeak-ng(또는 문장별 wav 준비), Pillow, 나눔 폰트, NotoColorEmoji
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "output" / "test"
W, H = 1080, 1920
FPS = 30
FONT_SUB = "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf"
FONT_LABEL = "/usr/share/fonts/truetype/nanum/NanumSquareR.ttf"
FONT_EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# 장면: (이모지, 라벨, 배경 밝기 오프셋, [문장들])
SCENES = [
    ("🍳", "당신의 부엌", 0, [
        "당신 부엌의 그 기계, 원래는 무기였습니다.",
    ]),
    ("📡", "1945 · 레이더 연구소", 8, [
        "매일 쓰는 전자레인지 얘기입니다.",
        "그런데 이걸 만든 사람은 요리사가 아니었어요.",
        "레이더를 만들던 군수회사 기술자였습니다.",
    ]),
    ("🍫", "이상한 발견", 16, [
        "1945년, 기술자 퍼시 스펜서는",
        "레이더 부품 앞에서 일하다 이상한 걸 느낍니다.",
        "주머니 속 초콜릿이 녹아 있던 겁니다.",
    ]),
    ("🍿", "실험", 24, [
        "그는 지나치지 않고 실험을 시작했어요.",
        "옥수수를 갖다 대자, 팝콘이 튀었습니다.",
        "달걀은 그대로 폭발했죠.",
    ]),
    ("⚡", "증명의 순간", 32, [
        "전파로 음식을 데운다는 게 증명된 순간입니다.",
    ]),
    ("⚙️", "최초의 전자레인지", 24, [
        "2년 뒤 나온 최초의 전자레인지는",
        "키가 사람보다 크고, 무게는 300킬로가 넘었습니다.",
    ]),
    ("💵", "그리고, 보상", 12, [
        "그런데 정작 스펜서가 회사에서 받은 발명 보상금은,",
        "단돈 2달러였습니다.",
    ]),
    ("🔔", "", 0, [
        "당신이 오늘 데운 한 끼는, 그 2달러에서 시작됐습니다.",
        "팔로우하면 내일 더 놀라운 이야기를 들려드립니다.",
    ]),
]


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def make_card(emoji: str, label: str, tint: int, path: Path):
    """네이비 그라데이션 + 대형 이모지 + 라벨의 카드 비주얼 (1080x1920)."""
    img = Image.new("RGB", (W, H))
    top = (16 + tint // 2, 21 + tint // 2, 31 + tint)
    bottom = (10, 13, 20)
    for y in range(H):
        t = y / H
        img.paste(
            tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)),
            (0, y, W, y + 1),
        )
    draw = ImageDraw.Draw(img)
    # NotoColorEmoji는 109px 비트맵 → 109로 그린 뒤 확대
    tile = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(tile).text(
        (70, 70), emoji, font=ImageFont.truetype(FONT_EMOJI, 109),
        embedded_color=True, anchor="mm",
    )
    big = tile.resize((640, 640), Image.LANCZOS)
    img.paste(big, ((W - 640) // 2, 430), big)
    if label:
        draw.text(
            (W // 2, 1210), label,
            font=ImageFont.truetype(FONT_LABEL, 44),
            fill=(139, 150, 168), anchor="mm",
        )
    # 상단 채널 워터마크 자리 (6장 오리지널리티 신호)
    draw.text(
        (W // 2, 150), "잡학 공장",
        font=ImageFont.truetype(FONT_LABEL, 40),
        fill=(90, 100, 118), anchor="mm",
    )
    img.save(path)


def wrap(text: str, limit: int = 15) -> str:
    """자막 2줄 래핑 — 공백 기준, limit자 초과 시 줄바꿈."""
    if len(text) <= limit:
        return text
    words, lines, cur = text.split(" "), [], ""
    for w_ in words:
        cand = (cur + " " + w_).strip()
        if len(cand) > limit and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = cand
    lines.append(cur)
    return "\n".join(lines[:3])


def tts(text: str, path: Path):
    run(["espeak-ng", "-v", "ko", "-s", "160", "-w", str(path), text])


def dur_of(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="shorts_"))
    seg_files, total, zoom_dir = [], 0.0, 1

    for si, (emoji, label, tint, lines) in enumerate(SCENES):
        card = work / f"card{si}.png"
        make_card(emoji, label, tint, card)
        for li, line in enumerate(lines):
            wav = work / f"s{si}_{li}.wav"
            tts(line, wav)
            d = dur_of(wav) + 0.25  # 문장 간 호흡
            sub = work / f"s{si}_{li}.txt"
            sub.write_text(wrap(line), encoding="utf-8")
            seg = work / f"seg{si}_{li}.mp4"
            frames = int(d * FPS)
            # 줌 모션(6장 오리지널리티 원칙) — 장면마다 줌인/줌아웃 교차
            if zoom_dir > 0:
                zexpr = f"1+0.10*on/{frames}"
            else:
                zexpr = f"1.10-0.10*on/{frames}"
            vf = (
                f"scale=2160:-1,zoompan=z='{zexpr}':d={frames}"
                f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
                f"drawtext=fontfile={FONT_SUB}:textfile={sub}:fontsize=58"
                f":fontcolor=white:borderw=5:bordercolor=black"
                f":x=(w-text_w)/2:y=h-460:line_spacing=18"
            )
            run([
                "ffmpeg", "-y", "-loop", "1", "-t", f"{d:.3f}", "-i", str(card),
                "-i", str(wav), "-vf", vf,
                "-af", "apad", "-shortest",
                "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-r", str(FPS), str(seg),
            ])
            seg_files.append(seg)
            total += d
        zoom_dir *= -1

    concat = work / "list.txt"
    concat.write_text("".join(f"file '{s}'\n" for s in seg_files), encoding="utf-8")
    final = OUT_DIR / "microwave_test.mp4"
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-movflags", "+faststart", str(final),
    ])
    print(f"OK: {final} ({final.stat().st_size/1024/1024:.1f} MB, {total:.1f}s, {len(seg_files)} segments)")


if __name__ == "__main__":
    main()
