"""
Turn a colour logo into a flat one-colour version with a transparent background.

Every pixel that differs from the background becomes the target colour; the
background itself becomes transparent.
That's a true knockout rather than a flatten, so shapes drawn in white inside a
mark survive: Crown's crown, Homeflow's chevron, Reload's arrow.

Logos with a gradient or a photograph in them will come out as a solid blob.
If the client's brand kit has an official reversed or mono version, use that.

Usage:
    python3 scripts/logos.py

Point SOURCES at the colour originals first. Output lands in assets/img/logos/.
"""

from PIL import Image
import numpy as np
import os

OUT = "assets/img/logos"
TARGET_H = 200          # well above display size, so fine detail survives
BOOST = 1.8             # pushes mid-greys to fully opaque, keeps antialiasing soft

CREAM = (255, 255, 255)   # for the dark Selected Work cards
INK = (19, 23, 17)        # for the cream Where I've worked row

# name -> (path to colour original, output colour)
SOURCES = {
    "crown-white":      ("originals/crown.png",       CREAM),
    "startle-white":    ("originals/startle.png",     CREAM),
    "homeflow-white":   ("originals/homeflow.png",    CREAM),
    "storefeeder-white": ("originals/storefeeder.png", CREAM),
    "ami-white":        ("originals/ami.png",         CREAM),
    "rocket-saas-ink":  ("originals/rocket-saas.png", INK),
    "andus-ink":        ("originals/andus.png",       INK),
    "famly-ink":        ("originals/famly.png",       INK),
    "man-ink":          ("originals/man.png",         INK),
    "canstar-ink":      ("originals/canstar.png",     INK),
    "reload-ink":       ("originals/reload.png",      INK),
}


def monoise(src, name, rgb_out):
    im = Image.open(src).convert("RGBA")

    # Flatten onto white first. Some logos arrive on a transparent background,
    # and without this the corner sample below reads that as black: dark text
    # then scores as "nearly background" and comes out half transparent, while
    # white knockouts score as ink and fill in solid.
    im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im)

    a = np.array(im).astype(np.float32)
    rgb, alpha0 = a[..., :3], a[..., 3:4] / 255.0

    # Background is sampled from the corners rather than assumed to be white,
    # so a logo supplied on grey (MAN) keys out as cleanly as one on white.
    corners = np.stack([rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]])
    bg = np.median(corners, axis=0)

    dist = np.abs(rgb - bg).max(axis=2) / 255.0
    coverage = dist * alpha0[..., 0]
    alpha = np.clip(coverage * BOOST, 0, 1)

    out = np.zeros_like(a)
    out[..., 0], out[..., 1], out[..., 2] = rgb_out
    out[..., 3] = alpha * 255.0

    w = Image.fromarray(out.astype(np.uint8), "RGBA")
    w = w.crop(w.getbbox())              # trim the surrounding white
    r = TARGET_H / w.height
    w = w.resize((max(1, round(w.width * r)), TARGET_H), Image.LANCZOS)
    w.save(f"{OUT}/{name}.png")
    print(f"{name:20} {w.width:4}x{w.height}  aspect {w.width / w.height:.2f}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, (path, colour) in SOURCES.items():
        if os.path.exists(path):
            monoise(path, name, colour)
        else:
            print(f"{name:20} skipped, no file at {path}")
