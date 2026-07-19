#!/usr/bin/env python3
"""ebook.md → 판매용 PDF 빌드 스크립트.

사용법:
    pip install weasyprint markdown
    (한글 폰트 필요: 예. apt-get install fonts-nanum)
    python3 build_pdf.py

출력: 하루1시간_쇼츠공장.pdf (같은 폴더)
"""
import markdown
from pathlib import Path
from weasyprint import HTML

HERE = Path(__file__).parent
SRC = HERE / "ebook.md"
OUT = HERE / "하루1시간_쇼츠공장.pdf"

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


def main():
    md_text = SRC.read_text(encoding="utf-8")
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    html = f'<html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    HTML(string=html).write_pdf(OUT)
    print(f"OK: {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
