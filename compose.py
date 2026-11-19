#!/usr/bin/env python3
"""Build the news-image-20261118 v3 front page (entry.png).

Splash-style broadsheet for Wednesday 18 November 2026. One dominant
lead photo, a huge splash headline, short labels only (no dense body
copy, so it stays legible at ~300 px wide), two larger secondary
photos, and a market strip. Photorealistic photos live in assets/.

Run: python3 compose.py  -> writes entry.png next to this file.
Only the standard library and Pillow are used (build-time only;
the submitted entrypoint main.py is a stdlib-only copy program).
"""
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (85, 85, 85)
LIGHT_GREY = (170, 170, 170)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
NOTO_DIR = "/usr/share/fonts/truetype/noto"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
DISPLAY_BLACK = os.path.join(NOTO_DIR, "NotoSerifDisplay-Black.ttf")
DISPLAY_BOLD = os.path.join(NOTO_DIR, "NotoSerifDisplay-Bold.ttf")
DISPLAY_ITALIC = os.path.join(NOTO_DIR, "NotoSerifDisplay-Italic.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_text(draw, text, fnt, max_w):
    """Shrink font until text fits max_w; return (font, width)."""
    size = fnt.size
    while size > 10:
        f = ImageFont.truetype(fnt.path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f, draw.textlength(text, font=f)
        size -= 2
    f = ImageFont.truetype(fnt.path, 10)
    return f, draw.textlength(text, font=f)


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover(im, tw, th, cy=0.5):
    """Center-crop image to fill tw x th (cy = vertical centre 0..1)."""
    return ImageOps.fit(im, (tw, th), Image.LANCZOS, centering=(0.5, cy))


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    mx = 36                      # side margin
    cw = W - 2 * mx              # content width = 952

    # ---- top rules + masthead -------------------------------------
    d.rectangle([mx, 12, W - mx, 15], fill=INK)
    d.rectangle([mx, 18, W - mx, 20], fill=RED)
    mast = font(DISPLAY_BLACK, 66)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 26), title, font=mast, fill=INK)
    # dateline strip
    dl = font(SANS_BOLD, 15)
    d.text((mx, 102), "WEDNESDAY, 18 NOVEMBER 2026", font=dl, fill=INK)
    mid = "LATE CITY EDITION"
    mw = d.textlength(mid, font=dl)
    d.text(((W - mw) / 2, 102), mid, font=dl, fill=RED)
    pr = "PRICE $2.50"
    pw = d.textlength(pr, font=dl)
    d.text((W - mx - pw, 102), pr, font=dl, fill=INK)
    d.rectangle([mx, 124, W - mx, 127], fill=INK)
    d.rectangle([mx, 130, W - mx, 131], fill=INK)

    # ---- lead photo ------------------------------------------------
    tanker = Image.open(os.path.join(HERE, "assets", "tanker.webp")).convert("RGB")
    lead = cover(tanker, cw, 344, cy=0.42)
    page.paste(lead, (mx, 138))
    d.rectangle([mx, 138, W - mx, 482], outline=INK, width=2)
    cap = font(DISPLAY_ITALIC, 14)
    caption = "A tanker burns in the Gulf after U.S. strikes sank five Iranian tankers. A U.S. warship stands by."
    d.text((mx, 490), caption, font=cap, fill=GREY)

    # ---- splash headline -------------------------------------------
    hl = font(DISPLAY_BLACK, 64)
    d.text((mx, 514), "U.S. SINKS FIVE", font=hl, fill=INK)
    d.text((mx, 584), "IRANIAN TANKERS", font=hl, fill=INK)
    deck = font(DISPLAY_BOLD, 22)
    d.text((mx, 660), "Iran hits back as the Gulf burns \u2014 oil spikes, markets tumble",
           font=deck, fill=RED)
    # standfirst (2 lines, larger type than body copy)
    sf = font(SERIF, 17)
    stand = ("American warships sank five Iranian tankers in the Gulf on "
             "Wednesday, and Tehran answered with strikes of its own. Oil "
             "prices surged and world markets fell as the region braced for more.")
    lines = wrap(d, stand, sf, cw)
    y = 694
    for ln in lines[:3]:
        d.text((mx, y), ln, font=sf, fill=INK)
        y += 22

    # ---- divider ----------------------------------------------------
    d.rectangle([mx, 766, W - mx, 767], fill=INK)

    # ---- secondary stories ------------------------------------------
    col_w = (cw - 20) // 2
    kerch = Image.open(os.path.join(HERE, "assets", "kerch.webp")).convert("RGB")
    gaza = Image.open(os.path.join(HERE, "assets", "gaza.webp")).convert("RGB")
    kimg = cover(kerch, col_w, 132, cy=0.5)
    gimg = cover(gaza, col_w, 132, cy=0.45)
    page.paste(kimg, (mx, 776))
    page.paste(gimg, (mx + col_w + 20, 776))
    d.rectangle([mx, 776, mx + col_w, 908], outline=INK, width=1)
    d.rectangle([mx + col_w + 20, 776, W - mx, 908], outline=INK, width=1)
    sub = font(DISPLAY_BOLD, 25)
    d.text((mx, 914), "KERCH BRIDGE HIT", font=sub, fill=INK)
    d.text((mx + col_w + 20, 914), "GAZA FREEZES", font=sub, fill=INK)
    capf = font(SANS, 13)
    kc = "A blast damages the crossing; traffic halted."
    gc = "Cold claims lives as families shelter in tents."
    d.text((mx, 944), kc, font=capf, fill=GREY)
    d.text((mx + col_w + 20, 944), gc, font=capf, fill=GREY)

    # ---- market strip ------------------------------------------------
    d.rectangle([0, 968, W, 1004], fill=INK)
    mk = font(SANS_BOLD, 17)
    mkt = "MARKETS:   DOW TUMBLES      NASDAQ DOWN 2%      OIL SURGES"
    mw = d.textlength(mkt, font=mk)
    d.text(((W - mw) / 2, 978), mkt, font=mk, fill=(255, 255, 255))
    # footer
    ft = font(SANS, 11)
    foot = "THE WORLD TODAY  \u2022  WEDNESDAY 18 NOVEMBER 2026  \u2022  THE DAY IN FULL"
    fw = d.textlength(foot, font=ft)
    d.text(((W - fw) / 2, 1008), foot, font=ft, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "JPEG", quality=90)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
