# Node Types

*FIRMWARE PROFIELEN · ROLLEN IN HET MESH*

MeshCore onderscheidt verschillende node types op basis van hun functie in het netwerk. Deze types worden bepaald door het **firmware profiel** dat je flasht op je hardware.

## Overzicht Node Types

- **Companion Radio** — Het meest gebruikte type voor eindgebruikers. Fungeert als radio-interface voor een smartphone via Bluetooth (BLE), USB of WiFi. De MeshCore Companion App bestuurt de node.
- **Repeater** — Primaire taak: berichten doorsturen om het netwerkbereik te vergroten. Typisch geplaatst op strategische locaties met goede antennepositie zoals dakranden of heuveltoppen.
- **Room Server** — Beheert een of meerdere Rooms met store-and-forward functionaliteit. Slaat berichten op voor offline ontvangers. Vereist Ultra-licentie voor beheer op afstand.
- **Standalone Apparaat** — Hardware zoals de T-Deck Plus kan volledig zelfstandig functioneren. Met ingebouwd scherm en toetsenbord kun je direct berichten typen en lezen — geen smartphone nodig.
- **Telemetry Node** — Specifiek voor het verzenden van sensordata: temperatuur, luchtvochtigheid, batterijspanning. Uitbreidbaar via GPIO, I²C of SPI interfaces.

## Typisch netwerk

In de praktijk bestaat een netwerk uit een combinatie van deze node types. Een typisch familienetwerk:

> [!NOTE]
> **Voorbeeld:** 2–4 Companion Radio's voor gezinsleden, 1 Repeater op een hoog punt voor betere dekking, en 1 Room Server thuis voor store-and-forward.

Network diagram SVG

![Diagram 1 bij node-types](../../images/node-types-1.svg)
