from machine import I2C, Pin
import time

from devlab_ddp import (
    CMD_TEMT6000_RAW,
    DDP_CAP_ANALOG_INPUT,
    DDP_CAP_RELAY,
    DDPError,
    DEVICE_TEMT6000,
    Master,
    format_device_info,
)

# Copy examples/i2c/micropython/lib/devlab_ddp.py to /lib/devlab_ddp.py.
# The repository examples use GPIO6 for SDA and GPIO7 for SCL. These are host
# pins, not the module's internal controller pins.
I2C_BUS = 0
SDA_PIN = 6
SCL_PIN = 7
I2C_FREQUENCY = 400_000

FACTORY_I2C_ADDRESS = 0x20
CURRENT_CAPABILITIES = 0x000001BB
DDP_ADC_MAX = 4095

# Set to an integer in 0x08..0x77 to request a persistent address change.
REQUESTED_I2C_ADDRESS = None
# Set to 1, 4, 8, 16, or 24; None only reports the current value.
REQUESTED_ADC_AVERAGING = None
BUILTIN_BLINK_COUNT = 3

i2c = I2C(
    I2C_BUS,
    sda=Pin(SDA_PIN),
    scl=Pin(SCL_PIN),
    freq=I2C_FREQUENCY,
)
ddp = Master(i2c, expected_device_id=DEVICE_TEMT6000)


def read_raw(info):
    value = ddp.read_sensor_u16(
        info.address,
        CMD_TEMT6000_RAW,
        verify=False,
    )
    if value > DDP_ADC_MAX:
        raise ValueError("invalid 12-bit ADC payload: {}".format(value))
    return value


def configure_address(info):
    reported = ddp.get_i2c_address(info.address, verify=False)
    print("Active 7-bit address: 0x{:02X}".format(reported))

    new_address = REQUESTED_I2C_ADDRESS
    if new_address is None or new_address == info.address:
        return info

    updated = ddp.set_i2c_address(info.address, new_address)
    print("Persistent address changed and identity verified")
    return updated


def configure_averaging(info):
    if REQUESTED_ADC_AVERAGING is None:
        return ddp.get_adc_averaging(info.address, verify=False)
    return ddp.set_adc_averaging(
        info.address,
        REQUESTED_ADC_AVERAGING,
        verify=False,
    )


def blink_builtin(info):
    if not info.has_capability(DDP_CAP_RELAY):
        print("BUILTIN blink skipped: RELAY is not announced")
        return
    for _ in range(BUILTIN_BLINK_COUNT):
        ddp.relay_on(info.address, verify=False)
        time.sleep_ms(150)
        ddp.relay_off(info.address, verify=False)
        time.sleep_ms(150)
    print("BUILTIN blink complete (relay-compatible PB5 commands)")


print("UNIT ATOM TEMT6000 — MicroPython DDP v1.0")
device = ddp.discover(preferred_address=FACTORY_I2C_ADDRESS)
averaging_samples = 1

if device is None:
    print("No compatible TEMT6000 DDP device found")
else:
    print(format_device_info(device, DEVICE_TEMT6000))
    if not device.has_capability(DDP_CAP_ANALOG_INPUT):
        raise DDPError("device does not announce ANALOG_INPUT")
    if device.capabilities != CURRENT_CAPABILITIES:
        print("Notice: capabilities differ from firmware 1.0 profile")
    device = configure_address(device)
    averaging_samples = configure_averaging(device)
    print("Device ADC averaging: {} sample(s)".format(averaging_samples))
    blink_builtin(device)

while True:
    if device is None:
        device = ddp.discover(preferred_address=FACTORY_I2C_ADDRESS)
        if device is None:
            time.sleep(2)
            continue
        averaging_samples = ddp.get_adc_averaging(
            device.address,
            verify=False,
        )

    try:
        print(
            "ADC0/TEMT6000 raw (device average {}): {} / 4095".format(
                averaging_samples,
                read_raw(device),
            )
        )
    except (OSError, DDPError, ValueError) as error:
        print("DDP read failed:", error)
        device = None

    time.sleep_ms(100)
