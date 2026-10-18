import os
import sys

# Ensure scripts directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_50_industry_articles import write_article, JOURNAL_DIR
from data_p1 import P1_ARTICLES
from data_p2 import P2_ARTICLES
from data_p3 import P3_ARTICLES
from data_p4 import P4_ARTICLES
from data_p5 import P5_ARTICLES
from data_p6 import P6_ARTICLES

all_articles = (
    P1_ARTICLES +
    P2_ARTICLES +
    P3_ARTICLES +
    P4_ARTICLES +
    P5_ARTICLES +
    P6_ARTICLES
)

print(f"Total articles to write: {len(all_articles)}")
assert len(all_articles) == 50, f"Expected 50 articles, got {len(all_articles)}"

# Clean out old technical/regulatory articles from the previous batch if needed,
# or write all 50 new industry articles
for i, item in enumerate(all_articles, 1):
    write_article(item, i)

print(f"\nSUCCESS: Successfully wrote all {len(all_articles)} industry-specific authoritative articles to {JOURNAL_DIR}!")
