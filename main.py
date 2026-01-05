from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.utils import platform
from kivy.core.window import Window
import threading
import os

# استيراد ملف الخدمة
try:
    import service
except ImportError:
    pass


class CameraBotApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)  # خلفية داكنة جداً
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=30)

        # العنوان
        self.layout.add_widget(Label(
            text="🛡️ BOT MONITOR SYSTEM",
            font_size='26sp',
            bold=True,
            color=(0, 0.7, 1, 1)
        ))

        # حاوية لزر السحب والنص
        switch_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        self.status_label = Label(
            text="OFFLINE",
            font_size='20sp',
            color=(1, 0, 0, 1)
        )

        # زر السحب (Switch)
        self.bot_switch = Switch(active=False)
        self.bot_switch.bind(active=self.on_switch_active)

        switch_layout.add_widget(self.status_label)
        switch_layout.add_widget(self.bot_switch)

        self.layout.add_widget(switch_layout)

        self.layout.add_widget(Label(
            text="سيستمر البوت في العمل بالخلفية\nحتى تقوم بإطفاء السويتش يدوياً",
            halign='center',
            color=(0.6, 0.6, 0.6, 1)
        ))

        if platform == 'android':
            self.request_android_permissions()

        return self.layout

    def request_android_permissions(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.INTERNET,
                Permission.FOREGROUND_SERVICE
            ])
        except:
            pass

    def on_switch_active(self, instance, value):
        if value:  # إذا تم السحب للتشغيل
            self.status_label.text = "ACTIVE"
            self.status_label.color = (0, 1, 0, 1)
            self.start_bot()
        else:  # إذا تم السحب للإيقاف
            self.status_label.text = "OFFLINE"
            self.status_label.color = (1, 0, 0, 1)
            self.stop_bot()

    def start_bot(self):
        # تفعيل علم التشغيل في ملف الخدمة
        service.is_running = True

        if platform == 'android':
            try:
                from android import PythonService
                android_service = PythonService('MonitorService', 'Bot is Running')
                android_service.start('')
            except:
                self.run_in_thread()
        else:
            self.run_in_thread()

    def stop_bot(self):
        # إيقاف العلم ليتوقف التكرار في ملف الخدمة
        service.is_running = False
        if platform == 'android':
            try:
                from android import PythonService
                android_service = PythonService('MonitorService', 'Bot is Running')
                android_service.stop()
            except:
                pass

    def run_in_thread(self):
        # تشغيل في خيط منفصل لـ Pydroid 3
        monitor_thread = threading.Thread(target=service.run_monitoring)
        monitor_thread.daemon = True
        monitor_thread.start()


if __name__ == '__main__':
    CameraBotApp().run()