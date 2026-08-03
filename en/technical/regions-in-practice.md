# Regions: intent and practice

*DESIGN INTENT · DUTCH PRACTICE · THE TRADE NOBODY MADE*

MeshCore's region mechanism is strikingly carefully designed. It deliberately
avoids a central registry, makes scopes unforgeable, and ensures no permanently
recognisable fingerprint travels over the air — all within two bytes.

Dutch practice has undone all three of those properties.

That is not a reproach to the people who built that practice. It solved a real
problem, and most alternatives were worse. But it is a trade, it is expensive,
and it has never been stated as one. This chapter sets out what the design buys,
what became of it, and what that costs.

For the mechanism itself — where the bytes sit and how a repeater decides — see
[Regions and Scopes](regions-and-scopes.md). For the convention itself see
[MeshWiki — Regio en scope](https://www.meshwiki.nl/wiki/Regio_en_scope). This
chapter is about the tension between the two.

> [!NOTE]
> **Source.** Verified against `MeshCore` v1.16.0 —
> `src/helpers/RegionMap.cpp`, `src/helpers/RegionMap.h`,
> `src/helpers/TransportKeyStore.cpp`. Municipality figures from Statistics
> Netherlands (CBS, as of 1 January 2026), UN/LOCODE release cadence from UNECE.

## What the design buys

The scope in a packet is not a region number but an HMAC over the payload, keyed
with the region key. That costs computation at every hop. Here is what it buys.

**No registry required.** The key follows from the name. Two people who
independently create `#hiking` end up in the same region, without anyone handing
out numbers. For a network that explicitly aims to work without infrastructure,
that is not a detail but the premise.

**No permanent collisions.** Had the code been a fixed hash of the name, 16 bits
would start colliding structurally within a few hundred regions:

| Regions worldwide | Chance of at least one permanently colliding pair |
|---|---|
| 100 | 7.3 % |
| 200 | 26.2 % |
| 342 | 58.9 % |
| 500 | 85.1 % |

Such a collision is unrepairable: two regions would forward each other's traffic
forever, and the only escape is renaming on every node that knows the region. The
HMAC design converts that systematic, permanent aliasing into an independent
1-in-65536 coincidence per packet. Comparable error rate, no lasting structure.
It is the most elegant property of the whole mechanism and it is rarely
mentioned.

**Unforgeable and unlinkable.** With a fixed number, anyone writes that value
into their packet and has the whole country flood it. And a fixed number is an
identifier: a passive listener can map which code belongs to which place, then
follow all traffic from that region. The HMAC prevents both — provided the key
is not guessable.

That last condition is where it comes apart.

## What the firmware does not know

The firmware has no concept of UN/LOCODE whatsoever. The key comes purely from
the name string:

```cpp
int RegionMap::getTransportKeysFor(const RegionEntry& src, TransportKey dest[], int max_num) {
  if (src.name[0] == '$') { ... }          // keystore region
  else if (src.name[0] == '#') {           // #hiking
    _store->getAutoKeyFor(src.id, src.name, dest[0]);
  } else {                                  // hiking -> becomes #hiking
    tmp[0] = '#'; strcpy(&tmp[1], src.name);
    _store->getAutoKeyFor(src.id, tmp, dest[0]);
  }
}
```

`src.parent` is never touched. No country code, no levels, no validation.
`#hiking` is a fully valid region name with the same 30 characters of room as
`#nl-ov-zwo`.

And the best counter-argument does not hold either. You might say the structured
name carries the hierarchy — but the hierarchy lives in a parent pointer set via
`region put <name> <parent>`, not in the name. In `findMatch()` the parent plays
no role at all; each region is tested individually against `region->flags`. The
tree determines how the `region` command prints the list and that children must
be removed first. For forwarding a packet it does nothing.

> [!IMPORTANT]
> You can name your regions `#netherlands` → `#overijssel` → `#zwolle`, or
> `#hiking`, and not a single byte of behaviour changes. The dashes in
> `nl-ov-zwo` are pure convention.

## What it became

In the Netherlands that convention has become a de-facto standard, with tools
that force you to configure regions via UN/LOCODE. That rebuilds precisely what
the protocol avoided: a central registry. Only now it is maintained by hand in a
table rather than by a server.

That in itself would still be defensible. The problem is what it does to the key
space.

The key of a `#` region is `SHA-256(name)`. The resilience of the entire scheme
therefore depends on how hard that name is to guess. And the convention makes the
candidate list not merely small but **public and complete**: the 342 Dutch
municipalities, plus twelve provinces and a country code. That list is published
in this very documentation project.

A listener who knows the convention computes a few hundred HMACs per captured
packet — trivial on a laptop — and thereby holds exactly the map the design set
out to prevent. Which regions are live, where they are live, and which traffic
belongs to which place.

**The outcome is that you perform the computation of a cryptographic scheme
and get the security of a readable label.**

With free-form names the picture is materially different. No list exists of
`#hiking`, `#teuns-walking-club` or `#deventer-christmas-market`, and then the
candidate space really is open.

## Where the convention comes from

The convention for regions and scopes lives at
[MeshWiki — Regio en scope](https://www.meshwiki.nl/wiki/Regio_en_scope), with the
complete code list at [Lijst van regio's](https://www.meshwiki.nl/wiki/Lijst_van_regio%27s)
and a parallel scheme at
[LocalMesh.nl](https://www.localmesh.nl/meshcore-regio-indeling/). It is four
layers deep:

| Layer | Standard | Example |
|---|---|---|
| Country | ISO 3166-1 | `nl` |
| Province | ISO 3166-2:NL | `nl-nb` |
| City | UN/LOCODE | `nl-nb-ein` (Eindhoven city) |
| Area | *no standard — locally invented* | `nl-ehv` (Eindhoven region) |

That last row is telling. `nl-ehv` appears in no standard. The same goes for the
disambiguation needed for provinces sharing a name with their capital, where
`nl-ut`, `nl-utc` and `nl-ut-utc` were placed side by side.

**So no standard is being followed; a registry is being maintained** — with its
own codes, its own exception rules and a published list. Precisely what the
protocol set out to avoid.

> [!NOTE]
> The wiki opens by stating that MeshCore uses a hierarchical region system based
> on international standards. That reads as a property of MeshCore, and it is not.
> The firmware knows nothing of ISO 3166 or UN/LOCODE; it knows only a name string
> that yields a key. The hierarchy in the wiki examples comes from
> `region put <name> <parent>` — a parent pointer that plays no role when matching
> a packet.

The page is otherwise sound: the per-repeater configuration examples are correct,
the warning to reboot after setting regions is right, and the advice to keep the
wildcard `*` enabled for now is exactly right. The criticism in this chapter is
not about that practice but about what the naming choice does to the properties of
the underlying mechanism — something never raised anywhere, because nobody had
reason to suspect the name matters cryptographically.

## The trade

The convention trades unlinkability for discoverability, and that is a real
trade with a real payoff.

For an emergency network, discoverability is not a side issue. Someone arriving
in Overijssel with a fresh node needs to know which region to configure without
first finding a Discord server and asking a human. A predictable name is then a
feature, not a leak. For NoodNet Overijssel the choice is well defensible.

What is missing is that it is ever stated as a choice. A private walking group
gains nothing from discoverability, and currently gives away for free the one
thing the cryptography had to offer it. That group should know that
`#teuns-walking-club` exists and suits it better.

## The gap the convention fills

There is a more charitable reading, and it is probably the correct one.

MeshCore has **no mechanism whatsoever for discovering regions**. There is no
"which regions do you carry?" question on air. `region list allowed` exists, but
that is the admin CLI of a node whose key you must already hold.

There is exactly one working discovery method: capture packets off the air, run
candidate names through the HMAC, and see which one reproduces the code. That
works only because the namespace is enumerable.

In other words: **the convention *is* the discovery mechanism.** The community
did not erect bureaucracy; it filled a missing protocol feature with the only
means available. That it costs the privacy property is not sloppiness but the
price of the gap.

## The downside

**A silent failure mode.** Configure a region no repeater in range carries, and
`findMatch()` returns `NULL`, `recv_pkt_region` stays empty,
`allowPacketForward()` returns `false`, and the packet disappears. No error, no
ack, nothing — flood traffic carries no feedback from repeaters. You are then
*worse off than with no scope at all*: unscoped traffic is still forwarded under
the wildcard, merely with a lower hop limit. A misconfigured scope silently
yields zero reach.

**A registry UN/LOCODE cannot provide.** The name list is stable: the number of
Dutch municipalities has stood at 342 since 2023, and UN/LOCODE has cut-off dates
of 31 March and 30 September. That is the easy part. What genuinely needs
maintaining and communicating is the *live state*: which repeater carries which
region, at what level people actually operate, which non-LOCODE regions are in
circulation. That changes every time someone touches a node — and follows from no
external standard.

**Computation.** Up to 32 regions × 4 keys = 128 HMAC-SHA256 computations over
50–190 bytes per flood packet, on an nRF52 or ESP32, before anything is decided.

**A persistent wrong mental model.** The term "region code", documentation
implying a lookup table, and tools enforcing a registry all point the same way:
that region codes are *issued*. Anyone believing that inevitably arrives at the
question of how a repeater knows which code to let through — a question with no
answer, because the premise is false.

## What the source code tells back

The source is the only place where the original design can still be read
honestly, and decoding it shows something other than what happens in practice.

The scheme is designed for `$` regions, with a key from the keystore that does not
follow from the name. There, unforgeability and unlinkability are real. Except
that `TransportKeyStore` is a stub in v1.16.0. `saveKeysFor()` contains
`// TODO: update hardware keystore` and returns `false`; `loadKeysFor()` has only
a RAM cache with `// TODO: retrieve from difficult-to-copy keystore`. The same
signals appear everywhere: `transport_code_2` reserved for the home region,
`REGION_DENY_DIRECT` marked `// reserved for future`, new regions defaulting to
*deny*.

**The code was not made complicated because it had to be, but because it was built
for a world that has not arrived.** What works today is exclusively the type whose
key follows from a guessable name.

And there the two diverge. The source assumes names nobody can guess. Practice
uses names anyone can look up. Both are internally consistent; together they are
not.

## A lookup table would have sufficed

This is the sharpest conclusion of this chapter, and it follows directly from the
above.

In defending the design above, I used the collision argument: a fixed hash of the
name would start colliding structurally within a few hundred regions, permanently
and unrepairably. That holds — **but only when codes are *derived* without
coordination.**

The moment a maintained, published list exists, you simply *assign* codes and
never hand out a duplicate. The collision problem disappears by definition. And
that list exists: it is exactly what MeshWiki and LocalMesh maintain.

So the principal argument for the HMAC scheme falls away precisely in the scenario
where the Netherlands uses it:

| | HMAC over the payload (today) | Assigned code from the registry |
|---|---|---|
| Registry required | no — yet there is one anyway | yes — and it already exists |
| Collisions | 1 in 65536 per packet, random | none, you assign them |
| Computation per packet | up to 128× HMAC-SHA256 | one comparison |
| Captures labellable | no | yes |
| Forgeable | in theory no, with a guessable name yes | yes |
| Trackable by a listener | yes, names are enumerable | yes |
| Silent failure mode | yes | yes |

On every row the outcome is equal or worse, except computation and
debuggability — and there the table wins.

The usual counter-argument is that a table in firmware requires a release for
every new region. That does not apply here: the codes are already typed in by
hand, from the same published list. `region put nl-nb` could just as well have
been `region put nl-nb 0x0042`, with the number taken from the wiki. The same
effort for the operator, no firmware update, and without the downsides
mentioned.

> [!IMPORTANT]
> **In the way the Netherlands uses regions, the HMAC scheme does nothing a simple
> lookup table would not also have done.** This costs computation, the
> registry is maintained, the names are enumerable, the codes are recomputable.
> What remains is the complexity.
>
> That is not an argument for changing the protocol — the scheme was not intended
> for this way of working. It is an argument for knowing what you are choosing:
> anyone using the published list is effectively using a lookup table, and should
> hold a lookup table's expectations of it.

## What would fix it

One protocol feature: a repeater that announces its regions. Then no central
table is needed, names can be free-form and unguessable, the silent failure mode
disappears, and the HMAC scheme keeps the properties it was built for.

Until then there is no good way out — only a choice:

| | Discoverable | Unlinkable |
|---|---|---|
| `#nl-ov-zwo` (convention) | ✔ strangers find you without asking | ✘ enumerable list, code trivially recomputed |
| `#teuns-walking-club` (free) | ✘ must be shared outside the mesh | ✔ no candidate list |
| `$private` (keystore) | ✘ key shared outside the mesh | ✔ genuinely — but not working in v1.16.0 |

## In practice

- **Emergency networks, public infrastructure, repeaters.** Use the LOCODE
  convention. Discoverability weighs more here, and that is a defensible choice.
- **Private group.** Use a free-form name and share it outside the mesh. You give
  up nothing you needed, and recover what the convention gives away.
- **Expect no confidentiality from a scope.** That role belongs to the channel
  PSK, and to it alone. A region saves airtime; nothing more.
- **Check that your scope lands somewhere.** No error will be reported. Test
  against a known repeater before assuming it works.

## Sources

- [MeshCore firmware — `src/helpers/RegionMap.cpp`](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/RegionMap.cpp)
- [MeshCore firmware — `src/helpers/TransportKeyStore.cpp`](https://github.com/meshcore-dev/MeshCore/blob/main/src/helpers/TransportKeyStore.cpp)
- [CBS — municipal divisions as of 1 January 2026](https://www.cbs.nl/nl-nl/onze-diensten/methoden/classificaties/overig/gemeentelijke-indelingen-per-jaar/indeling-per-jaar/gemeentelijke-indeling-op-1-januari-2026)
- [UNECE — UN/LOCODE](https://unece.org/trade/uncefact/unlocode)
- [MeshWiki — Regio en scope](https://www.meshwiki.nl/wiki/Regio_en_scope) — the convention
- [MeshWiki — Lijst van regio's](https://www.meshwiki.nl/wiki/Lijst_van_regio%27s) — the code list
- [LocalMesh.nl — MeshCore region layout](https://www.localmesh.nl/meshcore-regio-indeling/)
- [Regions and Scopes](regions-and-scopes.md) — the mechanism itself
