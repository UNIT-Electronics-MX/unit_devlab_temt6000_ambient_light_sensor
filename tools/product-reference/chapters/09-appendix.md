## **9 Appendix**

### **9.1 Legacy V0.0.1 Schematic** {.section-page}

The image below is rendered from
`hardware/unit_sch_V_0_0_1_ue0098_TEMT6000.pdf`. It documents the former
analog-only module and is retained for traceability. It is **not** the
electrical schematic for the controller-based V0.3.1 board.

![](hardware/resources/unit_schematic_V_0_0_1_ue0098_TEMT6000.png){width=7.1in}

The legacy circuit connects a TEMT6000 phototransistor and 10 kΩ load to one
analog signal. It contains no interface controller, SDA, SCL, PA0, PA1, reset,
SWD, indicators, or I2C disable bridge.

### **9.2 Document Control** {.section-page}

| Field | Value |
|---|---|
| Product | UNIT ATOM TEMT6000 Ambient Light Sensor |
| Product hierarchy | UNIT Electronics → DevLab board ecosystem → Atom family |
| Manufacturer Part Number (MPN) | UE0098 |
| Current board artwork | V0.3.1 |
| Current pinout | V3.1.0 |
| Available schematic | Legacy V0.0.1 only |
| Product Reference | Version 1.1.0 |
| Publication date | 2026-08-31 |
| Interfaces | Qwiic I2C with shared factory SWD, analog, and auxiliary pads |

### **9.3 Required Technical Releases**

- V0.3.1 schematic and bill of materials
- Exact controller memory/package option, released firmware image, and update procedure
- Exact oscillator/timing tolerances and uniform future DDP status behavior
- Complete-module supply/logic absolute-maximum ratings and current consumption
- Pull-up values and bus-loading limits
- Direct `SIG` transfer, loading, range, and ADC guidance
- Current-revision controlled mechanical drawing
- Module-level optical, electrical, environmental, and EMC characterization

### **9.4 Source Notes and Inconsistencies** {.section-page}

- Current board images and pinout resources use different revision-number
  formats in their filenames and storage directories.
- Current pinout artwork calls the product `DevLab: I2C TEMT6000`; this
  reference identifies UNIT Electronics as the company that creates and
  develops the DevLab board ecosystem, with Atom as a product family within it.
- The current pinout shows an onboard controller and I2C/debug resources, but
  the only schematic in the repository is the earlier analog V0.0.1 circuit.
- Archived V0.0.1 dimensions, topology, and board views do not describe the
  longer V0.3.1 controller-based board.
- Qwiic positions A and B are marked optional; released assembly variants and
  controlled contact numbering are not supplied.
- Earlier examples treated the sensor as a digital threshold input. The sensor
  signal is analog; I2C operation is provided by the new onboard controller.
- Current firmware maps `PA2` to `ADC0`, `PA4` to read-only `GPIO0`, and `PB5`
  to the relay-compatible actuator block. Digital output commands `0x42/0x43`
  are not implemented; exposed `PA0`/`PA1` remain unassigned.

### **9.5 Current Firmware Limitations**

- The `WATCHDOG` capability is announced, but the current watchdog command does
  not operate an active hardware IWDG and must remain experimental.
- `GET_RESET_INFO` is not implemented and NRST behavior is incomplete.
- An internal ADC error can be returned as `0x0FFF`, indistinguishable from a
  legitimate full-scale sample.
- Current main-loop code does not call the available prolonged-BUSY recovery.
- There is no sample timestamp, sample counter, or calibrated lux result.
