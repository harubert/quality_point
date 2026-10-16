# Funktionen im Überblick

Was eine mit Quality Point gebaute Präsentation kann – für alle, die damit vortragen, unterrichten oder sie weitergeben. Die Präsentation ist **eine HTML-Datei** (`praesentation.html`), die in jedem aktuellen Browser läuft, offline und ohne Installation. In der Präsentation zeigt **`H`** (oder **`?`**) jederzeit alle Tasten.

## Vortragen

| Funktion | Bedienung | Hinweise |
|---|---|---|
| Weiter / zurück | `→` `Leertaste` / `←`, Wischen am Touchscreen | ein Schritt = ein Gedanke; Folien haben Teilschritte |
| Ganze Folie vor/zurück | `Umschalt` + `→` / `←` | überspringt die Teilschritte |
| Steuerleiste | Knöpfe am unteren Rand | SVG-Pfeile; der Knopf füllt sich mit jedem Teilschritt, man sieht also, wie viel von der Folie noch kommt. Solange Teilschritte offen sind, gibt es zusätzlich „ganze Folie zurück“. |
| Direkt springen | Ziffern + `Enter` | z. B. `47` `Enter` |
| Folie per Adresse | `praesentation.html#47` oder `#47.2` | Folie 47, Schritt 2; funktioniert auch bei schon geöffneter Präsentation – praktisch für Links aus Materialien und Mails |
| Übersicht | `O` | alle Folien als Kacheln, mit Suche über Titel und Text |
| Vollbild | `F` | |
| Schwarzbild | `B` oder `.` | Bildschirm schwarz mit dezentem Hinweis, wie es weitergeht; viele Presenter-Fernbedienungen senden `.` |
| Hilfe | `H` oder `?` | Tastentabelle mit Tipps für den Hörsaal |

## Referentenansicht und zwei Bildschirme

| Funktion | Bedienung | Hinweise |
|---|---|---|
| Notizleiste | `N` | Notizen neben der Folie, die Folie rückt zur Seite |
| Referentenansicht | `P` | eigenes Fenster mit Notizen, nächster Folie, Uhr und Timer |
| Zwei-Bildschirm-Modus | `S` | Folien als Vollbild auf dem Beamer, Notizfenster am Laptop. Chrome oder Edge, Windows und macOS (Window-Management-API; der Browser fragt einmal nach der Erlaubnis „Fensterverwaltung“). In Safari/Firefox: Fenster auf den Beamer ziehen, `F`, dann `P`. |
| Folie groß im Notizfenster | `V` | zwischen Notizen und großer Folie umschalten |
| Notizschrift | `+` / `−` | |
| Timer zurücksetzen | `R` | |

Gesteuert wird aus beiden Fenstern; sie bleiben synchron. Tipp: Beamer als **erweiterten** Bildschirm anschließen, nicht spiegeln.

Presenter und Tastatur: Nach jedem Tastendruck erscheint für 1,6 s nur die Weiter-Schaltfläche mit den Teilschritten („Teil 2 von 4“), auch wenn die Steuerleiste ausgeblendet ist – so weiß man, ob die Folie noch Schritte hat.

## Zeigen und Markieren

| Funktion | Bedienung | Hinweise |
|---|---|---|
| Stifte | `Z` | Malstift, Leuchtstift, Emoji-Stempel, Radierer; Maus, Stift oder Finger |
| Spotlight | `X` | alles abdunkeln bis auf einen Lichtkreis; Mausrad ändert die Größe |
| Laserpointer | `L` | |
| Bildansicht mit Lupe | Bild anklicken | großes Bild mit Lupe; `+`/`−` zoomen, Pfeile verschieben, `0` einpassen, `W` volle Breite, Ziehen verschiebt |
| Pointen-Banner | `K` | blendet die Kernaussage („Pointe“) der Folie ein bzw. aus |
| Zähler | automatisch | Kennzahlen zählen beim Aufrufen der Folie hoch |

## Wissen und Quellen

| Funktion | Bedienung | Hinweise |
|---|---|---|
| Glossar | `G`, oder Begriff auf der Folie anklicken | Popover mit Erklärung in einfachen Worten, ggf. mit Quelle |
| Quellenlinks | Quellenangabe anklicken | springt ins Quellenverzeichnis am Ende; **↗** öffnet das Original; ein Knopf führt zurück zur Folie |
| Sprungkarten | Karte anklicken | springt zu einer verwandten Folie und bietet den Rücksprung an |
| Video-Inhaltsangaben | Videokarte | Standbild, Titel, Länge, Beobachtungsauftrag, geprüfter Link (öffnet in neuem Tab) |
| Lokale Videokopien | Knopf auf der Videokarte | nur am Vortragsrechner: liegt eine Datei in `video_lokal/`, erscheint ein Abspielknopf; online gibt es den Ordner nicht, das Webpaket bleibt schlank und rechtlich sauber |

## Interaktionsbausteine

Alle laufen im Browser ohne Server und ohne Konto. Sie eignen sich für Präsenz; Ergebnisse werden nicht gespeichert oder übertragen.

| Baustein | Wofür |
|---|---|
| Schätzregler | Publikum schätzt eine Zahl, dann „Auflösen“ |
| Vorher-nachher | Schieberegler zwischen zwei Bildern (z. B. Original und Retusche) |
| Ausschnitt | erst ein Bildausschnitt, dann das ganze Bild |
| Echt oder Fake | Abstimmung mit Zählern, dann Auflösung mit Erklärung |
| Zuordnen | Karten in Felder ziehen oder antippen |
| Timer | für Arbeitsphasen, mit „+1 Min.“ |
| Zufallsrad | Gruppen, Fragen, Reihenfolgen auslosen |
| Wortwolke | Begriffe eintippen, die Wolke wächst |
| Karteikarte | Vorderseite Frage, Rückseite Antwort |
| QR-Code | Link oder diese Folie aufs Handy (lokal erzeugt) |
| Ampel | rot/gelb/grün-Stimmungsbild mit Zählern |

## Live mitmachen (Server-Modus, optional)

Mit `live.an` in `quality_point.json` entsteht zusätzlich eine **Teilnehmerfassung** (`teilnehmer.html`) und ein kleiner Server-Teil (`live/api.php`, PHP 8, keine Datenbank). Teilnehmer*innen scannen den QR-Code der Startseite; die Folien laufen am eigenen Gerät mit.

| Für Teilnehmer*innen | Für Vortragende |
|---|---|
| Folien folgen dem Vortrag (oder frei blättern, einstellbar) | Anmeldung mit Passwort über „Präsentation starten (Referent*in)“ |
| Stimmungsbarometer: Tempo, Verständlichkeit, Relevanz, Stimmung, Lautstärke, Pause (einzeln schaltbar) | Badge rechts unten: Teilnehmer*innen online, neue Hinweise; Hinweise poppen auf |
| Hinweise, Fragen, Fehler, Ergänzungen zur aktuellen Folie (anonym; eigene bleiben am Gerät sichtbar) | Live-Panel (`A`): Übersicht mit Barometer-Verteilungen, Hinweise („Auf der Folie zeigen“ als Beitrag), Ergebnisse je Baustein mit Freigabe, Verlauf über die Zeit mit Export, Einstellungen |
| „Fertig“-Knopf auf Aufgabenfolien | sieht, wie viele fertig sind |
| Umfragen, Schätzen, Echt/Fake, Wortwolke, Ampel, Zuordnen am eigenen Gerät | Ergebnisse direkt im Baustein auf der Folie; Auflösen gibt die Lösung frei |

Standalone bleibt der Normalfall: ohne `live.an` ändert sich nichts. Voraussetzungen, Datenschutz und Grenzen: `docs/LIVE.md`.

## Begleitseiten und Materialien (je nach Bauliste)

| Seite / Datei | Inhalt |
|---|---|
| Landingpage (`index.html`) | Startseite mit allen Teilen, Einheiten, Materialien, Links zu Glossar, Quellen, Artikel |
| Glossar (`glossar.html`) | alle Fachbegriffe, alphabetisch, verlinkt |
| Quellen (`quellen.html`) | Quellenverzeichnis (APA 7), aus dem Fachartikel und den Zusatzquellen |
| Lehrplan (`lehrplan.html`) | Bezug zu Lehrplan-Stellen, sofern Lehrplan-Daten vorliegen |
| Fachartikel (`artikel.html`) | aus claude-research übernommen, mit klickbaren Zitaten |
| Word-Materialien (`formulare/`) | Arbeitsblätter mit Feinzielen, didaktischer Analyse nach Klafki, Ablauf und Lösungen mit Begründung; optional Bilder bzw. Bildraster, Seitenumbruch vor einer Aufgabe (Auflösung erst nach dem Umblättern), Aufzählungen ohne Ankreuzkästchen |
| Unterrichtsfolien | je Material eine Folie „Im Unterricht: …“ mit Illustration, Ablauf und Download |
| Handout (`handout/*.pdf`) | A4-PDF im Design der Präsentation: Titelseite mit QR-Code, Kernaussagen, Kapitel mit Kernaussage, Beispielen, Bildern und „Fragestellungen für die eigene Kompetenzentwicklung“, gesamte Literaturliste (`handout_bauen.py`, Druck über Edge/Chrome) |
| Bilder-Herkunftsübersicht | alle Bilder mit Herkunft, Lizenz bzw. Zitatrecht, generiert oder „Herkunft unbekannt“ |

## Werkzeuge für Autor*innen

Alle Skripte liegen im Quality-Point-Ordner unter `engine/` und werden mit dem Projektordner aufgerufen: `python engine/<skript>.py <projektordner>`. Einstellungen stehen in der `quality_point.json` des Projekts.

| Werkzeug | Zweck |
|---|---|
| `neues_projekt.py` | legt ein neues Projekt mit `quality_point.json` und Ordnergerüst an |
| `build.py` | baut `praesentation.html` aus Hülle, Stil, Folien, Glossar, Quellen, Pointen; warnt bei Typografie-Fehlern |
| `pruefen.py` | öffnet die Präsentation headless in Edge/Chrome, deckt alle Schritte auf und meldet alles, was über den Rand ragt; Ziel: „OK“ |
| `screenshot.py` | Screenshots einzelner Folien und Schritte (`5.3`) plus Kontaktbogen |
| `bilder_extrahieren.py` | Bilder und Katalog aus einer vorhandenen PPTX (Bestandskatalog) |
| `quellen_bauen.py` | Quellenverzeichnis aus den zitierten Quellen |
| `seiten_bauen.py` | Landingpage, Glossar, Lehrplan, Artikel, Quellen |
| `materialien_bauen.py`, `bisstrich_docx.py` | Word-Materialien bauen bzw. typografisch korrigieren |
| `unterricht_folien.py` | Unterrichtsfolien je Material |
| `deploy.py` | baut den Veröffentlichungsordner nur aus einer Positivliste und bricht bei Sperrlisten-Treffern ab (Schlüssel, lokale Pfade, private Adressen, CDNs) |
| `styles/index.html` | Stilauswahl: 10 Stile × 10 Schriftsets |
| `bilder_generieren.py` (in `styles/`) | generierte Bilder per API-Schlüssel (aus Umgebungsvariable) |

## Datenschutz und Technik

- Keine externen Schriften, keine CDNs, keine Tracker: die Präsentation lädt zur Laufzeit nichts von fremden Servern (außer Links, die man selbst anklickt).
- Läuft direkt vom Dateisystem (Doppelklick) oder von jedem Webspace.
- **Notizschutz (optional):** Im veröffentlichten Paket sind Sprechernotizen und Pointen verschlüsselt (AES-GCM); N, P, S und V fragen zuerst eine PIN ab, danach bleibt der Browser-Tab freigeschaltet. Einschalten mit `"notizschutz": {"bis": "JJJJ-MM-TT"}` in `quality_point.json`, PIN in der Umgebungsvariable `QP_NOTIZ_PIN`. Eine kurze PIN hält Neugierige ab, keinen gezielten Angriff; nach dem Stichtag einmal neu veröffentlichen.
- Optimiert für 16 : 9 (Bühne 1920 × 1080), skaliert auf jede Bildschirmgröße.
