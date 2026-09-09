## **2 Ratings**

This chapter summarizes the electrical operating conditions and interface
characteristics relevant to integrating the UNIT ATOM TEMT6000. It covers the
module supply, I2C operation, analog sensor path, controller capabilities, and
ambient-light sensor characteristics. Use these ratings to select a compatible
power source and host interface and to identify the electrical characteristics
that require application-specific verification.

### **2.1 Recommended Operating Conditions** {.section-page}

| Symbol | Description | Min. | Typ. | Max. | Unit |
|---|---|---:|---:|---:|---|
| `VCC` | Module supply voltage | — | 3.3 or 5 | — | V |
| `VI2C` | I2C logic-high and pull-up voltage | — | `VCC` | — | V |
| `fSCL` | I2C clock frequency | 100 | — | 400 | kHz |
| `VSIG` | Direct analog `SIG` voltage range | — | Not specified | — | V |
| `ICC` | Module supply current | — | Not specified | — | mA |
| `TA` | Module ambient operating temperature | Not specified | — | Not specified | °C |

The `VCC` values are the supported nominal operating points; they are not
complete-module absolute maximum ratings. The validated continuous supply
range around each nominal point is not specified.

Use a current-limited source during initial bring-up. The I2C pull-ups follow
the module supply, so the host must tolerate the actual bus voltage. When the
module operates at 5 V with a 3.3 V host, bidirectional level translation may
be required.

The direct `SIG` range requires analog-stage verification and measurement.
Module current consumption must include the controller, indicators, pull-ups,
and sensor load. The complete-module ambient-temperature range has not been
qualified. I2C pull-up resistance, bus capacitance, and complete-module
absolute maximum ratings are also not specified.

### **2.2 Digital Interface and Firmware Characteristics**

| Parameter | Value | Description |
|---|---:|---|
| I2C addressing | 7-bit slave | Valid configurable addresses are `0x08..0x77` |
| Factory I2C address | `0x20` (7-bit) | Pass `0x20` directly to the host I2C library; `0x40` is the 8-bit write address, not the device address |
| Device protocol | DDP v1.0 | Command transaction followed by an exact-length read transaction |
| Logical Device ID | `0x0102` | TEMT6000 identity; independent of the I2C address |
| Firmware / hardware | 1.0 / 1.0 | Current observable controller profile |
| Capability bitmap | `0x000001B9` | I2C configuration, analog input, sensor data, relay, watchdog, and persistent configuration |
| Raw digital sample | `0` to `4095` | 12-bit ADC code returned as an unsigned 16-bit little-endian value |
| ADC update interval | Approximately 20 ms | Background acquisition; an I2C read returns the latest published sample |
| Command processing delay | 2 to 5 ms | Use 5 ms conservatively before reading |
| Pending setter timeout | 250 ms | Parameter must arrive before expiry |

These values describe the currently documented digital behavior. Detailed DDP
commands and transaction sequences are provided in Chapter 3.

### **2.3 Interface Controller Characteristics**

The available controller reference documentation identifies a 32-bit Arm Cortex-M0+ device with 16 KB Flash and 2 KB SRAM.

| Feature | Controller capability |
|---|---|
| CPU and application clock | 32-bit Arm Cortex-M0+; internal HSI at up to 24 MHz |
| Memory | 16 KB Flash and 2 KB SRAM |
| Controller operating-voltage guidance | 2.0–5.5 V; conservative range pending confirmation of the exact fitted variant |
| ADC | 12-bit analog-to-digital conversion used for sensor acquisition |
| I2C | Standard mode at 100 kHz and Fast mode at 400 kHz; 7-bit addressing |
| GPIO | General-purpose digital I/O and external-interrupt capability |
| Timers | General-purpose, advanced-control, low-power, watchdog, and system timing resources |
| Other interfaces | SPI, USART, DMA, RTC, CRC, comparators, unique device identification, and factory programming/debug functionality |

Programming and debugging functionality is reserved for factory use on this module. The controller operating range applies only to the controller and does not establish the absolute maximum ratings of the complete module or every externally accessible contact.

### **2.4 TEMT6000 Maximum Ratings**

The values below are included only as a comparative TEMT6000 profile. They do not confirm that a specific manufacturer or ordering variant is fitted to the module and must not be interpreted as complete-module ratings.

These values also do not define limits for the interface controller, indicators, pull-ups, connectors, or other board components.

| Parameter | Symbol | Value | Unit |
|---|---:|---:|---|
| Collector-emitter voltage | `VCEO` | 6 | V |
| Emitter-collector voltage | `VECO` | 1.5 | V |
| Collector current | `IC` | 20 | mA |
| Power dissipation at 25 °C | `PV` | 100 | mW |
| Junction temperature | `Tj` | 100 | °C |
| Component operating temperature | `Tamb` | −40 to +100 | °C |

### **2.5 TEMT6000 Characteristics** {.section-page}

Unless noted otherwise, the following values are specified at 25 °C and are provided for comparison only. Production specifications must be based on the confirmed fitted component and module-level validation.

| Parameter | Test condition | Min. | Typ. | Max. | Unit |
|---|---|---:|---:|---:|---|
| Collector dark current | `VCE = 5 V`, `Ev = 0` | — | 3 | 50 | nA |
| Collector light current | `Ev = 20 lx`, CIE illuminant A, `VCE = 5 V` | 3.5 | 10 | 16 | µA |
| Collector light current | `Ev = 100 lx`, CIE illuminant A, `VCE = 5 V` | — | 50 | — | µA |
| Collector-emitter capacitance | `VCE = 0 V`, `f = 1 MHz`, dark | — | 16 | — | pF |
| Collector-emitter saturation voltage | `Ev = 20 lx`, `IPCE = 1.2 µA` | — | 0.1 | — | V |
| Angle of half sensitivity | — | — | ±60 | — | degrees |
| Peak sensitivity wavelength | — | — | 570 | — | nm |
| Spectral bandwidth at half sensitivity | — | 440 | — | 800 | nm |

The component values in Sections 2.4 and 2.5 are published by Vishay in document 81579. The complete source is listed in Chapter 8, Reference Documentation.

### **2.6 Current Analog Circuit Scope**

The V2.0.0 schematic shows the TEMT6000 sensor with a 10 kΩ resistor (`R1`) to ground. The resulting `SIGNAL` net is connected to the controller ADC input and to the external `VCC`/`GND`/`SIG` header.

As a first-order estimate, `VSIGNAL ≈ IPCE × 10 kΩ` outside saturation. Applying the typical 100 lx photocurrent from the comparative TEMT6000 data gives an estimated signal of approximately 0.50 V. This calculation is an engineering estimate and must not be interpreted as a guaranteed or calibrated lux output.

The schematic also documents the I2C `SDA` and `SCL` signals, status indicators, pull-ups, test points, and the two optional I2C connector positions. The I2C connection points share controller signals with the factory programming/debug interface; there is no separate user-accessible SWD connector.

The direct `SIG` range, analog transfer accuracy, source impedance, loading behavior, and complete-module response still require measurement and qualification.

### **2.7 Unspecified Current-Module Characteristics** {.section-page}

- Complete-module absolute maximum ratings, current consumption, and power-up behavior
- Exact oscillator and timing tolerance
- Electrical I2C bus-loading limits
- Pull-up resistance and supported bus capacitance
- I2C logic-level compatibility under all supported supply conditions
- Direct analog transfer function, load resistance, range, accuracy, and source impedance
- Guaranteed lux measurement range, accuracy, repeatability, response time, and calibration
- Exact controller ordering variant
- Controlled firmware image and manufacturer programming procedure
- Board-level operating-temperature range
- ESD and EMC ratings
- Humidity and ingress ratings

Until these characteristics are validated, component-level specifications must not be interpreted as guaranteed complete-module specifications.

### **2.8 Electrical Precautions**

1. Use a current-limited 3.3 V or 5 V supply during engineering bring-up.
2. Verify connector orientation and establish a common ground before applying power.
3. Do not exceed the controller upper operating-voltage limit of 5.5 V.
4. When operating the module at 5 V, verify host compatibility with the actual voltage present on `SDA`, `SCL`, and `SIG`. Use appropriate level translation when required.
5. During normal operation, use the I2C connection points only for I2C communication. The same physical signals are shared with the controller's factory programming and debugging functions; SWD is not provided as a separate user interface.
6. Do not attempt firmware replacement or external debugging through the I2C connection points. Programming, debugging, and reset functions are reserved for manufacturer use and factory diagnostics.
7. Remove power before cutting, soldering, or reworking the I2C disable bridge or optional connector positions.
8. Verify the current released schematic, component specifications, and interface documentation before production integration.
