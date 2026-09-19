# Pin assignments — ESP32

*43 VARIANTS · SIGNAL NAME · GPIO · SOURCE LINE*

Which pin of the ESP32 connects to what, per variant in the firmware repo.
This is a reference page for anyone who builds, measures or wants to
understand a board — which device you can buy is in
[Node matrix](../node-matrix.md), and what sits inside the chip per family is
in [The four platform families](../platform-families.md).

> [!NOTE]
> **Source.** MeshCore v1.17.1, commit
> [`d929643`](https://github.com/meshcore-dev/MeshCore/blob/d92964352441e53b93e8667b802e04f6e072b39e), 14 August 2026 — `variants/*/platformio.ini` and the
> headers in the same directory. Reproduce with
> [`tools/variant-pins.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/variant-pins.py):
>
> ```bash
> python3 tools/variant-pins.py --repo ../MeshCore \
>     --familie ESP32 --markdown --taal en --kopniveau 3
> ```
>
> Commented-out lines do not count. A `#define` inside `#if 0` does: the
> script cannot tell the difference.

## How to read these tables

Per variant the signals are grouped: LoRa radio, I2C, SPI, display, GPS,
buttons and LED, power and battery, and whatever falls outside that. Each
line names the file and line number where the definition sits, so you can
check it yourself.

The value is sometimes not a number but another name — `P_LORA_NSS` then
points at `LORA_CS`, which sits a few lines up with the real number. The
first occurrence wins: if a name appears twice, the second is an alias.

Constants that look like a pin but are not do not appear in the table.
`LORA_TX_POWER`, `SX126X_DIO3_TCXO_VOLTAGE` and `BLE_PIN_CODE` are radio and
firmware settings; the script reports them separately.

Nearly all ESP32 variants put their pins in the `build_flags` of
`platformio.ini`, as `-D P_LORA_NSS=8`. Across the forty-three variants, 948
signals come from there and 149 from a header. The value is a bare GPIO
number: `8` is GPIO8.

## The variants

### `ebyte_eora_s3`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `34` | `platformio.ini` l.11 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.8 |
| `P_LORA_MISO` | `3` | `platformio.ini` l.13 |
| `P_LORA_MOSI` | `6` | `platformio.ini` l.14 |
| `P_LORA_NSS` | `7` | `platformio.ini` l.9 |
| `P_LORA_RESET` | `8` | `platformio.ini` l.10 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.12 |
| `P_LORA_TX_LED` | `37` | `platformio.ini` l.15 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` l.19 |
| `PIN_BOARD_SDA` | `18` | `platformio.ini` l.18 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.17 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` l.16 |


### `generic-e22`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `SX126X_CS` | `variant.h` l.40 |
| `LORA_DIO1` | `SX126X_DIO1` | `variant.h` l.44 |
| `LORA_MISO` | `SX126X_MISO` | `variant.h` l.43 |
| `LORA_MOSI` | `SX126X_MOSI` | `variant.h` l.42 |
| `LORA_SCK` | `SX126X_SCK` | `variant.h` l.41 |
| `P_LORA_BUSY` | `32` | `platformio.ini` l.13 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.10 |
| `P_LORA_MISO` | `19` | `platformio.ini` l.16 |
| `P_LORA_MOSI` | `27` | `platformio.ini` l.15 |
| `P_LORA_NSS` | `18` | `platformio.ini` l.11 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` l.12 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.14 |
| `P_LORA_TX_LED` | `2` | `platformio.ini` l.8 |
| `SX126X_BUSY` | `32` | `variant.h` l.30 |
| `SX126X_CS` | `18` | `variant.h` l.25 |
| `SX126X_DIO1` | `33` | `variant.h` l.31 |
| `SX126X_MAX_POWER` | `22` | `variant.h` l.22 |
| `SX126X_MISO` | `19` | `variant.h` l.28 |
| `SX126X_MOSI` | `27` | `variant.h` l.27 |
| `SX126X_RESET` | `23` | `variant.h` l.29 |
| `SX126X_RXEN` | `14` | `variant.h` l.38 |
| `SX126X_SCK` | `5` | `variant.h` l.26 |
| `SX126X_TXEN` | `13` | `variant.h` l.37 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` l.20 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` l.19 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `GPS_RX_PIN` | `12` | `variant.h` l.7 |
| `GPS_TX_PIN` | `15` | `variant.h` l.6 |
| `PIN_GPS_EN` | `4` | `variant.h` l.8 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `39` | `variant.h` l.11 |
| `LED_PIN` | `2` | `variant.h` l.17 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `35` | `variant.h` l.12 |
| `PIN_VBAT_READ` | `35` | `platformio.ini` l.9 |


### `generic_espnow`

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `-1` | `platformio.ini` l.13 |
| `PIN_BOARD_SDA` | `-1` | `platformio.ini` l.12 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.15 |


### `heltec_ct62`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `4` | `platformio.ini` l.23 |
| `P_LORA_DIO_0` | `RADIOLIB_NC` | `platformio.ini` l.21 |
| `P_LORA_DIO_1` | `3` | `platformio.ini` l.18 |
| `P_LORA_DIO_2` | `RADIOLIB_NC` | `platformio.ini` l.22 |
| `P_LORA_MISO` | `6` | `platformio.ini` l.25 |
| `P_LORA_MOSI` | `7` | `platformio.ini` l.26 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.19 |
| `P_LORA_RESET` | `5` | `platformio.ini` l.20 |
| `P_LORA_SCLK` | `10` | `platformio.ini` l.24 |
| `P_LORA_TX_LED` | `18` | `platformio.ini` l.13 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `1` | `platformio.ini` l.15 |
| `PIN_BOARD_SDA` | `0` | `platformio.ini` l.14 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `2` | `platformio.ini` l.17 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_DIGITAL_IN` | `19` | `platformio.ini` l.146 |
| `PIN_BOARD_RELAY_CH1` | `0` | `platformio.ini` l.144 |
| `PIN_BOARD_RELAY_CH2` | `1` | `platformio.ini` l.145 |


### `heltec_e213`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.15 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.12 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.17 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.18 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.13 |
| `P_LORA_RESET` | `12` | `platformio.ini` l.14 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.16 |
| `P_LORA_TX_LED` | `45` | `platformio.ini` l.19 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `38` | `platformio.ini` l.31 |
| `PIN_BOARD_SDA` | `39` | `platformio.ini` l.30 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.21 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `7` | `platformio.ini` l.24 |
| `PIN_VEXT_EN` | `18` | `platformio.ini` l.22 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` l.23 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_ADC_CTRL` | `46` | `platformio.ini` l.25 |


### `heltec_e290`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.13 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.18 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.19 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.14 |
| `P_LORA_RESET` | `12` | `platformio.ini` l.15 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.17 |
| `P_LORA_TX_LED` | `45` | `platformio.ini` l.20 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `38` | `platformio.ini` l.31 |
| `PIN_BOARD_SDA` | `39` | `platformio.ini` l.30 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.21 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `7` | `platformio.ini` l.24 |
| `PIN_VEXT_EN` | `18` | `platformio.ini` l.22 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` l.23 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_ADC_CTRL` | `46` | `platformio.ini` l.25 |


### `heltec_rc32`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `10` | `variant.h` l.14 |
| `LORA_DIO0` | `RADIOLIB_NC` | `variant.h` l.15 |
| `LORA_DIO1` | `14` | `variant.h` l.16 |
| `LORA_MISO` | `13` | `variant.h` l.12 |
| `LORA_MOSI` | `12` | `variant.h` l.13 |
| `LORA_RESET` | `9` | `variant.h` l.17 |
| `LORA_SCK` | `11` | `variant.h` l.11 |
| `P_LORA_BUSY` | `1` | `platformio.ini` l.18 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.15 |
| `P_LORA_MISO` | `13` | `platformio.ini` l.20 |
| `P_LORA_MOSI` | `12` | `platformio.ini` l.21 |
| `P_LORA_NSS` | `10` | `platformio.ini` l.16 |
| `P_LORA_RESET` | `9` | `platformio.ini` l.17 |
| `P_LORA_SCLK` | `11` | `platformio.ini` l.19 |
| `P_LORA_TX_LED` | `47` | `platformio.ini` l.29 |
| `SX126X_BUSY` | `1` | `variant.h` l.21 |
| `SX126X_CS` | `LORA_CS` | `variant.h` l.19 |
| `SX126X_DIO1` | `LORA_DIO1` | `variant.h` l.20 |
| `SX126X_REGISTER_PATCH` | `1` | `platformio.ini` l.58 |
| `SX126X_RESET` | `LORA_RESET` | `variant.h` l.22 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` l.25 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` l.24 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_BL` | `5` | `platformio.ini` l.38 |
| `PIN_TFT_BL_ACTIVE` | `HIGH` | `platformio.ini` l.39 |
| `PIN_TFT_CS` | `39` | `platformio.ini` l.33 |
| `PIN_TFT_DC` | `16` | `platformio.ini` l.34 |
| `PIN_TFT_EN` | `6` | `platformio.ini` l.36 |
| `PIN_TFT_EN_ACTIVE` | `LOW` | `platformio.ini` l.37 |
| `PIN_TFT_RST` | `4` | `platformio.ini` l.35 |
| `PIN_TFT_SCL` | `17` | `platformio.ini` l.31 |
| `PIN_TFT_SDA` | `38` | `platformio.ini` l.32 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `45` | `platformio.ini` l.43 |
| `PIN_GPS_EN_ACTIVE` | `HIGH` | `platformio.ini` l.44 |
| `PIN_GPS_PPS` | `41` | `platformio.ini` l.47 |
| `PIN_GPS_RESET` | `40` | `platformio.ini` l.45 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` l.46 |
| `PIN_GPS_RX` | `43` | `platformio.ini` l.42 |
| `PIN_GPS_TX` | `44` | `platformio.ini` l.41 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `0` | `variant.h` l.4 |
| `PIN_USER_BTN` | `0` | `platformio.ini` l.23 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `7` | `variant.h` l.24 |
| `PIN_VBAT_READ` | `7` | `platformio.ini` l.51 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `18` | `platformio.ini` l.204 |
| `ENV_PIN_SDA` | `21` | `platformio.ini` l.203 |
| `PIN_ADC_CTRL` | `15` | `platformio.ini` l.50 |
| `PIN_BUZZER` | `48` | `platformio.ini` l.30 |
| `SENSOR_INT_PIN` | `42` | `variant.h` l.8 |
| `SENSOR_POWER_CTRL_PIN` | `46` | `platformio.ini` l.26 |
| `SENSOR_RST_PIN` | `2` | `platformio.ini` l.28 |


### `heltec_t190`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.15 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.12 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.17 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.18 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.13 |
| `P_LORA_RESET` | `12` | `platformio.ini` l.14 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.16 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `1` | `platformio.ini` l.30 |
| `PIN_BOARD_SDA` | `2` | `platformio.ini` l.29 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_CS` | `39` | `platformio.ini` l.37 |
| `PIN_TFT_DC` | `47` | `platformio.ini` l.38 |
| `PIN_TFT_LEDA_CTL` | `17` | `platformio.ini` l.35 |
| `PIN_TFT_LEDA_CTL_ACTIVE` | `HIGH` | `platformio.ini` l.36 |
| `PIN_TFT_RST` | `40` | `platformio.ini` l.33 |
| `PIN_TFT_SCL` | `38` | `platformio.ini` l.31 |
| `PIN_TFT_SDA` | `48` | `platformio.ini` l.32 |
| `PIN_TFT_VDD_CTL` | `7` | `platformio.ini` l.34 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.20 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `6` | `platformio.ini` l.23 |
| `PIN_VEXT_EN` | `5` | `platformio.ini` l.21 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` l.22 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_ADC_CTRL` | `46` | `platformio.ini` l.24 |


### `heltec_tracker`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.13 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.10 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.15 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.16 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.11 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` l.12 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.14 |
| `P_LORA_TX_LED` | `18` | `platformio.ini` l.21 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `46` | `platformio.ini` l.23 |
| `PIN_BOARD_SDA` | `45` | `platformio.ini` l.22 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_CS` | `38` | `platformio.ini` l.30 |
| `PIN_TFT_DC` | `40` | `platformio.ini` l.28 |
| `PIN_TFT_LEDA_CTL` | `21` | `platformio.ini` l.33 |
| `PIN_TFT_RST` | `39` | `platformio.ini` l.29 |
| `PIN_TFT_SCL` | `41` | `platformio.ini` l.27 |
| `PIN_TFT_SDA` | `42` | `platformio.ini` l.26 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `35` | `platformio.ini` l.36 |
| `PIN_GPS_RESET` | `36` | `platformio.ini` l.37 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` l.38 |
| `PIN_GPS_RX` | `33` | `platformio.ini` l.34 |
| `PIN_GPS_TX` | `34` | `platformio.ini` l.35 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.24 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VEXT_EN` | `3` | `platformio.ini` l.32 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_ADC_CTRL` | `2` | `platformio.ini` l.25 |
| `USE_PIN_TFT` | `1` | `platformio.ini` l.31 |


### `heltec_tracker_v2`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.17 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.14 |
| `P_LORA_KCT8103L_PA_CSD` | `4` | `platformio.ini` l.22 |
| `P_LORA_KCT8103L_PA_CTX` | `5` | `platformio.ini` l.23 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.19 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.20 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.15 |
| `P_LORA_PA_POWER` | `7` | `platformio.ini` l.21 |
| `P_LORA_RESET` | `12` | `platformio.ini` l.16 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.18 |
| `P_LORA_TX_LED` | `18` | `platformio.ini` l.13 |
| `SX126X_REGISTER_PATCH` | `1` | `platformio.ini` l.30 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` l.32 |
| `PIN_BOARD_SDA` | `6` | `platformio.ini` l.31 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_CS` | `38` | `platformio.ini` l.38 |
| `PIN_TFT_DC` | `40` | `platformio.ini` l.36 |
| `PIN_TFT_LEDA_CTL` | `21` | `platformio.ini` l.42 |
| `PIN_TFT_RST` | `39` | `platformio.ini` l.37 |
| `PIN_TFT_SCL` | `41` | `platformio.ini` l.35 |
| `PIN_TFT_SDA` | `42` | `platformio.ini` l.34 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_RESET` | `35` | `platformio.ini` l.46 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` l.47 |
| `PIN_GPS_RX` | `34` | `platformio.ini` l.44 |
| `PIN_GPS_TX` | `33` | `platformio.ini` l.45 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.33 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` l.51 |
| `PIN_VEXT_EN` | `3` | `platformio.ini` l.40 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` l.41 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_ADC_CTRL` | `2` | `platformio.ini` l.50 |
| `USE_PIN_TFT` | `1` | `platformio.ini` l.39 |


### `heltec_v2`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` l.10 |
| `P_LORA_DIO_1` | `35` | `platformio.ini` l.11 |
| `P_LORA_MISO` | `19` | `platformio.ini` l.15 |
| `P_LORA_MOSI` | `27` | `platformio.ini` l.16 |
| `P_LORA_NSS` | `18` | `platformio.ini` l.12 |
| `P_LORA_RESET` | `14` | `platformio.ini` l.13 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.14 |
| `P_LORA_TX_LED` | `25` | `platformio.ini` l.17 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `15` | `platformio.ini` l.21 |
| `PIN_BOARD_SDA` | `4` | `platformio.ini` l.20 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_LED_BUILTIN` | `25` | `HeltecV2Board.h` l.8 |
| `PIN_USER_BTN` | `0` | `platformio.ini` l.22 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `37` | `HeltecV2Board.h` l.7 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_OLED_RESET` | `16` | `platformio.ini` l.23 |


### `heltec_v3`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.13 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.10 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.15 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.16 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.11 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` l.12 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.14 |
| `P_LORA_TX_LED` | `35` | `platformio.ini` l.21 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` l.23 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` l.22 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `26` | `platformio.ini` l.32 |
| `PIN_GPS_RX` | `47` | `platformio.ini` l.30 |
| `PIN_GPS_TX` | `48` | `platformio.ini` l.31 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.24 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `HeltecV3Board.h` l.9 |
| `PIN_VEXT_EN` | `36` | `platformio.ini` l.25 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `34` | `platformio.ini` l.216 |
| `ENV_PIN_SDA` | `33` | `platformio.ini` l.215 |
| `PIN_ADC_CTRL` | `37` | `HeltecV3Board.h` l.12 |
| `PIN_ADC_CTRL_ACTIVE` | `LOW` | `HeltecV3Board.h` l.17 |
| `PIN_ADC_CTRL_INACTIVE` | `HIGH` | `HeltecV3Board.h` l.18 |


### `heltec_v4`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.17 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.14 |
| `P_LORA_GC1109_PA_EN` | `2` | `platformio.ini` l.22 |
| `P_LORA_GC1109_PA_TX_EN` | `46` | `platformio.ini` l.23 |
| `P_LORA_KCT8103L_PA_CSD` | `2` | `platformio.ini` l.24 |
| `P_LORA_KCT8103L_PA_CTX` | `5` | `platformio.ini` l.25 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.19 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.20 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.15 |
| `P_LORA_PA_POWER` | `7` | `platformio.ini` l.21 |
| `P_LORA_RESET` | `12` | `platformio.ini` l.16 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.18 |
| `P_LORA_TX_LED` | `35` | `platformio.ini` l.13 |
| `SX126X_REGISTER_PATCH` | `1` | `platformio.ini` l.31 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` l.58 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` l.57 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_CS` | `15` | `platformio.ini` l.76 |
| `PIN_TFT_DC` | `16` | `platformio.ini` l.77 |
| `PIN_TFT_LEDA_CTL` | `21` | `platformio.ini` l.74 |
| `PIN_TFT_LEDA_CTL_ACTIVE` | `HIGH` | `platformio.ini` l.75 |
| `PIN_TFT_RST` | `18` | `platformio.ini` l.72 |
| `PIN_TFT_SCL` | `17` | `platformio.ini` l.78 |
| `PIN_TFT_SDA` | `33` | `platformio.ini` l.79 |
| `PIN_TFT_VDD_CTL` | `-1` | `platformio.ini` l.73 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `34` | `platformio.ini` l.40 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `platformio.ini` l.41 |
| `PIN_GPS_RESET` | `42` | `platformio.ini` l.38 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` l.39 |
| `PIN_GPS_RX` | `38` | `platformio.ini` l.36 |
| `PIN_GPS_TX` | `39` | `platformio.ini` l.37 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.26 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` l.44 |
| `PIN_VEXT_EN` | `36` | `platformio.ini` l.27 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` l.28 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `3` | `platformio.ini` l.118 |
| `ENV_PIN_SDA` | `4` | `platformio.ini` l.117 |
| `PIN_ADC_CTRL` | `37` | `platformio.ini` l.43 |
| `PIN_OLED_RESET` | `21` | `platformio.ini` l.59 |


### `heltec_v4_r8`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.13 |
| `P_LORA_KCT8103L_PA_CSD` | `2` | `platformio.ini` l.21 |
| `P_LORA_KCT8103L_PA_CTX` | `5` | `platformio.ini` l.22 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.18 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.19 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.14 |
| `P_LORA_PA_POWER` | `7` | `platformio.ini` l.20 |
| `P_LORA_RESET` | `12` | `platformio.ini` l.15 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.17 |
| `P_LORA_TX_LED` | `46` | `platformio.ini` l.23 |
| `SX126X_REGISTER_PATCH` | `1` | `platformio.ini` l.31 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` l.54 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` l.53 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_CS` | `47` | `platformio.ini` l.72 |
| `PIN_TFT_DC` | `48` | `platformio.ini` l.73 |
| `PIN_TFT_LEDA_CTL` | `44` | `platformio.ini` l.70 |
| `PIN_TFT_LEDA_CTL_ACTIVE` | `HIGH` | `platformio.ini` l.71 |
| `PIN_TFT_MISO` | `45` | `platformio.ini` l.76 |
| `PIN_TFT_RST` | `-1` | `platformio.ini` l.68 |
| `PIN_TFT_SCL` | `16` | `platformio.ini` l.74 |
| `PIN_TFT_SDA` | `15` | `platformio.ini` l.75 |
| `PIN_TFT_VDD_CTL` | `-1` | `platformio.ini` l.69 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `42` | `platformio.ini` l.38 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `platformio.ini` l.39 |
| `PIN_GPS_RX` | `38` | `platformio.ini` l.36 |
| `PIN_GPS_TX` | `39` | `platformio.ini` l.37 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.24 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` l.28 |
| `PIN_VEXT_EN` | `40` | `platformio.ini` l.25 |
| `PIN_VEXT_EN_ACTIVE` | `LOW` | `platformio.ini` l.26 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUZZER` | `4` | `platformio.ini` l.77 |
| `PIN_OLED_RESET` | `21` | `platformio.ini` l.55 |
| `PIN_TOUCH_RST` | `21` | `platformio.ini` l.78 |


### `heltec_wireless_paper`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.12 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.9 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.14 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.15 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.10 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` l.11 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.13 |
| `P_LORA_TX_LED` | `18` | `platformio.ini` l.20 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.23 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `20` | `platformio.ini` l.26 |
| `PIN_VEXT_EN` | `45` | `platformio.ini` l.24 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_ADC_CTRL` | `19` | `platformio.ini` l.27 |


### `lilygo_t3s3`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `34` | `platformio.ini` l.11 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.8 |
| `P_LORA_MISO` | `3` | `platformio.ini` l.13 |
| `P_LORA_MOSI` | `6` | `platformio.ini` l.14 |
| `P_LORA_NSS` | `7` | `platformio.ini` l.9 |
| `P_LORA_RESET` | `8` | `platformio.ini` l.10 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.12 |
| `P_LORA_TX_LED` | `37` | `platformio.ini` l.15 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` l.19 |
| `PIN_BOARD_SDA` | `18` | `platformio.ini` l.18 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.17 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` l.16 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_OLED_RESET` | `21` | `platformio.ini` l.21 |


### `lilygo_t3s3_sx1276`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_DIO_0` | `9` | `platformio.ini` l.8 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.9 |
| `P_LORA_MISO` | `3` | `platformio.ini` l.13 |
| `P_LORA_MOSI` | `6` | `platformio.ini` l.14 |
| `P_LORA_NSS` | `7` | `platformio.ini` l.10 |
| `P_LORA_RESET` | `8` | `platformio.ini` l.11 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.12 |
| `P_LORA_TX_LED` | `37` | `platformio.ini` l.15 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` l.19 |
| `PIN_BOARD_SDA` | `18` | `platformio.ini` l.18 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.17 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` l.16 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_OLED_RESET` | `21` | `platformio.ini` l.20 |


### `lilygo_tbeam_1w`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_BUSY` | `38` | `variant.h` l.44 |
| `LORA_CS` | `15` | `variant.h` l.41 |
| `LORA_DIO1` | `1` | `variant.h` l.43 |
| `LORA_MISO` | `SPI_MISO` | `variant.h` l.39 |
| `LORA_MOSI` | `SPI_MOSI` | `variant.h` l.40 |
| `LORA_RESET` | `3` | `variant.h` l.42 |
| `LORA_SCK` | `SPI_SCK` | `variant.h` l.38 |
| `P_LORA_BUSY` | `38` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `1` | `platformio.ini` l.13 |
| `P_LORA_MISO` | `12` | `platformio.ini` l.18 |
| `P_LORA_MOSI` | `11` | `platformio.ini` l.19 |
| `P_LORA_NSS` | `15` | `platformio.ini` l.14 |
| `P_LORA_RESET` | `3` | `platformio.ini` l.15 |
| `P_LORA_SCLK` | `13` | `platformio.ini` l.17 |
| `SX126X_BUSY` | `LORA_BUSY` | `variant.h` l.53 |
| `SX126X_CS` | `LORA_CS` | `variant.h` l.51 |
| `SX126X_DIO1` | `LORA_DIO1` | `variant.h` l.52 |
| `SX126X_MAX_POWER` | `22` | `variant.h` l.67 |
| `SX126X_PA_RAMP_US` | `0x05` | `variant.h` l.88 |
| `SX126X_POWER_EN` | `40` | `variant.h` l.48 |
| `SX126X_RESET` | `LORA_RESET` | `variant.h` l.54 |
| `SX126X_RXEN` | `21` | `variant.h` l.62 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `9` | `platformio.ini` l.43 |
| `PIN_BOARD_SDA` | `8` | `platformio.ini` l.42 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `16` | `variant.h` l.16 |
| `PIN_GPS_PPS` | `7` | `variant.h` l.15 |
| `PIN_GPS_RX` | `6` | `variant.h` l.14 |
| `PIN_GPS_TX` | `5` | `variant.h` l.13 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `0` | `variant.h` l.21 |
| `BUTTON_PIN_ALT` | `17` | `variant.h` l.22 |
| `LED_PIN` | `18` | `variant.h` l.71 |
| `PIN_USER_BTN` | `17` | `platformio.ini` l.54 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `4` | `variant.h` l.75 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `FAN_CTRL_PIN` | `41` | `variant.h` l.84 |
| `NTC_PIN` | `14` | `variant.h` l.81 |


### `lilygo_tbeam_SX1262`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` l.8 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.9 |
| `P_LORA_MISO` | `19` | `platformio.ini` l.13 |
| `P_LORA_MOSI` | `27` | `platformio.ini` l.14 |
| `P_LORA_NSS` | `18` | `platformio.ini` l.10 |
| `P_LORA_RESET` | `23` | `platformio.ini` l.11 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.12 |
| `P_LORA_TX_LED` | `4` | `platformio.ini` l.24 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` l.26 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` l.25 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_RX` | `12` | `platformio.ini` l.27 |
| `PIN_GPS_TX` | `34` | `platformio.ini` l.28 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` l.29 |


### `lilygo_tbeam_SX1276`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` l.8 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.9 |
| `P_LORA_MISO` | `19` | `platformio.ini` l.13 |
| `P_LORA_MOSI` | `27` | `platformio.ini` l.14 |
| `P_LORA_NSS` | `18` | `platformio.ini` l.10 |
| `P_LORA_RESET` | `23` | `platformio.ini` l.11 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.12 |
| `P_LORA_TX_LED` | `4` | `platformio.ini` l.20 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` l.22 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` l.21 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_RX` | `12` | `platformio.ini` l.23 |
| `PIN_GPS_TX` | `34` | `platformio.ini` l.24 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` l.25 |


### `lilygo_tbeam_supreme_SX1262`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` l.8 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.9 |
| `P_LORA_MISO` | `19` | `platformio.ini` l.13 |
| `P_LORA_MOSI` | `27` | `platformio.ini` l.14 |
| `P_LORA_NSS` | `18` | `platformio.ini` l.10 |
| `P_LORA_RESET` | `23` | `platformio.ini` l.11 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.12 |
| `P_LORA_TX_LED` | `6` | `platformio.ini` l.23 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` l.25 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` l.24 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `7` | `platformio.ini` l.28 |
| `PIN_GPS_RX` | `8` | `platformio.ini` l.26 |
| `PIN_GPS_TX` | `9` | `platformio.ini` l.27 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.29 |


### `lilygo_tdeck`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.40 |
| `P_LORA_DIO_1` | `45` | `platformio.ini` l.22 |
| `P_LORA_MISO` | `38` | `platformio.ini` l.42 |
| `P_LORA_MOSI` | `41` | `platformio.ini` l.43 |
| `P_LORA_NSS` | `9` | `platformio.ini` l.38 |
| `P_LORA_RESET` | `17` | `platformio.ini` l.39 |
| `P_LORA_SCLK` | `40` | `platformio.ini` l.41 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_CS` | `12` | `platformio.ini` l.50 |
| `PIN_TFT_DC` | `11` | `platformio.ini` l.51 |
| `PIN_TFT_LEDA_CTL` | `42` | `platformio.ini` l.49 |
| `PIN_TFT_RST` | `-1` | `platformio.ini` l.47 |
| `PIN_TFT_SCL` | `40` | `platformio.ini` l.52 |
| `PIN_TFT_SDA` | `41` | `platformio.ini` l.53 |
| `PIN_TFT_VDD_CTL` | `-1` | `platformio.ini` l.48 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_RX` | `43` | `platformio.ini` l.54 |
| `PIN_GPS_TX` | `44` | `platformio.ini` l.55 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.12 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `4` | `TDeckBoard.h` l.7 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_PERF_POWERON` | `10` | `platformio.ini` l.13 |


### `lilygo_teth_elite`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `16` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `8` | `platformio.ini` l.13 |
| `P_LORA_MISO` | `9` | `platformio.ini` l.18 |
| `P_LORA_MOSI` | `11` | `platformio.ini` l.19 |
| `P_LORA_NSS` | `40` | `platformio.ini` l.14 |
| `P_LORA_RESET` | `46` | `platformio.ini` l.15 |
| `P_LORA_SCLK` | `10` | `platformio.ini` l.17 |
| `P_LORA_TX_LED` | `38` | `platformio.ini` l.20 |


### `lilygo_tlora_c6`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `22` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `23` | `platformio.ini` l.15 |
| `P_LORA_MISO` | `1` | `platformio.ini` l.12 |
| `P_LORA_MOSI` | `0` | `platformio.ini` l.13 |
| `P_LORA_NSS` | `18` | `platformio.ini` l.14 |
| `P_LORA_RESET` | `21` | `platformio.ini` l.17 |
| `P_LORA_SCLK` | `6` | `platformio.ini` l.11 |
| `P_LORA_TX_LED` | `7` | `platformio.ini` l.10 |
| `SX126X_RXEN` | `15` | `platformio.ini` l.20 |
| `SX126X_TXEN` | `14` | `platformio.ini` l.21 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `9` | `platformio.ini` l.19 |
| `PIN_BOARD_SDA` | `8` | `platformio.ini` l.18 |


### `lilygo_tlora_v2_1`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_DIO_0` | `26` | `platformio.ini` l.14 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.15 |
| `P_LORA_MISO` | `19` | `platformio.ini` l.19 |
| `P_LORA_MOSI` | `27` | `platformio.ini` l.20 |
| `P_LORA_NSS` | `18` | `platformio.ini` l.16 |
| `P_LORA_RESET` | `14` | `platformio.ini` l.17 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.18 |
| `P_LORA_TX_LED` | `25` | `platformio.ini` l.21 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` l.23 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` l.22 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.25 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `35` | `platformio.ini` l.24 |


### `m5stack_unit_c6l`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `19` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `7` | `platformio.ini` l.15 |
| `P_LORA_MISO` | `22` | `platformio.ini` l.12 |
| `P_LORA_MOSI` | `21` | `platformio.ini` l.13 |
| `P_LORA_NSS` | `23` | `platformio.ini` l.14 |
| `P_LORA_RESET` | `-1` | `platformio.ini` l.17 |
| `P_LORA_SCLK` | `20` | `platformio.ini` l.11 |
| `P_LORA_TX_LED` | `15` | `platformio.ini` l.10 |
| `SX126X_RXEN` | `5` | `platformio.ini` l.21 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` l.20 |
| `PIN_BOARD_SDA` | `16` | `platformio.ini` l.19 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUZZER` | `11` | `platformio.ini` l.18 |


### `meshadventurer`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `SX126X_CS` | `variant.h` l.40 |
| `LORA_DIO1` | `SX126X_DIO1` | `variant.h` l.44 |
| `LORA_MISO` | `SX126X_MISO` | `variant.h` l.43 |
| `LORA_MOSI` | `SX126X_MOSI` | `variant.h` l.42 |
| `LORA_SCK` | `SX126X_SCK` | `variant.h` l.41 |
| `P_LORA_BUSY` | `32` | `platformio.ini` l.15 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.12 |
| `P_LORA_MISO` | `19` | `platformio.ini` l.18 |
| `P_LORA_MOSI` | `27` | `platformio.ini` l.17 |
| `P_LORA_NSS` | `18` | `platformio.ini` l.13 |
| `P_LORA_RESET` | `23` | `platformio.ini` l.14 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.16 |
| `P_LORA_TX_LED` | `2` | `platformio.ini` l.9 |
| `SX126X_BUSY` | `32` | `variant.h` l.30 |
| `SX126X_CS` | `18` | `variant.h` l.25 |
| `SX126X_DIO1` | `33` | `variant.h` l.31 |
| `SX126X_MAX_POWER` | `22` | `variant.h` l.22 |
| `SX126X_MISO` | `19` | `variant.h` l.28 |
| `SX126X_MOSI` | `27` | `variant.h` l.27 |
| `SX126X_RESET` | `23` | `variant.h` l.29 |
| `SX126X_RXEN` | `14` | `variant.h` l.38 |
| `SX126X_SCK` | `5` | `variant.h` l.26 |
| `SX126X_TXEN` | `13` | `variant.h` l.37 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `22` | `platformio.ini` l.22 |
| `PIN_BOARD_SDA` | `21` | `platformio.ini` l.21 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `GPS_RX_PIN` | `12` | `variant.h` l.7 |
| `GPS_TX_PIN` | `15` | `variant.h` l.6 |
| `PIN_GPS_EN` | `4` | `variant.h` l.8 |
| `PIN_GPS_RX` | `12` | `platformio.ini` l.26 |
| `PIN_GPS_TX` | `15` | `platformio.ini` l.27 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `39` | `variant.h` l.11 |
| `LED_PIN` | `2` | `variant.h` l.17 |
| `PIN_USER_BTN` | `39` | `platformio.ini` l.11 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `35` | `variant.h` l.12 |
| `PIN_VBAT_READ` | `35` | `platformio.ini` l.10 |


### `meshnology_w12`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.22 |
| `P_LORA_DIO_1` | `14` | `platformio.ini` l.15 |
| `P_LORA_HF_PA_POWER` | `3` | `platformio.ini` l.26 |
| `P_LORA_LF_PA_POWER` | `4` | `platformio.ini` l.25 |
| `P_LORA_MISO` | `11` | `platformio.ini` l.20 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.19 |
| `P_LORA_NSS` | `8` | `platformio.ini` l.17 |
| `P_LORA_RESET` | `12` | `platformio.ini` l.21 |
| `P_LORA_SCLK` | `9` | `platformio.ini` l.18 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `18` | `platformio.ini` l.42 |
| `PIN_BOARD_SDA` | `17` | `platformio.ini` l.41 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `48` | `platformio.ini` l.36 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `platformio.ini` l.37 |
| `PIN_GPS_RESET` | `42` | `platformio.ini` l.34 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` l.35 |
| `PIN_GPS_RX` | `38` | `platformio.ini` l.32 |
| `PIN_GPS_TX` | `39` | `platformio.ini` l.33 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `0` | `platformio.ini` l.27 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` l.39 |
| `PIN_VEXT_EN` | `45` | `platformio.ini` l.28 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` l.29 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `4` | `platformio.ini` l.202 |
| `ENV_PIN_SDA` | `3` | `platformio.ini` l.201 |
| `PIN_ADC_CTRL` | `2` | `platformio.ini` l.40 |
| `PIN_RESET` | `47` | `platformio.ini` l.43 |


### `nibble_screen_connect`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `5` | `platformio.ini` l.11 |
| `P_LORA_DIO_1` | `4` | `platformio.ini` l.8 |
| `P_LORA_MISO` | `12` | `platformio.ini` l.13 |
| `P_LORA_MOSI` | `11` | `platformio.ini` l.14 |
| `P_LORA_NSS` | `10` | `platformio.ini` l.9 |
| `P_LORA_RESET` | `6` | `platformio.ini` l.10 |
| `P_LORA_SCLK` | `13` | `platformio.ini` l.12 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `7` | `platformio.ini` l.17 |
| `PIN_BOARD_SDA` | `8` | `platformio.ini` l.16 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `1` | `platformio.ini` l.15 |


### `nibble_zero_connect`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `5` | `platformio.ini` l.11 |
| `P_LORA_DIO_1` | `4` | `platformio.ini` l.8 |
| `P_LORA_MISO` | `13` | `platformio.ini` l.13 |
| `P_LORA_MOSI` | `11` | `platformio.ini` l.14 |
| `P_LORA_NSS` | `10` | `platformio.ini` l.9 |
| `P_LORA_RESET` | `6` | `platformio.ini` l.10 |
| `P_LORA_SCLK` | `12` | `platformio.ini` l.12 |
| `P_LORA_TX_LED` | `39` | `platformio.ini` l.19 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `7` | `platformio.ini` l.17 |
| `PIN_BOARD_SDA` | `8` | `platformio.ini` l.16 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_STATUS_LED` | `39` | `platformio.ini` l.18 |
| `PIN_USER_BTN` | `1` | `platformio.ini` l.15 |


### `rak3112`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `48` | `platformio.ini` l.14 |
| `P_LORA_DIO_1` | `47` | `platformio.ini` l.11 |
| `P_LORA_MISO` | `3` | `platformio.ini` l.16 |
| `P_LORA_MOSI` | `6` | `platformio.ini` l.17 |
| `P_LORA_NSS` | `7` | `platformio.ini` l.12 |
| `P_LORA_RESET` | `8` | `platformio.ini` l.13 |
| `P_LORA_SCLK` | `5` | `platformio.ini` l.15 |
| `P_LORA_TX_LED` | `46` | `platformio.ini` l.22 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `40` | `platformio.ini` l.24 |
| `PIN_BOARD_SDA` | `9` | `platformio.ini` l.23 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_RX` | `43` | `platformio.ini` l.31 |
| `PIN_GPS_TX` | `44` | `platformio.ini` l.32 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `-1` | `platformio.ini` l.25 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `RAK3112Board.h` l.9 |
| `PIN_VEXT_EN` | `14` | `platformio.ini` l.26 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `34` | `platformio.ini` l.200 |
| `ENV_PIN_SDA` | `33` | `platformio.ini` l.199 |
| `PIN_ADC_CTRL` | `36` | `RAK3112Board.h` l.12 |
| `PIN_ADC_CTRL_ACTIVE` | `LOW` | `RAK3112Board.h` l.14 |
| `PIN_ADC_CTRL_INACTIVE` | `HIGH` | `RAK3112Board.h` l.15 |


### `sensecap_indicator-espnow`

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `40` | `platformio.ini` l.13 |
| `PIN_BOARD_SDA` | `39` | `platformio.ini` l.12 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` l.23 |


### `station_g2`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `47` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `48` | `platformio.ini` l.13 |
| `P_LORA_MISO` | `14` | `platformio.ini` l.18 |
| `P_LORA_MOSI` | `13` | `platformio.ini` l.19 |
| `P_LORA_NSS` | `11` | `platformio.ini` l.14 |
| `P_LORA_RESET` | `21` | `platformio.ini` l.15 |
| `P_LORA_SCLK` | `12` | `platformio.ini` l.17 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `6` | `platformio.ini` l.24 |
| `PIN_BOARD_SDA` | `5` | `platformio.ini` l.23 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_RX` | `15` | `platformio.ini` l.26 |
| `PIN_GPS_TX` | `7` | `platformio.ini` l.27 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` l.25 |


### `station_g3_esp32`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `47` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `48` | `platformio.ini` l.13 |
| `P_LORA_MISO` | `14` | `platformio.ini` l.18 |
| `P_LORA_MOSI` | `13` | `platformio.ini` l.19 |
| `P_LORA_NSS` | `11` | `platformio.ini` l.14 |
| `P_LORA_RESET` | `21` | `platformio.ini` l.15 |
| `P_LORA_SCLK` | `12` | `platformio.ini` l.17 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `6` | `platformio.ini` l.28 |
| `PIN_BOARD_SDA` | `5` | `platformio.ini` l.27 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_RX` | `15` | `platformio.ini` l.30 |
| `PIN_GPS_TX` | `7` | `platformio.ini` l.31 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `38` | `platformio.ini` l.29 |


### `tenstar_c3`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_TX_BOOST_PIN` | `4` | `platformio.ini` l.8 |
| `P_LORA_BUSY` | `3` | `platformio.ini` l.17 |
| `P_LORA_DIO_1` | `2` | `platformio.ini` l.14 |
| `P_LORA_MISO` | `9` | `platformio.ini` l.11 |
| `P_LORA_MOSI` | `7` | `platformio.ini` l.13 |
| `P_LORA_NSS` | `6` | `platformio.ini` l.15 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `platformio.ini` l.16 |
| `P_LORA_SCLK` | `8` | `platformio.ini` l.12 |
| `P_LORA_TX_NEOPIXEL_LED` | `10` | `platformio.ini` l.9 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` l.10 |


### `thinknode_m2`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `14` | `platformio.ini` l.17 |
| `P_LORA_DIO_1` | `3` | `platformio.ini` l.14 |
| `P_LORA_MISO` | `13` | `platformio.ini` l.19 |
| `P_LORA_MOSI` | `11` | `platformio.ini` l.20 |
| `P_LORA_NSS` | `10` | `platformio.ini` l.15 |
| `P_LORA_RESET` | `21` | `platformio.ini` l.16 |
| `P_LORA_SCLK` | `12` | `platformio.ini` l.18 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `15` | `platformio.ini` l.12 |
| `PIN_BOARD_SDA` | `16` | `platformio.ini` l.13 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_LED` | `6` | `variant.h` l.10 |
| `PIN_STATUS_LED` | `6` | `variant.h` l.11 |
| `PIN_USER_BTN` | `47` | `variant.h` l.9 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `17` | `variant.h` l.3 |
| `PIN_VEXT_EN` | `46` | `variant.h` l.8 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `variant.h` l.7 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUZZER` | `5` | `variant.h` l.6 |
| `PIN_PWRBTN` | `4` | `variant.h` l.12 |


### `thinknode_m5`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `5` | `platformio.ini` l.15 |
| `P_LORA_DIO_1` | `4` | `platformio.ini` l.12 |
| `P_LORA_EN` | `46` | `platformio.ini` l.11 |
| `P_LORA_MISO` | `7` | `platformio.ini` l.17 |
| `P_LORA_MOSI` | `15` | `platformio.ini` l.18 |
| `P_LORA_NSS` | `17` | `platformio.ini` l.13 |
| `P_LORA_RESET` | `6` | `platformio.ini` l.14 |
| `P_LORA_SCLK` | `16` | `platformio.ini` l.16 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `1` | `platformio.ini` l.9 |
| `PIN_BOARD_SDA` | `2` | `platformio.ini` l.10 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_DISPLAY_BUSY` | `(42)` | `variant.h` l.20 |
| `PIN_DISPLAY_CS` | `(39)` | `variant.h` l.17 |
| `PIN_DISPLAY_DC` | `(40)` | `variant.h` l.18 |
| `PIN_DISPLAY_MISO` | `(-1)` | `variant.h` l.14 |
| `PIN_DISPLAY_MOSI` | `(45)` | `variant.h` l.15 |
| `PIN_DISPLAY_RST` | `(41)` | `variant.h` l.19 |
| `PIN_DISPLAY_SCLK` | `(38)` | `variant.h` l.16 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(11)` | `variant.h` l.24 |
| `PIN_GPS_RESET` | `(13)` | `variant.h` l.25 |
| `PIN_GPS_RX` | `(20)` | `variant.h` l.26 |
| `PIN_GPS_SWITCH` | `(10)` | `variant.h` l.28 |
| `PIN_GPS_TX` | `(19)` | `variant.h` l.27 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON2` | `14` | `platformio.ini` l.20 |
| `PIN_USER_BTN` | `21` | `variant.h` l.9 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `8` | `variant.h` l.3 |
| `PIN_VEXT_EN` | `46` | `variant.h` l.8 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `variant.h` l.7 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `EXP_PIN_BACKLIGHT` | `(5)` | `variant.h` l.21 |
| `EXP_PIN_LED` | `1` | `platformio.ini` l.21 |
| `EXP_PIN_POWER` | `(4)` | `variant.h` l.22 |
| `PIN_BUZZER` | `9` | `variant.h` l.6 |
| `PIN_PWRBTN` | `14` | `variant.h` l.12 |


### `thinknode_m7`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `13` | `platformio.ini` l.21 |
| `P_LORA_DIO_1` | `38` | `platformio.ini` l.24 |
| `P_LORA_MISO` | `9` | `platformio.ini` l.25 |
| `P_LORA_MOSI` | `10` | `platformio.ini` l.26 |
| `P_LORA_NSS` | `12` | `platformio.ini` l.23 |
| `P_LORA_RESET` | `39` | `platformio.ini` l.27 |
| `P_LORA_SCLK` | `11` | `platformio.ini` l.22 |
| `P_LORA_TX_LED` | `46` | `platformio.ini` l.28 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_STATUS_LED` | `3` | `platformio.ini` l.13 |
| `PIN_USER_BTN_ANA` | `4` | `platformio.ini` l.12 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ETH_CS_PIN` | `21` | `platformio.ini` l.47 |
| `ETH_INT_PIN` | `45` | `platformio.ini` l.48 |
| `ETH_MISO_PIN` | `14` | `platformio.ini` l.44 |
| `ETH_MOSI_PIN` | `48` | `platformio.ini` l.45 |
| `ETH_SCLK_PIN` | `47` | `platformio.ini` l.46 |


### `thinknode_m9`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `39` | `variant.h` l.98 |
| `LORA_DIO0` | `41` | `variant.h` l.100 |
| `LORA_MISO` | `SPI_MISO` | `variant.h` l.96 |
| `LORA_MOSI` | `SPI_MOSI` | `variant.h` l.97 |
| `LORA_RESET` | `45` | `variant.h` l.99 |
| `LORA_SCK` | `SPI_SCK` | `variant.h` l.95 |
| `P_LORA_BUSY` | `41` | `platformio.ini` l.19 |
| `P_LORA_DIO_1` | `42` | `platformio.ini` l.23 |
| `P_LORA_MISO` | `38` | `platformio.ini` l.21 |
| `P_LORA_MOSI` | `47` | `platformio.ini` l.22 |
| `P_LORA_NSS` | `39` | `platformio.ini` l.17 |
| `P_LORA_RESET` | `45` | `platformio.ini` l.18 |
| `P_LORA_SCLK` | `40` | `platformio.ini` l.20 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `6` | `platformio.ini` l.15 |
| `PIN_BOARD_SDA` | `7` | `platformio.ini` l.16 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_LEDA_CTL` | `17` | `platformio.ini` l.37 |
| `PIN_TFT_RST` | `14` | `platformio.ini` l.38 |
| `PIN_TFT_VDD_CTL` | `-1` | `platformio.ini` l.36 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `GPS_RX_PIN` | `2` | `variant.h` l.36 |
| `GPS_TX_PIN` | `3` | `variant.h` l.35 |
| `PIN_GPS_EN` | `11` | `variant.h` l.4 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `platformio.ini` l.42 |
| `PIN_GPS_PPS` | `4` | `variant.h` l.33 |
| `PIN_GPS_RESET` | `5` | `variant.h` l.32 |
| `PIN_GPS_RESET_ACTIVE` | `HIGH` | `platformio.ini` l.44 |
| `PIN_GPS_RX` | `3` | `platformio.ini` l.39 |
| `PIN_GPS_STANDBY` | `10` | `variant.h` l.34 |
| `PIN_GPS_TX` | `2` | `platformio.ini` l.40 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_LED` | `13` | `variant.h` l.18 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `13` | `platformio.ini` l.47 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `LGFX_PIN_BL` | `ST7789_BL` | `variant.h` l.87 |
| `LGFX_PIN_CS` | `ST7789_CS` | `variant.h` l.86 |
| `LGFX_PIN_DC` | `ST7789_RS` | `variant.h` l.85 |
| `LGFX_PIN_MOSI` | `ST7789_SDA` | `variant.h` l.84 |
| `LGFX_PIN_SCK` | `ST7789_SCK` | `variant.h` l.83 |
| `LR1110_BUSY_PIN` | `LORA_DIO0` | `variant.h` l.105 |
| `LR1110_IRQ_PIN` | `42` | `variant.h` l.103 |
| `LR1110_NRESET_PIN` | `LORA_RESET` | `variant.h` l.104 |
| `LR1110_SPI_MISO_PIN` | `LORA_MISO` | `variant.h` l.109 |
| `LR1110_SPI_MOSI_PIN` | `LORA_MOSI` | `variant.h` l.108 |
| `LR1110_SPI_NSS_PIN` | `LORA_CS` | `variant.h` l.106 |
| `LR1110_SPI_SCK_PIN` | `LORA_SCK` | `variant.h` l.107 |
| `PIN_BUZZER` | `9` | `variant.h` l.22 |


### `xiao_c3`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `D3` | `platformio.ini` l.12 |
| `P_LORA_DIO_1` | `D1` | `platformio.ini` l.9 |
| `P_LORA_NSS` | `D4` | `platformio.ini` l.10 |
| `P_LORA_RESET` | `D2` | `platformio.ini` l.11 |
| `SX126X_RXEN` | `D5` | `platformio.ini` l.20 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `D7` | `platformio.ini` l.14 |
| `PIN_BOARD_SDA` | `D6` | `platformio.ini` l.13 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `D0` | `platformio.ini` l.8 |


### `xiao_c6`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `21` | `platformio.ini` l.17 |
| `P_LORA_DIO_1` | `1` | `platformio.ini` l.16 |
| `P_LORA_MISO` | `20` | `platformio.ini` l.13 |
| `P_LORA_MOSI` | `18` | `platformio.ini` l.14 |
| `P_LORA_NSS` | `22` | `platformio.ini` l.15 |
| `P_LORA_RESET` | `2` | `platformio.ini` l.18 |
| `P_LORA_SCLK` | `19` | `platformio.ini` l.12 |
| `P_LORA_TX_LED` | `15` | `platformio.ini` l.11 |
| `SX126X_RXEN` | `23` | `platformio.ini` l.21 |
| `SX126X_TXEN` | `3` | `platformio.ini` l.144 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `17` | `platformio.ini` l.20 |
| `PIN_BOARD_SDA` | `16` | `platformio.ini` l.19 |


### `xiao_s3`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `4` | `platformio.ini` l.15 |
| `P_LORA_DIO_1` | `2` | `platformio.ini` l.12 |
| `P_LORA_MISO` | `8` | `platformio.ini` l.17 |
| `P_LORA_MOSI` | `9` | `platformio.ini` l.18 |
| `P_LORA_NSS` | `5` | `platformio.ini` l.13 |
| `P_LORA_RESET` | `3` | `platformio.ini` l.14 |
| `P_LORA_SCLK` | `7` | `platformio.ini` l.16 |
| `SX126X_RXEN` | `6` | `platformio.ini` l.23 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `platformio.ini` l.24 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `D7` | `platformio.ini` l.22 |
| `PIN_BOARD_SDA` | `D6` | `platformio.ini` l.21 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_STATUS_LED` | `21` | `platformio.ini` l.20 |
| `PIN_USER_BTN` | `-1` | `platformio.ini` l.19 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `1` | `platformio.ini` l.11 |


### `xiao_s3_wio`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `40` | `platformio.ini` l.14 |
| `P_LORA_DIO_1` | `39` | `platformio.ini` l.11 |
| `P_LORA_MISO` | `8` | `platformio.ini` l.16 |
| `P_LORA_MOSI` | `9` | `platformio.ini` l.17 |
| `P_LORA_NSS` | `41` | `platformio.ini` l.12 |
| `P_LORA_RESET` | `42` | `platformio.ini` l.13 |
| `P_LORA_SCLK` | `7` | `platformio.ini` l.15 |
| `SX126X_RXEN` | `38` | `platformio.ini` l.22 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `platformio.ini` l.23 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `D5` | `platformio.ini` l.21 |
| `PIN_BOARD_SDA` | `D4` | `platformio.ini` l.20 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_STATUS_LED` | `48` | `platformio.ini` l.19 |
| `PIN_USER_BTN` | `21` | `platformio.ini` l.18 |

## Sources

- [`variants/`](https://github.com/meshcore-dev/MeshCore/tree/d92964352441e53b93e8667b802e04f6e072b39e/variants)
  — 43 directories of this family, each with a `platformio.ini` and the
  headers beside it
- [`tools/variant-pins.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/variant-pins.py) — the script that builds
  these tables

Related in this documentation:

- [Node matrix](../node-matrix.md) — which devices you can buy
- [MeshCore Platforms](../platforms.md) — why the platform matters
- [The four platform families](../platform-families.md) — what sits inside
  the chip per family
