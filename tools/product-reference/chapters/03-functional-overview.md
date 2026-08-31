## **3 Functional Overview**

The TEMT6000 sensor generates a light-dependent analog signal. That signal is
exposed at `SIG` and is acquired by the onboard controller through ADC input
`PA2` for DDP access. Controller output `PB5` drives the `BUILTIN` LED. The
missing V0.3.1 schematic must still confirm the passive circuitry and
electrical characteristics around these mapped signals.

### **3.1 Functional Paths** {.section-page}

![](tools/product-reference/assets/functional-block-diagram.png){width=7.1in}

**Figure 3.1 — Functional signal and control paths.** The direct `SIG` branch
and controller `PA2` ADC observe the sensor path. DDP publishes the averaged
sample through I2C and controls the internal `PB5/BUILTIN` indicator.

### **3.2 Board Topology**

| Region | Elements | Function |
|---|---|---|
| Direct-contact end | `VCC`, `GND`, `SIG`, `PA0`, `PA1` | Direct analog access and reserved GPIO pads |
| Upper center | TEMT6000 sensor and controller | Optical sensing; internal ADC acquisition on `PA2` |
| Center | Mounting hole and product identification | Mechanical attachment and identification |
| Qwiic end | Indicators, bus routing, optional connector | Host power and I2C communication |
| Bottom side | Qwiic, reset, and SWD aliases | Alternate connector; I2C/SWD share the same physical port |

### **3.3 I2C Mode** {.section-page}

With the I2C bridge intact, the onboard controller is connected to the module's
I2C path. Either populated Qwiic position can route `GND`, `VCC`, `SDA`, and
`SCL`; the pinout labels connectors as optional. The module operates as a
7-bit slave at bus clocks from 100 kHz through 400 kHz. In normal operation,
`PA10` and `PB6` are used as `SDA` and `SCL`; the factory-only SWD aliases on
those pins cannot operate simultaneously with I2C.

The onboard controller firmware uses DevLab Device Protocol v1.0. A host writes one
command byte, issues STOP, waits 2 to 5 ms, and then performs a separate
exact-length read.
Discovery reads protocol version, Device ID, firmware version, hardware
version, and capabilities before any feature command is used. The TEMT6000 is
identified by Device ID `0x0102`; `TEMT6000_RAW` (`0x80`) returns a 12-bit ADC
code (`0` to `4095`) as unsigned 16-bit little endian. Common `READ_ADC0`
(`0x60`) returns the same published `PA2` sample.

The factory 7-bit address is `0x20`; configurable values are `0x08..0x77`.
Current firmware/hardware versions are 1.0 and capabilities are `0x000001BB`.
Hosts must still verify DDP identity rather than recognizing the product from
its address alone.

### **3.4 I2C Address and DDP Command Map** {.section-page}

The bus address and command address are independent values. A library receives
the **7-bit I2C slave address** (`0x20` at the factory) and then sends one
**DDP command byte** from the map below. Do not pass the shifted wire bytes
`0x40`/`0x41` as the device address.

```text
host → [7-bit slave address + W] [DDP command byte] → STOP
       wait 2…5 ms
host ← [7-bit slave address + R] [exact response length] ← STOP
```

| DDP command-byte block | Commands defined for this profile | Current support |
|---:|---|---|
| `0x00..0x1F` Device information | `0x00 GET_DEVICE_ID`; `0x01 GET_FIRMWARE_VERSION`; `0x02 GET_HARDWARE_VERSION`; `0x03 GET_CAPABILITIES`; `0x04 GET_PROTOCOL` | Implemented; these five values form the identity/discovery sequence |
| `0x20..0x3F` Configuration | `0x20 GET_I2C_ADDR`; `0x21 SET_I2C_ADDR`; `0x22 SAVE_CONFIG`; `0x23 RESET_FACTORY`; `0x24 GET_I2C_STATUS` | Implemented; setters persist configuration and address changes require rediscovery |
| `0x40..0x5F` Digital I/O | `0x40 READ_GPIO0` | Reads `PA4`; `0x41 READ_GPIO1` and `0x42/0x43 WRITE_GPIO0/1` are unsupported |
| `0x60..0x7F` Analog input | `0x60 READ_ADC0`; `0x62 SET_ADC_AVERAGING`; `0x63 GET_ADC_AVERAGING` | Implemented for `PA2/ADC0`; `0x61 READ_ADC1` is unsupported |
| `0x80..0x9F` Sensor data | `0x80 TEMT6000_RAW` | Implemented; same unsigned 12-bit sample as `READ_ADC0` |
| `0xA0..0xBF` Actuators | `0xA0 RELAY_OFF`; `0xA1 RELAY_ON`; `0xA2 RELAY_TOGGLE`; `0xA3 SET_TOGGLE_TIME`; `0xA4 GET_TOGGLE_TIME` | Implemented for `PB5/BUILTIN`; other actuator bytes are unsupported |
| `0xC0..0xDF` Calibration | None | Capability is not announced; commands are unsupported |
| `0xE0..0xEF` Reserved | None | Reserved; do not use |
| `0xF0..0xFF` System | `0xF0 RESET`; `0xF1 WATCHDOG_RESET`; `0xF2 GET_RESET_INFO`; `0xF3 DISABLE_NRST`; `0xF4 CHECK_NRST` | `RESET` is implemented without a reply; watchdog is experimental; reset-info/NRST functions are unsupported or incomplete |

Any command byte not listed as implemented returns the current packed
unknown-command response. Staged commands (`0x21`, `0x62`, and `0xA3`) require
a separate value write within 250 ms; the command and value must not be sent in
the same I2C write transaction.

### **3.5 Direct Analog Mode**

The top-side `SIG` contact provides direct sensor access for ADC experiments,
production test, or calibration. Its V0.3.1 transfer function and safe input
range are not documented. Configure the host as a high-impedance analog input
and measure the actual range before connecting a lower-voltage ADC.

The controller samples this sensor path internally on `PA2`, mapped to logical
`ADC0`. `READ_ADC0` and the module-specific `TEMT6000_RAW` command are
equivalent in the current firmware.

### **3.6 I2C Disable Bridge** {.section-page}

The released pinout instructs the user to cut a solder bridge to disable I2C.
The missing current schematic leaves the exact isolation boundary unspecified.
Do not assume that cutting the bridge removes pull-ups, disconnects every
controller pin, or changes the analog transfer in a particular way. Rework only
with power removed and after continuity checks on the target revision.

### **3.7 Optical Response**

The reference-only Vishay document 81579 specifies a 570 nm peak, a 440 nm to
800 nm half-sensitivity spectral bandwidth, and a ±60° half-sensitivity angle
for its TEMT6000X01. These values are comparative, not guaranteed for the
unconfirmed fitted part. Source spectrum, temperature, sensor spread,
enclosure windows, and mechanical shadowing can also change the response.

### **3.8 Service and Expansion Signals**

The pinout exposes `PA0`, `PA1`, `RESET`, `SWDIO`, and `SWCLK`. `PA0` and `PA1`
have no application assignment in the current firmware and are reserved for
future use. `PA4` is logical read-only `GPIO0`; `PB5` is assigned internally to
the `BUILTIN` LED through the relay-compatible command block. `SWDIO`/`SWCLK`
are alternate functions of the same `PA10`/`PB6` pins used for `SDA`/`SCL`, not
a separate port. They and `RESET` are reserved for manufacturer programming
and advanced factory diagnostics; user firmware replacement is unsupported.
