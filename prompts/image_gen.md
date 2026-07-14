# AI 이미지 프롬프트 템플릿 (MS Designer / Bing Image Creator 용)

스톡 이미지(Pexels/Pixabay)로 커버가 안 되는 항목에만 AI 생성 이미지를 사용한다.

## 기본 템플릿

```
[subject], vertical 9:16 composition, cinematic lighting,
high detail, dramatic atmosphere, no text, no watermark
```

- `[subject]`에 대본의 "이미지 키워드"를 영어로 넣는다.
- **no text 필수**: AI가 넣는 글자는 대부분 오탈자 → 자막은 Vrew에서만.

## 스타일 변형

| 용도 | 추가 키워드 |
|------|------------|
| 우주/과학 | `deep space, nebula colors, NASA photography style` |
| 인체/의학 | `medical illustration style, clean background` |
| 역사 | `historical painting style, muted colors, archival photo look` |
| 동물 | `wildlife photography, telephoto lens, natural habitat` |
| 심리/추상 | `surreal concept art, symbolic, minimal composition` |

## 규칙
- 실존 인물 얼굴 생성 금지 (초상권 위험).
- 타인 영상/이미지 재사용 금지 — 스톡(라이선스 확인) 또는 직접 생성만.
- 생성 이미지는 `assets/weekXX/`에 저장 (git 추적 제외).
