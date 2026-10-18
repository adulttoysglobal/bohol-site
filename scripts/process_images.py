#!/usr/bin/env python3
"""
BOHOL Automated WebP Image Processing Engine & Code Reference Synchronizer
========================================================================
Mandate:
  All images on the website MUST be processed into .webp format.
  Uncompressed formats (.jpg, .jpeg, .png, .bmp, .tiff) are automatically
  transcoded to WebP (quality 82, method 6) with EXIF orientation preserved,
  and references across src/ (JSON, Astro, MD, etc.) are synchronized.

Usage:
  python scripts/process_images.py                # Batch process all images & sync code
  python scripts/process_images.py --check        # Audit images (returns exit code 1 if non-webp found)
  python scripts/process_images.py --watch        # Continuous file watcher mode for live uploads
  python scripts/process_images.py --keep-source  # Keep original files instead of removing them
"""

import os
import sys
import time
import argparse
from pathlib import Path
try:
    from PIL import Image, ImageOps
except ImportError:
    Image = None
    ImageOps = None

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
PUBLIC_IMAGES_DIR = ROOT_DIR / "public" / "images"
SRC_DIR = ROOT_DIR / "src"

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".jfif"}
CODE_EXTS = {".json", ".astro", ".md", ".ts", ".js", ".mjs", ".html", ".css", ".yml", ".yaml"}

def convert_to_webp(image_path: Path, quality: int = 82) -> Path:
    """
    Converts a single image to .webp with optimal compression and color space handling.
    Preserves EXIF orientation before stripping metadata.
    """
    webp_path = image_path.with_suffix(".webp")
    
    with Image.open(image_path) as img:
        # Correct orientation based on EXIF before stripping
        img = ImageOps.exif_transpose(img)
        
        # Color mode handling
        if img.mode in ("RGBA", "LA"):
            # Transparent images preserve alpha in WebP
            save_mode = "RGBA"
            if img.mode != "RGBA":
                img = img.convert("RGBA")
        elif img.mode == "P":
            # Palette images
            if "transparency" in img.info:
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")
            
        # Save as WebP
        img.save(webp_path, "WEBP", quality=quality, method=6)
        
    return webp_path

def update_code_references(converted_map: dict[str, str]):
    """
    Scans src/ and replaces references to old image paths with the new .webp paths.
    converted_map maps old filename/relative path to new .webp filename/path.
    """
    if not converted_map:
        return 0

    modified_files = 0
    # Collect all code files
    code_files = [p for p in SRC_DIR.rglob("*") if p.is_file() and p.suffix.lower() in CODE_EXTS]
    
    # Also include public/admin/config.yml
    admin_config = ROOT_DIR / "public" / "admin" / "config.yml"
    if admin_config.exists():
        code_files.append(admin_config)

    for code_file in code_files:
        try:
            content = code_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        original_content = content
        for old_ref, new_ref in converted_map.items():
            if old_ref in content:
                content = content.replace(old_ref, new_ref)

        if content != original_content:
            code_file.write_text(content, encoding="utf-8")
            modified_files += 1

    return modified_files

def process_batch(target_dir: Path, delete_source: bool = True, quality: int = 82):
    """
    Scans target directory recursively and converts all non-webp images to .webp.
    """
    if not target_dir.exists():
        print(f"[ProcessImages] Error: Directory '{target_dir}' does not exist.")
        return False

    # Find all source images
    source_files = [p for p in target_dir.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS]
    
    if not source_files:
        print(f"[ProcessImages] All images in '{target_dir}' are already .webp! (0 pending)")
        return True

    print(f"[ProcessImages] Found {len(source_files)} images to convert to .webp in '{target_dir}'...")
    
    converted_map = {}
    total_old_size = 0
    total_new_size = 0
    success_count = 0
    error_count = 0

    for idx, img_path in enumerate(source_files, start=1):
        try:
            old_size = img_path.stat().st_size
            webp_path = convert_to_webp(img_path, quality=quality)
            new_size = webp_path.stat().st_size
            
            total_old_size += old_size
            total_new_size += new_size
            success_count += 1
            
            # Map both basename and web-relative path
            # e.g. "product.jpg" -> "product.webp"
            # e.g. "/images/9rabbit/products/nr-1.jpg" -> "/images/9rabbit/products/nr-1.webp"
            old_name = img_path.name
            new_name = webp_path.name
            converted_map[old_name] = new_name
            
            # Relative to public/
            try:
                rel_to_public = img_path.relative_to(ROOT_DIR / "public").as_posix()
                rel_new_public = webp_path.relative_to(ROOT_DIR / "public").as_posix()
                converted_map[f"/{rel_to_public}"] = f"/{rel_new_public}"
                converted_map[rel_to_public] = rel_new_public
            except ValueError:
                pass

            if delete_source:
                img_path.unlink()

            if idx % 50 == 0 or idx == len(source_files):
                pct = (idx / len(source_files)) * 100
                print(f"  [{pct:5.1f}%] Converted {idx}/{len(source_files)} images...")
                
        except Exception as e:
            error_count += 1
            print(f"  [ERROR] Failed to convert {img_path}: {e}")

    saved_bytes = total_old_size - total_new_size
    saved_mb = saved_bytes / (1024 * 1024)
    old_mb = total_old_size / (1024 * 1024)
    new_mb = total_new_size / (1024 * 1024)
    reduction = (saved_bytes / total_old_size * 100) if total_old_size > 0 else 0

    print("=" * 60)
    print(f"[ProcessImages] Batch Conversion Complete:")
    print(f"  - Converted: {success_count} images (Errors: {error_count})")
    print(f"  - Original Size: {old_mb:.2f} MB")
    print(f"  - WebP Size:     {new_mb:.2f} MB")
    print(f"  - Storage Saved: {saved_mb:.2f} MB ({reduction:.1f}% reduction)")
    print("=" * 60)

    # Synchronize code references
    print(f"[ProcessImages] Updating references in code files...")
    updated_files = update_code_references(converted_map)
    print(f"[ProcessImages] Successfully updated image references across {updated_files} code files.")

    return True

def audit_images(target_dir: Path) -> bool:
    """
    Checks if any uncompressed images exist. Returns True if all are .webp, False otherwise.
    """
    non_webp = [p for p in target_dir.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS]
    if non_webp:
        print(f"[Audit] FAILED: Found {len(non_webp)} non-webp images in {target_dir}:")
        for p in non_webp[:10]:
            print(f"  - {p.relative_to(ROOT_DIR)}")
        if len(non_webp) > 10:
            print(f"  ... and {len(non_webp) - 10} more.")
        return False
    else:
        print(f"[Audit] PASSED: 100% of images in {target_dir} are in .webp format.")
        return True

def watch_directory(target_dir: Path, delete_source: bool = True, quality: int = 82):
    """
    Monitors directory continuously and converts any newly dropped image to WebP.
    """
    print(f"[Watcher] Watching '{target_dir}' for incoming JPG/PNG images (Polling every 2s)...")
    print("[Watcher] Press Ctrl+C to terminate.")
    
    try:
        while True:
            source_files = [p for p in target_dir.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS]
            if source_files:
                print(f"[Watcher] Detected {len(source_files)} new image(s). Processing...")
                process_batch(target_dir, delete_source=delete_source, quality=quality)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[Watcher] Stopped.")

def main():
    if Image is None:
        print("[ProcessImages] Notice: PIL (Pillow) not installed in this environment. Skipping image processing hook.")
        sys.exit(0)

    parser = argparse.ArgumentParser(description="BOHOL WebP Image Processing Engine")
    parser.add_argument("--dir", type=str, default=str(PUBLIC_IMAGES_DIR), help="Target directory (defaults to public/images)")
    parser.add_argument("--keep-source", action="store_true", help="Do not delete original files after conversion")
    parser.add_argument("--quality", type=int, default=82, help="WebP compression quality (default 82)")
    parser.add_argument("--check", action="store_true", help="Audit mode: exit code 1 if non-webp images exist")
    parser.add_argument("--watch", action="store_true", help="Watch mode: continuously convert newly dropped images")

    args = parser.parse_args()
    target_path = Path(args.dir)

    if args.check:
        passed = audit_images(target_path)
        sys.exit(0 if passed else 1)
        
    if args.watch:
        watch_directory(target_path, delete_source=not args.keep_source, quality=args.quality)
    else:
        success = process_batch(target_path, delete_source=not args.keep_source, quality=args.quality)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
