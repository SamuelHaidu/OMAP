import pyms
import pafy
from musicscreen_widgets import SearchBox, VideoWidget, PlaylistWidget
from downloader import Downloader
from kivyplayer import Player
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
ext = ''       
class MusicScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MusicScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.txtbx_search = SearchBox()
        self.txtbx_search.size_hint = (1, None)
        self.txtbx_search.size = (Window.width,dp(46))
        self.txtbx_search.music_callback = self.load_music
        self.txtbx_search.artist_callback = self.load_artist
        self.txtbx_search.playlist_callback = self.load_playlists
        self.add_widget(self.txtbx_search)
        
        self.videogrid = GridLayout(cols=1, spacing=1, size_hint=(1,None)) 
        self.videogrid.bind(minimum_height=self.videogrid.setter('height'))
        
        self.scroll = ScrollView()

        self.scroll.size_hint= (1, 1)
        self.scroll.add_widget(self.videogrid)
        self.add_widget(self.scroll)
        
        self.pl = Player(self.nextmusic, self.previusmusic)
        self.pl.size_hint = (1, None)
        self.pl.size = (Window.width,dp(130))
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
        self.dlPopup.open()
        self.dlPopup.title = 'Downloading...'
        self.label_downloadtitle.text = 'Title: ' + title
        self.dlPopup.content = self.content
        Downloader(url, tp, callback=self._downloadCall).start()
    
    def _downloadCall(self, total, recvd, ratio, rate, eta):
        self.progress_download.value = ratio*100
        self.label_downloadinfo.text = ' Rate - %.2f KB/s Reaming ' % rate + str(int(eta)) + 's'
        if self.progress_download.value == 100: self.dlPopup.dismiss()
    
    def _fromplaylist(self, videos):
        self.videos = videos
        self.videogrid.clear_widgets(children=None)
        for i in range(len(self.videos)):
            self.video = VideoWidget(i,
                                     self.videos[i]['title'],
                                     self.videos[i]['link'],
                                     '--:--',
                                     play_callback=self.play,
                                     download_callback=self._download_click)
            self.videogrid.add_widget(self.video)
        
        
    def load_music(self, videos):
        self.videos = videos
        self.videogrid.clear_widgets(children=None)
        for i in range(len(self.videos)):
            self.video = VideoWidget(i,
                                     self.videos[i]['title'],
                                     self.videos[i]['link'],
                                     self.videos[i]['duration'],
                                     play_callback=self.play,
                                     download_callback=self._download_click)
            self.videogrid.add_widget(self.video)

    def load_playlists(self, playlists):
        self.videogrid.clear_widgets(children=None)
        for i in range(len(playlists)):
            self.plist = PlaylistWidget(i,
                                     playlists[i]['title'], 
                                     playlists[i]['link'], 
                                     playlists[i]['numtracks'])
            self.videogrid.add_widget(self.plist)
            
    def load_artist(self, videos):
        self.videos = videos
        self.videogrid.clear_widgets(children=None)
        for i in range(len(self.videos)):
            self.video = VideoWidget(i,
                                     self.videos[i]['title'],
                                     self.videos[i]['link'],
                                     '--:--',
                                     play_callback=self.play,
                                     download_callback=self._download_click)
            self.videogrid.add_widget(self.video)
        
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
        