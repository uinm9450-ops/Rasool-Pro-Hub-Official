import os
import subprocess
import time

# المسارات الأساسية
BASE_DIR = r"C:\Users\HP\Desktop\Rasoolprohub"
DESKTOP_PATH = r"C:\Users\HP\Desktop"
BACKEND_DIR = os.path.join(BASE_DIR, "rasool", "backend")

def find_react_folder(start_path):
    """البحث عن المجلد الذي يحتوي على package.json الخاص بالفرونتند"""
    print(f"--- جاري البحث عن مجلد React في: {start_path} ---")
    for root, dirs, files in os.walk(start_path):
        # نتجاهل مجلدات node_modules لتسريع البحث
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        
        if "package.json" in files:
            # نتأكد أنه مجلد فرونتند وليس باكيند (إذا كان الباكيند يحتوي عليه أيضاً)
            if "src" in dirs or "vite.config" in str(files):
                return root
    return None

def update_bat_file(frontend_path):
    """تحديث ملف الـ Batch على سطح المكتب لتشغيل المشروع كاملاً"""
    bat_path = os.path.join(DESKTOP_PATH, "Run_My_Cyber_Site.bat")
    
    bat_content = f"""@echo off
title Rasool Pro Hub - Full System
echo --- Starting Backend Server ---
start cmd /k "cd /d {BACKEND_DIR} && echo Starting Backend... && python main.py"

echo --- Starting Frontend Server ---
start cmd /k "cd /d {frontend_path} && echo Installing Dependencies... && npm install && echo Starting Frontend... && npm run dev"

echo.
echo [OK] Both servers are starting in separate windows.
pause
"""
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print(f"[+] تم تحديث ملف التشغيل على سطح المكتب: {bat_path}")

def main():
    frontend_dir = find_react_folder(BASE_DIR)
    
    if not frontend_dir:
        print("[!] خطأ: لم يتم العثور على مجلد يحتوي على package.json")
        return

    print(f"[+] تم العثور على الفرونتند في: {frontend_dir}")
    
    # تحديث ملف الـ Batch
    update_bat_file(frontend_dir)
    
    # تشغيل الفرونتند فوراً في نافذة جديدة
    print("[+] جاري تشغيل الفرونتند في نافذة جديدة...")
    command = f'start cmd /k "cd /d {frontend_dir} && npm install && npm run dev"'
    os.system(command)
    
    print("\n--- تمت المهمة! يمكنك الآن استخدام ملف الـ Batch من سطح المكتب لاحقاً ---")

if __name__ == "__main__":
    main()
