__version__ = "1.0-stable"
__author__ = "Samuel Haidu"
__licence__ = "MIT"

import json
import os
from os.path import abspath, dirname

scriptfolder = dirname(abspath(__file__))
with open(scriptfolder+'/internal/config.json') as config_file:
    config_data = json.load(config_file)
DOWNLOAD_PATH = config_data['download_path']
PLAYLIST_PATH = config_data['playlist_path']
try: os.chdir(DOWNLOAD_PATH)
except: DOWNLOAD_PATH = scriptfolder+"/internal/Download"
try: os.chdir(PLAYLIST_PATH)
except: PLAYLIST_PATH = scriptfolder+"/internal/Playlists"
os.chdir(scriptfolder)

from kivy.graphics import Color, Rectangle
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.logger import Logger
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from buttons import ImgToggleButton
from plscreen import PlaylistScreen
from musicscreen import MusicScreen
from configscreen import ConfigScreen
from playlistpopup import ErrorPopup

class Config(Screen):
    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        self.name='config'
        self.ConfigScreen = ConfigScreen()
        self.add_widget(self.ConfigScreen)

class Music(Screen):
    def __init__(self, **kwargs):
        super(Music, self).__init__(**kwargs)
        self.MusicSreen = MusicScreen()
        self.name='music'
        self.add_widget(self.MusicSreen)

class Playlist(Screen):
    def __init__(self, **kwargs):
        super(Playlist, self).__init__(**kwargs)
        self.name='playlist'
        self.PlaylistScreen = PlaylistScreen()
        self.add_widget(self.PlaylistScreen)

class Main(BoxLayout):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.sm = ScreenManager()
        self.btlayout= BoxLayout(size_hint=(1,None))
        self.btlayout.height = '64dp'
        
        self.config = Config()
        self.sm.add_widget(self.config)
        
        self.music = Music()
        self.sm.add_widget(self.music)
       
        self.pl = Playlist()
        self.pl.PlaylistScreen.call = self.music.MusicSreen._fromplaylist
        self.sm.add_widget(self.pl)
        
        self.bt_goto1 = ImgToggleButton(scriptfolder+'/images/screen_buttons/configsreen_normal.png',
                                        scriptfolder+'/images/screen_buttons/configsreen_press.png',
                                        group='screen')
        self.bt_goto1.bind(on_release=self.bt_goto1_click)
        self.btlayout.add_widget(self.bt_goto1)
        
        self.bt_goto2 = ImgToggleButton(scriptfolder+'/images/screen_buttons/searchscreen_normal.png',
                                        scriptfolder+'/images/screen_buttons/searchscreen_press.png',
                                        group='screen')
        self.bt_goto2.bind(on_release=self.bt_goto2_click)
        self.btlayout.add_widget(self.bt_goto2)
        
        self.bt_goto3 = ImgToggleButton(scriptfolder+'/images/screen_buttons/playlistscreen_normal.png',
                                        scriptfolder+'/images/screen_buttons/playlistscreen_press.png',
                                        group='screen')
        self.bt_goto3.bind(on_release=self.bt_goto3_click)
        self.btlayout.add_widget(self.bt_goto3)

        self.sm.current='music'
        self.bt_goto2.state = 'down'
        self.add_widget(self.sm)
        self.add_widget(self.btlayout)
    
    def bt_goto1_click(self, inst):
        self.sm.current='config'
        
    def bt_goto2_click(self, inst):
        self.sm.current='music'
        
    def bt_goto3_click(self, inst):
        self.sm.current='playlist'
    
    def update_rect(instance, value, a):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
                
class OMAP(App):
    Window.clearcolor = (0.2, 0.2, 0.2, 1)
    main = Main()
    def build(self):
        return self.main

class E(ExceptionHandler):
    def handle_exception(self, inst):
        ErrorPopup(str(inst)).open()
        return ExceptionManager.PASS
        
ExceptionManager.add_handler(E())
if __name__ == '__main__':
    app = OMAP()
    app.run()
