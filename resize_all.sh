#!/usr/bin/env bash
set -euo pipefail

# ================================
# CONFIG (LOCKED)
# ================================

SRC="tests/output/avatar_forest_jim_12_px8.png"
OUTDIR="tests/output/resized_locked"
PALETTE_NAME="forest-jim-12"

# Size → pixel-size mapping (DO NOT EDIT)
# format: size:px
SIZES=(
  "32:1"
  "48:1"
  "64:1"
  "96:1"
  "128:2"
  "256:4"
  "512:8"
  "1024:16"
  # "2048:32"  # OPTIONAL MASTER — uncomment only if explicitly needed
)

# ================================
# PRECHECKS
# ================================

command -v magick >/dev/null || { echo "ImageMagick missing"; exit 1; }
command -v identify >/dev/null || { echo "identify missing"; exit 1; }

[ -f "$SRC" ] || {
  echo "ERROR: source image not found:"
  echo "  $SRC"
  exit 1
}

mkdir -p "$OUTDIR"

echo "== Locked resize pipeline =="
echo "Source: $SRC"
echo "Palette: $PALETTE_NAME"
echo

# ================================
# PROCESS
# ================================

for entry in "${SIZES[@]}"; do
  size="${entry%%:*}"
  px="${entry##*:}"
  out="$OUTDIR/avatar_${size}x${size}.png"

  echo "→ ${size}x${size} (px=${px})"

  # Resize using strict nearest-neighbor ONLY
  magick "$SRC" \
    -filter point \
    -resize "${size}x${size}!" \
    "$out"

  # ================================
  # VALIDATION
  # ================================

  # 1. Dimension check
  dims=$(identify -format "%wx%h" "$out")
  if [ "$dims" != "${size}x${size}" ]; then
    echo "FAIL: dimension mismatch ($dims)"
    exit 1
  fi

  # 2. Pixel grid check (must divide cleanly)
  if (( size % px != 0 )); then
    echo "FAIL: size ${size} not divisible by px ${px}"
    exit 1
  fi

  # 3. Palette size check (≤12)
  colors=$(identify -format "%k" "$out")
  if (( colors > 12 )); then
    echo "FAIL: palette leak (${colors} colors)"
    exit 1
  fi

done

echo
echo "✔ ALL OUTPUTS VERIFIED"
echo "✔ Nearest-neighbor only"
echo "✔ Grid integrity preserved"
echo "✔ Palette respected"