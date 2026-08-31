# UNIT ATOM TEMT6000 examples

Choose the interface first. The `i2c/` examples use the module's DDP firmware;
the `adc/` examples read the separate direct `SIG` contact. They are kept in
different trees so wiring and host-pin assumptions are not mixed.

## Layout

```text
examples/
├── i2c/
│   ├── cpp_examples/
│   │   ├── ddp_temt6000/       normal DDP measurement client
│   │   └── i2c_scanner/        bus troubleshooting only
│   └── micropython/
│       ├── lib/devlab_ddp.py   reusable library; copy to the board's /lib
│       ├── ddp_temt6000.py     normal DDP measurement client
│       └── i2c_scan.py         bus troubleshooting only
└── adc/
    ├── cpp_examples/
    │   └── light_sensor/       direct SIG reading
    └── micropython/
        └── light_sensor.py     averaged direct SIG reading
```

## I2C — recommended interface

Start with `ddp_temt6000` for normal operation. Use `i2c_scanner` or
`i2c_scan.py` only when the module is not discovered.

| Language | Normal example | Diagnostic example |
|---|---|---|
| C++/Arduino framework | [`i2c/cpp_examples/ddp_temt6000`](i2c/cpp_examples/ddp_temt6000/ddp_temt6000.ino) | [`i2c/cpp_examples/i2c_scanner`](i2c/cpp_examples/i2c_scanner/i2c_scanner.ino) |
| MicroPython | [`i2c/micropython/ddp_temt6000.py`](i2c/micropython/ddp_temt6000.py) | [`i2c/micropython/i2c_scan.py`](i2c/micropython/i2c_scan.py) |

The ESP32 and MicroPython I2C examples use host GPIO6 for SDA and GPIO7 for
SCL. Generic Arduino targets fall back to the board's default `Wire` pins.
These are host pins, not the module's internal controller pins.

The C++ client requires the canonical
[`DevLabDDP`](https://github.com/UNIT-Electronics-Labs/unit_devlab_ddp_library)
library. For MicroPython, install
[`i2c/micropython/lib/devlab_ddp.py`](i2c/micropython/lib/devlab_ddp.py) in the
device's `/lib` directory; see the
[`i2c/micropython` guide](i2c/micropython/README.md).

## ADC — direct SIG only

Use this path only when the host is wired to the direct `SIG` contact instead
of using the DDP measurement client.

| Language | Example |
|---|---|
| C++/Arduino framework | [`adc/cpp_examples/light_sensor`](adc/cpp_examples/light_sensor/light_sensor.ino) |
| MicroPython | [`adc/micropython/light_sensor.py`](adc/micropython/light_sensor.py) |

Set the ADC-capable host pin and full-scale voltage for the selected board.
The examples report ADC code and voltage, not lux, because the V0.3.1 analog
transfer function still requires release and validation.

## Electrical note

The module supports nominal 3.3 V or 5 V operation. At 5 V, the host must
tolerate the actual I2C pull-up level or use a bidirectional level shifter.
`SDA/SCL` share their physical controller pins with the factory-only
`SWDIO/SWCLK` functions; user examples use I2C only.

See [`../protocol/README.md`](../protocol/README.md) for command timing,
response formats, capabilities, and address-change behavior.
