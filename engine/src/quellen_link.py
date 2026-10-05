# Wird von build.py importiert (Arbeitsordner = Projekt): verlinkt Quellenangaben (<cite class="src">)
# mit dem Quellenverzeichnis und der Originalquelle. Beschreibung: engine/FOLIEN.md, Abschnitt „Quellen“.
import re, json, os
REFS = json.load(open('src/quellen.json', encoding='utf-8')) if os.path.exists('src/quellen.json') else []
BYKEY = {}
for r in REFS: BYKEY.setdefault(r['key'], []).append(r)
KEYS = sorted(BYKEY, key=len, reverse=True)
KEYRX = re.compile(r'(?<![\wÄÖÜäöü])(' + '|'.join(re.escape(k) for k in KEYS) + r')(?![\wäöü])') if KEYS else None
# Feste Ausdrücke, die ohne Autorkürzel auf eine Quelle zeigen sollen: (Regex, Quellen-id)
EXTRA = []   # z. B. [(re.compile(r'Lehrplan 2023[^;]*'), 'lehrplan2023')]

def pick(key, seg):
    """Wählt bei mehreren Werken desselben Kürzels das passende: zuerst über die Jahreszahl im Zitat,
    sonst über ein Unterscheidungswort aus dem Feld 'match' (z. B. Zweitautor)."""
    cands = BYKEY[key]
    if len(cands) == 1: return cands[0]
    near = seg[:80]
    for c in cands:
        if c.get('match') and c['match'] in near: return c
    for y in re.findall(r'(\d{4}[a-z]?)', near):
        hits = [c for c in cands if c['year'] == y and not c.get('match')] or [c for c in cands if c['year'] == y]
        if hits: return hits[0]
    return None

def link(r, inner):
    o = f'<a class="qo" href="{r["url"]}" target="_blank" rel="noopener" title="{ {"doi":"Originalquelle (DOI)","web":"Originalquelle (Webseite)","suche":"Quelle online suchen"}[r["kind"]] }">↗</a>'
    return f'<a class="ql" data-q="{r["id"]}" title="Im Quellenverzeichnis anzeigen">{inner}</a>{o}'

def link_cite(c):
    c = c.replace('&amp;', '@@AMP@@')   # „&amp;“ würde das Trennen an „;“ stören
    out = []
    for seg in re.split(r'(;\s*)', c):
        if seg.startswith(';') or not KEYRX: out.append(seg); continue
        done = False
        for rx, rid in EXTRA:
            m = rx.search(seg)
            if m:
                r = [x for x in REFS if x['id'] == rid][0]
                seg = seg[:m.start()] + link(r, m.group(0)) + seg[m.end():]; done = True; break
        if not done:
            m = KEYRX.search(seg)
            if m:
                r = pick(m.group(1), seg[m.start():].replace('@@AMP@@', '&'))
                if r:
                    end = m.end()
                    p = re.match(r'[^;()]{0,80}?\([^)]*\)', seg[m.start():])   # bis einschließlich „(Jahr)“
                    if p: end = m.start() + p.end()
                    seg = seg[:m.start()] + link(r, seg[m.start():end]) + seg[end:]
        out.append(seg)
    return ''.join(out).replace('@@AMP@@', '&amp;')

def process(slides):
    slides = re.sub(r'(<cite class="src[^"]*">)(.*?)(</cite>)', lambda m: m.group(1) + link_cite(m.group(2)) + m.group(3), slides, flags=re.S)
    # Quellenverzeichnis: <li> mit exakt gleichem HTML wie in quellen.json bekommt Anker + Originallink
    byhtml = {r['html']: r for r in REFS}
    def li(m):
        r = byhtml.get(m.group(1).strip())
        if not r: return m.group(0)
        lab = {'doi': 'DOI', 'web': 'online', 'suche': 'suchen'}[r['kind']]
        return f'<li id="q-{r["id"]}">{m.group(1)} <a class="qo2" href="{r["url"]}" target="_blank" rel="noopener">↗ {lab}</a></li>'
    slides = re.sub(r'<li>(.*?)</li>', li, slides, flags=re.S)
    return slides

def unlinked_bibliography(slides):
    """Prüfhilfe: Einträge aus quellen.json, die im Verzeichnis (ul.ql) fehlen."""
    return [r['id'] for r in REFS if f'id="q-{r["id"]}"' not in slides]
