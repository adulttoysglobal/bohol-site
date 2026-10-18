import os, re
from collections import Counter
counts = Counter()
d = r'src\data\journal'
for f in os.listdir(d):
    if f.endswith('.md'):
        with open(os.path.join(d, f), encoding='utf-8') as fp:
            txt = fp.read()
            m = re.search(r'category:\s*\"([^\"]+)\"', txt)
            if m:
                counts[m.group(1)] += 1
            else:
                counts['Other'] += 1
for k, v in counts.items():
    print(f"{k}: {v}")
