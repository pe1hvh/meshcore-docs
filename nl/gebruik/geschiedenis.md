# Ontstaan en Geschiedenis

*VAN RADARTECHNIEK NAAR OFF-GRID MESH*

De technologische evolutie van radartechniek uit de Tweede Wereldoorlog naar moderne off-grid mesh-communicatie via LoRa en MeshCore.

## Chirp Spread Spectrum (jaren '40)

De wortels van MeshCore liggen in Chirp Spread Spectrum (CSS), een modulatietechniek ontwikkeld in de jaren '40 voor radarapplicaties. CSS verspreidt een signaal over een brede bandbreedte door de frequentie lineair te laten stijgen of dalen (chirps). Dit maakt het signaal robuust tegen multipath-fading, interferentie en jamming.  
  
**Multipath-fading** Een radiosignaal kan via meerdere paden de ontvanger bereiken: direct, maar ook via reflecties tegen gebouwen, bergen of andere objecten. Deze signalen komen op iets verschillende tijdstippen aan en kunnen elkaar versterken of uitdoven (fading). CSS is hier robuust tegen omdat de frequentie continu verandert - een reflectie die even later aankomt heeft een andere frequentie en interfereert daardoor niet destructief met het directe signaal.

**Interferentie** Andere radiobronnen op dezelfde of nabijgelegen frequenties kunnen je signaal verstoren. Denk aan WiFi, andere LoRa-zenders, of industriële apparatuur. CSS spreidt het signaal over een brede bandbreedte en een lange tijd. Een korte stoorzender raakt maar een klein deel van je chirp, en de FFT kan het symbool nog steeds reconstrueren uit de overige samples.

**Jamming** Opzettelijke verstoring door een zender die continu ruis of een sterk signaal uitzendt op jouw frequentie. CSS is moeilijk te jammen omdat:

- Je moet de hele 64 kHz (in NL) bandbreedte tegelijk verstoren (niet één frequentie)

- De processing gain zorgt dat je signaal nog steeds detecteerbaar is zolang de jammer niet extreem sterk is

- Verschillende spreading factors zijn orthogonaal, dus een jammer op SF7 stoort SF12 niet

**Orthogonaal** betekent in dit verband "onafhankelijk" of "niet-interfererend".  

## Tijdlijn
### LoRa: van idee naar chip (2009-2012)


In 2009 begonnen twee Franse ingenieurs, Nicolas Sornin en Olivier Seller, met de ontwikkeling van een long-range, low-power modulatietechniek gebaseerd op CSS. In 2010 voegde François Sforza zich bij hen en richtten ze samen Cycleo op in Frankrijk. In mei 2012 werd Cycleo overgenomen door Semtech Corporation, die de technologie commercialiseerde onder de merknaam LoRa (Long Range).

### Toegankelijke hardware (2016-2018)


De echte doorbraak voor hobbyisten kwam met de combinatie van Semtech's LoRa-chips (SX1276/SX1262) en Espressif's ESP32-microcontroller. Fabrikanten als Heltec en LILYGO brachten geïntegreerde development boards op de markt voor ~\$20-30.

### Meshtastic: de eerste mesh-golf (2019-2020)


In 2019 startte de Amerikaanse software-engineer Kevin Hester (GitHub: geeksville) het Meshtastic-project. Meshtastic gebruikt een flooding mesh-protocol waarbij elk apparaat berichten doorstuurt. Bij grote netwerken leidde dit tot congestie.

### MeshCore: intelligente routing (2024-2025)


Eind 2024 begon de Australische ontwikkelaar Scott Powell (Ripple Radios) aan een nieuw protocol. Begin 2025 lanceerde hij samen met Andy Kirby (UK) en Liam Cottle (NZ) het MeshCore-project met:

- Hybride routing: eerste contact via flood, daarna geleerde routes voor efficiëntie
- Rol-scheiding: Companion Radio's, Repeaters en Room Servers als aparte functies
- Schaalbaarheid: tot 64 hops, state-aware netwerk, AES-128 encryptie
- Lightweight C++: geen dynamische geheugenallocatie, embedded-first design

### Splitsing MeshCore Team (2026)


In april 2026 brak het MeshCore-ontwikkelteam. Oprichter Scott Powell (firmware), Liam Cottle (app), Recrof (map/flasher), FDLamotte (Python/STM32) en Oltaco (bootloader) vormen nu het "core team" op meshcore.io.  
  
Andy Kirby (UK) - voorheen verantwoordelijk voor branding, community en het meshcore.co.uk-domein - is afgesplitst nadat hij zonder overleg een handelsmerkaanvraag voor "MeshCore" indiende en grote delen van de ecosystem-tools met Claude Code had herschreven zonder dat kenbaar te maken.  
  
Andy zelf stelt dat de aanvraag puur ter bescherming van het merk was en dat de lancering van meshcore.io zonder zijn medeweten de eigenlijke breuk veroorzaakte.  
  
Hij zet zijn eigen werk nu voort als het aparte MeshOS-project op meshcore.co.uk, terwijl het core team de GitHub-repository (meshcore-dev/MeshCore) als enige bron van waarheid voor de firmware beschouwt (en IMO de meshcore community ook).





