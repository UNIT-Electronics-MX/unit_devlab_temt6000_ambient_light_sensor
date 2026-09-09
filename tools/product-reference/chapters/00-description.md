## **Description**

The UNIT ATOM TEMT6000 is an ambient-light sensor module developed by UNIT Electronics as part of the DevLab ecosystem. It combines a TEMT6000 visible-light phototransistor with an onboard interface controller, providing both I2C communication and direct access to the sensor’s analog signal.

The board provides direct VCC, GND, and SIG contacts, reserved expansion pads, power and status indicators, and a solder bridge for disabling the I2C interface. The onboard controller acquires the TEMT6000 signal through its analog-to-digital converter (ADC) and makes the resulting measurements available through the I2C interface.

### **Applications**

- I2C-connected ambient-light acquisition
- Direct analog light measurement during development and calibration
- Automatic display and indicator brightness control
- Day/night and relative-light detection
- Environmental data logging
- Educational I2C, ADC, and phototransistor experiments

### **DevLab Format Compatibility**

As part of the DevLab Atom family, the TEMT6000 module follows a compact and standardized form factor intended for rapid prototyping and integration with other DevLab modules. The board provides three 4-pin, 1.00 mm-pitch I2C connection positions carrying GND, VCC, SDA, and SCL. One connector is populated by default, while two additional horizontal positions are available for optional JST/Qwiic-compatible connectors. This arrangement provides multiple physical access points to the same I2C interface and supports different module integration and mounting configurations.

The module is designed for nominal 3.3 V or 5 V operation. Before connecting it to a host, verify the supply voltage, I2C pull-up voltage, connector orientation, and applicable electrical ratings. When operating the module at 5 V with a 3.3 V host, level translation may be required.

### **Hardware Features**

- TEMT6000 ambient-light phototransistor
- 32-bit Arm Cortex-M0+ controller with 16 KB Flash and 2 KB SRAM, using its internal HSI at up to 24 MHz
- Nominal 3.3 V and 5 V operation; controller upper operating limit of 5.5 V
- 7-bit I2C slave operation from 100 kHz to 400 kHz
- Three I2C connection positions carrying `GND`, `VCC`, `SDA`, and `SCL`: one populated by default and two optional horizontal positions
- Direct analog `SIG` access with adjacent `VCC` and `GND` contacts
- Two reserved expansion pads with no current application assignment
- Internal ADC acquisition of the TEMT6000 analog signal
- Shared I2C and factory programming signals
- Factory-only SWD/reset functions, power indicator, and built-in status indicator
- Cuttable solder bridge for disabling I2C operation
- Manufacturer Part Number (MPN): `UE0098`

The controller implements DevLab Device Protocol (DDP) v1.0. The TEMT6000 profile is identified by Device ID `0x0102`; command `TEMT6000_RAW` (`0x80`) returns a 12-bit ADC sample in an unsigned 16-bit little-endian response. The current controller firmware reports factory address `0x20`, firmware/hardware version 1.0, and capabilities `0x000001B9`.

The I2C data and clock signals are shared with the controller's factory programming interface; therefore, I2C communication and SWD programming cannot be used simultaneously. SWD and reset functions are reserved for manufacturer programming and advanced factory diagnostics, not for user firmware replacement.
