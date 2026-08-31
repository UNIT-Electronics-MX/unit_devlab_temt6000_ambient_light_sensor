"""DevLab Device Protocol (DDP) 1.0 master for MicroPython I2C hosts.

Copy this file to ``/lib/devlab_ddp.py`` on the MicroPython device.  The
module uses the standard ``machine.I2C`` methods ``scan()``, ``writeto()`` and
``readfrom()`` and does not depend on a product-specific sensor library.
"""

try:
    from micropython import const
except ImportError:  # CPython validation and documentation builds
    def const(value):
        return value

import time


def _default_sleep_ms(milliseconds):
    sleep_ms = getattr(time, "sleep_ms", None)
    if sleep_ms is not None:
        sleep_ms(milliseconds)
    else:
        time.sleep(milliseconds / 1000.0)


DEVLAB_PROTOCOL_MAJOR = const(1)
DEVLAB_PROTOCOL_MINOR = const(0)

DDP_BLOCK_DEVICE_INFO = const(0x00)
DDP_BLOCK_CONFIGURATION = const(0x20)
DDP_BLOCK_DIGITAL_IO = const(0x40)
DDP_BLOCK_ANALOG = const(0x60)
DDP_BLOCK_SENSOR_DATA = const(0x80)
DDP_BLOCK_ACTUATORS = const(0xA0)
DDP_BLOCK_CALIBRATION = const(0xC0)
DDP_BLOCK_RESERVED = const(0xE0)
DDP_BLOCK_SYSTEM = const(0xF0)

DEVICE_JOYSTICK = const(0x0101)
DEVICE_TEMT6000 = const(0x0102)
DEVICE_DS18B20 = const(0x0103)
DEVICE_WS12XX_NEO = const(0x0400)

CMD_GET_DEVICE_ID = const(0x00)
CMD_GET_FIRMWARE_VERSION = const(0x01)
CMD_GET_HARDWARE_VERSION = const(0x02)
CMD_GET_CAPABILITIES = const(0x03)
CMD_GET_PROTOCOL = const(0x04)

CMD_GET_I2C_ADDR = const(0x20)
CMD_SET_I2C_ADDR = const(0x21)
CMD_SAVE_CONFIG = const(0x22)
CMD_RESET_FACTORY = const(0x23)
CMD_GET_I2C_STATUS = const(0x24)

CMD_READ_GPIO0 = const(0x40)
CMD_READ_GPIO1 = const(0x41)
CMD_WRITE_GPIO0 = const(0x42)
CMD_WRITE_GPIO1 = const(0x43)

CMD_READ_ADC0 = const(0x60)
CMD_READ_ADC1 = const(0x61)
CMD_SET_ADC_AVERAGING = const(0x62)
CMD_GET_ADC_AVERAGING = const(0x63)

CMD_TEMT6000_RAW = const(0x80)

CMD_RELAY_OFF = const(0xA0)
CMD_RELAY_ON = const(0xA1)
CMD_RELAY_TOGGLE = const(0xA2)
CMD_SET_TOGGLE_TIME = const(0xA3)
CMD_GET_TOGGLE_TIME = const(0xA4)

CMD_NEO_SET_PIXEL = const(0xB0)
CMD_NEO_FILL = const(0xB1)
CMD_NEO_CLEAR = const(0xB2)
CMD_NEO_SHOW = const(0xB3)
CMD_NEO_SET_HUE = const(0xB4)
CMD_NEO_BRIGHTNESS = const(0xB5)
CMD_NEO_CCT_MODE = const(0xB6)
CMD_NEO_GET_INTENSITY = const(0xB7)
CMD_NEO_RGB_COLOR = const(0xB8)

CMD_RESET = const(0xF0)
CMD_WATCHDOG_RESET = const(0xF1)
CMD_GET_RESET_INFO = const(0xF2)
CMD_DISABLE_NRST = const(0xF3)
CMD_CHECK_NRST = const(0xF4)

# Legacy wire values are exported for migration tools. New clients should use
# the DDP 1.0 commands above.
CMD_LEGACY_PB0_DIGITAL = const(0x06)
CMD_LEGACY_PA4_DIGITAL = const(0x07)
CMD_LEGACY_PA0_DIGITAL = const(0x09)
CMD_LEGACY_DISABLE_NRST = const(0x30)
CMD_LEGACY_CHECK_NRST = const(0x31)
CMD_LEGACY_INIT_PB0 = const(0x32)
CMD_LEGACY_GET_RESET_INFO = const(0x33)
CMD_LEGACY_SAVE_DATA = const(0x3A)
CMD_LEGACY_READ_DATA = const(0x3B)
RESPONSE_DATA = const(0x3C)
CMD_LEGACY_SET_I2C_ADDR = const(0x3D)
CMD_LEGACY_RESET_FACTORY = const(0x3E)
CMD_LEGACY_GET_I2C_STATUS = const(0x3F)
CMD_LEGACY_RELAY_TOGGLE = const(0xA6)
CMD_LEGACY_SET_TOGGLE_TIME = const(0xA7)
CMD_LEGACY_GET_TOGGLE_TIME = const(0xA8)
CMD_LEGACY_SET_ADC_AVERAGING = const(0xDC)
CMD_LEGACY_GET_ADC_AVERAGING = const(0xDD)
CMD_LEGACY_RESET = const(0xFE)
CMD_LEGACY_WATCHDOG_RESET = const(0xFF)

DDP_CAP_I2C_CONFIG = const(1 << 0)
DDP_CAP_DIGITAL_INPUT = const(1 << 1)
DDP_CAP_DIGITAL_OUTPUT = const(1 << 2)
DDP_CAP_ANALOG_INPUT = const(1 << 3)
DDP_CAP_SENSOR_DATA = const(1 << 4)
DDP_CAP_RELAY = const(1 << 5)
DDP_CAP_CALIBRATION = const(1 << 6)
DDP_CAP_WATCHDOG = const(1 << 7)
DDP_CAP_PERSISTENT_CONFIG = const(1 << 8)

DDP_STATUS_OK = const(0x00)
DDP_STATUS_UNKNOWN_CMD = const(0x01)
DDP_STATUS_INVALID_VALUE = const(0x02)
DDP_STATUS_BUSY = const(0x03)
DDP_STATUS_NOT_SUPPORTED = const(0x04)
DDP_STATUS_IO_ERROR = const(0x05)

# Legacy command-specific acknowledgement values.  These bytes are contextual;
# for example, 0x01 below means only the RELAY_ON acknowledgement.
RESP_RELAY_OFF = const(0x00)
RESP_RELAY_ON = const(0x01)
RESP_RELAY_TOGGLE = const(0x06)
RESP_TOGGLE_TIME_SET = const(0x07)
RESP_I2C_ERROR = const(0x08)
RESP_PA4_DIGITAL = const(0x09)
RESP_WATCHDOG_OK = const(0x0A)
RESP_CMD_UNKNOWN = const(0x0B)
RESP_ADC_AVERAGING_SET = const(0x0C)
RESP_I2C_ADDR_SET = const(0x0D)
RESP_FACTORY_RESET = const(0x0E)
RESP_I2C_FROM_FLASH = const(0x0F)
RESP_I2C_FROM_UID = const(0x0A)
RESP_NRST_DISABLED = const(0x10)
RESP_NRST_GPIO = const(0x11)
RESP_NRST_ACTIVE = const(0x12)
RESP_PB0_DIGITAL = const(0x13)
RESP_PB0_INITIALIZED = const(0x14)
RESP_RESET_OK = const(0x0F)

RESET_CAUSE_POWER_ON = const(0x00)
RESET_CAUSE_PIN = const(0x01)
RESET_CAUSE_SOFTWARE = const(0x02)
RESET_CAUSE_IWDG = const(0x03)
RESET_CAUSE_WWDG = const(0x04)
RESET_CAUSE_OBL = const(0x05)
RESET_CAUSE_UNKNOWN = const(0xFF)

VALID_I2C_ADDRESS_MIN = const(0x08)
VALID_I2C_ADDRESS_MAX = const(0x77)
VALID_ADC_AVERAGING = (1, 4, 8, 16, 24)

_DEVICE_NAMES = {
    DEVICE_JOYSTICK: "joystick",
    DEVICE_TEMT6000: "temt6000",
    DEVICE_DS18B20: "ds18b20",
    DEVICE_WS12XX_NEO: "ws12xx-neopixel",
}


class DDPError(Exception):
    """Base error for DDP transport, identity, or response failures."""


class DDPProtocolError(DDPError):
    """The device does not report a compatible DDP protocol major."""


class DDPIdentityError(DDPError):
    """The responding DDP device does not match the expected Device ID."""


class DDPResponseError(DDPError):
    """The response length, acknowledgement, or value is invalid."""


class DDPCollisionError(DDPError):
    """A requested new I2C address is already occupied."""


def uint16_le(data):
    if len(data) != 2:
        raise DDPResponseError("uint16 requires exactly 2 bytes")
    return data[0] | (data[1] << 8)


def uint32_le(data):
    if len(data) != 4:
        raise DDPResponseError("uint32 requires exactly 4 bytes")
    return data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24)


def ack_low_nibble_is(response, expected):
    return (response & 0x0F) == expected


def device_name(device_id):
    return _DEVICE_NAMES.get(device_id, "unknown")


class DeviceInfo:
    __slots__ = (
        "address",
        "device_id",
        "firmware",
        "hardware",
        "protocol",
        "capabilities",
        "valid",
    )

    def __init__(
        self,
        address,
        device_id,
        firmware,
        hardware,
        protocol,
        capabilities,
        valid=True,
    ):
        self.address = address
        self.device_id = device_id
        self.firmware = firmware
        self.hardware = hardware
        self.protocol = protocol
        self.capabilities = capabilities
        self.valid = valid

    def has_capability(self, capability):
        return (self.capabilities & capability) != 0

    def as_dict(self):
        return {
            "address": self.address,
            "device_id": self.device_id,
            "firmware": self.firmware,
            "hardware": self.hardware,
            "protocol": self.protocol,
            "capabilities": self.capabilities,
            "valid": self.valid,
        }


def format_device_info(info, expected_device_id=None):
    match = "unknown"
    if expected_device_id is not None:
        match = "yes" if info.device_id == expected_device_id else "NO"
    return (
        "addr=0x{:02X} id=0x{:04X} type={} protocol={}.{} "
        "firmware={}.{} hardware={}.{} caps=0x{:08X} match={}"
    ).format(
        info.address,
        info.device_id,
        device_name(info.device_id),
        info.protocol[0],
        info.protocol[1],
        info.firmware[0],
        info.firmware[1],
        info.hardware[0],
        info.hardware[1],
        info.capabilities,
        match,
    )


class Master:
    """Reusable DDP 1.0 master over a configured ``machine.I2C`` object."""

    def __init__(
        self,
        i2c,
        expected_device_id=None,
        processing_delay_ms=5,
        sleep_ms=None,
    ):
        self.i2c = i2c
        self.expected_device_id = expected_device_id
        self.processing_delay_ms = processing_delay_ms
        self._sleep_ms = sleep_ms or _default_sleep_ms

    @staticmethod
    def _validate_address(address):
        if not VALID_I2C_ADDRESS_MIN <= address <= VALID_I2C_ADDRESS_MAX:
            raise ValueError("I2C address must be in 0x08..0x77")

    @staticmethod
    def _validate_byte(value, name="value"):
        if not 0 <= value <= 0xFF:
            raise ValueError("{} must be in 0..255".format(name))

    def scan(self):
        return list(self.i2c.scan())

    def ping(self, address):
        self._validate_address(address)
        try:
            return address in self.i2c.scan()
        except OSError:
            return False

    def write_byte(self, address, value):
        self._validate_address(address)
        self._validate_byte(value)
        written = self.i2c.writeto(address, bytes((value,)), stop=True)
        if written is not None and written != 1:
            raise OSError("short I2C write")

    def read_response(self, address, length):
        self._validate_address(address)
        if length <= 0:
            raise ValueError("response length must be positive")
        response = self.i2c.readfrom(address, length, stop=True)
        if len(response) != length:
            raise DDPResponseError(
                "expected {} response bytes, received {}".format(
                    length, len(response)
                )
            )
        return response

    def read_command(self, address, command, length, processing_delay_ms=None):
        self.write_byte(address, command)
        delay_ms = self.processing_delay_ms
        if processing_delay_ms is not None:
            delay_ms = processing_delay_ms
        self._sleep_ms(delay_ms)
        return self.read_response(address, length)

    def identify(self, address):
        protocol_data = self.read_command(address, CMD_GET_PROTOCOL, 2)
        protocol = (protocol_data[0], protocol_data[1])
        if protocol[0] != DEVLAB_PROTOCOL_MAJOR:
            raise DDPProtocolError(
                "unsupported DDP protocol {}.{}".format(
                    protocol[0], protocol[1]
                )
            )

        device_id = uint16_le(self.read_command(address, CMD_GET_DEVICE_ID, 2))
        firmware_data = self.read_command(address, CMD_GET_FIRMWARE_VERSION, 2)
        hardware_data = self.read_command(address, CMD_GET_HARDWARE_VERSION, 2)
        capabilities = uint32_le(
            self.read_command(address, CMD_GET_CAPABILITIES, 4)
        )
        return DeviceInfo(
            address,
            device_id,
            (firmware_data[0], firmware_data[1]),
            (hardware_data[0], hardware_data[1]),
            protocol,
            capabilities,
        )

    def try_identify(self, address):
        try:
            return self.identify(address)
        except (OSError, DDPError):
            return None

    def matches_expected_device(self, address):
        info = self.try_identify(address)
        return (
            info is not None
            and self.expected_device_id is not None
            and info.device_id == self.expected_device_id
        )

    def require_expected_device(self, address):
        info = self.identify(address)
        if (
            self.expected_device_id is not None
            and info.device_id != self.expected_device_id
        ):
            raise DDPIdentityError(
                "expected Device ID 0x{:04X}, received 0x{:04X}".format(
                    self.expected_device_id, info.device_id
                )
            )
        return info

    def discover(self, preferred_address=None):
        addresses = self.scan()
        if preferred_address in addresses:
            addresses.remove(preferred_address)
            addresses.insert(0, preferred_address)
        for address in addresses:
            info = self.try_identify(address)
            if info is None:
                continue
            if (
                self.expected_device_id is None
                or info.device_id == self.expected_device_id
            ):
                return info
        return None

    def scan_ddp(self):
        devices = []
        for address in self.scan():
            info = self.try_identify(address)
            if info is not None:
                devices.append(info)
        return devices

    def get_i2c_address(self, address, verify=True):
        if verify:
            self.require_expected_device(address)
        reported = self.read_command(address, CMD_GET_I2C_ADDR, 1)[0]
        self._validate_address(reported)
        return reported

    def get_i2c_status(self, address, verify=True):
        if verify:
            self.require_expected_device(address)
        status = self.read_command(address, CMD_GET_I2C_STATUS, 1)[0]
        if status not in (0x00, 0x01):
            raise DDPResponseError(
                "invalid GET_I2C_STATUS response 0x{:02X}".format(status)
            )
        return status

    def staged_write_u8(
        self,
        address,
        command,
        value,
        expected_ack_low,
        value_delay_ms=25,
    ):
        self._validate_byte(value)
        initial = self.read_command(address, command, 1)[0]
        if not ack_low_nibble_is(initial, expected_ack_low):
            raise DDPResponseError(
                "command 0x{:02X} rejected with 0x{:02X}".format(
                    command, initial
                )
            )
        self.write_byte(address, value)
        self._sleep_ms(value_delay_ms)
        final = self.read_response(address, 1)[0]
        if not ack_low_nibble_is(final, expected_ack_low):
            raise DDPResponseError(
                "value for command 0x{:02X} rejected with 0x{:02X}".format(
                    command, final
                )
            )
        return final

    def set_i2c_address(self, old_address, new_address):
        self._validate_address(old_address)
        self._validate_address(new_address)
        if old_address == new_address:
            return self.require_expected_device(old_address)
        self.require_expected_device(old_address)
        if self.ping(new_address):
            raise DDPCollisionError(
                "I2C address 0x{:02X} is already occupied".format(new_address)
            )

        initial = self.read_command(old_address, CMD_SET_I2C_ADDR, 1, 10)[0]
        if not ack_low_nibble_is(initial, RESP_I2C_ADDR_SET):
            raise DDPResponseError("SET_I2C_ADDR was not accepted")
        self.write_byte(old_address, new_address)
        self._sleep_ms(100)
        final = self.read_response(old_address, 1)[0]
        if not ack_low_nibble_is(final, RESP_I2C_ADDR_SET):
            raise DDPResponseError("new I2C address was not saved")
        self._sleep_ms(300)
        return self.require_expected_device(new_address)

    def reset(self, address, verify=True):
        if verify:
            self.require_expected_device(address)
        self.write_byte(address, CMD_RESET)

    def read_adc(self, address, channel=0, verify=True, delay_ms=30):
        if channel not in (0, 1):
            raise ValueError("ADC channel must be 0 or 1")
        if verify:
            self.require_expected_device(address)
        command = CMD_READ_ADC0 if channel == 0 else CMD_READ_ADC1
        return uint16_le(self.read_command(address, command, 2, delay_ms))

    def read_sensor_u16(self, address, command, verify=True, delay_ms=5):
        if verify:
            self.require_expected_device(address)
        return uint16_le(self.read_command(address, command, 2, delay_ms))

    def read_gpio(self, address, channel=0, verify=True):
        if channel not in (0, 1):
            raise ValueError("GPIO channel must be 0 or 1")
        if verify:
            self.require_expected_device(address)
        command = CMD_READ_GPIO0 if channel == 0 else CMD_READ_GPIO1
        raw = self.read_command(address, command, 1)[0]
        if raw not in (0, 1):
            raise DDPResponseError("GPIO response must be 0 or 1")
        return raw == 1

    def get_adc_averaging(self, address, verify=True):
        if verify:
            self.require_expected_device(address)
        samples = self.read_command(address, CMD_GET_ADC_AVERAGING, 1)[0]
        if samples not in VALID_ADC_AVERAGING:
            raise DDPResponseError(
                "invalid ADC averaging value {}".format(samples)
            )
        return samples

    def set_adc_averaging(self, address, samples, verify=True):
        if samples not in VALID_ADC_AVERAGING:
            raise ValueError("ADC averaging must be 1, 4, 8, 16, or 24")
        if verify:
            self.require_expected_device(address)
        current = self.get_adc_averaging(address, verify=False)
        if current == samples:
            return current
        self.staged_write_u8(
            address,
            CMD_SET_ADC_AVERAGING,
            samples,
            RESP_ADC_AVERAGING_SET,
        )
        self._sleep_ms(samples * 20)
        return samples

    def actuator_command(self, address, command, expected_ack_low, verify=True):
        if verify:
            self.require_expected_device(address)
        response = self.read_command(address, command, 1)[0]
        if not ack_low_nibble_is(response, expected_ack_low):
            raise DDPResponseError(
                "actuator command 0x{:02X} returned 0x{:02X}".format(
                    command, response
                )
            )
        return response

    def relay_off(self, address, verify=True):
        return self.actuator_command(
            address, CMD_RELAY_OFF, RESP_RELAY_OFF, verify
        )

    def relay_on(self, address, verify=True):
        return self.actuator_command(
            address, CMD_RELAY_ON, RESP_RELAY_ON, verify
        )

    def relay_toggle(self, address, verify=True):
        return self.actuator_command(
            address, CMD_RELAY_TOGGLE, RESP_RELAY_TOGGLE, verify
        )

    def get_toggle_time(self, address, verify=True):
        if verify:
            self.require_expected_device(address)
        units = self.read_command(address, CMD_GET_TOGGLE_TIME, 1)[0]
        if not 1 <= units <= 40:
            raise DDPResponseError("toggle time must be in 1..40 units")
        return units

    def set_toggle_time(self, address, units, verify=True):
        if not 1 <= units <= 40:
            raise ValueError("toggle time must be in 1..40 units of 25 ms")
        if verify:
            self.require_expected_device(address)
        self.staged_write_u8(
            address,
            CMD_SET_TOGGLE_TIME,
            units,
            RESP_TOGGLE_TIME_SET,
        )
        return units
