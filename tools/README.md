# 안내 페이지 생성기 (tools/)

`camrescue/camera-error*.html` 은 손으로 고치지 않고 아래에서 만들어요.

- 틀: `tools/guide_template.html` (CSS·머리말·구조는 여기 한 곳)
- 글: `camrescue/guide/<코드>.json` (언어마다 하나, 기준은 `en.json`)
- 생성기: `tools/build_guides.py` (python3 표준 라이브러리만 사용)

## 다시 만들기

```
python3 tools/build_guides.py
```

JSON 이 있는 언어만 HTML 을 만들고 `sitemap.xml` 도 다시 써요. JSON 이 없는 언어는 건너뛰어요.
`en.json` 에 있는 키가 빠졌거나 목록 길이가 다르거나 `meta_description` 이 155자를 넘으면 오류로 멈춰요.
각 페이지의 hreflang 목록과 언어 전환 메뉴는 존재하는 언어만으로 자동 구성돼요.

## 언어 추가

1. `camrescue/guide/en.json` 을 `camrescue/guide/<코드>.json` 으로 복사해요. 코드는 `build_guides.py` 의 `LANGS` 에 있는 것만 써요
   (ar bn cs da de el en es fa fi fil fr hi hu id it iw ja ko ms nl pl pt-BR ro ru sv sw th tr uk ur vi zh-CN zh-TW).
2. `_notes` 를 읽고 모든 값을 번역해요. 키 이름과 목록 길이(steps 7, faq 4, features 4, intro 2)는 그대로 둬요.
3. `python3 tools/build_guides.py` 를 실행하고 `camrescue/camera-error-<코드>.html` 을 브라우저로 확인해요.
4. 커밋해요. (`ko` → `camera-error.html`, `en` → `camera-error-en.html`, 그 밖의 언어는 `camera-error-<코드>.html`)

`iw` 는 파일 이름에는 `iw`, HTML 의 `lang`/hreflang 에는 `he` 를 써요. `ar fa iw ur` 은 `dir="rtl"` 로 만들어져요.
영상은 한국어만 `gGhgxkQdpfE`, 나머지는 `Wu2mAjuBOtQ` 이고, Play 링크는 `&hl=<코드>` 가 붙어요.

## JSON 키

`lang_name`, `lang_switch_label`, `title`, `meta_description`, `og_title`, `og_description`, `h1_main`, `h1_accent`,
`intro[2]`, `howto_name`, `howto_description`, `steps[7]{title, body}`, `app_name`, `app_tagline`, `cta_title`, `cta_intro`,
`features[4]`, `cta_note`, `play_button`, `video_title`, `faq_title`, `faq[4]{q, a}`, `back_home`.
글 안에서는 `<b>…</b>` 만 쓸 수 있고, JSON-LD(HowTo, FAQPage)에는 같은 글이 태그 없이 들어가요.
