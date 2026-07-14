"""
fetch_stock.py — Pexels 세로형 이미지 일괄 수집기 (잡학 랭킹 쇼츠용)

[무엇을 하나]
- 이미지 키워드로 Pexels를 검색해 세로형(portrait) 사진만 골라
  assets/weekXX/ 아래에 다운로드한다.

[사전 준비]
1. Pexels API 키 발급: https://www.pexels.com/api/ 에서 무료 발급
   (로그인 후 "Your API Key" 확인. 상업적 사용 가능, 크레딧 표기 권장)
2. 프로젝트 루트에 .env 파일을 만들고 아래 한 줄을 넣는다:
       PEXELS_API_KEY=여기에_발급받은_키
   (.env.example를 복사해서 채우면 된다. .env는 git에 올라가지 않음)
3. 의존성 설치:
       pip install requests python-dotenv

[사용법 — PowerShell]
    # 키워드 1개 이상, --week 는 저장 폴더(assets/weekXX) 지정
    python tools/fetch_stock.py --week 01 --per 3 "human brain" "galaxy stars" "octopus underwater"

    # 대본 이미지 키워드를 그대로 넘기면 편함
    # 결과: assets/week01/human_brain_1.jpg ... 형태로 저장

[옵션]
    --week   저장 폴더 주차 번호 (예: 01) — 필수
    --per    키워드당 다운로드 장수 (기본 3)
    --out    저장 루트 (기본 assets)

[규칙]
- 세로형(portrait)만 저장한다. 쇼츠는 9:16이므로.
- 타인 영상/이미지 재사용 금지. Pexels 스톡(라이선스 확인)만 사용.
- 다운로드한 파일은 git에 올라가지 않는다(.gitignore에서 assets/ 제외).
"""

import argparse
import os
import re
import sys
import time

try:
    import requests
except ImportError:
    sys.exit("requests 가 필요합니다:  pip install requests python-dotenv")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv 없이도 환경변수로 키가 있으면 동작
    pass

PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"


def slugify(text: str) -> str:
    """키워드를 파일명에 쓸 수 있게 정리."""
    s = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower())
    return s.strip("_") or "image"


def fetch_keyword(api_key: str, keyword: str, per: int, out_dir: str) -> int:
    """키워드 하나로 검색 → 세로형만 per장 다운로드. 저장한 장수 반환."""
    headers = {"Authorization": api_key}
    # 넉넉히 받아서 그중 portrait만 고른다.
    params = {"query": keyword, "orientation": "portrait", "per_page": max(per * 2, per)}

    try:
        resp = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params, timeout=20)
    except requests.RequestException as e:
        print(f"  ! 네트워크 오류 ({keyword}): {e}")
        return 0

    if resp.status_code == 401:
        sys.exit("  ! 인증 실패: PEXELS_API_KEY 값을 확인하세요.")
    if resp.status_code != 200:
        print(f"  ! 검색 실패 ({keyword}): HTTP {resp.status_code}")
        return 0

    photos = resp.json().get("photos", [])
    if not photos:
        print(f"  - 결과 없음: {keyword}")
        return 0

    slug = slugify(keyword)
    saved = 0
    for photo in photos:
        if saved >= per:
            break
        # orientation=portrait로 요청했지만 한 번 더 방어적으로 확인
        if photo.get("width", 0) >= photo.get("height", 1):
            continue
        src = photo.get("src", {}).get("portrait") or photo.get("src", {}).get("large")
        if not src:
            continue
        try:
            img = requests.get(src, timeout=30)
            img.raise_for_status()
        except requests.RequestException as e:
            print(f"  ! 다운로드 실패: {e}")
            continue

        path = os.path.join(out_dir, f"{slug}_{saved + 1}.jpg")
        with open(path, "wb") as f:
            f.write(img.content)
        saved += 1
        print(f"  + {path}  (by {photo.get('photographer', 'unknown')}, Pexels)")
        time.sleep(0.3)  # API 예의상 약간의 간격

    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description="Pexels 세로형 이미지 수집기")
    parser.add_argument("keywords", nargs="+", help="검색 키워드 (영어 권장)")
    parser.add_argument("--week", required=True, help="주차 번호 (예: 01)")
    parser.add_argument("--per", type=int, default=3, help="키워드당 다운로드 장수 (기본 3)")
    parser.add_argument("--out", default="assets", help="저장 루트 (기본 assets)")
    args = parser.parse_args()

    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        sys.exit(
            "PEXELS_API_KEY 가 없습니다.\n"
            "  1) https://www.pexels.com/api/ 에서 키를 발급받고\n"
            "  2) .env 파일에  PEXELS_API_KEY=...  를 넣으세요 (.env.example 참고)."
        )

    out_dir = os.path.join(args.out, f"week{args.week}")
    os.makedirs(out_dir, exist_ok=True)
    print(f"저장 폴더: {out_dir}\n")

    total = 0
    for kw in args.keywords:
        print(f"[검색] {kw}")
        total += fetch_keyword(api_key, kw, args.per, out_dir)

    print(f"\n완료: 총 {total}장 저장됨 → {out_dir}")
    print("주의: Pexels 라이선스(상업적 사용 가능)이며, 크레딧 표기를 권장합니다.")


if __name__ == "__main__":
    main()
