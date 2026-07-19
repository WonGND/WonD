# PROGRESS — 잡학 랭킹 쇼츠 팩토리 작업 로그

> 형식: 날짜 / 작업 / 결과 / 다음 할 일

---

## 2026-07-14

### STEP 0. Git 저장소 생성
- **작업**: 저장소 초기화, .gitignore 작성, 첫 커밋
- **결과**: 완료. 실행 환경이 원격 Linux 컨테이너(Claude Code)이고 GitHub 접근이
  `WonGND/WonD` 저장소로 지정되어 있어, 별도 `shorts-factory` 저장소를 새로 만드는 대신
  비어 있던 `WonD` 저장소 루트에 프로젝트를 구성함 (브랜치: `claude/shorts-factory-setup-9xu3po`).
  gh CLI는 이 환경에 없으나 remote(origin)가 이미 연결되어 있어 불필요.
  .gitignore에 output/, assets/, *.mp4, *.mp3, .env 제외 처리.
- **다음 할 일**: 프로젝트 폴더 구조 생성

### STEP 1. 프로젝트 구조 생성
- **작업**: docs/, prompts/, scripts_content/week01/, tools/, templates/, output/ 생성
- **결과**: 완료. PROGRESS.md(본 파일), 프롬프트 템플릿 2종 뼈대 생성.
  output/은 git 추적 제외(.gitkeep만 유지).
- **다음 할 일**: 운영 문서(PIPELINE, CALENDAR, 업로드 체크리스트) 작성

### STEP 2. 운영 문서 작성
- **작업**: PIPELINE.md, CALENDAR.md, templates/upload_checklist.md 작성
- **결과**: 완료. 파이프라인 6단계(대본→Vrew→이미지→BGM→내보내기→크로스 업로드,
  편당 60분/주 5편), 주 6시간 배분표 + 30일 플랜, 업로드 전 7항목 체크리스트 문서화.
- **다음 할 일**: 첫 주 대본 5편 작성

### STEP 3. 첫 주 대본 5편 생성
- **작업**: scripts_content/week01/ep01~ep05.md (인체/우주/동물/역사/심리)
- **결과**: 완료. 5편 모두 후킹/본문/마무리/이미지 키워드(영어 5개)/팩트 검증 메모 형식.
  불확실한 수치는 "약/추정/거의" 등으로 완화하고 [검증 필요] 항목을 각 편 메모에 표시함.
  ⚠️ 편집 전 각 편의 [검증 필요] 항목을 반드시 재확인할 것.
- **다음 할 일**: 소재 수집 스크립트 작성

### STEP 4. 소재 수집 스크립트
- **작업**: tools/fetch_stock.py, .env.example
- **결과**: 완료. Pexels API로 키워드 검색 → 세로형(portrait) 필터 → assets/weekXX/ 다운로드.
  API 키는 .env(PEXELS_API_KEY)에서 로드, .env.example 제공. 사용법은 스크립트 상단
  docstring에 포함. `python3 -m py_compile` 구문 검증 통과, --help 동작 확인.
  API 키 발급은 pexels.com/api 안내만 함(실제 키 미포함).
- **다음 할 일**: (사람 작업) 토요일 대본 검증·소재 수집 → 일요일 Vrew 편집 5편 → 평일 업로드.
  다음 주 대본이 필요하면: "week02 대본 5편 생성하고 커밋해줘"

---

## 2026-07-19

### STEP 5. 72시간 수익화 프로젝트 — 상품화 완료
- **작업**: 쇼츠 팩토리 시스템을 판매 상품 2종으로 패키징
  (브랜치: `claude/72h-million-won-revenue-pfbpf1`)
- **결과**: 완료.
  - 전자책 『하루 1시간 쇼츠 공장』 완성: `product/ebook/ebook.md` → PDF 16p
    (`build_pdf.py`, weasyprint + 나눔 폰트). 판매 가능 완성본.
  - 고단가 서비스 상품 설계: 쇼츠 채널 풀 세팅 패키지 49만원 (`sales/service_listing.md`)
  - 전자책 판매 페이지(`sales/ebook_listing.md`), 홍보·DM 문구 6종(`sales/outreach_templates.md`)
  - 72시간 실행 플랜(`docs/PLAN_72H.md`): 주력 = 서비스 2건(98만원), 보조 = 전자책.
    수익 보장 표현은 전 문서에서 배제(법적 리스크 + 신뢰).
- **다음 할 일**: (사람 작업 — PLAN_72H.md Day 1부터)
  ① 크몽 판매자 등록 + 상품 2종 심사 신청 (최우선 — 심사 1~3일)
  ② 토스 송금 링크/구글폼으로 즉시 판매 경로 확보
  ③ 지인 20명 소개 요청 발송.
  서비스 수주 시: "고객 주제 [X]로 컨셉 설계서 + 대본 10편 생성해줘"
