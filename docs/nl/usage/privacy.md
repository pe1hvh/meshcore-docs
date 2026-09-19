# Privacy & Beveiliging

*ENCRYPTIE · HAM VS ISM · ZICHTBAARHEID*

## Wat is altijd zichtbaar?

Elke node moet **beacons** uitzenden voor routing. Andere nodes zien dat er een node bestaat en actief is. Dit is noodzakelijk voor het functioneren van het mesh-netwerk.

## Wat is NOOIT zichtbaar (ISM-modus)?

- Met wie je communiceert
- In welke Rooms je zit
- De inhoud van je berichten
- Zelfs het bestaan van jouw Rooms

> [!NOTE]
> **Encryptie:** MeshCore gebruikt AES-128, zowel voor channels als voor direct messages. Direct Messages zijn end-to-end versleuteld met public key cryptografie.

## HAM vs ISM modus

| Aspect | ISM-modus (868 MHz) | HAM-modus (70 cm-band) |
|---|---|---|
| Encryptie | Volledig versleuteld | Geen (regelgeving) |
| Identificatie | Anoniem mogelijk | Callsign verplicht |
| Frequentie | 868 MHz ISM-band | 430–440 MHz |
| Licentie | Niet vereist | Amateurlicentie vereist |
| Vermogen | 500 mW e.r.p. (H4) of 25 mW e.r.p. (H5) | Hoger (conform licentie) |
