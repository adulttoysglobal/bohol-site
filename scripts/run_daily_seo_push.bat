@echo off
chcp 65001 > nul
cd /d "C:\Users\admin\.gemini\antigravity\scratch\bohol-site"
"C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe" "scripts\daily_seo_pusher.py" >> "scripts\daily_push.log" 2>&1
