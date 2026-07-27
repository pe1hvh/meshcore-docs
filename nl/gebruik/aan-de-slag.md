# Aan de Slag

*EERSTE INSTALLATIE · IN 3 STAPPEN ONLINE*

## Benodigdheden

- MeshCore-compatibele hardware (bijv. Heltec V3, T-Deck Plus, T1000-E)
- Antenne voor **868 MHz** (EU-frequentie)
- Android of iOS telefoon met de MeshCore Companion App
- USB-kabel voor eerste configuratie

## Stap 1 — Firmware flashen

Ga naar [flasher.meshcore.co.uk](https://flasher.meshcore.co.uk) in Chrome of Edge. Selecteer je apparaat, kies **'Companion Radio BLE'** firmware, en klik Flash.

> [!WARNING]
> **Let op:** De Web Flasher werkt alleen in Chromium-gebaseerde browsers (Chrome, Edge). Firefox en Safari worden niet ondersteund vanwege Web Serial API-beperkingen.

## Stap 2 — Verbinden met de app

Start de **MeshCore Companion App**, kies Scan, selecteer je node en tik Connect. De app is beschikbaar voor zowel Android als iOS via de officiële app stores.

## Stap 3 — Configureren

Selecteer in de app het preset **EU/UK (narrow)**. Dit stelt automatisch de volgende parameters in:

| Parameter | Waarde | Toelichting |
|---|---|---|
| Preset | EU/UK (narrow) | Aanbevolen voor Europa |
| Frequentie | 869.618 MHz | EU ISM-band |
| Bandbreedte | 62.5 kHz | Smal — meer bereik, minder snelheid |
| Spreading Factor | SF8 | Goede balans bereik/snelheid |
| Coding Rate | 4/8 | Maximale foutcorrectie |
| Vermogen | 14 dBm | EU-limiet (25 mW ERP) |
| Encryptie | Aan (standaard) | AES-128 |


## Stap 4 - Regio-instellingen


Sinds firmware 1.10 kent MeshCore regio's en scopes om onnodige airtime te vermijden: een bericht voor je eigen buurt hoeft niet door heel Nederland doorgestuurd te worden. Repeaters kennen een of meer regio's (“welke postzegels laat ik door”), en elk bericht krijgt een scope (“welke postzegel plak ik erop”). Een repeater stuurt een bericht alleen door als de scope overeenkomt met een van zijn ingestelde regio's.

De indeling volgt de ISO 3166-2:NL provinciecodes, met een landelijke laag erboven:

| Niveau | Voorbeeld | Betekenis |
|------------|--------------------------|--------------------------------------------|
| Land       | nl                       | Heel Nederland                             |
| Provincie  | nl-ov, nl-ge, nl-ut, ... | Eigen provincie (12x)                      |
| Lokaal     | nl-ov-zwolle             | Community-afspraak, niet gestandaardiseerd |

**Basisconfiguratie op een repeater:**

```text
region put eu
region put nl eu
region put <jouw-provincie> nl
region default <jouw-provincie>
region save
```

Het tweede argument van `region put` is de ouder. Laat je dat weg, dan hangt de
regio onder de wildcard `*` en krijg je een vlakke lijst in plaats van een boom.

> [!WARNING]
> **Regio's erven niet.** Een repeater vergelijkt de scope van een pakket met
> elke regio die hij zelf kent, los van de hiërarchie. Een repeater die alleen
> `nl` kent, stuurt een bericht met scope `nl-ov` dus **niet** door. Wil je
> zowel landelijk als provinciaal verkeer doorgeven, zet dan beide regio's op de
> repeater. De boomstructuur is er voor het overzicht en voor `region remove`,
> niet voor het doorsturen.

*Let op: het commando “region denyf \*” (strikte regiofiltering, alles buiten je regio's weigeren) stond gepland voor fase 8 van de landelijke uitrol op 18 juli 2026. Voortijdig gebruik laat je repeater berichten droppen van nodes die hun regio nog niet hebben ingesteld; controleer de actuele stand van de uitrol voordat je dit aanzet.*

Een zachtere tussenstap is `set flood.max.unscoped 3`. Ongescoopt verkeer blijft
dan lokaal werken, maar reist niet meer het hele land door — zonder dat je nodes
zonder regio-instelling volledig afsnijdt.

In de Companion App stel je per kanaal een scope in (bijvoorbeeld landelijk, provinciaal of lokaal); de community bepaalt lokale codes onderling. De app stuurt daarbij de 16-byte sleutel naar de node, niet de naam, en zet die per verzending. Wat er over de lucht gaat is een 16-bits code die uit die sleutel en de berichtinhoud wordt berekend — zie [MeshCore Packet Structuur](../techniek/techniek-packets.md). Voor de actuele configuratie en hulpmiddelen:

- Regiocodes instellen (stap-voor-stap configurator): mesh-up.nl/tools/regiocodes-instellen
- Dashboard-configurator: dashboard-elburg.f3dp.nl (tab “region-configurator”)
- Volledige lijst regiocodes: meshwiki.nl/wiki/Lijst_van_regio%27s


## En nu?

Na configuratie is je node actief in het mesh. Je kunt berichten sturen via het **#public** kanaal, andere nodes ontdekken via de kaart, en Direct Messages sturen naar nodes die je hebt gezien. Lees meer over communicatie in de sectie *Communicatie*.
