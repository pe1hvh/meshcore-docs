# Posts and Synchronisation

*CYCLIC QUEUE · SIGNED PLAIN · ACK HASH · SYNC_SINCE*

A room server pushes, it does not deliver on request. It keeps a single
timestamp per client — how far that client has got — and works through its
participants in a fixed rotation, one post per turn, each time waiting for a
delivery confirmation before the next one may go. This chapter follows a
message from the moment it arrives to the moment the recipient's counter
moves forward, and works out the bytes on the radio.

> [!NOTE]
> **Source.** This page has been verified against the firmware itself:
> `MeshCore` v1.16.0, commit `03b6ef4`, 28 July 2026 — files
> `examples/simple_room_server/MyMesh.h`,
> `examples/simple_room_server/MyMesh.cpp`, `src/Utils.cpp`,
> `src/helpers/TxtDataHelpers.h`, `src/helpers/BaseChatMesh.cpp`,
> `src/helpers/ClientACL.h`. The worked example can be reproduced with
> [`tools/room-server-overview.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/room-server-overview.py).

## From message to post

What a client sends is an ordinary text message: `PAYLOAD_TYPE_TXT_MSG` with
flags `TXT_TYPE_PLAIN`, exactly like a direct message. The server looks at
the sender's rights and decides what happens to it.

| Role of the sender | What the server does |
|---|---|
| `GUEST` (0) | nothing — no post, no reply, and no ACK either |
| `READ_WRITE` (2) | add the post and send an ACK |
| `ADMIN` (3) | add the post and send an ACK |

Here too, silence is the answer to a refusal. A guest who posts sees their
message stay marked as undelivered, without explanation.

`examples/simple_room_server/MyMesh.cpp` r.41-50

```cpp
void MyMesh::addPost(ClientInfo *client, const char *postData) {
  // TODO: suggested postData format: <title>/<descrption>
  posts[next_post_idx].author = client->id; // add to cyclic queue
  StrHelper::strncpy(posts[next_post_idx].text, postData, MAX_POST_TEXT_LEN);

  posts[next_post_idx].post_timestamp = getRTCClock()->getCurrentTimeUnique();
  next_post_idx = (next_post_idx + 1) % MAX_UNSYNCED_POSTS;

  next_push = futureMillis(PUSH_NOTIFY_DELAY_MILLIS);
  _num_posted++; // stats
}
```

Three things to hold on to. The post gets a timestamp from **the server's
clock**, not the sender's — which makes the ordering between posts reliable
even when clients have their time set wrong. The text is truncated at
`MAX_POST_TEXT_LEN`, which is `(160-9)` and therefore 151 characters. And
`next_post_idx` wraps around: post 33 overwrites post 1, whether or not it
has reached everyone by then.

`getCurrentTimeUnique()` also guarantees that two posts within the same
second still get different timestamps. That is necessary because the
timestamp doubles as a sequence number.

## The queue

32 slots (`MAX_UNSYNCED_POSTS`), an array in working memory, and nothing
else. Nothing is written to the file system anywhere: the only files a room
server touches are the ACL and the optional packet log.

![Cyclic queue with 32 slots, a sync_since timestamp per client, and the loop
of push, ACK, advance the timestamp](../../../images/en/room-server-sync-1.svg)

Against that queue stands a single timestamp per client: `sync_since`.
Anything with a higher timestamp is new to them, anything below it they have
already had. There is therefore no list of "who has what", only a boundary
per client — 4 bytes per participant instead of a matrix of 32 × 20 bits.

Selecting the next post uses three conditions at once:

`examples/simple_room_server/MyMesh.cpp` r.966-976

```cpp
      for (int k = 0, idx = next_post_idx; k < MAX_UNSYNCED_POSTS; k++) {
        auto p = &posts[idx];
        if (now >= p->post_timestamp + POST_SYNC_DELAY_SECS &&
            p->post_timestamp > client->extra.room.sync_since // is new post for this Client?
            && !p->author.matches(client->id)) {   // don't push posts to the author
          // push this post to Client, then wait for ACK
          pushPostToClient(client, *p);
          did_push = true;
          MESH_DEBUG_PRINTLN("loop - pushed to client %02X: %s", (uint32_t)client->id.pub_key[0], p->text);
          break;
        }
```

The loop starts at `next_post_idx` and not at 0, so at the oldest slot in the
ring — posts arrive in the order they were placed. The three conditions are:
the post is at least 6 seconds old (`POST_SYNC_DELAY_SECS`), the post is new
to this client, and **the author does not get their own post back**.

Why those six seconds are there, the firmware does not say — there is no
comment on the constant. The effect is that the server does not start pushing
while the ACK to the poster is still in flight, but that is an
interpretation, not a documented intention.

That last condition has a consequence that causes confusion in practice: you
do not see your own contribution come back from the server. Your client shows
it because it sent it itself, not because the room confirmed it. If your post
goes missing somewhere along the way, the only sign is the absent ACK.

## The packet the server sends

`examples/simple_room_server/MyMesh.cpp` r.53-68

```cpp
void MyMesh::pushPostToClient(ClientInfo *client, PostInfo &post) {
  int len = 0;
  memcpy(&reply_data[len], &post.post_timestamp, 4);
  len += 4; // this is a PAST timestamp... but should be accepted by client

  uint8_t attempt;
  getRNG()->random(&attempt, 1); // need this for re-tries, so packet hash (and ACK) will be different
  reply_data[len++] = (TXT_TYPE_SIGNED_PLAIN << 2) | (attempt & 3); // 'signed' plain text

  // encode prefix of post.author.pub_key
  memcpy(&reply_data[len], post.author.pub_key, 4);
  len += 4; // just first 4 bytes

  int text_len = strlen(post.text);
  memcpy(&reply_data[len], post.text, text_len);
  len += text_len;
```

The plaintext is therefore four fields:

| Field | Size | Meaning |
|---|---|---|
| `post_timestamp` | 4 | the post's timestamp, LSB first — a point in the past |
| flags | 1 | `TXT_TYPE_SIGNED_PLAIN` (2) in the top six bits, attempt number in the bottom two |
| author prefix | 4 | the first four bytes of the public key of whoever placed the post |
| text | rest | at most 151 characters |

The author field is why this type is called "signed plain". With an ordinary
direct message you know who the sender is because the packet comes from them;
here the packet comes from the server, and without this field every post
would look identical. Four bytes is enough to look the author up in your
contact list, and too little to serve as proof: it is an indication, not a
signature. Whoever administers the server can put in it whatever they like.

The bottom two bits of the flags byte are pure chance — `getRNG()` fills
them. They are there because a repeated attempt would otherwise be identical
byte for byte to the previous one, would get the same packet hash, and would
be discarded by the network as a duplicate.

## The expected ACK

The server works out in advance which confirmation it wants to see back:

`examples/simple_room_server/MyMesh.cpp` r.70-72

```cpp
  // calc expected ACK reply
  mesh::Utils::sha256((uint8_t *)&client->extra.room.pending_ack, 4, reply_data, len, client->id.pub_key, PUB_KEY_SIZE);
  client->extra.room.push_post_timestamp = post.post_timestamp;
```

That is SHA-256 over the plaintext followed by the recipient's public key,
truncated to four bytes (`src/Utils.cpp` r.23-28). On receipt the client
computes the same thing and sends the result back. Nothing is looked up and
nothing is transmitted: both sides reproduce the same value from data they
already hold. The same construction as the transport codes in
[Regions and Scopes](../regions-and-scopes.md).

### Worked out

With the project examples: `PE1RDP` posts
`"Op Woensdag a.s. Blauwvingerdagen"` at `1785412800`, and the server pushes
it to `PE1HVH`.

```text
post_timestamp   1785412800        C0 3C 6B 6A
flags            (2 << 2) | 0      08
author prefix    PE1RDP            E3 A0 31 3A
text             33 characters     4F 70 20 57 6F 65 6E 73 64 61 67 …

plaintext (42 bytes)
C0 3C 6B 6A 08 E3 A0 31 3A 4F 70 20 57 6F 65 6E 73 64 61 67 20 61 2E 73 2E
20 42 6C 61 75 77 76 69 6E 67 65 72 64 61 67 65 6E

expected ACK     88 C5 39 94   ->  0x9439C588
```

> [!NOTE]
> **The public keys are example values.** They follow the same convention as
> in `tools/dm-example.py`: `sha256("voorbeeld public key PE1HVH")`. A real
> key comes from the device and cannot be reproduced from public data.
> Everything after that — the construction of the plaintext and the ACK
> calculation — is exactly the firmware path.

Of the 151 available characters this example uses 33. The 42-byte payload
then goes through encryption and receives the ordinary packet headers; what
that looks like is covered in
[Packet Structure](../packet-structure.md).

## The counter only moves on the ACK

`examples/simple_room_server/MyMesh.cpp` r.104-115

```cpp
bool MyMesh::processAck(const uint8_t *data) {
  for (int i = 0; i < acl.getNumClients(); i++) {
    auto client = acl.getClientByIdx(i);
    if (client->extra.room.pending_ack && memcmp(data, &client->extra.room.pending_ack, 4) == 0) { // got an ACK from Client!
      client->extra.room.pending_ack = 0; // clear this, so next push can happen
      client->extra.room.push_failures = 0;
      client->extra.room.sync_since = client->extra.room.push_post_timestamp; // advance Client's SINCE timestamp, to sync next post
      return true;
    }
  }
  return false;
}
```

This is the core of the reliability. `sync_since` only goes up once the
confirmation is in. If the post is lost on the way, the counter stays put and
the same post is offered again. The server needs to track nothing extra for
that: the counter *is* the bookkeeping.

Note that the search runs over *all* clients and matches on the four bytes.
Two clients that happened to have the same expected ACK could claim each
other's confirmation. Because the client's public key is part of the hash,
that is only possible on a genuine 32-bit hash collision.

## Timing

| Constant | Value | What it governs |
|---|---|---|
| `PUSH_NOTIFY_DELAY_MILLIS` | 2000 ms | wait after a new post before the rotation runs again |
| `POST_SYNC_DELAY_SECS` | 6 s | minimum age of a post before it is pushed |
| `SYNC_PUSH_INTERVAL` | 1200 ms | between two pushed posts |
| `SYNC_PUSH_INTERVAL / 8` | 150 ms | on to the next client when there was nothing to push |
| `PUSH_ACK_TIMEOUT_FLOOD` | 12000 ms | wait for an ACK when the path is unknown |
| `PUSH_TIMEOUT_BASE` | 4000 ms | base wait with a known path |
| `PUSH_ACK_TIMEOUT_FACTOR` | 2000 ms | on top of that, per hop in the path |

The rotation is round robin: one client gets a turn per pass of the main
loop, and only that client. A participant with a large backlog therefore does
not hold the others up, but does not catch up quickly either — with twenty
active participants there is at worst some 24 seconds between two of your
turns; if most are up to date that drops to a few seconds, because an empty
turn costs only 150 ms.

Clients that are skipped are those still waiting for an ACK, those that have
never been active, and those with three failed attempts in a row. That last
threshold is hard: after `push_failures == 3` a client receives nothing more,
and the only way to recover is for it to send something itself. Every
message, every keep-alive and every request resets the counter to zero.

## What a client does with it

At the other end `BaseChatMesh` keeps the same counter, but more cautiously:

`src/helpers/BaseChatMesh.cpp` r.253-258

```cpp
    } else if (flags == TXT_TYPE_SIGNED_PLAIN) {
      if (timestamp > from.sync_since) {  // make sure 'sync_since' is up-to-date
        from.sync_since = timestamp;
      }
      from.lastmod = getRTCClock()->getCurrentTime(); // update last heard time
      onSignedMessageRecv(from, packet, timestamp, &data[5], (const char *) &data[9]);  // let UI know
```

The client advances its own `sync_since` as soon as it has processed the
post, and sends that value along at the next login and with every keep-alive.
That allows synchronisation to continue after the server has lost the client
— after a restart, for instance, where only administrators are retained (see
[Logging In and the ACL](login-and-acl.md)). The client then tells the server
again where it had got to.

What does *not* continue are the posts themselves. They were in RAM and are
gone after the restart; the counter then points at a boundary in an empty
queue.

## Sources

- [MeshCore firmware — `examples/simple_room_server/MyMesh.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.h)
- [MeshCore firmware — `examples/simple_room_server/MyMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/examples/simple_room_server/MyMesh.cpp)
- [MeshCore firmware — `src/Utils.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/Utils.cpp)
- [MeshCore firmware — `src/helpers/TxtDataHelpers.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/TxtDataHelpers.h)
- [MeshCore firmware — `src/helpers/BaseChatMesh.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/BaseChatMesh.cpp)
- [MeshCore firmware — `src/helpers/ClientACL.h`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/ClientACL.h)
- [MeshCore firmware — `docs/payloads.md`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/docs/payloads.md)

Translated from Dutch by Anthropic Claude
