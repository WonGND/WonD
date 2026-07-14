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
- **결과**: (진행 예정)
- **다음 할 일**: 첫 주 대본 5편 작성

### STEP 3. 첫 주 대본 5편 생성
- **작업**: scripts_content/week01/ep01~ep05.md (인체/우주/동물/역사/심리)
- **결과**: (진행 예정)
- **다음 할 일**: 소재 수집 스크립트 작성

### STEP 4. 소재 수집 스크립트
- **작업**: tools/fetch_stock.py, .env.example
- **결과**: (진행 예정)
- **다음 할 일**: Vrew 편집 → 첫 업로드 (토요일 대본/소재, 일요일 편집)
