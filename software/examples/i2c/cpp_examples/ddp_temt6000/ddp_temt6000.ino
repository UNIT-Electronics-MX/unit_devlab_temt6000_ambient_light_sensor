#include <Arduino.h>
#include <Wire.h>
#include <DevLabDDP.h>

namespace {

constexpr uint8_t FACTORY_I2C_ADDRESS = 0x20U;
constexpr uint32_t I2C_CLOCK_HZ = 400000UL;
#if defined(ARDUINO_ARCH_ESP32)
constexpr uint8_t I2C_SDA_PIN = 6U;
constexpr uint8_t I2C_SCL_PIN = 7U;
#endif
constexpr uint16_t DDP_ADC_MAX = 4095U;
constexpr uint32_t CURRENT_CAPABILITIES = 0x000001B9UL;
constexpr uint8_t EXPECTED_ADC_AVERAGING_ACK = 0x0CU;
// Command-specific packed-ACK low nibbles; 0x01 means RELAY_ON accepted here.
constexpr uint8_t EXPECTED_RELAY_OFF_ACK = 0x00U;
constexpr uint8_t EXPECTED_RELAY_ON_ACK = 0x01U;
constexpr uint8_t BUILTIN_BLINK_COUNT = 3U;

// Set to 0x08..0x77 to request a persistent address change; 0 disables it.
constexpr uint8_t REQUESTED_I2C_ADDRESS = 0U;
// Set to 1, 4, 8, 16, or 24; 0 only reports the current persistent value.
constexpr uint8_t REQUESTED_ADC_AVERAGING = 0U;

DevLabDDP::Master temt6000(Wire, DevLabDDP::DEVICE_TEMT6000);
DevLabDDP::DeviceInfo deviceInfo;
uint8_t deviceAddress = 0U;
uint8_t averagingSamples = 1U;

bool ackLowNibbleIs(uint8_t response, uint8_t expected) {
  return (response & 0x0FU) == expected;
}

bool identifyAt(uint8_t address) {
  DevLabDDP::DeviceInfo candidate;
  if (!temt6000.matchesExpectedDevice(address, &candidate)) return false;
  if ((candidate.capabilities & DDP_CAP_ANALOG_INPUT) == 0U) return false;

  deviceAddress = address;
  deviceInfo = candidate;
  DevLabDDP::printDeviceInfo(
      Serial, deviceAddress, deviceInfo, DevLabDDP::DEVICE_TEMT6000);
  if (deviceInfo.capabilities != CURRENT_CAPABILITIES) {
    Serial.println("Notice: capabilities differ from firmware 1.0 profile.");
  }
  return true;
}

bool discoverTemt6000() {
  if (identifyAt(FACTORY_I2C_ADDRESS)) return true;
  for (uint8_t address = 0x08U; address <= 0x77U; ++address) {
    if (address != FACTORY_I2C_ADDRESS && identifyAt(address)) return true;
  }
  return false;
}

bool readRaw(uint16_t &value) {
  uint8_t bytes[2];
  if (!temt6000.readCommand(
          deviceAddress, CMD_READ_ADC0, bytes, sizeof(bytes), 5U)) {
    return false;
  }
  if ((bytes[1] & 0xF0U) != 0U) return false;
  value = static_cast<uint16_t>(bytes[0]) |
          (static_cast<uint16_t>(bytes[1]) << 8);
  return value <= DDP_ADC_MAX;
}

bool getAveraging(uint8_t &samples) {
  if (!temt6000.readCommand(
          deviceAddress, CMD_GET_ADC_AVERAGING, &samples, 1U, 5U)) {
    return false;
  }
  return samples == 1U || samples == 4U || samples == 8U ||
         samples == 16U || samples == 24U;
}

bool setAveraging(uint8_t samples) {
  if (samples != 1U && samples != 4U && samples != 8U &&
      samples != 16U && samples != 24U) {
    return false;
  }

  uint8_t current = 0U;
  if (!getAveraging(current)) return false;
  if (current == samples) {
    averagingSamples = current;
    return true;
  }

  uint8_t ack = 0U;
  if (!temt6000.readCommand(
          deviceAddress, CMD_SET_ADC_AVERAGING, &ack, 1U, 5U) ||
      !ackLowNibbleIs(ack, EXPECTED_ADC_AVERAGING_ACK) ||
      !temt6000.writeByte(deviceAddress, samples)) {
    return false;
  }

  delay(25U);
  if (Wire.requestFrom(deviceAddress, static_cast<uint8_t>(1U)) != 1U ||
      !ackLowNibbleIs(Wire.read(), EXPECTED_ADC_AVERAGING_ACK)) {
    return false;
  }

  averagingSamples = samples;
  delay(static_cast<uint32_t>(samples) * 20UL);
  return true;
}

void reportAndOptionallyChangeAddress() {
  uint8_t reportedAddress = 0U;
  if (temt6000.getI2cAddress(deviceAddress, reportedAddress)) {
    Serial.print("Active 7-bit address: 0x");
    if (reportedAddress < 0x10U) Serial.print('0');
    Serial.println(reportedAddress, HEX);
  }

  if (REQUESTED_I2C_ADDRESS == 0U || REQUESTED_I2C_ADDRESS == deviceAddress) {
    return;
  }
  if (!temt6000.setI2cAddress(deviceAddress, REQUESTED_I2C_ADDRESS)) {
    Serial.println("Address change failed; target may be occupied.");
    return;
  }

  deviceAddress = REQUESTED_I2C_ADDRESS;
  if (!identifyAt(deviceAddress)) {
    Serial.println("Device ID 0x0102 not verified at the new address.");
    deviceAddress = 0U;
  } else {
    Serial.println("Persistent address changed and identity verified.");
  }
}

bool actuatorCommand(uint8_t command, uint8_t expectedLowNibble) {
  uint8_t ack = 0U;
  return temt6000.readCommand(deviceAddress, command, &ack, 1U, 5U) &&
         ackLowNibbleIs(ack, expectedLowNibble);
}

void blinkBuiltin() {
  if ((deviceInfo.capabilities & DDP_CAP_RELAY) == 0U) return;
  for (uint8_t cycle = 0U; cycle < BUILTIN_BLINK_COUNT; ++cycle) {
    if (!actuatorCommand(CMD_RELAY_ON, EXPECTED_RELAY_ON_ACK)) return;
    delay(150U);
    if (!actuatorCommand(CMD_RELAY_OFF, EXPECTED_RELAY_OFF_ACK)) return;
    delay(150U);
  }
  Serial.println("BUILTIN blink complete (relay-compatible PB5 commands).");
}

void configureAveraging() {
  if (!getAveraging(averagingSamples)) {
    Serial.println("Could not read ADC averaging configuration.");
    return;
  }

  if (REQUESTED_ADC_AVERAGING != 0U &&
      !setAveraging(REQUESTED_ADC_AVERAGING)) {
    Serial.println("ADC averaging change failed.");
    return;
  }

  Serial.print("Device ADC averaging: ");
  Serial.print(averagingSamples);
  Serial.println(" sample(s)");
}

}  // namespace

void setup() {
  Serial.begin(115200);
#if defined(ARDUINO_ARCH_ESP32)
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
#else
  Wire.begin();
#endif
  Wire.setClock(I2C_CLOCK_HZ);

  Serial.println("UNIT ATOM TEMT6000 — DDP v1.0");
  if (!discoverTemt6000()) {
    Serial.println("No compatible TEMT6000 DDP device found.");
    return;
  }

  reportAndOptionallyChangeAddress();
  if (deviceAddress == 0U) return;
  configureAveraging();
  blinkBuiltin();
}

void loop() {
  if (deviceAddress == 0U && !discoverTemt6000()) {
    delay(2000U);
    return;
  }

  uint16_t raw = 0U;
  if (readRaw(raw)) {
    Serial.print("ADC0/TEMT6000 raw (device average ");
    Serial.print(averagingSamples);
    Serial.print("): ");
    Serial.print(raw);
    Serial.println(" / 4095");
  } else {
    Serial.println("Read failed; rediscovering device.");
    deviceAddress = 0U;
  }

  delay(100U);
}
