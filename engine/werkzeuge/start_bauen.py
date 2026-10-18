"""Baut start.html im Wurzelordner: die Einrichtungsseite von Quality Point.

Alles, was die Aufnahme sonst im Chat fragt, steht hier mit Erklärung, Beispiel und Voreinstellung: Eckdaten, Material,
Inhaltsschalter, Bauliste, Stil und Schriftset (mit Vorschauen), Bilder-Weg, Veröffentlichung, Quality Response.
Ergebnis für Claude: ein Code zum Einfügen in den Chat (QP1…) oder die gespeicherte quality_point.json
(lesen mit engine/werkzeuge/code_lesen.py). Keine Server, keine Fremddienste – die Seite läuft per Doppelklick.

Aufruf:  python engine/werkzeuge/start_bauen.py        (liest styles/*/stil.json und styles/_schriftsets/*.json)
"""
import html, json
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
STYLES = WURZEL / 'styles'
REIHENFOLGE = ["papiertheater", "fibel", "gouache", "knetwerk", "herbarium", "nordisch", "magazin", "journal", "galerie", "schweizer",
               "bauhaus", "zeitung", "riso", "linol", "comic", "beton", "nachtprogramm", "tafelkreide", "konsole", "blaupause"]
E = lambda t: html.escape(str(t), quote=True)


def bild(sid, namen):
    for n in namen:
        for ext in ('svg', 'webp', 'jpg', 'png'):
            if (STYLES / sid / 'beispiel' / f'{n}.{ext}').exists(): return f'styles/{sid}/beispiel/{n}.{ext}'
    return ''


def main():
    stile = []
    for sid in REIHENFOLGE + sorted(d.name for d in STYLES.iterdir() if d.is_dir() and not d.name.startswith('_') and d.name not in REIHENFOLGE):
        p = STYLES / sid / 'stil.json'
        if p.exists(): stile.append(json.loads(p.read_text(encoding='utf-8')))
    sets = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((STYLES / '_schriftsets').glob('*.json'))]
    sets.sort(key=lambda s: REIHENFOLGE.index(s['standard_fuer_stil']) if s['standard_fuer_stil'] in REIHENFOLGE else 99)
    BADGE = {'voll': ('ok', 'Kein Schlüssel nötig'), 'gut': ('mittel', 'Geht ohne Schlüssel'), 'schwach': ('key', 'Bildgenerator empfohlen')}
    karten = ''
    for c in stile:
        b = c.get('bilder', {}); st = b.get('vektor', 'gut'); bk, bt = BADGE[st]
        karten += (f'<label class="stil" data-stil="{c["id"]}"><input type="radio" name="stil" value="{c["id"]}"{" checked" if c["id"] == "papiertheater" else ""}>'
                   f'<img src="styles/{c["id"]}/vorschau.webp" alt="" loading="lazy"><div class="st-txt"><b>{E(c["name"])}</b><span class="badge {bk}">{bt}</span>'
                   f'<p>{E(c["stimmung"])}</p><small>{E(", ".join(c["passt_zu"][:3]))}</small><a href="styles/_vorschau/{c["id"]}.html" target="_blank" rel="noopener">Musterfolien groß ↗</a></div></label>')
    beispiele = {c['id']: {'vektor': bild(c['id'], ['vektor', 'titel']) if bild(c['id'], ['vektor']) or bild(c['id'], ['titel']).endswith('.svg') else '',
                           'ki': bild(c['id'], ['titel']) if bild(c['id'], ['titel']).endswith('.webp') else '', 'hinweis': c.get('bilder', {}).get('hinweis', ''),
                           'set': c['schriftset'], 'name': c['name']} for c in stile}
    setopt = '<option value="">Standard des Stils</option>' + ''.join(f'<option value="{s["id"]}">{E(s["name"])} – {E(s["titel"]["familie"])} / {E(s["ui"]["familie"])}</option>' for s in sets)
    setfonts = {s['id']: s['css_variablen'] for s in sets}
    fontlinks = ''.join(f'<link rel="stylesheet" href="styles/_schriftsets/fonts/{s["id"]}.css">' for s in sets)

    seite = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quality Point – Einrichtung</title>
{fontlinks}
<style>
:root{{--bg:#F5F2EC;--fg:#1E1E1E;--mut:#5B5750;--card:#fff;--line:#DDD6C8;--acc:#B23A2A;--ok:#2E7D4F;--mittel:#9A6A10;--key:#7A3FA0;--teal:#1F5F5B;--hell:#EEF4F2}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16171A;--fg:#ECEAE4;--mut:#B4B0A8;--card:#212226;--line:#34363C;--acc:#F08A6E;--ok:#3F9A65;--mittel:#B07E1A;--key:#9A62C4;--teal:#7CC4BC;--hell:#1E2A28}}}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg);color:var(--fg);font:400 17px/1.55 "Instrument Sans","Segoe UI",system-ui,sans-serif;padding-bottom:120px}}
main{{max-width:1180px;margin:0 auto;padding:0 20px}}
h1{{font:400 44px/1.1 "Young Serif",Georgia,serif;margin:36px 0 8px}} h2{{font:400 30px/1.2 "Young Serif",Georgia,serif;margin:0}}
h3{{font:600 19px/1.3 "Instrument Sans",system-ui,sans-serif;margin:22px 0 6px}}
.lead{{font-size:19px;max-width:820px;color:var(--mut)}}
.kicker{{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);font-weight:600}}
details.abschnitt{{background:var(--card);border:1px solid var(--line);border-radius:16px;margin:18px 0;padding:0}}
details.abschnitt>summary{{list-style:none;cursor:pointer;display:flex;align-items:center;gap:16px;padding:18px 24px}}
details.abschnitt>summary::-webkit-details-marker{{display:none}}
details.abschnitt>summary .nr{{font:400 30px/1 "Young Serif",Georgia,serif;color:var(--acc);min-width:36px}}
details.abschnitt>summary .zu{{margin-left:auto;font-size:14px;color:var(--mut);white-space:nowrap}}
details.abschnitt>summary .zu b{{color:var(--fg);font-weight:600}}
details.abschnitt>.in{{padding:4px 24px 26px;border-top:1px solid var(--line)}}
.erkl{{color:var(--mut);max-width:820px;margin:8px 0 14px}}
.std{{display:inline-block;font:600 12px/1 system-ui;letter-spacing:.08em;text-transform:uppercase;background:var(--hell);color:var(--teal);padding:4px 8px;border-radius:12px;margin-left:8px;vertical-align:middle}}
.felder{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:12px 18px}}
.feld{{display:flex;flex-direction:column;gap:5px}} .feld label{{font-size:14px;font-weight:600}} .feld small{{color:var(--mut);font-size:13px}}
input[type=text],textarea,select{{font:inherit;font-size:16px;padding:9px 11px;border:1px solid var(--line);border-radius:9px;background:var(--bg);color:var(--fg);width:100%}}
textarea{{min-height:70px;resize:vertical}}
.wahl{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(260px,100%),1fr));gap:12px;margin:10px 0}}
.wahl label{{display:block;background:var(--bg);border:2px solid var(--line);border-radius:12px;padding:12px 14px;cursor:pointer}}
.wahl label:has(input:checked){{border-color:var(--teal);background:var(--hell)}}
.wahl label b{{display:block;margin-bottom:3px}} .wahl label span{{font-size:14px;color:var(--mut)}} .wahl input{{margin-right:6px}}
.bsp{{display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap;margin:8px 0 0}} .bsp img{{width:min(360px,100%);border-radius:8px;border:1px solid var(--line)}}
.bsp figcaption{{font-size:13px;color:var(--mut);margin-top:4px}} .bsp figure{{margin:0}}
.stile{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(270px,100%),1fr));gap:14px;margin-top:10px}}
.stil{{display:block;background:var(--bg);border:2px solid var(--line);border-radius:12px;overflow:hidden;cursor:pointer;position:relative}}
.stil:has(input:checked){{border-color:var(--acc);box-shadow:0 0 0 3px color-mix(in srgb,var(--acc) 25%,transparent)}}
.stil input{{position:absolute;left:10px;top:10px;z-index:1;transform:scale(1.3)}} .stil img{{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}}
.st-txt{{padding:10px 12px 12px}} .st-txt b{{font-size:17px;margin-right:6px}} .st-txt p{{margin:4px 0 2px;font-size:14px;color:var(--mut)}} .st-txt small{{color:var(--mut);display:block;font-size:12px}}
.st-txt a{{font-size:13px;color:var(--acc);text-decoration:none;font-weight:600}}
.badge{{display:inline-block;font:600 11px/1 system-ui;padding:5px 8px;border-radius:99px;color:#fff;background:var(--ok);vertical-align:middle}} .badge.mittel{{background:var(--mittel)}} .badge.key{{background:var(--key)}}
.probe{{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin-top:10px}}
.probe .pt{{font-size:34px;line-height:1.15}} .probe .pa{{font-size:28px;font-style:italic;color:var(--acc)}} .probe .pl{{font-size:20px;font-style:italic}} .probe .pu{{font-size:17px}}
.bild2{{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:760px;margin-top:10px}} .bild2 img{{width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:8px;border:1px solid var(--line);display:block}}
.bild2 figure{{margin:0}} .bild2 figcaption{{font-size:13px;color:var(--mut);margin-top:4px}} .bild2 .leer{{aspect-ratio:3/2;border:1px dashed var(--line);border-radius:8px;display:flex;align-items:center;justify-content:center;text-align:center;padding:12px;color:var(--mut);font-size:14px}}
table.t{{border-collapse:collapse;font-size:14px;margin:8px 0}} table.t td,table.t th{{border-bottom:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}} table.t th{{color:var(--mut);font-weight:600}}
.hinweis{{background:var(--hell);border-left:5px solid var(--teal);padding:10px 14px;border-radius:0 10px 10px 0;font-size:15px;margin:10px 0}}
.warn{{border-left-color:var(--acc);background:color-mix(in srgb,var(--acc) 10%,var(--card))}}
#leiste{{position:fixed;left:0;right:0;bottom:0;z-index:20;background:var(--card);border-top:1px solid var(--line);box-shadow:0 -14px 40px -20px rgba(0,0,0,.4);padding:12px 20px}}
#leiste .innen{{max-width:1180px;margin:0 auto;display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
#leiste .stand{{font-size:14px;color:var(--mut);flex:1;min-width:200px}}
button.k{{font:600 15px/1 system-ui;padding:12px 16px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--fg);cursor:pointer}}
button.k.p{{background:var(--acc);border-color:var(--acc);color:#fff}} button.k.t{{background:var(--teal);border-color:var(--teal);color:#fff}}
#code{{width:100%;font:500 13px/1.5 ui-monospace,Consolas,monospace;min-height:84px;word-break:break-all}}
#fertig .wege{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:14px;margin-top:10px}}
#fertig .weg{{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:14px 16px}} #fertig .weg b{{display:block;margin-bottom:6px}}
#vorschau{{font:400 12px/1.45 ui-monospace,Consolas,monospace;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px;max-height:260px;overflow:auto;white-space:pre-wrap}}
.schritte{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(230px,100%),1fr));gap:12px;margin:18px 0 6px}}
.schritte div{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:15px}} .schritte b{{display:block;font-size:17px}} .schritte i{{font:400 26px/1 "Young Serif",Georgia,serif;color:var(--acc);font-style:normal;display:block;margin-bottom:4px}}
.galerie{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(200px,100%),1fr));gap:10px;margin-top:8px}} .galerie img{{width:100%;border-radius:8px;border:1px solid var(--line)}} .galerie figcaption{{font-size:13px;color:var(--mut)}} .galerie figure{{margin:0}}
.kopiert{{color:var(--ok);font-weight:600}}
</style></head><body>
<main>
<div class="kicker">Quality Point · Einrichtung</div>
<h1>Einstellen, was entstehen soll.</h1>
<p class="lead">Alles ist voreingestellt. Du kannst unten sofort <b>„Standard übernehmen“</b> drücken – oder in Ruhe durch die Abschnitte gehen: Jede Wahl ist erklärt, Stile und Beispiele sind zu sehen. Am Ende bekommst du einen Code für den Chat oder eine Datei für den Projektordner. Die Seite speichert nichts im Netz; was du einträgst, bleibt auf diesem Gerät.</p>
<div class="schritte">
<div><i>1</i><b>Hier einstellen</b>oder Standard übernehmen</div><div><i>2</i><b>Code in den Chat</b>Claude liest ihn und fragt nur, was fehlt</div><div><i>3</i><b>Gliederung freigeben</b>die einzige Rückfrage danach</div><div><i>4</i><b>Claude baut</b>Folien, Seiten, Material – geprüft, mit Quellen</div>
</div>
<div class="galerie">
<figure><img src="docs/bilder/titelfolie.png" alt=""><figcaption>Folien in deinem Stil</figcaption></figure>
<figure><img src="docs/bilder/referentenansicht.png" alt=""><figcaption>Referentenansicht mit Notizen, Timer, zwei Bildschirme</figcaption></figure>
<figure><img src="docs/bilder/uebersicht.png" alt=""><figcaption>Übersicht und Suche</figcaption></figure>
<figure><img src="docs/bilder/interaktion.png" alt=""><figcaption>Interaktionsbausteine am Vortragsrechner</figcaption></figure>
</div>

<form id="f" autocomplete="off">
<details class="abschnitt" open id="s1"><summary><span class="nr">1</span><h2>Eckdaten</h2><span class="zu">Thema, Zielgruppe, Dauer</span></summary><div class="in">
<p class="erkl">Das steht auf Titel- und Startseite. Was du leer lässt, fragt Claude im Chat nach.</p>
<div class="felder">
<div class="feld"><label>Titel oder Thema</label><input type="text" name="titel" placeholder="z. B. Medienpädagogik in der Primarstufe"></div>
<div class="feld"><label>Untertitel</label><input type="text" name="untertitel" placeholder="optional"></div>
<div class="feld"><label>Autor*in</label><input type="text" name="autor" placeholder="Vorname Nachname"><small>Name, wie er auf der Titelfolie stehen soll</small></div>
<div class="feld"><label>Institution</label><input type="text" name="institution" placeholder="z. B. Pädagogische Hochschule Vorarlberg"></div>
<div class="feld"><label>Anlass</label><input type="text" name="veranstaltung" placeholder="Veranstaltung, Ort, Datum"></div>
</div>
<h3>Zielgruppe <span class="std">Standard: Studierende</span></h3>
<p class="erkl">Bestimmt Tonfall, Beispiele und wie viel Fachsprache erklärt wird.</p>
<div class="wahl">
<label><input type="radio" name="zielgruppe" value="studierende" checked><b>Studierende (Lehramt)</b><span>Fachbegriffe mit Glossar, Praxisbezug zur Schule, Prüfungsrelevanz</span></label>
<label><input type="radio" name="zielgruppe" value="schueler"><b>Schüler*innen</b><span>Kurze Sätze, viele Bilder, Mitmach-Phasen</span></label>
<label><input type="radio" name="zielgruppe" value="kollegium"><b>Kollegium / Fortbildung</b><span>Umsetzungsideen, Material zum Mitnehmen</span></label>
<label><input type="radio" name="zielgruppe" value="fachpublikum"><b>Fachpublikum / Tagung</b><span>Belege im Vordergrund, dichter Vortrag</span></label>
<label><input type="radio" name="zielgruppe" value="eltern"><b>Eltern / Öffentlichkeit</b><span>Alltagsnah, ohne Fachjargon, konkrete Tipps</span></label>
</div>
<h3>Sprache <span class="std">Standard: Deutsch (Österreich)</span></h3>
<div class="wahl">
<label><input type="radio" name="sprache" value="de" checked><b>Deutsch (Österreich)</b><span>Schulstufe, Volksschule, Jänner …</span></label>
<label><input type="radio" name="sprache" value="de-DE"><b>Deutsch (Deutschland/Schweiz)</b><span>Grundschule, Klasse, Januar …</span></label>
<label><input type="radio" name="sprache" value="en"><b>Englisch</b><span>Begleitseiten und Bedienung auf Englisch</span></label>
</div>
<h3>Dauer <span class="std">Standard: 90 Minuten</span></h3>
<p class="erkl">Faustregel: etwa eine Folie pro Minute, bei Werkstattphasen deutlich weniger.</p>
<div class="wahl">
<label><input type="radio" name="dauer" value="20"><b>20 – 30 Minuten</b><span>Kurzvortrag, ca. 20 Folien</span></label>
<label><input type="radio" name="dauer" value="45"><b>45 Minuten</b><span>Eine Stunde, ca. 35 Folien</span></label>
<label><input type="radio" name="dauer" value="90" checked><b>90 Minuten</b><span>Seminar oder Doppelstunde, mit Werkstatt</span></label>
<label><input type="radio" name="dauer" value="tag"><b>Halber oder ganzer Tag</b><span>Mehrere Teile mit Pausen und Aufträgen</span></label>
<label><input type="radio" name="dauer" value="semester"><b>Semester in Teilen</b><span>Eine Präsentation, mehrere Einheiten mit eigenen Kacheln</span></label>
</div>
</div></details>

<details class="abschnitt" open id="s2"><summary><span class="nr">2</span><h2>Material</h2><span class="zu">Womit Claude arbeitet</span></summary><div class="in">
<p class="erkl">Mehrfachauswahl. Dateien legst du am besten in einen Unterordner <code>vorlage/</code> des Projekts und nennst hier den Pfad. Ohne Auswahl recherchiert Claude selbst.</p>
<div class="wahl">
<label><input type="checkbox" name="m_vorlage"><b>Vorhandene Präsentation</b><span>PowerPoint, oder Keynote als PPTX/PDF exportiert. Texte, Bilder, Videos, Links werden katalogisiert.</span></label>
<label><input type="checkbox" name="m_pdf"><b>PDF, Buch, Skript, Aufsätze</b><span>Als Quellen und Steinbruch für Folien</span></label>
<label><input type="checkbox" name="m_links"><b>Webseiten und Videolinks</b><span>Werden abgerufen, geprüft und zitiert</span></label>
<label><input type="checkbox" name="m_research"><b>Eigenes claude-research-Projekt</b><span>Geprüfte Quellen und Artikel aus dem Forschungs-Template</span></label>
<label><input type="checkbox" name="m_selbst" checked><b>Claude recherchiert selbst</b><span>Studien, Gesetze, Zahlen mit Beleg – jede Zahl mit Bezugsgruppe</span></label>
</div>
<div class="felder">
<div class="feld"><label>Pfade zu Vorlage und Dateien</label><textarea name="m_pfade" placeholder="z. B. vorlage/Seminar_2025.pptx&#10;vorlage/Lehrplan.pdf"></textarea></div>
<div class="feld"><label>Links</label><textarea name="m_linkliste" placeholder="eine Adresse je Zeile"></textarea></div>
</div>
<h3>Fachartikel mit claude-research <span class="std">Standard: nein</span></h3>
<p class="erkl"><a href="https://github.com/harubert/claude-research" target="_blank" rel="noopener">claude-research</a> ist das Forschungs-Template desselben Autors (MIT): Es recherchiert, prüft Quellen am Primärtext und schreibt einen Fachartikel. Quality Point übernimmt daraus Quellenverzeichnis und Artikelseite.</p>
<div class="wahl">
<label><input type="radio" name="artikel" value="nein" checked><b>Nein</b><span>Quellen werden direkt im Projekt gepflegt</span></label>
<label><input type="radio" name="artikel" value="neu"><b>Ja, neu erstellen</b><span>Claude klont claude-research neben das Projekt und schreibt den Artikel zuerst</span></label>
<label><input type="radio" name="artikel" value="vorhanden"><b>Ja, gibt es schon</b><span>Pfad unten eintragen</span></label>
</div>
<div class="felder"><div class="feld"><label>Pfad zum claude-research-Projekt</label><input type="text" name="artikel_pfad" placeholder="z. B. ../claude-research"></div></div>
</div></details>

<details class="abschnitt" open id="s3"><summary><span class="nr">3</span><h2>Inhaltsschalter</h2><span class="zu">Wie frei Claude mit der Vorlage umgeht</span></summary><div class="in">
<p class="erkl">Die wichtigste Entscheidung bei einer Vorlage: Was ist Pflicht, was darf Claude ändern oder ergänzen?</p>
<div class="wahl">
<label><input type="radio" name="inhalt" value="exakt"><b>Exakt und vollständig nach Vorlage</b><span>Alle Texte, Bilder, Videos, Links und Fragen bleiben – nur die Gestaltung ist neu. Jedes Element bekommt einen Platz oder eine begründete Ausnahme.</span></label>
<label><input type="radio" name="inhalt" value="vorlage_regie" checked><b>Vorlage + eigene Regie</b><span>Vorlage vollständig, dazu Forschung, Beispiele und Übungen von Claude – in den Notizen als Ergänzung erkennbar.</span></label>
<label><input type="radio" name="inhalt" value="frei"><b>Freie Regie</b><span>Claude entwirft neu; die Vorlage ist Steinbruch. Ohne Vorlage automatisch dieser Weg.</span></label>
<label><input type="radio" name="inhalt" value="schema"><b>Anderes Schema</b><span>Ein Format gibt die Struktur vor – Auswahl unten</span></label>
</div>
<div class="felder"><div class="feld"><label>Schema (bei „Anderes Schema“)</label><select name="schema"><option value="">–</option><option value="didaktisch">Didaktisch: Einstieg – Erarbeitung – Sicherung – Transfer</option><option value="vorlesung">Vorlesung: Input-Blöcke mit kurzen Aktivierungen</option><option value="workshop">Workshop / Flipped Classroom: kurzer Input, lange Werkstatt</option><option value="pecha">Pecha Kucha: 20 Folien × 20 Sekunden</option><option value="keynote">Keynote-Talk: starker Erzählbogen, wenig Text</option></select></div></div>
</div></details>

<details class="abschnitt" open id="s4"><summary><span class="nr">4</span><h2>Bauliste</h2><span class="zu">Was außer den Folien entsteht</span></summary><div class="in">
<p class="erkl">Die Präsentation mit Referentenansicht, Notizen, Glossar-Klick und Quellenlinks ist immer dabei. Alles andere ist wählbar.</p>
<div class="wahl">
<label><input type="checkbox" name="b_landingpage" checked><b>Landingpage</b><span>Startseite mit Teilen, Materialien, Links – auch zum Weitergeben</span></label>
<label><input type="checkbox" name="b_glossar" checked><b>Glossar</b><span>Fachbegriffe in einfachen Worten, auf den Folien anklickbar, als eigene Seite</span></label>
<label><input type="checkbox" name="b_quellen" checked><b>Quellenverzeichnis</b><span>APA 7, jede Quelle mit Link zum Original, Rücksprung zur Folie</span></label>
<label><input type="checkbox" name="b_interaktion" checked><b>Interaktionsbausteine</b><span>Schätzregler, Umfrage mit Balken, Echt/Fake, Zuordnen, Wortwolke, Ampel, Timer, Zufallsrad, Karteikarte, QR – alles am Vortragsrechner, ohne Server</span></label>
<label><input type="checkbox" name="b_videoinhalte" checked><b>Video-Inhaltsangaben</b><span>Zu jedem Video: Standbild, Titel, Länge, Beobachtungsauftrag, geprüfter Link, Inhaltsangabe zum Nachlesen</span></label>
<label><input type="checkbox" name="b_werkstatt" checked><b>Werkstatt-Aufträge</b><span>Arbeitsphasen mit Auftrag, Material, Zeit und Sozialform auf eigenen Folien</span></label>
<label><input type="checkbox" name="b_material"><b>Unterrichtsmaterial als Word</b><span>Arbeitsblätter mit Feinzielen („Die Schüler*innen können …“), didaktischer Analyse nach Klafki, Lösungen mit Begründung</span></label>
<label><input type="checkbox" name="b_unterrichtsfolien"><b>Unterrichtsfolien je Material</b><span>Eine Folie „Im Unterricht: …“ mit Illustration und Download-Link</span></label>
<label><input type="checkbox" name="b_lehrplan"><b>Lehrplan-Bezug</b><span>Wörtliche Fundstellen mit Seite – braucht den Lehrplan als Link, PDF oder Auszug (bei Material angeben)</span></label>
<label><input type="checkbox" name="b_handout"><b>Handout als PDF</b><span>A4 im Design der Folien: Kernaussagen, Kapitel mit Bildern, Fragestellungen für die eigene Kompetenzentwicklung, Literatur, QR-Code</span></label>
<label><input type="checkbox" name="b_notizschutz"><b>Notizschutz mit PIN</b><span>Im veröffentlichten Paket sind Sprechernotizen verschlüsselt – nützlich, wenn Studierende die Folien vor einer Prüfung sehen</span></label>
</div>
<div class="felder"><div class="feld"><label>Handout: etwa wie viele Seiten?</label><input type="text" name="handout_seiten" value="12"></div></div>
<div class="bsp"><figure><img src="docs/bilder/interaktion.png" alt=""><figcaption>Interaktionsbaustein „Echt oder Fake“ – Handzeichen zählen, auflösen</figcaption></figure></div>
</div></details>

<details class="abschnitt" open id="s5"><summary><span class="nr">5</span><h2>Stil und Schrift</h2><span class="zu"><b id="zu-stil">Papiertheater</b></span></summary><div class="in">
<p class="erkl">{len(stile)} Stile, alle Schriften lokal und frei lizenziert. Das Abzeichen sagt ehrlich, ob der Stil ohne Bildgenerator gleichwertig aussieht. Klick auf „Musterfolien groß“ zeigt acht Folientypen im Stil.</p>
<label class="wahl" style="grid-template-columns:1fr"><span style="display:block;background:var(--bg);border:2px solid var(--line);border-radius:12px;padding:12px 14px"><input type="radio" name="stil" value="auto"> <b>Claude wählt passend zur Zielgruppe</b> <span style="color:var(--mut);font-size:14px">– und begründet die Wahl</span></span></label>
<div class="stile">{karten}</div>
<h3>Schriftset <span class="std">Standard: das des Stils</span></h3>
<p class="erkl">Jedes Set lässt sich mit jedem Stil kombinieren. Die Probe unten zeigt Titel, Akzent, Lesekursive und Fließtext.</p>
<select name="schriftset" id="setwahl">{setopt}</select>
<div class="probe" id="probe"><div class="pt">Zwischen Bildschirm und Bilderbuch</div><div class="pa">wirklich wichtig – Gespräch</div><div class="pl">„Kinder lernen am besten, wenn Mediennutzung geteilt wird.“</div><div class="pu">Fließtext und Beschriftungen: Schülerinnen und Schüler gestalten gemeinsam ein Plakat (3./4. Schulstufe). Äpfel, Öl, Übung, Straße – 0123456789</div></div>
</div></details>

<details class="abschnitt" open id="s6"><summary><span class="nr">6</span><h2>Bilder</h2><span class="zu">Woher die Illustrationen kommen</span></summary><div class="in">
<p class="erkl">Drei Wege, auch kombinierbar. Ohne Schlüssel funktioniert alles.</p>
<div class="wahl">
<label><input type="radio" name="grafik" value="vektor" checked><b>Claude zeichnet selbst (SVG)</b><span>Kostenlos, offline, scharf in jeder Größe. Stark bei flachen, grafischen Stilen, Piktogrammen, Diagrammen; Malerei und Material nur angenähert.</span></label>
<label><input type="radio" name="grafik" value="generator"><b>Bildgenerator mit eigenem Schlüssel</b><span>KI-Bilder über ein Konto bei einem Anbieter. Je nach Anbieter Bruchteile eines Cents bis ca. 0,25 USD pro Bild; eine Präsentation braucht meist 10 – 30 Bilder.</span></label>
<label><input type="radio" name="grafik" value="eigene"><b>Nur eigene oder freie Bilder</b><span>Fotos aus der Vorlage oder frei lizenziert (z. B. Wikimedia Commons) – Urheber*in und Lizenz stehen auf der Folie.</span></label>
</div>
<div class="bild2" id="bildbsp"></div>
<p class="erkl" id="bildhinweis"></p>
<h3>Anbieter (nur bei Bildgenerator)</h3>
<select name="anbieter"><option value="openai">OpenAI gpt-image – sehr gute Prompt-Treue, eher teuer (OPENAI_API_KEY)</option><option value="gemini">Google Gemini / Imagen – gut, schnell, Kontingente je Konto (GEMINI_API_KEY)</option><option value="fal">fal.ai Flux – sehr schnell, günstig, Qualität je Modell (FAL_KEY)</option><option value="stability">Stability AI – etablierte Modelle, Prompt-Treue schwankt (STABILITY_API_KEY)</option><option value="replicate">Replicate – viele offene Modelle, Abrechnung nach Laufzeit (REPLICATE_API_TOKEN)</option></select>
<div class="hinweis warn"><b>Schlüssel-Regel:</b> Den Schlüssel setzt du selbst als Umgebungsvariable (PowerShell <code>$env:OPENAI_API_KEY="…"</code>, macOS/Linux <code>export OPENAI_API_KEY=…</code>). Er kommt nie in eine Datei, nie in den Chat, nie in diese Seite.</div>
</div></details>

<details class="abschnitt" open id="s7"><summary><span class="nr">7</span><h2>Veröffentlichung</h2><span class="zu">Wo es hingeht</span></summary><div class="in">
<div class="wahl">
<label><input type="radio" name="veroeff" value="lokal" checked><b>Nur lokal</b><span>Ein Ordner <code>deployment/</code> mit allem – per Doppelklick, USB-Stick, Lernplattform oder Webspace nutzbar</span></label>
<label><input type="radio" name="veroeff" value="server"><b>Übergabe an Webspace</b><span>Claude nennt Ordner und Dateien; hochgeladen wird nur nach deiner Freigabe (oder durch eine eigene Server-Session)</span></label>
</div>
<div class="felder"><div class="feld"><label>Ziel (bei Übergabe)</label><input type="text" name="veroeff_ziel" placeholder="z. B. Adresse oder Name der Server-Session"></div></div>
<div class="hinweis">Werden fremde Screenshots oder Werbemotive zitiert, gehört das Paket hinter einen Zugangsschutz (Passwort, Lernplattform).</div>
<h3>Mitmachen vom eigenen Gerät aus <span class="std">Standard: nein</span></h3>
<p class="erkl">Teilnehmer*innen scannen einen QR-Code; die Folien laufen am Handy mit, dazu Stimmungsbarometer, Fragen und Hinweise an dich, „Fertig“-Knopf, Umfragen und Aufgaben mit Live-Ergebnis. Das ist das getrennte Produkt <a href="https://github.com/harubert/quality_response" target="_blank" rel="noopener">Quality Response</a>: Es setzt nach dem Bauen auf dem Paket auf und braucht einen Webspace mit <b>PHP 8</b> und Schreibrecht. Quality Point selbst bleibt reines HTML.</p>
<div class="wahl"><label><input type="checkbox" name="response"><b>Ja, Quality Response einbauen</b><span>Claude holt das Repo, baut den Live-Teil ein und nennt dir das Startpasswort</span></label></div>
</div></details>
</form>

<details class="abschnitt" open id="fertig"><summary><span class="nr">✓</span><h2>Fertig</h2><span class="zu">Code oder Datei an Claude</span></summary><div class="in">
<div class="wege">
<div class="weg"><b>Weg 1 · Code in den Chat (empfohlen)</b>„Code kopieren“ drücken und im Chat einfügen, z. B. „Bau mir die Präsentation, hier die Einrichtung: QP1…“. Claude liest alles daraus und fragt nur nach, was fehlt.</div>
<div class="weg"><b>Weg 2 · Datei speichern</b>„Datei speichern“ lädt <code>quality_point.json</code> herunter. Die Datei in den Projektordner legen (oder Claude sagen, wo sie liegt).</div>
</div>
<h3>Dein Code</h3>
<textarea id="code" readonly></textarea>
<p class="erkl" style="margin-top:6px">Der Code enthält nur, was auf dieser Seite steht – keine Schlüssel, keine Dateien. <span id="kop"></span></p>
<h3>Was Claude bekommt</h3>
<pre id="vorschau"></pre>
</div></details>
</main>

<div id="leiste"><div class="innen"><span class="stand" id="stand">Alles voreingestellt. Ändere, was du willst – oder übernimm den Standard.</span>
<button class="k" type="button" id="bStd">Standard übernehmen</button><button class="k t" type="button" id="bDatei">Datei speichern</button><button class="k p" type="button" id="bCode">Code kopieren</button></div></div>

<script>
const BEISPIELE={json.dumps(beispiele, ensure_ascii=False)};
const SETS={json.dumps(setfonts, ensure_ascii=False)};
const f=document.getElementById('f'), $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const BAU={{b_landingpage:'landingpage',b_glossar:'glossar',b_quellen:'quellen',b_interaktion:'interaktion',b_videoinhalte:'videoinhalte',b_werkstatt:'werkstatt',b_material:'material',b_unterrichtsfolien:'unterrichtsfolien',b_lehrplan:'lehrplan',b_handout:'handout',b_notizschutz:'notizschutz'}};
const MAT={{m_vorlage:'vorlage',m_pdf:'pdf',m_links:'links',m_research:'research',m_selbst:'selbst'}};
const v=n=>{{const e=f.elements[n]; if(!e) return ''; if(e.type==='checkbox') return e.checked; if(e.length&&e[0]&&e[0].type==='radio') return (f.querySelector('[name="'+n+'"]:checked')||{{}}).value||''; return (e.value||'').trim();}};
function sammle(){{
  const stil=v('stil'); const d={{_quelle:'start.html',titel:v('titel'),untertitel:v('untertitel'),autor:v('autor'),institution:v('institution'),veranstaltung:v('veranstaltung'),
    sprache:v('sprache').startsWith('de')?'de':'en',stil:stil==='auto'?'':stil,schriftset:v('schriftset'),
    lehrplan:{{an:v('b_lehrplan')}},materialien:{{an:v('b_material')}},
    aufnahme:{{zielgruppe:v('zielgruppe'),sprache_variante:v('sprache'),dauer:v('dauer'),stil_auto:stil==='auto',
      material:Object.fromEntries(Object.entries(MAT).map(([k,n])=>[n,v(k)])),material_pfade:v('m_pfade'),links:v('m_linkliste'),
      artikel:v('artikel'),artikel_pfad:v('artikel_pfad'),inhaltsschalter:v('inhalt'),schema:v('schema'),
      bauliste:Object.entries(BAU).filter(([k])=>v(k)).map(([,n])=>n),handout_seiten:+v('handout_seiten')||12,
      grafik:{{weg:v('grafik'),anbieter:v('grafik')==='generator'?v('anbieter'):''}},
      veroeffentlichung:{{art:v('veroeff'),ziel:v('veroeff_ziel'),response:v('response')}}}}}};
  return d;
}}
const b64=u8=>btoa(String.fromCharCode(...u8)).replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'');
async function code(){{
  const txt=JSON.stringify(sammle()); const roh=new TextEncoder().encode(txt);
  try{{ if(typeof CompressionStream==='function'){{ const cs=new CompressionStream('deflate-raw'); const w=cs.writable.getWriter(); w.write(roh); w.close();
    const buf=new Uint8Array(await new Response(cs.readable).arrayBuffer()); return 'QP1r.'+b64(buf); }} }}catch(e){{}}
  return 'QP1p.'+b64(roh);
}}
let t=null;
async function zeige(){{ const d=sammle(); $('#vorschau').textContent=JSON.stringify(d,null,1); $('#code').value=await code();
  const st=f.querySelector('[name=stil]:checked'); $('#zu-stil').textContent=st&&st.value!=='auto'?(BEISPIELE[st.value]||{{}}).name||st.value:'Claude wählt';
  bilder(); schrift(); try{{ localStorage.setItem('qp-start',JSON.stringify(d)); }}catch(e){{}} }}
function bilder(){{ const st=v('stil'); const box=$('#bildbsp'); const b=BEISPIELE[st]; if(!b){{ box.innerHTML=''; $('#bildhinweis').textContent='Claude wählt den Stil – die Beispiele richten sich danach.'; return; }}
  box.innerHTML=(b.vektor?'<figure><img src="'+b.vektor+'" alt=""><figcaption>Claude zeichnet selbst (SVG) – '+b.name+'</figcaption></figure>':'<figure><div class="leer">Kein Vektorbeispiel</div></figure>')
    +(b.ki?'<figure><img src="'+b.ki+'" alt=""><figcaption>Mit Bildgenerator (KI) – '+b.name+'</figcaption></figure>':'<figure><div class="leer">Bildgenerator optional – der Stil braucht ihn nicht.</div><figcaption>Mit Bildgenerator (KI)</figcaption></figure>');
  $('#bildhinweis').textContent=b.hinweis||''; }}
function schrift(){{ let s=v('schriftset'); if(!s){{ const b=BEISPIELE[v('stil')]; s=b?b.set:'theater'; }} const c=SETS[s]; if(!c) return; const p=$('#probe');
  p.querySelector('.pt').style.fontFamily=c['--serif']; p.querySelector('.pa').style.fontFamily=c['--accent']; p.querySelector('.pl').style.fontFamily=c['--lesen']; p.querySelector('.pu').style.fontFamily=c['--ui']; }}
f.addEventListener('input',()=>{{ clearTimeout(t); t=setTimeout(zeige,150); }}); f.addEventListener('change',zeige);
$('#bStd').addEventListener('click',()=>{{ const eck={{}}; ['titel','untertitel','autor','institution','veranstaltung'].forEach(n=>eck[n]=v(n)); f.reset(); Object.entries(eck).forEach(([n,w])=>f.elements[n].value=w);
  zeige().then(()=>{{ $('#stand').textContent='Standard übernommen – jetzt „Code kopieren“ und im Chat einfügen.'; $('#fertig').open=true; $('#fertig').scrollIntoView({{behavior:'smooth'}}); }}); }});
$('#bCode').addEventListener('click',async()=>{{ await zeige(); const c=$('#code'); try{{ await navigator.clipboard.writeText(c.value); $('#kop').innerHTML='<span class="kopiert">Kopiert – jetzt im Chat einfügen.</span>'; }}catch(e){{ c.focus(); c.select(); $('#kop').textContent='Bitte markieren und kopieren (Strg+C).'; }} $('#fertig').open=true; $('#fertig').scrollIntoView({{behavior:'smooth'}}); }});
$('#bDatei').addEventListener('click',async()=>{{ await zeige(); const d=sammle(); delete d._quelle; const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([JSON.stringify(d,null,2)],{{type:'application/json'}})); a.download='quality_point.json'; document.body.appendChild(a); a.click(); setTimeout(()=>{{URL.revokeObjectURL(a.href);a.remove();}},500); $('#stand').textContent='quality_point.json gespeichert – in den Projektordner legen oder Claude den Ort nennen.'; }});
(function(){{ try{{ const d=JSON.parse(localStorage.getItem('qp-start')||'null'); if(d){{ ['titel','untertitel','autor','institution','veranstaltung'].forEach(n=>{{ if(d[n]) f.elements[n].value=d[n]; }});
  const a=d.aufnahme||{{}}; const setR=(n,w)=>{{ const e=f.querySelector('[name="'+n+'"][value="'+w+'"]'); if(e) e.checked=true; }};
  setR('zielgruppe',a.zielgruppe); setR('sprache',a.sprache_variante); setR('dauer',a.dauer); setR('inhalt',a.inhaltsschalter); setR('grafik',(a.grafik||{{}}).weg); setR('veroeff',(a.veroeffentlichung||{{}}).art);
  setR('stil',a.stil_auto?'auto':d.stil); setR('artikel',a.artikel); if(d.schriftset) f.elements.schriftset.value=d.schriftset;
  Object.entries(MAT).forEach(([k,n])=>{{ if(a.material&&n in a.material) f.elements[k].checked=!!a.material[n]; }}); Object.entries(BAU).forEach(([k,n])=>{{ if(a.bauliste) f.elements[k].checked=a.bauliste.includes(n); }});
  if(a.material_pfade) f.elements.m_pfade.value=a.material_pfade; if(a.links) f.elements.m_linkliste.value=a.links; if(a.artikel_pfad) f.elements.artikel_pfad.value=a.artikel_pfad; if(a.schema) f.elements.schema.value=a.schema;
  if(a.handout_seiten) f.elements.handout_seiten.value=a.handout_seiten; if((a.grafik||{{}}).anbieter) f.elements.anbieter.value=a.grafik.anbieter; if((a.veroeffentlichung||{{}}).ziel) f.elements.veroeff_ziel.value=a.veroeffentlichung.ziel; f.elements.response.checked=!!(a.veroeffentlichung||{{}}).response; }} }}catch(e){{}} zeige(); }})();
</script>
</body></html>
'''
    (WURZEL / 'start.html').write_text(seite, encoding='utf-8')
    print(f'start.html: {len(stile)} Stile, {len(sets)} Schriftsets')


if __name__ == '__main__':
    main()
