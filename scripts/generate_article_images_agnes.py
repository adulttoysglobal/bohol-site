#!/usr/bin/env python3
"""
Generate bespoke high-definition B2B images for BOHOL journal articles using Agnes AI API.
Converts generated images to optimized WebP format and updates markdown frontmatter.
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
        "prompt": "Ultra-luxury modern couple wellness smart device with glowing subtle cyan Bluetooth 5.3 LED ring, lying elegantly next to a premium smartphone displaying a minimalist IoT telemetry dashboard, set on a dark walnut table with soft ambient studio lighting, clean industrial design, 8k photography, hyperrealistic."
    },
    {
        "file": "src/data/journal/closed-loop-servo-linear-reciprocating-masturbators.md",
        "slug": "closed-loop-servo-linear-reciprocating-masturbators",
        "prompt": "Precision mechatronics cross-section cutaway showing a miniature brushless DC servo motor with magnetic encoder, helical precision ball screw drive, and aerospace-grade aluminum chassis, cleanroom assembly workstation, macro photography, 8k resolution, photorealistic industrial engineering."
    },
    {
        "file": "src/data/journal/001mm-waterborne-polyurethane-condom-tensile-leak-testing.md",
        "slug": "001mm-waterborne-polyurethane-condom-tensile-leak-testing",
        "prompt": "Ultra-modern polymer science testing laboratory with a high-precision digital tensile test machine holding an ultra-thin 0.01mm transparent waterborne polyurethane membrane, laser micrometer readout, clean sterile white laboratory lighting, 8k photorealistic quality control."
    },
    {
        "file": "src/data/journal/contactless-hotel-minibar-vending-nayax-emv-telemetry.md",
        "slug": "contactless-hotel-minibar-vending-nayax-emv-telemetry",
        "prompt": "Luxury 5-star boutique hotel suite wall featuring a compact built-in automated glass-front mini-bar dispenser cabinet with an integrated Nayax contactless EMV payment terminal, subtle ambient glow, high-end hospitality interior, photorealistic."
    },
    {
        "file": "src/data/journal/class-100000-cleanroom-lsr-injection-airborne-particulate-control.md",
        "slug": "class-100000-cleanroom-lsr-injection-airborne-particulate-control",
        "prompt": "Pharmaceutical Class 100,000 cleanroom manufacturing facility with an automated robotic arm extracting precision liquid silicone rubber (LSR) molded components from an all-electric injection molding machine, HEPA ceiling filtration panels, sterile cleanroom suits, 8k industrial photography."
    },
    {
        "file": "src/data/journal/double-curvature-silicone-cock-rings-neurovascular-ergonomics.md",
        "slug": "double-curvature-silicone-cock-rings-neurovascular-ergonomics",
        "prompt": "Minimalist luxury ergonomic male wellness accessory sculpted from satin-matte platinum medical-grade silicone, displayed on a frosted crystal pedestal, gentle directional studio lighting, deep charcoal background, sleek sensual aesthetic, 8k product photography."
    },
    {
        "file": "src/data/journal/ul1642-un383-lithium-battery-safety-pcm-thermal-throttling.md",
        "slug": "ul1642-un383-lithium-battery-safety-pcm-thermal-throttling",
        "prompt": "Electronic engineering laboratory test bench with an open hardware chassis showing a compact lithium polymer pouch battery, dual-MOSFET protection circuit board (PCM), gold-plated contacts, digital multimeter probe, technical macro photography."
    },
    {
        "file": "src/data/journal/water-based-vs-silicone-lubricant-osmolality-ph-balance.md",
        "slug": "water-based-vs-silicone-lubricant-osmolality-ph-balance",
        "prompt": "Pharmaceutical skincare laboratory showing elegant amber and frosted glass dropper bottles of isotonic personal lubricant, clear fluid viscosity droplet suspended in crystal beaker, digital pH meter in background, bright scientific aesthetic."
    },
    {
        "file": "src/data/journal/private-mold-tooling-contracts-ip-escrow-china.md",
        "slug": "private-mold-tooling-contracts-ip-escrow-china",
        "prompt": "High-precision 5-axis CNC machining center cutting a mirror-polished multi-cavity S136 stainless steel injection mold tool, fine coolant mist, glowing inspection light, precision industrial engineering, 8k photography."
    },
    {
        "file": "src/data/journal/ipx8-continuous-submersion-waterproofing-ultrasonic-welding.md",
        "slug": "ipx8-continuous-submersion-waterproofing-ultrasonic-welding",
        "prompt": "High-pressure transparent hydro-test pressure chamber filled with illuminated sapphire-blue water testing a submerged luxury electronic device under water pressure, tiny air bubbles, digital barometric gauge display, IPX8 laboratory verification, 8k photography."
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
            print(f"  [API] Sending generation request (Attempt {attempt})...")
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
    print(f"  [Download] Fetching from {url}...")
    res = requests.get(url, timeout=60)
    res.raise_for_status()
    
    img = Image.open(io.BytesIO(res.content))
    if img.mode in ("RGBA", "LA"):
        save_mode = "RGBA"
    else:
        img = img.convert("RGB")
        save_mode = "RGB"
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "WEBP", quality=85, method=6)
    size_kb = output_path.stat().st_size / 1024
    print(f"  [Saved] {output_path.name} ({size_kb:.1f} KB, format: WEBP)")

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
    print("=" * 60)
    print("BOHOL - Agnes AI Article Image Generator")
    print(f"Target count: {len(TARGET_ARTICLES)} articles")
    print("=" * 60)
    
    success_count = 0
    for idx, item in enumerate(TARGET_ARTICLES, 1):
        md_file = ROOT_DIR / item["file"]
        slug = item["slug"]
        webp_path = OUTPUT_DIR / f"{slug}.webp"
        webp_rel_url = f"/images/journal/{slug}.webp"
        
        print(f"\n[{idx}/{len(TARGET_ARTICLES)}] Processing: {slug}")
        if webp_path.exists():
            print(f"  [Cache] {webp_path.name} already exists. Updating markdown...")
            update_markdown_image(md_file, webp_rel_url)
            success_count += 1
            continue
            
        try:
            image_url = generate_image_url(item["prompt"])
            download_and_save_webp(image_url, webp_path)
            update_markdown_image(md_file, webp_rel_url)
            success_count += 1
        except Exception as e:
            print(f"  [Failed] Error generating {slug}: {e}")
            
        # Brief throttle between requests
        time.sleep(1.5)
        
    print("\n" + "=" * 60)
    print(f"Completed: {success_count}/{len(TARGET_ARTICLES)} images generated & linked successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
