## **9 Appendix**

### **9.1 Current V2.0.0 Schematic** {.section-page}

The current schematic is documented in
`hardware/unit_sch_v_2_0_0_ue0098_temt6000.pdf`. It documents the
controller-based V0.3.1 board, including the reference controller, TEMT6000
analog stage, I2C interfaces, status indicators, test points, and optional
connectors.

![](../../../hardware/resources/unit_schematic_v_2_0_0_ue0098_temt6000.png){width=7.0in}

**Figure 9.1 — Current V2.0.0 electrical schematic.**

The sensor signal uses a 10 kΩ resistor (`R1`) to ground and is routed to the
controller ADC input and the external `VCC`/`GND`/`SIG` header. As a
first-order estimate outside saturation, `VSIGNAL ≈ IPCE × 10 kΩ`; this is
not a calibrated or guaranteed conversion to lux.

The I2C `SDA` and `SCL` signals are available at three physical connection
positions: one connector populated by default and two optional horizontal
positions. These signals are shared with the controller's factory programming
and debugging interface; there is no separate user-accessible SWD connector.

### **9.2 Document Control** {.section-page}

| Field | Value |
|---|---|
| Product | UNIT ATOM TEMT6000 Ambient Light Sensor |
| Product hierarchy | UNIT Electronics → DevLab board ecosystem → Atom family |
| Manufacturer Part Number (MPN) | UE0098 |
| Current board artwork | V0.3.1 |
| Current pinout, topology, and dimensions | V3.1.0 |
| Available schematic | Current V2.0.0 |
| Product Reference | Version 1.1.0 |
| Publication date | 2026-08-31 |
| Interfaces | Three I2C connection positions on one bus; `VCC`/`GND`/`SIG` header; reserved expansion pads; shared factory programming/debug signals |

### **9.3 Required Technical Releases**

- V0.3.1 bill of materials
- Exact controller package/ordering suffix and controlled manufacturer programming release
- Exact oscillator/timing tolerances and uniform future DDP status behavior
- Complete-module supply/logic absolute-maximum ratings and current consumption
- Pull-up values and bus-loading limits
- Direct `SIG` transfer, loading, range, and ADC guidance
- Mechanical tolerances, board thickness, component heights, and finished mass
- Module-level optical, electrical, environmental, and EMC characterization
