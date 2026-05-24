#!/usr/bin/env python3
"""
make_featured.py — Turn ANY image into a clean, uniformly-framed cover.

The Hugo Blox theme crops card/featured images to a fixed ratio, which makes
images of odd aspect ratios look zoomed or badly cropped. This script fixes that
by fitting the WHOLE image (no crop) onto a fixed 16:9 canvas, over a softly
blurred background built from the image itself — so letterboxing never shows as
ugly bars and every card looks consistent.

Usage:
    python tools/make_featured.py <input> [output]
    # If <output> is omitted, the input file is overwritten.

Examples:
    python tools/make_featured.py photo.jpg content/fr/event/talk/featured.jpg
    python tools/make_featured.py figure.png            # overwrites figure.png

Requires: Pillow  (pip install pillow)
"""
import sys, os
from PIL import Image, ImageFilter

TARGET_W, TARGET_H = 1200, 675          # 16:9 — good for cards AND social sharing
INNER = 0.90                            # foreground occupies 90% of the canvas
BG_BLUR = 28                            # background blur radius
BG_DARKEN = 0.82                        # multiply background brightness (0-1)

def cover_resize(im, w, h):
    """Scale + center-crop to exactly fill (w, h)."""
    src_w, src_h = im.size
    scale = max(w / src_w, h / src_h)
    nw, nh = int(src_w * scale + 0.5), int(src_h * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    return im.crop((left, top, left + w, top + h))

def contain_resize(im, w, h):
    """Scale to fit entirely inside (w, h), keeping aspect ratio."""
    src_w, src_h = im.size
    scale = min(w / src_w, h / src_h)
    nw, nh = max(1, int(src_w * scale + 0.5)), max(1, int(src_h * scale + 0.5))
    return im.resize((nw, nh), Image.LANCZOS)

def make(inp, outp):
    im = Image.open(inp).convert("RGB")
    # Background: blurred, slightly darkened cover of the image
    bg = cover_resize(im, TARGET_W, TARGET_H).filter(ImageFilter.GaussianBlur(BG_BLUR))
    bg = Image.eval(bg, lambda p: int(p * BG_DARKEN))
    # Foreground: the full image, fit inside the inner safe area
    fg = contain_resize(im, int(TARGET_W * INNER), int(TARGET_H * INNER))
    canvas = bg.copy()
    x = (TARGET_W - fg.width) // 2
    y = (TARGET_H - fg.height) // 2
    canvas.paste(fg, (x, y))
    ext = os.path.splitext(outp)[1].lower()
    if ext in (".jpg", ".jpeg"):
        canvas.save(outp, "JPEG", quality=88, optimize=True)
    else:
        canvas.save(outp, "PNG", optimize=True)
    print(f"  {inp}  ->  {outp}  ({TARGET_W}x{TARGET_H})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src
    make(src, dst)
