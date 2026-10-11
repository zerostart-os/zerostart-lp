#!/usr/bin/env python3
"""愛媛の市ごとの粗大ごみ案内ページ（area/index.html）を作る。情報は各市の公式ページで確認したものだけ。"""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publish import HEAD, CSS, CTA, FOOT, BASE, ROOT
CHECKED = "2026年10月"
CITIES = [
 ("松山市","https://www.city.matsuyama.ehime.jp/kurashi/gomi/dashikata/sodaigomi.html","ハガキ・インターネット・市のLINEで申込み。収集日の朝8時までに、粗大ごみシールを貼って申込み時の場所へ出します。木製たんす等は西クリーンセンターへの持ち込みもできます。"),
 ("今治市","https://www.city.imabari.ehime.jp/recycle/kateigomi/kateigomi_imabari.html","有料・予約制。粗大ごみ受付センターへ申込みます。"),
 ("宇和島市","https://www.city.uwajima.ehime.jp/soshiki/15/gomi-sutekata.html","市の収集の対象外です。環境センターへ自分で持ち込むか、市の許可業者に頼む形です（有料）。"),
 ("八幡浜市","https://www.city.yawatahama.ehime.jp/doc/2022091300010/","定期の収集はありません。環境センターへ持ち込むか、電話で収集を頼みます（有料）。"),
 ("新居浜市","https://www.city.niihama.lg.jp/soshiki/haiki/dasikata-oogata.html","「大型ごみ」として、電話か電子申請で申込み、処理券を貼って出します。空き家・引っ越し・遺品整理で出るごみは対象外と案内されています。"),
 ("西条市","https://www.city.saijo.ehime.jp/soshiki/eisei/gominowakekata.html","電話かインターネットで事前に申込み、処理券を貼って出します。"),
 ("大洲市","https://www.city.ozu.ehime.jp/uploaded/attachment/46102.pdf","電話で予約し、粗大ごみ処理シールを貼って出します（市の「ごみ分別辞典」）。"),
 ("伊予市","https://www.city.iyo.lg.jp/shiminseikatsu/kurashi/gomi/bunbetsu/sodai/dashikata/calendar.html","申込みはがきか電子申請で申込み、届いた粗大ごみシールを貼って出します。"),
 ("四国中央市","https://www.city.shikokuchuo.ehime.jp/soshiki/15/1924.html","申込み方法と手数料は、市の「粗大ごみ収集運搬の手引き」（PDF）に載っています。問い合わせは生活環境課 ごみ減量推進係（0896-28-6015）です。"),
 ("西予市","https://www.city.seiyo.ehime.jp/kurashi/life/gomi/2370.html","出し方は、市の「ごみの分け方・出し方」（PDF）の粗大ごみの項に載っています。問い合わせは環境衛生課（0894-62-1132）です。"),
 ("東温市","https://www.city.toon.ehime.jp/uploaded/attachment/22090.pdf","1メートル程度・大人2人で運べる物を、小さくして集積場にそのまま出します。引っ越しや片付けで一度に多く出すときは集積場に出さず、専門業者に個別に頼むよう案内されています。東温市リサイクルセンターは粗大ごみを受け入れていません。"),
]
def build():
    url=BASE+"area/"
    title="愛媛の市ごとの粗大ごみの出し方｜実家の片付け前に｜ZERO START"
    desc="愛媛県の11市の、粗大ごみの申込み方法と市の公式ページをまとめました。市によって申込みの仕方も、そもそも市が集めるかどうかも違います。"
    ld={"@context":"https://schema.org","@type":"WebPage","name":title,"description":desc,"url":url,"inLanguage":"ja"}
    h=HEAD.format(title=html.escape(title),desc=html.escape(desc),url=url,base=BASE,css=CSS+".city{border-bottom:1px solid #D9DDD8;padding:16px 0}.city h2{margin:0 0 6px;border:0;padding:0;font-size:19px}.city p{margin:0 0 6px}",ogtype="website",ld=f'<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>')
    body=f"""<h1>愛媛の市ごとの、粗大ごみの出し方</h1>
<p>実家の片付けで、大きな家具や家電をご自分で出そうとすると、市によって仕組みがまったく違うことに驚かれると思います。ハガキで申し込む市、電話で予約する市、そもそも市が集めない市もあります。</p>
<p>下は、各市の公式ページで確かめた申込み方法の要点です（{CHECKED}時点）。出す前に、必ずリンク先の市のページで最新の案内を確認してください。</p>
"""
    for name,link,how in CITIES:
        body+=f'<div class="city"><h2>{html.escape(name)}</h2>'
        body+=f'<p>{html.escape(how)}</p>' if how else '<p>市の案内（PDF）で出し方を確認してください。</p>'
        body+=f'<p><a href="{html.escape(link)}">{html.escape(name)}の公式ページを開く</a></p></div>\n'
    body+="""<h2>出す前に、一度だけ止まってください</h2>
<p>粗大ごみとして出そうとしている物の中に、行先のある物が混ざっていることは少なくありません。タンスの引き出しの中身、箱のままの贈答品、重い金属の置物、古い道具。出してしまうと、もう戻りません。</p>
<p>ZERO STARTの「仕分けコーディネート」では、私たちが一緒に入って、行先のある物とそうでない物を見分けます。行先のある物はお引き受けし、処分になる物は、上の市のルールでご家族に出していただく形です。</p>
<p><a href="../kiji/">片付けの現場からの読みもの</a>もあわせてどうぞ。</p>
"""
    open(os.path.join(ROOT,"area","index.html"),"w",encoding="utf-8").write(h+body+CTA+FOOT.format(base=BASE))
if __name__=="__main__": build(); print("ok")
