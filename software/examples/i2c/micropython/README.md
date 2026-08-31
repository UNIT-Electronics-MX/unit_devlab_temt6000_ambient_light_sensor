# DevLab DDP for MicroPython

[`lib/devlab_ddp.py`](lib/devlab_ddp.py) is a reusable MicroPython master for DevLab
Device Protocol 1.0 over I2C. It mirrors the canonical Arduino transport rules:

- one command byte followed by STOP;
- a configurable processing delay before the response read;
- exact response lengths;
- little-endian decoding for Device ID, capabilities, and ADC data;
- mandatory protocol-major validation;
- Device ID discovery and matching;
- staged one-byte setters with packed acknowledgement validation; and
- collision-safe persistent I2C address changes.

## Install on a MicroPython board

Create `/lib` if it does not exist, then copy the module and example with
`mpremote`:

```bash
mpremote fs mkdir :/lib
mpremote fs cp software/examples/i2c/micropython/lib/devlab_ddp.py :/lib/devlab_ddp.py
mpremote fs cp software/examples/i2c/micropython/ddp_temt6000.py :/ddp_temt6000.py
```

The included I2C examples default to host GPIO6 for SDA and GPIO7 for SCL.
Edit `I2C_BUS`, `SDA_PIN`, and `SCL_PIN` only when the host board requires a
different mapping, then run:

```bash
mpremote run software/examples/i2c/micropython/ddp_temt6000.py
```

The module uses only the standard `machine.I2C` API. The host port must provide
`scan()`, `writeto()`, and `readfrom()` with STOP support.

## Minimal use

```python
from machine import I2C, Pin
from devlab_ddp import DEVICE_TEMT6000, Master, format_device_info

i2c = I2C(0, sda=Pin(6), scl=Pin(7), freq=400_000)
ddp = Master(i2c, expected_device_id=DEVICE_TEMT6000)
info = ddp.discover(preferred_address=0x20)

if info is None:
    raise OSError("TEMT6000 DDP device not found")

print(format_device_info(info, DEVICE_TEMT6000))
print(ddp.read_adc(info.address, channel=0, verify=False))
```

After discovery, `verify=False` avoids repeating the five identity reads before
every sample. Repeat discovery after reset, address change, or bus recovery.

## Main API

| Method | Purpose |
|---|---|
| `identify(address)` | Read protocol, Device ID, versions, and capabilities |
| `discover(preferred_address=None)` | Find the expected DDP device on the bus |
| `scan_ddp()` | Return every valid DDP device found |
| `read_command(address, command, length)` | Execute the DDP command/STOP/read transaction |
| `read_adc(address, channel)` | Read generic ADC0 or ADC1 |
| `read_gpio(address, channel)` | Read logical GPIO0 or GPIO1 |
| `get_adc_averaging(address)` | Read the persistent averaging window |
| `set_adc_averaging(address, samples)` | Apply a validated staged averaging write |
| `get_i2c_address(address)` | Read the active 7-bit address |
| `set_i2c_address(old, new)` | Check collision, persist the address, and rediscover |
| `relay_off/on/toggle(address)` | Execute the relay-compatible actuator commands |
| `set_toggle_time(address, units)` | Set `1..40` units of 25 ms |

Protocol constants, capability bits, Device IDs, response codes, exception
types, little-endian helpers, and `DeviceInfo` are exported by the module.

## Host-side tests

The tests use a scripted fake I2C bus and do not require hardware:

```bash
python3 -m unittest software/tests/test_devlab_ddp.py
```
