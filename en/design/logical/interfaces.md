# Contracts

*ABSTRACT AGREEMENTS · DUTY AND OPTION · WHAT A CONTRACT ENFORCES*

Between the components from the previous chapter lie fixed agreements. A
component that satisfies such an agreement can replace any other
implementation without the rest of the firmware changing. This chapter
describes the eight contracts that carry the design, and what each contract
requires and what it leaves free.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — `src/MeshCore.h`,
> `src/Dispatcher.h`, `src/Mesh.h`, `src/helpers/ui/DisplayDriver.h` and
> `src/helpers/AbstractBridge.h`.

## Duty and option

Every contract consists of two kinds of agreement. Some must be implemented —
skip them and you get no working node. Others have a sensible default answer
and only need implementing when the hardware can manage it.

That split is the hinge of the design. Adding a new board means implementing
the mandatory agreements and leaving the rest alone. A board without a
temperature sensor simply reports that there is no temperature, and nobody has
to account for it.

`src/MeshCore.h` l.45-50

```cpp
class MainBoard {
public:
  virtual uint16_t getBattMilliVolts() = 0;
  virtual float getMCUTemperature() { return NAN; }
  virtual bool setAdcMultiplier(float multiplier) { return false; };
  virtual float getAdcMultiplier() const { return 0.0f; }
```

The first method is mandatory — every board must be able to report its battery
voltage. The three remaining methods return a default value for boards without
that capability: `NAN`, `false` and `0.0f`.

![Eight contracts as horizontal bars. Above each bar stands who uses it, below
it how many implementations exist. Radio and display have six and eleven
respectively; clock and entropy three and two.](../../../images/en/interfaces-1.svg)

## The eight contracts

| Contract | Mandatory | Implementations | Used by |
|---|---|---|---|
| Radio | Receive, send, estimate airtime, report send status | 6 + 1 | Packet handling |
| Board | Battery voltage, manufacturer name, restart, startup reason | 7 | Application, packet handling |
| Clock | Read and set time | 3 | Mesh logic, application |
| Entropy | Supply random bytes | 2 | Mesh logic |
| Seen table | Ask whether a packet is known, and clear | 1 | Mesh logic |
| Packet pool | Hand out, take back, queue, fetch | 1 | Packet handling |
| Display | On, off, clear, draw, flush | 11 | Application |
| Bridge | Offer and fetch a packet | 2 | Mesh logic |

The *Implementations* column counts the classes that implement the contract in
this commit. That there is only one seen table and one packet pool does not
make the contract redundant: it keeps the mesh logic independent of how that
table is built.

Two figures need explanation. Radio says 6 + 1: six implementations go through
the radio library, and one — ESP-NOW — bypasses it entirely and uses WiFi
hardware as the transport medium. Of those six, five are used; the sixth is
present but selected by no build target.

Board says 7, not 4. Three implementations are shared per platform family and
live in `src/helpers/`. The fourth family, RP2040, has no shared
implementation: each of the four RP2040 variants writes its own board class in
its own variant directory. That is an asymmetry in the design, not a mistake in
the count.

## The radio contract

The sharpest contract in the design, and the only one that genuinely makes the
firmware portable across four different radio chips.

`src/Dispatcher.h` l.22-32

```cpp
class Radio {
public:
  virtual void begin() { }

  /**
   * \brief  polls for incoming raw packet.
   * \param  bytes  destination to store incoming raw packet.
   * \param  sz   maximum packet size allowed.
   * \returns 0 if no incoming data, otherwise length of complete packet received.
  */
  virtual int recvRaw(uint8_t* bytes, int sz) = 0;
```

Note what is not in it. No frequency, no bandwidth, no spreading factor. The
contract is exclusively about bytes in and bytes out, plus what the layer above
needs in order to schedule: how long does sending this many bytes take, and is
the previous transmission finished.

The radio parameters are not in this contract because they are not the
responsibility of the layer above. Changing the spreading factor changes the
radio setting, not the mesh behaviour.

## The smallest contract

The seen table consists of two agreements:

`src/Mesh.h` l.16-20

```cpp
class MeshTables {
public:
  virtual bool hasSeen(const Packet* packet) = 0;
  virtual void clear(const Packet* packet) = 0;   // remove this packet hash from table
};
```

No more is needed. The mesh logic need not know how large the table is, how
long a packet is remembered or what happens when it fills up. Those are all
choices of the implementation.

## The widest contract

The display contract is the only one that brings its own vocabulary —
dimensions and colours — because an application that draws does after all need
to know how much room there is.

`src/helpers/ui/DisplayDriver.h` l.6-20

```cpp
class DisplayDriver {
  int _w, _h;
protected:
  DisplayDriver(int w, int h) { _w = w; _h = h; }
public:
  enum Color { DARK=0, LIGHT, RED, GREEN, BLUE, YELLOW, ORANGE }; // on b/w screen, colors will be !=0 synonym of light

  int width() const { return _w; }
  int height() const { return _h; }

  virtual bool isOn() = 0;
  virtual bool isEink() { return false; } // default to non-eink, override in eink drivers
  virtual void turnOn() = 0;
  virtual void turnOff() = 0;
  virtual void clear() = 0;
```

Eleven display types implement this contract. One of them does nothing: nodes
without a screen get that implementation, so the application never has to ask
whether there is a screen.

The contract has one limitation that cannot be abstracted away. An e-ink
screen cannot be treated as an LCD —
refreshing takes seconds rather than milliseconds — and that difference cannot
be abstracted away. The contract solves it by letting the application ask what
kind of screen it is. That is a deliberate concession; see
[Design decisions](decisions.md).

## What a contract does not enforce

None of the contracts fixes when something is called or how long a call may
take. Everything runs in one loop, and an implementation that hangs holds up
the whole system. That is an agreement written down nowhere but in force
nonetheless.

Nor does a contract enforce that an implementation behaves well on failure.
There is no error model: a radio that does not respond does not say so, it
simply delivers no packets.

## Sources

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/MeshCore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/MeshCore.h)
- [MeshCore `03b6ef4` — `src/Mesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Mesh.h)
- [MeshCore `03b6ef4` — `src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/DisplayDriver.h)

Translated from Dutch by Anthropic Claude
