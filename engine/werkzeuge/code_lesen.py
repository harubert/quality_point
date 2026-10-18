"""Liest den Einrichtungs-Code von start.html (oder die gespeicherte quality_point.json) und schreibt die Projektkonfiguration.

Aufruf:  python engine/werkzeuge/code_lesen.py <projektordner> "<code>"          Code aus dem Chat (beginnt mit QP1)
         python engine/werkzeuge/code_lesen.py <projektordner> <datei.json>      von start.html gespeicherte Datei (z. B. aus Downloads)
         python engine/werkzeuge/code_lesen.py --zeigen "<code>"                  nur anzeigen, nichts schreiben

Ergebnis: <projekt>/quality_point.json (vorhandene Werte werden ergänzt, nicht gelöscht) – der Abschnitt „aufnahme“ enthält
die Antworten der Aufnahme (Zielgruppe, Material, Inhaltsschalter, Bauliste, Grafik, Veröffentlichung), die build.py nicht braucht,
der Skill aber liest. Code-Format: „QP1r.“ + base64url(deflate-raw(JSON)) oder „QP1p.“ + base64url(JSON).
"""
import base64, json, os, sys, zlib


def dekodiere(code):
    code = code.strip().strip('"\'`')
    if not code.startswith('QP1'):
        raise SystemExit('Kein Einrichtungs-Code (beginnt nicht mit QP1)')
    art, _, rest = code.partition('.')
    roh = base64.urlsafe_b64decode(rest + '=' * (-len(rest) % 4))
    if art == 'QP1r': roh = zlib.decompress(roh, -15)
    return json.loads(roh.decode('utf-8'))


def mischen(alt, neu):
    for k, v in neu.items():
        if isinstance(v, dict) and isinstance(alt.get(k), dict): mischen(alt[k], v)
        else: alt[k] = v
    return alt


def main():
    for s in (sys.stdout, sys.stderr):
        try: s.reconfigure(encoding='utf-8')
        except Exception: pass
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    quelle = sys.argv[2]
    daten = json.load(open(quelle, encoding='utf-8')) if os.path.isfile(quelle) else dekodiere(quelle)
    daten.pop('_quelle', None)
    if sys.argv[1] == '--zeigen':
        print(json.dumps(daten, ensure_ascii=False, indent=2)); return
    projekt = os.path.abspath(sys.argv[1]); ziel = os.path.join(projekt, 'quality_point.json')
    alt = json.load(open(ziel, encoding='utf-8')) if os.path.exists(ziel) else {}
    os.makedirs(projekt, exist_ok=True)
    json.dump(mischen(alt, daten), open(ziel, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    a = daten.get('aufnahme', {})
    print(f'{ziel} geschrieben: Stil {daten.get("stil", "?")}, Schriftset {daten.get("schriftset") or "Standard des Stils"}, '
          f'Inhaltsschalter {a.get("inhaltsschalter", "?")}, Grafik {a.get("grafik", {}).get("weg", "?")}, Bauliste {", ".join(a.get("bauliste", [])) or "–"}')
    fehlt = [k for k in ('titel', 'autor') if not daten.get(k)]
    if fehlt: print('Noch offen (im Chat erfragen):', ', '.join(fehlt))


if __name__ == '__main__':
    main()
