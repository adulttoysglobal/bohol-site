import os, glob, re

img_pattern = re.compile(r'["\'](/(?:images|assets)/[^"\']+\.(?:webp|png|jpg|jpeg|svg|gif))["\']')
missing_refs = set()

for root, dirs, files in os.walk('src'):
    for f in files:
        if f.endswith(('.astro', '.md', '.ts', '.js', '.json')):
            path = os.path.join(root, f)
            try:
                text = open(path, encoding='utf-8', errors='ignore').read()
                for match in img_pattern.findall(text):
                    clean = match.lstrip('/')
                    local_path = os.path.join('public', clean)
                    if not os.path.exists(local_path):
                        missing_refs.add((match, path))
            except Exception as e:
                pass

print(f"Total missing image references: {len(missing_refs)}")
for m, p in sorted(missing_refs):
    print(f"{m}  <-- {p}")
