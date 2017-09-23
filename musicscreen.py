import pyms
import pafy
import os
from os.path import abspath, dirname
from downloader import Downloader
from os import getcwd
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.metrics import dp , mm
from kivyplayer import Player

scriptfolder = dirname(abspath(__file__))

class VideoWidget(BoxLayout):
    def __init__(self,
                 idx, 
                 videotitle='Title of Video', 
                 videourl='http://url',
                 play_callback=None,
                 download_callback=None,
                 **kwargs):
                 
        super(VideoWidget, self).__init__(**kwargs)
        self.height = dp(32)
        self.orientation = 'horizontal'
        self.size_hint = 1, None
        self.size = (Window.width,self.height)
        self.spacing = 3
        
        self.idx = idx
        self.title = videotitle
        self.url = videourl
        if play_callback == None: self.play_callback = self._p
        else: self.play_callback =  play_callback
        if download_callback == None: self.download_callback = self._d
        else: self.download_callback =  download_callback
        
        # Create the Title Label
        self.label_title = Label(text=self.title)
        self.label_title.halign = 'left'
        self.label_title.size_hint_y = 1
        self.label_title.bind(size=self.label_title.setter('text_size'))
        self.label_title.shorten = True
        self.label_title.shorten_from = 'right'
        self.add_widget(self.label_title)
        
        # Create the dowload button
        self.bt_download = Button()
        self.bt_download.size_hint = (None, 1)
        self.bt_download.width = self.height
        self.bt_download.bind(on_press=self._bt_download_click)
        self.bt_download.border=(0, 0, 0, 0)
        self.bt_download.background_normal = scriptfolder + '/images/bt_dl_normal.png'
        self.bt_download.background_down = scriptfolder + '/images/bt_dl_press.png'
        self.bt_download.allow_stretch = True
        self.add_widget(self.bt_download)
        # Create the play button
        self.bt_play = Button()
        self.bt_play.size_hint = (None, 1)
        self.bt_play.width = self.height
        self.bt_play.bind(on_press=self._bt_play_click)
        self.bt_play.border=(0, 0, 0, 0)
        self.bt_play.background_normal = scriptfolder + '/images/play_normal.png'
        self.bt_play.background_down = scriptfolder + '/images/play_press.png'
        self.add_widget(self.bt_play)
    
    def _bt_play_click(self, instance):
        self.play_callback(self.title, self.url, self.idx)
        
    def _bt_download_click(self, instance): 
        self.download_callback(self.title ,self.url)
        
    def _p(self, title, url, idx): pass
    def _d(self, url): pass

class MusicScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MusicScreen, self).__init__(**kwargs)
        
        self.orientation = 'vertical'
        
        self.txtbx_search = TextInput(text='Search Music Here',multiline=False)
        self.txtbx_search.size_hint = (1, None)
        self.txtbx_search.size = (Window.width,dp(30))
        self.txtbx_search.bind(on_text_validate=self._txtbx_search_enter, focus=self.on_focus)
        self.add_widget(self.txtbx_search)
        
        self.videogrid = GridLayout(cols=1, spacing=5, size_hint=(1,None)) 
        self.videogrid.bind(minimum_height=self.videogrid.setter('height'))
        
        self.scroll = ScrollView()
        self.scroll.size_hint= (1, 1)
        self.scroll.add_widget(self.videogrid)
        self.add_widget(self.scroll)
        
        self.pl = Player(self.nextmusic, self.previusmusic)
        self.pl.size_hint = (1, None)
        self.pl.size = (Window.width,dp(100))
        self.add_widget(self.pl)
        self.plidx = 0
        
        self.dlPopup = Popup(size_hint=(0.9, 0.3), auto_dismiss=False)
        self.content = BoxLayout(orientation='vertical')
        self.label_downloadtitle = Label(text='Title: ')
        self.label_downloadtitle.halign = 'center'
        self.label_downloadtitle.bind(size=self.label_downloadtitle.setter('text_size'))
        self.label_downloadinfo = Label(text='Reaming Rate')     
        self.progress_download = ProgressBar(min=0, max=100)
        self.content.add_widget(self.label_downloadtitle)
        self.content.add_widget(self.label_downloadinfo)
        self.content.add_widget(self.progress_download)
        
        self.videos = None
        
    def _download_click(self, title, url):
        self.dlPopup.open()
        self.dlPopup.title = 'Downloaded'
        self.label_downloadtitle.text = 'Title: ' + title
        self.dlPopup.content = self.content
        Downloader(url, callback=self._downloadCall).start()
    
    def _downloadCall(self, total, recvd, ratio, rate, eta):
        self.progress_download.value = ratio*100
        self.label_downloadinfo.text = ' Rate - %.2f KB/s Reaming ' % rate + str(int(eta)) + 's'
        if self.progress_download.value == 100: self.dlPopup.dismiss()
    
    def _fromplaylist(self, videos):
        self.videos = videos
        self.videogrid.clear_widgets(children=None)
        for i in range(len(self.videos)):
            self.video = VideoWidget(i,
                                     ' '+self.videos[i]['title'],
                                     self.videos[i]['link'],
                                     play_callback=self.play,
                                     download_callback=self._download_click)
            self.videogrid.add_widget(self.video)
    
    def _txtbx_search_enter(self,instance):
        self.query = instance.text.split()
        if self.query[0] == 'a:':
            self.videos = pyms.ytsArtist(" ".join(self.query[0:]))
        else:
            self.videos = pyms.yts(" ".join(self.query))
        self.videogrid.clear_widgets(children=None)
        for i in range(len(self.videos)):
            self.video = VideoWidget(i,
                                     ' '+self.videos[i]['title'],
                                     self.videos[i]['link'],
                                     play_callback=self.play,
                                     download_callback=self._download_click)
            self.videogrid.add_widget(self.video)
    
    def on_focus(self,instance, value):
        if value: instance.text = ''
        else: instance.text = 'Search Music Here'
 
    def play(self, title, url, idx):
        if self.videos == None: return
        self.videomedia = pafy.new(url)
        self.mediaurl = self.videomedia.getbestaudio(preftype='m4a').url
        self.plidx = idx
        self.pl.stop()
        self.pl.load(self.mediaurl, self.videos[self.plidx]['title'])
        self.pl.play()
        
    
    def nextmusic(self):
        if self.videos == None: return
        self.plidx += 1
        self.videomedia = pafy.new(self.videos[self.plidx]['link'])
        self.mediaurl = self.videomedia.getbestaudio(preftype='m4a').url
        self.pl.stop()
        self.pl.load(self.mediaurl, self.videos[self.plidx]['title'])
        self.pl.play()
        
        
    def previusmusic(self):
        if self.videos == None: return
        self.plidx -= 1
        self.videomedia = pafy.new(self.videos[self.plidx]['link'])
        self.mediaurl = self.videomedia.getbestaudio(preftype='m4a').url
        self.pl.stop()
        self.pl.load(self.mediaurl, self.videos[self.plidx]['title'])
        self.pl.play()
        
 