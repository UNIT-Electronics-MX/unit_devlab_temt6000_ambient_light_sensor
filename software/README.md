# Using the UNIT ATOM TEMT6000

UNIT Electronics creates and develops the DevLab board ecosystem, and this
product belongs to its Atom family. Hardware V0.3.1 provides two development
paths: Qwiic I2C through its onboard PY32F003 controller and direct analog observation
through `SIG`.

## I2C bring-up

Use a current-limited 3.3 V or 5 V supply and connect `GND`, `VCC`, `SDA`, and
`SCL` in the released pinout orientation. At 5 V, the host must tolerate the
actual I2C pull-up voltage or use a level shifter. Use 7-bit addressing and an I2C clock
from 100 kHz through 400 kHz. The repository includes low-level bus scanners:

The normal function of `PA10`/`PB6` is `SDA`/`SCL`. Their factory-only
`SWDIO`/`SWCLK` functions use the same physical pins, not a separate port, and
must never be driven while the I2C bus is active.

- [`examples/i2c/cpp_examples/i2c_scanner/i2c_scanner.ino`](examples/i2c/cpp_examples/i2c_scanner/i2c_scanner.ino)
  for C++ with the Arduino framework;
- [`examples/i2c/micropython/i2c_scan.py`](examples/i2c/micropython/i2c_scan.py) for
  MicroPython.

It also includes DDP measurement clients:

- [`examples/i2c/cpp_examples/ddp_temt6000/ddp_temt6000.ino`](examples/i2c/cpp_examples/ddp_temt6000/ddp_temt6000.ino)
  for C++ with the Arduino framework, using the canonical
  [`DevLabDDP`](https://github.com/UNIT-Electronics-Labs/unit_devlab_ddp_library)
  library;
- [`examples/i2c/micropython/ddp_temt6000.py`](examples/i2c/micropython/ddp_temt6000.py)
  for MicroPython, using the reusable
  [`devlab_ddp.py`](examples/i2c/micropython/lib/devlab_ddp.py) module.

The example tree is separated by interface (`i2c` or `adc`) and then by
language. See [`examples/README.md`](examples/README.md) for the selected
end-user examples and dependencies.

Both clients start with factory address `0x20`, can scan valid 7-bit addresses,
execute the mandatory DDP discovery sequence, accept only Device ID `0x0102`,
inspect capabilities at runtime, and then read the TEMT6000 sample. The command
is `TEMT6000_RAW` (`0x80`),
which returns a 12-bit ADC code (`0` to `4095`) in an unsigned 16-bit
little-endian response. The same published `PA2` sample is available through
common `READ_ADC0` (`0x60`).

The controller publishes an internally averaged ADC value approximately every 20 ms.
The persistent averaging window accepts 1, 4, 8, 16, or 24 samples; clients
read the current value before writing it. DDP address commands `0x20..0x24`
report, change, restore, and describe the active 7-bit address. Address and
averaging mutation are disabled by default in the examples.

`PB5/BUILTIN` uses `RELAY_OFF/ON/TOGGLE` (`0xA0..0xA2`), not the unsupported
digital-output commands. See [`protocol/README.md`](protocol/README.md) for the
exact controller command profile, staged acknowledgements, timing, and limitations.

For MicroPython installation and API details, see
[`examples/i2c/micropython/README.md`](examples/i2c/micropython/README.md). Copy
`devlab_ddp.py` to the host's `/lib` directory before running the DDP example.
The repository's ESP32 and MicroPython I2C examples use GPIO6 for SDA and GPIO7
for SCL.

## Direct analog bring-up

Connect the direct contacts while unpowered:

| Module | Host | Note |
|---|---|---|
| `GND` | Ground | Common reference |
| `VCC` | Module supply | 3.3 V or 5 V nominal; controller upper operating limit is 5.5 V |
| `SIG` | High-impedance ADC input | Signal is referenced to `VCC`; verify range before connecting a lower-voltage ADC |

- [`examples/adc/cpp_examples/light_sensor/light_sensor.ino`](examples/adc/cpp_examples/light_sensor/light_sensor.ino)
  reports averaged
  ADC code and voltage.
- [`examples/adc/micropython/light_sensor.py`](examples/adc/micropython/light_sensor.py)
  adds averaging and voltage conversion.

Set the ADC pin, resolution, and full-scale voltage for the host. The examples
do not convert to lux because the only schematic in the repository applies to
legacy V0.0.1 hardware; the V0.3.1 analog transfer needs release and validation.

## I2C disable bridge

Do not cut the bridge as a first troubleshooting step. Verify power, connector
orientation, SDA/SCL continuity, pull-ups, and bus ownership first. If the
current assembly must be isolated for analog-only testing, remove power and
document/inspect the rework carefully.

## Troubleshooting

| Symptom | Check |
|---|---|
| No I2C address | Supply and bus-logic compatibility, ground, connector population/orientation, SDA/SCL, intact bridge |
| Bus held low | Cable reversal, unpowered device, pull-ups, or unintended external drive on shared service lines |
| Address found but rejected | Confirm DDP protocol major 1 and Device ID `0x0102`; check for another device at that address |
| DDP device found but read fails | Confirm `ANALOG_INPUT`/`SENSOR_DATA`, 5 ms processing delay, exact response length, and command/STOP/read sequence |
| Analog always zero/full scale | ADC pin/range, supply, optical path, current-board transfer |
| Noisy analog value | Cable length, averaging, acquisition time, reference and supply noise |
