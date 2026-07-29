# Communication

*CHANNELS · ROOM SERVERS · DIRECT MESSAGES*

MeshCore offers three forms of communication: **Channels** for real-time group chat, **Room Servers** for persistent group communication with store-and-forward, and **Direct Messages** for private end-to-end encrypted messages.

## Channels

A Channel is a shared cryptographic key (PSK for AES-128 encryption). Nodes with the same key can read each other's messages. There is no central server or member list — messages are real-time and are not stored.

### Public Channel (#public)

The default channel automatically added during every installation. This is the "marketplace" channel that everyone listens to. Useful for initial contact, but offers no privacy.

### Hashtag Channel (#name)

Community channels for specific topics or regions, such as **#switzerland**, **#berlin**, or **#morsecode**. The key is derived from the name, so anyone who knows the name can listen in.

### Private Channel (own key)

A channel with a self-chosen, random key that you share only with the intended participants. This provides genuine privacy — only those with the key can listen in.

## Room Servers

A Room Server is a physical node running server firmware that acts as a BBS
(Bulletin Board System). It offers:

- **Store-and-forward** — messages are held until the recipient is reachable
  again
- **Password-based access** — one password for participants, one for the
  administrator, and the password you enter determines what you may do
- **A queue of 32 posts** — cyclic, so post 33 overwrites post 1
- **Pushing rather than fetching** — the server tracks how far each
  participant has got and sends the next post when their turn comes

Users log in with a password and are then sent what was posted while they
were away.

> [!WARNING]
> **The queue lives in working memory only.** A restart, a flat battery or a
> `reboot` wipes all 32 posts. A Room Server bridges hours to days; it is not
> an archive. There is also *no* member list — not even an administrator can
> ask who is in the Room — and administration consists of one command that
> sets rights on a public key, not of adding and removing members.

Exactly how that logging in, pushing and confirming works is covered in
[What a Room Server Is](../technical/roomserver/introduction.md) and the four
deeper chapters behind it.

## Direct Messages (DM)

Private messages between two specific nodes. DMs are **end-to-end encrypted** and can only be read by the sender and recipient.

### How DMs work

1. Node A broadcasts an *advert* containing its public key
2. Node B receives the advert and stores the public key
3. Node B can now send an encrypted DM to Node A
4. For two-way communication, Node B must also broadcast an advert

> [!NOTE]
> **Zero-hop or flood.** An advert can go on air in two ways. A *zero-hop*
> advert stays with the direct neighbours: nobody forwards it. A *flood* advert
> **is** passed on by repeaters, up to its own hop limit (`flood.max.advert`) and
> at reduced priority. Nodes therefore do not necessarily have to hear each other
> directly for the key exchange; it depends on how the advert was sent.

For the technical side of a DM — how the path is learned, what the packet looks
like and why it carries no region code — see
[Direct Messages](../technical/direct-messages.md).

## Channels vs. Rooms vs. DMs

| Property | Channel | Room Server | Direct Message |
|---|---|---|---|
| Storage | None | 32 posts, in RAM | None |
| Privacy | Shared key | Password | End-to-end |
| Member list | No | No | N/A |
| Offline messages | No | Yes | No |
| Survives a restart | N/A | No | N/A |
| Server required | No | Yes (dedicated node) | No |

Translated from Dutch by Anthropic Claude
