import pyms
import pafy
from playlistpopup import addTrackPopup
from downloader import Downloader
from kivyplayer import Player
from os import getcwd
from os.path import abspath, dirname
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown

ext = ''
scriptfolder = dirname(abspath(__file__))

class VideoWidget(ButtonBehavior, BoxLayout):
    def __init__(self,
                 idx=0, 
                 videotitle='Title of Video', 
                 videourl='http://url',
                 duration='00:00',
                 play_callback=None,
                 download_callback=None,
                 **kwargs):
                 
        super(VideoWidget, self).__init__(**kwargs)
        self.height = dp(46)
        self.orientation = 'horizontal'
        self.size_hint = 1, None
        self.size = (Window.width,self.height)
        self.spacing = 3
        
        self.titlelayout = BoxLayout(orientation='vertical')
        
        with self.canvas.before:
            Color(1,1,1,0.0)
            self.rect = Rectangle(size=self.size, pos=self.pos)

            
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.idx = idx
        self.title = videotitle
        self.url = videourl
        self.duration = duration
        self.play_callback = play_callback
        self.download_callback = download_callback
        
        self.label_idx = Label(text=str(self.idx), size_hint=(None,None), size=(dp(46),dp(46)))
        self.add_widget(self.label_idx)
        
        
        self.label_title = Label(text=self.title,size_hint=(1, 1))
        self.label_title.halign = 'left'
        self.label_title.valign = 'center'
        self.label_title.bind(size=self.label_title.setter('text_size'))
        self.label_title.shorten = True
        self.label_title.shorten_from = 'right'
        self.titlelayout.add_widget(self.label_title)
        
        self.label_duration = Label(text=self.duration,size_hint=(None, 1))
        self.label_duration.width = dp(41)
        self.titlelayout.add_widget(self.label_duration)
        
        self.add_widget(self.titlelayout)
        
        self.drop_op = DropDown(auto_width=False)
        
        self.bt_donwload_m4a = Button(text='', size_hint=(1,None), size=(dp(50),dp(32)))
        self.bt_donwload_m4a.background_normal = scriptfolder + '/images/dl_m4a.png'
        self.bt_donwload_m4a.border=(0, 0, 0, 0)
        self.bt_donwload_m4a.bind(on_release=self.bt_download_m4a)
        self.drop_op.add_widget(self.bt_donwload_m4a)
        
        self.bt_donwload_ogg = Button(text='', size_hint=(1,None), size=(dp(50),dp(32)))
        self.bt_donwload_ogg.background_normal = scriptfolder + '/images/dl_ogg.png'
        self.bt_donwload_ogg.border=(0, 0, 0, 0)
        self.bt_donwload_ogg.bind(on_release=self.bt_download_ogg)
        self.drop_op.add_widget(self.bt_donwload_ogg)

        self.bt_donwload_mp3 = Button(text='', size_hint=(1,None), size=(50,dp(32)))
        self.bt_donwload_mp3.background_normal = scriptfolder + '/images/dl_mp3.png'
        self.bt_donwload_mp3.border=(0, 0, 0, 0)
        self.bt_donwload_mp3.bind(on_release=self.bt_download_mp3_click)
        self.drop_op.add_widget(self.bt_donwload_mp3)
        
        self.bt_addtoplaylist = Button(text='', size_hint=(1,None), size=(50,dp(32)))
        self.bt_addtoplaylist.border=(0, 0, 0, 0)
        self.bt_addtoplaylist.background_normal = scriptfolder + '/images/bt_addto.png'
        self.bt_addtoplaylist.bind(on_release=self.bt_addtoplaylist_click)
        self.drop_op.add_widget(self.bt_addtoplaylist)
        
        self.bt_op = Button(text='', size_hint=(None,1),width=dp(32))
        self.bt_op.background_normal = scriptfolder + '/images/bt_op.png'
        self.bt_op.border=(0, 0, 0, 0)
        self.bt_op.bind(on_release=self.drop_op.open)
        self.add_widget(self.bt_op)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        with self.canvas.after:
            self.line = Line(points=[0, self.pos[1],self.size[0],self.pos[1]], color=Color(.55,.55,.55,1))
            
    def on_press(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 0.8, mode='rgba')
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
    def on_release(self):
        self.canvas.before.clear()
        if self.play_callback: self.play_callback(self.title, self.url, self.idx)
        with self.canvas.before:
            Color(1, 1, 1, 0.0, mode='rgba')
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        
            
    def bt_download_m4a(self, instance):
         if self.download_callback: self.download_callback(self.title, self.url, 'm4a')
    
    def bt_download_ogg(self, instance):
         if self.download_callback: self.download_callback(self.title, self.url, 'ogg')
    
    def bt_download_mp3_click(self, instance):
         if self.download_callback: self.download_callback(self.title, self.url, 'mp3')
    
    def bt_addtoplaylist_click(self, instance):
         addTrackPopup(self).open()

class MusicScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MusicScreen, self).__init__(**kwargs)
        
        self.orientation = 'vertical'
        
        self.txtbx_search = TextInput(text='Search Music Here',multiline=False)
        self.txtbx_search.size_hint = (1, None)
        self.txtbx_search.size = (Window.width,dp(32))
        self.txtbx_search.bind(on_text_validate=self._txtbx_search_enter, focus=self.on_focus)
        self.add_widget(self.txtbx_search)
        
        self.videogrid = GridLayout(cols=1, spacing=1, size_hint=(1,None)) 
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
    def _download_click(self, title, url, tp):
        self.path = getcwd() + '/'
        self.dlPopup.open()
        self.dlPopup.title = 'Downloaded'
        self.label_downloadtitle.text = 'Title: ' + title
        self.dlPopup.content = self.content
        Downloader(url, tp=tp, callback=self._downloadCall).start()
    
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
                                     duration='',
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
                                     duration=self.videos[i]['duration'],
                                     play_callback=self.play,
                                     download_callback=self._download_click)
            self.videogrid.add_widget(self.video)
    
    def on_focus(self,instance, value):
        if instance.text == 'Search Music Here': instance.text = ''
        elif instance.text == '': instance.text = 'Search Music Here'
 
    def play(self, title, url, idx):
        if self.videos == None: return
        self.videomedia = pafy.new(url)
        self.mediaurl = self.videomedia.getbestaudio(preftype='m4a').url
        self.plidx = idx
        self.pl.stop()
        self.pl.load(self.mediaurl + ext, self.videos[self.plidx]['title'])
        self.pl.play()
        print 'playing now music', self.plidx, self.videos[self.plidx]['title']
    
    def nextmusic(self):
        if self.videos == None: return
        self.plidx += 1
        self.videomedia = pafy.new(self.videos[self.plidx]['link'])
        self.mediaurl = self.videomedia.getbestaudio(preftype='m4a').url
        self.pl.stop()
        self.pl.load(self.mediaurl + ext, self.videos[self.plidx]['title'])
        self.pl.play()
        print 'playing now music', self.plidx, self.videos[self.plidx]['title']
        
    def previusmusic(self):
        if self.videos == None: return
        self.plidx -= 1
        self.videomedia = pafy.new(self.videos[self.plidx]['link'])
        self.mediaurl = self.videomedia.getbestaudio(preftype='m4a').url
        self.pl.stop()
        self.pl.load(self.mediaurl + ext, self.videos[self.plidx]['title'])
        self.pl.play()
        print 'playing now music', self.plidx, self.videos[self.plidx]['title']
 