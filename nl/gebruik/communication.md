# Communicatie

*CHANNELS · ROOM SERVERS · DIRECT MESSAGES*

MeshCore kent drie communicatievormen: **Channels** voor real-time groepschat, **Room Servers** voor persistente groepscommunicatie met store-and-forward, en **Direct Messages** voor privé end-to-end versleutelde berichten.

## Channels

Een Channel is een gedeelde cryptografische sleutel (PSK voor AES-128 encryptie). Nodes met dezelfde sleutel kunnen elkaars berichten lezen. Er is geen centrale server of ledenlijst — berichten zijn real-time en worden niet opgeslagen.

### Public Channel (#public)

Het standaard kanaal dat automatisch wordt toegevoegd bij elke installatie. Dit is het "marktplaats" kanaal waar iedereen op luistert. Handig voor eerste contact, maar geen privacy.

### Hashtag Channel (#naam)

Community-kanalen voor specifieke onderwerpen of regio's, zoals **#switzerland**, **#berlin**, of **#morsecode**. De sleutel wordt berekend uit de naam, dus iedereen die de naam kent kan meeluisteren.

### Private Channel (eigen sleutel)

Een kanaal met een zelf gekozen, willekeurige sleutel die je alleen deelt met de beoogde deelnemers. Dit biedt echte privacy — alleen wie de sleutel heeft kan meeluisteren.

## Room Servers

Een Room Server is een fysieke node met server-firmware die werkt als een BBS (Bulletin Board System). Het biedt:

- **Store-and-forward** — berichten worden opgeslagen tot de ontvanger online komt
- **Ledenlijst** — je ziet wie er in de Room zit
- **Beheer** — moderators kunnen leden toevoegen en verwijderen
- **Persistentie** — tot 32 berichten worden bewaard

Gebruikers loggen in met een wachtwoord en kunnen later berichten ophalen die verstuurd zijn terwijl ze offline waren.

## Direct Messages (DM)

Privéberichten tussen twee specifieke nodes. DM's zijn **end-to-end versleuteld** en kunnen alleen worden gelezen door de afzender en ontvanger.

### Hoe DM's werken

1. Node A zendt een *advert* uit met zijn public key
2. Node B ontvangt de advert en slaat de public key op
3. Node B kan nu een versleuteld DM naar Node A sturen
4. Voor tweerichtingsverkeer moet Node B ook een advert uitzenden

> [!NOTE]
> **Zero-hop of flood.** Een advert kan op twee manieren de lucht in. Een
> *zero-hop* advert blijft bij de directe buren: niemand stuurt hem door. Een
> *flood* advert wordt wél door repeaters doorgegeven, tot een eigen hoplimiet
> (`flood.max.advert`) en met verlaagde prioriteit. Nodes hoeven elkaar dus niet
> per se direct te kunnen horen voor de key-uitwisseling; dat hangt af van hoe de
> advert is verstuurd.

Voor de techniek achter een DM — hoe het pad wordt geleerd, hoe het pakket eruit
ziet en waarom er geen regiocode in zit — zie
[Direct Messages](../techniek/direct-messages.md).

## Channels vs. Rooms vs. DM's

| Eigenschap | Channel | Room Server | Direct Message |
|---|---|---|---|
| Opslag | Geen | Store-and-forward | Geen |
| Privacy | Gedeelde sleutel | Wachtwoord | End-to-end |
| Ledenlijst | Nee | Ja | N.v.t. |
| Offline berichten | Nee | Ja | Nee |
| Server nodig | Nee | Ja (dedicated node) | Nee |
