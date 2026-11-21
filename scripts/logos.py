"""
Knock the background out of a colour logo and keep the colours.

Every pixel that differs from the background keeps its own colour; the
background itself becomes transparent. That's a true knockout rather than a
flatten, so shapes drawn in white inside a mark survive as holes: Crown's
crown, Homeflow's chevron, Reload's arrow.

One file per brand does all three jobs on the site, via CSS:

    ink      filter: brightness(0) opacity(.92)   cream backgrounds
    white    filter: brightness(0) invert(1)      dark backgrounds
    colour   filter: none                         hover

brightness(0) crushes every channel to zero without touching alpha, so the
result is the same silhouette the old mono files gave, holes and all.

Logos with a gradient or a photograph in them will come out looking muddy once
knocked out. If the client's brand kit has an official reversed or mono
version, use that instead.

Usage:
    python3 scripts/logos.py

Point SOURCES at the colour originals first. Output lands in assets/img/logos/.
"""

from PIL import Image
import numpy as np
import os
import shutil
import subprocess

OUT = "assets/img/logos"
TARGET_H = 200          # well above display size, so fine detail survives
BOOST = 1.8             # pushes mid-greys to fully opaque, keeps antialiasing soft

SOURCES = {
    "crown":       "originals/crown.png",
    "startle":     "originals/startle.png",
    "homeflow":    "originals/homeflow.png",
    "storefeeder": "originals/storefeeder.png",
    "ami":         "originals/ami.png",
    "rocket-saas": "originals/rocket-saas.png",
    "andus":       "originals/andus.png",
    "famly":       "originals/famly.png",
    "man":         "originals/man.png",
    "reload":      "originals/reload.png",
}


def knockout(src, name):
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
    alpha = np.clip(dist * alpha0[..., 0] * BOOST, 0, 1)

    out = np.dstack([rgb, alpha * 255.0])

    w = Image.fromarray(out.astype(np.uint8), "RGBA")
    w = w.crop(w.getbbox())              # trim the surrounding white
    r = TARGET_H / w.height
    w = w.resize((max(1, round(w.width * r)), TARGET_H), Image.LANCZOS)
    dest = f"{OUT}/{name}.png"
    w.save(dest)

    # Flat-colour artwork quantises to a small palette with no visible loss,
    # and these go from roughly 70KB to 20KB. Skipped silently if pngquant
    # isn't installed: pip install pngquant-cli.
    if shutil.which("pngquant"):
        subprocess.run(["pngquant", "--quality", "70-95", "--speed", "1",
                        "--force", "--output", dest, dest], check=True)

    # Mean colour of the solid pixels, and its relative luminance. A logo under
    # about 0.2 will struggle against the near-black Selected work cards, so
    # it's worth knowing before turning the hover fill on there.
    px = np.array(w).astype(np.float32)
    solid = px[..., 3] > 200
    mean = px[..., :3][solid].mean(axis=0) if solid.any() else np.zeros(3)
    lin = np.where(mean / 255 <= 0.04045, (mean / 255) / 12.92,
                   (((mean / 255) + 0.055) / 1.055) ** 2.4)
    lum = float(np.dot(lin, [0.2126, 0.7152, 0.0722]))

    print(f"{name:14} {w.width:4}x{w.height}  aspect {w.width / w.height:.2f}  "
          f"mean #{int(mean[0]):02x}{int(mean[1]):02x}{int(mean[2]):02x}  lum {lum:.3f}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, path in SOURCES.items():
        if os.path.exists(path):
            knockout(path, name)
        else:
            print(f"{name:14} skipped, no file at {path}")
