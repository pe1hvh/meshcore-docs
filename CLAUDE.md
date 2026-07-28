# meshcore-docs

Tweetalige (NL/EN) documentatie over MeshCore: gebruik, hardware,
regelgeving en de internals van het LoRa-protocol. Een DOMCA-project
(Dutch Open MeshCore Activity), gepubliceerd op [domca.nl](https://domca.nl).

Repo: `https://github.com/pe1hvh/meshcore-docs` · branch `main` ·
tekst en diagrammen CC BY-SA 4.0, code in `tools/` MIT.

## Doel van dit document

Richt-document voor wie aan deze documentatie werkt: redacteuren,
vertalers en AI-assistenten (Claude) in vervolgsessies. Bevat de bindende
regels, conventies en valkuilen die het gedrag bij **elke** taak sturen.

Beschrijft **niet** wat MeshCore is of hoe het werkt — dat staat in de
hoofdstukken zelf. Beschrijft **niet** hoe de website wordt gebouwd.
Voor de inhoudsopgave: `nl/README.md` en `en/README.md`.

## Repo in één scherm

```
├── nl/                  Nederlandse hoofdstukken (bron)
│   ├── gebruik/         gebruik, hardware, regelgeving, privacy
│   ├── techniek/        protocol, pakketten, encryptie, repeaters
│   ├── platform/        platformfamilies, chipkeuze
│   ├── naslag/          terminologie, referenties, links
│   └── project/         over DOMCA, GitHub-overzicht
├── en/                  Engelse hoofdstukken (vertaling, 1-op-1 spiegel)
│   ├── usage/
│   ├── technical/
│   ├── platform/
│   ├── reference/
│   └── project/
├── images/
│   ├── nl/              diagrammen (SVG) en foto's voor de NL-hoofdstukken
│   └── en/              diagrammen (SVG) en foto's voor de EN-hoofdstukken
├── tools/               narekenscripts bij de techniekhoofdstukken
├── README.md            tweetalige landingspagina
├── CHANGELOG.md         Keep a Changelog + semver
└── LICENSE              CC BY-SA 4.0
```

- **NL is de bron, EN is de vertaling.** Inhoudelijke wijzigingen beginnen
  in het Nederlandse hoofdstuk en landen daarna in het Engelse.
- **Bestandsnamen zijn altijd Engels**, kebab-case, ook in de
  Nederlandse boom en ook voor scripts, diagrammen en bijlagen. Dit gaat
  over bestanden; mapnamen vallen er niet onder en volgen de rubrieks-
  mapping hieronder. Bestaat er geen gangbare Engelse term, gebruik dan de
  firmware-term.
- **Slugs zijn Engels, kebab-case, zonder rubrieksprefix, en in beide talen
  identiek.** Alleen de mapnaam verschilt: `gebruik` ↔ `usage`,
  `techniek` ↔ `technical`, `naslag` ↔ `reference`, `platform` ↔ `platform`,
  `project` ↔ `project`. Dus `nl/techniek/packet-structure.md` ↔
  `en/technical/packet-structure.md`.
- **Twee inhoudsopgaven.** `nl/README.md` en `en/README.md` bevatten
  dezelfde hoofdstukken in dezelfde volgorde.
- **Geen gedeelde beeldmap.** Elk diagram bestaat twee keer, onder
  dezelfde bestandsnaam: `images/nl/<slug>-<n>.svg` en
  `images/en/<slug>-<n>.svg`. Ook als er geen tekst in staat.

## Waar deze documentatie op stuurt

Vier eigenschappen onderscheiden dit project van een gewone handleiding.
Ze zijn geen stijlwens maar de reden van bestaan:

1. **Byte voor byte.** Pakketten worden uitgeschreven met echte waarden,
   nooit met `XX XX`.
2. **Geverifieerd tegen de broncode.** Technische claims vermelden de
   firmwareversie, commit en het bestand waartegen ze zijn gecontroleerd.
3. **Narekenbaar.** Rekenvoorbeelden zijn te reproduceren met de scripts
   in `tools/`.
4. **Ook wat níet werkt.** Stub-implementaties, `TODO`'s in de firmware en
   onbeschreven commando's staan er gewoon in.

## Documentconventies

### Pagina-opbouw

- `#` H1 = paginatitel.
- Daaronder een cursieve subtitelregel in hoofdletters, gescheiden door
  `·` — bijvoorbeeld `*HEADER · ROUTE · PATH · PAYLOAD · REGIO-SCOPE*`.
- Daarna een inleidende alinea (2–5 regels) die de hele pagina samenvat.
- Secties met `##`, subsecties met `###`. **Geen `####`** op
  hoofdstukniveau.
- Technische hoofdstukken eindigen met `## Bronnen` (NL) / `## Sources` (EN).
- Elk EN-hoofdstuk eindigt met de regel:
  `Translated from Dutch by Anthropic Claude`.

### Tekst

- Nieuwe proza harde wrap op ±80 kolommen. (Oudere hoofdstukken hebben nog
  lange regels; wrap wat je aanraakt, herformatteer niet ongevraagd de rest.)
- GitHub-alerts: `> [!NOTE]` voor toelichting en bronvermelding,
  `> [!WARNING]` voor risico's en juridische waarschuwingen.
- Tabellen met scheidingsrij `|---|---|`; cursieve rijen voor velden die
  strikt genomen buiten scope vallen (zie `packet-structure.md`).
- Codeblokken altijd met taal-tag: ` ```text `, ` ```python `, ` ```bash `.
- Firmware-identifiers, bestandsnamen, commando's en hexwaarden in
  `` `backticks` ``.
- Nuchtere toon, geen marketingtaal, geen superlatieven.

### Bronvermelding in techniekhoofdstukken

Bovenaan, direct na de inleiding:

```markdown
> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `a3a1aa5`, 19 juli 2026 — bestanden
> `src/Packet.h`, `src/Dispatcher.cpp`, en de officiële
> `docs/packet_format.md`.
```

Onderaan een `## Bronnen`-lijst met links naar
`https://github.com/meshcore-dev/MeshCore/blob/<commit>/<pad>`.

Pin de commit in de link, niet `main` — `main` verschuift en maakt de
bronvermelding binnen weken onnauwkeurig.

### Afbeeldingen

- Pad vanuit een NL-hoofdstuk: `../../images/nl/<slug>-<n>.svg`.
- Pad vanuit een EN-hoofdstuk: `../../images/en/<slug>-<n>.svg`.
- Beide bestanden bestaan altijd en heten hetzelfde. Bevat het diagram
  geen tekst, dan is de EN-versie een identieke kopie.
- Alt-tekst is beschrijvend en zelfstandig leesbaar — niet
  `Diagram 1 bij layer-model`.
- **Nieuwe diagrammen als SVG**, niet als PNG.
- SVG-conventie (zie `images/nl/layer-model-1.svg` als referentie):
  `style="width:100%;margin:1rem 0"`, een `viewBox`, een ingebedde
  `<style>` met `:root`-variabelen plus een
  `@media (prefers-color-scheme: dark)`-blok, alle kleuren via
  `var(--…)`, teksten in `'JetBrains Mono',monospace`.

### Links

- Relatieve links binnen dezelfde taalboom. **Nooit** van `nl/` naar `en/`
  of andersom.
- Verwijzingen naar de firmware gaan naar het concrete bestand in
  `meshcore-dev/MeshCore`, niet naar de repo-root.

## Bindende regels

### 🛑 Stoppen en vragen

**Deze regel gaat boven alle andere in dit hoofdstuk.** Wordt hij overtreden,
dan is de rest van het werk waardeloos, hoe correct het verder ook is
uitgevoerd. Er is geen opdracht, deadline of ogenschijnlijke
vanzelfsprekendheid die hem opzij zet.

- **Bij tegenspraak tussen bronnen: stoppen en vragen.** Nooit zelf
  beslechten, ook niet als één lezing veel waarschijnlijker lijkt. Meld welke
  bron wat zegt en leg de keuze voor.
- **Een expliciet signaal wordt nooit wegverklaard.** Staat er iets in de
  opdracht, in dit document of in de repo dat niet strookt met je eigen
  waarneming, dan is je waarneming verdacht — niet het signaal. "Dat zal een
  typefout zijn" en "dat is vast verouderd" zijn verboden conclusies.
- **Inventariseer volledig.** Lege mappen, verborgen bestanden en mapentries
  in een archief horen bij de inventaris. Een methode die ze niet toont, is
  geen inventarisatie: `find -type f` mist lege mappen, `unzip -l` niet.
- **Lees de woorden van de opdrachtgever letterlijk.** Meervoud is meervoud.
  Leg een instructie niet langs je eigen indeling van het probleem; botsen
  die twee, dan wint de instructie.
- **Een gegeven antwoord is bindend.** Stel je een vraag, dan voer je het
  antwoord uit — juist als het tegen je eigen aanname ingaat. Anders had je
  de vraag niet moeten stellen.
- **Twijfel hoort vóór het bouwen.** Een openstaand punt onder een oplevering
  zetten is geen vraag stellen: dan is het werk al op een aanname gedaan.
- **Checkpoint 2 is niet optioneel.** Impactanalyse en bevestiging vóór de
  eerste regel wordt geschreven, ook — en vooral — bij een opdracht die
  uitputtend oogt. Hoe gedetailleerder de opdracht, hoe scherper de
  tegenspraken erin.
- **Een regel die je hier vastlegt, pas je in dezelfde sessie toe op de
  repo.** Kan dat niet, dan meld je dat vooraf met de reden. Zelf besluiten
  dat iets "een aparte opdracht" is, is niet aan de uitvoerder.

### 🌐 Taalpariteit

- **Elke inhoudelijke wijziging landt in beide talen**, in dezelfde sessie.
- Kopstructuur, tabelkolommen, alerts, afbeeldingen en volgorde zijn in NL
  en EN identiek. Alleen de taal verschilt.
- Slug blijft gelijk; alleen de mapnaam verschilt.
- Nieuw of hernoemd hoofdstuk → `nl/README.md` **én** `en/README.md`
  bijwerken, op dezelfde positie in dezelfde rubriek.
- Raakt een correctie alleen de vertaling (taalfout, ontbrekende sectie),
  dan mag de EN-versie alleen wijzigen — meld dat expliciet.

### 🔬 Verifieerbaarheid

- Technische claims worden gecontroleerd tegen de MeshCore-broncode, niet
  tegen forumberichten of eerdere hoofdstukken.
- Vermeld firmwareversie, commit-hash, datum en geraadpleegde bestanden.
- Geen pakketvoorbeelden met `XX XX`: echte, narekenbare waarden.
- Kun je iets niet verifiëren, schrijf het op als onbevestigd. **Verzin
  niets** — de disclaimer over AI-hallucinaties in `README.md` is er niet
  voor niets.
- Firmware-defaults veranderen per release. Bij het aanraken van een
  hoofdstuk: controleer of de vermelde versie nog actueel is.
- Cijfers die **niet** uit de firmware-repo komen (datasheets van
  Raspberry Pi, Espressif, Nordic, ST; de web flasher; webshops) worden
  als externe bron gemarkeerd, met een voetnoot bij de tabel of het getal.

### 🧮 Consistentie van voorbeelden

- De voorbeelddata zijn projectbreed gelijk: regio `nl-ov-zwo`, kanaal
  `#zwolle`, afzender `PE1HVH`, timestamp `1785412800`, tekst
  `"Op Woensdag a.s. Blauwvingerdagen"`.
- Wijzigt een voorbeeld, dan wijzigt `tools/example-calculation.py` mee — en
  omgekeerd.
- Elk getal in een techniekhoofdstuk moet met een script in `tools/`
  reproduceerbaar zijn, of expliciet als externe bron gemarkeerd. Klopt de
  tekst niet met de scriptuitvoer, dan is de tekst fout.
- Genereert een hoofdstuk zijn tabellen uit de firmware, dan levert het
  zijn eigen script mee. Naamconventie: Engels, kebab-case, zoals
  `tools/example-calculation.py` en `tools/dm-example.py`.

### 📚 Terminologie en naslag

- `nl/naslag/terminology.md` en `en/reference/terminology.md` zijn
  **alfabetisch gesorteerd** — nieuwe termen worden op hun plaats
  ingevoegd, niet onderaan geplakt.
- Introduceer je een afkorting in een hoofdstuk, dan staat die ook in de
  terminologietabel (beide talen).
- Nieuwe externe bron → `naslag/references.md` / `reference/references.md`;
  nieuwe tool of website → `naslag/links.md` / `reference/links.md`.
- **Neem de woordkeuze van de firmware over waar die eenduidig is.** De
  repo spreekt van *platforms* (`ESP32_PLATFORM`, `NRF52_PLATFORM`,
  `RP2040_PLATFORM`, `STM32_PLATFORM`), niet van microcontrollers. Gebruik
  *platform* en *platformfamilie* voor de vier bouwdoelen, *SoC* voor de
  chip, en *MCU* alleen waar het echt om de rekenkern gaat. Wijk je
  bewust af omdat de lezersterm anders is, zet dat dan in het hoofdstuk
  zelf uit — niet stilzwijgend.

### 🛡️ Bestaande inhoud

- Inventariseer per geraakt bestand wat erin staat vóór je wijzigt.
- Wat niet in de taak staat wordt niet gewijzigd, verwijderd of herschreven.
- Geen nieuwe top-level mappen; geen hernoemde of verwijderde bestanden
  zonder expliciete opdracht.
- Waarschuwingen over regelgeving, duty cycle en encryptie in HAM-modus
  worden niet afgezwakt, ingekort of samengevat weggelaten.
- De AI-disclaimer in `README.md` en `project/about-domca.md` blijft staan.
- Bij twijfel: **STOP en vraag.**

### 📋 CHANGELOG en commits

- `CHANGELOG.md` volgt [Keep a Changelog](https://keepachangelog.com/):
  secties `Added` / `Changed` / `Fixed` / `Removed` onder `[Unreleased]`.
- Entries noemen de bestandspaden van **beide** taalversies en leggen uit
  *waarom* de wijziging is gedaan, niet alleen wat.
- Feitelijke correcties horen onder `Fixed` met de foute bewering erbij —
  zodat lezers die de oude tekst kennen weten wat er mis was.
- Commits volgens Conventional Commits: `docs(regions-and-scopes): …`,
  `fix(regulations): …`, `chore(images): …`. Scope = hoofdstuk-slug.

## Werkproces in een chat-sessie

Drie verplichte checkpoints. Ze vallen alle drie onder 🛑 *Stoppen en
vragen*: een checkpoint overslaan omdat de opdracht duidelijk lijkt, is zelf
de fout die die regel adresseert.

1. **Source verification** (eerst, altijd) — inventariseer alle beschikbare
   sources, inclusief lege mappen en mapentries in een archief; meld welke je
   ziet met timestamps; vraag welke leidend is. Begin elke inhoudelijke
   response met *"Werkend met: [bestandsnaam] (uploaded [timestamp])"*.
2. **Impact analyse** (vóór implementatie) — welke bestanden en mappen worden
   geraakt (NL, EN, README-indexen, `images/nl/`, `images/en/`,
   `terminology.md`, `CHANGELOG.md`, `tools/`), wat staat daar nu in, en welke
   tegenspraken zitten er in de opdracht; vraag bevestiging vóór je begint.
3. **Delivery validation** (vóór oplevering) — loop de checklist hieronder
   af en meld het resultaat per punt.

**Delivery-checklist:**

- [ ] NL en EN hebben dezelfde secties, tabellen, alerts en afbeeldingen
- [ ] EN-bestand eindigt op `Translated from Dutch by Anthropic Claude`
- [ ] Alle relatieve links wijzen naar bestaande bestanden
- [ ] Elk diagram bestaat in `images/nl/` **en** `images/en/`, onder
      dezelfde naam
- [ ] Nieuwe termen staan alfabetisch in beide terminologiebestanden
- [ ] Bron-blok en `## Bronnen` kloppen met de gebruikte firmwareversie en
      commit; de links pinnen die commit
- [ ] Getallen komen overeen met de uitvoer van `tools/`, of zijn als
      externe bron gemarkeerd
- [ ] README-index bijgewerkt indien hoofdstukken toegevoegd/hernoemd
- [ ] `CHANGELOG.md`-entry onder `[Unreleased]`, beide talen genoemd
- [ ] Geen resterende HTML→markdown-conversieartefacten

**File-source-priority** (van hoog naar laag): meest recente upload >
losse bestanden (op upload-tijd) > de repo op GitHub (alleen op verzoek of
bij ontbreken van uploads) > chat-history (nooit als tekst-source).
Bij conflict: STOP en vraag. Dat geldt ook voor dit document: spreekt
`CLAUDE.md` de repo-inhoud tegen, dan is de repo leidend en wordt
`CLAUDE.md` in dezelfde sessie bijgewerkt.

## Output- en delivery-conventies

Per bestand: pad vanaf de repo-root, de volledige inhoud, korte uitleg wat
verandert en waarom, en wat **niet** is veranderd. NL eerst, EN daarna.

Geen fragmenten en geen `…ongewijzigd…`-markeringen in markdown-opleveringen:
de bestanden worden 1-op-1 in de repo geplakt.

Bij meer dan twee bestanden: één ZIP met de directorystructuur vanaf de
repo-root (`nl/`, `en/`, `images/`, …), naamconventie
`meshcore_docs_[onderwerp]_result.zip`. Maximaal 1 ZIP per chat.

## Bekende valkuilen

- **Twee verweesde SVG's met een Nederlandse rubrieksprefix.**
  `images/nl/techniek-chirp-2.svg` en `images/en/techniek-chirp-3.svg`
  voldoen niet aan de regel dat bestandsnamen Engels zijn, en worden
  bovendien nergens aangehaald — de chirp-hoofdstukken wijzen naar
  `text-to-chirp-*.svg`. Hernoemen kan niet zonder botsing met die
  bestaande bestanden; ze horen verwijderd te worden.
- **Conversieartefacten uit de HTML→markdown-migratie.** Losse regels als
  `Layer stack SVG` in `layer-model.md`, formules en configuratieblokken
  die op één regel geplakt staan, en `####`-koppen waar `##` hoort. Fix ze
  in de bestanden die je toch aanraakt. `regulations.md` heeft in beide
  talen nog `####`-koppen.
- **Alt-teksten voldoen nog niet aan de eigen regel.** Meerdere
  hoofdstukken gebruiken `![Diagram 1 bij …](…)`. Nieuwe hoofdstukken doen
  het goed; bestaande worden meegenomen bij de eerstvolgende inhoudelijke
  wijziging.
- **Dubbele en verweesde afbeeldingen.** Sommige PNG's uit de website-export
  zijn identiek (`05-group-communication-1.png` en `-2.png`) of worden
  nergens meer aangehaald. Controleer vóór hergebruik.
- **Twee naamgevingsstijlen in `images/`.** Legacy-PNG's met
  nummerprefix (`20-channel-structure-psk-1.png`) naast SVG's met
  hoofdstuk-slug (`channel-structure-1.svg`). Nieuwe bestanden volgen de
  slug-stijl.
- **De transport code is geen regio-identificatie** — hij verandert per
  bericht. Een veelgemaakte fout in samenvattingen van
  `packet-structure.md` en `regions-and-scopes.md`.
- **Firmware-default `set dutycycle` staat op 50 %**, ruim boven H4 (10 %)
  en H5 (0,1 %). Dat feit mag nergens sneuvelen bij het inkorten van
  `regulations.md`.
- **Niet elk hoofdstuk heeft al een Bron-blok.** Ontbreekt het, voeg het toe
  als je de inhoud verifieert; laat het leeg als je niets hebt kunnen
  controleren, in plaats van een versie te gokken.
- **`main` van MeshCore verschuift dagelijks.** Noteer de commit waarop je
  je baseert, en ga er niet van uit dat tellingen uit een eerdere sessie
  nog kloppen. Tussen `a3a1aa5` (19 juli 2026) en `03b6ef4` (28 juli 2026)
  verschoven bijvoorbeeld al twee build-target-tellingen.

## Verwijzingen

- **`nl/README.md` · `en/README.md`** — inhoudsopgave per taal.
- **`README.md`** — landingspagina, structuuroverzicht, licentie, disclaimer.
- **`CHANGELOG.md`** — wat er per wijziging is veranderd en waarom.
- **`tools/example-calculation.py`** — reproduceert de projectbrede
  voorbeelddata; aangehaald vanuit `README.md`.
- **`tools/dm-example.py`** — reproduceert het rekenvoorbeeld in
  `direct-messages.md`.
- **`nl/naslag/terminology.md`** — begrippenlijst, leidend voor woordkeuze.
- **`nl/naslag/references.md`** — bronnenlijst.
- **[meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore)** —
  firmware-broncode, de ground truth voor techniekhoofdstukken.
- **[docs.meshcore.io](https://docs.meshcore.io/)** — officiële documentatie.
