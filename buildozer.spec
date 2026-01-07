[app]
title = sh1
package.name = cammonitor
package.domain = org.monitor
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.6

requirements = python3,kivy,requests,urllib3,charset-normalizer,idna,pyjnius,android

orientation = portrait
services = MonitorService:service.py

# الأذونات المطلوبة لجميع الإصدارات حتى أندرويد 15
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, FOREGROUND_SERVICE_DATA_SYNC, RECEIVE_BOOT_COMPLETED, POST_NOTIFICATIONS, READ_MEDIA_IMAGES, MANAGE_EXTERNAL_STORAGE

android.api = 34
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# تحديد نوع الخدمة - إلزامي لأندرويد 14 و 15
android.manifest.foreground_service_type = dataSync

fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
