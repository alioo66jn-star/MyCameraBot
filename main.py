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
        
        # إضافة صورة الخلفية background.png إذا كانت موجودة
        if os.path.exists('background.png'):
            root.add_widget(Image(source='background.png', allow_stretch=True, keep_ratio=False))
            
        main_layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        # العنوان الرئيسي
        main_layout.add_widget(Label(
            text="🛡️ SH1 MONITOR", 
            font_size='26sp', 
            bold=True, 
            color=(0, 0.7, 1, 1)
        ))

        # حاوية السويتش وحالة البوت
        switch_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.status_label = Label(text="OFFLINE", font_size='20sp', color=(1, 0, 0, 1))
        
        self.bot_switch = Switch(active=False)
        self.bot_switch.bind(active=self.on_switch_active)

        switch_layout.add_widget(self.status_label)
        switch_layout.add_widget(self.bot_switch)
        main_layout.add_widget(switch_layout)
        
        root.add_widget(main_layout)

        if platform == 'android':
            self.request_android_permissions()
            
        return root

    def request_android_permissions(self):
        """طلب الأذونات الشاملة لأندرويد 12 و 13"""
        from android.permissions import request_permissions, Permission
        import android
        
        perms = [
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.FOREGROUND_SERVICE,
            Permission.RECEIVE_BOOT_COMPLETED
        ]
        
        # أذونات إضافية ضرورية لأندرويد 13+ (API 33)
        if android.api_version >= 33:
            perms.append(Permission.POST_NOTIFICATIONS)
            perms.append("android.permission.READ_MEDIA_IMAGES")
            
        request_permissions(perms)

    def on_switch_active(self, instance, value):
        if value:
            self.status_label.text = "ACTIVE"
            self.status_label.color = (0, 1, 0, 1)
            self.start_service()
        else:
            self.status_label.text = "OFFLINE"
            self.status_label.color = (1, 0, 0, 1)
            self.stop_service()

    def start_service(self):
        if platform == 'android':
            from android import python_act
            python_act.get_service().startService(python_act.mActivity, "start")

    def stop_service(self):
        if platform == 'android':
            from android import python_act
            python_act.get_service().stopService(python_act.mActivity)

if __name__ == '__main__':
    CameraBotApp().run()
