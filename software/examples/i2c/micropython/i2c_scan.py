from machine import I2C, Pin
import time

# Repository example wiring: GPIO6 = SDA and GPIO7 = SCL on the host board.
I2C_BUS = 0
SDA_PIN = 6
SCL_PIN = 7

i2c = I2C(
    I2C_BUS,
    sda=Pin(SDA_PIN),
    scl=Pin(SCL_PIN),
    freq=100_000,
)

print("UNIT ATOM TEMT6000 I2C scanner")
print("A detected address does not define the measurement protocol.")

while True:
    devices = i2c.scan()
    if devices:
        print("I2C responses:", ", ".join("0x{:02X}".format(a) for a in devices))
    else:
        print("No I2C devices found")
    time.sleep(2)
