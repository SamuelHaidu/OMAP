from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors import ButtonBehavior

class ImgToggleButton(ToggleButtonBehavior, Image):
    def __init__(self, img_normal, img_down,**kwargs):
        super(ImgToggleButton, self).__init__(**kwargs)
        self.source = img_normal
        self.mipmap = True
        self.img_normal = img_normal
        self.img_down = img_down

    def on_state(self, widget, value):
        if value == 'down':
            self.source = self.img_down
        else:
            self.source = self.img_normal

class ImgButton(ButtonBehavior, Image):
    def __init__(self, img_normal, img_press, **kwargs):
        super(ImgButton, self).__init__(**kwargs)
        self.normal = img_normal
        self.press = img_press
        self.source = self.normal
        self.allow_stretch = True
        self.mipmap = False
    
    def on_press(self):
        self.source = self.press

    def on_release(self):
        self.source = self.normal