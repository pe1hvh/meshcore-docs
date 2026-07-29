# Requests and CLI

*STATUS · KEEP-ALIVE · TELEMETRY · ACCESS LIST · ADMINISTRATION OVER RADIO*

Besides posting, a logged-in client can also *ask* the server something. Four
request types, each with its own threshold: some are open to anyone logged
in, one is reserved for the administrator, and one gives a different answer
depending on your rights. On top of that, an administrator can drive the
entire CLI over the radio — the same command set you get over USB.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/simple_room_server/MyMesh.cpp`,
> `examples/simple_repeater/MyMesh.cpp`,
> `examples/simple_sensor/SensorMesh.cpp`, `src/helpers/CommonCLI.cpp`,
> `src/helpers/ClientACL.cpp`, and the official `docs/cli_commands.md`,
> `docs/payloads.md` and `docs/faq.md`.

## The overview

![Request types from client to room server, with who may use each one](../../../images/en/room-server-requests-1.svg)

A request goes as `PAYLOAD_TYPE_REQ`: four bytes of timestamp, then one byte
of request type, then any parameters. The reply is a
`PAYLOAD_TYPE_RESPONSE` in which the server echoes the timestamp of the
question, so the client can tie question and answer together.

The numbering is not exclusive to the room server. `0x01`, `0x02` and `0x03`
also occur on the repeater, the sensor and the companion; `0x04`
(`REQ_TYPE_GET_AVG_MIN_MAX`) belongs to the sensor only, and `0x06` and
`0x07` (neighbours and owner information) to the repeater only. A room server
that receives `0x06` falls through to the end of `handleRequest()` and does
not answer.

## 0x01 — status

Returns a 52-byte block with the state of the node: battery voltage, noise
floor, last RSSI and SNR, counts of packets sent and received split by flood
and direct, total air time, uptime, duplicates, and two counters only a room
server has.

`examples/simple_room_server/MyMesh.cpp` r.24-39

```cpp
struct ServerStats {
  uint16_t batt_milli_volts;
  uint16_t curr_tx_queue_len;
  int16_t noise_floor;
  int16_t last_rssi;
  uint32_t n_packets_recv;
  uint32_t n_packets_sent;
  uint32_t total_air_time_secs;
  uint32_t total_up_time_secs;
  uint32_t n_sent_flood, n_sent_direct;
  uint32_t n_recv_flood, n_recv_direct;
  uint16_t err_events; // was 'n_full_events'
  int16_t last_snr;    // x 4
  uint16_t n_direct_dups, n_flood_dups;
  uint16_t n_posted, n_post_push;
};
```

`n_posted` counts how many posts have ever been placed, `n_post_push` how
many push attempts have been made. The difference between the two says
something about the health of the room: with two active participants
`n_post_push` should be roughly equal to `n_posted` (each post goes to one
other), with ten participants roughly nine times as high. If it runs much
higher still, posts are being repeated because the confirmations are not
arriving.

`last_snr` is stored multiplied by 4 in the field; the client has to divide
to get the real value.

## 0x02 — keep-alive

This is the only request the server answers **direct only**, so not while the
path is still unknown. A client sends it periodically to do three things at
once: signal that it is still there, adjust its `sync_since`, and hear how
much is waiting for it.

The reply is not a `RESPONSE` but an ACK with one byte appended:

`examples/simple_room_server/MyMesh.cpp` r.554-561

```cpp
          uint32_t ack_hash; // calc ACK to prove to sender that we got request
          mesh::Utils::sha256((uint8_t *)&ack_hash, 4, data, 9, client->id.pub_key, PUB_KEY_SIZE);

          auto reply = createAck(ack_hash);
          if (reply) {
            reply->payload[reply->payload_len++] = getUnsyncedCount(client); // NEW: add unsynced counter to end of ACK packet
            sendDirect(reply, client->out_path, client->out_path_len, SERVER_RESPONSE_DELAY);
          }
```

That extra byte is the counter that used to sit in the login reply (see
[Logging In and the ACL](login-and-acl.md)). It counts the posts that are
newer than `sync_since` and not from this client itself — so what is still in
the queue for them.

The client may optionally include four bytes in the request holding the
timestamp of the last post it has. If that value is greater than zero, the
server overwrites its own `sync_since` for this client with it. That is the
recovery path after a server restart: the client says where it had got to.

> [!NOTE]
> **That overwrite is not checked.** The server adopts the value without
> testing whether it moves forward or backward. A client can therefore also
> wind its counter back and receive posts again — as far as they are still in
> the queue.

## 0x03 — telemetry

Returns the node's readings in CayenneLPP format: at minimum the battery
voltage and, where the board supports it, the processor temperature. External
sensors are added if present.

The client sends a mask that determines which channels it wants to see. For a
guest that mask is ignored and set to `0x00`: they get the base values only,
whatever they ask for
(`examples/simple_room_server/MyMesh.cpp` r.170-172).

## 0x05 — access list

Administrators only, and the answer is narrower than the name suggests.

`examples/simple_room_server/MyMesh.cpp` r.185-195

```cpp
  if (payload[0] == REQ_TYPE_GET_ACCESS_LIST && sender->isAdmin()) {
    uint8_t res1 = payload[1];   // reserved for future  (extra query params)
    uint8_t res2 = payload[2];
    if (res1 == 0 && res2 == 0) {
      uint8_t ofs = 4;
      for (int i = 0; i < acl.getNumClients() && ofs + 7 <= sizeof(reply_data) - 4; i++) {
        auto c = acl.getClientByIdx(i);
        if (!c->isAdmin()) continue;  // skip non-Admin entries
        memcpy(&reply_data[ofs], c->id.pub_key, 6); ofs += 6;  // just 6-byte pub_key prefix
        reply_data[ofs++] = c->permissions;
      }
    }
```

Seven bytes per entry: six bytes of key prefix and one permissions byte. The
line `if (!c->isAdmin()) continue;` ensures that only administrators end up
in the list. Anyone hoping to see the participants of their room is out of
luck: **that list does not exist**, not even for an administrator. A room
server does know who is logged in — it needs their keys and their counters —
but it never surrenders that knowledge.

> [!WARNING]
> **This documentation used to claim otherwise.** Up to this revision the
> chapter [Communication](../../usage/communication.md) listed a member list
> as a property of a room server. That was incorrect and has been fixed.

A client that is not logged in as an administrator gets no error on `0x05`
but no answer at all: `handleRequest()` falls through to `return 0` and the
caller then sends nothing.

## The CLI over the radio

An administrator can send any CLI command to the server as a text message
with flags `TXT_TYPE_CLI_DATA` instead of `TXT_TYPE_PLAIN`. The answer comes
back as a text message with the same flags.

`examples/simple_room_server/MyMesh.cpp` r.452-464

```cpp
      if (flags == TXT_TYPE_CLI_DATA) {
        if (client->isAdmin()) {
          if (is_retry) {
            temp[5] = 0; // no reply
          } else {
            handleCommand(sender_timestamp, (char *)&data[5], (char *)&temp[5]);
            temp[4] = (TXT_TYPE_CLI_DATA << 2); // attempt and flags,  (NOTE: legacy was: TXT_TYPE_PLAIN)
          }
          send_ack = false;
        } else {
          temp[5] = 0;      // no reply
          send_ack = false; // and no ACK...  user shoudn't be sending these
        }
```

Two things stand out. There is **never** an ACK on a CLI command, not even
for an administrator: the answer itself is the confirmation. And a repeated
attempt is recognised and not carried out again — which prevents a `reboot`
being executed twice because the answer went missing, but it also means a
repeat gets you no answer at all.

A non-administrator who sends a command gets nothing back. No refusal, no
ACK.

### The room-specific commands

Most commands come from `CommonCLI` and are the same as on a repeater. Four
matter here:

| Command | What it does | Serial only |
|---|---|---|
| `set guest.password <text>` | the participant password | no |
| `set allow.read.only on\|off` | reading along without a valid password | no |
| `setperm <pubkey-hex> <number>` | set rights on a public key | no |
| `get acl` | dump the ACL to the console | **yes** |

`setperm` is all the administration there is. It takes a public key in hex —
a prefix is allowed, provided it is an even number of characters — and a
number with the new rights. Rights `0` removes the contact from the table
instead of saving it with role `GUEST` (`src/helpers/ClientACL.cpp`
r.123-128). There is no separate command to add somebody: a participant adds
themselves by logging in.

`get acl` explicitly checks for `sender_timestamp == 0`, which is only true
for input over the serial console. Over the radio this command does not
exist; it then falls through to ordinary CLI handling, which does not know
it.

### Remote administration from a client

What the firmware does is described above: any logged-in administrator can
send CLI commands. Whether *your* client offers that is another matter. The
official FAQ states that on a T-Deck you need a registration key to unlock
administration over RF, and that the Android and iOS apps have a wait timer
for administering repeaters and room servers that you can buy off. That is
therefore a restriction in the client software, not in the room server.

> [!NOTE]
> **This too used to read differently in this documentation.** The chapter
> [Node Types](../../usage/node-types.md) spoke of an "Ultra licence". That
> term appears neither in the firmware nor in the official documentation and
> has been replaced by what the FAQ describes.

## Sources

- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_repeater/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_repeater/MyMesh.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.cpp)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)
- [MeshCore firmware — `docs/payloads.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/payloads.md)
- [MeshCore firmware — `docs/faq.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/faq.md)

Translated from Dutch by Anthropic Claude
