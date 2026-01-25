#!/usr/bin/env bash
set -euo pipefail

echo "== Pixel.py test suite =="

# Resolve paths safely
ROOT="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$ROOT/.." && pwd)"
PIXEL="$PROJECT_ROOT/pixel.py"
IN="$ROOT/input"
OUT="$ROOT/output"

mkdir -p "$OUT"

# -------------------------
# Test 1: Grid snap only
# -------------------------
echo
echo "[1/5] Avatar grid snap (px=8)"

python3 "$PIXEL" run \
  "$IN/avatar.png" \
  "$OUT/avatar_px8.png" \
  --px 8

# -------------------------
# Test 2: Palette + grid
# -------------------------
echo
echo "[2/5] Avatar DMG-green (px=8)"

python3 "$PIXEL" run \
  "$IN/avatar.png" \
  "$OUT/avatar_dmg_green_px8.png" \
  --px 8 \
  --palette dmg-green

# -------------------------
# Test 3: Palette color count
# -------------------------
echo
echo "[3/5] Palette color count (expect 4)"

python3 - <<EOF
from PIL import Image
img = Image.open("$OUT/avatar_dmg_green_px8.png").convert("RGB")
colors = img.getcolors(1_000_000)
assert colors is not None, "getcolors() returned None"
print("Unique colors:", len(colors))
assert len(colors) == 4, "Expected 4 colors"
EOF

# -------------------------
# Test 4: JB icons batch sanity (manual loop)
# -------------------------
echo
echo "[4/5] JB icons sanity run (DMG-green)"

JB_IN="$IN/jb_icons_working"
JB_OUT="$OUT/jb_icons_dmg"

mkdir -p "$JB_OUT"

count=0
for f in "$JB_IN"/*.png; do
  name="$(basename "$f")"
  python3 "$PIXEL" run \
    "$f" \
    "$JB_OUT/$name" \
    --px 8 \
    --palette dmg-green
  count=$((count+1))
done

echo "Processed $count JB icons"

# -------------------------
# Test 5: Output existence
# -------------------------
echo
echo "[5/5] Output file presence check"

for f in \
  "$OUT/avatar_px8.png" \
  "$OUT/avatar_dmg_green_px8.png"
do
  [ -f "$f" ] || { echo "Missing: $f"; exit 1; }
done

echo
echo "== All tests passed =="
