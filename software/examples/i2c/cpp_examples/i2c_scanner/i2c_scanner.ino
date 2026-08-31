#include <Arduino.h>
#include <Wire.h>

#if defined(ARDUINO_ARCH_ESP32)
constexpr uint8_t I2C_SDA_PIN = 6U;
constexpr uint8_t I2C_SCL_PIN = 7U;
#endif

void setup() {
  Serial.begin(115200);
#if defined(ARDUINO_ARCH_ESP32)
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
#else
  Wire.begin();
#endif
  Wire.setClock(100000);

  Serial.println("UNIT ATOM TEMT6000 I2C scanner");
  Serial.println("A detected address does not define the measurement protocol.");
}

void loop() {
  uint8_t devices = 0;

  Serial.println("Scanning...");
  for (uint8_t address = 1; address < 127; ++address) {
    Wire.beginTransmission(address);
    const uint8_t error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C response at 0x");
      if (address < 0x10) {
        Serial.print('0');
      }
      Serial.println(address, HEX);
      ++devices;
    } else if (error == 4) {
      Serial.print("Unknown bus error at 0x");
      if (address < 0x10) {
        Serial.print('0');
      }
      Serial.println(address, HEX);
    }
  }

  if (devices == 0) {
    Serial.println("No I2C devices found.");
  } else {
    Serial.print("Devices found: ");
    Serial.println(devices);
  }

  delay(2000);
}
