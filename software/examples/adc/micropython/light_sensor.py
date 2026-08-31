from machine import ADC, Pin
import time

# ADC-only example: connect this host pin to the board's direct SIG contact.
# Do not combine this ADC-only wiring with the GPIO6/GPIO7 I2C wiring.
ADC_PIN = 6
ADC_FULL_SCALE_V = 3.3
SAMPLE_COUNT = 16

sensor = ADC(Pin(ADC_PIN))

try:
    sensor.atten(ADC.ATTN_11DB)
except (AttributeError, OSError):
    pass


def read_once():
    if hasattr(sensor, "read_u16"):
        return sensor.read_u16(), 65535
    return sensor.read(), 4095


def read_average():
    total = 0
    adc_max = 0
    for _ in range(SAMPLE_COUNT):
        raw, adc_max = read_once()
        total += raw
        time.sleep_ms(2)
    return total / SAMPLE_COUNT, adc_max


print("UNIT ATOM TEMT6000 direct analog SIG")
print("V0.3.1 transfer and lux calibration are not yet specified.")

while True:
    raw, adc_max = read_average()
    voltage = raw * ADC_FULL_SCALE_V / adc_max
    print("Raw: {:.1f}  Voltage: {:.3f} V".format(raw, voltage))
    time.sleep_ms(500)
