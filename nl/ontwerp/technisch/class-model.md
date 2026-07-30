# Het klassenmodel

*CONTRACT · INVULLING · ZELFSTANDIG · GRENSGEVALLEN*

De 196 klassen van MeshCore vallen in drie soorten uiteen: klassen die
vastleggen wat een ander onderdeel mag verwachten, klassen die zo'n afspraak
invullen, en klassen die op zichzelf staan. Dit hoofdstuk beschrijft die
driedeling, benoemt wat een contract wél en niet is, en loopt de 119 klassen
uit de gedeelde boom stuk voor stuk langs. De 77 uit `variants/` staan als
samenvatting aan het eind.

> [!NOTE]
> **Bron.** Deze pagina is geverifieerd tegen de firmware zelf: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 juli 2026 — elke klasse in de tabellen is
> nagelopen op bestand en regelnummer in `src/`, `examples/` en `variants/`.

## Wat een contract is

Een contract is een klasse die uitsluitend bestaat om vast te leggen wat een
ander onderdeel mag verwachten. Hij bevat geen werkende code, alleen de
opsomming van wat een invulling moet kunnen, plus soms een standaardantwoord
voor het geval de hardware iets niet kan. In C++ herken je hem aan virtuele
methoden, waarvan de verplichte op `= 0` eindigen.

Drie eigenschappen maken iets tot contract:

1. **Het beschrijft, het doet niet.** `Radio` weet niet hoe je een SX1262
   aanstuurt; het legt vast dat er iets moet zijn dat bytes verstuurt.
2. **De gebruiker kent alleen het contract.** De pakketafhandeling houdt een
   `Radio*` vast en heeft geen idee welke chip eraan hangt.
3. **Invullingen zijn onderling verwisselbaar.** Elke klasse die het contract
   invult, kan elke andere vervangen zonder dat de gebruiker verandert.

De logische kant van dit verhaal — welke afspraken er zijn en wat ze beloven —
staat in [Contracten](../logisch/interfaces.md). Hier gaat het om de klassen
die ze dragen.

![Drie kolommen. Links veertien contractdefiniërende klassen zonder eigen
code, in het midden vijftig klassen die er een invullen met pijlen naar links,
rechts vijfenvijftig zelfstandige klassen zonder pijlen. Onderaan loopt een
brede balk met de zevenenzeventig klassen uit variants naar de middelste
kolom.](../../../images/nl/class-model-1.svg)

## Wat geen contract is

Een basisklasse waar gedeelde code in zit, is geen contract maar een
gemeenschappelijke ouder. `ESP32Board` is zo'n geval: hij vult het bordcontract
in *en* biedt code die de afgeleide bordklassen erven. Hij staat daarom in
groep 2, niet in groep 1.

Het onderscheid is niet altijd scherp. `BridgeBase` en `RadioLibWrapper` zijn
allebei een invulling én een ouder: ze vullen `AbstractBridge` respectievelijk
`mesh::Radio` in, en er hangen weer klassen onder die van hen erven. Wie de
driedeling als een harde indeling leest, komt bij die twee in de problemen.
Ze staan in groep 2 omdat ze een contract invullen; dat ze er zelf ook kinderen
onder hebben, verandert niets aan die eigenschap.

**Zelfstandig** is alles wat geen contract is en er ook geen invult: klassen
die één ding doen en waar niets van af hangt. `ClientACL` beheert de
rechtenlijst, `RegionMap` zet regiocodes om, `Packet` is een gegevensobject.
Ze zijn niet vervangbaar omdat er niets is dat ze zou moeten kunnen vervangen.

Een leerzaam geval is `CustomSX1262`. Die staat in groep 3, niet in groep 2.
De klasse erft van RadioLibs `SX1262` en vult geen MeshCore-contract in; het is
`CustomSX1262Wrapper` die dat doet, via `RadioLibWrapper`. Dat verklaart waarom
er twee klassen per radiochip zijn: één die de chipdriver aanpast, één die het
resultaat in het MeshCore-contract giet. Zie
[Radiorealisatie](radio-realisation.md).

## De verdeling

De gedeelde boom telt 119 klassen: **14** contractdefiniërend, **50**
contractvullend, **55** zelfstandig.

| Groep | Aantal | Kenmerk |
|---|---|---|
| 1 — contractdefiniërend | 14 | Alleen virtuele methoden, geen werkende code |
| 2 — contractvullend | 50 | Erft van een klasse uit groep 1 |
| 3 — zelfstandig | 55 | Geen contract, vult er ook geen in |

## Groep 1 — contractdefiniërend (14)

| Klasse | Plek |
|---|---|
| `DataStoreHost` | `examples/companion_radio/DataStore.h` r.8 |
| `MillisecondClock` | `src/Dispatcher.h` r.14 |
| `Radio` | `src/Dispatcher.h` r.22 |
| `PacketManager` | `src/Dispatcher.h` r.85 |
| `MeshTables` | `src/Mesh.h` r.16 |
| `MainBoard` | `src/MeshCore.h` r.45 |
| `RTCClock` | `src/MeshCore.h` r.80 |
| `RNG` | `src/Utils.h` r.9 |
| `AbstractBridge` | `src/helpers/AbstractBridge.h` r.5 |
| `BaseSerialInterface` | `src/helpers/BaseSerialInterface.h` r.7 |
| `CommonCLICallbacks` | `src/helpers/CommonCLI.h` r.68 |
| `SensorManager` | `src/helpers/SensorManager.h` r.12 |
| `LocationProvider` | `src/helpers/sensors/LocationProvider.h` r.6 |
| `DisplayDriver` | `src/helpers/ui/DisplayDriver.h` r.6 |

Twee dingen vallen op aan deze lijst.

`SensorManager` en `LocationProvider` staan niet in `src/` maar in
`src/helpers/`. Dat is geen vergissing: het zijn contracten die pas nodig
werden toen sensoren erbij kwamen, en ze zijn niet naar de kern verhuisd.

`CommonCLICallbacks` en `DataStoreHost` draaien de afhankelijkheid om. Ze
worden gedefinieerd door de laag die eronder zit, maar ingevuld door de
applicatie erboven — `MyMesh` in `examples/simple_repeater/` vult
`CommonCLICallbacks` in, zodat de bediening in `src/helpers/CommonCLI.cpp`
iets kan aanroepen zonder te weten welke applicatie draait. De onderliggende
laag roept de bovenliggende aan zonder hem te kennen.

## Groep 2 — contractvullend (50)

| Klasse | Contract | Plek | Erft van |
|---|---|---|---|
| `ESP32Board` | Bord | `src/helpers/ESP32Board.h` r.18 | mesh::MainBoard |
| `MeshadventurerBoard` | Bord | `src/helpers/MeshadventurerBoard.h` r.20 | ESP32Board |
| `NRF52Board` | Bord | `src/helpers/NRF52Board.h` r.27 | mesh::MainBoard |
| `NRF52BoardDCDC` | Bord | `src/helpers/NRF52Board.h` r.74 | NRF52Board |
| `STM32Board` | Bord | `src/helpers/stm32/STM32Board.h` r.6 | mesh::MainBoard |
| `TBeamBoard` | Bord | `src/helpers/esp32/TBeamBoard.h` r.91 | ESP32Board |
| `BridgeBase` | Brug | `src/helpers/bridges/BridgeBase.h` r.21 | AbstractBridge |
| `ESPNowBridge` | Brug | `src/helpers/bridges/ESPNowBridge.h` r.42 | BridgeBase |
| `RS232Bridge` | Brug | `src/helpers/bridges/RS232Bridge.h` r.47 | BridgeBase |
| `SimpleMeshTables` | Gezien-tabel | `src/helpers/SimpleMeshTables.h` r.11 | mesh::MeshTables |
| `LocalIdentity` | Identiteit | `src/Identity.h` r.54 | Identity |
| `AutoDiscoverRTCClock` | Klok | `src/helpers/AutoDiscoverRTCClock.h` r.7 | mesh::RTCClock |
| `ESP32RTCClock` | Klok | `src/helpers/ESP32Board.h` r.160 | mesh::RTCClock |
| `VolatileRTCClock` | Klok | `src/helpers/ArduinoHelpers.h` r.6 | mesh::RTCClock |
| `ArduinoSerialInterface` | Koppelvlak | `src/helpers/ArduinoSerialInterface.h` r.6 | BaseSerialInterface |
| `SerialBLEInterface` | Koppelvlak | `src/helpers/esp32/SerialBLEInterface.h` r.9 | BaseSerialInterface, BLESecurityCallbacks, BLEServerCallbacks, BLECharacteristicCallbacks |
| `SerialBLEInterface` | Koppelvlak | `src/helpers/nrf52/SerialBLEInterface.h` r.10 | BaseSerialInterface |
| `SerialWifiInterface` | Koppelvlak | `src/helpers/esp32/SerialWifiInterface.h` r.6 | BaseSerialInterface |
| `MicroNMEALocationProvider` | Locatie | `src/helpers/sensors/MicroNMEALocationProvider.h` r.36 | LocationProvider |
| `RAK12500LocationProvider` | Locatie | `src/helpers/sensors/EnvironmentSensorManager.cpp` r.177 | LocationProvider |
| `BaseChatMesh` | Mesh | `src/helpers/BaseChatMesh.h` r.59 | mesh::Mesh |
| `MyMesh` | Mesh | `examples/simple_secure_chat/main.cpp` r.73 | BaseChatMesh, ContactVisitor |
| `MyMesh` | Mesh | `examples/simple_repeater/MyMesh.h` r.83 | mesh::Mesh, CommonCLICallbacks |
| `MyMesh` | Mesh | `examples/simple_room_server/MyMesh.h` r.91 | mesh::Mesh, CommonCLICallbacks |
| `MyMesh` | Mesh | `examples/simple_sensor/main.cpp` r.8 | SensorMesh |
| `MyMesh` | Mesh | `examples/companion_radio/MyMesh.h` r.87 | BaseChatMesh, DataStoreHost |
| `SensorMesh` | Mesh | `examples/simple_sensor/SensorMesh.h` r.49 | mesh::Mesh, CommonCLICallbacks |
| `ArduinoMillis` | Millisecondeklok | `src/helpers/ArduinoHelpers.h` r.22 | mesh::MillisecondClock |
| `StaticPoolPacketManager` | Pakketvoorraad | `src/helpers/StaticPoolPacketManager.h` r.21 | mesh::PacketManager |
| `CustomLLCC68Wrapper` | Radio | `src/helpers/radiolib/CustomLLCC68Wrapper.h` r.7 | RadioLibWrapper |
| `CustomLR1110Wrapper` | Radio | `src/helpers/radiolib/CustomLR1110Wrapper.h` r.7 | RadioLibWrapper |
| `CustomSTM32WLxWrapper` | Radio | `src/helpers/radiolib/CustomSTM32WLxWrapper.h` r.8 | RadioLibWrapper |
| `CustomSX1262Wrapper` | Radio | `src/helpers/radiolib/CustomSX1262Wrapper.h` r.11 | RadioLibWrapper |
| `CustomSX1268Wrapper` | Radio | `src/helpers/radiolib/CustomSX1268Wrapper.h` r.11 | RadioLibWrapper |
| `CustomSX1276Wrapper` | Radio | `src/helpers/radiolib/CustomSX1276Wrapper.h` r.10 | RadioLibWrapper |
| `ESPNOWRadio` | Radio | `src/helpers/esp32/ESPNOWRadio.h` r.5 | mesh::Radio |
| `RadioLibWrapper` | Radio | `src/helpers/radiolib/RadioLibWrappers.h` r.6 | mesh::Radio |
| `E213Display` | Scherm | `src/helpers/ui/E213Display.h` r.12 | DisplayDriver |
| `E290Display` | Scherm | `src/helpers/ui/E290Display.h` r.12 | DisplayDriver |
| `GxEPDDisplay` | Scherm | `src/helpers/ui/GxEPDDisplay.h` r.19 | DisplayDriver |
| `LGFXDisplay` | Scherm | `src/helpers/ui/LGFXDisplay.h` r.12 | DisplayDriver |
| `NullDisplayDriver` | Scherm | `src/helpers/ui/NullDisplayDriver.h` r.5 | DisplayDriver |
| `SSD1306Display` | Scherm | `src/helpers/ui/SSD1306Display.h` r.18 | DisplayDriver |
| `ST7735Display` | Scherm | `src/helpers/ui/ST7735Display.h` r.10 | DisplayDriver |
| `ST7789Display` | Scherm | `src/helpers/ui/ST7789Display.h` r.9 | DisplayDriver |
| `ST7789LCDDisplay` | Scherm | `src/helpers/ui/ST7789LCDDisplay.h` r.10 | DisplayDriver |
| `U8g2Display` | Scherm | `src/helpers/ui/U8g2Display.h` r.19 | DisplayDriver |
| `EnvironmentSensorManager` | Sensorbeheer | `src/helpers/sensors/EnvironmentSensorManager.h` r.7 | SensorManager |
| `RadioNoiseListener` | Toevalsbron | `src/helpers/radiolib/RadioLibWrappers.h` r.74 | mesh::RNG |
| `StdRNG` | Toevalsbron | `src/helpers/ArduinoHelpers.h` r.27 | mesh::RNG |

> [!NOTE]
> De kolom *Erft van* geeft de basisklassen zoals ze in de declaratie staan,
> zonder het toegangsniveau. Eén uitzondering is het vermelden waard:
> `NRF52BoardDCDC` erft `virtual public NRF52Board`. Die virtuele overerving
> is nodig omdat er dertig bordklassen in `variants/` onder hangen die langs
> twee wegen bij `NRF52Board` uitkomen; zonder `virtual` zou elk van die
> borden twee kopieën van de basisklasse krijgen.

`SerialBLEInterface` en `MyMesh` komen meer dan eens voor. Dat is geen fout in
de tabel: het zijn verschillende klassen met dezelfde naam, in verschillende
bestanden, en per build compileert er precies één van. `SerialBLEInterface`
bestaat twee keer — één voor ESP32, één voor nRF52 — en `MyMesh` vijf keer,
één per applicatie die er een nodig heeft.

## Groep 3 — zelfstandig (55)

| Klasse | Plek |
|---|---|
| `AbstractUITask` | `examples/companion_radio/AbstractUITask.h` r.25 |
| `DataStore` | `examples/companion_radio/DataStore.h` r.16 |
| `SplashScreen` | `examples/companion_radio/ui-new/UITask.cpp` r.34 |
| `HomeScreen` | `examples/companion_radio/ui-new/UITask.cpp` r.86 |
| `MsgPreviewScreen` | `examples/companion_radio/ui-new/UITask.cpp` r.466 |
| `UITask` | `examples/companion_radio/ui-new/UITask.h` r.25 |
| `Button` | `examples/companion_radio/ui-orig/Button.h` r.12 |
| `UITask` | `examples/companion_radio/ui-orig/UITask.h` r.17 |
| `ScrollingStatusBar` | `examples/companion_radio/ui-tiny/ScrollingStatusBar.h` r.18 |
| `SplashScreen` | `examples/companion_radio/ui-tiny/UITask.cpp` r.34 |
| `HomeScreen` | `examples/companion_radio/ui-tiny/UITask.cpp` r.90 |
| `UITask` | `examples/companion_radio/ui-tiny/UITask.h` r.28 |
| `KissModem` | `examples/kiss_modem/KissModem.h` r.100 |
| `RateLimiter` | `examples/simple_repeater/RateLimiter.h` r.5 |
| `UITask` | `examples/simple_repeater/UITask.h` r.6 |
| `UITask` | `examples/simple_room_server/UITask.h` r.6 |
| `TimeSeriesData` | `examples/simple_sensor/TimeSeriesData.h` r.11 |
| `UITask` | `examples/simple_sensor/UITask.h` r.6 |
| `Dispatcher` | `src/Dispatcher.h` r.116 |
| `Identity` | `src/Identity.h` r.11 |
| `GroupChannel` | `src/Mesh.h` r.7 |
| `Mesh` | `src/Mesh.h` r.26 |
| `Packet` | `src/Packet.h` r.42 |
| `Utils` | `src/Utils.h` r.19 |
| `AdvertDataBuilder` | `src/helpers/AdvertDataHelpers.h` r.19 |
| `AdvertDataParser` | `src/helpers/AdvertDataHelpers.h` r.43 |
| `AdvertTimeHelper` | `src/helpers/AdvertDataHelpers.h` r.68 |
| `ContactVisitor` | `src/helpers/BaseChatMesh.h` r.23 |
| `ContactsIterator` | `src/helpers/BaseChatMesh.h` r.30 |
| `ClientACL` | `src/helpers/ClientACL.h` r.40 |
| `CommonCLI` | `src/helpers/CommonCLI.h` r.117 |
| `IdentityStore` | `src/helpers/IdentityStore.h` r.14 |
| `RTC_RX8130CE` | `src/helpers/RTC_RX8130CE.h` r.9 |
| `RefCountedDigitalPin` | `src/helpers/RefCountedDigitalPin.h` r.5 |
| `BufStream` | `src/helpers/RegionMap.cpp` r.7 |
| `RegionMap` | `src/helpers/RegionMap.h` r.23 |
| `PacketQueue` | `src/helpers/StaticPoolPacketManager.h` r.5 |
| `StatsFormatHelper` | `src/helpers/StatsFormatHelper.h` r.5 |
| `TransportKeyStore` | `src/helpers/TransportKeyStore.h` r.16 |
| `StrHelper` | `src/helpers/TxtDataHelpers.h` r.12 |
| `CustomLLCC68` | `src/helpers/radiolib/CustomLLCC68.h` r.8 |
| `CustomLR1110` | `src/helpers/radiolib/CustomLR1110.h` r.6 |
| `CustomSTM32WLx` | `src/helpers/radiolib/CustomSTM32WLx.h` r.8 |
| `CustomSX1262` | `src/helpers/radiolib/CustomSX1262.h` r.8 |
| `CustomSX1268` | `src/helpers/radiolib/CustomSX1268.h` r.8 |
| `CustomSX1276` | `src/helpers/radiolib/CustomSX1276.h` r.11 |
| `LPPReader` | `src/helpers/sensors/LPPDataHelpers.h` r.66 |
| `LPPWriter` | `src/helpers/sensors/LPPDataHelpers.h` r.175 |
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
> vooruitverwijzing uit gevendorde code. Beide zijn geen MeshCore-ontwerp maar
> overgenomen code van ThingPulse; zie [De bronboom](source-layout.md).

## De 77 uit `variants/`

`variants/` telt 77 klassendeclaraties onder 73 unieke namen — vier namen komen
in meer dan één variantmap voor. Ze zijn niet stuk voor stuk uitgeschreven,
omdat ze alle hetzelfde doen: een contract invullen met de pinbezetting van één
bord.

| Contract dat wordt ingevuld | Klassen |
|---|---|
| Bord | 65 |
| Sensorbeheer | 7 |
| Scherm | 3 |
| Toevalsbron | 2 |

De 65 bordklassen vullen alle hetzelfde contract op dezelfde manier in. Vier
ervan zijn wél apart het noemen waard, omdat ze de enige RP2040-bordklassen
zijn: die familie heeft als enige geen gedeelde bordklasse in `src/helpers/`.

| RP2040-bordklasse | Plek |
|---|---|
| `RAK11310Board` | `variants/rak11310/RAK11310Board.h` r.15 |
| `PicoWBoard` | `variants/rpi_picow/PicoWBoard.h` r.11 |
| `WaveshareBoard` | `variants/waveshare_rp2040_lora/WaveshareBoard.h` r.27 |
| `XiaoRP2040Board` | `variants/xiao_rp2040/XiaoRP2040Board.h` r.25 |

Alle andere bordklassen erven van een gedeelde ouder — 30 van
`NRF52BoardDCDC`, 23 van `ESP32Board`, 3 van `NRF52Board`, 3 van
`STM32Board`, plus enkele van `HeltecV3Board` en `TBeamBoard`. Deze vier
erven rechtstreeks van `mesh::MainBoard` en schrijven dus zelf uit wat de
andere 61 van hun ouder krijgen.

![Twee overervingsbomen naast elkaar. Links het bordcontract mesh::MainBoard
met daaronder ESP32Board, NRF52Board en STM32Board en hun afgeleiden; rechts
de vier losse RP2040-bordklassen die rechtstreeks onder het contract hangen,
zonder tussenlaag.](../../../images/nl/class-model-2.svg)

## Narekenen

De aantallen in dit hoofdstuk komen uit `tools/design-overview.py`:

```bash
python3 tools/design-overview.py /pad/naar/MeshCore --classes
```

Het script telt elke regel van de vorm `class Naam { …` of
`class Naam : basis { …` met de accolade op dezelfde regel. `struct` telt niet
mee, voorwaartse declaraties zonder body evenmin.

## Bronnen

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/helpers/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src/helpers)
- [MeshCore `03b6ef4` — `src/helpers/NRF52Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/NRF52Board.h)
- [MeshCore `03b6ef4` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)
