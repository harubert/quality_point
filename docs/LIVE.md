# Quality Point Live – Mitmachen über den Server

Quality Point läuft normalerweise als reines HTML: Doppelklick, USB-Stick, Lernplattform, beliebiger Webspace – nichts wird gespeichert. Der **Server-Modus** ergänzt das um Mitmach-Funktionen für das Publikum. Beides entscheidet die Person, die die Präsentation baut (Frage „Betriebsart“ in der Aufnahme).

| | Standalone | Server mit Live |
|---|---|---|
| Läuft auf | jedem Gerät, auch offline | Webspace mit PHP |
| Teilnehmer*innen | sehen den Beamer | haben die Folien am eigenen Gerät, folgen dem Vortrag |
| Interaktionsbausteine | am Vortragsrechner (Handzeichen zählen, eintippen) | Antworten von allen Geräten, Ergebnisse live |
| Hinweise aus dem Publikum | mündlich | anonym als Text, poppen bei der Referentin / dem Referenten auf |
| Stimmungsbarometer | – | Tempo, Verständlichkeit, Relevanz, Stimmung, Lautstärke, Pause – live und als Verlauf |
| Gespeichert wird | nichts | anonyme Kennung je Gerät, Antworten, Hinweise, Barometerwerte (auf dem eigenen Server) |

## Was entsteht

- `praesentation.html` – Referentenfassung wie bisher (Notizen, Pointen, Referentenfenster), zusätzlich Anmeldung und **Live-Panel** (Taste `A`).
- `teilnehmer.html` – Teilnehmerfassung: ohne Notizen und Pointen, ohne Folien mit `data-nur="referent"`, ohne Lösungen der Bausteine. Darunter die **Mitmach-Leiste** mit den Reitern Stimmung, Hinweis, Aufgabe.
- `index.html` – Startseite mit „▶ Präsentation starten (Referent*in)“, „Mitmachen (Teilnehmer*innen)“ und **QR-Code** zur Teilnehmerfassung.
- `live/api.php` – der ganze Server-Teil, eine Datei. `live/daten/` – Datenordner (JSON/JSONL), per `.htaccess` gesperrt.

## Voraussetzungen (Rahmenbedingungen)

- **PHP 8.0 oder neuer** (mbstring empfohlen, nicht nötig). Keine Datenbank, keine Zusatzpakete.
- **Schreibrecht** des Webservers auf `live/daten/` (Dateien werden dort angelegt und mit Dateisperren geschrieben).
- **Apache mit `.htaccess`** (`Require all denied` im Datenordner liegt bei). Bei nginx den Ordner selbst sperren, z. B. `location ~ ^/.*/live/daten/ { deny all; }`. Prüfen: `…/live/daten/einstellungen.json` muss im Browser **403** liefern.
- **HTTPS**, damit Hinweise und Passwort nicht im Klartext reisen; das Sitzungscookie wird dann als `secure` gesetzt.
- Alles unter **einer Adresse** (gleicher Host, gleicher Ordner) – die Seiten rufen `live/api.php` relativ auf.
- Beim **Hochladen eines neuen Stands** den Ordner `live/daten/` am Server **nicht löschen**, sonst sind Passwort, Antworten und Hinweise der laufenden Sitzung weg. `deploy.py` lässt den lokalen Datenordner ebenfalls stehen.
- Läuft die Präsentation hinter einem eigenen Zugangsschutz (z. B. Code-Abfrage), gilt der für Teilnehmer*innen genauso – den Code also mit dem QR-Code bekannt geben.

## Passwort der Vortragenden

`deploy.py` schreibt den Passwort-Hash nach `live/daten/zugang.json`:

1. Umgebungsvariable `QP_LIVE_PASSWORT` (empfohlen; z. B. PowerShell `$env:QP_LIVE_PASSWORT="…"`),
2. sonst `live.passwort` in `quality_point.json` (dann steht es im Projektordner – nicht in ein öffentliches Repo legen),
3. sonst erzeugt `deploy.py` ein Startpasswort wie `tafel-4821` und zeigt es **einmal** an.

Ändern: Live-Panel → Einstellungen → Passwort ändern. Nach fünf Fehlversuchen wartet die Anmeldung eine Minute. Die Anmeldung gilt für den Browser-Tab (Sitzungscookie, `HttpOnly`, `SameSite=Lax`).

## Ablauf im Hörsaal

1. Startseite öffnen → „Präsentation starten (Referent*in)“ → Passwort. Von da an ist der Vortragsrechner die Quelle: Jede Folie und jeder Teilschritt wird gemeldet.
2. QR-Code zeigen (Startseite oder Live-Panel → Übersicht). Teilnehmer*innen öffnen `teilnehmer.html`, tippen „Los geht’s“ und sehen die aktuelle Folie; ihre Navigation ist gesperrt, solange „Folien folgen dem Vortrag“ eingeschaltet ist.
3. Rechts unten zeigt ein Badge die Zahl der Teilnehmer*innen und neue Hinweise; ein Hinweis poppt kurz auf. `A` öffnet das Panel:
   - **Übersicht** – online, fertig auf dieser Folie, offene Hinweise, Barometer (letzte 15 Minuten, je Person der jüngste Wert), QR-Code.
   - **Hinweise** – chronologisch mit Art (Frage, Hinweis, Fehler, Ergänzung) und Folie; „Auf der Folie zeigen“ legt den Text groß über die Folie (als Beitrag nutzen), „Zur Folie“, „Erledigt“.
   - **Ergebnisse** – Bausteine der aktuellen Folie: Zahl der Antworten, Ergebnis für Teilnehmer*innen freigeben/verbergen, Antworten löschen. Die Ergebnisse selbst stehen im Baustein auf der Folie (Balken, Median, Wolke …).
   - **Verlauf** – Barometer über die Zeit je Kategorie, Export als JSON/CSV (anonym).
   - **Einstellungen** – folgen/frei, Hinweise an/aus, Fertig-Knopf, Barometer-Kategorien, Standard für Ergebnisse (sofort / erst nach Freigabe / nie), Sitzung zurücksetzen, Passwort.
4. Bausteine auf Folien: „Auflösen“ bzw. „Prüfen“ beim Referenten gibt zugleich die Lösung für Teilnehmer*innen frei.

## Bausteine mit Live-Funktion

`ia-umfrage` (Einfach-/Mehrfachwahl mit Balken, optional richtige Antwort), `ia-schaetz` (Schätzregler: Verteilung und Median), `ia-quiz` (echt/fake), `ia-wolke` (Wortwolke aus allen Begriffen), `ia-ampel` (Ja/Unentschieden/Nein), `ia-sort` (Zuordnen: Anteil richtiger Zuordnungen). Ohne Server laufen dieselben Bausteine am Vortragsrechner. Steuerung je Baustein über `data-ergebnis="sofort|freigabe|nie"`; Beschreibung in `engine/FOLIEN.md`.

## Datenschutz

- Teilnehmer*innen bleiben **anonym**: Das Gerät erzeugt eine Zufallskennung (im Browser gespeichert), damit eine Person je Frage nur einmal zählt. Keine Namen, keine Anmeldung, keine IP-Adressen in den Daten (nur die Sperre nach Fehlversuchen beim Passwort merkt sich kurz die IP).
- Gespeichert werden Barometerwerte, Antworten, Fertig-Meldungen und die **Texte der Hinweise** – darauf vor Beginn hinweisen („Bitte keine Namen in Hinweise schreiben“). Im Export sind die Kennungen zusätzlich gekürzte Prüfsummen.
- Eigene Hinweise sieht eine Person nur auf dem eigenen Gerät (Browser-Speicher) wieder.
- **Sitzung zurücksetzen** (Panel → Einstellungen) löscht alle gesammelten Daten; vor der nächsten Veranstaltung empfohlen. Der Datenordner lässt sich auch einfach leeren.

## Grenzen

- Abgleich per Abfrage alle 3 – 4 Sekunden (kein WebSocket) – robust auf jedem Webspace, Verzögerung von wenigen Sekunden ist normal.
- Ausgelegt für Seminar- bis Hörsaalgröße (einige hundert Geräte); Dateien statt Datenbank.
- Teilnehmer*innen vertrauen dem eigenen Gerät: Wer die Kennung im Browser löscht, kann erneut abstimmen. Für Prüfungen ist das Modul nicht gedacht.
- Ohne Server-Modus gibt es keine Teilnehmerfassung; der Umschalter ist `live.an` in `quality_point.json`, danach `deploy.py` neu ausführen.
