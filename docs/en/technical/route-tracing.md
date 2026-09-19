# Route Tracing

*TECHNICAL · WHY A PATH IS NEVER 100% CERTAIN*

The messages page shows a map with the route a packet has travelled for each message. That display is an **approximation** — not an exact reconstruction. MeshCore does record which nodes forwarded a packet, but the combination of the routing protocol, packet structure, and RF conditions makes it impossible to say with 100% certainty which path a message followed. This page explains why.

⚠️ In short:
a MeshCore packet travels simultaneously via multiple routes. The receiver records only the route of the
first
copy that arrives. All other routes are invisible.

## 1 · Flood routing — first arrival wins

When a node sends a message to a contact for the first time — or when a previously learned path has expired — MeshCore uses `ROUTE_TYPE_FLOOD`.<sup>[[2]](#bron2)</sup> The packet is then sent to all reachable repeaters, which in turn forward it further. Each repeater appends its own hash to the path field of the packet and forwards it after a random delay.

The result is that the receiver receives *multiple copies* of the same packet — each via a different physical route. The firmware checks with `hasSeen()` whether the packet has already been processed.<sup>[[2]](#bron2)</sup> Only the **first** copy is processed; all subsequent copies are silently discarded. The path that is recorded is therefore exclusively the path of the fastest copy at that moment — determined by RF conditions and random backoff timers, not by a deterministic algorithm.

> [!NOTE]
> Consequence:
> there may be ten routes along which a packet reached the destination. Only one of them is visible in the hop data.

## 2 · Non-deterministic — staggered retransmission

To avoid collisions on the LoRa channel, MeshCore uses a staggered retransmission mechanism: repeaters wait a calculated time before forwarding a packet. The waiting time is inversely proportional to the received signal strength (SNR) — a repeater with a strong signal may transmit earlier than one with a weak signal.<sup>[[4]](#bron4)</sup>

In practice, this means the repeater with the best connection forwards the packet first and thereby wins the race. But RF conditions vary continuously due to atmospheric conditions, node movement, and interference. The same message, sent a minute later under slightly changed conditions, may follow a completely different path — even if the network topology is identical.

## 3 · Hash collisions with 1-byte paths

In the original MeshCore protocol, the first byte of a repeater's public key is used as an identifier in the path field. With one byte there are only 254 usable unique values (0x00 and 0xFF are reserved).<sup>[[3]](#bron3)</sup> In larger networks, multiple repeaters share the same first byte. The packet is correctly forwarded — the network functions normally — but analysis tools cannot determine with certainty which physical repeater the identifier represents.

| Hash size | Unique IDs | Collision risk with 100 nodes | From firmware |
|---|---|---|---|
| 1 byte | 254 | ~33% chance of ≥1 collision | all versions |
| 2 bytes | 65,534 | <0.08% | v1.14+ |
| 3 bytes | 16,777,214 | negligible | v1.14+ |

## 4 · Multibyte paths — collisions resolved, other problems not

From firmware version 1.14, repeaters can advertise with 1-, 2-, or 3-byte addresses, and companions can send messages with corresponding path sizes.<sup>[[3]](#bron3)</sup> With 3-byte hashes the probability of a collision in all practical networks is negligibly small.

However, multibyte only resolves the *collision problem*. The remaining sources of uncertainty — first-arrival flood, staggered retransmission, `removeSelfFromPath()`, and missing GPS data — remain fully in effect, regardless of hash size.

> [!NOTE]
> Conclusion:
> 2- and 3-byte paths make the hop data
> more reliable
> , but not
> complete
> . They do not solve the fundamental problem that only the first received route is visible.

## 5 · `removeSelfFromPath()` — the path is modified in transit

When a repeater forwards a directly-routed packet, the firmware calls `removeSelfFromPath()`.<sup>[[2]](#bron2)</sup> This method removes the forwarding repeater's hash from the path field, so that the next hop in the chain knows who still follows in the route.

This is technically necessary for correct operation of direct routing, but has the side effect that the path field in the received packet *no longer contains the complete original route* as built by the sender. Part of the route history has been removed in transit.

## 6 · Only one of multiple simultaneous copies is visible

With flood routing, every repeater that receives the packet forwards it — all routes the network knows are traversed simultaneously. The destination receives multiple copies via different physical paths. After the first copy is processed, all subsequent copies are silently dropped by `hasSeen()`.<sup>[[4]](#bron4)</sup>

There is no mechanism in the protocol to track how many alternative routes also carried the packet, or which routes those were. That information is permanently lost as soon as the first copy is processed.

## 7 · GPS data is optional and non-real-time

MeshCore nodes only advertise their position when the user manually initiates it, or at a configured interval. Repeaters send a flood-advert by default every 12 hours.<sup>[[3]](#bron3)</sup> The position data in the node database may therefore be outdated, incomplete, or entirely absent at the time a message is received.

Nodes without GPS coordinates cannot be placed geographically. Even nodes that have advertised coordinates may be mobile — their registered position need not match their location at the moment they forwarded the packet.

## Summary

**First-arrival flood**

- **Cause 1** — Only the fastest of multiple simultaneous routes is recorded.

**Staggered retransmission**

- **Cause 2** — Which repeater "wins" depends on the SNR at that moment — not deterministic.

**1-byte hash collisions**

- **Cause 3** — 254 unique IDs for potentially hundreds of nodes — same ID, different physical node.

**Multibyte incomplete**

- **Cause 4** — 2/3-byte solves collisions, but not the fundamental first-arrival problem.

**removeSelfFromPath()**

- **Cause 5** — Repeaters remove their own hash in transit — the complete original route is lost.

**Alternative routes invisible**

- **Cause 6** — All copies after the first are dropped without any logging of their routes.

**Missing or outdated GPS**

- **Cause 7** — Position data is opt-in and up to 12 hours old — geographic placement is an approximation.

**Approximation, not an exact route**

- **Conclusion** — The map display shows one snapshot of one route — not the complete propagation path.

## Sources

1. [1]LocalMesh NL — MeshCore routing algorithms:[localmesh.nl/en/meshcore-routing-algorithms/ ↗](https://www.localmesh.nl/en/meshcore-routing-algorithms/)
2. [2]DeepWiki — MeshCore source: Routing and Path Discovery (src/Mesh.cpp):[deepwiki.com/meshcore-dev/MeshCore/7.2-routing-and-path-discovery ↗](https://deepwiki.com/meshcore-dev/MeshCore/7.2-routing-and-path-discovery)
3. [3]GitHub — MeshCore FAQ (docs/faq.md):[github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md ↗](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md)
4. [4]Eastmesh Wiki — MeshCore routing internals:[wiki.eastmesh.au/meshcore/routing ↗](https://wiki.eastmesh.au/meshcore/routing)
5. [5]GitHub — MeshCore Packet.h (packet structure source):[github.com/meshcore-dev/MeshCore/blob/main/src/Packet.h ↗](https://github.com/meshcore-dev/MeshCore/blob/main/src/Packet.h)
6. [6]LocalMesh NL — MeshCore protocol explained:[localmesh.nl/en/meshcore-protocol-explained/ ↗](https://www.localmesh.nl/en/meshcore-protocol-explained/)
7. [7]NodakMesh — MeshCore explained: device roles & routing:[nodakmesh.org/blog/meshcore-how-it-works-guide ↗](https://nodakmesh.org/blog/meshcore-how-it-works-guide)

Translated from Dutch by Anthropic Claude
