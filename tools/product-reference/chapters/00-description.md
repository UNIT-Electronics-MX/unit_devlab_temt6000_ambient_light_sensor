## **Description**

The UNIT ATOM TEMT6000 is an I2C-compatible ambient-light sensor module from
UNIT Electronics, the company that creates and develops the DevLab board
ecosystem. Atom is a product family within that ecosystem. Hardware V0.3.1
combines a TEMT6000 visible-light phototransistor with an onboard interface
controller, Qwiic I2C routing, and direct access to the sensor's analog
signal. The fitted sensor manufacturer and exact orderable suffix have not
been confirmed.

![](hardware/resources/v_3_1_0/unit_top_V_0_3_1_ue0098_temt6000.png){width=2.2in}

The released pinout identifies two optional Qwiic connection positions, direct
`VCC`/`GND`/`SIG` contacts, reserved `PA0` and `PA1` pads, factory-only reset
and SWD functions multiplexed on the I2C port, power and built-in indicators,
and a solder bridge that disables the
I2C function when cut. Inside the controller, the sensor ADC input is
`PA2`, digital input is `PA4`, `BUILTIN` is driven by `PB5`, and the I2C bus
uses `PB6/SCL/SWCLK` and `PA10/SDA/SWDIO`.

### **Applications**

- I2C-connected ambient-light acquisition
- Direct analog light measurement during development and calibration
- Automatic display and indicator brightness control
- Day/night and relative-light detection
- Environmental data logging
- Educational I2C, ADC, and phototransistor experiments

### **DevLab Format Compatibility**

As an Atom-family product within the DevLab ecosystem, the TEMT6000 follows the
compact DevLab integration format for rapid prototyping and reuse across
sensor and interface systems. The standardized layout preserves direct analog
`VCC`/`GND`/`SIG` access while adding controller-based I2C operation.

The module provides two optional positions for a horizontal 4-pin, 1.00 mm
pitch JST/Qwiic connector carrying `GND`, `VCC`, `SDA`, and `SCL`. Mechanical
format compatibility does not override electrical requirements: the module
supports nominal 3.3 V and 5 V operation, but the host must tolerate the
actual I2C pull-up voltage or use level translation. Verify connector
population and orientation, addresses, pull-ups, and bus loading.

### **Hardware Features**

- TEMT6000 ambient-light phototransistor; fitted manufacturer/orderable part not confirmed
- 32-bit Arm Cortex-M0+ controller using its internal HSI at up to 24 MHz; no external oscillator is used
- Nominal 3.3 V and 5 V operation; controller upper operating limit 5.5 V
- 7-bit I2C slave operation from 100 kHz through 400 kHz
- Qwiic `GND`, `VCC`, `SDA`, and `SCL` routing
- Direct analog `SIG` access with adjacent `VCC` and `GND`
- Reserved `PA0` and `PA1` pads with no current application assignment
- Internal sensor ADC connection to controller pin `PA2`
- Internal `PA4` input and shared `PB6/SCL/SWCLK` / `PA10/SDA/SWDIO` mapping
- Factory-only SWD/reset functions, power LED, and `PB5`-controlled built-in LED
- Cuttable solder bridge for disabling I2C operation
- Manufacturer Part Number (MPN) UE0098

The controller implements DevLab Device Protocol (DDP) v1.0. The TEMT6000
profile is identified by Device ID `0x0102`; command `TEMT6000_RAW` (`0x80`)
returns a 12-bit ADC sample in an unsigned 16-bit little-endian response. The
current controller firmware reports factory address `0x20`, firmware/hardware 1.0,
and capabilities `0x000001BB`. Procurement does not establish the fitted
controller suffix, so the published controller voltage guidance uses the
conservative x7 range without identifying the physical variant. The technical
package also does not provide the exact memory/package option,
current-revision schematic, or complete module electrical limits.

`SWDIO` shares physical pin `PA10` with `SDA`, and `SWCLK` shares `PB6` with
`SCL`; there is no separate SWD port and the two modes are mutually exclusive.
SWD/reset are reserved for manufacturer programming and advanced factory
diagnostics, not user firmware replacement.
