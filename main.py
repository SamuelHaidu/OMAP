__version__ = "0.2.0"
__author__ = "Samuel Haidu"
__license__ = "MIT"

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.pagelayout import PageLayout
from plscreen import PlaylistScreen
from musicscreen import MusicScreen
from kivy.metrics import dp
import os
sdcard = '/mnt/sdcard/'

class Main(PageLayout):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.MusicSreen = MusicScreen()
        self.PlaylistScreen = PlaylistScreen()
        self.PlaylistScreen.call = self.MusicSreen._fromplaylist
        self.add_widget(self.MusicSreen)
        self.add_widget(self.PlaylistScreen)
    
class OMAP(App):
    main = Main()
    title = 'OMAP - Open Music App'
    def build(self):
        Window.clearcolor = (0.2, 0.2, 0.2, 1)
        os.chdir(sdcard)
        try:
            os.makedirs('OMAP/Playlists')
        except:
            pass
        try:
            os.makedirs('OMAP/Download')
        except:
            pass
        
        return self.main
    
    def on_pause(self):
        return True

if __name__ == '__main__':
    app = OMAP()
    app.run()
