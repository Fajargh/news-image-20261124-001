#!/usr/bin/env python3
"""THE WORLD TODAY - Tuesday, 24 November 2026.

Draws a one-page newspaper front page summing up the world's news of
24 November 2026 and writes it to /output/entry.png (1024x1024, PNG).

Pure procedural drawing with Pillow; no network, no randomness, no
timestamps, so two runs produce byte-identical output.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (18, 64, 120)
GREEN = (22, 110, 60)
GREY = (90, 90, 90)
LIGHT_GREY = (210, 205, 190)
GOLD = (176, 132, 30)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, max_w, lines, fnt, fill=INK, leading=1.28):
    """Draw wrapped lines starting at (x, y); return y after the block."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, x, y, w, width=2, fill=INK):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


def chip_icon(draw, x, y, s):
    """A green computer chip, for the Nvidia lead story."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=GREEN)
    draw.rounded_rectangle([x + s // 4, y + s // 4, x + 3 * s // 4, y + 3 * s // 4],
                           radius=4, outline=(255, 255, 255), width=3)
    for i in range(3):
        px = x + s // 4 + i * s // 4
        draw.line([(px, y - 8), (px, y)], fill=GREEN, width=4)
        draw.line([(px, y + s), (px, y + s + 8)], fill=GREEN, width=4)
        py = y + s // 4 + i * s // 4
        draw.line([(x - 8, py), (x, py)], fill=GREEN, width=4)
        draw.line([(x + s, py), (x + s + 8, py)], fill=GREEN, width=4)
    f = font(SANS_B, s // 6)
    draw.text((x + s // 2, y + s // 2), "+31%", font=f, fill=(255, 255, 255),
              anchor="mm")


def globe_icon(draw, x, y, s):
    """A warming globe, for the COP31 story."""
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 200, 60),
             width=5)
    draw.ellipse([cx + r - 14, cy - r - 2, cx + r + 2, cy - r + 14],
                 fill=(255, 120, 40))
    draw.line([(cx - r + 6, cy), (cx + r - 6, cy)], fill=(255, 255, 255), width=2)
    draw.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 270, 90,
             fill=(255, 255, 255), width=2)


def ship_icon(draw, x, y, s):
    """A warship at sea, for the Libya strike story."""
    draw.rectangle([x, y + s - 14, x + s, y + s - 8], fill=(120, 170, 210))
    draw.polygon([(x + 6, y + s - 14), (x + s - 6, y + s - 14),
                  (x + s - 18, y + s - 26), (x + 18, y + s - 26)],
                 fill=(60, 60, 70))
    draw.rectangle([x + s // 2 - 4, y + 6, x + s // 2 + 4, y + s - 26],
                   fill=(60, 60, 70))
    draw.polygon([(x + s // 2 + 4, y + 8), (x + s // 2 + 22, y + 18),
                  (x + s // 2 + 4, y + 20)], fill=RED)


def radar_icon(draw, x, y, s):
    """Radar sweep, for the NATO / Poland story."""
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    draw.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                 outline=BLUE, width=2)
    draw.line([(cx, cy), (cx + r - 4, cy - r + 10)], fill=RED, width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=1)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=BLUE, width=1)


def flame_icon(draw, x, y, s):
    """A flame, for the Indonesia factory fire story."""
    draw.polygon([(x + s // 2, y + 2), (x + s - 8, y + s // 2),
                  (x + s - 2, y + s - 8), (x + s // 2 + 8, y + s - 14),
                  (x + s // 2 - 2, y + s - 4), (x + 10, y + s - 10),
                  (x + 4, y + s // 2)], fill=(230, 90, 20))
    draw.polygon([(x + s // 2, y + s // 2), (x + s - 14, y + s - 8),
                  (x + s // 2, y + s - 4), (x + 14, y + s - 8)],
                 fill=(255, 200, 60))


def chess_icon(draw, x, y, s):
    """A chessboard, for the World Chess Championship story."""
    cell = s // 4
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                draw.rectangle([x + c * cell, y + r * cell,
                                x + (c + 1) * cell, y + (r + 1) * cell],
                               fill=INK)
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=3)
    f = font(SERIF_B, s // 2)
    draw.text((x + s // 2, y + s // 2), "K", font=f, fill=RED, anchor="mm")


STORIES = [
    # (kicker, headline, deck, icon)
    ("CLIMATE  •  TURKEY", "COP31 talks collapse with no deal",
     "UN climate summit ends without agreement; talks may resume next year.",
     globe_icon),
    ("CONFLICT  •  LIBYA", "Ukraine says it sank a Russian warship off Libya",
     "Kyiv claims drones destroyed a corvette in Benghazi port.",
     ship_icon),
    ("SECURITY  •  POLAND", "NATO sends early-warning jets to Poland",
     "Alliance to deploy AWACS jets after missiles landed on Polish soil.",
     radar_icon),
    ("DISASTER  •  INDONESIA", "Factory fire in Indonesia kills at least 24",
     "Blaze at a candy factory leaves dozens missing as rescuers search.",
     flame_icon),
    ("SPORT  •  GENEVA", "Chess crown on the line as Gukesh defends title",
     "World championship begins in Geneva: Gukesh faces Sindarov.",
     chess_icon),
]

IN_BRIEF = ("IN BRIEF  —  Israeli strikes kill three in Gaza, including a UN "
            "worker  •  US sanctions dozens over Iran's shadow banking  •  "
            "Trump pauses Iowa explosives detonation  •  India–New Zealand "
            "Test ends in a draw  •  CrowdStrike agrees to buy Zscaler")


def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([4, 4, W - 5, H - 5], outline=INK, width=3)

    # ---- Masthead ----
    title_f = font(SERIF_B, 62)
    draw.text((W // 2, 78), "THE WORLD TODAY", font=title_f, fill=INK,
              anchor="mm")
    rule(draw, MARGIN, 118, W - 2 * MARGIN, width=3)
    date_f = font(SANS_B, 24)
    draw.text((W // 2, 142), "TUESDAY, 24 NOVEMBER 2026", font=date_f,
              fill=RED, anchor="mm")
    sub_f = font(SANS, 17)
    draw.text((W // 2, 168), "THE WORLD'S NEWS IN ONE PAGE  •  SIX STORIES THAT DEFINED THE DAY",
              font=sub_f, fill=GREY, anchor="mm")
    rule(draw, MARGIN, 188, W - 2 * MARGIN, width=2)

    # ---- Lead story: Nvidia ----
    y = 206
    kick_f = font(SANS_B, 19)
    draw.text((MARGIN, y), "TECHNOLOGY  •  BUSINESS  —  LEAD STORY",
              font=kick_f, fill=RED)
    y += 30
    head_f = font(SERIF_B, 40)
    lead_head = "Huang returns: Nvidia reinstates its chief as shares surge 31%"
    y = draw_text_block(draw, MARGIN, y, 640,
                        wrap(draw, lead_head, head_f, 640), head_f, leading=1.12)
    y += 6
    deck_f = font(SERIF, 21)
    lead_deck = ("The board brings Jensen Huang back as chief executive after an "
                 "inquiry into alleged affairs — and the chipmaker's value climbs "
                 "by almost $1 trillion in a single day.")
    y = draw_text_block(draw, MARGIN, y, 640,
                        wrap(draw, lead_deck, deck_f, 640), deck_f, leading=1.3)
    chip_icon(draw, 760, 250, 150)
    draw.text((835, 420), "NVDA +31% IN A DAY", font=font(SANS_B, 16),
              fill=GREEN, anchor="mm")

    rule(draw, MARGIN, 452, W - 2 * MARGIN, width=2)

    # ---- Five more stories, two columns ----
    col_w = (W - 2 * MARGIN - 28) // 2
    xs = [MARGIN, MARGIN + col_w + 28]
    # left column: stories 0, 1, 2 ; right column: stories 3, 4
    columns = [[STORIES[0], STORIES[1], STORIES[2]],
               [STORIES[3], STORIES[4]]]
    story_h = 126
    for ci, col in enumerate(columns):
        cy = 466
        for si, (kicker, headline, deck, icon) in enumerate(col):
            icon(draw, xs[ci], cy + 4, 64)
            tx = xs[ci] + 78
            draw.text((tx, cy), kicker, font=font(SANS_B, 15), fill=RED)
            hf = font(SERIF_B, 22)
            lines = wrap(draw, headline, hf, col_w - 78)
            ny = draw_text_block(draw, tx, cy + 22, col_w - 78, lines, hf,
                                 leading=1.08)
            df = font(SANS, 15)
            dlines = wrap(draw, deck, df, col_w - 78)
            draw_text_block(draw, tx, ny + 4, col_w - 78, dlines, df,
                            fill=(40, 40, 40), leading=1.25)
            cy += story_h
            if si < len(col) - 1:
                rule(draw, xs[ci], cy - 8, col_w, width=1, fill=LIGHT_GREY)

    # ---- In brief strip ----
    rule(draw, MARGIN, 852, W - 2 * MARGIN, width=2)
    brief_f = font(SANS, 17)
    blines = wrap(draw, IN_BRIEF, brief_f, W - 2 * MARGIN)
    by = 866
    for line in blines:
        draw.text((MARGIN, by), line, font=brief_f, fill=INK)
        by += 24
    rule(draw, MARGIN, 962, W - 2 * MARGIN, width=2)
    foot_f = font(SANS, 14)
    draw.text((W // 2, 980),
              "Sources: Reuters, BBC, The Times of India  •  Events of Tuesday, 24 November 2026",
              font=foot_f, fill=GREY, anchor="mm")
    return img


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        probe = os.path.join(out_dir, ".write-test")
        with open(probe, "w") as fh:
            fh.write("ok")
        os.remove(probe)
    except OSError:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
        os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def validate(path):
    """Guard: re-open the written file and verify it is a whole, legal PNG.

    Checks the PNG signature, dimensions, file size, and that a fresh
    in-memory render produces byte-identical output (determinism).
    """
    import hashlib
    import io

    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("validation failed: not a PNG file")
    if len(data) > 1048576:
        raise SystemExit(f"validation failed: image too large: {len(data)} bytes")
    with Image.open(io.BytesIO(data)) as im:
        im.load()
        if im.size != (1024, 1024):
            raise SystemExit(f"validation failed: bad dimensions: {im.size}")
        if im.format != "PNG":
            raise SystemExit(f"validation failed: bad format: {im.format}")
    buf = io.BytesIO()
    build_image().save(buf, format="PNG", optimize=True)
    if hashlib.sha256(buf.getvalue()).hexdigest() != hashlib.sha256(data).hexdigest():
        raise SystemExit("validation failed: output is not deterministic")
    return len(data)


def main():
    img = build_image()
    path = output_path()
    img.save(path, format="PNG", optimize=True)
    size = validate(path)
    print(f"wrote {path} ({img.size[0]}x{img.size[1]}, {size} bytes)")


if __name__ == "__main__":
    main()
