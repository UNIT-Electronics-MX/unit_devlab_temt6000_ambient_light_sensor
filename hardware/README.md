# Hardware
<div align="center">
    <a href="./unit_sch_V_0_0_1_ue0098_TEMT6000.pdf"><img src="./resources/v_3_1_0/Schematics_icon.jpg" width="450px" alt="Schematics"/><br/> Schematics</a>
</div>

---


## Key Technical Specifications

<!-- 
========================================
EDITABLE SPECIFICATIONS TEMPLATE
========================================
Edita los valores a continuación según necesites.
El formato se mantendrá automáticamente en el PDF generado.
-->

### 🔌 Connectivity
<!-- Edita las interfaces y conectores disponibles -->
<div align=center>

| Interface | Details |
|-----------|---------|
| **Primary Interface** | GPIO (Analog) |
| **Connector Type** | JST 4-pin 1.0mm |
| **Logic Levels** | VCC |

</div>


## ⚙️ Technical Specifications

<div align="center">

| Pin | Symbol | Type     | Description                                                                 |
| :---: | :----- | :------- | :-------------------------------------------------------------------------- |
| 1     | GND    | Power    | Ground reference (connect to MCU GND)                                       |
| 2     | VCC    | Power    | +3.3 V to +5 V supply voltage                                               |
| 3     | D0     | Analog   | voltage ∝ ambient light; connect to an ADC input of your MCU |
</div>

> **Note:** Do not exceed 5 V on VCC. SIO swings between 0 V (dark) and VCC (bright).

### Electrical Characteristics

<div align=center>

| Symbol/Rail | Description                                          | Min  | Typ         | Max  | Unit |
|-------------|------------------------------------------------------|------|-------------|------|------|
|   V_CEO     | Collector emitter voltage                            | -    | -           | 6    | V    |
|   I_C       | Collector Current                                    | -    | -           | 20   | mA   |
|   V_ECO     | Emitter collector voltage                            | -    | -           | 1.5  | V    |
|   P_V       | Power dissipation                                    | -    | -           | 100  | mW   |
|   φ         | Angle of half sensitivity                            | -    | ±60         | -    | deg  |
|   λ_P       | Wavelength of peak sensitivity                       | -    | 570         | -    | nm   |
|   λ_0.5     | Range of spectral bandwidth                          | 440  | -           | 800  | nm   |

</div>

## 🔌 Pinout

<div align="center">
    <a href="./unit_pinout_v_3_1_0_ue0098_temt6000_ambient_light_sensor_en.pdf"><img src="./resources/pinout/v_0_3_1/unit_pinout_v_3_1_0_ue0098_temt6000_ambient_light_sensor_en.png" width="500px"><br/>Pinout</a>
    <br/><br/>

</div>

### **Pinout Details**

<div align="center">

| Pin Label | Function        | Notes                             |
|-----------|-----------------|-----------------------------------|
| VCC       | Power Supply    | 3.3V or 5V, depending on design    |
| GND       | Ground          | Common ground reference            |
| D0        | Data Signal     | Digital input/output signal        |

</div>

## 📃 Topology

<div align="center">
<a href="./resources/unit_topology_V_0_0_1_ue0098_TEMT6000.png"><img src="./resources/unit_topology_V_0_0_1_ue0098_TEMT6000.png" width="300px"><br/> Topology</a>

| Ref. | Description                              |
|------|------------------------------------------|
| S1   | TEMT6000 Ambient Light Sensor            |
| J1   | JST 1 mm pitch Connector for Power Supply and Signal |

</div>

## 📏 Dimensions

<div align="center">
<a href="./resources/unit_dimension_V_0_0_1_ue0098_TEMT6000.png"><img src="./resources/unit_dimension_V_0_0_1_ue0098_TEMT6000.png" width="500px"><br/> Dimensions</a>
</div>

## Reference 

- [Datasheet](https://www.vishay.com/docs/84374/temt6000.pdf)