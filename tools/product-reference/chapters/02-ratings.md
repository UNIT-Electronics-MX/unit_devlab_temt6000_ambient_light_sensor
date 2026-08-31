## **2 Ratings**

No current-revision schematic or released board-level electrical table is
present for V0.3.1. This chapter therefore separates the expected Qwiic
integration domain from comparative TEMT6000X01 reference data and explicitly
marks current module values that still require release. That external data
does not identify the manufacturer or exact part fitted to the board.

### **2.1 Current Module Operating Conditions** {.section-page}

| Parameter | Value | Status |
|---|---:|---|
| Nominal module supply | 3.3 V or 5 V | Supported operating points; use a current-limited source during bring-up |
| Controller operating voltage | x7: 2.0–5.5 V | Selected product variant; supports nominal 3.3 V and 5 V |
| I2C logic domain | Follows the actual bus pull-up rail | At 5 V, use a 5 V-tolerant host or bidirectional level translation |
| I2C bus speed | 100 kHz to 400 kHz | Supported operating range |
| I2C addressing | 7-bit slave | Valid configurable addresses are `0x08..0x77` |
| Factory I2C address | `0x20` | Pass the 7-bit value, not wire byte `0x40` |
| Device protocol | DDP v1.0 | Command transaction followed by an exact-length read transaction |
| Logical Device ID | `0x0102` | TEMT6000 identity; independent of I2C address |
| Firmware / hardware | 1.0 / 1.0 | Current observable controller profile |
| Capability bitmap | `0x000001BB` | I2C config, digital input, analog input, sensor data, relay, watchdog, persistent config |
| Raw digital sample | `0` to `4095` | 12-bit ADC code returned as unsigned 16-bit little endian |
| ADC update interval | Approximately 20 ms | Background acquisition; I2C read returns latest published sample |
| Command processing delay | 2 to 5 ms | Use 5 ms conservatively before reading |
| Pending setter timeout | 250 ms | Parameter must arrive before expiry |
| Direct `SIG` range | Not specified | Requires current analog-stage schematic and measurement |
| Module current consumption | Not specified | Controller, LEDs, pull-ups, and sensor load are undocumented |
| Module ambient temperature | Not specified | No complete-module qualification supplied |

Nominal 5 V operation is supported by the controller; do not exceed
its 5.5 V upper operating limit. The direct `SIG` path and I2C levels are
referenced to the powered system, so every attached host must tolerate the
resulting voltage or use level translation. Complete-module absolute maximums
still require the V0.3.1 schematic and qualification.

### **2.2 Interface Controller Characteristics**

The interface controller is a PY32F003 x7 variant. The following
characteristics apply to this selected controller variant. The exact memory
density and package fitted to this module have not yet been recorded.

| Feature | Controller capability |
|---|---|
| CPU | 32-bit Arm Cortex-M0+, up to 32 MHz |
| Memory | Up to 64 KB Flash and up to 8 KB SRAM |
| Operating voltage | 2.0–5.5 V |
| ADC | One 12-bit ADC, up to 10 external channels, conversion range `0..VCC` |
| I2C | Standard mode 100 kHz, Fast mode 400 kHz, 7-bit addressing |
| GPIO | Up to 18 I/Os, all available as external interrupts |
| Timers | TIM1, TIM3, TIM14, TIM16, TIM17, LPTIM, IWDG, WWDG, SysTick, IRTIM |
| Other interfaces | SPI, two USARTs, DMA, RTC, CRC-32, two comparators, UID; SWD is reserved for factory use on this module |
| Operating temperature | −40 to +105 °C |

The controller range establishes that 5 V is valid. It does
not by itself establish pull-up resistance, complete-module current, or the
absolute maximum of every external contact.

### **2.3 Reference-Only TEMT6000X01 Maximum Ratings**

The values below come from Vishay document 81579 and are included only as a
comparative TEMT6000X01 profile. They are not proof that a Vishay part is
fitted, are not guaranteed for the fitted sensor, and do not define limits for
the V0.3.1 controller, LEDs, pull-ups, connectors, or complete board.

| Parameter | Symbol | Value | Unit |
|---|---:|---:|---|
| Collector-emitter voltage | `VCEO` | 6 | V |
| Emitter-collector voltage | `VECO` | 1.5 | V |
| Collector current | `IC` | 20 | mA |
| Power dissipation at 25 °C | `PV` | 100 | mW |
| Junction temperature | `Tj` | 100 | °C |
| Component operating temperature | `Tamb` | −40 to +100 | °C |

### **2.4 Reference-Only TEMT6000X01 Characteristics** {.section-page}

Unless noted otherwise, these are values published in Vishay document 81579
at 25 °C and are provided for comparison only. Production specifications must
come from the confirmed fitted part and module-level validation.

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

### **2.5 Legacy Analog Circuit Scope**

The V0.0.1 schematic shows a TEMT6000 with a 10 kΩ emitter resistor, giving the
first-order relation `VSIGNAL ≈ IPCE × 10 kΩ` outside saturation. Applying the
100 lx typical current from the reference-only datasheet predicts about 0.50 V;
this is not a guaranteed current-board value.

V0.3.1 adds an interface controller and other circuitry. Without its schematic,
the legacy resistor value and transfer function must not be represented as a
guaranteed current-board characteristic. Direct `SIG` must be measured and
validated on V0.3.1.

### **2.6 Unspecified Current-Module Characteristics** {.section-page}

- Complete-module absolute maximum, current consumption, and power-up behavior
- Exact oscillator/timing tolerance and electrical bus-loading limits
- Pull-up resistance, bus capacitance allowance, and level compatibility
- Direct analog transfer function, load resistance, range, accuracy, and source impedance
- Guaranteed lux range, accuracy, repeatability, response time, and calibration
- Exact controller memory/package option, released firmware image, and update procedure
- Board-level temperature, ESD, EMC, humidity, and ingress ratings

### **2.7 Electrical Precautions**

1. Use a current-limited 3.3 V or 5 V supply for engineering bring-up.
2. Verify connector orientation and share ground before applying power.
3. Do not exceed the controller upper operating limit of 5.5 V.
4. At 5 V, confirm host tolerance at `SDA`, `SCL`, and `SIG`, or add suitable
   level translation before connection.
5. Do not connect to reset or SWD; these signals are reserved for manufacturer
   programming and advanced factory diagnostics, not user firmware replacement.
6. Remove power before cutting or reworking the I2C solder bridge.
7. Confirm the current schematic and interface specification before production.
