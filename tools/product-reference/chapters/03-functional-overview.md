## **3 Functional Overview**

The TEMT6000 sensor generates a light-dependent analog signal. That signal is
exposed at `SIG` and is acquired by the onboard controller through ADC input
`PA2` for DDP access. Controller output `PB5` drives the `BUILTIN` LED. The
missing V0.3.1 schematic must still confirm the passive circuitry and
electrical characteristics around these mapped signals.

### **3.1 Functional Paths** {.section-page}

```text
                              ┌──────────────→ direct SIG contact
Ambient light → TEMT6000 ─────┤
                              └→ PA2 ADC · controller → PA10/SDA · PB6/SCL → host
                                             │
                            PB5 → BUILTIN · RESET

                       factory SWD aliases: PA10/SWDIO · PB6/SWCLK
                       (same physical pins as I2C; mutually exclusive)

                     PA0 / PA1 → reserved, no current application
```

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

### **3.4 Direct Analog Mode**

The top-side `SIG` contact provides direct sensor access for ADC experiments,
production test, or calibration. Its V0.3.1 transfer function and safe input
range are not documented. Configure the host as a high-impedance analog input
and measure the actual range before connecting a lower-voltage ADC.

The controller samples this sensor path internally on `PA2`, mapped to logical
`ADC0`. `READ_ADC0` and the module-specific `TEMT6000_RAW` command are
equivalent in the current firmware.

### **3.5 I2C Disable Bridge** {.section-page}

The released pinout instructs the user to cut a solder bridge to disable I2C.
The missing current schematic leaves the exact isolation boundary unspecified.
Do not assume that cutting the bridge removes pull-ups, disconnects every
controller pin, or changes the analog transfer in a particular way. Rework only
with power removed and after continuity checks on the target revision.

### **3.6 Optical Response**

The reference-only Vishay document 81579 specifies a 570 nm peak, a 440 nm to
800 nm half-sensitivity spectral bandwidth, and a ±60° half-sensitivity angle
for its TEMT6000X01. These values are comparative, not guaranteed for the
unconfirmed fitted part. Source spectrum, temperature, sensor spread,
enclosure windows, and mechanical shadowing can also change the response.

### **3.7 Service and Expansion Signals**

The pinout exposes `PA0`, `PA1`, `RESET`, `SWDIO`, and `SWCLK`. `PA0` and `PA1`
have no application assignment in the current firmware and are reserved for
future use. `PA4` is logical read-only `GPIO0`; `PB5` is assigned internally to
the `BUILTIN` LED through the relay-compatible command block. `SWDIO`/`SWCLK`
are alternate functions of the same `PA10`/`PB6` pins used for `SDA`/`SCL`, not
a separate port. They and `RESET` are reserved for manufacturer programming
and advanced factory diagnostics; user firmware replacement is unsupported.
