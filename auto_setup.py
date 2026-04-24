import os
import sys
import ctypes

# إعداد المسارات الأساسية - تأكد من مطابقتها لجهازك
BASE_PATH = r"C:\Users\HP\Desktop\Rasoolprohub"
BACKEND_PATH = os.path.join(BASE_PATH, "rasool", "backend")
DESKTOP_PATH = r"C:\Users\HP\Desktop"

# 1. كود منطق الأمن (security_logic.py)
SECURITY_LOGIC_CODE = """import ctypes
import os
import sys
from cryptography.fernet import Fernet

class SecurityLogic:
    def __init__(self, key_path="secret.key"):
        self.key_path = os.path.join(r"C:\\Users\\HP\\Desktop\\Rasoolprohub\\rasool\\backend", key_path)
        self.key = self._load_or_create_key()

    def _load_or_create_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f: return f.read()
        key = Fernet.generate_key()
        with open(self.key_path, "wb") as f: f.write(key)
        if sys.platform == "win32":
            ctypes.windll.kernel32.SetFileAttributesW(self.key_path, 0x02 | 0x04)
        return key

    def protect(self, filename):
        path = os.path.join(r"C:\\Users\\HP\\Desktop\\Rasoolprohub\\rasool\\backend", filename)
        if not os.path.exists(path): return False, "File not found"
        try:
            with open(path, "rb") as f: data = f.read()
            encrypted = Fernet(self.key).encrypt(data)
            with open(path, "wb") as f: f.write(encrypted)
            if sys.platform == "win32":
                ctypes.windll.kernel32.SetFileAttributesW(path, 0x02 | 0x04)
            return True, "Protected Successfully"
        except Exception as e: return False, str(e)

    def restore(self, filename):
        path = os.path.join(r"C:\\Users\\HP\\Desktop\\Rasoolprohub\\rasool\\backend", filename)
        if not os.path.exists(path): return False, "File not found"
        try:
            if sys.platform == "win32":
                ctypes.windll.kernel32.SetFileAttributesW(path, 0x80)
            with open(path, "rb") as f: data = f.read()
            decrypted = Fernet(self.key).decrypt(data)
            with open(path, "wb") as f: f.write(decrypted)
            return True, "Restored Successfully"
        except Exception as e: return False, str(e)

security_engine = SecurityLogic()
"""

def setup():
    print("--- البدء في عملية الإعداد التلقائي لنظام Rasool Pro Hub ---")

    # إنشاء ملف security_logic.py
    logic_file = os.path.join(BACKEND_PATH, "security_logic.py")
    with open(logic_file, "w", encoding="utf-8") as f:
        f.write(SECURITY_LOGIC_CODE)
    print(f"[+] تم إنشاء ملف الأمن: {logic_file}")

    # تحديث requirements.txt
    req_file = os.path.join(BACKEND_PATH, "requirements.txt")
    with open(req_file, "a+") as f:
        f.seek(0)
        content = f.read()
        if "cryptography" not in content:
            f.write("\ncryptography\n")
        if "fastapi" not in content:
            f.write("fastapi\n")
    print("[+] تم تحديث المتطلبات (requirements.txt)")

    # تعديل main.py (حقن المسارات الجديدة)
    main_file = os.path.join(BACKEND_PATH, "main.py")
    with open(main_file, "r", encoding="utf-8") as f:
        main_content = f.read()

    if "security_logic" not in main_content:
        # إضافة الاستيراد والـ Endpoints
        injection = """
# --- Cyber Security Integration ---
from security_logic import security_engine
from pydantic import BaseModel
class SecReq(BaseModel): filename: str

@app.post("/api/v1/secure/hide")
async def hide_api(req: SecReq):
    res, msg = security_engine.protect(req.filename)
    return {"status": res, "message": msg}

@app.post("/api/v1/secure/show")
async def show_api(req: SecReq):
    res, msg = security_engine.restore(req.filename)
    return {"status": res, "message": msg}
# ---------------------------------
"""
        # الحقن قبل تشغيل uvicorn
        if 'if __name__ == "__main__":' in main_content:
            main_content = main_content.replace('if __name__ == "__main__":', injection + '\nif __name__ == "__main__":')
        else:
            main_content += injection
        
        with open(main_file, "w", encoding="utf-8") as f:
            f.write(main_content)
        print("[+] تم حقن مسارات الأمان في main.py")
    else:
        print("[!] مسارات الأمان موجودة مسبقاً في main.py")

    # إنشاء ملف Batch على سطح المكتب
    bat_file = os.path.join(DESKTOP_PATH, "Run_My_Cyber_Site.bat")
    bat_content = f"""@echo off
title Rasool Pro Hub - Cyber Security Server
cd /d "{BACKEND_PATH}"
echo Starting Backend Server...
python main.py
pause
"""
    with open(bat_file, "w") as f:
        f.write(bat_content)
    print(f"[+] تم إنشاء ملف التشغيل السريع على سطح المكتب: {bat_file}")

    print("\n--- تمت العملية بنجاح! ---")

if __name__ == "__main__":
    setup()
