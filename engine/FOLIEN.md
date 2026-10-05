# Folien-Markup (Quality Point)

Projekt: `src/slides/*.html` (alphabetisch zusammengefügt), Bühne 1920 × 1080 px. Bauen: `python engine/build.py <projekt>`.

## Folie
```html
<section class="slide" data-chap="Teil 1" data-title="Eindeutiger Titel">
  <div class="kick">Teil 1</div>
  <h2>Überschrift mit <em>Akzent</em></h2>
  …
  <cite class="src">Muster (2024); Beispiel &amp; Anders (2020, S. 4)</cite>
  <aside class="notes"><p><span class="lbl">Kern</span>…</p></aside>
</section>
```
- `data-title`: eindeutig; Schlüssel für Pointen, `data-nach`, `jump`. `data-chap`: Kapitel in der Fußzeile ab hier.
- Folientypen (zusätzliche Klasse): `s-title` (`.tt`, `h1`, `.sub`, `.who`, optional `img.hero`), `s-chapter` (`img.hero` + `.etikett` mit `.kick/h2/.lead/.toc`, oder ohne Bild mit `.bignum`), `s-statement` (`.big`), `s-dark`, `s-auftrag` (`.wk .wn/.wl`, `.panel h4`, `.meta span`).
- Bausteine: `.card` (+`t/c/r/y`, `.num`, `.tape`), `.box.def/.res/.tip/.daz` mit `.bh`, `.quote` (+`cite`), `table.tbl` (`.compact`), `ul.dots`, `ol.steps` (`.red/.y`), `.tag`, `.wcard`, `.chat .bub.l/.r/.x`, `.flips .flip .in .fa/.fb`, `.fax .fh/.fb/.ff`, `.pool4 .pc`, Raster `.row .col .g2 .g3 .g4 .grow .fill .mt .mt2 .tc .mut .small .lead`.
- `cite.src` wandert in die Fußzeile („Quelle:“); `cite.src.nolabel` ohne Präfix. Kürzel + Jahr werden mit dem Verzeichnis verlinkt.
- Notizen `aside.notes`; Labels `<span class="lbl">Kern</span>`, `lbl q` (Frage), `lbl v` (Material/Steuerung), `lbl z` (Video).

## Schritte und Animation
- `.f` = Fragment (ein Klick je Element); `.fs` = Schritt ohne eigene Einblendung (nur Zustand); `.fw` = erscheint mit dem vorigen Fragment. Richtung: `fl fr fz fb fo`. Reihenfolge: `data-o="2"`. Folie mit `dim-past`: frühere Fragmente abgedunkelt.
- `st-N`: Die Folie bekommt `st-1 … st-N`, sobald Schritt N erreicht ist → Zustände per CSS in einem `<style>` auf der Folie, z. B. `.meine.st-2 .pfeil{opacity:1}`.
- Auto beim Betreten: `.a`/`.az` mit `data-d="0.4"`; `.draw` (SVG-Linie), `.mark`, `.type` (`--n`), `.strike`, `.morph` (2 `span`), `.pulse`, `.shake`, `.out` – jeweils mit `.f` (Schritt) oder `.auto`.
- Zähler: `<span class="count" data-to="42" data-from="0" data-dec="1" data-dur="1400">0</span>` (läuft beim Aufruf der Folie).
- Balken: `<div class="bars"><div class="bz f"><span>Label</span><div class="bt"><i style="--w:51%"></i></div><span class="bv">51 %</span></div></div>` (`bz t` = Zweitfarbe; `bars auto` ohne Klick). Kennzahl: `.zahl` (+`small`), `.zl`.

## Text-Bausteine
- Lesehilfe unter Kennzahlen: `<p class="lesehilfe"><span class="lh">→</span>Das heißt: …</p>`.
- Übersetzung unter fremdsprachigem Zitat: `<p class="ueb">„…“</p>` (Präfix „Übersetzung:“ automatisch).
- Notiz-Zettel: `<div class="zettel" style="--r:2deg">…</div>`.

## Bilder, Sprünge, Video, Material
- Foto mit Lupe: `<figure class="foto zoom contain" data-img="img/x.webp" data-cap="Bildunterschrift" data-url="https://…" style="--r:-1deg;width:600px;height:400px"><img src="img/x.webp" alt="…"></figure>` (`contain` = ganz zeigen, sonst beschnitten; `zoom` = Klick öffnet Lupe).
- Sprungkarte: `<a class="card jump" data-to="data-title der Zielfolie">…</a>` (Rücksprung-Knopf erscheint).
- Lokale Videokopie (nur Vortragsrechner, `video_lokal/` wird nicht veröffentlicht): `<a class="vlokal" data-lokal="video_lokal/clip.mp4" hidden>▶ Lokale Kopie</a>`. YouTube-Links + `src/video_inhalte.json` (`{"<id>": {titel, kanal, dauer, datum, kurz, punkte[], zitate[], basis}}`) → Knopf „Video-Inhalt lesen“.
- Material-Links: `<div class="matlinks" data-thema="schluessel"></div>` (oder `class="matlinks matgrid"`); `schluessel` → quality_point.json `themen` → Feld `thema` der Materialien; `alle` = alle.
- SVG-Bausteine: `{{name}}` → `src/snippets/name.svg`.

## Interaktion (src/interaktion.js)
`ia-schaetz` (`data-frage data-wert data-min data-max data-einheit data-schritt`), `ia-vergleich` (`data-a data-b data-la data-lb`), `ia-ausschnitt` (`data-img data-x data-y data-w data-h` in %), `ia-quiz` (`data-loesung="echt|fake" data-text`, Bild als Kind), `ia-sort` (`data-felder="A|B"`, Kinder `<span data-ziel="A">`), `ia-timer` (`data-min`), `ia-rad` (`data-items="a|b|c"`), `ia-wolke` (`data-frage`), `ia-karte` (`data-vorne data-hinten`), `ia-qr` (`data-url data-text`; ohne URL: diese Folie), `ia-ampel` (`data-frage`). Spotlight: Taste X.

## Projektdateien
- **Pointen** `src/pointen*.txt`: Blöcke durch Leerzeile; Zeile 1 = `data-title`, `Z:` Zweck (Notizkopf), `P:` Pointe (Banner, Taste K). `#` = Kommentar.
- **Glossar** `src/glossar*.txt`: `Begriff | Form 2 | Form 3`, darunter `E: Erklärung`, optional `Q: quellen-id`. Erstes Vorkommen je Folie wird anklickbar (nicht in Überschrift h1, cite, a, svg).
- **Quellen** `src/quellen_extra*.json`: `[{"id","key","year","kind":"doi|web|suche","html","text","doi","url","match"?}]`; `key` = Kürzel auf der Folie, `match` unterscheidet gleiche Kürzel+Jahr. Nur zitierte Quellen kommen ins Verzeichnis (`src/slides/95_quellen.html`, automatisch).
- **Einfügen** `src/einfuegen_*.html.txt`: Folien mit `data-nach="<data-title>"` werden hinter diese Folie gesetzt (auch die erzeugten Unterrichtsfolien).
- **Material** `material/*.json` → `materialien_bauen.py` (Schema im Dateikopf, Beispiel `engine/material/beispiel.json`); Feld `nach` erzeugt eine Unterrichtsfolie (`unterricht_folien.py`), Bild optional `img/unterricht/<id>.webp`.
- **Lehrplan** `daten/lehrplan.json` (quality_point.json `lehrplan.an`): `{titel, kick?, einleitung, abschnitte:[{titel, text?, zitate:[{text, fundstelle, seite, verifiziert}], tabelle?:{spalten[], zeilen[[]], filter_spalte?}}], quellen:[{titel, url, abgerufen}]}`.
- Eigenes CSS nur für dieses Projekt: `src/projekt.css` (nach dem Stil geladen).

## Tasten
→ / Leertaste / Bild↓ weiter · ← / Bild↑ zurück · Umschalt+Pfeil ganze Folie · Pos1/Ende · Ziffern + Enter: Folie direkt ·
B oder . schwarz · F Vollbild · P Referentenfenster · S zwei Bildschirme (Notizen hier, Folien auf Beamer) · V im Notizfenster große Folie ·
Z Stifte · X Spotlight · N Notizleiste · +/− Notizschrift · O Übersicht mit Suche · H Hilfe · G Glossar · L Laserpointer · K Pointe-Banner aus/ein ·
R Timer zurücksetzen · Esc schließt Ebenen. Adresse `#5.2` = Folie 5, Schritt 2; `?notes` öffnet Notizen; `?check` = Layoutprüfung (pruefen.py).
