import pathlib
import sys
import unittest


MICROPYTHON_LIBRARY = (
    pathlib.Path(__file__).resolve().parents[1]
    / "examples"
    / "i2c"
    / "micropython"
    / "lib"
)
sys.path.insert(0, str(MICROPYTHON_LIBRARY))

import devlab_ddp as ddp


def command_steps(address, command, response):
    return [
        ("write", address, bytes((command,))),
        ("read", address, len(response), bytes(response)),
    ]


def identity_steps(address, device_id=ddp.DEVICE_TEMT6000, protocol=(1, 0)):
    return (
        command_steps(address, ddp.CMD_GET_PROTOCOL, protocol)
        + command_steps(
            address,
            ddp.CMD_GET_DEVICE_ID,
            (device_id & 0xFF, (device_id >> 8) & 0xFF),
        )
        + command_steps(address, ddp.CMD_GET_FIRMWARE_VERSION, (1, 2))
        + command_steps(address, ddp.CMD_GET_HARDWARE_VERSION, (3, 4))
        + command_steps(address, ddp.CMD_GET_CAPABILITIES, (0xB9, 0x01, 0, 0))
    )


class ScriptedI2C:
    def __init__(self, steps=(), scans=()):
        self.steps = list(steps)
        self.scans = list(scans)

    def scan(self):
        if not self.scans:
            return []
        if len(self.scans) == 1:
            return list(self.scans[0])
        return list(self.scans.pop(0))

    def writeto(self, address, data, stop=True):
        self.assert_step("write", address, bytes(data))
        self.assertTrueStop(stop)
        return len(data)

    def readfrom(self, address, length, stop=True):
        if not self.steps:
            raise AssertionError("unexpected read")
        kind, expected_address, expected_length, response = self.steps.pop(0)
        if kind != "read":
            raise AssertionError("expected {}, received read".format(kind))
        if address != expected_address or length != expected_length:
            raise AssertionError(
                "read expected address 0x{:02X}/length {}, got 0x{:02X}/{}".format(
                    expected_address, expected_length, address, length
                )
            )
        self.assertTrueStop(stop)
        return response

    def assert_step(self, kind, address, value):
        if not self.steps:
            raise AssertionError("unexpected {}".format(kind))
        expected_kind, expected_address, expected_value = self.steps.pop(0)
        if (kind, address, value) != (
            expected_kind,
            expected_address,
            expected_value,
        ):
            raise AssertionError(
                "expected {!r}, got {!r}".format(
                    (expected_kind, expected_address, expected_value),
                    (kind, address, value),
                )
            )

    @staticmethod
    def assertTrueStop(stop):
        if stop is not True:
            raise AssertionError("DDP transactions must issue STOP")

    def assert_done(self):
        if self.steps:
            raise AssertionError("unconsumed I2C steps: {!r}".format(self.steps))


class DevLabDDPTests(unittest.TestCase):
    def make_master(self, bus, delays=None):
        delay_log = delays if delays is not None else []
        return ddp.Master(
            bus,
            expected_device_id=ddp.DEVICE_TEMT6000,
            sleep_ms=delay_log.append,
        )

    def test_identify_decodes_little_endian_metadata(self):
        bus = ScriptedI2C(identity_steps(0x20))
        master = self.make_master(bus)

        info = master.identify(0x20)

        self.assertEqual(info.address, 0x20)
        self.assertEqual(info.device_id, 0x0102)
        self.assertEqual(info.protocol, (1, 0))
        self.assertEqual(info.firmware, (1, 2))
        self.assertEqual(info.hardware, (3, 4))
        self.assertEqual(info.capabilities, 0x000001B9)
        self.assertTrue(info.has_capability(ddp.DDP_CAP_ANALOG_INPUT))
        self.assertIn("id=0x0102", ddp.format_device_info(info, 0x0102))
        bus.assert_done()

    def test_discover_uses_preferred_address(self):
        bus = ScriptedI2C(identity_steps(0x20), scans=([0x30, 0x20],))
        master = self.make_master(bus)

        info = master.discover(preferred_address=0x20)

        self.assertIsNotNone(info)
        self.assertEqual(info.address, 0x20)
        bus.assert_done()

    def test_read_adc_without_repeating_identity(self):
        bus = ScriptedI2C(command_steps(0x20, ddp.CMD_READ_ADC0, (0x34, 0x02)))
        master = self.make_master(bus)

        self.assertEqual(master.read_adc(0x20, verify=False), 0x0234)
        bus.assert_done()

    def test_staged_adc_averaging_accepts_packed_ack(self):
        steps = command_steps(0x20, ddp.CMD_GET_ADC_AVERAGING, (1,))
        steps += command_steps(0x20, ddp.CMD_SET_ADC_AVERAGING, (0xFC,))
        steps += [
            ("write", 0x20, bytes((8,))),
            ("read", 0x20, 1, bytes((0x0C,))),
        ]
        delays = []
        bus = ScriptedI2C(steps)
        master = self.make_master(bus, delays)

        self.assertEqual(master.set_adc_averaging(0x20, 8, verify=False), 8)
        self.assertEqual(delays[-2:], [25, 160])
        bus.assert_done()

    def test_address_change_verifies_old_and_new_identity(self):
        steps = identity_steps(0x20)
        steps += command_steps(0x20, ddp.CMD_SET_I2C_ADDR, (0xFD,))
        steps += [
            ("write", 0x20, bytes((0x30,))),
            ("read", 0x20, 1, bytes((0x0D,))),
        ]
        steps += identity_steps(0x30)
        bus = ScriptedI2C(steps, scans=([0x20],))
        master = self.make_master(bus)

        info = master.set_i2c_address(0x20, 0x30)

        self.assertEqual(info.address, 0x30)
        self.assertEqual(info.device_id, ddp.DEVICE_TEMT6000)
        bus.assert_done()

    def test_address_collision_stops_before_setter(self):
        bus = ScriptedI2C(identity_steps(0x20), scans=([0x20, 0x30],))
        master = self.make_master(bus)

        with self.assertRaises(ddp.DDPCollisionError):
            master.set_i2c_address(0x20, 0x30)
        bus.assert_done()

    def test_incompatible_protocol_raises(self):
        bus = ScriptedI2C(
            command_steps(0x20, ddp.CMD_GET_PROTOCOL, (2, 0))
        )
        master = self.make_master(bus)

        with self.assertRaises(ddp.DDPProtocolError):
            master.identify(0x20)
        bus.assert_done()

    def test_short_response_raises(self):
        bus = ScriptedI2C(
            [
                ("write", 0x20, bytes((ddp.CMD_READ_ADC0,))),
                ("read", 0x20, 2, bytes((0x34,))),
            ]
        )
        master = self.make_master(bus)

        with self.assertRaises(ddp.DDPResponseError):
            master.read_adc(0x20, verify=False)
        bus.assert_done()


if __name__ == "__main__":
    unittest.main()
