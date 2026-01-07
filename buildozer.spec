[app]
title = sh1
package.name = cammonitor
package.domain = org.monitor
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.6

# المكتبات الضرورية للعمل في الخلفية
requirements = python3,kivy,requests,urllib3,charset-normalizer,idna,pyjnius,android

orientation = portrait
services = MonitorService:service.py

# --- الأذونات الشاملة لكل إصدارات أندرويد ---
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, FOREGROUND_SERVICE_DATA_SYNC, RECEIVE_BOOT_COMPLETED, POST_NOTIFICATIONS, READ_MEDIA_IMAGES, MANAGE_EXTERNAL_STORAGE

# استهداف أندرويد 14 (API 34) وهو متوافق تماماً مع أندرويد 15
android.api = 34
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# سطر إلزامي لأندرويد 14 و 15 لتحديد نوع العمل في الخلفية
android.manifest.foreground_service_type = dataSync
