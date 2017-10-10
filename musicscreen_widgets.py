import pyms
import pafy
import __main__
from playlistpopup import addTrackPopup, AddPlaylistFromYTPopup
from buttons import ImgButton
from os.path import abspath, dirname
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown

scriptfolder = dirname(abspath(__file__))

NOTEICON_PATH = scriptfolder+'/images/searchbox_buttons/note_icon.png'
ARTISTICON_PATH = scriptfolder+'/images/searchbox_buttons/artist_icon.png'
PLAYLIST_ICON_PATH = scriptfolder+'/images/searchbox_buttons/playlist_icon.png'

BUTTONDLMP3_PATH = scriptfolder+'/images/dl_mp3.png'
BUTTONDLM4A_PATH = scriptfolder+'/images/dl_m4a.png'
BUTTONDLOGG_PATH = scriptfolder+'/images/dl_ogg.png'
BUTTONADD_PATH = scriptfolder+'/images/bt_addto.png'

BUTTON_SAVEPLAYLIST = scriptfolder+'/images/bt_savepl.png'

BUTTON_OPARTIST_PATH = scriptfolder+'/images/searchbox_buttons/bt_artist.png'
BUTTON_OPMUSIC_PATH = scriptfolder+'/images/searchbox_buttons/bt_music.png'
BUTTON_OPPLAYLIST_PATH = scriptfolder+'/images/searchbox_buttons/bt_playlist.png'

class SearchBox(BoxLayout):
    def __init__(self, **kwargs):
        super(SearchBox, self).__init__(**kwargs)
        self.drop_op = DropDown(auto_width=False)
        self.drop_op.width = dp(120)
        self.search_option = 'music'

        self.music_callback = None
        self.playlist_callback = None
        self.artist_callback = None
        
        self.txt_search = TextInput(text='Search Music Here', size_hint_y=None, height=dp(46), multiline=False)
        self.txt_search.padding = [15,15]
        self.txt_search.bind(on_text_validate=self.search, focus=self.txt_search_focus)
        self.add_widget(self.txt_search)

        self.bt_op = ImgButton(NOTEICON_PATH,
                               NOTEICON_PATH,
                               size_hint=(None, None), size=(dp(46),dp(46)))
        self.bt_op.bind(on_release=self.drop_op.open)
        self.add_widget(self.bt_op)

        self.bt_op_artist = ImgButton(BUTTON_OPARTIST_PATH, BUTTON_OPARTIST_PATH, 
                                      size_hint=(None,None), size=(dp(120),dp(46)))
        self.bt_op_artist.bind(on_release=self.bt_op_artist_click)
        self.drop_op.add_widget(self.bt_op_artist)
        
        self.bt_op_playlist = ImgButton(BUTTON_OPPLAYLIST_PATH, BUTTON_OPPLAYLIST_PATH, 
                                        size_hint=(None,None), size=(dp(120),dp(46)))
        self.bt_op_playlist.bind(on_release=self.bt_op_playlist_click)
        self.drop_op.add_widget(self.bt_op_playlist)
        
        self.bt_op_music = ImgButton(BUTTON_OPMUSIC_PATH, BUTTON_OPMUSIC_PATH, 
                                     size_hint=(None,None), size=(dp(120),dp(46)))
        self.bt_op_music.bind(on_release=self.bt_op_music_click)
        self.drop_op.add_widget(self.bt_op_music)
    
    def txt_search_focus(self, instance, value):
        if instance.text == 'Search Music Here': instance.text = ''
        elif instance.text == '': instance.text = 'Search Music Here'
        
    def bt_op_artist_click(self, instance):
        self.bt_op.source = ARTISTICON_PATH
        self.search_option = 'artist'
        self.drop_op.dismiss()
    
    def bt_op_playlist_click(self, instance):
        self.bt_op.source = PLAYLIST_ICON_PATH
        self.search_option = 'playlist'
        self.drop_op.dismiss()
    
    def bt_op_music_click(self, instance):
        self.bt_op.source = NOTEICON_PATH
        self.search_option = 'music'
        self.drop_op.dismiss()
    
    def search(self, instance):
        if self.search_option == 'music':
            self.videos = pyms.yts(self.txt_search.text)
            if self.music_callback: self.music_callback(self.videos)
        elif self.search_option == 'playlist':
            self.playlists = pyms.ytspl(self.txt_search.text)
            if self.playlist_callback: self.playlist_callback(self.playlists)
        elif self.search_option == 'artist':
            self.videos = pyms.ytsArtist(self.txt_search.text)
            if self.artist_callback: self.artist_callback(self.videos)
            

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
        
        self.bt_donwload_m4a = ImgButton(BUTTONDLM4A_PATH, BUTTONDLM4A_PATH,
                                         size_hint=(None,None), size=(dp(100),dp(46)))
        self.bt_donwload_m4a.bind(on_release=self.bt_download_m4a_click)
        self.drop_op.add_widget(self.bt_donwload_m4a)
        
        self.bt_donwload_ogg = ImgButton(BUTTONDLOGG_PATH, BUTTONDLOGG_PATH,
                                         size_hint=(None,None), size=(dp(100),dp(46)))    
        self.bt_donwload_ogg.border=(0, 0, 0, 0)
        self.bt_donwload_ogg.bind(on_release=self.bt_download_ogg_click)
        self.drop_op.add_widget(self.bt_donwload_ogg)
    
        self.bt_donwload_mp3 = ImgButton(BUTTONDLMP3_PATH, BUTTONDLMP3_PATH,
                                         size_hint=(None,None), size=(dp(100),dp(46)))
        self.bt_donwload_mp3.border=(0, 0, 0, 0)
        self.bt_donwload_mp3.bind(on_release=self.bt_download_mp3_click)
        self.drop_op.add_widget(self.bt_donwload_mp3)

        self.bt_addtoplaylist = ImgButton(BUTTONADD_PATH, BUTTONADD_PATH, 
                                          size_hint=(None,None), size=(dp(100),dp(46)))
        self.bt_addtoplaylist.bind(on_release=self.bt_addtoplaylist_click)
        self.bt_addtoplaylist.border=(0, 0, 0, 0)
        
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
                  
    def bt_download_m4a_click(self, instance):
         if self.download_callback: self.download_callback(self.title, self.url, 'm4a')
    
    def bt_download_ogg_click(self, instance):
         if self.download_callback: self.download_callback(self.title, self.url, 'ogg')
    
    def bt_download_mp3_click(self, instance):
         if self.download_callback: self.download_callback(self.title, self.url, 'mp3')
    
    def bt_addtoplaylist_click(self, instance):
         addTrackPopup(self).open()

class PlaylistWidget(ButtonBehavior, BoxLayout):
    def __init__(self, 
                 idx='0',
                 playlisttitle='Title of Video', 
                 playlisturl='http://url',
                 numtracks='0',
                 **kwargs):
                 
        super(PlaylistWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = 1, None
        self.height = dp(46)
        #self.size = (Window.width,self.height)
        self.spacing = 3
        
        self.titlelayout = BoxLayout(orientation='vertical')
        
        with self.canvas.before:
            Color(1,1,1,0)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.idx=idx
        self.title = playlisttitle
        self.url = playlisturl
        self.numtracks = numtracks
        
        self.label_idx = Label(text=str(self.idx), size_hint=(None,None), size=(dp(46),dp(46)))
        self.add_widget(self.label_idx)
        
        self.label_title = Label(text=self.title,size_hint=(1, 1))
        self.label_title.halign = 'left'
        self.label_title.valign = 'center'
        self.label_title.bind(size=self.label_title.setter('text_size'))
        self.label_title.shorten = True
        self.label_title.shorten_from = 'right'
        self.titlelayout.add_widget(self.label_title)
        
        self.label_numtracks = Label(text=self.numtracks+' Tracks')
        self.titlelayout.add_widget(self.label_numtracks)
        
        self.add_widget(self.titlelayout)
        
        self.drop_op = DropDown(auto_width=False)

        self.bt_save = ImgButton(BUTTON_SAVEPLAYLIST, BUTTON_SAVEPLAYLIST, 
                                 size_hint=(None,None), size=(dp(100),dp(46)))
        self.bt_save.bind(on_release=self.bt_save_click)
        self.bt_save.border=(0, 0, 0, 0)
        self.drop_op.add_widget(self.bt_save)

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
        self.ppl = pafy.get_playlist(self.url)
        self.videos = []
        for item in self.ppl['items']:
            self.videos.append({'title':item['pafy'].title, 'link':item['pafy'].videoid})
        __main__.app.main.music.MusicSreen._fromplaylist(self.videos)

        with self.canvas.before:
            Color(1, 1, 1, 0.0, mode='rgba')
            self.rect = Rectangle(pos=self.pos, size=self.size)
    
    def bt_save_click(self, instance):
        self.popup_AddPlaylistFromYT = AddPlaylistFromYTPopup()
        self.popup_AddPlaylistFromYT.txtbx_playlisttitle.text = self.title
        self.popup_AddPlaylistFromYT.txtbx_playlistlink.text = self.url
        self.popup_AddPlaylistFromYT.open()
