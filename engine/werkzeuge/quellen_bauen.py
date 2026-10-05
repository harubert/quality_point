# Erzeugt <projekt>/src/quellen.json und die Verzeichnisfolien src/slides/95_quellen.html (+ src/pointen_zz_quellen.txt).
# Kandidaten: Quellen des Artikels (quality_point.json „artikel“ -> <artikel>/sources/sources.json, falls gesetzt)
#             + geprüfte Zusatzquellen der Folien (src/quellen_extra*.json, Schema siehe engine/FOLIEN.md).
# Aufgenommen werden nur Quellen, die in einem <cite class="src"> der Folien vorkommen (Kürzel + Jahr).
# Aufruf: python engine/werkzeuge/quellen_bauen.py <projekt>   (build.py ruft es automatisch auf)
import json, os, re, sys, glob, html, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import konfig


def esc(t): return html.escape(t, quote=False)


def autoren(lst, INST):
    namen = []
    for a in lst:
        k = a.split(',')[0].strip()
        if k in INST and (len(lst) == 1 or a.strip() in (k, k + ', A.', k + ', B.')):
            namen.append(INST[k].get('lang') or INST[k].get('anzeige') or k); continue
        namen.append(a.strip())
    if len(namen) > 7: namen = namen[:6] + ['…', namen[-1]]
    if len(namen) == 1: return esc(namen[0])
    return ', '.join(esc(n) for n in namen[:-1]) + ' &amp; ' + esc(namen[-1])


def aus_artikel(s, INST):
    k = s['authors'][0].split(',')[0].strip()
    key = (INST.get(k) or {}).get('anzeige', k)
    titel, journal, year = s['title'].strip().rstrip('.'), (s.get('journal') or '').strip().rstrip('.'), str(s['year'])
    titel = re.sub(r'"([^"]*)"', '„\\1“', titel)
    au = autoren(s['authors'], INST)
    if s.get('type') in ('book', 'report', 'web'):
        h = f'{au}. ({year}). <i>{esc(titel)}</i>. {esc(journal)}.'
    else:
        h = f'{au}. ({year}). {esc(titel)}. <i>{esc(journal)}</i>.'
    h = h.replace('..', '.')
    if s.get('doi'): url, kind = 'https://doi.org/' + s['doi'], 'doi'
    elif s.get('url'): url, kind = s['url'], 'web'
    else: url, kind = 'https://scholar.google.com/scholar?q=' + re.sub(r'\s+', '+', titel[:90]), 'suche'
    return {'id': s['id'].lower() + '_' + re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', k.lower()))[:12],
            'key': key, 'year': year, 'kind': kind, 'html': h,
            'text': html.unescape(re.sub(r'<[^>]+>', '', h)), 'doi': s.get('doi') or '', 'url': url}


def main(K):
    os.chdir(K['_projekt'])
    INST = K['institutionen']
    kandidaten = []
    if K['_artikel']:
        sj = os.path.join(K['_artikel'], 'sources', 'sources.json')
        if os.path.exists(sj): kandidaten = [aus_artikel(s, INST) for s in json.load(open(sj, encoding='utf-8'))]
        else: print('WARNUNG: Artikelquellen fehlen:', sj)
    for p in sorted(glob.glob('src/quellen_extra*.json')):
        kandidaten += json.load(open(p, encoding='utf-8'))

    folien = ''.join(open(p, encoding='utf-8').read() for p in sorted(glob.glob('src/slides/*.html')) if not p.endswith('95_quellen.html'))
    folien += ''.join(open(p, encoding='utf-8').read() for p in sorted(glob.glob('src/einfuegen_*.html.txt') + glob.glob('src/unterricht_folien.html.txt')))
    zitate = ' ; '.join(re.findall(r'<cite class="src[^"]*">(.*?)</cite>', folien, flags=re.S))
    zitate += ' ; ' + ' ; '.join(re.findall(r'data-q="([^"]*)"', folien))
    zitate = html.unescape(re.sub(r'<[^>]+>', '', zitate))

    def zitiert(r):
        for m in re.finditer(r'(?<![\wÄÖÜäöü])' + re.escape(r['key']) + r'(?![\wäöü])', zitate):
            umfeld = zitate[m.start(): m.start() + 90].split(';')[0]
            if r['year'] in umfeld or r['year'] in ('o. J.', 'n.d.'): return True
        return False

    seen, refs = set(), []
    for r in kandidaten:
        if zitiert(r) and r['id'] not in seen:
            seen.add(r['id']); refs.append(r)
    refs.sort(key=lambda r: unicodedata.normalize('NFKD', r['text']).lower())
    json.dump(refs, open('src/quellen.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    de = K['sprache'] != 'en'
    QW = 'Quellen' if de else 'References'
    if not refs:   # keine Verzeichnisfolie ohne Quellen
        for f in ('src/slides/95_quellen.html', 'src/pointen_zz_quellen.txt'):
            if os.path.exists(f): os.remove(f)
        print(f'0 zitierte Quellen von {len(kandidaten)} Kandidaten')
        return refs
    PRO = 15
    teile = [refs[i:i + PRO] for i in range(0, len(refs), PRO)]
    out, pz = [], []
    for n, t in enumerate(teile, 1):
        titel = QW if len(teile) == 1 else f'{QW} {n}/{len(teile)}'
        chap = f' data-chap="{QW}"' if n == 1 else ''
        lis = '\n'.join(f'    <li>{r["html"]}</li>' for r in t)
        out.append(f'''<section class="slide quellen"{chap} data-title="{titel}">
  <div class="kick">{QW}</div>
  <h2 style="font-size:52px;margin-bottom:20px">{titel}</h2>
  <ul class="ql">
{lis}
  </ul>
  <style>.ql{{columns:2;column-gap:60px;list-style:none}}.ql li{{font-size:18px;line-height:1.32;margin-bottom:8px;padding-left:22px;text-indent:-22px;break-inside:avoid}}</style>
  <cite class="src nolabel">{'alle in diesem Foliensatz zitierten Werke · vollständiges Verzeichnis: quellen.html' if de else 'all works cited in this deck · full list: quellen.html'}</cite>
  <aside class="notes"><p><span class="lbl">{'Kern' if de else 'Core'}</span>{'Verzeichnis der auf den Folien zitierten Werke. Klick auf eine Quellenangabe springt hierher; „↗“ öffnet das Original.' if de else 'References cited on the slides. Clicking a citation jumps here; “↗” opens the original.'}</p></aside>
</section>''')
        pz.append(f'{titel}\nZ: ' + ('Verzeichnis der auf den Folien zitierten Werke mit Link zum Original.\nP: Wer zitiert, verlinkt.' if de else 'References cited on the slides, linked to the originals.\nP: Cite it, link it.'))
    os.makedirs('src/slides', exist_ok=True)
    open('src/slides/95_quellen.html', 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
    open('src/pointen_zz_quellen.txt', 'w', encoding='utf-8').write('\n\n'.join(pz) + '\n')
    print(f'{len(refs)} zitierte Quellen von {len(kandidaten)} Kandidaten -> src/quellen.json, {len(teile)} Verzeichnisfolie(n)')
    return refs


if __name__ == '__main__':
    main(konfig.lade())
