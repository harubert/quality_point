---
name: quality-point
description: "Quality Point: baut aus einem Thema oder aus vorhandenem Material (PowerPoint/Keynote-Export, PDF, Skripten, Webseiten, claude-research-Projekt) eine geprüfte HTML-Präsentation mit Referentenansicht, Quellen, Glossar und optional Landingpage, Fachartikel, Unterrichtsmaterial (Word) und Interaktionsbausteinen. Verwenden, wenn jemand eine Präsentation, einen Foliensatz, einen Vortrag, eine Seminar- oder Unterrichtseinheit erstellen, eine bestehende PPTX/Keynote neu gestalten, erweitern oder in HTML überführen möchte, oder ausdrücklich „Quality Point“ nennt. Nicht verwenden, wenn ausdrücklich eine .pptx-Datei als Ergebnis verlangt wird oder nur eine einzelne Folie kurz umformuliert werden soll."
---

# Quality Point

Du baust mit der Quality-Point-Engine eine Präsentation, die man ohne PowerPoint im Browser zeigt, und auf Wunsch alles, was dazugehört (Landingpage, Glossar, Quellen, Fachartikel, Unterrichtsmaterial). Maßstab ist Qualität: nichts erfinden, alles belegen, alles prüfen, sauber gestalten.

Arbeitsweise in einem Satz: **erst sorgfältig fragen (A), Gliederung freigeben lassen, dann autonom bauen und prüfen (B), am Ende knapp berichten.** Die Qualitätsregeln (C) gelten immer.

---

## 0 · Vorbereitung (vor der ersten Frage, ohne Rückfrage)

1. **Quality-Point-Ordner finden.** Der Skill braucht die Engine aus dem Repository `harubert/quality_point`. Suche in dieser Reihenfolge: Umgebungsvariable `QP_HOME` · aktueller Arbeitsordner (enthält `engine/build.py`) · übergeordnete Ordner · `~/quality_point`. Nichts gefunden → `git clone https://github.com/harubert/quality_point` in einen Ordner neben dem Projekt und kurz sagen, dass das passiert ist.
   Die Engine bleibt im Quality-Point-Ordner; Projekte liegen woanders. **Aufrufmuster aller Skripte:** `python <quality_point>/engine/<skript>.py <projektordner>` (Windows auch `py`; ohne Ordnerangabe gilt der aktuelle Ordner). Jedes Projekt hat eine `quality_point.json` (Vorlage `engine/quality_point.beispiel.json`, Standardwerte in `engine/konfig.py`).
2. **Lesen, bevor du baust:** `engine/FOLIEN.md` (Folientypen, Bausteine, Schritte, Notizen, Glossar-, Quellen- und Pointenformat), `engine/TOKENS.md` (Design-Variablen, an die sich jeder Stil hält), `docs/REGELN.md` (Qualitätsregeln). Sind FOLIEN.md oder TOKENS.md im Repo noch nicht vorhanden, gelten die Kommentare in `engine/build.py`, `engine/src/basis.css (und styles/<stil>/stil.css)` und `engine/src/interaktion.js`.
3. **Vorhandenes prüfen:** Gibt es im Arbeitsordner schon eine `quality_point.json`? Dann ist das ein laufendes Projekt: lesen, Stand zusammenfassen und nur nach dem Fehlenden fragen. Hat die Person im ersten Satz schon Antworten gegeben (Thema, Dauer, Material …), diese übernehmen und **nicht erneut fragen**.

---

## A · Aufnahme: nacheinander fragen

Frage mit dem Werkzeug **AskUserQuestion**, ein Block nach dem anderen (höchstens 4 Fragen pro Aufruf, je 2 – 4 Optionen; „Anders“ ergänzt das Werkzeug automatisch, also nicht selbst als Option anlegen). Gib bei jeder Frage eine **Empfehlung** an (erste Option, Zusatz „(empfohlen)“). Freitextangaben (Titel, Name) kurz im Chat erfragen, nicht als Scheinoptionen. Wortlaut und Optionen im Detail: `docs/ABLAUF.md`.

**1. Eckdaten** – Thema/Arbeitstitel · Zielgruppe (z. B. Studierende, Schüler*innen Sek I, Kollegium, Fachpublikum) · Anlass/Veranstaltung und Datum · Sprache · Dauer bzw. Umfang (z. B. 20 Min., 90 Min., ganzes Semester in Teilen) · Autor*in mit Rolle/Institution.

**2. Material** – Womit fütterst du mich? Mehrfachauswahl: vorhandene PPTX/Keynote-Export · PDF (Skript, Buch, Aufsatz) · Webseiten/Links · eigenes claude-research-Projekt · „Claude recherchiert selbst“. Aktiv vorschlagen, was die Qualität hebt: eigene Notizen, Lehrplan, frühere Arbeitsblätter, Videolinks, Fotos mit geklärten Rechten, Literaturliste.
Danach **ausdrücklich** fragen: **„Soll zusätzlich ein Fachartikel mit claude-research entstehen?“**
- Ja, und es gibt noch keins → `git clone https://github.com/harubert/claude-research` neben das Projekt (Hinweis: Forschungs-Template desselben Autors, MIT-Lizenz), dort `CLAUDE.md` befolgen. Der Artikel liefert `sources/sources.json` (geprüfte Quellen) und `standalone.html`; Quality Point übernimmt beides (Quellenverzeichnis, Artikelseite).
- Ja, existiert schon → Pfad erfragen und `sources.json` als Hauptquelle für Befunde verwenden.

**3. Inhaltsschalter** (eigene Frage, Einzelauswahl – bestimmt alles Weitere):
- **Exakt und vollständig nach Vorlage** – Texte, Bilder, Videos, Links, Fragen der Vorlage sind Mindestumfang; nur die Gestaltung ist neu.
- **Vorlage + eigene Regie** – Vorlage vollständig, Claude ergänzt Forschung, Beispiele, Übungen.
- **Freie Regie** – Claude entwirft neu, die Vorlage ist Steinbruch.
- **Anderes Schema** – z. B. didaktisch (Einstieg – Erarbeitung – Sicherung), Vorlesung, Workshop, Flipped Classroom, Pecha Kucha (20 × 20 s), Keynote-Talk. Bei Wahl: Schema nachfragen.

**4. Bauliste** (multiSelect, auf zwei bis drei Fragen verteilen, weil höchstens 4 Optionen je Frage):
- Präsentation (immer, nicht abwählbar – nur zur Info nennen) · Landingpage · Glossar · Quellenverzeichnis
- Fachartikel (claude-research) · Lehrplan-Bezug (braucht Lehrplan-Daten oder -Link) · Unterrichtsmaterial als Word (Feinziele „Die Schüler*innen können …“, didaktische Analyse nach Klafki, Lösungen mit Begründung) · Unterrichtsfolien je Material mit Illustration
- Video-Inhaltsangaben · Werkstatt-Aufträge · Interaktionsbausteine

**5. Stil** – `styles/index.html` im Browser öffnen (Windows: `start "" "<pfad>\styles\index.html"`, macOS: `open …`). Dort 10 Stile × 10 Schriftsets frei kombinierbar. Stile sind Ordner unter `styles/` (bauhaus, comic, fibel, gouache, journal, knetwerk, nachtprogramm, papiertheater, riso, tafelkreide), Schriftsets liegen in `styles/_schriftsets/`. Person nennt Stil + Schriftset (oder „du entscheidest passend zur Zielgruppe“); Eintrag in `quality_point.json` (`stil`, Schriftset laut `engine/quality_point.beispiel.json`).

**6. Grafik** (Einzelauswahl):
- **Generierte Bilder per API-Schlüssel** – Anbieter nachfragen: OpenAI gpt-image · Google Gemini/Imagen · fal.ai Flux · Stability/Replicate. Vor- und Nachteile und grobe Kosten: `docs/ABLAUF.md`. **Schlüssel nur als Umgebungsvariable**, nie in eine Datei, nie in den Chat zurückschreiben, nie committen. Erzeugt wird mit `styles/bilder_generieren.py`.
- **Vektorgrafiken direkt von Claude Code** (SVG, kostenlos, offline).
- **Nur Bilder aus der Vorlage bzw. frei lizenzierte** (Wikimedia Commons u. Ä., mit Lizenzangabe).

**7. Veröffentlichung** – nur lokal (`deployment/`) · zusätzlich Übergabe an eigene Server-Session/Webspace (Ziel erfragen; du lädst nichts ohne ausdrückliche Freigabe hoch). Wird Zitatrecht genutzt (fremde Screenshots, Werbemotive), **Zugangsschutz empfehlen** (z. B. Passwort per `.htaccess`, LMS-Kurs).

Danach alles in `quality_point.json` des Projekts schreiben (Vorlage: `engine/quality_point.beispiel.json`) und **einmal** zusammenfassen: „So baue ich es – passt das?“

---

## B · Arbeitsablauf

1. **Projekt anlegen:** `python <quality_point>/engine/neues_projekt.py <projektordner>` (weitere Argumente siehe Kopf des Skripts; macOS/Linux `python3`). Es legt `quality_point.json`, `src/slides/`, `img/` usw. an; danach die Antworten aus Teil A in `quality_point.json` eintragen.
2. **Bestandskatalog der Vorlage** (falls Vorlage): Bilder mit `bilder_extrahieren.py` (Engine-Werkzeug) in `img/orig/` ziehen (Katalog `img/orig/katalog.json`: Satz, Folie, Text, Bilddateien). Zusätzlich mit Python (zipfile) Hyperlinks (`_rels`), eingebettete und verlinkte Videos, Notizen auslesen. Ergebnis: Abgleichtabelle Original-Element → geplanter Fundort. Im Modus „exakt“ bzw. „Vorlage + Regie“ ist jede Zeile Pflicht.
3. **Gliederung vorschlagen** (Teile, Folientitel, Dauer je Teil, wo Interaktion/Werkstatt/Material sitzt) und **freigeben lassen**. Das ist die einzige Rückfrage im Ablauf.
4. **Ab hier autonom bis zum Ende** (Vorbild: claude-research). Keine Zwischenfragen wie „Soll ich …?“. Einzige Ausnahme: ein fehlender Schlüssel oder eine Rechtefrage, die du nicht selbst klären kannst.
5. **Folien bauen** nach `engine/FOLIEN.md`: pro Folie eindeutiger `data-title`, Quelle in `<cite class="src">`, ausführliche Notizen (`aside.notes`, 80 – 200 Wörter: Kern, Frage ans Publikum, Hintergrund mit Zahlen), Pointe, Glossarbegriffe. Animation nur mit Bedeutung: ein Klick = ein Gedanke.
6. **Quellen prüfen** (jede Zahl, jedes Zitat, jeder Link per WebFetch/WebSearch):
   - Jede Zahl mit Bezugsgruppe (wer, wann, wie viele) und Lesehilfe „Das heißt: …“ mit Vergleichsmaßstab.
   - Englische Zitate: Original + deutsche Übersetzung direkt darunter, **gleichzeitig eingeblendet**.
   - Bildquellen recherchieren; nicht auffindbar → „Herkunft unbekannt (Recherche ohne Ergebnis)“.
   - Zitatrecht (Analysezweck, nur so groß wie nötig, mit Herkunft) klar trennen von freier Lizenz (Lizenz + Urheber*in nennen).
   - Datenschutz: private Namen, E-Mail-Adressen, Kennzeichen unkenntlich; keine erkennbaren Kindergesichter.
7. **Zusatzseiten** laut Bauliste (Schalter in `quality_point.json`: `artikel`, `lehrplan.an`, `materialien.an`, `einheiten` für die Kacheln der Landingpage): Glossar, Quellen, Landingpage, Lehrplan, Artikel (`seiten_bauen.py`), Word-Materialien (`materialien_bauen.py`), Unterrichtsfolien (`unterricht_folien.py`), generierte Bilder (`bilder_generieren.py` im Ordner `styles/`; Schlüssel nur aus der Umgebungsvariable).
8. **Prüfen** – Schleife bis alles sauber ist (Skriptnamen wie in `engine/`; jeweils mit Projektordner als Argument):
   `quellen_bauen.py` → `build.py` (Warnungen lesen und beheben) → `pruefen.py` (**muss „OK“ melden**) → `screenshot.py <projekt> 1 5 5.3 …` und die Bilder **wirklich ansehen** (Read), jede geänderte Folie im Endzustand.
9. **Deploy:** `deploy.py` baut den Veröffentlichungsordner (`ziel` in `quality_point.json`, Standard `../deployment`) nur aus der Positivliste und bricht bei Treffern der **Sperrliste** ab (Schlüssel, lokale Pfade, private Adressen, CDNs). Eigene vertrauliche Namen vorher in `sperrliste_zusatz` ergänzen. Nie die Sperrliste lockern, um einen Treffer „wegzubekommen“ – Ursache entfernen.
10. **Rückmeldung** (kurz): was entstanden ist (Dateien, Folienzahl, Quellen), Prüfergebnis, bewusst nicht Übernommenes mit Grund, offene Punkte (z. B. „Herkunft unbekannt“ bei 3 Bildern), wie man startet (`praesentation.html` öffnen, `H` für Hilfe).

---

## C · Qualitätsregeln (Kurzfassung – vollständig in `docs/REGELN.md`)

- **Nichts erfinden.** Unsicheres kennzeichnen („nicht geprüft“, „Schätzung“). Legenden und Anekdoten sichtbar vom Belegten trennen.
- **Originalfolien der Autor*in nie als Quelle zitieren** – kein „Seminarpräsentation“, „laut Originalfolie“. Deren Inhalte sind ihr Werk und werden einfach gebracht; Belege kommen aus den eigentlichen Quellen.
- Effektstärken und Prozentwerte immer mit Vergleichsmaßstab („d = 0,4 – etwa so viel wie …“).
- Lernziele operationalisiert („Die Schüler*innen können … benennen/unterscheiden/begründen“). Zu jeder Ankreuz- oder Zuordnungsaufgabe eine Lösung mit Begründung.
- Typografie: Bis-Strich mit Leerzeichen „12 – 17“, Halbgeviertstrich statt Geviertstrich, typografische Anführungszeichen „…“, geschütztes Leerzeichen vor %. Gendern mit Stern (Schüler*innen).
- Keine Google Fonts, keine CDNs zur Laufzeit: Schriften und Skripte liegen lokal.
- Barrierearm: Kontrast mindestens WCAG AA, große Schrift (Fließtext auf Folien nicht unter 28 px bei 1920 × 1080), Alternativtexte, Information nie nur über Farbe.
- Sprache: klar, konkret, ohne KI-Floskeln; österreichische bzw. gewünschte Sprachvariante.
