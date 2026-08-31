## **4 Connectors & Pinouts**

Pin labels below come from the released English pinout. It does not
provide controlled contact numbers or a mating-connector part number, so the
signal order must be checked against connector orientation before producing a
harness.

### **4.1 General Pinout** {.section-page}

![](hardware/resources/pinout/v_0_3_1/unit_pinout_v_3_1_0_ue0098_temt6000_ambient_light_sensor_en.png){width=4.6in}

### **4.2 Direct Sensor Contacts**

| Label | Type | Description |
|---|---|---|
| `VCC` | Power | Module supply; nominal 3.3 V or 5 V operation |
| `GND` | Power | Common power and signal reference |
| `SIG` / `SIGNAL` | Analog | Direct light-dependent sensor signal; current transfer function unspecified |

These three contacts are shown at the end opposite the primary Qwiic connector.

### **4.3 Qwiic I2C Positions A and B** {.section-page}

| Signal | Type | Description |
|---|---|---|
| `GND` | Power | Common return |
| `VCC` | Power | I2C peripheral supply; nominal 3.3 V or 5 V |
| `SDA` / `SWDIO` | Bidirectional I2C / factory debug data | One physical `PA10` line; normal use is `SDA`; host must tolerate the bus pull-up voltage |
| `SCL` / `SWCLK` | I2C clock / factory debug clock | One physical `PB6` line; normal use is `SCL` at 100 kHz to 400 kHz |

The pinout shows two possible horizontal 1.0 mm JST connector positions and
marks JST connectors as optional. Verify which position is populated on the
ordered assembly. Parallel connectors are intended for bus pass-through, but
that topology must be confirmed by the current schematic.

I2C and SWD are multiplexed on this same physical port: `PA10` is
`SDA/SWDIO`, and `PB6` is `SCL/SWCLK`. They are mutually exclusive, and there
is no independent SWD connector or pin pair.

### **4.4 Auxiliary and Factory Service Functions**

| Label | Documented role | Qualification status |
|---|---|---|
| `PA0` | GPIO / reserved pin | No current application assignment; electrical limits unspecified |
| `PA1` | GPIO / reserved pin | No current application assignment; electrical limits unspecified |
| `RESET` | System reset | Factory service only; not intended for routine user operation |

Do not connect an SWD probe or drive reset/debug functions. They are not user
interfaces, and the product is not designed for user firmware replacement.
Manufacturer diagnostics must make I2C inactive and isolate other bus devices
before selecting SWD on the shared pins.

### **4.5 Indicators and I2C Bridge**

The pinout identifies a `POWER` LED, a firmware-controlled `BUILTIN` LED, and a
cuttable bridge used to disable I2C. Controller pin `PB5` drives `BUILTIN`.
Indicator polarity/current and bridge net connections still require the
current schematic. The sensor ADC input is mapped internally to controller
`PA2`; it is not an additional external contact in this pinout.
