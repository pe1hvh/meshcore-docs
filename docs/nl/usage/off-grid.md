# Off-Grid Client Repeat Mode

*MESH VERSTERKEN · CLIENT ALS REPEATER · BEREIK VERGROTEN*

In MeshCore bestaat een strikte scheiding tussen **clients** (die berichten versturen en ontvangen) en **repeaters** (die verkeer doorsturen). Met de **Client Repeat Mode** vervalt die scheiding: een gewone client-node kan tegelijkertijd als repeater fungeren en zo het meshnetwerk uitbreiden — zonder extra hardware.

## Hoe werkt het?

Normaal gesproken verwerkt een client-node alleen eigen verkeer: berichten verzenden, ontvangen en weergeven op het scherm of via de companion-app. Zodra **Client Repeat Mode** wordt ingeschakeld, herhaalt (repeat) de node ook pakketten van andere nodes in het netwerk. Het apparaat wordt in feite een *hybride*: volledig bruikbaar als client én actief als doorgeefluik voor het meshverkeer van anderen.

## Waarom is dit belangrijk?

- **Dynamisch bereik** — Elke deelnemende client vergroot automatisch het netwerk. Hoe meer gebruikers, hoe verder het bereik — zonder vaste infrastructuur.
- **Geen repeaters nodig** — In afgelegen gebieden of tijdens evenementen is er vaak geen vaste repeater beschikbaar. Client Repeat Mode vult dat gat op.
- **Eenvoudig aan/uit** — De modus kan worden in- of uitgeschakeld via de companion-app. Handig om batterij te sparen wanneer je niet wilt doorsturen.
- **Volledige encryptie** — Doorgestuurde pakketten blijven volledig versleuteld. De herhalende node kan de inhoud niet lezen — alleen doorsturen.

## Typische toepassingen

Client Repeat Mode is bijzonder nuttig in situaties waarbij het mesh spontaan moet ontstaan uit de aanwezige apparaten:

- **Wandel- en bergtochten** — deelnemers verspreid over een route vormen samen een ketting van repeaters, waardoor berichten van kop naar staart kunnen reizen
- **Festivals en evenementen** — grote groepen met MeshCore-apparaten bouwen automatisch een dicht, zelfherstellend netwerk
- **Noodcommunicatie** — wanneer vaste infrastructuur ontbreekt of is uitgevallen, vormt elke client een extra schakel in het netwerk
- **Velddagen en radioactiviteiten** — deelnemers op verschillende locaties versterken elkaars bereik zonder extra apparatuur

## Hoe schakel je het in?

De instelling is beschikbaar in de companion-app (Android/iOS) onder de node-instellingen. Na het inschakelen begint het apparaat direct met het doorsturen van pakketten van andere nodes. De eigen functionaliteit als client blijft volledig behouden — berichten versturen, ontvangen, DM's en Room-toegang werken gewoon door.

> [!WARNING]
> **Let op:** Client Repeat Mode verhoogt het batterijverbruik aanzienlijk, omdat de radio vaker actief is. Gebruik bij voorkeur een apparaat met USB-voeding of een grotere batterij wanneer je langdurig als repeater wilt fungeren.

## Client vs. Repeater vs. Client Repeat

| Eigenschap | Client | Repeater | Client Repeat |
|---|---|---|---|
| Berichten versturen | Ja | Nee | Ja |
| Berichten ontvangen | Ja | Nee | Ja |
| Pakketten doorsturen | Nee | Ja | Ja |
| Companion-app | Ja | Nee | Ja |
| Batterijverbruik | Laag | Hoog | Hoog |
| Dedicated hardware nodig | Nee | Ja | Nee |

## Bron

Dit artikel is gebaseerd op de publicatie van Ripple over de Off-Grid Client Repeat Mode:<br> [buymeacoffee.com/ripplebiz — Off-Grid Client Repeat Mode ↗](https://buymeacoffee.com/ripplebiz/off-grid-client-repeat-mode)
