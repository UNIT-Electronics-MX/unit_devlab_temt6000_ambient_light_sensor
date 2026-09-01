# UNIT ATOM TEMT6000 — controller DDP device profile

UNIT Electronics creates and develops the DevLab board ecosystem; this product
belongs to its Atom family. Hardware V0.3.1 communicates through **DevLab
Device Protocol (DDP) v1.0** over I2C. This profile describes the observable
behavior of the current controller firmware. Common command values come from the canonical
[`unit_devlab_ddp_library`](https://github.com/UNIT-Electronics-Labs/unit_devlab_ddp_library).

Repository implementations are the Arduino `DevLabDDP` client and the reusable
MicroPython [`devlab_ddp.py`](../examples/i2c/micropython/lib/devlab_ddp.py) module. Both use the
same command/STOP/read transaction model and identity sequence.

## Released runtime profile

| Field | Current value |
|---|---|
| DDP Device ID | `0x0102` (little-endian bytes `[0x02, 0x01]`) |
| Protocol version | 1.0 (major/minor bytes `[0x01, 0x00]`) |
| Firmware version | 1.0 (major/minor bytes `[0x01, 0x00]`) |
| Hardware version | 1.0 (major/minor bytes `[0x01, 0x00]`) |
| Capabilities | `0x000001B9` (little-endian bytes `[0xB9, 0x01, 0x00, 0x00]`) |
| Factory 7-bit address | `0x20` |
| Configurable address range | `0x08..0x77` |
| I2C clock | 100 kHz to 400 kHz; examples use 400 kHz |
| Controller | PY32F003, 32-bit Arm Cortex-M0+; 16 KB Flash, 2 KB SRAM; internal HSI at up to 24 MHz for this application; no external HSE oscillator |
| Published controller supply range | 2.0–5.5 V, using the conservative x7 voltage limit; fitted suffix not asserted |
| Controller bus pins | `PB6/SCL`, `PA10/SDA` |
| Command/parameter size | One byte per write transaction |
| Maximum prepared response | Four bytes |
| Processing delay before read | 2–5 ms; use 5 ms conservatively |
| Pending setter timeout | 250 ms |
| ADC format | 12-bit unsigned, `0..4095`, little-endian `uint16` |

The capability bitmap announces `I2C_CONFIG`, `ANALOG_INPUT`, `SENSOR_DATA`,
`RELAY`, `WATCHDOG`, and `PERSISTENT_CONFIG`. It does not announce digital I/O;
commands `READ_GPIO0/1` (`0x40/0x41`) and `WRITE_GPIO0/1` (`0x42/0x43`) are not
implemented.

### Meaning of byte `0x01`

`0x01` has no universal meaning in DDP; its meaning comes from the command,
response length, and field encoding. In this profile:

- as a command byte, `0x01` selects `GET_FIRMWARE_VERSION`;
- in version bytes `[0x01, 0x00]`, it is major version 1;
- in Device ID bytes `[0x02, 0x01]`, it is the high byte of little-endian
  `0x0102`;
- in capability bytes `[0xB9, 0x01, 0x00, 0x00]`, it is byte 1 of the
  little-endian bitmap `0x000001B9`;
- as the low nibble of a `RELAY_ON` acknowledgement, `0x1` means that driving
  `PB5/BUILTIN` HIGH was accepted; and
- as the `GET_I2C_STATUS` response, `0x01` means the active address was loaded
  from Flash.

Never interpret an isolated `0x01` without first identifying its command and
expected response format.

## Logical and physical mapping

| Logical resource | Physical resource | Implemented command |
|---|---|---|
| `ADC0` | TEMT6000 sampled on controller `PA2` | `READ_ADC0` (`0x60`) |
| TEMT6000 sensor data | Same published ADC sample | `TEMT6000_RAW` (`0x80`) |
| Relay-compatible actuator | Controller `PB5` / `BUILTIN` | `RELAY_OFF/ON/TOGGLE` (`0xA0..0xA2`) |
| `PA0`, `PA1` | Exposed reserved pads | No current application assignment |

`READ_ADC0` and `TEMT6000_RAW` return the same most recently published
sample. An I2C read does not start an ADC conversion. The historical `RELAY_*`
names control `PB5` and therefore the `BUILTIN` indicator on this product.

## I2C transaction model

This is a command protocol, not a memory-mapped register interface. A normal
read requires a STOP between command and response:

```text
host -> [SLA+W, command] -> STOP
wait 2..5 ms
host -> [SLA+R, exact documented response length] -> NACK + STOP
```

Do not send a command and its parameter in one write. Setters use two explicit
stages and packed compatibility acknowledgements:

```text
host -> [SLA+W, command] -> STOP
wait, then read one-byte initial ACK
host -> [SLA+W, value] -> STOP       (within 250 ms)
wait, then read one-byte final ACK
```

Validate the documented low nibble of each staged-operation acknowledgement;
never mask ADC data, addresses, versions, or averaging values. If a read is too
early or too long, transport padding can be `0xFF`, so clients must validate
length, identity, and value range.

## Mandatory discovery

| Order | Command | Value | Exact current response |
|---:|---|---:|---|
| 1 | `GET_PROTOCOL` | `0x04` | `[0x01, 0x00]` = major 1, minor 0 |
| 2 | `GET_DEVICE_ID` | `0x00` | `[0x02, 0x01]` = little-endian `0x0102` |
| 3 | `GET_FIRMWARE_VERSION` | `0x01` | `[0x01, 0x00]` = major 1, minor 0 |
| 4 | `GET_HARDWARE_VERSION` | `0x02` | `[0x01, 0x00]` = major 1, minor 0 |
| 5 | `GET_CAPABILITIES` | `0x03` | `[0xB9, 0x01, 0x00, 0x00]` = little-endian `0x000001B9` |

Cache identity after `begin()` rather than repeating all five reads before
every sample. Repeat discovery after reset, address change, or bus recovery.

## Implemented application commands

| Command | Code | Response/effect |
|---|---:|---|
| `READ_ADC0` | `0x60` | ADC `[LSB, MSB]` |
| `SET_ADC_AVERAGING` | `0x62` | Staged write; ACK low nibble `0xC` |
| `GET_ADC_AVERAGING` | `0x63` | `1`, `4`, `8`, `16`, or `24` |
| `TEMT6000_RAW` | `0x80` | Same ADC `[LSB, MSB]` as `0x60` |
| `RELAY_OFF` | `0xA0` | ACK low `0x0`; drives `PB5` low |
| `RELAY_ON` | `0xA1` | ACK low nibble `0x1` = `PB5` HIGH accepted |
| `RELAY_TOGGLE` | `0xA2` | ACK low `0x6`; non-blocking pulse |
| `SET_TOGGLE_TIME` | `0xA3` | Staged write `1..40`; ACK low `0x7` |
| `GET_TOGGLE_TIME` | `0xA4` | `1..40`, in units of 25 ms |

`READ_GPIO0/1`, `WRITE_GPIO0/1`, and `READ_ADC1` are not implemented and
return the packed unknown-command code with low nibble `0xB`.

## ADC acquisition and averaging

The controller updates its ADC sample in the background approximately every 20 ms
(about 50 samples/s). For each update it discards one conversion to settle the
sample-and-hold, takes one 12-bit conversion, updates a circular buffer, and
publishes `round(sum / valid_samples)`.

| Samples | Window | Fill time after change | Typical use |
|---:|---:|---:|---|
| 1 | 20 ms | 20 ms | Fast response |
| 4 | 80 ms | 80 ms | Low-latency control |
| 8 | 160 ms | 160 ms | UI and general automation |
| 16 | 320 ms | 320 ms | Stable ambient measurement |
| 24 | 480 ms | 480 ms | Maximum stability |

The factory averaging value is 1. `SET_ADC_AVERAGING` persists the selected
value in Flash, so read `GET_ADC_AVERAGING` first and write only when it needs
to change. Wait `N × 20 ms` for a fully refilled window. Do not poll faster than
20 ms expecting a new sample, and do not describe the raw average as lux.

## Address management

| Command | Code | Current behavior |
|---|---:|---|
| `GET_I2C_ADDR` | `0x20` | Active 7-bit address |
| `SET_I2C_ADDR` | `0x21` | Staged value `0x08..0x77`; ACK low `0xD`; saves Flash and resets automatically |
| `SAVE_CONFIG` | `0x22` | Returns `00`; idempotent because setters already persist |
| `RESET_FACTORY` | `0x23` | ACK low `0xE`; reset still required |
| `GET_I2C_STATUS` | `0x24` | `0x00` = factory/default; `0x01` = address loaded from Flash |

Before an address change, verify that the target is free. Read the initial ACK,
write the new value within 250 ms, wait about 100 ms for Flash, read the final
ACK at the old address, wait about 300 ms for reset, then verify protocol 1.x
and Device ID `0x0102` at the new address. If the final ACK is lost, probe the
new address once and then the old address rather than rewriting indefinitely.

Factory restoration keeps the old address active until reset:

```text
old: RESET_FACTORY (0x23) -> ACK low 0xE
old: RESET (0xF0) -> do not request a response
wait 300 ms
identify factory address 0x20
```

## Built-in indicator

`PB5/BUILTIN` uses the relay-compatible actuator block, not digital GPIO
output commands. A client can blink using `RELAY_ON`/`RELAY_OFF` with host
timing, or request a non-blocking pulse with `RELAY_TOGGLE`. Toggle time accepts
`1..40` units of 25 ms (25–1000 ms) and is persistent.

## Current firmware limitations

- `WATCHDOG` is announced, but `WATCHDOG_RESET` does not use an active hardware
  IWDG and must remain experimental/disabled by default.
- `GET_RESET_INFO` is not implemented; NRST support is incomplete.
- The internal error sentinel can appear as `0x0FFF`, indistinguishable from a
  legitimate full-scale ADC sample.
- Bus-BUSY recovery exists in firmware but is not called by the current main
  loop.
- There is no timestamp, sample counter, or calibrated lux output.
- The V0.3.1 schematic and complete module electrical limits remain pending.
