# Änderungen

## 2026-10-11

- **Startseite mit Onboarding** (`styles/index.html`): Der Skill öffnet sie vor der ersten Frage. Sie zeigt den Ablauf in vier Schritten und die drei Bilder-Wege (Claude zeichnet selbst als SVG · Bildgenerator mit eigenem Schlüssel · eigene oder freie Bilder) mit Kosten und Grenzen.
- **Ehrliche Angabe je Stil**, ob er ohne Schlüssel trägt (`bilder.vektor` in `stil.json`): Abzeichen „Kein Schlüssel nötig“, „Geht ohne Schlüssel“ oder „Bildgenerator empfohlen“, dazu ein Filter.
- **Vektor-Beispiele** (`beispiel/vektor.svg`) für Papiertheater, Fibel, Gouache, Knetwerk, Nachtprogramm und Riso, auf jeder Stilkarte neben dem KI-Beispiel.
- **Neuer Baustein Handout** (`engine/werkzeuge/handout_bauen.py`): A4-PDF im Design der Präsentation mit Kernaussagen, Kapiteln, Bildern, „Fragestellungen für die eigene Kompetenzentwicklung“, gesamter Literaturliste und QR-Code. Druck über Edge/Chrome, keine Zusatzpakete außer Pillow.
- `vorschau_bauen.py` lädt die Schriften aus `styles/_schriftsets/fonts/`, passend zum Entfernen der doppelten Schriften.

## 2026-10-05

- Erste Veröffentlichung: Skill, Engine, 10 Stile × 10 Schriftsets, Werkzeuge, zwei Demos.
