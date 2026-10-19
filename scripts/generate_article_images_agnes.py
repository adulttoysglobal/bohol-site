#!/usr/bin/env python3
"""
Regenerate 10 bespoke high-definition B2B images for BOHOL adult novelty articles using Agnes AI API.
Accurately centers on actual Adult Novelty / Adult Toys products:
- Vibrators (Rabbit, Wand, Wearable couple panty vibrators)
- Male Automatic Masturbator Strokers & Cups
- 0.01mm Polyurethane Condoms & Packaging
- Hotel In-Room Adult Amenity Vending & Dispensers
- Cleanroom Liquid Silicone Sex Toy Molding
- Dual-loop Silicone Cock Rings
- Magnetic USB Charging Bases with Adult Vibrators
- Intimate Sexual Lubricants
- Precision Metal Tooling for Adult Sex Toys
- IPX8 Submerged Waterproof Adult Sex Toys
"""

import os
import sys
import time
import re
import requests
from pathlib import Path
from PIL import Image
import io

API_KEY = "sk-aD72q1Hem02QPSC12OZxmn4avIoQW1BbqwDVFM7GG5YU25gp"
API_URL = "https://apihub.agnes-ai.com/v1/images/generations"
MODEL = "agnes-image-2.0-flash"

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "public" / "images" / "journal"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_ARTICLES = [
    {
        "file": "src/data/journal/smart-app-ble-53-long-distance-couple-tele-intimacy.md",
        "slug": "smart-app-ble-53-long-distance-couple-tele-intimacy",
        "prompt": "Luxury adult sex toy product photography, sleek ergonomic couple wearable panty vibrator in soft blush pink liquid silicone, with subtle glowing LED light, resting beside an elegant smartphone showing a sensual couple tele-control app on a luxury silk bedroom setting, 8k commercial photography, premium adult novelty design."
    },
    {
        "file": "src/data/journal/closed-loop-servo-linear-reciprocating-masturbators.md",
        "slug": "closed-loop-servo-linear-reciprocating-masturbators",
        "prompt": "High-end automatic male masturbator cup stroker device, sleek futuristic matte black and metallic cylindrical adult novelty toy with textured soft silicone entry opening, modern LED control panel, standing on a bedside table with soft moody rim lighting, 8k commercial adult toy photography."
    },
    {
        "file": "src/data/journal/001mm-waterborne-polyurethane-condom-tensile-leak-testing.md",
        "slug": "001mm-waterborne-polyurethane-condom-tensile-leak-testing",
        "prompt": "Luxury adult condoms commercial display, elegant black and gold foiled condom packaging boxes with sleek individual foil tear packets, one translucent ultra-thin 0.01mm rolled condom clearly displayed on a smooth dark satin background, high-end adult wellness product photo, 8k."
    },
    {
        "file": "src/data/journal/contactless-hotel-minibar-vending-nayax-emv-telemetry.md",
        "slug": "contactless-hotel-minibar-vending-nayax-emv-telemetry",
        "prompt": "Luxury hotel in-room adult amenity vending dispenser, illuminated compact glass display stocked with boutique adult novelty wellness products, condom boxes, mini bullet vibrators, and intimate lubricant bottles, equipped with a sleek touchless card payment reader, warm boutique hotel room background."
    },
    {
        "file": "src/data/journal/class-100000-cleanroom-lsr-injection-airborne-particulate-control.md",
        "slug": "class-100000-cleanroom-lsr-injection-airborne-particulate-control",
        "prompt": "Cleanroom manufacturing workshop producing colorful medical silicone adult sex toys, fresh smooth liquid silicone vibrators in pastel lavender, rose pink, and mint green neatly arranged on stainless steel inspection trays, sterile technician inspecting adult novelty products, 8k industrial photo."
    },
    {
        "file": "src/data/journal/double-curvature-silicone-cock-rings-neurovascular-ergonomics.md",
        "slug": "double-curvature-silicone-cock-rings-neurovascular-ergonomics",
        "prompt": "Luxury adult male silicone cock rings and vibrating pleasure rings, crafted in silky matte black and midnight blue medical-grade silicone with dual-loop ergonomic contour, placed on a frosted glass pedestal with soft sensual studio lighting, high-end adult toy product photography, 8k."
    },
    {
        "file": "src/data/journal/ul1642-un383-lithium-battery-safety-pcm-thermal-throttling.md",
        "slug": "ul1642-un383-lithium-battery-safety-pcm-thermal-throttling",
        "prompt": "Luxury rechargeable adult wand vibrator and bullet massager in premium lilac silicone with gold trim, resting securely on its magnetic contact charging base, soft glow LED charging light, resting on a white marble vanity table, elegant commercial adult toy photography, 8k."
    },
    {
        "file": "src/data/journal/water-based-vs-silicone-lubricant-osmolality-ph-balance.md",
        "slug": "water-based-vs-silicone-lubricant-osmolality-ph-balance",
        "prompt": "High-end personal intimate sexual lubricant product line, elegant minimalist pump dispenser bottles labeled Water-Based and Silicone Sensual Lube, clear viscous liquid droplet glistening on a smooth dark surface, soft sensual studio lighting, 8k luxury adult cosmetics photography."
    },
    {
        "file": "src/data/journal/private-mold-tooling-contracts-ip-escrow-china.md",
        "slug": "private-mold-tooling-contracts-ip-escrow-china",
        "prompt": "High-precision metal injection mold tooling for adult sex toys, showing the distinct mirror-polished cavity shape of a rabbit dual-stimulation vibrator body, with a freshly molded bright pink silicone toy body resting next to the steel mold, professional factory tooling photography."
    },
    {
        "file": "src/data/journal/ipx8-continuous-submersion-waterproofing-ultrasonic-welding.md",
        "slug": "ipx8-continuous-submersion-waterproofing-ultrasonic-welding",
        "prompt": "Submerged luxury waterproof rabbit vibrator adult sex toy made of bright coral-pink silicone, completely underwater in a crystal-clear acrylic water tank with sparkling air bubbles rising around it, underwater dramatic lighting, 100% IPX8 submersible waterproof adult toy demonstration, 8k."
    }
]

def generate_image_url(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "size": "1024x768",
        "extra_body": {
            "response_format": "url"
        }
    }
    
    for attempt in range(1, 4):
        try:
            print(f"  [API] Requesting Agnes AI generation (Attempt {attempt})...")
            res = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            if res.status_code == 200:
                data = res.json()
                if "data" in data and len(data["data"]) > 0 and "url" in data["data"][0]:
                    return data["data"][0]["url"]
                else:
                    print(f"  [Error] Unexpected JSON format: {data}")
            else:
                print(f"  [Error] Status {res.status_code}: {res.text}")
        except Exception as e:
            print(f"  [Exception] {e}")
        time.sleep(3)
        
    raise RuntimeError(f"Failed to generate image for prompt: {prompt[:40]}...")

def download_and_save_webp(url: str, output_path: Path):
    print(f"  [Download] Fetching image from {url}...")
    res = requests.get(url, timeout=60)
    res.raise_for_status()
    
    img = Image.open(io.BytesIO(res.content))
    if img.mode in ("RGBA", "LA"):
        img = img.convert("RGBA")
    else:
        img = img.convert("RGB")
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "WEBP", quality=85, method=6)
    size_kb = output_path.stat().st_size / 1024
    print(f"  [Saved] {output_path.name} ({size_kb:.1f} KB, WebP)")

def update_markdown_image(file_path: Path, webp_url: str):
    content = file_path.read_text(encoding="utf-8")
    new_content = re.sub(
        r'image:\s*["\']?[^"\'\r\n]+["\']?',
        f'image: "{webp_url}"',
        content,
        count=1
    )
    file_path.write_text(new_content, encoding="utf-8")
    print(f"  [Markdown Updated] {file_path.name} -> {webp_url}")

def main():
    print("=" * 65)
    print("BOHOL - Agnes AI Adult Toys Product Image Generator (Overwriting with Adult Toy Visuals)")
    print(f"Target count: {len(TARGET_ARTICLES)} articles")
    print("=" * 65)
    
    success_count = 0
    for idx, item in enumerate(TARGET_ARTICLES, 1):
        md_file = ROOT_DIR / item["file"]
        slug = item["slug"]
        webp_path = OUTPUT_DIR / f"{slug}.webp"
        webp_rel_url = f"/images/journal/{slug}.webp"
        
        print(f"\n[{idx}/{len(TARGET_ARTICLES)}] Generating adult toy visual for: {slug}")
        try:
            image_url = generate_image_url(item["prompt"])
            download_and_save_webp(image_url, webp_path)
            update_markdown_image(md_file, webp_rel_url)
            success_count += 1
        except Exception as e:
            print(f"  [Failed] Error generating {slug}: {e}")
            
        time.sleep(1.5)
        
    print("\n" + "=" * 65)
    print(f"Completed: {success_count}/{len(TARGET_ARTICLES)} adult toy images generated & replaced!")
    print("=" * 65)

if __name__ == "__main__":
    main()
