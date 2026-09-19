# Pinbezetting — ESP32

*43 VARIANTEN · SIGNAALNAAM · GPIO · BRONREGEL*

Welke pin van de ESP32 waar aan vastzit, per variant in de firmware-repo.
Dit is een naslagpagina voor wie zelf bouwt, meet of een bord doorgrondt —
welk apparaat je kunt kopen staat in [Nodematrix](../node-matrix.md), en wat
er per familie in de chip zit in
[De vier platformfamilies](../platform-families.md).

> [!NOTE]
> **Bron.** MeshCore v1.17.1, commit
> [`d929643`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e), 14 augustus 2026 — `variants/*/platformio.ini` en de
> headers in dezelfde map. Reproduceren kan met
> [`tools/variant-pins.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/variant-pins.py):
>
> ```bash
> python3 tools/variant-pins.py --repo ../MeshCore \
>     --familie ESP32 --markdown --kopniveau 3
> ```
>
> Uitgecommentarieerde regels tellen niet mee. Een `#define` binnen `#if 0`
> wel: dat onderscheid maakt het script niet.

## Hoe je deze tabellen leest

Per variant staan de signalen gegroepeerd: LoRa-radio, I2C, SPI, display,
GPS, knoppen en LED, voeding en accu, en wat daarbuiten valt. Elke regel
noemt het bestand en het regelnummer waar de definitie staat, zodat je hem
zelf kunt nakijken.

De waarde is soms geen getal maar een andere naam — `P_LORA_NSS` wijst dan
naar `LORA_CS`, en die staat een paar regels hoger met het echte nummer. De
eerste vindplaats wint: staat een naam twee keer, dan is de tweede een alias.

Constanten die op een pin lijken maar het niet zijn, staan niet in de tabel.
`LORA_TX_POWER`, `SX126X_DIO3_TCXO_VOLTAGE` en `BLE_PIN_CODE` zijn
radio- en firmware-instellingen; het script meldt ze apart.

De ESP32-varianten zetten hun pinnen vrijwel allemaal in de `build_flags`
van `platformio.ini`, als `-D P_LORA_NSS=8`. Over de drieënveertig varianten
komen 948 signalen daarvandaan en 149 uit een header. De waarde is een kaal
GPIO-nummer: `8` is GPIO8.

## De varianten

### `ebyte_eora_s3`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `34` | `platformio.ini` r.11 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` r.8 |
| `P_LORA_MISO` | `3` | `platformio.ini` r.13 |
| `P_LORA_MOSI` | `6` | `platformio.ini` r.14 |
| `P_LORA_NSS` | `7` | `platformio.ini` r.9 |
| `P_LORA_RESET` | `8` | `platformio.ini` r.10 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.12 |
| `P_LORA_TX_LED` | `37` | `platformio.ini` r.15 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` r.19 |
| `PIN_BOARD_SDA` | `18` | `platformio.ini` r.18 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.17 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` r.16 |


### `generic-e22`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `LORA_CS` | `SX126X_CS` | `variant.h` r.40 |
| `LORA_DIO1` | `SX126X_DIO1` | `variant.h` r.44 |
| `LORA_MISO` | `SX126X_MISO` | `variant.h` r.43 |
| `LORA_MOSI` | `SX126X_MOSI` | `variant.h` r.42 |
| `LORA_SCK` | `SX126X_SCK` | `variant.h` r.41 |
| `P_LORA_BUSY` | `32` | `platformio.ini` r.13 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` r.10 |
| `P_LORA_MISO` | `19` | `platformio.ini` r.16 |
| `P_LORA_MOSI` | `27` | `platformio.ini` r.15 |
| `P_LORA_NSS` | `18` | `platformio.ini` r.11 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` r.12 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.14 |
| `P_LORA_TX_LED` | `2` | `platformio.ini` r.8 |
| `SX126X_BUSY` | `32` | `variant.h` r.30 |
| `SX126X_CS` | `18` | `variant.h` r.25 |
| `SX126X_DIO1` | `33` | `variant.h` r.31 |
| `SX126X_MAX_POWER` | `22` | `variant.h` r.22 |
| `SX126X_MISO` | `19` | `variant.h` r.28 |
| `SX126X_MOSI` | `27` | `variant.h` r.27 |
| `SX126X_RESET` | `23` | `variant.h` r.29 |
| `SX126X_RXEN` | `14` | `variant.h` r.38 |
| `SX126X_SCK` | `5` | `variant.h` r.26 |
| `SX126X_TXEN` | `13` | `variant.h` r.37 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` r.20 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` r.19 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `GPS_RX_PIN` | `12` | `variant.h` r.7 |
| `GPS_TX_PIN` | `15` | `variant.h` r.6 |
| `PIN_GPS_EN` | `4` | `variant.h` r.8 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `BUTTON_PIN` | `39` | `variant.h` r.11 |
| `LED_PIN` | `2` | `variant.h` r.17 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `BATTERY_PIN` | `35` | `variant.h` r.12 |
| `PIN_VBAT_READ` | `35` | `platformio.ini` r.9 |


### `generic_espnow`

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `-1` | `platformio.ini` r.13 |
| `PIN_BOARD_SDA` | `-1` | `platformio.ini` r.12 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.15 |


### `heltec_ct62`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `4` | `platformio.ini` r.23 |
| `P_LORA_DIO_0` | `RADIOLIB_NC` | `platformio.ini` r.21 |
| `P_LORA_DIO_1` | `3` | `platformio.ini` r.18 |
| `P_LORA_DIO_2` | `RADIOLIB_NC` | `platformio.ini` r.22 |
| `P_LORA_MISO` | `6` | `platformio.ini` r.25 |
| `P_LORA_MOSI` | `7` | `platformio.ini` r.26 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.19 |
| `P_LORA_RESET` | `5` | `platformio.ini` r.20 |
| `P_LORA_SCLK` | `10` | `platformio.ini` r.24 |
| `P_LORA_TX_LED` | `18` | `platformio.ini` r.13 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `1` | `platformio.ini` r.15 |
| `PIN_BOARD_SDA` | `0` | `platformio.ini` r.14 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `2` | `platformio.ini` r.17 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_DIGITAL_IN` | `19` | `platformio.ini` r.146 |
| `PIN_BOARD_RELAY_CH1` | `0` | `platformio.ini` r.144 |
| `PIN_BOARD_RELAY_CH2` | `1` | `platformio.ini` r.145 |


### `heltec_e213`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.15 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.12 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.17 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.18 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.13 |
| `P_LORA_RESET` | `12` | `platformio.ini` r.14 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.16 |
| `P_LORA_TX_LED` | `45` | `platformio.ini` r.19 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `38` | `platformio.ini` r.31 |
| `PIN_BOARD_SDA` | `39` | `platformio.ini` r.30 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.21 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `7` | `platformio.ini` r.24 |
| `PIN_VEXT_EN` | `18` | `platformio.ini` r.22 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` r.23 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_ADC_CTRL` | `46` | `platformio.ini` r.25 |


### `heltec_e290`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.16 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.13 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.18 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.19 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.14 |
| `P_LORA_RESET` | `12` | `platformio.ini` r.15 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.17 |
| `P_LORA_TX_LED` | `45` | `platformio.ini` r.20 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `38` | `platformio.ini` r.31 |
| `PIN_BOARD_SDA` | `39` | `platformio.ini` r.30 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.21 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `7` | `platformio.ini` r.24 |
| `PIN_VEXT_EN` | `18` | `platformio.ini` r.22 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` r.23 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_ADC_CTRL` | `46` | `platformio.ini` r.25 |


### `heltec_rc32`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `LORA_CS` | `10` | `variant.h` r.14 |
| `LORA_DIO0` | `RADIOLIB_NC` | `variant.h` r.15 |
| `LORA_DIO1` | `14` | `variant.h` r.16 |
| `LORA_MISO` | `13` | `variant.h` r.12 |
| `LORA_MOSI` | `12` | `variant.h` r.13 |
| `LORA_RESET` | `9` | `variant.h` r.17 |
| `LORA_SCK` | `11` | `variant.h` r.11 |
| `P_LORA_BUSY` | `1` | `platformio.ini` r.18 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.15 |
| `P_LORA_MISO` | `13` | `platformio.ini` r.20 |
| `P_LORA_MOSI` | `12` | `platformio.ini` r.21 |
| `P_LORA_NSS` | `10` | `platformio.ini` r.16 |
| `P_LORA_RESET` | `9` | `platformio.ini` r.17 |
| `P_LORA_SCLK` | `11` | `platformio.ini` r.19 |
| `P_LORA_TX_LED` | `47` | `platformio.ini` r.29 |
| `SX126X_BUSY` | `1` | `variant.h` r.21 |
| `SX126X_CS` | `LORA_CS` | `variant.h` r.19 |
| `SX126X_DIO1` | `LORA_DIO1` | `variant.h` r.20 |
| `SX126X_REGISTER_PATCH` | `1` | `platformio.ini` r.58 |
| `SX126X_RESET` | `LORA_RESET` | `variant.h` r.22 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` r.25 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` r.24 |

**Display**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_TFT_BL` | `5` | `platformio.ini` r.38 |
| `PIN_TFT_BL_ACTIVE` | `HIGH` | `platformio.ini` r.39 |
| `PIN_TFT_CS` | `39` | `platformio.ini` r.33 |
| `PIN_TFT_DC` | `16` | `platformio.ini` r.34 |
| `PIN_TFT_EN` | `6` | `platformio.ini` r.36 |
| `PIN_TFT_EN_ACTIVE` | `LOW` | `platformio.ini` r.37 |
| `PIN_TFT_RST` | `4` | `platformio.ini` r.35 |
| `PIN_TFT_SCL` | `17` | `platformio.ini` r.31 |
| `PIN_TFT_SDA` | `38` | `platformio.ini` r.32 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_EN` | `45` | `platformio.ini` r.43 |
| `PIN_GPS_EN_ACTIVE` | `HIGH` | `platformio.ini` r.44 |
| `PIN_GPS_PPS` | `41` | `platformio.ini` r.47 |
| `PIN_GPS_RESET` | `40` | `platformio.ini` r.45 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` r.46 |
| `PIN_GPS_RX` | `43` | `platformio.ini` r.42 |
| `PIN_GPS_TX` | `44` | `platformio.ini` r.41 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `BUTTON_PIN` | `0` | `variant.h` r.4 |
| `PIN_USER_BTN` | `0` | `platformio.ini` r.23 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `BATTERY_PIN` | `7` | `variant.h` r.24 |
| `PIN_VBAT_READ` | `7` | `platformio.ini` r.51 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `ENV_PIN_SCL` | `18` | `platformio.ini` r.204 |
| `ENV_PIN_SDA` | `21` | `platformio.ini` r.203 |
| `PIN_ADC_CTRL` | `15` | `platformio.ini` r.50 |
| `PIN_BUZZER` | `48` | `platformio.ini` r.30 |
| `SENSOR_INT_PIN` | `42` | `variant.h` r.8 |
| `SENSOR_POWER_CTRL_PIN` | `46` | `platformio.ini` r.26 |
| `SENSOR_RST_PIN` | `2` | `platformio.ini` r.28 |


### `heltec_t190`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.15 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.12 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.17 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.18 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.13 |
| `P_LORA_RESET` | `12` | `platformio.ini` r.14 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.16 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `1` | `platformio.ini` r.30 |
| `PIN_BOARD_SDA` | `2` | `platformio.ini` r.29 |

**Display**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_TFT_CS` | `39` | `platformio.ini` r.37 |
| `PIN_TFT_DC` | `47` | `platformio.ini` r.38 |
| `PIN_TFT_LEDA_CTL` | `17` | `platformio.ini` r.35 |
| `PIN_TFT_LEDA_CTL_ACTIVE` | `HIGH` | `platformio.ini` r.36 |
| `PIN_TFT_RST` | `40` | `platformio.ini` r.33 |
| `PIN_TFT_SCL` | `38` | `platformio.ini` r.31 |
| `PIN_TFT_SDA` | `48` | `platformio.ini` r.32 |
| `PIN_TFT_VDD_CTL` | `7` | `platformio.ini` r.34 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.20 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `6` | `platformio.ini` r.23 |
| `PIN_VEXT_EN` | `5` | `platformio.ini` r.21 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` r.22 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_ADC_CTRL` | `46` | `platformio.ini` r.24 |


### `heltec_tracker`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.13 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.10 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.15 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.16 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.11 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` r.12 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.14 |
| `P_LORA_TX_LED` | `18` | `platformio.ini` r.21 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `46` | `platformio.ini` r.23 |
| `PIN_BOARD_SDA` | `45` | `platformio.ini` r.22 |

**Display**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_TFT_CS` | `38` | `platformio.ini` r.30 |
| `PIN_TFT_DC` | `40` | `platformio.ini` r.28 |
| `PIN_TFT_LEDA_CTL` | `21` | `platformio.ini` r.33 |
| `PIN_TFT_RST` | `39` | `platformio.ini` r.29 |
| `PIN_TFT_SCL` | `41` | `platformio.ini` r.27 |
| `PIN_TFT_SDA` | `42` | `platformio.ini` r.26 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_EN` | `35` | `platformio.ini` r.36 |
| `PIN_GPS_RESET` | `36` | `platformio.ini` r.37 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` r.38 |
| `PIN_GPS_RX` | `33` | `platformio.ini` r.34 |
| `PIN_GPS_TX` | `34` | `platformio.ini` r.35 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.24 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VEXT_EN` | `3` | `platformio.ini` r.32 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_ADC_CTRL` | `2` | `platformio.ini` r.25 |
| `USE_PIN_TFT` | `1` | `platformio.ini` r.31 |


### `heltec_tracker_v2`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.17 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.14 |
| `P_LORA_KCT8103L_PA_CSD` | `4` | `platformio.ini` r.22 |
| `P_LORA_KCT8103L_PA_CTX` | `5` | `platformio.ini` r.23 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.19 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.20 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.15 |
| `P_LORA_PA_POWER` | `7` | `platformio.ini` r.21 |
| `P_LORA_RESET` | `12` | `platformio.ini` r.16 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.18 |
| `P_LORA_TX_LED` | `18` | `platformio.ini` r.13 |
| `SX126X_REGISTER_PATCH` | `1` | `platformio.ini` r.30 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` r.32 |
| `PIN_BOARD_SDA` | `6` | `platformio.ini` r.31 |

**Display**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_TFT_CS` | `38` | `platformio.ini` r.38 |
| `PIN_TFT_DC` | `40` | `platformio.ini` r.36 |
| `PIN_TFT_LEDA_CTL` | `21` | `platformio.ini` r.42 |
| `PIN_TFT_RST` | `39` | `platformio.ini` r.37 |
| `PIN_TFT_SCL` | `41` | `platformio.ini` r.35 |
| `PIN_TFT_SDA` | `42` | `platformio.ini` r.34 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_RESET` | `35` | `platformio.ini` r.46 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` r.47 |
| `PIN_GPS_RX` | `34` | `platformio.ini` r.44 |
| `PIN_GPS_TX` | `33` | `platformio.ini` r.45 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.33 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` r.51 |
| `PIN_VEXT_EN` | `3` | `platformio.ini` r.40 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` r.41 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_ADC_CTRL` | `2` | `platformio.ini` r.50 |
| `USE_PIN_TFT` | `1` | `platformio.ini` r.39 |


### `heltec_v2`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` r.10 |
| `P_LORA_DIO_1` | `35` | `platformio.ini` r.11 |
| `P_LORA_MISO` | `19` | `platformio.ini` r.15 |
| `P_LORA_MOSI` | `27` | `platformio.ini` r.16 |
| `P_LORA_NSS` | `18` | `platformio.ini` r.12 |
| `P_LORA_RESET` | `14` | `platformio.ini` r.13 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.14 |
| `P_LORA_TX_LED` | `25` | `platformio.ini` r.17 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `15` | `platformio.ini` r.21 |
| `PIN_BOARD_SDA` | `4` | `platformio.ini` r.20 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_LED_BUILTIN` | `25` | `HeltecV2Board.h` r.8 |
| `PIN_USER_BTN` | `0` | `platformio.ini` r.22 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `37` | `HeltecV2Board.h` r.7 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_OLED_RESET` | `16` | `platformio.ini` r.23 |


### `heltec_v3`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.13 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.10 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.15 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.16 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.11 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` r.12 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.14 |
| `P_LORA_TX_LED` | `35` | `platformio.ini` r.21 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` r.23 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` r.22 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_EN` | `26` | `platformio.ini` r.32 |
| `PIN_GPS_RX` | `47` | `platformio.ini` r.30 |
| `PIN_GPS_TX` | `48` | `platformio.ini` r.31 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.24 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `HeltecV3Board.h` r.9 |
| `PIN_VEXT_EN` | `36` | `platformio.ini` r.25 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `ENV_PIN_SCL` | `34` | `platformio.ini` r.216 |
| `ENV_PIN_SDA` | `33` | `platformio.ini` r.215 |
| `PIN_ADC_CTRL` | `37` | `HeltecV3Board.h` r.12 |
| `PIN_ADC_CTRL_ACTIVE` | `LOW` | `HeltecV3Board.h` r.17 |
| `PIN_ADC_CTRL_INACTIVE` | `HIGH` | `HeltecV3Board.h` r.18 |


### `heltec_v4`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.17 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.14 |
| `P_LORA_GC1109_PA_EN` | `2` | `platformio.ini` r.22 |
| `P_LORA_GC1109_PA_TX_EN` | `46` | `platformio.ini` r.23 |
| `P_LORA_KCT8103L_PA_CSD` | `2` | `platformio.ini` r.24 |
| `P_LORA_KCT8103L_PA_CTX` | `5` | `platformio.ini` r.25 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.19 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.20 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.15 |
| `P_LORA_PA_POWER` | `7` | `platformio.ini` r.21 |
| `P_LORA_RESET` | `12` | `platformio.ini` r.16 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.18 |
| `P_LORA_TX_LED` | `35` | `platformio.ini` r.13 |
| `SX126X_REGISTER_PATCH` | `1` | `platformio.ini` r.31 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` r.58 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` r.57 |

**Display**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_TFT_CS` | `15` | `platformio.ini` r.76 |
| `PIN_TFT_DC` | `16` | `platformio.ini` r.77 |
| `PIN_TFT_LEDA_CTL` | `21` | `platformio.ini` r.74 |
| `PIN_TFT_LEDA_CTL_ACTIVE` | `HIGH` | `platformio.ini` r.75 |
| `PIN_TFT_RST` | `18` | `platformio.ini` r.72 |
| `PIN_TFT_SCL` | `17` | `platformio.ini` r.78 |
| `PIN_TFT_SDA` | `33` | `platformio.ini` r.79 |
| `PIN_TFT_VDD_CTL` | `-1` | `platformio.ini` r.73 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_EN` | `34` | `platformio.ini` r.40 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `platformio.ini` r.41 |
| `PIN_GPS_RESET` | `42` | `platformio.ini` r.38 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` r.39 |
| `PIN_GPS_RX` | `38` | `platformio.ini` r.36 |
| `PIN_GPS_TX` | `39` | `platformio.ini` r.37 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.26 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` r.44 |
| `PIN_VEXT_EN` | `36` | `platformio.ini` r.27 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` r.28 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `ENV_PIN_SCL` | `3` | `platformio.ini` r.118 |
| `ENV_PIN_SDA` | `4` | `platformio.ini` r.117 |
| `PIN_ADC_CTRL` | `37` | `platformio.ini` r.43 |
| `PIN_OLED_RESET` | `21` | `platformio.ini` r.59 |


### `heltec_v4_r8`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.16 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.13 |
| `P_LORA_KCT8103L_PA_CSD` | `2` | `platformio.ini` r.21 |
| `P_LORA_KCT8103L_PA_CTX` | `5` | `platformio.ini` r.22 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.18 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.19 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.14 |
| `P_LORA_PA_POWER` | `7` | `platformio.ini` r.20 |
| `P_LORA_RESET` | `12` | `platformio.ini` r.15 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.17 |
| `P_LORA_TX_LED` | `46` | `platformio.ini` r.23 |
| `SX126X_REGISTER_PATCH` | `1` | `platformio.ini` r.31 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` r.54 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` r.53 |

**Display**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_TFT_CS` | `47` | `platformio.ini` r.72 |
| `PIN_TFT_DC` | `48` | `platformio.ini` r.73 |
| `PIN_TFT_LEDA_CTL` | `44` | `platformio.ini` r.70 |
| `PIN_TFT_LEDA_CTL_ACTIVE` | `HIGH` | `platformio.ini` r.71 |
| `PIN_TFT_MISO` | `45` | `platformio.ini` r.76 |
| `PIN_TFT_RST` | `-1` | `platformio.ini` r.68 |
| `PIN_TFT_SCL` | `16` | `platformio.ini` r.74 |
| `PIN_TFT_SDA` | `15` | `platformio.ini` r.75 |
| `PIN_TFT_VDD_CTL` | `-1` | `platformio.ini` r.69 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_EN` | `42` | `platformio.ini` r.38 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `platformio.ini` r.39 |
| `PIN_GPS_RX` | `38` | `platformio.ini` r.36 |
| `PIN_GPS_TX` | `39` | `platformio.ini` r.37 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.24 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` r.28 |
| `PIN_VEXT_EN` | `40` | `platformio.ini` r.25 |
| `PIN_VEXT_EN_ACTIVE` | `LOW` | `platformio.ini` r.26 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BUZZER` | `4` | `platformio.ini` r.77 |
| `PIN_OLED_RESET` | `21` | `platformio.ini` r.55 |
| `PIN_TOUCH_RST` | `21` | `platformio.ini` r.78 |


### `heltec_wireless_paper`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.12 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.9 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.14 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.15 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.10 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` r.11 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.13 |
| `P_LORA_TX_LED` | `18` | `platformio.ini` r.20 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.23 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `20` | `platformio.ini` r.26 |
| `PIN_VEXT_EN` | `45` | `platformio.ini` r.24 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_ADC_CTRL` | `19` | `platformio.ini` r.27 |


### `lilygo_t3s3`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `34` | `platformio.ini` r.11 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` r.8 |
| `P_LORA_MISO` | `3` | `platformio.ini` r.13 |
| `P_LORA_MOSI` | `6` | `platformio.ini` r.14 |
| `P_LORA_NSS` | `7` | `platformio.ini` r.9 |
| `P_LORA_RESET` | `8` | `platformio.ini` r.10 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.12 |
| `P_LORA_TX_LED` | `37` | `platformio.ini` r.15 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` r.19 |
| `PIN_BOARD_SDA` | `18` | `platformio.ini` r.18 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.17 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` r.16 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_OLED_RESET` | `21` | `platformio.ini` r.21 |


### `lilygo_t3s3_sx1276`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_DIO_0` | `9` | `platformio.ini` r.8 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` r.9 |
| `P_LORA_MISO` | `3` | `platformio.ini` r.13 |
| `P_LORA_MOSI` | `6` | `platformio.ini` r.14 |
| `P_LORA_NSS` | `7` | `platformio.ini` r.10 |
| `P_LORA_RESET` | `8` | `platformio.ini` r.11 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.12 |
| `P_LORA_TX_LED` | `37` | `platformio.ini` r.15 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` r.19 |
| `PIN_BOARD_SDA` | `18` | `platformio.ini` r.18 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.17 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` r.16 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_OLED_RESET` | `21` | `platformio.ini` r.20 |


### `lilygo_tbeam_1w`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `LORA_BUSY` | `38` | `variant.h` r.44 |
| `LORA_CS` | `15` | `variant.h` r.41 |
| `LORA_DIO1` | `1` | `variant.h` r.43 |
| `LORA_MISO` | `SPI_MISO` | `variant.h` r.39 |
| `LORA_MOSI` | `SPI_MOSI` | `variant.h` r.40 |
| `LORA_RESET` | `3` | `variant.h` r.42 |
| `LORA_SCK` | `SPI_SCK` | `variant.h` r.38 |
| `P_LORA_BUSY` | `38` | `platformio.ini` r.16 |
| `P_LORA_DIO_1` | `1` | `platformio.ini` r.13 |
| `P_LORA_MISO` | `12` | `platformio.ini` r.18 |
| `P_LORA_MOSI` | `11` | `platformio.ini` r.19 |
| `P_LORA_NSS` | `15` | `platformio.ini` r.14 |
| `P_LORA_RESET` | `3` | `platformio.ini` r.15 |
| `P_LORA_SCLK` | `13` | `platformio.ini` r.17 |
| `SX126X_BUSY` | `LORA_BUSY` | `variant.h` r.53 |
| `SX126X_CS` | `LORA_CS` | `variant.h` r.51 |
| `SX126X_DIO1` | `LORA_DIO1` | `variant.h` r.52 |
| `SX126X_MAX_POWER` | `22` | `variant.h` r.67 |
| `SX126X_PA_RAMP_US` | `0x05` | `variant.h` r.88 |
| `SX126X_POWER_EN` | `40` | `variant.h` r.48 |
| `SX126X_RESET` | `LORA_RESET` | `variant.h` r.54 |
| `SX126X_RXEN` | `21` | `variant.h` r.62 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `9` | `platformio.ini` r.43 |
| `PIN_BOARD_SDA` | `8` | `platformio.ini` r.42 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_EN` | `16` | `variant.h` r.16 |
| `PIN_GPS_PPS` | `7` | `variant.h` r.15 |
| `PIN_GPS_RX` | `6` | `variant.h` r.14 |
| `PIN_GPS_TX` | `5` | `variant.h` r.13 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `BUTTON_PIN` | `0` | `variant.h` r.21 |
| `BUTTON_PIN_ALT` | `17` | `variant.h` r.22 |
| `LED_PIN` | `18` | `variant.h` r.71 |
| `PIN_USER_BTN` | `17` | `platformio.ini` r.54 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `BATTERY_PIN` | `4` | `variant.h` r.75 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `FAN_CTRL_PIN` | `41` | `variant.h` r.84 |
| `NTC_PIN` | `14` | `variant.h` r.81 |


### `lilygo_tbeam_SX1262`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` r.8 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` r.9 |
| `P_LORA_MISO` | `19` | `platformio.ini` r.13 |
| `P_LORA_MOSI` | `27` | `platformio.ini` r.14 |
| `P_LORA_NSS` | `18` | `platformio.ini` r.10 |
| `P_LORA_RESET` | `23` | `platformio.ini` r.11 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.12 |
| `P_LORA_TX_LED` | `4` | `platformio.ini` r.24 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` r.26 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` r.25 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_RX` | `12` | `platformio.ini` r.27 |
| `PIN_GPS_TX` | `34` | `platformio.ini` r.28 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` r.29 |


### `lilygo_tbeam_SX1276`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` r.8 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` r.9 |
| `P_LORA_MISO` | `19` | `platformio.ini` r.13 |
| `P_LORA_MOSI` | `27` | `platformio.ini` r.14 |
| `P_LORA_NSS` | `18` | `platformio.ini` r.10 |
| `P_LORA_RESET` | `23` | `platformio.ini` r.11 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.12 |
| `P_LORA_TX_LED` | `4` | `platformio.ini` r.20 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` r.22 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` r.21 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_RX` | `12` | `platformio.ini` r.23 |
| `PIN_GPS_TX` | `34` | `platformio.ini` r.24 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` r.25 |


### `lilygo_tbeam_supreme_SX1262`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` r.8 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` r.9 |
| `P_LORA_MISO` | `19` | `platformio.ini` r.13 |
| `P_LORA_MOSI` | `27` | `platformio.ini` r.14 |
| `P_LORA_NSS` | `18` | `platformio.ini` r.10 |
| `P_LORA_RESET` | `23` | `platformio.ini` r.11 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.12 |
| `P_LORA_TX_LED` | `6` | `platformio.ini` r.23 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` r.25 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` r.24 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_EN` | `7` | `platformio.ini` r.28 |
| `PIN_GPS_RX` | `8` | `platformio.ini` r.26 |
| `PIN_GPS_TX` | `9` | `platformio.ini` r.27 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.29 |


### `lilygo_tdeck`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.40 |
| `P_LORA_DIO_1` | `45` | `platformio.ini` r.22 |
| `P_LORA_MISO` | `38` | `platformio.ini` r.42 |
| `P_LORA_MOSI` | `41` | `platformio.ini` r.43 |
| `P_LORA_NSS` | `9` | `platformio.ini` r.38 |
| `P_LORA_RESET` | `17` | `platformio.ini` r.39 |
| `P_LORA_SCLK` | `40` | `platformio.ini` r.41 |

**Display**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_TFT_CS` | `12` | `platformio.ini` r.50 |
| `PIN_TFT_DC` | `11` | `platformio.ini` r.51 |
| `PIN_TFT_LEDA_CTL` | `42` | `platformio.ini` r.49 |
| `PIN_TFT_RST` | `-1` | `platformio.ini` r.47 |
| `PIN_TFT_SCL` | `40` | `platformio.ini` r.52 |
| `PIN_TFT_SDA` | `41` | `platformio.ini` r.53 |
| `PIN_TFT_VDD_CTL` | `-1` | `platformio.ini` r.48 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_RX` | `43` | `platformio.ini` r.54 |
| `PIN_GPS_TX` | `44` | `platformio.ini` r.55 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.12 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `4` | `TDeckBoard.h` r.7 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_PERF_POWERON` | `10` | `platformio.ini` r.13 |


### `lilygo_teth_elite`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `16` | `platformio.ini` r.16 |
| `P_LORA_DIO_1` | `8` | `platformio.ini` r.13 |
| `P_LORA_MISO` | `9` | `platformio.ini` r.18 |
| `P_LORA_MOSI` | `11` | `platformio.ini` r.19 |
| `P_LORA_NSS` | `40` | `platformio.ini` r.14 |
| `P_LORA_RESET` | `46` | `platformio.ini` r.15 |
| `P_LORA_SCLK` | `10` | `platformio.ini` r.17 |
| `P_LORA_TX_LED` | `38` | `platformio.ini` r.20 |


### `lilygo_tlora_c6`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `22` | `platformio.ini` r.16 |
| `P_LORA_DIO_1` | `23` | `platformio.ini` r.15 |
| `P_LORA_MISO` | `1` | `platformio.ini` r.12 |
| `P_LORA_MOSI` | `0` | `platformio.ini` r.13 |
| `P_LORA_NSS` | `18` | `platformio.ini` r.14 |
| `P_LORA_RESET` | `21` | `platformio.ini` r.17 |
| `P_LORA_SCLK` | `6` | `platformio.ini` r.11 |
| `P_LORA_TX_LED` | `7` | `platformio.ini` r.10 |
| `SX126X_RXEN` | `15` | `platformio.ini` r.20 |
| `SX126X_TXEN` | `14` | `platformio.ini` r.21 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `9` | `platformio.ini` r.19 |
| `PIN_BOARD_SDA` | `8` | `platformio.ini` r.18 |


### `lilygo_tlora_v2_1`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` r.14 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` r.15 |
| `P_LORA_MISO` | `19` | `platformio.ini` r.19 |
| `P_LORA_MOSI` | `27` | `platformio.ini` r.20 |
| `P_LORA_NSS` | `18` | `platformio.ini` r.16 |
| `P_LORA_RESET` | `14` | `platformio.ini` r.17 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.18 |
| `P_LORA_TX_LED` | `25` | `platformio.ini` r.21 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` r.23 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` r.22 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.25 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `35` | `platformio.ini` r.24 |


### `m5stack_unit_c6l`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `19` | `platformio.ini` r.16 |
| `P_LORA_DIO_1` | `7` | `platformio.ini` r.15 |
| `P_LORA_MISO` | `22` | `platformio.ini` r.12 |
| `P_LORA_MOSI` | `21` | `platformio.ini` r.13 |
| `P_LORA_NSS` | `23` | `platformio.ini` r.14 |
| `P_LORA_RESET` | `-1` | `platformio.ini` r.17 |
| `P_LORA_SCLK` | `20` | `platformio.ini` r.11 |
| `P_LORA_TX_LED` | `15` | `platformio.ini` r.10 |
| `SX126X_RXEN` | `5` | `platformio.ini` r.21 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` r.20 |
| `PIN_BOARD_SDA` | `16` | `platformio.ini` r.19 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BUZZER` | `11` | `platformio.ini` r.18 |


### `meshadventurer`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `LORA_CS` | `SX126X_CS` | `variant.h` r.40 |
| `LORA_DIO1` | `SX126X_DIO1` | `variant.h` r.44 |
| `LORA_MISO` | `SX126X_MISO` | `variant.h` r.43 |
| `LORA_MOSI` | `SX126X_MOSI` | `variant.h` r.42 |
| `LORA_SCK` | `SX126X_SCK` | `variant.h` r.41 |
| `P_LORA_BUSY` | `32` | `platformio.ini` r.15 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` r.12 |
| `P_LORA_MISO` | `19` | `platformio.ini` r.18 |
| `P_LORA_MOSI` | `27` | `platformio.ini` r.17 |
| `P_LORA_NSS` | `18` | `platformio.ini` r.13 |
| `P_LORA_RESET` | `23` | `platformio.ini` r.14 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.16 |
| `P_LORA_TX_LED` | `2` | `platformio.ini` r.9 |
| `SX126X_BUSY` | `32` | `variant.h` r.30 |
| `SX126X_CS` | `18` | `variant.h` r.25 |
| `SX126X_DIO1` | `33` | `variant.h` r.31 |
| `SX126X_MAX_POWER` | `22` | `variant.h` r.22 |
| `SX126X_MISO` | `19` | `variant.h` r.28 |
| `SX126X_MOSI` | `27` | `variant.h` r.27 |
| `SX126X_RESET` | `23` | `variant.h` r.29 |
| `SX126X_RXEN` | `14` | `variant.h` r.38 |
| `SX126X_SCK` | `5` | `variant.h` r.26 |
| `SX126X_TXEN` | `13` | `variant.h` r.37 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` r.22 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` r.21 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `GPS_RX_PIN` | `12` | `variant.h` r.7 |
| `GPS_TX_PIN` | `15` | `variant.h` r.6 |
| `PIN_GPS_EN` | `4` | `variant.h` r.8 |
| `PIN_GPS_RX` | `12` | `platformio.ini` r.26 |
| `PIN_GPS_TX` | `15` | `platformio.ini` r.27 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `BUTTON_PIN` | `39` | `variant.h` r.11 |
| `LED_PIN` | `2` | `variant.h` r.17 |
| `PIN_USER_BTN` | `39` | `platformio.ini` r.11 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `BATTERY_PIN` | `35` | `variant.h` r.12 |
| `PIN_VBAT_READ` | `35` | `platformio.ini` r.10 |


### `meshnology_w12`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.22 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` r.15 |
| `P_LORA_HF_PA_POWER` | `3` | `platformio.ini` r.26 |
| `P_LORA_LF_PA_POWER` | `4` | `platformio.ini` r.25 |
| `P_LORA_MISO` | `11` | `platformio.ini` r.20 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.19 |
| `P_LORA_NSS` | `8` | `platformio.ini` r.17 |
| `P_LORA_RESET` | `12` | `platformio.ini` r.21 |
| `P_LORA_SCLK` | `9` | `platformio.ini` r.18 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` r.42 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` r.41 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_EN` | `48` | `platformio.ini` r.36 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `platformio.ini` r.37 |
| `PIN_GPS_RESET` | `42` | `platformio.ini` r.34 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` r.35 |
| `PIN_GPS_RX` | `38` | `platformio.ini` r.32 |
| `PIN_GPS_TX` | `39` | `platformio.ini` r.33 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` r.27 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` r.39 |
| `PIN_VEXT_EN` | `45` | `platformio.ini` r.28 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` r.29 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `ENV_PIN_SCL` | `4` | `platformio.ini` r.202 |
| `ENV_PIN_SDA` | `3` | `platformio.ini` r.201 |
| `PIN_ADC_CTRL` | `2` | `platformio.ini` r.40 |
| `PIN_RESET` | `47` | `platformio.ini` r.43 |


### `nibble_screen_connect`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `5` | `platformio.ini` r.11 |
| `P_LORA_DIO_1` | `4` | `platformio.ini` r.8 |
| `P_LORA_MISO` | `12` | `platformio.ini` r.13 |
| `P_LORA_MOSI` | `11` | `platformio.ini` r.14 |
| `P_LORA_NSS` | `10` | `platformio.ini` r.9 |
| `P_LORA_RESET` | `6` | `platformio.ini` r.10 |
| `P_LORA_SCLK` | `13` | `platformio.ini` r.12 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `7` | `platformio.ini` r.17 |
| `PIN_BOARD_SDA` | `8` | `platformio.ini` r.16 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `1` | `platformio.ini` r.15 |


### `nibble_zero_connect`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `5` | `platformio.ini` r.11 |
| `P_LORA_DIO_1` | `4` | `platformio.ini` r.8 |
| `P_LORA_MISO` | `13` | `platformio.ini` r.13 |
| `P_LORA_MOSI` | `11` | `platformio.ini` r.14 |
| `P_LORA_NSS` | `10` | `platformio.ini` r.9 |
| `P_LORA_RESET` | `6` | `platformio.ini` r.10 |
| `P_LORA_SCLK` | `12` | `platformio.ini` r.12 |
| `P_LORA_TX_LED` | `39` | `platformio.ini` r.19 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `7` | `platformio.ini` r.17 |
| `PIN_BOARD_SDA` | `8` | `platformio.ini` r.16 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_STATUS_LED` | `39` | `platformio.ini` r.18 |
| `PIN_USER_BTN` | `1` | `platformio.ini` r.15 |


### `rak3112`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `48` | `platformio.ini` r.14 |
| `P_LORA_DIO_1` | `47` | `platformio.ini` r.11 |
| `P_LORA_MISO` | `3` | `platformio.ini` r.16 |
| `P_LORA_MOSI` | `6` | `platformio.ini` r.17 |
| `P_LORA_NSS` | `7` | `platformio.ini` r.12 |
| `P_LORA_RESET` | `8` | `platformio.ini` r.13 |
| `P_LORA_SCLK` | `5` | `platformio.ini` r.15 |
| `P_LORA_TX_LED` | `46` | `platformio.ini` r.22 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `40` | `platformio.ini` r.24 |
| `PIN_BOARD_SDA` | `9` | `platformio.ini` r.23 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_RX` | `43` | `platformio.ini` r.31 |
| `PIN_GPS_TX` | `44` | `platformio.ini` r.32 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `-1` | `platformio.ini` r.25 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `RAK3112Board.h` r.9 |
| `PIN_VEXT_EN` | `14` | `platformio.ini` r.26 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `ENV_PIN_SCL` | `34` | `platformio.ini` r.200 |
| `ENV_PIN_SDA` | `33` | `platformio.ini` r.199 |
| `PIN_ADC_CTRL` | `36` | `RAK3112Board.h` r.12 |
| `PIN_ADC_CTRL_ACTIVE` | `LOW` | `RAK3112Board.h` r.14 |
| `PIN_ADC_CTRL_INACTIVE` | `HIGH` | `RAK3112Board.h` r.15 |


### `sensecap_indicator-espnow`

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `40` | `platformio.ini` r.13 |
| `PIN_BOARD_SDA` | `39` | `platformio.ini` r.12 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` r.23 |


### `station_g2`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `47` | `platformio.ini` r.16 |
| `P_LORA_DIO_1` | `48` | `platformio.ini` r.13 |
| `P_LORA_MISO` | `14` | `platformio.ini` r.18 |
| `P_LORA_MOSI` | `13` | `platformio.ini` r.19 |
| `P_LORA_NSS` | `11` | `platformio.ini` r.14 |
| `P_LORA_RESET` | `21` | `platformio.ini` r.15 |
| `P_LORA_SCLK` | `12` | `platformio.ini` r.17 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `6` | `platformio.ini` r.24 |
| `PIN_BOARD_SDA` | `5` | `platformio.ini` r.23 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_RX` | `15` | `platformio.ini` r.26 |
| `PIN_GPS_TX` | `7` | `platformio.ini` r.27 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` r.25 |


### `station_g3_esp32`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `47` | `platformio.ini` r.16 |
| `P_LORA_DIO_1` | `48` | `platformio.ini` r.13 |
| `P_LORA_MISO` | `14` | `platformio.ini` r.18 |
| `P_LORA_MOSI` | `13` | `platformio.ini` r.19 |
| `P_LORA_NSS` | `11` | `platformio.ini` r.14 |
| `P_LORA_RESET` | `21` | `platformio.ini` r.15 |
| `P_LORA_SCLK` | `12` | `platformio.ini` r.17 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `6` | `platformio.ini` r.28 |
| `PIN_BOARD_SDA` | `5` | `platformio.ini` r.27 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_RX` | `15` | `platformio.ini` r.30 |
| `PIN_GPS_TX` | `7` | `platformio.ini` r.31 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` r.29 |


### `tenstar_c3`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `LORA_TX_BOOST_PIN` | `4` | `platformio.ini` r.8 |
| `P_LORA_BUSY` | `3` | `platformio.ini` r.17 |
| `P_LORA_DIO_1` | `2` | `platformio.ini` r.14 |
| `P_LORA_MISO` | `9` | `platformio.ini` r.11 |
| `P_LORA_MOSI` | `7` | `platformio.ini` r.13 |
| `P_LORA_NSS` | `6` | `platformio.ini` r.15 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` r.16 |
| `P_LORA_SCLK` | `8` | `platformio.ini` r.12 |
| `P_LORA_TX_NEOPIXEL_LED` | `10` | `platformio.ini` r.9 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` r.10 |


### `thinknode_m2`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `14` | `platformio.ini` r.17 |
| `P_LORA_DIO_1` | `3` | `platformio.ini` r.14 |
| `P_LORA_MISO` | `13` | `platformio.ini` r.19 |
| `P_LORA_MOSI` | `11` | `platformio.ini` r.20 |
| `P_LORA_NSS` | `10` | `platformio.ini` r.15 |
| `P_LORA_RESET` | `21` | `platformio.ini` r.16 |
| `P_LORA_SCLK` | `12` | `platformio.ini` r.18 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `15` | `platformio.ini` r.12 |
| `PIN_BOARD_SDA` | `16` | `platformio.ini` r.13 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_LED` | `6` | `variant.h` r.10 |
| `PIN_STATUS_LED` | `6` | `variant.h` r.11 |
| `PIN_USER_BTN` | `47` | `variant.h` r.9 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `17` | `variant.h` r.3 |
| `PIN_VEXT_EN` | `46` | `variant.h` r.8 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `variant.h` r.7 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BUZZER` | `5` | `variant.h` r.6 |
| `PIN_PWRBTN` | `4` | `variant.h` r.12 |


### `thinknode_m5`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `5` | `platformio.ini` r.15 |
| `P_LORA_DIO_1` | `4` | `platformio.ini` r.12 |
| `P_LORA_EN` | `46` | `platformio.ini` r.11 |
| `P_LORA_MISO` | `7` | `platformio.ini` r.17 |
| `P_LORA_MOSI` | `15` | `platformio.ini` r.18 |
| `P_LORA_NSS` | `17` | `platformio.ini` r.13 |
| `P_LORA_RESET` | `6` | `platformio.ini` r.14 |
| `P_LORA_SCLK` | `16` | `platformio.ini` r.16 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `1` | `platformio.ini` r.9 |
| `PIN_BOARD_SDA` | `2` | `platformio.ini` r.10 |

**Display**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_DISPLAY_BUSY` | `(42)` | `variant.h` r.20 |
| `PIN_DISPLAY_CS` | `(39)` | `variant.h` r.17 |
| `PIN_DISPLAY_DC` | `(40)` | `variant.h` r.18 |
| `PIN_DISPLAY_MISO` | `(-1)` | `variant.h` r.14 |
| `PIN_DISPLAY_MOSI` | `(45)` | `variant.h` r.15 |
| `PIN_DISPLAY_RST` | `(41)` | `variant.h` r.19 |
| `PIN_DISPLAY_SCLK` | `(38)` | `variant.h` r.16 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_GPS_EN` | `(11)` | `variant.h` r.24 |
| `PIN_GPS_RESET` | `(13)` | `variant.h` r.25 |
| `PIN_GPS_RX` | `(20)` | `variant.h` r.26 |
| `PIN_GPS_SWITCH` | `(10)` | `variant.h` r.28 |
| `PIN_GPS_TX` | `(19)` | `variant.h` r.27 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BUTTON2` | `14` | `platformio.ini` r.20 |
| `PIN_USER_BTN` | `21` | `variant.h` r.9 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `8` | `variant.h` r.3 |
| `PIN_VEXT_EN` | `46` | `variant.h` r.8 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `variant.h` r.7 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `EXP_PIN_BACKLIGHT` | `(5)` | `variant.h` r.21 |
| `EXP_PIN_LED` | `1` | `platformio.ini` r.21 |
| `EXP_PIN_POWER` | `(4)` | `variant.h` r.22 |
| `PIN_BUZZER` | `9` | `variant.h` r.6 |
| `PIN_PWRBTN` | `14` | `variant.h` r.12 |


### `thinknode_m7`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` r.21 |
| `P_LORA_DIO_1` | `38` | `platformio.ini` r.24 |
| `P_LORA_MISO` | `9` | `platformio.ini` r.25 |
| `P_LORA_MOSI` | `10` | `platformio.ini` r.26 |
| `P_LORA_NSS` | `12` | `platformio.ini` r.23 |
| `P_LORA_RESET` | `39` | `platformio.ini` r.27 |
| `P_LORA_SCLK` | `11` | `platformio.ini` r.22 |
| `P_LORA_TX_LED` | `46` | `platformio.ini` r.28 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_STATUS_LED` | `3` | `platformio.ini` r.13 |
| `PIN_USER_BTN_ANA` | `4` | `platformio.ini` r.12 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `ETH_CS_PIN` | `21` | `platformio.ini` r.47 |
| `ETH_INT_PIN` | `45` | `platformio.ini` r.48 |
| `ETH_MISO_PIN` | `14` | `platformio.ini` r.44 |
| `ETH_MOSI_PIN` | `48` | `platformio.ini` r.45 |
| `ETH_SCLK_PIN` | `47` | `platformio.ini` r.46 |


### `thinknode_m9`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `LORA_CS` | `39` | `variant.h` r.98 |
| `LORA_DIO0` | `41` | `variant.h` r.100 |
| `LORA_MISO` | `SPI_MISO` | `variant.h` r.96 |
| `LORA_MOSI` | `SPI_MOSI` | `variant.h` r.97 |
| `LORA_RESET` | `45` | `variant.h` r.99 |
| `LORA_SCK` | `SPI_SCK` | `variant.h` r.95 |
| `P_LORA_BUSY` | `41` | `platformio.ini` r.19 |
| `P_LORA_DIO_1` | `42` | `platformio.ini` r.23 |
| `P_LORA_MISO` | `38` | `platformio.ini` r.21 |
| `P_LORA_MOSI` | `47` | `platformio.ini` r.22 |
| `P_LORA_NSS` | `39` | `platformio.ini` r.17 |
| `P_LORA_RESET` | `45` | `platformio.ini` r.18 |
| `P_LORA_SCLK` | `40` | `platformio.ini` r.20 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `6` | `platformio.ini` r.15 |
| `PIN_BOARD_SDA` | `7` | `platformio.ini` r.16 |

**Display**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_TFT_LEDA_CTL` | `17` | `platformio.ini` r.37 |
| `PIN_TFT_RST` | `14` | `platformio.ini` r.38 |
| `PIN_TFT_VDD_CTL` | `-1` | `platformio.ini` r.36 |

**GPS**

| Signaal | Waarde | Bron |
|---|---|---|
| `GPS_RX_PIN` | `2` | `variant.h` r.36 |
| `GPS_TX_PIN` | `3` | `variant.h` r.35 |
| `PIN_GPS_EN` | `11` | `variant.h` r.4 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `platformio.ini` r.42 |
| `PIN_GPS_PPS` | `4` | `variant.h` r.33 |
| `PIN_GPS_RESET` | `5` | `variant.h` r.32 |
| `PIN_GPS_RESET_ACTIVE` | `HIGH` | `platformio.ini` r.44 |
| `PIN_GPS_RX` | `3` | `platformio.ini` r.39 |
| `PIN_GPS_STANDBY` | `10` | `variant.h` r.34 |
| `PIN_GPS_TX` | `2` | `platformio.ini` r.40 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_LED` | `13` | `variant.h` r.18 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `13` | `platformio.ini` r.47 |

**Overig**

| Signaal | Waarde | Bron |
|---|---|---|
| `LGFX_PIN_BL` | `ST7789_BL` | `variant.h` r.87 |
| `LGFX_PIN_CS` | `ST7789_CS` | `variant.h` r.86 |
| `LGFX_PIN_DC` | `ST7789_RS` | `variant.h` r.85 |
| `LGFX_PIN_MOSI` | `ST7789_SDA` | `variant.h` r.84 |
| `LGFX_PIN_SCK` | `ST7789_SCK` | `variant.h` r.83 |
| `LR1110_BUSY_PIN` | `LORA_DIO0` | `variant.h` r.105 |
| `LR1110_IRQ_PIN` | `42` | `variant.h` r.103 |
| `LR1110_NRESET_PIN` | `LORA_RESET` | `variant.h` r.104 |
| `LR1110_SPI_MISO_PIN` | `LORA_MISO` | `variant.h` r.109 |
| `LR1110_SPI_MOSI_PIN` | `LORA_MOSI` | `variant.h` r.108 |
| `LR1110_SPI_NSS_PIN` | `LORA_CS` | `variant.h` r.106 |
| `LR1110_SPI_SCK_PIN` | `LORA_SCK` | `variant.h` r.107 |
| `PIN_BUZZER` | `9` | `variant.h` r.22 |


### `xiao_c3`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `D3` | `platformio.ini` r.12 |
| `P_LORA_DIO_1` | `D1` | `platformio.ini` r.9 |
| `P_LORA_NSS` | `D4` | `platformio.ini` r.10 |
| `P_LORA_RESET` | `D2` | `platformio.ini` r.11 |
| `SX126X_RXEN` | `D5` | `platformio.ini` r.20 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `D7` | `platformio.ini` r.14 |
| `PIN_BOARD_SDA` | `D6` | `platformio.ini` r.13 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `D0` | `platformio.ini` r.8 |


### `xiao_c6`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `21` | `platformio.ini` r.17 |
| `P_LORA_DIO_1` | `1` | `platformio.ini` r.16 |
| `P_LORA_MISO` | `20` | `platformio.ini` r.13 |
| `P_LORA_MOSI` | `18` | `platformio.ini` r.14 |
| `P_LORA_NSS` | `22` | `platformio.ini` r.15 |
| `P_LORA_RESET` | `2` | `platformio.ini` r.18 |
| `P_LORA_SCLK` | `19` | `platformio.ini` r.12 |
| `P_LORA_TX_LED` | `15` | `platformio.ini` r.11 |
| `SX126X_RXEN` | `23` | `platformio.ini` r.21 |
| `SX126X_TXEN` | `3` | `platformio.ini` r.144 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` r.20 |
| `PIN_BOARD_SDA` | `16` | `platformio.ini` r.19 |


### `xiao_s3`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `4` | `platformio.ini` r.15 |
| `P_LORA_DIO_1` | `2` | `platformio.ini` r.12 |
| `P_LORA_MISO` | `8` | `platformio.ini` r.17 |
| `P_LORA_MOSI` | `9` | `platformio.ini` r.18 |
| `P_LORA_NSS` | `5` | `platformio.ini` r.13 |
| `P_LORA_RESET` | `3` | `platformio.ini` r.14 |
| `P_LORA_SCLK` | `7` | `platformio.ini` r.16 |
| `SX126X_RXEN` | `6` | `platformio.ini` r.23 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `platformio.ini` r.24 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `D7` | `platformio.ini` r.22 |
| `PIN_BOARD_SDA` | `D6` | `platformio.ini` r.21 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_STATUS_LED` | `21` | `platformio.ini` r.20 |
| `PIN_USER_BTN` | `-1` | `platformio.ini` r.19 |

**Voeding en accu**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` r.11 |


### `xiao_s3_wio`

**LoRa-radio**

| Signaal | Waarde | Bron |
|---|---|---|
| `P_LORA_BUSY` | `40` | `platformio.ini` r.14 |
| `P_LORA_DIO_1` | `39` | `platformio.ini` r.11 |
| `P_LORA_MISO` | `8` | `platformio.ini` r.16 |
| `P_LORA_MOSI` | `9` | `platformio.ini` r.17 |
| `P_LORA_NSS` | `41` | `platformio.ini` r.12 |
| `P_LORA_RESET` | `42` | `platformio.ini` r.13 |
| `P_LORA_SCLK` | `7` | `platformio.ini` r.15 |
| `SX126X_RXEN` | `38` | `platformio.ini` r.22 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `platformio.ini` r.23 |

**I2C**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_BOARD_SCL` | `D5` | `platformio.ini` r.21 |
| `PIN_BOARD_SDA` | `D4` | `platformio.ini` r.20 |

**Knoppen en LED**

| Signaal | Waarde | Bron |
|---|---|---|
| `PIN_STATUS_LED` | `48` | `platformio.ini` r.19 |
| `PIN_USER_BTN` | `21` | `platformio.ini` r.18 |

## Bronnen

- [`variants/`](https://github.com/meshcore-dev/MeshCore/tree/d92964352441e53b93e8667b802e04f6e072b39e/variants)
  — 43 mappen van deze familie, elk met `platformio.ini` en de headers
  ernaast
- [`tools/variant-pins.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/variant-pins.py) — het script dat deze
  tabellen maakt

Verwant in deze documentatie:

- [Nodematrix](../node-matrix.md) — welke apparaten er te koop zijn
- [MeshCore Platforms](../platforms.md) — waarom het platform uitmaakt
- [De vier platformfamilies](../platform-families.md) — wat er per familie in
  de chip zit
