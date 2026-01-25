#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from PIL import Image

VERSION = "0.2"

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
    if not PALETTES_DIR.exists():
        return palettes

    for path in PALETTES_DIR.rglob("*.json"):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                name = data.get("name") or path.stem
                colors = [c["hex"] for c in data.get("colors", []) if "hex" in c]
                if colors:
                    palettes[name] = colors
        except Exception:
            pass

    return palettes


PALETTES = load_palettes()


def list_palettes():
    if not PALETTES:
        print("No palettes found.")
        return
    for name, colors in sorted(PALETTES.items()):
        print(f"{name:20} {len(colors)} colors")


def check_palette(name):
    if name not in PALETTES:
        die(f"Unknown palette: {name}")
    print(f"Palette: {name}")
    for c in PALETTES[name]:
        print(f"  {c}")


def get_palette(name, max_colors=None):
    if name is None or name == "auto":
        return None
    if name not in PALETTES:
        die(f"Unknown palette: {name}")
    cols = PALETTES[name]
    return cols[:max_colors] if max_colors else cols


# ----------------------------
# Image processing
# ----------------------------

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def quantize_to_palette(img, palette_hex):
    palette_rgb = []
    for h in palette_hex:
        palette_rgb.extend(hex_to_rgb(h))

    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(palette_rgb * (256 // len(palette_hex)))

    return (
        img.convert("RGB")
        .quantize(palette=pal_img, dither=Image.NONE)
        .convert("RGBA")
    )


def snap_to_grid(img, px):
    if px <= 1:
        return img
    w, h = img.size
    w2, h2 = max(1, w // px), max(1, h // px)
    small = img.resize((w2, h2), Image.NEAREST)
    return small.resize((w2 * px, h2 * px), Image.NEAREST)


# ----------------------------
# Commands
# ----------------------------

def cmd_help():
    banner()
    print(
"""Usage:
  pixel help
  pixel palette
  pixel check <palette>
  pixel run <input> <output> [options]
  pixel batch <input-dir> <output-dir> [options]

Options:
  --palette <name>    Palette name (default: auto)
  --colors <n>        Limit palette colors
  --px <n>            Pixel size / grid (default: 1)
"""
    )


def cmd_run(args):
    if len(args) < 2:
        die("run requires <input> <output>")

    inp = Path(args[0])
    out = Path(args[1])

    palette = None
    colors = None
    px = 1

    i = 2
    while i < len(args):
        if args[i] == "--palette":
            palette = args[i + 1]
            i += 2
        elif args[i] == "--colors":
            colors = int(args[i + 1])
            i += 2
        elif args[i] == "--px":
            px = int(args[i + 1])
            i += 2
        else:
            die(f"Unknown option: {args[i]}")

    if not inp.exists():
        die(f"Input not found: {inp}")

    img = Image.open(inp).convert("RGBA")
    img = snap_to_grid(img, px)

    pal = get_palette(palette, colors)
    if pal:
        img = quantize_to_palette(img, pal)

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"Wrote {out}")


def cmd_batch(args):
    if len(args) < 2:
        die("batch requires <input-dir> <output-dir>")

    inp_dir = Path(args[0])
    out_dir = Path(args[1])

    if not inp_dir.exists() or not inp_dir.is_dir():
        die(f"Input dir not found: {inp_dir}")

    palette = None
    colors = None
    px = 1

    i = 2
    while i < len(args):
        if args[i] == "--palette":
            palette = args[i + 1]
            i += 2
        elif args[i] == "--colors":
            colors = int(args[i + 1])
            i += 2
        elif args[i] == "--px":
            px = int(args[i + 1])
            i += 2
        else:
            die(f"Unknown option: {args[i]}")

    processed = 0
    skipped = 0

    for f in sorted(inp_dir.iterdir()):
        if not f.is_file():
            continue
        try:
            cmd_run([
                str(f),
                str(out_dir / f.name),
                *(["--palette", palette] if palette else []),
                *(["--colors", str(colors)] if colors else []),
                *(["--px", str(px)] if px else [])
            ])
            processed += 1
        except Exception as e:
            print(f"Skip {f.name}: {e}")
            skipped += 1

    print(f"Batch complete: {processed} processed, {skipped} skipped")


# ----------------------------
# Main
# ----------------------------

def main():
    if len(sys.argv) < 2:
        cmd_help()
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "help":
        cmd_help()
    elif cmd == "palette":
        list_palettes()
    elif cmd == "check":
        if not args:
            die("check requires <palette>")
        check_palette(args[0])
    elif cmd == "run":
        cmd_run(args)
    elif cmd == "batch":
        cmd_batch(args)
    else:
        banner()
        die(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()