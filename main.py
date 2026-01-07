from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.utils import platform
from kivy.core.window import Window
import threading
import os

try:
    import service
except ImportError:
    service = None

class CameraBotApp(App):
    def build(self):
        root = FloatLayout()
        
        # خلفية التطبيق
        if os.path.exists('background.png'):
            root.add_widget(Image(source='background.png', allow_stretch=True, keep_ratio=False))
        
        main_layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        main_layout.add_widget(Label(
            text="sha1",
            font_size='26sp', bold=True, color=(0, 0.7, 1, 1)
        ))

        switch_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.status_label = Label(text="OFFLINE", font_size='20sp', color=(1, 0, 0, 1))
        
        # تحميل الحالة السابقة للسويتش
        saved_state = self.load_state()
        self.bot_switch = Switch(active=(saved_state == "ON"))
        self.bot_switch.bind(active=self.on_switch_active)

        switch_layout.add_widget(self.status_label)
        switch_layout.add_widget(self.bot_switch)
        main_layout.add_widget(switch_layout)
        
        root.add_widget(main_layout)

        if platform == 'android':
            self.request_android_permissions()
            # إذا كان محفوظاً أنه ON، نتأكد من تشغيل الخدمة فور فتح التطبيق
            if saved_state == "ON":
                self.start_bot()

        return root

    def load_state(self):
        """تحميل حالة البوت من الملف"""
        try:
            with open("state.txt", "r") as f:
                return f.read().strip()
        except:
            return "OFF"

    def save_state(self, state):
        """حفظ حالة البوت في ملف"""
        with open("state.txt", "w") as f:
            f.write(state)

    def on_switch_active(self, instance, value):
        if value:
            self.status_label.text = "ACTIVE"
            self.status_label.color = (0, 1, 0, 1)
            self.save_state("ON")
            self.start_bot()
        else:
            self.status_label.text = "OFFLINE"
            self.status_label.color = (1, 0, 0, 1)
            self.save_state("OFF")
            self.stop_bot()

    def start_bot(self):
        if platform == 'android':
            try:
                from android import python_act
                python_act.get_service().startService(python_act.mActivity, "start")
            except:
                self.run_local_logic()
        else:
            self.run_local_logic()

    def stop_bot(self):
        if platform == 'android':
            try:
                from android import python_act
                python_act.get_service().stopService(python_act.mActivity)
            except:
                if service: service.is_running = False
        else:
            if service: service.is_running = False

    def run_local_logic(self):
        if service:
            service.is_running = True
            threading.Thread(target=service.monitor_camera, daemon=True).start()

    def request_android_permissions(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.INTERNET,
                Permission.FOREGROUND_SERVICE,
                Permission.RECEIVE_BOOT_COMPLETED # إذن مهم جداً
            ])
        except:
            pass

if __name__ == '__main__':
    CameraBotApp().run()
