## **9 Appendix**

### **9.1 Current V2.0.0 Schematic** {.section-page}

The current schematic is documented in
`hardware/unit_sch_v_2_0_0_ue0098_temt6000.pdf`. It documents the
controller-based V0.3.1 board, including the PY32F003L24D6TR, TEMT6000 analog
stage, I2C interfaces, status LEDs, test points, and optional connectors.

![](hardware/resources/unit_schematic_v_2_0_0_ue0098_temt6000.png){width=7.0in}

**Figure 9.1 — Current V2.0.0 electrical schematic.**

The sensor signal uses a 10 kΩ resistor (`R1`) to ground and is routed to
controller `PA2`/ADC0 and the RAW Signal Header. The I2C bus uses
`PA10/SDA` and `PB6/SCL`, with the same physical lines reserved for factory
SWD aliases.

### **9.2 Document Control** {.section-page}

| Field | Value |
|---|---|
| Product | UNIT ATOM TEMT6000 Ambient Light Sensor |
| Product hierarchy | UNIT Electronics → DevLab board ecosystem → Atom family |
| Manufacturer Part Number (MPN) | UE0098 |
| Current board artwork | V0.3.1 |
| Current pinout | V3.1.0 |
| Available schematic | Current V2.0.0 |
| Product Reference | Version 1.1.0 |
| Publication date | 2026-08-31 |
| Interfaces | Qwiic I2C with shared factory SWD, analog, and auxiliary pads |

### **9.3 Required Technical Releases**

- V0.3.1 bill of materials
- Exact controller package/ordering suffix, released firmware image, and update procedure
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
- The V2.0.0 schematic now documents the onboard controller and I2C/debug
  resources shown by the current pinout.
- Archived V0.0.1 dimensions, topology, and board views do not describe the
  longer V0.3.1 controller-based board.
- Qwiic positions A and B are marked optional; released assembly variants and
  controlled contact numbering are not supplied.
- Earlier examples treated the sensor as a digital threshold input. The sensor
  signal is analog; I2C operation is provided by the new onboard controller.
- Current firmware maps `PA2` to `ADC0` and `PB5` to the relay-compatible
  actuator block. Digital-I/O commands `0x40..0x43` are not implemented;
  exposed `PA0`/`PA1` remain unassigned.

### **9.5 Current Firmware Limitations**

- The `WATCHDOG` capability is announced, but the current watchdog command does
  not operate an active hardware IWDG and must remain experimental.
- `GET_RESET_INFO` is not implemented and NRST behavior is incomplete.
- An internal ADC error can be returned as `0x0FFF`, indistinguishable from a
  legitimate full-scale sample.
- Current main-loop code does not call the available prolonged-BUSY recovery.
- There is no sample timestamp, sample counter, or calibrated lux result.
