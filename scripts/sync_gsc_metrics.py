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

    # 4. Search Analytics query (Impressions, Clicks, CTR, Position)
    from datetime import timedelta
    now_dt = datetime.now(timezone.utc)
    end_date = now_dt.strftime('%Y-%m-%d')
    start_date = (now_dt - timedelta(days=28)).strftime('%Y-%m-%d')

    analytics_data = {
        'totalClicks': 0,
        'totalImpressions': 0,
        'avgCtr': 0.0,
        'avgPosition': 0.0,
        'dateRange': f"{start_date} ~ {end_date}",
        'queries': [],
        'pages': [],
        'hasRows': False
    }

    try:
        # Total metrics query
        req_total = {
            'startDate': start_date,
            'endDate': end_date
        }
        res_total = service.searchanalytics().query(siteUrl=SITE_URL, body=req_total).execute()
        rows_total = res_total.get('rows', [])
        if rows_total:
            analytics_data['hasRows'] = True
            tot_clicks = sum(r.get('clicks', 0) for r in rows_total)
            tot_impr = sum(r.get('impressions', 0) for r in rows_total)
            analytics_data['totalClicks'] = tot_clicks
            analytics_data['totalImpressions'] = tot_impr
            analytics_data['avgCtr'] = round((tot_clicks / tot_impr * 100), 2) if tot_impr > 0 else 0.0
            analytics_data['avgPosition'] = round(sum(r.get('position', 0) for r in rows_total) / len(rows_total), 1)

        # Top queries query
        req_queries = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['query'],
            'rowLimit': 10
        }
        res_queries = service.searchanalytics().query(siteUrl=SITE_URL, body=req_queries).execute()
        if res_queries.get('rows'):
            analytics_data['queries'] = res_queries.get('rows', [])

        # Top pages query
        req_pages = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['page'],
            'rowLimit': 10
        }
        res_pages = service.searchanalytics().query(siteUrl=SITE_URL, body=req_pages).execute()
        if res_pages.get('rows'):
            analytics_data['pages'] = res_pages.get('rows', [])
    except Exception as e:
        print(f"[Warning] Search analytics query notice: {e}")

    payload = {
        'lastSyncedAt': datetime.now(timezone.utc).isoformat(),
        'siteUrl': SITE_URL,
        'permissionLevel': permission_level,
        'status': 'CONNECTED',
        'searchAnalytics': analytics_data,
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
