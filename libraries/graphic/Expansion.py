import time

from kivymd.uix.boxlayout import MDBoxLayout
from .Misc import CustomSnackbar
from kivy.app import App
from threading import Thread
from kivymd.toast import toast

class OvenContent(MDBoxLayout):
    #cant make it into another libraries???
    def __init__(self,temp,*args,**kwargs):
        super(OvenContent, self).__init__(**kwargs)
        self.temp = temp
        self.app = App.get_running_app()
        self.os = self.app.root.ids.operation_screen

    def start_oven(self):
        # if not self.temp.connected:
        #     toast("Temperature Controller not Connected!")
        #     return
        self.os.oven_start()
        time.sleep(0.05)
        self.update_status()

    def stop_oven(self):
        # if not self.temp.connected:
        #     toast("Temperature Controller not Connected!")
        #     return
        self.os.oven_stop()
        self.update_status()

    def update_status(self):
        if self.os.oven_running:
            self.ids.status_label.text = "Status : Running"
            self.ids.status_label.text_color = self.app.theme_cls.primary_light
        else:
            self.ids.status_label.text = "Status : Stopped"
            self.ids.status_label.text_color = self.app.theme_cls.text_color
