# Mudol Labs 사이트

Mudol Labs 앱들의 공개 웹 페이지예요. GitHub Pages(`mudol-labs/site`, `main` 브랜치 루트)로 올라가요.

- 주소: https://mudol-labs.github.io/site/
- 빌드 단계 없음: 정적 HTML 이라 `main` 에 푸시하면 바로 반영돼요 (`.nojekyll` 로 Jekyll 처리 끔)
- 카메라 오류 안내 페이지만 `tools/build_guides.py` 로 생성해요

## 페이지

| 경로 | 내용 | 쓰는 곳 |
|---|---|---|
| `index.html` | Mudol Labs 소개, 찰나 카메라(CamRescue) 소개와 Play 링크 | 홈 |
| `camrescue/privacy.html` | CamRescue 개인정보처리방침 | Play Console 개인정보처리방침 URL |
| `hypeboard/privacy.html` | Hypeboard 개인정보처리방침 | Play Console 개인정보처리방침 URL |
| `sleep/privacy.html` | SleepSonar(슬립소나) 개인정보처리방침 | Play Console 개인정보처리방침 URL |
| `camrescue/camera-error.html` | 카메라 오류 해결 안내 (한국어) | 검색 유입 → CamRescue 설치 |
| `camrescue/camera-error-<코드>.html` | 같은 안내의 다른 언어판 (`en` 포함 33개) | 〃 |
| `google5a7ae87d10111e4e.html` | Google Search Console 소유권 확인 파일. 지우면 안 돼요 | Search Console |
| `robots.txt`, `sitemap.xml` | 검색 엔진용. `sitemap.xml` 은 생성기가 다시 써요 | 검색 엔진 |

개인정보처리방침 URL 은 Play Console 에 등록돼 있어서 경로를 바꾸면 안 돼요.

## 폴더

| 폴더 | 내용 |
|---|---|
| `assets/` | 로고, OG 이미지, CamRescue 아이콘과 스크린샷(한국어·영어) |
| `brand/` | Play 개발자 페이지용 아이콘(512)과 헤더(4096×2304) |
| `camrescue/` | CamRescue 페이지들 |
| `camrescue/guide/` | 안내 페이지 글 JSON, 언어마다 하나 (34개, 기준은 `en.json`) |
| `hypeboard/`, `sleep/` | 각 앱의 개인정보처리방침 |
| `tools/` | 안내 페이지 생성기, 틀, 실제 기기 메뉴 문자열 |

## 카메라 오류 안내 페이지 만들기

`camrescue/camera-error*.html` 은 손으로 고치지 않아요. 글은 `camrescue/guide/<코드>.json`, 틀은 `tools/guide_template.html` 을 고친 뒤 다시 만들어요.

```
python3 tools/build_guides.py
```

python3 표준 라이브러리만 써요. 언어 추가, JSON 키, 메뉴 이름 규칙(`tools/verified_ui_strings.json`)은 [`tools/README.md`](tools/README.md) 에 있어요.

## 고칠 때 규칙

- 개인정보처리방침은 앱에서 수집·권한이 바뀔 때 같이 고치고, 페이지 안의 버전과 날짜도 올려요
- 새 페이지를 추가하면 `sitemap.xml` 에도 넣어요 (안내 페이지는 생성기가 알아서 넣어요)
- 로컬 확인: `python3 -m http.server` 뒤 http://localhost:8000/ 를 열어요
- 커밋은 기능 단위로 나눠서, 한국어 메시지로 써요 (`feat(camrescue): …`, `docs(sleep): …`)
