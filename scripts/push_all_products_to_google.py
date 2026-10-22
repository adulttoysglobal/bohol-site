#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
BOHOL Adult Toys Global - Direct Product URLs Pusher to Google Indexing API
=============================================================================
Authoritative push of all 39 flagship & catalog product URLs directly to
Googlebot using Google Cloud Indexing API v3 and Google Search Console API.
=============================================================================
"""

import os
import sys
import time
import json
from datetime import datetime, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

KEY_PATH = os.path.join(os.path.dirname(__file__), 'google_service_account.json')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HOST = 'adulttoysglobal.com'
SITE_URL = f"https://{HOST}/"

SCOPES = [
    'https://www.googleapis.com/auth/webmasters',
    'https://www.googleapis.com/auth/indexing'
]

# Complete 39 Product URLs List
PRODUCT_URLS = [
    f"https://{HOST}/products/",
    f"https://{HOST}/catalogue/",
    # 14 Private-Mold Flagship Hardware Models
    f"https://{HOST}/products/twist-fun/",
    f"https://{HOST}/products/starship/",
    f"https://{HOST}/products/bobi-i/",
    f"https://{HOST}/products/bobi-iii/",
    f"https://{HOST}/products/cj7/",
    f"https://{HOST}/products/big-mouth/",
    f"https://{HOST}/products/wearable-big-mouth/",
    f"https://{HOST}/products/lenas/",
    f"https://{HOST}/products/mengqu/",
    f"https://{HOST}/products/bite/",
    f"https://{HOST}/products/summer-rabbit/",
    f"https://{HOST}/products/harmony-rabbit/",
    f"https://{HOST}/products/xiaoqiao/",
    f"https://{HOST}/products/space/",
    # Automatic Masturbator Cups
    f"https://{HOST}/products/nr-mast-1/",
    f"https://{HOST}/products/nr-mast-2/",
    f"https://{HOST}/products/nr-mast-3/",
    f"https://{HOST}/products/nr-mast-4/",
    # Whisper Quiet Vibrators & Wands
    f"https://{HOST}/products/nr-vibr-1/",
    f"https://{HOST}/products/nr-vibr-2/",
    f"https://{HOST}/products/nr-vibr-3/",
    f"https://{HOST}/products/nr-vibr-4/",
    # Ultra-Thin 001 Condoms
    f"https://{HOST}/products/nr-cond-1/",
    f"https://{HOST}/products/nr-cond-2/",
    f"https://{HOST}/products/nr-cond-3/",
    f"https://{HOST}/products/nr-cond-4/",
    # Water-Based & Hyaluronic Lubricants
    f"https://{HOST}/products/nr-lubr-1/",
    f"https://{HOST}/products/nr-lubr-2/",
    f"https://{HOST}/products/nr-lubr-3/",
    f"https://{HOST}/products/nr-lubr-4/",
    # Sensual Apparel
    f"https://{HOST}/products/nr-clot-1/",
    f"https://{HOST}/products/nr-clot-2/",
    f"https://{HOST}/products/nr-clot-3/",
    f"https://{HOST}/products/nr-clot-4/",
    # Intimate Wellness Accessories & Cleaners
    f"https://{HOST}/products/nr-acce-1/",
    f"https://{HOST}/products/nr-acce-2/",
    f"https://{HOST}/products/nr-acce-3/",
    f"https://{HOST}/products/nr-acce-4/",
]

def main():
    print("=" * 70)
    print(" 🚀 BOHOL - GOOGLE INDEXING API PRODUCT LINK BATCH PUSHER")
    print("=" * 70)
    print(f"Target Site: {SITE_URL}")
    print(f"Total Product & Catalog URLs to push: {len(PRODUCT_URLS)}")

    if not os.path.exists(KEY_PATH):
        print(f"[ERROR] Service account key not found at {KEY_PATH}")
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    indexing_service = build('indexing', 'v3', credentials=creds)
    webmasters_service = build('searchconsole', 'v1', credentials=creds)

    # Step 1: Submit Sitemaps containing all products
    print("\n[Step 1/2] 📡 Re-submitting Product Sitemaps to Google Search Console...")
    for sm in [f"https://{HOST}/sitemap-index.xml", f"https://{HOST}/sitemap-0.xml"]:
        try:
            webmasters_service.sitemaps().submit(siteUrl=SITE_URL, feedpath=sm).execute()
            print(f"  ✓ Sitemap Submitted: {sm}")
        except Exception as e:
            print(f"  ✗ Sitemap Error ({sm}): {e}")

    # Step 2: Push Each Product URL to Google Indexing API
    print("\n[Step 2/2] ⚡ Pushing All 39 Product URLs directly to Google Indexing API...")
    success_urls = []
    failed_urls = []

    for idx, url in enumerate(PRODUCT_URLS, 1):
        body = {
            'url': url,
            'type': 'URL_UPDATED'
        }
        try:
            resp = indexing_service.urlNotifications().publish(body=body).execute()
            notify_time = resp.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('notifyTime', '')
            print(f"  [{idx:02d}/{len(PRODUCT_URLS)}] ✓ Pushed: {url} -> {notify_time or 'OK'}")
            success_urls.append({'url': url, 'notifyTime': notify_time})
            time.sleep(0.3)  # Gentle rate limit pacing
        except Exception as e:
            print(f"  [{idx:02d}/{len(PRODUCT_URLS)}] ✗ Failed: {url} -> {e}")
            failed_urls.append({'url': url, 'error': str(e)})

    print("\n" + "=" * 70)
    print(f" ✅ Push Finished! Successfully pushed {len(success_urls)} / {len(PRODUCT_URLS)} product URLs to Google Indexing API.")
    if failed_urls:
        print(f" ⚠️ Failed: {len(failed_urls)}")
    print("=" * 70)

    # Save push receipt
    receipt_path = os.path.join(os.path.dirname(__file__), 'product_push_receipt.json')
    with open(receipt_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'totalPushed': len(success_urls),
            'successUrls': success_urls,
            'failedUrls': failed_urls
        }, f, indent=2, ensure_ascii=False)
    print(f"Receipt written to: {receipt_path}")

if __name__ == '__main__':
    main()
