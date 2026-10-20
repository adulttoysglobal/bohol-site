@echo off
chcp 65001 > nul
cd /d "C:\Users\admin\.gemini\antigravity\scratch\bohol-site"
echo [BOHOL] Launching Automated SEO Article & Agnes AI Image Publisher...
"C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe" "scripts\auto_seo_publisher.py" >> "scripts\auto_publisher.log" 2>&1
echo [BOHOL] Daily cycle completed. See scripts\auto_publisher.log for details.
