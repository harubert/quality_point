# Wird von build.py importiert (Arbeitsordner = Projekt): Glossar src/glossar*.txt einlesen
# und Fachbegriffe auf den Folien anklickbar machen. Format: engine/FOLIEN.md, Abschnitt „Glossar“.
import re, json, html as _h
def load():
    G = []
    import glob   # liest glossar.txt und glossar_teilN.txt
    alle = '\n\n'.join(open(p, encoding='utf-8').read() for p in sorted(glob.glob('src/glossar*.txt')))
    for block in re.split(r'\n\s*\n', alle):
        lines = [l for l in block.strip().split('\n') if l.strip() and not l.startswith('#')]
        if not lines or '|' not in lines[0]: continue
        parts = [p.strip() for p in lines[0].split('|')]
        e = dict(id='g%d' % len(G), term=parts[0], forms=[p for p in parts[1:] if p], e='', q='')
        for l in lines[1:]:
            if l.startswith('E:'): e['e'] = l[2:].strip()
            if l.startswith('Q:'): e['q'] = l[2:].strip()
        G.append(e)
    return G
SKIP = ('svg', 'aside', 'cite', 'style', 'script', 'a', 'button', 'textarea', 'h1')
def process(slides):
    G = load()
    forms = sorted(((f, g['id']) for g in G for f in [g['term']] + g['forms']), key=lambda x: -len(x[0]))
    if not forms: return slides, G
    rx = re.compile(r'(?<![\wÄÖÜäöüß„-])(' + '|'.join(re.escape(f) for f, _ in forms) + r')(?![\wÄÖÜäöüß-])')
    fid = dict(forms)
    gmap = {g['id']: g for g in G}
    def per_slide(m):
        sec = m.group(0); used = set(); out = []; skip = []
        for tok in re.split(r'(<[^>]+>)', sec):
            if tok.startswith('<'):
                t = re.match(r'</?\s*([a-zA-Z0-9]+)', tok)
                if t:
                    name = t.group(1).lower()
                    if tok.startswith('</'):
                        if skip and skip[-1] == name: skip.pop()
                    elif (name in SKIP or (name == 'div' and ('bignum' in tok or 'kick' in tok or 'class="cap' in tok)) or (name == 'ul' and 'class="ql' in tok) or (name == 'p' and 'class="cap' in tok)) and not tok.endswith('/>'):
                        skip.append(name)
                    elif skip and name == skip[-1] and not tok.endswith('/>'):
                        skip.append(name)
                out.append(tok); continue
            if skip or not tok.strip(): out.append(tok); continue
            def wrap(mm):
                gid = fid[mm.group(1)]
                if gid in used: return mm.group(0)
                used.add(gid); g = gmap[gid]
                tip = _h.escape(g['term'] + ': ' + g['e'], quote=True)
                return f'<span class="gl" data-g="{gid}" title="{tip}">{mm.group(1)}</span>'
            out.append(rx.sub(wrap, tok))
        return ''.join(out)
    slides = re.sub(r'<section class="slide.*?</section>', per_slide, slides, flags=re.S)
    return slides, G
