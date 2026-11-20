#!/usr/bin/env python3
"""Draw the GTA 6 launch-week meme for make.fun bounty gta6-meme-x-01.

A loading bar for GTA VI in Leonida at sunset: thirteen years of waiting,
one bar, finally at 100%. The make.fun ghost watches from the beach.
Pure Pillow, deterministic output, 1024x1024 PNG.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (15, 21, 48)
MAGENTA = (230, 0, 126)
GOLD = (255, 210, 62)
GREEN = (0, 194, 106)
SAND = (232, 201, 138)
SEA = (31, 138, 156)
PURPLE = (45, 27, 78)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def fit_font(draw, text, start, max_width):
    """Largest bold size at which text fits max_width."""
    size = start
    while size > 10:
        f = font(size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_width:
            return f
        size -= 2
    return font(10)


def text_center(draw, cx, y, text, fill, size, max_width=980,
                stroke=0, stroke_fill=(0, 0, 0)):
    f = fit_font(draw, text, size, max_width)
    box = draw.textbbox((0, 0), text, font=f, stroke_width=stroke)
    w = box[2] - box[0]
    draw.text((cx - w / 2 - box[0], y), text, font=f, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    return f


def vgrad(draw, top, bottom, stops):
    """Vertical gradient over y in [top, bottom] through color stops."""
    n = bottom - top
    for y in range(top, bottom):
        t = y / max(n - 1, 1) * (len(stops) - 1)
        i = min(int(t), len(stops) - 2)
        frac = t - i
        c = tuple(int(stops[i][k] + (stops[i + 1][k] - stops[i][k]) * frac)
                  for k in range(3))
        draw.line([(0, y), (W, y)], fill=c)


def cloud(draw, cx, cy, s):
    """A puffy white cloud from overlapping ellipses."""
    for dx, dy, rx, ry in [(-70, 10, 70, 42), (0, -18, 78, 52),
                           (70, 12, 66, 40), (-30, 22, 60, 34),
                           (35, 24, 62, 34)]:
        draw.ellipse([cx + dx * s - rx * s, cy + dy * s - ry * s,
                      cx + dx * s + rx * s, cy + dy * s + ry * s],
                     fill=(255, 255, 255))


def skyline(draw):
    """Dark purple Vice City towers with lit windows, behind the panel."""
    import random
    rnd = random.Random(6)
    x = -10
    while x < W:
        bw = rnd.randint(60, 110)
        bh = rnd.randint(90, 230)
        top = 640 - bh
        draw.rectangle([x, top, x + bw, 640], fill=PURPLE)
        for wy in range(top + 18, 630, 34):
            for wx in range(x + 12, x + bw - 10, 30):
                if rnd.random() < 0.45:
                    draw.rectangle([wx, wy, wx + 12, wy + 16],
                                   fill=(255, 214, 92))
        x += bw + rnd.randint(4, 18)


def palm(draw, bx, by, s, flip):
    """A simple palm silhouette: curved trunk and radiating fronds."""
    trunk_top = (bx - 18 * s * flip, by - 150 * s)
    draw.line([(bx, by), trunk_top], fill=(29, 77, 43), width=int(14 * s))
    for ang in (-150, -120, -95, -70, -40, -15):
        rad = math.radians(ang if not flip else 180 - ang)
        ex = trunk_top[0] + math.cos(rad) * 120 * s
        ey = trunk_top[1] + math.sin(rad) * 70 * s + 46 * s
        draw.line([trunk_top, (ex, ey)], fill=(29, 77, 43),
                  width=int(11 * s))
        mx = (trunk_top[0] + ex) / 2
        my = (trunk_top[1] + ey) / 2 + 26 * s
        draw.line([trunk_top, (mx, my)], fill=(29, 77, 43),
                  width=int(7 * s))


def sparkle(draw, cx, cy, r, fill):
    """A four-pointed sparkle star."""
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rad = r if i % 2 == 0 else r * 0.22
        pts.append((cx + math.cos(ang) * rad, cy - math.sin(ang) * rad))
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r, fill):
    """A five-pointed star."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
    draw.polygon(pts, fill=fill)


def ghost_points(cx, cy, w, h):
    """Outline points of the make.fun ghost: domed top, wavy base.

    cy is the dome centre; the total height is h, so the base sits at
    cy + h - w/2 (the dome alone is w/2 tall).
    """
    base = cy + h - w / 2
    pts = []
    rx, ry = w / 2, w / 2
    for deg in range(180, -1, -6):
        rad = math.radians(deg)
        pts.append((cx + math.cos(rad) * rx, cy - ry + ry
                    - math.sin(rad) * ry))
    # sides down to the wavy base
    pts.append((cx + rx, base - 46))
    pts.append((cx + rx * 0.5, base))
    pts.append((cx, base - 46))
    pts.append((cx - rx * 0.5, base))
    pts.append((cx - rx, base - 46))
    return pts


def ghost(draw, cx, top, w, h):
    """The make.fun ghost: white body, thick black outline, sparkle eyes,
    small round hand holding a magenta star coin."""
    cy = top + w / 2
    body = ghost_points(cx, cy, w, h)
    # black outline: same shape, slightly larger, drawn behind
    big = [(cx + (x - cx) * 1.06, cy + (y - cy) * 1.05) for x, y in body]
    draw.polygon(big, fill=(0, 0, 0))
    draw.polygon(body, fill=(255, 255, 255))
    sparkle(draw, cx - 42, top + 92, 30, (0, 0, 0))
    sparkle(draw, cx + 42, top + 92, 30, (0, 0, 0))
    # small round hand + magenta coin with a white star
    draw.ellipse([cx + 88, top + 158, cx + 116, top + 186],
                 fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    draw.ellipse([cx + 96, top + 148, cx + 172, top + 224],
                 fill=MAGENTA, outline=(0, 0, 0), width=4)
    star5(draw, cx + 134, top + 186, 26, (255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), (255, 138, 61))
    d = ImageDraw.Draw(img)

    # --- sky: orange sunset fading to pink ---
    vgrad(d, 0, 560, [(255, 138, 61), (255, 107, 107), (232, 93, 158)])

    # --- sun peeking above the panel ---
    d.ellipse([402, 220, 622, 440], fill=(255, 223, 94))
    d.ellipse([422, 240, 602, 420], fill=(255, 210, 62))

    # --- clouds ---
    cloud(d, 170, 185, 0.85)
    cloud(d, 760, 215, 0.9)
    cloud(d, 330, 305, 0.7)
    cloud(d, 880, 140, 0.6)

    # --- skyline, sea, sand ---
    skyline(d)
    d.rectangle([0, 640, W, 722], fill=SEA)
    for y in (662, 688, 712):
        for x in range(20, W, 90):
            d.line([(x, y), (x + 46, y)], fill=(127, 212, 212), width=4)
    d.rectangle([0, 722, W, 960], fill=SAND)

    # --- palms at the edges ---
    palm(d, 78, 770, 1.3, flip=False)
    palm(d, 946, 775, 1.3, flip=True)

    # --- headline ---
    text_center(d, W // 2, 24, "13 YEARS WAITING", (255, 255, 255),
                72, max_width=940, stroke=4)
    text_center(d, W // 2, 104, "FOR THIS BAR TO MOVE", GOLD,
                72, max_width=940, stroke=4)

    # --- central panel: navy, magenta top strip, white rim ---
    d.rounded_rectangle([100, 330, 924, 640], radius=28, fill=MAGENTA)
    d.rectangle([100, 356, 924, 640], fill=NAVY)
    d.rounded_rectangle([100, 330, 924, 640], radius=28,
                        outline=(255, 255, 255), width=4)
    text_center(d, W // 2, 372, "GTA VI", (255, 255, 255), 140,
                max_width=780)
    # letterspaced LEONIDA
    word = "L E O N I D A"
    text_center(d, W // 2, 500, word, GOLD, 40, max_width=780)
    # --- loading bar, full at last ---
    d.rounded_rectangle([190, 556, 834, 606], radius=24, fill=GREEN,
                        outline=(255, 255, 255), width=3)
    text_center(d, W // 2, 564, "100% — FINALLY OUT", (255, 255, 255),
                36, max_width=600, stroke=3)

    # --- make.fun ghost on the sand, bottom right ---
    ghost(d, 790, 690, 200, 240)

    # --- bottom magenta band ---
    d.rectangle([0, 960, W, H], fill=MAGENTA)
    text_center(d, W // 2, 978, "make.fun • MY AGENT EARNS WHILE I PLAY",
                (255, 255, 255), 36, max_width=990, stroke=2)

    out = os.path.join(HERE, "meme.png")
    img.save(out, "PNG")
    print(f"wrote {out} {W}x{H}")


if __name__ == "__main__":
    main()
