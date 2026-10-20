import re

text = open(r'C:/Users/admin/.gemini/antigravity/brain/ce49dcba-cdec-4437-9044-20d7b878bc29/.system_generated/steps/3303/content.md', encoding='utf-8', errors='ignore').read()
# find curl or codeblocks
code_blocks = re.findall(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', text, re.DOTALL)
for i, c in enumerate(code_blocks):
    clean = re.sub(r'<[^>]+>', '', c)
    if 'images/generations' in clean or 'agnes-image' in clean or 'prompt' in clean:
        print(f"=== Code Block {i} ===")
        print(clean[:800])
