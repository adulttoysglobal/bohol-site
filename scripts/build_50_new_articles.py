import os
import sys
import json

# Ensure scripts directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_batch2_p1 import BATCH2_P1_ARTICLES
from data_batch2_p2 import BATCH2_P2_ARTICLES
from data_batch2_p3 import BATCH2_P3_ARTICLES
from data_batch2_p4 import BATCH2_P4_ARTICLES
from data_batch2_p5 import BATCH2_P5_ARTICLES

JOURNAL_DIR = r"C:\Users\admin\.gemini\antigravity\scratch\bohol-site\src\data\journal"
os.makedirs(JOURNAL_DIR, exist_ok=True)

all_new_articles = (
    BATCH2_P1_ARTICLES +
    BATCH2_P2_ARTICLES +
    BATCH2_P3_ARTICLES +
    BATCH2_P4_ARTICLES +
    BATCH2_P5_ARTICLES
)

print(f"Total new articles to generate: {len(all_new_articles)}")
assert len(all_new_articles) == 50, f"Expected 50 articles, got {len(all_new_articles)}"

def write_article(item, order_num):
    slug = item["slug"]
    filepath = os.path.join(JOURNAL_DIR, f"{slug}.md")

    # Generate table markdown
    table_md = ""
    if "table_headers" in item and "table_rows" in item:
        headers = " | ".join(item["table_headers"])
        divider = " | ".join([":---" for _ in item["table_headers"]])
        rows_str = "\n".join(["| " + " | ".join(row) + " |" for row in item["table_rows"]])
        table_md = f"| {headers} |\n| {divider} |\n{rows_str}\n"

    # Takeaways list
    takeaways_md = "\n".join([f"- **{t.split(':')[0] if ':' in t else t[:30]}**: {t}" if ':' in t else f"- {t}" for t in item["takeaways"]])

    content = f"""---
title: "{item['title']}"
description: "{item['description']}"
category: "{item['category']}"
image: "{item['image']}"
order: {order_num}
readTime: "{item['readTime']}"
pubDate: "{item['pubDate']}"
author: "Alex Chen"
tags: {json.dumps(item['tags'])}
featured: {str(item.get('featured', False)).lower()}
seoKeywords: "{item['seoKeywords']}"
---

{item['overview']}

> [!NOTE]
> Looking for audited, biocompatible manufacturing? Explore the [{item['product_name']}]({item['product_link']}) or review our [cleanroom manufacturing specifications](/manufacturing/) to request an [instant factory quotation](/rfq/).

<section class="geo-executive-summary" style="background:#f8fafc; border-left:4px solid #0284c7; padding:1.25rem 1.5rem; margin:1.75rem 0; border-radius:0 8px 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
<h3 style="margin-top:0; color:#0f172a; font-size:1.1rem; font-weight:700;">Executive Engineering & Procurement Takeaways</h3>
{takeaways_md}
</section>

## {item['h2_1']}

{item['body_1']}

## {item['h2_2']}

{item['body_2']}

{table_md}

<div style="margin: 2rem 0; background: #ffffff; border-left: 4px solid #0284c7; padding: 18px 24px; border-radius: 0 12px 12px 0; box-shadow: 0 2px 8px rgba(15,23,42,0.04);">
  <blockquote style="margin: 0; font-size: 14px; line-height: 1.7; color: #334155;">
    "All hardware mechanisms and intimate formulations produced by BOHOL strictly conform to audited ISO 13485:2016 quality management systems and FDA 21 CFR § 177.2600 liquid silicone elastomer biocompatibility standards. Every production batch undergoes automated acoustic analysis, high-voltage insulation tests, and IPX7 vacuum immersion verification."
    <footer style="margin-top: 8px; font-size: 12.5px; color: #64748b; font-weight: 600;">
      — Audited under <a href="https://www.iso.org/standard/59752.html" target="_blank" rel="noopener noreferrer" style="color: #0284c7; text-decoration: underline;">ISO 13485:2016</a> &amp; <a href="https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/cfrsearch.cfm?fr=177.2600" target="_blank" rel="noopener noreferrer" style="color: #0284c7; text-decoration: underline;">FDA 21 CFR § 177.2600</a>
    </footer>
  </blockquote>
</div>

## Frequently Asked Questions

### {item['faq_q1']}
{item['faq_a1']}

### {item['faq_q2']}
{item['faq_a2']}

---
*For direct wholesale procurement, custom private tooling, or hotel vending telemetry deployments, connect directly with our engineering trade desk via our [online RFQ calculator](/rfq/), explore our [cleanroom manufacturing campus](/manufacturing/), or reach our global team at our [official contact desk](/contact/).*
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated ({order_num}): {slug}.md")

# Start ordering from 60 up to 109
for idx, item in enumerate(all_new_articles, start=60):
    write_article(item, idx)

print(f"\nSUCCESS: Successfully generated all {len(all_new_articles)} new high-quality articles in {JOURNAL_DIR}!")
