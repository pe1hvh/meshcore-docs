# Node Types

*FIRMWARE PROFIELEN · ROLLEN IN HET MESH*

MeshCore onderscheidt verschillende node types op basis van hun functie in het netwerk. Deze types worden bepaald door het **firmware profiel** dat je flasht op je hardware.

## Overzicht Node Types

- **Companion Radio** — Het meest gebruikte type voor eindgebruikers. Fungeert als radio-interface voor een smartphone via Bluetooth (BLE), USB of WiFi. De MeshCore Companion App bestuurt de node.
- **Repeater** — Primaire taak: berichten doorsturen om het netwerkbereik te vergroten. Typisch geplaatst op strategische locaties met goede antennepositie zoals dakranden of heuveltoppen.
- **Room Server** — Eén Room per node, met store-and-forward: berichten worden vastgehouden tot de ontvanger weer bereikbaar is. De wachtrij telt 32 posts en staat in het werkgeheugen. Beheer op afstand kan met elk beheerderswachtwoord; of je client dat aanbiedt is een tweede — op een T-Deck vraagt het een registratiesleutel, in de smartphone-app een ontgrendeling.
- **Standalone Apparaat** — Hardware zoals de T-Deck Plus kan volledig zelfstandig functioneren. Met ingebouwd scherm en toetsenbord kun je direct berichten typen en lezen — geen smartphone nodig.
- **Telemetry Node** — Specifiek voor het verzenden van sensordata: temperatuur, luchtvochtigheid, batterijspanning. Uitbreidbaar via GPIO, I²C of SPI interfaces.

## Typisch netwerk

In de praktijk bestaat een netwerk uit een combinatie van deze node types. Een typisch familienetwerk:

> [!NOTE]
> **Voorbeeld:** 2–4 Companion Radio's voor gezinsleden, 1 Repeater op een hoog punt voor betere dekking, en 1 Room Server thuis voor store-and-forward.

![Alle vijf node types in een netwerk: twee companion radio's, een repeater, een room server, een standalone apparaat en een telemetry node](../../images/nl/node-types-1.svg)
