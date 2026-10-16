# Baut die Begleitseiten in den Projektordner (deploy.py kopiert sie danach):
#   index.html     – Startseite (Einheiten aus quality_point.json, Materialien, Kacheln)
#   glossar.html   – alle Begriffe aus src/glossar*.txt
#   quellen.html   – Kopie aus dem Artikelprojekt (falls „artikel“ gesetzt), sonst aus src/quellen.json
#   artikel.html   – optional: bereinigte Kopie von <artikel>/standalone.html
#   lehrplan.html  – optional („lehrplan.an“): aus daten/lehrplan.json (Schema: engine/FOLIEN.md)
# Aufruf: python engine/werkzeuge/seiten_bauen.py <projekt>   (nach build.py)
import os, re, sys, json, glob, html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import konfig
E = lambda t: html.escape(str(t), quote=True)


def main(K):
    os.chdir(K['_projekt']); T = konfig.T(K)
    rd = lambda p: open(p, encoding='utf-8').read()
    praes = rd(K['ausgabe']) if os.path.exists(K['ausgabe']) else ''
    if not praes: print('Hinweis: erst build.py ausführen')
    titel = [html.unescape(t) for t in re.findall(r'<section class="slide[^"]*"[^>]*data-title="([^"]*)"', praes)]
    folie = lambda t: titel.index(t) + 1 if t in titel else 1
    aus = K['materialien'].get('ausgabe', 'formulare')
    mat = json.load(open(os.path.join(aus, 'materialien.json'), encoding='utf-8')) if K['materialien'].get('an') and os.path.exists(os.path.join(aus, 'materialien.json')) else []
    hat_art, hat_lp = bool(K['_artikel']), bool(K['lehrplan'].get('an'))

    # Glossar
    GL = []
    for p in sorted(glob.glob('src/glossar*.txt')):
        for block in re.split(r'\n\s*\n', rd(p)):
            lines = [l for l in block.strip().split('\n') if l.strip() and not l.startswith('#')]
            if not lines or lines[0].startswith(('E:', 'Q:')): continue      # Begriff ohne „|“ ist erlaubt
            d = {'t': lines[0].split('|')[0].strip(), 'e': ''}
            for l in lines[1:]:
                if l.startswith('E:'): d['e'] = l[2:].strip()
            GL.append(d)
    GL.sort(key=lambda d: d['t'].lower().replace('ä', 'a').replace('ö', 'o').replace('ü', 'u'))

    # CSS: Tokens aus basis.css und Stil, dann seiten.css, dann optional styles/<stil>/seiten.css
    roots = lambda t: '\n'.join(re.findall(r':root\s*\{[^}]*\}', re.sub(r'/\*.*?\*/', '', t, flags=re.S)))
    CSS = roots(rd(os.path.join(K['_engine'], 'src', 'basis.css')))
    sc = os.path.join(K['_stil'], 'stil.css')
    if os.path.exists(sc): CSS += '\n' + roots(rd(sc))
    CSS += '\n' + rd(os.path.join(K['_engine'], 'src', 'seiten.css'))
    ss = os.path.join(K['_stil'], 'seiten.css')
    if os.path.exists(ss): CSS += '\n' + rd(ss)
    FONTS = '<link rel="stylesheet" href="fonts/fonts.css">' if os.path.exists('fonts/fonts.css') else ''
    JAHR = '<span class="js-year">2026</span>'
    JS_JAHR = '<script>document.querySelectorAll(".js-year").forEach(function(e){e.textContent=new Date().getFullYear()});</script>'
    nav = [('index.html', T['start']), (K['ausgabe'], T['praes'])]
    if hat_art: nav.append(('artikel.html', T['artikel']))
    nav += [('quellen.html', T['quellen']), ('glossar.html', T['glossar'])]
    if hat_lp: nav.append(('lehrplan.html', T['lehrplan']))
    if mat: nav.append(('index.html#materialien', T['materialien']))
    NAV = '<nav>' + ''.join(f'<a href="{h}">{E(t)}</a>' for h, t in nav) + '</nav>'
    BIS = re.compile(r'(\d)\s*–\s*(\d)')
    fuss = ' · '.join(E(x) for x in (K['autor'], K['institution'], K['veranstaltung']) if x)

    def seite(datei, title, body, desc=''):
        if K['bis_leerzeichen']: body = BIS.sub(lambda m: m.group(1) + ' – ' + m.group(2), body)
        open(datei, 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="{E(K['sprache'])}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">{FONTS}<style>{CSS}</style></head>
<body>{body}
<footer class="wrap"><span>{fuss}{' · ' if fuss else ''}{JAHR}</span>{f'<span>{E(K["fusszeile"])}</span>' if K['fusszeile'] else ''}<span>{E(T['erstellt'])}</span></footer>
{JS_JAHR}</body></html>''')

    def kopf(kick, h):
        return f'<header class="wrap top"><a class="home" href="index.html">{E(K["titel"])}</a>{NAV}</header><main class="wrap"><section><div class="kick">{E(kick)}</div><h2>{h}</h2>'

    # ---------- index.html ----------
    def karte(m):
        fa = ''.join(f'<span class="chip s">{E(f)}</span>' for f in m.get('faecher', [])[:3])
        return (f'<a class="mat" href="{aus}/{E(m["datei"])}" download><b>{E(m["titel"])}</b><span>{E(m.get("kurz",""))}</span>'
                f'<div class="chips"><span class="chip d">{E(m.get("stufe",""))}</span>{fa}<span class="chip">{E(m.get("zeit",""))}</span></div></a>')
    EH = K['einheiten']
    mat_html = ''
    if mat:
        for e in EH:
            ms = [m for m in mat if m.get('einheit') == e.get('kurz')]
            if ms: mat_html += f'<div class="matgruppe"><h3 id="mat-{E(e["kurz"])}"><small>{E(e["kurz"])}</small>{E(e.get("name",""))}</h3><div class="mats">' + ''.join(karte(m) for m in ms) + '</div></div>'
        rest = [m for m in mat if m.get('einheit') not in [e.get('kurz') for e in EH]]
        if rest: mat_html += f'<div class="matgruppe"><h3>{E(T["weitere"] if EH else T["materialien"])}</h3><div class="mats">' + ''.join(karte(m) for m in rest) + '</div></div>'
    units = ''
    for i, e in enumerate(EH, 1):
        n = folie(e.get('folie', '')); anz = sum(1 for m in mat if m.get('einheit') == e.get('kurz'))
        bild = f'<img src="{E(e["bild"])}" alt="" loading="lazy">' if e.get('bild') and os.path.exists(e['bild']) else ''
        units += (f'<article class="unit">{bild}<div class="in"><span class="nr">{E(T["einheit"])} {i}{(" · " + E(e["kurz"])) if e.get("kurz") else ""}</span>'
                  f'<h3>{E(e.get("name",""))}</h3><p>{E(e.get("text",""))}</p><div class="act"><a href="{K["ausgabe"]}#{n}">{E(T["folien_ab"])} {n}</a>'
                  + (f'<a href="#mat-{E(e["kurz"])}">{anz} {T["material1"] if anz == 1 else T["materialn"]}</a>' if anz else '') + '</div></div></article>')
    tb = K['titelbild'] if K['titelbild'] and os.path.exists(K['titelbild']) else ''
    kick = ' · '.join(x for x in (K['veranstaltung'], K['institution']) if x)
    tiles = ''
    if hat_art: tiles += f'<a class="tile" href="artikel.html"><b>{E(T["artikel"])}</b><span>{E(T["artikel_t"])}</span></a>'
    if hat_lp: tiles += f'<a class="tile" href="lehrplan.html"><b>{E(T["lehrplan"])}</b><span>{E(T["lehrplan_t"])}</span></a>'
    tiles += f'<a class="tile" href="glossar.html"><b>{E(T["glossar"])}</b><span>{len(GL)} · {E(T["glossar_t"])}</span></a>'
    tiles += f'<a class="tile" href="quellen.html"><b>{E(T["quellen"])}</b><span>{E(T["quellen_t"])}</span></a>'
    body = f'''<header class="wrap hero{'' if tb else ' ohne-bild'}">
  <div>{f'<div class="kick">{E(kick)}</div>' if kick else ''}
  <h1>{E(K["titel"])}</h1>
  {f'<p class="lead" style="margin-top:1rem">{E(K["untertitel"])}</p>' if K['untertitel'] else ''}
  <div class="btns"><a class="btn p" href="{K["ausgabe"]}">{E(T["praes_start"])}</a>{f'<a class="btn" href="artikel.html">{E(T["artikel_lesen"])}</a>' if hat_art else ''}{f'<a class="btn" href="#materialien">{E(T["materialien"])}</a>' if mat else ''}</div>
  <p class="meta">{len(titel)} {E(T["folien"])}{f" · {len(mat)} {E(T['material1'] if len(mat) == 1 else T['materialn'])}" if mat else ''} · {len(GL)} {E(T["begriffe"])} · {E(T["stand"])} {JAHR}</p></div>
  {f'<div class="bild tape"><img src="{E(tb)}" alt=""></div>' if tb else ''}
</header>
<main>
{f'<section class="wrap" id="einheiten"><div class="kick">{E(T["einheiten"])}</div><h2>{E(T["einheiten"])}</h2><div class="units">{units}</div></section>' if units else ''}
{f'<section class="wrap" id="materialien"><div class="kick">{E(T["mat_kick"])}</div><h2>{T["mat_h"]}</h2><p class="lead">{E(T["mat_lead"])}</p>{mat_html}</section>' if mat else ''}
<section class="wrap"><div class="kick">{E(T["nachlesen"])}</div><h2>{T["grundlage"]}</h2><div class="tiles">{tiles}</div></section>
</main>'''
    seite('index.html', K['titel'], body, K['untertitel'])

    # ---------- glossar.html ----------
    dl = ''.join(f'<dt id="g-{i}">{E(g["t"])}</dt><dd>{E(g["e"])}</dd>' for i, g in enumerate(GL))
    body = (kopf(T['glossar'], f'{len(GL)} <em>{E(T["fachbegriffe"])}</em>') + f'<p class="lead">{E(T["gl_lead"])}</p>'
            f'<input class="suche" id="q" type="search" placeholder="{E(T["gl_suche"])}" aria-label="{E(T["gl_suche"])}"><dl class="gl" id="gl">{dl}</dl></section></main>'
            '<script>document.getElementById("q").addEventListener("input",function(){var q=this.value.toLowerCase();document.querySelectorAll("#gl dt").forEach(function(dt){var dd=dt.nextElementSibling;var hit=(dt.textContent+" "+dd.textContent).toLowerCase().indexOf(q)>=0;dt.hidden=!hit;dd.hidden=!hit;});});</script>')
    seite('glossar.html', f'{T["glossar"]} · {K["titel"]}', body)

    # ---------- lehrplan.html (optional) ----------
    if hat_lp:
        lpd = K['lehrplan'].get('datei', 'daten/lehrplan.json')
        lp = json.load(open(lpd, encoding='utf-8')) if os.path.exists(lpd) else None
        if not lp: print('WARNUNG: Lehrplan eingeschaltet, aber', lpd, 'fehlt')
        else:
            def zit(x):
                if isinstance(x, str): return f'<div class="fax"><div>{E(x)}</div></div>'
                fs = ' · '.join(E(v) for v in [x.get('fundstelle'), ('S. ' + str(x['seite'])) if x.get('seite') else None] if v)
                ver = x.get('verifiziert')
                vk = '' if ver is None else (f' <span class="ok">{E(T["geprueft"])}</span>' if ver else f' <span class="nok">{E(T["ungeprueft"])}</span>')
                return f'<div class="fax"><div class="fh">{fs}{vk}</div><div>{E(x.get("text",""))}</div></div>'
            teile = []
            for k, a in enumerate(lp.get('abschnitte', [])):
                t = f'<h3 style="margin-top:2rem">{E(a.get("titel",""))}</h3>' + (f'<p>{E(a["text"])}</p>' if a.get('text') else '') + ''.join(zit(x) for x in a.get('zitate', []))
                tab = a.get('tabelle')
                if tab:
                    fsp = tab.get('filter_spalte')
                    rows = ''.join(f'<tr data-f="{E(z[fsp]) if fsp is not None else ""}">' + ''.join(f'<td>{E(c)}</td>' for c in z) + '</tr>' for z in tab.get('zeilen', []))
                    if fsp is not None:
                        opts = ''.join(f'<option>{E(v)}</option>' for v in sorted({z[fsp] for z in tab.get('zeilen', [])}))
                        t += (f'<select class="suche" id="ff{k}" style="max-width:280px;margin:.6rem 0"><option value="">{E(T["alle"])}</option>{opts}</select>'
                              f'<script>document.addEventListener("DOMContentLoaded",function(){{var s=document.getElementById("ff{k}");s.onchange=function(){{document.querySelectorAll("#lpt{k} tr[data-f]").forEach(function(r){{r.hidden=!!s.value&&r.dataset.f!==s.value;}});}};}});</script>')
                    t += f'<div class="tbl-wrap"><table class="lp" id="lpt{k}"><tr>' + ''.join(f'<th>{E(s)}</th>' for s in tab.get('spalten', [])) + f'</tr>{rows}</table></div>'
                teile.append(t)
            qu = ''.join(f'<li><a href="{E(q.get("url",""))}" target="_blank" rel="noopener">{E(q.get("titel",""))}</a>' + (f' · {E(T["abgerufen"])} {E(q["abgerufen"])}' if q.get('abgerufen') else '') + '</li>' for q in lp.get('quellen', []))
            body = (kopf(lp.get('kick', T['lehrplan']), E(lp.get('titel', T['lehrplan']))) + (f'<p class="lead">{E(lp["einleitung"])}</p>' if lp.get('einleitung') else '')
                    + ''.join(teile) + (f'<h3 style="margin-top:2rem">{E(T["primaer"])}</h3><ul>{qu}</ul>' if qu else '') + '</section></main>')
            seite('lehrplan.html', f'{lp.get("titel", T["lehrplan"])} · {K["titel"]}', body)

    # ---------- artikel.html / quellen.html ----------
    ART = K['_artikel']
    if ART:
        a = rd(os.path.join(ART, 'standalone.html'))
        a = re.sub(r'<script>\s*window\._WEB_PAKET_TEXT=.*?</script>', '', a, flags=re.S)                          # eingebettetes Alt-Paket
        if not re.search(r'class="katex|\$\$|\\\(', a):
            a = re.sub(r'<link[^>]*katex[^>]*>\s*|<script[^>]*katex.*?</script>\s*', '', a, flags=re.S)          # KaTeX (CDN) nur ohne Formeln entfernen
        a = re.sub(r'/\* ── Web-Paket \(ZIP\) ── \*/.*?(?=\n\}\)\(\);</script>)', '', a, flags=re.S)             # ZIP-Export (lädt JSZip vom CDN)
        a = a.replace('id="exp-tab-web" style="', 'id="exp-tab-web" hidden style="display:none;')
        a = re.sub(r'(<div id="exp-panel-web" style="display:none">).*?(<button onclick="webPaketDownload\(\)"[^>]*>.*?</button>)\s*', r'\1', a, flags=re.S)
        a = a.replace('href="presentation/index.html"', f'href="{K["ausgabe"]}"').replace('href="HIER-LINK-EINFÜGEN"', 'href="index.html"')
        if 'webPaketDownload' in a: print('WARNUNG: Web-Paket-Reste im Artikel')
        open('artikel.html', 'w', encoding='utf-8').write(a)
        q = rd(os.path.join(ART, 'quellen.html')).replace('standalone.html', 'artikel.html')
        open('quellen.html', 'w', encoding='utf-8').write(q)
    else:
        refs = json.load(open('src/quellen.json', encoding='utf-8')) if os.path.exists('src/quellen.json') else []
        li = ''.join(f'<li id="q-{E(r["id"])}" data-t="{E(r.get("text","").lower())}">{r["html"]} <a href="{E(r["url"])}" target="_blank" rel="noopener">↗</a></li>' for r in refs)
        body = (kopf(T['quellen'], f'{len(refs)} <em>{E(T["werke"])}</em>') + f'<p class="lead">{E(T["q_lead"])}</p>'
                f'<input class="suche" id="q" type="search" placeholder="{E(T["q_suche"])}" aria-label="{E(T["q_suche"])}"><ol class="qv" id="qv">{li}</ol></section></main>'
                '<script>document.getElementById("q").addEventListener("input",function(){var q=this.value.toLowerCase();document.querySelectorAll("#qv li").forEach(function(l){l.hidden=l.dataset.t.indexOf(q)<0;});});</script>')
        seite('quellen.html', f'{T["quellen"]} · {K["titel"]}', body)
    print(f'Seiten: {", ".join(konfig.seiten(K))} ({len(GL)} Glossarbegriffe, {len(mat)} Materialien)')


if __name__ == '__main__':
    main(konfig.lade())
