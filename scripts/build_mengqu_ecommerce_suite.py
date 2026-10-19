#!/usr/bin/env python3
"""
Pixel-Perfect 6-Image E-Commerce Suite for MENGQU Sucking Device (萌趣吸吮器)
Refined with Microsoft YaHei font (zero tofu boxes), custom vector icons,
clean typography, and balanced visual layouts.
"""

import os
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "public" / "images" / "products"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DETAILS_DIR = ROOT_DIR / "public" / "images" / "9rabbit" / "details"
DETAILS_DIR.mkdir(parents=True, exist_ok=True)

BRAIN_DIR = Path(r"C:\Users\admin\.gemini\antigravity\brain\ce49dcba-cdec-4437-9044-20d7b878bc29\.user_uploaded")
IMG_BACK = BRAIN_DIR / "media_1792430879949_9b95141d.png"   # Back view
IMG_FRONT = BRAIN_DIR / "media_1792430880005_f91774d9.png"  # Front & suction view

# Colors
BG_WHITE = (255, 255, 255)
BG_LIGHT_PINK = (255, 245, 247)
ACCENT_PINK = (235, 95, 125)
ACCENT_ROSE = (215, 60, 95)
DARK_TEXT = (25, 30, 45)
MUTED_TEXT = (90, 105, 125)
BORDER_PINK = (248, 205, 215)
SOFT_GRAY = (245, 247, 250)

# Fonts using Microsoft YaHei (renders English, Numbers, and Chinese flawlessly)
def get_font(size: int, bold: bool = False):
    font_name = "msyhbd.ttc" if bold else "msyh.ttc"
    font_path = Path("C:/Windows/Fonts") / font_name
    if not font_path.exists():
        font_path = Path("C:/Windows/Fonts") / ("segoeuib.ttf" if bold else "segoeui.ttf")
    return ImageFont.truetype(str(font_path), size)

def add_header(draw: ImageDraw.ImageDraw, tag: str, title: str, subtitle: str, title_size: int = 35):
    font_tag = get_font(18, bold=True)
    font_title = get_font(title_size, bold=True)
    font_sub = get_font(20, bold=False)

    # Tag pill
    tag_bbox = font_tag.getbbox(tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    pill_w = tag_w + 32
    pill_h = 32
    draw.rounded_rectangle([(60, 45), (60 + pill_w, 45 + pill_h)], radius=16, fill=ACCENT_PINK)
    draw.text((76, 49), tag, fill=(255, 255, 255), font=font_tag)

    # Title & Subtitle
    draw.text((60, 92), title, fill=DARK_TEXT, font=font_title)
    draw.text((60, 145), subtitle, fill=MUTED_TEXT, font=font_sub)

def create_shadow(image_size, shadow_rect, radius=25):
    shadow = Image.new("RGBA", image_size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse(shadow_rect, fill=(215, 175, 185, 65))
    return shadow.filter(ImageFilter.GaussianBlur(radius))

# -------------------------------------------------------------
# IMAGE 1: Flagship Hero Main Image (主图)
# -------------------------------------------------------------
def build_image_1():
    print("[1/6] Building Hero Main Image...")
    canvas = Image.new("RGB", (1200, 1200), BG_WHITE)
    draw = ImageDraw.Draw(canvas)

    add_header(
        draw,
        tag="MENGQU · 萌趣吸吮器",
        title="MENGQU Cat Sonic Air-Pulse Sucking Device",
        subtitle="Discreet Kawaii Sleeping Kitten Clitoral Stimulator with Pink Cloud Stand"
    )

    src_front = Image.open(IMG_FRONT).convert("RGBA")
    prod_w, prod_h = src_front.size
    ratio = 980 / prod_w
    target_size = (int(prod_w * ratio), int(prod_h * ratio))
    resized_prod = src_front.resize(target_size, Image.Resampling.LANCZOS)

    # Ambient shadow
    shadow = create_shadow((1200, 1200), [(140, 930), (1060, 1010)], radius=25)
    canvas.paste(shadow, (0, 0), shadow)

    paste_x = (1200 - target_size[0]) // 2
    paste_y = 170
    canvas.paste(resized_prod, (paste_x, paste_y), resized_prod)

    # 4 Bottom Feature Badges
    badges = [
        ("100% Medical Silicone", "Body-safe, velvety touch"),
        ("3 Speeds × 6 Rhythms", "18 Clitoral pulse modes"),
        ("Whisper Quiet ≤ 50 dB", "Absolute bedroom privacy"),
        ("IPX5 Washable Grade", "Easy soap & water rinse")
    ]
    card_y = 1040
    card_w = 250
    gap = 20
    start_x = (1200 - (4 * card_w + 3 * gap)) // 2

    font_b_title = get_font(18, bold=True)
    font_b_sub = get_font(14, bold=False)

    for i, (b_title, b_sub) in enumerate(badges):
        bx = start_x + i * (card_w + gap)
        draw.rounded_rectangle([(bx, card_y), (bx + card_w, card_y + 110)], radius=14, fill=BG_LIGHT_PINK, outline=BORDER_PINK, width=1)
        # Small circle indicator
        draw.ellipse([(bx + 18, card_y + 24), (bx + 28, card_y + 34)], fill=ACCENT_PINK)
        draw.text((bx + 36, card_y + 18), b_title, fill=DARK_TEXT, font=font_b_title)
        draw.text((bx + 18, card_y + 58), b_sub, fill=MUTED_TEXT, font=font_b_sub)

    return canvas

# -------------------------------------------------------------
# IMAGE 2: Clitoral Sonic Air-Pulse Suction Detail (核心卖点)
# -------------------------------------------------------------
def build_image_2():
    print("[2/6] Building Suction Detail Image...")
    canvas = Image.new("RGB", (1200, 1200), BG_WHITE)
    draw = ImageDraw.Draw(canvas)

    add_header(
        draw,
        tag="SONIC AIR-PULSE TECHNOLOGY",
        title="Contactless Clitoral Sonic Wave Suction",
        subtitle="Delivers 8,000+ Sonic Waves/Min for Non-Numbing Overwhelming Pleasure"
    )

    src = Image.open(IMG_FRONT).convert("RGBA")
    # Resize whole product gracefully to fit left half
    pw, ph = src.size
    ratio = 700 / pw
    resized_prod = src.resize((int(pw * ratio), int(ph * ratio)), Image.Resampling.LANCZOS)

    # Ambient shadow
    shadow = create_shadow((1200, 1200), [(50, 940), (660, 1010)], radius=25)
    canvas.paste(shadow, (0, 0), shadow)
    canvas.paste(resized_prod, (30, 380), resized_prod)

    # Concentric pulse wave rings radiating from suction mouth
    # Mouth position in scaled image: roughly x=500, y=570
    mouth_cx, mouth_cy = 490, 560
    for r in [90, 140, 190, 240, 290]:
        draw.ellipse(
            [(mouth_cx - r, mouth_cy - r), (mouth_cx + r, mouth_cy + r)],
            outline=(245, 125, 150),
            width=2
        )
    # Suction pointer line
    draw.line([(mouth_cx, mouth_cy), (mouth_cx + 80, mouth_cy - 120), (620, mouth_cy - 120)], fill=ACCENT_PINK, width=3)
    draw.ellipse([(mouth_cx - 5, mouth_cy - 5), (mouth_cx + 5, mouth_cy + 5)], fill=ACCENT_PINK)

    # Right 3 Feature Cards
    features = [
        ("Rose-Gold Electroplated Bezel", "Precision metallic vacuum collar creates an airtight pressure seal, ensuring zero air leakage during deep clitoral suction pulses."),
        ("Velvet-Touch Medical Silicone", "Ultra-soft food-grade liquid silicone rim gently wraps around sensitive contours without pinching, chafing, or skin irritation."),
        ("Targeted Sonic Pressure Waves", "Contactless sonic acoustic waves stimulate 8,000+ nerve endings simultaneously, eliminating friction desensitization.")
    ]

    card_x = 640
    card_w = 500
    start_y = 280
    font_num = get_font(26, bold=True)
    font_t = get_font(21, bold=True)
    font_d = get_font(16, bold=False)

    for i, (t, d) in enumerate(features):
        cy = start_y + i * 270
        draw.rounded_rectangle([(card_x, cy), (card_x + card_w, cy + 235)], radius=16, fill=BG_LIGHT_PINK, outline=BORDER_PINK, width=1)
        
        # Number badge
        draw.text((card_x + 24, cy + 22), f"0{i+1}", fill=ACCENT_PINK, font=font_num)
        draw.text((card_x + 72, cy + 26), t, fill=DARK_TEXT, font=font_t)

        # Word wrap text
        words = d.split(" ")
        lines, curr = [], ""
        for w in words:
            if len(curr + " " + w) < 38:
                curr = curr + (" " if curr else "") + w
            else:
                lines.append(curr)
                curr = w
        if curr: lines.append(curr)

        for l_idx, line in enumerate(lines[:4]):
            draw.text((card_x + 24, cy + 78 + l_idx * 32), line, fill=MUTED_TEXT, font=font_d)

    return canvas

# -------------------------------------------------------------
# IMAGE 3: Kawaii Sleeping Kitten & Cloud Dock Aesthetic
# -------------------------------------------------------------
def build_image_3():
    print("[3/6] Building Aesthetic & Cloud Dock Image...")
    canvas = Image.new("RGB", (1200, 1200), BG_WHITE)
    draw = ImageDraw.Draw(canvas)

    add_header(
        draw,
        tag="KAWAII AESTHETIC · DISCREET ART PIECE",
        title="Sleeping Kitten Form with Cloud Display Stand",
        subtitle="Blends Naturally into Bedside Decor with 100% Privacy & Zero Embarrassment"
    )

    src = Image.open(IMG_FRONT).convert("RGBA")
    cat_crop = src.crop((50, 270, 560, 850))
    cat_resized = cat_crop.resize((int(cat_crop.width * 1.5), int(cat_crop.height * 1.5)), Image.Resampling.LANCZOS)

    shadow = create_shadow((1200, 1200), [(60, 990), (740, 1070)], radius=25)
    canvas.paste(shadow, (0, 0), shadow)
    canvas.paste(cat_resized, (30, 280), cat_resized)

    callouts = [
        ("Organic Contoured Cloud Dock", "Custom-sculpted pastel pink cloud stand securely cradles the cat body, elevating the silicone suction mouth hygienically off table surfaces."),
        ("Whimsical Sleeping Silhouette", "Curved closed eyes, sweet whiskers, and soft miniature ears give this wellness device a friendly, comforting aesthetic free of intimidating shapes."),
        ("100% Discreet Bedside Placement", "Disguises as a charming designer desktop figurine or ceramic nightlight. Family, friends, or roommates will never suspect its true intimate function.")
    ]

    card_x = 650
    card_w = 490
    start_y = 280
    font_t = get_font(21, bold=True)
    font_d = get_font(16, bold=False)

    for i, (t, d) in enumerate(callouts):
        cy = start_y + i * 270
        draw.rounded_rectangle([(card_x, cy), (card_x + card_w, cy + 235)], radius=16, fill=BG_LIGHT_PINK, outline=BORDER_PINK, width=1)
        
        draw.ellipse([(card_x + 22, cy + 28), (card_x + 34, cy + 40)], fill=ACCENT_PINK)
        draw.text((card_x + 44, cy + 22), t, fill=DARK_TEXT, font=font_t)

        words = d.split(" ")
        lines, curr = [], ""
        for w in words:
            if len(curr + " " + w) < 38:
                curr = curr + (" " if curr else "") + w
            else:
                lines.append(curr)
                curr = w
        if curr: lines.append(curr)

        for l_idx, line in enumerate(lines[:4]):
            draw.text((card_x + 24, cy + 78 + l_idx * 32), line, fill=MUTED_TEXT, font=font_d)

    return canvas

# -------------------------------------------------------------
# IMAGE 4: Cat Paw Control & 3 Intensities x 6 Frequencies
# -------------------------------------------------------------
def build_image_4():
    print("[4/6] Building Modes & Control Image...")
    canvas = Image.new("RGB", (1200, 1200), BG_WHITE)
    draw = ImageDraw.Draw(canvas)

    add_header(
        draw,
        tag="TACTILE PAW CONTROL · 18 MODES",
        title="Intelligent Cat Paw Touch & Dual-Phase Rhythms",
        subtitle="3 Suction Intensities × 6 Pulsing Frequencies for Infinite Tailored Orgasms"
    )

    src_back = Image.open(IMG_BACK).convert("RGBA")
    back_crop = src_back.crop((140, 220, 880, 960))
    back_resized = back_crop.resize((int(back_crop.width * 0.95), int(back_crop.height * 0.95)), Image.Resampling.LANCZOS)

    shadow = create_shadow((1200, 1200), [(60, 960), (660, 1030)], radius=25)
    canvas.paste(shadow, (0, 0), shadow)
    canvas.paste(back_resized, (30, 280), back_resized)

    # Pointer line to Paw Button
    paw_x, paw_y = 380, 480
    draw.line([(paw_x, paw_y), (paw_x + 120, paw_y - 60), (600, paw_y - 60)], fill=ACCENT_PINK, width=3)
    draw.ellipse([(paw_x - 5, paw_y - 5), (paw_x + 5, paw_y + 5)], fill=ACCENT_PINK)

    card_x = 640
    card_w = 510

    # Block 1: Button Logic
    draw.rounded_rectangle([(card_x, 260), (card_x + card_w, 480)], radius=16, fill=BG_LIGHT_PINK, outline=BORDER_PINK, width=1)
    draw.text((card_x + 24, 275), "One-Touch Paw Button Logic", fill=DARK_TEXT, font=get_font(22, bold=True))
    draw.text((card_x + 24, 320), "• 1.5s Long Press: Power ON / OFF (Tactile vibration alert)", fill=MUTED_TEXT, font=get_font(16))
    draw.text((card_x + 24, 365), "• Single Click: Cycle forward through 6 pulse rhythms", fill=MUTED_TEXT, font=get_font(16))
    draw.text((card_x + 24, 410), "• Smart Memory: Automatically resumes your favorite mode", fill=MUTED_TEXT, font=get_font(16))

    # Block 2: 3 Intensities
    draw.rounded_rectangle([(card_x, 500), (card_x + card_w, 760)], radius=16, fill=(255, 255, 255), outline=BORDER_PINK, width=1)
    draw.text((card_x + 24, 515), "3 Suction Intensity Levels", fill=DARK_TEXT, font=get_font(22, bold=True))
    
    levels = [
        ("Level 01 · Gentle Teasing", "Soft, gentle micro-vacuum fluttering for sensitive foreplay"),
        ("Level 02 · Surging Pulse", "Medium rhythmic suction waves accelerating pelvic blood flow"),
        ("Level 03 · Deep Climax", "Maximum vacuum force triggering involuntary vaginal climax")
    ]
    for idx, (lt, ld) in enumerate(levels):
        draw.text((card_x + 24, 560 + idx * 60), lt, fill=ACCENT_PINK, font=get_font(17, bold=True))
        draw.text((card_x + 24, 588 + idx * 60), ld, fill=MUTED_TEXT, font=get_font(14))

    # Block 3: 6 Wave Frequencies
    draw.rounded_rectangle([(card_x, 780), (card_x + card_w, 1070)], radius=16, fill=BG_LIGHT_PINK, outline=BORDER_PINK, width=1)
    draw.text((card_x + 24, 795), "6 Dynamic Pulsing Frequencies", fill=DARK_TEXT, font=get_font(22, bold=True))
    
    freqs = [
        "1. Constant Stream — Continuous steady acoustic vacuum",
        "2. Escalating Wave — Gradually rising rhythmic pulse speed",
        "3. Heartbeat Thump — Deep sensual throb mimicking heartbeat",
        "4. Staccato Burst — Rapid fire intermittent flutter suction",
        "5. Rollercoaster Wave — Alternating fast and slow cycles",
        "6. Chaotic Climax — Randomized multi-frequency surge"
    ]
    for f_idx, fr in enumerate(freqs):
        draw.text((card_x + 24, 840 + f_idx * 35), fr, fill=MUTED_TEXT, font=get_font(15))

    return canvas

# -------------------------------------------------------------
# IMAGE 5: Whisper Quiet <=50dB, IPX5 Waterproof & Pin Fast Charging
# -------------------------------------------------------------
def build_image_5():
    print("[5/6] Building Performance & Specs Image...")
    canvas = Image.new("RGB", (1200, 1200), BG_WHITE)
    draw = ImageDraw.Draw(canvas)

    add_header(
        draw,
        tag="PERFORMANCE & RELIABILITY",
        title="Whisper-Quiet, IPX5 Waterproof & 40-Min Rapid Pin Charge",
        subtitle="Medical Precision Engineering Designed for Discretion, Hygiene & Fast Turnaround"
    )

    # 3 Performance Cards on Left
    cards = [
        {
            "tag": "≤ 50 dB SILENT",
            "title": "Acoustic Noise ≤ 50 dB",
            "desc": "Brushless micro-motor encased in shock-absorbing liquid silicone. Quieter than a soft whisper in a quiet bedroom for 100% privacy."
        },
        {
            "tag": "IPX5 RATING",
            "title": "IPX5 Washable & Waterproof",
            "desc": "Seamless ultrasonically sealed body withstands direct water faucet rinsing. Safe with all water-based lubricants and mild soaps."
        },
        {
            "tag": "100-MIN PLAYTIME",
            "title": "40-Min Rapid DC Pin Charging",
            "desc": "High-efficiency 5V DC pin charging port reaches 100% capacity in only 40 minutes, providing up to 100 minutes of continuous runtime."
        }
    ]

    card_x = 60
    card_w = 600
    start_y = 270
    card_h = 245
    gap = 25

    for i, c in enumerate(cards):
        cy = start_y + i * (card_h + gap)
        draw.rounded_rectangle([(card_x, cy), (card_x + card_w, cy + card_h)], radius=18, fill=BG_LIGHT_PINK, outline=BORDER_PINK, width=1)

        # Badge
        badge_w = len(c["tag"]) * 10 + 20
        draw.rounded_rectangle([(card_x + 24, cy + 22), (card_x + 24 + badge_w, cy + 50)], radius=8, fill=ACCENT_PINK)
        draw.text((card_x + 34, cy + 26), c["tag"], fill=(255, 255, 255), font=get_font(13, bold=True))

        # Title
        draw.text((card_x + 24, cy + 62), c["title"], fill=DARK_TEXT, font=get_font(24, bold=True))

        # Description
        words = c["desc"].split(" ")
        lines, curr = [], ""
        for w in words:
            if len(curr + " " + w) < 40:
                curr = curr + (" " if curr else "") + w
            else:
                lines.append(curr)
                curr = w
        if curr: lines.append(curr)

        for l_idx, line in enumerate(lines[:4]):
            draw.text((card_x + 24, cy + 115 + l_idx * 30), line, fill=MUTED_TEXT, font=get_font(16))

    # Right side: Product visual showcasing both front cat and DC pin port
    src = Image.open(IMG_BACK).convert("RGBA")
    cat_back = src.crop((140, 240, 880, 940)).resize((440, 420), Image.Resampling.LANCZOS)
    
    shadow = create_shadow((1200, 1200), [(710, 880), (1130, 960)], radius=25)
    canvas.paste(shadow, (0, 0), shadow)
    canvas.paste(cat_back, (700, 480), cat_back)

    # Pin Charging Callout
    draw.rounded_rectangle([(700, 290), (1140, 420)], radius=16, fill=(255, 255, 255), outline=BORDER_PINK, width=1)
    draw.text((724, 308), "Dedicated DC Pin Charging Port", fill=DARK_TEXT, font=get_font(20, bold=True))
    draw.text((724, 345), "• 40 Minutes = 100% Full Charge", fill=ACCENT_PINK, font=get_font(16, bold=True))
    draw.text((724, 378), "• Standard 5V USB Compatible", fill=MUTED_TEXT, font=get_font(15))

    return canvas

# -------------------------------------------------------------
# IMAGE 6: CAD Blueprint Dimensions, Parameters & Unboxing (参数与清单)
# -------------------------------------------------------------
def build_image_6():
    print("[6/6] Building Blueprint & Specifications Image...")
    canvas = Image.new("RGB", (1200, 1200), BG_WHITE)
    draw = ImageDraw.Draw(canvas)

    add_header(
        draw,
        tag="OFFICIAL SPECIFICATION DOSSIER",
        title="Product Dimensions, Technical Parameters & In-The-Box",
        subtitle="100% Verified Factory Standards · Direct Wholesale & OEM Dossier"
    )

    # Left Column: Dimensions
    left_x = 60
    left_w = 460
    draw.rounded_rectangle([(left_x, 260), (left_x + left_w, 1080)], radius=20, fill=BG_LIGHT_PINK, outline=BORDER_PINK, width=1)
    draw.text((left_x + 30, 285), "Precision CAD Dimensions", fill=DARK_TEXT, font=get_font(24, bold=True))

    src = Image.open(IMG_BACK).convert("RGBA")
    cat_small = src.crop((180, 240, 840, 940)).resize((340, 360), Image.Resampling.LANCZOS)
    canvas.paste(cat_small, (left_x + 60, 420), cat_small)

    font_cad = get_font(17, bold=True)
    # Width arrow 69 mm
    draw.line([(left_x + 80, 820), (left_x + 380, 820)], fill=ACCENT_PINK, width=2)
    draw.line([(left_x + 80, 810), (left_x + 80, 830)], fill=ACCENT_PINK, width=2)
    draw.line([(left_x + 380, 810), (left_x + 380, 830)], fill=ACCENT_PINK, width=2)
    draw.text((left_x + 190, 830), "Width: 69 mm", fill=ACCENT_PINK, font=font_cad)

    # Height arrow 54 mm
    draw.line([(left_x + 420, 430), (left_x + 420, 790)], fill=ACCENT_PINK, width=2)
    draw.line([(left_x + 410, 430), (left_x + 430, 430)], fill=ACCENT_PINK, width=2)
    draw.line([(left_x + 410, 790), (left_x + 430, 790)], fill=ACCENT_PINK, width=2)
    draw.text((left_x + 290, 385), "Height: 54 mm", fill=ACCENT_PINK, font=font_cad)

    # Bottom summary box
    draw.rounded_rectangle([(left_x + 30, 910), (left_x + left_w - 30, 1040)], radius=14, fill=(255, 255, 255), outline=BORDER_PINK, width=1)
    draw.text((left_x + 45, 925), "Net Dimensions: 96 × 69 × 54 mm", fill=DARK_TEXT, font=get_font(19, bold=True))
    draw.text((left_x + 45, 962), "Ultra-Light Net Weight: 105 g", fill=ACCENT_PINK, font=get_font(19, bold=True))
    draw.text((left_x + 45, 998), "Compact travel & bedside ergonomics", fill=MUTED_TEXT, font=get_font(15))

    # Right Column Top: 2-Column Parameter Table
    right_x = 550
    right_w = 590
    draw.rounded_rectangle([(right_x, 260), (right_x + right_w, 730)], radius=20, fill=(255, 255, 255), outline=BORDER_PINK, width=1)
    draw.text((right_x + 30, 285), "Certified Product Specifications", fill=DARK_TEXT, font=get_font(24, bold=True))

    specs = [
        ("Product Name", "MENGQU Sucking Device (萌趣吸吮器)"),
        ("Model Series", "MZB-WT054 (White) / MZB-WT055 (Pink)"),
        ("Main Materials", "Food-Grade Liquid Silicone + ABS"),
        ("Rated Voltage", "3.7V (Rechargeable Lithium Cell)"),
        ("Charging Specs", "5V / 1A via Dedicated DC Pin Cable"),
        ("Charging Time", "Approximately 40 Minutes"),
        ("Running Runtime", "Approximately 100 Minutes"),
        ("Maximum Noise", "≤ 50 dB (Whisper Silent)"),
        ("Waterproof Rating", "IPX5 (Washable & Splash-Resistant)"),
        ("User Group", "Adult Women's Sensual Wellness")
    ]

    font_lbl = get_font(16, bold=True)
    font_val = get_font(16, bold=False)

    for s_idx, (lbl, val) in enumerate(specs):
        sy = 340 + s_idx * 37
        if s_idx % 2 == 1:
            draw.rectangle([(right_x + 10, sy - 4), (right_x + right_w - 10, sy + 30)], fill=BG_LIGHT_PINK)
        draw.text((right_x + 24, sy), lbl, fill=DARK_TEXT, font=font_lbl)
        draw.text((right_x + 195, sy), val, fill=MUTED_TEXT, font=font_val)

    # Right Column Bottom: In-the-box Accessories
    draw.rounded_rectangle([(right_x, 760), (right_x + right_w, 1080)], radius=20, fill=BG_LIGHT_PINK, outline=BORDER_PINK, width=1)
    draw.text((right_x + 30, 785), "Packaging & Accessories Checklist", fill=DARK_TEXT, font=get_font(24, bold=True))

    items = [
        ("1× MENGQU Device", "Soft liquid silicone clitoral sucking unit"),
        ("1× Cloud Display Stand", "Pastel pink display & hygienic storage dock"),
        ("1× DC Pin USB Cable", "Fast-charge compatible with USB ports & power banks"),
        ("1× Multilingual Manual", "Detailed English / international user instructions"),
        ("1× Discreet Gift Box", "Plain unmarked outer carton with confidential label")
    ]

    for it_idx, (it_title, it_desc) in enumerate(items):
        iy = 835 + it_idx * 48
        draw.text((right_x + 30, iy), f"•  {it_title}", fill=ACCENT_PINK, font=get_font(16, bold=True))
        draw.text((right_x + 265, iy + 1), it_desc, fill=MUTED_TEXT, font=get_font(13))

    return canvas

# -------------------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------------------
def main():
    print("=" * 65)
    print("BOHOL - MENGQU Sucking Device (萌趣吸吮器) Perfected Suite")
    print("=" * 65)

    images = [
        ("mengqu-01-hero.webp", build_image_1),
        ("mengqu-02-suction.webp", build_image_2),
        ("mengqu-03-aesthetic.webp", build_image_3),
        ("mengqu-04-modes.webp", build_image_4),
        ("mengqu-05-performance.webp", build_image_5),
        ("mengqu-06-specs.webp", build_image_6)
    ]

    saved_paths = []
    for filename, builder in images:
        img = builder()
        out_prod = OUTPUT_DIR / filename
        img.save(out_prod, "WEBP", quality=92, method=6)

        out_detail = DETAILS_DIR / filename
        img.save(out_detail, "WEBP", quality=92, method=6)

        size_kb = out_prod.stat().st_size / 1024
        print(f"  [Created] {filename} ({size_kb:.1f} KB)")
        saved_paths.append(f"/images/products/{filename}")

    # Update src/data/products/mengqu.json
    json_path = ROOT_DIR / "src" / "data" / "products" / "mengqu.json"
    print(f"\nUpdating {json_path.name} with official parameters & new 6-image suite...")
    
    product_data = {
        "name": "MENGQU Sucking Device",
        "subtitle": "Kawaii Sleeping Cat Sonic Air-Pulse Clitoral Stimulator with Cloud Stand",
        "description": "Engineered for sensual clitoral wellness, the MENGQU Sucking Device combines an adorable sleeping kitten aesthetic with powerful contactless sonic air-pulse suction. Features a velvety body-safe liquid silicone mouth, an organic pink cloud docking base, 3 suction intensities, 6 pulse wave rhythms (18 total modes), whisper-silent operation (≤50dB), and fast 40-minute DC pin charging.",
        "category": "Compact",
        "label": "KAWAII AIR-PULSE WELLNESS",
        "order": 9,
        "featured": True,
        "price": "$32.00",
        "image": saved_paths[0],
        "gallery": saved_paths,
        "detailImages": saved_paths,
        "features": [
            "Contactless Air-Pulse Sonic Suction",
            "3 Intensities × 6 Rhythms (18 Modes)",
            "Matching Pastel Pink Cloud Dock",
            "Whisper-Quiet Operation ≤ 50 dB",
            "IPX5 Washable & Water-Resistant",
            "Fast 40-Min DC Pin Charging"
        ],
        "specs": [
            {"label": "Product Name", "value": "MENGQU Sucking Device (萌趣吸吮器)"},
            {"label": "Model Series", "value": "MZB-WT054 (White) / MZB-WT055 (Pink)"},
            {"label": "Dimensions", "value": "96 × 69 × 54 mm"},
            {"label": "Net Weight", "value": "105 g"},
            {"label": "Materials", "value": "Medical-Grade Liquid Silicone + ABS"},
            {"label": "Rated Voltage", "value": "3.7V (Rechargeable Lithium Battery)"},
            {"label": "Charging Voltage", "value": "5V / 1A via DC Pin Cable"},
            {"label": "Charging Time", "value": "Approximately 40 minutes"},
            {"label": "Listed Runtime", "value": "Approximately 100 minutes"},
            {"label": "Waterproof Rating", "value": "IPX5 (Washable and short-term soaking)"},
            {"label": "Maximum Noise", "value": "≤ 50 dB (Whisper Silent)"},
            {"label": "Packaging Accessories", "value": "Device, Cloud Dock, Pin Charging Cable, Manual"}
        ],
        "highlights": [
            {
                "title": "Contactless Clitoral Sonic Pulse Suction",
                "body": "The precision rose-gold rimmed acoustic suction mouth delivers gentle, rhythmic vacuum pressure waves directly to 8,000+ sensitive nerve endings without physical friction or desensitization."
            },
            {
                "title": "100% Discreet Bedside Art Ornament",
                "body": "Designed as an adorable sleeping kitten resting in a plush pink cloud base. Blends innocently into nightstand decor, eliminating any awkwardness when guests or family visit."
            },
            {
                "title": "Dual-Phase Rhythmic Control (18 Modes)",
                "body": "Long press the raised cat paw button for 1.5s to power on with vibration feedback. Cycle seamlessly through 3 suction intensities (Mild, Medium, Climax) across 6 dynamic wave patterns."
            },
            {
                "title": "Rapid Pin Charging & Whisper Silence",
                "body": "Equipped with a rear DC pin charging port that reaches 100% charge in just 40 minutes for 100 minutes of continuous runtime, operating under 50 dB for absolute privacy."
            }
        ],
        "seoTitle": "MENGQU Sucking Device — Wholesale & Private Label OEM | BOHOL",
        "seoDescription": "Source the MENGQU Sucking Device directly from BOHOL factory. Kawaii sleeping cat clitoral air-pulse stimulator, pink cloud dock, 18 modes, IPX5, <=50dB.",
        "note": "Specifications follow the supplied MENGQU official factory technical data sheet. 100% body-safe silicone, CE / RoHS compliant.",
        "subCategory": "Women's Toys",
        "vendor": "BOHOL Direct OEM"
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(product_data, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {json_path.name} with complete 6-image e-commerce suite!")

    print("\n" + "=" * 65)
    print("All 6 Perfected E-Commerce Images Generated and Saved Successfully!")
    print("=" * 65)

if __name__ == "__main__":
    main()
