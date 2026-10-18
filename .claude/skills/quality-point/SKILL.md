---
name: quality-point
description: "Quality Point: baut aus einem Thema oder aus vorhandenem Material (PowerPoint/Keynote-Export, PDF, Skripten, Webseiten, claude-research-Projekt) eine geprüfte HTML-Präsentation mit Referentenansicht, Quellen, Glossar und optional Landingpage, Fachartikel, Unterrichtsmaterial (Word) und Interaktionsbausteinen. Verwenden, wenn jemand eine Präsentation, einen Foliensatz, einen Vortrag, eine Seminar- oder Unterrichtseinheit erstellen, eine bestehende PPTX/Keynote neu gestalten, erweitern oder in HTML überführen möchte, oder ausdrücklich „Quality Point“ nennt. Nicht verwenden, wenn ausdrücklich eine .pptx-Datei als Ergebnis verlangt wird oder nur eine einzelne Folie kurz umformuliert werden soll."
---

# Quality Point

Du baust mit der Quality-Point-Engine eine Präsentation, die man ohne PowerPoint im Browser zeigt, und auf Wunsch alles, was dazugehört (Landingpage, Glossar, Quellen, Fachartikel, Unterrichtsmaterial). Maßstab ist Qualität: nichts erfinden, alles belegen, alles prüfen, sauber gestalten.

Arbeitsweise in einem Satz: **Einrichtungsseite öffnen und deren Code lesen (A), nur Lücken erfragen, Gliederung freigeben lassen, dann autonom bauen und prüfen (B), am Ende knapp berichten.** Die Qualitätsregeln (C) gelten immer.

---

## 0 · Vorbereitung (vor der ersten Frage, ohne Rückfrage)

1. **Quality-Point-Ordner finden.** Der Skill braucht die Engine aus dem Repository `harubert/quality_point`. Suche in dieser Reihenfolge: Umgebungsvariable `QP_HOME` · aktueller Arbeitsordner (enthält `engine/build.py`) · übergeordnete Ordner · `~/quality_point`. Nichts gefunden → `git clone https://github.com/harubert/quality_point` in einen Ordner neben dem Projekt und kurz sagen, dass das passiert ist.
   Die Engine bleibt im Quality-Point-Ordner; Projekte liegen woanders. **Aufrufmuster aller Skripte:** `python <quality_point>/engine/<skript>.py <projektordner>` (Windows auch `py`; ohne Ordnerangabe gilt der aktuelle Ordner). Jedes Projekt hat eine `quality_point.json` (Vorlage `engine/quality_point.beispiel.json`, Standardwerte in `engine/konfig.py`).
2. **Lesen, bevor du baust:** `engine/FOLIEN.md` (Folientypen, Bausteine, Schritte, Notizen, Glossar-, Quellen- und Pointenformat), `engine/TOKENS.md` (Design-Variablen, an die sich jeder Stil hält), `docs/REGELN.md` (Qualitätsregeln). Sind FOLIEN.md oder TOKENS.md im Repo noch nicht vorhanden, gelten die Kommentare in `engine/build.py`, `engine/src/basis.css (und styles/<stil>/stil.css)` und `engine/src/interaktion.js`.
3. **Einrichtungsseite öffnen – immer zuerst, noch vor der ersten Frage** (außer bei einem laufenden Projekt, siehe 4): `start.html` im Wurzelordner von Quality Point im Browser öffnen (Windows: `start "" "<pfad>\start.html"`, macOS: `open …`, Linux: `xdg-open …`). Dort ist **alles voreingestellt und erklärt**: Eckdaten, Material, Inhaltsschalter, Bauliste, 20 Stile mit Musterfolien und Schriftprobe, Bilder-Weg mit Beispielen, Veröffentlichung, Quality Response. Die Person drückt entweder „Standard übernehmen“ oder stellt ein und bekommt am Ende einen **Code** (`QP1…`) für den Chat oder eine Datei `quality_point.json`. Im Chat dazu nur zwei Sätze: „Die Einrichtungsseite ist offen – stell ein, was du willst, oder nimm den Standard; dann den Code hier einfügen (oder die gespeicherte Datei in den Projektordner legen).“ **Keine Fragen stellen, bevor der Code oder die Datei da ist.**
4. **Vorhandenes prüfen:** Gibt es im Arbeitsordner schon eine `quality_point.json`? Dann ist das ein laufendes Projekt: lesen, Stand zusammenfassen und nur nach dem Fehlenden fragen. Hat die Person im ersten Satz schon Antworten gegeben (Thema, Dauer, Material …), diese übernehmen und **nicht erneut fragen**.

---

## A · Aufnahme: Code lesen, nur Lücken erfragen

1. **Code oder Datei einlesen:** `python <quality_point>/engine/werkzeuge/code_lesen.py <projektordner> "<code>"` (oder mit dem Pfad der gespeicherten `quality_point.json`, z. B. aus dem Download-Ordner). Das Werkzeug schreibt `<projekt>/quality_point.json`; der Abschnitt `aufnahme` enthält Zielgruppe, Dauer, Material, Inhaltsschalter, Bauliste, Grafik und Veröffentlichung. Zum Nachsehen: `code_lesen.py --zeigen "<code>"`.
2. **Nur Lücken im Chat erfragen**, kompakt als eine Liste: Titel/Thema und Autor*in, falls leer; Pfade zu Dateien, die in `aufnahme.material_pfade` fehlen; bei `artikel = "vorhanden"` der Pfad; bei `grafik.weg = "generator"` der Hinweis auf die Umgebungsvariable (Schlüssel nie in Dateien, nie im Chat); bei `stil_auto` die eigene Stilwahl kurz begründen. Nichts fragen, was die Seite schon beantwortet hat.
3. **Ohne Code** (die Person will nicht klicken): dieselben Punkte in der Reihenfolge der Seite mit **AskUserQuestion** abfragen (höchstens 4 Fragen je Aufruf, Empfehlung zuerst; Wortlaut und Optionen: `docs/ABLAUF.md`). Das ist der Ausweichweg, nicht der Normalfall.
4. **Bedeutung der Werte** (`aufnahme`): `inhaltsschalter` exakt · vorlage_regie · frei · schema (+ `schema`) – siehe `docs/ABLAUF.md` Block 3. `bauliste` kann enthalten: landingpage, glossar, quellen, interaktion, videoinhalte, werkstatt, material (→ `materialien.an`), unterrichtsfolien, lehrplan (→ `lehrplan.an`, braucht Lehrplandaten), handout (+ `handout_seiten`), notizschutz (→ `notizschutz` in `quality_point.json`, PIN per `QP_NOTIZ_PIN`). `grafik.weg` vektor · generator (+ `anbieter`) · eigene. `veroeffentlichung.art` lokal · server (+ `ziel`); `veroeffentlichung.response = true` → nach dem Deploy **Quality Response** einbauen (eigenes Repo, eigener Skill: https://github.com/harubert/quality_response, braucht PHP am Server – der Person vorher sagen).
5. Danach **einmal** zusammenfassen: „So baue ich es – passt das?“ (ein Absatz, keine Rückfragen zu Dingen aus dem Code), dann Teil B.

## B · Arbeitsablauf

1. **Projekt anlegen:** `python <quality_point>/engine/neues_projekt.py <projektordner>` (weitere Argumente siehe Kopf des Skripts; macOS/Linux `python3`). Es legt `quality_point.json`, `src/slides/`, `img/` usw. an; danach die Antworten aus Teil A in `quality_point.json` eintragen.
2. **Bestandskatalog der Vorlage** (falls Vorlage): Bilder mit `bilder_extrahieren.py` (Engine-Werkzeug) in `img/orig/` ziehen (Katalog `img/orig/katalog.json`: Satz, Folie, Text, Bilddateien). Zusätzlich mit Python (zipfile) Hyperlinks (`_rels`), eingebettete und verlinkte Videos, Notizen auslesen. Ergebnis: Abgleichtabelle Original-Element → geplanter Fundort. Im Modus „exakt“ bzw. „Vorlage + Regie“ ist jede Zeile Pflicht.
3. **Gliederung vorschlagen** (Teile, Folientitel, Dauer je Teil, wo Interaktion/Werkstatt/Material sitzt) und **freigeben lassen**. Das ist die einzige Rückfrage im Ablauf.
4. **Ab hier autonom bis zum Ende** (Vorbild: claude-research). Keine Zwischenfragen wie „Soll ich …?“. Einzige Ausnahme: ein fehlender Schlüssel oder eine Rechtefrage, die du nicht selbst klären kannst.
5. **Folien bauen** nach `engine/FOLIEN.md`: pro Folie eindeutiger `data-title`, Quelle in `<cite class="src">`, ausführliche Notizen (`aside.notes`, 80 – 200 Wörter: Kern, Frage ans Publikum, Hintergrund mit Zahlen), Pointe, Glossarbegriffe. Animation nur mit Bedeutung: ein Klick = ein Gedanke. **Die Weiter-Schaltfläche zeigt die Zahl der Teilschritte („Teil 2 von 4“) – prüfen, ob diese Zahl eine Lösung verrät** (z. B. ein Schritt je richtiger Antwort, „wie viele davon sind Fakes?“ mit einem Schritt je Fake): dann die Auflösung in einen einzigen Schritt legen oder die Zählung mit `.fw` zu einem Schritt zusammenfassen.
6. **Quellen prüfen** (jede Zahl, jedes Zitat, jeder Link per WebFetch/WebSearch):
   - Jede Zahl mit Bezugsgruppe (wer, wann, wie viele) und Lesehilfe „Das heißt: …“ mit Vergleichsmaßstab.
   - Englische Zitate: Original + deutsche Übersetzung direkt darunter, **gleichzeitig eingeblendet**.
   - Bildquellen recherchieren; nicht auffindbar → „Herkunft unbekannt (Recherche ohne Ergebnis)“.
   - Zitatrecht (Analysezweck, nur so groß wie nötig, mit Herkunft) klar trennen von freier Lizenz (Lizenz + Urheber*in nennen).
   - Datenschutz: private Namen, E-Mail-Adressen, Kennzeichen unkenntlich; keine erkennbaren Kindergesichter.
7. **Zusatzseiten** laut Bauliste (Schalter in `quality_point.json`: `artikel`, `lehrplan.an`, `materialien.an`, `einheiten` für die Kacheln der Landingpage): Glossar, Quellen, Landingpage, Lehrplan, Artikel (`seiten_bauen.py`), Word-Materialien (`materialien_bauen.py`), Unterrichtsfolien (`unterricht_folien.py`), Handout (`src/handout.json` aus Folien, Notizen und Artikel verfassen – Aufbau im Kopf von `handout_bauen.py`, nichts erfinden, Zahlen mit Bezugsgruppe; dann `handout_bauen.py` → PDF in `handout/`, jede Seite ansehen; enthält es Bildzitate, nur hinter Zugangsschutz veröffentlichen), generierte Bilder (`bilder_generieren.py` im Ordner `styles/`; Schlüssel nur aus der Umgebungsvariable).
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
