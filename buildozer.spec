[app]

# (str) اسم التطبيق الذي سيظهر على الهاتف
title = shm1
# (str) اسم الحزمة (بدون مسافات)
package.name = cammonitor

# (str) نطاق الحزمة
package.domain = org.monitor

# (str) المجلد الذي يحتوي على الكود (النقطة تعني المجلد الحالي)
source.dir = .

# (list) أنواع الملفات التي سيتم تضمينها في التطبيق
source.include_exts = py,png,jpg,kv,atlas

# (str) إصدار التطبيق
version = 1.0

# (list) المكتبات المطلوبة
requirements = python3,kivy,requests,urllib3,charset-normalizer,idna

# (list) اتجاه الشاشة المدعوم
orientation = portrait

# (list) تعريف الخدمة التي ستعمل في الخلفية
services = MonitorService:service.py

#
# Android specific
#

# (bool) هل التطبيق ملء الشاشة
fullscreen = 0

# (list) الأذونات المطلوبة
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, RECEIVE_BOOT_COMPLETED

# (int) إصدار API المستهدف (أندرويد 12 هو 31)
android.api = 31

# (int) أدنى إصدار أندرويد مدعوم
android.minapi = 21

# (bool) الموافقة التلقائية على تراخيص أندرويد (ضروري جداً للـ GitHub Actions)
android.accept_sdk_license = True

# (list) المعماريات المدعومة
android.archs = arm64-v8a, armeabi-v7a

# (bool) السماح بالنسخ الاحتياطي التلقائي
android.allow_backup = True

# (str) نوع الملف الناتج (apk)
android.debug_artifact = apk

[buildozer]

# (int) مستوى السجلات (2 تعني إظهار كل شيء)
log_level = 2

# (int) إظهار تحذير إذا تم التشغيل كمسؤول (Root)
warn_on_root = 1

