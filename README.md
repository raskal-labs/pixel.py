# pixel.py

Deterministic image → pixel-art conversion with palette quantization.

## Goals
- Deterministic, repeatable output
- Palette-driven recoloring (DMG / GBC / EL styles)
- Simple CLI, scriptable, testable
- Suitable for stateless and batch pipelines

## Requirements
- Python 3.9+
- Pillow (PIL)

### Debian / Ubuntu
```bash
apt update
apt install -y python3 python3-pip
pip3 install --break-system-packages pillow

Usage

Help

python3 pixel.py help

List palettes

python3 pixel.py palette

Inspect a palette

python3 pixel.py check dmg-green

Run (single image)

python3 pixel.py run tests/input/avatar.png /tmp/out.png --px 8 --palette dmg-green

Run options
	•	--px N
Snap image to an N×N pixel grid (nearest-neighbor).
	•	--palette NAME
Palette name loaded from palettes/**/*.json.
	•	--colors N
Limit palette to first N colors (useful for testing or constraints).

Palettes

Palettes live in the palettes/ directory and are defined as JSON files.

Palette format

{
  "name": "dmg-green",
  "colors": [
    { "hex": "#0F380F" },
    { "hex": "#306230" },
    { "hex": "#8BAC0F" },
    { "hex": "#9BBC0F" }
  ]
}

Notes:
	•	Color order matters (dark → light recommended)
	•	Hex colors only (no alpha)
	•	2–8 colors recommended

Tests

Run the test suite:

cd tests
chmod +x run_all_tests.sh
./run_all_tests.sh

Notes:
	•	tests/output/ is generated
	•	Tests are deterministic
	•	Failures should be visually diffable

Project layout

pixel.py/
├── pixel.py
├── palettes/
├── tests/
│   ├── input/
│   ├── output/
│   └── run_all_tests.sh
├── examples/
├── README.md
├── CHANGELOG.md
└── .gitignore

Repository

Name: raskal-labs/pixel.py
Description: Deterministic pixel-art conversion and palette quantization for icons and wallpapers.

