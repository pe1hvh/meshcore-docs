# Buttons and LEDs

*MOMENTARYBUTTON · FIVE EVENTS · RTTTL · TX LAMP*

The simplest parts of a node are also the only ones you operate it with
without a phone. One button, a lamp and sometimes a buzzer. This chapter
describes how the firmware gets five different events out of one button,
which lamps exist, and which tune plays at startup.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `src/helpers/ui/MomentaryButton.h`, `src/helpers/ui/MomentaryButton.cpp`,
> `src/helpers/ui/buzzer.h`, `src/helpers/ESP32Board.h` and the pin flags in
> `variants/`.

## Five events out of one button

Most MeshCore boards have exactly one operable button. Forty-two variant
files set a `-D PIN_USER_BTN=` line, forty-four lines in total — `rak4631`
sets the flag three times, in three different `[env:…]` sections. Reproducible
with `tools/hardware-overview.py`. Out of that single button the firmware gets
five different events:

`src/helpers/ui/MomentaryButton.h` r.5-9

```cpp
#define BUTTON_EVENT_NONE        0
#define BUTTON_EVENT_CLICK       1
#define BUTTON_EVENT_LONG_PRESS  2
#define BUTTON_EVENT_DOUBLE_CLICK 3
#define BUTTON_EVENT_TRIPLE_CLICK 4
```

![How one button yields five events: a short press, twice and three times
within 280 milliseconds, and a press longer than the configured
threshold](../../../images/en/buttons-and-leds-1.svg)

The distinction rests on two timings. The long press has a threshold passed
in per board; on the Heltec V3 that is 1000 milliseconds
(`variants/heltec_v3/target.cpp` r.28). The window for double and triple
clicks is fixed in the code:

`src/helpers/ui/MomentaryButton.cpp` r.3

```cpp
#define MULTI_CLICK_WINDOW_MS  280
```

If another click follows within 280 milliseconds it becomes a double or a
triple. That also means an ordinary click can only be reported *after* that
window — the firmware has to wait and see whether another one follows.
Anyone not needing multiple clicks can set that window to zero with the
constructor parameter `multiclick`, and then the button reports
immediately.

## The button knows four wirings

Not every board pulls its button the same way. The constructor catches that
with two flags, and there is a second constructor for buttons hanging off
an analogue input instead of a digital one.

`src/helpers/ui/MomentaryButton.cpp` r.35-39

```cpp
void MomentaryButton::begin() {
  if (_pin >= 0 && _threshold == 0) {
    pinMode(_pin, _pull ? (_reverse ? INPUT_PULLUP : INPUT_PULLDOWN) : INPUT);
  }
}
```

| Parameter | Meaning |
|---|---|
| `reverse` | pressed is low instead of high |
| `pulldownup` | enable the internal resistor; direction follows from `reverse` |
| `analog_threshold` | button on an analogue input; above this value it counts as pressed |

For the analogue variant `pinMode()` is skipped — hence the condition
`_threshold == 0`. A pin of `-1` means no button, and then `begin()` does
nothing either.

## Lamps

There are three kinds of lamp in the firmware and all three do something
different. Counted over uncommented `-D` lines in `variants/`:

| Flag | Lines | Files | What it does |
|---|---|---|---|
| `P_LORA_TX_LED` | 45 | 44 | lit while transmitting |
| `PIN_STATUS_LED` | 6 | 6 | status indication |
| `PIN_LED` | 1 | 1 | general lamp |

Repeat with `grep -rh -- "-D P_LORA_TX_LED=" variants/ | grep -v "^\s*;" | wc -l`
and the same pattern for the other two.

The transmit lamp is the only one the board class initialises itself:

`src/helpers/ESP32Board.h` r.39-42

```cpp
  #ifdef P_LORA_TX_LED
    pinMode(P_LORA_TX_LED, OUTPUT);
    digitalWrite(P_LORA_TX_LED, LOW);
  #endif
```

That the lamp lights while transmitting is not decoration: it is the only
way to see on a node without a screen that it really is transmitting.

On three boards an addressable RGB LED sits there instead
(`heltec_mesh_solar`, `nibble_screen_connect` and `lilygo_techo_card`, via
the Adafruit NeoPixel library). That falls outside the flags above; what
the library does is in [Peripherals](../../libraries/other/peripherals.md).

## The buzzer plays ringtones from 1999

Fourteen variant files set a `-D PIN_BUZZER=` line. What sounds is not a
sequence of tones in the code but an RTTTL string — the format Nokia phones
once stored their ringtones in:

`src/helpers/ui/buzzer.h` r.33-34

```cpp
        const char *startup_song = "Startup:d=4,o=5,b=160:16c6,16e6,8g6";
        const char *shutdown_song = "Shutdown:d=4,o=5,b=100:8g5,16e5,16c5";
```

The startup tune is a rising c-e-g in the sixth octave at tempo 160; the
shutdown tune is the same triad reversed and slower. The class around it is
thin, and says so itself:

`src/helpers/ui/buzzer.h` r.6-17

```cpp
/* class abstracts underlying RTTTL library 

    Just a simple implementation to start.  At the moment use same
    melody for message and discovery
    Suggest enum type for different sounds
    - on message
    - on discovery

    TODO
    - make message ring tone configurable

*/
```

Message and discovery therefore get the same sound, and it is not
configurable. That is written there as an open point, literally.

Playing is non-blocking: `loop()` pushes the melody along bit by bit, so
the node can keep handling packets meanwhile. There is one off switch,
`quiet()`.

## Vibration

For boards with a vibration motor there is `GenericVibration`
(`src/helpers/ui/GenericVibration.h`). No variant file currently sets a
`-D PIN_VIBRATION=` line in its build flags; the support is there, the use
is not yet.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`src/helpers/ui/MomentaryButton.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/MomentaryButton.h)
  — the five events and the constructors
- [`src/helpers/ui/MomentaryButton.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/MomentaryButton.cpp)
  — the click window and the pin configuration
- [`src/helpers/ui/buzzer.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ui/buzzer.h)
  — the melodies and the open point
- [`src/helpers/ESP32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/src/helpers/ESP32Board.h)
  — the transmit lamp

Related in this documentation:

- [The Display](display.md) — the other side of the user interface
- [Peripherals](../../libraries/other/peripherals.md) — the libraries
  behind buzzer, NeoPixel and bus expander
- [Node Matrix](../../platform/node-matrix.md) — which board has buttons

Translated from Dutch by Anthropic Claude
