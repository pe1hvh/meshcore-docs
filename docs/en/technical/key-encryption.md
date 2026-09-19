# Private & Public Key Encryption

*IDENTITY · TRUST · CONFIDENTIALITY · WITHOUT INTERNET · CC310*

> [!NOTE]
> **Source.** The section *Hardware crypto on nRF52* has been verified against
> the firmware itself: `MeshCore` v1.17.1, commit `d929643`, 14 August 2026 —
> files `platformio.ini`, `src/Utils.cpp`, `src/Identity.cpp`,
> `src/helpers/NRF52Board.cpp` and
> `src/helpers/radiolib/RadioLibWrappers.h`. The rest of this chapter
> describes the protocol and the kinds of key; that text has not yet been
> checked against a specific commit and therefore carries no pin of its own.

## The problem: communication without authority

MeshCore is designed for situations where **no internet, no servers, and no central authority** are available. Think of emergency communication during a disaster, off-grid operations in remote areas, or simply an autonomous local network independent of telecom providers or cloud infrastructure.

That sounds good, but it creates a problem. In a normal network (internet, WhatsApp, Signal) there is always a **trusted third party** in between: a server that verifies identities, issues certificates, and exchanges keys. On an open mesh radio network, that party does not exist. Every node is equal — there is no one saying "this node really is who it claims to be."

The cryptography in MeshCore solves three problems that arise when you remove that trusted third party:

> [!NOTE]
> **1. Identity** — How do I know who I am communicating with when there is no server registering users??
> **2. Authenticity** — How do I know a message truly comes from that node and has not been forged by someone else??
> **3. Confidentiality** — How do I prevent third parties from reading along on an open radio channel where literally anyone can listen??

The answer to all three is the same foundation: **public/private key cryptography**. Every communication type in MeshCore — channels, DM's, Room Servers — uses this foundation in a different way, tailored to the specific needs of that communication type.

## The Ed25519 Keypair: your identity on the mesh

On first flashing, every node generates an **Ed25519 keypair**. This is no trivial detail — it is the moment the node receives its **unique, unforgeable identity**. Without central registration, this keypair is the only proof that a node is who it claims to be.

| Key | Size | Purpose |
|---|---|---|
| Private Key | 64 bytes | Secret — never leaves the device. Proves identity by signing messages, and enables computing shared secrets for encrypted communication. |
| Public Key | 32 bytes | Public — distributed via ADVERT packets. Other nodes use it to recognise your identity, verify your signatures, and send encrypted messages to you. |

The first byte (2 hex characters) of the public key functions as a **short node identifier** in trace paths and packet routing. In a growing mesh these 1-byte identifiers can collide; a custom key generator can then guarantee a unique prefix.

> [!NOTE]
> **Compare it to a signature:** your public key is your name that everyone knows. Your private key is the way you sign — unique, impossible to forge, and proof that it is you.

## ADVERT: announcing yourself without a server

On the internet you register an account with a service and that service tells others you exist. On a mesh there is no service. The solution: every node **announces itself** via an ADVERT packet (payload type `0x04`).

```text
┌──────────────┬────────────┬──────────────┬──────────────────┐
│  Public Key  │ Timestamp  │  Signature   │     App Data     │
│   32 bytes   │  4 bytes   │   64 bytes   │   0-32 bytes     │
└──────────────┴────────────┴──────────────┴──────────────────┘
```

This packet is always **flood-routed** — every repeater forwards it. Each field serves a specific purpose in building trust without central authority:

- **Public Key** (32 bytes) — your complete public key, so other nodes can "get to know" you and later communicate securely with you
- **Ed25519 Signature** (64 bytes) — the signature covers the public key, timestamp, and app data, made **with your private key**. This solves the *authenticity* problem: nobody can forge an ADVERT on your behalf, because only you possess the private key that belongs to the public key
- **Timestamp** (4 bytes) — protection against **replay attacks**: if someone re-broadcasts an old ADVERT, receivers reject it because they already have a newer timestamp from the same sender
- **App Data** (up to 32 bytes) — a flags byte carrying the node type (chat / repeater / room server / sensor), optional GPS coordinates, and the name. There is no separate length field: the app data runs to the end of the payload

> [!WARNING]
> **This is the foundation:** without ADVERT exchange, no secure communication is possible. Receiving someone's public key via an ADVERT is the moment you can send DMs'to that node. No ADVERT received = no encrypted communication possible.

## Channel Messages: open square vs. closed room

Not all communication needs to be private. A mesh network also needs **open communication** — a digital marketplace where everyone can read along — and **group channels** for specific topics or teams. Here a different type of key is used: the **PSK (Pre-Shared Key)**.

### Why not public/private keys for channels?

The ECDH mechanism that secures DMs' works by definition between **two** nodes — it computes a shared secret from two keypairs. A group channel, however, has tens or hundreds of participants who all need to be able to read the same messages. That requires a **shared group key** (PSK) instead of per-pair keys. It is a deliberate architectural choice: group communication sacrifices individual cryptographic identity for scalability.

### Wat is een PSK?

A PSK (Pre-Shared Key) is an encryption key that is **shared in advance** among all participants — via QR code, handed over in person, or via another secure channel outside the mesh. All nodes with the same PSK can read and write messages on that channel. The node's personal keypair plays no role here.

### Packet structure (payload type 0x05)

```text
┌──────────────┬──────────┬──────────────────────────┐
│ Channel Hash │   MAC    │   Encrypted Payload      │
│   1 byte     │  2 bytes │      variable            │
└──────────────┴──────────┴──────────────────────────┘
```

After decryption with the PSK the payload contains:

```text
┌───────────┬───────┬────────────────────┐
│ Timestamp │ Flags │  "NodeName: text"  │
│  4 bytes  │ 1 byte│     variable       │
└───────────┴───────┴────────────────────┘
```

### Three channel types, three levels of openness

The choice between channel types is a deliberate trade-off between **reach** and **confidentiality**:

| Channel Type | How the PSK is determined | Purpose |
|---|---|---|
| Public | Fixed, known key (e.g. `AQ==`) | Open communication — the village square of the mesh where everyone is welcome |
| Hashtag (#naam) | Hash of the channel name | Thematic organisation — like a shared table in a café, not secret but shielded from the bustle |
| Private | Randomly generated, shared out-of-band | Closed group — like a meeting room with a lock, accessible only to those who have received the key |

### How it travels over the air

Channel messages are **always flood-routed**: every repeater blindly forwards the packet, even if that repeater cannot read the content. This is essential for the purpose of channels — **maximum reach**. The Channel Hash (1 byte) is a quick filter so a node can check whether it has a matching PSK without needing to decrypt everything.

> [!WARNING]
> **Note:** The public channel is technically encrypted (AES-128), but because the PSK is publicly known it provides no real privacy. The purpose of encryption here is not secrecy, but enabling correct decoding of the message from the radio signal.

## Direct Messages: private conversation without intermediary

Channels solve the problem of group communication, but for a **private conversation** between two people they are unsuitable — everyone with the PSK can read along. Here the public and private keys come into their own via **ECDH (Elliptic Curve Diffie-Hellman)**.

### The goal: a shared secret without ever exchanging it

The remarkable thing about ECDH is that two nodes can compute an **identical secret** without ever sending that secret over the radio. This is the most important thing in a mesh environment: everything you transmit over the air can be picked up by every repeater and every listener. With ECDH the secret itself never needs to go on the radio.

### The ECDH process

1. Node A knows the **public key** of Node B (received via ADVERT)
2. Node A computes: `shared_secret = ECDH(A_private, B_public)`
3. Node B computes independently: `shared_secret = ECDH(B_private, A_public)`
4. Both results are **mathematically identical** — property of elliptic curves
5. The shared secret is computed once when a contact is added and cached
6. All messages are AES-encrypted with this shared secret

> [!NOTE]
> **Why does this work without a central authority?** Because the trust lives in the mathematics, not in a server. Even if an attacker intercepts every ADVERT packet with its public key, they cannot compute the shared secret — that requires one of the two private keys, and those never leave the device.

### Packet structure (payload type 0x02)

```text
┌───────────┬──────────┬──────────┬──────────────────────────┐
│ Dest Hash │ Src Hash │   MAC    │   Encrypted Payload      │
│  1 byte   │  1 byte  │  2 bytes │      variable            │
└───────────┴──────────┴──────────┴──────────────────────────┘
```

The **Dest Hash** and **Src Hash** are the first bytes of the recipient's and sender's public keys. Repeaters can route the packet (they see the hashes) but **cannot read the content**. This is the heart of the privacy model: even the infrastructure that relays your message cannot read along.

After decryption with the ECDH shared secret:

```text
┌───────────┬───────┬──────────┬──────────────────┐
│ Timestamp │ Flags │   Text   │ Optional: Attempt│
│  4 bytes  │ 1 byte│ variable │     1 byte       │
└───────────┴───────┴──────────┴──────────────────┘
```

### Routing and confirmation

Unlike channels, DMs can be either **flood-** or **direct-routed**. If the mesh has previously learned a path to the recipient, the message follows that specific path — more efficient and less demanding on the network. The receiver sends back an **ACK** as proof that the message arrived unchanged: SHA256 over the timestamp, flags, text, and the sender's public key, truncated to 4 bytes. The ACK payload of an ordinary DM is 6 bytes — those 4 hash bytes plus a byte with the attempt number and a random byte, which keep the packet hash unique. Only the first 4 bytes are compared.

How the path is learned and why a directly routed DM carries no region code is covered in [Direct Messages](direct-messages.md).

## Room Servers: group chat with memory and anonymity

Channels are real-time and have no memory — if you are offline, you miss messages. DM's are private but only one-to-one. Room Servers combine the best of both: **group communication with message storage**. But logging into a Room Server carries an extra privacy risk: you might expose your permanent identity to the server.

### Solution: ephemeral (temporary) keys

When approaching a Room Server an **ANON_REQ** packet (type `0x07`) is sent. For this the node generates a **disposable keypair** — a temporary identity that exists only for this session:

1. The node creates an ephemeral Ed25519 keypair
2. The ephemeral public key is included in the packet
3. The Room Server derives a temporary shared secret from this
4. After authentication (password) the user receives the latest unread messages

The goal: your permanent identity (your real public key) is not directly exposed on first contact. This provides an **extra privacy layer** — the Room Server does not need to know who you "really" are in order to deliver messages to you.

| Room Type | Access | Typical use |
|---|---|---|
| Public Room | Empty or widely shared password | Open group communication with message history |
| Private Room | Secret password | Closed team communication with storage |
| Read-only Room | Admins only can write | Announcements, bulletins, news feeds |

## The bigger picture: why different mechanisms?

At first glance it seems complex: PSKs, ECDH, ephemeral keys — why not just one system? The answer lies in the **fundamentally different goals** of each communication type:

| Type | Primary goal | Encryption | Keypair role | Routing |
|---|---|---|---|---|
| Public Channel | Maximum reach, open communication | AES-128 with a publicly known PSK | None | Flood |
| Hashtag Channel | Thematic grouping without registration | AES-128 with a key hashed from the name | None | Flood |
| Private Channel | Secure group communication | AES-128 with a random PSK | None | Flood |
| Direct Message | Maximum privacy between two nodes | AES-128 with the ECDH secret | Central | Flood or Direct |
| Room Server | Group chat with memory and anonymity | Password + ephemeral ECDH | Temporary keypair | Direct |

The spectrum runs from **fully open** (public channel: everyone can listen in) to **maximally private** (DM: only the two involved nodes). Each communication type is a deliberate trade-off between reach, scalability, and confidentiality — and each uses precisely the cryptographic mechanism that fits that trade-off.

## The common thread: keys in every packet

The public keys are not only relevant for encryption — they are woven into the **foundation of every packet** that flies across the mesh:

```text
┌────────┬──────────┬─────────────────────────┐
│ Header │ Path Len │ Path[]                  │
│ 1 byte │ 1 byte   │ 1 byte per hop, max 64  │
└────────┴──────────┴─────────────────────────┘

Header byte = payload type + route type (flood of direct)
Path[]      = list of node identifiers (first bytes of public keys)
```

With **flood routing** every repeater appends its own identifier (= first byte of public key) to the path. With **direct routing** the complete planned path is already in the packet and each hop peels one off.

The public keys thus function on **two levels** simultaneously:

- **Routing addresses** — the first byte of the public key is the "house number" by which packets find their way through the mesh
- **Cryptographic foundation** — the complete public key is the raw material for ECDH shared secrets (DM's) and signature verification (ADVERT's)

This dual use makes the system elegant: the same identity that makes a node unique on the network is simultaneously the key to secure communication — all without ever involving a server, a provider, or a certificate authority.

## Hardware crypto on nRF52

Everything above describes *what* happens computationally. Since v1.17.1,
what changed on nRF52 boards is *who* does it: not the processor, but the
CryptoCell CC310, a separate unit inside the same chip. The same operations,
the same results, no protocol change — two nodes notice nothing of the
difference between them. The consequence sits in the device, not in the
network.

### The flag belongs to the family, not to a board

`USE_CC310_HW_CRYPTO` is not a board property. The flag sits in
`[nrf52_base]` (r.81) in the `platformio.ini` at the repository root, the
section every nRF52 variant file inherits from:

`platformio.ini` r.90-94

```text
build_flags = ${arduino_base.build_flags}
  -D NRF52_PLATFORM
  -D LFS_NO_ASSERT=1
  -D EXTRAFS=1
  -D USE_CC310_HW_CRYPTO=1
```

So there is no nRF52 build without hardware crypto — this holds for **every**
nRF52 build, not for a single board. ESP32, RP2040 and STM32 do not have the
flag and follow the software path everywhere. Which variant runs on which
family is in [MeshCore Platforms](../platform/platforms.md).

The unit is switched on in `NRF52Board::begin()`, at
`src/helpers/NRF52Board.cpp` r.29, and shut down again when the peripherals
are powered off before deep sleep, at r.364. Outside those two places there
is nothing to configure.

### Six operations move

Each of the six sits in the source as an `#ifdef USE_CC310_HW_CRYPTO` with
the software path in the `#else` branch. Both branches therefore stay in the
repository; which one is compiled in depends on the flag alone.

| Operation | Function | Software path | Hardware path | Location |
|---|---|---|---|---|
| SHA-256 over one block | `Utils::sha256` | `SHA256` from the Crypto library | `CRYS_HASH` | `src/Utils.cpp` r.24 |
| SHA-256 over two fragments | `Utils::sha256` (overload) | same, with `update()` per fragment | `CRYS_HASH_Init` / `_Update` / `_Finish` | `src/Utils.cpp` r.36 |
| AES-ECB decryption | `Utils::decrypt` | `AES128` | `SaSi_Aes*` | `src/Utils.cpp` r.53 |
| AES-ECB encryption | `Utils::encrypt` | `AES128` | `SaSi_Aes*` | `src/Utils.cpp` r.85 |
| Signature verification | `Identity::verify` | `Ed25519::verify` | `CRYS_ECEDW_Verify` | `src/Identity.cpp` r.22 |
| Random numbers | `RadioNoiseListener::random` | radio noise | `nRFCrypto.Random`, combined with radio noise | `src/helpers/radiolib/RadioLibWrappers.h` r.93 |

The first four and the sixth are a swap of library: same input, same output, a
different performer. The fifth is the only one where the firmware itself
explains why.

### The signature check, written out

An ADVERT comes in, the node has to verify the Ed25519 signature, and that
happens in the radio's receive path. The reason for the hardware path is in
the source code itself:

`src/Identity.cpp` r.22-33

```cpp
bool Identity::verify(const uint8_t* sig, const uint8_t* message, int msg_len) const {
#ifdef USE_CC310_HW_CRYPTO
  // nRF52840 CryptoCell CC310 hardware Ed25519 verification. The software
  // implementations need ~3KB of stack (which can overflow the Adafruit core's
  // 4KB loop task stack from the advert receive path); the hardware path
  // needs much less, around 600-700bytes. The CC310 workspace is static, faster,
  // should save power at scale as well.
  static CRYS_ECEDW_TempBuff_t cc310_tmp;
  CRYSError_t rc = CRYS_ECEDW_Verify((uint8_t*)sig, CRYS_ECEDW_SIGNATURE_BYTES,
                                     (uint8_t*)pub_key, CRYS_ECEDW_MOD_SIZE_IN_BYTES,
                                     (uint8_t*)message, (size_t)msg_len, &cc310_tmp);
  return rc == CRYS_OK;
```

The software verification takes up around 3 kB of stack. The Adafruit core's
loop task has 4 kB, and the verification is called from the advert receive
path — so from a call chain that already uses stack itself. That can overflow.
The hardware path requires 600 to 700 bytes and puts its working memory down
statically as well, outside the stack.

So this is not a speed-up that was gone looking for. It is a stack problem
being solved; the comment mentions the gain in speed and the lower current
draw second and third.

### The random generator does not replace the radio noise

In the five operations above the hardware takes the work over. In the sixth
something is added. `RadioNoiseListener` draws its entropy from the noise on
the radio input; with the CC310 present that noise is not replaced but XORed
with the hardware output:

`src/helpers/radiolib/RadioLibWrappers.h` r.93-103

```cpp
  void random(uint8_t* dest, size_t sz) override {
#ifdef USE_CC310_HW_CRYPTO
    nRFCrypto.Random.generate(dest, (uint16_t)sz);
    for (int i = 0; i < sz; i++) {
      dest[i] ^= _radio->randomByte() ^ (::random(0, 256) & 0xFF); // combine with Radio's entropy
    }
#else
    for (int i = 0; i < sz; i++) {
      dest[i] = _radio->randomByte() ^ (::random(0, 256) & 0xFF);
    }
#endif
```

Note the difference between the two branches: `^=` against `=`. In the
software branch the radio noise is the only source; in the hardware branch the
CC310 fills the buffer and that same radio noise is then mixed in. Two
independent sources combined is no weaker than the stronger of the two, and
the comment at `src/helpers/NRF52Board.cpp` r.30 says why the CC310 was
brought in: its output does not depend on the environment, and radio noise
does.

This is the only one of the six where the hardware adds something to the
result instead of computing it a different way. Where the keypair made with it
comes from is above, under
[The Ed25519 Keypair](#the-ed25519-keypair-your-identity-on-the-mesh).

## Sources

Firmware, commit `d929643` (v1.17.1, 14 August 2026) — for the section
*Hardware crypto on nRF52*:

- [`platformio.ini`](https://github.com/meshcore-dev/MeshCore/blob/d929643/platformio.ini)
  — `USE_CC310_HW_CRYPTO` in `[nrf52_base]`
- [`src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/Utils.cpp)
  — hash and AES, both branches
- [`src/Identity.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/Identity.cpp)
  — the signature check and the stack reasoning
- [`src/helpers/NRF52Board.cpp`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/NRF52Board.cpp)
  — starting and shutting down the unit
- [`src/helpers/radiolib/RadioLibWrappers.h`](https://github.com/meshcore-dev/MeshCore/blob/d929643/src/helpers/radiolib/RadioLibWrappers.h)
  — the random generator

Related in this documentation:

- [Crypto: rweather and ed25519](../libraries/core/crypto.md) — the libraries
  behind the software path
- [Platform realisation](../design/technical/platform-realisation.md) — what
  the nRF52 family does differently elsewhere
- [MeshCore Packet Structure](packet-structure.md) — where the signature sits
  in the packet

Translated from Dutch by Anthropic Claude
