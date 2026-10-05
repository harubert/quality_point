# Qualitätsregeln

Diese Regeln gelten für alles, was mit Quality Point entsteht: Folien, Notizen, Begleitseiten, Word-Materialien. Sie sind aus der Arbeit an echten Lehrveranstaltungen entstanden. Wo eine Regel mit einem Wunsch der Autor*in kollidiert, gilt der Wunsch, aber nie auf Kosten der Wahrheit oder fremder Rechte.

## 1 · Wahrheit und Belege

1. **Nichts erfinden.** Keine Zahl, kein Zitat, keine Quelle, kein Studienname ohne geprüften Beleg. Jede Quelle wird per Abruf geprüft (Seite existiert, Titel und Autor*innen stimmen, die Aussage steht wirklich drin).
2. **Unsicheres kennzeichnen.** Was nicht belegbar ist, wird weggelassen oder sichtbar markiert: „Schätzung“, „nicht geprüft“, „Zahl aus einer TV-Dokumentation, Herkunft unklar“.
3. **Legenden und Belegtes trennen.** Bekannte Anekdoten (die Popcorn-Werbung im Kino, das Goldfisch-Gedächtnis …) dürfen vorkommen, aber als solche: „Legende“, „widerlegt“, „gut erzählt, schlecht belegt“ – mit Quelle für die Widerlegung.
4. **Jede Zahl braucht eine Bezugsgruppe.** Wer wurde befragt, wann, wie viele, wo? „32 %“ allein ist keine Information; „32 % der befragten 6- bis 7-Jährigen in Deutschland (Studie, Jahr, Stichprobengröße n)“ schon.
5. **Lesehilfe „Das heißt: …“.** Zu jeder wichtigen Zahl ein Satz, der sie greifbar macht, mit Vergleichsmaßstab: „Das heißt: In einer Klasse mit 24 Kindern sind das etwa 8.“
6. **Effektstärken mit Vergleichsmaßstab.** d, r, Odds Ratio usw. nie nackt. Einordnung nach üblichen Konventionen (z. B. Cohen: d = 0,2 klein, 0,5 mittel, 0,8 groß) und, wo möglich, mit einem anschaulichen Vergleich. Korrelation ist nicht Kausalität – das steht dabei, wenn es naheliegt, es zu verwechseln.
7. **Fremdsprachige Zitate:** Original und deutsche Übersetzung direkt darunter, **gleichzeitig eingeblendet** (nicht in getrennten Animationsschritten). Übersetzung als solche kennzeichnen („Übers.: …“).
8. **Originalfolien der Autor*in nie als Quelle zitieren.** Formulierungen wie „Seminarpräsentation“, „laut Originalfolie“, „aus MP3“ sind verboten. Die Inhalte der Vorlage sind das Werk der Autor*in und werden einfach gebracht; Belege kommen aus den eigentlichen Quellen (Studie, Gesetz, Website).
9. **Quellenform:** APA 7 im Quellenverzeichnis; auf der Folie kurz in `<cite class="src">` (`Nachname (Jahr)`, `Nachname & Nachname (Jahr)`, `Nachname u. a. (Jahr)`). Eigene Darstellungen sind als solche erkennbar.
10. **Links prüfen.** Tote oder umgeleitete Links werden ersetzt; Videos über die oEmbed-Schnittstelle bzw. Seitenabruf geprüft. Ist ein Video verschwunden, wird ein inhaltsgleicher Ersatz gesucht und das in den Notizen vermerkt.

## 2 · Bilder, Rechte, Datenschutz

1. **Herkunft jedes Bildes klären.** Fotos ohne Angabe werden recherchiert (Bildsuche, Motivdetails, Schriftzüge, Hersteller- und Pressearchive, Wikimedia Commons). Kein Ergebnis → „Herkunft unbekannt (Recherche ohne Ergebnis)“. Die Bilder-Herkunftsübersicht listet alle Fälle.
2. **Zitatrecht oder freie Lizenz – nie vermischen.**
   - *Zitatrecht* (fremde Screenshots, Werbemotive, Zeitungsausschnitte): nur mit Analysezweck auf der Folie, nur so groß wie nötig, mit Herkunft. Für Veröffentlichung Zugangsschutz empfehlen.
   - *Freie Lizenz* (CC BY, CC BY-SA, CC0 …): Urheber*in, Lizenz und Link angeben, Bearbeitungen vermerken.
3. **Generierte Bilder** werden als solche gekennzeichnet (in der Herkunftsübersicht) und auf Fehler geprüft: Hände, Schrift, Symbole, Klischees, ungewollte Markenlogos.
4. **Datenschutz:** private Namen, E-Mail-Adressen, Telefonnummern, Kennzeichen, Adressen unkenntlich machen oder weglassen. **Keine erkennbaren Kindergesichter.** Kinderzeichnungen sind in Ordnung, ohne Namen.
5. **Videos:** keine eingebetteten Fremd-Videodateien im Webpaket. Online-Videos werden verlinkt (Standbild, Titel, Länge, Beobachtungsauftrag, `target="_blank" rel="noopener"`). Lokale Kopien liegen nur in `video_lokal/` am Vortragsrechner.
6. **Keine Geheimnisse im Paket.** API-Schlüssel nur als Umgebungsvariable. `deploy.py` prüft das Webpaket gegen eine Sperrliste (Schlüsselmuster, lokale Pfade, private Adressen, CDNs) und bricht bei Treffern ab. Die Sperrliste wird nicht gelockert, die Ursache wird entfernt.

## 3 · Sprache und Typografie

1. **Gendern mit Stern:** Schüler*innen, Lehrer*innen, Autor*innen. Nicht Doppelpunkt, nicht Binnen-I, kein generisches Maskulinum (sofern die Autor*in nichts anderes festlegt).
2. **Bis-Strich mit Leerzeichen:** „12 – 17 Jahre“, „S. 45 – 52“ (im Quellenverzeichnis nach APA ohne Leerzeichen). `build.py` und `bisstrich_docx.py` setzen das automatisch, prüfen schadet nicht.
3. **Halbgeviertstrich „–“** als Gedankenstrich, kein Geviertstrich „—“. `build.py` warnt.
4. **Typografische Anführungszeichen:** im Deutschen „…“ und ‚…‘, im Englischen “…”. Keine geraden " im Text. `build.py` warnt.
5. **Geschütztes Leerzeichen** vor % und ‰ sowie zwischen Zahl und Einheit, damit nichts allein in die nächste Zeile rutscht.
6. **Klar und konkret.** Kurze Sätze, Verben statt Substantivierungen, Beispiele und Zahlen statt Allgemeinplätzen. Keine Floskeln („Es ist wichtig zu beachten …“, „Zusammenfassend lässt sich sagen …“). Keine Emojis im Fließtext.
7. **Sprachvariante** einhalten (Standard: Deutsch, österreichische Variante – „Jänner“, „heuer“, „Matura“).

## 4 · Didaktik

1. **Lernziele operationalisiert:** „Die Schüler*innen können … benennen / unterscheiden / begründen / gestalten.“ Beobachtbare Verben, keine „verstehen“ oder „kennenlernen“ als Ziel.
2. **Unterrichtsmaterial** enthält: Feinziele, didaktische Analyse nach Klafki (Gegenwartsbedeutung, Zukunftsbedeutung, exemplarische Bedeutung, Struktur des Inhalts, Zugänglichkeit), Ablauf mit Zeiten, Arbeitsauftrag für die Schüler*innen, Differenzierung, **Lösungen mit Begründung**.
3. **Zu jeder Ankreuz-, Zuordnungs- oder Schätzaufgabe gibt es eine Lösung** – auf der Folie (Auflösen-Knopf, letzter Schritt) und im Material.
4. **Werkstatt-Aufträge** sind konkret: Was, mit wem, wie lange, welches Produkt am Ende.
5. **Animation nur mit Bedeutung.** Ein Klick = ein Gedanke. Lieber 3 – 5 Schritte als 12. Effekte, die nichts erklären, fallen weg.
6. **Notizen sind der ausführliche Teil:** 80 – 200 Wörter je Folie mit Kern, Frage ans Publikum, Hintergrund mit Zahlen und Quelle.

## 5 · Gestaltung und Barrierefreiheit

1. **Kontrast** mindestens WCAG AA (4,5 : 1 für Text, 3 : 1 für große Schrift und Grafikelemente). Alle Stile in `styles/` sind darauf ausgelegt; eigene Farben nachprüfen.
2. **Schriftgrößen** auf der Bühne 1920 × 1080: Fließtext nicht unter 28 px, Bildunterschriften und Quellen nicht unter 20 px. Lieber eine Folie mehr als zu kleine Schrift.
3. **Information nie nur über Farbe** (zusätzlich Form, Beschriftung, Muster).
4. **Alternativtexte** für alle inhaltlichen Bilder; reine Dekoration mit leerem `alt=""`.
5. **Lesbarkeit:** linksbündig, Zeilenlänge begrenzt, keine Textblöcke über ganze Bildschirmbreite, keine Schrift über unruhigem Bild ohne Abdunklung.
6. **Bewegung sparsam;** Animationen sind kurz und lösen kein Flackern aus.
7. **Keine Google Fonts und keine CDNs zur Laufzeit.** Schriften (WOFF2, SIL Open Font License) und Skripte liegen lokal. So funktioniert die Präsentation offline und ohne Datenabfluss an Dritte.
8. **Nichts ragt über den Rand.** `pruefen.py` muss „OK“ melden; Screenshots jeder geänderten Folie werden im Endzustand angesehen.

## 6 · Prüfliste vor der Abgabe

- [ ] Jede Zahl mit Bezugsgruppe, Quelle und „Das heißt: …“?
- [ ] Jede Quelle abgerufen und geprüft, kein toter Link?
- [ ] Keine Originalfolie als Quelle zitiert?
- [ ] Englische Zitate mit Übersetzung, gleichzeitig sichtbar?
- [ ] Bildherkunft geklärt oder als unbekannt markiert, Zitatrecht vs. Lizenz sauber?
- [ ] Keine privaten Daten, keine Kindergesichter?
- [ ] Bis-Strich, Anführungszeichen, Genderstern, keine Geviertstriche (`build.py` ohne Warnungen)?
- [ ] Lernziele operationalisiert, Lösungen vorhanden?
- [ ] `pruefen.py` meldet „OK“, Screenshots angesehen?
- [ ] `deploy.py` ohne Sperrlisten-Treffer, keine Schlüssel, keine CDN-Aufrufe?
- [ ] Im Modus „exakt“ bzw. „Vorlage + Regie“: Abgleichtabelle vollständig, Ausnahmen begründet?
