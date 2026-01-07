[app]

# (str) اسم التطبيق الذي سيظهر تحت الأيقونة
title = sh1

# (str) اسم الحزمة (يفضل تغييره إذا كنت تريد تثبيته كتطبيق جديد تماماً)
package.name = cammonitor

# (str) نطاق الحزمة
package.domain = org.monitor

# (str) المجلد الذي يحتوي على الكود
source.dir = .

# (list) الملفات المضمنة (تأكد من وجود py و png للخلفية)
source.include_exts = py,png,jpg,kv,atlas

# (str) إصدار التطبيق (ارفعه لـ 1.1 ليعتبره الهاتف تحديثاً)
version = 1.1

# (list) المكتبات المطلوبة (أضفنا pyjnius للتعامل مع نظام أندرويد)
requirements = python3,kivy,requests,urllib3,charset-normalizer,idna,pyjnius,android

# (list) اتجاه الشاشة
orientation = portrait

# (list) تعريف الخدمة الخلفية (ضروري جداً لعمل التطبيق في الخلفية)
services = MonitorService:service.py

#
# Android specific
#

# (bool) هل التطبيق ملء الشاشة
fullscreen = 0

# (list) الأذونات (تم إضافة POST_NOTIFICATIONS لأندرويد 13+)
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, RECEIVE_BOOT_COMPLETED, POST_NOTIFICATIONS

# (int) إصدار API المستهدف (33 يدعم أحدث ميزات الحماية)
android.api = 33

# (int) أدنى إصدار أندرويد مدعوم
android.minapi = 21

# (bool) الموافقة التلقائية على تراخيص SDK
android.accept_sdk_license = True

# (list) المعماريات المدعومة
android.archs = arm64-v8a, armeabi-v7a

# (bool) السماح بالنسخ الاحتياطي
android.allow_backup = True

# (str) نوع الملف الناتج
android.debug_artifact = apk

[buildozer]

# (int) مستوى السجلات (2 لإظهار التفاصيل في حال حدوث خطأ)
log_level = 2

# (int) تحذير Root
warn_on_root = 1
