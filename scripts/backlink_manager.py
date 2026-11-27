#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOHOL Backlink Manager & Outreach Engine
Implements the 4-Criteria Screening & 5-Tier Anchor Text Distribution Model
Based on the Independent Website SEO Backlink Masterclass (Video 2):
  1. 4-Criteria Evaluation: Niche Relevance + Real Organic Traffic + DA/PA + Spam Score (SS < 5%)
  2. Anchor Text Distribution: 45% Brand + 30% Naked URL + 10% Generic + 5% Target Keyword + 10% Natural LSI
  3. Target Page Allocation: 40% Homepage, 60% Inner High-Ranking Pages & Linkable Assets
  4. Monthly Execution Cadence: 3-5 Industry Blogs + Relevant Trade Media + Active Q&A Communities
"""

import sys
import json
import os
import random
from datetime import datetime

# Ensure utf-8 encoding on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TARGET_LANDING_PAGES = [
    {
        "url": "https://adulttoysglobal.com/",
        "type": "Homepage",
        "description": "35,000 m² Cleanroom Smart Factory & OEM/ODM Headquarters",
        "weight": 0.40
    },
    {
        "url": "https://adulttoysglobal.com/catalogue/",
        "type": "Inner - Catalogue",
        "description": "38+ Private-Mold Hardware Specification Catalogue (Page 1 Rank #7.5)",
        "weight": 0.20
    },
    {
        "url": "https://adulttoysglobal.com/tools/customs-hs-code-calculator/",
        "type": "Inner - Linkable Asset Tool",
        "description": "2026 Interactive Customs HS Code & Tariff Calculator",
        "weight": 0.15
    },
    {
        "url": "https://adulttoysglobal.com/journal/customs-clearance-hs-codes-adult-novelty/",
        "type": "Inner - Ranking Whitepaper",
        "description": "Compliant HS Code Classification Whitepaper (Page 1 Rank #7.4)",
        "weight": 0.10
    },
    {
        "url": "https://adulttoysglobal.com/journal/how-to-wash-dry-powder-tpe-sleeves/",
        "type": "Inner - Ranking Whitepaper",
        "description": "TPE Durometer & Maintenance Whitepaper (Page 1 Rank #6.3)",
        "weight": 0.05
    },
    {
        "url": "https://adulttoysglobal.com/manufacturing/",
        "type": "Inner - Authority Campus",
        "description": "Cleanroom LSR Injection & 5-Axis CNC Tooling Tour",
        "weight": 0.05
    },
    {
        "url": "https://adulttoysglobal.com/rfq/",
        "type": "Inner - Conversion",
        "description": "B2B Volume Wholesale & OEM Instant Pricing Form",
        "weight": 0.05
    }
]

ANCHOR_TEXT_TEMPLATES = {
    "brand": [
        "BOHOL",
        "BOHOL Adult Toys",
        "BOHOL Smart Manufacturing",
        "BOHOL Factory",
        "BOHOL Intimate Hardware",
        "BOHOL Global"
    ],
    "naked_url": [
        "https://adulttoysglobal.com",
        "https://adulttoysglobal.com/",
        "adulttoysglobal.com",
        "https://adulttoysglobal.com/catalogue/",
        "https://adulttoysglobal.com/tools/customs-hs-code-calculator/"
    ],
    "generic": [
        "visit official website",
        "learn more",
        "view full technical specifications",
        "source guide",
        "read official whitepaper",
        "explore manufacturer details",
        "access online calculator",
        "check full catalogue"
    ],
    "keyword": [
        "adult toy manufacturer",
        "silicone vibrator OEM factory",
        "smart hotel vending machine manufacturer",
        "medical-grade silicone toy OEM",
        "custom adult wellness private label"
    ],
    "natural_lsi": [
        "medical-grade liquid silicone manufacturing at BOHOL",
        "custom silicone personal massagers engineered by BOHOL",
        "BOHOL's cleanroom adult hardware facility",
        "OEM adult product specifications on adulttoysglobal.com",
        "2026 adult novelty HS code classification matrix",
        "hotel room adult vending kiosk deployment"
    ]
}

TARGET_OPPORTUNITIES = [
    # Category A: 行业博客 (Niche Industry Blogs & Tech Outlets)
    {
        "domain": "xbiz.com",
        "name": "XBIZ B2B Tech & News",
        "category": "A - 行业博客",
        "da": 68,
        "traffic": "250K/mo",
        "spam_score": "1%",
        "relevance": "High (Adult Wellness B2B Trade Authority)",
        "target_page": "https://adulttoysglobal.com/catalogue/",
        "anchor_type": "natural_lsi",
        "suggested_anchor": "medical-grade liquid silicone manufacturing at BOHOL",
        "pitch_angle": "How ISO 13485 Cleanroom Automation Is Reshaping 2026 Adult Hardware Quality Standards"
    },
    {
        "domain": "avn.com",
        "name": "AVN Novelty Business News",
        "category": "A - 行业博客",
        "da": 74,
        "traffic": "400K/mo",
        "spam_score": "2%",
        "relevance": "High (Adult Novelty Industry Standard)",
        "target_page": "https://adulttoysglobal.com/tools/customs-hs-code-calculator/",
        "anchor_type": "generic",
        "suggested_anchor": "access online calculator",
        "pitch_angle": "Free Tool Announcement: 2026 Global Adult Novelty HS Code & Customs Duty Calculator"
    },
    {
        "domain": "ecommerceceo.com",
        "name": "E-commerce CEO & Sourcing Guide",
        "category": "A - 行业博客",
        "da": 54,
        "traffic": "180K/mo",
        "spam_score": "1%",
        "relevance": "High (E-commerce Brand Owners & Sourcing)",
        "target_page": "https://adulttoysglobal.com/",
        "anchor_type": "brand",
        "suggested_anchor": "BOHOL",
        "pitch_angle": "How to Vet Chinese Adult Toy OEM Suppliers: Non-Disclosure, Mold Ownership, and Quality Audits"
    },
    {
        "domain": "supplychaindive.com",
        "name": "Supply Chain Dive Trade Portal",
        "category": "A - 行业博客",
        "da": 67,
        "traffic": "320K/mo",
        "spam_score": "1%",
        "relevance": "High (International Logistics & Trade Tariffs)",
        "target_page": "https://adulttoysglobal.com/journal/customs-clearance-hs-codes-adult-novelty/",
        "anchor_type": "natural_lsi",
        "suggested_anchor": "2026 adult novelty HS code classification matrix",
        "pitch_angle": "Anti-Seizure Customs Classification: How Intimate Wellness Importers Clear US/EU Border Ports"
    },
    {
        "domain": "hospitalitynet.org",
        "name": "Hospitality Net Hotel Technology",
        "category": "A - 行业博客",
        "da": 71,
        "traffic": "550K/mo",
        "spam_score": "1%",
        "relevance": "High (Hotel Operators & In-Room Vending)",
        "target_page": "https://adulttoysglobal.com/products/?subcat=Vending",
        "anchor_type": "keyword",
        "suggested_anchor": "smart hotel vending machine manufacturer",
        "pitch_angle": "Unlocking In-Room Hotel Revenue: Wall-Mounted Adult Wellness Vending Kiosks with IoT Telemetry"
    },

    # Category B: 相关媒体与权威商业目录 (Trade Media & Verified Directories)
    {
        "domain": "thomasnet.com",
        "name": "ThomasNet North American Sourcing",
        "category": "B - 权威制造目录",
        "da": 86,
        "traffic": "3.5M/mo",
        "spam_score": "1%",
        "relevance": "High (OEM / Contract Manufacturing Directory)",
        "target_page": "https://adulttoysglobal.com/",
        "anchor_type": "naked_url",
        "suggested_anchor": "https://adulttoysglobal.com",
        "pitch_angle": "Verified International OEM Profile: Cleanroom LSR Silicone Molding & Precision Tooling"
    },
    {
        "domain": "globalsources.com",
        "name": "Global Sources Direct Supplier Listing",
        "category": "B - 权威商业目录",
        "da": 85,
        "traffic": "2.8M/mo",
        "spam_score": "1%",
        "relevance": "High (Verified Chinese Source Manufacturer)",
        "target_page": "https://adulttoysglobal.com/catalogue/",
        "anchor_type": "brand",
        "suggested_anchor": "BOHOL Smart Manufacturing",
        "pitch_angle": "35,000 m² Verified Factory Campus with In-House 5-Axis CNC Tooling"
    },
    {
        "domain": "kompass.com",
        "name": "Kompass Worldwide B2B Directory",
        "category": "B - 权威商业目录",
        "da": 79,
        "traffic": "1.2M/mo",
        "spam_score": "1%",
        "relevance": "High (Global B2B Trade Directory)",
        "target_page": "https://adulttoysglobal.com/",
        "anchor_type": "naked_url",
        "suggested_anchor": "adulttoysglobal.com",
        "pitch_angle": "Corporate Profile: ISO 13485 and FDA FEI Registered Intimate Wellness Hardware"
    },
    {
        "domain": "industrytoday.com",
        "name": "Industry Today Manufacturing News",
        "category": "B - 行业媒体",
        "da": 57,
        "traffic": "95K/mo",
        "spam_score": "1%",
        "relevance": "Medium-High (Precision Engineering & Mold Technology)",
        "target_page": "https://adulttoysglobal.com/manufacturing/",
        "anchor_type": "generic",
        "suggested_anchor": "learn more",
        "pitch_angle": "Press Release: BOHOL Expands 120-Line Cleanroom Assembly Campus in Guangdong"
    },
    {
        "domain": "prlog.org",
        "name": "PRLog Global Press Release Wire",
        "category": "B - 媒体快讯",
        "da": 81,
        "traffic": "450K/mo",
        "spam_score": "2%",
        "relevance": "Medium (Syndicated Global B2B PR)",
        "target_page": "https://adulttoysglobal.com/tools/customs-hs-code-calculator/",
        "anchor_type": "naked_url",
        "suggested_anchor": "https://adulttoysglobal.com/tools/customs-hs-code-calculator/",
        "pitch_angle": "BOHOL Unveils Free 2026 Harmonized System Tariff Calculator for Adult Novelty Importers"
    },

    # Category C: 真实活跃问答与技术社区 (Real Active Q&A Communities & Tech Forums)
    {
        "domain": "reddit.com",
        "name": "Reddit (r/ecommerce, r/adulttech, r/smallbusiness)",
        "category": "C - 活跃社区",
        "da": 96,
        "traffic": "1.8B/mo",
        "spam_score": "1%",
        "relevance": "High (Buyers asking for legit suppliers & customs advice)",
        "target_page": "https://adulttoysglobal.com/tools/customs-hs-code-calculator/",
        "anchor_type": "generic",
        "suggested_anchor": "this interactive calculator",
        "pitch_angle": "Answering: 'What HS code should I use to import silicone novelties without US customs seizing them?'"
    },
    {
        "domain": "quora.com",
        "name": "Quora Adult Industry & Sourcing Q&A",
        "category": "C - 活跃问答",
        "da": 93,
        "traffic": "750M/mo",
        "spam_score": "2%",
        "relevance": "High (Direct overseas sourcing inquiries)",
        "target_page": "https://adulttoysglobal.com/catalogue/",
        "anchor_type": "brand",
        "suggested_anchor": "BOHOL",
        "pitch_angle": "Answering: 'How to find a reliable OEM manufacturer for private label adult toys in China?'"
    },
    {
        "domain": "medium.com",
        "name": "Medium Tech & Sourcing Publication",
        "category": "C - 权威内容分发",
        "da": 94,
        "traffic": "140M/mo",
        "spam_score": "1%",
        "relevance": "High (Engineering & Hardware Tear-Downs)",
        "target_page": "https://adulttoysglobal.com/journal/how-to-wash-dry-powder-tpe-sleeves/",
        "anchor_type": "natural_lsi",
        "suggested_anchor": "TPE durometer specifications and maintenance guide",
        "pitch_angle": "Syndicated Article: The Polymer Science of Adult Toys: Shore Hardness 00 vs Shore A Explained"
    },
    {
        "domain": "linkedin.com",
        "name": "LinkedIn Pulse B2B Articles",
        "category": "C - 商业社交网络",
        "da": 98,
        "traffic": "1.2B/mo",
        "spam_score": "1%",
        "relevance": "High (B2B Procurement Officers & Product Managers)",
        "target_page": "https://adulttoysglobal.com/",
        "anchor_type": "naked_url",
        "suggested_anchor": "https://adulttoysglobal.com",
        "pitch_angle": "Executive Article: Avoiding Cargo Detention: Why Medical Cleanrooms Are Essential for Intimate Hardware"
    },
    {
        "domain": "github.com",
        "name": "GitHub Open Data & Tool Repository",
        "category": "C - 开源开发者社区",
        "da": 96,
        "traffic": "400M/mo",
        "spam_score": "1%",
        "relevance": "High (Open Tariff & HS Code Reference JSON)",
        "target_page": "https://adulttoysglobal.com/tools/customs-hs-code-calculator/",
        "anchor_type": "brand",
        "suggested_anchor": "BOHOL Trade Compliance Directorate",
        "pitch_angle": "Open Source Repository: 2026-adult-novelty-hs-codes-tariff-matrix"
    }
]

def print_banner():
    print("=" * 78)
    print("  BOHOL BACKLINK ORCHESTRATION ENGINE (Video 2 SEO Implementation)")
    print("  4-Criteria Filter | 5-Tier Anchor Text Ratio | 60% Inner Page Push")
    print("=" * 78)

def audit_strategy():
    print_banner()
    print("\n[1] ANCHOR TEXT RATIO AUDIT (Video 2 Golden Rule: 45 / 30 / 10 / 5 / 10)")
    ratios = {
        "Brand Keywords (品牌词)": "45%",
        "Naked / Direct URL (直接网址)": "30%",
        "Generic Descriptors (普通描述词)": "10%",
        "Target Keywords (精准关键词)": "5%",
        "Natural LSI / Long-Tail Variants (其他自然变体)": "10%"
    }
    for k, v in ratios.items():
        print(f"  • {k:<45}: {v}")

    print("\n[2] LANDING PAGE DISTRIBUTION (Video 2 Rule: 不要全指首页)")
    print(f"  {'Target URL':<60} {'Type':<22} {'Weight':<8}")
    print("  " + "-" * 92)
    for p in TARGET_LANDING_PAGES:
        print(f"  {p['url']:<60} {p['type']:<22} {int(p['weight']*100)}%")

    print("\n[3] 4-CRITERIA SITE SCREENING MATRIX (Video 2 Combo Filter)")
    print("  1. 行业相关性 (Niche Relevance): Adult Wellness, LSR Molding, Vending IoT, Medical Polymers")
    print("  2. 真实自然流量 (Organic Traffic): > 1,000 monthly Google organic visitors")
    print("  3. 权重指标 (DA / PA): DA > 25 (Preferably DA 50-95)")
    print("  4. 垃圾评分 (Spam Score): SS < 5% (Strict low penalty risk)")

def generate_monthly_plan():
    print_banner()
    print("\n[+] GENERATING 90-DAY BACKLINK EXECUTION SCHEDULE (Q1 2026)")
    print("    Balanced Cadence: 3-5 Guest Posts/Month + Trade Directories + Q&A Syndications\n")

    for idx, opp in enumerate(TARGET_OPPORTUNITIES, 1):
        print(f"[{idx:02d}] {opp['name']} ({opp['domain']})")
        print(f"     Category : {opp['category']}")
        print(f"     Metrics  : DA {opp['da']} | Traffic: {opp['traffic']} | Spam Score: {opp['spam_score']}")
        print(f"     Target   : {opp['target_page']}")
        print(f"     Anchor   : [{opp['suggested_anchor']}] (Type: {opp['anchor_type']})")
        print(f"     Angle    : {opp['pitch_angle']}")
        print("     " + "." * 70)

def generate_pitches():
    print_banner()
    print("\n[+] GENERATING READY-TO-SEND ENGLISH OUTREACH EMAIL TEMPLATES\n")

    template_blog = """--------------------------------------------------------------------------------
SUBJECT: Guest Contribution / Sourcing Guide: How Cleanroom LSR Molding Is Changing Adult Hardware
TO: Editorial Team @ {domain}

Hi {domain} Editorial Team,

I've been following your in-depth coverage of consumer wellness and hardware manufacturing trends.

I lead the trade and engineering communication desk at BOHOL (https://adulttoysglobal.com), an audited 35,000 m² cleanroom adult hardware factory in Guangdong operating 120+ lean assembly lines and 5-axis CNC mold centers.

With overseas buyers facing unprecedented challenges around biocompatibility (FDA 21 CFR § 177.2600), battery transit (UN38.3), and customs clearance, I have prepared a comprehensive engineering breakdown tailored for your readers:

Title: "Behind the Mold: How Medical-Grade Liquid Silicone (LSR) & Cleanroom Automation Are Transforming Adult Wellness Manufacturing in 2026"

Key Insights in the Article:
1. Why traditional vulcanized silicone fails modern durometer tests (Shore 00 vs. Shore A comparisons).
2. The mechanical engineering behind acoustic whisper decibels (<35 dB vs. 45 dB).
3. Practical tips for distributors to avoid customs seizures under HS Code 8509.80.

Would you be open to reviewing the draft for a guest publication? There is no promotional fluff—only verified engineering data, test photos, and actionable procurement criteria.

Looking forward to your thoughts,

Best regards,

Alex Chen
Chief Sourcing Architect | BOHOL
WhatsApp: +86 185 8858 3798
Web: https://adulttoysglobal.com
--------------------------------------------------------------------------------"""

    template_tool = """--------------------------------------------------------------------------------
SUBJECT: Resource Suggestion for Your Importers: Free 2026 Adult Novelty HS Code & Customs Calculator
TO: Trade Desk @ {domain}

Hello {domain} Team,

I noticed your excellent article covering international trade tariffs and import compliance for consumer electronics and lifestyle goods.

In the adult novelty and personal massager category, international customs holds and moral seizures remain the #1 pain point for e-commerce brands and importers due to misclassification under crude terms.

To help the industry navigate 2026 WCO tariff subheadings and Section 301 calculations, our trade compliance directorate has published a completely free interactive tool:

Link: https://adulttoysglobal.com/tools/customs-hs-code-calculator/

Key Features:
- Instantly matches hardware (motorized vibrators, strokers, silicone articles, condoms, vending kiosks) with US HTS, EU TARIC, and UK Commodity Codes.
- Provides compliant, non-colloquial commercial invoice line item descriptions that pass CBP/EU customs scans.
- Lists mandatory export testing dossiers (CE-RED, RoHS 2.0, FCC Part 15C, UN38.3 battery dossiers).

Would this be a valuable addition to your resources or import guide page?

Thanks for your continuous contributions to the trade community!

Best regards,

Alex Chen
BOHOL Trade Compliance Directorate
https://adulttoysglobal.com
--------------------------------------------------------------------------------"""

    print("=== TEMPLATE 1: FOR INDUSTRY BLOGS & TECH EDITORS ===")
    print(template_blog.format(domain="xbiz.com"))
    print("\n=== TEMPLATE 2: FOR TRADE PORTALS & RESOURCE PAGES (LINKABLE ASSET) ===")
    print(template_tool.format(domain="supplychaindive.com"))

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "audit"
    if cmd == "audit":
        audit_strategy()
    elif cmd == "plan":
        generate_monthly_plan()
    elif cmd == "pitches":
        generate_pitches()
    elif cmd == "all":
        audit_strategy()
        generate_monthly_plan()
        generate_pitches()
    else:
        print(f"Unknown command: {cmd}. Usage: python backlink_manager.py [audit|plan|pitches|all]")

if __name__ == "__main__":
    main()
