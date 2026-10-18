#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync live Google Search Console API metrics to src/data/gsc_live_cache.json
"""
import os
import sys
import json
from datetime import datetime, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_PATH = os.path.join(os.path.dirname(__file__), 'google_service_account.json')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'gsc_live_cache.json')
SITE_URL = 'https://adulttoysglobal.com/'
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def sync():
    if not os.path.exists(KEY_PATH):
        print(f"[Error] Key file not found: {KEY_PATH}")
        return False

    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    service = build('searchconsole', 'v1', credentials=creds)

    # 1. Sites list
    sites_res = service.sites().list().execute()
    site_entries = sites_res.get('siteEntry', [])
    permission_level = 'Unknown'
    for s in site_entries:
        if s.get('siteUrl') == SITE_URL:
            permission_level = s.get('permissionLevel', 'siteFullUser')

    # 2. Sitemaps
    sitemaps_res = service.sitemaps().list(siteUrl=SITE_URL).execute()
    sitemaps_list = sitemaps_res.get('sitemap', [])

    # 3. URL Inspection for homepage
    inspect_res = service.urlInspection().index().inspect(body={
        'inspectionUrl': SITE_URL,
        'siteUrl': SITE_URL
    }).execute()

    payload = {
        'lastSyncedAt': datetime.now(timezone.utc).isoformat(),
        'siteUrl': SITE_URL,
        'permissionLevel': permission_level,
        'status': 'CONNECTED',
        'sitemaps': sitemaps_list,
        'homepageInspection': inspect_res.get('inspectionResult', {})
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"[OK] Live GSC metrics synced to {OUTPUT_PATH}")
    return True

if __name__ == '__main__':
    sync()
