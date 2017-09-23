from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.image import Image
from kivy.app import App
from os.path import abspath, dirname
scriptfolder = dirname(abspath(__file__))
class PlayButton(ButtonBehavior, Image):
    normal = scriptfolder + '/images/play_normal.png'
    press = scriptfolder + '/images/play_press.png'
    def __init__(self, **kwargs):
        super(PlayButton, self).__init__(**kwargs)
        self.source = self.normal
        self.allow_stretch = True
    def on_press(self):
        self.source = self.press

    def on_release(self):
        self.source = self.normal
    
    def set_pause(self):
        self.normal = scriptfolder + '/images/pause_normal.png'
        self.press = scriptfolder + '/images/pause_press.png'
        self.source = self.normal
        
    def set_play(self):
        self.normal = scriptfolder + '/images/play_normal.png'
        self.press = scriptfolder + '/images/play_press.png'
        self.source = self.normal

class NextButton(ButtonBehavior, Image):
    normal = scriptfolder + '/images/next_normal.png'
    press = scriptfolder + '/images/next_press.png'
    def __init__(self, **kwargs):
        super(NextButton, self).__init__(**kwargs)
        self.source = self.normal
        self.allow_stretch = True
    
    def on_press(self):
        self.source = self.press

    def on_release(self):
        self.source = self.normal

class PrevButton(ButtonBehavior, Image):
    normal = scriptfolder + '/images/prev_normal.png'
    press = scriptfolder  + '/images/prev_press.png'
    def __init__(self, **kwargs):
        super(PrevButton, self).__init__(**kwargs)
        self.source = self.normal
        self.allow_stretch = True
    
    def on_press(self):
        self.source = self.press
    
    def on_release(self):
        self.source = self.normal

class RepeatButton(ToggleButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(RepeatButton, self).__init__(**kwargs)
        self.source = scriptfolder  + '/images/loop_normal.png'

    def on_state(self, widget, value):
        if value == 'down':
            self.source = scriptfolder  + '/images/loop_down.png'
        else:
            self.source = scriptfolder  + '/images/loop_normal.png'

class SoundButton(ToggleButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(SoundButton, self).__init__(**kwargs)
        self.source = scriptfolder  + '/images/sound_normal.png'

    def on_state(self, widget, value):
        if value == 'down':
            self.source = scriptfolder  + '/images/sound_normal.png'
        else:
            self.source = scriptfolder  + '/images/sound_mute.png'


        
 
