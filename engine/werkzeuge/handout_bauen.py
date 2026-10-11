"""Handout als PDF (A4) im Design der Präsentation.

Aufruf:  python <quality_point>/engine/werkzeuge/handout_bauen.py <projektordner> [--html]

Liest   <projekt>/src/handout.json        Inhalt (Aufbau siehe unten), von Claude aus Folien, Notizen und Artikel verfasst
        <projekt>/src/quellen.json        Literaturliste (alle Quellen der Folien, automatisch angehängt)
        <projekt>/praesentation.html      Design: Schriften (@font-face) und Farb-/Schrift-Tokens aus :root
Schreibt <projekt>/handout/<datei>.pdf    (dazu handout.html und verkleinerte Bilder in handout/_bilder/)
PDF-Druck über headless Edge/Chrome – keine Zusatzpakete außer Pillow, keine Aufrufe ins Netz.
Mit --html wird nur die HTML-Seite gebaut (zum Ansehen im Browser).

handout.json:
{
  "titel", "untertitel", "autor", "veranstaltung", "datum",   Titelseite
  "titelbild": "img/…",                                         optional
  "datei": "Handout_Thema_2026",                                optional, sonst aus dem Titel
  "url", "url_hinweis", "zugang_hinweis",                       QR-Code mit Hinweis (Titelseite, Kernaussagen, Fußzeile)
  "these": "…",                                                 zentrale These (große Box)
  "kernaussagen": ["…"],                                        6–8 Einsichten
  "kapitel": [{ "kick", "titel", "kern",                        Kernaussage des Kapitels
                "absaetze": ["… <b>…</b> …"],
                "kaesten": [{"art": "beispiel|merke|praxis", "titel", "html"}],
                "bilder": [{"datei": "img/…", "unterschrift", "quelle"}],
                "fragen": ["…"],                                 „Fragestellungen für die eigene Kompetenzentwicklung“
                "neue_seite": true }],
  "literatur": true                                             false = ohne Literaturliste
}
Regeln wie bei den Folien: nichts erfinden, Zahlen mit Bezugsgruppe, englische Zitate mit Übersetzung,
Bis-Strich mit Leerzeichen. Bildzitate (Zitatrecht) → PDF nur hinter Zugangsschutz veröffentlichen.
"""
import html, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

BROWSER = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
           r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
           r"C:\Program Files\Google\Chrome\Application\chrome.exe",
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
           "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
           "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"]
QR_JS = [Path(__file__).resolve().parent.parent / "src" / "vendor" / "qrcode.js"]
FRAGEN = "Fragestellungen für die eigene Kompetenzentwicklung"
e = html.escape


def browser():
    for b in BROWSER:
        if Path(b).exists():
            return b
    return shutil.which("msedge") or shutil.which("chromium") or shutil.which("google-chrome")


def design(prj):
    """@font-face-Regeln und :root-Tokens (nur oberste Ebene, nicht in @media) aus dem Haupt-<style>."""
    p = prj / "praesentation.html"
    if not p.exists():
        return "", ""
    t = p.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", t, flags=re.S)
    css = m.group(1) if m else ""
    fonts, roots, tiefe, i = [], [], 0, 0
    while i < len(css):
        if tiefe == 0 and css.startswith("@font-face", i) or tiefe == 0 and re.match(r":root\s*\{", css[i:i + 12]):
            j = css.index("}", i) + 1
            (fonts if css[i] == "@" else roots).append(css[i:j]); i = j; continue
        tiefe += css[i] == "{"; tiefe -= css[i] == "}"; i += 1
    fonts = [re.sub(r"url\((['\"]?)(?!data:|https?:|/)", r"url(\1../", f) for f in fonts]   # Pfade relativ zu handout/
    return "\n".join(fonts), "\n".join(roots)


def bild(prj, ziel, datei, breite=1400):
    """Verkleinerte JPEG-Kopie in handout/_bilder/ (spart PDF-Größe); SVG unverändert."""
    q = prj / datei
    if not q.exists():
        print("WARNUNG: Bild fehlt", datei); return ""
    if q.suffix.lower() == ".svg":
        return "../" + datei
    from PIL import Image
    z = ziel / "_bilder" / (re.sub(r"[^\w.-]", "_", datei).rsplit(".", 1)[0] + ".jpg")
    if not z.exists() or z.stat().st_mtime < q.stat().st_mtime:
        z.parent.mkdir(exist_ok=True)
        im = Image.open(q)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA"); grund = Image.new("RGB", im.size, "white"); grund.paste(im, mask=im.split()[-1]); im = grund
        im = im.convert("RGB"); im.thumbnail((breite, breite)); im.save(z, "JPEG", quality=80, optimize=True)
    return "_bilder/" + z.name


def literatur(prj):
    p = prj / "src" / "quellen.json"
    if not p.exists():
        return []
    Q = json.loads(p.read_text(encoding="utf-8"))
    Q.sort(key=lambda x: re.sub(r"^[^A-Za-zÄÖÜäöü]+", "", x.get("text") or x.get("html", "")).lower())
    out = []
    for x in Q:
        u = x.get("url") or (("https://doi.org/" + x["doi"]) if x.get("doi") else "")
        k = re.sub(r"^https?://(www\.)?", "", u)
        k = k[:62] + "…" if len(k) > 64 else k
        a = ' <a href="%s">%s</a>' % (e(u), e(k)) if u else ""
        out.append("<li>%s%s</li>" % (x.get("html") or e(x.get("text", "")), a))
    return out


def kurz_url(u):
    return re.sub(r"^https?://(www\.)?", "", u or "").rstrip("/")


def liste(eintraege, tag="li"):
    return "".join("<%s>%s</%s>" % (tag, x, tag) for x in eintraege)


def seiten(prj, ziel, H):
    qr = ""
    if H.get("url"):
        zg = "<br>" + e(H["zugang_hinweis"]) if H.get("zugang_hinweis") else ""
        qr = ('<div class="qr"><div class="qrbild" data-url="%s"></div><div><b>%s</b><br><span class="url">%s</span>%s</div></div>'
              % (e(H["url"]), e(H.get("url_hinweis", "")), e(kurz_url(H["url"])), zg))
    tb = bild(prj, ziel, H["titelbild"], 1800) if H.get("titelbild") else ""
    tbild = '<img class="tbild" src="%s" alt="">' % tb if tb else ""
    sub = '<p class="tsub">%s</p>' % e(H["untertitel"]) if H.get("untertitel") else ""
    datum = " · " + e(H["datum"]) if H.get("datum") else ""
    P = ['<section class="titel">%s<div class="tkick">%s</div><h1>%s</h1>%s<p class="twer"><b>%s</b>%s</p>%s</section>'
         % (tbild, e(H.get("veranstaltung", "")), e(H["titel"]), sub, e(H.get("autor", "")), datum, qr)]
    inhalt = "".join('<li><span>%s</span>%s</li>' % (e(k.get("kick", "")), re.sub(r"<[^>]+>", "", k["titel"]))
                     for k in H["kapitel"] if "Fortsetzung" not in k.get("kick", ""))
    P.append('<section class="seite"><div class="kick">Auf einen Blick</div><h2>Die Kernaussagen</h2>'
             '<div class="these">%s</div><ol class="kerne">%s</ol><h3>Inhalt</h3><ol class="inhalt">%s</ol>%s</section>'
             % (H.get("these", ""), liste(H.get("kernaussagen", [])), inhalt, qr))
    for k in H["kapitel"]:
        b = [x for x in k.get("bilder", []) if x.get("datei")]
        figs = ""
        for x in b:
            ql = ' <span class="quelle">%s</span>' % x["quelle"] if x.get("quelle") else ""
            figs += '<figure><img src="%s" alt=""><figcaption>%s%s</figcaption></figure>' % (bild(prj, ziel, x["datei"]), x.get("unterschrift", ""), ql)
        kae = "".join('<div class="kasten %s"><b>%s</b>%s</div>' % (e(x.get("art", "merke")), x.get("titel", ""), x.get("html", ""))
                      for x in k.get("kaesten", []))
        fr = ('<div class="fragen"><div class="fk">%s</div><ol>%s</ol></div>' % (FRAGEN, liste(k["fragen"]))) if k.get("fragen") else ""
        kern = '<div class="kern"><span>Kernaussage</span>%s</div>' % k["kern"] if k.get("kern") else ""
        bilder = '<div class="bilder n%d">%s</div>' % (min(len(b), 3), figs) if b else ""
        P.append('<section class="seite%s"><div class="kick">%s</div><h2>%s</h2>%s<div class="text">%s</div>%s%s%s</section>'
                 % ("" if k.get("neue_seite", True) else " weiter", e(k.get("kick", "")), k["titel"], kern,
                    liste(k.get("absaetze", []), "p"), bilder, kae, fr))
    if H.get("literatur", True):
        L = literatur(prj)
        if L:
            P.append('<section class="seite"><div class="kick">Anhang</div><h2>Literatur und Quellen</h2>'
                     '<p class="lhin">Alle %d Quellen der Präsentation, alphabetisch.</p><ol class="lit">%s</ol></section>' % (len(L), "".join(L)))
    return P


CSS = r"""
@page{size:A4;margin:16mm 17mm 20mm;
  @bottom-left{content:var(--fuss);font:8.5pt var(--ui);color:#666}
  @bottom-right{content:counter(page);font:600 9pt var(--ui);color:#666}}
@page:first{@bottom-left{content:none}@bottom-right{content:none}}
:root{--fuss:""}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;background:#fff;color:var(--ink,#1E1E1E);font:10.5pt/1.5 var(--ui,"Segoe UI",system-ui,sans-serif)}
h1,h2,h3{font-family:var(--serif,Georgia,serif);font-weight:400;line-height:1.15;text-wrap:balance;margin:0}
h1{font-size:34pt} h2{font-size:22pt;margin:2mm 0 4mm} h3{font-size:14pt;margin:7mm 0 2mm}
em{font-family:var(--accent,inherit);color:var(--red,#B23A2A)}
a{color:var(--teal,#1F5F5B);text-decoration:none;word-break:break-all}
b{font-weight:700}
.kick,.tkick{font:700 8.5pt var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--red,#B23A2A)}
.titel{break-after:page;min-height:255mm;display:flex;flex-direction:column;gap:4mm}
.tbild{width:100%;height:105mm;object-fit:cover;border-radius:3mm;margin-bottom:6mm}
.tsub{font:italic 15pt/1.35 var(--lesen,Georgia,serif);margin:0;color:var(--ink2,#444)}
.twer{margin:2mm 0 0;font-size:11pt}
.titel .qr{margin-top:auto}
.seite{break-before:page} .seite.weiter{break-before:auto;margin-top:8mm}
.these{background:var(--red,#B23A2A);color:#fff;font:400 17pt/1.3 var(--serif);padding:6mm 7mm;border-radius:2.5mm;margin:2mm 0 5mm}
.these b,.these em{color:#fff}
.kerne{margin:0;padding-left:6mm;font-size:11.5pt} .kerne li{margin:0 0 2.2mm;padding-left:1mm}
.kerne li::marker{font:700 11pt var(--ui);color:var(--red,#B23A2A)}
.inhalt{list-style:none;padding:0;margin:0;columns:2;column-gap:8mm;font-size:10.5pt}
.inhalt li{break-inside:avoid;margin:0 0 1.5mm} .inhalt span{display:inline-block;min-width:16mm;font-weight:700;color:var(--teal,#1F5F5B)}
.qr{display:flex;gap:5mm;align-items:center;border:.4mm solid var(--line,#CFC6B4);border-radius:2.5mm;padding:4mm 5mm;margin-top:6mm;break-inside:avoid;font-size:10pt}
.qrbild{width:28mm;height:28mm;flex:none} .qrbild svg{width:100%;height:100%}
.url{font:600 11pt var(--ui);color:var(--teal,#1F5F5B)}
.kern{background:var(--teal,#1F5F5B);color:#fff;font:400 13pt/1.35 var(--serif);padding:4mm 5mm;border-radius:2mm;margin:0 0 5mm;break-inside:avoid}
.kern span{display:block;font:700 7.5pt var(--ui);letter-spacing:.14em;text-transform:uppercase;opacity:.85;margin-bottom:1mm}
.kern b,.kern em{color:#fff}
.text p{margin:0 0 3mm;text-align:left;hyphens:auto}
.bilder{display:grid;gap:4mm;margin:2mm 0 4mm;break-inside:avoid} .bilder.n2{grid-template-columns:1fr 1fr} .bilder.n3{grid-template-columns:1fr 1fr 1fr}
.bilder figure{margin:0;break-inside:avoid} .bilder img{width:100%;max-height:78mm;object-fit:contain;background:#F4F1EA;border-radius:1.5mm;display:block}
.bilder.n1 img{max-height:95mm}
figcaption{font-size:8.5pt;line-height:1.35;color:#555;margin-top:1.5mm} .quelle{color:#888}
.kasten{border-left:1.6mm solid var(--yellow,#D9A441);background:#FAF6EC;padding:3mm 4mm;margin:0 0 4mm;break-inside:avoid;font-size:10pt}
.kasten.praxis{border-color:var(--teal,#1F5F5B);background:#EEF4F2} .kasten.beispiel{border-color:var(--red,#B23A2A);background:#FBEFEC}
.kasten b:first-child{display:block;font:700 10.5pt var(--ui);margin-bottom:1mm}
.kasten ul,.kasten ol{margin:1mm 0 0;padding-left:5mm}
.fragen{border:.5mm solid var(--ink,#222);border-radius:2mm;padding:3.5mm 5mm;margin:5mm 0 0;break-inside:avoid;font-size:10pt}
.fk{font:700 8pt var(--ui);letter-spacing:.12em;text-transform:uppercase;margin-bottom:1.5mm;color:var(--red,#B23A2A)}
.fragen ol{margin:0;padding-left:5mm} .fragen li{margin:0 0 1.2mm}
.lhin{margin:0 0 3mm;color:#555}
.lit{columns:2;column-gap:7mm;font-size:7.6pt;line-height:1.35;padding-left:5mm;margin:0}
.lit li{break-inside:avoid;margin:0 0 1.3mm}
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prj = Path(args[0] if args else ".").resolve()
    H = json.loads((prj / "src" / "handout.json").read_text(encoding="utf-8"))
    ziel = prj / "handout"; ziel.mkdir(exist_ok=True)
    fonts, roots = design(prj)
    qr = next((p for p in QR_JS + [prj / "src" / "vendor" / "qrcode.js"] if p.exists()), None)
    fuss = " · ".join(x for x in (H.get("titel"), H.get("autor"), kurz_url(H.get("url"))) if x)
    qr_js = qr.read_text(encoding="utf-8") if qr else ""
    stil = "\n".join([fonts, roots, CSS, ':root{--fuss:"%s"}' % fuss.replace('"', "'")])
    doc = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>%s – Handout</title><style>%s</style></head><body>\n%s\n'
           '<script>%s</script>\n<script>document.querySelectorAll(".qrbild").forEach(function(d){if(typeof qrcode!=="function")return;'
           'var q=qrcode(0,"M");q.addData(d.dataset.url);q.make();d.innerHTML=q.createSvgTag({cellSize:4,margin:0,scalable:true});});</script>\n'
           '</body></html>') % (e(H["titel"]), stil, "".join(seiten(prj, ziel, H)), qr_js)
    seite = ziel / "handout.html"
    seite.write_text(doc, encoding="utf-8")
    if "--html" in sys.argv:
        print("HTML:", seite); return
    exe = browser()
    if not exe:
        sys.exit("Kein Edge/Chrome gefunden – nur handout.html gebaut.")
    name = H.get("datei") or "Handout_" + re.sub(r"\W+", "_", H["titel"]).strip("_")
    pdf = ziel / f"{name}.pdf"
    with tempfile.TemporaryDirectory() as prof:
        subprocess.run([exe, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}", "--no-pdf-header-footer",
                        "--virtual-time-budget=20000", f"--print-to-pdf={pdf}", seite.as_uri()],
                       check=False, capture_output=True, timeout=300)
    if not pdf.exists():
        sys.exit("FEHLER: PDF wurde nicht erzeugt.")
    n = len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))
    print(f"{pdf.name}: {n} Seiten, {pdf.stat().st_size / 1e6:.1f} MB -> {pdf}")


if __name__ == "__main__":
    main()
