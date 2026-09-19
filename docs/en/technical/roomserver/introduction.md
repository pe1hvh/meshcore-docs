# What a Room Server Is

*BBS · STORE-AND-FORWARD · LOGGING IN · WHAT YOU NOTICE AS A USER*

A channel is like calling out in a hall: whoever is present hears it, whoever
is away is out of luck. A room server is the node that holds the conversation
for you. You log in with a password, you send your message to the server
instead of into the air, and whoever comes back later still gets to hear what
they missed. This chapter explains what that means in practice — the
machinery behind it is covered by the four chapters that follow.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/simple_room_server/MyMesh.h`,
> `examples/simple_room_server/MyMesh.cpp`, `src/helpers/ClientACL.h`,
> `src/helpers/AdvertDataHelpers.h`, and the official `docs/faq.md`. The
> build-target figures come from
> [`tools/room-server-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/room-server-overview.py).

## The comparison that holds

The official FAQ puts it sharply: a channel is like calling out, a room
server is like e-mail. With a channel you receive a message at the moment it
is sent, or you never receive it at all. With a room server it waits for you
to come and collect it — or more precisely: until the server can get it to
you.

![A channel message only reaches whoever is switched on at that moment; a
room server holds the post and delivers it once the recipient is back](../../../images/en/room-server-overview-1.svg)

That difference is the entire reason the thing exists. For a group that is
not online at the same time — a club, a neighbourhood, a party of walkers
spread out along a route — a channel is useless and a room server is exactly
what you want.

The name *BBS* you come across in the firmware (the default name of an
unconfigured room server is literally `Test BBS`) refers to the bulletin
boards that predate the internet: a central place where you leave messages
and collect messages, and where nobody has to be present at the same time.

## What you do as a user

1. **The server appears in your contact list.** A room server broadcasts an
   advert periodically, just like any other node, but with a type of its own.
   Your client uses that to recognise it as a server rather than an ordinary
   conversation partner, and files it separately.
2. **You log in with a password.** There are two passwords: one for ordinary
   participants and one for the administrator. Which one you enter determines
   what you are allowed to do. By default most firmware has the participant
   password set to `hello` and the administrator password to `password` —
   both should be changed when the node is put into service.
3. **You send your message to the server.** To your client this feels like a
   direct message to a single contact. The server turns it into a *post* and
   places it in its queue.
4. **The server pushes the posts to you.** You do not fetch anything: the
   server tracks how far each participant has got, and sends the next post
   whenever it gets round to it. For every post it wants a delivery
   confirmation back; if that fails to arrive, it tries again.

Step 4 is where the biggest gap sits between the firmware and what people
expect. There is no "fetch my messages" button. The server works through its
participants one by one, in a fixed rotation, and sends one post per turn.
Anyone who has been away for a long time therefore receives their backlog in
a trickle rather than all at once.

## What a room server does *not* do

This list is longer than you would expect, and it matters more than the list
above. Four things that are commonly assumed and that the firmware does not
offer:

| Expectation | What the firmware does |
|---|---|
| You can see who is in the room | There is no member list. Only an administrator can request a list, and it contains other administrators only |
| The history is retained | The queue has 32 slots and lives in working memory only. After a restart everything is gone |
| An administrator adds and removes members | There is one command that sets rights on a public key. Adding and removing as an action does not exist |
| A room server also strengthens the network | Forwarding is off by default. You can switch it on, but the official FAQ advises against it: you then miss the features only the repeater firmware has |

> [!WARNING]
> **Do not count on a room server as an archive.** The 32 posts live in RAM
> and nowhere else. A power cut, a flat battery or a `reboot` wipes them
> without warning. The server is a relay that can wait a while, not a storage
> place. Anyone who wants to keep the conversation keeps it on the client.

## How many there are

The room server is not a side track in the project. Of the 79 variant
directories in the firmware, **65** have at least one room-server build
target, **73** targets in total — some boards have two or three, for a
different display variant or a different transmit power. Virtually every
board MeshCore supports can therefore become a room server; it is a matter of
flashing different firmware, not of buying different hardware.

The firmware itself is small: five files totalling 1518 lines, of which
`MyMesh.cpp` accounts for 1030. That is manageable, and it is the reason the
following chapters can go down to the byte.

## Where this goes next

- [Logging In and the ACL](login-and-acl.md) — the three password paths, what
  each password allows you to do, and which part of your membership survives
  a restart.
- [Posts and Synchronisation](posts-and-sync.md) — how a message becomes a
  post, how the queue works and how the server tracks who is where.
- [Requests and CLI](requests-and-cli.md) — what else a client can ask the
  server, and how you administer it remotely.
- [Limits and Loose Ends](limits-and-todos.md) — what the firmware does not
  do yet, including the `TODO`s that are literally written into it.

For the place of the room server among the other forms of communication, see
[Communication](../../usage/communication.md). For the packet a post travels
in, see [Direct Messages](../direct-messages.md) — a post uses the same
payload type.

## Sources

- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `src/helpers/AdvertDataHelpers.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/AdvertDataHelpers.h)
- [MeshCore firmware — `docs/faq.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/faq.md)

Translated from Dutch by Anthropic Claude
