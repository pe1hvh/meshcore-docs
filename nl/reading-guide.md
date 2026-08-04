# Leeswijzer

*SECTIES · VOORKENNIS · WAT DIT ANDERS MAAKT*

MeshCore laat goedkope LoRa-radiootjes een eigen netwerk vormen. Berichten
hoppen van node naar node tot ze aankomen — zonder internet, zonder
zendmast, zonder abonnement. **DOMCA** — Dutch Open MeshCore Activity — is
een initiatief om die kennis toegankelijk te maken voor de Nederlandse
community. Deze pagina zegt waar je begint en wat elke sectie van je vraagt.

## Wat hier staat

De documentatie telt 95 hoofdstukken in het Nederlands en dezelfde 95 in het
Engels, met 77 diagrammen per taal. De hoofdstuktelling is het aantal
`.md`-bestanden per taalboom zonder de `README.md`-indexen; de
diagramtelling is het aantal SVG's waarnaar een hoofdstuk verwijst, niet het
aantal bestanden in `images/`.

Het volledige overzicht staat in de [inhoudsopgave](README.md).

## Welke voorkennis elke sectie vraagt

De hoofdstukken lopen sterk uiteen in benodigde voorkennis. Deze tabel zegt
per sectie welke voorkennis handig is, zodat je weet welk detailniveau je
kunt verwachten. Elke sectienaam linkt naar het eerste hoofdstuk ervan.

| Sectie | Wat je er vindt | Benodigde voorkennis |
|---|---|---|
| [Gebruik](gebruik/what-is-meshcore.md) | Wat MeshCore is, een node aan de praat krijgen, hardware, regelgeving, privacy | Geen programmeerkennis vereist |
| [Techniek](techniek/layer-model.md) | Protocol, pakketopbouw byte voor byte, encryptie, routing, repeaters, room server | Basisbegrip van netwerken en hexadecimale notatie helpt; programmeren niet nodig |
| [Platform](platform/platforms.md) | De vier platformfamilies en de keuze ertussen | Geen, afgezien van globale kennis van microcontrollers |
| [Hardware](hardware/introduction.md) | Radio, antenne, linkbudget, filters, BLE, WiFi, USB, I²C, SPI, scherm, GPS, knoppen | Basiskennis elektronica aanbevolen; enkele hoofdstukken tonen C++ fragmenten |
| [Libraries](libraries/introduction.md) | De tweeënvijftig externe libraries die de firmware in gaan | Kennis van PlatformIO-buildconfiguraties aanbevolen |
| [Ontwerp Node → logisch](ontwerp/logisch/roles.md) | Rollen, componenten, contracten, informatiemodel, variabiliteit, ontwerpbeslissingen | Basiskennis van klassen en interfaces aanbevolen; de tekst blijft weg bij broncode |
| [Ontwerp Node → technisch](ontwerp/technisch/source-layout.md) | Broncodestructuur, klassenmodel, platform- en radiorealisatie, buildsysteem, macro's, traceerbaarheid | C++ klassen, overerving en PlatformIO-buildconfiguraties |
| [Ontwerp Companion → logisch](companion/logisch/responsibilities.md) | Wie bewaart wat, vraag-antwoord en push, versieonderhandeling, informatiemodel | Basisbegrip van verkeer tussen twee systemen; enkele C++ fragmenten |
| [Ontwerp Companion → technisch](companion/technisch/transports.md) | De drie transporten, het frameformaat, alle achtenvijftig commando's, de lagen van een client | Programmeerervaring; kennis van binaire protocollen helpt |
| [Naslag](naslag/terminology.md) | Terminologie, referenties, links | Geen. Bedoeld om in op te zoeken, niet om door te lezen |
| [Project](project/about-domca.md) | Over DOMCA, opzet van de repository | Geen |

Kom je een term tegen die je niet kent, dan staat hij in
[Terminologie](naslag/terminology.md).

## Wat dit anders maakt

De gebruikershoofdstukken doen wat je verwacht. De techniekhoofdstukken gaan
een stap verder, en dat is bewust:

- **Byte voor byte.** Pakketten worden uitgeschreven met echte waarden, niet
  met `XX XX`. Je ziet waar de header ophoudt en de payload begint.
- **Geverifieerd tegen de broncode.** Technische claims vermelden de
  firmwareversie en commit waartegen ze zijn gecontroleerd, met verwijzing
  naar het betreffende bestand in `meshcore-dev/MeshCore`.
- **Narekenbaar.** De voorbeelden in
  [Regio's en Scopes](techniek/regions-and-scopes.md) zijn met
  [`tools/example-calculation.py`](../tools/example-calculation.py) te
  reproduceren. Klopt de tekst niet, dan zie je dat zelf.
- **Ook wat níet werkt.** Stub-implementaties, `TODO`'s in de firmware en
  onbeschreven commando's staan er gewoon in.
