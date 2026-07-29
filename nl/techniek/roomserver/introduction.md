# Wat een Room Server is

*BBS · STORE-AND-FORWARD · INLOGGEN · WAT JE ALS GEBRUIKER MERKT*

Een kanaal is als roepen in een zaal: wie er op dat moment is hoort het, wie
weg is heeft pech. Een room server is de node die het gesprek voor je
vasthoudt. Je logt in met een wachtwoord, je stuurt je bericht naar de server
in plaats van de lucht in, en wie later terugkomt krijgt alsnog te horen wat
hij gemist heeft. Dit hoofdstuk legt uit wat dat in de praktijk betekent — de
techniek erachter staat in de vier hoofdstukken die hierop volgen.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestanden
> `examples/simple_room_server/MyMesh.h`,
> `examples/simple_room_server/MyMesh.cpp`, `src/helpers/ClientACL.h`,
> `src/helpers/AdvertDataHelpers.h`, en de officiële `docs/faq.md`. De
> cijfers over build-targets komen uit
> [`tools/room-server-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/room-server-overview.py).

## De vergelijking die klopt

De officiële FAQ zet het scherp neer: een kanaal lijkt op roepen, een room
server op e-mail. Bij een kanaal ontvang je een bericht op het moment dat het
verstuurd wordt, of je ontvangt het nooit. Bij een room server staat het
klaar tot je het komt ophalen — of preciezer: tot de server het aan je kwijt
kan.

![Een kanaalbericht bereikt alleen wie op dat moment aanstaat; een room
server bewaart de post en levert hem af zodra de ontvanger terug is](../../../images/nl/room-server-overview-1.svg)

Dat verschil is de hele reden dat het ding bestaat. Voor een groep die niet
tegelijk online is — een vereniging, een wijk, een groep wandelaars die
verspreid onderweg is — is een kanaal onbruikbaar en een room server precies
wat je zoekt.

De naam *BBS* die je in de firmware tegenkomt (de standaardnaam van een
onbeschreven room server is letterlijk `Test BBS`) verwijst naar de bulletin
boards van voor het internet: een centrale plek waar je berichten achterlaat
en berichten ophaalt, en waar niemand tegelijk aanwezig hoeft te zijn.

## Wat je als gebruiker doet

1. **De server verschijnt in je contactenlijst.** Een room server zendt
   periodiek een advert uit, net als elke andere node, maar met een eigen
   type. Je client herkent daaraan dat het geen gewone gesprekspartner is
   maar een server, en zet hem apart.
2. **Je logt in met een wachtwoord.** Er zijn twee wachtwoorden: één voor
   gewone deelnemers en één voor de beheerder. Welke je invult bepaalt wat je
   mag. Standaard staat het deelnemerswachtwoord in de meeste firmware op
   `hello` en het beheerderswachtwoord op `password` — beide horen bij
   ingebruikname te worden veranderd.
3. **Je stuurt je bericht naar de server.** Voor je client voelt dat als een
   direct bericht aan één contact. De server maakt er een *post* van en zet
   die in zijn wachtrij.
4. **De server duwt de posts naar je toe.** Je haalt niets op: de server
   houdt per deelnemer bij tot hoe ver die is, en stuurt de volgende post
   zodra hij tijd heeft. Voor elke post wil hij een ontvangstbevestiging
   terug; blijft die uit, dan probeert hij het opnieuw.

Bij stap 4 zit het grootste verschil met wat mensen verwachten. Er is geen
knop "haal mijn berichten op". De server werkt zijn deelnemers één voor één
af, in een vaste ronde, en stuurt per beurt één post. Wie lang weg is
geweest, krijgt zijn achterstand dus druppelsgewijs binnen en niet in één
klap.

## Wat een room server níet doet

Deze lijst is langer dan je zou denken, en hij is belangrijker dan de lijst
hierboven. Vier dingen die vaak worden aangenomen en die de firmware niet
biedt:

| Verwachting | Wat de firmware doet |
|---|---|
| Je ziet wie er in de room zit | Er is geen ledenlijst. Alleen een beheerder kan een lijst opvragen, en daar staan uitsluitend andere beheerders in |
| De geschiedenis blijft bewaard | De wachtrij heeft 32 plaatsen en staat alleen in het werkgeheugen. Na een herstart is alles weg |
| Een beheerder voegt leden toe en verwijdert ze | Er is één commando dat rechten zet op een publieke sleutel. Toevoegen en verwijderen als handeling bestaat niet |
| Een room server versterkt ook het netwerk | Doorsturen staat standaard uit. Je kunt het aanzetten, maar de officiële FAQ raadt dat af: dan mis je de functies die alleen de repeater-firmware heeft |

> [!WARNING]
> **Reken niet op een room server als archief.** De 32 posts staan in RAM en
> nergens anders. Een stroomstoring, een lege accu of een `reboot` wist ze
> zonder waarschuwing. De server is een doorgeefluik dat even kan wachten,
> geen opslagplaats. Wie het gesprek wil bewaren, bewaart het op de client.

## Hoeveel er van zijn

De room server is geen zijspoor in het project. Van de 79 variantmappen in de
firmware hebben er **65** minstens één room-server-build-target, samen
**73** targets — sommige borden hebben er twee of drie, voor een andere
schermvariant of een ander zendvermogen. Vrijwel elk bord dat MeshCore
ondersteunt kan dus een room server worden; het is een kwestie van andere
firmware flashen, niet van andere hardware kopen.

De firmware zelf is klein: vijf bestanden, samen 1518 regels, waarvan
`MyMesh.cpp` er 1030 voor zijn rekening neemt. Dat is te overzien, en het is
de reden dat de volgende hoofdstukken tot op de byte kunnen gaan.

## Waar dit verder gaat

- [Inloggen en de ACL](login-and-acl.md) — de drie wachtwoordpaden, wat je
  met welk wachtwoord mag, en wat er van je lidmaatschap een herstart
  overleeft.
- [Posts en synchronisatie](posts-and-sync.md) — hoe een bericht een post
  wordt, hoe de wachtrij werkt en hoe de server bijhoudt wie waar is.
- [Requests en CLI](requests-and-cli.md) — wat een client verder aan de
  server kan vragen, en hoe je hem op afstand beheert.
- [Grenzen en open einden](limits-and-todos.md) — wat de firmware nog niet
  doet, inclusief de `TODO`'s die er letterlijk in staan.

Voor de plek van de room server tussen de andere communicatievormen, zie
[Communicatie](../../gebruik/communication.md). Voor het pakket waarin een
post over de lucht gaat, zie [Direct Messages](../direct-messages.md) — een
post gebruikt hetzelfde payloadtype.

## Bronnen

- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `src/helpers/AdvertDataHelpers.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/AdvertDataHelpers.h)
- [MeshCore firmware — `docs/faq.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/faq.md)
