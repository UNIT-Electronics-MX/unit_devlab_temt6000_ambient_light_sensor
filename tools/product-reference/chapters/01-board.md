## **1 The Board**

The V0.3.1 design supports two host paths. A Qwiic-capable controller can attach
through the I2C positions, while an ADC-capable host or test instrument can
sample the exposed `SIG` contact directly. Factory debug reuses the same
controller pins and physical port as I2C; it is not a separate user interface.

### **1.1 Accessories** {.section-page}

No accessory bundle is specified. Typical integration items are:

| Accessory | Purpose | Selection notes |
|---|---|---|
| Qwiic cable | Connects `GND`, `VCC`, `SDA`, and `SCL` | Verify 1.0 mm pitch, orientation, and contact order; connectors are shown as optional |
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
| Optical component | TEMT6000; fitted manufacturer/orderable part not confirmed |
| Interface controller | 32-bit Arm Cortex-M0+; fitted suffix not asserted; published voltage guidance uses the x7 range |
| Manufacturer Part Number (MPN) | UE0098 |
| Current board artwork | V0.3.1 |
| Available schematic | Legacy analog hardware V0.0.1 only |
| Product Reference | Version 1.1.0 |

Board, pinout, schematic, and documentation revisions are controlled
independently.

### **1.3 Identified Assemblies**

| Assembly | Function | Source status |
|---|---|---|
| TEMT6000 sensor | Converts visible light to photocurrent | Functional identity shown by board/pinout artwork; manufacturer and exact suffix unconfirmed |
| Interface controller | Samples or processes the sensor for I2C access | 32-bit Arm Cortex-M0+; fitted suffix not asserted; published voltage guidance uses the x7 range |
| Qwiic positions A and B | I2C power and bus access | Shown as optional horizontal JST connectors |
| Direct contacts | `VCC`, `GND`, and analog `SIG` | Identified on the top view |
| I2C disable bridge | Disconnects or disables I2C when cut | Function identified; exact circuit unspecified |
| Power and built-in LEDs | Power and firmware indication | `BUILTIN` is driven by controller `PB5` |
| PA0/PA1 and service functions | Reserved GPIO and factory reset/debug | `PA0`/`PA1` have no current application; SWD aliases share the I2C port |
| Internal controller mapping | `PA2` ADC, `PA4` input, `PB5` built-in actuator, `PB6/SCL/SWCLK`, `PA10/SDA/SWDIO` | Current firmware/hardware mapping |

### **1.4 Board Views** {.section-page}

![](hardware/resources/v_3_1_0/unit_top_V_0_3_1_ue0098_temt6000.png){width=2.35in}

The top view shows the direct sensor contacts, controller, sensor, mounting
hole, indicator circuitry, and one Qwiic connector position.

![](hardware/resources/v_3_1_0/unit_btm_V_0_3_1_ue0098_temt6000.png){width=2.35in}

The bottom view labels Qwiic, the SWD aliases on that same port, reset, and the
second optional connector position.

### **1.5 Handling** {.section-page}

Use normal ESD precautions. Keep the transparent sensor package clean and
optically unobstructed. Remove power before changing connectors or modifying
the I2C solder bridge. Do not attach an SWD probe or attempt to replace the
firmware. SWD/reset access is reserved for the manufacturer and advanced
factory diagnostics; I2C must be inactive and isolated before factory SWD use.
