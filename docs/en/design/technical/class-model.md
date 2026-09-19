# The class model

*CONTRACT · IMPLEMENTATION · STANDALONE · BORDERLINE CASES*

MeshCore's 233 classes fall into three kinds: classes that lay down what
another part may expect, classes that implement such an agreement, and classes
that stand on their own. This chapter describes that three-way split, states
what a contract is and is not, and walks through the 144 classes of the shared
tree one by one. The 89 from `variants/` appear as a summary at the end.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.17.1, commit `d929643`, 14 August 2026 — every class in the tables was
> checked for file and line number in `src/`, `examples/` and `variants/`.

## What a contract is

A contract is a class that exists solely to lay down what another part may
expect. It holds no working code, only the list of what an implementation must
be able to do, plus sometimes a default answer for when the hardware cannot do
something. In C++ you recognise it by its virtual methods, the mandatory ones
ending in `= 0`.

Three properties make something a contract:

1. **It describes, it does not do.** `Radio` does not know how to drive an
   SX1262; it lays down that there must be something that sends bytes.
2. **The user knows only the contract.** Packet handling holds a `Radio*` and
   has no idea which chip hangs off it.
3. **Implementations are interchangeable.** Every class that implements the
   contract can replace any other without the user changing.

The logical side of this story — which agreements exist and what they promise
— is in [Contracts](../logical/interfaces.md). Here it is about the classes
that carry them.

![Three columns. On the left seventeen interface classes without code of their
own, in the middle sixty-five classes that implement one, with arrows pointing
left, on the right sixty-two standalone classes without arrows. Along the
bottom runs a wide bar with the eighty-nine classes from variants pointing at
the middle column.](../../../images/en/class-model-1.svg)

## What is not a contract

A base class that holds shared code is not a contract but a common parent.
`ESP32Board` is such a case: it implements the board contract *and* offers
code the derived board classes inherit. It therefore sits in group 2, not
group 1.

The distinction is not always sharp. `BridgeBase` and `RadioLibWrapper` are
both an implementation *and* a parent: they implement `AbstractBridge` and
`mesh::Radio` respectively, and there are classes hanging under them in turn.
Anyone reading the three-way split as a hard partition runs into trouble with
those two. They sit in group 2 because they implement a contract; that they
have children of their own changes nothing about that property.

`ConfigSerializer` is the sharpest borderline case since v1.17.1. The class
carries working code — a series of `def()` methods plus `loadSerial()` and
`saveSerial()`, together the JSON reader and writer — and that argues for a
common parent. It sits in group 1 nonetheless. It has one mandatory method
(`structure()`, on `= 0`), its users in `CommonCLI` hold a `ConfigSerializer&`
without knowing which settings block hangs off it, and the twelve blocks are
interchangeable. Properties 2 and 3 therefore hold in full; only property 1
does not quite. Anyone reading the split differently and placing it in group 3
moves its twelve settings blocks to group 3 along with it.

**Standalone** is everything that is not a contract and implements none
either: classes that do one thing and that mostly have nothing depending on
them. `ClientACL` manages the access list, `RegionMap` converts region codes,
`Packet` is a data object. They are not replaceable because there is nothing
that would have to replace them.

Two classes in group 3 do have children: `mesh::Mesh` and `Identity`. They
carry working code and implement no contract themselves, so they are common
parents. Their direct descendants `BaseChatMesh` and `LocalIdentity` therefore
sit in group 3 as well, and with them the `MyMesh` from
`examples/simple_secure_chat/` — it inherits from `BaseChatMesh` and
`ContactVisitor`, and neither is a contract. The four other `MyMesh` classes
do sit in group 2, because they additionally implement `CommonCLICallbacks` or
`DataStoreHost`.

> [!NOTE]
> **Departure from the previous edition.** Up to and including `03b6ef4`,
> `BaseChatMesh`, `LocalIdentity` and the `MyMesh` from `simple_secure_chat`
> sat in group 2, with *Mesh* and *Identity* respectively in the *Contract*
> column. Neither name ever appeared in the contract table of group 1; the
> classification did not close on that point. That has been put right here,
> which lowers group 2 by three and raises group 3 by three.

An instructive case is `CustomSX1262`. It sits in group 3, not group 2. The
class inherits from RadioLib's `SX1262` and implements no MeshCore contract;
it is `CustomSX1262Wrapper` that does, by way of `RadioLibWrapper`. That
explains why there are two classes per radio chip: one that adapts the chip
driver, one that pours the result into the MeshCore contract. See [Radio
realisation](radio-realisation.md). Since v1.17.1 the same holds for
`CustomLR2021` and `CustomLR2021Wrapper`; see [The
LR2021](../../hardware/radio/lr2021.md).

## The distribution

The shared tree counts 144 classes: **17** interface classes, **65**
implementation classes and **62** standalone classes.

| Group | Count | Characteristic |
|---|---|---|
| 1 — interface classes | 17 | Virtual methods only, no working code |
| 2 — implementation classes | 65 | Inherits from a class in group 1 |
| 3 — standalone | 62 | No contract, implements none either |

Relative to `03b6ef4`, 25 classes were added and two disappeared from
`variants/`. The largest item is the conversion of the settings to JSON:
`ConfigSerializer` plus twelve settings blocks, together thirteen of the 25.
Beyond that came ethernet (`SerialEthernetInterface` with two
hardware-specific descendants), the LR2021 (`CustomLR2021` and
`CustomLR2021Wrapper`), an external watchdog, a rotary input, the colour
scheme `UIColor`, the display `NV3001BDisplay`, the haptics
`DRV2605Vibration` and `MultiSerialInterface`.

The two classes that disappeared were both called `NullDisplayDriver` and sat
in `variants/minewsemi_me25ls01/` and `variants/wio-e5-mini/`. They were not
dropped but merged: there is now one shared
`src/helpers/ui/NullDisplayDriver.h`. That immediately explains why the
display classes in `variants/` fall from three to one.

## Group 1 — interface classes (17)

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

Three things stand out in this list.

`SensorManager` and `LocationProvider` are not in `src/` but in
`src/helpers/`. That is not a mistake: they are contracts that only became
necessary once sensors arrived, and they have not been moved to the core. The
same holds for `ConfigSerializer`, `ExternalWatchdogManager` and
`RotaryInput`: all three new in v1.17.1, all three in `src/helpers/`.

`CommonCLICallbacks` and `DataStoreHost` reverse the dependency. They are
defined by the layer below but implemented by the application above — `MyMesh`
in `examples/simple_repeater/` implements `CommonCLICallbacks` so that the
control code in `src/helpers/CommonCLI.cpp` can call something without knowing
which application is running. The lower layer calls the higher one without
knowing it.

`ExternalWatchdogManager` is the only contract without a mandatory method. All
four of its methods are virtual with a default answer: `begin()` returns
`false`, `getIntervalMs()` returns zero, `loop()` and `feed()` do nothing. A
board without an external watchdog therefore need do nothing with it; two
boards do override them.

## Group 2 — implementation classes (65)

| Klasse | Contract | Plek | Erft van |
|---|---|---|---|
| `MyMesh` | Storage | `examples/companion_radio/MyMesh.h` r.87 | BaseChatMesh, DataStoreHost |
| `NodePrefs` | Settings block | `examples/companion_radio/NodePrefs.h` r.12 | ConfigSerializer |
| `RadioPrefs` | Settings block | `examples/companion_radio/NodePrefs.h` r.45 | ConfigSerializer |
| `GPSPrefs` | Settings block | `examples/companion_radio/NodePrefs.h` r.76 | ConfigSerializer |
| `RepeatPrefs` | Settings block | `examples/companion_radio/NodePrefs.h` r.89 | ConfigSerializer |
| `CompanionPrefs` | Settings block | `examples/companion_radio/NodePrefs.h` r.103 | ConfigSerializer |
| `MyMesh` | CLI callback | `examples/simple_repeater/MyMesh.h` r.85 | Mesh, CommonCLICallbacks |
| `MyMesh` | CLI callback | `examples/simple_room_server/MyMesh.h` r.92 | Mesh, CommonCLICallbacks |
| `SensorMesh` | CLI callback | `examples/simple_sensor/SensorMesh.h` r.49 | Mesh, CommonCLICallbacks |
| `MyMesh` | CLI callback | `examples/simple_sensor/main.cpp` r.8 | SensorMesh |
| `VolatileRTCClock` | Clock | `src/helpers/ArduinoHelpers.h` r.6 | RTCClock |
| `ArduinoMillis` | Millisecond clock | `src/helpers/ArduinoHelpers.h` r.22 | MillisecondClock |
| `StdRNG` | Entropy | `src/helpers/ArduinoHelpers.h` r.27 | RNG |
| `ArduinoSerialInterface` | Interface | `src/helpers/ArduinoSerialInterface.h` r.6 | BaseSerialInterface |
| `AutoDiscoverRTCClock` | Clock | `src/helpers/AutoDiscoverRTCClock.h` r.7 | RTCClock |
| `NodePrefs` | Settings block | `src/helpers/CommonCLI.h` r.23 | ConfigSerializer |
| `RadioPrefs` | Settings block | `src/helpers/CommonCLI.h` r.75 | ConfigSerializer |
| `BridgePrefs` | Settings block | `src/helpers/CommonCLI.h` r.102 | ConfigSerializer |
| `GPSPrefs` | Settings block | `src/helpers/CommonCLI.h` r.118 | ConfigSerializer |
| `PowerPrefs` | Settings block | `src/helpers/CommonCLI.h` r.131 | ConfigSerializer |
| `RepeatPrefs` | Settings block | `src/helpers/CommonCLI.h` r.143 | ConfigSerializer |
| `RoomPrefs` | Settings block | `src/helpers/CommonCLI.h` r.158 | ConfigSerializer |
| `ESP32Board` | Board | `src/helpers/ESP32Board.h` r.19 | MainBoard |
| `ESP32RTCClock` | Clock | `src/helpers/ESP32Board.h` r.200 | RTCClock |
| `MeshadventurerBoard` | Board | `src/helpers/MeshadventurerBoard.h` r.18 | ESP32Board |
| `MultiSerialInterface` | Interface | `src/helpers/MultiSerialInterface.h` r.19 | BaseSerialInterface |
| `NRF52Board` | Board | `src/helpers/NRF52Board.h` r.27 | MainBoard |
| `NRF52BoardDCDC` | Board | `src/helpers/NRF52Board.h` r.76 | NRF52Board |
| `SimpleMeshTables` | Seen table | `src/helpers/SimpleMeshTables.h` r.11 | MeshTables |
| `StaticPoolPacketManager` | Packet pool | `src/helpers/StaticPoolPacketManager.h` r.21 | PacketManager |
| `BridgeBase` | Bridge | `src/helpers/bridges/BridgeBase.h` r.21 | AbstractBridge |
| `ESPNowBridge` | Bridge | `src/helpers/bridges/ESPNowBridge.h` r.42 | BridgeBase |
| `RS232Bridge` | Bridge | `src/helpers/bridges/RS232Bridge.h` r.47 | BridgeBase |
| `ESPNOWRadio` | Radio | `src/helpers/esp32/ESPNOWRadio.h` r.5 | Radio |
| `SerialBLEInterface` | Interface | `src/helpers/esp32/SerialBLEInterface.h` r.11 | BaseSerialInterface, BLESecurityCallbacks, BLEServerCallbacks, BLECharacteristicCallbacks |
| `SerialWifiInterface` | Interface | `src/helpers/esp32/SerialWifiInterface.h` r.6 | BaseSerialInterface |
| `TBeamBoard` | Board | `src/helpers/esp32/TBeamBoard.h` r.91 | ESP32Board |
| `RAK13800EthernetInterface` | Interface | `src/helpers/ethernet/RAK13800/RAK13800EthernetInterface.h` r.7 | SerialEthernetInterface |
| `SerialEthernetInterface` | Interface | `src/helpers/ethernet/SerialEthernetInterface.h` r.10 | BaseSerialInterface |
| `CH390EthernetInterface` | Interface | `src/helpers/ethernet/ch390/CH390EthernetInterface.h` r.10 | SerialEthernetInterface |
| `SerialBLEInterface` | Interface | `src/helpers/nrf52/SerialBLEInterface.h` r.10 | BaseSerialInterface |
| `CustomLLCC68Wrapper` | Radio | `src/helpers/radiolib/CustomLLCC68Wrapper.h` r.7 | RadioLibWrapper |
| `CustomLR1110Wrapper` | Radio | `src/helpers/radiolib/CustomLR1110Wrapper.h` r.7 | RadioLibWrapper |
| `CustomLR2021Wrapper` | Radio | `src/helpers/radiolib/CustomLR2021Wrapper.h` r.14 | RadioLibWrapper |
| `CustomSTM32WLxWrapper` | Radio | `src/helpers/radiolib/CustomSTM32WLxWrapper.h` r.8 | RadioLibWrapper |
| `CustomSX1262Wrapper` | Radio | `src/helpers/radiolib/CustomSX1262Wrapper.h` r.11 | RadioLibWrapper |
| `CustomSX1268Wrapper` | Radio | `src/helpers/radiolib/CustomSX1268Wrapper.h` r.11 | RadioLibWrapper |
| `CustomSX1276Wrapper` | Radio | `src/helpers/radiolib/CustomSX1276Wrapper.h` r.10 | RadioLibWrapper |
| `RadioLibWrapper` | Radio | `src/helpers/radiolib/RadioLibWrappers.h` r.14 | Radio |
| `RadioNoiseListener` | Entropy | `src/helpers/radiolib/RadioLibWrappers.h` r.88 | RNG |
| `RAK12500LocationProvider` | Location | `src/helpers/sensors/EnvironmentSensorManager.cpp` r.177 | LocationProvider |
| `EnvironmentSensorManager` | Sensor management | `src/helpers/sensors/EnvironmentSensorManager.h` r.7 | SensorManager |
| `MicroNMEALocationProvider` | Location | `src/helpers/sensors/MicroNMEALocationProvider.h` r.40 | LocationProvider |
| `STM32Board` | Board | `src/helpers/stm32/STM32Board.h` r.6 | MainBoard |
| `E213Display` | Display | `src/helpers/ui/E213Display.h` r.12 | DisplayDriver |
| `E290Display` | Display | `src/helpers/ui/E290Display.h` r.12 | DisplayDriver |
| `GxEPDDisplay` | Display | `src/helpers/ui/GxEPDDisplay.h` r.19 | DisplayDriver |
| `LGFXDisplay` | Display | `src/helpers/ui/LGFXDisplay.h` r.12 | DisplayDriver |
| `NV3001BDisplay` | Display | `src/helpers/ui/NV3001BDisplay.h` r.27 | DisplayDriver |
| `NullDisplayDriver` | Display | `src/helpers/ui/NullDisplayDriver.h` r.5 | DisplayDriver |
| `SSD1306Display` | Display | `src/helpers/ui/SSD1306Display.h` r.18 | DisplayDriver |
| `ST7735Display` | Display | `src/helpers/ui/ST7735Display.h` r.9 | DisplayDriver |
| `ST7789Display` | Display | `src/helpers/ui/ST7789Display.h` r.9 | DisplayDriver |
| `ST7789LCDDisplay` | Display | `src/helpers/ui/ST7789LCDDisplay.h` r.10 | DisplayDriver |
| `U8g2Display` | Display | `src/helpers/ui/U8g2Display.h` r.19 | DisplayDriver |

> [!NOTE]
> The *Inherits from* column gives the base classes as they appear in the
> declaration, without the access level. One exception is worth mentioning:
> `NRF52BoardDCDC` inherits `virtual public NRF52Board`. That virtual
> inheritance is needed because thirty-two board classes in `variants/` hang
> under it and reach `NRF52Board` along two paths; without `virtual` each of
> those boards would get two copies of the base class.

`SerialBLEInterface` and `MyMesh` appear more than once. That is not an error
in the table: they are different classes with the same name, in different
files, and each build compiles exactly one of them. `SerialBLEInterface`
exists twice — one for ESP32, one for nRF52 — and `MyMesh` five times, one per
application that needs one.

The settings blocks appear twice for the same reason. `NodePrefs`,
`RadioPrefs`, `GPSPrefs` and `RepeatPrefs` sit in both
`src/helpers/CommonCLI.h` and `examples/companion_radio/NodePrefs.h`: the
companion application keeps its own set of blocks with different fields.
`BridgePrefs`, `PowerPrefs` and `RoomPrefs` exist only in the shared variant,
`CompanionPrefs` only in the companion variant. Twelve declarations under
eight names, then.

## Group 3 — standalone (62)

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
> `OLEDDisplay` appears twice in `src/helpers/ui/OLEDDisplay.h`, on lines 159
> and 161, behind an `#if` — one version inherits from `Print`, the other from
> `Stream`. `String` on line 50 in that same file is a forward reference from
> vendored code. Neither is MeshCore design but code adopted from ThingPulse;
> see [The source tree](source-layout.md).

> [!NOTE]
> `Context` sits on line 23 of `src/helpers/ConfigSerializer.h` and is not a
> standalone class in the ordinary sense: it is nested inside
> `ConfigSerializer` and unreachable outside it. It counts because the
> counting method takes every declaration with a body, regardless of nesting.

## The 89 from `variants/`

`variants/` counts 89 class declarations under 84 unique names — five names
occur in more than one variant directory. They are not written out one by one,
because nearly all of them do the same thing: implement a contract with the
pin assignment of one board.

| Contract being implemented | Classes |
|---|---|
| Board | 72 |
| Sensor management | 8 |
| Entropy | 2 |
| External watchdog | 2 |
| Display | 1 |
| Rotary input | 1 |

Three classes in `variants/` implement no contract at all and therefore sit in
group 3. All three are called `LoRaFEMControl` — in `heltec_tower_v2`,
`heltec_v4_r8` and `station_g3_esp32` — and drive the power amplifier on the
antenna side of the radio. Up to and including `03b6ef4` every class in
`variants/` filled a contract; that no longer holds.

The 72 board classes all implement the same contract in the same way. Four of
them are worth naming separately, because they are the only RP2040 board
classes: that family is the only one without a shared board class in
`src/helpers/`.

| RP2040 board class | Location |
|---|---|
| `RAK11310Board` | `variants/rak11310/RAK11310Board.h` r.15 |
| `PicoWBoard` | `variants/rpi_picow/PicoWBoard.h` r.11 |
| `WaveshareBoard` | `variants/waveshare_rp2040_lora/WaveshareBoard.h` r.27 |
| `XiaoRP2040Board` | `variants/xiao_rp2040/XiaoRP2040Board.h` r.25 |

All other board classes inherit from a shared parent — 32 from
`NRF52BoardDCDC`, 28 from `ESP32Board`, 3 from `NRF52Board`, 3 from
`STM32Board`, plus one from `HeltecV3Board` and one from `TBeamBoard`. These
four inherit from `mesh::MainBoard` directly and therefore write out
themselves what the other 68 get from their parent.

![Two inheritance trees side by side. On the left the board contract
mesh::MainBoard with ESP32Board, NRF52Board and STM32Board and their
descendants below it; on the right the four loose RP2040 board classes that
hang directly under the contract, without an intermediate
layer.](../../../images/en/class-model-2.svg)

## Recomputing

The class census in this chapter comes from `tools/design-overview.py`:

```bash
python3 tools/design-overview.py /path/to/MeshCore --classes
```

The script counts every line of the form `class Name { …` or
`class Name : base { …` with the brace on the same line. `struct` does not
count, and neither do forward declarations without a body.

The split into the three groups comes from `tools/class-groups.py`, which uses
the same parser:

```bash
python3 tools/class-groups.py /path/to/MeshCore
python3 tools/class-groups.py /path/to/MeshCore --groep 2 --taal en --markdown
```

Group 1 is a named list in that script, because whether a class is a contract
cannot be read off mechanically: `DisplayDriver` has `width()` and `height()`
with a body and is one all the same, `ESP32Board` has virtual methods and is
not one. Groups 2 and 3 do follow mechanically — everything that inherits,
directly or through intermediate classes, from a class in group 1 sits in
group 2.

The line numbers in the tables can be checked with `tools/cite-check.py`:

```bash
python3 tools/cite-check.py /path/to/MeshCore docs/en/design/technical/class-model.md
```

## Sources

- [MeshCore `d929643` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/Dispatcher.h)
- [MeshCore `d929643` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/MeshCore.h)
- [MeshCore `d929643` — `src/helpers/`](https://github.com/meshcore-dev/MeshCore/tree/d929643/src/helpers)
- [MeshCore `d929643` — `src/helpers/ConfigSerializer.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ConfigSerializer.h)
- [MeshCore `d929643` — `src/helpers/NRF52Board.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/NRF52Board.h)
- [MeshCore `d929643` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/d929643/variants)
