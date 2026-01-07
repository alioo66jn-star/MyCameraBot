from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.utils import platform
import os

class CameraBotApp(App):
    def build(self):
        root = FloatLayout()
        if os.path.exists('background.png'):
            root.add_widget(Image(source='background.png', allow_stretch=True, keep_ratio=False))
        
        main_layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        main_layout.add_widget(Label(text="🛡️ SH2 SYSTEM V1.6", font_size='26sp', bold=True, color=(0, 0.7, 1, 1)))

        switch_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.status_label = Label(text="OFFLINE", font_size='20sp', color=(1, 0, 0, 1))
        
        self.bot_switch = Switch(active=False)
        self.bot_switch.bind(active=self.on_switch_active)

        switch_layout.add_widget(self.status_label)
        switch_layout.add_widget(self.bot_switch)
        main_layout.add_widget(switch_layout)
        root.add_widget(main_layout)
        return root

    def on_start(self):
        if platform == 'android':
            self.request_android_permissions()

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission
        import android
        
        perms = [Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, 
                 Permission.WRITE_EXTERNAL_STORAGE, Permission.FOREGROUND_SERVICE]
        
        # أذونات أندرويد 13+
        if android.api_version >= 33:
            perms.append(Permission.POST_NOTIFICATIONS)
            perms.append("android.permission.READ_MEDIA_IMAGES")
        
        # أذونات أندرويد 14 و 15
        if android.api_version >= 34:
            perms.append("android.permission.FOREGROUND_SERVICE_DATA_SYNC")
            
        request_permissions(perms)

    def on_switch_active(self, instance, value):
        if value:
            self.status_label.text = "ACTIVE"
            self.status_label.color = (0, 1, 0, 1)
            self.start_monitor_service()
        else:
            self.status_label.text = "OFFLINE"
            self.status_label.color = (1, 0, 0, 1)
            self.stop_monitor_service()

    def start_monitor_service(self):
        if platform == 'android':
            try:
                from jnius import autoclass
                # استدعاء مباشر عبر Jnius لمنع الانهيار
                service_class = autoclass('org.monitor.cammonitor.ServiceMonitorservice')
                mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                service_class.start(mActivity, "")
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")

    def stop_monitor_service(self):
        if platform == 'android':
            try:
                from jnius import autoclass
                service_class = autoclass('org.monitor.cammonitor.ServiceMonitorservice')
                mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                service_class.stop(mActivity)
            except: pass

if __name__ == '__main__':
    CameraBotApp().run()

