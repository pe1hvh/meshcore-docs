# Contracten

*ABSTRACTE AFSPRAKEN · PLICHT EN OPTIE · WAT EEN CONTRACT AFDWINGT*

Tussen de componenten uit het vorige hoofdstuk liggen afspraken vast. Een
component die aan zo'n afspraak voldoet, kan elke andere implementatie
vervangen zonder dat de rest van de firmware verandert. Dit hoofdstuk
beschrijft de acht contracten die het ontwerp dragen, en wat elk contract
verplicht stelt en wat het vrijlaat.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — `src/MeshCore.h`,
> `src/Dispatcher.h`, `src/Mesh.h`, `src/helpers/ui/DisplayDriver.h` en
> `src/helpers/AbstractBridge.h`.

## Plicht en optie

Elk contract bestaat uit twee soorten afspraken. Sommige moeten worden
geïmplementeerd — wie ze overslaat krijgt geen werkende node. Andere hebben
een zinnig standaardantwoord en hoeven alleen te worden geïmplementeerd als de
hardware het aankan.

Die tweedeling is het scharnier van het ontwerp. Een nieuw bord toevoegen
betekent: de verplichte afspraken implementeren en de rest laten staan. Een
bord zonder temperatuursensor meldt eenvoudigweg dat er geen temperatuur is,
en niemand hoeft daar rekening mee te houden.

`src/MeshCore.h` r.45-50

```cpp
class MainBoard {
public:
  virtual uint16_t getBattMilliVolts() = 0;
  virtual float getMCUTemperature() { return NAN; }
  virtual bool setAdcMultiplier(float multiplier) { return false; };
  virtual float getAdcMultiplier() const { return 0.0f; }
```

De eerste methode is verplicht — elk bord moet zijn batterijspanning kunnen
melden. De drie overige methoden geven voor borden zonder die mogelijkheid een
standaardwaarde terug: `NAN`, `false` en `0.0f`.

![Acht contracten als horizontale balken. Boven elke balk staat wie hem
gebruikt, eronder hoeveel implementaties er bestaan. Radio en scherm hebben er
respectievelijk zes en elf; klok en entropiebron drie en twee.](../../../images/nl/interfaces-1.svg)

## De acht contracten

| Contract | Verplicht | Implementaties | Gebruikt door |
|---|---|---|---|
| Radio | Ontvangen, zenden, zendtijd schatten, zendstatus melden | 6 + 1 | Pakketafhandeling |
| Bord | Batterijspanning, fabrikantnaam, herstart, opstartreden | 7 | Applicatie, pakketafhandeling |
| Klok | Tijd lezen en zetten | 3 | Mesh-logica, applicatie |
| Entropiebron | Willekeurige bytes leveren | 2 | Mesh-logica |
| Gezien-tabel | Vraag of een pakket bekend is, en wissen | 1 | Mesh-logica |
| Pakketpool | Uitgeven, teruggeven, in de rij zetten, ophalen | 1 | Pakketafhandeling |
| Scherm | Aan, uit, wissen, tekenen, doorvoeren | 11 | Applicatie |
| Brug | Pakket aanbieden en ophalen | 2 | Mesh-logica |

De kolom *Implementaties* telt de klassen die het contract in deze commit
daadwerkelijk implementeren. Dat er maar één gezien-tabel is en één pakketpool
betekent niet dat het contract overbodig is: het houdt de mesh-logica
onafhankelijk van hoe die tabel is opgebouwd.

Twee getallen verdienen toelichting. Bij *Radio* staat 6 + 1: zes
implementaties lopen via de radiolibrary, en één — ESP-NOW — omzeilt die
volledig en zet WiFi-hardware in als transportmedium. Van die zes worden er
vijf gebruikt; de zesde is aanwezig maar door geen enkel buildtarget
geselecteerd.

Bij *Bord* staat 7, niet 4. Drie implementaties zijn gedeeld per
platformfamilie en staan in `src/helpers/`. De vierde familie, RP2040, heeft
geen gedeelde implementatie: elk van de vier RP2040-varianten schrijft zijn
eigen bordklasse in zijn eigen variantdirectory. Dat is een asymmetrie in het
ontwerp, geen vergissing van de telling.

## Het radiocontract

Het scherpste contract in het ontwerp, en het enige dat de firmware
werkelijk draagbaar maakt over vier verschillende radiochips.

`src/Dispatcher.h` r.22-32

```cpp
class Radio {
public:
  virtual void begin() { }

  /**
   * \brief  polls for incoming raw packet.
   * \param  bytes  destination to store incoming raw packet.
   * \param  sz   maximum packet size allowed.
   * \returns 0 if no incoming data, otherwise length of complete packet received.
  */
  virtual int recvRaw(uint8_t* bytes, int sz) = 0;
```

Let op wat er niet in staat. Geen frequentie, geen bandbreedte, geen
spreidingsfactor. Het contract gaat uitsluitend over bytes in en bytes uit,
plus wat de laag erboven nodig heeft om te plannen: hoe lang duurt het zenden
van zoveel bytes, en is de vorige zending klaar.

De radioparameters zitten niet in dit contract omdat ze niet tot de
verantwoordelijkheid van de laag erboven behoren. Wie de spreidingsfactor
verandert, verandert de radio-instelling, niet het mesh-gedrag.

## Het kleinste contract

De gezien-tabel bestaat uit twee afspraken:

`src/Mesh.h` r.16-20

```cpp
class MeshTables {
public:
  virtual bool hasSeen(const Packet* packet) = 0;
  virtual void clear(const Packet* packet) = 0;   // remove this packet hash from table
};
```

Meer is er niet nodig. De mesh-logica hoeft niet te weten hoe groot de tabel
is, hoe lang een pakket onthouden wordt of wat er gebeurt als hij vol raakt.
Dat zijn allemaal keuzes van de implementatie.

## Het breedste contract

Het schermcontract is het enige dat een eigen begrippenkader meebrengt —
afmetingen en kleuren — omdat een applicatie die tekent nu eenmaal moet weten
hoeveel ruimte er is.

`src/helpers/ui/DisplayDriver.h` r.6-20

```cpp
class DisplayDriver {
  int _w, _h;
protected:
  DisplayDriver(int w, int h) { _w = w; _h = h; }
public:
  enum Color { DARK=0, LIGHT, RED, GREEN, BLUE, YELLOW, ORANGE }; // on b/w screen, colors will be !=0 synonym of light

  int width() const { return _w; }
  int height() const { return _h; }

  virtual bool isOn() = 0;
  virtual bool isEink() { return false; } // default to non-eink, override in eink drivers
  virtual void turnOn() = 0;
  virtual void turnOff() = 0;
  virtual void clear() = 0;
```

Elf displaytypen implementeren dit contract. Eén ervan doet niets: nodes
zonder scherm krijgen die implementatie, zodat de applicatie niet hoeft te
vragen of er een scherm is.

Het contract kent één beperking die niet is weg te abstraheren. Een e-ink
scherm laat zich niet behandelen als een LCD — het verversen duurt seconden in
plaats van milliseconden — en dat verschil is niet weg te abstraheren. Het
contract lost dat op door de applicatie te laten vragen om wat voor scherm het
gaat. Dat is een bewuste concessie; zie [Ontwerpbeslissingen](decisions.md).

## Wat een contract niet afdwingt

Geen van de contracten legt vast wanneer iets wordt aangeroepen of hoe lang
een aanroep mag duren. Alles draait in één lus, en een implementatie die te
lang blijft hangen houdt het hele systeem op. Dat is een afspraak die nergens
is opgeschreven maar wel geldt.

Evenmin dwingt een contract af dat een implementatie zich netjes gedraagt bij
fouten. Er is geen foutmodel: een radio die niet reageert, meldt dat niet, hij
levert eenvoudigweg geen pakketten.

## Bronnen

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/Mesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Mesh.h)
- [MeshCore `03b6ef4` — `src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/DisplayDriver.h)
