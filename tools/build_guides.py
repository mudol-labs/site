#!/usr/bin/env python3
"""CamRescue 카메라 오류 안내 페이지 생성기 (python3 표준 라이브러리만 사용).

camrescue/guide/<lang>.json + tools/guide_template.html -> camrescue/camera-error*.html
그리고 sitemap.xml 을 다시 쓴다. 사용법은 tools/README.md 참고.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE_DIR = ROOT / "camrescue" / "guide"
OUT_DIR = ROOT / "camrescue"
TEMPLATE = Path(__file__).resolve().parent / "guide_template.html"
SITE = "https://mudol-labs.github.io/site"
VIDEO_KO = "gGhgxkQdpfE"
VIDEO_OTHER = "Wu2mAjuBOtQ"
META_MAX = 155

# 코드 -> (html lang / hreflang, og:locale, Play hl, 방향)
LANGS = {
    "ar": ("ar", "ar_AR", "ar", "rtl"),
    "bn": ("bn", "bn_IN", "bn", "ltr"),
    "cs": ("cs", "cs_CZ", "cs", "ltr"),
    "da": ("da", "da_DK", "da", "ltr"),
    "de": ("de", "de_DE", "de", "ltr"),
    "el": ("el", "el_GR", "el", "ltr"),
    "en": ("en", "en_US", "en", "ltr"),
    "es": ("es", "es_ES", "es", "ltr"),
    "fa": ("fa", "fa_IR", "fa", "rtl"),
    "fi": ("fi", "fi_FI", "fi", "ltr"),
    "fil": ("fil", "fil_PH", "fil", "ltr"),
    "fr": ("fr", "fr_FR", "fr", "ltr"),
    "hi": ("hi", "hi_IN", "hi", "ltr"),
    "hu": ("hu", "hu_HU", "hu", "ltr"),
    "id": ("id", "id_ID", "id", "ltr"),
    "it": ("it", "it_IT", "it", "ltr"),
    "iw": ("he", "he_IL", "iw", "rtl"),
    "ja": ("ja", "ja_JP", "ja", "ltr"),
    "ko": ("ko", "ko_KR", "ko", "ltr"),
    "ms": ("ms", "ms_MY", "ms", "ltr"),
    "nl": ("nl", "nl_NL", "nl", "ltr"),
    "pl": ("pl", "pl_PL", "pl", "ltr"),
    "pt-BR": ("pt-BR", "pt_BR", "pt-BR", "ltr"),
    "ro": ("ro", "ro_RO", "ro", "ltr"),
    "ru": ("ru", "ru_RU", "ru", "ltr"),
    "sv": ("sv", "sv_SE", "sv", "ltr"),
    "sw": ("sw", "sw_KE", "sw", "ltr"),
    "th": ("th", "th_TH", "th", "ltr"),
    "tr": ("tr", "tr_TR", "tr", "ltr"),
    "uk": ("uk", "uk_UA", "uk", "ltr"),
    "ur": ("ur", "ur_PK", "ur", "rtl"),
    "vi": ("vi", "vi_VN", "vi", "ltr"),
    "zh-CN": ("zh-CN", "zh_CN", "zh-CN", "ltr"),
    "zh-TW": ("zh-TW", "zh_TW", "zh-TW", "ltr"),
}
STRING_KEYS = [
    "lang_name", "lang_switch_label", "title", "meta_description", "og_title", "og_description",
    "h1_main", "h1_accent", "howto_name", "howto_description", "app_name", "app_tagline",
    "cta_title", "cta_intro", "cta_note", "play_button", "video_title", "faq_title", "back_home",
]
BOLD = re.compile(r"</?b>")


def filename(code):
    return {"ko": "camera-error.html", "en": "camera-error-en.html"}.get(code, f"camera-error-{code}.html")


def url(code):
    return f"{SITE}/camrescue/{filename(code)}"


def esc(text):
    """일반 글자는 이스케이프하고 <b>만 살린다."""
    out = html.escape(text, quote=False)
    return out.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")


def plain(text):
    return BOLD.sub("", text)


def attr(text):
    return html.escape(plain(text), quote=False).replace('"', "&quot;")


def check_shape(code, data, ref):
    """en.json 에 있는 키가 빠졌거나 모양이 다르면 바로 실패한다."""
    errors = []

    def walk(path, d, r):
        if isinstance(r, dict):
            if not isinstance(d, dict):
                errors.append(f"{path}: 객체여야 합니다")
                return
            for k, v in r.items():
                if k.startswith("_"):
                    continue
                if k not in d:
                    errors.append(f"{path}{k}: 키가 없습니다")
                else:
                    walk(f"{path}{k}.", d[k], v)
        elif isinstance(r, list):
            if not isinstance(d, list) or len(d) != len(r):
                errors.append(f"{path.rstrip('.')}: 목록 길이가 {len(r)} 이어야 합니다")
                return
            for i, (dv, rv) in enumerate(zip(d, r)):
                walk(f"{path}{i}.", dv, rv)
        else:
            if not isinstance(d, str) or not d.strip():
                errors.append(f"{path.rstrip('.')}: 비어 있지 않은 문자열이어야 합니다")
            elif re.search(r"<(?!/?b>)", d):
                errors.append(f"{path.rstrip('.')}: <b> 외의 태그는 쓸 수 없습니다")

    walk("", data, ref)
    if len(data.get("meta_description", "")) > META_MAX:
        errors.append(f"meta_description: {len(data['meta_description'])}자 (최대 {META_MAX})")
    if errors:
        sys.exit(f"[{code}.json] 오류:\n  " + "\n  ".join(errors))


def render(code, data, codes, names):
    html_lang, og_locale, play_hl, direction = LANGS[code]
    page = url(code)
    hreflang = [
        f'<link rel="alternate" hreflang="{LANGS[c][0]}" href="{url(c)}">' for c in codes
    ]
    hreflang.append(f'<link rel="alternate" hreflang="x-default" href="{url("en")}">')
    alternates = [
        f'<meta property="og:locale:alternate" content="{LANGS[c][1]}">' for c in codes if c != code
    ]
    lang_links = []
    for c in codes:
        cur = ' aria-current="page"' if c == code else ""
        lang_links.append(
            f'          <li><a href="{filename(c)}" hreflang="{LANGS[c][0]}" lang="{LANGS[c][0]}"{cur}>'
            f"{html.escape(names[c], quote=False)}</a></li>"
        )
    steps_html, steps_ld = [], []
    for i, s in enumerate(data["steps"], 1):
        steps_html.append(f'      <li id="step-{i}"><h3>{esc(s["title"])}</h3><p>{esc(s["body"])}</p></li>')
        steps_ld.append({"@type": "HowToStep", "position": i, "name": s["title"], "text": plain(s["body"]),
                         "url": f"{page}#step-{i}"})
    faq_html = [f'      <details><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>' for f in data["faq"]]
    ld = [
        {"@context": "https://schema.org", "@type": "HowTo", "name": data["howto_name"],
         "description": data["howto_description"], "inLanguage": html_lang, "step": steps_ld},
        {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": html_lang,
         "mainEntity": [{"@type": "Question", "name": plain(f["q"]),
                         "acceptedAnswer": {"@type": "Answer", "text": plain(f["a"])}} for f in data["faq"]]},
    ]
    ld_text = json.dumps(ld, ensure_ascii=False, indent=2).replace("</", "<\\/")
    values = {
        "html_lang": html_lang, "dir": direction, "site": SITE, "page_url": page, "og_locale": og_locale,
        "title": html.escape(data["title"], quote=False),
        "meta_description": attr(data["meta_description"]),
        "og_title": attr(data["og_title"]), "og_description": attr(data["og_description"]),
        "hreflang_links": "\n".join(hreflang), "og_alternates": "\n".join(alternates),
        "json_ld": ld_text,
        "lang_switch_label": attr(data["lang_switch_label"]),
        "lang_name": html.escape(data["lang_name"], quote=False), "lang_links": "\n".join(lang_links),
        "h1_main": esc(data["h1_main"]), "h1_accent": esc(data["h1_accent"]),
        "intro": "\n".join(f'    <p class="intro">{esc(p)}</p>' for p in data["intro"]),
        "steps": "\n".join(steps_html),
        "app_name": esc(data["app_name"]), "app_tagline": esc(data["app_tagline"]),
        "cta_title": esc(data["cta_title"]), "cta_intro": esc(data["cta_intro"]),
        "features": "\n".join(f"        <li><span>{esc(f)}</span></li>" for f in data["features"]),
        "cta_note": esc(data["cta_note"]),
        "play_hl": play_hl, "play_button": esc(data["play_button"]),
        "video_id": VIDEO_KO if code == "ko" else VIDEO_OTHER, "video_title": attr(data["video_title"]),
        "faq_title": esc(data["faq_title"]), "faq": "\n".join(faq_html), "back_home": esc(data["back_home"]),
    }
    out = TEMPLATE.read_text(encoding="utf-8")
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], out)
    return out


def write_sitemap(codes):
    path = ROOT / "sitemap.xml"
    old = re.findall(r"<loc>(.*?)</loc>", path.read_text(encoding="utf-8")) if path.exists() else []
    guide = [url(c) for c in sorted(codes, key=lambda c: (c not in ("ko", "en"), c != "ko", c))]
    is_guide = re.compile(re.escape(f"{SITE}/camrescue/camera-error") + r"(-[A-Za-z-]+)?\.html$")
    locs, inserted = [], False
    for loc in old:
        if is_guide.match(loc):
            if not inserted:
                locs += guide
                inserted = True
        else:
            locs.append(loc)
    if not inserted:
        locs += guide
    body = "\n".join(f"  <url><loc>{html.escape(l)}</loc></url>" for l in locs)
    path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n",
                    encoding="utf-8")


def main():
    en_path = GUIDE_DIR / "en.json"
    if not en_path.exists():
        sys.exit("camrescue/guide/en.json 이 없습니다 (기준 파일)")
    ref = json.loads(en_path.read_text(encoding="utf-8"))
    for stray in sorted(GUIDE_DIR.glob("*.json")):
        if stray.stem not in LANGS:
            sys.exit(f"{stray.name}: 알 수 없는 언어 코드입니다 (허용: {' '.join(LANGS)})")
    codes, data, skipped = [], {}, []
    for code in LANGS:  # LANGS 순서 = 언어 전환 목록 순서
        p = GUIDE_DIR / f"{code}.json"
        if not p.exists():
            skipped.append(code)
            continue
        try:
            data[code] = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            sys.exit(f"[{code}.json] JSON 문법 오류: {e}")
        check_shape(code, data[code], ref)
        codes.append(code)
    names = {c: data[c]["lang_name"] for c in codes}
    for code in codes:
        (OUT_DIR / filename(code)).write_text(render(code, data[code], codes, names), encoding="utf-8")
    write_sitemap(codes)
    print(f"생성 {len(codes)}개: {' '.join(codes)}")
    if skipped:
        print(f"건너뜀(JSON 없음) {len(skipped)}개: {' '.join(skipped)}")


if __name__ == "__main__":
    main()
