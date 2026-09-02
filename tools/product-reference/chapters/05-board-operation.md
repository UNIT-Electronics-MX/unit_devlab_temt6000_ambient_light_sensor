## **5 Board Operation**

This chapter shows how to verify one UNIT ATOM TEMT6000 and read its raw
ambient-light value with Arduino. The example supports the Pulsar ESP32-C6 and
Pulsar RP2350 host boards.

### **5.1 Required Hardware and Software** {.section-page}

- UNIT ATOM TEMT6000 module
- Pulsar ESP32-C6 or Pulsar RP2350 development board
- I2C connection for `VCC`, `GND`, `SDA`, and `SCL`
- USB cable for programming and Serial Monitor access
- Arduino IDE with the selected board package installed
- `DevLab_TEMT6000` Arduino library

### **5.2 Library Installation**

1. Open **Tools > Manage Libraries** in Arduino IDE.
2. Search for `DevLab_TEMT6000`.
3. Select the current release and click **Install**.
4. Allow Arduino IDE to install the `DevLabDDP` dependency when prompted.

![](tools/product-reference/assets/temt6000_library.png){width=2.8in}

**Figure 5.1 — DevLab_TEMT6000 in Arduino Library Manager.** The installed
package provides the TEMT6000 examples and installs the DDP communication
dependency used by the sketch below.

### **5.3 I2C Connection and Example Settings** {.page-break}

Connect the module with power removed.

![](tools/product-reference/assets/devlab_atom.png){width=5.8in}

**Figure 5.2 — Qwiic connection to a Pulsar ESP32-C6 host.** Align the
connector with the orientation shown and verify `VCC`, `GND`, `SDA`, and `SCL`
before applying power.

| Module | Pulsar ESP32-C6 | Pulsar RP2350 | Function |
|---|---:|---:|---|
| `VCC` | 3.3 V or 5 V | 3.3 V or 5 V | Module supply |
| `GND` | `GND` | `GND` | Common reference |
| `SDA` | GPIO6 | GPIO24 | I2C data |
| `SCL` | GPIO7 | GPIO25 | I2C clock |

The pin numbers above match `singleSensor.ino`. Change `I2C_SDA` and
`I2C_SCL` when the selected host board uses different I2C pins. At 5 V,
confirm that the host accepts the bus pull-up voltage or use bidirectional
level translation.

The example uses the following settings:

| Constant | Default | Purpose |
|---|---:|---|
| `I2C_SDA` | GPIO6 on Pulsar ESP32-C6; GPIO24 on Pulsar RP2350 | Host SDA pin |
| `I2C_SCL` | GPIO7 on Pulsar ESP32-C6; GPIO25 on Pulsar RP2350 | Host SCL pin |
| `I2C_FREQ` | 400000 Hz | I2C clock |
| `SENSOR_ADDRESS` | `0x20` | Factory 7-bit module address |
| `READ_INTERVAL_MS` | 1000 ms | Time between printed readings |

If the module address was changed previously, update `SENSOR_ADDRESS` before
uploading the sketch.

### **5.4 Single-Sensor Arduino Example** {.page-break}

Open or create `singleSensor.ino`, then use the following sketch:

```{.cpp .compact-code}
/**
 * @file singleSensor.ino
 * @brief Verifies a single TEMT6000 DDP device on the I2C bus and prints
 *        its raw ADC0 readings over Serial at a fixed interval.
 * @author Cesar Bautista
 */

#include <Arduino.h>
#include <Wire.h>
#include <DevLabDDP.h>
#include <DevLabI2CBusRecovery.h>

#if defined(ARDUINO_ARCH_RP2040)
#define I2C_BUS Wire
constexpr uint8_t I2C_SDA = 24U, I2C_SCL = 25U;
#elif defined(ARDUINO_ARCH_ESP32)
#define I2C_BUS Wire
constexpr uint8_t I2C_SDA = 6U, I2C_SCL = 7U;
#else
#error "Use Pulsar ESP32-C6 or Pulsar RP2350"
#endif

constexpr uint32_t I2C_FREQ = 400000;
constexpr uint8_t SENSOR_ADDRESS = 0x20;
constexpr uint32_t READ_INTERVAL_MS = 1000U;

DevLabDDP::Master master(I2C_BUS, DevLabDDP::DEVICE_TEMT6000);
bool deviceVerified = false;

void setup() {
  Serial.begin(115200);
  delay(500);

  if (!devlabBeginI2cBusRecovered(
          I2C_BUS, I2C_SDA, I2C_SCL, I2C_FREQ, 100)) {
    Serial.println("ERROR: I2C bus is blocked");
    return;
  }

  DevLabDDP::DeviceInfo info;
  deviceVerified = master.matchesExpectedDevice(SENSOR_ADDRESS, &info);

  if (!deviceVerified) {
    Serial.println("ERROR: address is not a DDP TEMT6000 (ID 0x0102)");
    return;
  }

  DevLabDDP::printDeviceInfo(
      Serial,
      SENSOR_ADDRESS,
      info,
      DevLabDDP::DEVICE_TEMT6000);

  Serial.println("adc0_raw");
}

void loop() {
  uint16_t raw;

  if (deviceVerified && master.readAdc(SENSOR_ADDRESS, 0, raw)) {
    Serial.println(raw);
  } else {
    Serial.println("ERR");
  }

  delay(READ_INTERVAL_MS);
}
```

### **5.5 Upload and Serial Output** {.section-page}

1. Select the connected Pulsar ESP32-C6 or Pulsar RP2350 board in Arduino IDE.
2. Select its serial port.
3. Compile and upload `singleSensor.ino`.
4. Open Serial Monitor at **115200 baud**.
5. Illuminate and cover the TEMT6000 to confirm that the printed value changes.

At startup, the sketch recovers and initializes the I2C bus, verifies that
address `0x20` contains a DDP TEMT6000 with Device ID `0x0102`, and prints
the reported device information. It then prints the heading `adc0_raw` and one
reading per second.

```text
<DDP device information>
adc0_raw
<value from 0 to 4095>
<value from 0 to 4095>
```

The readings are raw ADC values. They indicate relative light level and must
not be interpreted directly as lux.

### **5.6 Troubleshooting** {.section-page}

| Serial output or symptom | Check |
|---|---|
| `ERROR: I2C bus is blocked` | Wiring, connector orientation, shared ground, pull-up voltage, and unintended SDA/SCL drive |
| `ERROR: address is not a DDP TEMT6000 (ID 0x0102)` | Address setting, I2C pins, module power, and possible address collision |
| `ERR` after successful identification | Cable continuity, bus clock, supply stability, and I2C connections |
| Constant `0` or `4095` | Sensor obstruction, excessive illumination, supply, and module orientation |
| Values change but lux is inaccurate | Calibrate the complete optical installation against a reference light meter |

The complete Arduino examples and the reusable DDP library are listed in
Chapter 8.
