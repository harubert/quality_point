# Änderungen

## 2026-10-16

- **Notizschutz** (`engine/werkzeuge/notizschutz.py`, optional): Sprechernotizen und Pointen im veröffentlichten Paket verschlüsselt, Freischaltung per PIN (N, P, S, V); PIN aus `QP_NOTIZ_PIN`, optionaler Stichtag. Ohne PIN bricht `deploy.py` ab, bevor der Zielordner angefasst wird.
- **Arbeitsblätter:** Bilder unter dem Titel und je Aufgabe, Bildraster (`bilder_spalten`), Seitenumbruch vor einer Aufgabe (`neue_seite`), Aufzählungen ohne Kästchen (`ohne_kaestchen`); Schreiblinien bleiben in Word einzeln sichtbar.
- **Glossar:** Begriffe ohne weitere Schreibweise („Begriff“ ohne „|“) werden erkannt und verlinkt – bisher fielen sie stillschweigend weg.
- **Pointen:** `data-pointe`/`data-zweck` direkt an der Folie haben Vorrang vor `pointen*.txt`.
- **Paket:** Bilder des Vorher-nachher-Reglers (`data-a`/`data-b`) und Abbildungen des Fachartikels (`figures/`) kommen mit; Schriften fehlen auch beim allerersten Deploy eines neuen Projekts nicht mehr.
- **Lesbarkeit:** Notizen im Referentenfenster und in der Notizleiste behalten ihre Farbe, auch wenn ein Stil (riso, journal) Absätze global einfärbt.
- Anregungen dazu kamen aus dem Einsatz in der Lehrveranstaltung „Visuelle Medien und Bildkompetenz“.

## 2026-10-11

- **Startseite mit Onboarding** (`styles/index.html`): Der Skill öffnet sie vor der ersten Frage. Sie zeigt den Ablauf in vier Schritten und die drei Bilder-Wege (Claude zeichnet selbst als SVG · Bildgenerator mit eigenem Schlüssel · eigene oder freie Bilder) mit Kosten und Grenzen.
- **Ehrliche Angabe je Stil**, ob er ohne Schlüssel trägt (`bilder.vektor` in `stil.json`): Abzeichen „Kein Schlüssel nötig“, „Geht ohne Schlüssel“ oder „Bildgenerator empfohlen“, dazu ein Filter.
- **Vektor-Beispiele** (`beispiel/vektor.svg`) für Papiertheater, Fibel, Gouache, Knetwerk, Nachtprogramm und Riso, auf jeder Stilkarte neben dem KI-Beispiel.
- **Neuer Baustein Handout** (`engine/werkzeuge/handout_bauen.py`): A4-PDF im Design der Präsentation mit Kernaussagen, Kapiteln, Bildern, „Fragestellungen für die eigene Kompetenzentwicklung“, gesamter Literaturliste und QR-Code. Druck über Edge/Chrome, keine Zusatzpakete außer Pillow.
- `vorschau_bauen.py` lädt die Schriften aus `styles/_schriftsets/fonts/`, passend zum Entfernen der doppelten Schriften.

## 2026-10-05

- Erste Veröffentlichung: Skill, Engine, 10 Stile × 10 Schriftsets, Werkzeuge, zwei Demos.
