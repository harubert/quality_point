# Änderungen

## 2026-10-18

- **Einrichtungsseite `start.html`** statt Fragenkette im Chat: alles voreingestellt und erklärt (Eckdaten, Material, Inhaltsschalter, Bauliste, 20 Stile mit Musterfolien und Schriftprobe, Bilder-Wege mit Beispielen, Veröffentlichung, Quality Response). „Standard übernehmen“ oder einstellen; Ergebnis als Code `QP1…` für den Chat oder als Datei. `engine/werkzeuge/code_lesen.py` liest beides; der Skill fragt nur noch nach Lücken. Erzeugt von `engine/werkzeuge/start_bauen.py`.
- **Trennung:** Quality Point bleibt reines HTML/JS ohne Server. Der am 16. 10. eingebaute Live-Modus (PHP, Teilnehmerfassung, Live-Panel) ist wieder ausgebaut und lebt als eigenes Produkt weiter: **Quality Response** (https://github.com/harubert/quality_response) setzt auf einem fertigen Quality-Point-Paket auf. Geblieben sind die Andockpunkte (`data-nr`, `data-id`, `window.deck`, Ereignis `qp-folie`), der Baustein `ia-umfrage` (lokal, Handzeichen zählen), die Presenter-Anzeige der Teilschritte und der Fokus-Fix.
- Aufgeklappte Bilder (Lupe), Glossar-Ebene, Video-Inhalt und laufende Videos schließen sich beim Weiterklicken (Schritt oder Folie) von selbst.

## 2026-10-16

- **Zehn neue Stile** (jetzt 20, je mit eigenem Schriftset, OFL, lokal): Herbarium (naturkundlicher Atlas), Nordisch (skandinavischer Katalog), Magazin (Lifestyle-Editorial), Galerie (White Cube), Schweizer Typografie, Zeitung, Linolschnitt, Beton (Web-Brutalismus), Konsole (Terminal, dunkel), Blaupause (technische Zeichnung, dunkel). Alle mit handgezeichneten Vektorbeispielen; Startseite in vier Gruppen geordnet (warm · editorial · grafisch · dunkel).
- Live-Mitmachen (Server-Modus) – am 18. 10. wieder ausgebaut, siehe oben.
- **Neuer Baustein `ia-umfrage`** (Antworten als Handzeichen zählen, Balken, optional richtige Antwort).
- **Presenter:** Nach Tastendruck erscheint kurz nur die Weiter-Schaltfläche mit den Teilschritten; ein angeklickter Baustein-Knopf blockiert die Tastatur nicht mehr.
- `build.py` vergibt `data-nr` je Folie und `data-id` je Baustein (Andockpunkte); Skill-Regel: die Schrittzahl der Weiter-Schaltfläche darf keine Lösung verraten.
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
