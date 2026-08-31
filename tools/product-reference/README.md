# Product Reference build

The UNIT ATOM TEMT6000 Product Reference source is maintained in Markdown under
`chapters/`. Document metadata and chapter order are defined in `book.yml`.
Version 1.1.0 is based on the V0.3.1 board images, V3.1.0 pinout, legacy
V0.0.1 schematic, a Vishay TEMT6000X01 datasheet used only as a comparative
reference, DevLab Device Protocol v1.0, and the repository examples. The
reference datasheet does not establish the manufacturer or exact orderable
part fitted to the module.

The Product Reference documents the current PY32F003 firmware profile: factory
address `0x20`, DDP identity `0x0102`, versions 1.0, capabilities
`0x000001BB`, command timing, persistent configuration, ADC averaging, and the
`TEMT6000_RAW` (`0x80`) 12-bit response. It keeps the current-revision
schematic and complete module electrical limits as open requirements.

## Local validation build

Requirements:

- Pandoc
- WeasyPrint, Google Chrome, or Chromium

Run from the repository root and direct validation output outside the
repository:

```bash
./tools/product-reference/build.sh /tmp/atom-temt6000-product-reference
```

The build produces:

```text
unit_product_reference_v_1_1_0_atom_temt6000_ambient_light_sensor.md
unit_product_reference_v_1_1_0_atom_temt6000_ambient_light_sensor.docx
unit_product_reference_v_1_1_0_atom_temt6000_ambient_light_sensor.html
unit_product_reference_v_1_1_0_atom_temt6000_ambient_light_sensor.pdf
```

GitHub Actions publishes the PDF and DOCX under `docs/hardware/`. Do not edit
generated documents or `docs/` manually.

The Markdown chapters are the source of truth. Module values and mappings must
come from controlled technical references. The V0.3.1 module provides Qwiic
I2C connectors and separate direct analog access. Do not infer complete module
limits from the legacy analog schematic or an individual component rating.

Known source inconsistencies and unspecified board-level values are listed in
Chapter 9.
