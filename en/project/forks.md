# Forks & variants

*FORKS · REPEATER POLICY · COMPANION · MEASUREMENT METHOD*

More than a thousand forks of `meshcore-dev/MeshCore` exist. The vast majority
contain no work of their own. This page describes the twelve forks in which
development does happen: what each one adds functionally, and how far it stands
from upstream on the reference date. Where
[GitHub Repositories](github.md) catalogues what exists, this page describes what
the forks do differently.

> [!NOTE]
> **Source.** The figures on this page were measured directly, not taken from
> READMEs or third-party summaries. The fork list was retrieved through the
> GitHub API and sorted by stars; 300 forks were examined out of the roughly
> 1300 the API reports — the tail that was not retrieved has zero stars by
> definition. For each highlighted fork the active branch was fetched locally
> and compared against upstream `dev` with `git merge-base` and `git rev-list`.
> The functional descriptions come from the fork's documentation, and where that
> was missing or unclear, from its source code. No commit hash of upstream `dev`
> was recorded during the measurement; the comparison holds for the state of
> 19 September 2026. None of this firmware was tested on hardware, so this page
> makes no claims about stability or real-world performance and expresses no
> preference for any fork.

The measurement can be repeated with three commands, where `up` is the remote
pointing at `meshcore-dev/MeshCore`:

```bash
git merge-base up/dev <fork-branch>          # common starting point
git rev-list --count <base>..<fork-branch>   # own commits
git rev-list --count <base>..up/dev          # commits behind
```

## What the fork landscape looks like

Of the 300 forks examined:

| Characteristic | Count |
|---|---|
| Zero stars | 167 |
| Wrote their own description | 39 |
| Repository renamed | 49 |
| Untouched for more than six months | 72 |

The rough conclusion from those four rows: over 80% of the forks examined
contain no work of their own. Someone forks to add one board, change one line or
keep a copy of the code. The figure of 1300 therefore says little about how many
variants actually matter.

## State per fork on the reference date

**Reference date: 19 September 2026.** This table is a snapshot and ages daily;
the rest of the page does not. *Own* is the number of commits the fork is ahead
of the common starting point with upstream `dev`, *behind* the number upstream
has added since.

| Fork | Active branch | Own | Behind | Last commit |
| --- | --- | ---: | ---: | --- |
| jhuebert | `repeater-filter` | 46 | 4 | 17-09 |
| weebl2000 | `dev_plus` | 276 | 14 | 15-09 |
| l5yth (meshcore-linux) | `linux` | 16 | 56 | 30-08 |
| Dutch-MeshCore | `dmc-dev` | 39 | 29 | 14-09 |
| MichTronics (MeshCoreNG) | `main` | 265 | 122 | 10-09 |
| ksanislo (LVGL) | `main` | 294 | 122 | 15-08 |
| tek126 (mtbeacon) | `meshtastic-beacon` | 28 | 122 | 29-08 |
| MarekZegare4 (Solo) | `main` | 709 | 122 | 08-09 |
| jooray (BitChat) | `feature/bitchat-bridge` | 27 | 169 | 10-08 |
| Meshcore-Portugal (lusofw) | `main` | 122 | 481 | 01-07 |
| TogeriX-hub (FieldMesh) | `main` | 55 | 760 | 28-04 |
| mattzzw (Evo) | `meshcore-evo` | 27 | 1337 | 17-01 |

The *behind* column is the most useful figure in the table. Above a hundred you
miss the recent corrections from upstream; above five hundred the fork is
effectively a dead end, however many stars it has.

## What the forks add

The order below runs from much to little added functionality for a Dutch
repeater, not from new to old.

### jhuebert — repeater filtering on channel identity

[jhuebert/MeshCore](https://github.com/jhuebert/MeshCore), branch
`repeater-filter`.

**Strong point: filter rules that match on the actual channel identity, in a
fork that stays almost level with upstream.**

A single rule can combine packet type, route type (flood or direct), region, hop
range, payload length, Signal-to-Noise Ratio (SNR) range, path hash size and
channel, with pass, drop or log-only as the action. First match wins.

Channel filtering works in two ways. The coarse way is the 1-byte air hash —
marked in the code itself as collision-prone. The main route is to register a
channel with its actual Pre-Shared Key (PSK): the repeater decrypts the group
message and matches on the real channel identity, and optionally on sender name
or on the message text through a compact regular-expression engine of its own.

Further:

- **Rate limiting of flood adverts per node**, with a window of up to thirty
  days.
- **Below a configurable battery voltage the repeater stops forwarding**, but
  remains reachable and keeps advertising; it recovers automatically, with
  debounce and hysteresis. Intended for solar and off-grid sites.
- **Remote administration over the mesh** by an authenticated administrator,
  alongside the ordinary serial [CLI](../cli/introduction.md).
- **Weekly automatic synchronisation with upstream** through an automated
  workflow, plus two release channels: a dev channel based on `dev` and a stable
  channel based on upstream releases.

That automatic synchronisation turns out to be more valuable than the filter
itself: it is the reason this fork has the smallest gap of the twelve while the
rest drifts away.

**Point of attention.** Filtering on sender or text requires the PSK to be
present in the repeater and the repeater to read along. For a spammer on a
public channel that is defensible; for emergency communication it turns a relay
into a body that decides on content. A badly written regular expression makes a
call for help disappear silently. On top of that, the expression runs per packet
on text supplied by the sender — the code parses visibly defensively, but it
remains an attack surface the other forks do not have.

### Dutch-MeshCore — explicit rules and a correct duty cycle

[Dutch-MeshCore/MeshCore](https://github.com/Dutch-MeshCore/MeshCore), branch
`dmc-dev`. Here `main` mirrors upstream; the work is on `dmc-dev`.

**Strong point: the automatic derivation of the duty cycle, and a filter whose
discards you can see.**

**Duty cycle on `auto`.** Since v1.15 upstream has had a configurable limit with
50% as the default. This fork makes `auto` the default: the limit follows the
sub-band the node is tuned to, and is determined again as soon as `set freq` or
`set radio` changes that frequency.

| Sub-band (MHz) | Limit |
|---|---|
| 863.0 – 865.0 | 0.1% |
| 865.0 – 868.0 | 1% |
| 868.0 – 868.6 | 1% |
| 868.7 – 869.2 | 0.1% |
| 869.4 – 869.65 | 10% |

Outside 863–870 MHz, `auto` means no limit. This is the fork's most important
change; the recommendation to bring it back to upstream is at the bottom of this
page. The Dutch rules it connects to are in
[Regulations & Duty Cycle](../usage/regulations.md).

**Packet filter.** Off by default. Directly routed traffic and priority traffic
from known contacts in the Access Control List (ACL) always pass; only flood
traffic is filtered. Five mechanisms:

- **Hop limit per packet type**, for each of the twelve types separately.
- **Rate limit per type**, optionally with a gradual taper: pass everything up to
  a lower bound, then a linearly decreasing forwarding probability, closed at the
  hard limit. That prevents an abrupt limit from dragging legitimate traffic
  along at the moment a spammer fills the counter.
- **Channel blocking**, up to sixteen names.
- **Minimum path hash length** — the documentation itself warns that a minimum of
  2 removes almost all flood traffic, not just the abuse.
- **Checking for malformed group messages.**

More important than the filters themselves: `filter stats <subject>` reports per
reason how much was discarded, so you can see whether a rule does anything before
you tighten it.

Channel blocking has a limitation. Matching happens on one byte derived from the
channel name. Roughly one in 256 other channels therefore shares that value and
is blocked unintentionally. Channels with a random PSK of their own cannot be
entered, because the hash cannot then be reconstructed from the name. Only group
texts are affected, and there is no white list — only a black list.

**Closing regions temporarily at a high duty cycle.** Off unless enabled. If the
node's own TX duty cycle rises above the threshold (70% by default), the repeater
closes regions from the outside in: first the wildcard, then the broadest named
regions. The innermost layer and the home region always stay open. Below the
threshold minus hysteresis (60% by default) they open again from the inside out,
with a small random delay per step so that neighbouring repeaters do not recover
in lockstep. The region hierarchy this builds on is described in
[Regions and Scopes](../technical/regions-and-scopes.md).

The closing is explicitly temporary: it is never written to the region
configuration, so that a `region save` or a restart in the middle of a peak
cannot leave a permanent block behind. Order per packet: the region step first,
then the packet filter.

### MeshCoreNG (MichTronics) — measuring and damping automatically

[MichTronics/MeshCoreNG](https://github.com/MichTronics/MeshCoreNG), branch
`main`.

**Strong point: it is the only fork that makes a repeater's behaviour in a busy
network measurable.**

Explicitly developed from the Netherlands, on the argument that a small, densely
populated country with the duty cycle limits of EU868 is exactly where problems
with a dense mesh show up first.

- **`get dense.stats`** shows received, forwarded and discarded adverts,
  duplicate flood packets, estimated RX/TX airtime, the number of channel-busy
  detections, and a density and congestion level. In RAM only; gone after a
  restart.
- **Forwarding fewer adverts as the hop count rises** — a base factor (0.308 by
  default) sets how strongly that happens. 0 forwards nothing, 1 forwards
  everything as before.
- **`flood.relay.prob` 0–255** — the probability with which flood traffic is
  forwarded, half of it for instance.
- **Channel-busy detection through hardware Channel Activity Detection (CAD)**
  before transmitting.
- **Keeping neighbouring repeaters out of phase** — on top of the existing random
  `txdelay`, a small fixed offset derived from the node identity, stable across
  restarts, so that repeaters do not start transmitting simultaneously.
- **Suppression on hearing duplicates** — if a repeater hears enough others
  forward the same packet before its own timer expires, it cancels its own
  retransmission.
- **Battery monitoring at startup and during operation** — below a set voltage
  the node sleeps and tries again later, instead of switching on radio, GPS and
  display and draining the battery further.
- **Dutch region lookup table** — 2484 places across twelve provinces, generated
  from the MeshWiki list and stored as a table in flash, with a `regiondb`
  command. Explicitly a lookup table *beside* the editable region map, not inside
  it. See [Regions: intent and practice](../technical/regions-in-practice.md).

An announced dynamic mode is present but does nothing in this version; the
authors want to gather data from real networks before the firmware makes
decisions itself.

### weebl2000 — the hardened dev branch

[weebl2000/meshcore](https://github.com/weebl2000/meshcore), branch `dev_plus`.

**Strong point: correctness and safety, in the best-maintained of the heavy
forks.**

No new features to boast about, but the things that go wrong quietly:

- Constant-time comparison when verifying the Message Authentication Code (MAC),
  instead of an ordinary memory comparison.
- Bounds checks repaired when processing PATH and TRACE payloads.
- Errors around millisecond counter overflow resolved; time now survives a warm
  reset on nRF52.
- Watchdog added, and protection against faulty crystals at startup.

Functionally added: duty cycle enforcement through a token bucket, dynamic CAD
sensitivity, a coding rate that adapts to the measured SNR on retransmission, and
a series of new boards (RAK11200/13300, ThinkNode M4, T-Beam Supreme S3).

This is the only fork that touches the routing core itself substantially.

### meshcore-linux (l5yth) — native on the Raspberry Pi

[l5yth/meshcore-linux](https://github.com/l5yth/meshcore-linux), branch `linux`.

**Strong point: no microcontroller needed any more, and small enough to keep up
to date.**

Runs the same firmware code natively on a Raspberry Pi with an SX1262 on the SPI
bus, through an Arduino API layer for Linux. Yields a `meshcored` daemon. Tested
on Pi Zero up to Pi 5. With a small number of own commits this is a fork that can
be kept current without much effort.

### Solo (MarekZegare4) — the node as a standalone device

[MarekZegare4/MeshCore-Solo](https://github.com/MarekZegare4/MeshCore-Solo),
branch `main`.

**Strong point: fully usable without a phone.**

Reading and typing messages on the display; setting waypoints and navigating
back; a compass derived from course over ground, so without a magnetometer; track
recording with export to a GPX file; sharing locations and broadcasting live
position; a geofence with an alarm on arrival or departure, with a buzzer that
beeps faster as you get closer; clock with alarm, timer and stopwatch; screen
lock; sensor screens; and keyboard layouts for ten languages. Works with external
CardKB keypads.

### FieldMesh (TogeriX-hub) — outdoor use

[TogeriX-hub/FieldMesh](https://github.com/TogeriX-hub/FieldMesh), branch `main`.

**Strong point: corrects the frequency settings of Client Repeat.**

The author states that the upstream defaults for Client Repeat were unusable or
illegal: 433 MHz a single illegal point frequency, 869 MHz in a sub-band with
0.1% duty cycle, and 915 MHz outside the band in some regions. FieldMesh puts
legal values in their place and offers a one-button Off-Grid mode on
869.4625 MHz that preserves the normal parameters so you can return. What Client
Repeat itself does is described in
[Off-Grid Client Repeat Mode](../usage/off-grid.md).

Further: automatic GPS advert every five minutes, zero-hop by default so the
wider network does not suffer; a separate page with positions and distances of
favourite contacts; message history on the device; and an SOS button with buzzer.

This fork is far behind upstream — see the table above. The ideas are more
interesting than the code.

### lusofw (Meshcore-Portugal) — distribution, not a fork

[Meshcore-Portugal/lusofw](https://github.com/Meshcore-Portugal/lusofw), branch
`main`.

**Strong point: explicitly positioned as a release and test channel, not as a
hard fork.**

433 MHz by default, bridge off by default, time synchronisation based on advert
data, duty cycle through a token bucket, a probability mechanism that limits
advert forwarding, and adverts forwarded only in a maintenance window between
02:00 and 07:00. Neighbours older than 48 hours drop out automatically. Its own
region `#portugal`, set to flood by default.

### mtbeacon (tek126) — visible on Meshtastic

[tek126/MeshCore-mtbeacon](https://github.com/tek126/MeshCore-mtbeacon), branch
`meshtastic-beacon`.

**Strong point: narrowly scoped and well documented.**

Lets a MeshCore repeater announce itself periodically on a Meshtastic network, so
that Meshtastic users see a line of text appear. The README explains clearly why
that requires work: the two use a different sync word (`0x12` against `0x2B`),
different bandwidth and spreading factor, and different framing — the radios
simply do not hear each other. For one packet the repeater therefore presents
itself as a Meshtastic transmitter.

### BitChat (jooray) — a bridge to another protocol

[jooray/MeshCore-BitChat](https://github.com/jooray/MeshCore-BitChat), branch
`feature/bitchat-bridge`.

**Strong point: the idea.**

A bridge device that passes messages between BitChat users and MeshCore. Because
the Bluetooth connection is occupied for that purpose, you configure such a node
over USB serial.

**Point of attention on quality.** Of the roughly 45,000 added lines, about half
are build log files committed by accident in a `tmp` directory.

### LVGL (ksanislo) — a second graphical companion

[ksanislo/MeshCore-LVGL](https://github.com/ksanislo/MeshCore-LVGL), branch
`main`.

**Strong point: the release infrastructure around it.**

No new network features, but a complete second companion with a graphical
interface. The wrapper is more interesting: Over-The-Air (OTA) updates over WiFi,
core dumps to SD card with the matching debug symbols kept so that crashes remain
readable afterwards, and its own notification sounds without licence
restrictions.

### Evo (mattzzw) — a warning

[mattzzw/MeshCore-Evo](https://github.com/mattzzw/MeshCore-Evo), branch
`meshcore-evo`.

A well-known name in this list, but the active branch has the largest gap of the
twelve and has not been touched for months — see the table above. The reputation
runs far ahead of reality. Included for that reason, not for its content.

## What follows from this

**The routing core is uncontested.** Almost all added functionality sits in three
corners: companion interface, repeater policy, and new boards or platforms. Only
weebl2000 touches the core substantially, and then mostly to repair it. That is
in effect a compliment to upstream — the protocol itself is not what people
disagree about.

**A lot is built twice.** At least four independent companion interfaces and two
independently written packet filters. The loss in this ecosystem is not in the
forking but in building the same thing three times.

**Two philosophies for the same problem.** MeshCoreNG measures and damps
continuously and automatically; Dutch-MeshCore lets the administrator set
explicit rules and only intervenes automatically during a peak; jhuebert offers
the most detailed rules but asks for access to the message content in return. For
emergency communication the second approach makes the strongest case, because you
have to be able to explain afterwards why a packet did not get through.

**Forking requires permanent merge work.** Whoever forks has to keep merging
every upstream change themselves. Of the twelve forks discussed, three genuinely
keep pace, and the only one that has solved this structurally — jhuebert, with
weekly automatic synchronisation — owes that to automation, not to discipline.

## One recommendation for upstream

Of everything on this page there is one change that belongs in the original
repository without discussion: the **automatic derivation of the duty cycle from
the frequency** from Dutch-MeshCore.

The default frequency in the upstream configuration is 869.618 MHz, which falls
in the sub-band with a 10% duty cycle. The default setting is 50%, or airtime
factor 1.0 — five times the permitted transmission time. This is moreover an SRD
band, so an amateur licence does not help here; that applies to the amateur
bands. Upstream says as much itself for the deprecated `af` parameter: the user
is responsible for a value that suits their jurisdiction. The Dutch side of this
is in [Regulations & Duty Cycle](../usage/regulations.md), the commands in
[Routing](../cli/routing.md).

The nuance that goes with it: it is a ceiling, not a target. A normal repeater
does not come near 50%, so in daily practice nothing happens. But the setting is
silently permissive at exactly the moment things get busy — and that is the
moment it was meant to work.

The solution breaks nothing in the protocol, affects no client, and is purely a
matter of correctness.

## Sources

- [MeshCore firmware — `meshcore-dev/MeshCore`, branch `dev`](https://github.com/meshcore-dev/MeshCore/tree/dev)
  — the comparison point for every figure on this page.
- [MeshCore firmware — `src/helpers/CommonCLI.cpp`](https://github.com/meshcore-dev/MeshCore/blob/03b6ef4/src/helpers/CommonCLI.cpp)
  — `set dutycycle` and `set af`, commit `03b6ef4` (v1.16.0).
- The repositories of the twelve forks: the link is given with each fork above.
  Functional descriptions come from the documentation and source code of those
  repositories, as retrieved on 19 September 2026.

Translated from Dutch by Anthropic Claude
