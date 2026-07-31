# Architecture of a client

*SIX LAYERS · RECONNECTING · SUBSCRIPTIONS · EXISTING CLIENTS*

A working companion client is not a thin wrapper around a socket. There are
six clearly separated responsibilities in it, and `meshcore_py` shows which.
This chapter describes that layering and sets out which clients already
exist.

> [!NOTE]
> **Source.** The layering is derived from `meshcore_py` v2.3.8, commit
> `c487efb` — modules `ble_cx.py`, `serial_cx.py`, `tcp_cx.py`,
> `connection_manager.py`, `reader.py`, `events.py`, `commands/` and
> `meshcore.py`. The protocol facts referred to come from `MeshCore`
> v1.16.0, commit `03b6ef4`.

![Six layers stacked, from transport to facade with cache, each with the
meshcore_py module fulfilling that role](../../../images/en/companion-architecture-1.svg)

> [!WARNING]
> This chapter is normative: it describes a layering that works, not a
> prescribed standard. There is no official reference architecture for
> MeshCore clients. If your client differs and works, that is not a mistake.

The six layers, one sentence each:

| Layer | What that layer does |
|---|---|
| Transport | opens the connection and moves bytes; knows nothing of frames |
| Connection management | watches the connection and re-announces the app after reconnecting |
| Frame reader | cuts the byte stream into frames and turns each frame into an object with named fields |
| Events | distributes those objects to every part of the app waiting for them |
| Command layer | sends commands and matches incoming responses to the right request |
| Facade with cache | the layer the app itself calls; keeps the current state |

## Layer 1 — Transport

Connect, bytes in and out, nothing more. Three implementations behind one
agreement, exactly as `BaseSerialInterface` does on the firmware side.
`meshcore_py` fixes that agreement as a `Protocol` with four methods and
documents the return contract explicitly:

`src/meshcore/connection_manager.py` r.13-23

```python
class ConnectionProtocol(Protocol):
    """Protocol defining the interface that connection classes must implement.

    Return contract for connect():
        - On success: return a truthy value (typically an address string)
          that identifies the connection. This value is included in the
          CONNECTED event payload as ``connection_info``.
        - On failure: return ``None`` (soft failure — triggers a retry in
          ``_attempt_reconnect``) **or** raise an exception (hard failure —
          also triggers a retry, logged as an error).
    """
```

What `connect()` returns ends up in the data of the connection event
(`connection_info` in the `CONNECTED` event). The distinction between soft
and hard failure is not cosmetic: a BLE radio that momentarily finds nothing
is a different matter from a serial port that does not exist, but both must
lead to another attempt.

## Layer 2 — Connection management

Reconnect, count how often, and — this is the point clients most often miss
— re-announce after every successful reconnection. `ConnectionManager` takes
a `reconnect_callback` for that.

This is the layer where the behaviour from
[The interaction model](../logical/interaction-model.md) belongs:
`app_target_ver` on the node is zero again after a drop, so `CMD_APP_START`
and `CMD_DEVICE_QUERY` have to be repeated. Hang that announcement off
program start-up instead of the connection, and the client works the first
time and silently delivers wrongly parsed frames afterwards.

## Layer 3 — Frame reader

Bytes in, typed event out. One entry point that reads the first byte,
decides whether it is a response or an unsolicited notification, reads the
fields out of the payload and turns it into an object. In `meshcore_py` that
is `reader.py` — at over a thousand lines the largest module in the library,
which is a reasonable indication of how much work this layer is.

The length check belongs here too: a field that exists only from a certain
`FIRMWARE_VER_CODE` onwards may only be read if the frame is long enough.
See [The frame](frame-format.md).

## Layer 4 — Events

Subscriptions instead of callbacks. The reason lies in the nature of the
protocol: push codes arrive unsolicited and can have several interested
parties. A map view, a notification counter and a conversation window all
three want to know something about the same incoming message.

`meshcore_py` defines over fifty event types for this, including two that do
not come from the protocol but from layer 2: `CONNECTED` and `DISCONNECTED`.

## Layer 5 — Command layer

Send, wait, and match the answer to the request. Two things are fixed here:

- **One request at a time.** `meshcore_py` uses a lock around requests that
  go into the mesh. That is not caution but necessity: the node's send queue
  is four or twelve frames long and overflow is silent. See
  [The three transports](transports.md).
- **A time limit per request.** `CommandHandlerBase.DEFAULT_TIMEOUT` stands
  at 15 seconds. Requests that go into the mesh may take longer and get
  their limit from the node's own answer.

## Layer 6 — Facade with cache

The layer an app actually uses: the facade the five layers below it hide
behind. Keeps contacts, `self_info` and the clock, and offers the
synchronisation loop as something you switch on rather than something you
write yourself. That cache is more than a speed measure: it is the current
state the app works on, and it therefore has to be updated as soon as a
notification arrives that affects it. `meshcore_py` subscribes to
`MESSAGES_WAITING` and then starts a loop repeating `CMD_SYNC_NEXT_MESSAGE`
until there are no messages left — exactly the pattern from
[Responsibilities](../logical/responsibilities.md).

## Why this order

| Layer | Changes when | Must know nothing about |
|---|---|---|
| Transport | a new connection type is added | opcodes |
| Connection management | the reconnection policy changes | payload layout |
| Frame reader | the firmware adds a field | the user interface |
| Events | rarely | bytes |
| Command layer | a command is added | the transport |
| Facade | the app wants something else | frame limits |

The middle column predicts where the work sits at a firmware update: almost
always in layers 3 and 5, rarely outside them.

## Which clients exist

The official MeshCore Companion App is closed. There is no public repository
of the Android, iOS or web version; the app is built in Flutter and free to
use.

| Client | Platform | Source | Status |
|---|---|---|---|
| MeshCore Companion App | Android, iOS, web | closed | the official app |
| `meshcore_py` | Python | MIT | official, v2.3.8 |
| `meshcore.js` | JavaScript | MIT | official, v1.13.0 |
| `meshcore-cli` | Python | MIT | official, on top of `meshcore_py` |
| `liamcottle/meshcore-web` | web | open | no longer updated, explicitly meant as a reference |
| MeshCore Open | Flutter, several platforms | MIT | community |
| MeshCore One | iOS | open | community |

The bottom two are not official projects and are listed here because they
are working, readable implementations — not as a recommendation.

> [!NOTE]
> The firmware points at different repositories for the same libraries in
> two places. `README.md` r.70-71 names `liamcottle/meshcore.js` and
> `fdlamotte/meshcore-cli`; `docs/companion_protocol.md` r.16-17 names
> `meshcore-dev/meshcore.js` and `meshcore-dev/meshcore_py`. The projects
> moved to the organisation and the README did not follow. Assume the
> `meshcore-dev` variants.

## Sources

`meshcore_py` v2.3.8, commit `c487efb`:

- [`src/meshcore/connection_manager.py`](https://github.com/meshcore-dev/meshcore_py/blob/main/src/meshcore/connection_manager.py)
  — the connection contract and the reconnecting
- [`src/meshcore/reader.py`](https://github.com/meshcore-dev/meshcore_py/blob/main/src/meshcore/reader.py)
  — frames into events
- [`src/meshcore/commands/base.py`](https://github.com/meshcore-dev/meshcore_py/blob/main/src/meshcore/commands/base.py)
  — time limits and matching answer to request
- [`src/meshcore/meshcore.py`](https://github.com/meshcore-dev/meshcore_py/blob/main/src/meshcore/meshcore.py)
  — the facade and the synchronisation loop

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`README.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/README.md)
  — the client list with the differing references

Related chapters:

- [The interaction model](../logical/interaction-model.md) — why
  reconnecting means re-announcing
- [The three transports](transports.md) — why one request at a time
- [GitHub Repositories](../../project/github.md) — the repositories
  themselves

Translated from Dutch by Anthropic Claude
