# Pin assignments — nRF52

*36 VARIANTS · SIGNAL NAME · GPIO · SOURCE LINE*

Which pin of the nRF52 connects to what, per variant in the firmware repo.
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
>     --familie nRF52 --markdown --taal en --kopniveau 3
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

The nRF52 variants put their pins in `variant.h` or `pins_arduino.h`. Across
the thirty-six variants, 1463 signals come from a header and 430 from the
`build_flags`. Mind the notation: 149 values read `(0 + 30)` or `(32 + 10)`.
That is the port number times 32 plus the pin number, so P0.30 and P1.10.

## The variants

### `gat562_30s_mesh_kit`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(46)` | `variant.h` l.180 |
| `P_LORA_DIO_1` | `(47)` | `variant.h` l.181 |
| `P_LORA_MISO` | `(45)` | `variant.h` l.179 |
| `P_LORA_MOSI` | `(44)` | `variant.h` l.178 |
| `P_LORA_NSS` | `(42)` | `variant.h` l.176 |
| `P_LORA_RESET` | `(38)` | `variant.h` l.175 |
| `P_LORA_SCLK` | `(43)` | `variant.h` l.177 |
| `P_LORA_TX_LED` | `LED_GREEN` | `variant.h` l.82 |
| `SX126X_POWER_EN` | `(37)` | `variant.h` l.174 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `14` | `platformio.ini` l.11 |
| `PIN_BOARD_SDA` | `13` | `platformio.ini` l.12 |
| `PIN_WIRE_SCL` | `(14)` | `variant.h` l.192 |
| `PIN_WIRE_SDA` | `(13)` | `variant.h` l.191 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(29)` | `variant.h` l.163 |
| `PIN_SPI_MOSI` | `(30)` | `variant.h` l.164 |
| `PIN_SPI_SCK` | `(3)` | `variant.h` l.165 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(33)` | `variant.h` l.219 |
| `PIN_GPS_PPS` | `(17)` | `variant.h` l.220 |
| `PIN_GPS_RX` | `PIN_SERIAL1_TX` | `variant.h` l.218 |
| `PIN_GPS_TX` | `PIN_SERIAL1_RX` | `variant.h` l.217 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(9)` | `variant.h` l.88 |
| `PIN_BUTTON2` | `(28)` | `variant.h` l.89 |
| `PIN_BUTTON3` | `(4)` | `variant.h` l.90 |
| `PIN_BUTTON4` | `(30)` | `variant.h` l.91 |
| `PIN_BUTTON5` | `(31)` | `variant.h` l.92 |
| `PIN_BUTTON6` | `(26)` | `variant.h` l.93 |
| `PIN_LED1` | `(35)` | `variant.h` l.69 |
| `PIN_LED2` | `(36)` | `variant.h` l.70 |
| `PIN_LED3` | `(29)` | `variant.h` l.71 |
| `PIN_USER_BTN` | `PIN_BUTTON6` | `variant.h` l.100 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `(5)` | `variant.h` l.105 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.64 |
| `PINS_COUNT` | `(48)` | `variant.h` l.63 |
| `PIN_A0` | `(5)` | `variant.h` l.113 |
| `PIN_A1` | `(31)` | `variant.h` l.114 |
| `PIN_A2` | `(28)` | `variant.h` l.115 |
| `PIN_A3` | `(29)` | `variant.h` l.116 |
| `PIN_A4` | `(30)` | `variant.h` l.117 |
| `PIN_A5` | `(31)` | `variant.h` l.118 |
| `PIN_A6` | `(0xff)` | `variant.h` l.119 |
| `PIN_A7` | `(0xff)` | `variant.h` l.120 |
| `PIN_AREF` | `(2)` | `variant.h` l.141 |
| `PIN_BACK_BTN` | `PIN_BUTTON1` | `variant.h` l.94 |
| `PIN_BUZZER` | `33` | `platformio.ini` l.19 |
| `PIN_NFC1` | `(9)` | `variant.h` l.142 |
| `PIN_NFC2` | `(10)` | `variant.h` l.143 |
| `PIN_OLED_RESET` | `-1` | `platformio.ini` l.13 |
| `PIN_QSPI_CS` | `26` | `variant.h` l.200 |
| `PIN_QSPI_IO0` | `30` | `variant.h` l.201 |
| `PIN_QSPI_IO1` | `29` | `variant.h` l.202 |
| `PIN_QSPI_IO2` | `28` | `variant.h` l.203 |
| `PIN_QSPI_IO3` | `2` | `variant.h` l.204 |
| `PIN_QSPI_SCK` | `3` | `variant.h` l.199 |
| `PIN_SERIAL1_RX` | `(15)` | `variant.h` l.151 |
| `PIN_SERIAL1_TX` | `(16)` | `variant.h` l.152 |
| `PIN_SERIAL2_RX` | `(19)` | `variant.h` l.155 |
| `PIN_SERIAL2_TX` | `(20)` | `variant.h` l.156 |
| `PIN_WIRE1_SCL` | `(25)` | `variant.h` l.195 |
| `PIN_WIRE1_SDA` | `(24)` | `variant.h` l.194 |
| `WS2812_PIN` | `PIN_LED3` | `variant.h` l.75 |


### `gat562_mesh_evb_pro`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(46)` | `variant.h` l.166 |
| `P_LORA_DIO_1` | `(47)` | `variant.h` l.167 |
| `P_LORA_MISO` | `(45)` | `variant.h` l.165 |
| `P_LORA_MOSI` | `(44)` | `variant.h` l.164 |
| `P_LORA_NSS` | `(42)` | `variant.h` l.162 |
| `P_LORA_RESET` | `(38)` | `variant.h` l.161 |
| `P_LORA_SCLK` | `(43)` | `variant.h` l.163 |
| `SX126X_POWER_EN` | `(37)` | `variant.h` l.160 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `14` | `platformio.ini` l.9 |
| `PIN_BOARD_SDA` | `13` | `platformio.ini` l.10 |
| `PIN_WIRE_SCL` | `(14)` | `variant.h` l.178 |
| `PIN_WIRE_SDA` | `(13)` | `variant.h` l.177 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(29)` | `variant.h` l.149 |
| `PIN_SPI_MOSI` | `(30)` | `variant.h` l.150 |
| `PIN_SPI_SCK` | `(3)` | `variant.h` l.151 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(33)` | `variant.h` l.205 |
| `PIN_GPS_PPS` | `(17)` | `variant.h` l.206 |
| `PIN_GPS_RX` | `PIN_SERIAL1_TX` | `variant.h` l.204 |
| `PIN_GPS_TX` | `PIN_SERIAL1_RX` | `variant.h` l.203 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(9)` | `variant.h` l.86 |
| `PIN_LED1` | `(35)` | `variant.h` l.69 |
| `PIN_LED2` | `(36)` | `variant.h` l.70 |
| `PIN_USER_BTN` | `PIN_BUTTON1` | `variant.h` l.88 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `(5)` | `variant.h` l.92 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.64 |
| `PINS_COUNT` | `(48)` | `variant.h` l.63 |
| `PIN_A0` | `(5)` | `variant.h` l.99 |
| `PIN_A1` | `(31)` | `variant.h` l.100 |
| `PIN_A2` | `(28)` | `variant.h` l.101 |
| `PIN_A3` | `(29)` | `variant.h` l.102 |
| `PIN_A4` | `(30)` | `variant.h` l.103 |
| `PIN_A5` | `(31)` | `variant.h` l.104 |
| `PIN_A6` | `(0xff)` | `variant.h` l.105 |
| `PIN_A7` | `(0xff)` | `variant.h` l.106 |
| `PIN_AREF` | `(2)` | `variant.h` l.127 |
| `PIN_BACK_BTN` | `PIN_BUTTON1` | `variant.h` l.87 |
| `PIN_NFC1` | `(9)` | `variant.h` l.128 |
| `PIN_NFC2` | `(10)` | `variant.h` l.129 |
| `PIN_QSPI_CS` | `26` | `variant.h` l.186 |
| `PIN_QSPI_IO0` | `30` | `variant.h` l.187 |
| `PIN_QSPI_IO1` | `29` | `variant.h` l.188 |
| `PIN_QSPI_IO2` | `28` | `variant.h` l.189 |
| `PIN_QSPI_IO3` | `2` | `variant.h` l.190 |
| `PIN_QSPI_SCK` | `3` | `variant.h` l.185 |
| `PIN_SERIAL1_RX` | `(15)` | `variant.h` l.137 |
| `PIN_SERIAL1_TX` | `(16)` | `variant.h` l.138 |
| `PIN_SERIAL2_RX` | `(19)` | `variant.h` l.141 |
| `PIN_SERIAL2_TX` | `(20)` | `variant.h` l.142 |
| `PIN_WIRE1_SCL` | `(25)` | `variant.h` l.181 |
| `PIN_WIRE1_SDA` | `(24)` | `variant.h` l.180 |


### `gat562_mesh_tracker_pro`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(46)` | `variant.h` l.176 |
| `P_LORA_DIO_1` | `(47)` | `variant.h` l.177 |
| `P_LORA_MISO` | `(45)` | `variant.h` l.175 |
| `P_LORA_MOSI` | `(44)` | `variant.h` l.174 |
| `P_LORA_NSS` | `(42)` | `variant.h` l.172 |
| `P_LORA_RESET` | `(38)` | `variant.h` l.171 |
| `P_LORA_SCLK` | `(43)` | `variant.h` l.173 |
| `SX126X_POWER_EN` | `(37)` | `variant.h` l.170 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `14` | `platformio.ini` l.9 |
| `PIN_BOARD_SDA` | `13` | `platformio.ini` l.10 |
| `PIN_WIRE_SCL` | `(14)` | `variant.h` l.188 |
| `PIN_WIRE_SDA` | `(13)` | `variant.h` l.187 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(29)` | `variant.h` l.159 |
| `PIN_SPI_MOSI` | `(30)` | `variant.h` l.160 |
| `PIN_SPI_SCK` | `(3)` | `variant.h` l.161 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(33)` | `variant.h` l.215 |
| `PIN_GPS_PPS` | `(17)` | `variant.h` l.216 |
| `PIN_GPS_RX` | `PIN_SERIAL1_TX` | `variant.h` l.214 |
| `PIN_GPS_TX` | `PIN_SERIAL1_RX` | `variant.h` l.213 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(9)` | `variant.h` l.86 |
| `PIN_BUTTON2` | `(28)` | `variant.h` l.87 |
| `PIN_BUTTON3` | `(4)` | `variant.h` l.88 |
| `PIN_BUTTON4` | `(30)` | `variant.h` l.89 |
| `PIN_BUTTON5` | `(31)` | `variant.h` l.90 |
| `PIN_BUTTON6` | `(26)` | `variant.h` l.91 |
| `PIN_LED1` | `(35)` | `variant.h` l.69 |
| `PIN_LED2` | `(36)` | `variant.h` l.70 |
| `PIN_USER_BTN` | `PIN_BUTTON6` | `variant.h` l.98 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `(5)` | `variant.h` l.102 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.64 |
| `PINS_COUNT` | `(48)` | `variant.h` l.63 |
| `PIN_A0` | `(5)` | `variant.h` l.109 |
| `PIN_A1` | `(31)` | `variant.h` l.110 |
| `PIN_A2` | `(28)` | `variant.h` l.111 |
| `PIN_A3` | `(29)` | `variant.h` l.112 |
| `PIN_A4` | `(30)` | `variant.h` l.113 |
| `PIN_A5` | `(31)` | `variant.h` l.114 |
| `PIN_A6` | `(0xff)` | `variant.h` l.115 |
| `PIN_A7` | `(0xff)` | `variant.h` l.116 |
| `PIN_AREF` | `(2)` | `variant.h` l.137 |
| `PIN_BACK_BTN` | `PIN_BUTTON1` | `variant.h` l.92 |
| `PIN_NFC1` | `(9)` | `variant.h` l.138 |
| `PIN_NFC2` | `(10)` | `variant.h` l.139 |
| `PIN_OLED_RESET` | `-1` | `platformio.ini` l.11 |
| `PIN_QSPI_CS` | `26` | `variant.h` l.196 |
| `PIN_QSPI_IO0` | `30` | `variant.h` l.197 |
| `PIN_QSPI_IO1` | `29` | `variant.h` l.198 |
| `PIN_QSPI_IO2` | `28` | `variant.h` l.199 |
| `PIN_QSPI_IO3` | `2` | `variant.h` l.200 |
| `PIN_QSPI_SCK` | `3` | `variant.h` l.195 |
| `PIN_SERIAL1_RX` | `(15)` | `variant.h` l.147 |
| `PIN_SERIAL1_TX` | `(16)` | `variant.h` l.148 |
| `PIN_SERIAL2_RX` | `(19)` | `variant.h` l.151 |
| `PIN_SERIAL2_TX` | `(20)` | `variant.h` l.152 |
| `PIN_WIRE1_SCL` | `(25)` | `variant.h` l.191 |
| `PIN_WIRE1_SDA` | `(24)` | `variant.h` l.190 |


### `gat562_mesh_watch13`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(46)` | `variant.h` l.161 |
| `P_LORA_DIO_1` | `(47)` | `variant.h` l.162 |
| `P_LORA_MISO` | `(45)` | `variant.h` l.160 |
| `P_LORA_MOSI` | `(44)` | `variant.h` l.159 |
| `P_LORA_NSS` | `(42)` | `variant.h` l.157 |
| `P_LORA_RESET` | `(38)` | `variant.h` l.156 |
| `P_LORA_SCLK` | `(43)` | `variant.h` l.158 |
| `SX126X_POWER_EN` | `(37)` | `variant.h` l.155 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `14` | `platformio.ini` l.12 |
| `PIN_BOARD_SDA` | `13` | `platformio.ini` l.13 |
| `PIN_WIRE_SCL` | `(14)` | `variant.h` l.173 |
| `PIN_WIRE_SDA` | `(13)` | `variant.h` l.172 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(29)` | `variant.h` l.144 |
| `PIN_SPI_MOSI` | `(30)` | `variant.h` l.145 |
| `PIN_SPI_SCK` | `(3)` | `variant.h` l.146 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(9)` | `variant.h` l.80 |
| `PIN_BUTTON2` | `(10)` | `variant.h` l.81 |
| `PIN_LED` | `(-1)` | `variant.h` l.69 |
| `PIN_USER_BTN` | `PIN_BUTTON1` | `variant.h` l.82 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `(5)` | `variant.h` l.87 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.64 |
| `PINS_COUNT` | `(48)` | `variant.h` l.63 |
| `PIN_A0` | `(5)` | `variant.h` l.94 |
| `PIN_A1` | `(31)` | `variant.h` l.95 |
| `PIN_A2` | `(28)` | `variant.h` l.96 |
| `PIN_A3` | `(29)` | `variant.h` l.97 |
| `PIN_A4` | `(30)` | `variant.h` l.98 |
| `PIN_A5` | `(31)` | `variant.h` l.99 |
| `PIN_A6` | `(0xff)` | `variant.h` l.100 |
| `PIN_A7` | `(0xff)` | `variant.h` l.101 |
| `PIN_AREF` | `(2)` | `variant.h` l.122 |
| `PIN_BACK_BTN` | `PIN_BUTTON2` | `variant.h` l.83 |
| `PIN_NFC1` | `(9)` | `variant.h` l.123 |
| `PIN_NFC2` | `(10)` | `variant.h` l.124 |
| `PIN_OLED_RESET` | `-1` | `platformio.ini` l.14 |
| `PIN_QSPI_CS` | `26` | `variant.h` l.181 |
| `PIN_QSPI_IO0` | `30` | `variant.h` l.182 |
| `PIN_QSPI_IO1` | `29` | `variant.h` l.183 |
| `PIN_QSPI_IO2` | `28` | `variant.h` l.184 |
| `PIN_QSPI_IO3` | `2` | `variant.h` l.185 |
| `PIN_QSPI_SCK` | `3` | `variant.h` l.180 |
| `PIN_SERIAL1_RX` | `(15)` | `variant.h` l.132 |
| `PIN_SERIAL1_TX` | `(16)` | `variant.h` l.133 |
| `PIN_SERIAL2_RX` | `(19)` | `variant.h` l.136 |
| `PIN_SERIAL2_TX` | `(20)` | `variant.h` l.137 |
| `PIN_WIRE1_SCL` | `(25)` | `variant.h` l.176 |
| `PIN_WIRE1_SDA` | `(24)` | `variant.h` l.175 |


### `heltec_mesh_solar`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `(24)` | `variant.h` l.92 |
| `P_LORA_BUSY` | `17` | `MeshSolarBoard.h` l.15 |
| `P_LORA_DIO_1` | `20` | `MeshSolarBoard.h` l.12 |
| `P_LORA_MISO` | `23` | `MeshSolarBoard.h` l.17 |
| `P_LORA_MOSI` | `22` | `MeshSolarBoard.h` l.18 |
| `P_LORA_NSS` | `24` | `MeshSolarBoard.h` l.13 |
| `P_LORA_RESET` | `25` | `MeshSolarBoard.h` l.14 |
| `P_LORA_SCLK` | `19` | `MeshSolarBoard.h` l.16 |
| `SX126X_BUSY` | `(17)` | `variant.h` l.94 |
| `SX126X_DIO1` | `(20)` | `variant.h` l.93 |
| `SX126X_RESET` | `(25)` | `variant.h` l.95 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(26)` | `variant.h` l.45 |
| `PIN_WIRE_SDA` | `(6)` | `variant.h` l.44 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(43)` | `variant.h` l.99 |
| `PIN_SPI1_MOSI` | `(41)` | `variant.h` l.100 |
| `PIN_SPI1_SCK` | `(40)` | `variant.h` l.101 |
| `PIN_SPI_MISO` | `(23)` | `variant.h` l.55 |
| `PIN_SPI_MOSI` | `(22)` | `variant.h` l.56 |
| `PIN_SPI_NSS` | `(24)` | `variant.h` l.58 |
| `PIN_SPI_SCK` | `(19)` | `variant.h` l.57 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.78 |
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.67 |
| `PIN_BUTTON1` | `(42)` | `variant.h` l.77 |
| `PIN_LED` | `LED_BUILTIN` | `variant.h` l.64 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.83 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `BQ4050_EMERGENCY_SHUTDOWN_PIN` | `(35)` | `variant.h` l.127 |
| `BQ4050_SCL_PIN` | `(32)` | `variant.h` l.126 |
| `BQ4050_SDA_PIN` | `(33)` | `variant.h` l.125 |
| `EXTERNAL_WATCHDOG_DONE_PIN` | `9` | `platformio.ini` l.17 |
| `EXTERNAL_WATCHDOG_WAKE_PIN` | `10` | `platformio.ini` l.18 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.27 |
| `PINS_COUNT` | `(48)` | `variant.h` l.26 |
| `PIN_NEOPIXEL` | `(47)` | `variant.h` l.71 |
| `PIN_SERIAL1_RX` | `(37)` | `variant.h` l.34 |
| `PIN_SERIAL1_TX` | `(39)` | `variant.h` l.35 |
| `PIN_SERIAL2_RX` | `(-1)` | `variant.h` l.37 |
| `PIN_SERIAL2_TX` | `(-1)` | `variant.h` l.38 |
| `PIN_WIRE1_SCL` | `(5)` | `variant.h` l.48 |
| `PIN_WIRE1_SDA` | `(30)` | `variant.h` l.47 |


### `heltec_t096`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `(0 + 5)` | `variant.h` l.90 |
| `P_LORA_BUSY` | `19` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `21` | `platformio.ini` l.13 |
| `P_LORA_KCT8103L_PA_CSD` | `12` | `platformio.ini` l.22 |
| `P_LORA_KCT8103L_PA_CTX` | `41` | `platformio.ini` l.23 |
| `P_LORA_MISO` | `14` | `platformio.ini` l.18 |
| `P_LORA_MOSI` | `11` | `platformio.ini` l.19 |
| `P_LORA_NSS` | `5` | `platformio.ini` l.14 |
| `P_LORA_PA_POWER` | `30` | `platformio.ini` l.21 |
| `P_LORA_RESET` | `16` | `platformio.ini` l.15 |
| `P_LORA_SCLK` | `40` | `platformio.ini` l.17 |
| `P_LORA_TX_LED` | `28` | `platformio.ini` l.20 |
| `SX126X_BUSY` | `(0 + 19)` | `variant.h` l.92 |
| `SX126X_DIO1` | `(0 + 21)` | `variant.h` l.91 |
| `SX126X_RESET` | `(0 + 16)` | `variant.h` l.93 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(0 + 8)` | `variant.h` l.54 |
| `PIN_WIRE_SDA` | `(0 + 7)` | `variant.h` l.53 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(0)` | `variant.h` l.107 |
| `PIN_SPI1_MOSI` | `(0+17)` | `variant.h` l.108 |
| `PIN_SPI1_SCK` | `(0+20)` | `variant.h` l.109 |
| `PIN_SPI_MISO` | `(0 + 14)` | `variant.h` l.102 |
| `PIN_SPI_MOSI` | `(0 + 11)` | `variant.h` l.103 |
| `PIN_SPI_NSS` | `LORA_CS` | `variant.h` l.105 |
| `PIN_SPI_SCK` | `(32 + 8)` | `variant.h` l.104 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_CS` | `(0 + 22)` | `variant.h` l.131 |
| `PIN_TFT_DC` | `(0 + 15)` | `variant.h` l.132 |
| `PIN_TFT_LEDA_CTL` | `(32 + 12)` | `variant.h` l.129 |
| `PIN_TFT_LEDA_CTL_ACTIVE` | `LOW` | `variant.h` l.130 |
| `PIN_TFT_RST` | `(0 + 13)` | `variant.h` l.127 |
| `PIN_TFT_SCL` | `(0 + 20)` | `variant.h` l.125 |
| `PIN_TFT_SDA` | `(0 + 17)` | `variant.h` l.126 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `GPS_EN` | `platformio.ini` l.36 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `platformio.ini` l.37 |
| `PIN_GPS_RESET` | `GPS_RESET` | `platformio.ini` l.38 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` l.39 |
| `PIN_GPS_RX` | `25` | `platformio.ini` l.34 |
| `PIN_GPS_TX` | `23` | `platformio.ini` l.35 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.79 |
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.68 |
| `PIN_BUTTON1` | `(32 + 10)` | `variant.h` l.78 |
| `PIN_LED` | `LED_BUILTIN` | `variant.h` l.65 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.84 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(3)` | `variant.h` l.25 |
| `PIN_BAT_CTL` | `47` | `platformio.ini` l.42 |
| `PIN_VBAT_READ` | `BATTERY_PIN` | `platformio.ini` l.41 |
| `PIN_VEXT_EN` | `26` | `platformio.ini` l.32 |
| `PIN_VEXT_EN_ACTIVE` | `HIGH` | `platformio.ini` l.33 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `PIN_WIRE1_SCL` | `platformio.ini` l.115 |
| `ENV_PIN_SDA` | `PIN_WIRE1_SDA` | `platformio.ini` l.114 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.46 |
| `PINS_COUNT` | `(48)` | `variant.h` l.45 |
| `PIN_3V3_EN` | `(38)` | `variant.h` l.23 |
| `PIN_SERIAL1_RX` | `(0 + 23)` | `variant.h` l.117 |
| `PIN_SERIAL1_TX` | `(0 + 25)` | `variant.h` l.118 |
| `PIN_SERIAL2_RX` | `(0 + 9)` | `variant.h` l.120 |
| `PIN_SERIAL2_TX` | `(0 + 10)` | `variant.h` l.121 |
| `PIN_WIRE1_SCL` | `(0 + 27)` | `variant.h` l.59 |
| `PIN_WIRE1_SDA` | `(0 + 4)` | `variant.h` l.58 |


### `heltec_t1`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `SX126X_CS` | `variant.h` l.87 |
| `P_LORA_BUSY` | `SX126X_BUSY` | `variant.h` l.99 |
| `P_LORA_DIO_1` | `SX126X_DIO1` | `variant.h` l.96 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.117 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.118 |
| `P_LORA_NSS` | `LORA_CS` | `variant.h` l.97 |
| `P_LORA_RESET` | `SX126X_RESET` | `variant.h` l.98 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.116 |
| `P_LORA_TX_LED` | `PIN_LED1` | `variant.h` l.100 |
| `SX126X_BUSY` | `(0 + 29)` | `variant.h` l.89 |
| `SX126X_CS` | `(32 + 11)` | `variant.h` l.86 |
| `SX126X_DIO1` | `(0 + 31)` | `variant.h` l.88 |
| `SX126X_RESET` | `(0 + 2)` | `variant.h` l.90 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(0 + 10)` | `variant.h` l.77 |
| `PIN_WIRE_SDA` | `(32 + 3)` | `variant.h` l.76 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `ST7735_MISO` | `variant.h` l.112 |
| `PIN_SPI1_MOSI` | `ST7735_SDA` | `variant.h` l.113 |
| `PIN_SPI1_SCK` | `ST7735_SCK` | `variant.h` l.114 |
| `PIN_SPI_MISO` | `(0 + 3)` | `variant.h` l.107 |
| `PIN_SPI_MOSI` | `(32 + 14)` | `variant.h` l.108 |
| `PIN_SPI_NSS` | `LORA_CS` | `variant.h` l.110 |
| `PIN_SPI_SCK` | `(32 + 13)` | `variant.h` l.109 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_CS` | `ST7735_CS` | `variant.h` l.33 |
| `PIN_TFT_DC` | `ST7735_RS` | `variant.h` l.34 |
| `PIN_TFT_LEDA_CTL` | `ST7735_BL` | `variant.h` l.38 |
| `PIN_TFT_LEDA_CTL_ACTIVE` | `LOW` | `variant.h` l.39 |
| `PIN_TFT_RST` | `ST7735_RESET` | `variant.h` l.37 |
| `PIN_TFT_SCL` | `ST7735_SCK` | `variant.h` l.36 |
| `PIN_TFT_SDA` | `ST7735_SDA` | `variant.h` l.35 |
| `PIN_TFT_VDD_CTL` | `VTFT_CTRL` | `variant.h` l.40 |
| `PIN_TFT_VDD_CTL_ACTIVE` | `LOW` | `variant.h` l.41 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `GPS_RX_PIN` | `(0 + 7)` | `variant.h` l.135 |
| `GPS_TX_PIN` | `(0 + 8)` | `variant.h` l.134 |
| `PIN_GPS_EN` | `(0 + 4)` | `variant.h` l.129 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `variant.h` l.132 |
| `PIN_GPS_PPS` | `(32 + 9)` | `variant.h` l.133 |
| `PIN_GPS_RESET` | `(0 + 26)` | `variant.h` l.125 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `variant.h` l.128 |
| `PIN_GPS_RX` | `GPS_RX_PIN` | `variant.h` l.137 |
| `PIN_GPS_TX` | `GPS_TX_PIN` | `variant.h` l.136 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.61 |
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.53 |
| `PIN_BUTTON1` | `(32 + 10)` | `variant.h` l.59 |
| `PIN_BUTTON2` | `(0 + 14)` | `variant.h` l.60 |
| `PIN_LED` | `LED_BUILTIN` | `variant.h` l.49 |
| `PIN_LED1` | `(0 + 16)` | `variant.h` l.47 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.63 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(0 + 5)` | `variant.h` l.155 |
| `PIN_BAT_CTL` | `ADC_CTRL` | `variant.h` l.153 |
| `PIN_VBAT_READ` | `BATTERY_PIN` | `variant.h` l.156 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.16 |
| `PINS_COUNT` | `(48)` | `variant.h` l.15 |
| `PIN_BUZZER` | `(0 + 9)` | `variant.h` l.145 |
| `PIN_BUZZER_VOLTAGE_MULTIPLIER_1` | `(32 + 2)` | `variant.h` l.146 |
| `PIN_BUZZER_VOLTAGE_MULTIPLIER_2` | `(32 + 5)` | `variant.h` l.147 |
| `PIN_SENSOR_EN` | `(32 + 6)` | `variant.h` l.79 |
| `PIN_SENSOR_EN_ACTIVE` | `LOW` | `variant.h` l.80 |
| `PIN_SERIAL1_RX` | `GPS_RX_PIN` | `variant.h` l.139 |
| `PIN_SERIAL1_TX` | `GPS_TX_PIN` | `variant.h` l.140 |


### `heltec_t114`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `(24)` | `variant.h` l.109 |
| `P_LORA_BUSY` | `17` | `platformio.ini` l.19 |
| `P_LORA_DIO_1` | `20` | `platformio.ini` l.16 |
| `P_LORA_MISO` | `23` | `platformio.ini` l.21 |
| `P_LORA_MOSI` | `22` | `platformio.ini` l.22 |
| `P_LORA_NSS` | `24` | `platformio.ini` l.17 |
| `P_LORA_RESET` | `25` | `platformio.ini` l.18 |
| `P_LORA_SCLK` | `19` | `platformio.ini` l.20 |
| `P_LORA_TX_LED` | `35` | `platformio.ini` l.23 |
| `SX126X_BUSY` | `(17)` | `variant.h` l.111 |
| `SX126X_DIO1` | `(20)` | `variant.h` l.110 |
| `SX126X_POWER_EN` | `37` | `platformio.ini` l.27 |
| `SX126X_RESET` | `(25)` | `variant.h` l.112 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(27)` | `variant.h` l.62 |
| `PIN_WIRE_SDA` | `(26)` | `variant.h` l.61 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(43)` | `variant.h` l.116 |
| `PIN_SPI1_MOSI` | `(41)` | `variant.h` l.117 |
| `PIN_SPI1_SCK` | `(40)` | `variant.h` l.118 |
| `PIN_SPI_MISO` | `(23)` | `variant.h` l.72 |
| `PIN_SPI_MOSI` | `(22)` | `variant.h` l.73 |
| `PIN_SPI_NSS` | `(24)` | `variant.h` l.75 |
| `PIN_SPI_SCK` | `(19)` | `variant.h` l.74 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_TFT_CS` | `(11)` | `variant.h` l.141 |
| `PIN_TFT_DC` | `(12)` | `variant.h` l.142 |
| `PIN_TFT_LEDA_CTL` | `(15)` | `variant.h` l.140 |
| `PIN_TFT_RST` | `(2)` | `variant.h` l.138 |
| `PIN_TFT_SCL` | `(40)` | `variant.h` l.136 |
| `PIN_TFT_SDA` | `(41)` | `variant.h` l.137 |
| `PIN_TFT_VDD_CTL` | `(3)` | `variant.h` l.139 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `21` | `platformio.ini` l.34 |
| `PIN_GPS_RESET` | `38` | `platformio.ini` l.35 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` l.36 |
| `PIN_GPS_RX` | `(39)` | `variant.h` l.131 |
| `PIN_GPS_TX` | `(37)` | `variant.h` l.132 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.95 |
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.84 |
| `PIN_BUTTON1` | `(42)` | `variant.h` l.94 |
| `PIN_LED` | `LED_BUILTIN` | `variant.h` l.81 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.100 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(4)` | `variant.h` l.25 |
| `PIN_BAT_CTL` | `6` | `T114Board.h` l.9 |
| `PIN_VBAT_READ` | `4` | `T114Board.h` l.8 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `PIN_WIRE1_SCL` | `platformio.ini` l.38 |
| `ENV_PIN_SDA` | `PIN_WIRE1_SDA` | `platformio.ini` l.37 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.45 |
| `PINS_COUNT` | `(48)` | `variant.h` l.44 |
| `PIN_3V3_EN` | `(38)` | `variant.h` l.23 |
| `PIN_NEOPIXEL` | `(14)` | `variant.h` l.88 |
| `PIN_SERIAL1_RX` | `(37)` | `variant.h` l.52 |
| `PIN_SERIAL1_TX` | `(39)` | `variant.h` l.53 |
| `PIN_SERIAL2_RX` | `(9)` | `variant.h` l.55 |
| `PIN_SERIAL2_TX` | `(10)` | `variant.h` l.56 |
| `PIN_WIRE1_SCL` | `(8)` | `variant.h` l.65 |
| `PIN_WIRE1_SDA` | `(7)` | `variant.h` l.64 |


### `heltec_tower_v2`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `SX126X_CS` | `variant.h` l.40 |
| `LORA_KCT8103L_EN` | `(0 + 15)` | `variant.h` l.56 |
| `LORA_KCT8103L_TX_RX` | `(0 + 16)` | `variant.h` l.57 |
| `LORA_PA_POWER` | `LORA_KCT8103L_EN` | `variant.h` l.58 |
| `P_LORA_BUSY` | `SX126X_BUSY` | `variant.h` l.49 |
| `P_LORA_DIO_1` | `SX126X_DIO1` | `variant.h` l.48 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.51 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.52 |
| `P_LORA_NSS` | `LORA_CS` | `variant.h` l.47 |
| `P_LORA_RESET` | `SX126X_RESET` | `variant.h` l.50 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.53 |
| `P_LORA_TX_LED` | `LED_BUILTIN` | `variant.h` l.31 |
| `SX126X_BUSY` | `(0 + 17)` | `variant.h` l.42 |
| `SX126X_CS` | `(0 + 24)` | `variant.h` l.39 |
| `SX126X_DIO1` | `(0 + 20)` | `variant.h` l.41 |
| `SX126X_RESET` | `(0 + 25)` | `variant.h` l.43 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `PIN_WIRE_SCL` | `variant.h` l.17 |
| `PIN_BOARD_SDA` | `PIN_WIRE_SDA` | `variant.h` l.16 |
| `PIN_WIRE_SCL` | `(0 + 5)` | `variant.h` l.15 |
| `PIN_WIRE_SDA` | `(0 + 30)` | `variant.h` l.14 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(0 + 23)` | `variant.h` l.20 |
| `PIN_SPI_MOSI` | `(0 + 22)` | `variant.h` l.21 |
| `PIN_SPI_NSS` | `LORA_CS` | `variant.h` l.23 |
| `PIN_SPI_SCK` | `(0 + 19)` | `variant.h` l.22 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `GPS_RX_PIN` | `(32 + 5)` | `variant.h` l.76 |
| `GPS_TX_PIN` | `(32 + 7)` | `variant.h` l.75 |
| `PIN_GPS_EN` | `(0 + 7)` | `variant.h` l.66 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `variant.h` l.67 |
| `PIN_GPS_PPS` | `(32 + 4)` | `variant.h` l.70 |
| `PIN_GPS_RESET` | `(32 + 6)` | `variant.h` l.64 |
| `PIN_GPS_RESET_ACTIVE` | `GPS_RESET_MODE` | `variant.h` l.65 |
| `PIN_GPS_RX` | `GPS_TX_PIN` | `variant.h` l.78 |
| `PIN_GPS_STANDBY` | `(32 + 2)` | `variant.h` l.69 |
| `PIN_GPS_TX` | `GPS_RX_PIN` | `variant.h` l.77 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.35 |
| `LED_PIN` | `(-1)` | `variant.h` l.30 |
| `PIN_BUTTON1` | `(32 + 10)` | `variant.h` l.34 |
| `PIN_LED` | `LED_BUILTIN` | `variant.h` l.26 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.36 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(0 + 4)` | `variant.h` l.95 |
| `PIN_BAT_CTL` | `(0 + 21)` | `variant.h` l.92 |
| `PIN_VBAT_READ` | `BATTERY_PIN` | `variant.h` l.96 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `EXTERNAL_WATCHDOG_DONE_PIN` | `(0 + 9)` | `variant.h` l.86 |
| `EXTERNAL_WATCHDOG_WAKE_PIN` | `(0 + 10)` | `variant.h` l.87 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.9 |
| `PINS_COUNT` | `(48)` | `variant.h` l.8 |
| `PIN_SERIAL1_RX` | `PIN_GPS_TX` | `variant.h` l.80 |
| `PIN_SERIAL1_TX` | `PIN_GPS_RX` | `variant.h` l.81 |
| `PIN_SERIAL2_RX` | `(-1)` | `variant.h` l.82 |
| `PIN_SERIAL2_TX` | `(-1)` | `variant.h` l.83 |
| `RF_PA_DETECT_PIN` | `(0 + 13)` | `variant.h` l.59 |


### `ikoka_handheld_nrf`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `D3` | `platformio.ini` l.18 |
| `P_LORA_DIO_1` | `D1` | `platformio.ini` l.16 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.106 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.107 |
| `P_LORA_NSS` | `D4` | `platformio.ini` l.19 |
| `P_LORA_RESET` | `D2` | `platformio.ini` l.17 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.105 |
| `P_LORA_TX_LED` | `11` | `platformio.ini` l.15 |
| `SX126X_RXEN` | `D5` | `platformio.ini` l.20 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `platformio.ini` l.21 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(7)` | `variant.h` l.113 |
| `PIN_WIRE_SDA` | `(6)` | `variant.h` l.112 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(25)` | `variant.h` l.100 |
| `PIN_SPI1_MOSI` | `(26)` | `variant.h` l.101 |
| `PIN_SPI1_SCK` | `(29)` | `variant.h` l.102 |
| `PIN_SPI_MISO` | `(9)` | `variant.h` l.96 |
| `PIN_SPI_MOSI` | `(10)` | `variant.h` l.97 |
| `PIN_SPI_SCK` | `(8)` | `variant.h` l.98 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(PINS_COUNT)` | `variant.h` l.41 |
| `PIN_LED` | `(LED_RED)` | `variant.h` l.27 |
| `PIN_USER_BTN` | `D0` | `platformio.ini` l.42 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT` | `(32)` | `variant.h` l.68 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(33)` | `variant.h` l.22 |
| `PINS_COUNT` | `(33)` | `variant.h` l.21 |
| `PIN_A0` | `(0)` | `variant.h` l.62 |
| `PIN_A1` | `(1)` | `variant.h` l.63 |
| `PIN_A2` | `(2)` | `variant.h` l.64 |
| `PIN_A3` | `(3)` | `variant.h` l.65 |
| `PIN_A4` | `(4)` | `variant.h` l.66 |
| `PIN_A5` | `(5)` | `variant.h` l.67 |
| `PIN_CHARGING_CURRENT` | `(22)` | `variant.h` l.59 |
| `PIN_LSM6DS3TR_C_INT1` | `(18)` | `variant.h` l.121 |
| `PIN_LSM6DS3TR_C_POWER` | `(15)` | `variant.h` l.120 |
| `PIN_NEOPIXEL` | `(PINS_COUNT)` | `variant.h` l.29 |
| `PIN_NFC1` | `(30)` | `variant.h` l.86 |
| `PIN_NFC2` | `(31)` | `variant.h` l.87 |
| `PIN_PDM_CLK` | `(20)` | `variant.h` l.125 |
| `PIN_PDM_DIN` | `(21)` | `variant.h` l.126 |
| `PIN_PDM_PWR` | `(19)` | `variant.h` l.124 |
| `PIN_QSPI_CS` | `(25)` | `variant.h` l.130 |
| `PIN_QSPI_IO0` | `(26)` | `variant.h` l.131 |
| `PIN_QSPI_IO1` | `(27)` | `variant.h` l.132 |
| `PIN_QSPI_IO2` | `(28)` | `variant.h` l.133 |
| `PIN_QSPI_IO3` | `(29)` | `variant.h` l.134 |
| `PIN_QSPI_SCK` | `(24)` | `variant.h` l.129 |
| `PIN_SERIAL1_RX` | `(7)` | `variant.h` l.90 |
| `PIN_SERIAL1_TX` | `(6)` | `variant.h` l.91 |


### `ikoka_nano_nrf`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `D2` | `platformio.ini` l.18 |
| `P_LORA_DIO_1` | `D1` | `platformio.ini` l.17 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.107 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.108 |
| `P_LORA_NSS` | `D0` | `platformio.ini` l.20 |
| `P_LORA_RESET` | `D3` | `platformio.ini` l.19 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.106 |
| `P_LORA_TX_LED` | `11` | `platformio.ini` l.12 |
| `SX126X_RXEN` | `D7` | `platformio.ini` l.21 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `platformio.ini` l.22 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `5` | `platformio.ini` l.27 |
| `PIN_WIRE_SDA` | `4` | `platformio.ini` l.28 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(25)` | `variant.h` l.101 |
| `PIN_SPI1_MOSI` | `(26)` | `variant.h` l.102 |
| `PIN_SPI1_SCK` | `(29)` | `variant.h` l.103 |
| `PIN_SPI_MISO` | `(9)` | `variant.h` l.97 |
| `PIN_SPI_MOSI` | `(10)` | `variant.h` l.98 |
| `PIN_SPI_SCK` | `(8)` | `variant.h` l.99 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_LED` | `(LED_RED)` | `variant.h` l.27 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT` | `(32)` | `variant.h` l.69 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(33)` | `variant.h` l.22 |
| `PINS_COUNT` | `(33)` | `variant.h` l.21 |
| `PIN_A0` | `(0)` | `variant.h` l.63 |
| `PIN_A1` | `(1)` | `variant.h` l.64 |
| `PIN_A2` | `(2)` | `variant.h` l.65 |
| `PIN_A3` | `(3)` | `variant.h` l.66 |
| `PIN_A4` | `(4)` | `variant.h` l.67 |
| `PIN_A5` | `(5)` | `variant.h` l.68 |
| `PIN_CHARGING_CURRENT` | `(22)` | `variant.h` l.59 |
| `PIN_LSM6DS3TR_C_INT1` | `(18)` | `variant.h` l.122 |
| `PIN_LSM6DS3TR_C_POWER` | `(15)` | `variant.h` l.121 |
| `PIN_NEOPIXEL` | `(PINS_COUNT)` | `variant.h` l.29 |
| `PIN_NFC1` | `(30)` | `variant.h` l.87 |
| `PIN_NFC2` | `(31)` | `variant.h` l.88 |
| `PIN_PDM_CLK` | `(20)` | `variant.h` l.126 |
| `PIN_PDM_DIN` | `(21)` | `variant.h` l.127 |
| `PIN_PDM_PWR` | `(19)` | `variant.h` l.125 |
| `PIN_QSPI_CS` | `(25)` | `variant.h` l.131 |
| `PIN_QSPI_IO0` | `(26)` | `variant.h` l.132 |
| `PIN_QSPI_IO1` | `(27)` | `variant.h` l.133 |
| `PIN_QSPI_IO2` | `(28)` | `variant.h` l.134 |
| `PIN_QSPI_IO3` | `(29)` | `variant.h` l.135 |
| `PIN_QSPI_SCK` | `(24)` | `variant.h` l.130 |
| `PIN_SERIAL1_RX` | `(7)` | `variant.h` l.91 |
| `PIN_SERIAL1_TX` | `(6)` | `variant.h` l.92 |


### `ikoka_stick_nrf`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `D3` | `platformio.ini` l.20 |
| `P_LORA_DIO_1` | `D1` | `platformio.ini` l.18 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.107 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.108 |
| `P_LORA_NSS` | `D4` | `platformio.ini` l.21 |
| `P_LORA_RESET` | `D2` | `platformio.ini` l.19 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.106 |
| `P_LORA_TX_LED` | `11` | `platformio.ini` l.12 |
| `SX126X_RXEN` | `D5` | `platformio.ini` l.22 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `platformio.ini` l.23 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `7` | `platformio.ini` l.29 |
| `PIN_WIRE_SDA` | `6` | `platformio.ini` l.30 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(25)` | `variant.h` l.101 |
| `PIN_SPI1_MOSI` | `(26)` | `variant.h` l.102 |
| `PIN_SPI1_SCK` | `(29)` | `variant.h` l.103 |
| `PIN_SPI_MISO` | `(9)` | `variant.h` l.97 |
| `PIN_SPI_MOSI` | `(10)` | `variant.h` l.98 |
| `PIN_SPI_SCK` | `(8)` | `variant.h` l.99 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(PINS_COUNT)` | `variant.h` l.41 |
| `PIN_LED` | `(LED_RED)` | `variant.h` l.27 |
| `PIN_USER_BTN` | `0` | `platformio.ini` l.28 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT` | `(32)` | `variant.h` l.69 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(33)` | `variant.h` l.22 |
| `PINS_COUNT` | `(33)` | `variant.h` l.21 |
| `PIN_A0` | `(0)` | `variant.h` l.63 |
| `PIN_A1` | `(1)` | `variant.h` l.64 |
| `PIN_A2` | `(2)` | `variant.h` l.65 |
| `PIN_A3` | `(3)` | `variant.h` l.66 |
| `PIN_A4` | `(4)` | `variant.h` l.67 |
| `PIN_A5` | `(5)` | `variant.h` l.68 |
| `PIN_CHARGING_CURRENT` | `(22)` | `variant.h` l.59 |
| `PIN_LSM6DS3TR_C_INT1` | `(18)` | `variant.h` l.122 |
| `PIN_LSM6DS3TR_C_POWER` | `(15)` | `variant.h` l.121 |
| `PIN_NEOPIXEL` | `(PINS_COUNT)` | `variant.h` l.29 |
| `PIN_NFC1` | `(30)` | `variant.h` l.87 |
| `PIN_NFC2` | `(31)` | `variant.h` l.88 |
| `PIN_PDM_CLK` | `(20)` | `variant.h` l.126 |
| `PIN_PDM_DIN` | `(21)` | `variant.h` l.127 |
| `PIN_PDM_PWR` | `(19)` | `variant.h` l.125 |
| `PIN_QSPI_CS` | `(25)` | `variant.h` l.131 |
| `PIN_QSPI_IO0` | `(26)` | `variant.h` l.132 |
| `PIN_QSPI_IO1` | `(27)` | `variant.h` l.133 |
| `PIN_QSPI_IO2` | `(28)` | `variant.h` l.134 |
| `PIN_QSPI_IO3` | `(29)` | `variant.h` l.135 |
| `PIN_QSPI_SCK` | `(24)` | `variant.h` l.130 |
| `PIN_SERIAL1_RX` | `(7)` | `variant.h` l.91 |
| `PIN_SERIAL1_TX` | `(6)` | `variant.h` l.92 |


### `keepteen_lt1`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(29)` | `variant.h` l.49 |
| `P_LORA_DIO_1` | `(10)` | `variant.h` l.54 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.50 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.51 |
| `P_LORA_NSS` | `(45)` | `variant.h` l.52 |
| `P_LORA_RESET` | `(9)` | `variant.h` l.55 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.53 |
| `P_LORA_TX_LED` | `PIN_LED` | `variant.h` l.24 |
| `SX126X_RXEN` | `RADIOLIB_NC` | `variant.h` l.56 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `variant.h` l.57 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `36` | `platformio.ini` l.14 |
| `PIN_BOARD_SDA` | `34` | `platformio.ini` l.13 |
| `PIN_WIRE_SCL` | `(36)` | `variant.h` l.65 |
| `PIN_WIRE_SDA` | `(34)` | `variant.h` l.64 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(2)` | `variant.h` l.44 |
| `PIN_SPI_MOSI` | `(38)` | `variant.h` l.45 |
| `PIN_SPI_SCK` | `(43)` | `variant.h` l.46 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(24)` | `variant.h` l.72 |
| `PIN_GPS_RX` | `PIN_SERIAL1_TX` | `variant.h` l.71 |
| `PIN_GPS_TX` | `PIN_SERIAL1_RX` | `variant.h` l.70 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(32)` | `variant.h` l.28 |
| `PIN_LED` | `(15)` | `variant.h` l.20 |
| `PIN_LED2` | `(13)` | `variant.h` l.21 |
| `PIN_USER_BTN` | `PIN_BUTTON1` | `variant.h` l.29 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `(31)` | `variant.h` l.32 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.15 |
| `PINS_COUNT` | `(48)` | `variant.h` l.14 |
| `PIN_SERIAL1_RX` | `(22)` | `variant.h` l.38 |
| `PIN_SERIAL1_TX` | `(20)` | `variant.h` l.39 |


### `lilygo_t_impulse_plus`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `SX1262_BUSY` | `variant.h` l.77 |
| `P_LORA_DIO_0` | `RADIOLIB_NC` | `variant.h` l.78 |
| `P_LORA_DIO_1` | `SX1262_DIO1` | `variant.h` l.75 |
| `P_LORA_DIO_2` | `SX1262_DIO2` | `variant.h` l.79 |
| `P_LORA_MISO` | `SX1262_MISO` | `variant.h` l.81 |
| `P_LORA_MOSI` | `SX1262_MOSI` | `variant.h` l.82 |
| `P_LORA_NSS` | `SX1262_CS` | `variant.h` l.74 |
| `P_LORA_RESET` | `SX1262_RST` | `variant.h` l.76 |
| `P_LORA_SCLK` | `SX1262_SCLK` | `variant.h` l.80 |
| `SX126X_RXEN` | `SX1262_RF_VC2` | `variant.h` l.72 |
| `SX126X_TXEN` | `SX1262_RF_VC1` | `variant.h` l.71 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(27)` | `variant.h` l.190 |
| `PIN_WIRE_SDA` | `(26)` | `variant.h` l.189 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(46)` | `variant.h` l.175 |
| `PIN_SPI_MOSI` | `(45)` | `variant.h` l.176 |
| `PIN_SPI_SCK` | `(47)` | `variant.h` l.177 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `GPS_EN` | `variant.h` l.93 |
| `PIN_GPS_EN_ACTIVE` | `LOW` | `variant.h` l.95 |
| `PIN_GPS_RX` | `GPS_UART_RX` | `variant.h` l.91 |
| `PIN_GPS_TX` | `GPS_UART_TX` | `variant.h` l.92 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `_PINNUM(0, 24)` | `variant.h` l.124 |
| `PIN_LED1` | `(_PINNUM(0, 17))` | `variant.h` l.108 |
| `PIN_USER_BTN` | `-1` | `platformio.ini` l.14 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `IIC_SCL_2` | `platformio.ini` l.20 |
| `ENV_PIN_SDA` | `IIC_SDA_2` | `platformio.ini` l.19 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.103 |
| `PINS_COUNT` | `(48)` | `variant.h` l.102 |
| `PIN_A0` | `(3)` | `variant.h` l.132 |
| `PIN_A1` | `(4)` | `variant.h` l.133 |
| `PIN_A2` | `(28)` | `variant.h` l.134 |
| `PIN_A3` | `(29)` | `variant.h` l.135 |
| `PIN_A4` | `(30)` | `variant.h` l.136 |
| `PIN_A5` | `(31)` | `variant.h` l.137 |
| `PIN_A6` | `(0xff)` | `variant.h` l.138 |
| `PIN_A7` | `(0xff)` | `variant.h` l.139 |
| `PIN_AREF` | `(2)` | `variant.h` l.152 |
| `PIN_NFC1` | `(9)` | `variant.h` l.153 |
| `PIN_NFC2` | `(10)` | `variant.h` l.154 |
| `PIN_QSPI_CS` | `ZD25WQ32C_CS` | `variant.h` l.206 |
| `PIN_QSPI_IO0` | `ZD25WQ32C_IO0` | `variant.h` l.207 |
| `PIN_QSPI_IO1` | `ZD25WQ32C_IO1` | `variant.h` l.208 |
| `PIN_QSPI_IO2` | `ZD25WQ32C_IO2` | `variant.h` l.209 |
| `PIN_QSPI_IO3` | `ZD25WQ32C_IO3` | `variant.h` l.210 |
| `PIN_QSPI_SCK` | `ZD25WQ32C_SCLK` | `variant.h` l.205 |
| `PIN_SERIAL1_RX` | `(33)` | `variant.h` l.163 |
| `PIN_SERIAL1_TX` | `(34)` | `variant.h` l.164 |
| `PIN_SERIAL2_RX` | `(8)` | `variant.h` l.167 |
| `PIN_SERIAL2_TX` | `(6)` | `variant.h` l.168 |
| `PIN_WIRE1_SCL` | `(27)` | `variant.h` l.193 |
| `PIN_WIRE1_SDA` | `(26)` | `variant.h` l.192 |


### `lilygo_techo`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `(24)` | `variant.h` l.103 |
| `P_LORA_BUSY` | `17` | `platformio.ini` l.17 |
| `P_LORA_DIO_1` | `20` | `platformio.ini` l.14 |
| `P_LORA_MISO` | `23` | `platformio.ini` l.19 |
| `P_LORA_MOSI` | `22` | `platformio.ini` l.20 |
| `P_LORA_NSS` | `24` | `platformio.ini` l.15 |
| `P_LORA_RESET` | `25` | `platformio.ini` l.16 |
| `P_LORA_SCLK` | `19` | `platformio.ini` l.18 |
| `P_LORA_TX_LED` | `LED_GREEN` | `platformio.ini` l.26 |
| `SX126X_BUSY` | `(17)` | `variant.h` l.105 |
| `SX126X_DIO1` | `(20)` | `variant.h` l.104 |
| `SX126X_POWER_EN` | `37` | `platformio.ini` l.21 |
| `SX126X_RESET` | `(25)` | `variant.h` l.106 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(27)` | `variant.h` l.49 |
| `PIN_WIRE_SDA` | `(26)` | `variant.h` l.48 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(38)` | `variant.h` l.113 |
| `PIN_SPI1_MOSI` | `(29)` | `variant.h` l.114 |
| `PIN_SPI1_SCK` | `(31)` | `variant.h` l.115 |
| `PIN_SPI_MISO` | `(23)` | `variant.h` l.56 |
| `PIN_SPI_MOSI` | `(22)` | `variant.h` l.57 |
| `PIN_SPI_NSS` | `(24)` | `variant.h` l.59 |
| `PIN_SPI_SCK` | `(19)` | `variant.h` l.58 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `GPS_EN` | `platformio.ini` l.31 |
| `PIN_GPS_PPS` | `(36)` | `variant.h` l.141 |
| `PIN_GPS_RESET` | `(37)` | `variant.h` l.140 |
| `PIN_GPS_RESET_ACTIVE` | `LOW` | `platformio.ini` l.32 |
| `PIN_GPS_RX` | `(40)` | `variant.h` l.137 |
| `PIN_GPS_TX` | `(41)` | `variant.h` l.138 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.90 |
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.83 |
| `PIN_BUTTON1` | `(42)` | `variant.h` l.89 |
| `PIN_BUTTON2` | `(11)` | `variant.h` l.93 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.91 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(4)` | `variant.h` l.24 |
| `PIN_VBAT_READ` | `(4)` | `TechoBoard.h` l.13 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.36 |
| `PINS_COUNT` | `(48)` | `variant.h` l.35 |
| `PIN_PWR_EN` | `(12)` | `variant.h` l.22 |
| `PIN_QSPI_CS` | `(47)` | `variant.h` l.65 |
| `PIN_QSPI_IO0` | `(44)` | `variant.h` l.66 |
| `PIN_QSPI_IO1` | `(45)` | `variant.h` l.67 |
| `PIN_QSPI_IO2` | `(7)` | `variant.h` l.68 |
| `PIN_QSPI_IO3` | `(5)` | `variant.h` l.69 |
| `PIN_QSPI_SCK` | `(46)` | `variant.h` l.64 |
| `PIN_SERIAL1_RX` | `PIN_GPS_TX` | `variant.h` l.43 |
| `PIN_SERIAL1_TX` | `PIN_GPS_RX` | `variant.h` l.44 |
| `PIN_TXCO` | `(21)` | `variant.h` l.18 |


### `lilygo_techo_card`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(14)` | `variant.h` l.106 |
| `P_LORA_DIO_1` | `(40)` | `variant.h` l.104 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.102 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.103 |
| `P_LORA_NSS` | `(11)` | `variant.h` l.107 |
| `P_LORA_RESET` | `(7)` | `variant.h` l.105 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.101 |
| `SX126X_RXEN` | `(33)` | `variant.h` l.108 |
| `SX126X_TXEN` | `(27)` | `variant.h` l.109 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(34)` | `variant.h` l.48 |
| `PIN_WIRE_SDA` | `(36)` | `variant.h` l.47 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(17)` | `variant.h` l.57 |
| `PIN_SPI_MOSI` | `(15)` | `variant.h` l.58 |
| `PIN_SPI_SCK` | `(13)` | `variant.h` l.59 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(25)` | `variant.h` l.122 |
| `PIN_GPS_PPS` | `(23)` | `variant.h` l.125 |
| `PIN_GPS_RESET` | `(47)` | `variant.h` l.123 |
| `PIN_GPS_RX` | `(21)` | `variant.h` l.120 |
| `PIN_GPS_STANDBY` | `(29)` | `variant.h` l.124 |
| `PIN_GPS_TX` | `(19)` | `variant.h` l.121 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.91 |
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.84 |
| `PIN_BUTTON1` | `(42)` | `variant.h` l.90 |
| `PIN_BUTTON2` | `(24)` | `variant.h` l.94 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.92 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_BAT_CTL` | `(31)` | `variant.h` l.23 |
| `PIN_VBAT_READ` | `(2)` | `TechoCardBoard.h` l.14 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.35 |
| `PINS_COUNT` | `(48)` | `variant.h` l.34 |
| `PIN_BUZZER` | `38` | `platformio.ini` l.73 |
| `PIN_OLED_RESET` | `-1` | `platformio.ini` l.21 |
| `PIN_PWR_EN` | `(30)` | `variant.h` l.21 |
| `PIN_QSPI_CS` | `(12)` | `variant.h` l.65 |
| `PIN_QSPI_IO0` | `(6)` | `variant.h` l.66 |
| `PIN_QSPI_IO1` | `(8)` | `variant.h` l.67 |
| `PIN_QSPI_IO2` | `(41)` | `variant.h` l.68 |
| `PIN_QSPI_IO3` | `(26)` | `variant.h` l.69 |
| `PIN_QSPI_SCK` | `(4)` | `variant.h` l.64 |
| `PIN_SERIAL1_RX` | `PIN_GPS_TX` | `variant.h` l.42 |
| `PIN_SERIAL1_TX` | `PIN_GPS_RX` | `variant.h` l.43 |


### `lilygo_techo_lite`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `_PINNUM(0, 11)` | `variant.h` l.105 |
| `P_LORA_BUSY` | `SX126X_BUSY` | `variant.h` l.118 |
| `P_LORA_DIO_1` | `SX126X_DIO1` | `variant.h` l.114 |
| `P_LORA_DIO_2` | `SX126X_DIO2` | `variant.h` l.115 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.120 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.121 |
| `P_LORA_NSS` | `LORA_CS` | `variant.h` l.116 |
| `P_LORA_RESET` | `SX126X_RESET` | `variant.h` l.117 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.119 |
| `P_LORA_TX_LED` | `LED_GREEN` | `platformio.ini` l.18 |
| `SX126X_BUSY` | `_PINNUM(0, 14)` | `variant.h` l.109 |
| `SX126X_DIO1` | `_PINNUM(1, 8)` | `variant.h` l.107 |
| `SX126X_DIO2` | `_PINNUM(0, 5)` | `variant.h` l.108 |
| `SX126X_POWER_EN` | `_PINNUM(0, 30)` | `variant.h` l.106 |
| `SX126X_RESET` | `_PINNUM(0, 7)` | `variant.h` l.110 |
| `SX126X_RXEN` | `_PINNUM(1, 1)` | `variant.h` l.111 |
| `SX126X_TXEN` | `_PINNUM(0, 27)` | `variant.h` l.112 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `_PINNUM(1, 2)` | `variant.h` l.51 |
| `PIN_WIRE_SDA` | `_PINNUM(1, 4)` | `variant.h` l.50 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(0)` | `variant.h` l.126 |
| `PIN_SPI1_MOSI` | `_PINNUM(0, 20)` | `variant.h` l.127 |
| `PIN_SPI1_SCK` | `_PINNUM(0, 19)` | `variant.h` l.128 |
| `PIN_SPI_MISO` | `_PINNUM(0, 17)` | `variant.h` l.58 |
| `PIN_SPI_MOSI` | `_PINNUM(0, 15)` | `variant.h` l.59 |
| `PIN_SPI_NSS` | `(0)` | `variant.h` l.61 |
| `PIN_SPI_SCK` | `_PINNUM(0, 13)` | `variant.h` l.60 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_DISPLAY_BUSY` | `DISP_BUSY` | `variant.h` l.151 |
| `PIN_DISPLAY_CS` | `DISP_CS` | `variant.h` l.148 |
| `PIN_DISPLAY_DC` | `DISP_DC` | `variant.h` l.149 |
| `PIN_DISPLAY_RST` | `DISP_RST` | `variant.h` l.150 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `GPS_EN` | `platformio.ini` l.22 |
| `PIN_GPS_PPS` | `_PINNUM(1, 15)` | `variant.h` l.161 |
| `PIN_GPS_RX` | `_PINNUM(1, 10)` | `variant.h` l.158 |
| `PIN_GPS_STANDBY` | `_PINNUM(1, 13)` | `variant.h` l.160 |
| `PIN_GPS_TX` | `_PINNUM(0, 29)` | `variant.h` l.157 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.92 |
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.85 |
| `PIN_BUTTON1` | `_PINNUM(0, 24)` | `variant.h` l.91 |
| `PIN_BUTTON2` | `_PINNUM(0, 18)` | `variant.h` l.95 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.93 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `_PINNUM(0, 2)` | `variant.h` l.26 |
| `PIN_VBAT_MEAS_EN` | `_PINNUM(0, 31)` | `TechoBoard.h` l.12 |
| `PIN_VBAT_READ` | `_PINNUM(0, 2)` | `TechoBoard.h` l.11 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.38 |
| `PINS_COUNT` | `(48)` | `variant.h` l.37 |
| `PIN_PWR_EN` | `_PINNUM(0, 30)` | `variant.h` l.24 |
| `PIN_QSPI_CS` | `_PINNUM(0, 12)` | `variant.h` l.67 |
| `PIN_QSPI_IO0` | `_PINNUM(0, 6)` | `variant.h` l.68 |
| `PIN_QSPI_IO1` | `_PINNUM(0, 8)` | `variant.h` l.69 |
| `PIN_QSPI_IO2` | `_PINNUM(1, 9)` | `variant.h` l.70 |
| `PIN_QSPI_IO3` | `_PINNUM(0, 26)` | `variant.h` l.71 |
| `PIN_QSPI_SCK` | `_PINNUM(0, 4)` | `variant.h` l.66 |
| `PIN_SERIAL1_RX` | `PIN_GPS_TX` | `variant.h` l.45 |
| `PIN_SERIAL1_TX` | `PIN_GPS_RX` | `variant.h` l.46 |


### `mesh_pocket`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `SX126X_CS` | `variant.h` l.93 |
| `P_LORA_BUSY` | `SX126X_BUSY` | `variant.h` l.97 |
| `P_LORA_DIO_1` | `SX126X_DIO1` | `variant.h` l.94 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.99 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.100 |
| `P_LORA_NSS` | `SX126X_CS` | `variant.h` l.95 |
| `P_LORA_RESET` | `SX126X_RESET` | `variant.h` l.96 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.98 |
| `SX126X_BUSY` | `(0 + 15)` | `variant.h` l.84 |
| `SX126X_CS` | `(0 + 26)` | `variant.h` l.82 |
| `SX126X_DIO1` | `(0 + 16)` | `variant.h` l.83 |
| `SX126X_RESET` | `(0 + 12)` | `variant.h` l.85 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(32+13)` | `variant.h` l.51 |
| `PIN_WIRE_SDA` | `(32+15)` | `variant.h` l.50 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(0)` | `variant.h` l.111 |
| `PIN_SPI1_MOSI` | `(20)` | `variant.h` l.112 |
| `PIN_SPI1_SCK` | `(22)` | `variant.h` l.113 |
| `PIN_SPI_MISO` | `(32 + 9)` | `variant.h` l.89 |
| `PIN_SPI_MOSI` | `(0 + 5)` | `variant.h` l.90 |
| `PIN_SPI_SCK` | `(0 + 4)` | `variant.h` l.91 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_DISPLAY_BUSY` | `(32 + 6)` | `variant.h` l.107 |
| `PIN_DISPLAY_CS` | `(24)` | `variant.h` l.106 |
| `PIN_DISPLAY_DC` | `(31)` | `variant.h` l.108 |
| `PIN_DISPLAY_RST` | `(32 + 4)` | `variant.h` l.109 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.68 |
| `PIN_BUTTON1` | `(32 + 10)` | `variant.h` l.67 |
| `PIN_LED` | `LED_BUILTIN` | `variant.h` l.57 |
| `PIN_STATUS_LED` | `LED_BUILTIN` | `variant.h` l.60 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.73 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(0 + 29)` | `variant.h` l.20 |
| `PIN_BAT_CTL` | `34` | `MeshPocket.h` l.9 |
| `PIN_BAT_CTRL` | `(32 + 2)` | `variant.h` l.21 |
| `PIN_VBAT_READ` | `29` | `MeshPocket.h` l.8 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.33 |
| `PINS_COUNT` | `(48)` | `variant.h` l.32 |
| `PIN_SERIAL1_RX` | `(37)` | `variant.h` l.40 |
| `PIN_SERIAL1_TX` | `(39)` | `variant.h` l.41 |
| `PIN_SERIAL2_RX` | `(7)` | `variant.h` l.43 |
| `PIN_SERIAL2_TX` | `(8)` | `variant.h` l.44 |


### `meshtiny`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(46)` | `variant.h` l.78 |
| `P_LORA_DIO_1` | `(47)` | `variant.h` l.76 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.74 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.75 |
| `P_LORA_NSS` | `(42)` | `variant.h` l.79 |
| `P_LORA_RESET` | `(38)` | `variant.h` l.77 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.73 |
| `P_LORA_TX_LED` | `PIN_LED2` | `variant.h` l.28 |
| `SX126X_POWER_EN` | `(37)` | `variant.h` l.80 |
| `SX126X_RXEN` | `RADIOLIB_NC` | `variant.h` l.82 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `variant.h` l.83 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `(14)` | `variant.h` l.93 |
| `PIN_BOARD_SDA` | `(13)` | `variant.h` l.92 |
| `PIN_WIRE_SCL` | `(14)` | `variant.h` l.91 |
| `PIN_WIRE_SDA` | `(13)` | `variant.h` l.90 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(29)` | `variant.h` l.68 |
| `PIN_SPI1_MOSI` | `(30)` | `variant.h` l.69 |
| `PIN_SPI1_SCK` | `(3)` | `variant.h` l.70 |
| `PIN_SPI_MISO` | `(45)` | `variant.h` l.64 |
| `PIN_SPI_MOSI` | `(44)` | `variant.h` l.65 |
| `PIN_SPI_SCK` | `(43)` | `variant.h` l.66 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.32 |
| `PIN_BUTTON1` | `(9)` | `variant.h` l.36 |
| `PIN_BUTTON2` | `(4)` | `variant.h` l.37 |
| `PIN_BUTTON3` | `(26)` | `variant.h` l.38 |
| `PIN_BUTTON4` | `(28)` | `variant.h` l.39 |
| `PIN_LED` | `LED_BUILTIN` | `variant.h` l.31 |
| `PIN_LED1` | `(35)` | `variant.h` l.21 |
| `PIN_LED2` | `(36)` | `variant.h` l.22 |
| `PIN_USER_BTN` | `PIN_SIDE_BUTTON` | `variant.h` l.44 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `(5)` | `variant.h` l.47 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.16 |
| `PINS_COUNT` | `(48)` | `variant.h` l.15 |
| `PIN_3V3_EN` | `(34)` | `variant.h` l.96 |
| `PIN_BUZZER` | `30` | `platformio.ini` l.34 |
| `PIN_SERIAL1_RX` | `(15)` | `variant.h` l.56 |
| `PIN_SERIAL1_TX` | `(16)` | `variant.h` l.57 |
| `PIN_SERIAL2_RX` | `(8)` | `variant.h` l.58 |
| `PIN_SERIAL2_TX` | `(6)` | `variant.h` l.59 |
| `PIN_SIDE_BUTTON` | `PIN_BUTTON1` | `variant.h` l.40 |


### `meshtracker_x1`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_BUSY` | `(7)` | `variant.h` l.97 |
| `LORA_DIO_1` | `(33)` | `variant.h` l.94 |
| `LORA_MISO` | `(PIN_SPI_MISO)` | `variant.h` l.99 |
| `LORA_MOSI` | `(PIN_SPI_MOSI)` | `variant.h` l.100 |
| `LORA_NSS` | `(PIN_SPI_NSS)` | `variant.h` l.95 |
| `LORA_RESET` | `(42)` | `variant.h` l.96 |
| `LORA_SCLK` | `(PIN_SPI_SCK)` | `variant.h` l.98 |
| `P_LORA_BUSY` | `7` | `platformio.ini` l.22 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.25 |
| `P_LORA_MISO` | `40` | `platformio.ini` l.26 |
| `P_LORA_MOSI` | `41` | `platformio.ini` l.27 |
| `P_LORA_NSS` | `12` | `platformio.ini` l.24 |
| `P_LORA_RESET` | `42` | `platformio.ini` l.28 |
| `P_LORA_SCLK` | `11` | `platformio.ini` l.23 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(46)` | `variant.h` l.61 |
| `PIN_WIRE_SDA` | `(47)` | `variant.h` l.60 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(40)` | `variant.h` l.69 |
| `PIN_SPI_MOSI` | `(41)` | `variant.h` l.70 |
| `PIN_SPI_NSS` | `(12)` | `variant.h` l.72 |
| `PIN_SPI_SCK` | `(11)` | `variant.h` l.71 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `GPS_RX_PIN` | `PIN_SERIAL1_RX` | `variant.h` l.106 |
| `GPS_TX_PIN` | `PIN_SERIAL1_TX` | `variant.h` l.107 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.89 |
| `LED_PIN` | `LED_GREEN` | `variant.h` l.81 |
| `PIN_BUTTON1` | `(6)` | `variant.h` l.88 |
| `PIN_STATUS_LED` | `24` | `platformio.ini` l.14 |
| `PIN_STATUS_LED_B` | `28` | `platformio.ini` l.17 |
| `PIN_STATUS_LED_G` | `24` | `platformio.ini` l.16 |
| `PIN_STATUS_LED_R` | `3` | `platformio.ini` l.15 |
| `PIN_USER_BTN` | `6` | `platformio.ini` l.12 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(2)` | `variant.h` l.23 |
| `PIN_BAT_ADC_EN` | `(38)` | `variant.h` l.20 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `BUZZER_PIN` | `(25)` | `variant.h` l.125 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.41 |
| `PINS_COUNT` | `(48)` | `variant.h` l.40 |
| `PIN_3V3_EN` | `(39)` | `variant.h` l.19 |
| `PIN_BUZZER` | `25` | `platformio.ini` l.85 |
| `PIN_DRV_EN` | `(37)` | `variant.h` l.120 |
| `PIN_FLASH_EN` | `(15)` | `variant.h` l.130 |
| `PIN_QSPI_CS` | `(20)` | `variant.h` l.133 |
| `PIN_QSPI_IO0` | `(21)` | `variant.h` l.134 |
| `PIN_QSPI_IO1` | `(22)` | `variant.h` l.135 |
| `PIN_QSPI_IO2` | `(23)` | `variant.h` l.136 |
| `PIN_QSPI_IO3` | `(32)` | `variant.h` l.137 |
| `PIN_QSPI_SCK` | `(19)` | `variant.h` l.132 |
| `PIN_RTC_EN` | `(9)` | `variant.h` l.21 |
| `PIN_SERIAL1_RX` | `(14)` | `variant.h` l.48 |
| `PIN_SERIAL1_TX` | `(13)` | `variant.h` l.49 |
| `PIN_SERIAL2_RX` | `(17)` | `variant.h` l.51 |
| `PIN_SERIAL2_TX` | `(16)` | `variant.h` l.52 |


### `minewsemi_me25ls01`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_BUSY` | `(32 + 10)` | `variant.h` l.66 |
| `LORA_CS` | `PIN_SPI_NSS` | `variant.h` l.70 |
| `LORA_DIO_1` | `(32 + 12)` | `variant.h` l.62 |
| `LORA_DIO_2` | `(32 + 10)` | `variant.h` l.63 |
| `LORA_MISO` | `(PIN_SPI_MISO)` | `variant.h` l.68 |
| `LORA_MOSI` | `(PIN_SPI_MOSI)` | `variant.h` l.69 |
| `LORA_NSS` | `(PIN_SPI_NSS)` | `variant.h` l.64 |
| `LORA_RESET` | `(32 + 11)` | `variant.h` l.65 |
| `LORA_SCLK` | `(PIN_SPI_SCK)` | `variant.h` l.67 |
| `P_LORA_BUSY` | `(32 + 10)` | `MinewsemiME25LS01Board.h` l.12 |
| `P_LORA_DIO_1` | `(32 + 12)` | `MinewsemiME25LS01Board.h` l.9 |
| `P_LORA_MISO` | `(0 + 29)` | `MinewsemiME25LS01Board.h` l.14 |
| `P_LORA_MOSI` | `(0 + 2)` | `MinewsemiME25LS01Board.h` l.15 |
| `P_LORA_NSS` | `(32 + 13)` | `MinewsemiME25LS01Board.h` l.10 |
| `P_LORA_RESET` | `(32 + 11)` | `MinewsemiME25LS01Board.h` l.11 |
| `P_LORA_SCLK` | `(32 + 15)` | `MinewsemiME25LS01Board.h` l.13 |
| `P_LORA_TX_LED` | `LED_RED` | `variant.h` l.52 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(16)` | `variant.h` l.36 |
| `PIN_WIRE_SDA` | `(21)` | `variant.h` l.35 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(0 + 29)` | `variant.h` l.42 |
| `PIN_SPI_MOSI` | `(0 + 2)` | `variant.h` l.43 |
| `PIN_SPI_NSS` | `(32 + 13)` | `variant.h` l.45 |
| `PIN_SPI_SCK` | `(32 + 15)` | `variant.h` l.44 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `GPS_RX_PIN` | `PIN_SERIAL1_RX` | `variant.h` l.85 |
| `GPS_TX_PIN` | `PIN_SERIAL1_TX` | `variant.h` l.86 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.59 |
| `LED_PIN` | `LED_BLUE` | `variant.h` l.51 |
| `PIN_BUTTON1` | `(0 + 27)` | `variant.h` l.58 |
| `PIN_STATUS_LED` | `39` | `platformio.ini` l.12 |
| `PIN_USER_BTN` | `27` | `platformio.ini` l.11 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(31)` | `variant.h` l.11 |
| `PIN_VBAT_READ` | `BATTERY_PIN` | `MinewsemiME25LS01Board.h` l.20 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `LR1110_BUSY_PIN` | `LORA_DIO_2` | `variant.h` l.77 |
| `LR1110_IRQ_PIN` | `LORA_DIO_1` | `variant.h` l.75 |
| `LR1110_NRESET_PIN` | `LORA_RESET` | `variant.h` l.76 |
| `LR1110_SPI_MISO_PIN` | `LORA_MISO` | `variant.h` l.81 |
| `LR1110_SPI_MOSI_PIN` | `LORA_MOSI` | `variant.h` l.80 |
| `LR1110_SPI_NSS_PIN` | `LORA_CS` | `variant.h` l.78 |
| `LR1110_SPI_SCK_PIN` | `LORA_SCLK` | `variant.h` l.79 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.20 |
| `PINS_COUNT` | `(48)` | `variant.h` l.19 |
| `PIN_SERIAL1_RX` | `(14)` | `variant.h` l.25 |
| `PIN_SERIAL1_TX` | `(13)` | `variant.h` l.26 |
| `PIN_SERIAL2_RX` | `(15)` | `variant.h` l.28 |
| `PIN_SERIAL2_TX` | `(17)` | `variant.h` l.29 |


### `muziworks_r1_neo`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(46)` | `variant.h` l.58 |
| `P_LORA_DIO_1` | `(47)` | `variant.h` l.55 |
| `P_LORA_MISO` | `(45)` | `variant.h` l.60 |
| `P_LORA_MOSI` | `(44)` | `variant.h` l.61 |
| `P_LORA_NSS` | `(42)` | `variant.h` l.56 |
| `P_LORA_RESET` | `RADIOLIB_NC` | `variant.h` l.57 |
| `P_LORA_SCLK` | `(43)` | `variant.h` l.59 |
| `P_LORA_TX_LED` | `LED_GREEN` | `variant.h` l.88 |
| `SX126X_POWER_EN` | `(37)` | `variant.h` l.62 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(RTC_SCL)` | `variant.h` l.144 |
| `PIN_WIRE_SDA` | `(RTC_SDA)` | `variant.h` l.143 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(10)` | `variant.h` l.137 |
| `PIN_SPI_MOSI` | `(9)` | `variant.h` l.136 |
| `PIN_SPI_SCK` | `(21)` | `variant.h` l.138 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_1PPS` | `GPS_PPS` | `variant.h` l.74 |
| `PIN_GPS_EN` | `(GPS_EN)` | `variant.h` l.128 |
| `PIN_GPS_RX` | `(GPS_RX)` | `variant.h` l.127 |
| `PIN_GPS_TX` | `(GPS_TX)` | `variant.h` l.126 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_USER_BTN` | `(26)` | `variant.h` l.94 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_BAT_CHG` | `(34)` | `variant.h` l.162 |
| `PIN_VBAT_READ` | `(31)` | `variant.h` l.161 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.43 |
| `PINS_COUNT` | `(48)` | `variant.h` l.42 |
| `PIN_A0` | `(0xFF)` | `variant.h` l.101 |
| `PIN_A1` | `(0xFF)` | `variant.h` l.102 |
| `PIN_A2` | `(4)` | `variant.h` l.103 |
| `PIN_A3` | `(5)` | `variant.h` l.104 |
| `PIN_A4` | `(0xFF)` | `variant.h` l.105 |
| `PIN_A5` | `(0xFF)` | `variant.h` l.106 |
| `PIN_A6` | `(0xFF)` | `variant.h` l.107 |
| `PIN_A7` | `(31)` | `variant.h` l.108 |
| `PIN_AREF` | `(0xFF)` | `variant.h` l.121 |
| `PIN_BUZZER` | `(3)` | `variant.h` l.97 |
| `PIN_DCDC_EN_MCU_HOLD` | `(13)` | `variant.h` l.48 |
| `PIN_MCU_SIGNAL` | `(30)` | `variant.h` l.50 |
| `PIN_QSPI_CS` | `(26)` | `variant.h` l.149 |
| `PIN_QSPI_IO0` | `(30)` | `variant.h` l.150 |
| `PIN_QSPI_IO1` | `(29)` | `variant.h` l.151 |
| `PIN_QSPI_IO2` | `(28)` | `variant.h` l.152 |
| `PIN_QSPI_IO3` | `(2)` | `variant.h` l.153 |
| `PIN_QSPI_SCK` | `(3)` | `variant.h` l.148 |
| `PIN_SERIAL1_RX` | `(PIN_GPS_RX)` | `variant.h` l.131 |
| `PIN_SERIAL1_TX` | `(PIN_GPS_TX)` | `variant.h` l.130 |
| `PIN_SOFT_SHUTDOWN` | `(29)` | `variant.h` l.49 |


### `nano_g2_ultra`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(32 + 11)` | `nano-g2.h` l.13 |
| `P_LORA_DIO_1` | `(32 + 10)` | `nano-g2.h` l.10 |
| `P_LORA_MISO` | `(32 + 9)` | `nano-g2.h` l.15 |
| `P_LORA_MOSI` | `(0 + 11)` | `nano-g2.h` l.16 |
| `P_LORA_NSS` | `(32 + 13)` | `nano-g2.h` l.11 |
| `P_LORA_RESET` | `(32 + 15)` | `nano-g2.h` l.12 |
| `P_LORA_SCLK` | `(0 + 12)` | `nano-g2.h` l.14 |
| `SX126X_BUSY` | `(32 + 11)` | `variant.h` l.119 |
| `SX126X_CS` | `(32 + 13)` | `variant.h` l.114 |
| `SX126X_DIO1` | `(32 + 10)` | `variant.h` l.115 |
| `SX126X_POWER_EN` | `37` | `nano-g2.h` l.20 |
| `SX126X_RESET` | `(32 + 15)` | `variant.h` l.120 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(0 + 15)` | `variant.h` l.89 |
| `PIN_WIRE_SDA` | `(0 + 17)` | `variant.h` l.88 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(32 + 9)` | `variant.h` l.157 |
| `PIN_SPI_MOSI` | `(0 + 11)` | `variant.h` l.158 |
| `PIN_SPI_SCK` | `(0 + 12)` | `variant.h` l.159 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `GPS_RX_PIN` | `PIN_GPS_RX` | `variant.h` l.139 |
| `GPS_TX_PIN` | `PIN_GPS_TX` | `variant.h` l.140 |
| `PIN_GPS_RX` | `(0 + 10)` | `variant.h` l.138 |
| `PIN_GPS_STANDBY` | `(0 + 13)` | `variant.h` l.136 |
| `PIN_GPS_TX` | `(0 + 9)` | `variant.h` l.137 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `nano-g2.h` l.24 |
| `PIN_BUTTON1` | `(32 + 6)` | `nano-g2.h` l.23 |
| `PIN_LED1` | `(-1)` | `variant.h` l.46 |
| `PIN_LED2` | `(-1)` | `variant.h` l.47 |
| `PIN_LED3` | `(-1)` | `variant.h` l.48 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `nano-g2.h` l.25 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `PIN_A4` | `variant.h` l.71 |
| `PIN_VBAT_READ` | `(0 + 2)` | `nano-g2.h` l.35 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.41 |
| `PINS_COUNT` | `(48)` | `variant.h` l.40 |
| `PIN_A4` | `(0 + 2)` | `variant.h` l.69 |
| `PIN_BUZZER` | `4` | `platformio.ini` l.73 |
| `PIN_QSPI_CS` | `(32 + 7)` | `variant.h` l.99 |
| `PIN_QSPI_IO0` | `(0 + 6)` | `variant.h` l.100 |
| `PIN_QSPI_IO1` | `(0 + 26)` | `variant.h` l.101 |
| `PIN_QSPI_IO2` | `(32 + 4)` | `variant.h` l.102 |
| `PIN_QSPI_IO3` | `(32 + 2)` | `variant.h` l.103 |
| `PIN_QSPI_SCK` | `(0 + 8)` | `variant.h` l.98 |
| `PIN_RTC_INT` | `(0 + 14)` | `variant.h` l.91 |
| `PIN_SERIAL1_RX` | `PIN_GPS_TX` | `variant.h` l.145 |
| `PIN_SERIAL1_TX` | `PIN_GPS_RX` | `variant.h` l.146 |
| `PIN_SERIAL2_RX` | `(0 + 22)` | `variant.h` l.80 |
| `PIN_SERIAL2_TX` | `(0 + 20)` | `variant.h` l.81 |


### `promicro`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(16)` | `variant.h` l.88 |
| `P_LORA_DIO_1` | `(11)` | `variant.h` l.86 |
| `P_LORA_MISO` | `(15)` | `variant.h` l.89 |
| `P_LORA_MOSI` | `(14)` | `variant.h` l.91 |
| `P_LORA_NSS` | `(13)` | `variant.h` l.85 |
| `P_LORA_RESET` | `(10)` | `variant.h` l.87 |
| `P_LORA_SCLK` | `(12)` | `variant.h` l.90 |
| `SX126X_POWER_EN` | `(21)` | `variant.h` l.92 |
| `SX126X_RXEN` | `(2)` | `variant.h` l.93 |
| `SX126X_TXEN` | `(-1)` | `variant.h` l.94 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `7` | `platformio.ini` l.13 |
| `PIN_BOARD_SDA` | `8` | `platformio.ini` l.14 |
| `PIN_WIRE_SCL` | `(7)` | `variant.h` l.48 |
| `PIN_WIRE_SDA` | `(6)` | `variant.h` l.47 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(19)` | `variant.h` l.64 |
| `PIN_SPI1_MOSI` | `(20)` | `variant.h` l.65 |
| `PIN_SPI1_SCK` | `(18)` | `variant.h` l.63 |
| `PIN_SPI_MISO` | `(3)` | `variant.h` l.58 |
| `PIN_SPI_MOSI` | `(4)` | `variant.h` l.59 |
| `PIN_SPI_NSS` | `(5)` | `variant.h` l.61 |
| `PIN_SPI_SCK` | `(2)` | `variant.h` l.57 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `5` | `platformio.ini` l.19 |
| `PIN_GPS_RX` | `3` | `platformio.ini` l.17 |
| `PIN_GPS_TX` | `4` | `platformio.ini` l.18 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.80 |
| `LED_PIN` | `PIN_LED` | `variant.h` l.71 |
| `PIN_BUTTON1` | `(6)` | `variant.h` l.79 |
| `PIN_LED` | `(22)` | `variant.h` l.70 |
| `PIN_USER_BTN` | `6` | `platformio.ini` l.16 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(17)` | `variant.h` l.25 |
| `PIN_VBAT_READ` | `17` | `PromicroBoard.h` l.7 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(23)` | `variant.h` l.32 |
| `PINS_COUNT` | `(23)` | `variant.h` l.31 |
| `PIN_EXT_VCC` | `(21)` | `variant.h` l.22 |
| `PIN_OLED_RESET` | `-1` | `platformio.ini` l.15 |
| `PIN_SERIAL1_RX` | `(0)` | `variant.h` l.40 |
| `PIN_SERIAL1_TX` | `(1)` | `variant.h` l.39 |
| `PIN_WIRE1_SCL` | `(14)` | `variant.h` l.50 |
| `PIN_WIRE1_SDA` | `(13)` | `variant.h` l.49 |


### `rak3401`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `SX126X_BUSY` | `variant.h` l.175 |
| `P_LORA_DIO_1` | `SX126X_DIO1` | `variant.h` l.174 |
| `P_LORA_MISO` | `PIN_SPI1_MISO` | `variant.h` l.171 |
| `P_LORA_MOSI` | `PIN_SPI1_MOSI` | `variant.h` l.172 |
| `P_LORA_NSS` | `SX126X_CS` | `variant.h` l.173 |
| `P_LORA_RESET` | `SX126X_RESET` | `variant.h` l.176 |
| `P_LORA_SCLK` | `PIN_SPI1_SCK` | `variant.h` l.170 |
| `SX126X_BUSY` | `(9)` | `variant.h` l.155 |
| `SX126X_CS` | `(26)` | `variant.h` l.153 |
| `SX126X_DIO1` | `(10)` | `variant.h` l.154 |
| `SX126X_POWER_EN` | `(21)` | `variant.h` l.164 |
| `SX126X_REGISTER_PATCH` | `1` | `platformio.ini` l.15 |
| `SX126X_RESET` | `(4)` | `variant.h` l.156 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(WB_I2C1_SCL)` | `variant.h` l.136 |
| `PIN_WIRE_SDA` | `(WB_I2C1_SDA)` | `variant.h` l.135 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(29)` | `variant.h` l.121 |
| `PIN_SPI1_MOSI` | `(30)` | `variant.h` l.122 |
| `PIN_SPI1_SCK` | `(3)` | `variant.h` l.123 |
| `PIN_SPI_MISO` | `(45)` | `variant.h` l.117 |
| `PIN_SPI_MOSI` | `(44)` | `variant.h` l.118 |
| `PIN_SPI_SCK` | `(43)` | `variant.h` l.119 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_1PPS` | `PIN_GPS_PPS` | `variant.h` l.194 |
| `PIN_GPS_PPS` | `(17)` | `variant.h` l.189 |
| `PIN_GPS_RX` | `PIN_SERIAL1_RX` | `variant.h` l.191 |
| `PIN_GPS_TX` | `PIN_SERIAL1_TX` | `variant.h` l.192 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_LED1` | `(35)` | `variant.h` l.48 |
| `PIN_LED2` | `(36)` | `variant.h` l.49 |
| `PIN_USER_BTN_ANA` | `31` | `platformio.ini` l.66 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `PIN_A0` | `variant.h` l.200 |
| `PIN_VBAT_READ` | `5` | `RAK3401Board.h` l.8 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.43 |
| `PINS_COUNT` | `(48)` | `variant.h` l.42 |
| `PIN_3V3_EN` | `(34)` | `RAK3401Board.h` l.11 |
| `PIN_A0` | `(5)` | `variant.h` l.62 |
| `PIN_A1` | `(31)` | `variant.h` l.63 |
| `PIN_A2` | `(28)` | `variant.h` l.64 |
| `PIN_A3` | `(29)` | `variant.h` l.65 |
| `PIN_A4` | `(30)` | `variant.h` l.66 |
| `PIN_A5` | `(31)` | `variant.h` l.67 |
| `PIN_A6` | `(0xff)` | `variant.h` l.68 |
| `PIN_A7` | `(0xff)` | `variant.h` l.69 |
| `PIN_AREF` | `(2)` | `variant.h` l.93 |
| `PIN_NFC1` | `(9)` | `variant.h` l.94 |
| `PIN_NFC2` | `(10)` | `variant.h` l.97 |
| `PIN_QSPI_CS` | `26` | `variant.h` l.141 |
| `PIN_QSPI_IO0` | `30` | `variant.h` l.142 |
| `PIN_QSPI_IO1` | `29` | `variant.h` l.143 |
| `PIN_QSPI_IO2` | `28` | `variant.h` l.144 |
| `PIN_QSPI_IO3` | `2` | `variant.h` l.145 |
| `PIN_QSPI_SCK` | `3` | `variant.h` l.140 |
| `PIN_SERIAL1_RX` | `(15)` | `variant.h` l.105 |
| `PIN_SERIAL1_TX` | `(16)` | `variant.h` l.106 |
| `PIN_SERIAL2_RX` | `(8)` | `variant.h` l.109 |
| `PIN_SERIAL2_TX` | `(6)` | `variant.h` l.110 |


### `rak4631`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(46)` | `variant.h` l.151 |
| `P_LORA_DIO_1` | `(47)` | `variant.h` l.148 |
| `P_LORA_MISO` | `(45)` | `variant.h` l.153 |
| `P_LORA_MOSI` | `(44)` | `variant.h` l.154 |
| `P_LORA_NSS` | `(42)` | `variant.h` l.149 |
| `P_LORA_RESET` | `(38)` | `variant.h` l.150 |
| `P_LORA_SCLK` | `(43)` | `variant.h` l.152 |
| `SX126X_POWER_EN` | `(37)` | `variant.h` l.155 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `14` | `platformio.ini` l.13 |
| `PIN_BOARD_SDA` | `13` | `platformio.ini` l.14 |
| `PIN_WIRE_SCL` | `(14)` | `variant.h` l.166 |
| `PIN_WIRE_SDA` | `(13)` | `variant.h` l.165 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(29)` | `variant.h` l.138 |
| `PIN_SPI_MOSI` | `(30)` | `variant.h` l.139 |
| `PIN_SPI_SCK` | `(3)` | `variant.h` l.140 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_1PPS` | `17` | `variant.h` l.185 |
| `PIN_GPS_EN` | `-1` | `platformio.ini` l.17 |
| `PIN_GPS_RX` | `PIN_SERIAL1_TX` | `platformio.ini` l.16 |
| `PIN_GPS_TX` | `PIN_SERIAL1_RX` | `platformio.ini` l.15 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_LED1` | `(35)` | `variant.h` l.69 |
| `PIN_LED2` | `(36)` | `variant.h` l.70 |
| `PIN_USER_BTN` | `9` | `platformio.ini` l.163 |
| `PIN_USER_BTN_ANA` | `31` | `platformio.ini` l.164 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `5` | `RAK4631Board.h` l.8 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.64 |
| `PINS_COUNT` | `(48)` | `variant.h` l.63 |
| `PIN_A0` | `(5)` | `variant.h` l.88 |
| `PIN_A1` | `(31)` | `variant.h` l.89 |
| `PIN_A2` | `(28)` | `variant.h` l.90 |
| `PIN_A3` | `(29)` | `variant.h` l.91 |
| `PIN_A4` | `(30)` | `variant.h` l.92 |
| `PIN_A5` | `(31)` | `variant.h` l.93 |
| `PIN_A6` | `(0xff)` | `variant.h` l.94 |
| `PIN_A7` | `(0xff)` | `variant.h` l.95 |
| `PIN_AREF` | `(2)` | `variant.h` l.116 |
| `PIN_NFC1` | `(9)` | `variant.h` l.117 |
| `PIN_NFC2` | `(10)` | `variant.h` l.118 |
| `PIN_OLED_RESET` | `-1` | `platformio.ini` l.18 |
| `PIN_QSPI_CS` | `26` | `variant.h` l.174 |
| `PIN_QSPI_IO0` | `30` | `variant.h` l.175 |
| `PIN_QSPI_IO1` | `29` | `variant.h` l.176 |
| `PIN_QSPI_IO2` | `28` | `variant.h` l.177 |
| `PIN_QSPI_IO3` | `2` | `variant.h` l.178 |
| `PIN_QSPI_SCK` | `3` | `variant.h` l.173 |
| `PIN_SERIAL1_RX` | `(15)` | `variant.h` l.126 |
| `PIN_SERIAL1_TX` | `(16)` | `variant.h` l.127 |
| `PIN_SERIAL2_RX` | `(19)` | `variant.h` l.130 |
| `PIN_SERIAL2_TX` | `(20)` | `variant.h` l.131 |
| `PIN_WIRE1_SCL` | `(25)` | `variant.h` l.169 |
| `PIN_WIRE1_SDA` | `(24)` | `variant.h` l.168 |


### `rak_wismesh_tag`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `(42)` | `variant.h` l.88 |
| `P_LORA_BUSY` | `SX126X_BUSY` | `platformio.ini` l.15 |
| `P_LORA_DIO_1` | `SX126X_DIO1` | `platformio.ini` l.12 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `platformio.ini` l.17 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `platformio.ini` l.18 |
| `P_LORA_NSS` | `PIN_SPI_NSS` | `platformio.ini` l.13 |
| `P_LORA_RESET` | `SX126X_RESET` | `platformio.ini` l.14 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `platformio.ini` l.16 |
| `P_LORA_TX_LED` | `LED_GREEN` | `platformio.ini` l.11 |
| `SX126X_BUSY` | `(46)` | `variant.h` l.90 |
| `SX126X_DIO1` | `(47)` | `variant.h` l.89 |
| `SX126X_POWER_EN` | `(37)` | `variant.h` l.92 |
| `SX126X_RESET` | `(38)` | `variant.h` l.91 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_BOARD_SCL` | `PIN_WIRE_SCL` | `platformio.ini` l.27 |
| `PIN_BOARD_SDA` | `PIN_WIRE_SDA` | `platformio.ini` l.26 |
| `PIN_WIRE_SCL` | `(24)` | `variant.h` l.50 |
| `PIN_WIRE_SDA` | `(25)` | `variant.h` l.49 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(29)` | `variant.h` l.99 |
| `PIN_SPI1_MOSI` | `(30)` | `variant.h` l.100 |
| `PIN_SPI1_SCK` | `(3)` | `variant.h` l.101 |
| `PIN_SPI_MISO` | `(45)` | `variant.h` l.57 |
| `PIN_SPI_MOSI` | `(44)` | `variant.h` l.58 |
| `PIN_SPI_NSS` | `(42)` | `variant.h` l.60 |
| `PIN_SPI_SCK` | `(43)` | `variant.h` l.59 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(34)` | `variant.h` l.114 |
| `PIN_GPS_PPS` | `(17)` | `variant.h` l.113 |
| `PIN_GPS_RX` | `(PIN_SERIAL1_TX)` | `variant.h` l.111 |
| `PIN_GPS_TX` | `(PIN_SERIAL1_RX)` | `variant.h` l.112 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.78 |
| `LED_PIN` | `LED_GREEN` | `variant.h` l.71 |
| `PIN_BUTTON1` | `(9)` | `variant.h` l.77 |
| `PIN_BUTTON2` | `(12)` | `variant.h` l.81 |
| `PIN_STATUS_LED` | `LED_BLUE` | `variant.h` l.69 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.79 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(5)` | `variant.h` l.24 |
| `PIN_VBAT_READ` | `5` | `RAKWismeshTagBoard.h` l.8 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.36 |
| `PINS_COUNT` | `(48)` | `variant.h` l.35 |
| `PIN_AREF` | `(2)` | `variant.h` l.118 |
| `PIN_BUZZER` | `(21)` | `variant.h` l.121 |
| `PIN_NFC1` | `(9)` | `variant.h` l.119 |
| `PIN_NFC2` | `(10)` | `variant.h` l.120 |
| `PIN_PWR_EN` | `(12)` | `variant.h` l.22 |
| `PIN_SERIAL1_RX` | `(15)` | `variant.h` l.43 |
| `PIN_SERIAL1_TX` | `(16)` | `variant.h` l.44 |
| `PIN_TXCO` | `(21)` | `variant.h` l.18 |


### `sensecap_solar`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `3` | `platformio.ini` l.19 |
| `P_LORA_DIO_1` | `1` | `platformio.ini` l.17 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.63 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.64 |
| `P_LORA_NSS` | `4` | `platformio.ini` l.20 |
| `P_LORA_RESET` | `2` | `platformio.ini` l.18 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.62 |
| `P_LORA_TX_LED` | `12` | `platformio.ini` l.16 |
| `SX126X_RXEN` | `5` | `platformio.ini` l.23 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `platformio.ini` l.24 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(15)` | `variant.h` l.70 |
| `PIN_WIRE_SDA` | `(14)` | `variant.h` l.69 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(9)` | `variant.h` l.57 |
| `PIN_SPI_MOSI` | `(10)` | `variant.h` l.58 |
| `PIN_SPI_SCK` | `(8)` | `variant.h` l.59 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_RX` | `PIN_SERIAL1_TX` | `variant.h` l.76 |
| `PIN_GPS_STANDBY` | `(0)` | `variant.h` l.77 |
| `PIN_GPS_TX` | `PIN_SERIAL1_RX` | `variant.h` l.75 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(13)` | `variant.h` l.33 |
| `PIN_BUTTON2` | `(20)` | `variant.h` l.34 |
| `PIN_LED` | `(12)` | `variant.h` l.21 |
| `PIN_USER_BTN` | `PIN_BUTTON1` | `variant.h` l.35 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(16)` | `variant.h` l.40 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(33)` | `variant.h` l.16 |
| `PINS_COUNT` | `(33)` | `variant.h` l.15 |
| `PIN_QSPI_CS` | `(22)` | `variant.h` l.82 |
| `PIN_QSPI_IO0` | `(23)` | `variant.h` l.83 |
| `PIN_QSPI_IO1` | `(24)` | `variant.h` l.84 |
| `PIN_QSPI_IO2` | `(25)` | `variant.h` l.85 |
| `PIN_QSPI_IO3` | `(26)` | `variant.h` l.86 |
| `PIN_QSPI_SCK` | `(21)` | `variant.h` l.81 |
| `PIN_SERIAL1_RX` | `(7)` | `variant.h` l.51 |
| `PIN_SERIAL1_TX` | `(6)` | `variant.h` l.52 |


### `t1000-e`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_BUSY` | `(7)` | `variant.h` l.97 |
| `LORA_DIO_1` | `(33)` | `variant.h` l.94 |
| `LORA_MISO` | `(PIN_SPI_MISO)` | `variant.h` l.99 |
| `LORA_MOSI` | `(PIN_SPI_MOSI)` | `variant.h` l.100 |
| `LORA_NSS` | `(PIN_SPI_NSS)` | `variant.h` l.95 |
| `LORA_RESET` | `(42)` | `variant.h` l.96 |
| `LORA_SCLK` | `(PIN_SPI_SCK)` | `variant.h` l.98 |
| `P_LORA_BUSY` | `7` | `platformio.ini` l.21 |
| `P_LORA_DIO_1` | `33` | `platformio.ini` l.24 |
| `P_LORA_MISO` | `40` | `platformio.ini` l.25 |
| `P_LORA_MOSI` | `41` | `platformio.ini` l.26 |
| `P_LORA_NSS` | `12` | `platformio.ini` l.23 |
| `P_LORA_RESET` | `42` | `platformio.ini` l.27 |
| `P_LORA_SCLK` | `11` | `platformio.ini` l.22 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(27)` | `variant.h` l.60 |
| `PIN_WIRE_SDA` | `(26)` | `variant.h` l.59 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(40)` | `variant.h` l.70 |
| `PIN_SPI_MOSI` | `(41)` | `variant.h` l.71 |
| `PIN_SPI_NSS` | `(12)` | `variant.h` l.73 |
| `PIN_SPI_SCK` | `(11)` | `variant.h` l.72 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `GPS_RX_PIN` | `PIN_SERIAL1_RX` | `variant.h` l.109 |
| `GPS_TX_PIN` | `PIN_SERIAL1_TX` | `variant.h` l.110 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.89 |
| `LED_PIN` | `LED_GREEN` | `variant.h` l.81 |
| `PIN_BUTTON1` | `(6)` | `variant.h` l.88 |
| `PIN_STATUS_LED` | `24` | `platformio.ini` l.14 |
| `PIN_USER_BTN` | `6` | `platformio.ini` l.12 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(2)` | `variant.h` l.24 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `BUZZER_PIN` | `(25)` | `variant.h` l.136 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.40 |
| `PINS_COUNT` | `(48)` | `variant.h` l.39 |
| `PIN_3V3_ACC_EN` | `(39)` | `variant.h` l.130 |
| `PIN_3V3_EN` | `(38)` | `variant.h` l.22 |
| `PIN_BUZZER` | `25` | `platformio.ini` l.83 |
| `PIN_BUZZER_EN` | `37` | `platformio.ini` l.84 |
| `PIN_SERIAL1_RX` | `(14)` | `variant.h` l.47 |
| `PIN_SERIAL1_TX` | `(13)` | `variant.h` l.48 |
| `PIN_SERIAL2_RX` | `(17)` | `variant.h` l.50 |
| `PIN_SERIAL2_TX` | `(16)` | `variant.h` l.51 |
| `QMA_6100P_INT_PIN` | `(34)` | `variant.h` l.63 |


### `thinknode_m1`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_CS` | `(24)` | `variant.h` l.94 |
| `P_LORA_BUSY` | `17` | `platformio.ini` l.16 |
| `P_LORA_DIO_1` | `20` | `platformio.ini` l.13 |
| `P_LORA_MISO` | `23` | `platformio.ini` l.18 |
| `P_LORA_MOSI` | `22` | `platformio.ini` l.19 |
| `P_LORA_NSS` | `24` | `platformio.ini` l.14 |
| `P_LORA_RESET` | `25` | `platformio.ini` l.15 |
| `P_LORA_SCLK` | `19` | `platformio.ini` l.17 |
| `P_LORA_TX_LED` | `13` | `platformio.ini` l.26 |
| `SX126X_BUSY` | `(17)` | `variant.h` l.96 |
| `SX126X_DIO1` | `(20)` | `variant.h` l.95 |
| `SX126X_POWER_EN` | `37` | `platformio.ini` l.20 |
| `SX126X_RESET` | `(25)` | `variant.h` l.97 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(27)` | `variant.h` l.49 |
| `PIN_WIRE_SDA` | `(26)` | `variant.h` l.48 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(38)` | `variant.h` l.104 |
| `PIN_SPI1_MOSI` | `(29)` | `variant.h` l.105 |
| `PIN_SPI1_SCK` | `(31)` | `variant.h` l.106 |
| `PIN_SPI_MISO` | `(23)` | `variant.h` l.56 |
| `PIN_SPI_MOSI` | `(22)` | `variant.h` l.57 |
| `PIN_SPI_NSS` | `(24)` | `variant.h` l.59 |
| `PIN_SPI_SCK` | `(19)` | `variant.h` l.58 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_PPS` | `(36)` | `variant.h` l.141 |
| `PIN_GPS_RESET` | `(37)` | `variant.h` l.140 |
| `PIN_GPS_RX` | `(40)` | `variant.h` l.137 |
| `PIN_GPS_STANDBY` | `(34)` | `variant.h` l.142 |
| `PIN_GPS_SWITCH` | `(33)` | `variant.h` l.143 |
| `PIN_GPS_TX` | `(41)` | `variant.h` l.138 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.81 |
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.71 |
| `PIN_BUTTON1` | `(42)` | `variant.h` l.80 |
| `PIN_BUTTON2` | `(11)` | `variant.h` l.84 |
| `PIN_LED` | `LED_BUILTIN` | `variant.h` l.70 |
| `PIN_STATUS_LED` | `LED_GREEN` | `variant.h` l.68 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.82 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(4)` | `variant.h` l.24 |
| `PIN_VBAT_READ` | `(4)` | `ThinkNodeM1Board.h` l.13 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.36 |
| `PINS_COUNT` | `(48)` | `variant.h` l.35 |
| `PIN_BUZZER` | `6` | `platformio.ini` l.84 |
| `PIN_NEOPIXEL` | `(14)` | `variant.h` l.74 |
| `PIN_PWR_EN` | `(12)` | `variant.h` l.22 |
| `PIN_QSPI_CS` | `(47)` | `variant.h` l.116 |
| `PIN_QSPI_IO0` | `(44)` | `variant.h` l.117 |
| `PIN_QSPI_IO1` | `(45)` | `variant.h` l.118 |
| `PIN_QSPI_IO2` | `(7)` | `variant.h` l.119 |
| `PIN_QSPI_IO3` | `(5)` | `variant.h` l.120 |
| `PIN_QSPI_SCK` | `(46)` | `variant.h` l.115 |
| `PIN_SERIAL1_RX` | `PIN_GPS_TX` | `variant.h` l.43 |
| `PIN_SERIAL1_TX` | `PIN_GPS_RX` | `variant.h` l.44 |
| `PIN_TXCO` | `(21)` | `variant.h` l.18 |


### `thinknode_m3`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `43` | `platformio.ini` l.19 |
| `P_LORA_DIO_1` | `40` | `platformio.ini` l.22 |
| `P_LORA_MISO` | `47` | `platformio.ini` l.23 |
| `P_LORA_MOSI` | `46` | `platformio.ini` l.24 |
| `P_LORA_NSS` | `44` | `platformio.ini` l.21 |
| `P_LORA_RESET` | `42` | `platformio.ini` l.25 |
| `P_LORA_SCLK` | `45` | `platformio.ini` l.20 |
| `P_LORA_TX_LED` | `PIN_LED_BLUE` | `platformio.ini` l.26 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(27)` | `variant.h` l.60 |
| `PIN_WIRE_SDA` | `(26)` | `variant.h` l.59 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(47)` | `variant.h` l.68 |
| `PIN_SPI_MOSI` | `(46)` | `variant.h` l.69 |
| `PIN_SPI_NSS` | `(44)` | `variant.h` l.71 |
| `PIN_SPI_SCK` | `(45)` | `variant.h` l.70 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(21)` | `variant.h` l.99 |
| `PIN_GPS_POWER` | `(14)` | `variant.h` l.98 |
| `PIN_GPS_RESET` | `(25)` | `variant.h` l.100 |
| `PIN_GPS_RX` | `(22)` | `variant.h` l.95 |
| `PIN_GPS_TX` | `(20)` | `variant.h` l.96 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.89 |
| `LED_PIN` | `PIN_LED_GREEN` | `variant.h` l.81 |
| `PIN_BUTTON1` | `(12)` | `variant.h` l.88 |
| `PIN_LED_BLUE` | `(37)` | `variant.h` l.78 |
| `PIN_LED_GREEN` | `(35)` | `variant.h` l.79 |
| `PIN_LED_RED` | `(33)` | `variant.h` l.80 |
| `PIN_STATUS_LED` | `35` | `platformio.ini` l.13 |
| `PIN_USER_BTN` | `12` | `platformio.ini` l.12 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `(5)` | `variant.h` l.35 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `BUZZER_PIN` | `(25)` | `variant.h` l.110 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.22 |
| `PINS_COUNT` | `(48)` | `variant.h` l.21 |
| `PIN_BUZZER` | `23` | `platformio.ini` l.84 |
| `PIN_BUZZER_EN` | `36` | `platformio.ini` l.85 |
| `PIN_PWR_EN` | `(16)` | `variant.h` l.44 |
| `PIN_SERIAL1_RX` | `PIN_GPS_TX` | `variant.h` l.50 |
| `PIN_SERIAL1_TX` | `PIN_GPS_RX` | `variant.h` l.51 |


### `thinknode_m6`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `43` | `platformio.ini` l.18 |
| `P_LORA_DIO_1` | `38` | `platformio.ini` l.15 |
| `P_LORA_MISO` | `47` | `platformio.ini` l.20 |
| `P_LORA_MOSI` | `46` | `platformio.ini` l.21 |
| `P_LORA_NSS` | `44` | `platformio.ini` l.16 |
| `P_LORA_RESET` | `42` | `platformio.ini` l.17 |
| `P_LORA_SCLK` | `45` | `platformio.ini` l.19 |
| `P_LORA_TX_LED` | `PIN_LED_BLUE` | `platformio.ini` l.27 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(8)` | `variant.h` l.53 |
| `PIN_WIRE_SDA` | `(41)` | `variant.h` l.52 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(47)` | `variant.h` l.60 |
| `PIN_SPI_MOSI` | `(46)` | `variant.h` l.61 |
| `PIN_SPI_SCK` | `(45)` | `variant.h` l.62 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(6)` | `variant.h` l.104 |
| `PIN_GPS_PPS` | `(31)` | `variant.h` l.112 |
| `PIN_GPS_RESET` | `(29)` | `variant.h` l.105 |
| `PIN_GPS_RX` | `(2)` | `variant.h` l.102 |
| `PIN_GPS_STANDBY` | `(30)` | `variant.h` l.111 |
| `PIN_GPS_TX` | `(3)` | `variant.h` l.103 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.81 |
| `LED_PIN` | `LED_BUILTIN` | `variant.h` l.74 |
| `PIN_BUTTON1` | `(17)` | `variant.h` l.80 |
| `PIN_LED` | `LED_BUILTIN` | `variant.h` l.73 |
| `PIN_LED_BLUE` | `(7)` | `variant.h` l.69 |
| `PIN_LED_RED` | `(12)` | `variant.h` l.68 |
| `PIN_USER_BTN` | `BUTTON_PIN` | `variant.h` l.82 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(28)` | `variant.h` l.23 |
| `PIN_VBAT_READ` | `BATTERY_PIN` | `ThinkNodeM6Board.h` l.12 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.36 |
| `PINS_COUNT` | `(48)` | `variant.h` l.35 |
| `PIN_ADC_CTRL` | `(11)` | `variant.h` l.25 |
| `PIN_PWR_EN` | `(27)` | `variant.h` l.21 |
| `PIN_QSPI_CS` | `(23)` | `variant.h` l.91 |
| `PIN_QSPI_IO0` | `(33)` | `variant.h` l.92 |
| `PIN_QSPI_IO1` | `(34)` | `variant.h` l.93 |
| `PIN_QSPI_IO2` | `(36)` | `variant.h` l.94 |
| `PIN_QSPI_IO3` | `(37)` | `variant.h` l.95 |
| `PIN_QSPI_SCK` | `(35)` | `variant.h` l.90 |
| `PIN_SERIAL1_RX` | `PIN_GPS_TX` | `variant.h` l.43 |
| `PIN_SERIAL1_TX` | `PIN_GPS_RX` | `variant.h` l.44 |
| `PIN_SERIAL2_RX` | `(22)` | `variant.h` l.46 |
| `PIN_SERIAL2_TX` | `(24)` | `variant.h` l.47 |


### `wio-tracker-l1`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `(3)` | `variant.h` l.70 |
| `P_LORA_DIO_1` | `(1)` | `variant.h` l.68 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.66 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.67 |
| `P_LORA_NSS` | `(4)` | `variant.h` l.71 |
| `P_LORA_RESET` | `(2)` | `variant.h` l.69 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.65 |
| `P_LORA_TX_LED` | `PIN_LED` | `variant.h` l.24 |
| `SX126X_RXEN` | `(5)` | `variant.h` l.72 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `variant.h` l.73 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(15)` | `variant.h` l.81 |
| `PIN_WIRE_SDA` | `(14)` | `variant.h` l.80 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(37)` | `variant.h` l.111 |
| `PIN_SPI1_MOSI` | `(33)` | `variant.h` l.112 |
| `PIN_SPI1_SCK` | `(31)` | `variant.h` l.113 |
| `PIN_SPI_MISO` | `(9)` | `variant.h` l.60 |
| `PIN_SPI_MOSI` | `(10)` | `variant.h` l.61 |
| `PIN_SPI_SCK` | `(8)` | `variant.h` l.62 |

**Display**

| Signal | Value | Source |
|---|---|---|
| `PIN_DISPLAY_BUSY` | `(35)` | `variant.h` l.107 |
| `PIN_DISPLAY_CS` | `(36)` | `variant.h` l.106 |
| `PIN_DISPLAY_DC` | `(34)` | `variant.h` l.108 |
| `PIN_DISPLAY_RST` | `(32)` | `variant.h` l.109 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_EN` | `(PIN_GPS_STANDBY)` | `variant.h` l.92 |
| `PIN_GPS_RX` | `PIN_SERIAL1_TX` | `variant.h` l.90 |
| `PIN_GPS_STANDBY` | `(0)` | `variant.h` l.91 |
| `PIN_GPS_TX` | `PIN_SERIAL1_RX` | `variant.h` l.89 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(13)` | `variant.h` l.28 |
| `PIN_BUTTON2` | `(25)` | `variant.h` l.29 |
| `PIN_BUTTON3` | `(26)` | `variant.h` l.30 |
| `PIN_BUTTON4` | `(27)` | `variant.h` l.31 |
| `PIN_BUTTON5` | `(28)` | `variant.h` l.32 |
| `PIN_BUTTON6` | `(29)` | `variant.h` l.33 |
| `PIN_LED` | `(11)` | `variant.h` l.21 |
| `PIN_USER_BTN` | `PIN_BUTTON6` | `variant.h` l.40 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT_READ` | `(16)` | `variant.h` l.48 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `PIN_WIRE1_SCL` | `platformio.ini` l.102 |
| `ENV_PIN_SDA` | `PIN_WIRE1_SDA` | `platformio.ini` l.101 |
| `NUM_DIGITAL_PINS` | `(38)` | `variant.h` l.16 |
| `PINS_COUNT` | `(38)` | `variant.h` l.15 |
| `PIN_BACK_BTN` | `PIN_BUTTON1` | `variant.h` l.34 |
| `PIN_BUZZER` | `12` | `platformio.ini` l.69 |
| `PIN_OLED_RESET` | `-1` | `platformio.ini` l.17 |
| `PIN_QSPI_CS` | `(20)` | `variant.h` l.96 |
| `PIN_QSPI_IO0` | `(21)` | `variant.h` l.97 |
| `PIN_QSPI_IO1` | `(22)` | `variant.h` l.98 |
| `PIN_QSPI_IO2` | `(23)` | `variant.h` l.99 |
| `PIN_QSPI_IO3` | `(24)` | `variant.h` l.100 |
| `PIN_QSPI_SCK` | `(19)` | `variant.h` l.95 |
| `PIN_SERIAL1_RX` | `(7)` | `variant.h` l.54 |
| `PIN_SERIAL1_TX` | `(6)` | `variant.h` l.55 |
| `PIN_WIRE1_SCL` | `(17)` | `variant.h` l.83 |
| `PIN_WIRE1_SDA` | `(18)` | `variant.h` l.82 |


### `wio-tracker-l1-eink`

**Other**

| Signal | Value | Source |
|---|---|---|
| `ENV_PIN_SCL` | `PIN_WIRE1_SCL` | `platformio.ini` l.29 |
| `ENV_PIN_SDA` | `PIN_WIRE1_SDA` | `platformio.ini` l.28 |
| `PIN_BUZZER` | `12` | `platformio.ini` l.54 |
| `PIN_OLED_RESET` | `-1` | `platformio.ini` l.18 |


### `wio_wm1110`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `LORA_BUSY` | `(43)` | `variant.h` l.96 |
| `LORA_CS` | `PIN_SPI_NSS` | `variant.h` l.100 |
| `LORA_DIO_1` | `(40)` | `variant.h` l.93 |
| `LORA_MISO` | `(PIN_SPI_MISO)` | `variant.h` l.98 |
| `LORA_MOSI` | `(PIN_SPI_MOSI)` | `variant.h` l.99 |
| `LORA_NSS` | `(PIN_SPI_NSS)` | `variant.h` l.94 |
| `LORA_RESET` | `(42)` | `variant.h` l.95 |
| `LORA_SCLK` | `(PIN_SPI_SCK)` | `variant.h` l.97 |
| `P_LORA_BUSY` | `43` | `platformio.ini` l.19 |
| `P_LORA_DIO_1` | `40` | `platformio.ini` l.17 |
| `P_LORA_MISO` | `47` | `platformio.ini` l.23 |
| `P_LORA_MOSI` | `46` | `platformio.ini` l.22 |
| `P_LORA_NSS` | `44` | `platformio.ini` l.20 |
| `P_LORA_RESET` | `42` | `platformio.ini` l.18 |
| `P_LORA_SCLK` | `45` | `platformio.ini` l.21 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `(26)` | `variant.h` l.52 |
| `PIN_WIRE_SDA` | `(27)` | `variant.h` l.51 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI_MISO` | `(47)` | `variant.h` l.68 |
| `PIN_SPI_MOSI` | `(46)` | `variant.h` l.69 |
| `PIN_SPI_NSS` | `(44)` | `variant.h` l.71 |
| `PIN_SPI_SCK` | `(45)` | `variant.h` l.70 |

**GPS**

| Signal | Value | Source |
|---|---|---|
| `PIN_GPS_RX` | `(-1)` | `variant.h` l.142 |
| `PIN_GPS_TX` | `(-1)` | `variant.h` l.141 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `BUTTON_PIN` | `PIN_BUTTON1` | `variant.h` l.88 |
| `LED_PIN` | `LED_GREEN` | `variant.h` l.80 |
| `PIN_BUTTON1` | `(-1)` | `variant.h` l.87 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `BATTERY_PIN` | `(31)` | `variant.h` l.19 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `LIS3DH_INT_PIN_1` | `(11)` | `variant.h` l.58 |
| `LIS3DH_INT_PIN_2` | `(12)` | `variant.h` l.59 |
| `LR1110_BUSY_PIN` | `LORA_BUSY` | `variant.h` l.110 |
| `LR1110_GNSS_ANT_PIN` | `(37)` | `variant.h` l.105 |
| `LR1110_IRQ_PIN` | `LORA_DIO_1` | `variant.h` l.108 |
| `LR1110_NRESET_PIN` | `LORA_RESET` | `variant.h` l.109 |
| `LR1110_SPI_MISO_PIN` | `LORA_MISO` | `variant.h` l.114 |
| `LR1110_SPI_MOSI_PIN` | `LORA_MOSI` | `variant.h` l.113 |
| `LR1110_SPI_NSS_PIN` | `LORA_CS` | `variant.h` l.111 |
| `LR1110_SPI_SCK_PIN` | `LORA_SCLK` | `variant.h` l.112 |
| `NUM_DIGITAL_PINS` | `(48)` | `variant.h` l.32 |
| `PINS_COUNT` | `(48)` | `variant.h` l.31 |
| `PIN_SERIAL1_RX` | `(22)` | `variant.h` l.39 |
| `PIN_SERIAL1_TX` | `(24)` | `variant.h` l.40 |
| `PIN_SERIAL2_RX` | `(6)` | `variant.h` l.42 |
| `PIN_SERIAL2_TX` | `(8)` | `variant.h` l.43 |
| `SENSOR_POWER_PIN` | `(7)` | `variant.h` l.55 |


### `xiao_nrf52`

**LoRa radio**

| Signal | Value | Source |
|---|---|---|
| `P_LORA_BUSY` | `D3` | `platformio.ini` l.21 |
| `P_LORA_DIO_1` | `D1` | `platformio.ini` l.19 |
| `P_LORA_MISO` | `PIN_SPI_MISO` | `variant.h` l.123 |
| `P_LORA_MOSI` | `PIN_SPI_MOSI` | `variant.h` l.124 |
| `P_LORA_NSS` | `D4` | `platformio.ini` l.22 |
| `P_LORA_RESET` | `D2` | `platformio.ini` l.20 |
| `P_LORA_SCLK` | `PIN_SPI_SCK` | `variant.h` l.122 |
| `P_LORA_TX_LED` | `11` | `platformio.ini` l.18 |
| `SX126X_RXEN` | `D5` | `platformio.ini` l.23 |
| `SX126X_TXEN` | `RADIOLIB_NC` | `platformio.ini` l.24 |

**I2C**

| Signal | Value | Source |
|---|---|---|
| `PIN_WIRE_SCL` | `D6` | `platformio.ini` l.29 |
| `PIN_WIRE_SDA` | `D7` | `platformio.ini` l.30 |

**SPI**

| Signal | Value | Source |
|---|---|---|
| `PIN_SPI1_MISO` | `(25)` | `variant.h` l.117 |
| `PIN_SPI1_MOSI` | `(26)` | `variant.h` l.118 |
| `PIN_SPI1_SCK` | `(29)` | `variant.h` l.119 |
| `PIN_SPI_MISO` | `(9)` | `variant.h` l.113 |
| `PIN_SPI_MOSI` | `(10)` | `variant.h` l.114 |
| `PIN_SPI_SCK` | `(8)` | `variant.h` l.115 |

**Buttons and LED**

| Signal | Value | Source |
|---|---|---|
| `PIN_BUTTON1` | `(0)` | `variant.h` l.42 |
| `PIN_LED` | `(LED_RED)` | `variant.h` l.27 |
| `PIN_STATUS_LED` | `(LED_BLUE)` | `variant.h` l.37 |
| `PIN_USER_BTN` | `PIN_BUTTON1` | `platformio.ini` l.31 |

**Power and battery**

| Signal | Value | Source |
|---|---|---|
| `PIN_VBAT` | `(32)` | `variant.h` l.70 |

**Other**

| Signal | Value | Source |
|---|---|---|
| `NUM_DIGITAL_PINS` | `(33)` | `variant.h` l.22 |
| `PINS_COUNT` | `(33)` | `variant.h` l.21 |
| `PIN_A0` | `(0)` | `variant.h` l.64 |
| `PIN_A1` | `(1)` | `variant.h` l.65 |
| `PIN_A2` | `(2)` | `variant.h` l.66 |
| `PIN_A3` | `(3)` | `variant.h` l.67 |
| `PIN_A4` | `(4)` | `variant.h` l.68 |
| `PIN_A5` | `(5)` | `variant.h` l.69 |
| `PIN_CHARGING_CURRENT` | `(22)` | `variant.h` l.60 |
| `PIN_LSM6DS3TR_C_INT1` | `(18)` | `variant.h` l.138 |
| `PIN_LSM6DS3TR_C_POWER` | `(15)` | `variant.h` l.137 |
| `PIN_NEOPIXEL` | `(PINS_COUNT)` | `variant.h` l.29 |
| `PIN_NFC1` | `(30)` | `variant.h` l.103 |
| `PIN_NFC2` | `(31)` | `variant.h` l.104 |
| `PIN_PDM_CLK` | `(20)` | `variant.h` l.142 |
| `PIN_PDM_DIN` | `(21)` | `variant.h` l.143 |
| `PIN_PDM_PWR` | `(19)` | `variant.h` l.141 |
| `PIN_QSPI_CS` | `(25)` | `variant.h` l.147 |
| `PIN_QSPI_IO0` | `(26)` | `variant.h` l.148 |
| `PIN_QSPI_IO1` | `(27)` | `variant.h` l.149 |
| `PIN_QSPI_IO2` | `(28)` | `variant.h` l.150 |
| `PIN_QSPI_IO3` | `(29)` | `variant.h` l.151 |
| `PIN_QSPI_SCK` | `(24)` | `variant.h` l.146 |
| `PIN_SERIAL1_RX` | `(7)` | `variant.h` l.107 |
| `PIN_SERIAL1_TX` | `(6)` | `variant.h` l.108 |

## Sources

- [`variants/`](https://github.com/meshcore-dev/MeshCore/tree/d92964352441e53b93e8667b802e04f6e072b39e/variants)
  — 36 directories of this family, each with a `platformio.ini` and the
  headers beside it
- [`tools/variant-pins.py`](https://github.com/pe1hvh/meshcore-docs/blob/main/tools/variant-pins.py) — the script that builds
  these tables

Related in this documentation:

- [Node matrix](../node-matrix.md) — which devices you can buy
- [MeshCore Platforms](../platforms.md) — why the platform matters
- [The four platform families](../platform-families.md) — what sits inside
  the chip per family
