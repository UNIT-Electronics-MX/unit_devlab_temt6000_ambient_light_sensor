## **1 The Board**

The design supports two host paths. A Qwiic-capable controller can attach
through the I2C positions, while an ADC-capable host or test instrument can
sample the exposed `SIG` contact directly. Factory programming and debugging
reuse the I2C signals; they are not a separate user interface.

### **1.1 Accessories** {.section-page}

The module is supplied with a Qwiic-compatible cable for connection to the I2C interface.

| Accessory | Purpose | Selection notes |
|---|---|---|
| JST/Qwiic-compatible cable | Connects `GND`, `VCC`, `SDA`, and `SCL` | Verify 1.00 mm pitch, connector orientation, and contact order against the populated connector |

### **1.2 Recommended Test Equipment** 

The following equipment may be used for integration, testing, and validation. These items are not included with the module.

| Equipment | Purpose | Selection notes |
|---|---|---|
| I2C-capable host | Scans and communicates with the module | Use 7-bit addressing and an I2C clock from 100 kHz through 400 kHz |
| Analog test lead or carrier | Provides access to `VCC`, `GND`, and `SIG` | `SIG` must connect to a voltage-compatible ADC input |
| Logic analyzer | Checks I2C communication activity | Use input thresholds compatible with the powered board |
| Reference lux meter | Supports optical calibration and validation | Required for quantitative illuminance validation |

### **1.3 Board Identification**

| Item | Value |
|---|---|
| Product | UNIT ATOM TEMT6000 Ambient Light Sensor |
| Brand / company | UNIT Electronics |
| Board ecosystem | DevLab |
| Product family | Atom |
| Product type | I2C-compatible and direct-analog ambient-light module |
| Optical component | TEMT6000 |
| Interface controller | 32-bit Arm Cortex-M0+; 16 KB Flash and 2 KB SRAM |
| Manufacturer Part Number (MPN) | UE0098 |
| Current board artwork | |
| Product Reference | Version 1.1.0 |

Board, pinout, schematic, and documentation revisions are controlled
independently.

### **1.4 Board Components and Features**

| Component / Feature | Function | Implementation / Notes |
|---|---|---|
| TEMT6000 sensor | Converts visible light to photocurrent | Primary ambient-light sensing element |
| Interface controller | Samples and processes the sensor signal for I2C access | 32-bit Arm Cortex-M0+ with 16 KB Flash and 2 KB SRAM |
| I2C connections | Provide module power and I2C bus access | `J1` is populated by default; `J3` and `J4` support optional horizontal 4-pin, 1.00 mm-pitch JST/Qwiic-compatible connectors |
| Direct contacts | Provide direct access to `VCC`, `GND`, and analog `SIG` | Intended for analog signal access and external ADC measurement |
| I2C disable bridge | Allows the I2C interface to be disabled | Cut `JP1` to disable I2C operation |
| Power indicator | Indicates that the board is powered | Onboard `PWR` indicator |
| Built-in status indicator | Provides firmware-controlled status indication | Onboard `USR_LED` indicator |
| Reserved expansion pads | Provide connections reserved for future expansion | No user function is currently assigned |
| Factory service functions | Support controller programming, debugging, and reset | Reserved for manufacturer use; programming signals share the I2C interface |

### **1.5 Board Layout and Reference Designators** {.section-page}

![](../../../hardware/resources/unit_topology_v_3_1_0_ue0098_temt6000_ambient_light_sensor.png){width=7.0in}

**Figure 1.1 — Location of components and reference designators on the top and
bottom sides of the PCB.**

This drawing is a component-location reference. It helps locate parts named in
the schematic and in the table below; it does not define connector pin order
or indicate that every connector footprint is populated.

The top side contains the TEMT6000 sensor (`Q1`), interface controller (`IC1`),
direct `VCC`/`GND`/`SIG` contacts (`J2`), and the I2C connector installed by
default (`J1`). The bottom side provides two additional footprints, `J3` and
`J4`, for optional horizontal I2C connectors. `J1`, `J3`, and `J4` carry the
same `GND`, `VCC`, `SDA`, and `SCL` signals and provide access to the same I2C
bus.

The drawing also locates the I2C-disable bridge (`JP1`), the power and status
indicators, and factory test points. Refer to Chapter 4 for user connections
and to the released schematic for circuit-level information.

| Ref. | Description |
|---|---|
| `Q1` | TEMT6000 ambient-light sensor |
| `IC1` | Onboard interface controller |
| `J1` | Factory-populated 4-pin, 1.00 mm-pitch I2C connector |
| `J3`, `J4` | Two optional horizontal 4-pin, 1.00 mm-pitch I2C connector positions |
| `J2` | Direct `VCC`/`GND`/`SIG` contacts |
| `JP1` | Cuttable bridge for disabling I2C operation |
| `PWR` | Power indicator |
| `USR_LED` | Built-in status indicator |
| `TP1`–`TP7` | Factory test points |

### **1.5 Board Views** {.section-page}

![](../../../hardware/resources/unit_top_v_0_3_1_ue0098_temt6000.png){width=2.35in}

The top view shows the direct sensor contacts, controller, sensor, mounting
hole, indicator circuitry, and the factory-populated I2C connector.

![](../../../hardware/resources/unit_btm_v_0_3_1_ue0098_temt6000.png){width=2.35in}

The bottom view shows the I2C connection points, reserved expansion pads,
factory service markings, and the optional horizontal connector positions.
The I2C signals are shared with the controller's factory programming and
debugging interface; there is no separate user-accessible SWD connector.

### **1.6 Handling** {.section-page}

Use normal ESD precautions. Keep the transparent sensor package clean and optically unobstructed. Remove power before changing connectors or modifying the I2C solder bridge.
