# The class model

*CONTRACT · FILLER · STANDALONE · BORDERLINE CASES*

MeshCore's 196 classes fall into three kinds: classes that lay down what
another part may expect, classes that fill such an agreement, and classes that
stand on their own. This chapter describes that three-way split, states what a
contract is and is not, and walks through the 119 classes of the shared tree
one by one. The 77 from `variants/` appear as a summary at the end.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — every class in the tables was
> checked for file and line number in `src/`, `examples/` and `variants/`.

## What a contract is

A contract is a class that exists solely to lay down what another part may
expect. It holds no working code, only the list of what a filler must be able
to do, plus sometimes a default answer for when the hardware cannot do
something. In C++ you recognise it by its virtual methods, the mandatory ones
ending in `= 0`.

Three properties make something a contract:

1. **It describes, it does not do.** `Radio` does not know how to drive an
   SX1262; it lays down that there must be something that sends bytes.
2. **The user knows only the contract.** Packet handling holds a `Radio*` and
   has no idea which chip hangs off it.
3. **Fillers are interchangeable.** Every class that fills the contract can
   replace any other without the user changing.

The logical side of this story — which agreements exist and what they promise
— is in [Contracts](../logical/interfaces.md). Here it is about the classes
that carry them.

![Three columns. On the left fourteen contract-defining classes without code
of their own, in the middle fifty classes that fill one with arrows pointing
left, on the right fifty-five standalone classes without arrows. Along the
bottom a wide bar with the seventy-seven classes from variants runs into the
middle column.](../../../images/en/class-model-1.svg)

## What is not a contract

A base class that holds shared code is not a contract but a common parent.
`ESP32Board` is such a case: it fills the board contract *and* offers code the
derived board classes inherit. It therefore sits in group 2, not group 1.

The distinction is not always sharp. `BridgeBase` and `RadioLibWrapper` are
both a filler *and* a parent: they fill `AbstractBridge` and `mesh::Radio`
respectively, and there are classes hanging under them in turn. Anyone reading
the three-way split as a hard partition runs into trouble with those two. They
sit in group 2 because they fill a contract; that they also have children of
their own changes nothing about that property.

**Standalone** is everything that is not a contract and fills none either:
classes that do one thing and on which nothing depends. `ClientACL` manages
the access list, `RegionMap` converts region codes, `Packet` is a data object.
They are not replaceable because there is nothing they would have to replace.

An instructive case is `CustomSX1262`. It sits in group 3, not group 2. The
class inherits from RadioLib's `SX1262` and fills no MeshCore contract; it is
`CustomSX1262Wrapper` that does, via `RadioLibWrapper`. That explains why
there are two classes per radio chip: one that adapts the chip driver, one
that pours the result into the MeshCore contract. See
[Radio realisation](radio-realisation.md).

## The distribution

The shared tree counts 119 classes: **14** contract-defining, **50**
contract-filling, **55** standalone.

| Group | Count | Characteristic |
|---|---|---|
| 1 — contract-defining | 14 | Virtual methods only, no working code |
| 2 — contract-filling | 50 | Inherits from a class in group 1 |
| 3 — standalone | 55 | No contract, fills none either |

## Group 1 — contract-defining (14)

| Class | Location |
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

Two things stand out in this list.

`SensorManager` and `LocationProvider` are not in `src/` but in
`src/helpers/`. That is not a mistake: they are contracts that only became
necessary once sensors arrived, and they have not been moved to the core.

`CommonCLICallbacks` and `DataStoreHost` reverse the dependency. They are
defined by the layer below but filled by the application above — `MyMesh` in
`examples/simple_repeater/` fills `CommonCLICallbacks` so that the control
code in `src/helpers/CommonCLI.cpp` can call something without knowing which
application is running. The lower layer calls the higher one without knowing
it.

## Group 2 — contract-filling (50)

| Class | Contract | Location | Inherits from |
|---|---|---|---|
| `ESP32Board` | Board | `src/helpers/ESP32Board.h` r.18 | mesh::MainBoard |
| `MeshadventurerBoard` | Board | `src/helpers/MeshadventurerBoard.h` r.20 | ESP32Board |
| `NRF52Board` | Board | `src/helpers/NRF52Board.h` r.27 | mesh::MainBoard |
| `NRF52BoardDCDC` | Board | `src/helpers/NRF52Board.h` r.74 | NRF52Board |
| `STM32Board` | Board | `src/helpers/stm32/STM32Board.h` r.6 | mesh::MainBoard |
| `TBeamBoard` | Board | `src/helpers/esp32/TBeamBoard.h` r.91 | ESP32Board |
| `BridgeBase` | Bridge | `src/helpers/bridges/BridgeBase.h` r.21 | AbstractBridge |
| `ESPNowBridge` | Bridge | `src/helpers/bridges/ESPNowBridge.h` r.42 | BridgeBase |
| `RS232Bridge` | Bridge | `src/helpers/bridges/RS232Bridge.h` r.47 | BridgeBase |
| `SimpleMeshTables` | Seen table | `src/helpers/SimpleMeshTables.h` r.11 | mesh::MeshTables |
| `LocalIdentity` | Identity | `src/Identity.h` r.54 | Identity |
| `AutoDiscoverRTCClock` | Clock | `src/helpers/AutoDiscoverRTCClock.h` r.7 | mesh::RTCClock |
| `ESP32RTCClock` | Clock | `src/helpers/ESP32Board.h` r.160 | mesh::RTCClock |
| `VolatileRTCClock` | Clock | `src/helpers/ArduinoHelpers.h` r.6 | mesh::RTCClock |
| `ArduinoSerialInterface` | Interface | `src/helpers/ArduinoSerialInterface.h` r.6 | BaseSerialInterface |
| `SerialBLEInterface` | Interface | `src/helpers/esp32/SerialBLEInterface.h` r.9 | BaseSerialInterface, BLESecurityCallbacks, BLEServerCallbacks, BLECharacteristicCallbacks |
| `SerialBLEInterface` | Interface | `src/helpers/nrf52/SerialBLEInterface.h` r.10 | BaseSerialInterface |
| `SerialWifiInterface` | Interface | `src/helpers/esp32/SerialWifiInterface.h` r.6 | BaseSerialInterface |
| `MicroNMEALocationProvider` | Location | `src/helpers/sensors/MicroNMEALocationProvider.h` r.36 | LocationProvider |
| `RAK12500LocationProvider` | Location | `src/helpers/sensors/EnvironmentSensorManager.cpp` r.177 | LocationProvider |
| `BaseChatMesh` | Mesh | `src/helpers/BaseChatMesh.h` r.59 | mesh::Mesh |
| `MyMesh` | Mesh | `examples/simple_secure_chat/main.cpp` r.73 | BaseChatMesh, ContactVisitor |
| `MyMesh` | Mesh | `examples/simple_repeater/MyMesh.h` r.83 | mesh::Mesh, CommonCLICallbacks |
| `MyMesh` | Mesh | `examples/simple_room_server/MyMesh.h` r.91 | mesh::Mesh, CommonCLICallbacks |
| `MyMesh` | Mesh | `examples/simple_sensor/main.cpp` r.8 | SensorMesh |
| `MyMesh` | Mesh | `examples/companion_radio/MyMesh.h` r.87 | BaseChatMesh, DataStoreHost |
| `SensorMesh` | Mesh | `examples/simple_sensor/SensorMesh.h` r.49 | mesh::Mesh, CommonCLICallbacks |
| `ArduinoMillis` | Millisecond clock | `src/helpers/ArduinoHelpers.h` r.22 | mesh::MillisecondClock |
| `StaticPoolPacketManager` | Packet pool | `src/helpers/StaticPoolPacketManager.h` r.21 | mesh::PacketManager |
| `CustomLLCC68Wrapper` | Radio | `src/helpers/radiolib/CustomLLCC68Wrapper.h` r.7 | RadioLibWrapper |
| `CustomLR1110Wrapper` | Radio | `src/helpers/radiolib/CustomLR1110Wrapper.h` r.7 | RadioLibWrapper |
| `CustomSTM32WLxWrapper` | Radio | `src/helpers/radiolib/CustomSTM32WLxWrapper.h` r.8 | RadioLibWrapper |
| `CustomSX1262Wrapper` | Radio | `src/helpers/radiolib/CustomSX1262Wrapper.h` r.11 | RadioLibWrapper |
| `CustomSX1268Wrapper` | Radio | `src/helpers/radiolib/CustomSX1268Wrapper.h` r.11 | RadioLibWrapper |
| `CustomSX1276Wrapper` | Radio | `src/helpers/radiolib/CustomSX1276Wrapper.h` r.10 | RadioLibWrapper |
| `ESPNOWRadio` | Radio | `src/helpers/esp32/ESPNOWRadio.h` r.5 | mesh::Radio |
| `RadioLibWrapper` | Radio | `src/helpers/radiolib/RadioLibWrappers.h` r.6 | mesh::Radio |
| `E213Display` | Display | `src/helpers/ui/E213Display.h` r.12 | DisplayDriver |
| `E290Display` | Display | `src/helpers/ui/E290Display.h` r.12 | DisplayDriver |
| `GxEPDDisplay` | Display | `src/helpers/ui/GxEPDDisplay.h` r.19 | DisplayDriver |
| `LGFXDisplay` | Display | `src/helpers/ui/LGFXDisplay.h` r.12 | DisplayDriver |
| `NullDisplayDriver` | Display | `src/helpers/ui/NullDisplayDriver.h` r.5 | DisplayDriver |
| `SSD1306Display` | Display | `src/helpers/ui/SSD1306Display.h` r.18 | DisplayDriver |
| `ST7735Display` | Display | `src/helpers/ui/ST7735Display.h` r.10 | DisplayDriver |
| `ST7789Display` | Display | `src/helpers/ui/ST7789Display.h` r.9 | DisplayDriver |
| `ST7789LCDDisplay` | Display | `src/helpers/ui/ST7789LCDDisplay.h` r.10 | DisplayDriver |
| `U8g2Display` | Display | `src/helpers/ui/U8g2Display.h` r.19 | DisplayDriver |
| `EnvironmentSensorManager` | Sensor management | `src/helpers/sensors/EnvironmentSensorManager.h` r.7 | SensorManager |
| `RadioNoiseListener` | Entropy | `src/helpers/radiolib/RadioLibWrappers.h` r.74 | mesh::RNG |
| `StdRNG` | Entropy | `src/helpers/ArduinoHelpers.h` r.27 | mesh::RNG |

> [!NOTE]
> The *Inherits from* column gives the base classes as they appear in the
> declaration, without the access level. One exception is worth mentioning:
> `NRF52BoardDCDC` inherits `virtual public NRF52Board`. That virtual
> inheritance is needed because thirty board classes in `variants/` hang under
> it and reach `NRF52Board` along two paths; without `virtual` each of those
> boards would get two copies of the base class.

`SerialBLEInterface` and `MyMesh` appear more than once. That is not an error
in the table: they are different classes with the same name, in different
files, and each build compiles exactly one of them. `SerialBLEInterface`
exists twice — one for ESP32, one for nRF52 — and `MyMesh` five times, one per
application that needs one.

## Group 3 — standalone (55)

| Class | Location |
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
> `OLEDDisplay` appears twice in `src/helpers/ui/OLEDDisplay.h`, on lines 159
> and 161, behind an `#if` — one version inherits from `Print`, the other from
> `Stream`. `String` on line 50 in that same file is a forward reference from
> vendored code. Neither is MeshCore design but code adopted from ThingPulse;
> see [The source tree](source-layout.md).

## The 77 from `variants/`

`variants/` counts 77 class declarations under 73 unique names — four names
occur in more than one variant directory. They are not written out one by one,
because they all do the same thing: fill a contract with the pin assignment of
one board.

| Contract being filled | Classes |
|---|---|
| Board | 65 |
| Sensor management | 7 |
| Display | 3 |
| Entropy | 2 |

The 65 board classes all fill the same contract in the same way. Four of them
are worth naming separately, because they are the only RP2040 board classes:
that family is the only one without a shared board class in `src/helpers/`.

| RP2040 board class | Location |
|---|---|
| `RAK11310Board` | `variants/rak11310/RAK11310Board.h` r.15 |
| `PicoWBoard` | `variants/rpi_picow/PicoWBoard.h` r.11 |
| `WaveshareBoard` | `variants/waveshare_rp2040_lora/WaveshareBoard.h` r.27 |
| `XiaoRP2040Board` | `variants/xiao_rp2040/XiaoRP2040Board.h` r.25 |

All other board classes inherit from a shared parent — 30 from
`NRF52BoardDCDC`, 23 from `ESP32Board`, 3 from `NRF52Board`, 3 from
`STM32Board`, plus a few from `HeltecV3Board` and `TBeamBoard`. These four
inherit from `mesh::MainBoard` directly and therefore write out for themselves
what the other 61 get from their parent.

![Two inheritance trees side by side. On the left the board contract
mesh::MainBoard with ESP32Board, NRF52Board and STM32Board and their
descendants underneath; on the right the four separate RP2040 board classes
hanging directly off the contract, with no intermediate
layer.](../../../images/en/class-model-2.svg)

## Recomputing

The counts in this chapter come from `tools/design-overview.py`:

```bash
python3 tools/design-overview.py /path/to/MeshCore --classes
```

The script counts every line of the form `class Name { …` or
`class Name : base { …` with the brace on the same line. `struct` does not
count, and neither do forward declarations without a body.

## Sources

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/helpers/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src/helpers)
- [MeshCore `03b6ef4` — `src/helpers/NRF52Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/NRF52Board.h)
- [MeshCore `03b6ef4` — `variants/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/variants)

Translated from Dutch by Anthropic Claude
