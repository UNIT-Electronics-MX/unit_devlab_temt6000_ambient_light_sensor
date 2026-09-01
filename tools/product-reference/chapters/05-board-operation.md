## **5 Board Operation**

The repository supports safe electrical bring-up through I2C scanning, DDP
identity and measurement reads, and direct analog observation.

### **5.1 I2C Bring-up** {.section-page}

1. Inspect the board revision, connector population, and I2C bridge.
2. With power off, select a nominal 3.3 V or 5 V supply and connect `GND`,
   `VCC`, `SDA`, and `SCL` in the documented orientation. For 5 V operation,
   verify host tolerance at the bus pull-up voltage or add level translation.
3. Power from a current-limited source and check for unexpected heating.
4. Select an I2C clock from 100 kHz through 400 kHz; maintained examples use
   400 kHz. The ESP32 and MicroPython examples map host GPIO6 to SDA and GPIO7
   to SCL. Start at factory 7-bit address `0x20`, or scan if it was changed.
5. Record the active address, protocol, firmware, hardware, and capability
   values reported during discovery.
6. Verify protocol/firmware/hardware 1.0 and capabilities `0x000001B9`, then
   read either `READ_ADC0` (`0x60`) or equivalent `TEMT6000_RAW` (`0x80`).
7. Use a logic analyzer to capture start, address, acknowledge, STOP, and read
   timing
   if enumeration fails.

The maintained DDP clients are
[`software/examples/i2c/cpp_examples/ddp_temt6000/ddp_temt6000.ino`](software/examples/i2c/cpp_examples/ddp_temt6000/ddp_temt6000.ino)
and
[`software/examples/i2c/micropython/ddp_temt6000.py`](software/examples/i2c/micropython/ddp_temt6000.py).
The MicroPython example imports the reusable
[`software/examples/i2c/micropython/lib/devlab_ddp.py`](software/examples/i2c/micropython/lib/devlab_ddp.py)
module, which is installed as `/lib/devlab_ddp.py` on the host.
Low-level scanner sketches are
[`software/examples/i2c/cpp_examples/i2c_scanner/i2c_scanner.ino`](software/examples/i2c/cpp_examples/i2c_scanner/i2c_scanner.ino)
and
[`software/examples/i2c/micropython/i2c_scan.py`](software/examples/i2c/micropython/i2c_scan.py).

### **5.2 Application 1: Read Ambient-Light Data**

1. Initialize I2C at 100 kHz or 400 kHz using 7-bit address `0x20`.
2. Run the Chapter 3 discovery sequence and accept only DDP major 1 with
   Device ID `0x0102`.
3. Write `TEMT6000_RAW` (`0x80`), issue STOP, wait 5 ms, and read exactly two
   bytes.
4. Decode `raw = response[0] | (response[1] << 8)` and reject values above
   `4095`.
5. Repeat no faster than the approximately 20 ms background update interval
   when a new sample is required.

`READ_ADC0` (`0x60`) may replace `TEMT6000_RAW`; both access the same published
`PA2/ADC0` sample. The value is an uncalibrated ADC code, not lux. Convert to
lux only after calibration against a reference meter in the final optical and
mechanical installation.

### **5.3 Application 2: Change the I2C Address** {.section-page}

The common DDP block provides `GET_I2C_ADDR` (`0x20`), `SET_I2C_ADDR` (`0x21`),
`SAVE_CONFIG` (`0x22`), `RESET_FACTORY` (`0x23`), and `GET_I2C_STATUS` (`0x24`).
Factory address is `0x20`; a new value must be within `0x08..0x77`.

Address change is a staged operation. Send `0x21`, wait/read ACK low nibble
`0xD`, send the new one-byte value within 250 ms, wait about 100 ms, and read
the final ACK at the old address. The setter saves Flash and reset follows when
the final ACK is consumed. Wait about 300 ms and identify `0x0102` at the new
address. `SAVE_CONFIG` is currently idempotent. Factory restore returns ACK low
`0xE` but requires a separate reset before address `0x20` becomes active.

### **5.4 Application 3: Averaged Capture**

The controller updates ADC0 in the background about every 20 ms and publishes a
rounded circular-buffer mean. `GET_ADC_AVERAGING` (`0x63`) returns 1, 4, 8, 16,
or 24. `SET_ADC_AVERAGING` (`0x62`) is staged with ACK low nibble `0xC` and
persists to Flash. Read before writing, and wait `N × 20 ms` for a full window.
Recommended values are 8 for UI/general automation and 16 for stable ambient
measurement. Do not poll faster than 20 ms expecting a new value.

### **5.5 Application 4: Built-in Indicator**

Controller `PB5/BUILTIN` uses the relay-compatible commands: `RELAY_OFF`
(`0xA0`), `RELAY_ON` (`0xA1`), and non-blocking `RELAY_TOGGLE` (`0xA2`). It is
not a digital GPIO signal, and the digital-I/O commands are unsupported. Pulse
time is configured with `SET_TOGGLE_TIME` (`0xA3`) in `1..40` units of 25 ms.

### **5.6 Application 5: Direct Analog Bring-up** {.section-page}

1. Leave the I2C/service pins undriven and configure a host ADC as a
   high-impedance input.
2. Connect the direct `GND`, `VCC`, and `SIG` contacts with power removed.
3. Verify the actual `SIG` range using a multimeter before relying on the ADC;
   the controller ADC conversion range is `0..VCC`.
4. Compare covered and illuminated readings and check that the response is
   repeatable.
5. Calibrate against a reference meter for quantitative lux measurements.

The analog examples remain available under `software/examples/adc/`, separate
from the I2C clients. Their voltage calculations require
measurement because the only available schematic describes legacy
V0.0.1 hardware.

### **5.7 Service Operation: Modifying the I2C Bridge**

Do not cut the bridge as a first troubleshooting step. First verify power,
connector order, pull-ups, bus ownership, and scan timing. If analog-only
operation requires isolation, remove power, document the original bridge,
cut only the marked feature, inspect for debris, and confirm continuity before
repowering. Restoring the bridge requires controlled solder rework.

### **5.8 Troubleshooting Guide** {.page-break}

| Symptom | Checks |
|---|---|
| No address found | Supply/bus-logic compatibility, ground, connector orientation, populated connector, SDA/SCL continuity, intact I2C bridge |
| Bus held low | Cable reversal, duplicate pull-ups, unintended drive on shared `SDA/SWDIO` or `SCL/SWCLK`, solder bridge, unpowered device |
| Address found but rejected | Verify DDP major 1, Device ID `0x0102`, exact response lengths, and possible address collision |
| DDP identity succeeds but measurement fails | Check `ANALOG_INPUT`/`SENSOR_DATA`, 5 ms delay, exact length, byte order, and 12-bit range |
| Direct `SIG` always zero/full scale | Supply, ADC range, contact order, optical obstruction, current-board transfer function |
| Built-in LED unexpected | Use relay-compatible commands for `PB5`; digital-I/O commands are unsupported |
| Lux result inaccurate | Sensor spread, source spectrum, geometry, enclosure, temperature, ADC and calibration |
