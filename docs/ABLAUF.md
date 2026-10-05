# Ablauf: Aufnahme-Dialog und Arbeitsschritte

Diese Datei beschreibt im Detail, wie Claude mit dem Quality-Point-Skill ein Projekt aufnimmt. Die Kurzform steht in `.claude/skills/quality-point/SKILL.md`; bei Abweichungen gilt diese Datei für den Wortlaut, SKILL.md für die Reihenfolge.

## Grundsätze

- **Nacheinander fragen, nicht alles auf einmal.** Jeder Block ist ein Aufruf von `AskUserQuestion` mit höchstens 4 Fragen und je 2 – 4 Optionen. Die Option „Anders“ (Freitext) ergänzt das Werkzeug automatisch.
- **Immer eine Empfehlung.** Die erste Option ist die empfohlene und trägt den Zusatz „(empfohlen)“.
- **Nichts doppelt fragen.** Was schon im ersten Satz, in einer vorhandenen `quality_point.json` oder im claude-research-Projekt (`content/meta.json`) steht, wird übernommen und nur bestätigt.
- **Freitext im Chat.** Titel, Namen, Institution, Datum fragt Claude als kurze Liste im Chat ab, nicht als erfundene Auswahloptionen.
- **Nach der Freigabe der Gliederung arbeitet Claude autonom** bis zur Rückmeldung. Ausnahme: ein fehlender API-Schlüssel oder eine Rechtefrage.

---

## Block 1 · Eckdaten

Im Chat (Freitext), kompakt als nummerierte Liste:

1. **Thema / Arbeitstitel** (1 – 2 Sätze)
2. **Autor*in** – Name, Rolle, Institution (erscheint auf Titel- und Landingpage)
3. **Anlass** – Veranstaltung, Ort, Datum

Danach `AskUserQuestion`:

| Frage | Optionen (Beispiel) |
|---|---|
| Zielgruppe? | Studierende (Lehramt) · Schüler*innen · Kollegium/Fortbildung · Fachpublikum |
| Sprache? | Deutsch (Österreich) · Deutsch (Deutschland/Schweiz) · Englisch · zweisprachig |
| Dauer/Umfang? | 20 – 30 Min. · 90 Min. · halber/ganzer Tag · Semester in mehreren Teilen |

Faustregel für den Umfang: etwa eine Folie pro Minute Vortrag, bei Werkstattphasen deutlich weniger.

---

## Block 2 · Material

`AskUserQuestion`, **multiSelect**: „Womit soll ich arbeiten?“

- Vorhandene Präsentation (PPTX oder Keynote-Export als PPTX/PDF)
- PDF, Buch, Skript, Aufsätze
- Webseiten, Videolinks, eigenes claude-research-Projekt
- Claude recherchiert selbst

Anschließend aktiv vorschlagen, was die Qualität hebt (eine kurze Liste im Chat, keine Pflicht):

- eigene Notizen oder Sprechertext, frühere Arbeitsblätter, Lösungen
- Lehrplan bzw. Curriculum (Link oder PDF) – nötig für den Lehrplan-Bezug
- Literaturliste, Lieblingsquellen, Videos, die unbedingt vorkommen sollen
- Fotos, deren Rechte geklärt sind (eigene Aufnahmen, Freigaben)
- Dinge, die **nicht** vorkommen dürfen (Namen, interne Daten)

Dateien legt die Person am besten in einen Unterordner `vorlage/` des Projekts.

### Fachartikel mit claude-research

Eigene, ausdrückliche Frage: **„Soll zusätzlich ein Fachartikel mit claude-research entstehen?“**

| Option | Was passiert |
|---|---|
| Ja, neu erstellen (empfohlen bei „Claude recherchiert selbst“) | `git clone https://github.com/harubert/claude-research` neben das Projekt. Hinweis an die Person: Forschungs-Template desselben Autors, MIT-Lizenz. Dann dessen `CLAUDE.md` befolgen (Quellenrecherche, Kapitel, Build). |
| Ja, gibt es schon | Pfad erfragen. `sources/sources.json` wird Hauptquelle für Befunde, `standalone.html` wird als `artikel.html` übernommen. |
| Nein | Quellen werden direkt im Quality-Point-Projekt gepflegt (`src/quellen_extra_*.json`). |

Der Artikel läuft zuerst (oder parallel durch einen eigenen Agenten), weil die Präsentation auf seine geprüften Quellen zugreift.

---

## Block 3 · Inhaltsschalter

Eigene Frage, Einzelauswahl. Sie entscheidet, wie viel von der Vorlage Pflicht ist.

| Option | Bedeutung | Folgen für die Arbeit |
|---|---|---|
| **Exakt und vollständig nach Vorlage** | Alle Inhalte der Vorlage (Texte, Bilder, Videos, Links, Fragen) sind Mindestumfang. Nur die Gestaltung ist neu. | Vollständige Abgleichtabelle; jedes Element bekommt einen Platz oder eine begründete Ausnahme (z. B. Datenschutz). Keine inhaltlichen Ergänzungen außer Quellenbelegen. |
| **Vorlage + eigene Regie** | Vorlage vollständig, Claude ergänzt Forschung, Beispiele, Übungen. | Abgleichtabelle wie oben, zusätzlich Ergänzungen; Ergänzungen sind in den Notizen als solche erkennbar. |
| **Freie Regie** | Claude entwirft neu, die Vorlage ist Steinbruch. | Keine Vollständigkeitspflicht; was übernommen wird, wird trotzdem geprüft. |
| **Anderes Schema** | Ein didaktisches oder dramaturgisches Format gibt die Struktur vor. | Folgefrage nach dem Schema (siehe unten). |

Schemata für „Anderes Schema“ (Folgefrage, Einzelauswahl):

- **Didaktisch** – Einstieg – Erarbeitung – Sicherung (– Transfer)
- **Vorlesung** – Input-Blöcke mit kurzen Aktivierungen
- **Workshop / Flipped Classroom** – kurzer Input, lange Werkstattphasen, Material vorab
- **Pecha Kucha / Keynote-Talk** – 20 Folien × 20 Sekunden bzw. ein starker Erzählbogen mit wenig Text

---

## Block 4 · Bauliste

`AskUserQuestion`, **multiSelect**, auf zwei Fragen verteilt. Die Präsentation selbst ist immer dabei.

**Frage 4a – Begleitseiten**

- Landingpage (Startseite mit allen Teilen, Materialien, Links)
- Glossar (Fachbegriffe, auf den Folien anklickbar)
- Quellenverzeichnis (APA 7, Rücksprung zur Folie)
- Fachartikel (claude-research)

**Frage 4b – Für den Unterricht**

- Unterrichtsmaterial als Word: Feinziele („Die Schüler*innen können …“), didaktische Analyse nach Klafki (Gegenwarts-, Zukunfts-, exemplarische Bedeutung, Struktur, Zugänglichkeit), Arbeitsauftrag, Lösungen mit Begründung
- Unterrichtsfolien je Material, mit Illustration und Download-Link
- Lehrplan-Bezug (braucht Lehrplan-Daten: Link, PDF oder Auszug)
- Werkstatt-Aufträge für die Teilnehmenden

**Frage 4c – Im Vortrag** (nur wenn sinnvoll)

- Interaktionsbausteine (Schätzregler, Echt/Fake, Zuordnen, Timer, Zufallsrad, Wortwolke, QR …)
- Video-Inhaltsangaben (Standbild, Titel, Länge, Beobachtungsauftrag, geprüfter Link)

---

## Block 5 · Stil

1. `styles/index.html` öffnen (Windows `start "" "…\styles\index.html"`, macOS `open "…/styles/index.html"`).
2. Die Seite zeigt 10 Stile und 10 Schriftsets; beide sind frei kombinierbar. Jede Kombination hält sich an dieselben Design-Variablen (`engine/TOKENS.md`), deshalb funktionieren alle Folientypen in jedem Stil.
3. Frage im Chat: „Welcher Stil und welches Schriftset? Oder soll ich passend zur Zielgruppe wählen?“
4. Die Wahl landet in `quality_point.json` (`stil` = Ordnername unter `styles/`, z. B. `papiertheater`; das Schriftset aus `styles/_schriftsets/`). `build.py` bindet beides beim Bauen ein. Schriften liegen lokal (WOFF2, SIL Open Font License).

Die zehn Stile: bauhaus · comic · fibel · gouache · journal · knetwerk · nachtprogramm · papiertheater · riso · tafelkreide.

---

## Block 6 · Grafik

Einzelauswahl:

| Option | Gut für | Zu bedenken |
|---|---|---|
| **Generierte Bilder per API-Schlüssel** | stimmige Kapitel- und Titelbilder, Illustrationen zu Unterrichtsmaterial | kostet Geld, braucht Konto und Schlüssel; Bilder kontrollieren (Hände, Schrift, Klischees) |
| **Vektorgrafiken von Claude Code (SVG)** | Diagramme, Piktogramme, schematische Illustrationen; kostenlos, offline, scharf in jeder Größe | weniger „malerisch“; komplexe Szenen wirken schlicht |
| **Nur Bilder aus der Vorlage / frei lizenziert** | Projekte mit vielen eigenen Fotos; maximale Rechtssicherheit | Lizenz und Urheber*in bei jedem Bild angeben (z. B. Wikimedia Commons) |

### Anbieter für generierte Bilder

Preise ändern sich laufend; die Angaben sind Größenordnungen (Stand Herbst 2026) und vor der Nutzung beim Anbieter zu prüfen. Die genauen Variablennamen und Modelle stehen im Kopf von `styles/bilder_generieren.py`.

| Anbieter | Umgebungsvariable (üblich) | Stärken | Schwächen | Kosten grob |
|---|---|---|---|---|
| OpenAI gpt-image | `OPENAI_API_KEY` | sehr gute Prompt-Treue, Text im Bild möglich | eher teuer in hoher Qualität, langsamer | einige Cent bis ca. 0,25 USD je Bild |
| Google Gemini / Imagen | `GEMINI_API_KEY` | gute Qualität, schnell, Bildbearbeitung | Kontingente/Regionen je nach Konto | wenige Cent je Bild |
| fal.ai Flux | `FAL_KEY` | sehr schnell, günstig, viele Modelle | Qualität je nach Modell (schnell vs. pro) | Bruchteil eines Cents bis wenige Cent |
| Stability AI | `STABILITY_API_KEY` | etablierte Modelle, Stilkontrolle | Prompt-Treue schwankt | wenige Cent je Bild |
| Replicate | `REPLICATE_API_TOKEN` | Zugriff auf viele offene Modelle | Abrechnung nach Laufzeit, schwer planbar | je nach Modell |

**Schlüssel-Regeln (verbindlich):**

- Den Schlüssel setzt die Person selbst als Umgebungsvariable, z. B. PowerShell `$env:OPENAI_API_KEY = "…"` (nur für die Sitzung) bzw. dauerhaft über die Systemeinstellungen, macOS/Linux `export OPENAI_API_KEY=…`.
- Claude schreibt den Schlüssel **nie** in eine Datei, nie in `quality_point.json`, nie in eine HTML-Seite und gibt ihn nie im Chat wieder.
- `.gitignore` schließt `.env`, `*.key` und ähnliche Dateien aus; `deploy.py` bricht ab, wenn ein Schlüsselmuster im Webpaket auftaucht.
- Ein Bild ohne Text im Bild ist fast immer besser: Beschriftung gehört auf die Folie, nicht ins Bild.

---

## Block 7 · Veröffentlichung

| Option | Was passiert |
|---|---|
| Nur lokal (empfohlen für den Anfang) | `python <quality_point>/engine/deploy.py <projekt>` erzeugt den Veröffentlichungsordner (`ziel` in `quality_point.json`, Standard `deployment/` neben dem Projekt) mit Präsentation, Begleitseiten, Schriften, Bildern und Materialien. Diesen Ordner kann man per USB-Stick, LMS-Upload oder Webspace weitergeben. |
| Übergabe an Server/Webspace | Claude nennt Ordner und Dateien; hochgeladen wird nur nach ausdrücklicher Freigabe, z. B. durch eine eigene Server-Session der Person. |

**Zugangsschutz empfehlen**, sobald Zitatrecht genutzt wird (fremde Screenshots, Werbemotive, Zeitungsausschnitte): Passwortschutz per `.htaccess`, Kurs im Lernmanagementsystem oder ein nicht öffentlich verlinkter Ordner. Lokale Videokopien (`video_lokal/`) kommen nie ins Webpaket.

---

## Abschluss der Aufnahme

Claude legt das Projekt mit `engine/neues_projekt.py` an, schreibt alle Antworten in dessen `quality_point.json` (Vorlage `engine/quality_point.beispiel.json`) und fasst einmal zusammen:

> So baue ich es: *Thema* für *Zielgruppe*, *Dauer*, Modus *Inhaltsschalter*, Stil *X* mit Schriftset *Y*, Grafik *Z*. Dazu: *Bauliste*. Passt das?

Danach folgt der Arbeitsablauf aus SKILL.md, Teil B: Projekt anlegen → Bestandskatalog → **Gliederung freigeben lassen** → autonom bauen → Quellen prüfen → `pruefen.py` OK und Screenshots angesehen → `deploy.py` → kurze Rückmeldung.

### Die Gliederungsfreigabe

Die Gliederung ist eine Tabelle im Chat: Teil · Folientitel · Minuten · Interaktion/Werkstatt/Material · Hauptquellen. Bei „exakt“ zeigt Claude zusätzlich, wie viele Original-Elemente es gibt und wo sie landen. Erst nach dem „Passt“ wird gebaut.

### Die Rückmeldung am Ende

Kurz und prüfbar:

- erzeugte Dateien und Folienzahl, Anzahl Quellen, Glossarbegriffe, Materialien
- Ergebnis von `pruefen.py` und `deploy.py`
- bewusst nicht Übernommenes mit Grund (z. B. Foto mit Kindergesicht)
- offene Punkte (z. B. „3 Bilder: Herkunft unbekannt“, „Video X nicht mehr verfügbar, Ersatz verlinkt“)
- Start: `praesentation.html` öffnen, `H` zeigt alle Tasten
