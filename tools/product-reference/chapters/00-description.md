## **Description**

The UNIT ATOM TEMT6000 is an ambient-light sensor module developed by UNIT Electronics as part of the DevLab ecosystem. It combines a TEMT6000 visible-light phototransistor with an onboard interface controller, providing both I²C communication and direct access to the sensor’s analog signal.

![](hardware/resources/v_3_1_0/unit_top_V_0_3_1_ue0098_temt6000.png){width=2.2in}

The board provides two alternative Qwiic connection positions, direct VCC, GND, and SIG contacts, reserved PA0 and PA1 pads, power and built-in status indicators, and a solder bridge for disabling the I²C interface. The controller reads the sensor through its PA2 ADC input. The built-in indicator is controlled through PB5, while the I²C interface uses PB6/SCL and PA10/SDA. These pins are also shared with the factory programming interface as SWCLK and SWDIO.

### **Applications**

- I2C-connected ambient-light acquisition
- Direct analog light measurement during development and calibration
- Automatic display and indicator brightness control
- Day/night and relative-light detection
- Environmental data logging
- Educational I2C, ADC, and phototransistor experiments

### **DevLab Format Compatibility**

As part of the DevLab Atom family, the TEMT6000 module uses a compact,
standardized format for rapid prototyping and integration into sensing systems.
It provides direct access to the analog signal through the `VCC`, `GND`, and
`SIG` contacts, while the onboard controller publishes digital sensor readings
through I²C. The module is intended for nominal 3.3 V or 5 V operation. The
controller guidance uses a conservative 2.0–5.5 V range; complete-module
electrical limits require the current schematic and validation.

The board has two optional positions for horizontal 4-pin, 1.00 mm-pitch
JST/Qwiic connectors carrying `GND`, `VCC`, `SDA`, and `SCL`. They provide
alternative I²C connection points. Before connection, confirm the populated
connector and its orientation, and ensure the host tolerates the actual I²C
pull-up voltage; a 3.3 V host may require level translation when the module is
powered at 5 V. The pull-up resistance is not specified by the released
documentation.

### **Hardware Features**

- TEMT6000 ambient-light phototransistor
- 32-bit Arm Cortex-M0+ controller with 16 KB Flash and 2 KB SRAM, using its internal HSI at up to 24 MHz
- Nominal 3.3 V and 5 V operation; controller upper operating limit 5.5 V
- 7-bit I2C slave operation from 100 kHz through 400 kHz
- Qwiic `GND`, `VCC`, `SDA`, and `SCL` routing
- Direct analog `SIG` access with adjacent `VCC` and `GND`
- Reserved `PA0` and `PA1` pads with no current application assignment
- Internal sensor ADC connection to controller pin `PA2`
- Shared `PB6/SCL/SWCLK` / `PA10/SDA/SWDIO` controller mapping
- Factory-only SWD/reset functions, power LED, and `PB5`-controlled built-in LED
- Cuttable solder bridge for disabling I2C operation
- Manufacturer Part Number (MPN) UE0098

The controller implements DevLab Device Protocol (DDP) v1.0. The TEMT6000
profile is identified by Device ID `0x0102`; command `TEMT6000_RAW` (`0x80`)
returns a 12-bit ADC sample in an unsigned 16-bit little-endian response. The
current controller firmware reports factory address `0x20`, firmware/hardware 1.0,
and capabilities `0x000001B9`.

`SWDIO` shares physical pin `PA10` with `SDA`, and `SWCLK` shares `PB6` with
`SCL`; there is no separate SWD port and the two modes are mutually exclusive.
SWD/reset are reserved for manufacturer programming and advanced factory
diagnostics, not user firmware replacement.
