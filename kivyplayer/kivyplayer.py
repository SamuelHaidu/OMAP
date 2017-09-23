import time
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.app import App
from custombutton import PlayButton, NextButton, PrevButton, RepeatButton, SoundButton
from android_backend import MPlayer
#from vlc_backend import MPlayer
#from kivy_backend import MPlayer

class SliderHack(Factory.Slider):
    '''This class create a slider with a touch events '''
    touch_transform = Factory.NumericProperty()
    callback_down = None
    callback_move = None
    callback_up = None
    
    def on_touch_down(self, touch):
        if super(SliderHack, self).on_touch_down(touch):
            self.touch_transform = self.value
            if (self.callback_down):self.callback_down()
    def on_touch_move(self, touch):
        if super(SliderHack, self).on_touch_move(touch):
            self.touch_transform = self.value
            if (self.callback_move):self.callback_move()
    def on_touch_up(self, touch):
        if super(SliderHack, self).on_touch_up(touch):
            self.touch_transform = self.value
            if (self.callback_up): self.callback_up()
            
class Player(BoxLayout):
    ''' This class populate and create a widget'''
    def __init__(self,
                 next_callback,
                 back_callback,
                 **kwargs):
        super(Player, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.titlelayout = BoxLayout(orientation='horizontal')
        self.titlelayout.size_hint_y = None
        self.titlelayout.height = 16
        
        self.uplayout = BoxLayout(orientation='horizontal')
        self.uplayout.size_hint_y = None
        self.uplayout.height = 16
        
        self.downlayout = BoxLayout(orientation='horizontal')
        self.downlayout.size_hint_y = 0.5
        
        self.next_callback = next_callback
        self.back_callback = back_callback
        
        self.media = None
        self.pausetime = 0
        self.pausestate = False
        
        self.timer = Clock
        self.timer.schedule_interval(self._progresstimer, 0.1) # Update the slider and labels
        
        self.add_widget(self.titlelayout)
        self.add_widget(self.uplayout)
        self.add_widget(self.downlayout)
        
        self.label_title = Label(text='No Music')
        self.titlelayout.add_widget(self.label_title)
        
        # Slider and labels
        self.label_time = Label(text='00:00')
        self.label_time.size_hint = (0.15, 1)
        self.uplayout.add_widget(self.label_time)
        
        self.slid_timemusic = SliderHack()
        self.slid_timemusic.orientation = 'horizontal'
        self.slid_timemusic.callback_up = self._sliderup
        self.slid_timemusic.value_track = True
        self.slid_timemusic.value_track_color = [0, 0.7, 2, 1]
        self.slid_timemusic.cursor_size = (16, 16)
        self.slid_timemusic.min = 0
        self.uplayout.add_widget(self.slid_timemusic)
        
        self.label_length = Label(text='00:00')
        self.label_length.size_hint= (0.15, 1)
        self.uplayout.add_widget(self.label_length)
        
        # Buttons
        self.bt_sound = SoundButton(state='down')
        self.downlayout.add_widget(self.bt_sound)
        
        self.bt_back = PrevButton()
        self.bt_back.bind(on_press=self._bt_back_click)
        self.downlayout.add_widget(self.bt_back)
        
        self.bt_play = PlayButton()
        self.bt_play.bind(on_press=self._bt_play_click)
        self.downlayout.add_widget(self.bt_play)
        
        self.bt_next = NextButton()
        self.bt_next.bind(on_press=self._bt_next_click)
        self.downlayout.add_widget(self.bt_next)
        
        self.bt_repeat = RepeatButton()
        self.downlayout.add_widget(self.bt_repeat)
        
    def _bt_play_click(self, instance): # Play button callback
        if self.media == None: return
        if self.media.state == 'play': self.pause(); instance.set_play()
        elif self.media.state == 'stop' and self.pausestate == True: 
            self.play() 
            instance.set_pause()
        else: 
            self.media.play() 
            instance.set_pause()
            
        
    def _bt_back_click(self, instance):# Previus button internal callback
        self.slid_timemusic.value = 0
        self.label_time.text = "00:00"
        self.back_callback()

    def _bt_next_click(self, instance): # Next button internal callback
        self.slid_timemusic.value = 0
        self.label_time.text = "00:00"
        self.next_callback() 
    
    def _bt_stop_click(self, instance): # Stop button callback
        self.slid_timemusic.value = 0
        self.label_time.text = "00:00"
        self.stop()
            
    def load(self, audio, title=''): 
        self.media = MPlayer()
        self.media.load(audio)
        self.label_title.text = title
        self.slid_timemusic.max = self.media.length
        self.label_length.text = "%02d:%02d" % divmod(self.media.length,60)
        
    
    def play(self):
        '''Play the music in the current state'''
        if self.media == None: return
        if self.media.state == 'play': return
        elif self.media.state == 'stop' and self.pausestate == True:
            self.media.play()
            self.bt_play.text = 'Pause'
        else: self.media.play(); self.bt_play.set_pause()
    
    def stop(self):
        '''Stop the loaded music but not unload'''
        if self.media == None: return
        if self.media.state == 'play': 
            self.media.stop() 
            self.bt_play.text = 'Play'
            self.pausestate = False
        else: return
    
    def pause(self):
        '''Pause the music '''
        if self.media == None: return
        if self.media.state == 'play':
            self.media.pause()
            self.pausestate = True
            

    def _progresstimer(self,dt):
        '''Update the slider when music is playing'''
        if self.media == None:return
        if self.bt_sound.state == 'normal':
            self.media.set_mute()
        else:
            self.media.set_unmute()
        
        if self.media.state == 'play': 
            self.slid_timemusic.value = self.media.get_pos()
            self.label_time.text = "%02d:%02d" % divmod(self.slid_timemusic.value, 60)
        
        if self.label_time.text == self.label_length.text and self.bt_repeat.state == 'normal':
            self._bt_next_click(self.bt_next)
        elif self.label_time.text == self.label_length.text and self.bt_repeat.state == 'down':
            self.media.stop()
            self.media.play()
    
    def _sliderup(self):
        if self.media == None: return
        if self.media.state == 'play':
            self.media.seek(self.slid_timemusic.value)
        

class testapp(App):
    title = 'Testes'
    
    def build(self):
        p = Player(self.next,self.prev)
        p.load('alok-fuego.mp3', title='Alok - Fuego')
        
        return p
    def next(self):pass
    def prev(self):pass  

if __name__ == '__main__':
    testapp().run()