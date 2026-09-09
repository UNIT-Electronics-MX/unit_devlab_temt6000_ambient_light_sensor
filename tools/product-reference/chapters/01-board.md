## **1 The Board**

The design supports two host paths. A Qwiic-capable controller can attach
through the I2C positions, while an ADC-capable host or test instrument can
sample the exposed `SIG` contact directly. Factory programming and debugging
reuse the I2C signals; they are not a separate user interface.

### **1.1 Accessories** {.section-page}

No accessory bundle is specified. Typical integration items are:

| Accessory | Purpose | Selection notes |
|---|---|---|
| JST/Qwiic-compatible cable | Connects `GND`, `VCC`, `SDA`, and `SCL` | Verify 1.00 mm pitch, orientation, and contact order against the populated connector |
| I2C-capable host | Scans and communicates with the module | Use 7-bit addressing and a clock from 100 kHz through 400 kHz |
| Analog test lead or carrier | Accesses `VCC`, `GND`, and `SIG` | `SIG` must connect to a voltage-compatible ADC input |
| Logic analyzer | Checks I2C activity | Use input thresholds compatible with the powered board |
| Reference lux meter | Supports optical calibration | Required for quantitative illuminance validation |

### **1.2 Board Identification**

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

### **1.3 Identified Assemblies**

| Assembly | Function | Source status |
|---|---|---|
| TEMT6000 sensor | Converts visible light to photocurrent | Functional identity shown by board/pinout artwork; manufacturer and exact suffix unconfirmed |
| Interface controller | Samples and processes the sensor signal for I2C access | 32-bit Arm Cortex-M0+; 16 KB Flash and 2 KB SRAM |
| I2C connection positions | Provide module power and I2C bus access | `J1` is populated by default; `J3` and `J4` are optional horizontal 4-pin, 1.00 mm-pitch JST/Qwiic-compatible connector positions |
| Direct contacts | Provide `VCC`, `GND`, and analog `SIG` access | Identified on the top view |
| I2C disable bridge | Allows the I2C interface to be disconnected or disabled by cutting the bridge | Function identified; exact circuit implementation unspecified |
| Power and built-in indicators | Provide power and firmware-controlled status indication | Power and built-in indicators identified on the board |
| Reserved expansion pads | Reserved connections with no current application assignment | Two reserved pads identified on the board |
| Factory service functions | Provide controller programming, debug, and reset functions | Reserved for manufacturer use; programming signals share the I2C interface |

### **1.4 Board Layout and Reference Designators** {.section-page}

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
