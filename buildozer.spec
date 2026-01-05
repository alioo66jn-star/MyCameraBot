[app]

# (str) اسم التطبيق الذي سيظهر على الهاتف
title = Camera Monitor Bot

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

# (list) المكتبات المطلوبة (تم تصحيحها لضمان عمل Requests)
requirements = python3,kivy,requests,urllib3,charset-normalizer,idna

# (list) اتجاه الشاشة المدعوم
orientation = portrait

# (list) تعريف الخدمة التي ستعمل في الخلفية (مهم جداً)
services = MonitorService:service.py

#
# Android specific
#

# (bool) هل التطبيق ملء الشاشة
fullscreen = 0

# (list) الأذونات المطلوبة (الإنترنت، الملفات، والخدمة الخلفية)
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, RECEIVE_BOOT_COMPLETED

# (int) إصدار API المستهدف (أندرويد 12 هو 31)
android.api = 31

# (int) أدنى إصدار أندرويد مدعوم
android.minapi = 21

# (list) المعماريات المدعومة للهواتف الحديثة
android.archs = arm64-v8a, armeabi-v7a

# (bool) السماح بالنسخ الاحتياطي التلقائي
android.allow_backup = True

# (str) نوع الملف الناتج (apk)
android.debug_artifact = apk

[buildozer]

# (int) مستوى السجلات (2 تعني إظهار كل شيء للمساعدة في حل الأخطاء)
log_level = 2

# (int) إظهار تحذير إذا تم التشغيل كمسؤول (Root)
warn_on_root = 1