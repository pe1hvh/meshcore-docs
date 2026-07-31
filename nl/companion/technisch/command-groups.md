# De commandogroepen

*58 COMMANDO'S · NEGEN GROEPEN · GERESERVEERDE NUMMERS · WAT ONTBREEKT*

De firmware kent achtenvijftig commando's, verdeeld over een nummerreeks van
1 tot 65 met zeven gaten erin. Ze staan in één `#define`-blok en worden
afgehandeld door één else-if-keten. Dit hoofdstuk ordent ze naar onderwerp,
zodat te zien is welke een client nodig heeft en welke bijzaak zijn.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 juli 2026 — bestand
> `examples/companion_radio/MyMesh.cpp` r.6-64 voor de nummers en de
> else-if-keten daaronder voor de afhandeling. De indeling in groepen is van
> deze documentatie en staat niet zo in de firmware;
> `tools/companion-opcodes.py` controleert dat elk nummer precies in één
> groep valt.

## Alle 58 commando's worden door de firmware afgehandeld

Elk `#define CMD_…` heeft een bijbehorende `cmd_frame[0] == …` in de
afhandeling: 58 van de 58. Er zijn dus geen commando's die wel een nummer
hebben maar niets doen. Wat er wél is, zijn gereserveerde nummers zonder
naam:

| Ongebruikt | Wat de firmware erover zegt |
|---|---|
| 44 – 49 | `// NOTE: CMD range 44..49 parked, potentially for WiFi operations` |
| 53 | geen toelichting |

Een client mag die nummers niet gebruiken en moet erop rekenen dat ze in een
latere versie betekenis krijgen.

## Sessie en apparaat — 12 commando's

Alles wat over de verbinding zelf en het apparaat gaat.

| Nr | Commando | Doel |
|---|---|---|
| 1 | `CMD_APP_START` | de app meldt zich met een naam; antwoord is `RESP_CODE_SELF_INFO` |
| 22 | `CMD_DEVICE_QUERY` | versieonderhandeling en de grenzen van dit apparaat |
| 5 | `CMD_GET_DEVICE_TIME` | de klok van de node uitlezen |
| 6 | `CMD_SET_DEVICE_TIME` | de klok zetten; nodig vóór alles met een tijdstempel |
| 19 | `CMD_REBOOT` | herstarten |
| 51 | `CMD_FACTORY_RESET` | wissen; verlangt letterlijk de tekst `reset` als argument |
| 37 | `CMD_SET_DEVICE_PIN` | de BLE-pincode wijzigen |
| 20 | `CMD_GET_BATT_AND_STORAGE` | accuspanning en opslaggebruik |
| 56 | `CMD_GET_STATS` | tellers; tweede byte kiest kern, radio of pakketten |
| 43 | `CMD_GET_TUNING_PARAMS` | fijnafstelling uitlezen |
| 21 | `CMD_SET_TUNING_PARAMS` | fijnafstelling zetten (ontvangstvertraging, AGC) |
| 38 | `CMD_SET_OTHER_PARAMS` | handmatig contacten toevoegen en de drie telemetriemodi |

## Identiteit en aankondiging — 9 commando's

| Nr | Commando | Doel |
|---|---|---|
| 7 | `CMD_SEND_SELF_ADVERT` | zichzelf aankondigen; argument bepaalt zero-hop of flood |
| 8 | `CMD_SET_ADVERT_NAME` | de naam waaronder de node zich meldt |
| 14 | `CMD_SET_ADVERT_LATLON` | de positie in de aankondiging |
| 23 | `CMD_EXPORT_PRIVATE_KEY` | de privésleutel eruit halen |
| 24 | `CMD_IMPORT_PRIVATE_KEY` | een privésleutel terugzetten |
| 42 | `CMD_GET_ADVERT_PATH` | het bewaarde pad naar een node opvragen |
| 33 | `CMD_SIGN_START` | ondertekenen beginnen; antwoord meldt de maximale lengte |
| 34 | `CMD_SIGN_DATA` | een brok gegevens aanleveren |
| 35 | `CMD_SIGN_FINISH` | afsluiten; antwoord is de handtekening |

Twee termen uit de eerste regel: **zero-hop** betekent rechtstreeks, zonder
dat andere nodes het bericht doorsturen. **Flood** betekent dat elke
daarvoor geschikte node het doorstuurt, zodat het zich over het hele
bereikbare netwerk verspreidt.

> [!WARNING]
> `CMD_EXPORT_PRIVATE_KEY` (23) geeft de identiteit van de node weg. Wie de
> sleutel heeft, is de node — berichten ondertekenen, directe berichten
> ontsleutelen, alles. Een client die dit commando aanbiedt, hoort het achter
> een expliciete bevestiging te zetten en het resultaat nooit te loggen.

## Contacten — 9 commando's

| Nr | Commando | Doel |
|---|---|---|
| 4 | `CMD_GET_CONTACTS` | alle contacten, optioneel alleen die na een tijdstempel |
| 9 | `CMD_ADD_UPDATE_CONTACT` | toevoegen of wijzigen |
| 15 | `CMD_REMOVE_CONTACT` | verwijderen |
| 16 | `CMD_SHARE_CONTACT` | een contact over de mesh delen |
| 17 | `CMD_EXPORT_CONTACT` | een contact als deelbare tekst opvragen |
| 18 | `CMD_IMPORT_CONTACT` | zo'n tekst weer inlezen |
| 30 | `CMD_GET_CONTACT_BY_KEY` | één contact opzoeken op het eerste deel van de publieke sleutel |
| 58 | `CMD_SET_AUTOADD_CONFIG` | het bitmasker voor automatisch toevoegen: één getal waarvan elke bit een soort node aan- of uitzet |
| 59 | `CMD_GET_AUTOADD_CONFIG` | datzelfde masker uitlezen |

## Kanalen — 2 commando's

| Nr | Commando | Doel |
|---|---|---|
| 31 | `CMD_GET_CHANNEL` | één kanaalplaats lezen, op index |
| 32 | `CMD_SET_CHANNEL` | één kanaalplaats schrijven: index, naam, sleutel |

Er is geen commando om een kanaal te verwijderen. Een plaats leegmaken doe
je door haar te overschrijven.

## Berichten — 6 commando's

| Nr | Commando | Doel |
|---|---|---|
| 2 | `CMD_SEND_TXT_MSG` | direct bericht aan een contact |
| 3 | `CMD_SEND_CHANNEL_TXT_MSG` | bericht op een kanaal |
| 10 | `CMD_SYNC_NEXT_MESSAGE` | het volgende bericht uit de wachtrij halen |
| 62 | `CMD_SEND_CHANNEL_DATA` | los gegevenspakket (datagram) op een kanaal, maximaal 167 bytes |
| 25 | `CMD_SEND_RAW_DATA` | ruwe gegevens naar een contact |
| 65 | `CMD_SEND_RAW_PACKET` | een compleet opgebouwd pakket injecteren |

Dat laatste commando is de achterdeur voor gereedschap: de app bouwt het
pakket zelf en de node zendt het uit zonder er iets aan toe te voegen.

## Verbinding met andere nodes — 8 commando's

Voor repeaters, room servers en sensoren die een sessie verlangen.

| Nr | Commando | Doel |
|---|---|---|
| 26 | `CMD_SEND_LOGIN` | inloggen op een node op afstand |
| 29 | `CMD_LOGOUT` | die sessie beëindigen |
| 28 | `CMD_HAS_CONNECTION` | is er nog een sessie met deze sleutel |
| 27 | `CMD_SEND_STATUS_REQ` | statusvraag |
| 39 | `CMD_SEND_TELEMETRY_REQ` | telemetrie opvragen; de firmware noemt dit zelf vervangbaar |
| 50 | `CMD_SEND_BINARY_REQ` | het opvolgende, getypeerde verzoek |
| 55 | `CMD_SEND_CONTROL_DATA` | besturingsgegevens, rechtstreeks (zero-hop) |
| 57 | `CMD_SEND_ANON_REQ` | verzoek aan een node die geen contact is |

Nummer 57 werkt alleen vanaf `FIRMWARE_VER_CODE` 13; op oudere firmware
verlangt de node dat de ontvanger een bekend contact is.

## Radio en pad — 7 commando's

| Nr | Commando | Doel |
|---|---|---|
| 11 | `CMD_SET_RADIO_PARAMS` | frequentie, bandbreedte, spreiding, codering |
| 12 | `CMD_SET_RADIO_TX_POWER` | zendvermogen, begrensd op `MAX_LORA_TX_POWER` |
| 13 | `CMD_RESET_PATH` | het bewaarde pad naar een contact wissen |
| 36 | `CMD_SEND_TRACE_PATH` | een route traceren |
| 52 | `CMD_SEND_PATH_DISCOVERY_REQ` | een pad laten zoeken |
| 61 | `CMD_SET_PATH_HASH_MODE` | hoe de node paden vergelijkt: op de volledige route of op een verkorte vingerafdruk daarvan (padhash); waarden 0 tot 2 |
| 60 | `CMD_GET_ALLOWED_REPEAT_FREQ` | de frequentiebereiken waarin herhalen mag |

Nummer 60 is regelgeving in code: de node geeft de bereiken terug waarbinnen
`client repeat` toegestaan is. Zie
[Regelgeving & Duty Cycle](../../gebruik/regulations.md).

## Regio en verspreidingsgebied — 3 commando's

| Nr | Commando | Doel |
|---|---|---|
| 54 | `CMD_SET_FLOOD_SCOPE_KEY` | tijdelijke sleutel voor het verspreidingsgebied, of versturen zonder beperking tot een gebied forceren |
| 63 | `CMD_SET_DEFAULT_FLOOD_SCOPE` | het vaste standaardgebied van de node |
| 64 | `CMD_GET_DEFAULT_FLOOD_SCOPE` | die standaard uitlezen |

Deze drie zijn de reden dat de app moet bijhouden bij welk kanaal welk
verspreidingsgebied (*scope*) hoort: de firmware bewaart die koppeling niet.
Zie
[Regio's en Scopes](../../techniek/regions-and-scopes.md).

## Eigen variabelen — 2 commando's

| Nr | Commando | Doel |
|---|---|---|
| 40 | `CMD_GET_CUSTOM_VARS` | de instelbare variabelen als lijst met komma's |
| 41 | `CMD_SET_CUSTOM_VAR` | er één zetten |

Bedoeld voor sensorvarianten die eigen instellingen meebrengen.

## Wat de officiële specificatie beschrijft

Van deze achtenvijftig staan er zeven bij naam in
`docs/companion_protocol.md`: `CMD_APP_START`, `CMD_DEVICE_QUERY`,
`CMD_GET_CHANNEL`, `CMD_SET_CHANNEL`, `CMD_SEND_CHANNEL_TXT_MSG`,
`CMD_SEND_CHANNEL_DATA` en `CMD_GET_BATT_AND_STORAGE`. Van de 46 antwoord-
en pushcodes staan er vijf in.

Dat is geen verwijt aan de specificatie — die zegt zelf nog in ontwikkeling
te zijn — maar het is wel de reden dat een ontwikkelaar van een client de
firmware nodig heeft en niet genoeg heeft aan alleen dit document.

## Bronnen

Firmware, commit `03b6ef4` (v1.16.0, 28 juli 2026):

- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — de nummers r.6-64 en de afhandeling daaronder
- [`docs/companion_protocol.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/docs/companion_protocol.md)
  — de officiële specificatie en wat die wel beschrijft

Reproductie:

- `tools/companion-opcodes.py` — de nummers, de groepsindeling en de
  dekkingscijfers
- `tools/companion-opcodes-snapshot.json` — de uitkomst op commit `03b6ef4`

Verwante hoofdstukken:

- [Het interactiemodel](../logisch/interaction-model.md) — hoe een commando
  aan zijn antwoord komt
- [Het frame](frame-format.md) — wat er in de payload past
- [Architectuur van een client](client-architecture.md) — hoe je dit in
  lagen giet
