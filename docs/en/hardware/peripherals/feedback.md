# Feedback

*MOMENTARYBUTTON · FIVE EVENTS · RTTTL · VIBRATION · TX LAMP*

The simplest parts of a node are also the only ones you operate and read it
with without a phone. One button, a lamp, sometimes a buzzer and sometimes a
vibration motor. This chapter describes how the firmware gets five different
events out of one button, which lamps exist, which tune plays at startup, and
along which two routes a node can vibrate.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.17.1, commit `d929643`, 14 August 2026 — files
> `src/helpers/ui/MomentaryButton.h`, `src/helpers/ui/MomentaryButton.cpp`,
> `src/helpers/ui/buzzer.h`, `src/helpers/ui/GenericVibration.h`,
> `src/helpers/ui/DRV2605Vibration.h`, `src/helpers/ESP32Board.h`, the three
> `UITask` variants under `examples/companion_radio/` and the pin flags in
> `variants/`.

> [!NOTE]
> The diagram belonging to this chapter is called `buttons-and-leds-1.svg` and
> not `feedback-1.svg`. That is not a mistake. `IMAGES.md` states that image
> files are never moved or renamed, not even when the chapter's slug changes;
> the file name and the slug therefore diverge.

## Five events out of one button

Most MeshCore boards have exactly one operable button. Forty-seven variant
files set a `-D PIN_USER_BTN=` line, fifty lines in total — `rak4631`
sets the flag four times, in four different `[env:…]` sections. Reproducible
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
| `P_LORA_TX_LED` | 49 | 45 | lit while transmitting |
| `PIN_STATUS_LED` | 9 | 9 | status indication |
| `PIN_LED` | 1 | 1 | general lamp |

Repeat with `grep -rh -- "-D P_LORA_TX_LED=" variants/ | grep -v "^\s*;" | wc -l`
and the same pattern for the other two.

The transmit lamp is the only one the board class initialises itself:

`src/helpers/ESP32Board.h` r.40-43

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

Eighteen variant files set a `-D PIN_BUZZER=` line, twenty-six lines in
total. What sounds is not a
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

A notification does not have to be audible. Beside the buzzer the firmware
knows a vibration motor: the same kind of notification, along a different
sense. That is why this section sits here, right next to the RTTTL tunes.

There are two implementations, with the same purpose and a very different
mechanism:

| Class | Location | Mechanism | Belongs to |
|---|---|---|---|
| `GenericVibration` | `src/helpers/ui/GenericVibration.h` r.21 | switches a pin on and off again | `ui-new`, `ui-tiny` |
| `DRV2605Vibration` | `src/helpers/ui/DRV2605Vibration.h` r.22 | a driver chip on I²C plays an effect from its own library | `ui-orig` |

Both wait `VIBRATION_TIMEOUT` — 5000 milliseconds — between two vibrations
(`src/helpers/ui/GenericVibration.h` r.18). The first only switches the pin
`PIN_VIBRATION`; the second sends effect number 16 to the chip, "1000 ms
alert" from the DRV2605 effect library — see `DRV2605_EFFECT` in
`src/helpers/ui/DRV2605Vibration.h` r.19.

`DRV2605Vibration` can do two things `GenericVibration` cannot. Suppress the
vibration temporarily with `quiet(bool)`, and read that state back with
`isQuiet()` (`src/helpers/ui/DRV2605Vibration.h` r.29 and r.30). And force a
vibration past the cooldown, through the `force` parameter on `trigger()`
(r.25). The first is no ornament: `ui-orig` uses it to cycle through the alert
modes on a triple press — buzz and vibrate, buzz only, vibrate only, silent.

### Which of the two is in there depends on the UI variant

This is the core finding of this section. It is not the board that chooses
between the two classes but the chosen UI variant. Each variant knows exactly
one of them:

| UI variant | Class | Location |
|---|---|---|
| `ui-orig` | `DRV2605Vibration` | `examples/companion_radio/ui-orig/UITask.h` r.18 |
| `ui-new` | `GenericVibration` | `examples/companion_radio/ui-new/UITask.h` r.19 |
| `ui-tiny` | `GenericVibration` | `examples/companion_radio/ui-tiny/UITask.h` r.22 |

The board decides something else: whether there is a vibration motor at all.
Both classes sit entirely inside an `#ifdef` — `GenericVibration` in
`PIN_VIBRATION`, `DRV2605Vibration` in `HAS_DRV2605`. Without that flag the
class stays empty and none of it is compiled in.

> [!NOTE]
> **On the pinned commit one board has working vibration.**
> `meshtracker_x1` switches `HAS_DRV2605` on
> (`variants/meshtracker_x1/platformio.ini` r.86) and takes `ui-orig`. On
> `gat562_mesh_watch13` the file `GenericVibration.cpp` is in the
> `build_src_filter`, but the flag `PIN_VIBRATION` is commented out
> (`variants/gat562_mesh_watch13/platformio.ini` r.77). Commented out does not
> count: that board does not vibrate. Reproducible with
> `tools/hardware-overview.py`, section 9b.

### When it vibrates differs per variant

The two variants do not vibrate at the same moment, and that is not a detail.

`ui-orig` vibrates only on a new message, in `UITask::newMsg`
(`examples/companion_radio/ui-orig/UITask.cpp` r.142) — even while the app is
connected.

`ui-new` and `ui-tiny` vibrate in `UITask::notify`
(`examples/companion_radio/ui-new/UITask.cpp` r.622 and
`examples/companion_radio/ui-tiny/UITask.cpp` r.476), on every `UIEventType`
except `none`. That is five of them: `contactMessage`, `channelMessage`,
`roomMessage`, `newContactMessage` and `ack`. Where `ui-orig` vibrates once,
the other two also vibrate on a delivery acknowledgement.

## Sources

Firmware, commit `d929643` (v1.17.1, 14 August 2026):

- [`src/helpers/ui/MomentaryButton.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/MomentaryButton.h)
  — the five events and the constructors
- [`src/helpers/ui/MomentaryButton.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/MomentaryButton.cpp)
  — the click window and the pin configuration
- [`src/helpers/ui/buzzer.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/buzzer.h)
  — the melodies and the open point
- [`src/helpers/ui/GenericVibration.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/GenericVibration.h)
  — the pin-driven vibration and the cooldown
- [`src/helpers/ui/DRV2605Vibration.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ui/DRV2605Vibration.h)
  — the I²C driver chip, the effect number and `quiet()`
- [`src/helpers/ESP32Board.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/ESP32Board.h)
  — the transmit lamp

Related in this documentation:

- [The Display](display.md) — the other side of the user interface
- [Peripherals](../../libraries/other/peripherals.md) — the libraries
  behind buzzer, NeoPixel and bus expander
- [Node Matrix](../../platform/node-matrix.md) — which board has buttons

Translated from Dutch by Anthropic Claude
