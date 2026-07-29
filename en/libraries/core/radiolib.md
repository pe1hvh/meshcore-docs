# RadioLib

*TRANSCEIVER · GODMODE · EXCLUDE · WRAPPER*

RadioLib is the layer between MeshCore and the radio chip. Six different
transceivers are driven through it, each with its own wrapper in
`src/helpers/radiolib/`. MeshCore does not use the library as intended: with
`RADIOLIB_GODMODE` the internal registers are opened up, and fourteen
protocols are stripped out at compile time.

> [!NOTE]
> **Source.** This page was verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files `platformio.ini`
> and the sixteen files in `src/helpers/radiolib/`.

## What it does

RadioLib by Jan Gromeš is an Arduino library for wireless modules. It supports
dozens of chips and a range of protocols — LoRa, FSK, but also AX.25, APRS,
morse, RTTY and SSTV — behind a single interface. For every supported
transceiver there is a class that handles the SPI commands, the register model
and the timing of that specific chip. The documentation lives at
[github.com/jgromes/RadioLib](https://github.com/jgromes/RadioLib) and the API
is extensively documented in that repository's wiki.

## How MeshCore pulls it in

`platformio.ini` r.22

```text
  jgromes/RadioLib @ ^7.6.0
```

The line sits in `[arduino_base]`, so RadioLib is in all 507 build targets.
The version range is open upwards within the 7.x series.

Two build flags steer how the library behaves:

`platformio.ini` r.27

```text
build_flags = -w -DNDEBUG -DRADIOLIB_STATIC_ONLY=1 -DRADIOLIB_GODMODE=1
```

`RADIOLIB_STATIC_ONLY` forbids dynamic allocation inside the library.
`RADIOLIB_GODMODE` makes all `private` and `protected` members public. That
last one is not a debug option left behind: MeshCore needs it, as shown below.

After that, fourteen protocols are switched off:

`platformio.ini` r.34-47

```text
  -D RADIOLIB_EXCLUDE_CC1101=1
  -D RADIOLIB_EXCLUDE_RF69=1
  -D RADIOLIB_EXCLUDE_SX1231=1
  -D RADIOLIB_EXCLUDE_SI443X=1
  -D RADIOLIB_EXCLUDE_RFM2X=1
  -D RADIOLIB_EXCLUDE_SX128X=1
  -D RADIOLIB_EXCLUDE_AFSK=1
  -D RADIOLIB_EXCLUDE_AX25=1
  -D RADIOLIB_EXCLUDE_HELLSCHREIBER=1
  -D RADIOLIB_EXCLUDE_MORSE=1
  -D RADIOLIB_EXCLUDE_APRS=1
  -D RADIOLIB_EXCLUDE_BELL=1
  -D RADIOLIB_EXCLUDE_RTTY=1
  -D RADIOLIB_EXCLUDE_SSTV=1
```

Six of those exclude chip families MeshCore does not use, eight exclude
protocols the library offers on top of the radio.

## How MeshCore uses it

`src/helpers/radiolib/` holds sixteen files. Six of them are pairs of a
`Custom*` class and a `Custom*Wrapper`: LLCC68, LR1110, STM32WLx, SX1262,
SX1268 and SX1276. The `Custom*` class inherits from the RadioLib class and
adds what MeshCore misses; the wrapper translates that to the mesh layer's
generic radio interface.

`src/helpers/radiolib/CustomSTM32WLx.h` r.8-16

```cpp
class CustomSTM32WLx : public STM32WLx {
  public:
    CustomSTM32WLx(STM32WLx_Module *mod) : STM32WLx(mod) { }

    bool isReceiving() {
      uint16_t irq = getIrqFlags();
      bool detected = (irq & SX126X_IRQ_HEADER_VALID) || (irq & SX126X_IRQ_PREAMBLE_DETECTED);
      return detected;
    }
};
```

What GODMODE is needed for is shown by `SX126xReset.h`. To recalibrate an
SX126x chip, MeshCore talks straight to RadioLib's module layer — `mod` and
`hal` are not public in the library itself:

`src/helpers/radiolib/SX126xReset.h` r.13-18

```cpp
  radio->mod->SPIwriteStream(RADIOLIB_SX126X_CMD_CALIBRATE, &calData, 1, true, false);
  radio->mod->hal->delay(5);
  uint32_t start = millis();
  while (radio->mod->hal->digitalRead(radio->mod->getGpio())) {
    if (millis() - start > 50) break;
    radio->mod->hal->yield();
  }
```

The text `RadioLib` occurs in 94 of the repo's 590 source files — by far the
most of any library. The bulk of those are `variants/` files that pick a
`RADIO_CLASS`.

![From the MeshCore wrapper classes through RadioLib to the transceiver: six
Custom wrapper pairs drive LLCC68, LR1110, SX1262, SX1268 and SX1276 over the
SPI bus, while the STM32WLx forms a separate branch sitting on the same chip
as the processor](../../../images/en/radiolib-1.svg)

## What it means for a node

The choice of radio chip is a compile-time choice, not a setting. A variant
sets `RADIO_CLASS` to the right `Custom*` class, and that fixes which
transceiver the firmware can drive. Flash a board with the wrong variant and
you get firmware that cannot find the radio.

The excluded protocols are simply not there: a MeshCore node cannot transmit
APRS or morse, even though the library could in principle.

## Sources

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/platformio.ini)
- [`src/helpers/radiolib/`](https://github.com/meshcore-dev/MeshCore/tree/03b6ef4/src/helpers/radiolib)
- [`src/helpers/radiolib/SX126xReset.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/SX126xReset.h)
- [`src/helpers/radiolib/CustomSTM32WLx.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/radiolib/CustomSTM32WLx.h)
- [jgromes/RadioLib](https://github.com/jgromes/RadioLib)

Translated from Dutch by Anthropic Claude
