# Responsibilities

*NODE · APP · STORAGE · QUEUE · WHAT GETS LOST*

The node and the app both keep something, and the split is not arbitrary.
The node holds what it needs to keep working without a phone; the app holds
everything that grows. Draw that line wrongly and you build a client that
loses messages.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/companion_radio/MyMesh.h`,
> `examples/companion_radio/MyMesh.cpp` and
> `examples/companion_radio/DataStore.h`. The distribution of the limit
> values across the build targets comes from `tools/companion-opcodes.py`.

![The node keeps identity, preferences, contacts, channel slots and a
message queue; the app keeps the full history and the mapping between
channel and scope](../../../images/en/companion-responsibilities-1.svg)

## What the node keeps

`DataStore` is the only place where the firmware writes to the file system.
The class names exactly five kinds of data:

`examples/companion_radio/DataStore.h` r.34-40

```cpp
  bool loadMainIdentity(mesh::LocalIdentity &identity);
  bool saveMainIdentity(const mesh::LocalIdentity &identity);
  void loadPrefs(NodePrefs& prefs, double& node_lat, double& node_lon);
  void savePrefs(const NodePrefs& prefs, double node_lat, double node_lon);
  void loadContacts(DataStoreHost* host);
  void saveContacts(DataStoreHost* host, bool (*filter)(const ContactInfo& c) = NULL);
  void loadChannels(DataStoreHost* host);
```

Identity, preferences, contacts and channels. Nothing more — there is no
`loadMessages()`, and that is not an omission but the design.

## The maximum counts differ per firmware variant

The sizes are fixed at compile time. They are indeed constants, but their
value differs per firmware variant: the value in the header is usually
**not** the value running on the device. `MyMesh.h` puts them behind
`#ifndef` so a build flag can override them:

`examples/companion_radio/MyMesh.h` r.58-64

```cpp
#ifndef MAX_CONTACTS
#define MAX_CONTACTS 100
#endif

#ifndef OFFLINE_QUEUE_SIZE
#define OFFLINE_QUEUE_SIZE 16
#endif
```

Across the 174 build targets that compile `examples/companion_radio`, the
actual distribution looks like this:

| Constant | In the header | In the build targets |
|---|---|---|
| `MAX_CONTACTS` | 100 | 350 (151×), 160 (12×), 100 (8×), 300 (3×) |
| `OFFLINE_QUEUE_SIZE` | 16 | 256 (113×), 128 (10×), unset and therefore 16 (51×) |
| `MAX_GROUP_CHANNELS` | not present | 40 (154×), 8 (20×) |

For an app that means one thing: **read the limits from the response to
`CMD_DEVICE_QUERY` and never copy them from the source code.** See
[The interaction model](interaction-model.md).

> [!WARNING]
> **The contact count is halved in the frame.** The firmware sends
> `MAX_CONTACTS / 2`, not the value itself. A node with room for 350 contacts
> therefore puts 175 in the response to `CMD_DEVICE_QUERY`, and the app has
> to double that number: 175 × 2 = 350. An app that takes the frame literally
> thinks half as many contacts fit as actually do.

## What the app keeps

Everything that grows, and everything the firmware does not need in order to
function:

- the full message history, per contact and per channel
- which channel belongs to which region scope — the firmware does not know
  that mapping and expects the app to set the right scope before sending;
  see [Regions and Scopes](../../technical/regions-and-scopes.md)
- its own names, grouping, favourites and read state
- which messages had already been fetched when the connection dropped

## The queue is a pass-through buffer

A pass-through buffer is temporary storage: what sits in it stays only until
it is fetched, and disappears afterwards. `offline_queue` is the only place
where the node holds an incoming message until the app fetches it. When it
fills up, the firmware discards the oldest **channel message** to make
room:

`examples/companion_radio/MyMesh.cpp` r.219-232

```cpp
void MyMesh::addToOfflineQueue(const uint8_t frame[], int len) {
  if (offline_queue_len >= OFFLINE_QUEUE_SIZE) {
    MESH_DEBUG_PRINTLN("WARN: offline_queue is full!");
    int pos = 0;
    while (pos < offline_queue_len) {
      if (offline_queue[pos].isChannelMsg()) {
        for (int i = pos; i < offline_queue_len - 1; i++) { // delete oldest channel msg from queue
          offline_queue[i] = offline_queue[i + 1];
        }
        MESH_DEBUG_PRINTLN("INFO: removed oldest channel message from queue.");
        offline_queue[offline_queue_len - 1].len = len;
        memcpy(offline_queue[offline_queue_len - 1].buf, frame, len);
        return;
      }
```

If only direct messages are present, the loop runs out without removing
anything, the firmware reports `no channel messages to remove from queue`,
and the function returns *without* storing the new message. So it is not the
case that the oldest message always yields: **direct messages are never
discarded, but a new message is lost as soon as the queue is full of direct
messages.**

For a client that means one rule: drain the queue as soon as you can, and do
not rely on the node as storage.

## Consequences for designing an app

| Assumption | Wrong, because |
|---|---|
| "The node keeps my conversations" | there is no message storage, only a queue |
| "I can reinstall the app and get everything back" | the history existed only in the app |
| "Two apps on the same node see the same thing" | whoever synchronises first empties the queue |
| "40 channels always works" | it is 8 or 40, depending on the firmware variant |
| "The node knows which scope belongs to my channel" | that mapping exists only in the app |

That second-to-last point is why two simultaneous clients on one node get in
each other's way. See [The three transports](../technical/transports.md) for
what the transports do and do not do about it.

## Sources

Firmware, commit `03b6ef4` (v1.16.0, 28 July 2026):

- [`examples/companion_radio/DataStore.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/DataStore.h)
  — what goes to the file system
- [`examples/companion_radio/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.h)
  — `MAX_CONTACTS` and `OFFLINE_QUEUE_SIZE`, both behind `#ifndef`
- [`examples/companion_radio/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4b0de98fc70b49ef10a6d0d61f8381fb7a/examples/companion_radio/MyMesh.cpp)
  — `addToOfflineQueue()` and `getFromOfflineQueue()`

Reproduction:

- `tools/companion-opcodes.py` — counts the companion build targets and the
  distribution of `MAX_CONTACTS`, `OFFLINE_QUEUE_SIZE` and
  `MAX_GROUP_CHANNELS` across them

**Counting method.** The script treats an `[env:…]` as a companion when
`build_src_filter` contains `../examples/companion_radio`, with `extends` and
`${section.option}` resolved. The figure of 174 matches
`tools/design-overview.py`, which counts the same way.

Related chapters:

- [The interaction model](interaction-model.md) — how the queue gets drained
- [Information model](information-model.md) — which data exists exactly
- [Regions and Scopes](../../technical/regions-and-scopes.md) — the mapping
  the app has to maintain

Translated from Dutch by Anthropic Claude
