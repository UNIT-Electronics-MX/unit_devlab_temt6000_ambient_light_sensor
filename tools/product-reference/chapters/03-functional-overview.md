## **3 Functional Overview**

The TEMT6000 sensor generates a light-dependent analog signal. That signal is
exposed at `SIG` and acquired by the onboard controller through `PA2/ADC0` for
DDP access. The controller uses its internal 24 MHz clock; this application
does not use an external oscillator. Controller output `PB5` drives the
`BUILTIN` LED.

The missing schematic must still confirm the passive sensor circuitry
and complete module electrical characteristics. The logical associations and
observable firmware behavior documented below are the released interface.

### **3.1 Functional Block Diagram** {.section-page}

![](tools/product-reference/assets/block_diagram.png){width=7.1in}

**Figure 3.1 — Functional signal and control paths.** The direct `SIG` branch
and controller `PA2` ADC observe the sensor path. Firmware averages the sample
and publishes it through DDP over I2C. The internal HSI supplies the 24 MHz
application clock; no HSE crystal or external clock is used.

### **3.2 Controller Clock and Execution Model** {.page-break}

| Property | Application configuration | Functional consequence |
|---|---|---|
| Controller core | 32-bit Arm Cortex-M0+ | Executes acquisition, DDP, configuration, and indicator control |
| Controller memory | 16 KB Flash and 2 KB SRAM | Memory configuration for this module |
| Maximum application clock | 24 MHz | Maximum clock used and documented for this product firmware |
| System-clock source | Internal high-speed oscillator (`HSI`) | Self-clocked controller operation |
| External high-speed clock (`HSE`) | Not used | No external oscillator or crystal is required by this application |
| ADC execution | Background task, approximately every 20 ms | Reads return the most recently published sample rather than starting a conversion |
| Command execution | Command is prepared after an I2C write | Host waits 2–5 ms before the exact-length read |

The 24 MHz value describes this application configuration. It must not be
replaced by a higher generic family maximum when specifying this product.

### **3.3 Measurement and Command Flow**

1. Ambient light changes the TEMT6000 analog output.
2. Controller input `PA2/ADC0` performs a 12-bit conversion.
3. Firmware discards one settling conversion, updates the circular sample
   buffer, and publishes the rounded average.
4. A host addresses the module and writes one DDP command byte.
5. After STOP and a 2–5 ms processing interval, the host reads the exact
   response length.
6. `READ_ADC0` and `TEMT6000_RAW` return the same latest published sample.

| Functional timing | Value | Notes |
|---|---:|---|
| ADC update interval | Approximately 20 ms | About 50 background updates per second |
| Averaging selections | 1, 4, 8, 16, or 24 samples | Persistent configuration |
| Full averaging-window fill | `N × 20 ms` | 20, 80, 160, 320, or 480 ms |
| I2C bus clock | 100 kHz to 400 kHz | Standard mode and Fast mode |
| Command-to-read delay | 2–5 ms | Use 5 ms conservatively |
| Staged-parameter timeout | 250 ms | Applies to `0x21`, `0x62`, and `0xA3` |

### **3.4 Logical Register Association Map** {.section-page}

DDP presents command-selected data fields rather than MCU memory addresses.
The following table associates each externally visible logical field with its
physical resource and command address.

| Logical field | Physical association | DDP command address | Data or behavior |
|---|---|---:|---|
| Device identity | Firmware constant | `0x00` | Device ID `0x0102` |
| Firmware version | Firmware metadata | `0x01` | Version 1.0 |
| Hardware version | Product profile | `0x02` | Version 1.0 |
| Capabilities | Firmware feature bitmap | `0x03` | `0x000001B9` |
| Protocol version | DDP implementation | `0x04` | DDP 1.0 |
| Active I2C address | I2C slave configuration | `0x20` | Factory `0x20`; configurable `0x08..0x77` |
| Persistent configuration | Internal Flash | `0x21..0x24`, `0x62`, `0xA3` | Address, averaging, and toggle time |
| `ADC0` | TEMT6000 signal on controller `PA2` | `0x60` | Unsigned 12-bit ADC code |
| ADC averaging | Circular sample buffer | `0x62`, `0x63` | 1, 4, 8, 16, or 24 samples |
| TEMT6000 sensor data | Same published `PA2/ADC0` sample | `0x80` | Same two-byte response as `0x60` |
| Built-in indicator | Controller `PB5/BUILTIN` | `0xA0..0xA4` | Off, on, toggle, and persistent pulse time |
| System reset | Controller reset path | `0xF0` | Resets without a response read |
| I2C service pins | `PA10/SDA`, `PB6/SCL` | Transport, not a data register | Shared with factory-only SWD aliases |
| Reserved contacts | `PA0`, `PA1` | None | No current application assignment |

### **3.5 I2C and DDP Register Model**

DDP is **not** a memory-mapped register interface. The first byte written after
the 7-bit slave address is a command selector analogous to a register address.
The command byte selects a prepared response or an operation; it does not expose
the PY32F003 memory map.

The bus address and command address are independent values. A host passes the
**7-bit I2C slave address** (`0x20` at the factory) to its library, then writes
one **DDP command address** from `0x00` through `0xFF`. Do not pass shifted wire
bytes `0x40`/`0x41` as the device address.

```text
host → [7-bit slave address + W] [DDP command address] → STOP
       wait 2…5 ms
host ← [7-bit slave address + R] [exact response length] ← STOP
```

Multi-byte values are little endian. Staged setters require a second one-byte
write transaction within 250 ms; the selector and parameter must not be sent
in the same I2C write transaction.

### **3.6 Global Command Address Map** {.section-page}

| DDP address block | Commands defined for this profile | Current support |
|---:|---|---|
| `0x00..0x1F` Device information | `0x00..0x04` | Identity and discovery registers implemented |
| `0x20..0x3F` Configuration | `0x20..0x24` | I2C address and persistent configuration implemented |
| `0x40..0x5F` Digital I/O | None | Not implemented on this module |
| `0x60..0x7F` Analog input | `0x60`, `0x62`, `0x63` | `ADC0/PA2` and averaging implemented; `0x61` unsupported |
| `0x80..0x9F` Sensor data | `0x80` | TEMT6000 raw sample implemented |
| `0xA0..0xBF` Actuators | `0xA0..0xA4` | `PB5/BUILTIN` indicator control implemented |
| `0xC0..0xDF` Calibration | None | Capability not announced; unsupported |
| `0xE0..0xEF` Reserved | None | Reserved; do not use |
| `0xF0..0xFF` System | `0xF0..0xF4` | Reset implemented; watchdog experimental; remaining functions incomplete or unsupported |

Any undefined or unsupported selector returns the current packed
unknown-command response with low nibble `0xB`.

### **3.7 Command Register Descriptions** {.section-page}

Access notation: `R` selects and reads a prepared response; `W` performs an
operation or begins a staged parameter write; `W/R` writes the selector and
then reads its acknowledgement or result.

#### **3.7.1 Device Information Registers**

| Address | Symbol | Access | Exact response | Association |
|---:|---|:---:|---|---|
| `0x00` | `GET_DEVICE_ID` | R | `[0x02, 0x01]` | Device ID `0x0102` |
| `0x01` | `GET_FIRMWARE_VERSION` | R | `[0x01, 0x00]` | Firmware major 1, minor 0 |
| `0x02` | `GET_HARDWARE_VERSION` | R | `[0x01, 0x00]` | Hardware major 1, minor 0 |
| `0x03` | `GET_CAPABILITIES` | R | `[0xB9, 0x01, 0x00, 0x00]` | Little-endian bitmap `0x000001B9` |
| `0x04` | `GET_PROTOCOL` | R | `[0x01, 0x00]` | DDP major 1, minor 0 |

Discovery order is `0x04`, `0x00`, `0x01`, `0x02`, then `0x03`. A host must
verify protocol major 1 and Device ID `0x0102`; the I2C address alone does not
identify the product.

#### **3.7.2 Configuration Registers**

| Address | Symbol | Access | Parameter or response | Association |
|---:|---|:---:|---|---|
| `0x20` | `GET_I2C_ADDR` | R | One-byte active 7-bit address | I2C peripheral address |
| `0x21` | `SET_I2C_ADDR` | W | Staged `0x08..0x77`; ACK low nibble `0xD` | Saves Flash and resets after final ACK |
| `0x22` | `SAVE_CONFIG` | W/R | Returns `0x00` | Idempotent; setters already persist |
| `0x23` | `RESET_FACTORY` | W/R | ACK low nibble `0xE` | Restores defaults; separate reset required |
| `0x24` | `GET_I2C_STATUS` | R | `0x00` default; `0x01` loaded from Flash | Address-source status |

#### **3.7.3 Input and Sensor Registers**

| Address | Symbol | Access | Parameter or response | Physical association |
|---:|---|:---:|---|---|
| `0x60` | `READ_ADC0` | R | `[LSB, MSB]`, valid code `0..4095` | Latest `PA2` sample |
| `0x62` | `SET_ADC_AVERAGING` | W | Staged `1`, `4`, `8`, `16`, or `24`; ACK low `0xC` | Persistent averaging depth |
| `0x63` | `GET_ADC_AVERAGING` | R | One byte: `1`, `4`, `8`, `16`, or `24` | Active averaging depth |
| `0x80` | `TEMT6000_RAW` | R | `[LSB, MSB]`, valid code `0..4095` | Same published sample as `0x60` |

`READ_GPIO0/1` (`0x40/0x41`), `WRITE_GPIO0/1` (`0x42/0x43`), and
`READ_ADC1` (`0x61`) are unsupported.

#### **3.7.4 Indicator and System Registers**

| Address | Symbol | Access | Parameter, response, or effect | Physical association |
|---:|---|:---:|---|---|
| `0xA0` | `RELAY_OFF` | W/R | ACK low nibble `0x0`; output LOW | `PB5/BUILTIN` off |
| `0xA1` | `RELAY_ON` | W/R | ACK low nibble `0x1`; output HIGH | `PB5/BUILTIN` on |
| `0xA2` | `RELAY_TOGGLE` | W/R | ACK low nibble `0x6`; non-blocking pulse | `PB5/BUILTIN` toggle |
| `0xA3` | `SET_TOGGLE_TIME` | W | Staged `1..40`; ACK low nibble `0x7` | Persistent units of 25 ms |
| `0xA4` | `GET_TOGGLE_TIME` | R | One byte `1..40` | Active pulse time |
| `0xF0` | `RESET` | W | Immediate reset; do not request a reply | Controller reset path |
| `0xF1` | `WATCHDOG_RESET` | W | Experimental; no active hardware IWDG | Firmware system block |
| `0xF2..0xF4` | Reset-info/NRST functions | — | Unsupported or incomplete | Reserved for future profile completion |

### **3.8 Response-Byte Interpretation**

Response bytes have meaning only within the selected command and expected
length. For example, `0x01` may mean firmware major 1, hardware major 1,
protocol major 1, the high byte of Device ID `0x0102`, or “address loaded from
Flash” from `GET_I2C_STATUS`. It is not a universal success code.

### **3.9 Direct Analog Mode**

The top-side `SIG` contact provides direct sensor access for ADC experiments,
production test, or calibration. Its transfer function and safe input
range are not documented. Configure the host as a high-impedance analog input
and measure the actual range before connecting a lower-voltage ADC.

The controller samples this sensor path internally on `PA2`, mapped to logical
`ADC0`. `READ_ADC0` and `TEMT6000_RAW` are equivalent in the current firmware.

### **3.10 I2C Disable Bridge** {.section-page}

The released pinout instructs the user to cut a solder bridge to disable I2C.
The missing current schematic leaves the exact isolation boundary unspecified.
Do not assume that cutting the bridge removes pull-ups, disconnects every
controller pin, or changes the analog transfer in a particular way. Rework only
with power removed and after continuity checks on the target revision.

### **3.11 Optical Response**

Reference-only TEMT6000X01 data lists a 570 nm peak, a 440 nm to 800 nm
half-sensitivity spectral bandwidth, and a ±60° half-sensitivity angle. These
values are comparative, not guaranteed for the unconfirmed fitted part. Source
spectrum, temperature, sensor spread, enclosure windows, and mechanical
shadowing can also change the response.

### **3.12 Service and Expansion Signals**

The pinout exposes `PA0`, `PA1`, `RESET`, `SWDIO`, and `SWCLK`. `PA0` and `PA1`
have no application assignment and are reserved for future use. `SWDIO` and
`SWCLK` are alternate functions of the same `PA10`/`PB6` pins used for
`SDA`/`SCL`, not a separate port. They and `RESET` are reserved for manufacturer
programming and advanced factory diagnostics; user firmware replacement is
unsupported.
