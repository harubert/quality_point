"""Baut die Stil-Vorschauen und die Auswahlseite.

  styles/_vorschau/<stil>.html   8 Musterfolien (1920×1080) im jeweiligen Stil; mit #mini nur 4 (2×2)
  styles/index.html              Auswahlseite: alle Stile als Mini-Folien + alle Schriftsets
  styles/<stil>/vorschau.webp    Bildschirmfoto (headless Edge/Chrome) für README   (Option --bilder)

Aufruf:  python styles/_werkzeuge/vorschau_bauen.py [--bilder]
Nur lokale Ressourcen – keine Aufrufe ins Netz. Grundgerüst: engine/src/basis.css (wie im Build).
"""
import html, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

STYLES = Path(__file__).resolve().parent.parent
VS = STYLES / "_vorschau"
REIHENFOLGE = ["papiertheater", "fibel", "gouache", "knetwerk", "nachtprogramm", "riso",
               "tafelkreide", "bauhaus", "journal", "comic"]
BROWSER = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
           r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
           r"C:\Program Files\Google\Chrome\Application\chrome.exe",
           "/usr/bin/chromium", "/usr/bin/google-chrome",
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]


def bild(sid, name):
    for ext in ("webp", "svg", "jpg", "png"):
        p = STYLES / sid / "beispiel" / f"{name}.{ext}"
        if p.exists():
            return f"../{sid}/beispiel/{name}.{ext}"
    return ""


def folien(sid):
    t, m = bild(sid, "titel"), bild(sid, "motiv")
    fuss = lambda k, q, n: (f'<footer><span class="chap">{k}</span><span class="src{" nolabel" if not q else ""}">{q}</span>'
                            f'<span class="pg">{n}</span></footer>')
    return [
f'''<section class="slide s-title cur"><img class="hero" src="{t}" alt="">
<div class="tt"><div class="kick">Medienpädagogik · Primarstufe</div>
<h1>Zwischen <em>Bildschirm</em> und Bilderbuch</h1>
<p class="sub">Wie Kinder Medien erleben – und was Schule daraus macht</p></div>
<div class="who"><b>Vorname Nachname</b><br>Pädagogische Hochschule · Seminar 2026</div></section>''',
f'''<section class="slide s-chapter cur"><img class="hero" src="{m}" alt=""><div class="bignum">2</div>
<div class="etikett"><div class="kick">Kapitel 2</div><h2>Geschichten, die <em>wirken</em></h2>
<p class="lead">Werbung, Vorbilder und Spiele im Kinderzimmer</p>
<div class="toc"><div><b>2.1</b>Werbung erkennen</div><div><b>2.2</b>Lootboxen</div><div><b>2.3</b>Vorbilder</div><div><b>2.4</b>Gespräche führen</div></div></div>
{fuss("Kapitel 2", "", 7)}</section>''',
f'''<section class="slide cur"><div class="kick">Forschung</div><h2>Was Kinder <em>wirklich</em> brauchen</h2>
<div class="g2" style="align-items:start"><div class="card t tape"><div class="quote" style="font-size:44px">“Children learn best when media use is shared and talked about.”
<p class="ueb">Kinder lernen am besten, wenn Mediennutzung geteilt und besprochen wird.</p><cite>Beispielzitat (sinngemäß)</cite></div></div>
<div class="col"><div class="box tip"><div class="bh"><i><span>!</span></i>Tipp für die Praxis</div><p>Gemeinsam schauen, gemeinsam reden – Fragen der Kinder ernst nehmen.</p></div>
<ul class="dots"><li>Medienzeiten gemeinsam vereinbaren</li><li>Inhalte vorher selbst sichten</li><li>Über Gefühle beim Spielen sprechen</li></ul></div></div>
{fuss("Kapitel 1", "Beispielquelle (2026)", 3)}</section>''',
f'''<section class="slide cur"><div class="kick">Zahlen</div><h2>Mediennutzung in <em>Zahlen</em></h2>
<div class="g3"><div class="card r"><div class="zahl">71<small>%</small></div><div class="zl">nutzen täglich ein Tablet</div></div>
<div class="card t"><div class="zahl">48<small>min</small></div><div class="zl">Bildschirmzeit pro Schultag</div></div>
<div class="card y"><div class="zahl">3<small>von 4</small></div><div class="zl">Kindern schauen Videos allein</div></div></div>
<div class="bars auto mt"><div class="bz"><span>Videos</span><div class="bt"><i style="--w:78%"></i></div><span class="bv">78 %</span></div>
<div class="bz t"><span>Spiele</span><div class="bt"><i style="--w:56%"></i></div><span class="bv">56 %</span></div>
<div class="bz"><span>Hörbücher</span><div class="bt"><i style="--w:31%"></i></div><span class="bv">31 %</span></div></div>
<p class="lesehilfe"><span class="lh">i</span><b>Lesehilfe:</b> Beispielwerte zur Illustration des Stils – keine echten Daten.</p>
{fuss("Kapitel 1", "Beispielwerte", 4)}</section>''',
f'''<section class="slide s-statement cur"><div class="kick">Merksatz</div>
<p class="big">Medienbildung beginnt nicht am Gerät, sondern im <em>Gespräch</em>.</p>{fuss("Fazit", "", 12)}</section>''',
f'''<section class="slide s-dark cur"><div class="kick">Reflexion</div><h2>Was bleibt <em>hängen?</em></h2>
<div class="g3"><div class="card"><h3>Sehen</h3><p>Was fällt Ihnen an der Werbung zuerst auf?</p></div>
<div class="card"><h3>Fühlen</h3><p>Welche Gefühle soll sie bei Kindern wecken?</p></div>
<div class="card"><h3>Handeln</h3><p>Wie würden Sie im Unterricht reagieren?</p></div></div>
<div class="quote mt2" style="font-size:40px">“Media literacy is a conversation, not a lecture.”<p class="ueb">Medienkompetenz ist ein Gespräch, kein Vortrag.</p></div>
{fuss("Kapitel 2", "", 9)}</section>''',
f'''<section class="slide s-auftrag cur"><div class="wk"><span class="wn">W1</span><span class="wl">Werkstatt · 20 Minuten</span></div>
<h2>Eine Werbung <em>entlarven</em></h2>
<div class="g2"><div class="panel"><h4>Auftrag</h4><ol class="steps"><li>Clip zweimal ansehen</li><li>Tricks notieren (Musik, Farben, Stars)</li><li>Plakat „So wirkt Werbung“ gestalten</li></ol></div>
<div class="panel"><h4>Material</h4><ul class="dots"><li>Tablet mit Beispielclip</li><li>Plakatbogen, Stifte</li><li>Checkliste Werbetricks</li></ul>
<div class="meta mt"><span>Partnerarbeit</span><span>3./4. Klasse</span></div></div></div>
{fuss("Werkstatt", "", 10)}</section>''',
f'''<section class="slide cur"><div class="kick">Material</div><h2>Fotos, Zettel und <em>Tabellen</em></h2>
<div class="row fill" style="align-items:flex-start"><div class="foto" style="width:560px;height:420px;--r:-2deg"><img src="{m}" alt=""><p class="cap">Abb. 1: Beispielbild im Stil</p></div>
<div class="col grow"><div class="zettel" style="--r:1.2deg">Notiz: Erst fragen, was die Kinder schon kennen!</div>
<table class="tbl compact"><tr><th>Medium</th><th>Alter</th><th>Begleitung</th></tr><tr><td>Bilderbuch-App</td><td>ab 4</td><td>gemeinsam</td></tr>
<tr><td>Videoplattform</td><td>ab 6</td><td>Absprache</td></tr><tr><td>Online-Spiel</td><td>ab 8</td><td>Regeln</td></tr></table>
<div><span class="tag">Wahrnehmen</span> <span class="tag c">Bewerten</span> <span class="tag y">Gestalten</span></div></div></div>
{fuss("Anhang", "Eigene Darstellung", 14)}</section>''',
    ]


SEITE = '''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} – Stilvorschau</title>
<link rel="stylesheet" href="../../engine/src/basis.css">
<link rel="stylesheet" href="../{sid}/fonts/fonts.css">
<link rel="stylesheet" href="../{sid}/stil.css">
<style>
html,body{{height:auto;overflow:auto}} body{{display:block;padding:0}}
#vs{{display:grid;grid-template-columns:1920px 1920px;gap:40px;transform-origin:0 0;padding:40px;width:max-content}}
#vs .slide{{position:relative;inset:auto;opacity:1;visibility:visible;transform:none;transition:none}}
#vs .slide.s-title .a,#vs .slide .a{{opacity:1;transform:none}}
body.mini #vs{{gap:24px;padding:0}} body.mini #vs .slide:nth-child(n+5){{display:none}}
</style></head>
<body><div id="vs">
{folien}
</div>
<script>
if(location.hash==='#mini')document.body.classList.add('mini');
function fit(){{var v=document.getElementById('vs');v.style.transform='none';
  var w=v.scrollWidth,h=v.scrollHeight,s=Math.min(innerWidth/w,document.body.classList.contains('mini')?innerHeight/h:9);
  v.style.transform='scale('+s+')';document.body.style.height=(h*s)+'px';}}
addEventListener('resize',fit);fit();
</script></body></html>
'''


def seiten():
    stile = []
    for sid in REIHENFOLGE:
        if not (STYLES / sid / "stil.json").exists():
            continue
        cfg = json.loads((STYLES / sid / "stil.json").read_text(encoding="utf-8"))
        stile.append(cfg)
        (VS / f"{sid}.html").write_text(SEITE.format(name=html.escape(cfg["name"]), sid=sid,
                                                     folien="\n".join(folien(sid))), encoding="utf-8")
    sets = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((STYLES / "_schriftsets").glob("*.json"))]
    sets.sort(key=lambda s: REIHENFOLGE.index(s["standard_fuer_stil"]) if s["standard_fuer_stil"] in REIHENFOLGE else 99)
    karten = []
    for c in stile:
        farben = "".join(f'<i style="background:{v}" title="{k} {v}"></i>' for k, v in c["farben"].items()
                         if k in ("paper", "card", "ink", "red", "teal", "yellow", "coral"))
        karten.append(f'''<article class="stil"><a class="bildlink" href="_vorschau/{c["id"]}.html" title="Groß ansehen: alle Musterfolien">
<iframe src="_vorschau/{c["id"]}.html#mini" loading="lazy" tabindex="-1" title="{html.escape(c["name"])}"></iframe></a>
<div class="txt"><h3>{html.escape(c["name"])} <code>{c["id"]}</code></h3><p>{html.escape(c["beschreibung"])}</p>
<p class="meta"><b>Stimmung:</b> {html.escape(c["stimmung"])}<br><b>Schriftset:</b> {html.escape(c["schriftset"])} · <b>Passt zu:</b> {html.escape(", ".join(c["passt_zu"]))}</p>
<div class="farben">{farben}</div><a class="gross" href="_vorschau/{c["id"]}.html">Alle Musterfolien groß ansehen →</a></div></article>''')
    zeilen = []
    for s in sets:
        v = s["css_variablen"]
        zeilen.append(f'''<article class="set"><h3>{html.escape(s["name"])} <code>{s["id"]}</code> <small>Standard für „{s["standard_fuer_stil"]}“</small></h3>
<p class="m-titel" style="font-family:{html.escape(v["--serif"])}">Zwischen Bildschirm und Bilderbuch</p>
<p class="m-akzent" style="font-family:{html.escape(v["--accent"])}">wirklich wichtig – Gespräch</p>
<p class="m-lesen" style="font-family:{html.escape(v["--lesen"])}">„Kinder lernen am besten, wenn Mediennutzung geteilt wird.“ Äpfel, Öl, Übung, Straße – 0123456789</p>
<p class="m-ui" style="font-family:{html.escape(v["--ui"])}">Fließtext und Beschriftungen: Schülerinnen und Schüler gestalten gemeinsam ein Plakat (3./4. Schulstufe).</p>
<p class="sl">Titel <b>{s["titel"]["familie"]}</b> · Akzent <b>{s["akzent"]["familie"]}</b> · Lesen <b>{s["lesen"]["familie"]}</b> · UI <b>{s["ui"]["familie"]}</b> — {s["lizenz"]}</p></article>''')
    links = "\n".join(f'<link rel="stylesheet" href="_schriftsets/fonts/{s["id"]}.css">' for s in sets)
    (STYLES / "index.html").write_text(INDEX.format(links=links, karten="\n".join(karten), zeilen="\n".join(zeilen),
                                                    n=len(stile), m=len(sets)), encoding="utf-8")
    print(len(stile), "Stile,", len(sets), "Schriftsets -> index.html")
    return stile


INDEX = '''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quality Point – Stile und Schriftsets</title>
{links}
<style>
:root{{--bg:#F5F2EC;--fg:#1E1E1E;--mut:#555;--card:#fff;--line:#DDD6C8;--acc:#B23A2A}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16171A;--fg:#ECEAE4;--mut:#B4B0A8;--card:#212226;--line:#34363C;--acc:#F08A6E}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--fg);font:400 17px/1.55 "Instrument Sans","Segoe UI",system-ui,sans-serif}}
header,main{{max-width:1480px;margin:0 auto;padding:0 24px}}
header{{padding-top:40px}} h1{{font:400 46px/1.1 "Young Serif",Georgia,serif;margin:0 0 10px}} h2{{font:400 30px/1.2 "Young Serif",Georgia,serif;margin:48px 0 16px}}
header p{{max-width:860px;color:var(--mut)}} code{{font-size:.8em;background:rgba(127,127,127,.15);padding:2px 6px;border-radius:5px}}
.raster{{display:grid;grid-template-columns:repeat(auto-fill,minmax(440px,1fr));gap:24px}}
.stil{{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}}
.bildlink{{display:block;aspect-ratio:3864/2184;position:relative;background:#222}}
.bildlink iframe{{position:absolute;inset:0;width:100%;height:100%;border:0;pointer-events:none}}
.bildlink:hover{{outline:3px solid var(--acc);outline-offset:-3px}}
.txt{{padding:14px 18px 18px}} .txt h3{{margin:0 0 6px;font-size:21px}} .txt p{{margin:0 0 8px}}
.meta{{font-size:15px;color:var(--mut)}} .farben{{display:flex;gap:6px;margin:8px 0 10px}}
.farben i{{width:28px;height:28px;border-radius:50%;border:1px solid rgba(127,127,127,.4)}}
.gross{{color:var(--acc);font-weight:600;text-decoration:none}} .gross:hover{{text-decoration:underline}}
.sets{{display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:18px;margin-bottom:60px}}
.set{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 22px}}
.set h3{{margin:0 0 8px;font-size:18px}} .set h3 small{{color:var(--mut);font-weight:400}}
.set p{{margin:4px 0}} .m-titel{{font-size:36px;line-height:1.15}} .m-akzent{{font-size:30px;font-style:italic;color:var(--acc)}}
.m-lesen{{font-size:21px;font-style:italic}} .m-ui{{font-size:18px}} .sl{{font-size:14px;color:var(--mut);margin-top:10px!important}}
@media (max-width:520px){{.raster,.sets{{grid-template-columns:1fr}} h1{{font-size:34px}}}}
</style></head><body>
<header><h1>Quality Point – Stile und Schriftsets</h1>
<p>{n} Stile für 1920×1080-Folien. Jede Vorschau zeigt Titel-, Kapitel-, Zitat- und Kennzahlfolie im jeweiligen Stil;
ein Klick öffnet alle acht Musterfolien groß. Darunter die {m} Schriftsets – jedes Set lässt sich mit jedem Stil kombinieren.
Alle Schriften liegen lokal (SIL Open Font License 1.1).</p></header>
<main><h2>Stile</h2><div class="raster">
{karten}
</div>
<h2>Schriftsets</h2><div class="sets">
{zeilen}
</div></main></body></html>
'''


def browser():
    for b in BROWSER:
        if Path(b).exists():
            return b
    return shutil.which("msedge") or shutil.which("chromium") or shutil.which("google-chrome")


def bilder(stile):
    from PIL import Image
    exe = browser()
    if not exe:
        sys.exit("Kein Edge/Chrome gefunden – Vorschaubilder übersprungen.")
    tmp = Path(tempfile.mkdtemp())
    for c in stile:
        if not (STYLES / c["id"] / "stil.css").exists():
            print(c["id"], "– stil.css fehlt, kein Bild"); continue
        png = tmp / f"{c['id']}.png"
        url = (VS / f"{c['id']}.html").as_uri() + "#mini"
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--window-size=1944,1092", "--virtual-time-budget=6000", f"--screenshot={png}", url],
                       check=False, capture_output=True, timeout=120)
        if png.exists():
            im = Image.open(png).convert("RGB")
            im.thumbnail((1600, 1600))
            im.save(STYLES / c["id"] / "vorschau.webp", "WEBP", quality=82, method=6)
            print(c["id"], "vorschau.webp", im.size)
        else:
            print(c["id"], "FEHLER beim Bildschirmfoto")


if __name__ == "__main__":
    stile = seiten()
    if "--bilder" in sys.argv:
        bilder(stile)
