from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.utils import platform
from kivy.core.window import Window
import threading

# محاولة استيراد ملف الخدمة للتشغيل في بيئة Pydroid أو الحاسوب
try:
    import service
except ImportError:
    service = None

class CameraBotApp(App):
    def build(self):
        # إعدادات الواجهة (خلفية داكنة)
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=30)

        # العنوان الرئيسي
        self.layout.add_widget(Label(
            text=" shm1 ",
            font_size='26sp',
            bold=True,
            color=(0, 0.7, 1, 1)
        ))

        # حاوية زر التشغيل (Switch) وحالة البوت
        switch_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        
        self.status_label = Label(
            text="OFFLINE", 
            font_size='20sp', 
            color=(1, 0, 0, 1) # أحمر عند الإيقاف
        )

        self.bot_switch = Switch(active=False)
        self.bot_switch.bind(active=self.on_switch_active)

        switch_layout.add_widget(self.status_label)
        switch_layout.add_widget(self.bot_switch)
        self.layout.add_widget(switch_layout)

        # طلب صلاحيات أندرويد تلقائياً عند فتح التطبيق
        if platform == 'android':
            self.request_android_permissions()

        return self.layout

    def request_android_permissions(self):
        """طلب الصلاحيات اللازمة للوصول للصور والإنترنت"""
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.INTERNET,
                Permission.FOREGROUND_SERVICE
            ])
        except Exception as e:
            print(f"بيئة تجريبية: {e}")

    def on_switch_active(self, instance, value):
        """التحكم في تشغيل وإيقاف البوت"""
        if value:
            self.status_label.text = "ACTIVE"
            self.status_label.color = (0, 1, 0, 1) # أخضر عند التشغيل
            self.start_bot()
        else:
            self.status_label.text = "OFFLINE"
            self.status_label.color = (1, 0, 0, 1)
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

if __name__ == '__main__':
    CameraBotApp().run()
