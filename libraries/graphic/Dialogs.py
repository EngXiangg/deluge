import threading

from kivy.graphics import Rectangle, Color, Line
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRoundFlatIconButton,MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.selection import MDSelectionList
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDIcon
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tab import MDTabs
from kivymd.uix.list import OneLineListItem,OneLineIconListItem,MDList,IconRightWidget
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivy.core.window import Window
from .Misc import *
from functools import partial
from threading import Thread
from datetime import datetime

import threading
import time
import sys

from kivymd.toast import toast
from ..Errorcode import row_data,column_data,row_data1,column_data1

def get_app():
    global app
    app = App.get_running_app()


class ResetDialog(MDDialog):

    def __init__(self, callback, *args, title='Confirm to reset?', **kwargs):
        self.callback = callback

        self.title = title
        self.text = "All unsaved changes will be discarded.\n\nSelect 'Yes' to confirm, press anywhere to dismiss"

        self.buttons = [MDFlatButton(text='No', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        MDRaisedButton(text='Yes', on_release=self.yes)]

        super(ResetDialog, self).__init__()

    def yes(self, *args):
        self.callback()
        self.dismiss()


class DeleteDialog(MDDialog):

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback

        self.title = 'Confirm to delete location?'
        self.text = "Select 'Yes' to confirm, press anywhere to dismiss"

        self.buttons = [MDFlatButton(text='No', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        MDRaisedButton(text='Yes', on_release=self.yes)]

        super(DeleteDialog, self).__init__()

    def yes(self, *args):
        self.callback()
        self.dismiss()


class StopDialog(MDDialog):

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback

        self.title = 'Confirm to stop operation?'
        self.text = "Select 'Yes' to confirm, press anywhere to dismiss"

        self.buttons = [MDFlatButton(text='No', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.error_color),
                        MDRaisedButton(text='Yes', on_release=self.yes, md_bg_color=app.theme_cls.error_color)]

        super(StopDialog, self).__init__()

    def yes(self, *args):
        self.callback()
        self.dismiss()


class AddLocationDialog(MDDialog):
    def __init__(self, callback, names, *args, **kwargs):
        self.callback = callback
        self.names = names
        self.title = 'Add new location'
        self.type = 'custom'
        self.content_cls = self.create()

        self.buttons = [MDRaisedButton(text='Add', on_release=self.yes)]

        super(AddLocationDialog, self).__init__()

    def create(self):
        boxlayout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=80)

        self.text_field = MDTextField(max_text_length=20, on_text_validate=self.yes)

        boxlayout.add_widget(MDLabel(text='Enter new location name', theme_text_color='Custom',
                                     text_color=app.theme_cls.disabled_hint_text_color))
        boxlayout.add_widget(self.text_field)
        return boxlayout

    def yes(self, *args):
        if self.text_field.text == '':
            toast("Recipe name cannot be empty")
            return
        if len(self.text_field.text) > self.text_field.max_text_length:
            toast("Name exceed maximum length")
            return
        if self.text_field.text in self.names:
            toast("Name already exists")
            return
        self.callback(self.text_field.text)
        self.dismiss()


class StartDialog(MDDialog):

    def __init__(self,callback, *args, **kwargs):
        self.callback = callback
        self.title = 'Confirm to start operation?'
        self.type = 'custom'
        self.content_cls = self.create()
        self.yes_button = MDRaisedButton(text='Confirm', on_release=self.yes, disabled=True)
        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        self.yes_button]

        super(StartDialog, self).__init__()

    def open_menu(self, *args):
        self.menu.open()

    def create(self):
        boxlayout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=180)

        box1 = MDBoxLayout(spacing=12)
        self.checkbox = MDCheckbox()
        self.checkbox.bind(on_release=self.tick)
        box1.add_widget(self.checkbox)
        box1.add_widget(MDLabel(text='I confirm start the operation.', halign='left', size_hint_x=5))
        box1.add_widget(MDLabel())

        boxlayout.add_widget(box1)

        return boxlayout

    def yes(self, *args):
        self.callback()
        self.dismiss()

    def tick(self, *args):
        if self.checkbox.active:
            self.yes_button.disabled = False
        else:
            self.yes_button.disabled = True


class DisconnectDialog(MDDialog):

    def __init__(self, callback, target, *args, **kwargs):
        self.callback = callback

        self.title = f'Confirm to Disconnect {target}?'
        self.text = "Select 'Yes' to confirm, press anywhere to dismiss"

        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        MDRaisedButton(text='Yes', on_release=self.yes)]

        super(DisconnectDialog, self).__init__()

    def yes(self, *args):
        self.callback()
        self.dismiss()


class ResumeDialog(MDDialog):

    def __init__(self, callback, *args, **kwargs):
        self.title = 'Confirm to resume operation?'
        self.text = "Select 'Yes' to confirm, press anywhere to dismiss"

        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        MDRaisedButton(text='Yes', on_release=self.yes)]

        self.callback = callback
        super(ResumeDialog, self).__init__()

    def yes(self, *args):
        Thread(target=self.callback, name='Resume').start()
        self.dismiss()


class ShutdownDialog(MDDialog):

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback

        self.title = 'Select action'
        self.type = 'custom'
        self.content_cls = self.create()

        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color)]

        super(ShutdownDialog, self).__init__()

    def create(self):
        boxlayout = MDBoxLayout(spacing=12, size_hint_y=None, height=50)
        btn1 = MDRoundFlatIconButton(text='Power Off', icon='power', on_release=partial(self.yes, True))
        btn2 = MDRoundFlatIconButton(text='Close App', icon='exit-run', on_release=partial(self.yes, False))
        boxlayout.add_widget(btn1)
        boxlayout.add_widget(btn2)
        return boxlayout

    def yes(self, sel, *args):
        self.callback(sel)


class PasswordDialog(MDDialog):
    def __init__(self, callback, password,ope_password, *args, **kwargs):

        self.title = 'Enter Password to Continue'
        self.type = 'custom'
        self.password = password
        self.operator_password = ope_password
        self.content_cls = self.create()
        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        MDRaisedButton(text='Enter', on_release=self.yes)]
        self.callback = callback
        super(PasswordDialog, self).__init__()

    def create(self):
        self.textfield = MDTextField(hint_text='Password', password=True, on_text_validate=self.yes)
        self.showpwd = MDCheckbox(pos_hint={"center_x": 0.5, 'center_y': 0.5}, size_hint_x=0.1)
        self.showpwd.bind(on_release=self.check)
        boxlayout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=120)

        boxlayout.add_widget(self.textfield)

        second_box = MDBoxLayout()
        second_box.add_widget(self.showpwd)
        second_box.add_widget(MDLabel(text='Show Password'))

        self.alert_label = MDLabel(text='', font_size=25, theme_text_color='Error', halign='right')
        boxlayout.add_widget(second_box)
        boxlayout.add_widget(self.alert_label)
        return boxlayout

    def yes(self, *args):
        if self.textfield.text == self.password or self.operator_password or self.textfield.text == '':
            self.callback()
            self.dismiss()
        else:
            self.alert_label.text = 'Wrong password!'

    def check(self, *args):
        if self.showpwd.active:
            self.textfield.password = False
        else:
            self.textfield.password = True


class MoveToDialog(MDDialog):
    def __init__(self, pos, func, vel, joint, robot, *args, **kwargs):

        self.title = 'Confirm to move to position?'
        self.type = 'custom'
        self.func = func
        self.vel = vel
        self.target = pos
        self.joint = joint
        self.robot = robot
        self.content_cls = self.create()
        self.buttons = [MDRaisedButton(text='Move to\n(Press and hold)', on_release=self.stop, on_press=self.move,
                                       always_release=True), ]
        super(MoveToDialog, self).__init__()
        self.check_pos = Clock.schedule_interval(self.robot_pos_check, 1)

    def create(self):

        boxlayout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=140)

        self.subtitle = MDLabel(text='Target Coordinate : ', bold=True)
        self.position = MDLabel(text='')
        if not self.joint:
            self.position.text = 'x : {:.3f} , y : {:.3f} , z : {:.3f}\nrx : {:.3f}, ry : {:.3f} , rz : {:.3f}'.format(
                *self.target)
            self.target[0] = self.target[0] / 1000
            self.target[1] = self.target[1] / 1000
            self.target[2] = self.target[2] / 1000
        else:
            self.position.text = 'J1 : {:.3f} , J2 : {:.3f} , J3 : {:.3f}\nJ4 : {:.3f}, J5 : {:.3f} , J6 : {:.3f}'.format(
                *self.target)

        boxlayout.add_widget(self.subtitle)
        boxlayout.add_widget(self.position)

        second_box = MDBoxLayout()

        self.alert_label = MDLabel(text='', font_size=20, theme_text_color='Custom',
                                   text_color=app.theme_cls.accent_color, halign='right')
        boxlayout.add_widget(self.alert_label)
        boxlayout.add_widget(second_box)

        return boxlayout

    def robot_pos_check(self, *args):
        time.sleep(0.1)
        home_pos = self.target
        if self.joint:
            curr = self.robot.get_joint()
            for i in range(len(curr)):
                if abs(curr[i] - home_pos[i]) > 0.1:
                    # one joint not same > exit
                    return
        else:
            curr = self.robot.get_pose()
            for i in range(3):
                if abs(curr[i] - home_pos[i]) > 0.0001:
                    return
            for i in range(3):
                if abs(curr[i + 3] - home_pos[i + 3]) > 0.1:
                    return

        self.alert_label.text = 'Robot reached position !'
        self.check_pos.cancel()

    def move(self, *args):
        Thread(target=self.func, args=(self.target,), kwargs={'vel': self.vel}).start()

    def stop(self, *args):
        self.robot.robot_stop()

    def on_dismiss(self):
        self.stop()
        self.check_pos.cancel()


class ConnectRobotDialog(MDDialog):

    def __init__(self, *args, **kwargs):
        self.title = 'Robot is not connected !'
        self.text = "Connect to the robot before initializing!"

        self.buttons = [MDRaisedButton(text='OK', on_release=self.dismiss)]

        super(ConnectRobotDialog, self).__init__()


class InitRobotDialog(MDDialog):

    def __init__(self, *args, must=False, **kwargs):

        self.title = 'Robot Initialization'
        self.type = 'custom'

        self.buttons = [MDRaisedButton(text='Done', on_release=self.done_button)]
        self.content_cls = self.create()
        self.robot = args[0]
        self.callback = args[1]
        self.must_ready = must
        super(InitRobotDialog, self).__init__()

        self.update_clock = Clock.schedule_interval(self.update_status, 0.5)

    def done_button(self, *args):
        if not self.must_ready:
            self.dismiss()
            return
        if 'Robot Ready' in self.status_label.text:
            self.dismiss()
        else:
            toast('Robot not in ready mode')

    def create(self):
        boxlayout = MDBoxLayout(spacing=12, size_hint_y=None, height=140, orientation='vertical')

        self.subtitle = MDLabel(text="Ensure the robot is in 'Ready' mode",
                                font_style='Body1',
                                valign='top',
                                markup=True,
                                text_color=app.theme_cls.disabled_hint_text_color,
                                theme_text_color='Custom',
                                adaptive_height=True)

        boxlayout2 = MDBoxLayout(spacing=8)
        boxlayout3 = MDBoxLayout(spacing=32)
        self.status_title = MDLabel(text='Status :', bold=True)
        self.status_label = MDLabel(text='', bold=True, halign='left', markup=True)
        btn_pos_hint = {'x': 0, 'center_y': 0.5}
        self.off_button = MDRaisedButton(text='Power Off', md_bg_color=app.theme_cls.error_color,
                                         on_release=self.power_off, pos_hint=btn_pos_hint)
        self.on_button = MDRaisedButton(text='Power On', on_release=self.power_on, pos_hint=btn_pos_hint)

        boxlayout.add_widget(self.subtitle)
        boxlayout2.add_widget(self.status_title)
        boxlayout2.add_widget(self.status_label)
        boxlayout2.add_widget(MDLabel())
        boxlayout2.add_widget(MDLabel())

        boxlayout3.add_widget(self.off_button)
        boxlayout3.add_widget(self.on_button)

        boxlayout.add_widget(boxlayout2)
        boxlayout.add_widget(boxlayout3)

        return boxlayout

    def update_status(self, *args):
        status = self.robot.get_robot_mode()
        self.status = status
        if 'POWER_OFF' in status:
            color = get_hex_from_color(app.theme_cls.error_color)
            self.status_label.text = f'[color={color}]Power Off'
            self.on_button.text = 'Power On'
            self.on_button.disabled = False
        elif 'IDLE' in status:
            self.status_label.text = 'Robot Idle'
            self.on_button.text = 'Brake Release'
            self.on_button.disabled = False
        elif 'RUNNING' in status:
            color = get_hex_from_color(app.theme_cls.primary_color)
            self.status_label.text = f'[color={color}]Robot Ready'
            self.on_button.disabled = True
        elif 'POWER_ON' in status or 'BOOTING' in status:
            if self.status_label.text == 'Booting...' or 'Booting' not in self.status_label.text:
                self.status_label.text = 'Booting'
            else:
                self.status_label.text += '.'
            self.on_button.disabled = True
        else:
            self.status_label.text = 'Check Pendant'

    def power_off(self, *args):
        self.robot.power_off()

    def power_on(self, *args):
        if 'Power Off' in self.status_label.text:
            self.robot.power_on()
        elif self.status_label.text == 'Robot Idle':
            self.robot.brake_release()

    def on_dismiss(self):
        self.update_clock.cancel()
        self.callback()


class RobotIODialog(MDDialog):

    def __init__(self, robot, *args, **kwargs):
        self.title = 'Robot IO Control'
        self.type = 'custom'
        self.robot = robot

        self.buttons = [MDRaisedButton(text='Done', on_release=self.dismiss)]
        self.content_cls = self.create()
        super(RobotIODialog, self).__init__()

        self.update_clock = Clock.schedule_interval(self.read_input, 0.5)

    def get_card(self):
        return MDCard(orientation='vertical', focus_behavior=True, spacing="10dp")

    def get_card_title(self, **kwargs):
        return MDLabel(**kwargs, theme_text_color="Primary", valign='center', font_style='H6', bold='True',
                       adaptive_height=True)

    def get_on_btn(self, text='On', **kwargs):
        return MDRaisedButton(text=text, md_bg_color=app.theme_cls.primary_color, **kwargs)

    def get_off_btn(self, **kwargs):
        return MDFlatButton(text='Off', theme_text_color="Custom", text_color=app.theme_cls.primary_color, **kwargs)

    def get_sensor_title(self, **kwargs):
        return MDLabel(bold=True, font_style="Subtitle2", theme_text_color="Primary", **kwargs)

    def get_sensor_text(self, text='Unknown', **kwargs):
        return MDLabel(text=text, font_style="Body1", theme_text_color="Primary", **kwargs)

    def add_suction_card(self):
        card1 = self.get_card()
        cardbox1 = MDBoxLayout(orientation='vertical', adaptive_height=True, padding="10dp")
        cardbox2 = MDBoxLayout(padding=["10dp", 0, 0, "10dp"])
        cardbox3 = MDBoxLayout(padding=["10dp", 0, 0, 0])

        cardbox1.add_widget(self.get_card_title(text='Suction Cup'))
        cardbox2.add_widget(self.get_off_btn(on_release=self.robot.suction_off))
        cardbox2.add_widget(self.get_on_btn(on_release=self.robot.suction))

        cardbox3.add_widget(self.get_sensor_title(text="Status :"))
        self.suction_sensor = self.get_sensor_text()
        cardbox3.add_widget(self.suction_sensor)

        card1.add_widget(cardbox1)
        card1.add_widget(MDSeparator())
        card1.add_widget(cardbox3)
        card1.add_widget(cardbox2)

        return card1

    def add_cup_gripper_card(self):
        card1 = self.get_card()
        cardbox1 = MDBoxLayout(orientation='vertical', adaptive_height=True, padding="10dp")
        cardbox2 = MDBoxLayout(padding=["10dp", 0, 0, "10dp"])
        cardbox3 = MDBoxLayout(padding=["10dp", 0, 0, 0])

        cardbox1.add_widget(self.get_card_title(text='Cup Gripper'))
        cardbox2.add_widget(self.get_off_btn(on_release=self.robot.grip_cup_off))
        cardbox2.add_widget(self.get_on_btn(on_release=self.robot.grip_cup))

        cardbox3.add_widget(self.get_sensor_title(text="Status :"))
        self.cup_gripper_sensor = self.get_sensor_text()
        cardbox3.add_widget(self.cup_gripper_sensor)

        card1.add_widget(cardbox1)
        card1.add_widget(MDSeparator())
        card1.add_widget(cardbox3)
        card1.add_widget(cardbox2)

        return card1

    def add_needle_card(self):
        card1 = self.get_card()
        cardbox1 = MDBoxLayout(orientation='vertical', adaptive_height=True, padding="10dp")
        cardbox2 = MDBoxLayout(padding=["10dp", 0, 0, "10dp"])
        cardbox3 = MDBoxLayout(padding=["10dp", 0, 0, 0])

        cardbox1.add_widget(self.get_card_title(text='Needle'))
        cardbox2.add_widget(self.get_off_btn(on_release=self.robot.grip_cup_off))
        cardbox2.add_widget(self.get_on_btn(on_release=self.robot.grip_cup))

        cardbox3.add_widget(self.get_sensor_title(text="Status :"))
        self.needle_sensor = self.get_sensor_text()
        cardbox3.add_widget(self.needle_sensor)

        card1.add_widget(cardbox1)
        card1.add_widget(MDSeparator())
        card1.add_widget(cardbox3)
        card1.add_widget(cardbox2)

        return card1

    def add_sealer_card(self):
        card1 = self.get_card()
        cardbox1 = MDBoxLayout(orientation='vertical', adaptive_height=True, padding="10dp")
        cardbox2 = MDBoxLayout(padding=["10dp", 0, 0, "10dp"])
        cardbox3 = MDBoxLayout(padding=["10dp", 0, 0, 0])

        cardbox1.add_widget(self.get_card_title(text='Sealer'))
        cardbox2.add_widget(self.get_on_btn(text='Trigger', on_release=self.robot.sealer))

        cardbox3.add_widget(self.get_sensor_title(text="Status :"))
        self.sealer_sensor = self.get_sensor_text()
        cardbox3.add_widget(self.sealer_sensor)

        card1.add_widget(cardbox1)
        card1.add_widget(MDSeparator())
        card1.add_widget(cardbox3)
        card1.add_widget(cardbox2)

        return card1

    def add_pump_card(self):
        card1 = self.get_card()
        cardbox1 = MDBoxLayout(orientation='vertical', adaptive_height=True, padding="10dp")
        cardbox2 = MDBoxLayout(padding=["10dp", 0, 0, "10dp"])
        cardbox3 = MDBoxLayout(padding=["10dp", 0, 0, 0])

        cardbox1.add_widget(self.get_card_title(text='Pump'))
        cardbox2.add_widget(self.get_off_btn(on_release=self.robot.pump_off))
        cardbox2.add_widget(self.get_on_btn(on_release=self.robot.pump_on))

        cardbox3.add_widget(self.get_sensor_title(text="Status :"))
        self.pump_sensor = self.get_sensor_text()
        cardbox3.add_widget(self.pump_sensor)

        card1.add_widget(cardbox1)
        card1.add_widget(MDSeparator())
        card1.add_widget(cardbox3)
        card1.add_widget(cardbox2)

        return card1

    def add_load_cup_card(self):
        card1 = self.get_card()
        cardbox1 = MDBoxLayout(orientation='vertical', adaptive_height=True, padding="10dp")
        cardbox2 = MDBoxLayout(padding=["10dp", 0, 0, "10dp"])
        cardbox3 = MDBoxLayout(padding=["10dp", 0, 0, 0])

        cardbox1.add_widget(self.get_card_title(text='Load Cup'))
        cardbox2.add_widget(self.get_on_btn(text='Trigger', on_release=self.load_cup))

        cardbox3.add_widget(self.get_sensor_title(text="Status :"))
        self.pump_sensor = self.get_sensor_text()
        cardbox3.add_widget(self.pump_sensor)

        card1.add_widget(cardbox1)
        card1.add_widget(MDSeparator())
        card1.add_widget(cardbox3)
        card1.add_widget(cardbox2)

        return card1

    def load_cup(self, *args):
        Thread(target=self.robot.infinite_loop_cup).start()

    def create(self):
        boxlayout = MDBoxLayout(spacing=16, size_hint_y=None, height=600)

        box1 = MDBoxLayout(spacing=16, orientation='vertical')

        box1.add_widget(self.add_suction_card())
        box1.add_widget(self.add_cup_gripper_card())
        box1.add_widget(self.add_needle_card())

        box2 = MDBoxLayout(spacing=16, orientation='vertical')

        box2.add_widget(self.add_pump_card())
        box2.add_widget(self.add_sealer_card())
        box2.add_widget(self.add_load_cup_card())

        boxlayout.add_widget(box1)
        boxlayout.add_widget(box2)

        return boxlayout

    def read_input(self, *args):
        if not self.robot.connected:
            return

    def on_dismiss(self):
        self.update_clock.cancel()


class MoveHomeDialog(MDDialog):
    def __init__(self, pos, robot, *args, **kwargs):

        self.title = 'Robot Movement Control'
        self.type = 'custom'
        self.target = pos
        self.robot = robot
        self.content_cls = self.create()
        self.size_hint = (None, None)
        self.size = (850, 700)
        self.buttons = [
            MDRaisedButton(text='Move to position\n(Press and hold)', on_release=self.stop, on_press=self.move)]
        super(MoveHomeDialog, self).__init__()
        self.check_pos = Clock.schedule_interval(self.robot_pos_check, 0.5)

    def create(self):

        boxlayout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=250)

        self.subtitle = MDLabel(markup=True,
                                text='[b] Note : Please move the robot to home position before starting operation[/b]',
                                theme_text_color='Custom',
                                text_color=get_color_from_hex('ff0000'), font_size=20)

        self.position = MDLabel(text='')

        boxlayout.add_widget(self.subtitle)

        position_box = MDBoxLayout()
        current_box = MDBoxLayout(orientation='vertical')
        self.position = MDLabel(text='')
        current_box.add_widget(MDLabel(text='Current Position :'))
        current_box.add_widget(self.position)

        target_box = MDBoxLayout(orientation='vertical')
        self.target_label = MDLabel(text='')
        target_box.add_widget(MDLabel(text='Target Position :'))
        target_box.add_widget(self.target_label)

        position_box.add_widget(current_box)
        position_box.add_widget(target_box)
        boxlayout.add_widget(position_box)

        second_box = MDBoxLayout()
        freedrive_box = MDBoxLayout(spacing=8, size_hint_x=0.25)

        freedrive_box.add_widget(MDLabel(text='Freedrive', valign='center', bold=True))
        self.freedrive_check = MDCheckbox(on_release=self.freedrive)
        freedrive_box.add_widget(self.freedrive_check)
        # freedrive_box.add_widget(MDFlatButton(on_release=partial(self.freedrive,0),
        #                                       theme_text_color="Custom",
        #                                       text_color=app.theme_cls.primary_color,
        #                                       text='Stop',
        #                                       pos_hint={'center_y': 0.5}))
        # freedrive_box.add_widget(MDRaisedButton(on_release=partial(self.freedrive,1),text='Start',pos_hint={'center_y': 0.5}))

        second_box.add_widget(freedrive_box)
        second_box.add_widget(MDBoxLayout())
        self.alert_label = MDLabel(text='', font_size=20, theme_text_color='Custom',
                                   text_color=app.theme_cls.accent_color, halign='right')
        boxlayout.add_widget(second_box)
        boxlayout.add_widget(self.alert_label)

        return boxlayout

    def robot_pos_check(self, *args):
        curr = self.robot.get_joint()
        self.position.text = 'J1 : {:.3f} rad, J2 : {:.3f} rad, J3 : {:.3f} rad\nJ4 : {:.3f} rad, J5 : {:.3f} rad, J6 : {:.3f} rad'.format(
            *curr)
        home_pos = self.target
        self.target_label.text = 'J1 : {:.3f} rad, J2 : {:.3f} rad, J3 : {:.3f} rad\nJ4 : {:.3f} rad, J5 : {:.3f} rad, J6 : {:.3f} rad'.format(
            *home_pos)

        if not self.robot.check_homepos():
            self.alert_label.text = 'Robot not at home !'
            self.alert_label.text_color = app.theme_cls.accent_color
        else:
            self.alert_label.text_color = app.theme_cls.primary_light
            self.alert_label.text = 'Robot at home !'

    def freedrive(self, *args):
        if self.freedrive_check.active:
            self.robot.set_freedrive(1)
        else:
            self.robot.set_freedrive(0)

    def move(self, *args):
        Thread(target=self.robot.direct_movej, args=(self.target,)).start()

    def stop(self, *args):
        self.robot.robot_stop()

    def on_dismiss(self):
        self.stop()
        self.check_pos.cancel()


class EmergencyDialog(MDDialog):
    def __init__(self, robot, io, *args, **kwargs):
        self.robot = robot
        self.io = io

        self.title = 'Emergency Stop Pressed'
        self.type = 'custom'

        self.auto_dismiss = False
        self.release_button = MDRaisedButton(text='Next', on_release=self.nextpage, disabled=True)
        self.content_cls = self.create()
        self.buttons = [self.release_button]

        self.clock = Clock.schedule_interval(self.check_estop, 0.5)
        super(EmergencyDialog, self).__init__()

    def check_estop(self, *args):
        if self.robot.rtdectrl.NormalMode:
            self.release_button.disabled = False
        else:
            self.release_button.disabled = True
        self.status.text = f'Status : {self.robot.rtdectrl.safety_mode_text}'
        self.reset_button.disabled = False if self.robot.rtdectrl.Fault else True

    def create(self):
        boxlayout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=120)
        self.subtitle = MDLabel(text='Please release the E-Stop, reset fault if robot is in "FAULT" state\n'
                                     'Press "Next" and follow the instruction to recover operation\n',
                                theme_text_color='Custom',
                                text_color=app.theme_cls.disabled_hint_text_color)
        self.status = MDLabel(text='Robot')
        self.reset_button = MDRaisedButton(text='Reset Fault')
        self.reset_button.disabled = False if self.robot.rtdectrl.Fault else True
        self.reset_button.bind(on_release=self.reset_fault)
        boxlayout.add_widget(self.subtitle)

        boxlayout.add_widget(self.status)
        boxlayout.add_widget(self.reset_button)

        return boxlayout

    def reset_fault(self, *args):
        if self.reset_button.text == 'Resetting...':
            return
        Thread(target=self.robot.fault_reset).start()
        # self.robot.restart_safety()
        self.reset_button.text = 'Resetting...'
        Clock.schedule_once(self.reset_fault_button, 10)

    def reset_fault_button(self, *args):
        self.reset_button.text = 'Reset Fault'

    def nextpage(self, *args):
        self.robot.close_safety_popup()
        self.io.buzzer_off()

        if self.robot.rtdectrl.Fault:
            self.robot.restart_safety()
        else:
            RecoveryDialog(self.robot).open()
            diag = InitRobotDialog(self.robot, self.dismiss, must=True)
            diag.auto_dismiss = False
            diag.open()
            self.dismiss()

    def on_dismiss(self):
        self.clock.cancel()


class RecoveryDialog(MDDialog):
    def __init__(self, robot, *args, **kwargs):

        self.title = 'Robot Movement Control'
        self.type = 'custom'
        self.target = robot.lastmove[1] if len(robot.lastmove) > 1 else None
        self.robot = robot
        self.content_cls = self.create()
        self.size_hint = (None, None)
        self.size = (850, 700)
        self.buttons = [
            MDRaisedButton(text='Move to position\n(Press and hold)', on_release=self.stop, on_press=self.move,
                           disabled=True if self.target is None else False)]
        super(RecoveryDialog, self).__init__()

        self.check_pos = Clock.schedule_interval(self.robot_pos_check, 0.5)

    def create(self):

        boxlayout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=270)

        self.subtitle = MDLabel(text='Please move the robot to the next position before resuming operation\n'
                                     'Use IO Screen to control the I/O if required\n'
                                     'This tab can be revisited under "Move Recovery"',
                                theme_text_color='Custom',
                                text_color=app.theme_cls.disabled_hint_text_color)

        boxlayout.add_widget(self.subtitle)

        position_box = MDBoxLayout()
        current_box = MDBoxLayout(orientation='vertical')
        self.position = MDLabel(text='')
        current_box.add_widget(MDLabel(text='Current Position :'))
        current_box.add_widget(self.position)

        target_box = MDBoxLayout(orientation='vertical')
        self.target_label = MDLabel(text='')
        target_box.add_widget(MDLabel(text='Target Position :'))
        target_box.add_widget(self.target_label)

        position_box.add_widget(current_box)
        position_box.add_widget(target_box)
        boxlayout.add_widget(position_box)

        second_box = MDBoxLayout()
        freedrive_box = MDBoxLayout(spacing=8, size_hint_x=0.25)
        freedrive_box.add_widget(MDLabel(text='Freedrive', valign='center', bold=True))
        self.freedrive_check = MDCheckbox(on_release=self.freedrive)
        freedrive_box.add_widget(self.freedrive_check)
        # freedrive_box.add_widget(MDFlatButton(on_release=partial(self.freedrive, 0),
        #                                       theme_text_color="Custom",
        #                                       text_color=app.theme_cls.primary_color,
        #                                       text='Stop',
        #                                       pos_hint={'center_y': 0.5}))
        # freedrive_box.add_widget(
        #     MDRaisedButton(on_release=partial(self.freedrive, 1), text='Start', pos_hint={'center_y': 0.5}))

        second_box.add_widget(freedrive_box)
        second_box.add_widget(MDBoxLayout())
        self.alert_label = MDLabel(text='', font_size=20, theme_text_color='Custom',
                                   text_color=app.theme_cls.accent_color, halign='right')
        boxlayout.add_widget(second_box)
        boxlayout.add_widget(self.alert_label)

        return boxlayout

    def robot_pos_check(self, *args):
        if self.target is None:
            self.position.text = 'Unavailable'
            self.target_label.text = 'Unavailable'
            return

        if self.robot.lastmove[0] == 'l' or self.robot.lastmove[0] == 'lf':
            self.linear_check()
        elif self.robot.lastmove[0] == 'j':
            self.joint_check()
        elif self.robot.lastmove[0] == 'ls':
            self.target = self.robot.lastmove[1][-1]
            self.linear_check()
        elif self.robot.lastmove[0] == 'js':
            self.target = self.robot.lastmove[1][-1]
            self.joint_check()

    def joint_check(self):
        curr = self.robot.get_joint()
        home_pos = self.target

        self.position.text = 'J1 : {:.3f} rad, J2 : {:.3f} rad, J3 : {:.3f} rad\nJ4 : {:.3f} rad, J5 : {:.3f} rad, J6 : {:.3f} rad'.format(
            *curr)
        self.target_label.text = 'J1 : {:.3f} rad, J2 : {:.3f} rad, J3 : {:.3f} rad\nJ4 : {:.3f} rad, J5 : {:.3f} rad, J6 : {:.3f} rad'.format(
            *home_pos)

        for i in range(len(curr)):
            if abs(curr[i] - home_pos[i]) > 0.1:
                self.alert_label.text_color = app.theme_cls.accent_color
                self.alert_label.text = 'Robot not at position'
                return

        self.alert_label.text_color = app.theme_cls.primary_light
        self.alert_label.text = 'Robot at position'

    def linear_check(self):
        curr = self.robot.get_pose()
        home_pos = self.target

        self.position.text = 'x : {:.3f} mm, y : {:.3f} mm, z : {:.3f} mm\nrx : {:.3f} rad, ry : {:.3f} rad, rz : {:.3f} rad'.format(
            *curr)
        self.target_label.text = 'x : {:.3f} mm, y : {:.3f} mm, z : {:.3f} mm\nrx : {:.3f} rad, ry : {:.3f} rad, rz : {:.3f} rad'.format(
            *home_pos)
        curr[0] = curr[0] / 1000
        curr[1] = curr[1] / 1000
        curr[2] = curr[2] / 1000

        curr = self.robot.get_pose()
        for i in range(3):
            if abs(curr[i] - home_pos[i]) > 0.0005:
                self.alert_label.text_color = app.theme_cls.accent_color
                self.alert_label.text = 'Robot not at position'
                return
        for i in range(3):
            if abs(curr[i + 3] - home_pos[i + 3]) > 0.1:
                self.alert_label.text_color = app.theme_cls.accent_color
                self.alert_label.text = 'Robot not at position'
                return

        self.alert_label.text_color = app.theme_cls.primary_light
        self.alert_label.text = 'Robot at position'

    def freedrive(self, *args):
        if self.freedrive_check.active:
            self.robot.set_freedrive(1)
        else:
            self.robot.set_freedrive(0)

    def move(self, *args):
        # if self.robot.lastmove[0] == 'j':
        #     Thread(target=self.robot.direct_movej, args=(self.target,)).start()
        # else:
        #     Thread(target=self.robot.direct_movel, args=(self.target,)).start()
        Thread(target=self.robot.completelastmove).start()

    def stop(self, *args):
        self.robot.robot_stop()

    def on_dismiss(self):
        operationscreen = app.root.ids.operation_screen
        if operationscreen.safety_dialog_open:
            operationscreen.safety_dialog_open = False
            if self.robot.program_running:
                operationscreen.initiate_record()
        self.check_pos.cancel()
        self.robot.set_freedrive(0)

        if self.robot.is_running():
            self.stop()


class ProtectiveDialog(MDDialog):

    def __init__(self, robot, io, error_callback, *args, **kwargs):
        self.auto_dismiss = False
        self.title = 'Protective Stop Activated'
        self.t1 = f'Robot {robot.rtdectrl.safety_mode_text}\n'
        self.t2 = f'Unlock the robot and follow the instruction to recover operation\n'
        self.countdown_text = 'Unlock will be available in {} seconds'

        self.text = self.t1 + self.t2 + self.countdown_text
        self.robot = robot
        self.io = io
        self.error_callback = error_callback
        self.auto_dismiss = False

        self.release_button = MDRaisedButton(text='Unlock', disabled=True)
        self.buttons = [self.release_button]
        self.count = 0
        super(ProtectiveDialog, self).__init__()
        Clock.schedule_once(self.unlock_button, -1)
        # self.send_email()

    def send_email(self):
        detail = 'Protective Stop Triggered'
        content = f'Robot Status : {self.robot.rtdectrl.safety_mode_text}'
        Thread(target=send_mail, kwargs={'detail': detail, 'type': 'error', 'content': content}).start()

    def unlock_button(self, *args):
        self.release_button.bind(on_release=self.nextpage)
        if self.count >= 5:
            self.text = self.t1 + self.t2 + '\n'
            self.release_button.disabled = False
        else:
            self.countdown_text = f'Unlock will be available in {5 - self.count} seconds'
            self.text = self.t1 + self.t2 + self.countdown_text
            self.count += 1

            Clock.schedule_once(self.unlock_button, 1)

    def nextpage(self, *args):
        self.io.buzzer_off()
        if self.robot.start_place_oven:
            self.robot.skip_move = True
            num = self.robot.heated_blade
            self.robot.fail_list.append(num + 1)
            print(self.robot.fail_list)
            self.error_callback('0013')

        if self.robot.rtdectrl.ProtectiveStopped:
            self.robot.unlock_protective_stop()
        elif self.robot.rtdectrl.Fault:
            self.robot.restart_safety()
        else:
            self.robot.close_safety_popup()
            diag = InitRobotDialog(self.robot, self.dismiss, must=True)
            diag.auto_dismiss = False
            diag.open()
        self.dismiss()

class LowPressureDialog(MDDialog):
    def __init__(self, *args, **kwargs):
        self.auto_dismiss = False
        self.title = 'Low Pressure Detected'
        self.text = f'Ensure the pressure level is normal before continuing'

        self.release_button = MDRaisedButton(text='OK', on_release=self.ok)
        self.buttons = [self.release_button]
        super(LowPressureDialog, self).__init__()

    def ok(self, *args):
        self.dismiss()


class UpdatePositionDialog(MDDialog):
    def __init__(self, pos, new, type, key, callback, *args, **kwargs):

        self.title = 'Confirm Update Position?'
        self.type = 'custom'
        self.current_pos = pos
        self.new = new
        self.key = key
        self.move_type = type
        self.callback = callback

        self.content_cls = self.create()
        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        MDRaisedButton(text='Confirm', on_release=self.confirm)]
        super(UpdatePositionDialog, self).__init__()

    def create(self):
        layout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=200)
        current = self.current_pos
        new = self.new

        title1 = MDLabel(text=f'Updating [b]{self.key}[/b] from ', markup=True)
        self.current_label = MDLabel(markup=True)
        text1 = MDLabel(text=f'to', markup=True)
        self.new_label = MDLabel(markup=True)

        if self.move_type == 'Linear':
            self.current_label.text = '[b]x[/b] : {:.2f}, [b]y[/b] : {:.2f}, [b]z[/b] : {:.2f}, [b]rx[/b] : {:.2f}, [b]ry[/b] : {:.2f}, [b]rz[/b] : {:.2f}'.format(
                current[0] * 1000, current[1] * 1000, current[2] * 1000, current[3], current[4], current[5])
            self.new_label.text = '[b]x[/b] : {:.2f}, [b]y[/b] : {:.2f}, [b]z[/b] : {:.2f}, [b]rx[/b] : {:.2f}, [b]ry[/b] : {:.2f}, [b]rz[/b] : {:.2f}'.format(
                new[0] * 1000, new[1] * 1000, new[2] * 1000, new[3], new[4], new[5])
        else:
            self.current_label.text = '[b]J1[/b] : {:.2f}, [b]J2[/b] : {:.2f}, [b]J3[/b] : {:.2f}, [b]J4[/b] : {:.2f}, [b]J5[/b] : {:.2f}, [b]J6[/b] : {:.2f}'.format(
                current[0], current[1], current[2], current[3], current[4], current[5])
            self.new_label.text = '[b]J1[/b] : {:.2f}, [b]J2[/b] : {:.2f}, [b]J3[/b] : {:.2f}, [b]J4[/b] : {:.2f}, [b]J5[/b] : {:.2f}, [b]J6[/b] : {:.2f}'.format(
                new[0], new[1], new[2], new[3], new[4], new[5])

        layout.add_widget(title1)
        layout.add_widget(self.current_label)
        layout.add_widget(text1)
        layout.add_widget(self.new_label)
        return layout

    def confirm(self, *args):
        self.callback(self.key, self.new)
        self.dismiss()


class UpdateParameterDialog(MDDialog):
    def __init__(self, current, new, key, callback, *args, **kwargs):
        self.title = 'Confirm Update Parameter?'
        self.type = 'custom'
        self.current = current
        self.new = new
        self.key = key
        self.callback = callback

        self.content_cls = self.create()
        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        MDRaisedButton(text='Confirm', on_release=self.confirm)]
        super(UpdateParameterDialog, self).__init__()

    def create(self):
        layout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=59)

        title1 = MDLabel(text=f'Updating [b]{self.key}[/b] from [b]{self.current}[/b] to [b]{self.new} ', markup=True)
        # self.current_label = MDLabel(markup=True,text=f'{self.current}')
        # text1 = MDLabel(text=f'to',markup=True)
        # self.new_label = MDLabel(markup=True,text=f'{self.new}')

        layout.add_widget(title1)
        # layout.add_widget(self.current_label)
        # layout.add_widget(text1)
        # layout.add_widget(self.new_label)
        return layout

    def confirm(self, *args):
        self.callback(self.key, self.new)
        self.dismiss()


class AddRemarkDialog(MDDialog):
    def __init__(self, callback, remark, *args, **kwargs):
        self.title = 'Enter Remarks'
        self.type = 'custom'
        self.callback = callback
        self.remark = remark
        self.content_cls = self.create()
        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        MDRaisedButton(text='Confirm', on_release=self.confirm)]
        super(AddRemarkDialog, self).__init__()

    def create(self):
        layout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=170)
        subtitle = MDLabel(text="Remarks will apply to the most recent job",
                           font_style='Body1',
                           valign='top',
                           markup=True,
                           text_color=app.theme_cls.disabled_hint_text_color,
                           theme_text_color='Custom',
                           adaptive_height=True)

        self.mytext = MDTextField(multiline=True, text=f'{self.remark}', hint_text='Your Remarks', max_height="150dp",
                                  height="150dp")

        layout.add_widget(subtitle)
        layout.add_widget(self.mytext)
        return layout

    def confirm(self, *args):
        self.callback(self.mytext.text)
        self.dismiss()


class ErrorDialog(MDDialog):
    def __init__(self, callback, code, *args, test=False, **kwargs):

        self.title = 'Operation Error!'
        self.type = 'custom'
        self.callback = callback
        self.auto_dismiss = False
        self.get_error(code)
        self.content_cls = self.create()
        self.buttons = [
            MDRaisedButton(text='Acknowledge', on_release=self.dismiss, md_bg_color=app.theme_cls.accent_color)]
        self.robot_func = app.root.ids.io_screen
        super(ErrorDialog, self).__init__()
        if not test:
            self.send_email()

    def get_error(self, code):
        self.code = code
        self.message = 'Unknown Error Code'
        self.resolve = ''
        self.recovery = []

        # make sure the codes are declared properly
        if code in error_codes:
            if 'message' in error_codes[code]:
                self.message = error_codes[code]['message']
            if 'resolve' in error_codes[code]:
                self.resolve = error_codes[code]['resolve']
            if 'recovery' in error_codes[code]:
                self.recovery = error_codes[code]['recovery']

    def send_email(self):
        detail = 'Operation Error'
        content = f'<p>Error Code : {self.code}</p>' \
                  f'<p>Error Message : {self.message}</p>' \
                  f'<p>Resolving Step : {self.resolve}</p>'
        Thread(target=send_mail, kwargs={'detail': detail, 'type': 'error', 'content': content}).start()

    def create(self):
        layout = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None,
                             height=320 + (50 * len(self.recovery)))
        error_code = MDLabel(text=f'Error Code : {self.code}', size_hint_y=0.5, bold=True, theme_text_color='Custom',
                             text_color=app.theme_cls.accent_color)
        error_layout = MDBoxLayout(orientation='vertical', adaptive_height=True)
        error_title = MDLabel(text='Message', bold=True, underline=True)
        error_msg = MDLabel(markup=True,
                            text=f'{self.message}', )
        error_layout.add_widget(error_title)
        error_layout.add_widget(error_msg)

        sol_layout = MDBoxLayout(orientation='vertical', adaptive_height=True)
        sol_title = MDLabel(text='Solution', bold=True, underline=True)
        sol_msg = MDLabel(markup=True,
                          text=f'{self.resolve}', )
        sol_layout.add_widget(sol_title)
        sol_layout.add_widget(sol_msg)

        self.recovery_layout = MDBoxLayout(orientation='vertical', size_hint_y=3)

        self.recovery_layout.add_widget(MDLabel(text='Recovery', underline=True, bold=True))
        self.add_recovery()

        layout.add_widget(error_code)
        layout.add_widget(error_layout)
        layout.add_widget(sol_layout)
        layout.add_widget(self.recovery_layout)

        return layout

    def add_recovery(self):
        for no, i in enumerate(self.recovery):
            label = MDLabel(text=f'Step {no + 1} : {i}')
            self.recovery_layout.add_widget(label)

    def on_dismiss(self):
        self.callback()


class RestartDialog(MDDialog):
    def __init__(self, robot, *args, **kwargs):
        self.title = 'Robot Fault detected !'
        self.text = 'Press the Restart Robot button and wait for 5 seconds to restart robot '
        self.type = 'custom'
        self.robot = robot
        self.buttons = [MDRaisedButton(text='Restart Robot', on_release=self.restart_robot,
                                       md_bg_color=get_color_from_hex('ff0000')),
                        MDRaisedButton(text='Confirm', on_release=self.dismiss)
                        ]

        super(RestartDialog, self).__init__()

    def restart_robot(self):
        self.robot.close_safety_popup()
        self.robot.restart_safety()


class FinishedDialog(MDDialog):
    def __init__(self, stop, update, *args, **kwargs):
        self.title = 'Operation Cycle Completed'
        self.text = 'Do you want to run another cycle?\nPressing "Yes" will not start the operation'
        self.stopall = stop
        self.update = update
        self.auto_dismiss = False
        # self.buttons = [MDRaisedButton(text='Yes', on_release=self.yesbutton, md_bg_color=get_color_from_hex('6FE5BD')),
        #                 MDRaisedButton(text='No', on_release=self.nobutton, md_bg_color=get_color_from_hex('ff0000'))
        #                 ]
        self.buttons = [MDFlatButton(text='Stop', on_release=self.nobutton, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        MDRaisedButton(text='Yes', on_release=self.yesbutton)]
        super(FinishedDialog, self).__init__()

    def yesbutton(self, *args):
        # second run to true
        # update start button to 'continue run'
        self.update()
        # SecondRunDialog().open()
        self.dismiss()

    def nobutton(self, *args):
        self.stopall()
        # update start button to 'Start'
        self.dismiss()

class BladeDetailsDialog(MDDialog):
    def __init__(self, serial, partnum, serial2, partnum2, *args, **kwargs):
        self.title = 'Selected Blade details'
        self.type = 'custom'
        self.serial = serial
        self.partnum = partnum
        self.serial2 = serial2
        self.partnum2 = partnum2
        self.content_cls = self.create()

        super(BladeDetailsDialog, self).__init__()

    def create(self, ):
        box = MDBoxLayout(orientation='vertical', spacing=12, padding=6, size_hint_y=None, height=220)

        title1 = MDLabel(text='Selected Blade No 1', markup=True, underline=True, bold=True)
        title2 = MDLabel(text='Selected Blade No 2', markup=True, underline=True, bold=True)

        label1 = MDLabel(markup=True, font_size=20, text=f'[b]SMO number 1[/b]     :       {self.serial}')
        label2 = MDLabel(markup=True, font_size=20, text=f'[b]Part number 1[/b]        :       {self.partnum}')

        label12 = MDLabel(markup=True, font_size=20, text=f'[b]SMO number 2[/b]    :       {self.serial2}')
        label22 = MDLabel(markup=True, font_size=20, text=f'[b]Part number 2[/b]       :       {self.partnum2}')

        selectedbox1 = MDBoxLayout(orientation='vertical', spacing=6)
        selectedbox2 = MDBoxLayout(orientation='vertical', spacing=6)
        emptybox = MDBoxLayout(spacing=10)

        selectedbox1.add_widget(label1)
        selectedbox1.add_widget(label2)

        selectedbox2.add_widget(label12)
        selectedbox2.add_widget(label22)

        # box.add_widget(title1)
        box.add_widget(selectedbox1)
        # box.add_widget(title2)
        box.add_widget(selectedbox2)

        return box


class EnterDetail(MDDialog):
    def __init__(self, blades, partnumbers, callback, update, info, run1, run2, *args, **kwargs):

        self.title = 'Enter Blade details'
        self.type = 'custom'
        self.callback = callback
        self.partnumbers = partnumbers
        self.blades = blades
        self.info = info
        self.run1 = run1
        self.run2 = run2
        self.update = update
        self.content_cls = self.create()
        self.buttons = [MDRaisedButton(text='Save', on_release=self.yes)]

        super(EnterDetail, self).__init__()

    def create(self):
        box = MDBoxLayout(orientation='vertical', spacing=12, padding=6, size_hint_y=None, height="480sp")

        self.s1 = self.info[0] if self.info[0] is not None else ''
        self.p1 = self.info[1] if self.info[1] is not None else ''
        self.s2 = self.info[2] if self.info[2] is not None else ''
        self.p2 = self.info[3] if self.info[3] is not None else ''
        self.selected_blade = self.info[4] if self.info[4] is not None else ''
        self.selected_blade2 = self.info[5] if self.info[5] is not None else ''

        self.enter_serial1 = MDTextField(max_text_length=20, text=self.s1, write_tab=False,
                                         hint_text='Please enter SMO number', )
        self.enter_part1 = MDTextField(max_text_length=20, text=self.p1, write_tab=False,
                                       hint_text='Please enter part number', )
        self.enter_serial2 = MDTextField(max_text_length=20, text=self.s2, write_tab=False,
                                         hint_text='Please enter SMO number', )
        self.enter_part2 = MDTextField(max_text_length=20, text=self.p2, write_tab=False,
                                       hint_text='Please enter part number', )

        title1 = MDLabel(text='[b][u]Tray 1[u][b]', markup=True)
        title2 = MDLabel(text='[b][u]Tray 2[u][b]', markup=True)
        box1 = MDBoxLayout(orientation='vertical', spacing=6)
        box2 = MDBoxLayout(orientation='vertical', spacing=6)
        boxin1 = MDBoxLayout(orientation='horizontal', spacing=6)
        boxin2 = MDBoxLayout(orientation='horizontal', spacing=6)

        self.input1 = MDTextField(max_text_length=2, text='24', write_tab=False,
                                  hint_text='Please enter quantities to run', )
        self.input2 = MDTextField(max_text_length=2, text='24', write_tab=False,
                                  hint_text='Please enter quantities to run', )

        self.menu = MDDropdownMenu()
        self.recipe_dropdown = MDDropDownItem(on_release=self.open_menu, size_hint_x=None, pos_hint={'center_y': 0.5}, )

        if self.selected_blade != '':
            self.recipe_dropdown.text = f'{self.selected_blade}'
        else:
            self.recipe_dropdown.text = 'Please Select'
        titles = ["Please Select"] + [i for i in self.blades]
        menu_items = [
            {
                "text": f"{titles[i]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{titles[i]}": self.menu_callback(x),
            } for i in range(len(titles))
        ]
        self.menu.caller = self.recipe_dropdown
        self.menu.items = menu_items
        self.menu.width_mult = 4
        self.menu.max_height = 250

        self.menu2 = MDDropdownMenu()
        self.recipe_dropdown2 = MDDropDownItem(on_release=self.open_menu2, size_hint_x=0.9, pos_hint={'center_y': 0.5})

        if self.selected_blade2 != '':
            self.recipe_dropdown2.text = f'{self.selected_blade2}'
        else:
            self.recipe_dropdown2.text = 'Please Select'

        titles2 = ["Please Select"] + [i for i in self.blades]
        menu2_items = [
            {
                "text": f"{titles[i]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{titles[i]}": self.menu2_callback(x),
            } for i in range(len(titles))
        ]
        self.menu2.caller = self.recipe_dropdown2
        self.menu2.items = menu2_items
        self.menu2.width_mult = 4
        self.menu2.max_height = 250

        if self.run1:
            self.enter_serial1.disabled = True
            self.enter_part1.disabled = True
            self.recipe_dropdown.disabled = True

        if self.run2:
            self.enter_serial2.disabled = True
            self.enter_part2.disabled = True
            self.recipe_dropdown2.disabled = True

        if not self.run1:
            self.enter_serial1.disabled = False
            self.enter_part1.disabled = False
            self.recipe_dropdown.disabled = False

        if not self.run2:
            self.recipe_dropdown2.disabled = False
            self.enter_serial2.disabled = False
            self.enter_part2.disabled = False

        boxin1.add_widget(title1)
        boxin1.add_widget(self.input1)
        box1.add_widget(boxin1)
        box1.add_widget(self.recipe_dropdown)
        box1.add_widget(self.enter_serial1)
        box1.add_widget(self.enter_part1)

        boxin2.add_widget(title2)
        boxin2.add_widget(self.input2)
        box2.add_widget(boxin2)
        box2.add_widget(self.recipe_dropdown2)
        box2.add_widget(self.enter_serial2)
        box2.add_widget(self.enter_part2)
        box.add_widget(box1)
        box.add_widget(box2)

        return box

    def yes(self, *args):
        if not self.run1:
            if self.enter_serial1.text != '' or self.enter_part1.text != '' or (
                    self.selected_blade != '' and self.selected_blade != 'Please Select'):
                if self.enter_serial1.text == '':
                    return toast("SMO cannot be empty")

                if len(self.enter_serial1.text) > self.enter_serial1.max_text_length:
                    return toast("SMO exceed maximum length")

                if self.enter_part1.text == '':
                    return toast("Part number cannot be empty")

                if len(self.enter_part1.text) > self.enter_part1.max_text_length:
                    return toast("Part exceed maximum length")

                if self.selected_blade == '':
                    return toast("Please select tray 1 blade")

                if self.input1.text == '':
                    self.input1.text = '24'
                    # toast("Please enter total number of blade to run")

                # if self.enter_part1.text not in self.partnumbers[self.selected_blade]:
                #     return toast('Selected part does not match with part number')

                self.update(blade=self.selected_blade)
                self.callback(serial=self.enter_serial1.text, part=self.enter_part1.text, input1=self.input1.text)

        if not self.run2:
            if self.enter_serial2.text != '' or self.enter_part2.text != '' or (
                    self.selected_blade2 != '' and self.selected_blade2 != 'Please Select'):

                if self.enter_serial2.text == '':
                    return toast("SMO 2 cannot be empty")

                if len(self.enter_serial2.text) > self.enter_serial2.max_text_length:
                    return toast("SMO 2 exceed maximum length")

                if self.enter_part2.text == '':
                    return toast("Part2 number cannot be empty")

                if len(self.enter_part2.text) > self.enter_part2.max_text_length:
                    return toast("Part2 exceed maximum length")

                if self.selected_blade2 == '':
                    return toast("Please select tray 2 blade")

                if self.input2.text == '':
                    self.input2.text = '24'
                    # toast("Please enter total number of blade to run")
                # if self.enter_part2.text not in self.partnumbers[self.selected_blade2]:
                #     return toast('Selected part does not match with part number')

                self.update(blade2=self.selected_blade2)
                self.callback(serial2=self.enter_serial2.text, part2=self.enter_part2.text, input2=self.input2.text)

        # if self.enter_text.text in self.names:
        #     toast("Name already exists")
        #     return
        toast("Blade details saved")
        self.dismiss()

    def open_menu(self, *args):
        self.menu.open()
        self.info = None

    def open_menu2(self, *args):
        self.menu2.open()
        self.info = None

    def menu_callback(self, text_item, *args):
        self.recipe_dropdown.text = text_item if self.info is None else self.info[4]  # or self.selected_blade == ''
        self.selected_blade = text_item
        self.menu.dismiss()

    def menu2_callback(self, text_item, *args):
        self.recipe_dropdown2.text = text_item if self.info is None else self.info[5]  # or self.selected_blade2 == ''
        self.selected_blade2 = text_item
        self.menu2.dismiss()


class ConnectAll(MDDialog):
    animate_robot_connect_clock = None

    def __init__(self,plc, callback, **kwargs):
        self.title = 'Connection Status'
        self.type = 'custom'
        self.callback = callback
        # self.robot = robot
        self.plc = plc
        # self.motor = motor
        self.theme = app.theme_cls
        self.connect_text = 'Connecting'
        self.operationscreen = app.root.ids.operation_screen
        self.config = self.operationscreen.config
        self.content_cls = self.create()

        super(ConnectAll, self).__init__()
        # self.start_animate()

    def status_label(self, text):
        return MDLabel(text=text, markup=True, theme_text_color='Custom', text_color=self.theme.text_color)

    def create(self):
        box = MDBoxLayout(orientation='vertical', spacing=12, padding=[6, 12], size_hint_y=None, height="300sp",
                          width=200)
        # robot_box = MDBoxLayout(orientation='vertical', spacing=10)
        # robot_box1 = MDBoxLayout(spacing=10)
        # label4 = MDLabel(text='Robot', underline=True, bold=True)
        # self.robot_label = self.status_label('')
        # self.robot_conn = MDRoundFlatButton(text='Connect', on_release=self.robot_conn_btn, pos_hint={'center_y': 0.5})
        # self.robot_init = MDRoundFlatButton(text='Initialize', on_release=self.robot_init_btn,
        #                                     pos_hint={'center_y': 0.5})
        #
        # robot_box1.add_widget(self.robot_label)
        # robot_box1.add_widget(self.robot_conn)
        # robot_box1.add_widget(self.robot_init)
        # robot_box.add_widget(label4)
        # robot_box.add_widget(robot_box1)

        motor_box = MDBoxLayout(orientation='vertical', spacing=10)
        box_label2 = MDBoxLayout(orientation='horizontal', spacing=10, )
        label2 = MDLabel(text='Motor Controller', underline=True, bold=True)
        self.motor_label = self.status_label('[b]Status[/b] : Not Connected')
        self.motor_conn = MDRoundFlatButton(text='Connect', on_release=self.motor_conn_butt, pos_hint={'center_y': 0.5})

        plc_box = MDBoxLayout(orientation='vertical', spacing=10)
        box_label3 = MDBoxLayout(orientation='horizontal', spacing=10, )
        label3 = MDLabel(text='PLC ', underline=True, bold=True)
        self.plc_label = self.status_label('[b]Status[/b] : Not Connected')
        self.plc_conn = MDRoundFlatButton(text='Connect', on_release=self.plc_conn_butt, pos_hint={'center_y': 0.5})

        # con_all_box = MDBoxLayout(orientation='vertical', spacing=10)
        # box_label5 = MDBoxLayout(orientation='horizontal', spacing=10)
        # self.all_label = self.status_label('')
        # self.all_conn = MDRoundFlatButton(text='Connect All',size_hint=(0.3,0.8), md_bg_color="#fefbff", on_release=self.all_conn_butt, pos_hint={'center_y': 0.5})

        box_label2.add_widget(self.motor_label)
        box_label2.add_widget(self.motor_conn)
        motor_box.add_widget(label2)
        motor_box.add_widget(box_label2)

        box_label3.add_widget(self.plc_label)
        box_label3.add_widget(self.plc_conn)
        plc_box.add_widget(label3)
        plc_box.add_widget(box_label3)

        # box_label5.add_widget(self.all_label)
        # box_label5.add_widget(self.all_conn)
        # con_all_box.add_widget(box_label5)

        # box.add_widget(robot_box)
        # box.add_widget(MDSeparator())
        # box.add_widget(motor_box)
        # box.add_widget(MDSeparator())
        box.add_widget(plc_box)
        # box.add_widget(con_all_box)

        # self.update_robot_status()
        self.update_all_status()
        return box

    def update_robot_status(self):
        if self.robot.connected and self.robot.rtdectrl.received_pkg:
            self.robot_conn.text = 'Disconnect'
            if 'RUNNING' in self.robot.get_robot_mode():
                self.robot_label.text_color = self.theme.primary_light
                self.robot_label.text = f'[b]Status[/b] : Ready'
            else:
                self.robot_label.text_color = self.theme.error_color
                self.robot_label.text = f'[b]Status[/b] : Not Initialized'
        else:
            self.robot_label.text_color = self.theme.text_color
            self.robot_label.text = f'[b]Status[/b] : Not Connected'

    def update_all_status(self):
        # if self.motor.connected:
        #     self.motor_conn.text = 'Disconnect'
        #     self.motor_label.text = '[b]Status[/b] : ' + 'Connected'
        #     self.motor_label.text_color = self.theme.primary_light

        if self.plc.connected:
            self.plc_conn.text = 'Disconnect'
            self.plc_label.text = '[b]Status[/b] : ' + 'Connected'
            self.plc_label.text_color = self.theme.primary_light

    def robot_conn_btn(self, *args):
        if self.robot.connecting:
            self.robot.connecting = False
            self.robot_conn.text = 'Connect'
            self.animate_robot_connect_clock.cancel()
            self.animate_robot_connect_clock = None
            self.update_robot_status()
            return
        if not self.robot.connected:
            Thread(target=self.operationscreen.connect_robot, name='Robot Connect').start()
            self.start_animate()
        else:
            DisconnectDialog(self.disconnect_robot, 'Robot').open()

    def disconnect_robot(self):
        self.robot.disconnect()
        self.robot_conn.text = 'Connect'
        self.update_robot_status()

    def start_animate(self):
        self.robot_label.text_color = self.theme.text_color
        self.connect_time = time.time()
        self.animate_robot_connect_clock = Clock.schedule_interval(self.animate_robot_connect, 0.2)

    def animate_robot_connect(self, *args):
        if self.robot.connecting == False:
            self.animate_robot_connect_clock.cancel()
            self.animate_robot_connect_clock = None
            self.update_robot_status()
            return
        if time.time() - self.connect_time <= 5:
            if self.connect_text == 'Connecting...' or self.connect_text == 'Trying to Connect...':
                self.connect_text = 'Connecting'
            else:
                self.connect_text += '.'
        elif time.time() - self.connect_time <= 10:
            if self.connect_text == 'Please Wait...' or self.connect_text == 'Connecting...':
                self.connect_text = 'Please Wait'
            else:
                self.connect_text += '.'
        elif time.time() - self.connect_time <= 15:
            if self.connect_text == 'Trying to Connect...' or self.connect_text == 'Please Wait...':
                self.connect_text = 'Trying to Connect'
            else:
                self.connect_text += '.'
        else:
            self.connect_time = time.time()
        self.robot_label.text = '[b]Status[/b] : ' + self.connect_text

    def robot_init_btn(self, *args):
        if not self.robot.connected:
            ConnectRobotDialog().open()
        else:
            InitRobotDialog(self.robot, self.update_robot_status).open()

    def motor_conn_butt(self, *args):
        if not self.motor.connected:
            self.motor.connect(self.config['Motor Controller Port'])
            if self.motor.connected:
                self.motor_conn.text = 'Disconnect'
                self.motor_label.text = '[b]Status[/b] : Connected'
                self.motor_label.text_color = self.theme.primary_light
                toast('Sucessfully connected to Motor Controller')
            else:
                self.motor_conn.text = 'Connect'
                self.motor_label.text = '[b]Status[/b] : Not Connected'
                self.motor_label.text_color = self.theme.text_color
                toast('Failed connecting to Motor Controller')
        else:
            self.motor.disconnect()
            self.motor_conn.text = 'Connect'
            self.motor_label.text = '[b]Status[/b] : Disconnected'
            self.motor_label.text_color = self.theme.error_color
            toast('Disconnected Motor Controller')

    def plc_conn_butt(self,*args):
        if not self.plc.connected:
            print(self.config['PLC IP'])
            print(type(self.config['PLC IP']))
            self.plc.connect(str(self.config['PLC IP']))
            if self.plc.connected:
                self.plc_conn.text = 'Disconnect'
                self.plc_label.text = '[b]Status[/b] : Connected'
                self.plc_label.text_color = self.theme.primary_light
                toast('Sucessfully connected to PLC')
            else:
                self.plc_conn.text = 'Connect'
                self.plc_label.text = '[b]Status[/b] : Not Connected'
                self.plc_label.text_color = self.theme.text_color
                toast('Failed connecting to PLC')
        else:
            self.plc.disconnect()
            self.plc_conn.text = 'Connect'
            self.plc_label.text = '[b]Status[/b] : Disconnected'
            self.plc_label.text_color = self.theme.error_color
            toast('Disconnected PLC communication')

    def all_conn_butt(self,*args):
        if not self.robot.connected:
            self.robot_conn_btn()
        if not self.motor.connected:
            self.motor_conn_butt()

    def on_dismiss(self):
        # if self.therm.connected and self.io.connected and self.motor.connected and self.robot.connected and self.illu.connected and 'RUNNING' in self.robot.get_robot_mode():
        if self.plc.connected :
            self.callback(1)
        else:
            self.callback(0)

class DoorOpenedDialog(MDDialog):
    def __init__(self, io, callback, resume, *args, **kwargs):
        self.title = 'Door Opened'
        self.type = 'custom'
        self.io = io
        self.theme = app.theme_cls
        self.callback = callback
        self.resume = resume

        self.content_cls = self.create()
        # self.buttons = [MDRaisedButton(text='Dismiss', on_release=self.manual_close)]
        self.auto_dismiss = False

        super(DoorOpenedDialog, self).__init__()
        self.check_status = Clock.schedule_interval(self.check_door, 0.1)
        self.countdown_trigger = Clock.create_trigger(self.countdown, 0.5)
        self.timenow = time.time()

    def create(self):
        box = MDBoxLayout(orientation='vertical', spacing=12, padding=6, size_hint_y=None, height="500", width=200)

        return box

    def countdown(self, *args):
        self.ids.countdown_text.text = f'Door Closed, resuming operation in  [b]{5 - round(time.time() - self.timenow)}'
        if time.time() - self.timenow > 4:
            # resume process also
            self.resume()
            self.dismiss()
            self.countdown_trigger.cancel()
        elif time.time() - self.timenow < 1:
            self.ids.countdown_text.text = 'Close all doors to resume operation'
            self.countdown_trigger.cancel()
        else:
            self.countdown_trigger()

    def check_door(self, *args):
        # read door status
        if self.io.finished_door_sensor == 0:
            self.ids.left_door1.background_color = self.theme_cls.primary_light
        else:
            self.ids.left_door1.background_color = self.theme_cls.error_color

        if self.io.tray_door_sensor == 0:
            self.ids.front_door1.background_color = self.theme_cls.primary_light
        else:
            self.ids.front_door1.background_color = self.theme_cls.error_color

        if self.io.melter_door_sensor_2 == 0:
            self.ids.right_door1.background_color = self.theme_cls.primary_light
        else:
            self.ids.right_door1.background_color = self.theme_cls.error_color

        if self.io.injection_door_sensor == 0:
            self.ids.right_door2.background_color = self.theme_cls.primary_light
        else:
            self.ids.right_door2.background_color = self.theme_cls.error_color

        if self.io.melter_door_sensor_1 == 0:
            self.ids.right_door3.background_color = self.theme_cls.primary_light
        else:
            self.ids.right_door3.background_color = self.theme_cls.error_color

        if self.io.oven_outer_door_sensor == 0:
            self.ids.front_door2.background_color = self.theme_cls.primary_light
        else:
            self.ids.front_door2.background_color = self.theme_cls.error_color

        if self.io.finished_door_sensor == 1 or self.io.tray_door_sensor == 1 or self.io.oven_outer_door_sensor == 1 \
                or self.io.injection_door_sensor == 1 or self.io.melter_door_sensor_1 == 1 or self.io.melter_door_sensor_2 == 1:
            # reset tiemr if door is found not closed
            self.timenow = time.time()
        elif time.time() - self.timenow > 1:
            self.countdown_trigger()

    def manual_close(self, *args):
        self.dismiss()

    def on_dismiss(self):
        self.callback()
        self.check_status.cancel()


class ErrorListDialogContent(ScrollView):
    pass


class ErrorListDialog(MDDialog):
    def __init__(self, error_list, *args, **kwargs):
        self.theme = app.theme_cls
        self.error_list = error_list
        self.title = 'List of Errors'

        self.content_cls = ErrorListDialogContent()
        self.auto_dismiss = False
        Clock.schedule_once(self.add_items, -1)

        super(ErrorListDialog, self).__init__()

    def add_items(self, *args):
        for i in self.error_list:
            self.ids.container.add_widget(
                OneLineListItem(text=f"Code {i}", size_hint_y=None)
            )

    def create_content(self, code):
        box = MDBoxLayout(adaptive_height=True, orientation='vertical')
        message, resolve, recovery = self.get_error(code)

        box.add_widget(MDLabel(text=message))

        return box

    def get_error(self, code):
        message = 'Unknown Error Code'
        resolve = ''
        recovery = []

        # make sure the codes are declared properly
        if code in error_codes:
            if 'message' in error_codes[code]:
                message = error_codes[code]['message']
            if 'resolve' in error_codes[code]:
                resolve = error_codes[code]['resolve']
            if 'recovery' in error_codes[code]:
                recovery = error_codes[code]['recovery']

        return message, resolve, recovery


class MotorConfigDialog(MDDialog):
    def __init__(self, motor,callback, *args, **kwargs):
        self.theme = app.theme_cls
        self.motor = motor
        self.callback = callback
        self.selected_recipe = ''
        self.title = 'Motor Configuration'
        self.type = 'custom'
        self.motor_dir = 1
        self.content_cls = self.create()
        # self.auto_dismiss = False
        self.yes_button = MDRaisedButton(text='Save', on_release=self.yes)
        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        self.yes_button]
        self.check_speed = Clock.schedule_interval(self.update_speed, 0.5)

        super(MotorConfigDialog, self).__init__()

    def create(self, ):
        box = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height="300sp")

        box1 = MDBoxLayout(orientation='horizontal', spacing=8)
        label1 = MDLabel(text='Select Recipe :')
        self.menu = MDDropdownMenu()
        self.recipe_dropdown = MDDropDownItem(on_release=self.open_menu, size_hint_x=None, pos_hint={'center_y': 0.5}, )

        if self.selected_recipe != '':
            self.recipe_dropdown.text = f'{self.selected_recipe}'
        else:
            self.recipe_dropdown.text = 'Please Select'

        titles = [i for i in self.motor]
        menu_items = [
            {
                "text": f"{titles[i]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{titles[i]}": self.menu_callback(x),
            } for i in range(len(titles))
        ]
        self.menu.caller = self.recipe_dropdown
        self.menu.items = menu_items
        self.menu.width_mult = 4
        self.menu.max_height = 250

        motorbox = MDBoxLayout(orientation='horizontal',spacing=8,)
        motorlabel = MDLabel(text= 'Motor Number    :')
        self.motortext = MDTextField(max_text_length=1, text='1', write_tab=False,
                                  hint_text='Please enter motor number (range 1 - 8)')

        distbox = MDBoxLayout(orientation='horizontal',spacing=8,)
        distlabel = MDLabel(text='Enter Distance    :')
        self.disttext = MDTextField(max_text_length=5, text='1000', write_tab=False,
                                hint_text='Please enter steps to go')

        dirbox = MDBoxLayout(orientation='horizontal',spacing =8,)
        dirlabel =MDLabel(text='Direction    :')
        self.dircheckbox = MDCheckbox(active=True)
        self.dircheckbox.bind(on_release=self.direction)

        speedbox = MDBoxLayout(orientation='horizontal',spacing =8,)
        speedbox2 = MDBoxLayout(orientation='vertical',spacing =8)
        self.speedlabel = MDLabel(text='30',pos_hint={'x':0.2})
        speedicon = MDIcon(icon="run-fast",pos_hint={'x':0.2})
        speedbox3 = MDBoxLayout(orientation='vertical',spacing =8)
        self.speedslider = MDSlider(min=10,max=100,value=30,step=5,)
        self.speedslider.bind(on_touch_up=self.change_speed)

        motorbox.add_widget(motorlabel)
        motorbox.add_widget(self.motortext)
        distbox.add_widget(distlabel)
        distbox.add_widget(self.disttext)
        dirbox.add_widget(dirlabel)
        dirbox.add_widget(self.dircheckbox)
        speedbox2.add_widget(speedicon)
        speedbox2.add_widget(self.speedlabel)
        speedbox3.add_widget(self.speedslider)
        speedbox.add_widget(speedbox2)
        speedbox.add_widget(speedbox3)

        box1.add_widget(label1)
        box1.add_widget(self.recipe_dropdown)
        box.add_widget(box1)
        box.add_widget(motorbox)
        box.add_widget(distbox)
        box.add_widget(dirbox)
        box.add_widget(speedbox)

        return box

    def direction(self, *args):
        if self.dircheckbox.active :
            self.motor_dir = 1
        else:
            self.motor_dir = 0

    def change_speed(self,*args):
        self.speed = self.speedslider.value = self.speedlabel.text

    def update_speed(self, *args):
        self.speedlabel.text = str(self.speedslider.value)
        return self.speedlabel.text

    def yes(self, *args):
        if self.motortext.text == '':
            toast("Cant be empty")
            return

        if self.motortext.text.isalnum() is False:
            toast("invalid data type, enter numbers only")
            return

        if self.motortext.text.isalpha() is True:
            toast("invalid data type, enter numbers only")
            return

        if self.disttext.text.isalnum() is False:
            toast("invalid data type, enter numbers only")
            return

        if self.disttext.text.isalpha() is True:
            toast("invalid data type, enter numbers only")
            return

        if self.motortext.text != '':
            selected_motor = self.motortext.text

        if self.disttext.text != '':
            dist = int(self.disttext.text)

        if self.selected_recipe == '':
            return toast("Please select recipe")

        self.callback(self.selected_recipe,selected_motor,dist,self.motor_dir,self.speed)
        print(f'dialog = {self.selected_recipe,selected_motor,dist,self.motor_dir,self.speed}')
        self.dismiss()

    def on_dismiss(self):
        pass

    def open_menu(self, *args):
        self.menu.open()
        self.info = None

    def menu_callback(self, text_item, *args):
        self.recipe_dropdown.text = text_item
        self.selected_recipe = text_item
        self.menu.dismiss()

class EditDistDialog(MDDialog):
    def __init__(self, motor,callback, *args, **kwargs):
        self.theme = app.theme_cls
        self.motor = motor
        self.callback = callback
        self.selected_recipe = ''
        self.title = 'Edit Dist Move'
        self.type = 'custom'
        self.content_cls = self.create()
        # self.auto_dismiss = False
        self.yes_button = MDRaisedButton(text='Save', on_release=self.yes)
        self.buttons = [MDFlatButton(text='Cancel', on_release=self.dismiss, theme_text_color="Custom",
                                     text_color=app.theme_cls.primary_color),
                        self.yes_button]

        super(EditDistDialog, self).__init__()

    def create(self, ):
        box = MDBoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height="200sp")

        box1 = MDBoxLayout(orientation='horizontal', spacing=8)
        label1 = MDLabel(text='Select Recipe :')
        self.menu = MDDropdownMenu()
        self.recipe_dropdown = MDDropDownItem(on_release=self.open_menu, size_hint_x=None, pos_hint={'center_y': 0.5}, )

        if self.selected_recipe != '':
            self.recipe_dropdown.text = f'{self.selected_recipe}'
        else:
            self.recipe_dropdown.text = 'Please Select'

        titles = [i for i in self.motor]
        menu_items = [
            {
                "text": f"{titles[i]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{titles[i]}": self.menu_callback(x),
            } for i in range(len(titles))
        ]
        self.menu.caller = self.recipe_dropdown
        self.menu.items = menu_items
        self.menu.width_mult = 4
        self.menu.max_height = 250

        motorbox12= MDBoxLayout(orientation='horizontal',spacing=8,)
        motorlabel12 = MDLabel(text= 'Motor 1 and 2')
        self.motortext12 = MDTextField(max_text_length=6, text='', write_tab=False,
                                  hint_text='Enter number of steps to go')

        motorbox5 = MDBoxLayout(orientation='horizontal', spacing=8, )
        motorlabel5 = MDLabel(text='Motor 5')
        self.motortext5 = MDTextField(max_text_length=6, text='', write_tab=False,
                                       hint_text='Enter number of steps to go')

        motorbox6 = MDBoxLayout(orientation='horizontal', spacing=8, )
        motorlabel6 = MDLabel(text='Motor 6')
        self.motortext6 = MDTextField(max_text_length=6, text='', write_tab=False,
                                       hint_text='Enter number of steps to go')

        motorbox12.add_widget(motorlabel12)
        motorbox12.add_widget(self.motortext12)
        motorbox5.add_widget(motorlabel5)
        motorbox5.add_widget(self.motortext5)
        motorbox6.add_widget(motorlabel6)
        motorbox6.add_widget(self.motortext6)

        box1.add_widget(label1)
        box1.add_widget(self.recipe_dropdown)
        box.add_widget(box1)

        box.add_widget(motorbox12)
        box.add_widget(motorbox5)
        box.add_widget(motorbox6)

        return box

    def open_menu(self, *args):
        self.menu.open()
        self.info = None

    def menu_callback(self, text_item, *args):
        self.recipe_dropdown.text = text_item
        self.selected_recipe = text_item
        self.menu.dismiss()

    def yes(self, *args):
        if self.selected_recipe == '':
            return toast("Please select recipe")

        if self.motortext12.text == '':
            toast("Motor 1 and 2 cant be empty")
            return

        if self.motortext12.text.isalnum() is False:
            toast("Enter Numbers only")
            return

        if self.motortext12.text != '' and self.motortext12.text.isalnum() is True:
            self.dist12 = self.motortext12.text

        if self.motortext5.text == '':
            toast("Motor 5 cant be empty")
            return

        if self.motortext5.text.isalnum() is False:
            toast("Enter Numbers only")
            return

        if self.motortext5.text != '' and self.motortext5.text.isalnum() is True:
            self.dist5 = self.motortext5.text

        if self.motortext6.text.isalnum() is False:
            toast("Enter Numbers only")
            return

        if self.motortext6.text == '':
            toast("Motor 6 cant be empty")
            return

        if self.motortext6.text != '' and self.motortext6.text.isalnum() is True:
            self.dist6 = self.motortext6.text

        self.callback(self.dist12,self.dist5,self.dist6,self.selected_recipe)
        print(f'dialog = {self.dist12,self.dist5,self.dist6,self.selected_recipe}')
        self.dismiss()

    def on_dismiss(self):
        pass

class RecipeSelection(MDDialog):
    def __init__(self, recipe, update, *args, **kwargs):

        self.title = 'Recipe Selection'
        self.type = 'custom'
        self.selected_recipe = ''
        self.recipe = recipe
        self.update = update
        self.content_cls = self.create()
        self.buttons = [MDRaisedButton(text='Save', on_release=self.yes)]

        super(RecipeSelection, self).__init__()

    def create(self):
        box = MDBoxLayout(orientation='vertical', spacing=12, padding=6, size_hint_y=None, height="180sp")

        box1 = MDBoxLayout(orientation='vertical', spacing=8)
        label1 = MDLabel(text='Please select recipe',markup=True,bold=True)
        self.menu = MDDropdownMenu()
        self.recipe_dropdown = MDDropDownItem(on_release=self.open_menu, size_hint_x=None, pos_hint={'center_y': 0.5}, )

        if self.selected_recipe != '':
            self.recipe_dropdown.text = f'{self.selected_recipe}'
        else:
            self.recipe_dropdown.text = 'Please Select'

        titles = [i for i in self.recipe]
        menu_items = [
            {
                "text": f"{titles[i]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{titles[i]}": self.menu_callback(x),
            } for i in range(len(titles))
        ]
        self.menu.caller = self.recipe_dropdown
        self.menu.items = menu_items
        self.menu.width_mult = 4
        self.menu.max_height = 250

        box1.add_widget(label1)
        box1.add_widget(self.recipe_dropdown)
        box.add_widget(box1)

        return box

    def yes(self, *args):
        if self.selected_recipe == '':
            return toast("Please select recipe")

        # if self.enter_part1.text not in self.partnumbers[self.selected_blade]:
        #     return toast('Selected part does not match with part number')

        self.update(recipe=self.selected_recipe)

        toast("Recipe Selected Saved")
        self.dismiss()

    def open_menu(self, *args):
        self.menu.open()
        self.info = None

    def menu_callback(self, text_item, *args):
        self.recipe_dropdown.text = text_item
        self.selected_recipe = text_item
        self.menu.dismiss()

class DataTableDialog(MDDialog):
    def __init__(self,rdata,cdata, callback,*args, **kwargs):

        self.title = 'Database '
        self.type = 'custom'
        self.size_hint = (None, None)
        self.size = ("1080sp", "480sp")
        self.jobs = ['J09123', 'J0123', 'J01231']
        self.selected_job = ''
        self.row_data = rdata
        self.col_data = cdata
        self.row_list = []
        self.callback= callback
        self.auto_dismiss = False
        self.content_cls = self.create()
        self.add_butt = MDRaisedButton(text='ADD', on_release=self.add_row)
        self.reload_but = MDRaisedButton(text='Reload', on_release=self.load_file)
        self.buttons = [MDRaisedButton(text='Dismiss', on_release=self.yes),
                        self.reload_but]
        Window.bind(on_key_down=self._on_keyboard_down)


        super(DataTableDialog, self).__init__()

    def create(self):
        self.layout = MDBoxLayout(orientation="vertical",size_hint_y=None,height="480sp",padding=6,spacing= 16)
        self.layout2 = MDBoxLayout(orientation="horizontal",size_hint_y=None,height="100sp")
        self.box1 = MDBoxLayout(orientation="vertical")
        self.box2 = MDBoxLayout(orientation ="horizontal", spacing=8)
        self.text_field = MDTextField(mode="round",max_text_length=20, text='', write_tab=False,hint_text='Search',background_color = app.theme_cls.primary_color)
        search_butt = MDRoundFlatIconButton(text="Search",icon="text-search-variant",on_release=self.search_data)
        self.menu = MDDropdownMenu()
        self.recipe_dropdown = MDDropDownItem(on_release=self.open_menu, size_hint_x=None, pos_hint={'center_y': 0.5}, )

        if self.selected_job != '':
            self.recipe_dropdown.text = f'{self.selected_job}'
        else:
            self.recipe_dropdown.text = 'Please Select'
        titles = ["Please Select"] + [i for i in self.jobs]
        menu_items = [
            {
                "text": f"{titles[i]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{titles[i]}": self.menu_callback(x),
            } for i in range(len(titles))
        ]
        self.menu.caller = self.recipe_dropdown
        self.menu.items = menu_items
        self.menu.width_mult = 4
        self.menu.max_height = 250

        self.data_table = MDDataTable(
            size_hint=(0.98, 0.9),
            use_pagination=True,
            sorted_order = 'DSC',
            check=True,
            rows_num= 5,
            column_data=self.col_data,
            row_data=self.row_data,
            sorted_on = "Date",
        )

        self.data_table.bind(on_check_press=self.get_checked_data)
        self.data_table.bind(on_row_press=self.press_row)
        self.box1.add_widget(self.recipe_dropdown)
        self.box2.add_widget(self.text_field)
        self.box2.add_widget(search_butt)
        self.layout2.add_widget(self.box1)
        self.layout2.add_widget(self.box2)
        self.layout.add_widget(self.layout2)
        self.layout.add_widget(self.data_table)

        return self.layout

    def add_row(self, *args):
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_code = '008'
        signal = ["alert",[1, 0, 0, 1],"No Signal"]
        error_msg = "Air supply low"
        ack = "check the incoming air supply"
        new_data = [curr_time, error_code, signal, error_msg, ack]
        self.data_table.add_row((row_data[0][0],row_data[0][1], row_data[0][2], row_data[0][3], row_data[0][4]))

    def yes(self,*args ):
        operationscreen = app.root.ids.operation_screen
        if operationscreen.dialog_opened:
            operationscreen.dialog_opened = False
        self.dismiss()

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 7:  # press 'd'
            self.yes()

    def menu_callback(self, text_item, *args):
        self.recipe_dropdown.text = text_item
        self.selected_job = text_item
        self.menu.dismiss()

    def open_menu(self, *args):
        self.menu.open()

    def load_file(self,*args):
        self.text_field.text = ''
        if self.selected_job == 'J0123':
            self.clear_row()
            for i in range (len(row_data1)):
                # self.data_table.update_row(self.data_table.row_data[i],row_data1[i])
                self.data_table.add_row((row_data1[i][0],row_data1[i][1], row_data1[i][2], row_data1[i][3], row_data1[i][4]))
                self.data_table.row_data = row_data1

        else:
            self.clear_row()
            for i in range(len(row_data)):
                # self.data_table.update_row(self.data_table.row_data[i], row_data[i])
                self.data_table.add_row((row_data[i][0],row_data[i][1], row_data[i][2], row_data[i][3], row_data[i][4]))
                self.data_table.row_data = row_data

    def get_checked_data(self, *args):
        self.checked_data = self.data_table.get_row_checks()
        print(self.checked_data)

    def press_row(self,table,row ,*args):
        row_num = int(row.index / len(table.column_data))
        if row_num not in self.row_list:
            self.row_list.append(row_num)
        # row_data = table.row_data[row_num]
        print(self.row_list)

    def search_data(self,*args):
        self.info = []
        # get the row data index
        for i in range(len(self.data_table.row_data)):
            data = self.text_field.text
            if data not in self.data_table.row_data[i][1]:
                self.info.append(i)
        self.info.sort(reverse=True)
        print(self.info)

        if not self.check_empty_list(self.info):
            self.filter_row_data()

    def check_empty_list(self,list):
        if not list:
            return 1
        else:
            return 0

    # def filter_row_data12(self):
    #     c = len(self.info) - 1
    #     self.data_table.remove_row(self.data_table.row_data[self.info[0]])
    #     for i in range(c):
    #         if self.info[0] == 0:
    #             a = self.info[i + 1] - self.info[0]
    #             b = a - ((i+1)*1)
    #         else:
    #             a = self.info[i + 1] - self.info[i]
    #             b = a + i + 1
    #
    #         print(b)
    #         self.data_table.remove_row(self.data_table.row_data[b])

    def filter_row_data(self):
        c = len(self.info)
        # print(f'number of data to be remove = {c}')
        for i in range(c):
            b = self.info[i]
            # print(b)
            self.data_table.remove_row(self.data_table.row_data[b])

    def clear_row(self):
        for i in range(len(self.data_table.row_data)):
            self.data_table.remove_row(self.data_table.row_data[-1])

class RestockDialog(MDDialog):
    def __init__(self ,socketid,*args, **kwargs):
        self.stocks = ['a','b','c','d','e','f','g','h','i']
        self.title = 'Stock Alert'
        self.type = 'custom'
        self.socketid = socketid
        self.content_cls = self.create()
        # self.buttons = [MDRaisedButton(text='Save', on_release=self.yes)]
        super(RestockDialog, self).__init__()

    def create(self):
        color = get_color_from_hex('#FF2F15')
        color2 = get_color_from_hex('#6CD16F')
        outbox = MDBoxLayout(orientation='horizontal', spacing=12, padding=6, size_hint_y=None, height="180sp")
        boxicon = MDBoxLayout(orientation='horizontal', spacing=8)
        iconbutton = MDIconButton(icon="alert",icon_size="120sp",pos_hint={"center_x": .5, "center_y": .5},theme_icon_color="Custom",icon_color=color)
        box2 = MDBoxLayout(orientation='vertical', spacing=8)
        label1 = MDLabel(text=f'Please top up socket,socket id ={self.socketid}',markup=True)
        self.mdlist = MDList()
        view = MDScrollView(self.mdlist)

        for i in range(len(self.stocks)):
            item = OneLineIconListItem(IconRightWidget(icon='check-circle'),text=f'{self.stocks[i]}')
            # item = OneLineListItem(text=f'{self.stocks[i]}')
            self.mdlist.add_widget(item)

        # self.menu = MDDropdownMenu()
        # self.stock_dropdown = MDDropDownItem(on_release=self.open_menu, size_hint_x=None, pos_hint={'center_y': 0.5}, )
        #
        # titles = [i for i in self.stocks]
        # menu_items = [
        #     {
        #         "text": f"{titles[i]}",
        #         "icon": "check-circle",
        #         "icon_color" : color2,
        #         "viewclass": "IconListItem",
        #         "on_release": lambda x=f"{titles[i]}": self.menu_callback(x),
        #     } for i in range(len(titles))
        # ]
        #
        # # alpha-x-circle
        # self.menu.caller = self.stock_dropdown
        # self.menu.items = menu_items
        # self.menu.width_mult = 4
        # self.menu.max_height = 250

        box2.add_widget(view)
        boxicon.add_widget(iconbutton)
        outbox.add_widget(boxicon)
        outbox.add_widget(box2)

        return outbox

    def open_menu(self, *args):
        self.menu.open()
        self.info = None

    def menu_callback(self, text_item, *args):
        self.stock_dropdown.text = text_item
        self.menu.dismiss()

    def yes(self, *args):
        self.dismiss()

get_app()
