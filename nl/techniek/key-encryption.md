# Private & Public Key Encryptie

*IDENTITEIT · VERTROUWEN · VERTROUWELIJKHEID · ZONDER INTERNET*

## Het probleem: communicatie zonder autoriteit

MeshCore is ontworpen voor situaties waarin er **geen internet, geen servers en geen centrale autoriteit** beschikbaar is. Denk aan noodcommunicatie bij een ramp, off-grid operaties in afgelegen gebieden, of gewoon een autonoom lokaal netwerk dat niet afhankelijk is van telecomproviders of cloudinfrastructuur.

Dat klinkt mooi, maar het schept een probleem. In een normaal netwerk (internet, WhatsApp, Signal) staat er altijd een **vertrouwde derde partij** tussen: een server die identiteiten controleert, certificaten uitgeeft, en sleutels uitwisselt. Op een open mesh-radionetwerk bestaat die partij niet. Elke node is gelijk — er is niemand die zegt "deze node is echt wie hij zegt dat hij is."

De cryptografie in MeshCore lost drie problemen op die ontstaan wanneer je die vertrouwde derde partij weghaalt:

> [!NOTE]
> **1. Identiteit** — Hoe weet ik met wie ik communiceer als er geen server is die gebruikers registreert?
> **2. Authenticiteit** — Hoe weet ik dat een bericht echt van die node komt en niet is vervalst door iemand anders?
> **3. Vertrouwelijkheid** — Hoe voorkom ik dat derden meelezen op een open radiokanaal waar letterlijk iedereen kan luisteren?

Het antwoord op alle drie is hetzelfde fundament: **public/private key cryptografie**. Elk communicatietype in MeshCore — channels, DM's, Room Servers — maakt op een andere manier gebruik van dit fundament, afgestemd op de specifieke behoefte van dat type communicatie.

## Het Ed25519 Keypair: je identiteit op het mesh

Bij het eerste flashen genereert elke node een **Ed25519 keypair**. Dit is geen willekeurig detail — het is het moment waarop de node zijn **unieke, onvervalsbare identiteit** krijgt. Zonder centrale registratie is dit keypair het enige bewijs dat een node is wie hij zegt dat hij is.

| Sleutel | Grootte | Doel |
|---|---|---|
| Private Key | 64 bytes | Geheim — verlaat nooit het apparaat. Bewijst identiteit door berichten te ondertekenen, en maakt het mogelijk om gedeelde geheimen te berekenen voor versleutelde communicatie. |
| Public Key | 32 bytes | Openbaar — wordt verspreid via ADVERT-pakketten. Andere nodes gebruiken deze om jouw identiteit te herkennen, jouw handtekeningen te verifiëren, en versleutelde berichten naar jou te sturen. |

De eerste byte (2 hex-karakters) van de public key fungeert als **verkorte node-identifier** in trace paths en pakket-routing. In een groeiend mesh kunnen deze 1-byte identifiers botsen; een custom key generator kan dan een uniek prefix garanderen.

> [!NOTE]
> **Vergelijk het met een handtekening:** je public key is je naam die iedereen kent. Je private key is de manier waarop je je handtekening zet — uniek, niet na te maken, en het bewijs dat jij het bent.

## ADVERT: jezelf bekend maken zonder server

Op het internet registreer je een account bij een dienst en die dienst vertelt anderen dat je bestaat. Op een mesh is er geen dienst. De oplossing: elke node **kondigt zichzelf aan** via een ADVERT-pakket (payload type `0x04`).

```text
┌──────────────┬────────────┬──────────────┬──────────────────┐
│  Public Key  │ Timestamp  │  Signature   │     App Data     │
│   32 bytes   │  4 bytes   │   64 bytes   │  0-32 bytes      │
└──────────────┴────────────┴──────────────┴──────────────────┘
```

Dit pakket wordt altijd **flood-routed** — elke repeater stuurt het door. Elk veld dient een specifiek doel in het opbouwen van vertrouwen zonder centrale autoriteit:

- **Public Key** (32 bytes) — jouw volledige publieke sleutel, zodat andere nodes jou kunnen "leren kennen" en later beveiligd met jou kunnen communiceren
- **Ed25519 Signature** (64 bytes) — de handtekening dekt public key, timestamp en app data, gezet **met jouw private key**. Dit lost het *authenticiteits*-probleem op: niemand kan een ADVERT namens jou vervalsen, want alleen jij bezit de private key die bij de public key hoort
- **Timestamp** (4 bytes) — bescherming tegen **replay-aanvallen**: als iemand een oud ADVERT opnieuw uitstuurt, weigeren ontvangers het omdat ze al een nieuwere timestamp van dezelfde afzender hebben
- **App Data** (maximaal 32 bytes) — een flags-byte met het node-type (chat / repeater / room server / sensor), optioneel GPS-coördinaten, en de naam. Er is geen apart lengteveld: de app data loopt tot het einde van de payload

> [!WARNING]
> **Dit is het fundament:** zonder ADVERT-uitwisseling is geen enkele beveiligde communicatie mogelijk. Het ontvangen van iemands public key via een ADVERT is het moment waarop je DM's naar die node kunt versturen. Geen ADVERT ontvangen = geen versleutelde communicatie mogelijk.

## Channel Berichten: open plein vs. afgesloten kamer

Niet alle communicatie hoeft privé te zijn. Een mesh-netwerk heeft ook behoefte aan **open communicatie** — een digitaal marktplein waar iedereen kan meelezen, en aan **groepskanalen** voor specifieke onderwerpen of teams. Hier wordt een ander type sleutel gebruikt: de **PSK (Pre-Shared Key)**.

### Waarom geen public/private keys voor channels?

Het ECDH-mechanisme dat DM's beveiligt, werkt per definitie tussen **twee** nodes — het berekent een gedeeld geheim uit twee keypairs. Een groepschannel heeft echter tientallen of honderden deelnemers die allemaal dezelfde berichten moeten kunnen lezen. Dat vereist een **gedeelde groepssleutel** (PSK) in plaats van per-paar sleutels. Het is een bewuste architectuurkeuze: groepscommunicatie offert individuele cryptografische identiteit op voor schaalbaarheid.

### Wat is een PSK?

Een PSK (Pre-Shared Key) is een encryptiesleutel die **vooraf wordt gedeeld** tussen alle deelnemers — via QR-code, persoonlijk overhandigd, of via een ander beveiligd kanaal buiten het mesh om. Alle nodes met dezelfde PSK kunnen berichten op dat channel lezen en schrijven. Het persoonlijke keypair van de node speelt hierbij geen rol.

### Pakketstructuur (payload type 0x05)

```text
┌──────────────┬──────────┬──────────────────────────┐
│ Channel Hash │   MAC    │   Encrypted Payload      │
│   1 byte     │  2 bytes │      variable            │
└──────────────┴──────────┴──────────────────────────┘
```

Na decryptie met de PSK bevat de payload:

```text
┌───────────┬───────┬────────────────────┐
│ Timestamp │ Flags │  "NaamNode: tekst" │
│  4 bytes  │ 1 byte│     variable       │
└───────────┴───────┴────────────────────┘
```

### Drie typen channels, drie niveaus van openheid

De keuze tussen channel-typen is een bewuste afweging tussen **bereikbaarheid** en **vertrouwelijkheid**:

| Channel Type | Hoe de PSK bepaald wordt | Doel |
|---|---|---|
| Public | Vaste, bekende key (bv. `AQ==`) | Open communicatie — het dorpsplein van het mesh waar iedereen welkom is |
| Hashtag (#naam) | Hash van de channel-naam | Thematische organisatie — als een gedeelde tafel in een café, niet geheim maar wel afgeschermd van de drukte |
| Private | Random gegenereerd, out-of-band gedeeld | Besloten groep — als een vergaderruimte met slot, alleen toegankelijk voor wie de sleutel heeft ontvangen |

### Hoe het over de ether gaat

Channel-berichten worden **altijd flood-routed**: elke repeater stuurt het pakket blindelings door, ook als die repeater de inhoud niet kan lezen. Dit is essentieel voor het doel van channels — **maximaal bereik**. De Channel Hash (1 byte) is een snelle filter zodat een node kan checken of het een passende PSK heeft zonder alles te moeten decrypten.

> [!WARNING]
> **Let op:** Het public channel is technisch versleuteld (AES-128), maar omdat de PSK algemeen bekend is, biedt het geen werkelijke privacy. Het doel van encryptie hier is niet geheimhouding, maar het correct kunnen decoderen van het bericht uit het radiosignaal.

## Direct Messages: privégesprek zonder tussenpersoon

Channels lossen het probleem van groepscommunicatie op, maar voor een **privégesprek** tussen twee personen zijn ze ongeschikt — iedereen met de PSK kan meelezen. Hier komen de public en private keys tot hun recht via **ECDH (Elliptic Curve Diffie-Hellman)**.

### Het doel: een gedeeld geheim zonder het ooit uit te wisselen

Het bijzondere van ECDH is dat twee nodes een **identiek geheim** kunnen berekenen zonder dat geheim ooit over de radio te sturen. Dit is het belangrijkste in een mesh-omgeving: alles wat je over de ether stuurt, kan door elke repeater en elke luisteraar worden opgepikt. Met ECDH hoeft het geheim zelf nooit de radio op.

### Het ECDH-proces

1. Node A kent de **public key** van Node B (ontvangen via ADVERT)
2. Node A berekent: `shared_secret = ECDH(A_private, B_public)`
3. Node B berekent onafhankelijk: `shared_secret = ECDH(B_private, A_public)`
4. Beide uitkomsten zijn **wiskundig identiek** — eigenschap van elliptische krommen
5. Het shared secret wordt eenmalig berekend bij het toevoegen van een contact en gecached
6. Alle berichten worden AES-versleuteld met dit shared secret

> [!NOTE]
> **Waarom werkt dit zonder centrale autoriteit?** Omdat het vertrouwen zit in de wiskunde, niet in een server. Zelfs als een aanvaller alle ADVERT-pakketten met public keys onderschept, kan hij het shared secret niet berekenen — daarvoor is een van de twee private keys nodig, en die verlaten nooit het apparaat.

### Pakketstructuur (payload type 0x02)

```text
┌───────────┬──────────┬──────────┬──────────────────────────┐
│ Dest Hash │ Src Hash │   MAC    │   Encrypted Payload      │
│  1 byte   │  1 byte  │  2 bytes │      variable            │
└───────────┴──────────┴──────────┴──────────────────────────┘
```

De **Dest Hash** en **Src Hash** zijn de eerste bytes van de public keys van ontvanger en afzender. Repeaters kunnen het pakket routeren (ze zien de hashes), maar **niet de inhoud lezen**. Dit is het hart van de privacy: zelfs de infrastructuur die je bericht doorgeeft, kan niet meelezen.

Na decryptie met het ECDH shared secret:

```text
┌───────────┬───────┬──────────┬──────────────────┐
│ Timestamp │ Flags │   Text   │ Optional: Attempt│
│  4 bytes  │ 1 byte│ variable │     1 byte       │
└───────────┴───────┴──────────┴──────────────────┘
```

### Routing en bevestiging

Anders dan channels kunnen DM's zowel **flood-** als **direct-routed** zijn. Als het mesh eerder een pad naar de ontvanger heeft geleerd, volgt het bericht dat specifieke pad — efficiënter en minder belastend voor het netwerk. De ontvanger stuurt een **ACK** terug: een 4-byte SHA256-hash over timestamp, tekst en de public key van de afzender, als bewijs dat het bericht ongewijzigd is aangekomen.

## Room Servers: groepschat met geheugen én anonimiteit

Channels zijn real-time en hebben geen geheugen — als je offline bent, mis je berichten. DM's zijn privé maar alleen één-op-één. Room Servers combineren het beste van beide: **groepscommunicatie met berichtopslag**. Maar het inloggen op een Room Server brengt een extra privacyrisico: je zou je vaste identiteit blootgeven aan de server.

### Oplossing: ephemeral (tijdelijke) keys

Bij het benaderen van een Room Server wordt een **ANON_REQ**-pakket (type `0x07`) verstuurd. Hiervoor genereert de node een **wegwerp-keypair** — een tijdelijke identiteit die alleen voor deze sessie bestaat:

1. De node maakt een ephemeral Ed25519 keypair aan
2. De ephemeral public key gaat mee in het pakket
3. De Room Server leidt hieruit een tijdelijk shared secret af
4. Na authenticatie (wachtwoord) krijgt de gebruiker de laatste ongelezen berichten

Het doel: je vaste identiteit (je echte public key) wordt niet direct blootgesteld bij het eerste contact. Dit biedt een **extra privacylaag** — de Room Server hoeft niet te weten wie je "echt" bent om je berichten te leveren.

| Room Type | Toegang | Typisch gebruik |
|---|---|---|
| Public Room | Leeg of breed gedeeld wachtwoord | Open groepscommunicatie met berichtgeschiedenis |
| Private Room | Geheim wachtwoord | Besloten teamcommunicatie met opslag |
| Read-only Room | Alleen admins schrijven | Aankondigingen, bulletins, nieuwsfeeds |

## Het grotere plaatje: waarom verschillende mechanismen?

Op het eerste gezicht lijkt het complex: PSK's, ECDH, ephemeral keys — waarom niet gewoon één systeem? Het antwoord ligt in de **fundamenteel verschillende doelen** van elk communicatietype:

| Type | Primair doel | Encryptie | Rol Keypair | Routing |
|---|---|---|---|---|
| Public Channel | Maximaal bereik, open communicatie | AES-128 met bekende PSK | Geen | Flood |
| Hashtag Channel | Thematisch groeperen zonder registratie | AES-128 met hash van naam | Geen | Flood |
| Private Channel | Beveiligde groepscommunicatie | AES-128 met random PSK | Geen | Flood |
| Direct Message | Maximale privacy tussen twee nodes | AES-128 met ECDH secret | Centraal | Flood of Direct |
| Room Server | Groepschat met geheugen én anonimiteit | Wachtwoord + ephemeral ECDH | Tijdelijk keypair | Direct |

Het spectrum loopt van **volledig open** (public channel: iedereen kan meeluisteren) naar **maximaal privé** (DM: alleen de twee betrokken nodes). Elk communicatietype is een bewuste afweging tussen bereikbaarheid, schaalbaarheid en vertrouwelijkheid — en elk gebruikt precies het cryptografische mechanisme dat bij die afweging past.

## De rode draad: keys in elk pakket

De public keys zijn niet alleen relevant voor encryptie — ze zijn verweven in de **basis van elk pakket** dat over het mesh vliegt:

```text
┌────────┬──────────┬─────────────────────────┐
│ Header │ Path Len │ Path[]                  │
│ 1 byte │ 1 byte   │ 1 byte per hop, max 64  │
└────────┴──────────┴─────────────────────────┘

Header byte = payload type + route type (flood of direct)
Path[]      = lijst van node-identifiers (eerste bytes van public keys)
```

Bij **flood routing** voegt elke repeater zijn eigen identifier (= eerste byte public key) toe aan het path. Bij **direct routing** staat het volledige geplande pad er al in en pelt elke hop er één af.

De public keys functioneren dus op **twee niveaus** tegelijk:

- **Routing-adressen** — de eerste byte van de public key is het "huisnummer" waarmee pakketten hun weg door het mesh vinden
- **Cryptografische basis** — de volledige public key is de grondstof voor ECDH shared secrets (DM's) en handtekeningverificatie (ADVERT's)

Dit dubbele gebruik maakt het systeem elegant: dezelfde identiteit die een node uniek maakt op het netwerk, is tegelijk de sleutel tot beveiligde communicatie — allemaal zonder dat er ooit een server, een provider of een certificaatautoriteit aan te pas komt.
