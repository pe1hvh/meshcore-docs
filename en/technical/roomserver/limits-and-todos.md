# Limits and Loose Ends

*WHAT IS GONE · WHAT FILLS UP · WHAT IS LITERALLY MARKED TODO*

This chapter collects what the room server does *not* do. Not as criticism —
the firmware is small and does its job — but because a number of those limits
run counter to what users expect, and because the authors wrote part of it
down in the code themselves. Eight `TODO` and `REVISIT` lines appear in
`MyMesh.cpp`; all of them are named below.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/simple_room_server/MyMesh.h`,
> `examples/simple_room_server/MyMesh.cpp`, `src/helpers/ClientACL.h`,
> `src/helpers/ClientACL.cpp`, and the official `docs/faq.md`. The check for
> variant overrides comes from
> [`tools/room-server-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/room-server-overview.py).

## None of the content survives a restart

The queue is an array in working memory. There is not a single place in
`MyMesh.cpp` where posts go to the file system; the only files a room server
creates are the ACL and the optional packet log. A reset, a flat battery or a
`reboot` command wipes all 32 slots.

It also means that catching up on a backlog after a server restart does not
happen. The clients still know where they had got to and dutifully send their
`sync_since` along, but the server has nothing left to hold against that
boundary. No error appears: everything is up to date, because there is
nothing.

> [!WARNING]
> **Do not treat a room server as an archive.** Anyone who wants to keep the
> conversation keeps it on the client. The server is meant to bridge hours to
> days, not to hold history.

## The queue overflows without warning

32 slots, cyclic. `next_post_idx` wraps around and overwrites the oldest
slot, whether or not that post has reached everyone. The name
`MAX_UNSYNCED_POSTS` suggests it is about *unconfirmed* posts, but nothing in
the add path checks whether the slot being overwritten has been delivered.

Practical consequence: a participant who stays away for longer than 32 posts
can skip posts without anyone noticing. Their `sync_since` simply jumps to
the timestamp of the post they *did* receive at the next confirmation; what
sat in between was never sent and is never missed.

No variant sets `MAX_UNSYNCED_POSTS` or `MAX_CLIENTS` to a different value —
the firmware is identical on all 73 room-server build targets as far as these
two limits are concerned. Anyone wanting more compiles their own.

## The client table crowds out the quietest participant

`MAX_CLIENTS` is 20. When the table fills up, `putClient()` throws somebody
out to make room:

`src/helpers/ClientACL.cpp` r.97-113

```cpp
ClientInfo* ClientACL::putClient(const mesh::Identity& id, uint8_t init_perms) {
  uint32_t min_time = 0xFFFFFFFF;
  ClientInfo* oldest = &clients[MAX_CLIENTS - 1];
  for (int i = 0; i < num_clients; i++) {
    if (id.matches(clients[i].id)) return &clients[i];  // already known
    if (!clients[i].isAdmin() && clients[i].last_activity < min_time) {
      oldest = &clients[i];
      min_time = oldest->last_activity;
    }
  }

  ClientInfo* c;
  if (num_clients < MAX_CLIENTS) {
    c = &clients[num_clients++];
  } else {
    c = oldest;  // evict least active contact
  }
```

The longest inactive non-administrator is overwritten. That is reasonable
behaviour, but it is silent: the displaced participant gets no notification
and only notices because the server stops sending them anything. They get
back in by logging in again — after which they displace somebody else in
turn. Beyond twenty active participants a room server therefore starts to
churn.

One edge case deserves attention. `oldest` starts at the *last* slot in the
table, and the loop only replaces that pointer with non-administrators. If
all twenty slots are filled with administrators, `oldest` stays at
`clients[19]` and an **administrator** is overwritten there. That cannot be
provoked from outside — you would need twenty administrator passwords first —
but it is the only path by which an administrator disappears from the ACL
without `setperm`.

## After three failed attempts it goes quiet

A client whose pushes go unconfirmed three times in a row is skipped in the
rotation. There is no recovery mechanism on the server side: the counter only
returns to zero when the client sends something itself — a post, a keep-alive
or a request.

For a client that uses keep-alives that is no problem. For a client that does
not and only listens, it is: it falls permanently silent after three missed
pushes, even if it is perfectly reachable again afterwards.

There is a second limitation to go with it, one the authors noted themselves:

`examples/simple_room_server/MyMesh.cpp` r.955

```cpp
        c->extra.room.pending_ack = 0; // reset  (TODO: keep prev expected_ack's in a list, incase they arrive LATER, after we retry)
```

An ACK that arrives *after* the timeout is no longer recognised. The server
has discarded the expected value and counts the attempt as failed, while the
message did in fact arrive. On slow paths with many hops — where the timeout
is `4000 + 2000 × hops` milliseconds — that is a realistic scenario, and the
result is that the same post is sent all over again.

## Keep-alives are not throttled

`examples/simple_room_server/MyMesh.cpp` r.549-550

```cpp
        // TODO: Throttle KEEP_ALIVE requests!
        // if client sends too quickly, evict()
```

There is no brake. A client that sends keep-alives at a high rate is answered
every time, and every answer consumes air time on a band where the duty cycle
counts. The intended solution is written literally alongside it and has not
been built. See [Regulations & Duty Cycle](../../usage/regulations.md) for
why that is more than a cosmetic point.

`onPeerPathRecv()` — the function that stores a new path to a client — also
carries a loose end: `// TODO: prevent replay attacks` on r.589. Unlike
messages and requests, the timestamp is not checked there.

## Roles and fields that do nothing

| What | Where | Status |
|---|---|---|
| `PERM_ACL_READ_ONLY` (1) | `src/helpers/ClientACL.h` r.9 | defined, never granted by the room server |
| byte 5 of the login reply | `MyMesh.cpp` r.372 | always 0, was the recommended keep-alive interval |
| `<title>/<description>` in a post | `MyMesh.cpp` r.42 | noted as a `TODO`, not implemented |
| number of waiting posts in the login reply | `MyMesh.cpp` r.370 | noted as a `TODO`; now sits in the keep-alive ACK |

The third point explains why posts are unstructured in practice. The firmware
knows no subject and no layout: a post is 151 characters of plain text and
nothing more. Conventions about that are for a room to make itself.

## Forwarding is off, and that is deliberate

A room server has `disable_fwd = 1` as its default. It hears all the traffic
around it but passes nothing on. That can be switched on with `set repeat
on`, and the official FAQ advises against it: a room server with forwarding
enabled misses the full set of repeater features and the administration that
goes with them. The FAQ's recommendation is to run repeater and room server
on separate devices.

Two `REVISIT` lines touch this area. On r.78 the question is left open which
path-hash size a post should use when sent by flood while the path to a
client is still unknown; on r.719 whether the transport codes should carry a
separate region for the return leg. Both concern routing rather than the room
function itself; see [Regions and Scopes](../regions-and-scopes.md) for the
context.

## What this means for anyone setting one up

- Count on **a few days** of bridging, not on history.
- Keep the room under **twenty** active participants, or they will crowd each
  other out of the table.
- Change **both passwords** before the node goes on air.
- Do **not** let the node repeat as well; put a second node there for that.
- Expect no **member list** and no **moderation**: there is one command that
  sets rights, and nothing else.

## Sources

- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `src/helpers/ClientACL.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.cpp)
- [MeshCore firmware — `docs/faq.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/faq.md)

Translated from Dutch by Anthropic Claude
