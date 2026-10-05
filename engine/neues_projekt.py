# Legt ein neues Quality-Point-Projekt an. Die Engine bleibt im Repo; das Projekt verweist per quality_point.json („engine“) auf sie.
# Aufruf:  python engine/neues_projekt.py <ordner> [--titel "…"] [--stil papiertheater] [--sprache de|en]
# Danach:  python engine/build.py <ordner>     (Präsentation)      python engine/deploy.py <ordner>   (Paket)
import os, sys, json, shutil, argparse

ENGINE = os.path.dirname(os.path.abspath(__file__))

FOLIEN = {
'00_titel.html': '''<section class="slide s-title" data-chap="Start" data-title="{titel}">
  <div class="tt">
    <div class="kick a">{kick}</div>
    <h1 class="a" data-d=".2">{titel}</h1>
    <p class="sub a" data-d=".4">{untertitel}</p>
  </div>
  <div class="who a" data-d=".6"><b>{autor}</b><br><span class="js-year">2026</span></div>
  <aside class="notes">
    <p><span class="lbl">Kern</span>Worum es heute geht – in einem Satz.</p>
    <p><span class="lbl v">Steuerung</span>H zeigt alle Tasten, O die Übersicht, G das Glossar, N die Notizen, P das Referentenfenster.</p>
  </aside>
</section>
''',
'10_inhalt.html': '''<section class="slide" data-chap="Teil 1" data-title="Fakten und Meinungen">
  <div class="kick">Teil 1</div>
  <h2>Fakten und <em>Meinungen</em></h2>
  <div class="g2">
    <div class="card t f"><h3>Tatsache</h3><p>Lässt sich überprüfen: messen, nachschauen, nachfragen.</p></div>
    <div class="card r f"><h3>Meinung</h3><p>Eine Bewertung – sie kann gut begründet sein, ist aber nicht überprüfbar.</p></div>
  </div>
  <div class="matlinks mt" data-thema="beispiel"></div>
  <cite class="src">Muster (2024)</cite>
  <aside class="notes">
    <p><span class="lbl">Kern</span>Zwei Karten, nacheinander eingeblendet (Klasse f).</p>
    <p><span class="lbl q">Frage</span>Welche Aussage haben Sie heute schon gehört, die man nachprüfen könnte?</p>
  </aside>
</section>

<section class="slide" data-title="Eine Zahl, die hängen bleibt">
  <div class="kick">Teil 1</div>
  <h2>Eine Zahl, die <em>hängen bleibt</em></h2>
  <div class="zahl"><span class="count" data-to="42">0</span><small>%</small></div>
  <div class="zl">Beispielwert – ersetzen Sie ihn durch einen belegten Befund.</div>
  <p class="lesehilfe"><span class="lh">→</span>Das heißt: Fast jede zweite befragte Person stimmt zu.</p>
  <cite class="src">Muster (2024)</cite>
  <aside class="notes"><p><span class="lbl">Kern</span>Zähler läuft beim Aufruf der Folie hoch.</p></aside>
</section>
''',
}
EINFUEGEN = '''<!-- Folien mit data-nach werden hinter die Folie mit gleichem data-title gesetzt -->
<section class="slide s-statement" data-nach="Fakten und Meinungen" data-title="Merksatz">
  <div class="big">Was man <em>nachprüfen</em> kann, ist eine Tatsache.</div>
  <aside class="notes"><p><span class="lbl">Kern</span>Eingefügte Folie aus src/einfuegen_beispiel.html.txt.</p></aside>
</section>
'''
POINTEN = '''# Je Folie ein Block: erste Zeile = data-title, Z: Zweck, P: Pointe
{titel}
Z: Titel und Rahmen des Vortrags.
P: Ein Satz, der hängen bleibt.

Fakten und Meinungen
Z: Unterschied zwischen überprüfbaren und bewertenden Aussagen.
P: Prüfbar oder nicht – das ist die Frage.

Eine Zahl, die hängen bleibt
Z: Kennzahl mit Lesehilfe.
P: Zahlen brauchen einen Satz dazu.

Merksatz
Z: Sicherung in einem Satz.
P: Nachprüfbar = Tatsache.
'''
GLOSSAR = '''# Begriff | weitere Schreibweisen (alle werden auf den Folien erkannt)
# E: Erklärung in einfachen Worten   Q: optional id aus src/quellen.json

Tatsache | Tatsachen
E: Eine Aussage, die sich überprüfen lässt, etwa durch Messen oder Nachschauen.

Meinung | Meinungen
E: Eine persönliche Bewertung; sie kann begründet sein, lässt sich aber nicht nachprüfen.
'''
QUELLEN = [{"id": "muster2024", "key": "Muster", "year": "2024", "kind": "web",
            "html": "Muster, M. (2024). <i>Beispieltitel einer Quelle</i>. Beispielverlag.",
            "text": "Muster, M. (2024). Beispieltitel einer Quelle. Beispielverlag.", "doi": "", "url": "https://example.org/"}]
LEHRPLAN = {"titel": "Bezüge zum Lehrplan", "einleitung": "Wörtliche Auszüge mit Fundstelle.",
            "abschnitte": [{"titel": "Abschnitt", "zitate": [{"text": "Wörtliches Zitat aus dem Lehrplan.", "fundstelle": "Lehrplan, Abschnitt 1", "seite": 1, "verifiziert": False}]}],
            "quellen": [{"titel": "Lehrplan (Primärquelle)", "url": "https://example.org/", "abgerufen": "2026-01-01"}]}


def main():
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass
    ap = argparse.ArgumentParser(description='Neues Quality-Point-Projekt anlegen')
    ap.add_argument('ordner'); ap.add_argument('--titel', default=''); ap.add_argument('--stil', default='papiertheater')
    ap.add_argument('--sprache', default='de', choices=['de', 'en']); ap.add_argument('--autor', default='')
    a = ap.parse_args()
    ziel = os.path.abspath(a.ordner)
    if os.path.exists(os.path.join(ziel, 'quality_point.json')): sys.exit(f'{ziel} enthält schon eine quality_point.json')
    for d in ('src/slides', 'src/snippets', 'material', 'img', 'daten', 'formulare'):
        os.makedirs(os.path.join(ziel, d), exist_ok=True)
    titel = a.titel or os.path.basename(ziel).replace('_', ' ').replace('-', ' ').strip().capitalize()
    cfg = json.load(open(os.path.join(ENGINE, 'quality_point.beispiel.json'), encoding='utf-8'))
    cfg.update({'titel': titel, 'untertitel': '', 'autor': a.autor, 'veranstaltung': '', 'institution': '', 'sprache': a.sprache,
                'stil': a.stil, 'engine': os.path.relpath(ENGINE, ziel).replace('\\', '/'), 'einheiten': [], 'titelbild': '',
                'institutionen': {}, 'sperrliste_zusatz': []})
    w = lambda p, t: open(os.path.join(ziel, p), 'w', encoding='utf-8').write(t)
    w('quality_point.json', json.dumps(cfg, ensure_ascii=False, indent=2) + '\n')
    fmt = dict(titel=titel, kick=a.stil.capitalize(), untertitel='Untertitel', autor=a.autor or 'Name')
    for n, t in FOLIEN.items(): w(os.path.join('src', 'slides', n), t.format(**fmt) if '{titel}' in t else t)
    w(os.path.join('src', 'einfuegen_beispiel.html.txt'), EINFUEGEN)
    w(os.path.join('src', 'pointen.txt'), POINTEN.replace('{titel}', titel))
    w(os.path.join('src', 'glossar.txt'), GLOSSAR)
    w(os.path.join('src', 'quellen_extra.json'), json.dumps(QUELLEN, ensure_ascii=False, indent=1) + '\n')
    w(os.path.join('daten', 'lehrplan.json'), json.dumps(LEHRPLAN, ensure_ascii=False, indent=1) + '\n')
    shutil.copy2(os.path.join(ENGINE, 'material', 'beispiel.json'), os.path.join(ziel, 'material', 'beispiel.json'))
    e = cfg['engine']
    print(f'Projekt angelegt: {ziel}\n  Bauen:          python {e}/build.py .\n  Materialien:    python {e}/werkzeuge/materialien_bauen.py .'
          f'\n  Layout prüfen:  python {e}/werkzeuge/pruefen.py .\n  Veröffentlichen: python {e}/deploy.py .\n  Markup: {e}/FOLIEN.md')


if __name__ == '__main__':
    main()
