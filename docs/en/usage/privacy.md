# Privacy & Security

*ENCRYPTION · HAM VS ISM · VISIBILITY*

## What is always visible?

Every node must broadcast **beacons** for routing. Other nodes can see that a node exists and is active. This is necessary for the mesh network to function.

## What is NEVER visible (ISM mode)?

- Who you communicate with
- Which Rooms you are in
- The content of your messages
- Even the existence of your Rooms

> [!NOTE]
> **Encryption:** MeshCore uses AES-128, for channels as well as for direct messages. Direct Messages are end-to-end encrypted using public key cryptography.

## HAM vs ISM mode

| Aspect | ISM mode (868 MHz) | HAM mode (70 cm band) |
|---|---|---|
| Encryption | Fully encrypted | None (regulation) |
| Identification | Anonymous possible | Callsign required |
| Frequency | 868 MHz ISM band | 430–440 MHz |
| Licence | Not required | Amateur licence required |
| Power | 500 mW e.r.p. (H4) or 25 mW e.r.p. (H5) | Higher (per licence) |

Translated from Dutch by Anthropic Claude
