## **3 Functional Overview**

The UNIT ATOM TEMT6000 combines an ambient-light phototransistor with an
onboard controller. The module provides two ways to observe light level:
digital readings over I2C and direct access to the analog sensor signal at
`SIG`.

The TEMT6000 itself is an analog device. The onboard controller samples its
output, applies the selected averaging, and provides the latest raw reading
through DevLab Device Protocol (DDP) v1.0.

### **3.1 Functional Block Diagram** {.section-page}

![](tools/product-reference/assets/block_diagram.png){width=7.1in}

**Figure 3.1 — Functional signal and control paths.** Ambient light changes the
TEMT6000 output. The signal is available at `SIG` and is also sampled through
`PA2/ADC0` for access over I2C.

### **3.2 Operating Modes**

| Mode | Connection | User-visible result |
|---|---|---|
| Digital I2C | `VCC`, `GND`, `SDA`, and `SCL` | Averaged 12-bit raw light reading through DDP |
| Direct analog | `VCC`, `GND`, and `SIG` | Light-dependent voltage for a host ADC or measurement instrument |

Both modes observe the same sensor path. An I2C read returns the latest
available sample; it does not trigger a new light measurement. The direct
analog output may be used independently for development, comparison, or
application-specific calibration.

### **3.3 Digital Light Measurement** {.page-break}

The onboard ADC produces an unsigned 12-bit value. A higher value represents a
higher sensor output under the actual supply, optical, and mechanical
conditions.

| Measurement property | Value |
|---|---:|
| ADC resolution | 12 bits |
| Raw output range | `0..4095` |
| Response format | Two bytes, `[LSB, MSB]` |
| Update interval | Approximately 20 ms |
| Selectable averaging | 1, 4, 8, 16, or 24 samples |

The averaging setting controls the balance between response speed and
stability:

| Samples | Approximate time for a completely new average | Typical use |
|---:|---:|---|
| 1 | 20 ms | Fast changes |
| 4 | 80 ms | Low-latency smoothing |
| 8 | 160 ms | General monitoring |
| 16 | 320 ms | Stable ambient-light monitoring |
| 24 | 480 ms | Maximum available smoothing |

The result is a relative ADC reading, not a calibrated lux measurement.
Quantitative lux measurements require calibration in the final enclosure and
optical arrangement.

### **3.4 I2C Communication Model** {.page-break}

The I2C host always initiates communication. The 7-bit I2C address selects the
module, while the one-byte DDP selector identifies the requested function.
These are independent values.

![](tools/product-reference/assets/ddp_operation.png){width=7.1in}

**Figure 3.2 — DDP command and response over I2C.** The host writes one DDP
selector, issues STOP, waits 2–5 ms, and then reads the documented number of
response bytes. The host acknowledges intermediate bytes and sends NACK after
the final byte.

| Communication property | Value |
|---|---|
| Factory 7-bit address | `0x20` |
| Configurable address range | `0x08..0x77` |
| I2C clock | 100 kHz to 400 kHz |
| Delay before response read | 2–5 ms; use 5 ms conservatively |
| Byte order for multi-byte values | Little endian |
| Supported response lengths | 1, 2, or 4 bytes, depending on the selected function |

Pass `0x20` directly to an I2C library. Values `0x40` and `0x41` are the
shifted write/read address bytes visible on the bus, not the 7-bit address used
by typical host APIs.

### **3.5 User-Accessible DDP Functions** {.section-page}

| User function | DDP selector | Result |
|---|---:|---|
| Identify the module | `0x00` | Device ID `0x0102` |
| Read protocol version | `0x04` | DDP version 1.0 |
| Read active I2C address | `0x20` | Current 7-bit address |
| Change I2C address | `0x21` | Stores and applies a new address in the valid range |
| Restore factory configuration | `0x23` | Restores default configuration; reset required |
| Read ambient-light data | `0x60` or `0x80` | Latest two-byte 12-bit raw sample |
| Set ADC averaging | `0x62` | Selects 1, 4, 8, 16, or 24 samples |
| Read ADC averaging | `0x63` | Returns the active averaging setting |
| Turn `BUILTIN` off/on | `0xA0` / `0xA1` | Drives the built-in indicator LOW/HIGH |
| Pulse `BUILTIN` | `0xA2` | Starts a non-blocking timed pulse |
| Set/read pulse time | `0xA3` / `0xA4` | Uses 1–40 units of 25 ms |

The I2C address, averaging selection, and pulse duration are retained after a
power cycle. Changing a stored value should be an occasional configuration
operation rather than part of the normal measurement loop.

Detailed transaction handling is already implemented by the maintained C++
and MicroPython examples listed in Chapter 8.

### **3.6 Built-In Indicator**

`PB5/BUILTIN` is a user indicator controlled through the DDP actuator
functions. The shared DDP command names contain `RELAY`, but this product uses
them for the built-in indicator and does not provide an electromechanical
relay output.

The pulse duration is configurable from 25 ms to 1000 ms in 25 ms steps. A
timed pulse runs without interrupting light measurements or I2C communication.

### **3.7 Physical Interface Notes** {.section-page}

The `SIG` contact provides direct access to the analog sensor path. Its
complete board-level transfer function, source impedance, and guaranteed
output range are not specified for the current revision. Use a high-impedance
input and verify the actual range before connecting it to a lower-voltage ADC.

The normal I2C signals share controller pins with the service labels shown on
the board: `PA10` is `SDA/SWDIO`, and `PB6` is `SCL/SWCLK`. There is no
separate SWD connector. For normal product use, connect these lines as `SDA`
and `SCL`.

`PA0` and `PA1` are reserved and have no current user function. The I2C
disable bridge is intended for applications that require the analog path
without active I2C operation; remove power before cutting or restoring it.
