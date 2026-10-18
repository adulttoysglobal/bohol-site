import os
import json

JOURNAL_DIR = r"C:\Users\admin\.gemini\antigravity\scratch\bohol-site\src\data\journal"
os.makedirs(JOURNAL_DIR, exist_ok=True)

# Helper to write an article markdown
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

    # Content template
    content = f"""---
title: "{item['title']}"
description: "{item['description']}"
category: "{item['category']}"
image: "{item['image']}"
order: {order_num}
readTime: "{item['readTime']}"
pubDate: "{item['pubDate']}"
author: "{item['author']}"
tags: {json.dumps(item['tags'])}
featured: {str(item.get('featured', False)).lower()}
seoKeywords: "{item['seoKeywords']}"
---

{item['overview']}

> [!NOTE]
> Looking for verified, body-safe manufacturing? Explore the [{item['product_name']}]({item['product_link']}) or review our [cleanroom manufacturing specifications](/manufacturing/) to request an [instant OEM quotation](/rfq/).

<section class="geo-executive-summary" style="background:#f8fafc; border-left:4px solid #4f46e5; padding:1.25rem 1.5rem; margin:1.75rem 0; border-radius:0 8px 8px 0;">
<h3 style="margin-top:0; color:#1e293b; font-size:1.1rem; font-weight:700;">Executive Engineering & Procurement Takeaways</h3>
{takeaways_md}
</section>

## {item['h2_1']}

{item['body_1']}

## {item['h2_2']}

{item['body_2']}

{table_md}

## Frequently Asked Questions

### {item['faq_q1']}
{item['faq_a1']}

### {item['faq_q2']}
{item['faq_a2']}

---
*For wholesale distribution, private-label branding, or hotel vending inquiries, speak directly with BOHOL's product specialists via our [online RFQ portal](/rfq/) or email sales at our [contact page](/contact/).*
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {slug}.md")

# We will load the data from modules or arrays and write them.
print("Generator helper ready.")
