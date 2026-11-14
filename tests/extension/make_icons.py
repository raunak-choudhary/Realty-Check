"""Regenerate extension/icons/*.png: a plain check mark in a circle, accent blue on white."""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[2] / "extension" / "icons"
BLUE = (37, 99, 235, 255)


def icon(size: int) -> Image.Image:
    s = 8  # supersample
    n = size * s
    im = Image.new("RGBA", (n, n), (255, 255, 255, 255))
    d = ImageDraw.Draw(im)
    w = max(int(n * 0.085), 2)
    m = n * 0.09
    d.ellipse([m, m, n - m, n - m], outline=BLUE, width=w)
    pts = [(n * 0.32, n * 0.52), (n * 0.45, n * 0.645), (n * 0.69, n * 0.38)]
    d.line(pts, fill=BLUE, width=int(w * 1.1), joint="curve")
    for x, y in (pts[0], pts[-1]):
        r = w * 0.55
        d.ellipse([x - r, y - r, x + r, y + r], fill=BLUE)
    return im.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for sz in (16, 32, 48, 128):
        icon(sz).save(OUT / f"icon{sz}.png")
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))
