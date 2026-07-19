#!/usr/bin/env python3
"""ebook.md → 판매용 PDF + 홍보용 미리보기 PDF 빌드 스크립트.

사용법:
    pip install weasyprint markdown
    (한글 폰트 필요: 예. apt-get install fonts-nanum)
    python3 build_pdf.py

출력 (같은 폴더):
    하루1시간_쇼츠공장.pdf          — 판매용 완성본 (표지 포함)
    하루1시간_쇼츠공장_미리보기.pdf  — 무료 배포용 (표지+목차+1장+구매 안내)
"""
import markdown
from pathlib import Path
from weasyprint import HTML

HERE = Path(__file__).parent
SRC = HERE / "ebook.md"
OUT = HERE / "하루1시간_쇼츠공장.pdf"
OUT_SAMPLE = HERE / "하루1시간_쇼츠공장_미리보기.pdf"

COVER_HTML = """
<div id="cover">
  <div class="cover-top">FACELESS SHORTS SYSTEM</div>
  <div class="cover-title">하루 1시간<br>쇼츠 공장</div>
  <div class="cover-sub">얼굴 없이, 주 6시간으로 운영하는<br>유튜브 쇼츠 채널 시스템</div>
  <div class="cover-points">
    대본 프롬프트 · 편당 60분 공정표 · 30일 캘린더 · 업로드 체크리스트
  </div>
  {badge}
</div>
"""

COVER_CSS = """
#cover {
    page: cover;
    height: 253mm;
    background: #10151f;
    color: #fff;
    text-align: center;
    padding-top: 55mm;
}
@page cover { margin: 0; @bottom-center { content: none; } }
.cover-top { font-size: 10pt; letter-spacing: 4pt; color: #7a8699; margin-bottom: 18mm; }
.cover-title { font-family: 'NanumSquare', 'NanumBarunGothic', sans-serif;
    font-size: 42pt; font-weight: bold; line-height: 1.3; }
.cover-sub { font-size: 13pt; color: #c3cbd8; margin-top: 14mm; line-height: 1.7; }
.cover-points { font-size: 10pt; color: #8b96a8; margin-top: 30mm; }
.cover-badge { display: inline-block; margin-top: 12mm; padding: 3mm 8mm;
    border: 1pt solid #5b8def; border-radius: 3mm; color: #9db9f5; font-size: 11pt; }
"""

SAMPLE_CTA_HTML = """
<div id="sample-end">
  <h2 style="page-break-before: always;">여기까지가 무료 미리보기입니다</h2>
  <p>전체판(16페이지)에는 다음이 이어집니다.</p>
  <ul>
    <li>2장. 채널 컨셉 정하기 — '잡학 랭킹' 포맷</li>
    <li>3장. 45초 대본 공식 — AI에게 시키는 법 (프롬프트 전문 포함)</li>
    <li>4~6장. Vrew 편집 20분 워크플로 / 저작권 / 업로드 체크리스트</li>
    <li>7~9장. 주 6시간 운영 시스템, 지표 읽는 법, 수익화의 현실</li>
    <li>부록. 프롬프트 전문 · 체크리스트 · 예시 대본 · 지표 기록 양식</li>
  </ul>
  <blockquote><p><strong>구매 안내</strong>: 판매 페이지 링크는 배포 시 이 자리에 삽입 — build_pdf.py의 PURCHASE_URL 수정</p></blockquote>
</div>
"""

# 배포 전 판매 링크로 교체할 것 (크몽 상품 URL 또는 랜딩페이지 URL)
PURCHASE_URL = ""

CSS = """
@page {
    size: A4;
    margin: 22mm 20mm;
    @bottom-center { content: counter(page); font-size: 9pt; color: #999; }
}
body {
    font-family: 'NanumBarunGothic', 'NanumGothic', sans-serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #222;
}
h1 {
    font-size: 22pt; line-height: 1.35; color: #111;
    margin: 0 0 8pt 0; page-break-before: always;
}
h1:first-of-type { page-break-before: avoid; margin-top: 90pt; text-align: center; }
h1:first-of-type + p strong { display: block; text-align: center; font-size: 13pt; color: #555; }
h2 { font-size: 15pt; color: #1a1a1a; margin: 20pt 0 6pt 0; page-break-before: always; }
h3 { font-size: 12pt; color: #333; margin: 16pt 0 4pt 0; }
h2 + h3, h1 + h2 { page-break-before: avoid; }
p { margin: 6pt 0; }
blockquote {
    margin: 10pt 0; padding: 8pt 14pt; background: #f5f7fa;
    border-left: 3pt solid #4a6fa5; color: #333;
}
blockquote p { margin: 0; }
table { border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 9.5pt; }
th, td { border: 0.5pt solid #ccc; padding: 5pt 8pt; text-align: left; }
th { background: #eef1f5; }
code, pre {
    font-family: 'NanumGothicCoding', monospace; font-size: 9pt;
    background: #f4f4f4;
}
pre { padding: 10pt; border-radius: 4pt; white-space: pre-wrap; line-height: 1.5; }
ul, ol { margin: 6pt 0; padding-left: 18pt; }
li { margin: 3pt 0; }
hr { border: none; border-top: 0.5pt solid #ddd; margin: 16pt 0; }
strong { color: #111; }
"""


def render(body_html: str, out_path: Path, badge: str = "") -> None:
    cover = COVER_HTML.format(badge=badge)
    html = (
        f'<html lang="ko"><head><meta charset="utf-8">'
        f"<style>{CSS}{COVER_CSS}</style></head>"
        f"<body>{cover}{body_html}</body></html>"
    )
    HTML(string=html).write_pdf(out_path)
    print(f"OK: {out_path.name} ({out_path.stat().st_size / 1024:.0f} KB)")


def main():
    md_text = SRC.read_text(encoding="utf-8")
    # 원고 맨 앞의 제목·부제(속표지 역할)는 표지 페이지로 대체되므로
    # 첫 번째 "## " 헤딩 전까지 제거
    idx = md_text.find("\n## ")
    if md_text.startswith("# ") and idx != -1:
        md_text = md_text[idx + 1 :]
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])

    # 완성본
    render(body, OUT)

    # 미리보기: 1장 끝(2장 시작 전)까지 + 구매 안내
    marker = "<h2>2장"
    cut = body.find(marker)
    sample_body = body[:cut] if cut != -1 else body
    cta = SAMPLE_CTA_HTML
    if PURCHASE_URL:
        cta = cta.replace(
            "판매 페이지 링크는 배포 시 이 자리에 삽입 — build_pdf.py의 PURCHASE_URL 수정",
            f'전체판 구매: <a href="{PURCHASE_URL}">{PURCHASE_URL}</a>',
        )
    render(
        sample_body + cta,
        OUT_SAMPLE,
        badge='<div class="cover-badge">무료 미리보기</div>',
    )


if __name__ == "__main__":
    main()
