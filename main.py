#  Copyright (c) Aetec Pte Ltd
import random
import threading

version = '1.1'
import multiprocessing
if __name__ == '__main__':
    multiprocessing.freeze_support()

from kivy.config import Config
import os

Config.set("kivy","log_dir",os.getcwd() + '/log')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# Config.set('modules','monitor','')
from kivy.app import App
from kivy.properties import (NumericProperty, StringProperty, ReferenceListProperty, ObjectProperty, ListProperty, BoundedNumericProperty)
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.config import ConfigParser
from kivy.animation import Animation
from kivy.base import ExceptionHandler, ExceptionManager

#Kivy MD
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.circularlayout import MDCircularLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.button import MDIconButton, MDFlatButton, MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import (
    CircularRippleBehavior,
    FakeCircularElevationBehavior,
RoundedRectangularElevationBehavior
)
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.toast import toast
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.taptargetview import MDTapTargetView
from kivymd.uix.transition import MDFadeSlideTransition
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.screenmanager import ScreenManager

"""
Pyinstaller note to kivymd - add kivymd.effect hooks in master file
"""

from kivy.utils import get_color_from_hex, get_hex_from_color
import shutil
import csv
import traceback
import sys
import time
from os.path import exists
from datetime import datetime
from datetime import timedelta
from functools import partial
from threading import Thread, Lock
import logging
import cv2
import copy

##Import custom library
from libraries import ConfigLoader
from libraries.graphic.Dialogs import *
from libraries.graphic.Expansion import *
from libraries.graphic.Misc import *
from libraries.Errorcode import row_data,column_data
from libraries.PLC_python import PLC_Python

logging.Logger.manager.root = Logger
logger = logging.getLogger("Main Code")

__author__ = "Pang Kai Xuan"
__copyright__ = f"Copyright {datetime.now().year}, Aetec Pte Ltd"
machine_name = 'Epson'
#dictionary lock
plc_python = PLC_Python(ip='192.168.0.4',rack=0,slot=1)
lock = threading.Lock()

def motor_connected(func):
    def wrapper(*args,**kwargs):
        if motor.connected:
            return func(*args,**kwargs)
        else:
            toast("Motor Controller Not Connected !")
    return wrapper

def plc_connected(func):
    def wrapper(*args,**kwargs):
        if plc_python.connected:
            return func(*args,**kwargs)
        else:
            toast("PLC Not Connected !")
    return wrapper


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MyHandler(ExceptionHandler):
    def handle_exception(self, inst):
        if isinstance(inst, AssertionError):
            logger.exception('AssertionError caught by MyHandler')
            return ExceptionManager.PASS
        return ExceptionManager.RAISE

ExceptionManager.add_handler(MyHandler())

class CircularProgressBarMagenta(MDAnchorLayout):
    set_value = NumericProperty(5)
    value = NumericProperty(1)
    bar_color = ListProperty([255,0,255])
    text_color = ListProperty([1,1,1])
    bar_width = NumericProperty(10)
    overlap = NumericProperty(0)
    text = StringProperty("0%")
    counter = 100

    def __init__(self,**kwargs):
        super(CircularProgressBarMagenta, self).__init__(**kwargs)
        Clock.schedule_once(self.animate,0)

    def animate(self, *args):
        Clock.schedule_interval(self.percent_counter,0.1)

    def percent_counter(self, *args):
        if self.counter > self.value:
            self.counter -= 1
            self.text = f"{self.counter}%"
            self.overlap = self.counter*3.6
        else:
            # Clock.unschedule(self.percent_counter)
            pass

class CircularProgressBarCyan(MDAnchorLayout):
    set_value = NumericProperty(5)
    value = NumericProperty(1)
    bar_color = ListProperty([0,255,255])
    text_color = ListProperty([1,1,1])
    bar_width = NumericProperty(10)
    overlap = NumericProperty(0)
    text = StringProperty("0%")
    counter = 100

    def __init__(self,**kwargs):
        super(CircularProgressBarCyan, self).__init__(**kwargs)
        Clock.schedule_once(self.animate,0)

    def animate(self, *args):
        Clock.schedule_interval(self.percent_counter,1)

    def percent_counter(self, *args):
        if self.counter > self.value:
            self.counter -= 1
            self.text = f"{self.counter}%"
            self.overlap = self.counter*3.6
        else:
            # Clock.unschedule(self.percent_counter)
            pass

class CircularProgressBarYellow(MDAnchorLayout):
    set_value = NumericProperty(5)
    value = NumericProperty(1)
    bar_color = ListProperty([255,255,0])
    text_color = ListProperty([1,1,1])
    bar_width = NumericProperty(10)
    overlap = NumericProperty(0)
    text = StringProperty("0%")
    counter = 100

    def __init__(self,**kwargs):
        super(CircularProgressBarYellow, self).__init__(**kwargs)
        Clock.schedule_once(self.animate,0)

    def animate(self, *args):
        Clock.schedule_interval(self.percent_counter,0.1)

    def percent_counter(self, *args):
        if self.counter > self.value:
            self.counter -= 1
            self.text = f"{self.counter}%"
            self.overlap = self.counter*3.6
        else:
            # Clock.unschedule(self.percent_counter)
            pass

class CircularProgressBarBlack1(MDAnchorLayout):
    set_value = NumericProperty(5)
    value = NumericProperty(1)
    bar_color = ListProperty([160,160,160])
    text_color = ListProperty([1,1,1])
    bar_width = NumericProperty(10)
    overlap = NumericProperty(0)
    text = StringProperty("0%")
    counter = 100

    def __init__(self,**kwargs):
        super(CircularProgressBarBlack1, self).__init__(**kwargs)
        Clock.schedule_once(self.animate,0)

    def animate(self, *args):
        Clock.schedule_interval(self.percent_counter,0.8)

    def percent_counter(self, *args):
        if self.counter > self.value:
            self.counter -= 1
            self.text = f"{self.counter}%"
            self.overlap = self.counter*3.6
        else:
            # Clock.unschedule(self.percent_counter)
            pass

class CircularProgressBarBlack2(MDAnchorLayout):
    set_value = NumericProperty(5)
    value = NumericProperty(1)
    bar_color = ListProperty([192,192,192])
    text_color = ListProperty([1,1,1])
    bar_width = NumericProperty(10)
    overlap = NumericProperty(0)
    text = StringProperty("100%")
    counter = 100

    def __init__(self,**kwargs):
        super(CircularProgressBarBlack2, self).__init__(**kwargs)
        Clock.schedule_once(self.animate,0)

    def animate(self, *args):
        Clock.schedule_interval(self.percent_counter,0.1)

    def percent_counter(self, *args):
        if self.counter > self.value :
            self.counter -= 1
            self.text = f"{self.counter}%"
            self.overlap = self.counter*3.6
        else:
            # Clock.unschedule(self.percent_counter)
            pass
class CircularProgressBarPhotoBlack(MDAnchorLayout):
    set_value = NumericProperty(5)
    value = NumericProperty(1)
    bar_color = ListProperty([192,192,192])
    text_color = ListProperty([1,1,1])
    bar_width = NumericProperty(10)
    overlap = NumericProperty(0)
    text = StringProperty("0%")
    counter = 100

    def __init__(self,*args,**kwargs):
        super(CircularProgressBarPhotoBlack, self).__init__(**kwargs)
        Clock.schedule_once(self.animate,0)

    def animate(self, *args):
        Clock.schedule_interval(self.percent_counter,0.3)

    def percent_counter(self, *args):
        if self.counter > self.value:
            self.counter -= 1
            self.text = f"{self.counter}%"
            self.overlap = self.counter*3.6
        else:
            # Clock.unschedule(self.percent_counter)
            pass

class PasswordTextFieldButton(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.logged_in = False

    def on_enter(self):
        self.config = ConfigLoader.load_system_config()
        self.password = self.config['Password']
        self.username = self.config['Username']
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:  # 40 - Enter key pressed
            self.log_in()
        # else:
        #     print(keycode)

    def log_in(self, *args):
        text = 'Operation'
        if self.ids.user.text == self.username and self.ids.password_widget.ids.text_field.text == self.password:
            self.app.root.ids.toolbar.title = f'{machine_name} - {text}'
            self.app.root.ids.screen_manager.current = f'{text}'
            self.logged_in = True
        else:
            toast('Wrong username or Password')

    def clear(self, *args):
        self.ids.user.text = ''
        self.ids.password_widget.ids.text_field.text = ''

class OperationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rowdata = row_data
        self.coldata = column_data
        self.pallet_num = 1
        self.curr_num = 1
        self.green_color = get_color_from_hex('#8cd9b3')
        self.red_color = get_color_from_hex('#FF1300')
        self.read_sensor_clock = None
        self.stop_motor = False
        self.dialog_opened = False

        self.app = App.get_running_app()
        self.theme = self.app.theme_cls

    def on_enter(self):
        self.config = ConfigLoader.load_system_config()
        Window.bind(on_key_down=self._on_keyboard_down)

    def on_leave(self, *args):
       pass

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 22:  # 22 - "s" key pressed
            self.stop_button()
        if keycode == 4:  #  press 'a'
            self.start_button()
        if keycode == 23: # press 't'
            self.open_tabledialog()
        if keycode == 21: # press 'r'
            self.restock()
        # else:
        #     print(keycode)

    def clear_log(self):
        self.ids.log_label.clear_widgets()

    def get_time(self, log=False):
        if log:
            return datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @mainthread
    def update_log(self,msg,log_only=False):
        logger.info(f'Operation : {self.get_time(log=True)} > {msg}')
        if not log_only:
            try:
                btn = MDLabel(text=f'{self.get_time(log=True)} > {msg}', size_hint=(1, None),
                            x=self.ids.message_log.x)
                btn.bind(texture_size=btn.setter('size'))
                if len(self.ids.log_label.children) > 100:
                    self.ids.log_label.remove_widget(self.ids.log_label.children[-1])
                self.ids.log_label.add_widget(btn)
                if self.ids.auto_scroll.active:
                    self.ids.message_log.scroll_to(btn)
            except:
                pass

    @plc_connected
    def start_button(self):
        # if self.selected_recipe == '':
        #     RecipeSelection(self.motor_config,self.update_recipe).open()
        # else:
        StartDialog(self.start_confirm).open()

    @plc_connected
    def stop_button(self):
        self.selected_recipe = ''
        self.update_db(0)
        self.update_log('stop')

    def start_confirm(self):
        # read this status from operation script
        self.update_start(0)
        self.update_db(2)
        self.update_log("Starting operation...")

    def check_stop(self):
        if self.stop_motor == True:
            return True
        else:
            return False

    def connect_button(self):
        ConnectAll(plc_python,self.update_status).open()

    def sleep(self,sec):
        # if not self.check_stop():
        now = time.perf_counter()
        end = now + sec
        while now < end:
            now = time.perf_counter()

    def sleep_l(self,sec):
        time.sleep(sec)

    def open_data_table(self, ):
        if self.data_table is None:
            layout = MDAnchorLayout()

            self.data_table = MDDataTable(
                size_hint=(0.7, 0.6),
                pos_hint ={"center_x: 0.5", "center_y:0.5"},
                use_pagination=True,
                check=True,
                column_data=column_data,
                row_data=row_data
            )

            layout.add_widget(self.data_table)
            return layout

    def open_tabledialog(self):
        if not self.dialog_opened:
            self.dialog_opened = True
            DataTableDialog(self.rowdata,self.coldata,self.calldata).open()
        else:
            toast('Table is already opened')

    def calldata(self,r,c,job):
        r = self.rowdata
        c = self.coldata
        job = job

    def start_check(self):
        self.check_stock = Clock.schedule_interval(self.load_ink_status,1)

    def restock(self, *args):
        max = 100
        self.ids.magenta.counter = max
        self.ids.cyan.counter = max
        self.ids.yellow.counter = max
        self.ids.black1.counter = max
        self.ids.black2.counter = max
        self.ids.photoblack.counter = max

    @plc_connected
    def send_data(self,*args):
        start = time.time()
        temp_xoff = int(self.ids.x_off_field.text)
        temp_yoff = int(self.ids.y_off_field.text)
        temp_zoff = int(self.ids.z_off_field.text)

        self.x_bit1 , self.x_bit2  = plc_python.get_bit(temp_xoff)
        plc_python.reset()
        self.y_bit1 , self.y_bit2 = plc_python.get_bit(temp_yoff)
        plc_python.reset()
        self.z_bit1 , self.z_bit2 = plc_python.get_bit(temp_zoff)
        plc_python.reset()

        self.update_log(f'db4 int0 = {self.x_bit1}\n'
                        f'db4 int1 = {self.x_bit2}\n'
                        f'db4 int2 = {self.y_bit1}\n'
                        f'db4 int3 = {self.y_bit2}\n'
                        f'db4 int4 = {self.z_bit1}\n'
                        f'db4 int5 = {self.z_bit2}')

        if self.ids.x_off_field.text != '' and self.ids.y_off_field.text != '' and self.ids.z_off_field.text != '':
            plc_python.write_int(2,self.x_bit1)
            plc_python.write_int(4,self.x_bit2)
            plc_python.write_int(6,self.y_bit1)
            plc_python.write_int(8,self.y_bit2)
            plc_python.write_int(10,self.z_bit1)
            plc_python.write_int(12,self.z_bit2)
            time_taken = time.time() - start
            print(time_taken)
        else:
            toast('Enter the number before send')

    @plc_connected
    def send_real(self):
        temp_x = float(self.ids.x_off_fieldr.text)
        temp_y = float(self.ids.y_off_fieldr.text)
        temp_z = float(self.ids.z_off_fieldr.text)

        plc_python.write_real(104, temp_x)
        plc_python.write_real(108, temp_y)
        plc_python.write_real(112, temp_z)

    @plc_connected
    def read_data(self, *args):
        input1 = plc_python.get_int(8,0)
        input2 = plc_python.get_int(8,2)
        print(input1)
        print(input2)
        a = plc_python.read_usint_data(input1,input2)
        print(a)

    def recipe_parameter(self):
        self.quantity = 1
        self.pipe_diameter= 200
        self.nominal = 8
        self.outer_diameter = 8.63
        self.pipe_length = 236.2
        self.groove_start = True
        self.groove_end = True
        self.cut_orientation = 0
        self.cut_distance = 25.45
        self.socket_id = '730TX30151'
        self.hole_size = 2

    def update_status(self,val):
        if val:
            self.ids.system_status.text = 'Ready'
            self.ids.system_status.text_color = self.theme.primary_light
        else:
            self.ids.system_status.text = 'Not Ready'
            self.ids.system_status.text_color = self.theme.error_color

    def update_db(self,num):
        plc_python.write_int(102,num)
        self.update_log('Datablock Updated')

    def update_start(self, val):
        color = get_color_from_hex('#00aa00')
        self.ids.start_button.icon = "play-circle-outline"

        # if val == 0:
        #     # operation paused
        #     if robot.program_running:
        #         # update to resume, operation is paused
        #         self.ids.start_label.text = 'Resume'
        #         self.ids.operation_status.text = 'Paused'
        #         self.ids.operation_status.text_color = self.app.theme_cls.accent_color
        #     else:
        #         self.ids.start_label.text = 'Start'
        #         self.ids.operation_status.text = 'Idle'
        #         self.ids.operation_status.text_color = self.app.theme_cls.text_color
        # elif val == 1:
        #     if robot.program_running and not robot.program_paused:
        #         self.ids.start_label.text = 'Start'
        #     else:
        #         # update to pause, operation is running
        #         color = self.theme.accent_color
        #         self.ids.start_label.text = 'Pause'
        #         self.ids.start_button.icon = "pause-circle-outline"
        #         self.ids.operation_status.text = 'Running'
        #         self.ids.operation_status.text_color = self.app.theme_cls.primary_color
        # elif val == 2:
        #     self.ids.start_label.text = 'New Cycle'
        #     self.ids.operation_status.text = 'Idle'
        #     self.ids.operation_status.text_color = self.app.theme_cls.text_color
        #
        # self.ids.start_label.text_color = color
        # self.ids.start_button.icon_color = color

    def update_recipe(self,recipe=None):
        if recipe is not None:
            self.selected_recipe = recipe
            self.ids.recipe_selected = recipe
            print(self.selected_recipe)

class IOScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.green_color = get_color_from_hex('#8cd9b3')
        self.red_color = get_color_from_hex('#FF1300')
        self.read_sensor_clock = None
        self.app = App.get_running_app()

    def on_enter(self):
        pass

    def on_leave(self, *args):
        pass

    def update_color(self, item, color):
        if item.text_color != color:
            item.text_color = color


class TuningScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class TestScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log = None
        self.stop_log = False
        self.dic = ConfigLoader.load_system_config()
    def view_thread(self):
        for thread in threading.enumerate():
            print(thread.name)

class MyApp(MDApp):
    logo = StringProperty(resource_path('images/logo.png'))
    view = StringProperty(resource_path('images/topview.png'))
    machine_name = machine_name
    new_pass = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        get_app()

        self.menu = MDDropdownMenu(width_mult=3, max_height=230,opacity=0.9)
        titles = [['Operation','robot-angry'],
                  ['IO Control','controller']]
                  # ['Tuning','application-edit']]
                  # ['Tests','test-tube']]
        menu_items = [
            {
                "text": f"{titles[i][0]}",
                "icon" : f'{titles[i][1]}',
                "viewclass": "IconListItem",
                'iconpress' : lambda x=f"{titles[i][0]}": self.menu_callback(x),
                "height": dp(56),
                "on_release": lambda x=f"{titles[i][0]}": self.menu_callback(x),
            } for i in range(len(titles))
        ]
        self.menu.items = menu_items

    def resource_path(self,path):
        return resource_path(path)

    def build(self):
        self.title = f'{machine_name} v{version}'
        self.icon = resource_path('images/logo.png')
        self.use_kivy_settings = False
        self.app = App.get_running_app()
        Window.bind(on_request_close=self.on_request_close)
        return Builder.load_file(resource_path('resource\graphic.kv'))

    def _on_keyboard_settings(self, window, *largs):
        #so that pressing F1 will not open settings
        pass

    def on_request_close(self,*args):
        return True

    def build_config(self, config):
        dic = ConfigLoader.load_system_config()
        config.setdefaults('config', dic)

        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = dic['Theme Color']
        self.theme_cls.theme_style = dic['Theme Style']  # "Light"
        self.dic = dic

    def build_settings(self, settings):
        settings.add_json_panel('Settings', self.config, filename=resource_path('resource\settings.json'))

    def shut_down(self,*args):
        ShutdownDialog(self.shutdown).open()

    def shutdown(self,power=True):
        Clock.schedule_once(partial(toast, 'Shutting down...'),-1)
        if power:
            os.system("shutdown /s /t 1")

        # webserver.stop()

        for thread in threading.enumerate():
            print(thread.name)
        self.app.stop()
        sys.exit()

    def update_screen(self,text):
        #Access control here
        # if text == 'Tuning':
        #     PasswordDialog(partial(self.enter_tuning,text),self.dic['Password'],self.dic['Operator Password']).open()
        # else:
        self.app.root.ids.toolbar.title = f'{machine_name} - {text}'
        self.app.root.ids.screen_manager.current = f'{text}'

    def enter_tuning(self,text):
        self.app.root.ids.toolbar.title = f'{machine_name} - {text}'
        self.app.root.ids.screen_manager.current = f'{text}'

    def enter_settings(self):
        PasswordDialog(self.open_settings,self.dic['Password'],None).open()

    def log_out(self):
        text = 'Login'
        self.root.ids.login_screen.logged_in = False
        self.app.root.ids.toolbar.title = f'{machine_name} - {text}'
        self.app.root.ids.screen_manager.current = f'{text}'

    def call_menu(self,btn):
        if self.root.ids.login_screen.logged_in:
            self.menu.caller = btn
            self.menu.open()

    def menu_callback(self,text_item):
        self.menu.dismiss()
        self.update_screen(text_item)

    def on_config_change(self, config, section, key, value):
        ConfigLoader.write_system_config(key, (value))
        self.root.ids.operation_screen.load_system_config()
        self.dic = self.root.ids.operation_screen.config


if __name__ == '__main__':
    Window.maximize()
    MyApp().run()

