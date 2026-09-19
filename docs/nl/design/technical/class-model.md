# Het klassenmodel

*CONTRACT · IMPLEMENTATIE · ZELFSTANDIG · GRENSGEVALLEN*

De 233 klassen van MeshCore vallen in drie soorten uiteen: klassen die
vastleggen wat een ander onderdeel mag verwachten, klassen die zo'n afspraak
implementeren, en klassen die op zichzelf staan. Dit hoofdstuk beschrijft die
driedeling, benoemt wat een contract wél en niet is, en loopt de 144 klassen
uit de gedeelde broncode stuk voor stuk langs. De 89 uit `variants/` staan als
samenvatting aan het eind.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.17.1, commit `d929643`, 14 augustus 2026 — elke klasse in de tabellen is
> nagelopen op bestand en regelnummer in `src/`, `examples/` en `variants/`.

## Wat een contract is

Een contract is een klasse die uitsluitend bestaat om vast te leggen wat een
ander onderdeel mag verwachten. Hij bevat geen werkende code, alleen de
opsomming van wat een implementatie moet kunnen, plus soms een
standaardantwoord voor het geval de hardware iets niet kan. In C++ herken je
hem aan virtuele methoden, waarvan de verplichte op `= 0` eindigen.

Drie eigenschappen maken iets tot contract:

1. **Het beschrijft, het doet niet.** `Radio` weet niet hoe je een SX1262
   aanstuurt; het legt vast dat er iets moet zijn dat bytes verstuurt.
2. **De gebruiker kent alleen het contract.** De pakketafhandeling houdt een
   `Radio*` vast en heeft geen idee welke chip eraan hangt.
3. **Implementaties zijn onderling verwisselbaar.** Elke klasse die het
   contract implementeert, kan elke andere vervangen zonder dat de gebruiker
   verandert.

De logische kant van dit verhaal — welke afspraken er zijn en wat ze beloven —
staat in [Contracten](../logical/interfaces.md). Hier gaat het om de klassen
die ze dragen.

![Drie kolommen. Links zeventien interfaceklassen zonder eigen code, in het
midden vijfenzestig klassen die er een implementeren met pijlen naar links,
rechts tweeënzestig zelfstandige klassen zonder pijlen. Onderaan loopt een brede
balk met de negenentachtig klassen uit variants naar de middelste kolom.](../../../images/nl/class-model-1.svg)

## Wat geen contract is

Een basisklasse waar gedeelde code in zit, is geen contract maar een
gemeenschappelijke ouder. `ESP32Board` is zo'n geval: hij implementeert het
bordcontract *en* biedt code die de afgeleide bordklassen erven. Hij staat
daarom in groep 2, niet in groep 1.

Het onderscheid is niet altijd scherp. `BridgeBase` en `RadioLibWrapper` zijn
allebei een implementatie én een ouder: ze implementeren `AbstractBridge`
respectievelijk `mesh::Radio`, en er hangen weer klassen onder die van hen
erven. Wie de driedeling als een harde indeling leest, komt bij die twee in de
problemen. Ze staan in groep 2 omdat ze een contract implementeren; dat ze er
zelf ook kinderen onder hebben, verandert niets aan die eigenschap.

`ConfigSerializer` is sinds v1.17.1 het scherpste grensgeval. De klasse draagt
werkende code — een reeks `def()`-methoden en `loadSerial()` en `saveSerial()`,
samen de JSON-lezer en -schrijver — en dat pleit voor een gemeenschappelijke
ouder. Toch staat hij in groep 1. Hij heeft één verplichte methode
(`structure()`, op `= 0`), zijn gebruikers in `CommonCLI` houden een
`ConfigSerializer&` vast zonder te weten welk instellingenblok eraan hangt, en
de twaalf blokken zijn onderling verwisselbaar. Eigenschap 2 en 3 gelden dus
onverkort; alleen eigenschap 1 gaat niet helemaal op. Wie de indeling anders
leest en hem in groep 3 plaatst, verschuift daarmee ook zijn twaalf
instellingenblokken naar groep 3.

**Zelfstandig** is alles wat geen contract is en er ook geen implementeert:
klassen die één ding doen en waar meestal niets van af hangt. `ClientACL`
beheert de rechtenlijst, `RegionMap` zet regiocodes om, `Packet` is een
gegevensobject. Ze zijn niet vervangbaar omdat er niets is dat ze zou moeten
kunnen vervangen.

Twee klassen in groep 3 hebben wél kinderen: `mesh::Mesh` en `Identity`. Ze
dragen werkende code en implementeren zelf geen contract, dus zijn het
gemeenschappelijke ouders. Hun rechtstreekse afgeleiden `BaseChatMesh` en
`LocalIdentity` staan daarom ook in groep 3, en met hen de `MyMesh` uit
`examples/simple_secure_chat/` — die erft van `BaseChatMesh` en
`ContactVisitor`, en geen van beide is een contract. De vier andere
`MyMesh`-klassen staan wél in groep 2, omdat zij daarnaast
`CommonCLICallbacks` of `DataStoreHost` implementeren.

> [!NOTE]
> **Afwijking van de vorige uitgave.** Tot en met `03b6ef4` stonden
> `BaseChatMesh`, `LocalIdentity` en de `MyMesh` uit `simple_secure_chat` in
> groep 2, met *Mesh* respectievelijk *Identiteit* in de kolom *Contract*.
> Geen van beide namen kwam ooit in de contractentabel van groep 1 voor; de
> indeling was op dat punt niet sluitend. Dat is hier rechtgezet, wat groep 2
> met drie verlaagt en groep 3 met drie verhoogt.

Een leerzaam geval is `CustomSX1262`. Die staat in groep 3, niet in groep 2.
De klasse erft van RadioLibs `SX1262` en implementeert geen MeshCore-contract;
het is `CustomSX1262Wrapper` die dat doet, via `RadioLibWrapper`. Dat
verklaart waarom er twee klassen per radiochip zijn: één die de chipdriver
aanpast, één die het resultaat in het MeshCore-contract giet. Zie
[Radiorealisatie](radio-realisation.md). Sinds v1.17.1 geldt hetzelfde voor
`CustomLR2021` en `CustomLR2021Wrapper`; zie [De
LR2021](../../hardware/radio/lr2021.md).

## De verdeling

De gedeelde broncode telt 144 klassen: **17** interfaceklassen, **65**
implementatieklassen en **62** zelfstandige klassen.

| Groep | Aantal | Kenmerk |
|---|---|---|
| 1 — interfaceklassen | 17 | Alleen virtuele methoden, geen werkende code |
| 2 — implementatieklassen | 65 | Erft van een klasse uit groep 1 |
| 3 — zelfstandig | 62 | Geen contract, implementeert er ook geen |

Ten opzichte van `03b6ef4` kwamen er 25 klassen bij en verdwenen er twee uit
`variants/`. De grootste post is de omzetting van de instellingen naar JSON:
`ConfigSerializer` plus twaalf instellingenblokken, samen dertien van de 25.
Daarnaast kwamen ethernet (`SerialEthernetInterface` met twee
hardwarespecifieke afgeleiden), de LR2021 (`CustomLR2021` en
`CustomLR2021Wrapper`), een externe watchdog, een draaiknop, het
kleurenschema `UIColor`, het scherm `NV3001BDisplay`, de haptiek
`DRV2605Vibration` en `MultiSerialInterface` erbij.

De twee verdwenen klassen heetten allebei `NullDisplayDriver` en stonden in
`variants/minewsemi_me25ls01/` en `variants/wio-e5-mini/`. Ze zijn niet
geschrapt maar samengetrokken: er staat nu één gedeelde
`src/helpers/ui/NullDisplayDriver.h`. Dat verklaart meteen waarom de
schermklassen in `variants/` van drie naar één zakken.

## Groep 1 — interfaceklassen (17)

| Klasse | Plek |
|---|---|
| `DataStoreHost` | `examples/companion_radio/DataStore.h` r.8 |
| `MillisecondClock` | `src/Dispatcher.h` r.14 |
| `Radio` | `src/Dispatcher.h` r.22 |
| `PacketManager` | `src/Dispatcher.h` r.87 |
| `MeshTables` | `src/Mesh.h` r.16 |
| `MainBoard` | `src/MeshCore.h` r.45 |
| `RTCClock` | `src/MeshCore.h` r.87 |
| `RNG` | `src/Utils.h` r.9 |
| `AbstractBridge` | `src/helpers/AbstractBridge.h` r.5 |
| `BaseSerialInterface` | `src/helpers/BaseSerialInterface.h` r.7 |
| `CommonCLICallbacks` | `src/helpers/CommonCLI.h` r.197 |
| `ConfigSerializer` | `src/helpers/ConfigSerializer.h` r.17 |
| `ExternalWatchdogManager` | `src/helpers/ExternalWatchdogManager.h` r.3 |
| `SensorManager` | `src/helpers/SensorManager.h` r.12 |
| `LocationProvider` | `src/helpers/sensors/LocationProvider.h` r.6 |
| `DisplayDriver` | `src/helpers/ui/DisplayDriver.h` r.14 |
| `RotaryInput` | `src/helpers/ui/RotaryInput.h` r.11 |

Drie dingen vallen op aan deze lijst.

`SensorManager` en `LocationProvider` staan niet in `src/` maar in
`src/helpers/`. Dat is geen vergissing: het zijn contracten die pas nodig
werden toen sensoren erbij kwamen, en ze zijn niet naar de kern verhuisd.
Voor `ConfigSerializer`, `ExternalWatchdogManager` en `RotaryInput` geldt
hetzelfde: alle drie nieuw in v1.17.1, alle drie in `src/helpers/`.

`CommonCLICallbacks` en `DataStoreHost` draaien de afhankelijkheid om. Ze
worden gedefinieerd door de laag die eronder zit, maar geïmplementeerd door de
applicatie erboven — `MyMesh` in `examples/simple_repeater/` implementeert
`CommonCLICallbacks`, zodat de bediening in `src/helpers/CommonCLI.cpp`
iets kan aanroepen zonder te weten welke applicatie draait. De onderliggende
laag roept de bovenliggende aan zonder hem te kennen.

`ExternalWatchdogManager` is het enige contract zonder verplichte methode. Alle
vier de methoden zijn virtueel met een standaardantwoord: `begin()` geeft
`false`, `getIntervalMs()` geeft nul, `loop()` en `feed()` doen niets. Een bord
zonder externe watchdog hoeft er dus niets mee te doen; twee borden
overschrijven ze wel.

## Groep 2 — implementatieklassen (65)

| Klasse | Contract | Plek | Erft van |
|---|---|---|---|
| `MyMesh` | Opslag | `examples/companion_radio/MyMesh.h` r.87 | BaseChatMesh, DataStoreHost |
| `NodePrefs` | Instellingenblok | `examples/companion_radio/NodePrefs.h` r.12 | ConfigSerializer |
| `RadioPrefs` | Instellingenblok | `examples/companion_radio/NodePrefs.h` r.45 | ConfigSerializer |
| `GPSPrefs` | Instellingenblok | `examples/companion_radio/NodePrefs.h` r.76 | ConfigSerializer |
| `RepeatPrefs` | Instellingenblok | `examples/companion_radio/NodePrefs.h` r.89 | ConfigSerializer |
| `CompanionPrefs` | Instellingenblok | `examples/companion_radio/NodePrefs.h` r.103 | ConfigSerializer |
| `MyMesh` | CLI-terugroep | `examples/simple_repeater/MyMesh.h` r.85 | Mesh, CommonCLICallbacks |
| `MyMesh` | CLI-terugroep | `examples/simple_room_server/MyMesh.h` r.92 | Mesh, CommonCLICallbacks |
| `SensorMesh` | CLI-terugroep | `examples/simple_sensor/SensorMesh.h` r.49 | Mesh, CommonCLICallbacks |
| `MyMesh` | CLI-terugroep | `examples/simple_sensor/main.cpp` r.8 | SensorMesh |
| `VolatileRTCClock` | Realtimeklok | `src/helpers/ArduinoHelpers.h` r.6 | RTCClock |
| `ArduinoMillis` | Klok | `src/helpers/ArduinoHelpers.h` r.22 | MillisecondClock |
| `StdRNG` | Entropiebron | `src/helpers/ArduinoHelpers.h` r.27 | RNG |
| `ArduinoSerialInterface` | Seriële verbinding | `src/helpers/ArduinoSerialInterface.h` r.6 | BaseSerialInterface |
| `AutoDiscoverRTCClock` | Realtimeklok | `src/helpers/AutoDiscoverRTCClock.h` r.7 | RTCClock |
| `NodePrefs` | Instellingenblok | `src/helpers/CommonCLI.h` r.23 | ConfigSerializer |
| `RadioPrefs` | Instellingenblok | `src/helpers/CommonCLI.h` r.75 | ConfigSerializer |
| `BridgePrefs` | Instellingenblok | `src/helpers/CommonCLI.h` r.102 | ConfigSerializer |
| `GPSPrefs` | Instellingenblok | `src/helpers/CommonCLI.h` r.118 | ConfigSerializer |
| `PowerPrefs` | Instellingenblok | `src/helpers/CommonCLI.h` r.131 | ConfigSerializer |
| `RepeatPrefs` | Instellingenblok | `src/helpers/CommonCLI.h` r.143 | ConfigSerializer |
| `RoomPrefs` | Instellingenblok | `src/helpers/CommonCLI.h` r.158 | ConfigSerializer |
| `ESP32Board` | Bord | `src/helpers/ESP32Board.h` r.19 | MainBoard |
| `ESP32RTCClock` | Realtimeklok | `src/helpers/ESP32Board.h` r.200 | RTCClock |
| `MeshadventurerBoard` | Bord | `src/helpers/MeshadventurerBoard.h` r.18 | ESP32Board |
| `MultiSerialInterface` | Seriële verbinding | `src/helpers/MultiSerialInterface.h` r.19 | BaseSerialInterface |
| `NRF52Board` | Bord | `src/helpers/NRF52Board.h` r.27 | MainBoard |
| `NRF52BoardDCDC` | Bord | `src/helpers/NRF52Board.h` r.76 | NRF52Board |
| `SimpleMeshTables` | Meshtabellen | `src/helpers/SimpleMeshTables.h` r.11 | MeshTables |
| `StaticPoolPacketManager` | Pakketbeheer | `src/helpers/StaticPoolPacketManager.h` r.21 | PacketManager |
| `BridgeBase` | Brug | `src/helpers/bridges/BridgeBase.h` r.21 | AbstractBridge |
| `ESPNowBridge` | Brug | `src/helpers/bridges/ESPNowBridge.h` r.42 | BridgeBase |
| `RS232Bridge` | Brug | `src/helpers/bridges/RS232Bridge.h` r.47 | BridgeBase |
| `ESPNOWRadio` | Radio | `src/helpers/esp32/ESPNOWRadio.h` r.5 | Radio |
| `SerialBLEInterface` | Seriële verbinding | `src/helpers/esp32/SerialBLEInterface.h` r.11 | BaseSerialInterface, BLESecurityCallbacks, BLEServerCallbacks, BLECharacteristicCallbacks |
| `SerialWifiInterface` | Seriële verbinding | `src/helpers/esp32/SerialWifiInterface.h` r.6 | BaseSerialInterface |
| `TBeamBoard` | Bord | `src/helpers/esp32/TBeamBoard.h` r.91 | ESP32Board |
| `RAK13800EthernetInterface` | Seriële verbinding | `src/helpers/ethernet/RAK13800/RAK13800EthernetInterface.h` r.7 | SerialEthernetInterface |
| `SerialEthernetInterface` | Seriële verbinding | `src/helpers/ethernet/SerialEthernetInterface.h` r.10 | BaseSerialInterface |
| `CH390EthernetInterface` | Seriële verbinding | `src/helpers/ethernet/ch390/CH390EthernetInterface.h` r.10 | SerialEthernetInterface |
| `SerialBLEInterface` | Seriële verbinding | `src/helpers/nrf52/SerialBLEInterface.h` r.10 | BaseSerialInterface |
| `CustomLLCC68Wrapper` | Radio | `src/helpers/radiolib/CustomLLCC68Wrapper.h` r.7 | RadioLibWrapper |
| `CustomLR1110Wrapper` | Radio | `src/helpers/radiolib/CustomLR1110Wrapper.h` r.7 | RadioLibWrapper |
| `CustomLR2021Wrapper` | Radio | `src/helpers/radiolib/CustomLR2021Wrapper.h` r.14 | RadioLibWrapper |
| `CustomSTM32WLxWrapper` | Radio | `src/helpers/radiolib/CustomSTM32WLxWrapper.h` r.8 | RadioLibWrapper |
| `CustomSX1262Wrapper` | Radio | `src/helpers/radiolib/CustomSX1262Wrapper.h` r.11 | RadioLibWrapper |
| `CustomSX1268Wrapper` | Radio | `src/helpers/radiolib/CustomSX1268Wrapper.h` r.11 | RadioLibWrapper |
| `CustomSX1276Wrapper` | Radio | `src/helpers/radiolib/CustomSX1276Wrapper.h` r.10 | RadioLibWrapper |
| `RadioLibWrapper` | Radio | `src/helpers/radiolib/RadioLibWrappers.h` r.14 | Radio |
| `RadioNoiseListener` | Entropiebron | `src/helpers/radiolib/RadioLibWrappers.h` r.88 | RNG |
| `RAK12500LocationProvider` | Plaatsbepaling | `src/helpers/sensors/EnvironmentSensorManager.cpp` r.177 | LocationProvider |
| `EnvironmentSensorManager` | Sensorbeheer | `src/helpers/sensors/EnvironmentSensorManager.h` r.7 | SensorManager |
| `MicroNMEALocationProvider` | Plaatsbepaling | `src/helpers/sensors/MicroNMEALocationProvider.h` r.40 | LocationProvider |
| `STM32Board` | Bord | `src/helpers/stm32/STM32Board.h` r.6 | MainBoard |
| `E213Display` | Scherm | `src/helpers/ui/E213Display.h` r.12 | DisplayDriver |
| `E290Display` | Scherm | `src/helpers/ui/E290Display.h` r.12 | DisplayDriver |
| `GxEPDDisplay` | Scherm | `src/helpers/ui/GxEPDDisplay.h` r.19 | DisplayDriver |
| `LGFXDisplay` | Scherm | `src/helpers/ui/LGFXDisplay.h` r.12 | DisplayDriver |
| `NV3001BDisplay` | Scherm | `src/helpers/ui/NV3001BDisplay.h` r.27 | DisplayDriver |
| `NullDisplayDriver` | Scherm | `src/helpers/ui/NullDisplayDriver.h` r.5 | DisplayDriver |
| `SSD1306Display` | Scherm | `src/helpers/ui/SSD1306Display.h` r.18 | DisplayDriver |
| `ST7735Display` | Scherm | `src/helpers/ui/ST7735Display.h` r.9 | DisplayDriver |
| `ST7789Display` | Scherm | `src/helpers/ui/ST7789Display.h` r.9 | DisplayDriver |
| `ST7789LCDDisplay` | Scherm | `src/helpers/ui/ST7789LCDDisplay.h` r.10 | DisplayDriver |
| `U8g2Display` | Scherm | `src/helpers/ui/U8g2Display.h` r.19 | DisplayDriver |

> [!NOTE]
> De kolom *Erft van* geeft de basisklassen zoals ze in de declaratie staan,
> zonder het toegangsniveau. Eén uitzondering is het vermelden waard:
> `NRF52BoardDCDC` erft `virtual public NRF52Board`. Die virtuele overerving
> is nodig omdat er tweeëndertig bordklassen in `variants/` onder hangen die
> langs twee wegen bij `NRF52Board` uitkomen; zonder `virtual` zou elk van die
> borden twee kopieën van de basisklasse krijgen.

`SerialBLEInterface` en `MyMesh` komen meer dan eens voor. Dat is geen fout in
de tabel: het zijn verschillende klassen met dezelfde naam, in verschillende
bestanden, en per build compileert er precies één van. `SerialBLEInterface`
bestaat twee keer — één voor ESP32, één voor nRF52 — en `MyMesh` vijf keer,
één per applicatie die er een nodig heeft.

De instellingenblokken komen om dezelfde reden dubbel voor. `NodePrefs`,
`RadioPrefs`, `GPSPrefs` en `RepeatPrefs` staan zowel in
`src/helpers/CommonCLI.h` als in `examples/companion_radio/NodePrefs.h`: de
companion-applicatie houdt een eigen stel blokken aan met andere velden.
`BridgePrefs`, `PowerPrefs` en `RoomPrefs` bestaan alleen in de gedeelde
variant, `CompanionPrefs` alleen in de companion-variant. Twaalf declaraties
onder acht namen dus.

## Groep 3 — zelfstandig (62)

| Klasse | Plek |
|---|---|
| `AbstractUITask` | `examples/companion_radio/AbstractUITask.h` r.25 |
| `DataStore` | `examples/companion_radio/DataStore.h` r.16 |
| `SplashScreen` | `examples/companion_radio/ui-new/UITask.cpp` r.34 |
| `HomeScreen` | `examples/companion_radio/ui-new/UITask.cpp` r.87 |
| `MsgPreviewScreen` | `examples/companion_radio/ui-new/UITask.cpp` r.489 |
| `UITask` | `examples/companion_radio/ui-new/UITask.h` r.25 |
| `Button` | `examples/companion_radio/ui-orig/Button.h` r.12 |
| `UITask` | `examples/companion_radio/ui-orig/UITask.h` r.21 |
| `ScrollingStatusBar` | `examples/companion_radio/ui-tiny/ScrollingStatusBar.h` r.18 |
| `SplashScreen` | `examples/companion_radio/ui-tiny/UITask.cpp` r.34 |
| `HomeScreen` | `examples/companion_radio/ui-tiny/UITask.cpp` r.90 |
| `UITask` | `examples/companion_radio/ui-tiny/UITask.h` r.28 |
| `KissModem` | `examples/kiss_modem/KissModem.h` r.109 |
| `RateLimiter` | `examples/simple_repeater/RateLimiter.h` r.5 |
| `UITask` | `examples/simple_repeater/UITask.h` r.6 |
| `UITask` | `examples/simple_room_server/UITask.h` r.6 |
| `MyMesh` | `examples/simple_secure_chat/main.cpp` r.73 |
| `TimeSeriesData` | `examples/simple_sensor/TimeSeriesData.h` r.11 |
| `UITask` | `examples/simple_sensor/UITask.h` r.6 |
| `Dispatcher` | `src/Dispatcher.h` r.118 |
| `Identity` | `src/Identity.h` r.11 |
| `LocalIdentity` | `src/Identity.h` r.54 |
| `GroupChannel` | `src/Mesh.h` r.7 |
| `Mesh` | `src/Mesh.h` r.27 |
| `Packet` | `src/Packet.h` r.42 |
| `Utils` | `src/Utils.h` r.19 |
| `AdvertDataBuilder` | `src/helpers/AdvertDataHelpers.h` r.19 |
| `AdvertDataParser` | `src/helpers/AdvertDataHelpers.h` r.43 |
| `AdvertTimeHelper` | `src/helpers/AdvertDataHelpers.h` r.68 |
| `ContactVisitor` | `src/helpers/BaseChatMesh.h` r.23 |
| `ContactsIterator` | `src/helpers/BaseChatMesh.h` r.30 |
| `BaseChatMesh` | `src/helpers/BaseChatMesh.h` r.60 |
| `ClientACL` | `src/helpers/ClientACL.h` r.40 |
| `CommonCLI` | `src/helpers/CommonCLI.h` r.252 |
| `Context` | `src/helpers/ConfigSerializer.h` r.23 |
| `IdentityStore` | `src/helpers/IdentityStore.h` r.14 |
| `RTC_RX8130CE` | `src/helpers/RTC_RX8130CE.h` r.9 |
| `RefCountedDigitalPin` | `src/helpers/RefCountedDigitalPin.h` r.5 |
| `BufStream` | `src/helpers/RegionMap.cpp` r.7 |
| `RegionMap` | `src/helpers/RegionMap.h` r.23 |
| `PacketQueue` | `src/helpers/StaticPoolPacketManager.h` r.5 |
| `StatsFormatHelper` | `src/helpers/StatsFormatHelper.h` r.5 |
| `TransportKeyStore` | `src/helpers/TransportKeyStore.h` r.16 |
| `StrHelper` | `src/helpers/TxtDataHelpers.h` r.12 |
| `CustomLLCC68` | `src/helpers/radiolib/CustomLLCC68.h` r.5 |
| `CustomLR1110` | `src/helpers/radiolib/CustomLR1110.h` r.6 |
| `CustomLR2021` | `src/helpers/radiolib/CustomLR2021.h` r.6 |
| `CustomSTM32WLx` | `src/helpers/radiolib/CustomSTM32WLx.h` r.5 |
| `CustomSX1262` | `src/helpers/radiolib/CustomSX1262.h` r.6 |
| `CustomSX1268` | `src/helpers/radiolib/CustomSX1268.h` r.5 |
| `CustomSX1276` | `src/helpers/radiolib/CustomSX1276.h` r.11 |
| `LPPReader` | `src/helpers/sensors/LPPDataHelpers.h` r.66 |
| `LPPWriter` | `src/helpers/sensors/LPPDataHelpers.h` r.175 |
| `DRV2605Vibration` | `src/helpers/ui/DRV2605Vibration.h` r.22 |
| `UIColor` | `src/helpers/ui/DisplayDriver.h` r.8 |
| `GenericVibration` | `src/helpers/ui/GenericVibration.h` r.21 |
| `MomentaryButton` | `src/helpers/ui/MomentaryButton.h` r.11 |
| `String` | `src/helpers/ui/OLEDDisplay.h` r.50 |
| `OLEDDisplay` | `src/helpers/ui/OLEDDisplay.h` r.159 |
| `OLEDDisplay` | `src/helpers/ui/OLEDDisplay.h` r.161 |
| `ST7789Spi` | `src/helpers/ui/ST7789Spi.h` r.96 |
| `UIScreen` | `src/helpers/ui/UIScreen.h` r.17 |

> [!NOTE]
> `OLEDDisplay` komt twee keer voor in `src/helpers/ui/OLEDDisplay.h`, op
> regel 159 en 161, achter een `#if` — de ene versie erft van `Print`, de
> andere van `Stream`. `String` op regel 50 in datzelfde bestand is een
> vooruitverwijzing uit meegeleverde code. Beide zijn geen MeshCore-ontwerp
> maar overgenomen code van ThingPulse; zie [De
> broncodestructuur](source-layout.md).

> [!NOTE]
> `Context` staat op regel 23 van `src/helpers/ConfigSerializer.h` en is geen
> zelfstandige klasse in de gewone zin: hij is genest in `ConfigSerializer` en
> is daarbuiten niet bereikbaar. Hij telt mee omdat de telmethode elke
> declaratie met een body meeneemt, ongeacht nesting.

## De 89 uit `variants/`

`variants/` telt 89 klassendeclaraties onder 84 unieke namen — vijf namen
komen in meer dan één variantmap voor. Ze zijn niet stuk voor stuk
uitgeschreven, omdat ze vrijwel alle hetzelfde doen: een contract
implementeren met de pinbezetting van één bord.

| Contract dat wordt geïmplementeerd | Klassen |
|---|---|
| Bord | 72 |
| Sensorbeheer | 8 |
| Entropiebron | 2 |
| Externe watchdog | 2 |
| Scherm | 1 |
| Draaiknop | 1 |

Drie klassen in `variants/` implementeren geen enkel contract en staan dus in
groep 3. Alle drie heten `LoRaFEMControl` — in `heltec_tower_v2`,
`heltec_v4_r8` en `station_g3_esp32` — en bedienen de zendversterker aan de
antennekant van de radio. Tot en met `03b6ef4` vulde elke klasse in
`variants/` een contract in; dat is niet langer waar.

De 72 bordklassen implementeren alle hetzelfde contract op dezelfde manier.
Vier ervan zijn wél apart het noemen waard, omdat ze de enige
RP2040-bordklassen zijn: die familie heeft als enige geen gedeelde bordklasse
in `src/helpers/`.

| RP2040-bordklasse | Plek |
|---|---|
| `RAK11310Board` | `variants/rak11310/RAK11310Board.h` r.15 |
| `PicoWBoard` | `variants/rpi_picow/PicoWBoard.h` r.11 |
| `WaveshareBoard` | `variants/waveshare_rp2040_lora/WaveshareBoard.h` r.27 |
| `XiaoRP2040Board` | `variants/xiao_rp2040/XiaoRP2040Board.h` r.25 |

Alle andere bordklassen erven van een gedeelde ouder — 32 van
`NRF52BoardDCDC`, 28 van `ESP32Board`, 3 van `NRF52Board`, 3 van
`STM32Board`, plus één van `HeltecV3Board` en één van `TBeamBoard`. Deze vier
erven rechtstreeks van `mesh::MainBoard` en schrijven dus zelf uit wat de
andere 68 van hun ouder krijgen.

![Twee overervingsbomen naast elkaar. Links het bordcontract mesh::MainBoard
met daaronder ESP32Board, NRF52Board en STM32Board en hun afgeleiden; rechts
de vier losse RP2040-bordklassen die rechtstreeks onder het contract hangen,
zonder tussenlaag.](../../../images/nl/class-model-2.svg)

## Narekenen

De klassentelling in dit hoofdstuk komt uit `tools/design-overview.py`:

```bash
python3 tools/design-overview.py /pad/naar/MeshCore --classes
```

Het script telt elke regel van de vorm `class Naam { …` of
`class Naam : basis { …` met de accolade op dezelfde regel. `struct` telt niet
mee, voorwaartse declaraties zonder body evenmin.

De indeling in de drie groepen komt uit `tools/class-groups.py`, dat dezelfde
parser gebruikt:

```bash
python3 tools/class-groups.py /pad/naar/MeshCore
python3 tools/class-groups.py /pad/naar/MeshCore --groep 2 --markdown
```

Groep 1 is in dat script een benoemde lijst, omdat niet mechanisch af te lezen
valt of een klasse een contract is: `DisplayDriver` heeft `width()` en
`height()` met een body en is er toch een, `ESP32Board` heeft virtuele
methoden en is er toch geen. Groep 2 en groep 3 volgen daar wél mechanisch
uit — alles wat rechtstreeks of via tussenliggende klassen van een klasse uit
groep 1 erft, staat in groep 2.

De regelnummers in de tabellen zijn na te lopen met `tools/cite-check.py`:

```bash
python3 tools/cite-check.py /pad/naar/MeshCore docs/nl/design/technical/class-model.md
```

## Bronnen

- [MeshCore `d929643` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/Dispatcher.h)
- [MeshCore `d929643` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/MeshCore.h)
- [MeshCore `d929643` — `src/helpers/`](https://github.com/meshcore-dev/MeshCore/tree/d929643/src/helpers)
- [MeshCore `d929643` — `src/helpers/ConfigSerializer.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ConfigSerializer.h)
- [MeshCore `d929643` — `src/helpers/NRF52Board.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/NRF52Board.h)
- [MeshCore `d929643` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/d929643/variants)
