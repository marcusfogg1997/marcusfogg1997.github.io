"""Rebuild the hero portrait from its original, centred on Marcus.

The photograph as supplied has him left of centre, with noticeably more park
on the right than on the left, which reads as him standing off to one side in
the square frame the hero draws. This takes the widest square window that
centres him, which means trimming the right-hand side, then writes the three
sizes the <picture> element asks for, in WebP and JPEG.

FACE_X is where his face sits across the original, measured from the rendered
page: 0.5 would be dead centre. Everything else follows from it. Re-measure it
if the portrait is ever replaced.

Usage:
    python3 scripts/portrait.py
"""

from PIL import Image
import os

SRC = "originals/marcus-fogg-original.png"
OUT = "assets/img"
STEM = "marcus-fogg"
SIZES = (512, 768, 1024)
FACE_X = 0.432          # measured, not guessed


def build():
    im = Image.open(SRC).convert("RGB")
    w, h = im.size

    # The widest square that puts FACE_X in the middle. Centring him means
    # losing whichever side he sits nearer to, so the window is limited by the
    # shorter of the two gaps either side of him.
    centre = FACE_X * w
    side = min(centre, w - centre, h / 2) * 2
    side = int(side)
    left = int(centre - side / 2)
    top = 0                               # keeps the headroom, trims his chest

    im = im.crop((left, top, left + side, top + side))
    print(f"cropped {w}x{h} to {side}x{side} at x={left}, "
          f"face now at {(centre - left) / side:.1%}")

    os.makedirs(OUT, exist_ok=True)
    for size in SIZES:
        if size > side:
            print(f"  {size}px is an upscale from {side}px, by {size / side:.2f}x")
        r = im.resize((size, size), Image.LANCZOS)
        r.save(f"{OUT}/{STEM}-{size}.jpg", quality=86, optimize=True, progressive=True)
        r.save(f"{OUT}/{STEM}-{size}.webp", quality=82, method=6)
        j = os.path.getsize(f"{OUT}/{STEM}-{size}.jpg")
        wp = os.path.getsize(f"{OUT}/{STEM}-{size}.webp")
        print(f"  {size:4}  jpg {j // 1024:3}KB   webp {wp // 1024:3}KB")


if __name__ == "__main__":
    build()
