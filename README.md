# DevLab: I2C TEMT6000 Ambient Light Sensor

## Introduction

The **DevLab I2C TEMT6000 Ambient Light Sensor** is a compact ambient light sensing module based on the **Vishay TEMT6000 phototransistor** and a **PY32F003 microcontroller**.

Unlike a conventional TEMT6000 module with only an analog output, this version integrates an **I2C interface** that allows the sensor signal to be acquired and processed by the onboard microcontroller and accessed digitally from an I2C host.

The module also provides direct access to the **raw sensor signal** through a dedicated header, making it possible to use the TEMT6000 output directly for analog measurements, testing, characterization, or custom signal processing.

Three I2C connectors are available on the board, allowing easy integration with other DevLab modules and I2C-based systems.


<div align="center">

  <img src="hardware/resources/unit_top_V_0_3_1_ue0098_temt6000.png" width="500px" alt="DevLab I2C TEMT6000 Ambient Light Sensor">

</div>


<div align="center">

### Quick Setup

[<img src="https://img.shields.io/badge/Product%20Wiki-blue?style=for-the-badge" alt="Product Wiki">](https://wiki.uelectronics.com/wiki/devlab-temt6000-ambient-light-sensor)

[<img src="https://img.shields.io/badge/Datasheet-green?style=for-the-badge" alt="Datasheet">](https://github.com/UNIT-Electronics-MX/unit_devlab_temt6000_ambient_light_sensor/blob/main/hardware/unit_datasheet_v_1_0_0_ue0098_temt6000_ambient_light_sensor_en.pdf)

[<img src="https://img.shields.io/badge/Buy%20Now-orange?style=for-the-badge" alt="Buy Now">](https://uelectronics.com/)

[<img src="https://img.shields.io/badge/Getting%20Started-purple?style=for-the-badge" alt="Getting Started">](https://github.com/UNIT-Electronics-MX/unit_devlab_temt6000_ambient_light_sensor/tree/main/software)

</div>


## Overview

| Feature | Description |
|---|---|
| Sensor | TEMT6000 Ambient Light Sensor |
| Sensor Type | Ambient light phototransistor |
| Onboard MCU | PY32F003 |
| Main Interface | I2C |
| Raw Signal Access | Direct sensor signal available through dedicated header |
| I2C Connectivity | 3 I2C connectors |
| Status Indicators | Power and user/status LEDs |
| Debug / Test | Dedicated test points |
| Module Function | Ambient light acquisition and I2C sensor interface |


## How It Works

The **TEMT6000** phototransistor generates a signal according to the incident ambient light level.

This signal is connected directly to the onboard **PY32F003 microcontroller**, which can acquire and process the sensor output and make the resulting information available through the **I2C interface**.

The board also exposes the sensor signal through the **RAW Signal Header**, allowing direct access to the unprocessed TEMT6000 output independently of the I2C interface.

This architecture provides two ways to work with the sensor:

- **I2C interface:** Easy digital integration with microcontrollers and other I2C systems.
- **RAW signal:** Direct access to the sensor output for analog measurements, testing, or custom processing.


## I2C Interface

The module includes **three I2C connectors** connected to the same bus, providing convenient connection points for integration with DevLab modules and other compatible I2C devices.

The I2C interface provides:

- SDA
- SCL
- VCC
- GND

The onboard PY32F003 acts as the interface between the TEMT6000 sensor signal and the I2C bus.


## RAW Signal Header

A dedicated header provides direct access to the **unprocessed TEMT6000 sensor signal**.

This output can be useful for:

- Direct ADC measurements.
- Sensor characterization.
- Signal monitoring.
- Calibration and testing.
- Custom external processing.
- Educational experiments comparing raw and processed sensor data.


## Status LEDs

The module includes onboard status indicators for power and user/status feedback.

These LEDs provide a simple visual indication of the module operating state and can also be used during development, testing, and debugging.


## Test Points

Dedicated test points are included to facilitate development, debugging, production testing, and hardware validation.

They provide convenient access to relevant communication and control signals without requiring direct probing of the onboard components.


## Use Cases

- Ambient light monitoring.
- Automatic display brightness adjustment.
- Smart lighting systems.
- Home and industrial automation.
- IoT environmental monitoring.
- Light-level data logging.
- Educational and prototyping applications.
- Sensor characterization using the RAW signal output.
- Integration into I2C sensor networks.


## Resources

- [Schematic Diagram](https://github.com/UNIT-Electronics-MX/unit_devlab_temt6000_ambient_light_sensor/blob/main/hardware/unit_sch_v_2_0_0_ue0098_temt6000.pdf)

- [Pinout Diagram](https://github.com/UNIT-Electronics-MX/unit_devlab_temt6000_ambient_light_sensor/blob/main/hardware/unit_pinout_v_0_0_2_ue0098_temt6000_ambient_light_sensor_en.pdf)

- [Datasheet](https://github.com/UNIT-Electronics-MX/unit_devlab_temt6000_ambient_light_sensor/blob/main/hardware/unit_datasheet_v_1_0_0_ue0098_temt6000_ambient_light_sensor_en.pdf)


## 📝 License

All hardware and documentation in this project are licensed under the **MIT License**.

Please refer to [`LICENSE.md`](LICENSE.md) for full terms.


<div align="center">

  <sub>Developed by UNIT Electronics</sub>

</div>