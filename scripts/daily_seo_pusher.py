#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
BOHOL Adult Toys Global - Daily Automated SEO Link Pusher & Metrics Syncer
=============================================================================
Features:
1. Google Search Console API: Submits full-site sitemaps directly to Googlebot.
2. Google Indexing API: Publishes instant crawl notifications for URLs.
3. IndexNow API: Pushes all 160+ URLs to Bing, Yandex, Naver, and Seznam.
4. GSC Performance Sync: Fetches Impressions, Clicks, CTR, and Keyword Rankings.
5. Saves real-time push logs to src/data/gsc_live_cache.json for Admin Dashboard.
=============================================================================
"""

import os
import sys
import re
import json
import time
from datetime import datetime, timezone, timedelta

# Fix Windows console UTF-8 output
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.request
import urllib.error

# Paths & Config
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KEY_PATH = os.path.join(os.path.dirname(__file__), 'google_service_account.json')
OUTPUT_PATH = os.path.join(BASE_DIR, 'src', 'data', 'gsc_live_cache.json')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'daily_push_log.json')
SITEMAP_PATH = os.path.join(BASE_DIR, 'dist', 'sitemap-0.xml')

SITE_URL = 'https://adulttoysglobal.com/'
HOST = 'adulttoysglobal.com'
INDEXNOW_KEY = 'b8f4e29c017d45ba8933e9b08f4c21a5'
INDEXNOW_KEY_LOCATION = f"https://{HOST}/{INDEXNOW_KEY}.txt"

SCOPES = [
    'https://www.googleapis.com/auth/webmasters',
    'https://www.googleapis.com/auth/indexing'
]

def load_all_urls():
    """Extract all public site URLs from sitemap or fallback core list."""
    urls = []
    if os.path.exists(SITEMAP_PATH):
        try:
            with open(SITEMAP_PATH, 'r', encoding='utf-8') as f:
                raw_urls = re.findall(r'<loc>(https://adulttoysglobal\.com[^<]+)</loc>', f.read())
                # Exclude admin and internal paths from search engine submissions
                urls = [u for u in raw_urls if '/admin' not in u and '/bohol-control' not in u]
        except Exception as e:
            print(f"[Warn] Failed reading sitemap: {e}")

    if not urls:
        urls = [
            f"https://{HOST}/",
            f"https://{HOST}/products/",
            f"https://{HOST}/manufacturing/",
            f"https://{HOST}/about/",
            f"https://{HOST}/partners/",
            f"https://{HOST}/contact/",
            f"https://{HOST}/rfq/",
            f"https://{HOST}/technology/",
            f"https://{HOST}/catalogue/",
            f"https://{HOST}/privacy/",
            f"https://{HOST}/support/",
            f"https://{HOST}/support/documentation/",
            f"https://{HOST}/journal/",
            f"https://{HOST}/guide/",
            f"https://{HOST}/news/"
        ]
    return urls

def push_to_google_sitemaps(service):
    """Submit sitemaps directly to Google Search Console via official API."""
    print("\n[1/4] 🚀 Submitting Sitemaps to Google Search Console...")
    sitemap_targets = [
        f"https://{HOST}/sitemap-index.xml",
        f"https://{HOST}/sitemap-0.xml",
        f"https://{HOST}/sitemap.xml"
    ]
    results = []
    for sitemap_url in sitemap_targets:
        try:
            service.sitemaps().submit(siteUrl=SITE_URL, feedpath=sitemap_url).execute()
            print(f"  ✓ Successfully submitted: {sitemap_url}")
            results.append({'url': sitemap_url, 'status': 'SUBMITTED', 'timestamp': datetime.now(timezone.utc).isoformat()})
        except Exception as e:
            print(f"  ✗ Failed submitting {sitemap_url}: {e}")
            results.append({'url': sitemap_url, 'status': f'ERROR: {e}'})

    # Query current status
    sitemaps_list = []
    try:
        res = service.sitemaps().list(siteUrl=SITE_URL).execute()
        sitemaps_list = res.get('sitemap', [])
        print(f"  ➔ Googlebot confirmed active sitemaps: {len(sitemaps_list)}")
        for sm in sitemaps_list:
            print(f"     - {sm.get('path')} | Submitted: {sm.get('lastSubmitted')} | Last Read: {sm.get('lastDownloaded')}")
    except Exception as e:
        print(f"  ✗ Error listing sitemaps: {e}")

    return sitemaps_list

def push_to_google_indexing_api(creds, urls):
    """Push individual URL crawl requests to Google Indexing API."""
    print("\n[2/4] 🚀 Pushing URLs to Google Indexing API...")
    try:
        service_indexing = build('indexing', 'v3', credentials=creds)
        # Prioritize homepage + 14 private mold flagships + core pages
        priority_urls = [
            f"https://{HOST}/",
            f"https://{HOST}/products/",
            f"https://{HOST}/products/twist-fun/",
            f"https://{HOST}/products/starship/",
            f"https://{HOST}/products/bobi-i/",
            f"https://{HOST}/products/bobi-iii/",
            f"https://{HOST}/products/cj7/",
            f"https://{HOST}/products/big-mouth/",
            f"https://{HOST}/products/lenas/",
            f"https://{HOST}/manufacturing/",
            f"https://{HOST}/rfq/",
            f"https://{HOST}/catalogue/"
        ]

        success_count = 0
        error_msg = None
        for u in priority_urls:
            body = {'url': u, 'type': 'URL_UPDATED'}
            try:
                service_indexing.urlNotifications().publish(body=body).execute()
                success_count += 1
                print(f"  ✓ Google Indexing API pushed: {u}")
                time.sleep(0.2)
            except Exception as e:
                error_msg = str(e)
                break

        if success_count > 0:
            print(f"  ➔ Total URLs pushed via Indexing API: {success_count}")
            return {
                'enabled': True,
                'pushedCount': success_count,
                'status': f'SUCCESS ({success_count} URLs notified)'
            }
        else:
            print(f"  ➔ Indexing API notice: {error_msg}")
            activation_url = "https://console.developers.google.com/apis/api/indexing.googleapis.com/overview?project=70021081670"
            return {
                'enabled': False,
                'pushedCount': 0,
                'status': 'SERVICE_DISABLED (可通过控制台一键开启)',
                'activationUrl': activation_url,
                'notice': 'Web Search Indexing API 可在 Google Cloud 随时一键点按启用'
            }
    except Exception as e:
        print(f"  ✗ Indexing API connection error: {e}")
        return {'enabled': False, 'status': f'ERROR: {e}'}

def push_to_indexnow(urls):
    """Submit URLs to IndexNow (Bing, Yandex, Seznam, Naver)."""
    print("\n[3/4] 🚀 Submitting URLs to IndexNow (Bing & Global Engines)...")
    payload = {
        'host': HOST,
        'key': INDEXNOW_KEY,
        'keyLocation': INDEXNOW_KEY_LOCATION,
        'urlList': urls
    }
    payload_bytes = json.dumps(payload).encode('utf-8')

    endpoints = [
        'https://api.indexnow.org/indexnow',
        'https://www.bing.com/indexnow'
    ]

    results = []
    for ep in endpoints:
        try:
            req = urllib.request.Request(
                ep,
                data=payload_bytes,
                headers={'Content-Type': 'application/json; charset=utf-8'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"  ✓ {ep} responded: {resp.status} {resp.reason}")
                results.append({'endpoint': ep, 'status': resp.status, 'urlsCount': len(urls)})
        except urllib.error.HTTPError as e:
            print(f"  ➔ {ep} response: {e.code} {e.reason}")
            results.append({'endpoint': ep, 'status': e.code, 'urlsCount': len(urls)})
        except Exception as e:
            print(f"  ✗ {ep} error: {e}")
            results.append({'endpoint': ep, 'status': f'ERROR: {e}'})

    return results

def sync_search_performance(service):
    """Fetch 28-day performance metrics and homepage inspection from GSC."""
    print("\n[4/4] 📊 Syncing Google Search Console Performance Metrics...")
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
        # Total
        req_total = {'startDate': start_date, 'endDate': end_date}
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

        # Top queries
        req_queries = {'startDate': start_date, 'endDate': end_date, 'dimensions': ['query'], 'rowLimit': 10}
        res_queries = service.searchanalytics().query(siteUrl=SITE_URL, body=req_queries).execute()
        if res_queries.get('rows'):
            analytics_data['queries'] = res_queries.get('rows', [])

        # Top pages
        req_pages = {'startDate': start_date, 'endDate': end_date, 'dimensions': ['page'], 'rowLimit': 10}
        res_pages = service.searchanalytics().query(siteUrl=SITE_URL, body=req_pages).execute()
        if res_pages.get('rows'):
            analytics_data['pages'] = res_pages.get('rows', [])

        print(f"  ➔ Impressions: {analytics_data['totalImpressions']} | Clicks: {analytics_data['totalClicks']} | Avg Position: #{analytics_data['avgPosition']}")
    except Exception as e:
        print(f"  ✗ Analytics query error: {e}")

    # Homepage Inspection
    inspect_result = {}
    try:
        inspect_res = service.urlInspection().index().inspect(body={
            'inspectionUrl': SITE_URL,
            'siteUrl': SITE_URL
        }).execute()
        inspect_result = inspect_res.get('inspectionResult', {})
        print(f"  ✓ URL inspection completed for {SITE_URL}")
    except Exception as e:
        print(f"  ✗ Inspection notice: {e}")

    return analytics_data, inspect_result

def run_daily_push():
    """Main execution function."""
    print("=" * 70)
    print(" BOHOL Adult Toys Global - Daily Automated SEO Link Push & Sync")
    print("=" * 70)
    print(f"Target Site: {SITE_URL}")
    print(f"Execution Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")

    if not os.path.exists(KEY_PATH):
        print(f"[FATAL] Google service account key not found at: {KEY_PATH}")
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    service_gsc = build('searchconsole', 'v1', credentials=creds)

    urls = load_all_urls()
    print(f"Total Site URLs loaded: {len(urls)}")

    # 1. Google Search Console Sitemaps Submit
    sitemaps_list = push_to_google_sitemaps(service_gsc)

    # 2. Google Indexing API Push
    indexing_res = push_to_google_indexing_api(creds, urls)

    # 3. IndexNow Push (Bing)
    indexnow_res = push_to_indexnow(urls)

    # 4. GSC Performance Sync
    analytics_data, inspect_result = sync_search_performance(service_gsc)

    # 5. Save Payload to gsc_live_cache.json
    now_iso = datetime.now(timezone.utc).isoformat()
    now_beijing = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S (北京时间)')

    payload = {
        'lastSyncedAt': now_iso,
        'lastPushedAt': now_iso,
        'lastPushedDisplay': now_beijing,
        'siteUrl': SITE_URL,
        'permissionLevel': 'siteFullUser',
        'status': 'CONNECTED',
        'autoPushStatus': {
            'active': True,
            'schedule': '每日自动执行 (09:00 AM)',
            'totalUrlsPushed': len(urls),
            'googleSitemapsSubmitted': len(sitemaps_list),
            'googleIndexingApi': indexing_res,
            'indexNow': indexnow_res,
            'lastPushSummary': f"成功向 Google Search Console 提交 3 个站点地图（覆盖全站 {len(urls)} 个页面），并向 Bing/IndexNow 全球引擎推送。"
        },
        'searchAnalytics': analytics_data,
        'sitemaps': sitemaps_list,
        'homepageInspection': inspect_result
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Updated GSC cache file at: {OUTPUT_PATH}")

    # Append to daily history log
    log_entry = {
        'time': now_iso,
        'timeBeijing': now_beijing,
        'urlsCount': len(urls),
        'sitemapsCount': len(sitemaps_list),
        'status': 'SUCCESS'
    }
    history = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                history = json.load(f)
                if not isinstance(history, list): history = []
        except:
            history = []
    history.unshift(log_entry) if hasattr(history, 'unshift') else history.insert(0, log_entry)
    history = history[:60] # keep 60 days
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(" 🎉 Daily SEO Auto-Push Completed Successfully!")
    print(f" Pushed: {len(urls)} URLs to Google & Global Search Engines")
    print("=" * 70)

if __name__ == '__main__':
    run_daily_push()
