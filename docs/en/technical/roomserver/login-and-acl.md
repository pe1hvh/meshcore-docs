# Logging In and the ACL

*ANON_REQ · THREE PASSWORD PATHS · PERMISSIONS · WHAT SURVIVES A RESTART*

A room server accepts nothing from a stranger. Before a client may post or
request anything, it has to identify itself with a password — and the
password it enters determines not *whether* it gets in, but *as what*. This
chapter follows that login packet from the first byte to the rights the
server attaches to it, and shows which part of that membership does not
survive a restart.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/simple_room_server/MyMesh.cpp`, `src/helpers/ClientACL.h`,
> `src/helpers/ClientACL.cpp`, `src/helpers/BaseChatMesh.cpp`,
> `src/helpers/CommonCLI.cpp`, and the official `docs/payloads.md` and
> `docs/cli_commands.md`. The `ROOM_PASSWORD` counts come from
> [`tools/room-server-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/room-server-overview.py).

## The login packet

Logging in uses `PAYLOAD_TYPE_ANON_REQ`: a datagram in which the sender
includes its full public key, because the server does not know it yet. The
plaintext inside that packet is different for a room server than for a
repeater or sensor — there is one extra field in it.

| Field | Size | Value in the example |
|---|---|---|
| timestamp | 4 | `C0 3C 6B 6A` (1785412800) |
| `sync_since` | 4 | `00 00 00 00` (logging in for the first time) |
| password | rest | `68 65 6C 6C 6F` (`hello`) |

The second field is the interesting one. `sync_since` is the timestamp of the
last post this client already holds; the server uses it as a starting point
and sends only what was posted after it. For a repeater or sensor that field
is absent and the password starts directly after the timestamp.

`src/helpers/BaseChatMesh.cpp` r.565-572

```cpp
    uint32_t now = getRTCClock()->getCurrentTimeUnique();
    memcpy(temp, &now, 4);   // mostly an extra blob to help make packet_hash unique
    if (recipient.type == ADV_TYPE_ROOM) {
      memcpy(&temp[4], &recipient.sync_since, 4);
      int len = strlen(password); if (len > 15) len = 15;  // max 15 chars currently
      memcpy(&temp[8], password, len);
      tlen = 8 + len;
    } else {
```

A password is therefore at most 15 characters. The client truncates longer
input without saying anything about it; set a longer password on the server
and you will no longer be able to log in to it.

## The three paths

The server runs through four tests, in a fixed order. The first is a short
circuit for anyone already known; the other three determine the rights of a
new client.

![Decision tree for logging in: blank password with a known public key, admin
password, guest password, read-only flag, and otherwise no reply](../../../images/en/room-server-login-1.svg)

`examples/simple_room_server/MyMesh.cpp` r.329-342

```cpp
    if (client == NULL) {
      uint8_t perm;
      if (strcmp((char *)&data[8], _prefs.password) == 0) { // check for valid admin password
        perm = PERM_ACL_ADMIN;
      } else {
        if (strcmp((char *)&data[8], _prefs.guest_password) == 0) {   // check the room/public password
          perm = PERM_ACL_READ_WRITE;
        } else if (_prefs.allow_read_only) {
          perm = PERM_ACL_GUEST;
        } else {
          MESH_DEBUG_PRINTLN("Incorrect room password");
          return; // no response. Client will timeout
        }
      }
```

That last `return` is the most striking behaviour in this chapter: on a wrong
password the server sends back **nothing**. No error message, no refusal, not
a single packet. The client keeps waiting until its own timeout expires and
then reports that the server is not responding. To the user, a typo in the
password is therefore indistinguishable from a server that is out of range.

> [!NOTE]
> **That is a deliberate choice, not a bug.** A server that answered "wrong
> password" would confirm to anyone who tried that there is a room server
> listening on that key, and would make guessing passwords cheap. Silence
> forces an attacker into a full timeout per attempt.

## What the passwords are

| Setting | CLI | Build flag | Default |
|---|---|---|---|
| administrator | `set password` | `ADMIN_PASSWORD` | `password` |
| participant | `set guest.password` | `ROOM_PASSWORD` | blank in the code, `hello` in the variants |
| read access without a password | `set allow.read.only` | — | `off` |

The default value of the participant password needs a note, because the
firmware and the variants say different things. In `CommonCLI.h`
`guest_password` is an empty field; the variants set it through a build flag.
Of the 79 variant directories, 59 lines set `ROOM_PASSWORD` to `hello`, and
in one variant (`gat562_mesh_watch13`) that line is commented out. A room
server you take off the flasher therefore almost certainly has `hello` as its
participant password and `password` as its administrator password.

> [!WARNING]
> **Both default passwords are public in the source code.** As long as you do
> not change them, anyone who knows them can read along *and* post, and with
> `password` also reconfigure your node and change your transmit power. Change
> them before the node goes on air.

## The permissions

`src/helpers/ClientACL.h` r.7-11

```cpp
#define PERM_ACL_ROLE_MASK     3   // lower 2 bits
#define PERM_ACL_GUEST         0
#define PERM_ACL_READ_ONLY     1
#define PERM_ACL_READ_WRITE    2
#define PERM_ACL_ADMIN         3
```

| Value | Role | May post | May CLI | May access list |
|---|---|---|---|---|
| 0 | `GUEST` | no | no | no |
| 1 | `READ_ONLY` | — | — | — |
| *2* | *`READ_WRITE`* | *yes* | *no* | *no* |
| 3 | `ADMIN` | yes | yes | yes |

The row for value 1 is empty because the room server never grants that role.
The read access that `allow.read.only` enables yields `PERM_ACL_GUEST` —
value 0, not 1. In the whole firmware `PERM_ACL_READ_ONLY` is used in exactly
one place, in `examples/simple_sensor/SensorMesh.cpp` r.189, and even there
only as a lower bound in a comparison. For a room server the role is
therefore a reserved number without behaviour.

Only the bottom two bits of `permissions` are the role; the top six are free
and are used by a sensor as a mask for which readings a client may see.

## The reply to a successful login

Thirteen bytes, three of which carry traces of an older protocol version.

`examples/simple_room_server/MyMesh.cpp` r.368-377

```cpp
    uint32_t now = getRTCClock()->getCurrentTimeUnique();
    memcpy(reply_data, &now, 4); // response packets always prefixed with timestamp
    // TODO: maybe reply with count of messages waiting to be synced for THIS client?
    reply_data[4] = RESP_SERVER_LOGIN_OK;
    reply_data[5] = 0; // Legacy: was recommended keep-alive interval (secs / 16)
    reply_data[6] = (client->isAdmin() ? 1 : (client->permissions == 0 ? 2 : 0));
    // LEGACY: reply_data[7] = getUnsyncedCount(client);
    reply_data[7] = client->permissions; // NEW
    getRNG()->random(&reply_data[8], 4);   // random blob to help packet-hash uniqueness
    reply_data[12] = FIRMWARE_VER_LEVEL;  // New field
```

| Byte | Contents |
|---|---|
| 0-3 | the server's timestamp |
| 4 | `RESP_SERVER_LOGIN_OK` (0) |
| 5 | always 0 — was the recommended keep-alive interval |
| 6 | 1 for an administrator, 2 for a guest, 0 for the rest |
| 7 | the permissions byte — was the number of waiting posts |
| 8-11 | four random bytes, so the packet hash is unique |
| 12 | `FIRMWARE_VER_LEVEL` (1) |

Byte 7 is the thing to watch for version differences. Until this change it
held the number of posts still waiting for this client; now it holds the
rights. An older client still reads that number as a counter and therefore
thinks three messages are waiting when it logs in as `ADMIN`. Where that
counter can now be found is covered in
[Requests and CLI](requests-and-cli.md).

## What survives a restart

The ACL is stored on the file system, but not in full. A filter is applied
when saving:

`examples/simple_room_server/MyMesh.cpp` r.942-944

```cpp
bool MyMesh::saveFilter(ClientInfo* client) {
  return client->isAdmin();    // only save Admins
}
```

Only administrators are written out. A participant with `READ_WRITE` no
longer exists for the server after a restart — including their `sync_since`,
their known path and their shared secret. They have to log in again, and
because their client *has* kept its own `sync_since`, it sends the right
value along and synchronisation simply continues afterwards. What has
disappeared are the posts themselves; see
[Posts and Synchronisation](posts-and-sync.md).

`ClientACL::applyPermissions()` also refuses to store a guest role
(`src/helpers/ClientACL.cpp` r.123), so a `setperm … 0` effectively removes a
contact from the file rather than saving it with rights 0.

The table has 20 slots by default (`MAX_CLIENTS` in
`src/helpers/ClientACL.h` r.37) and no variant sets that value differently.
What happens when the table is full is covered in
[Limits and Loose Ends](limits-and-todos.md).

## Protection against replay

Every client has a `last_timestamp`: the highest timestamp the server has
ever seen from it. A login packet with a timestamp that is not above it is
discarded with the message `possible replay attack!`
(`examples/simple_room_server/MyMesh.cpp` r.345-347). Replaying a recorded
login packet therefore gets you nowhere.

The flip side is that the client's clock matters. A client whose clock runs
far ahead sets `last_timestamp` to a value in the future; after that
everything it sends with the correct time is refused until real time has
caught up with that value. The official FAQ names exactly this as the cause
when a node appears to have been "last seen many, many days ago".

## Sources

- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `src/helpers/ClientACL.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.cpp)
- [MeshCore firmware — `src/helpers/BaseChatMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/BaseChatMesh.cpp)
- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
- [MeshCore firmware — `examples/simple_sensor/SensorMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_sensor/SensorMesh.cpp)
- [MeshCore firmware — `docs/payloads.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/payloads.md)
- [MeshCore firmware — `docs/cli_commands.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/cli_commands.md)

Translated from Dutch by Anthropic Claude
