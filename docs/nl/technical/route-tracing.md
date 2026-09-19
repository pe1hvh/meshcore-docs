# Route traceren

*TECHNIEK · WAAROM EEN PAD NOOIT 100% ZEKER IS*

── Inleiding ────────────────────────────────────────────────────

De berichten-pagina toont bij elk bericht een kaart met de route die een pakket heeft afgelegd. Die weergave is een **benadering** — geen exacte reconstructie. MeshCore registreert wel welke nodes een pakket hebben doorgestuurd, maar de combinatie van het routeringsprotocol, de pakketstructuur en de RF-omstandigheden maakt het onmogelijk om met 100% zekerheid te zeggen welk pad een bericht heeft gevolgd. Deze pagina legt uit waarom.

⚠️ Kort gezegd:
een MeshCore-pakket reist gelijktijdig via meerdere routes. De ontvanger registreert uitsluitend de route van de
eerste
kopie die binnenkomt. Alle andere routes zijn onzichtbaar.
── 1. Flood routing ─────────────────────────────────────────────

## 1 · Flood routing — first arrival wins

Wanneer een node voor de eerste keer een bericht naar een contactpersoon stuurt — of wanneer een eerder geleerd pad is weggevallen — gebruikt MeshCore `ROUTE_TYPE_FLOOD`.<sup>[[2]](#bron2)</sup> Het pakket wordt dan naar alle bereikbare repeaters gestuurd, die het op hun beurt weer doorsturen. Elke repeater voegt zijn eigen hash toe aan het path-veld van het pakket en stuurt het door na een willekeurige vertraging.

Het gevolg is dat de ontvanger *meerdere kopieën* van hetzelfde pakket ontvangt — elk via een andere fysieke route. De firmware controleert met `hasSeen()` of het pakket al eerder is verwerkt.<sup>[[2]](#bron2)</sup> Alleen de **eerste** kopie wordt verwerkt; alle latere kopies worden stil genegeerd. Het path dat wordt geregistreerd is dus uitsluitend het pad van de snelste kopie op dat moment — bepaald door RF-omstandigheden en willekeurige backoff-timers, niet door een deterministisch algoritme.

> [!NOTE]
> Gevolg:
> er kunnen tien routes zijn waarlangs een pakket de bestemming heeft bereikt. Slechts één daarvan is zichtbaar in de hopdata.

── 2. Staggered retransmission ─────────────────────────────────

## 2 · Niet-deterministisch — staggered retransmission

Om botsingen op het LoRa-kanaal te voorkomen gebruikt MeshCore een staggered retransmission mechanisme: repeaters wachten een berekende tijd voordat ze een pakket doorsturen. De wachttijd is omgekeerd evenredig met de ontvangen signaalsterkte (SNR) — een repeater met een sterk signaal mag eerder zenden dan een met een zwak signaal.<sup>[[4]](#bron4)</sup>

Dit zorgt er in de praktijk voor dat de repeater met de beste verbinding als eerste het pakket doorstuurt, en daarmee de race wint. Maar RF-omstandigheden variëren continu door atmosferische condities, beweging van nodes en interferentie. Hetzelfde bericht, een minuut later verstuurd onder iets gewijzigde omstandigheden, kan een volledig ander pad volgen — ook al is de netwerktopologie identiek.

── 3. Hash-collisies ────────────────────────────────────────────

## 3 · Hash-collisies bij 1-byte paden

In het oorspronkelijke MeshCore-protocol wordt de eerste byte van de publieke sleutel van een repeater gebruikt als identifier in het path-veld. Met één byte zijn er slechts 254 bruikbare unieke waarden (0x00 en 0xFF zijn gereserveerd).<sup>[[3]](#bron3)</sup> In grotere netwerken hebben meerdere repeaters dezelfde eerste byte. Het pakket wordt correct doorgestuurd — het netwerk functioneert gewoon — maar analysehulpmiddelen kunnen niet met zekerheid bepalen welke fysieke repeater de identifier vertegenwoordigt.

| Hash-grootte | Unieke ID's | Botsingsrisico bij 100 nodes | Vanaf firmware |
|---|---|---|---|
| 1 byte | 254 | ~33% kans op ≥1 botsing | alle versies |
| 2 byte | 65.534 | <0,08% | v1.14+ |
| 3 byte | 16.777.214 | verwaarloosbaar | v1.14+ |

── 4. Multibyte ─────────────────────────────────────────────────

## 4 · Multibyte paden — collisies opgelost, andere problemen niet

Vanaf firmware versie 1.14 kunnen repeaters adverteren met 1-, 2- of 3-byte adressen, en kunnen companions berichten versturen met corresponderende path-groottes.<sup>[[3]](#bron3)</sup> Met 3-byte hashes is de kans op een botsing in alle praktische netwerken verwaarloosbaar klein.

Multibyte lost echter uitsluitend het *collisieprobleem* op. De overige oorzaken van onzekerheid — first-arrival flood, staggered retransmission, `removeSelfFromPath()` en ontbrekende GPS-data — blijven volledig van kracht, ongeacht de hash-grootte.

> [!NOTE]
> Conclusie:
> 2- en 3-byte paden maken de hopdata
> betrouwbaarder
> , maar niet
> compleet
> . Het fundamentele probleem dat alleen de eerste ontvangen route zichtbaar is, lossen ze niet op.

── 5. removeSelfFromPath ────────────────────────────────────────

## 5 · `removeSelfFromPath()` — het pad wordt onderweg gewijzigd

Wanneer een repeater een direct-gerouteerd pakket doorstuurt, roept de firmware `removeSelfFromPath()` aan.<sup>[[2]](#bron2)</sup> Deze methode verwijdert de hash van de doorstuurende repeater uit het path-veld, zodat de volgende hop in de keten weet wie er nog volgt in de route.

Dit is technisch noodzakelijk voor correcte werking van direct routing, maar heeft als neveneffect dat het path-veld in het ontvangen pakket *niet meer de volledige originele route* bevat zoals die door de zender is opgebouwd. Een deel van de routehistorie is onderweg verwijderd.

── 6. Alleen de eerste kopie ───────────────────────────────────

## 6 · Slechts één van meerdere gelijktijdige kopies is zichtbaar

Bij flood routing stuurt elke repeater die het pakket ontvangt het door — alle routes die het netwerk kent worden tegelijk bewandeld. De bestemming ontvangt meerdere kopieën via verschillende fysieke paden. Nadat de eerste kopie is verwerkt, worden alle volgende kopieën door `hasSeen()` stil gedropt.<sup>[[4]](#bron4)</sup>

Er bestaat geen mechanisme in het protocol om bij te houden hoeveel alternatieve routes het pakket ook hebben gedragen, of welke routes dat waren. Die informatie is definitief verloren zodra de eerste kopie is verwerkt.

── 7. GPS ───────────────────────────────────────────────────────

## 7 · GPS-data is optioneel en niet-realtime

MeshCore-nodes adverteren hun positie alleen wanneer de gebruiker dat handmatig initieert, of op een geconfigureerd interval. Repeaters sturen standaard elke 12 uur een flood-advert.<sup>[[3]](#bron3)</sup> De positiedata in de node-database is op het moment van ontvangst van een bericht dus mogelijk verouderd, onvolledig, of helemaal afwezig.

Nodes zonder GPS-coördinaten kunnen geografisch niet worden geplaatst. Ook nodes die wél coördinaten hebben geadverteerd kunnen onderweg zijn — hun geregistreerde positie hoeft niet overeen te komen met hun locatie op het moment dat zij het pakket doorgaven.

── Samenvatting ─────────────────────────────────────────────────

## Samenvatting

**First-arrival flood**

- **Oorzaak 1** — Alleen de snelste van meerdere gelijktijdige routes wordt geregistreerd.

**Staggered retransmission**

- **Oorzaak 2** — Welke repeater "wint" hangt af van de SNR op dat moment — niet deterministisch.

**1-byte hash-collisies**

- **Oorzaak 3** — 254 unieke ID's voor potentieel honderden nodes — zelfde ID, andere fysieke node.

**Multibyte onvolledig**

- **Oorzaak 4** — 2/3-byte lost collisies op, maar niet het fundamentele first-arrival probleem.

**removeSelfFromPath()**

- **Oorzaak 5** — Repeaters verwijderen hun eigen hash onderweg — de volledige originele route gaat verloren.

**Alternatieve routes onzichtbaar**

- **Oorzaak 6** — Alle kopies na de eerste worden gedropt zonder enige logging van hun routes.

**Ontbrekende of verouderde GPS**

- **Oorzaak 7** — Positiedata is opt-in en maximaal 12 uur oud — geografische plaatsing is een benadering.

**Benadering, geen exacte route**

- **Conclusie** — De kaartweergave toont één momentopname van één route — niet het volledige propagatiepad.

── Bronnen ──────────────────────────────────────────────────────

## Bronnen

1. [1]  LocalMesh NL — MeshCore routing algoritmen: [localmesh.nl/en/meshcore-routing-algorithms/ ↗](https://www.localmesh.nl/en/meshcore-routing-algorithms/)
2. [2]  DeepWiki — MeshCore broncode: Routing and Path Discovery (src/Mesh.cpp): [deepwiki.com/meshcore-dev/MeshCore/7.2-routing-and-path-discovery ↗](https://deepwiki.com/meshcore-dev/MeshCore/7.2-routing-and-path-discovery)
3. [3]  GitHub — MeshCore FAQ (docs/faq.md): [github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md ↗](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md)
4. [4]  Eastmesh Wiki — MeshCore routing internals: [wiki.eastmesh.au/meshcore/routing ↗](https://wiki.eastmesh.au/meshcore/routing)
5. [5]  GitHub — MeshCore Packet.h (broncode pakketstructuur): [github.com/meshcore-dev/MeshCore/blob/main/src/Packet.h ↗](https://github.com/meshcore-dev/MeshCore/blob/main/src/Packet.h)
6. [6]  LocalMesh NL — MeshCore protocol uitleg: [localmesh.nl/en/meshcore-protocol-explained/ ↗](https://www.localmesh.nl/en/meshcore-protocol-explained/)
7. [7]  NodakMesh — MeshCore explained: device roles & routing: [nodakmesh.org/blog/meshcore-how-it-works-guide ↗](https://nodakmesh.org/blog/meshcore-how-it-works-guide)
