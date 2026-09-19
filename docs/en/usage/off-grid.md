# Off-Grid Client Repeat Mode

*EXTENDING THE MESH · CLIENT AS REPEATER · INCREASING RANGE*

In MeshCore there is a strict separation between **clients** (which send and receive messages) and **repeaters** (which forward traffic). With **Client Repeat Mode** this separation disappears: a regular client node can simultaneously act as a repeater and extend the mesh network — without extra hardware.

## How does it work?

Normally a client node only processes its own traffic: sending, receiving, and displaying messages on screen or via the companion app. Once **Client Repeat Mode** is enabled, the node also repeats packets from other nodes in the network. The device effectively becomes a *hybrid*: fully usable as a client and actively forwarding mesh traffic for others.

## Why is this important?

- **Dynamic range** — Every participating client automatically extends the network. The more users, the greater the range — without fixed infrastructure.
- **No repeaters needed** — In remote areas or during events, a fixed repeater is often unavailable. Client Repeat Mode fills that gap.
- **Easy on/off** — The mode can be enabled or disabled via the companion app. Handy for saving battery when you don't want to forward traffic.
- **Full encryption** — Forwarded packets remain fully encrypted. The repeating node cannot read the content — only forward it.

## Typical use cases

Client Repeat Mode is particularly useful in situations where the mesh must emerge spontaneously from the devices present:

- **Hiking and mountain trips** — participants spread along a route together form a chain of repeaters, allowing messages to travel from head to tail
- **Festivals and events** — large groups with MeshCore devices automatically build a dense, self-healing network
- **Emergency communication** — when fixed infrastructure is missing or has failed, every client provides an extra link in the network
- **Field days and radio activities** — participants at different locations boost each other's range without extra equipment

## How to enable it?

The setting is available in the companion app (Android/iOS) under node settings. After enabling, the device immediately starts forwarding packets from other nodes. Its own functionality as a client remains fully intact — sending messages, receiving, DMs, and Room access all continue to work normally.

> [!WARNING]
> **Note:** Client Repeat Mode significantly increases battery consumption, because the radio is active more often. Preferably use a device with USB power or a larger battery when you want to operate as a repeater for an extended period.

## Client vs. Repeater vs. Client Repeat

| Property | Client | Repeater | Client Repeat |
|---|---|---|---|
| Send messages | Yes | No | Yes |
| Receive messages | Yes | No | Yes |
| Forward packets | No | Yes | Yes |
| Companion app | Yes | No | Yes |
| Battery consumption | Low | High | High |
| Dedicated hardware required | No | Yes | No |

## Source

This article is based on the publication by Ripple about Off-Grid Client Repeat Mode:<br> [buymeacoffee.com/ripplebiz — Off-Grid Client Repeat Mode ↗](https://buymeacoffee.com/ripplebiz/off-grid-client-repeat-mode)

Translated from Dutch by Anthropic Claude
