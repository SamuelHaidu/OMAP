from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.app import App
import pyms

class SearchBox(BoxLayout):
    def __init__(self, **kwargs):
        super(main, self).__init__(**kwargs)
        self.drop_op = DropDown(auto_width=False)
        self.drop_op.width = dp(120)
        self.search_option = 'music'

        self.music_callback = None
        self.playlist_callback = None
        self.artist_callback = None
        
        self.txt_search = TextInput(text='Search Music Here', size_hint_y=None, height=dp(46), multiline=False)
        self.txt_search.padding = [15,15]
        self.txt_search.bind(on_text_validate=self.search)
        self.add_widget(self.txt_search)

        self.bt_op = Button(text='M', size_hint=(None, None), size=(dp(46),dp(46)))
        self.bt_op.bind(on_release=self.drop_op.open)
        self.add_widget(self.bt_op)

        self.bt_op_artist = Button(text='Artist', size_hint=(None,None), size=(dp(120),dp(46)))
        self.bt_op_artist.bind(on_release=self.bt_op_artist_click)
        self.drop_op.add_widget(self.bt_op_artist)
        
        self.bt_op_playlist = Button(text='Playlists', size_hint=(None,None), size=(dp(120),dp(46)))
        self.bt_op_playlist.bind(on_release=self.bt_op_playlist_click)
        self.drop_op.add_widget(self.bt_op_playlist)
        
        self.bt_op_music = Button(text='Musics', size_hint=(None,None), size=(dp(120),dp(46)))
        self.bt_op_music.bind(on_release=self.bt_op_music_click)
        self.drop_op.add_widget(self.bt_op_music)
        
    def bt_op_artist_click(self, instance):
        self.bt_op.text='A'
        self.search_option = 'artist'
        self.drop_op.dismiss()
    
    def bt_op_playlist_click(self, instance):
        self.bt_op.text='P'
        self.search_option = 'playlist'
        self.drop_op.dismiss()
    
    def bt_op_music_click(self, instance):
        self.bt_op.text='M'
        self.search_option = 'music'
        self.drop_op.dismiss()
    
    def search(self, instance):
        if self.search_option == 'music':
            self.videos = pyms.yts(self.txt_search.text)
            if self.music_callback: self.callback(self.videos)
        elif self.search_option == 'playlist':
            self.playlists = pyms.ytpl(self.txt_search.text)
            if self.playlist_callback: self.callback(self.playlists)
        elif self.search_option == 'artist':
            self.videos = pyms.ytsArtist(self.txt_search.text)
            if self.artist_callback: self.callback(self.videos)
            
            