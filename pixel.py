#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from PIL import Image

VERSION = "0.6"

ROOT = Path(__file__).parent.resolve()
PALETTES_DIR = ROOT / "palettes"

# ----------------------------
# Utility
# ----------------------------

def die(msg):
    print(f"Error: {msg}")
    sys.exit(1)

def banner():
    print(
"""█████▄ ██ ██  ██ ██████ ██       ▄▄▄▄  ▄▄ ▄▄
██▄▄█▀ ██  ████  ██▄▄   ██       ██▄█▀ ▀███▀
██     ██ ██  ██ ██▄▄▄▄ ██████ ▄ ██      █
pixel.py
"""
    )

# ----------------------------
# Palette handling
# ----------------------------

def load_palettes():
    palettes = {}
    for path in PALETTES_DIR.rglob("*.json"):
        try:
            data = json.load(open(path))
            name = data.get("name", path.stem)
            name = name.replace("_", "-")
            colors = [c["hex"] for c in data.get("colors", []) if "hex" in c]
            if colors:
                palettes[name] = colors
        except Exception:
            pass
    return palettes

PALETTES = load_palettes()

def list_palettes():
    for name, cols in sorted(PALETTES.items()):
        print(f"{name:20} {len(cols)} colors")

def get_palette(name):
    if name is None or name == "auto":
        return None
    name = name.replace("_", "-")
    if name not in PALETTES:
        die(f"Unknown palette: {name}")
    return PALETTES[name]

# ----------------------------
# Image processing
# ----------------------------

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0,2,4))

def quantize(img, palette_hex):
    pal = []
    for h in palette_hex:
        pal.extend(hex_to_rgb(h))
    pal_img = Image.new("P", (1,1))
    pal_img.putpalette(pal * (256 // len(palette_hex)))
    return img.convert("RGB").quantize(
        palette=pal_img,
        dither=Image.NONE
    ).convert("RGBA")

def snap_to_grid(img, px):
    if px <= 1:
        return img
    w, h = img.size
    gw, gh = w // px, h // px
    img = img.resize((gw, gh), Image.NEAREST)
    return img

# ----------------------------
# Commands
# ----------------------------

def cmd_help():
    banner()
    print(
"""Usage:
  pixel.py palette
  pixel.py run <input> <output> [options]

Options:
  --px <n>            pixel grid size (default: 1)
  --palette <name>    palette name
"""
    )

def cmd_run(args):
    if len(args) < 2:
        die("run requires <input> <output>")

    inp = Path(args[0])
    out = Path(args[1])

    px = 1
    palette = None

    i = 2
    while i < len(args):
        if args[i] == "--px":
            px = int(args[i+1]); i += 2
        elif args[i] == "--palette":
            palette = args[i+1]; i += 2
        else:
            die(f"Unknown option: {args[i]}")

    if not inp.exists():
        die(f"Input not found: {inp}")

    img = Image.open(inp).convert("RGBA")
    img = snap_to_grid(img, px)

    pal = get_palette(palette)
    if pal:
        img = quantize(img, pal)

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"Wrote {out}")

# ----------------------------
# Entry
# ----------------------------

def main():
    if len(sys.argv) < 2:
        cmd_help()
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "palette":
        list_palettes()
    elif cmd == "run":
        cmd_run(args)
    else:
        cmd_help()

if __name__ == "__main__":
    main()