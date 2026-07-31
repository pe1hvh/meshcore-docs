# Remote Bediening

*COMMAND & CONTROL · GPIO · OFF-GRID*

MeshCore is niet alleen een chat-systeem. Het kan worden gebruikt als een volledig off-grid, versleuteld **command-and-control netwerk**.

## Elke node is meer dan een radio

Elke MeshCore-node is tegelijkertijd:

- **Een LoRa radio** — voor draadloze communicatie
- **Een router** — voor mesh-netwerkfuncties
- **Een computer (ESP32)** — met verwerkingskracht
- **I/O interfaces** — UART, GPIO, I2C, SPI, USB

## Wat kun je aansluiten?

- **Relais** — Schakelbare stroom voor apparaten op afstand.
- **Arduino / Raspberry Pi** — Complexere taken via UART of I2C aansturing.
- **Transceivers** — Aansturing via CAT-interface voor remote radio.
- **Sensoren** — Temperatuur, luchtvochtigheid, luchtdruk monitoring.
- **Motoren en rotors** — Antenne-richting aansturen op afstand.
- **Stroomschakelaars** — Remote on/off voor apparaten en installaties.

## Hoe werkt het?

> [!WARNING]
> **Wat het protocol wél en niet biedt.** In firmware v1.16.0 bestaat er geen
> service layer met aanroepen als `gpio.toggle`, `uart.send` of `i2c.read`, en
> geen COMMAND-pakkettype. Wat er wél is:
>
> - **CLI over de mesh** — een versleuteld tekstbericht met `txt_type` = CLI-commando (zie [MeshCore Pakketstructuur](packet-structure.md)). Een ingelogde admin stuurt zo elk CLI-commando naar een node op afstand.
> - **Requests** — `REQ` met sub-typen voor status, telemetrie, burentabel en toegangslijst.
> - **Sensoren** — `sensor get` / `sensor set`, en telemetrie in Cayenne LPP, mits sensorondersteuning meegecompileerd is.
> - **Eigen uitbreidingen** — `PAYLOAD_TYPE_RAW_CUSTOM` (`0x0F`) laat vrije bytes met eigen encryptie toe, en de firmware is zo gebouwd dat je er eigen afhandeling in kunt bouwen.
>
> De toepassingen hieronder zijn dus haalbaar, maar vragen eigen firmware of een
> aangesloten microcontroller die de CLI of een custom payload afhandelt. Ze
> vallen niet uit de standaardfirmware te configureren.

## Voorbeeld: Dakterras Remote Station

> [!NOTE]
> Node op het dak met GPIO-verbindingen naar antennerotator en transceiver. Node binnen via BLE naar telefoon. Commando: **Phone → BLE → binnennode → mesh → daknode → GPIO → rotor draait**. Geen wifi, geen internet, geen cloud.

## Waarom zo krachtig?

- Niet te jammen met een enkele zender (frequency hopping, mesh routing)
- Geen centraal punt dat kan falen
- Geen cloud of internet nodig
- Volledig versleuteld (AES)
- Tientallen kilometers bereik via mesh hops
