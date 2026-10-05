# Erzeugt für jedes Material mit Feld „nach“ eine Folie „Im Unterricht: …“ (Ablauf, Feinziele in den Notizen, Download).
# Daten: <ausgabe>/materialien.json (von materialien_bauen.py). Illustration optional: img/unterricht/<id>.webp
# Ausgabe: src/unterricht_folien.html.txt + src/pointen_unterricht.txt – build.py setzt jede Folie hinter die Folie mit data-title = „nach“.
# Aufruf: python engine/werkzeuge/unterricht_folien.py <projekt>
import json, os, re, sys, html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import konfig
E = lambda t: html.escape(str(t), quote=True)


def kurz(t, n=118):
    t = re.sub(r'\s+', ' ', t)
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + ' …'


def main(K):
    os.chdir(K['_projekt']); T = konfig.T(K); de = K['sprache'] != 'en'
    aus = K['materialien'].get('ausgabe', 'formulare')
    mf = os.path.join(aus, 'materialien.json')
    mat = json.load(open(mf, encoding='utf-8')) if os.path.exists(mf) else []
    out, po = [], []
    for m in mat:
        if not m.get('nach'): continue
        bild = f'img/unterricht/{m["id"]}.webp'
        hat_bild = os.path.exists(bild)
        steps = ''.join(f'<li>{E(kurz(a))}</li>' for a in m.get('ablauf', [])[:5]) or f'<li>{E(m.get("kurz",""))}</li>'
        chips = ''.join(f'<span class="tag">{E(x)}</span>' for x in [m.get('stufe', '')] + m.get('faecher', [])[:3] + [m.get('zeit', '').split(';')[0]] if x)
        fz = m.get('feinziele') or []
        titel = f'{T["im_unterricht"]}: {m["titel"]}'
        lp = m.get('lehrplanbezug', '')
        out.append(f'''<section class="slide uf{'' if hat_bild else ' ohne-bild'}" data-nach="{E(m["nach"])}" data-title="{E(titel)}">
  {f'<img class="hero uf-bild" src="{bild}" alt="">' if hat_bild else ''}
  <div class="uf-text">
    <div class="kick">{E(T["im_unterricht"])}{(' · ' + E(m["einheit"])) if m.get("einheit") else ''}</div>
    <h2>{E(m["titel"])}</h2>
    <p class="uf-kurz">{E(m.get("kurz",""))}</p>
    <div class="uf-chips">{chips}</div>
    <ol class="steps uf-steps">{steps}</ol>
    <div class="uf-dl"><a class="formlink" href="{aus}/{E(m["datei"])}" download>{E(T["mat_laden"])}</a>{f'<span class="uf-kz">{E(lp)}</span>' if lp else ''}</div>
  </div>
  <cite class="src nolabel">{'Unterrichtsmaterial' if de else 'Teaching material'}: {E(m["titel"])}</cite>
  <aside class="notes">
    <p><span class="lbl">{'Feinziele' if de else 'Objectives'}</span></p><ol>{''.join(f'<li>{E(z)}</li>' for z in fz)}</ol>
    <p><span class="lbl">{'Ablauf' if de else 'Procedure'}</span></p><ol>{''.join(f'<li>{E(a)}</li>' for a in m.get('ablauf', []))}</ol>
    <p><span class="lbl v">Material</span>{'Die Word-Datei enthält das Arbeitsblatt und eine Seite „Für die Lehrperson“ mit Lösungen, Differenzierung und Quellen.' if de else 'The Word file contains the worksheet and a teacher page with answers, differentiation and references.'}</p>
  </aside>
</section>''')
        po.append(f'{titel}\nZ: ' + ('Praxisbeispiel mit fertigem Arbeitsmaterial: ' if de else 'Classroom example with ready-made material: ') + m.get('kurz', '')
                  + '\nP: ' + ('Gleich ausprobieren – das Material liegt bei.' if de else 'Try it right away – the material is included.'))
    open('src/unterricht_folien.html.txt', 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
    open('src/pointen_unterricht.txt', 'w', encoding='utf-8').write('\n\n'.join(po) + '\n')
    print(len(out), 'Unterrichtsfolie(n) -> src/unterricht_folien.html.txt')


if __name__ == '__main__':
    main(konfig.lade())
