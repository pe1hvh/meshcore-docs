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

A Room Server is a physical node running server firmware that acts as a BBS (Bulletin Board System). It offers:

- **Store-and-forward** — messages are stored until the recipient comes online
- **Member list** — you can see who is in the Room
- **Management** — moderators can add and remove members
- **Persistence** — up to 32 messages are retained

Users log in with a password and can later retrieve messages sent while they were offline.

## Direct Messages (DM)

Private messages between two specific nodes. DMs are **end-to-end encrypted** and can only be read by the sender and recipient.

### How DMs work

1. Node A broadcasts an *advert* containing its public key
2. Node B receives the advert and stores the public key
3. Node B can now send an encrypted DM to Node A
4. For two-way communication, Node B must also broadcast an advert

> [!WARNING]
> **Important:** Adverts are NOT forwarded by repeaters. Both nodes must be able to directly "hear" each other for key exchange.

## Channels vs. Rooms vs. DMs

| Property | Channel | Room Server | Direct Message |
|---|---|---|---|
| Storage | None | Store-and-forward | None |
| Privacy | Shared key | Password | End-to-end |
| Member list | No | Yes | N/A |
| Offline messages | No | Yes | No |
| Server required | No | Yes (dedicated node) | No |

Translated from Dutch by Anthropic Claude
