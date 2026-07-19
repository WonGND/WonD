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
    검증된 대본 프롬프트 · 소재 아이디어 50선 · 편당 60분 공정표 · 30일 캘린더 · 트러블슈팅 가이드
  </div>
  {badge}
</div>
"""

COVER_CSS = """
#cover {
    page: cover;
    height: 245mm;
    background: #10151f;
    color: #fff;
    text-align: center;
    padding-top: 52mm;
}
@page cover {
    margin: 0;
    @bottom-left { content: none; }
    @bottom-right { content: none; }
}
.cover-top { font-size: 10pt; letter-spacing: 4pt; color: #7a8699; margin-bottom: 16mm; }
.cover-title { font-family: 'NanumSquare', 'NanumBarunGothic', sans-serif;
    font-size: 44pt; font-weight: bold; line-height: 1.3; letter-spacing: -1pt; }
.cover-title::after {
    content: ""; display: block; width: 18mm;
    border-top: 1.4mm solid #3b6fd4; margin: 11mm auto 0;
}
.cover-sub { font-size: 13pt; color: #c3cbd8; margin-top: 11mm; line-height: 1.75; }
.cover-points { font-size: 9.5pt; color: #8b96a8; margin-top: 28mm; letter-spacing: 0.5pt; }
.cover-badge { display: inline-block; margin-top: 12mm; padding: 3mm 8mm;
    border: 1pt solid #5b8def; border-radius: 3mm; color: #9db9f5; font-size: 11pt; }
"""

SAMPLE_CTA_HTML = """
<div id="sample-end">
  <h2 style="page-break-before: always;">여기까지가 무료 미리보기입니다</h2>
  <p>전체판에는 다음이 이어집니다.</p>
  <ul>
    <li>2장. 채널 컨셉 — '잡학 랭킹' 포맷 + 니치 변형 12선</li>
    <li>3장. 45초 대본 공식 + 후킹 패턴 12 (프롬프트 전문 포함)</li>
    <li>4~5장. Vrew 편집 20분 워크플로 / 이미지·BGM·저작권</li>
    <li>6장. '재사용된 콘텐츠' 판정 피하기 — 수익화 심사 최대 리스크</li>
    <li>7~9장. 업로드 체크리스트, 주 6시간 운영 시스템, 지표 읽는 법</li>
    <li>10~11장. 트러블슈팅 가이드, 수익화의 현실</li>
    <li>부록. 프롬프트 전문 · 체크리스트 · 예시 대본 3편 · 소재 아이디어 50선 · 채널 셋업 체크리스트 · 지표 양식</li>
  </ul>
  <blockquote><p><strong>구매 안내</strong>: 판매 페이지 링크는 배포 시 이 자리에 삽입 — build_pdf.py의 PURCHASE_URL 수정</p></blockquote>
</div>
"""

# 배포 전 판매 링크로 교체할 것 (크몽 상품 URL 또는 랜딩페이지 URL)
PURCHASE_URL = ""

ACCENT = "#3b6fd4"
NAVY = "#10151f"
INK = "#1f2530"

CSS = f"""
@page {{
    size: A4;
    margin: 24mm 20mm 26mm;
    @bottom-left {{
        content: "하루 1시간 쇼츠 공장";
        font-family: 'NanumBarunGothic', sans-serif;
        font-size: 8pt; color: #a6aebb; letter-spacing: 1pt;
    }}
    @bottom-right {{
        content: counter(page);
        font-family: 'NanumSquare', sans-serif;
        font-size: 9pt; font-weight: bold; color: {ACCENT};
    }}
}}
body {{
    font-family: 'NanumBarunGothic', 'NanumGothic', sans-serif;
    font-size: 10pt;
    line-height: 1.85;
    color: {INK};
}}

/* 장 제목 — 챕터 오프너 */
h2 {{
    font-family: 'NanumSquare', 'NanumBarunGothic', sans-serif;
    font-size: 19pt; font-weight: bold; color: {NAVY};
    line-height: 1.4; letter-spacing: -0.5pt;
    page-break-before: always;
    border-top: 2.5pt solid {NAVY};
    margin: 0 0 18pt; padding-top: 14pt;
}}

/* 절 제목 — 포인트 바 */
h3 {{
    font-family: 'NanumSquare', 'NanumBarunGothic', sans-serif;
    font-size: 12.5pt; font-weight: bold; color: {NAVY};
    border-left: 3pt solid {ACCENT}; padding-left: 9pt;
    margin: 20pt 0 8pt; page-break-after: avoid;
}}
h2 + h3 {{ margin-top: 4pt; }}

p {{ margin: 7pt 0; }}
strong {{ color: {NAVY}; }}

/* 콜아웃 카드 */
blockquote {{
    margin: 12pt 0; padding: 11pt 16px;
    background: #eef3fb; border-left: 3pt solid {ACCENT};
    border-radius: 0 4pt 4pt 0;
    color: #2a3446; page-break-inside: avoid;
}}
blockquote p {{ margin: 3pt 0; }}

/* 표 — 가로선만, 지브라 */
table {{
    border-collapse: collapse; width: 100%;
    margin: 12pt 0; font-size: 9pt; line-height: 1.6;
    page-break-inside: avoid;
}}
th {{
    background: {NAVY}; color: #ffffff; font-weight: bold;
    padding: 6pt 9pt; text-align: left; border: none;
}}
td {{
    padding: 5.5pt 9pt; text-align: left;
    border: none; border-bottom: 0.6pt solid #dde3ec;
}}
tr:nth-child(even) td {{ background: #f5f7fb; }}

/* 프롬프트 블록 — 다크 카드 */
code {{
    font-family: 'NanumGothicCoding', monospace; font-size: 9pt;
    background: #eef1f6; padding: 0.5pt 3pt; border-radius: 2pt;
}}
pre {{
    background: {NAVY}; color: #dce5f5;
    padding: 13pt 15pt; border-radius: 5pt;
    white-space: pre-wrap; line-height: 1.65;
    page-break-inside: avoid; margin: 12pt 0;
}}
pre code {{ background: none; padding: 0; color: inherit; }}

ul, ol {{ margin: 7pt 0; padding-left: 19pt; }}
li {{ margin: 4pt 0; }}
li::marker {{ color: {ACCENT}; font-weight: bold; }}

hr {{ border: none; border-top: 0.6pt solid #dfe4ec; margin: 18pt 0; }}

/* 목차 페이지 */
.toc-title + ol {{ line-height: 2.2; font-size: 10.5pt; padding-left: 24pt; }}
.toc-title + ol li {{ margin: 2pt 0; }}
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
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])
    # 목차 페이지 전용 스타일을 걸기 위한 클래스 부여
    body = body.replace("<h2>목차</h2>", '<h2 class="toc-title">목차</h2>')

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
