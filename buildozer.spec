[app]
# (str) الاسم الذي يظهر تحت أيقونة التطبيق
title = sh1

# (str) اسم الحزمة (بدون مسافات أو أحرف خاصة)
package.name = cammonitor

# (str) نطاق الحزمة
package.domain = org.monitor

# (str) المجلد الحالي للكود
source.dir = .

# (list) أنواع الملفات التي سيتم تضمينها
source.include_exts = py,png,jpg,kv,atlas

# (str) إصدار التطبيق (ارفعه عند كل بناء جديد لتجنب مشاكل التثبيت)
version = 1.2

# (list) المكتبات المطلوبة - ضروري جداً وجود pyjnius و android
requirements = python3,kivy,requests,urllib3,charset-normalizer,idna,pyjnius,android

# (list) اتجاه الشاشة
orientation = portrait

# (list) تعريف الخدمة الخلفية التي ستعمل بشكل دائم
services = MonitorService:service.py

# --- إعدادات أندرويد الخاصة ---

# (bool) هل التطبيق ملء الشاشة
fullscreen = 0

# (list) الأذونات الشاملة (ضرورية لأندرويد 12 و 13 لضمان عدم توقف البوت)
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, RECEIVE_BOOT_COMPLETED, POST_NOTIFICATIONS, READ_MEDIA_IMAGES, MANAGE_EXTERNAL_STORAGE

# (int) إصدار API المستهدف (33 يعني أندرويد 13)
android.api = 33

# (int) أدنى إصدار مدعوم (أندرويد 5.0)
android.minapi = 21

# (bool) الموافقة التلقائية على التراخيص (ضروري للـ GitHub)
android.accept_sdk_license = True

# (list) المعماريات المطلوبة للهواتف الحديثة
android.archs = arm64-v8a, armeabi-v7a

# (str) نوع الملف الناتج
android.debug_artifact = apk

[buildozer]
# (int) مستوى السجلات (2 لإظهار كل شيء في حال حدوث خطأ)
log_level = 2

# (int) تحذير إذا تم التشغيل كمسؤول
warn_on_root = 1
