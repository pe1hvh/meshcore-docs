# Design decisions

*CHOICES · CONSEQUENCES · WHAT THEY RULE OUT*

Every design is a sequence of choices, and every choice excludes something.
This chapter describes the seven decisions that determine MeshCore's character
— not as a justification, but as an explanation of what you can and cannot
expect from a node built this way.

> [!NOTE]
> **Source.** This page was verified against the firmware itself: `MeshCore`
> v1.16.0, commit `03b6ef4`, 28 July 2026 — `src/Dispatcher.h`,
> `src/MeshCore.h`, `src/helpers/StaticPoolPacketManager.h` and the root
> `platformio.ini`.

## 1. Configuration at compile time, not at startup

The role, the radio, the display and the bridges are fixed in the binary. There
is no configuration file deciding whether a node is a repeater or a room
server.

**Why.** An nRF52 with 256 KB of RAM cannot hold all six roles and eleven
display drivers in memory at once. Choosing at compile time means only the
chosen code ends up in the binary.

**What it costs.** You cannot change a node's role without flashing new
firmware. And the number of build targets grows with the product of the axes —
508 of them, all of which have to keep compiling.

## 2. One loop, no task model

Everything runs in one `loop()`. There is no scheduler, no threads, no
priorities between tasks.

**Why.** It saves memory, it makes behaviour predictable, and it works the same
on four platform families, two of which have no usable task model.

**What it costs.** Every component has to return quickly. A display driver
refreshing an e-ink screen holds up the radio. The design does not solve that;
it makes it visible, by letting the display contract tell the application
whether it is dealing with e-ink.

## 3. Packets from a fixed pool

Packets are not allocated dynamically but taken from a pre-reserved pool.

**Why.** On a microcontroller that has to run for months on end, memory
fragmentation is a slow killer. A fixed pool cannot fragment and memory use is
known at startup.

**What it costs.** The pool can run out. If more packets are in flight than
there are slots, one is dropped. That is a design choice — a predictable loss
rather than an unpredictable restart.

## 4. Routing is in the packet, not in the node

A node keeps no map of the network. Paths travel with the packets.

**Why.** A routing table has to be maintained, and that costs traffic. In a
network where airtime is legally capped and bandwidth is measured in hundreds
of bytes per second, every maintenance message is a message that does not get
through.

**What it costs.** A node does not know whether a path still works until it
tries. There is no way to discover that a repeater has failed other than by
noticing that nothing comes back.

## 5. Everything behind a contract, even with one implementation

The seen table and the packet pool each have exactly one implementation, and
still there is a contract in between.

**Why.** The contract is not preparation for future implementations but a
boundary. It fixes what the mesh logic may expect of that component, and
enforces that nothing leaks through.

**What it costs.** A layer of indirection that at this scale buys no
flexibility. That is the price the design knowingly pays.

## 6. Four platform families, three shared board classes

ESP32, nRF52 and STM32 each have a shared board implementation in the core.
RP2040 does not: each of the four RP2040 boards writes its own.

**Why.** This is not a design choice but a grown situation. RP2040 arrived
later and with few variants; there was never enough overlap to justify a shared
base.

**What it costs.** The same code for battery measurement and restart four
times, in four places that have to be maintained separately. Adding a fifth
RP2040 board means copying again.

It is the clearest place where the design is not carried through consistently,
and it is here because leaving it out would make the document prettier but
wrong.

## 7. No error model

Contracts return no errors. A radio that does not respond does not say so; it
simply delivers no packets. A write to storage that fails, fails silently.

**Why.** Error handling costs code and memory, and on a node without a user
there is usually nobody to report the error to.

**What it costs.** Remote diagnosis is hard. A repeater that has lost its radio
behaves like a repeater in a quiet area. The statistics a node keeps — sent,
received, airtime budget — are therefore the only tool there is.

## What these choices add up to

Six of the seven point the same way: predictable memory use and little traffic,
at the cost of flexibility at run time. That is a coherent design for what
MeshCore wants to be — a node you hang up and forget.

The seventh, the RP2040 asymmetry, does not fit that. It is simply there.

## Sources

- [MeshCore `03b6ef4` — `src/Dispatcher.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Dispatcher.h)
- [MeshCore `03b6ef4` — `src/helpers/StaticPoolPacketManager.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/StaticPoolPacketManager.h)
- [MeshCore `03b6ef4` — `src/helpers/ui/DisplayDriver.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ui/DisplayDriver.h)
- [MeshCore `03b6ef4` — `variants/rak11310/RAK11310Board.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/variants/rak11310/RAK11310Board.h)

Translated from Dutch by Anthropic Claude
