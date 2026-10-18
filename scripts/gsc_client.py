#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Search Console API Client for adulttoysglobal.com
Uses Service Account authentication to fetch indexing & performance metrics.
"""

import os
import sys
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_PATH = os.path.join(os.path.dirname(__file__), 'google_service_account.json')
SITE_URL = 'https://adulttoysglobal.com/'
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def get_service():
    if not os.path.exists(KEY_PATH):
        print(f"[Error] Key file not found: {KEY_PATH}")
        return None
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    return build('searchconsole', 'v1', credentials=creds)

def check_connection():
    service = get_service()
    if not service:
        return False
    try:
        sites_res = service.sites().list().execute()
        site_entries = sites_res.get('siteEntry', [])
        print(f"[GSC API] Connected successfully! Accessible properties count: {len(site_entries)}")
        matched = False
        for site in site_entries:
            print(f"  - {site.get('siteUrl')} (Permission: {site.get('permissionLevel')})")
            if site.get('siteUrl') == SITE_URL or 'adulttoysglobal.com' in site.get('siteUrl', ''):
                matched = True
        return matched
    except Exception as e:
        print(f"[GSC API Error] {e}")
        return False

def get_sitemaps():
    service = get_service()
    if not service:
        return None
    try:
        res = service.sitemaps().list(siteUrl=SITE_URL).execute()
        return res.get('sitemap', [])
    except Exception as e:
        print(f"[GSC Sitemaps Error] {e}")
        return None

if __name__ == '__main__':
    print("Testing Google Search Console API Connection...")
    has_access = check_connection()
    if has_access:
        print(f"\n[OK] Service account has verified access to {SITE_URL}!")
        sitemaps = get_sitemaps()
        print(f"Sitemaps: {json.dumps(sitemaps, indent=2, ensure_ascii=False)}")
    else:
        print(f"\n[Notice] Service account is authenticated, but needs to be added as a user in GSC for {SITE_URL}.")
