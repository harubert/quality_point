# Baut <projekt>/praesentation.html aus den Projektdateien (src/slides, Snippets, Pointen, Glossar, Quellen)
# und der Engine (Hülle, basis.css, interaktion.*, engine.js) im gewählten Stil.
# Aufruf:  python engine/build.py <projektordner>      Markup: engine/FOLIEN.md   Tokens: engine/TOKENS.md
import json, re, glob, os, sys, json, shutil, html as _h
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import konfig

K = konfig.lade()
ENG = K['_engine']
os.chdir(K['_projekt'])
AUSGABE = K['ausgabe']
# Stilprüfung im Folientext (Regex, Meldung) – an die eigenen Schreibregeln anpassen
PRUEF_MUSTER = [('—', 'Geviertstrich (nur „–“ verwenden)'), ('"', 'gerades Anführungszeichen im Text')]

rd = lambda p: open(p, encoding='utf-8').read()
er = lambda *t: os.path.join(ENG, *t)

# 0. Quellen: Verzeichnis aus Artikel + quellen_extra*.json (erzeugt src/quellen.json und src/slides/95_quellen.html)
if '--ohne-quellen' not in sys.argv:
    sys.path.insert(0, er('werkzeuge'))
    import quellen_bauen
    quellen_bauen.main(K)

parts = sorted(glob.glob('src/slides/*.html'))
if not parts: sys.exit('Keine Folien in src/slides/*.html')
slides = '\n'.join(rd(p) for p in parts)

# 1. Snippets: {{name}} -> src/snippets/name.svg
snips = {os.path.splitext(os.path.basename(p))[0]: rd(p) for p in glob.glob('src/snippets/*.svg')}
slides = re.sub(r'\{\{(\w+)\}\}', lambda m: snips.get(m.group(1), m.group(0)), slides)

# 1a. Einzufügende Folien (src/einfuegen_*.html.txt, src/unterricht_folien.html.txt) hinter die Folie mit data-title = data-nach
for _ef in sorted(glob.glob('src/einfuegen_*.html.txt')) + glob.glob('src/unterricht_folien.html.txt'):
    for uf in reversed(re.findall(r'<section class="slide[^"]*"[^>]*data-nach=.*?</section>', rd(_ef), flags=re.S)):
        nach = _h.unescape(re.search(r'data-nach="([^"]*)"', uf).group(1))
        m = re.search(r'<section class="slide[^"]*"[^>]*data-title="' + re.escape(_h.escape(nach, quote=True)) + r'"[^>]*>.*?</section>', slides, flags=re.S) \
            or re.search(r'<section class="slide[^"]*"[^>]*data-title="' + re.escape(nach) + r'"[^>]*>.*?</section>', slides, flags=re.S)
        if not m: print('WARNUNG eingefügte Folie ohne Ankerfolie:', nach); continue
        slides = slides[:m.end()] + '\n' + uf + slides[m.end():]

# 1b. Material-Links: <div class="matlinks" data-thema="x"></div> -> Downloads aus <ausgabe>/materialien.json
#     Zuordnung data-thema -> „thema“ der Materialien über quality_point.json „themen“; „alle“ = alle Materialien.
MAUS = K['materialien'].get('ausgabe', 'formulare')
MAT = json.load(open(os.path.join(MAUS, 'materialien.json'), encoding='utf-8')) if os.path.exists(os.path.join(MAUS, 'materialien.json')) else []
THEMEN = K['themen']
def _mat(m):
    thema, klassen = m.group(2), m.group(1)
    ms = MAT if thema == 'alle' else [x for x in MAT if x.get('thema') in THEMEN.get(thema, [thema])]
    if not ms: print('WARNUNG: keine Materialien für Thema', thema)
    if 'matgrid' in klassen:
        return ('<div class="matgrid">' + ''.join(
            f'<a class="mg" href="{MAUS}/{x["datei"]}" download><b>{_h.escape(x["titel"])}</b><span>{_h.escape(" · ".join(v for v in (x.get("einheit",""), x.get("stufe",""), x.get("zeit","").split(";")[0]) if v))}</span></a>'
            for x in ms) + '</div>')
    return '<div class="matlinks">' + ''.join(f'<a class="formlink" href="{MAUS}/{x["datei"]}" download>{_h.escape(x["titel"])}</a>' for x in ms) + '</div>'
slides = re.sub(r'<div class="(matlinks[^"]*)" data-thema="([\w-]+)"></div>', _mat, slides)

# 1c. Optional: Bis-Strich mit Leerzeichen „12–17“ -> „12 – 17“ und geschütztes Leerzeichen vor %.
_BIS = re.compile(r'(\d)\s*–\s*(\d)')
_PROZ = re.compile(r'(\d) (%|‰)')
def _bis(t):
    t = _PROZ.sub('\\1\u00a0\\2', t)
    return _BIS.sub('\\1\u00a0– \\2', t) if K['bis_leerzeichen'] else t
def _bis_slides(html):
    out = []
    for teil in re.split(r'(<style.*?</style>|<script.*?</script>|<ul class="ql">.*?</ul>|<[^>]+>)', html, flags=re.S):
        if not teil: continue
        if teil.startswith(('<style', '<script', '<ul class="ql">')): out.append(teil)
        elif teil.startswith('<'):
            out.append(re.sub(r'((?:data-cap|alt|title|data-zweck|data-pointe)=")([^"]*)(")', lambda m: m.group(1) + _bis(m.group(2)) + m.group(3), teil))
        else: out.append(_bis(teil))
    return ''.join(out)

# 2. Pointen: src/pointen*.txt -> data-zweck / data-pointe am <section>
pt = {}
_ptxt = '\n\n'.join(rd(p) for p in sorted(glob.glob('src/pointen*.txt')))
for block in re.split(r'\n\s*\n', _ptxt):
    lines = [l for l in block.strip().split('\n') if l and not l.startswith('#')]
    if not lines: continue
    d = {'t': lines[0].strip()}
    for l in lines[1:]:
        if l.startswith('Z:'): d['z'] = l[2:].strip()
        if l.startswith('P:'): d['p'] = l[2:].strip()
    pt[d['t']] = d
used = set()
def inj(m):
    tag, t = m.group(0), _h.unescape(m.group(1))
    d = pt.get(t)
    if not d: return tag
    used.add(t)
    if re.search(r'\sdata-(?:zweck|pointe)=', tag): return tag       # Merksatz direkt an der Folie gewinnt gegen pointen*.txt
    return tag[:-1] + f' data-zweck="{_h.escape(d.get("z",""))}" data-pointe="{_h.escape(d.get("p",""))}">'
slides = re.sub(r'<section class="slide[^>]*data-title="([^"]*)"[^>]*>', inj, slides)

# 3. Quellen verlinken, 4. Glossarbegriffe markieren
sys.path.insert(0, er('src')); import quellen_link, glossar_link
slides = quellen_link.process(slides)
slides, GLOSSAR = glossar_link.process(slides)
slides = _bis_slides(slides)

# 4b. Nummern: data-nr je Folie (Reihenfolge der Referentenfassung – die Teilnehmerfassung folgt darüber)
#     und data-id je Interaktionsbaustein (Antworten werden darunter gespeichert)
_zn = [0]
def _nr(m):
    if ' data-nr=' in m.group(0): return m.group(0)
    _zn[0] += 1; return m.group(0)[:-1] + f' data-nr="{_zn[0]}">'
slides = re.sub(r'<section class="slide[^"]*"[^>]*>', _nr, slides)
_zi = [0]
def _id(m):
    if ' data-id=' in m.group(0): return m.group(0)
    _zi[0] += 1; return m.group(0)[:-1] + f' data-id="ia{_zi[0]}">'
slides = re.sub(r'<div class="(?:[^"]* )?ia-[^"]*"[^>]*>', _id, slides)

# 5. Stil: Schriften aus dem Schriftset des Stils nach <projekt>/fonts/ kopieren, CSS zusammensetzen
#    Schriftset = Konfig „schriftset“ oder stil.json „schriftset“; Dateien liegen einmalig in styles/_schriftsets/fonts/
STIL = K['_stil']
_sj = os.path.join(STIL, 'stil.json')
SET = K.get('schriftset') or (json.load(open(_sj, encoding='utf-8')).get('schriftset') if os.path.exists(_sj) else '')
_SETS = os.path.join(os.path.dirname(STIL), '_schriftsets', 'fonts')
fcss = ''
if SET and os.path.exists(os.path.join(_SETS, SET + '.css')):
    roh = rd(os.path.join(_SETS, SET + '.css'))
    os.makedirs('fonts', exist_ok=True)
    for f in glob.glob('fonts/*'):
        if os.path.isfile(f): os.remove(f)
    for n in sorted(set(re.findall(r'url\(["\']?([^)"\']+\.woff2)', roh))):
        q = os.path.join(_SETS, os.path.basename(n))
        if os.path.exists(q): shutil.copy2(q, 'fonts')
    fcss = re.sub(r'url\((["\']?)(?![a-z]+:|/|fonts/)', r'url(\1fonts/', roh)   # relativ zum Projekt
    open('fonts/fonts.css', 'w', encoding='utf-8').write(roh)
else:
    print(f'Hinweis: Schriftset „{SET}“ nicht gefunden – Systemschriften (python styles/_werkzeuge/schriften_holen.py {SET or "<set>"})')
stil_css = rd(os.path.join(STIL, 'stil.css')) if os.path.exists(os.path.join(STIL, 'stil.css')) else ''
css = fcss + '\n' + rd(er('src', 'basis.css')) + '\n' + rd(er('src', 'interaktion.css')) + '\n' + stil_css
if os.path.exists('src/projekt.css'): css += '\n' + rd('src/projekt.css')   # projektspezifische Ergänzungen
LIVE = K['live'] if K['live'].get('an') else None
if LIVE: css += '\n' + rd(er('live', 'live.css'))

# 6. Zusammensetzen
data_js = ('const GLOSSAR=' + json.dumps(GLOSSAR, ensure_ascii=False) + ';\n'
           + 'const VIDEOINHALT=' + (rd('src/video_inhalte.json') if os.path.exists('src/video_inhalte.json') else '{}') + ';\n'
           + 'const QUELLEN=' + json.dumps({r['id']: {'url': r['url'], 'kind': r['kind']} for r in quellen_link.REFS}, ensure_ascii=False) + ';\n')
data_js = _bis(data_js)
js = data_js + rd(er('src', 'engine.js')) + '\n' + ''.join(rd(v) + '\n' for v in sorted(glob.glob(er('src', 'vendor', '*.js')))) + rd(er('src', 'interaktion.js'))
if LIVE: js += '\nconst QP_LIVE=' + json.dumps({'api': 'live/api.php', 'teilnehmer': LIVE['teilnehmer']}, ensure_ascii=False) + ';\n' + rd(er('live', 'live.js'))
shell = rd(er('src', 'shell.html')).replace('{{SPRACHE}}', _h.escape(K['sprache'])).replace('{{CSS}}', css).replace('{{JS}}', js)
out = shell.replace('{{TITEL}}', _h.escape(K['titel'])).replace('{{SLIDES}}', slides)
open(AUSGABE, 'w', encoding='utf-8').write(out)

# 6b. Teilnehmerfassung (Server-Modus): ohne Notizen, Pointen und Folien mit data-nur="referent";
#     Lösungen der Bausteine entfernt – sie kommen erst mit der Freigabe vom Server. Elemente mit Klasse nur-referent blendet CSS aus.
if LIVE:
    tn = re.sub(r'<section class="slide[^"]*"[^>]*data-nur="referent"[^>]*>.*?</section>\s*', '', slides, flags=re.S)
    tn = re.sub(r'\s*<aside class="notes">.*?</aside>', '', tn, flags=re.S)
    tn = re.sub(r'\s(?:data-zweck|data-pointe)="[^"]*"', '', tn)
    def _tn_ia(m):
        t = re.sub(r'\s(?:data-wert|data-loesung|data-richtig)="[^"]*"', '', m.group(0))
        if 'ia-quiz' in t: t = re.sub(r'\sdata-text="[^"]*"', '', t)
        return t
    tn = re.sub(r'<div class="(?:[^"]* )?ia-[^"]*"[^>]*>', _tn_ia, tn)
    tn = re.sub(r'(<[a-z0-9]+\b[^>]*?)\sdata-ziel="[^"]*"', r'\1 data-item=""', tn)
    out_tn = (shell.replace('{{TITEL}}', _h.escape(K['titel']) + ' · Mitmachen').replace('{{SLIDES}}', tn)
              .replace('<body>', '<body class="tn">', 1))
    open(LIVE['teilnehmer'], 'w', encoding='utf-8').write(out_tn)
    if re.search(r'data-wert=|data-loesung=|data-richtig=|data-ziel=|class="notes"|data-pointe=', tn): sys.exit('Teilnehmerfassung enthält noch Lösungen oder Notizen – Abbruch')

# ---- Prüfungen ----
secs = re.findall(r'<section class="slide.*?</section>', slides, flags=re.S)
print(f'{len(secs)} Folien aus {len(parts)} Dateien -> {AUSGABE} ({len(out)//1024} kB), Stil {K["stil"]}, {len(GLOSSAR)} Glossarbegriffe, {len(quellen_link.REFS)} Quellen'
      + (f'; Live: {LIVE["teilnehmer"]} ({_zi[0]} Bausteine)' if LIVE else ''))
left = re.findall(r'\{\{\w+\}\}', slides)
if left: print('FEHLENDE SNIPPETS:', set(left))
text_only = re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', '', slides, flags=re.S))
for pat, msg in PRUEF_MUSTER:
    hits = [m.start() for m in re.finditer(pat, text_only)]
    if hits:
        print(f'WARNUNG {msg}: {len(hits)}x')
        for h in hits[:6]: print('   …' + text_only[max(0, h-50):h+30].replace('\n', ' ') + '…')
miss = [i+1 for i, s in enumerate(secs) if 'class="notes"' not in s]
if miss: print('Folien ohne Notizen:', miss)
nz = [i+1 for i, s in enumerate(secs) if 'data-zweck=' not in s]
if nz: print('Folien ohne Eintrag in pointen*.txt:', nz)
if set(pt) - used: print('Pointen ohne passende Folie (Titel prüfen):', set(pt) - used)
fehl = quellen_link.unlinked_bibliography(slides)
if fehl: print('Quellen ohne Eintrag im Verzeichnis (ul.ql):', fehl)
