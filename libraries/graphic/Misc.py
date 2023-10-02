from kivy.properties import (NumericProperty, StringProperty, ReferenceListProperty, ObjectProperty, ListProperty, BoundedNumericProperty)
from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton, MDRaisedButton, MDFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from kivy.uix.image import Image
from kivymd.uix.slider import MDSlider
from kivy.graphics.texture import Texture
from kivymd.uix.list import OneLineIconListItem
from kivymd.toast import toast
from kivymd.uix.behaviors import (
    CircularRippleBehavior,
    FakeCircularElevationBehavior,
CommonElevationBehavior
)
from kivy.graphics import Rectangle, Color, Line, RoundedRectangle
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivy.app import App

import cv2

# def get_app():
#    global app
#    app = App.get_running_app()

class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")


class IOCard(MDCard, CommonElevationBehavior):
    def __init__(self, **kwargs):
        self.focus_behavior = True
        super().__init__(**kwargs)

class MyTab(MDTabs):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        touch.x = touch.x - self.x
        touch.y = touch.y - self.y
        self.parent.parent.ids.paint.on_touch_move(touch)

class AppTab(MDBoxLayout, MDTabsBase):
    # pass
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

class MyTextField(MDTextField):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        theme = self.app.theme_cls

        self.disabled_foreground_color = theme.disabled_hint_text_color
        self.text_color_normal = theme.text_color


    def dis(self,item):
        print('disabled', item.focus)

class MyToggleButton(MDRoundFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
        self.background_normal = [0,0,0,0]
        super().__init__(**kwargs)
        self.background_down = self.theme_cls.primary_light

class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.fps = 10

    def update(self,frame,*args):
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture
    def cancel(self):
        self.display.cancel()

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class IlluSlider(MDSlider):
    def __init__(self, **kwargs):
        self.call_func = lambda : None
        super(IlluSlider, self).__init__(**kwargs)

    def on_touch_up(self,touch):
        super().on_touch_up(touch)
        if touch.grab_current == self:
            self.value_pos = touch.pos
            #do illu here
            self.call_func()

class DrawInput(Widget):
    pencolor = ListProperty([1,1,0,1])
    xboun = 0
    yboun = 0
    def on_touch_down(self, touch):
        if self.x<touch.x<(self.x + self.width) and self.y< touch.y<(self.y + self.height):
            with self.canvas:
                Color(rgba=self.pencolor)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=1)
                # if sline:
                self.xs = touch.x
                self.ys = touch.y

    def on_touch_move(self,touch):
        if self.x<touch.x<(self.x + self.width) and self.y< touch.y<(self.y + self.height):
            try:
                with self.canvas.after:
                    self.canvas.after.clear()
                    Color(rgba=self.pencolor)
                    Line(rectangle=(self.xs, self.ys, touch.x - self.xs, touch.y - self.ys), width=1)
                self.xboun = touch.x
                self.yboun = touch.y
                return self.xs, self.ys, self.xboun, self.yboun
            except Exception as e:
                print(e)


    def on_touch_up(self, touch):
        #only fire inbound
        if self.x<touch.x<(self.x + self.width) and self.y< touch.y<(self.y + self.height):
            # if self.xboun != touch.x or self.yboun != touch.y:
            #     self.canvas.after.clear()
            #     toast("Invalid Drawing, please retry")
            #     return
            try:
                with self.canvas.after:
                    # print("RELEASED!", touch)
                    Color(rgba=self.pencolor)
                    Line(rectangle=(self.xs, self.ys, touch.x - self.xs, touch.y - self.ys), width=1)

                    self.confirm_color = self.pencolor
                    self.confirm_rect = (self.xs, self.ys, touch.x - self.xs, touch.y - self.ys)
                # print(self.x, self.y,self.heig
                # ht, self.width)
                pop = SaveBoxDialog(self.xs-self.x, self.ys-self.y, self.xboun-self.x, self.yboun-self.y, self.height, self.width)
                pop.open()
            except FileNotFoundError:
                toast("Master class file missing")
            except Exception as e:
                print(e)

    def confirm_box(self):
        with self.canvas:
            # print("RELEASED!", touch)
            Color(rgba=self.confirm_color)
            Line(rectangle=(self.confirm_rect), width=3)

class SaveBoxDialog(MDDialog):
    def __init__(self, x0, y0, x1, y1, height, width):
        super().__init__()
        temp = App.get_running_app()
        self.OS = temp.root.ids.tuning_screen
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.img_width = width
        self.img_height = height
        self.title = 'Enter Name'
        self.type = 'custom'

        self.content_cls = self.create()
        self.buttons = [MDFlatButton(text='Cancel', on_release=self.Abort, theme_text_color="Custom",
                                     text_color=temp.theme_cls.primary_color),
                        MDRaisedButton(text='Save', on_release=self.save)]
        super(SaveBoxDialog, self).__init__()


    def create(self):
        layout = MDBoxLayout(orientation='vertical',size_hint_y=None,height=100)

        layout.add_widget(MDLabel(text="Enter Box Name",size_hint_x=0.5))
        self.name = MDTextField()
        layout.add_widget(self.name)
        return layout

    def save(self,*args):
        if self.x1>self.x0 and self.y0>self.y1:
            xmin = self.x0
            xmax = self.x1
            ymin = self.y1
            ymax = self.y0
        elif self.x1 > self.x0 and self.y0 < self.y1:
            xmin = self.x0
            xmax = self.x1
            ymin = self.y0
            ymax = self.y1
        elif self.x1 < self.x0 and self.y0 > self.y1:
            xmin = self.x1
            xmax = self.x0
            ymin = self.y1
            ymax = self.y0
        elif self.x1 < self.x0 and self.y0 < self.y1:
            xmin = self.x1
            xmax = self.x0
            ymin = self.y0
            ymax = self.y1

        if self.name.text == '':
            toast("Please Enter a Name")
            return

        print(self.img_width,self.img_height)
        print(xmin,xmax,ymin,ymax)

        actual_width = 1280
        actual_height = 720

        x0 = (xmin / self.img_width) * actual_width
        x1 = (xmax / self.img_width) * actual_width
        y1 = actual_height - ((ymin / self.img_height) * actual_height)
        y0 = actual_height - ((ymax / self.img_height) * actual_height)

        self.OS.add_box(x0,y0,x1,y1,self.name.text)
        self.dismiss()

    def on_dismiss(self):
        self.OS.ids.paint.canvas.after.clear()

    def Abort(self,*args):
        self.dismiss()

# get_app()