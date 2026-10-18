# Gemeinsame Konfiguration aller Quality-Point-Werkzeuge.
# Jedes Projekt hat eine Datei quality_point.json (Vorlage: engine/quality_point.beispiel.json).
# Aufrufmuster aller Skripte:  python engine/<skript>.py <projektordner>   (ohne Angabe: aktueller Ordner)
import json, os, sys, copy

ENGINE = os.path.dirname(os.path.abspath(__file__))

STANDARD = {
    'titel': 'Ohne Titel',
    'untertitel': '',
    'autor': '',
    'veranstaltung': '',
    'institution': '',
    'sprache': 'de',                 # de | en (Begleitseiten, <html lang>, Zahlenformat)
    'stil': 'papiertheater',         # Ordnername unter styles/
    'engine': '',                    # Pfad zur Engine (nur Hinweis für Aufrufe: python <engine>/build.py <projekt>)
    'stile': '',                     # Pfad zum styles-Ordner; leer = <engine>/../styles
    'artikel': '',                   # Pfad zu einem claude-research-Projekt (standalone.html, quellen.html, sources/sources.json); leer = aus
    'lehrplan': {'an': False, 'datei': 'daten/lehrplan.json'},
    'materialien': {'an': False, 'ordner': 'material', 'ausgabe': 'formulare'},
    'themen': {},                    # data-thema der Folien -> Liste von „thema“-Werten der Materialien
    'einheiten': [],                 # Kacheln der Startseite: {kurz, folie (data-title), name, text, bild}
    'ziel': '../deployment',         # Veröffentlichungsordner (relativ zum Projekt)
    'sperrliste_zusatz': [],         # weitere Regex-Muster, die im Paket nicht vorkommen dürfen
    'notizschutz': {},               # {"bis": "JJJJ-MM-TT"} + PIN in Umgebungsvariable QP_NOTIZ_PIN: Notizen im Paket nur mit PIN (werkzeuge/notizschutz.py)
    'seiten_zusatz': [],             # weitere Dateien/Ordner fürs Paket (z. B. "img/hero.webp")
    'institutionen': {},             # Autorkürzel in Quellen -> {"anzeige": "UNESCO", "lang": "United Nations …"}
    'bis_leerzeichen': False,        # „12–17“ -> „12 – 17“ in Folien, Seiten und Word-Dateien
    'titelbild': '',                 # Bild der Startseite, z. B. img/titel.webp
    'fusszeile': '',                 # Zusatzzeile im Fuß der Begleitseiten (z. B. Hinweis auf KI-Bilder)
    'ausgabe': 'praesentation.html',
}


def projekt_aus_argv(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    pos = [a for a in argv if not a.startswith('-')]
    return os.path.abspath(pos[0] if pos else os.getcwd())


def _mischen(basis, neu):
    for k, v in neu.items():
        if isinstance(v, dict) and isinstance(basis.get(k), dict):
            _mischen(basis[k], v)
        else:
            basis[k] = v
    return basis


def lade(projekt=None):
    """Liest <projekt>/quality_point.json, ergänzt Standardwerte und berechnete Pfade (Schlüssel mit _)."""
    for s in (sys.stdout, sys.stderr):
        try: s.reconfigure(encoding='utf-8')
        except Exception: pass
    projekt = os.path.abspath(projekt or projekt_aus_argv())
    datei = os.path.join(projekt, 'quality_point.json')
    if not os.path.exists(datei):
        sys.exit(f'Keine quality_point.json in {projekt} – Projekt anlegen mit: python {os.path.join(ENGINE, "neues_projekt.py")} <ordner>')
    with open(datei, encoding='utf-8') as f:
        roh = json.load(f)
    K = _mischen(copy.deepcopy(STANDARD), {k: v for k, v in roh.items() if not k.startswith('_')})
    K['_projekt'] = projekt
    K['_engine'] = ENGINE
    K['_stile'] = os.path.abspath(os.path.join(projekt, K['stile'])) if K['stile'] else os.path.abspath(os.path.join(ENGINE, '..', 'styles'))
    K['_stil'] = os.path.join(K['_stile'], K['stil'])
    if not os.path.isdir(K['_stil']):
        print(f'WARNUNG: Stil „{K["stil"]}“ nicht gefunden ({K["_stil"]}) – es gilt nur basis.css')
    K['_artikel'] = os.path.abspath(os.path.join(projekt, K['artikel'])) if K['artikel'] else ''
    K['_ziel'] = os.path.abspath(os.path.join(projekt, K['ziel']))
    return K


def p(K, *teile):
    """Pfad im Projektordner."""
    return os.path.join(K['_projekt'], *teile)


def seiten(K):
    """Positivliste der Seiten, die gebaut und veröffentlicht werden."""
    s = ['index.html', K['ausgabe'], 'glossar.html', 'quellen.html']
    if K['_artikel']: s.append('artikel.html')
    if K['lehrplan'].get('an'): s.append('lehrplan.html')
    return s


TEXTE = {
    'de': {
        'start': 'Start', 'praes': 'Präsentation', 'artikel': 'Fachartikel', 'quellen': 'Quellen', 'glossar': 'Glossar',
        'lehrplan': 'Lehrplan', 'materialien': 'Materialien', 'praes_start': '▶ Präsentation starten', 'artikel_lesen': 'Fachartikel lesen',
        'folien': 'Folien', 'begriffe': 'Glossarbegriffe', 'stand': 'Stand', 'einheiten': 'Einheiten', 'einheit': 'Einheit',
        'folien_ab': 'Folien ab Nr.', 'material1': 'Material', 'materialn': 'Materialien', 'weitere': 'Weitere',
        'mat_kick': 'Für den Unterricht', 'mat_h': 'Fertige <em>Materialien</em>',
        'mat_lead': 'Arbeitsblätter als Word-Dateien zum Anpassen. Jedes Material enthält eine Seite „Für die Lehrperson“ mit Feinzielen, didaktischer Analyse, Ablauf, Lösungen und Quellen.',
        'mat_folgen': 'Materialien folgen.', 'nachlesen': 'Zum Nachlesen', 'grundlage': 'Zum <em>Nachlesen</em>',
        'artikel_t': 'Ausführlicher Text mit allen Belegen.', 'lehrplan_t': 'Bezüge zum Lehrplan, wörtlich mit Fundstelle.',
        'glossar_t': 'Fachbegriffe in einfachen Worten.', 'quellen_t': 'Alle zitierten Quellen mit Link zum Original.',
        'gl_lead': 'Die Begriffe sind in der Präsentation anklickbar (Taste G öffnet dort dasselbe Glossar).',
        'gl_suche': 'Begriff suchen …', 'fachbegriffe': 'Fachbegriffe', 'q_lead': 'Alle in der Präsentation zitierten Werke.',
        'q_suche': 'Quelle suchen …', 'werke': 'Werke', 'geprueft': '✓ am Primärtext geprüft', 'ungeprueft': 'nicht verifiziert',
        'primaer': 'Primärquellen', 'abgerufen': 'abgerufen', 'alle': 'Alle', 'erstellt': 'Erstellt mit Quality Point',
        'im_unterricht': 'Im Unterricht', 'mat_laden': 'Arbeitsmaterial herunterladen (Word)',
    },
    'en': {
        'start': 'Home', 'praes': 'Presentation', 'artikel': 'Article', 'quellen': 'References', 'glossar': 'Glossary',
        'lehrplan': 'Curriculum', 'materialien': 'Materials', 'praes_start': '▶ Start presentation', 'artikel_lesen': 'Read the article',
        'folien': 'slides', 'begriffe': 'glossary terms', 'stand': 'as of', 'einheiten': 'Units', 'einheit': 'Unit',
        'folien_ab': 'Slides from no.', 'material1': 'material', 'materialn': 'materials', 'weitere': 'More',
        'mat_kick': 'For the classroom', 'mat_h': 'Ready-made <em>materials</em>',
        'mat_lead': 'Worksheets as editable Word files. Each includes a teacher page with objectives, didactic analysis, procedure, answers and sources.',
        'mat_folgen': 'Materials will follow.', 'nachlesen': 'Further reading', 'grundlage': 'Further <em>reading</em>',
        'artikel_t': 'Full text with all references.', 'lehrplan_t': 'Curriculum references, quoted verbatim.',
        'glossar_t': 'Key terms in plain words.', 'quellen_t': 'All cited sources with links.',
        'gl_lead': 'Terms are clickable in the presentation (key G opens the same glossary).',
        'gl_suche': 'Search term …', 'fachbegriffe': 'terms', 'q_lead': 'All works cited in the presentation.',
        'q_suche': 'Search references …', 'werke': 'works', 'geprueft': '✓ checked against primary text', 'ungeprueft': 'not verified',
        'primaer': 'Primary sources', 'abgerufen': 'retrieved', 'alle': 'All', 'erstellt': 'Made with Quality Point',
        'im_unterricht': 'In class', 'mat_laden': 'Download material (Word)',
    },
}


def T(K):
    return TEXTE.get(K.get('sprache', 'de'), TEXTE['de'])
