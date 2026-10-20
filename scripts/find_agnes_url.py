import re

for step in [3299, 3303, 3314]:
    path = f"C:/Users/admin/.gemini/antigravity/brain/ce49dcba-cdec-4437-9044-20d7b878bc29/.system_generated/steps/{step}/content.md"
    try:
        text = open(path, encoding='utf-8', errors='ignore').read()
        print(f"=== Step {step} ===")
        # search for curl or api. or endpoint or baseURL
        matches = re.findall(r'(https?://[a-zA-Z0-9\-\.]*(?:api|v1)[a-zA-Z0-9\-\./_]*)', text, re.IGNORECASE)
        print("Matches:", set(matches))
        # search for code snippets
        snippets = re.findall(r'(curl [^\n\<\>]+)', text)
        if snippets:
            print("Curls:", snippets[:5])
        keywords = re.findall(r'([^\n]{0,80}(?:api\.agnes|base_url|baseURL|endpoint|api_base)[^\n]{0,80})', text, re.IGNORECASE)
        if keywords:
            for k in keywords[:5]:
                print("Keyword:", k.strip())
    except Exception as e:
        print("Err:", e)
