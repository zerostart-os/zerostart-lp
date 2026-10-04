#!/usr/bin/env python3
"""承認済み記事(JSON)を kiji/<id>.html に書き出し、記事一覧とサイトマップを作り直す。
使い方: python3 tools/publish.py path/to/article.json [...]
JSON: {id, title, description, body, keyword, publishedAt(YYYY-MM-DD)}"""
import json, sys, os, re, html, glob, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://zerostart-os.github.io/zerostart-lp/"
DATA = os.path.join(ROOT, "kiji", "data")
os.makedirs(DATA, exist_ok=True)

CSS = """body{margin:0;background:#F4F5F2;color:#18201C;font-family:'Zen Kaku Gothic New','Hiragino Sans','Noto Sans JP',sans-serif;line-height:1.95;font-size:17px;line-break:strict;overflow-wrap:anywhere}
a{color:#2F5D50}header{border-bottom:1px solid #D9DDD8;background:#F4F5F2;position:sticky;top:0;z-index:5}
.in{max-width:760px;margin:0 auto;padding:0 20px}.hd{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 20px;max-width:760px;margin:0 auto}
.logo{font-family:'Dela Gothic One',sans-serif;font-size:20px;color:#18201C;text-decoration:none;white-space:nowrap}
.tel{white-space:nowrap;background:#18201C;color:#fff;text-decoration:none;border-radius:999px;padding:8px 14px;font-weight:700;font-size:14px}
h1{font-size:clamp(23px,4.6vw,34px);line-height:1.5;margin:40px 0 12px;word-break:keep-all;overflow-wrap:anywhere}
h2{font-size:clamp(19px,3.6vw,24px);line-height:1.6;margin:44px 0 8px;padding-left:12px;border-left:4px solid #2F5D50;word-break:keep-all;overflow-wrap:anywhere}
p{margin:0 0 18px}ul{margin:0 0 18px;padding-left:1.3em}.meta{color:#55605A;font-size:14px;margin-bottom:28px}
.cta{background:#18201C;color:#F4F5F2;border-radius:16px;padding:26px 22px;margin:48px 0}.cta p{margin:0 0 14px}
.btns{display:flex;flex-wrap:wrap;gap:10px}.btn{flex:1 1 220px;display:block;text-align:center;padding:16px;border-radius:12px;font-weight:700;text-decoration:none}
.line{background:#2F5D50;color:#fff}.call{background:#fff;color:#18201C}
footer{font-size:14px;color:#55605A;padding:30px 0 60px}.list a{display:block;padding:16px 0;border-bottom:1px solid #D9DDD8;text-decoration:none;color:#18201C}
.list small{display:block;color:#55605A}"""

HEAD = """<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{base}ogp.png"><meta property="og:type" content="{ogtype}"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Zen+Kaku+Gothic+New:wght@400;700&display=swap">
<style>{css}</style>{ld}</head><body>
<header><div class="hd"><a class="logo" href="{base}">ZERO START</a><a class="tel" href="tel:08096797780">080-9679-7780</a></div></header>
<main class="in">"""

CTA = """<section class="cta"><p><b>迷う物が一つあるだけでも、ご相談ください。</b><br>写真を送るだけでも大丈夫です。愛媛県全域、下見・お見積りは無料です。</p>
<div class="btns"><a class="btn line" href="https://lin.ee/9xSARtV">LINEで写真を送る</a><a class="btn call" href="tel:08096797780">電話する 080-9679-7780</a></div></section>"""

FOOT = """</main><footer class="in">ZERO START（ゼロスタート）／愛媛県松山市菅沢町1024-1／古物商許可 愛媛県公安委員会 第821190001351号<br>
<a href="{base}">相談ページ</a>・<a href="{base}kiji/">読みもの一覧</a></footer></body></html>"""

def body_html(body):
    out=[]; blocks=re.split(r"\n\s*\n", body.strip())
    for b in blocks:
        lines=[l for l in b.split("\n") if l.strip()]
        if not lines: continue
        m=re.fullmatch(r"【(.+)】", lines[0].strip())
        if m:
            out.append(f"<h2>{html.escape(m.group(1))}</h2>"); lines=lines[1:]
            if not lines: continue
        if all(l.strip().startswith("・") for l in lines):
            out.append("<ul>"+"".join(f"<li>{html.escape(l.strip()[1:])}</li>" for l in lines)+"</ul>")
        else:
            out.append("<p>"+"<br>".join(html.escape(l) for l in lines)+"</p>")
    return "\n".join(out)

def strip_signoff(body):
    # 末尾の「捨てる前に、一度ご相談ください。…電話…」はCTAで置き換える
    return re.sub(r"\n*捨てる前に、一度ご相談ください。\s*\nZERO START[^\n]*$", "", body.strip())

def page(a):
    url=f"{BASE}kiji/{a['id']}.html"
    ld={"@context":"https://schema.org","@type":"Article","headline":a["title"],"description":a["description"],"datePublished":a["publishedAt"],
        "inLanguage":"ja","mainEntityOfPage":url,"image":BASE+"ogp.png","author":{"@type":"Organization","name":"ZERO START（ゼロスタート）","url":BASE},
        "publisher":{"@type":"Organization","name":"ZERO START（ゼロスタート）","logo":{"@type":"ImageObject","url":BASE+"ogp.png"}}}
    h=HEAD.format(title=html.escape(a["title"])+"｜ZERO START", desc=html.escape(a["description"]), url=url, base=BASE, css=CSS, ogtype="article",
        ld=f'<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>')
    return h+f"<h1>{html.escape(a['title'])}</h1><div class='meta'>{a['publishedAt'].replace('-','.')}　ZERO START</div>"+body_html(strip_signoff(a["body"]))+CTA+FOOT.format(base=BASE)

def rebuild():
    arts=[json.load(open(f)) for f in glob.glob(os.path.join(DATA,"*.json"))]
    arts.sort(key=lambda a:a["publishedAt"], reverse=True)
    for a in arts: open(os.path.join(ROOT,"kiji",a["id"]+".html"),"w",encoding="utf-8").write(page(a))
    idx=HEAD.format(title="読みもの｜ZERO START（松山の片付け・遺品整理）", desc="捨てる前に、行先を考える。松山・愛媛の片付けの現場から、物の行先の話。", url=BASE+"kiji/", base=BASE, css=CSS, ogtype="website", ld="")
    idx+="<h1>読みもの</h1><p>片付けの現場から、物の行先の話を書いています。</p><div class='list'>"+"".join(
        f"<a href='{a['id']}.html'>{html.escape(a['title'])}<small>{a['publishedAt'].replace('-','.')}</small></a>" for a in arts)+"</div>"+CTA+FOOT.format(base=BASE)
    open(os.path.join(ROOT,"kiji","index.html"),"w",encoding="utf-8").write(idx)
    today=datetime.date.today().isoformat()
    urls=[(BASE,today)]+([(BASE+"kiji/",arts[0]["publishedAt"])] if arts else [])+[(f"{BASE}kiji/{a['id']}.html",a["publishedAt"]) for a in arts]
    open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u,d in urls)+"</urlset>\n")
    return arts

if __name__=="__main__":
    for p in sys.argv[1:]:
        a=json.load(open(p)); keep={k:a[k] for k in ("id","title","description","body","keyword","publishedAt") if k in a}
        json.dump(keep, open(os.path.join(DATA,a["id"]+".json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(rebuild()), "articles")
