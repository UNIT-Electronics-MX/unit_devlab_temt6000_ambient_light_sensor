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
| Interface controller | 32-bit Arm Cortex-M0+; 16 KB Flash and 2 KB SRAM; fitted suffix not asserted |
| Manufacturer Part Number (MPN) | UE0098 |
| Current board artwork | |
| Product Reference | Version 1.1.0 |

Board, pinout, schematic, and documentation revisions are controlled
independently.

### **1.3 Identified Assemblies**

| Assembly | Function | Source status |
|---|---|---|
| TEMT6000 sensor | Converts visible light to photocurrent | Functional identity shown by board/pinout artwork; manufacturer and exact suffix unconfirmed |
| Interface controller | Samples and processes the sensor signal for I2C access | 32-bit Arm Cortex-M0+; 16 KB Flash and 2 KB SRAM; exact fitted variant not confirmed; conservative controller voltage guidance is 2.0–5.5 V |
| Optional I2C connector positions | Provide I2C power and bus access | Two positions are provided for optional horizontal 4-pin, 1.00 mm-pitch JST/Qwiic-compatible connectors |
| Direct contacts | Provide `VCC`, `GND`, and analog `SIG` access | Identified on the top view |
| I2C disable bridge | Allows the I2C interface to be disconnected or disabled by cutting the bridge | Function identified; exact circuit implementation unspecified |
| Power and built-in indicators | Provide power and firmware-controlled status indication | Power and built-in indicators identified on the board |
| Reserved expansion pads | Reserved connections with no current application assignment | Two reserved pads identified on the board |
| Factory service functions | Provide controller programming, debug, and reset functions | Reserved for manufacturer use; programming signals share the I2C interface |

### **1.4 Board Topology** {.section-page}

![](../../../hardware/resources/unit_topology_v_3_1_0_ue0098_temt6000_ambient_light_sensor.png){width=7.0in}

**Figure 1.1 — Board topology with top- and bottom-side reference
designators.**

The topology identifies the direct `VCC`/`GND`/`SIG` header `J2`, the three I2C
connection positions, I2C-disable bridge `JP1`, sensor `Q1`, controller `IC1`,
indicators, and factory service test points. One I2C connector is populated by
default; `J1` and `J3` are the two optional horizontal 4-pin, 1.00 mm-pitch
JST/Qwiic-compatible connector positions. All three positions provide physical
access to the same bus. Use the released schematic and pinout for electrical
connectivity and signal definitions.

| Ref. | Description |
|---|---|
| `TEMT6000` | Ambient Light Sensor |
| `IC1` | PY32F003L24D6TR I2C Driver / Controller |
| `J1`, `J3` | Optional horizontal I2C connector positions, 4-pin and 1.00 mm pitch |
| `J4` | Factory-populated I2C connector, 4-pin and 1.00 mm pitch |
| `J2` | `VCC`/`GND`/`SIG` header |
| `PWR` | Power indicator |
| `USR_LED` | Built-in status indicator |
| `TP` | Test points |

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
