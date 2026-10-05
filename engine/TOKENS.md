# Token-Vertrag (CSS-Variablen)

`engine/src/basis.css` färbt und setzt Schriften **nur** über diese Variablen. Ein Stil
(`styles/<stil>/stil.css`) wird **nach** `basis.css` und `interaktion.css` geladen, definiert die
Pflicht-Tokens in `:root` und darf danach beliebige Regeln überschreiben (Dekoration, Folientypen).
Die `:root`-Blöcke des Stils werden auch für die Begleitseiten (index, glossar, quellen, lehrplan)
übernommen; seitenspezifische Dekoration gehört in `styles/<stil>/seiten.css` (optional).

## Pflicht (jeder Stil definiert sie)

| Token | Bedeutung |
|---|---|
| `--paper` | Folienhintergrund, Seitenhintergrund |
| `--paper2` | zweite Fläche: Leisten, Balkenspur, Tabellenstreifen |
| `--card` | Karten, Kästen, Fotos, Eingabefelder; Text auf `--ink`-Flächen |
| `--ink` | Haupttext, Tabellenkopf, dunkle Schaltflächen |
| `--ink2` | Sekundärtext (Lead, Untertitel) |
| `--ink3` | gedämpfter Text (Fußzeile, Bildunterschriften) |
| `--red` | Hauptakzent: `h2 em`, Pointe-Etikett, Fortschrittsbalken, Balken |
| `--teal` | Zweitakzent: Kicker, Links, Schrittnummern, Notiz-Labels |
| `--teal-d` | dunkle Variante von `--teal` (Kapitelfolie ohne Bild, Text auf `--teal-l`) |
| `--yellow` | Markierung, Download-Knöpfe, Akzent auf dunklen Folien |
| `--coral` | dritter Akzent: Aufzählungspunkte, Zitatzeichen, aktive Knöpfe |
| `--serif` | Überschriften (h1–h3, große Zahlen) |
| `--accent` | Akzentwörter in Überschriften (`h2 em`, `h1 em`, `.big em`) |
| `--lesen` | Lesetext-Kursive: `.quote`, `.ueb`, `.zettel`, `.fax`, Video-Zitate |
| `--ui` | Oberfläche und Fließtext auf Folien (Kicker, Fußzeile, Knöpfe, Notizen) |
| `--sans` | Grundschrift von `body` und Begleitseiten |

## Optional (basis.css leitet sie per `color-mix()` ab; ein Stil darf sie setzen)

| Token | Vorgabe | Bedeutung |
|---|---|---|
| `--sand` | ink 14 % in paper | Linien, Rahmen, Trenner |
| `--teal-l` / `--red-l` / `--coral-l` / `--yellow-l` | Akzent hell auf card | helle Hinterlegungen (Tags, Kästen, Markierung) |
| `--gruen` | `#3C8D4E` | „richtig“ (ia-sort, ia-ampel) |
| `--night` | ink 85 % + Schwarz | Hintergrund `.s-dark`, `.s-auftrag` |
| `--buehne` | ink 55 % + Schwarz | Fläche um die skalierte Bühne |
| `--panel` | card/paper | Notizleiste, Hilfe, Glossar-Ebene |
| `--ui-dunkel` | ink 90 % + Schwarz | Steuerleiste, Übersicht, Stiftleiste, Hinweis |
| `--auf-dunkel` | paper | Text auf dunklen Flächen |
| `--auf-akzent` | `#fff` | Text auf `--red`/`--teal` |
| `--schatten` | ink 45 % transparent | Schattenfarbe |
| `--radius` / `--radius-s` | `18px` / `8px` | Eckenradius groß / klein |

## Am Element gesetzte Variablen (Markup, kein Stil-Token)

`--r` (Drehwinkel von `.foto`/`.zettel`; basis.css ignoriert ihn, ein Stil kann `transform:rotate(var(--r))` nutzen),
`--w` (Balkenlänge in `.bars`), `--d` (Verzögerung in s für `.a`), `--n` (Zeichen für `.type`),
`--i` (Stagger-Index, von engine.js gesetzt), `--len` (Pfadlänge, von engine.js gesetzt).

## stil.json (für `werkzeuge/schriften_holen.py`)

```json
{ "name": "Papiertheater", "schriften": ["Young Serif", "Instrument Sans:ital,wght@0,400..700;1,400..700",
  "Instrument Serif:ital@0;1", "Source Serif 4:ital,opsz,wght@0,8..60,400..600;1,8..60,400..600"],
  "subsets": ["latin", "latin-ext"] }
```
Ergebnis: `styles/<stil>/fonts/*.woff2` + `fonts.css` (url() relativ). `build.py` kopiert sie nach `<projekt>/fonts/`.

## Dunkle Stile (z. B. nachtprogramm, tafelkreide)

`basis.css` leitet einige Hilfsfarben per `color-mix` aus `--ink` ab und geht dabei von dunkler Schrift auf hellem Papier aus. Stile mit dunklem Grund setzen deshalb zusätzlich selbst:

- `--auf-dunkel`, `--auf-akzent` – Textfarbe auf dunklen Flächen bzw. auf Akzentflächen
- `--ui-dunkel`, `--panel` – Flächen der Bedienelemente und Paneele
- `--teal-d` hell genug für Text auf dunklem Grund

Kontrast: Fließtext (`--ink`, `--ink2`, `--ink3`) auf `--paper` und `--card` mindestens 4,5 : 1; Akzentfarben (`--red`, `--teal`) mindestens 3 : 1 (nur für große Schrift und Flächen).
